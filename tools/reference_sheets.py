"""Regenerate reference sheets with the Gemini API (gemini-3-pro-image), by editing the existing sheet so its
characters and drawing style carry over and only what the canon changed is redrawn.

  python3 tools/reference_sheets.py edit <name>            one attempt -> temp/references/<name>-aN.jpg
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
LEDGER = ("THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends, "
          "like an ancient Greek book-roll with a rod at each end. It is never a bound codex book: no covers, no spine, no pages. Closed, the "
          "two rolls sit side by side, tied with a cord and a small wax seal tag. Open, it is held horizontally with one rod in each hand, the "
          "parchment stretched between them showing a few columns of dark brown iron-gall ink lines (illegible squiggles, no real letters).")
NO_TEXT = "No readable words, letters or digits anywhere; keep any existing numbered circles as they are."

EDITS = {
    "IV-ledger": f"{STYLE}\n{LEDGER}\nRedraw every ledger study on this sheet as that scroll instead of a codex book, one study per existing slot: "
                 "(1) the closed ledger, both rolls tied with a cord and a wax seal tag bearing a dolphin emblem, carried by a leather strap; "
                 "(2) the ledger held open between its two rods, columns of neat ink entries with small red dots in the margin; "
                 "(3) open, with some entries struck through in red; (4) keep the torn tally scrap exactly as it is; "
                 "(5) open, with a meander (Greek key) border ruled around one column; (6) closed, with small coloured tags hanging from the rod ends as bookmarks. "
                 f"{NO_TEXT}",
    "IV-benches": f"{STYLE}\n{LEDGER}\nKeep all seven legislators exactly as drawn (faces, clothing, poses, bags). Replace every red codex book they hold "
                  "or carry with the closed ledger scroll: two wooden rods rolled together, tied with a cord, carried in the same hand or tucked under the same arm. "
                  f"The elder handing a ledger to the youth now hands over a closed scroll. {NO_TEXT}",
    "IV-legislators": f"{STYLE}\n{LEDGER}\nKeep all five legislators exactly as drawn (faces, clothing, poses, the hourglass, the stone seat). Replace each red codex "
                      "book in a shoulder bag with the closed ledger scroll's two rod ends poking out of the bag. The old man reading on the right now holds the ledger "
                      f"open between its two rods in both hands, reading the parchment stretched between them. {NO_TEXT}",
    "IV-symbols": f"{STYLE}\nIn the bottom row of round pictograms, the ninth circle shows a small brown book with a leaf: redraw only that pictogram as a small "
                  "parchment scroll wound on two rods (the ledger) with the same leaf. Everything else on the sheet stays identical. " + NO_TEXT,
}

def call(prompt, image_path):
    body = {"model": MODEL,
            "input": [{"type": "text", "text": prompt},
                      {"type": "image", "mime_type": "image/jpeg", "data": base64.b64encode(image_path.read_bytes()).decode()}],
            "response_format": {"type": "image", "mime_type": "image/jpeg", "aspect_ratio": "16:9", "image_size": "2K"}}
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
        dst.write_bytes(call(EDITS[name], REFS / f"{name}.jpg"))
        print(dst)
    elif cmd == "accept":
        from PIL import Image
        Image.open(sys.argv[3]).convert("RGB").save(REFS / f"{name}.jpg", quality=92)
        print(REFS / f"{name}.jpg")

if __name__ == "__main__":
    main()
