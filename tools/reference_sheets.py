"""Regenerate reference sheets with the Gemini API (gemini-3-pro-image), by editing the existing sheet so its
characters and drawing style carry over and only what the canon changed is redrawn.

  python3 tools/reference_sheets.py edit <name> [input]    one attempt -> temp/references/<name>-aN.jpg (input: an earlier attempt to refine;
                                                           then the prompt EDITS["<name>:fix"] is used when present)
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
NO_TEXT = "No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet."
CLOSED = ("A CLOSED ledger shows TWO separate parchment rolls lying side by side and touching, each wound on its own wooden rod with a knob "
          "at both ends (four knobs in all), tied together with a cord; it must not look like a single roll.")

EDITS = {
    "IV-ledger": f"{STYLE}\n{LEDGER}\nRedraw every ledger study on this sheet as that scroll instead of a codex book, one study per existing slot: "
                 "(1) the closed ledger, both rolls tied with a cord and a wax seal tag bearing a dolphin emblem, carried by a leather strap; "
                 "(2) the ledger held open between its two rods, columns of neat ink entries with small red dots in the margin; "
                 "(3) open, with some entries struck through in red; (4) keep the torn tally scrap exactly as it is; "
                 "(5) open, with a meander (Greek key) border ruled around one column; (6) closed, with small coloured tags hanging from the rod ends as bookmarks. "
                 f"{NO_TEXT}",
    "IV-benches": f"{STYLE}\n{LEDGER}\n{CLOSED}\nKeep all seven legislators exactly as drawn (faces, clothing, poses, bags). Replace every red codex book they hold "
                  "or carry with the closed ledger scroll: two wooden rods rolled together, tied with a cord, carried in the same hand or tucked under the same arm. "
                  f"The elder handing a ledger to the youth now hands over a closed scroll. {NO_TEXT}",
    "IV-legislators": f"{STYLE}\n{LEDGER}\n{CLOSED}\nKeep all five legislators exactly as drawn (faces, clothing, poses, the hourglass, the stone seat). Remove "
                      "every rectangular red leather book entirely, including the ones clasped against the body or held in a bag: no book shapes may remain. "
                      "In its place each legislator carries a closed ledger (two rolls tied together) under the arm or with the knobbed rod ends poking up out of the shoulder bag. The old man reading on the right now holds the ledger "
                      f"open between its two rods in both hands, reading the parchment stretched between them. {NO_TEXT}",
    "IV-symbols": f"{STYLE}\nChange exactly one small thing. In row 4 (the row of round pictogram circles), the circle between the bunch of grapes and the "
                  "anchor contains a small closed brown book with a green leaf. Inside that same circle, replace the book with a tiny parchment scroll wound "
                  "on two wooden rods (drawn open a little between its two rods), keeping the green leaf. Do not add any new pictograms or circles. Keep the "
                  "small sun, crescent moon and star symbols at the far right of row 4 exactly where they are. Every other element stays identical. " + NO_TEXT,
    "IV-benches:fix": f"{STYLE}\n{LEDGER}\nThe sheet is correct except for one thing: the black-haired woman third from the left, in the olive green shawl, "
                      "carries no ledger. Add one: a ledger scroll on two rods, rolled up, held in her right hand in front of her shoulder bag, drawn like the "
                      "ledgers the others carry. Change nothing else, and keep every other figure's ledger exactly as it is. " + NO_TEXT,
    "IV-ledger:fix": f"{STYLE}\n{LEDGER}\n{CLOSED}\nStudies 1, 2, 3 and 4 are correct: keep them exactly. Studies 5 and 6 are still bound codex books and must become "
                     "scrolls: (5) the ledger lying open on a table between its two rolls, with a meander (Greek key) border ruled around one column of entries; "
                     "(6) the closed ledger (two rolls tied together) with small coloured cloth tags hanging from the rod knobs as markers and a round dolphin seal. "
                     "No covers, spines or pages anywhere on the sheet. " + NO_TEXT,
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
        src = Path(sys.argv[3]) if len(sys.argv) > 3 else REFS / f"{name}.jpg"
        prompt = EDITS.get(f"{name}:fix", EDITS[name]) if len(sys.argv) > 3 else EDITS[name]
        dst.write_bytes(call(prompt, src))
        print(dst)
    elif cmd == "accept":
        from PIL import Image
        Image.open(sys.argv[3]).convert("RGB").save(REFS / f"{name}.jpg", quality=92)
        print(REFS / f"{name}.jpg")

if __name__ == "__main__":
    main()
