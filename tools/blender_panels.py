"""Panel layouts: blocking figures, stand-in props and a camera per panel, rendered from the built island.

  ~/.local/bin/blender -b blender/paxos.blend -P tools/blender_panels.py -- IV IV-03 IV-11 IV-06

Needs blender/paxos.blend from tools/blender_buildings.py (the full, deterministic scene build). Reads
volumes/<vol>-shots.json: for each panel, the camera (loc, target, lens, clip_start), aspect and resolution, the objects to
hide, and the blocking figures and stand-in props, all in Blender world coordinates. A z of "surface" (or "surface+1.6"
for a camera) stands on whatever is below the optional z_from height (default: from the sky); the resolved heights and each figure's position in the frame are written
back to the JSON, so a re-render reproduces the same frame.

Blocking lives in one collection per panel under "Panels", hidden from renders and viewports; only the panel being
rendered is shown, and blender/panels-<vol>.blend is saved with every blocking collection hidden again (checked by
reopening). Cameras sit in "Panel cameras", which renders nothing.

Outputs in renders/panels/: <id>-render.png (the lit colour render), and <id>-layout.png, the colour render with ink
outlines, found from quick normal and depth passes (Freestyle over the whole island was too slow to finish).
"""
import json, math, sys
from pathlib import Path
import bpy
import numpy as np
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blender_terrain as bt
from blender_kit import Kit, mat, TAU                                                              # noqa: F401
import blender_round as br
import blender_props as bp

OUT = bt.ROOT / "renders" / "panels"
INK = np.array([28, 21, 18]) / 255

# ---------------------------------------------------------------- stand-in props (true scale, crude)
def scroll_closed(k, x, y, z, ang, m, knob):
    """Two rolls side by side on their rods, lying on a surface; the axis runs along `ang`."""
    c, s = math.cos(ang), math.sin(ang)
    for sd in (-1, 1):
        cx, cy = x - s * .05 * sd, y + c * .05 * sd
        bp.wheel(k, cx, cy, z + .045, ang, .045, .30, m, 10)
        for e in (-1, 1): bp.wheel(k, cx + c * .17 * e, cy + s * .17 * e, z + .045, ang, .018, .06, knob, 6)

def scroll_carried(k, x, y, z, facing, m, knob):
    """A closed ledger tucked under the arm: upright rolls at the figure's side."""
    sx, sy = x - math.sin(facing) * .27, y + math.cos(facing) * .27
    for sd in (-1, 1):
        k.cyl(sx + math.cos(facing) * .05 * sd, sy + math.sin(facing) * .05 * sd, .04, z + .95, z + 1.3, m, 8)
        k.cyl(sx + math.cos(facing) * .05 * sd, sy + math.sin(facing) * .05 * sd, .015, z + 1.3, z + 1.36, knob, 6)

def hourglass(k, x, y, z, m, frame):
    k.cyl(x, y, .07, z, z + .02, frame, 10); k.cyl(x, y, .07, z + .26, z + .28, frame, 10)
    k.frustum(x, y, .055, .008, z + .02, z + .14, m, 10); k.frustum(x, y, .008, .055, z + .14, z + .26, m, 10)
    for i in range(3):
        a = i * TAU / 3; k.cyl(x + .06 * math.cos(a), y + .06 * math.sin(a), .008, z + .02, z + .26, frame, 5)

def ink_pot(k, x, y, z, m): k.cyl(x, y, .035, z, z + .06, m, 10)
def pen(k, x, y, z, ang, m): k.beam((x - .09 * math.cos(ang), y - .09 * math.sin(ang), z + .01), (x + .09 * math.cos(ang), y + .09 * math.sin(ang), z + .01), .01, .01, m)
def slip(k, x, y, z, ang, m): k.beam((x, y, z), (x + .12 * math.cos(ang), y + .12 * math.sin(ang), z + .07), .14, .004, m)

# ---------------------------------------------------------------- scene helpers
def collection(name, parent):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in parent.children: parent.children.link(c)
    return c

def surface(scene, x, y, below=3000.0, skip=()):
    dg = bpy.context.evaluated_depsgraph_get(); origin = Vector((x, y, below))
    for _ in range(8):
        hit, loc, _, _, ob, _ = scene.ray_cast(dg, origin, Vector((0, 0, -1)))
        if not hit: return None
        if ob is None or ob.name not in skip: return loc.z
        origin = loc - Vector((0, 0, .01))
    return None

def emission_material(name, build):
    m = bpy.data.materials.get(name)
    if m: return m
    m = bpy.data.materials.new(name); m.use_nodes = True; N, L = m.node_tree.nodes, m.node_tree.links
    for n in list(N): N.remove(n)
    out = N.new("ShaderNodeOutputMaterial"); em = N.new("ShaderNodeEmission")
    L.new(em.outputs[0], out.inputs["Surface"]); build(N, L, em.inputs["Color"])
    return m

def normal_material():
    def build(N, L, color):
        geo = N.new("ShaderNodeNewGeometry"); sc = N.new("ShaderNodeVectorMath"); sc.operation = "SCALE"; sc.inputs["Scale"].default_value = .5
        add = N.new("ShaderNodeVectorMath"); add.operation = "ADD"; add.inputs[1].default_value = (.5, .5, .5)
        L.new(geo.outputs["Normal"], sc.inputs[0]); L.new(sc.outputs[0], add.inputs[0]); L.new(add.outputs[0], color)
    return emission_material("Panel pass · normal", build)

FAR = 6000.0
def depth_material():
    def build(N, L, color):
        cam = N.new("ShaderNodeCameraData"); a = N.new("ShaderNodeMath"); a.operation = "ADD"; a.inputs[1].default_value = 1.0
        lg = N.new("ShaderNodeMath"); lg.operation = "LOGARITHM"; lg.inputs[1].default_value = math.e
        dv = N.new("ShaderNodeMath"); dv.operation = "DIVIDE"; dv.inputs[1].default_value = math.log(FAR + 1)
        L.new(cam.outputs["View Distance"], a.inputs[0]); L.new(a.outputs[0], lg.inputs[0]); L.new(lg.outputs[0], dv.inputs[0]); L.new(dv.outputs[0], color)
    return emission_material("Panel pass · depth", build)

def load_pixels(path):
    img = bpy.data.images.load(str(path)); w, h = img.size
    buf = np.empty(w * h * 4, np.float32); img.pixels.foreach_get(buf); bpy.data.images.remove(img)
    return buf.reshape(h, w, 4)

def save_pixels(arr, path):
    h, w = arr.shape[:2]; img = bpy.data.images.new(path.stem, w, h, alpha=True)
    img.pixels.foreach_set(arr.astype(np.float32).ravel()); img.filepath_raw = str(path); img.file_format = "PNG"; img.save()
    bpy.data.images.remove(img)

def outlines(color, normal, depth):
    """Ink where the surface normal turns by more than ~35 degrees or the depth jumps by more than ~4%, one pixel thick, then thickened by one."""
    n = normal[..., :3] * 2 - 1; d = depth[..., 0]
    edge = np.zeros(d.shape, bool)
    for ax in (0, 1):
        dot = (n * np.roll(n, -1, ax)).sum(-1)
        edge |= dot < math.cos(math.radians(35))
        edge |= np.abs(d - np.roll(d, -1, ax)) > math.log(1.04) / math.log(FAR + 1)
    edge[-1, :] = edge[:, -1] = False
    thick = edge | np.roll(edge, 1, 0) | np.roll(edge, 1, 1)
    out = color.copy(); out[..., :3] = np.where(thick[..., None], INK, color[..., :3]); out[..., 3] = 1
    return out, float(thick.mean())

# ---------------------------------------------------------------- one panel
def build_panel(scene, pid, spec, colors, top, cams):
    coll = collection(f"{pid} · blocking", top); coll.hide_render = coll.hide_viewport = True
    for ob in list(coll.objects): bpy.data.objects.remove(ob, do_unlink=True)
    mats = {k_: mat(f"Blocking · {k_}", h, .9) for k_, h in colors.items()}
    wood, parchment, glass, ink = mat("Blocking · rod", "#6a4a2e"), mat("Blocking · parchment", "#efe3c2"), mat("Blocking · glass", "#bcd8d4", .2), mat("Blocking · ink", "#1c1512")
    k = Kit(f"{pid} · blocking figures and props")
    for f in spec["figures"]:
        x, y = f["xy"]
        z = surface(scene, x, y, below=f.get("z_from", 3000.0)) if f["z"] == "surface" else f["z"]
        f["z_resolved"] = round(z, 3)
        face = math.radians(f["facing_deg"]); m = mats[f["color"]]
        br.figure(k, x, y, z, face, f.get("pose", "stand"), m, m, m)
        if f.get("carry") == "scroll": scroll_carried(k, x, y, z, face, parchment, wood)
    for p in spec["props"]:
        x, y = p["xy"]; z = p["z"]; a = math.radians(p.get("angle_deg", 0))
        {"scroll_closed": lambda: scroll_closed(k, x, y, z, a, parchment, wood), "hourglass": lambda: hourglass(k, x, y, z, glass, wood),
         "ink_pot": lambda: ink_pot(k, x, y, z, ink), "pen": lambda: pen(k, x, y, z, a, wood), "slip": lambda: slip(k, x, y, z, a, parchment)}[p["kind"]]()
    ob = k.finish(coll)
    c = spec["camera"]; lx, ly, lz = c["loc"]
    if isinstance(lz, str):                                                                         # "surface+1.6"
        lz = surface(scene, lx, ly, below=c.get("z_from", 3000.0), skip={ob.name}) + float(lz.split("+")[1]); c["z_resolved"] = round(lz, 3)
    old = bpy.data.objects.get(f"Cam · panel {pid}")
    if old:
        tgt = bpy.data.objects.get(old.name + " target"); bpy.data.objects.remove(old, do_unlink=True)
        if tgt: bpy.data.objects.remove(tgt, do_unlink=True)
    cam = bt.camera(f"Cam · panel {pid}", (lx, ly, lz), tuple(c["target"]), cams, lens=c["lens"])
    cam.data.clip_start = c.get("clip_start", .1)
    return coll, cam

def render_panel(scene, pid, spec, coll, cam):
    OUT.mkdir(parents=True, exist_ok=True)
    hidden = [o for o in (bpy.data.objects.get(n) for n in spec.get("hide", [])) if o]
    for o in hidden: o.hide_render = True
    coll.hide_render = coll.hide_viewport = False
    scene.camera = cam; scene.render.resolution_x, scene.render.resolution_y = spec["resolution"]
    scene.render.image_settings.file_format = "PNG"; scene.render.image_settings.color_depth = "8"                 # 8-bit loads as display-space bytes
    bpy.context.view_layer.update()
    for f in spec["figures"]:                                                                       # where each figure's head lands in the frame
        v = world_to_camera_view(scene, cam, Vector((f["xy"][0], f["xy"][1], f["z_resolved"] + 1.6)))
        f["screen"] = [round(v.x, 3), round(1 - v.y, 3)]; f["in_frame"] = bool(0 <= v.x <= 1 and 0 <= v.y <= 1 and v.z > 0)
    dg = bpy.context.evaluated_depsgraph_get(); eye = cam.matrix_world.translation
    blocking = {o.name for o in coll.objects}
    def seen(pt, pad=.35):
        d = Vector(pt) - eye; L = d.length
        hit, loc, _, _, ob, _ = scene.ray_cast(dg, eye, d.normalized(), distance=L)
        return (not hit) or (ob is not None and ob.name in blocking) or (loc - eye).length >= L - pad
    for f in spec["figures"]:
        f["visible"] = bool(seen((f["xy"][0], f["xy"][1], f["z_resolved"] + 1.45)))
    frame = cam.data.view_frame(scene=scene); m_ = cam.matrix_world
    near = []
    for u, v in ((.5, .5), (.1, .1), (.9, .1), (.1, .9), (.9, .9)):
        pt = m_ @ (frame[2] + (frame[1] - frame[2]) * u + (frame[3] - frame[2]) * v)
        hit, loc, _, _, ob, _ = scene.ray_cast(dg, eye, (pt - eye).normalized(), distance=spec["camera"].get("clear_m", 1.0))
        near.append(bool(hit) and not (ob is not None and ob.name in blocking))
    spec["lens_clear"] = not any(near)
    hit, loc, *_ = scene.ray_cast(dg, eye, (m_ @ (frame[2] + (frame[1] - frame[2]) * .5 + (frame[3] - frame[2]) * .5) - eye).normalized())
    spec["centre_clear_m"] = round((loc - eye).length, 1) if hit else None                          # nothing big right in front of the lens
    for p in spec["props"]:
        v = world_to_camera_view(scene, cam, Vector((p["xy"][0], p["xy"][1], p["z"] + .05)))
        p["screen"] = [round(v.x, 3), round(1 - v.y, 3)]; p["in_frame"] = bool(0 <= v.x <= 1 and 0 <= v.y <= 1 and v.z > 0)
    paths = {k_: OUT / f"{pid}-{k_}.png" for k_ in ("render", "normal", "depth")}
    bt.use_eevee(scene); scene.render.filepath = str(paths["render"]); bpy.ops.render.render(write_still=True)
    world = scene.world; bg = world.node_tree.nodes["Background"].inputs["Strength"]; strength = bg.default_value
    vt, look = scene.view_settings.view_transform, scene.view_settings.look
    bg.default_value = 0.0; scene.view_settings.view_transform = "Standard"
    scene.render.image_settings.color_depth = "16"                                                  # passes: precision for depth (loaded as linear floats, as written)
    for key, m in (("normal", normal_material()), ("depth", depth_material())):
        bpy.context.view_layer.material_override = m
        scene.render.filepath = str(paths[key]); bpy.ops.render.render(write_still=True)
    bpy.context.view_layer.material_override = None
    bg.default_value = strength; scene.view_settings.view_transform = vt; scene.view_settings.look = look
    layout, ink_share = outlines(load_pixels(paths["render"]), load_pixels(paths["normal"]), load_pixels(paths["depth"]))
    save_pixels(layout, OUT / f"{pid}-layout.png")
    for p_ in (paths["normal"], paths["depth"]): p_.unlink()
    coll.hide_render = coll.hide_viewport = True
    for o in hidden: o.hide_render = False
    spec["ink_share"] = round(ink_share, 3)
    return OUT / f"{pid}-layout.png"

def main():
    args = sys.argv[sys.argv.index("--") + 1:]
    vol, ids = args[0], args[1:]
    path = bt.ROOT / "volumes" / f"{vol}-shots.json"; shots = json.loads(path.read_text())
    scene = bpy.context.scene
    top = collection("Panels", scene.collection); cams = collection("Panel cameras", scene.collection)
    for pid in ids or list(shots["panels"]):
        spec = shots["panels"][pid]
        coll, cam = build_panel(scene, pid, spec, shots["colors"], top, cams)
        out = render_panel(scene, pid, spec, coll, cam)
        print("PANEL", pid, out, "lens clear:", spec["lens_clear"], "centre clear to", spec["centre_clear_m"], "m;", "figures in frame:", sum(f["in_frame"] for f in spec["figures"]), "/", len(spec["figures"]),
              "visible:", sum(f["visible"] for f in spec["figures"]),
              "props in frame:", sum(p["in_frame"] for p in spec["props"]), "/", len(spec["props"]), "ink", spec["ink_share"])
    path.write_text(json.dumps(shots, ensure_ascii=False, indent=1))
    blend = bt.OUT / f"panels-{vol}.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend), compress=True)
    bpy.ops.wm.open_mainfile(filepath=str(blend))                                                   # check the saved file keeps every blocking collection hidden
    shown = [c.name for c in bpy.data.collections.get("Panels").children if not (c.hide_render and c.hide_viewport)]
    print("SAVED", blend, "blocking collections hidden:", not shown, shown)

if __name__ == "__main__":
    main()
