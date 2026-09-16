#!/usr/bin/env python3
"""Stage 2, the painted map. The painting is made by hand in the Gemini web UI from the prompt in
prompts/painted-map.md; this tool prepares the upload and registers what comes back.

  python3 tools/painted_map.py reference
      maps/island-reference.svg -> maps/island-reference.png, 2200 x 1650 (4:3).
      The 11:8 map is letterboxed with 125 m of sea top and bottom, because 4:3 is the
      nearest ratio the image model offers.

  python3 tools/painted_map.py register <downloaded image>
      Scales the painting to the 4:3 frame, crops the letterbox back off, and writes
      maps/island-painted.jpg (2200 x 1600, the same frame as island.svg and the heightmap).
      Then measures how well its coastline sits on the heightmap's, writes maps/island-painted.json
      and island-painted-mismatch.png, and puts the scores in the page between its PAINTED markers.
"""
import json, re, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "maps"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
VW, VH = 2200, 1600                      # island.svg viewBox, 5 m per unit
PAD = 25                                 # units of sea above and below: 1650 / 2200 = 3:4
SEA = (143, 188, 205)                    # .sea0 in the map style
HMIN, HMAX, CELL = -120.0, 480.0, 12.5
TOLERANCE_M = 50.0

def reference():
    with tempfile.TemporaryDirectory() as tmp:
        shot = Path(tmp) / "ref.png"
        subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", f"--window-size={VW},{VH}",
                        f"--screenshot={shot}", (MAPS / "island-reference.svg").as_uri()],
                       check=True, capture_output=True, timeout=120)
        img = Image.open(shot).convert("RGB")
    assert img.size == (VW, VH), f"Chrome rendered {img.size}, expected {(VW, VH)}"
    out = Image.new("RGB", (VW, VH + 2 * PAD), SEA)
    out.paste(img, (0, PAD))
    out.save(MAPS / "island-reference.png", optimize=True)
    print(f"maps/island-reference.png  {out.size[0]} x {out.size[1]}")

def land_mask_from_painting(img):
    """Water is blue-dominant (deep sea, turquoise) or a pale sea-green wash (green over red, blue only a
    little under red). Land runs warm: beaches, fields and roofs have red above blue by a wide margin,
    and even hill greens sit far lower in blue."""
    a = np.asarray(img.convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return ~((b > r + 5) | ((g > r + 8) & (b > r - 30) & (r + g + b > 450)))

def grow(mask, cells):
    k = cells
    c = np.pad(mask.astype(np.int32), ((k + 1, k), (k + 1, k))).cumsum(0).cumsum(1)
    return (c[2 * k + 1:, 2 * k + 1:] - c[:-2 * k - 1, 2 * k + 1:] - c[2 * k + 1:, :-2 * k - 1] + c[:-2 * k - 1, :-2 * k - 1]) > 0

def register(path):
    raw = Image.open(path).convert("RGB")
    w, h = raw.size
    ratio = w / h
    if abs(ratio - 4 / 3) > .01:
        print(f"  ! the painting is {w} x {h} ({ratio:.3f}), not 4:3 (1.333); it will be stretched to fit, check the score")
    framed = raw.resize((VW * 2, (VH + 2 * PAD) * 2), Image.LANCZOS)          # 2 px per map unit
    painted = framed.crop((0, PAD * 2, VW * 2, (VH + PAD) * 2))
    painted.resize((VW, VH), Image.LANCZOS).save(MAPS / "island-painted.jpg", quality=88)
    height = np.asarray(Image.open(MAPS / "island-height.png")).astype(float)
    land = height / 65535 * (HMAX - HMIN) + HMIN > 0                            # 640 x 880 cells
    ny, nx = land.shape
    paint_land = land_mask_from_painting(painted.resize((nx, ny), Image.BOX))
    iou = (land & paint_land).sum() / (land | paint_land).sum()
    k = int(TOLERANCE_M / CELL)
    wrong = land != paint_land
    beyond = wrong & ~(grow(land, k) & grow(~land, k))                            # disagreement more than 50 m from the true coast
    report = {"source": str(Path(path).name), "source_px": [w, h], "land_iou": round(float(iou), 4),
              "cells_wrong_pct": round(100 * float(wrong.mean()), 2),
              "cells_wrong_beyond_50m_pct": round(100 * float(beyond.mean()), 2),
              "registered": "maps/island-painted.jpg (2200 x 1600, same frame as island.svg)"}
    (MAPS / "island-painted.json").write_text(json.dumps(report, indent=1))
    Image.fromarray(np.where(beyond[..., None], [191, 74, 38], np.where(land[..., None], [226, 213, 155], [143, 188, 205])).astype(np.uint8)) \
        .save(MAPS / "island-painted-mismatch.png")
    page = ROOT / "art-direction-grand-island-shape.html"
    rows = [("Source image", f"{w} × {h} px"), ("Land overlap (IoU) with the heightmap", f"{iou:.3f}"),
            ("Cells where land/sea disagree", f"{report['cells_wrong_pct']}%"),
            ("…more than 50 m from the true coast", f"{report['cells_wrong_beyond_50m_pct']}%")]
    block = '<dl class="stats">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows) + "</dl>"
    if page.exists():
        html = page.read_text()
        html = re.sub(r"(<!-- PAINTED -->).*?(<!-- /PAINTED -->)", lambda mo: mo.group(1) + "\n" + block + "\n" + mo.group(2), html, flags=re.S)
        page.write_text(html)
    print(json.dumps(report, indent=1))
    print("maps/island-painted-mismatch.png shows in terra red where the painting's coast strays more than 50 m")

if __name__ == "__main__":
    if sys.argv[1:2] == ["reference"]: reference()
    elif sys.argv[1:2] == ["register"] and len(sys.argv) == 3: register(sys.argv[2])
    else: sys.exit(__doc__)
