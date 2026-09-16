#!/usr/bin/env python3
"""Island-of-Paxos layout options for art-direction-grand.html.

Each option is a real elevation field (metres) on an 8 x 5.5 km world, so the
same source yields three things:
  maps/option-<k>.svg          rough map (hypsometric bands, roads, sites)
  maps/option-<k>-height.png   16-bit heightmap for Blender displacement
  maps/option-<k>-sites.json   site positions + elevations (for empties)
and the SVGs are inlined into art-direction-grand.html between MAP markers.

World: x east 0..8000 m, y south 0..5500 m. SVG unit = 5 m (1600 x 1100).
Heightmap range: -120 m .. +480 m  ->  0 .. 65535.
"""
import heapq, json, math, re, sys
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "maps"
W, H, CELL, U = 8000.0, 5500.0, 12.5, 5.0          # metres, metres, m/cell, m/svg-unit
NX, NY = int(W / CELL), int(H / CELL)
HMIN, HMAX = -120.0, 480.0

X0, Y0 = np.meshgrid((np.arange(NX) + .5) * CELL, (np.arange(NY) + .5) * CELL)
X, Y = X0, Y0                                     # primitives read these; warp() bends them

# ---------------------------------------------------------------- primitives
def blob(cx, cy, rx, ry, h, ang=0.0, p=2.0):
    a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    u = ((X - cx) * c + (Y - cy) * s) / rx
    v = (-(X - cx) * s + (Y - cy) * c) / ry
    return h * np.exp(-((u * u + v * v) ** (p / 2)))

def seg_dist(x0, y0, x1, y1, XX=None, YY=None):
    XX = X if XX is None else XX; YY = Y if YY is None else YY
    dx, dy = x1 - x0, y1 - y0
    t = np.clip(((XX - x0) * dx + (YY - y0) * dy) / (dx * dx + dy * dy), 0, 1)
    return np.hypot(XX - (x0 + t * dx), YY - (y0 + t * dy)), t

def ridge(x0, y0, x1, y1, w, h, p=2.0):
    d, _ = seg_dist(x0, y0, x1, y1)
    return h * np.exp(-((d / w) ** p))

def ring(cx, cy, r, w_in, w_out, h, gaps=(), soft=6.0):
    d = np.hypot(X - cx, Y - cy) - r
    w = np.where(d < 0, w_in, w_out)
    f = h * np.exp(-((np.abs(d) / w) ** 2))
    th = (np.degrees(np.arctan2(Y - cy, X - cx)) + 360) % 360   # 90 = south (y down)
    for a0, a1 in gaps:                                          # soft angular cut
        mid, half = (a0 + a1) / 2, (a1 - a0) / 2
        off = np.abs((th - mid + 180) % 360 - 180)
        f = f * np.clip((off - half) / soft, 0, 1)
    return f

def value_noise(seed, wavelengths=(1200, 600, 300, 150, 75), gain=.55):
    rng = np.random.default_rng(seed)
    out, amp, tot = np.zeros_like(X0), 1.0, 0.0
    for wl in wavelengths:
        gx, gy = int(W / wl) + 3, int(H / wl) + 3
        g = rng.uniform(-1, 1, (gy, gx))
        fx, fy = X0 / wl, Y0 / wl
        ix, iy = fx.astype(int), fy.astype(int)
        tx, ty = fx - ix, fy - iy
        tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
        a = g[iy, ix] * (1 - tx) + g[iy, ix + 1] * tx
        b = g[iy + 1, ix] * (1 - tx) + g[iy + 1, ix + 1] * tx
        out += amp * (a * (1 - ty) + b * ty); tot += amp; amp *= gain
    return out / tot

def warp(seed, amp=240.0):
    global X, Y
    X = X0 + amp * value_noise(seed + 100, (2200, 1100, 550))
    Y = Y0 + amp * value_noise(seed + 200, (2200, 1100, 550))

def finish(mass, seed, coast_noise=95.0, relief_noise=40.0):
    global X, Y
    h = mass - 45 + coast_noise * value_noise(seed) \
        + relief_noise * np.clip(mass / 250, 0, 1) * value_noise(seed + 1, (320, 160, 80, 40))
    X, Y = X0, Y0
    return np.where(h < 0, h * 1.6, h)

def near_sea(h, metres):
    k = max(1, int(metres / CELL))
    m = (h < 0).astype(np.int32)
    c = np.pad(m, ((k + 1, k), (k + 1, k))).cumsum(0).cumsum(1)
    box = c[2 * k + 1:, 2 * k + 1:] - c[:-2 * k - 1, 2 * k + 1:] - c[2 * k + 1:, :-2 * k - 1] + c[:-2 * k - 1, :-2 * k - 1]
    return box > 0

def snap(h, p, lo, hi, coast=None, radius=700.0):
    ok = (h >= lo) & (h <= hi)
    if coast: ok &= near_sea(h, coast)
    d2 = (X0 - p[0]) ** 2 + (Y0 - p[1]) ** 2
    d2 = np.where(ok & (d2 < radius * radius), d2, np.inf)
    i, j = np.unravel_index(np.argmin(d2), d2.shape)
    if not np.isfinite(d2[i, j]):
        print(f"      ! no cell in [{lo},{hi}] coast={coast} within {radius} m of {p}")
        return (float(p[0]), float(p[1]))
    return (float(X0[i, j]), float(Y0[i, j]))

def cothon(h, cx, cy, r=150.0):
    """Carthage-type circular inner harbour: quay platform, basin, central islet, channel to deep water."""
    deep = np.where(h < -6, (X0 - cx) ** 2 + (Y0 - cy) ** 2, np.inf)
    i, j = np.unravel_index(np.argmin(deep), deep.shape)
    ex, ey = X0[i, j], Y0[i, j]
    d = np.hypot(X0 - cx, Y0 - cy)
    h = np.where(d < r + 100, np.maximum(h, 7.0), h)
    cd, _ = seg_dist(cx, cy, ex, ey, X0, Y0)
    h = np.where((d < r) | (cd < 22), np.minimum(h, -7.0), h)
    return np.where(d < r * .3, 4.0, h), math.degrees(math.atan2(ey - cy, ex - cx))

# ---------------------------------------------------------------- sites (shared numbering)
SITES = [  # num, key, name, volumes, kind
    (1,  "hamA",     "Hamlet A",                       "1",   "dot"),
    (2,  "hamK",     "Hamlet K",                       "1",   "dot"),
    (3,  "hamM",     "Hamlet M",                       "1",   "dot"),
    (4,  "press",    "Olive press",                    "1",   "dot"),
    (5,  "signals",  "Signal headlands",               "1 4", "multi"),
    (6,  "citadel",  "Headland city → Citadel",        "2 7", "citadel"),
    (7,  "oracle",   "Oracle & cave",                  "3",   "dot"),
    (8,  "cothon",   "Circular harbour",               "4 5 7", "cothon"),
    (9,  "strait",   "The strait",                     "4",   "strait"),
    (10, "town",     "Harbour town · agora",           "1 5 7", "town"),
    (11, "round",    "The Great Round",                "5 8", "round"),
    (12, "banquet",  "Banquet house",                  "5",   "dot"),
    (13, "granary",  "Granary storehouses",            "6",   "multi"),
    (14, "granary2", "Granary on the heights",         "6",   "dot"),
    (15, "cliffs",   "Ledger cliffs",                  "8",   "cliff"),
    (16, "locks",    "Roman lock-houses",              "8",   "multi"),
]
VOL_ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX"}
# what each site demands of the ground: (min m, max m, within-metres-of-sea or None)
RULES = {"hamA": (40, 230, None), "hamK": (40, 230, None), "hamM": (40, 230, None), "press": (90, 300, None),
         "signals": (15, 260, 260), "citadel": (60, 240, 420), "oracle": (220, 999, None),
         "town": (4, 50, 320), "round": (140, 270, None), "banquet": (90, 250, None),
         "granary": (5, 90, None), "granary2": (90, 240, None), "cliffs": (15, 220, 140), "locks": (60, 300, None)}

# ---------------------------------------------------------------- options
# fn() -> (h, rough sites, cothon hint, rule overrides). Sites are snapped to their RULES afterwards.
def option_crescent():
    cx, cy, r = 4000, 1950, 2000
    at = lambda a, rr=r: (cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a)))
    warp(11)
    m = ring(cx, cy, r, 520, 680, 190, gaps=[(208, 332)], soft=16)
    m += blob(*at(172), 520, 460, 230)                                           # west mountain
    m += blob(*at(118), 360, 320, 75)
    m += blob(*at(72), 420, 360, 95)
    m += blob(*at(24), 460, 380, 125)
    m += ridge(4950, 3450, 4700, 2650, 170, 150, p=2.4)                          # citadel spur into the bay
    m += blob(6720, 560, 400, 300, 160, ang=-30)                                 # islet beyond the east horn
    h = finish(m, 11)
    sites = {
        "hamA": at(160, 2050), "hamK": at(60, 2250), "hamM": at(0, 2000), "press": at(75, 2000),
        "signals": [at(334, 2000), (6600, 700), at(206, 2000)],
        "citadel": (4760, 2780), "oracle": at(172), "strait": (6250, 850),
        "town": (3850, 3400), "round": at(106, 2050), "banquet": at(99, 2050),
        "granary": [at(140, 2350), at(146, 2350), at(152, 2350)], "granary2": at(145, 1950),
        "cliffs": at(80, 2600), "locks": [at(a, 2050) for a in (345, 355, 5, 15, 35)],
    }
    return h, sites, (4250, 3300), {}

def option_twin():
    warp(23)
    m = blob(2450, 2800, 1500, 1300, 220, ang=-8, p=3.0)                         # west lobe
    m += blob(1750, 2450, 520, 470, 230)                                         # the mountain (oracle)
    m += blob(2550, 3350, 420, 360, 90)                                          # south shoulder
    m += ridge(2700, 2750, 3700, 2600, 260, 70, p=2.2)                           # the saddle ridge
    m -= blob(3550, 3750, 620, 520, 170)                                         # south bay bites into the lobe
    m += ridge(3350, 2050, 3800, 1300, 170, 150, p=2.4)                          # citadel peninsula
    m += blob(6250, 2750, 1080, 900, 190, ang=12, p=3.0)                         # east lobe
    m += blob(6500, 2450, 420, 360, 125)
    h = finish(m, 23)
    d, _ = seg_dist(3950, 2900, 5300, 2850, X0, Y0)                             # the causeway: a tombolo
    h = np.where((d < 320) & (h < 0), np.maximum(h, -4.0 - d / 60), h)          # sandbar shallows
    h = np.where(d < 55, np.maximum(h, 2.5), h)
    sites = {
        "hamA": (1400, 3300), "hamK": (6750, 3150), "hamM": (5900, 2000), "press": (6450, 2550),
        "signals": [(3900, 3700), (5350, 3500), (900, 2600), (7250, 2500)],
        "citadel": (3700, 1450), "oracle": (1650, 2550), "strait": (4620, 2875),
        "town": (3800, 2450), "round": (3300, 2650), "banquet": (3450, 2650),
        "granary": [(5350, 3050), (5550, 3150), (5750, 3250)], "granary2": (6050, 2800),
        "cliffs": (2300, 4100), "locks": [(5600, 2050), (5800, 2080), (6000, 2110), (6200, 2140), (6400, 2170)],
    }
    return h, sites, (3980, 2450), {}

def option_caldera():
    cx, cy, r = 4000, 2850, 1550
    at = lambda a, f=1.0: (cx + r * f * math.cos(math.radians(a)), cy + r * f * math.sin(math.radians(a)))
    warp(37, 160)
    m = ring(cx, cy, r, 170, 700, 250, gaps=[(186, 196), (205, 244)], soft=4)
    m += blob(*at(300), 380, 320, 110)
    m += blob(*at(40), 400, 340, 90)
    m += blob(cx, cy, 280, 280, 200)                                             # the cone in the lagoon
    h = finish(m, 37, coast_noise=70)
    sites = {
        "hamA": at(145, 1.3), "hamK": at(70, 1.3), "hamM": at(335, 1.3), "press": at(20, 1.15),
        "signals": [at(185, 1.1), at(200, 1.0), at(92, 1.5)],
        "citadel": at(176), "oracle": (cx, cy), "strait": at(191),
        "town": at(258, .88), "round": at(274), "banquet": at(282),
        "granary": [at(100, 1.4), at(108, 1.4), at(116, 1.4)], "granary2": at(115, 1.15),
        "cliffs": at(60, .9), "locks": [at(a, 1.1) for a in (340, 348, 356, 4, 12)],
    }
    return h, sites, at(252, .82), {"oracle": (60, 999, None), "cliffs": (15, 260, 120)}

def option_spine():
    p0, p1 = (1550, 1050), (5600, 3750)
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
    nx, ny = uy, -ux                                                             # NE-pointing normal
    at = lambda tt, off=0: (p0[0] + ux * L * tt + nx * off, p0[1] + uy * L * tt + ny * off)
    warp(51)
    d, t = seg_dist(*p0, *p1)
    s = (X - p0[0]) * nx + (Y - p0[1]) * ny
    m = 200 * np.exp(-((d / np.where(s > 0, 820, 420)) ** 2.4))                 # gentle NE, cliffs SW
    m += blob(*at(.30), 460, 400, 140)
    m += blob(*at(.68), 420, 360, 115)
    m += ridge(*at(.46, 300), *at(.46, 1050), 160, 115, p=2.4)                  # citadel headland
    m += blob(7200, 4900, 400, 290, 150, ang=35)                                 # the southern islet
    h = finish(m, 51)
    sx, sy = 6800, 4520                                                          # cut the strait to the islet
    d, _ = seg_dist(sx - nx * 700, sy - ny * 700, sx + nx * 700, sy + ny * 700, X0, Y0)
    h = np.where(d < 110, np.minimum(h, -10.0 - (110 - d) / 8), h)
    bx, by = at(.05, 900)                                                        # round natural bay, north
    h = np.where(np.hypot(X0 - bx, Y0 - by) < 330, np.minimum(h, -14.0), h)
    sites = {
        "hamA": at(.18, 300), "hamK": at(.82, 250), "hamM": at(.38, -120), "press": at(.68, 100),
        "signals": [at(1.1, 0), (7050, 4750), at(-.08, 0)],
        "citadel": at(.46, 1000), "oracle": at(.34, -520), "strait": (6800, 4520),
        "town": at(.56, 820), "round": at(.53, 160), "banquet": at(.56, 300),
        "granary": [at(.72, 700), at(.75, 760), at(.78, 820)], "granary2": at(.76, 330),
        "cliffs": at(.62, -520), "locks": [at(.10 + .03 * k, 150) for k in range(5)],
    }
    return h, sites, at(.52, 980), {"oracle": (10, 140, 160)}

OPTIONS = {
    "a": ("Crescent", option_crescent),
    "b": ("Twin Lobes", option_twin),
    "c": ("Caldera", option_caldera),
    "d": ("Ridge Spine", option_spine),
}

def build(key):
    title, fn = OPTIONS[key]
    h, rough, hint, over = fn()
    ct = snap(h, hint, 1, 30, 200, 900)
    h, mouth = cothon(h, *ct)
    rules = {**RULES, **over}
    loc = {"cothon": ct, "strait": rough["strait"]}
    for skey, v in rough.items():
        if skey in loc: continue
        lo, hi, coast = rules[skey]
        loc[skey] = [snap(h, p, lo, hi, coast) for p in v] if isinstance(v, list) else snap(h, v, lo, hi, coast)
    place_by_sight(h, loc, rough, rules)
    return title, h, loc

def candidates(h, centre, radius, lo, hi, step=50.0):
    out = []
    for dx in np.arange(-radius, radius + 1, step):
        for dy in np.arange(-radius, radius + 1, step):
            x, y = centre[0] + dx, centre[1] + dy
            if dx * dx + dy * dy <= radius * radius and 0 <= x < W and 0 <= y < H and lo <= h_at(h, x, y) <= hi:
                out.append((float(x), float(y)))
    return out

def place_by_sight(h, loc, rough, rules):
    """Sightline rules the elevation bands can't express (D02, §1.2, Vol I)."""
    # The Round: a saddle with sea on two sides -> maximise the sea arc, prefer two opposed arcs.
    lo, hi, _ = rules["round"]
    def score(p):
        b = sea_bearings(h, p, reach=3000, step_m=50)
        opposed = two_sided(b)
        harbour = los_clear(h, p, loc["cothon"], 8, 2)        # "beyond the gate a galley sets sail from the harbour below"
        return len(b) * 15 + (90 if opposed else 0) + (120 if harbour else 0) - math.dist(p, rough["round"]) / 25
    loc["round"] = max(candidates(h, rough["round"], 900, lo, hi) + [loc["round"]], key=score)
    # Banquet house: a short walk east of the Round, lower, in plain view of the tiers.
    r = loc["round"]; rz = h_at(h, *r)
    want = (r[0] + 130, r[1])
    ok = [c for c in candidates(h, want, 160, max(5, rz - 70), rz - 4, 25)
          if c[0] - r[0] >= 60 and los_clear(h, r, c, 6, 4)]
    if ok: loc["banquet"] = min(ok, key=lambda c: math.dist(c, want))
    else: print("      ! no visible banquet site east of the Round")
    # Beacon pair: the second headland must see the first across the water.
    sig = loc["signals"]; lo, hi, coast = rules["signals"]
    if not los_clear(h, sig[0], sig[1], 6, 6):
        near = near_sea(h, coast)
        ok = [c for c in candidates(h, rough["signals"][1], 700, lo, hi, 25)
              if near[int(c[1] / CELL), int(c[0] / CELL)] and los_clear(h, sig[0], c, 6, 6)]
        if ok: sig[1] = min(ok, key=lambda c: math.dist(c, rough["signals"][1]))
        else: print("      ! no beacon site in sight of the first")
    # Hamlets: each hidden from the ones already placed.
    placed = [loc["hamA"]]
    for k in ("hamK", "hamM"):
        lo, hi, _ = rules[k]
        if all(not los_clear(h, loc[k], q, 3, 3) for q in placed):
            placed.append(loc[k]); continue
        ok = [c for c in candidates(h, rough[k], 900, lo, hi, 50) if all(not los_clear(h, c, q, 3, 3) for q in placed)]
        if ok: loc[k] = min(ok, key=lambda c: math.dist(c, rough[k]))
        else: print(f"      ! {k}: no hidden site within 900 m")
        placed.append(loc[k])

# ---------------------------------------------------------------- terrain queries
def h_at(h, x, y):
    j, i = int(np.clip(x / CELL, 0, NX - 1)), int(np.clip(y / CELL, 0, NY - 1))
    return float(h[i, j])

def least_cost_path(h, a, b, slope_k=900.0):
    """Dijkstra on the 12.5 m grid; roads avoid water and steep ground."""
    step = 2                                                                      # 25 m moves
    hs = h[::step, ::step]; ny, nx = hs.shape; c = CELL * step
    s = (int(a[1] / c), int(a[0] / c)); g = (int(b[1] / c), int(b[0] / c))
    dist = np.full(hs.shape, np.inf); prev = {}
    dist[s] = 0; pq = [(0.0, s)]
    nb = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    while pq:
        dd, (i, j) = heapq.heappop(pq)
        if (i, j) == g: break
        if dd > dist[i, j]: continue
        for di, dj in nb:
            ii, jj = i + di, j + dj
            if not (0 <= ii < ny and 0 <= jj < nx): continue
            if hs[ii, jj] < 1.5 and (ii, jj) != g: continue
            run = c * math.hypot(di, dj); grade = abs(hs[ii, jj] - hs[i, j]) / run
            nd = dd + run * (1 + slope_k * grade * grade)
            if nd < dist[ii, jj]:
                dist[ii, jj] = nd; prev[(ii, jj)] = (i, j); heapq.heappush(pq, (nd, (ii, jj)))
    path, cur = [], g
    while cur in prev: path.append(((cur[1] + .5) * c, (cur[0] + .5) * c)); cur = prev[cur]
    path.append(a); path.reverse(); path[-1] = b
    return path

def los_clear(h, p, q, eye=1.7, target=1.7, n=400):
    """True if nothing on the ground rises above the sightline from p (eye) to q (target)."""
    (x0, y0), (x1, y1) = p, q
    h0, h1 = max(h_at(h, x0, y0), 0) + eye, max(h_at(h, x1, y1), 0) + target
    for t in np.linspace(0, 1, n)[1:-1]:
        if h_at(h, x0 + (x1 - x0) * t, y0 + (y1 - y0) * t) > h0 + (h1 - h0) * t + .5:
            return False
    return True

def sea_bearings(h, p, eye=8.0, reach=4000.0, step_deg=15, step_m=25.0):
    """Bearings (of 360/step) along which open sea is visible from p."""
    x0, y0 = p; e = h_at(h, x0, y0) + eye; seen = []
    for b in range(0, 360, step_deg):
        dx, dy = math.sin(math.radians(b)), -math.cos(math.radians(b))   # 0 = north
        best = -1e9
        for d in np.arange(step_m, reach, step_m):
            x, y = x0 + dx * d, y0 + dy * d
            if not (0 <= x < W and 0 <= y < H): break
            z = h_at(h, x, y)
            if z < 0:
                if (0 - e) / d > best: seen.append(b); break
            else:
                best = max(best, (z - e) / d)
    return seen

def arcs(bearings, step=15):
    """Contiguous runs of visible-sea bearings, as (centre_deg, width_deg)."""
    on = set(bearings)
    if len(on) * step >= 360: return [(0, 360)]
    start = next(b for b in range(0, 360, step) if b not in on)
    out, run = [], []
    for k in range(1, 361 // step + 1):
        b = (start + k * step) % 360
        if b in on: run.append(b)
        elif run:
            out.append(((run[0] + (len(run) - 1) * step / 2) % 360, len(run) * step)); run = []
    return out

def two_sided(bearings):
    """Sea on both sides of a saddle: two arcs ≥30° facing apart, or one arc wrapping ≥240°."""
    a = arcs(bearings)
    if any(w >= 240 for _, w in a): return True
    big = [c for c, w in a if w >= 30]
    return any(abs((x - y + 180) % 360 - 180) >= 120 for x in big for y in big)

def checks(h, loc):
    hams = [("A", loc["hamA"]), ("K", loc["hamK"]), ("M", loc["hamM"])]
    pairs = [(a, b) for i, a in enumerate(hams) for b in hams[i + 1:]]
    ham_seen = [f"{a[0]}–{b[0]}" for a, b in pairs if los_clear(h, a[1], b[1], 3, 3)]
    sig = loc["signals"]
    sig_pairs = [(0, 1)]                                     # the beacon pair across the water
    sig_ok = sum(los_clear(h, sig[i], sig[j], 6, 6) for i, j in sig_pairs)
    sea = sea_bearings(h, loc["round"])
    return {"hamlets_mutually_visible": ham_seen,
            "banquet_visible_from_round": los_clear(h, loc["round"], loc["banquet"], 6, 4),
            "round_sea_bearings": len(sea) * 15, "round_sea_two_sided": two_sided(sea), "round_sea_arcs": arcs(sea),
            "signal_pairs_clear": [sig_ok, len(sig_pairs)],
            "town_to_round_clear": los_clear(h, loc["round"], loc["cothon"], 8, 2)}

# ---------------------------------------------------------------- contours
def march(h, t):
    f = np.pad(h, 1, constant_values=-1e4)
    ny, nx = f.shape
    ins = f >= t
    code = ins[:-1, :-1] * 8 + ins[:-1, 1:] * 4 + ins[1:, 1:] * 2 + ins[1:, :-1] * 1
    pt = {}
    def P(e):
        if e not in pt:
            k, i, j = e
            if k == "h": a, b, x0, y0, dx, dy = f[i, j], f[i, j + 1], j, i, 1, 0
            else:        a, b, x0, y0, dx, dy = f[i, j], f[i + 1, j], j, i, 0, 1
            fr = (t - a) / (b - a) if b != a else .5
            pt[e] = ((x0 + dx * fr - 1 + .5) * CELL / U, (y0 + dy * fr - 1 + .5) * CELL / U)
        return e
    adj = {}
    def link(a, b):
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    T = {1: [("l", "b")], 2: [("b", "r")], 3: [("l", "r")], 4: [("t", "r")], 6: [("t", "b")],
         7: [("l", "t")], 8: [("l", "t")], 9: [("t", "b")], 11: [("t", "r")], 12: [("l", "r")],
         13: [("b", "r")], 14: [("l", "b")]}
    for i, j in zip(*np.nonzero((code > 0) & (code < 15))):
        c = int(code[i, j])
        E = {"t": ("h", i, j), "b": ("h", i + 1, j), "l": ("v", i, j), "r": ("v", i, j + 1)}
        if c in (5, 10):
            centre = (f[i, j] + f[i, j + 1] + f[i + 1, j] + f[i + 1, j + 1]) / 4 >= t
            if c == 5: pairs = [("l", "t"), ("b", "r")] if centre else [("l", "b"), ("t", "r")]
            else:      pairs = [("t", "r"), ("l", "b")] if centre else [("l", "t"), ("b", "r")]
        else:
            pairs = T[c]
        for a, b in pairs: link(P(E[a]), P(E[b]))
    loops, seen = [], set()
    for start in adj:
        if start in seen: continue
        loop, prev, cur = [], None, start
        while True:
            seen.add(cur); loop.append(pt[cur])
            nxt = [n for n in adj[cur] if n != prev and n not in seen]
            if not nxt: break
            prev, cur = cur, nxt[0]
        if len(loop) >= 6: loops.append(loop)
    return loops

def chaikin(pts, n=2, closed=True):
    for _ in range(n):
        q = []
        m = len(pts) if closed else len(pts) - 1
        for k in range(m):
            (x0, y0), (x1, y1) = pts[k], pts[(k + 1) % len(pts)]
            q += [(.75 * x0 + .25 * x1, .75 * y0 + .25 * y1), (.25 * x0 + .75 * x1, .25 * y0 + .75 * y1)]
        pts = q if closed else [pts[0]] + q + [pts[-1]]
    return pts

def rdp(pts, eps):
    if len(pts) < 3: return pts
    a, b = np.array(pts[0]), np.array(pts[-1]); ab = b - a; n = np.hypot(*ab) or 1.0
    d = [abs(ab[0] * (p[1] - a[1]) - ab[1] * (p[0] - a[0])) / n for p in pts[1:-1]]
    k = int(np.argmax(d)) + 1
    if d[k - 1] > eps: return rdp(pts[:k + 1], eps)[:-1] + rdp(pts[k:], eps)
    return [pts[0], pts[-1]]

def loops_to_d(loops, eps=.45, min_area=6.0):
    out = []
    for lp in loops:
        xs, ys = zip(*lp)
        area = .5 * abs(sum(xs[k] * ys[k - 1] - xs[k - 1] * ys[k] for k in range(len(lp))))
        if area < min_area: continue
        c = chaikin(lp)
        far = max(range(len(c)), key=lambda k: (c[k][0] - c[0][0]) ** 2 + (c[k][1] - c[0][1]) ** 2)
        p = rdp(c[:far + 1], eps)[:-1] + rdp(c[far:] + [c[0]], eps)
        out.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in p) + "Z")
    return "".join(out)

def smooth_d(pts_m, closed=False):
    p = [(x / U, y / U) for x, y in pts_m]
    p = rdp(chaikin(p, 3, closed=False), .6)
    return "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in p)

# ---------------------------------------------------------------- svg
SEA_T = [-60, -25]
LAND_T = [0, 20, 70, 140, 220, 300, 380]
LINE_T = [-5, -13, -24]

def svg_for(key, title, h, sites, loc):
    S = []
    S.append(f'<svg class="islemap" viewBox="0 0 1600 1100" role="img" aria-labelledby="map-{key}-t" xmlns="http://www.w3.org/2000/svg">')
    S.append(f'<title id="map-{key}-t">Option {key.upper()} · {title}: rough map of Paxos</title>')
    S.append('<rect class="sea0" x="0" y="0" width="1600" height="1100"/>')
    for k, t in enumerate(SEA_T):
        S.append(f'<path class="sea{k + 1}" fill-rule="evenodd" d="{loops_to_d(march(h, t), .8, 20)}"/>')
    for k, t in enumerate(LINE_T):
        S.append(f'<path class="wline wl{k}" d="{loops_to_d(march(h, t), .6, 10)}"/>')
    for k, t in enumerate(LAND_T):
        d = loops_to_d(march(h, t), .45, 6 if k else 3)
        S.append(f'<path class="land{k}{" coast" if k == 0 else " contour"}" fill-rule="evenodd" d="{d}"/>')
    # roads (least-cost), statue walk first
    town, rnd = loc["town"], loc["round"]
    S.append(f'<path class="road walk" d="{smooth_d(least_cost_path(h, town, rnd))}"/>')
    S.append(f'<path class="road walk-dots" d="{smooth_d(least_cost_path(h, town, rnd))}"/>')
    for tgt in ["banquet", "hamA", "hamK", "hamM", "citadel", "press", "granary2", "oracle"]:
        p = loc[tgt][0] if isinstance(loc[tgt][0], tuple) else loc[tgt]
        if h_at(h, *p) < 1.5: continue
        path = least_cost_path(h, rnd if tgt == "banquet" else town, p)
        if len(path) > 2: S.append(f'<path class="road track" d="{smooth_d(path)}"/>')
    # town: little blocks on low ground
    rng = np.random.default_rng(7)
    tx, ty = town
    for _ in range(160):
        r, a = 420 * math.sqrt(rng.random()), rng.random() * math.tau
        x, y = tx + r * math.cos(a), ty + r * math.sin(a)
        if 3 < h_at(h, x, y) < 75 and math.hypot(x - loc["cothon"][0], y - loc["cothon"][1]) > 190:
            w_, hh = 5 + 5 * rng.random(), 4 + 4 * rng.random()
            S.append(f'<rect class="house" x="{x / U - w_ / 2:.1f}" y="{y / U - hh / 2:.1f}" width="{w_:.1f}" height="{hh:.1f}"/>')
    # site symbols
    for num, skey, name, vols, kind in SITES:
        pts = loc[skey] if isinstance(loc[skey], list) else [loc[skey]]
        cls = " ".join(f"v{v}" for v in vols.split())
        S.append(f'<g class="site {cls}" data-site="{num}">')
        x, y = pts[0][0] / U, pts[0][1] / U
        if kind == "round":
            S.append(f'<circle class="sym-round" cx="{x:.1f}" cy="{y:.1f}" r="16"/><circle class="sym-round-in" cx="{x:.1f}" cy="{y:.1f}" r="6.5"/>')
            for a in range(4):
                gx, gy = x + 16 * math.cos(a * math.pi / 2), y + 16 * math.sin(a * math.pi / 2)
                S.append(f'<rect class="sym-gate" x="{gx - 3.5:.1f}" y="{gy - 3.5:.1f}" width="7" height="7"/>')
        elif kind == "cothon":
            S.append(f'<circle class="sym-cothon" cx="{x:.1f}" cy="{y:.1f}" r="30"/><circle class="sym-cothon-isle" cx="{x:.1f}" cy="{y:.1f}" r="9"/>')
            for a in range(7):
                ang = a * math.tau / 7 - math.pi / 2
                S.append(f'<line class="sym-quay" x1="{x + 30 * math.cos(ang):.1f}" y1="{y + 30 * math.sin(ang):.1f}" x2="{x + 22 * math.cos(ang):.1f}" y2="{y + 22 * math.sin(ang):.1f}"/>')
        elif kind == "citadel":
            S.append(f'<path class="sym-citadel" d="M{x - 18:.1f} {y + 11:.1f}L{x - 18:.1f} {y - 7:.1f}L{x - 10:.1f} {y - 13:.1f}L{x + 10:.1f} {y - 13:.1f}L{x + 18:.1f} {y - 7:.1f}L{x + 18:.1f} {y + 11:.1f}Z"/>')
        elif kind == "strait":
            S.append(f'<circle class="sym-strait" cx="{x:.1f}" cy="{y:.1f}" r="22"/>')
        elif kind == "cliff":
            for k in range(-3, 4):
                S.append(f'<line class="sym-cliff" x1="{x + k * 9:.1f}" y1="{y - 9:.1f}" x2="{x + k * 9 + 4:.1f}" y2="{y + 9:.1f}"/>')
        for px, py in pts[(1 if kind in ("round", "cothon", "citadel", "strait", "cliff") else 0):]:
            S.append(f'<circle class="sym-dot" cx="{px / U:.1f}" cy="{py / U:.1f}" r="7"/>')
        lx, ly = pts[0][0] / U, pts[0][1] / U
        off = {"round": 20, "cothon": 34, "strait": 24, "citadel": 22, "cliff": 30}.get(kind, 10)
        S.append(f'<g class="tag"><circle class="num-bg" cx="{lx + off + 14:.1f}" cy="{ly - off * .5 - 6:.1f}" r="15"/>'
                 f'<text class="num" x="{lx + off + 14:.1f}" y="{ly - off * .5 + 1:.1f}">{num}</text></g>')
        S.append('</g>')
    # compass + scale (1 km and 5 stadia at 185 m)
    S.append('<g class="furniture"><g transform="translate(1520 90)"><path class="compass" d="M0 -38L9 6L0 0L-9 6Z"/>'
             '<text class="compass-n" x="0" y="-46">N</text></g>'
             '<g transform="translate(60 1050)"><rect class="scale-bg" x="-14" y="-44" width="300" height="66" rx="3"/>'
             '<path class="scale" d="M0 0H200M0 -7V7M100 -5V5M200 -7V7"/>'
             '<text class="scale-t" x="0" y="-14">0</text><text class="scale-t" x="200" y="-14">1 km</text>'
             f'<path class="scale st" d="M0 10H{5 * 185 / U:.1f}"/><text class="scale-t sm" x="{5 * 185 / U + 8:.1f}" y="16">5 stadia</text></g></g>')
    S.append('</svg>')
    return "\n".join(S)

SVG_STYLE = """<style>
.sea0{fill:#8fbccd}.sea1{fill:#a9cdd8}.sea2{fill:#c3dde1}
.wline{fill:none;stroke:#136f9e;stroke-width:1}.wl0{opacity:.5}.wl1{opacity:.3}.wl2{opacity:.16}
.land0{fill:#eee0b0}.land1{fill:#e2d59b}.land2{fill:#cfcb8c}.land3{fill:#b6b87d}.land4{fill:#a0a670}.land5{fill:#bfae8f}.land6{fill:#ddd2c0}
.coast{stroke:#1c1512;stroke-width:2.2;stroke-linejoin:round}.contour{stroke:#1c1512;stroke-opacity:.22;stroke-width:.8}
.road{fill:none;stroke-linecap:round;stroke-linejoin:round}.walk{stroke:#faf3e0;stroke-width:5}.walk-dots{stroke:#1c1512;stroke-width:4.2;stroke-dasharray:0 9}
.track{stroke:#6b5a43;stroke-width:1.4;stroke-dasharray:5 4}
.house{fill:#bf4a26;stroke:#1c1512;stroke-width:.6}
.sym-round{fill:#f8f5ee;stroke:#1c1512;stroke-width:2.4}.sym-round-in{fill:#e2cf9b;stroke:#1c1512;stroke-width:1}.sym-gate{fill:#c1912b;stroke:#1c1512;stroke-width:1}
.sym-cothon{fill:#7fb2c8;stroke:#1c1512;stroke-width:2.2}.sym-cothon-isle{fill:#f8f5ee;stroke:#1c1512;stroke-width:1.4}.sym-quay{stroke:#1c1512;stroke-width:2}
.sym-citadel{fill:#8e2323;stroke:#1c1512;stroke-width:1.6}.sym-strait{fill:none;stroke:#8e2323;stroke-width:2.2;stroke-dasharray:4 3}
.sym-cliff{stroke:#1c1512;stroke-width:2}.sym-dot{fill:#1c1512;stroke:#faf3e0;stroke-width:1.5}
.num-bg{fill:#1c1512}.num{fill:#ffe36e;font:700 19px Optima,'Gill Sans',sans-serif;text-anchor:middle}
.compass{fill:#1c1512}.compass-n,.scale-t{fill:#1c1512;font:700 22px Optima,'Gill Sans',sans-serif;text-anchor:middle}.scale-t.sm{font-size:17px;text-anchor:start;font-weight:400}
.scale-bg{fill:#faf3e0;fill-opacity:.85;stroke:#1c1512;stroke-width:1}.scale{fill:none;stroke:#1c1512;stroke-width:2}.scale.st{stroke-width:4;stroke:#bf4a26}
</style>"""

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1:] or list(OPTIONS)
    html_path = ROOT / "art-direction-grand.html"
    html = html_path.read_text() if html_path.exists() else None
    for key in only:
        title, h, loc = build(key)
        report = {}
        for num, skey, name, vols, kind in SITES:
            v = loc[skey]
            pts = v if isinstance(v, list) else [v]
            report[skey] = {"num": num, "name": name, "volumes": [VOL_ROMAN[int(x)] for x in vols.split()],
                            "points_m": [[round(px), round(py), round(h_at(h, px, py), 1)] for px, py in pts]}
        svg = svg_for(key, title, h, loc, loc)
        (OUT / f"option-{key}.svg").write_text(svg.replace(">", ">" + SVG_STYLE, 1))
        png = np.clip((h - HMIN) / (HMAX - HMIN), 0, 1) * 65535
        Image.fromarray(png.astype(np.uint16)).save(OUT / f"option-{key}-height.png")
        land = (h > 0).mean() * W * H / 1e6
        ck = checks(h, loc)
        print(f"    checks: hamlets seen {ck['hamlets_mutually_visible'] or 'none'} | banquet {ck['banquet_visible_from_round']}"
              f" | sea from Round {ck['round_sea_bearings']}° two-sided {ck['round_sea_two_sided']} {ck['round_sea_arcs']} | signals {ck['signal_pairs_clear']}"
              f" | harbour seen {ck['town_to_round_clear']} | walk {math.dist(loc['town'], loc['round']):.0f} m")
        meta = {"option": key, "title": title, "world_m": [W, H], "cell_m": CELL,
                "height_png_range_m": [HMIN, HMAX], "land_km2": round(land, 2),
                "summit_m": round(float(h.max())), "checks": ck, "sites": report}
        (OUT / f"option-{key}-sites.json").write_text(json.dumps(meta, indent=1))
        print(f"[{key}] {title}: land {land:.1f} km², summit {h.max():.0f} m")
        for skey, r in report.items():
            print(f"    {r['num']:>2} {skey:9s}", " ".join(f"{p[2]:>6.1f}" for p in r["points_m"]))
        if html:
            rp, tp, bp = (report[k_]["points_m"][0] for k_ in ("round", "town", "banquet"))
            stats = (f'<dl class="stats"><div><dt>Land</dt><dd>{land:.1f} km²</dd></div>'
                     f'<div><dt>Summit</dt><dd>{h.max():.0f} m</dd></div>'
                     f'<div><dt>The Round sits at</dt><dd>{rp[2]:.0f} m</dd></div>'
                     f'<div><dt>Harbour → Round</dt><dd>{math.dist(tp[:2], rp[:2]) / 1000:.2f} km, {rp[2] - tp[2]:.0f} m climb</dd></div>'
                     f'<div><dt>Banquet house</dt><dd>{math.dist(bp[:2], rp[:2]):.0f} m east, {rp[2] - bp[2]:.0f} m below</dd></div>'
                     f'<div><dt>Sea seen from the Round</dt><dd>{ck["round_sea_bearings"]}° of horizon</dd></div>'
                     + "".join(f'<div class="ck {"pass" if ok else "fail"}"><dt>{label}</dt><dd>{"✓ yes" if ok else "✗ no"}</dd></div>'
                               for label, ok in (("Sea on both sides of the Round", ck["round_sea_two_sided"]),
                                                 ("Harbour in view from the Round", ck["town_to_round_clear"]),
                                                 ("Banquet house in view from the tiers", ck["banquet_visible_from_round"]),
                                                 ("Hamlets out of each other's sight", not ck["hamlets_mutually_visible"]),
                                                 ("Beacons in sight across the water", ck["signal_pairs_clear"][0] == ck["signal_pairs_clear"][1])))
                     + '</dl>')
            thumb = (f'<svg class="thumb" viewBox="0 0 1600 1100" aria-hidden="true"><rect class="t-sea" width="1600" height="1100"/>'
                     f'<path class="t-land" fill-rule="evenodd" d="{loops_to_d(march(h, 0), 3.0, 60)}"/>'
                     f'<circle class="t-round" cx="{rp[0] / U:.0f}" cy="{rp[1] / U:.0f}" r="34"/></svg>')
            for tag, body in (("MAP", svg), ("STATS", stats), ("THUMB", thumb)):
                html = re.sub(rf"(<!-- {tag}:{key} -->).*?(<!-- /{tag}:{key} -->)",
                              lambda mo: mo.group(1) + "\n" + body + "\n" + mo.group(2), html, flags=re.S)
    if html: html_path.write_text(html)

if __name__ == "__main__":
    main()
