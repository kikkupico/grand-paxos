# Image references

These are reference sheets for characters, props and symbols, in the house comic style: ink outlines, halftone and the flat Mediterranean palette. Small props (the ledger, hourglass, abacus and so on) are not modelled in Blender. These sheets are their references when scene images are generated. Files are named by volume in walking order, and stored as full-resolution JPEG (quality 92).

| File | Volume | Contents |
|---|---|---|
| `I-characters.jpg` | I | The wandering scholar with an abacus, two shepherds with a goat and a ram, and two messengers with clay slates. |
| `I-props.jpg` | I | Water-clock, handheld abacus, vector abacus, horizontal bronze sundial, olive press, clay message slates and wax tokens, oil lamps, and a scroll case. |
| `III-characters.jpg` | III | A navigator with a sea chart, a pilot with a sounding line, a youth with an astrolabe, an official with a lantern, and a drummer. |
| `III-props.jpg` | III | Five sand-timers in increasing sizes, a signal lantern, a sounding line and weight, an astrolabe, a parchment sea chart, harbour bollards with tokens, a semicircular sundial, and a voting urn. |
| `IV-benches.jpg` | IV | Seven legislators, each with a shoulder bag and a ledger scroll. |
| `IV-legislators.jpg` | IV | Five legislators: one with an hourglass, one gesturing, one seated on a stone seat, one reading a ledger held open between its rods. |
| `IV-ledger.jpg` | IV | Ledger studies: the scroll on two rods, closed and open, with ruled and struck-through entries, plus a tally scrap. |
| `IV-messengers.jpg` | IV | Three messengers with scrolls, and a dropped satchel and scroll. |
| `IV-symbols.jpg` | IV | Sealed scrolls and tablets, seals and tokens, five emblem coins, and a row of pictograms (olive, lamp, goat, cheese, grapes, anchor and more). |
| `IV-townsfolk.jpg` | IV | Townsfolk: cheese seller, water carrier, mothers and children, a fisherwoman, a rope-maker, an old man, a flute player, a youth with a vase, and a hoplite. |

## Architecture
There are no architecture sheets. Buildings, harbours and terrain come from the Blender scene, which is the reference for every place.

## Kept to the canon
The canon on `art-direction-grand-island-shape.html` wins. **The ledger is a parchment scroll on two rods**, not a bound codex. These four sheets were edited from their earlier versions with `tools/reference_sheets.py` (Gemini API, `gemini-3-pro-image`). The edits kept each sheet's people and style and redrew only the ledgers. The prompts are in `prompts/reference-sheets.md`.

| Sheet | What changed | Attempts |
|---|---|---|
| `IV-ledger.jpg` | All six studies are now scrolls: closed on a strap with a dolphin seal; held open; open with struck entries; open with a meander border; closed with cloth markers. The tally scrap is unchanged. | 2. The first attempt left studies 5 and 6 as codex books; the second fixed them from the first. |
| `IV-benches.jpg` | All seven legislators carry a two-rod ledger; the elder hands an open one to the youth. | 4. The first attempt drew single rolls and added numbers; the second dropped the ledgers of two figures, which the third and fourth restored one at a time. |
| `IV-legislators.jpg` | The books in their bags became two-rod ledgers, and the reader holds one open. The hourglass and stone seat are kept. | 2. The first attempt left the books in place. |
| `IV-symbols.jpg` | The book pictogram (between the grapes and the anchor) is now a small two-rod scroll. | 2. The first attempt left the book and replaced the sun, moon and star instead. |
