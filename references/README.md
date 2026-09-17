# Image references

These are reference sheets for characters, props and symbols, in the house comic style: ink outlines, halftone and the flat Mediterranean palette. Small props (the ledger, hourglass, abacus and so on) are not modelled in Blender. These sheets are their references when scene images are generated. Files are named by volume in walking order, and stored as full-resolution JPEG (quality 92).

| File | Volume | Contents |
|---|---|---|
| `I-characters.jpg` | I | The wandering scholar with an abacus, two shepherds with a goat and a ram, and two messengers with clay slates. |
| `I-props.jpg` | I | Water-clock, handheld abacus, vector abacus, horizontal bronze sundial, olive press, clay message slates and wax tokens, oil lamps, and a scroll case. |
| `III-characters.jpg` | III | A navigator with a sea chart, a pilot with a sounding line, a youth with an astrolabe, an official with a lantern, and a drummer. |
| `III-props.jpg` | III | Five sand-timers in increasing sizes, a signal lantern, a sounding line and weight, an astrolabe, a parchment sea chart, harbour bollards with tokens, a semicircular sundial, and a voting urn. |
| `IV-benches.jpg` | IV | Seven legislators, each with a shoulder bag and a ledger scroll. |
| `IV-legislators.jpg` | IV | Five legislators: one with an hourglass, one gesturing, one seated on a stone seat, one reading a ledger held open upright between its rods. |
| `IV-ledger.jpg` | IV | Ledger studies: the scroll on two rods, closed, and open upright with entries written top to bottom (ruled, struck through, and with a meander border), plus a tally scrap. |
| `IV-messengers.jpg` | IV | Three messengers with scrolls, and a dropped satchel and scroll. |
| `IV-symbols.jpg` | IV | Sealed scrolls and tablets, seals and tokens, five emblem coins, and a row of pictograms (olive, lamp, goat, cheese, grapes, anchor and more). |
| `IV-townsfolk.jpg` | IV | Townsfolk: cheese seller, water carrier, mothers and children, a fisherwoman, a rope-maker, an old man, a flute player, a youth with a vase, and a hoplite. |

## Architecture
There are no architecture sheets. Buildings, harbours and terrain come from the Blender scene, which is the reference for every place.

## Kept to the canon
The canon on `art-direction-grand-island-shape.html` wins. **The ledger is a parchment scroll on two rods**, not a bound codex, **written like a log** (user, 17 Sep 2026). Each entry is one line parallel to the rods, entries run top to bottom down the strip with no side-by-side columns, and open it is held upright, one rod across the top and one across the bottom. These four sheets were edited with `tools/reference_sheets.py` (Gemini API, `gemini-3-pro-image`). The edits kept each sheet's people and style and redrew only the ledgers. The prompts are in `prompts/reference-sheets.md`.

### Written top to bottom (17 Sep 2026)

Whole-sheet edits ignore small details, so three sheets were changed with `patch`. It edits one region of a sheet and feathers the result back in, so everything outside that region stays pixel-identical. For a study that needs redrawing rather than touching up, the old drawing is first erased to plain paper, in the crop and in the style copy of the sheet sent with it. The sheet is also erased under the crop, so the feathered seam can't show the old drawing, and every region patched on that sheet is blanked in the style image, so the model doesn't copy those studies.

| Sheet | What changed | Attempts |
|---|---|---|
| `IV-ledger.jpg` | Studies 2, 3 and 5 are now upright: held by the top and bottom rods (plain, then with four entries struck through in red), and lying flat with a meander border, each with entries stacked top to bottom. Studies 1, 4 and 6 are unchanged. | About 12 calls. The whole-sheet edit changed nothing useful, and patching without erasing kept study 5 sideways. With the old study still under the seam, the feather showed ghost knobs and hands. Study 2 kept copying study 3's strike-throughs until every patched study was blanked in the style image as well. The circled numbers 2 and 3 were clipped by the erase and copied back pixel for pixel from the previous sheet. Left as is: study 2's hands are drawn darker and its entry lines repeat, and study 5 has a few heavier lines. |
| `IV-legislators.jpg` | The reader on the right holds his ledger upright, one hand on each rod, lines running across. The carried ledgers already had their rods across the top and bottom. | 1, a whole-sheet edit. |
| `IV-benches.jpg` | The open ledgers carried by the women in red and in the apron and by the young man in the meander robe had writing running across the rods. It now runs parallel to them. The elder's ledger already did. | A whole-sheet edit changed nothing. Then 3 patches, one per ledger. |
| `IV-symbols.jpg` | The scroll pictogram (between the grapes and the anchor) is upright, with lines parallel to its rods. | A whole-sheet edit and a plain patch kept the rods vertical. Erasing the circle's inside first worked. |

### Scroll on two rods (16 Sep 2026)

| Sheet | What changed | Attempts |
|---|---|---|
| `IV-ledger.jpg` | All six studies are now scrolls: closed on a strap with a dolphin seal; held open; open with struck entries; open with a meander border; closed with cloth markers. The tally scrap is unchanged. | 2. The first attempt left studies 5 and 6 as codex books; the second fixed them from the first. |
| `IV-benches.jpg` | All seven legislators carry a two-rod ledger; the elder hands an open one to the youth. | 4. The first attempt drew single rolls and added numbers; the second dropped the ledgers of two figures, which the third and fourth restored one at a time. |
| `IV-legislators.jpg` | The books in their bags became two-rod ledgers, and the reader holds one open. The hourglass and stone seat are kept. | 2. The first attempt left the books in place. |
| `IV-symbols.jpg` | The book pictogram (between the grapes and the anchor) is now a small two-rod scroll. | 2. The first attempt left the book and replaced the sun, moon and star instead. |
