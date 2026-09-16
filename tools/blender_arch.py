"""Architectural components at human scale, shared by the hero buildings: Doric columns, wall openings, a Doric
temple sized from its column diameter, crenellated walls and towers, and a portcullis.

Proportions follow Hellenistic practice closely enough for pre-vis: Doric columns 5.5 lower diameters high,
2.4 diameters centre to centre, three-step bases with risers of 0.4 m or less, and entablatures about 1.8
diameters deep. Every builder returns the numbers the checks need.
"""
import math
from blender_kit import *                                                                          # noqa: F401,F403

FIGURE = 1.75

def dark():
    return mat("Opening (dark)", "#2a2320", .95)

def column(k, X, Y, z0, z1, r, m):
    """Doric column: tapered fluted-looking shaft (16 sides), echinus, abacus. No base."""
    h = z1 - z0
    k.frustum(X, Y, r, r * .78, z0, z1 - h * .09, m, 16)
    k.frustum(X, Y, r * .8, r * 1.18, z1 - h * .09, z1 - h * .045, m, 16)
    k.box(X, Y, z1 - h * .045, z1, 2.5 * r, 2.5 * r, 0, m)

def opening(k, X, Y, ang, sx, sy, face, along, w, z0, z1, m=None):
    """A dark doorway or window on one face of a box built with Kit.box(X, Y, .., sx, sy, ang).
    face: '+x', '-x', '+y' or '-y'; `along` offsets it along that face."""
    m = m or dark(); c, s = math.cos(ang), math.sin(ang)
    if face in ("+x", "-x"):
        sg = 1 if face == "+x" else -1
        cx, cy = X + c * sg * (sx / 2 + .03) - s * along, Y + s * sg * (sx / 2 + .03) + c * along
        k.box(cx, cy, z0, z1, .08, w, ang, m)
    else:
        sg = 1 if face == "+y" else -1
        cx, cy = X - s * sg * (sy / 2 + .03) + c * along, Y + c * sg * (sy / 2 + .03) + s * along
        k.box(cx, cy, z0, z1, w, .08, ang, m)

def temple(k, M, ground, X, Y, ang, n_front, d, n_side=None, cella_door=True):
    """Doric peripteral temple facing local +x (ang). Returns its measurements."""
    col_h, axial = 5.5 * d, 2.4 * d
    n_side = n_side or (2 * n_front + 1)
    L, W = axial * (n_side - 1), axial * (n_front - 1)                                             # column-centre rectangle
    sx, sy = L + 1.8 * d, W + 1.8 * d                                                              # stylobate
    lo, hi = on_ground(ground, X, Y, sx + 2.4, sy + 2.4, ang, 1.0)
    riser, tread = min(.4, max(.25, .36 * d)), .45
    for i in range(3):
        grow = 2 * tread * (2 - i)
        k.box(X, Y, lo if i == 0 else hi + i * riser - .02, hi + (i + 1) * riser, sx + grow, sy + grow, ang, M["limestone"])
    z = hi + 3 * riser
    c, s = math.cos(ang), math.sin(ang); P = lambda u, v: (X + u * c - v * s, Y + u * s + v * c)
    pts = {(round(u, 3), round(v, 3)) for u in (-L / 2, L / 2) for v in [W * (j / (n_front - 1) - .5) for j in range(n_front)]} | \
          {(round(u, 3), round(v, 3)) for v in (-W / 2, W / 2) for u in [L * (j / (n_side - 1) - .5) for j in range(n_side)]}
    for u, v in pts: column(k, *P(u, v), z, z + col_h, d / 2, M["marble"])
    top = z + col_h
    k.box(X, Y, top, top + .75 * d, L + 1.3 * d, W + 1.3 * d, ang, M["marble"])                    # architrave
    k.box(X, Y, top + .75 * d, top + 1.5 * d, L + 1.3 * d, W + 1.3 * d, ang, M["marble"])           # frieze
    for sg in (-1, 1):                                                                             # triglyphs across both fronts
        for j in range(2 * n_front - 1):
            v = W * (j / (2 * n_front - 2) - .5)
            tx, ty = P(sg * (L / 2 + .65 * d + .04), v)
            k.box(tx, ty, top + .8 * d, top + 1.45 * d, .1, .5 * d, ang, mat("Triglyph", "#9c9482"))
    k.box(X, Y, top + 1.5 * d, top + 1.8 * d, L + 1.9 * d, W + 1.9 * d, ang, M["marble"])           # cornice
    rise = (W + 1.9 * d) * .14
    k.gable(X, Y, top + 1.8 * d, L + 1.9 * d, W + 1.9 * d, rise, ang, M["marble"])                  # pediments
    k.gable(X, Y, top + 1.8 * d + .06, L + 1.5 * d, W + 2.1 * d, rise, ang, M["roof"])              # tiled roof, set in from the pediments
    for sg in (-1, 1): k.box(*P(sg * (L / 2 + .95 * d), 0), top + 1.8 * d + rise, top + 1.8 * d + rise + .8 * d, .4 * d, .9 * d, ang, M["marble"])   # acroteria
    cl, cw = L - 2 * axial, W - 1.1 * axial
    if cl > 2 and cw > 2:
        k.box(X, Y, z, top, cl, cw, ang, M["limestone"])
        if cella_door: opening(k, X, Y, ang, cl, cw, "+x", 0, min(3.0, cw * .4), z, z + min(col_h * .75, 5.5))
    return {"column_h_over_d": round(col_h / d, 2), "axial_over_d": round(axial / d, 2), "step_riser_m": round(riser, 2),
            "door_h_m": round(min(col_h * .75, 5.5), 2), "floor_z": z, "front": (P(L / 2 + 1.5 * d, 0)), "length_m": round(sx, 1), "width_m": round(sy, 1)}

def crenellate(k, x0, y0, x1, y1, z_top, outward, offset, m, merlon=(1.0, 2.0), crenel=1.0, parapet=.6):
    """Merlons along a wall top from (x0, y0) to (x1, y1), set `offset` metres toward the outward unit normal."""
    L = math.hypot(x1 - x0, y1 - y0); ang = math.atan2(y1 - y0, x1 - x0)
    n = max(1, math.ceil(L / (merlon[0] + crenel)))                                               # round up, so gaps never exceed `crenel`
    for i in range(n):
        f = (i + .5) / n
        k.box(x0 + (x1 - x0) * f + outward[0] * offset, y0 + (y1 - y0) * f + outward[1] * offset, z_top, z_top + merlon[1], merlon[0], parapet, ang, m)
    return {"merlon_h_m": merlon[1], "crenel_w_m": round(L / n - merlon[0], 2)}

def crenellate_box(k, X, Y, sx, sy, ang, z_top, m):
    """Merlons round the top of a square tower."""
    c, s = math.cos(ang), math.sin(ang); P = lambda u, v: (X + u * c - v * s, Y + u * s + v * c)
    corners = [(-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)]
    for i in range(4):
        (u0, v0), (u1, v1) = corners[i], corners[(i + 1) % 4]
        mu, mv = (u0 + u1) / 2, (v0 + v1) / 2; n = math.hypot(mu, mv) or 1
        ox, oy = (mu * c - mv * s) / n, (mu * s + mv * c) / n
        crenellate(k, *P(u0, v0), *P(u1, v1), z_top, (ox, oy), -.3, m)

def crenellate_ring(k, X, Y, r, z_top, m, merlon=(1.0, 2.0), crenel=1.0, parapet=.6):
    n = max(4, int(math.tau * r // (merlon[0] + crenel)))
    for i in range(n):
        a = i * math.tau / n
        k.box(X + (r - parapet / 2) * math.cos(a), Y + (r - parapet / 2) * math.sin(a), z_top, z_top + merlon[1], parapet, merlon[0], a, m)

def portcullis(k, X, Y, ang, width, z0, height, m):
    c, s = math.cos(ang), math.sin(ang)
    for j in range(int(width / .45) + 1):
        v = -width / 2 + j * .45
        k.box(X - s * v, Y + c * v, z0, z0 + height, .12, .1, ang, m)
    for zz in (z0 + height * .25, z0 + height * .6, z0 + height * .95):
        k.box(X, Y, zz, zz + .12, .14, width, ang, m)
