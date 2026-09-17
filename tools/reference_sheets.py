"""Regenerate reference sheets with the Gemini API (gemini-3-pro-image), by editing the existing sheet so its
characters and drawing style carry over and only what the canon changed is redrawn.

  python3 tools/reference_sheets.py edit <name> [input]    one attempt -> temp/references/<name>-aN.jpg (input: an earlier attempt to refine;
                                                           then the prompt EDITS["<name>:fix"] is used when present)
  python3 tools/reference_sheets.py patch <name> <key> [input]   edit one region (PATCHES["<name>:<key>"]): the crop is sent alone, then
                                                           feathered back into the sheet, so everything outside it stays pixel-identical
  python3 tools/reference_sheets.py accept <name> <file>   copy an attempt into references/<name>.jpg (JPEG q92)

Prompts live in EDITS below and are recorded in prompts/reference-sheets.md. Needs GEMINI_API_KEY. Uses only the
standard library (REST Interactions API), so it runs with the system python3.
"""
import base64, json, os, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS, OUT = ROOT / "references", ROOT / "temp" / "references"
MODEL = "gemini-3-pro-image"

STYLE = ("Keep the exact drawing style of the attached sheet: vintage 1970s comic book reference sheet, bold black ink outlines, "
         "visible halftone dot shading, flat Mediterranean palette (aegean blue #136f9e, terracotta red #bf4a26, olive green #66722c, "
         "marble white, sand #f2e7cd, gold accents #c1912b, ink #1c1512) on cream paper. Keep the layout, framing and every element not "
         "mentioned below unchanged.")
LEDGER = ("THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends. "
          "It is never a bound codex book: no covers, no spine, no pages. It is written like a log: each entry is ONE short line of dark brown "
          "iron-gall ink (illegible squiggles, no real letters) running PARALLEL to the rods, and the entries follow one another from top to bottom "
          "down the length of the strip, the newest at the bottom. No side-by-side columns and no vertical lines of writing. Open, it is held "
          "VERTICALLY: one rod across the top and one across the bottom, both horizontal, the parchment hanging between them. Closed, the two "
          "rolls sit side by side, tied with a cord and a small wax seal tag.")
NO_TEXT = "No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet."
CLOSED = ("A CLOSED ledger shows TWO separate parchment rolls lying side by side and touching, each wound on its own wooden rod with a knob "
          "at both ends (four knobs in all), tied together with a cord; it must not look like a single roll.")

EDITS = {                                                                                           # 17 Sep 2026: entries written top to bottom, parallel to the rods
    "IV-ledger": f"{STYLE}\n{LEDGER}\nChange only the three OPEN ledger studies, (2), (3) and (5), so they follow the canon above. Keep studies (1), (4) and (6) "
                 "exactly as they are. (2) The ledger held open vertically, one hand gripping the top rod and the other the bottom rod, the parchment between "
                 "them filled with many short horizontal lines of entries stacked from top to bottom, each line parallel to the rods, with a small red dot in "
                 "the left margin beside each entry. (3) The same vertical ledger with some of those horizontal entry lines struck through in red. (5) The "
                 "ledger lying open on a table with one rod at the top and one at the bottom, a meander (Greek key) border ruled around the stack of "
                 f"horizontal entry lines. In each open study the strip is taller than it is wide. {NO_TEXT}",
    "IV-legislators": f"{STYLE}\n{LEDGER}\nKeep all five legislators exactly as drawn (faces, clothing, poses, the hourglass, the stone seat, and the ledgers the "
                      "first four carry). Change only the old man reading on the far right: he now holds his ledger open VERTICALLY in front of him, one hand "
                      "on the top rod and the other on the bottom rod, both rods horizontal, the parchment between them facing him and covered with short "
                      f"horizontal lines of entries stacked from top to bottom, parallel to the rods. {NO_TEXT}",
    "IV-benches": f"{STYLE}\n{LEDGER}\nKeep all seven legislators exactly as drawn (faces, clothing, poses, bags, and how each ledger is held). Change only the "
                  "writing on the open ledgers: the one carried by the woman in the red dress (second from left), the one carried by the woman in the tan "
                  "apron (fourth from left), the one carried by the young man in the robe with the Greek key border (far right), and the one the white-bearded "
                  "elder hands to the youth. On each, erase the vertical lines of writing and draw short HORIZONTAL lines of entries instead, parallel to the "
                  "two rods and stacked one under another from the top rod to the bottom rod. Each of those ledgers keeps one rod across its top and one "
                  f"across its bottom. Leave the rolled-up ledgers carried by the other figures unchanged. {NO_TEXT}",
    "IV-symbols": f"{STYLE}\nChange exactly one small thing. In row 4 (the row of round pictogram circles), the circle between the bunch of grapes and the "
                  "anchor contains a tiny scroll open between two vertical rods. Redraw that tiny scroll turned upright inside the same circle: its two rods "
                  "horizontal, one across the top and one across the bottom, and a few short horizontal ink lines on the parchment between them, parallel to "
                  "the rods. Do not add any new pictograms or circles. Keep the small sun, crescent moon and star symbols at the far right of row 4 exactly "
                  "where they are. Every other element stays identical. " + NO_TEXT,
}

CROP = ("This image is a close-up crop from a vintage 1970s comic book reference sheet: bold black ink outlines, halftone dot shading, flat "
        "colours on cream paper. Keep the crop's framing, everything at its edges, the line weight, halftone and colours exactly as they are; "
        "change only what is described.")
BLANK = ("Image 1 is a crop of a vintage 1970s comic book reference sheet in which the old drawing has been erased to plain cream paper. Draw the "
         "study described below into that empty space, in exactly the drawing style of image 2, the whole sheet: bold black ink outlines, halftone "
         "dot shading, the same colours, line weight and wood tones. Keep any circled number or outline already in image 1 where it is, and leave a "
         "margin of plain paper at the crop's edges.")
PATCHES = {                                                                                         # (x0, y0, x1, y1) in sheet pixels, prompt, erase first: None,
                                                                                                    # ("keep", [rects to keep]) or ("disc", cx, cy, r)
    "IV-ledger:2": ((905, 55, 1850, 780), f"{BLANK}\n{LEDGER}\nDraw study 2: the ledger held open UPRIGHT, centred in the space: one hand grips "
                   "the top rod and the other hand grips the bottom rod, both rods horizontal with knobbed ends like those in studies 1 and 6 of image 2, the "
                   "parchment between them taller than it is wide and filled with many short horizontal lines of entries stacked from top to bottom, parallel "
                   "to the rods, each with a small red dot in the left margin. Every entry is one thin handwritten squiggle in dark brown ink; no line is "
                   f"struck through, underlined or covered by a bar of any colour, and there is no red except the margin dots. {NO_TEXT}", ("keep", [(905, 55, 1003, 150)])),
    "IV-ledger:3": ((1840, 55, 2752, 780), f"{BLANK}\n{LEDGER}\nDraw study 3: the ledger held open UPRIGHT, centred in the space: one hand grips "
                   "the top rod and the other hand grips the bottom rod, both rods horizontal with knobbed ends like those in studies 1 and 6 of image 2, the "
                   "parchment between them taller than it is wide and filled with short horizontal lines of entries stacked from top to bottom, parallel to "
                   "the rods. Every entry is one thin handwritten squiggle in dark brown ink. Exactly four entries, spread down the strip, have a thin red "
                   f"line struck through them; no other line is struck through, underlined or covered by a bar of any colour. {NO_TEXT}", ("keep", [(1845, 55, 1948, 150)])),
    "IV-ledger:5": ((850, 790, 1992, 1536), f"{BLANK}\n{LEDGER}\nDraw study 5 in the middle of the space: the ledger lying open flat on a surface, seen "
                   "from above at a slight angle, UPRIGHT in the frame: one rod with knobbed ends across the top and one across the bottom, both horizontal "
                   "and like those in studies 1 and 6 of image 2, the parchment between them taller than it is wide, with a meander (Greek key) border ruled "
                   f"around a stack of short horizontal lines of entries running from top to bottom, parallel to the rods. {NO_TEXT}",
                   ("keep", [(850, 850, 950, 950), (1870, 845, 1965, 940)])),
    **{f"IV-benches:{who}": (box, f"{CROP}\nA hand holds a ledger scroll: a wooden rod across the top and one across the bottom, the parchment between "
                             "them. Redraw only the writing on that parchment: erase the vertical ink strokes and draw four or five short HORIZONTAL wavy "
                             "ink lines instead, stacked one under another from the top rod to the bottom rod, parallel to the rods. Keep the hand, the "
                             f"rods, any tag, the clothing and the background exactly as they are. {NO_TEXT}", None)
       for who, box in (("red", (440, 670, 760, 980)), ("apron", (1170, 680, 1490, 980)), ("key", (2430, 650, 2760, 920)))},
    "IV-symbols:scroll": ((1950, 1215, 2180, 1450), f"{BLANK}\nInside the empty black circle, draw one tiny round pictogram in the style of the "
                          "other pictograms in row 4 of image 2: a small parchment scroll standing UPRIGHT, its two wooden rods with knobbed ends horizontal, one "
                          "across the top and one across the bottom, the parchment between them taller than it is wide, with three or four short horizontal ink "
                          f"lines parallel to the rods. Keep the circle outline and the background identical. {NO_TEXT}", ("disc", 2064, 1333, 84)),
}
ASPECTS = {"1:1": 1, "4:3": 4 / 3, "3:4": 3 / 4, "3:2": 1.5, "2:3": 2 / 3, "5:4": 1.25, "4:5": .8, "16:9": 16 / 9, "9:16": 9 / 16, "21:9": 21 / 9}

def patch(sheet, key, prompt, box, dst, blank=None):
    """Crop `box` (grown to a Gemini aspect ratio), optionally erase the old drawing in it, edit the crop, match its paper tone to the
    sheet's, and feather the result back in."""
    from PIL import Image, ImageDraw, ImageFilter, ImageStat
    import io
    im = Image.open(sheet).convert("RGB"); W, H = im.size
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    aspect = min(ASPECTS, key=lambda a: abs(ASPECTS[a] - w / h)); r = ASPECTS[aspect]
    if w / h < r: g = round(h * r) - w; x0, x1 = max(0, x0 - g // 2), min(W, x1 + g - g // 2)
    else: g = round(w / r) - h; y0, y1 = max(0, y0 - g // 2), min(H, y1 + g - g // 2)
    crop = im.crop((x0, y0, x1, y1)); images = []
    border = lambda c: [ImageStat.Stat(c.crop(b)).median for b in ((0, 0, c.width, 8), (0, c.height - 8, c.width, c.height))]
    paper = tuple(int(sum(v) / 2) for v in zip(*border(crop)))
    if blank:
        erased = Image.new("RGB", crop.size, paper)
        if blank[0] == "keep":
            for kx0, ky0, kx1, ky1 in blank[1]:
                erased.paste(crop.crop((kx0 - x0, ky0 - y0, kx1 - x0, ky1 - y0)), (kx0 - x0, ky0 - y0))
        else:
            _, cx, cy, rr = blank; m = Image.new("L", crop.size, 255)
            ImageDraw.Draw(m).ellipse((cx - x0 - rr, cy - y0 - rr, cx - x0 + rr, cy - y0 + rr), fill=0)
            erased = Image.composite(crop, erased, m)
        crop = erased; im.paste(crop, (x0, y0))                                                     # erased under the seam too, or the feather shows the old drawing
    tmp = OUT / f"{key.replace(':', '-')}-crop.png"; crop.save(tmp); images.append(tmp)
    if blank:                                                                                       # the whole sheet as the style reference, with every region patched on
        style = im.copy()                                                                           # it erased, or the model copies those studies (strikes, old knobs)
        for k2, (b2, _, _) in PATCHES.items():
            if k2.split(":")[0] == key.split(":")[0]: style.paste(paper, b2)
        images.append(OUT / f"{key.replace(':', '-')}-style.png"); style.save(images[-1])
    out = Image.open(io.BytesIO(call(prompt, images, aspect))).convert("RGB").resize(crop.size, Image.LANCZOS)
    got = tuple(sum(v) / 2 for v in zip(*border(out)))                                               # match the paper tone before blending
    out = Image.merge("RGB", [ch.point(lambda v, k=paper[i] / max(got[i], 1): min(255, int(v * k))) for i, ch in enumerate(out.split())])
    f = max(6, min(crop.size) // 30)                                                                 # feather the seam
    mask = Image.new("L", crop.size, 0); mask.paste(255, (f, f, crop.size[0] - f, crop.size[1] - f)); mask = mask.filter(ImageFilter.GaussianBlur(f / 2))
    im.paste(out, (x0, y0), mask); im.save(dst, quality=95)

def call(prompt, images, aspect="16:9"):
    """One gemini-3-pro-image request: the prompt, then each image in order. Returns the last image's JPEG bytes."""
    images = [images] if isinstance(images, Path) else images
    mime = lambda p: "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    body = {"model": MODEL,
            "input": [{"type": "text", "text": prompt}] +
                     [{"type": "image", "mime_type": mime(p), "data": base64.b64encode(p.read_bytes()).decode()} for p in images],
            "response_format": {"type": "image", "mime_type": "image/jpeg", "aspect_ratio": aspect, "image_size": "2K"}}
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/interactions", data=json.dumps(body).encode(),
                                 headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"], "Content-Type": "application/json", "Api-Revision": "2026-05-20"})
    with urllib.request.urlopen(req, timeout=600) as r:
        resp = json.load(r)
    images = []
    def walk(o):
        if isinstance(o, dict):
            if o.get("type") == "image" and o.get("data"): images.append(o["data"])
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    walk(resp.get("steps", resp.get("outputs", resp)))
    if not images:
        raise SystemExit("no image in response: " + json.dumps(resp)[:1500])
    return base64.b64decode(images[-1])

def main():
    cmd, name = sys.argv[1], sys.argv[2]
    if cmd == "edit":
        OUT.mkdir(parents=True, exist_ok=True)
        n = 1 + len(list(OUT.glob(f"{name}-a*.jpg")))
        dst = OUT / f"{name}-a{n}.jpg"
        src = Path(sys.argv[3]) if len(sys.argv) > 3 else REFS / f"{name}.jpg"
        prompt = EDITS.get(f"{name}:fix", EDITS[name]) if len(sys.argv) > 3 else EDITS[name]
        dst.write_bytes(call(prompt, src))
        print(dst)
    elif cmd == "patch":
        OUT.mkdir(parents=True, exist_ok=True)
        key = f"{name}:{sys.argv[3]}"; box, prompt, blank = PATCHES[key]
        n = 1 + len(list(OUT.glob(f"{name}-a*.jpg")))
        dst = OUT / f"{name}-a{n}.jpg"
        patch(Path(sys.argv[4]) if len(sys.argv) > 4 else REFS / f"{name}.jpg", key, prompt, box, dst, blank)
        print(dst)
    elif cmd == "accept":
        from PIL import Image
        Image.open(sys.argv[3]).convert("RGB").save(REFS / f"{name}.jpg", quality=92)
        print(REFS / f"{name}.jpg")

if __name__ == "__main__":
    main()
