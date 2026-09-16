"""Stage 3b: the key buildings, placed on the terrain.

  ~/.local/bin/blender -b -P tools/blender_buildings.py              build terrain + buildings, save blender/paxos.blend
  ~/.local/bin/blender -b -P tools/blender_buildings.py -- --render  also render renders/buildings-*.png

Starts from a fresh terrain scene (blender_terrain.build), levels the ground where a building needs it
(pads are edits to the Blender mesh only; the heightmap stays the spec), then builds pre-vis models at true
scale from the site list, the town layout and the canon: the Great Round and the banquet house (IV), the
lantern harbour (III), the merchant quays and harbour town (IV), the besieged headland city and its siege
camps (V), and the citadel with its walled harbour (VII). Checks go to blender/buildings-checks.json and
the page between <!-- BUILDINGS --> markers.
"""
import json, math, random, sys
from pathlib import Path
import bpy
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blender_terrain as bt

from blender_kit import *                                                                          # noqa: F401,F403
import blender_sites as bs
import blender_nature as bn

# ---------------------------------------------------------------- the buildings
def great_round(ground, M, coll, report):
    X, Y = site("round"); rim = ground.z(X, Y)
    report["The Great Round"] = {"volume": "IV", "radius_m": 25, "relief_before_m": ground.relief(X, Y, 25)[0]}
    z_orch = rim - 11.2
    ground.pad(X, Y, 31, rim, 45)
    ground.edit(X, Y, 25, lambda d, dX, dY, g: np.where(d < 24, np.minimum(g, z_orch - 2), g))       # the bowl, hidden under the tiers
    k = Kit("IV · The Great Round")
    k.cyl(X, Y, 8.0, z_orch - 1, z_orch, M["sand"], 48)
    k.ring(X, Y, 8.0, 8.6, z_orch - 1, z_orch + .35, M["marble"], 48)
    radii = [8.6 + i * .95 + (1.4 if i >= 7 else 0) for i in range(14)]                           # the walkway after row 7
    for i, r_in in enumerate(radii):
        k.ring(X, Y, r_in, 23.4, z_orch - 1, z_orch + .8 * (i + 1), M["limestone"], 96)
    gate_half = math.asin(2.7 / 24.2)
    for g in range(4):                                                                              # ring wall between the gates
        k.ring(X, Y, 23.4, 25.0, rim - 12, rim + 7, M["ashlar"], 96, g * TAU / 4 + gate_half, (g + 1) * TAU / 4 - gate_half)
    for g in range(4):                                                                              # E, N, W, S gateways
        th = g * TAU / 4; cx, cy = X + 24.2 * math.cos(th), Y + 24.2 * math.sin(th)
        tx, ty = -math.sin(th), math.cos(th)
        for side in (-1, 1): k.box(cx + tx * 4.4 * side, cy + ty * 4.4 * side, rim - 2, rim + 10, 3.4, 3.4, th, M["ashlar"])
        k.box(cx, cy, rim + 6.2, rim + 7.6, 3.4, 12.2, th, M["ashlar"])
        for side in (-1, 1): k.box(cx + tx * 1.35 * side, cy + ty * 1.35 * side, rim, rim + 5.8, .35, 2.6, th, M["bronze"])
        k.box(cx - math.cos(th) * .45, cy - math.sin(th) * .45, rim + 2.7, rim + 3.1, .35, 5.6, th, M["timber"])
        k.box(cx, cy, rim - .3, rim, 5.0, 5.4, th, M["pave"])
    for sidx in range(8):                                                                           # radial stairways between gates
        th = TAU / 16 + sidx * TAU / 8
        for i, r_in in enumerate(radii):
            r_out = radii[i + 1] if i + 1 < len(radii) else 23.4
            top = z_orch + .8 * (i + 1)
            for f, zt in ((.25, top - .4), (.75, top)):
                r = r_in + (r_out - r_in) * f
                k.box(X + r * math.cos(th), Y + r * math.sin(th), top - .8, zt + .02, (r_out - r_in) / 2, 1.3, th, M["marble"])
    for sidx in range(24):                                                                          # legislators' statues outside the wall
        th = sidx * TAU / 24
        if min(abs((th - g * TAU / 4 + math.pi) % TAU - math.pi) for g in range(4)) < math.radians(12): continue
        sx, sy = X + 29.5 * math.cos(th), Y + 29.5 * math.sin(th)
        k.box(sx, sy, rim - .5, rim + 1.3, 1.1, 1.1, th, M["marble"])
        k.cyl(sx, sy, .32, rim + 1.3, rim + 3.0, M["marble"], 8)
        k.box(sx, sy, rim + 3.0, rim + 3.45, .45, .45, th, M["marble"])
    return k, (X, Y, rim)

def banquet_house(ground, M, coll, report, round_xy):
    X, Y = site("banquet"); g0 = ground.z(X, Y)
    report["Banquet house"] = {"volume": "IV", "radius_m": 17, "relief_before_m": ground.relief(X, Y, 16)[0]}
    ground.pad(X, Y, 18, g0, 25)
    ang = math.atan2(round_xy[1] - Y, round_xy[0] - X)                                             # local -x... faces the Round
    k = Kit("IV · Banquet house")
    k.box(X, Y, g0 - 2, g0 + .8, 30, 22, ang, M["limestone"])
    k.box(X, Y, g0 + .8, g0 + .95, 17, 10, ang, M["garden"])
    colonnade(k, X, Y, g0 + .8, g0 + 4.6, 24, 16, ang, 3.0, M["marble"])
    c, s = math.cos(ang), math.sin(ang)
    for u, v, sx, sy in ((0, 9.5, 27, 3), (0, -9.5, 27, 3), (12, 0, 3, 16), (-12, 0, 3, 16)):
        k.box(X + u * c - v * s, Y + u * s + v * c, g0 + 4.6, g0 + 5.2, sx, sy, ang, M["roof"])
    hx, hy = X - 9.5 * c, Y - 9.5 * s                                                               # dining hall on the side away from the Round
    k.box(hx, hy, g0 + .8, g0 + 6.5, 9, 17, ang, M["plaster"])
    k.gable(hx, hy, g0 + 6.5, 17.8, 9.8, 2.6, ang + math.pi / 2, M["roof"])
    return k

def lantern_harbour(ground, M, coll, report):
    info = SITES["built"]["cothon"]
    X, Y = B(*info["centre_m"])
    th_c = math.radians(-info["channel_bearing_deg_from_x_toward_y"])                             # map y points south
    R, RI = info["basin_radius_m"], info["islet_radius_m"]
    report["Lantern harbour"] = {"volume": "III", "radius_m": 270}
    def level(d, dX, dY, g):
        along = dX * math.cos(th_c) + dY * math.sin(th_c); across = np.abs(-dX * math.sin(th_c) + dY * math.cos(th_c))
        channel = (along > 0) & (across < 24)
        quay = (d >= R - 1) & (d < 250) & ~channel                                                  # right up to the basin wall: no stray hill vertices
        w = 1 - smooth((d - 250) / 60)
        g = np.where(quay, 2.8, np.where((d >= 250) & ~channel & (g > 2.8), g * (1 - w) + 2.8 * w, g))
        return np.where(d < RI, 2.6, g)
    ground.edit(X, Y, 320, level)
    k = Kit("III · Lantern harbour (cothon)")
    gap = math.radians(9)
    k.ring(X, Y, R, R + 6, -4, 2.8, M["limestone"], 128, th_c + gap, th_c + TAU - gap)
    k.ring(X, Y, RI, RI + 2, -4, 2.6, M["limestone"], 48)
    free = TAU - 2 * math.radians(25)
    for p in range(7):                                                                               # seven quays, one captain's post each
        th = th_c + math.radians(25) + (p + .5) * free / 7
        k.box(X + (R - 21) * math.cos(th), Y + (R - 21) * math.sin(th), -3, 2.6, 42, 8, th, M["limestone"])
        px, py = X + (R + 14) * math.cos(th), Y + (R + 14) * math.sin(th)
        house(k, ground, px, py, 6, 6, 3.5, th, M["plaster"], M["roof"])
    k.cyl(X, Y, 7, 2.5, 24, M["limestone"], 24)
    k.cyl(X, Y, 4.5, 24, 29, M["lantern"], 16)
    k.cone(X, Y, 5.5, 29, 33, M["roof"], 16)
    tx, ty = -math.sin(th_c), math.cos(th_c)
    mid = (R + 265) / 2
    for side in (-1, 1):
        cx, cy = X + math.cos(th_c) * mid + tx * 23 * side, Y + math.sin(th_c) * mid + ty * 23 * side
        k.box(cx, cy, -4, 2.8, 265 - R, 3, th_c, M["limestone"])
        ex, ey = X + math.cos(th_c) * 268 + tx * 27 * side, Y + math.sin(th_c) * 268 + ty * 27 * side
        k.box(ex, ey, -4, 16, 9, 9, th_c, M["ashlar"])
    basin = [ground.z(X + 100 * math.cos(a), Y + 100 * math.sin(a)) for a in np.linspace(0, TAU, 16, endpoint=False)]
    report["Lantern harbour"]["basin_depth_m"] = round(float(np.median(basin)), 1)
    return k

def merchant_quays(ground, M, coll, report):
    X, Y = site("port"); s = ground.seaward(X, Y)
    SX, SY = ground.shore(X, Y, s)
    ang = math.atan2(s[1], s[0]); tx, ty = -s[1], s[0]
    report["Merchant quays"] = {"volume": "IV", "radius_m": 110}
    k = Kit("IV · Merchant quays")
    k.box(SX + s[0] * 2, SY + s[1] * 2, -4, 1.8, 14, 200, ang, M["limestone"])
    tips = []
    for off in (-70, 0, 70):
        cx, cy = SX + s[0] * 44.5 + tx * off, SY + s[1] * 44.5 + ty * off
        k.box(cx, cy, -4, 1.8, 75, 9, ang, M["limestone"])
        tips.append(ground.z(SX + s[0] * 80 + tx * off, SY + s[1] * 80 + ty * off))
    for off in (-40, 40):                                                                           # warehouses behind the quay
        house(k, ground, SX - s[0] * 26 + tx * off, SY - s[1] * 26 + ty * off, 13, 55, 7, ang, M["plaster"], M["roof"])
    report["Merchant quays"]["pier_tip_depths_m"] = [round(t, 1) for t in tips]
    return k

def harbour_town(ground, M, coll, report):
    town = SITES["built"]["town"]
    ax, ay = B(*town["agora_m_deg"][:2]); aang = math.radians(-town["agora_m_deg"][2])
    report["Harbour town"] = {"volume": "IV", "insulae": len(town["insulae_m_deg"])}
    k = Kit("IV · Harbour town and agora")
    lo, hi = on_ground(ground, ax, ay, 40, 30, aang, 1)
    k.box(ax, ay, lo, hi + .25, 40, 30, aang, M["pave"])
    c, s = math.cos(aang), math.sin(aang)
    sx_, sy_ = ax - 19.5 * s * -1, ay + 19.5 * c                                                     # stoa along one long side
    sx_, sy_ = ax - (-19.5) * s, ay + (-19.5) * c
    sx_, sy_ = ax + 19.5 * -s, ay + 19.5 * c
    k.box(sx_, sy_, hi, hi + 7, 40, 9, aang, M["plaster"])
    k.gable(sx_, sy_, hi + 7, 41, 10, 2.2, aang, M["roof"])
    fx, fy = ax + 14.5 * -s, ay + 14.5 * c
    for i in range(13): k.cyl(fx + (i - 6) * 3.2 * c, fy + (i - 6) * 3.2 * s, .35, hi + .25, hi + 6, M["marble"], 10)
    k.cyl(ax, ay, 2.2, hi + .25, hi + 1, M["marble"], 16)                                           # fountain
    k.cyl(ax + 8 * c, ay + 8 * s, .4, hi + .25, hi + 3.2, M["marble"], 8)                           # sundial pillar
    for n, (x, y, deg) in enumerate(town["insulae_m_deg"]):
        X, Y = B(x, y); ang = math.radians(-deg); c, s = math.cos(ang), math.sin(ang)
        rnd = random.Random(n)
        for u, v, sx, sy in ((0, 10.5, 44, 9), (0, -10.5, 44, 9), (17, 0, 10, 12), (-17, 0, 10, 12)):
            if rnd.random() < .12: continue
            house(k, ground, X + u * c - v * s, Y + u * s + v * c, sx, sy, rnd.uniform(5, 8.5), ang if sx > sy else ang + math.pi / 2 * 0,
                  M["plaster"], M["roof"], rise=min(sx, sy) * .2)
    return k

def headland_city(ground, M, coll, report, toward):
    X, Y = site("city"); g0 = ground.z(X, Y)
    home = math.atan2(toward[1] - Y, toward[0] - X)
    walls = []
    for a in np.linspace(0, TAU, 28, endpoint=False):
        r = 115.0
        while r > 45 and ground.z(X + r * math.cos(a), Y + r * math.sin(a)) < 3: r -= 5
        walls.append((X + r * math.cos(a), Y + r * math.sin(a), a, r))
    gate = min(range(28), key=lambda i: abs((walls[i][2] - home + math.pi) % TAU - math.pi))
    report["Besieged headland city"] = {"volume": "V", "radius_m": max(w[3] for w in walls), "relief_before_m": ground.relief(X, Y, 80)[0]}
    k = Kit("V · Besieged headland city")
    for i in range(28):
        (x0, y0, _, _), (x1, y1, _, _) = walls[i], walls[(i + 1) % 28]
        if i == gate: continue
        L = math.hypot(x1 - x0, y1 - y0); za, zb = ground.z(x0, y0), ground.z(x1, y1)
        k.box((x0 + x1) / 2, (y0 + y1) / 2, min(za, zb) - 3, max(za, zb) + 9, L + 1.5, 3, math.atan2(y1 - y0, x1 - x0), M["ashlar"])
    for i in range(0, 28, 2):
        x, y, a, _ = walls[i]; z = ground.z(x, y)
        k.box(x, y, z - 3, z + 14, 7, 7, a, M["ashlar"])
    for i in (gate, (gate + 1) % 28):
        x, y, a, _ = walls[i]; z = ground.z(x, y)
        k.box(x, y, z - 3, z + 16, 8, 8, a, M["ashlar"])
    rnd = random.Random(5); best = (g0, X, Y)
    c, s = math.cos(home), math.sin(home)
    for u in np.arange(-110, 111, 17):
        for v in np.arange(-110, 111, 17):
            x, y = X + u * c - v * s, Y + u * s + v * c
            a = math.atan2(y - Y, x - X); i = int(round(a / TAU * 28)) % 28
            if math.hypot(u, v) > walls[i][3] - 14 or ground.z(x, y) < 3: continue
            if ground.z(x, y) > best[0]: best = (ground.z(x, y), x, y)
            if rnd.random() < .3: continue
            house(k, ground, x, y, rnd.uniform(10, 13), rnd.uniform(8, 11), rnd.uniform(5, 7), home, M["plaster"], M["roof"])
    _, tx, ty = best                                                                                  # temple on the highest ground inside
    lo, hi = on_ground(ground, tx, ty, 28, 13, home, 1)
    k.box(tx, ty, lo, hi + 1.2, 30, 15, home, M["limestone"])
    k.box(tx, ty, hi + 1.2, hi + 9, 18, 8, home, M["marble"])
    colonnade(k, tx, ty, hi + 1.2, hi + 8.5, 26, 11, home, 3.0, M["marble"], .5)
    k.gable(tx, ty, hi + 9, 29, 14, 3.2, home, M["roof"])
    camps = Kit("V · Siege camps")
    for n, (x, y, z) in enumerate(SITES["sites"]["camps"]["points_m"]):
        CX, CY = B(x, y); face = math.atan2(Y - CY, X - CX); gz = ground.z(CX, CY)
        camps.ring(CX, CY, 32, 32.4, gz - 2, gz + 2.6, M["timber"], 48, face + math.radians(8), face + TAU - math.radians(8))
        c2, s2 = math.cos(face), math.sin(face)
        for row in (-1, 1):
            for col in range(5):
                u, v = -16 + col * 8, row * 9
                px, py = CX + u * c2 - v * s2, CY + u * s2 + v * c2
                camps.gable(px, py, ground.z(px, py), 4.5, 3.5, 2.4, face, M["canvas"])
        camps.gable(CX - 18 * c2, CY - 18 * s2, ground.z(CX - 18 * c2, CY - 18 * s2), 9, 6, 3.5, face, M["canvas"])
    return k, camps

def citadel(ground, M, coll, report):
    X, Y = site("citadel"); HX, HY = site("seawall"); g0 = ground.z(X, Y)
    ang = math.atan2(HY - Y, HX - X); c, s = math.cos(ang), math.sin(ang)
    report["Citadel of Iron Quorums"] = {"volume": "VII", "radius_m": 82, "relief_before_m": ground.relief(X, Y, 70)[0]}
    samples = [ground.z(X + r * math.cos(q), Y + r * math.sin(q)) for r in (0, 30, 60) for q in np.linspace(0, TAU, 8, endpoint=False)]
    g0 = float(np.median(samples))                                                                  # level at the hilltop's median, not its centre
    ground.pad(X, Y, 50, g0, 85)
    k = Kit("VII · Citadel of Iron Quorums")
    L2, W2 = 65, 47.5
    corners = [(-L2, -W2), (L2, -W2), (L2, W2), (-L2, W2)]
    P = lambda u, v: (X + u * c - v * s, Y + u * s + v * c)
    for i in range(4):
        (u0, v0), (u1, v1) = corners[i], corners[(i + 1) % 4]
        for j in range(5):
            if i == 1 and j == 2: continue                                                          # gatehouse gap, facing the harbour
            f0, f1 = j / 5, (j + 1) / 5
            a, b = P(u0 + (u1 - u0) * f0, v0 + (v1 - v0) * f0), P(u0 + (u1 - u0) * f1, v0 + (v1 - v0) * f1)
            za, zb = ground.z(*a), ground.z(*b)
            k.box((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, min(za, zb) - 3, max(za, zb) + 13, math.hypot(b[0] - a[0], b[1] - a[1]) + 2, 4,
                  math.atan2(b[1] - a[1], b[0] - a[0]), M["wall_dark"])
        cx, cy = P(u0, v0); z = ground.z(cx, cy)
        k.cyl(cx, cy, 7.5, z - 3, z + 20, M["wall_dark"], 20)
        mx, my = P((u0 + u1) / 2, (v0 + v1) / 2)
        if i != 1: k.box(mx, my, ground.z(mx, my) - 3, ground.z(mx, my) + 17, 9, 9, ang, M["wall_dark"])
    for side in (-1, 1):
        gx, gy = P(L2, side * 8.5); z = ground.z(gx, gy)
        k.box(gx, gy, z - 3, z + 19, 10, 10, ang, M["wall_dark"])
    kx, ky = P(-10, 0)
    k.box(kx, ky, g0 - 2, g0 + 24, 26, 26, ang, M["wall_dark"])
    hx, hy = P(-42, 0)
    k.box(hx, hy, g0 - 1, g0 + 10, 20, 32, ang, M["ashlar"]); k.gable(hx, hy, g0 + 10, 33, 21, 4, ang + math.pi / 2, M["roof"])
    for side in (-1, 1):
        bx, by = P(20, side * 30)
        k.box(bx, by, g0 - 1, g0 + 7, 45, 10, ang, M["plaster"]); k.gable(bx, by, g0 + 7, 46, 11, 2.4, ang, M["roof"])
    # the walled harbour below
    sw = ground.seaward(HX, HY); SX, SY = ground.shore(HX, HY, sw)
    th = math.atan2(sw[1], sw[0]); tx, ty = -sw[1], sw[0]
    h = Kit("VII · Citadel harbour and sea wall")
    a0, a1 = th - math.radians(75), th + math.radians(75)
    h.ring(SX, SY, 104, 116, -8, 3, M["ashlar"], 64, a0, a1)
    for a in (a0, a1): h.cyl(SX + 110 * math.cos(a), SY + 110 * math.sin(a), 5, -8, 12, M["ashlar"], 16)
    wall = []
    for d in np.arange(-150, 151, 25):
        px, py = SX + tx * d, SY + ty * d
        for e in np.arange(-150, 150, 2.5):
            if ground.z(px + sw[0] * e, py + sw[1] * e) < 1: wall.append((px + sw[0] * e, py + sw[1] * e)); break
    for (x0, y0), (x1, y1) in zip(wall, wall[1:]):
        h.box((x0 + x1) / 2, (y0 + y1) / 2, -2, 7, math.hypot(x1 - x0, y1 - y0) + 2, 3, math.atan2(y1 - y0, x1 - x0), M["ashlar"])
    h.box(SX + sw[0] * 6, SY + sw[1] * 6, -3, 2, 10, 60, th, M["limestone"])
    arc = [ground.z(SX + 110 * math.cos(a), SY + 110 * math.sin(a)) for a in np.linspace(a0, a1, 16)]
    report["Citadel harbour and sea wall"] = {"volume": "VII", "radius_m": 116, "breakwater_over_water_pct": round(100 * float(np.mean(np.array(arc) < 0)), 1)}
    return k, h, (SX, SY)

# ---------------------------------------------------------------- checks, cameras, main
def bearing_diff(a, b):
    return abs((a - b + math.pi) % TAU - math.pi)

def main():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ctx = bt.build(); scene = ctx["scene"]
    ground = Ground(ctx["terrain"]); M = palette()
    top = bt.collection("Buildings")
    colls = {v: bt.collection(f"{v} · {bt.VOLUMES[v]}", top) for v in ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX")}
    report = {}
    rk, (RX, RY, rim) = great_round(ground, M, colls["IV"], report)
    bk = banquet_house(ground, M, colls["IV"], report, (RX, RY))
    ck = lantern_harbour(ground, M, colls["III"], report)
    ground.commit()                                                                                  # later builders sample the levelled ground
    ck_city, ck_camps = headland_city(ground, M, colls["V"], report, (RX, RY))
    cit, harb, (HSX, HSY) = citadel(ground, M, colls["VII"], report)
    ground.commit()
    mq = merchant_quays(ground, M, colls["IV"], report)
    tw = harbour_town(ground, M, colls["IV"], report)
    objs = [rk.finish(colls["IV"]), bk.finish(colls["IV"]), ck.finish(colls["III"]), mq.finish(colls["IV"]), tw.finish(colls["IV"]),
            ck_city.finish(colls["V"]), ck_camps.finish(colls["V"]), cit.finish(colls["VII"]), harb.finish(colls["VII"])]

    # the remaining sites (tools/blender_sites.py)
    M.update(bs.extra_mats())
    hamlets = [bs.hamlet(ground, M, key, f"Hamlet {key[-1]}", n) for n, key in enumerate(("hamA", "hamK", "hamM"))]
    press = bs.olive_press(ground, M)
    beacons, fires = bs.beacon_towers(ground, M)
    oracle_k = bs.oracle(ground, M)
    drums, decks = bs.drummers(ground, M)
    markers, n_markers = bs.causeway_markers(ground, M)
    agora = B(*SITES["built"]["town"]["agora_m_deg"][:2])
    walk, walk_info = bs.statue_walk(ground, M, agora)
    grans, gran_gap = bs.granaries(ground, M)
    guild, guild_info = bs.guild_quarter(ground, M, None)
    monk, jetty_tip = bs.monastery(ground, M, (RX, RY))
    ground.commit()
    site_objs = [hk.finish(colls["I"]) for hk, _ in hamlets] + [press.finish(colls["I"]), beacons.finish(colls["I"]), oracle_k.finish(colls["II"]),
                 drums.finish(colls["III"]), markers.finish(colls["III"]), walk.finish(colls["IV"]), grans.finish(colls["VI"]),
                 guild.finish(colls["VIII"]), monk.finish(colls["IX"])]
    terrain = ctx["terrain"]
    tops = [t for _, t in hamlets]
    ham_seen = [f"{'AKM'[i]}–{'AKM'[j]}" for i in range(3) for j in range(i + 1, 3) if bs.clear_sight(terrain, tops[i], tops[j])]
    OX, OY = site("oracle")
    summit_near = max(ground.z(OX + r * math.cos(a), OY + r * math.sin(a), before=True) for r in range(0, 401, 25) for a in np.linspace(0, TAU, 24, endpoint=False))
    lift = lambda p: (p[0], p[1], p[2] + 500)
    OX_, OY_ = site("oracle"); oz = ground.z(OX_, OY_)
    rays_work = all(bs.clear_sight(terrain, lift(tops[i]), lift(tops[j])) for i in range(3) for j in range(i + 1, 3)) \
        and not bs.clear_sight(terrain, (OX_ - 900, OY_, oz - 60), (OX_ + 900, OY_, oz - 60))       # self-test: clear 500 m up, blocked through the summit
    sres = {"sightline_self_test": rays_work, "hamlet_rooftops_in_sight": ham_seen, "beacon_fires_in_sight": bs.clear_sight(terrain, *fires),
            "drum_decks_in_sight": bs.clear_sight(terrain, *decks), "granary_min_gap_m": gran_gap,
            "oracle_below_local_summit_m": round(summit_near - ground.z(OX, OY, before=True), 1),
            "lock_houses": guild_info, "statue_walk": walk_info, "causeway_markers": n_markers, "monastery_jetty_tip_m": jetty_tip,
            "objects": len(site_objs), "faces": sum(len(o.data.polygons) for o in site_objs)}
    sres["ok"] = (rays_work and not ham_seen and sres["beacon_fires_in_sight"] and sres["drum_decks_in_sight"] and gran_gap >= 300
                  and sres["oracle_below_local_summit_m"] <= 15 and guild_info["lock_ground_min_m"] > 1 and jetty_tip < -1)
    (bt.OUT / "sites-checks.json").write_text(json.dumps(sres, indent=1))
    print("SITES CHECKS", json.dumps(sres))
    bt.page_block("SITES",
                  [("Models", f"{sres['objects']} objects, {sres['faces']:,} faces"),
                   ("Statue Walk", f"{walk_info['length_m']} m, {walk_info['statues']} statues"),
                   ("…grade on its levelled bed", f"mean {walk_info['mean_grade_pct']}%, steepest {walk_info['max_grade_pct']}% (ground alone: {walk_info['max_grade_ungraded_pct']}%)"),
                   ("Granary storehouses, closest pair", f"{gran_gap} m apart"),
                   ("Lock-house spacing", ", ".join(f"{v} m" for v in guild_info["lock_spacing_m"])),
                   ("Causeway marker posts", str(n_markers)), ("Monastery jetty tip", f"{jetty_tip} m")],
                  [("Sightline test works (clear 500 m up, blocked through the summit)", rays_work),
                   ("Hamlet rooftops hidden from each other (rays through the terrain)", not ham_seen),
                   ("Beacon fires in sight of each other", sres["beacon_fires_in_sight"]),
                   ("Drum platforms in sight across the strait", sres["drum_decks_in_sight"]),
                   ("Granary storehouses at least 300 m apart", gran_gap >= 300),
                   (f"Oracle within 15 m of the local summit ({sres['oracle_below_local_summit_m']} m below)", sres["oracle_below_local_summit_m"] <= 15),
                   ("Lock-houses all on land", guild_info["lock_ground_min_m"] > 1),
                   ("Monastery jetty reaches water", jetty_tip < -1)])

    BX, BY = site("banquet")
    land = {n: site(k_) for n, k_ in (("The Great Round", "round"), ("Banquet house", "banquet"), ("Besieged headland city", "city"),
                                      ("Citadel of Iron Quorums", "citadel"))}
    circles = {"The Great Round": (RX, RY, 32), "Banquet house": (BX, BY, 17), "Besieged headland city": (*site("city"), report["Besieged headland city"]["radius_m"]),
               "Citadel of Iron Quorums": (*site("citadel"), 82), "Lantern harbour": (*B(*SITES["built"]["cothon"]["centre_m"]), 270),
               "Citadel harbour and sea wall": (HSX, HSY, 116)}
    names = list(circles)
    overlaps = [f"{a} / {b}" for i, a in enumerate(names) for b in names[i + 1:]
                if math.hypot(circles[a][0] - circles[b][0], circles[a][1] - circles[b][1]) < circles[a][2] + circles[b][2]]
    res = {"buildings": report, "objects": len(objs), "faces": sum(len(o.data.polygons) for o in objs),
           "round_east_gate_to_banquet_deg": round(math.degrees(bearing_diff(math.atan2(BY - RY, BX - RX), 0.0)), 1),
           "land_buildings_on_land": all(ground.z(x, y, before=True) > 1 for x, y in land.values()),
           "pier_tips_in_water": all(t < -1 for t in report["Merchant quays"]["pier_tip_depths_m"]),
           "cothon_basin_water": report["Lantern harbour"]["basin_depth_m"] < -3,
           "breakwater_mostly_over_water": report["Citadel harbour and sea wall"]["breakwater_over_water_pct"] >= 70,
           "footprint_overlaps": overlaps}
    res["ok"] = (res["round_east_gate_to_banquet_deg"] <= 30 and res["land_buildings_on_land"] and res["pier_tips_in_water"]
                 and res["cothon_basin_water"] and res["breakwater_mostly_over_water"] and not overlaps)
    (bt.OUT / "buildings-checks.json").write_text(json.dumps(res, indent=1))
    print("BUILDINGS CHECKS", json.dumps(res))
    rel = report
    bt.page_block("BUILDINGS",
                  [("Models", f"{res['objects']} objects, {res['faces']:,} faces"),
                   ("Ground relief levelled under the Round", f"{rel['The Great Round']['relief_before_m']} m"),
                   ("…under the citadel", f"{rel['Citadel of Iron Quorums']['relief_before_m']} m"),
                   ("Lantern harbour basin depth", f"{rel['Lantern harbour']['basin_depth_m']} m"),
                   ("Merchant pier tips", ", ".join(f"{t} m" for t in rel["Merchant quays"]["pier_tip_depths_m"])),
                   ("Breakwater over water", f"{rel['Citadel harbour and sea wall']['breakwater_over_water_pct']}%"),
                   ("Town insulae", str(rel["Harbour town"]["insulae"]))],
                  [(f"The Round's east gate faces the banquet house (within 30°: {res['round_east_gate_to_banquet_deg']}°)", res["round_east_gate_to_banquet_deg"] <= 30),
                   ("Land buildings stand on land", res["land_buildings_on_land"]),
                   ("Merchant pier tips reach water", res["pier_tips_in_water"]),
                   ("The cothon basin holds water (deeper than 3 m)", res["cothon_basin_water"]),
                   ("The breakwater stands mostly in the sea (≥70%)", res["breakwater_mostly_over_water"]),
                   ("No hero footprints overlap", not overlaps)])

    # vegetation, fields and tracks (tools/blender_nature.py)
    PX_, PY_ = site("port"); BX_, BY_ = site("banquet")
    sightlines = [((RX, RY, rim + 8), (PX_, PY_, ground.z(PX_, PY_) + 2)), ((RX, RY, rim + 8), (BX_, BY_, ground.z(BX_, BY_) + 4)),
                  tuple(fires), tuple(decks)]
    exclusions = [(*B(x, y), r) for key, r in bn.EXCLUDE_M.items() for x, y, _ in SITES["sites"][key]["points_m"]]
    vres = bn.build(ctx, ground, bs.smooth_path, sightlines, exclusions)
    (bt.OUT / "vegetation-checks.json").write_text(json.dumps(vres, indent=1))
    print("VEGETATION CHECKS", json.dumps(vres))
    ic = vres["instances"]
    bt.page_block("VEGETATION",
                  [("Olive trees", f"{ic['olive groves']:,}"), ("Maquis shrubs", f"{ic['maquis']:,}"), ("Umbrella pines", f"{ic['umbrella pines']:,}"),
                   ("Cypresses (placed by hand)", str(vres["cypresses"])), ("Wheat and fallow parcels", f"{vres['wheat_and_fallow_km2']} km²"),
                   ("Track ribbons", f"{vres['track_ribbons_m']:,} m")],
                  [("No trees standing in water", vres["trees_standing_in_water"] == 0),
                   ("No tall trees on building footprints", vres["tall_trees_on_building_footprints"] == 0),
                   ("No tall trees on the story's sightlines (Round to quays and banquet house, beacons, drums)", vres["tall_trees_on_story_sightlines"] == 0)])

    look = ctx["look"]
    def cam_at(name, target, frm, height, lens=35):
        return bt.camera(name, (target[0] + frm[0], target[1] + frm[1], target[2] + height), target, look, lens=lens)
    CX, CY = B(*SITES["built"]["cothon"]["centre_m"]); th_c = math.radians(-SITES["built"]["cothon"]["channel_bearing_deg_from_x_toward_y"])
    PX, PY = site("port"); s_port = ground.seaward(PX, PY)
    CitX, CitY = site("citadel"); cityX, cityY = site("city")
    cams = {"round": cam_at("Cam · the Great Round", (RX, RY, rim - 4), (-95, -95), 70),
            "cothon": cam_at("Cam · the lantern harbour", (CX, CY, 0), (math.cos(th_c) * 520, math.sin(th_c) * 520), 330),
            "port": cam_at("Cam · merchant quays and town", (PX - s_port[0] * 180, PY - s_port[1] * 180, 20), (s_port[0] * 800, s_port[1] * 800), 360),
            "city": cam_at("Cam · the headland city", (cityX, cityY, ground.z(cityX, cityY)), (-420, -420), 330),
            "citadel": cam_at("Cam · citadel and walled harbour", ((CitX + HSX) / 2, (CitY + HSY) / 2, 40), (650, -250), 380),
            "parliament": cam_at("Cam · the Parliament's lobe", (RX + 300, RY + 100, 120), (-1400, -1500), 900, lens=40)}
    hAX, hAY = site("hamA"); OX2, OY2 = site("oracle"); stX, stY = site("strait"); HLX, HLY = site("hall"); MOX, MOY = site("monastery")
    gpts = [site("granary", i) for i in range(3)] + [site("granary2")]
    gcx, gcy = sum(p[0] for p in gpts) / 4, sum(p[1] for p in gpts) / 4
    cliffX, cliffY = site("cliffs"); s_cl = ground.seaward(cliffX, cliffY)
    walk_pts = [B(x, y) for x, y in SITES["built"]["statue_walk_m"]]; wmx, wmy = walk_pts[len(walk_pts) // 2]
    to_round = (RX - agora[0], RY - agora[1]); tr = math.hypot(*to_round)
    cams.update({
        "hamlet": cam_at("Cam · hamlet A", (hAX, hAY, ground.z(hAX, hAY)), (-150, -150), 95),
        "oracle": cam_at("Cam · the oracle on the summit", (OX2, OY2, ground.z(OX2, OY2) - 20), (-240, -260), 170),
        "neck": cam_at("Cam · the neck: causeway and drummers", ((site("drummers", 0)[0] + site("drummers", 1)[0]) / 2, (site("drummers", 0)[1] + site("drummers", 1)[1]) / 2, 5), (-760, -700), 460, lens=28),
        "granaries": cam_at("Cam · the granary plain", (gcx, gcy, 40), (-900, -420), 620, lens=32),
        "guild": cam_at("Cam · the guild quarter and quarry", ((HLX + cliffX) / 2, (HLY + cliffY) / 2, 60), (s_cl[0] * 650 - 250, s_cl[1] * 650 - 150), 420, lens=28),
        "monastery": cam_at("Cam · the Raft monastery", (MOX, MOY, ground.z(MOX, MOY)), ((RX - MOX) / math.hypot(RX - MOX, RY - MOY) * 210 + 60, (RY - MOY) / math.hypot(RX - MOX, RY - MOY) * 210 - 60), 110),
        "walk": bt.camera("Cam · up the Statue Walk", (agora[0] - to_round[0] / tr * 150, agora[1] - to_round[1] / tr * 150, ground.z(*agora) + 160), (wmx, wmy, ground.z(wmx, wmy)), look, lens=35)})
    scene.camera = ctx["cams"]["overview"]
    bpy.ops.wm.save_as_mainfile(filepath=str(bt.OUT / "paxos.blend"), compress=True)
    if "--render" in args:
        bt.RENDERS.mkdir(exist_ok=True); bt.use_eevee(scene)
        for key, cam in cams.items():
            bt.render(scene, cam, bt.RENDERS / f"buildings-{key}.png", (1600, 900))
        hAX_, hAY_ = site("hamA")
        close = cam_at("Cam · olive groves above hamlet A", (hAX_, hAY_, ground.z(hAX_, hAY_)), (-230, -150), 55, lens=30)
        for key, cam in (("overview", ctx["cams"]["overview"]), ("parliament", cams["parliament"]), ("plain", cams["granaries"]), ("groves", close)):
            bt.render(scene, cam, bt.RENDERS / f"nature-{key}.png", (1600, 900))
        scene.camera = ctx["cams"]["overview"]
        bpy.ops.wm.save_as_mainfile(filepath=str(bt.OUT / "paxos.blend"), compress=True)

if __name__ == "__main__":
    main()
