"""Shared Blender helpers for the scene builders: map <-> Blender coordinates, a ground sampler that can level
the terrain mesh, a small mesh kit (boxes, rings, cylinders, cones, gable roofs), materials, and a few
architectural pieces (houses on foundations, colonnades)."""
import json, math, random, sys
from pathlib import Path
import bpy, bmesh
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blender_terrain as bt

TAU = math.tau
SITES = json.loads(bt.SITES.read_text())

def B(x, y):
    """Map metres (x east, y south) -> Blender (X east, Y north)."""
    return x - bt.W / 2, bt.H / 2 - y

def site(key, k=0):
    x, y, z = SITES["sites"][key]["points_m"][k]
    return B(x, y)

def smooth(t):
    t = np.clip(t, 0, 1); return t * t * (3 - 2 * t)

# ---------------------------------------------------------------- ground: sample and level the terrain mesh
class Ground:
    def __init__(self, terrain):
        self.me = terrain.data
        self.co = np.empty(len(self.me.vertices) * 3, np.float32)
        self.me.vertices.foreach_get("co", self.co)
        ny, nx = bt.heights().shape
        self.g = self.co.reshape(ny, nx, 3)[..., 2]
        self.orig = self.g.copy()
        self.ny, self.nx = ny, nx

    def _cr(self, X, Y):
        return (X + bt.W / 2) / bt.CELL - .5, (bt.H / 2 - Y) / bt.CELL - .5

    def z(self, X, Y, before=False):
        g = self.orig if before else self.g
        c, r = self._cr(X, Y)
        c0, r0 = int(np.clip(math.floor(c), 0, self.nx - 2)), int(np.clip(math.floor(r), 0, self.ny - 2))
        fc, fr = min(max(c - c0, 0), 1), min(max(r - r0, 0), 1)
        return float(g[r0, c0] * (1 - fc) * (1 - fr) + g[r0, c0 + 1] * fc * (1 - fr) + g[r0 + 1, c0] * (1 - fc) * fr + g[r0 + 1, c0 + 1] * fc * fr)

    def edit(self, X, Y, reach, fn):
        """fn(d, dX, dY, g) -> new g for the vertices within `reach` metres of (X, Y)."""
        c, r = self._cr(X, Y); k = int(reach / bt.CELL) + 2
        r0, r1 = max(int(r) - k, 0), min(int(r) + k + 1, self.ny)
        c0, c1 = max(int(c) - k, 0), min(int(c) + k + 1, self.nx)
        rows, cols = np.mgrid[r0:r1, c0:c1]
        dX = (cols + .5) * bt.CELL - bt.W / 2 - X
        dY = bt.H / 2 - (rows + .5) * bt.CELL - Y
        self.g[r0:r1, c0:c1] = fn(np.hypot(dX, dY), dX, dY, self.g[r0:r1, c0:c1])

    def pad(self, X, Y, radius, level, falloff):
        w = lambda d: 1 - smooth((d - radius) / falloff)
        self.edit(X, Y, radius + falloff, lambda d, dX, dY, g: g * (1 - w(d)) + level * w(d))

    def relief(self, X, Y, radius):
        zs = [self.z(X + radius * f * math.cos(a), Y + radius * f * math.sin(a), before=True)
              for f in (0, .5, 1) for a in np.linspace(0, TAU, 12, endpoint=False)]
        return round(max(zs) - min(zs), 1), round(min(zs), 1)

    def seaward(self, X, Y, radius=150):
        v = np.zeros(2)
        for a in np.linspace(0, TAU, 72, endpoint=False):
            if self.z(X + radius * math.cos(a), Y + radius * math.sin(a)) < 0: v += (math.cos(a), math.sin(a))
        n = np.hypot(*v)
        return (v / n) if n else np.array([1.0, 0.0])

    def shore(self, X, Y, s, reach=600):
        for d in np.arange(0, reach, 2.5):
            if self.z(X + s[0] * d, Y + s[1] * d) < 0: return X + s[0] * d, Y + s[1] * d
        return X, Y

    def commit(self):
        self.me.vertices.foreach_set("co", self.co)
        self.me.update()

# ---------------------------------------------------------------- materials and a mesh kit
MATS = {}
def mat(name, hexc, rough=.85, metal=0.0, emit=None):
    if name in MATS: return MATS[name]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = bt.hexrgb(hexc)
    b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = bt.hexrgb(emit); b.inputs["Emission Strength"].default_value = 25
    MATS[name] = m
    return m

def palette():
    return {"limestone": mat("Limestone", "#d8ccb0"), "ashlar": mat("Ashlar", "#c6b793"), "marble": mat("Marble", "#eeeae0", .5),
            "sand": mat("Orchestra sand", "#d9c38e"), "roof": mat("Terracotta roof", "#b0532f"), "plaster": mat("Plaster", "#e4d8c1"),
            "bronze": mat("Bronze", "#8a6428", .35, .85), "timber": mat("Timber", "#6a4a2e"), "garden": mat("Garden", "#6d7b38"),
            "pave": mat("Paving", "#cdc0a2"), "canvas": mat("Tent canvas", "#d8d0b8"), "lantern": mat("Lantern", "#ffd27a", .4, 0, "#ffc861"),
            "wall_dark": mat("Fortress stone", "#a89c84")}

class Kit:
    """Accumulates boxes, rings, cylinders and roofs into one mesh object with material slots."""
    def __init__(self, name):
        self.name, self.bm, self.slots = name, bmesh.new(), []

    def _mi(self, m):
        if m not in self.slots: self.slots.append(m)
        return self.slots.index(m)

    def _face(self, vs, m):
        f = self.bm.faces.new(vs); f.material_index = self._mi(m)

    def box(self, X, Y, z0, z1, sx, sy, ang, m):
        c, s = math.cos(ang), math.sin(ang)
        pts = [(X + u * c - v * s, Y + u * s + v * c) for u, v in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2))]
        b = [self.bm.verts.new((x, y, z0)) for x, y in pts]; t = [self.bm.verts.new((x, y, z1)) for x, y in pts]
        self._face(b[::-1], m); self._face(t, m)
        for i in range(4): self._face([b[i], b[(i + 1) % 4], t[(i + 1) % 4], t[i]], m)

    def ring(self, X, Y, r_in, r_out, z0, z1, m, segs=64, a0=0.0, a1=TAU):
        full = a1 - a0 >= TAU - 1e-6
        n = segs if full else max(2, int(segs * (a1 - a0) / TAU) + 1)
        angs = np.linspace(a0, a1, n, endpoint=not full)
        P = lambda r, a, z: self.bm.verts.new((X + r * math.cos(a), Y + r * math.sin(a), z))
        ib = [P(r_in, a, z0) for a in angs]; ob = [P(r_out, a, z0) for a in angs]
        it = [P(r_in, a, z1) for a in angs]; ot = [P(r_out, a, z1) for a in angs]
        for k in range(n if full else n - 1):
            k2 = (k + 1) % n
            self._face([it[k], ot[k], ot[k2], it[k2]], m); self._face([ib[k], ib[k2], ob[k2], ob[k]], m)
            self._face([ob[k], ob[k2], ot[k2], ot[k]], m); self._face([ib[k], it[k], it[k2], ib[k2]], m)
        if not full:
            self._face([ib[0], ob[0], ot[0], it[0]], m); self._face([ib[-1], it[-1], ot[-1], ob[-1]], m)

    def cyl(self, X, Y, r, z0, z1, m, segs=20):
        angs = np.linspace(0, TAU, segs, endpoint=False)
        b = [self.bm.verts.new((X + r * math.cos(a), Y + r * math.sin(a), z0)) for a in angs]
        t = [self.bm.verts.new((X + r * math.cos(a), Y + r * math.sin(a), z1)) for a in angs]
        self._face(b[::-1], m); self._face(t, m)
        for i in range(segs): self._face([b[i], b[(i + 1) % segs], t[(i + 1) % segs], t[i]], m)

    def cone(self, X, Y, r, z0, z1, m, segs=20):
        angs = np.linspace(0, TAU, segs, endpoint=False)
        b = [self.bm.verts.new((X + r * math.cos(a), Y + r * math.sin(a), z0)) for a in angs]
        apex = self.bm.verts.new((X, Y, z1))
        self._face(b[::-1], m)
        for i in range(segs): self._face([b[i], b[(i + 1) % segs], apex], m)

    def gable(self, X, Y, z, sx, sy, rise, ang, m):
        """Pitched roof, ridge along the local x axis."""
        c, s = math.cos(ang), math.sin(ang)
        L = lambda u, v, zz: self.bm.verts.new((X + u * c - v * s, Y + u * s + v * c, zz))
        a, b_, c_, d = L(-sx / 2, -sy / 2, z), L(sx / 2, -sy / 2, z), L(sx / 2, sy / 2, z), L(-sx / 2, sy / 2, z)
        r0, r1 = L(-sx / 2, 0, z + rise), L(sx / 2, 0, z + rise)
        self._face([d, c_, b_, a], m); self._face([a, b_, r1, r0], m); self._face([c_, d, r0, r1], m)
        self._face([b_, c_, r1], m); self._face([d, a, r0], m)

    def frustum(self, X, Y, r0, r1, z0, z1, m, segs=12):
        angs = np.linspace(0, TAU, segs, endpoint=False)
        b = [self.bm.verts.new((X + r0 * math.cos(a), Y + r0 * math.sin(a), z0)) for a in angs]
        t = [self.bm.verts.new((X + r1 * math.cos(a), Y + r1 * math.sin(a), z1)) for a in angs]
        self._face(b[::-1], m); self._face(t, m)
        for i in range(segs): self._face([b[i], b[(i + 1) % segs], t[(i + 1) % segs], t[i]], m)

    def ellipsoid(self, X, Y, Z, rx, ry, rz, m, subdiv=1):
        from mathutils import Matrix
        res = bmesh.ops.create_icosphere(self.bm, subdivisions=subdiv, radius=1.0,
                                         matrix=Matrix.Translation((X, Y, Z)) @ Matrix.Diagonal((rx, ry, rz, 1.0)))
        for f in {f for v in res["verts"] for f in v.link_faces}: f.material_index = self._mi(m)

    def beam(self, p0, p1, w, d, m):
        """A box from point p0 to point p1 (any direction) with a w x d cross-section."""
        from mathutils import Vector
        a, b = Vector(p0), Vector(p1); ax = b - a
        if ax.length < 1e-6: return
        ax.normalize(); ref = Vector((0, 0, 1)) if abs(ax.z) < .9 else Vector((1, 0, 0))
        u = ax.cross(ref).normalized() * (w / 2); v = ax.cross(u).normalized() * (d / 2)
        c0 = [a + su * u + sv * v for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        vs0 = [self.bm.verts.new(p) for p in c0]; vs1 = [self.bm.verts.new(p + (b - a)) for p in c0]
        self._face(vs0[::-1], m); self._face(vs1, m)
        for i in range(4): self._face([vs0[i], vs0[(i + 1) % 4], vs1[(i + 1) % 4], vs1[i]], m)

    def finish(self, coll, **props):
        bmesh.ops.recalc_face_normals(self.bm, faces=self.bm.faces[:])
        me = bpy.data.meshes.new(self.name); self.bm.to_mesh(me); self.bm.free()
        for m in self.slots: me.materials.append(m)
        ob = bpy.data.objects.new(self.name, me); coll.objects.link(ob)
        for k, v in props.items(): ob[k] = v
        return ob

def on_ground(ground, X, Y, sx, sy, ang, extra=0.0):
    """Lowest and highest ground under a rotated footprint."""
    c, s = math.cos(ang), math.sin(ang)
    zs = [ground.z(X + u * c - v * s, Y + u * s + v * c) for u in (-sx / 2, 0, sx / 2) for v in (-sy / 2, 0, sy / 2)]
    return min(zs) - extra, max(zs)

def house(kit, ground, X, Y, sx, sy, h, ang, wall, roof, rise=None):
    lo, hi = on_ground(ground, X, Y, sx, sy, ang, 1.5)
    kit.box(X, Y, lo, hi + h, sx, sy, ang, wall)
    kit.gable(X, Y, hi + h, sx + .8, sy + .8, rise if rise is not None else min(sx, sy) * .22, ang, roof)

def colonnade(kit, X, Y, z0, z1, sx, sy, ang, spacing, m, r=.35):
    c, s = math.cos(ang), math.sin(ang)
    nu, nv = max(1, round(sx / spacing)), max(1, round(sy / spacing))
    pts = {(round(u, 2), round(-sy / 2, 2)) for u in np.linspace(-sx / 2, sx / 2, nu + 1)} | {(round(u, 2), round(sy / 2, 2)) for u in np.linspace(-sx / 2, sx / 2, nu + 1)} \
        | {(round(-sx / 2, 2), round(v, 2)) for v in np.linspace(-sy / 2, sy / 2, nv + 1)} | {(round(sx / 2, 2), round(v, 2)) for v in np.linspace(-sy / 2, sy / 2, nv + 1)}
    for u, v in pts: kit.cyl(X + u * c - v * s, Y + u * s + v * c, r, z0, z1, m, 10)

