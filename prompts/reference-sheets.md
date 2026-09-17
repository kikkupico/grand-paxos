# Reference sheet edits (Gemini API)

`tools/reference_sheets.py` edits the sheets in `references/` with `gemini-3-pro-image`, writing attempts to `temp/references/`:

- `edit <name> [input]` sends a whole sheet and its `EDITS` prompt (16:9, 2K).
- `patch <name> <key> [input]` sends one region with its `PATCHES` prompt and feathers the result back in. Everything outside the region stays pixel-identical. With an erase spec, the old drawing is first erased to paper in the crop and in the sheet sent as the style reference.
- `accept <name> <file>` copies an attempt into `references/`.

These are the prompts for the 17 Sep 2026 change (ledgers written top to bottom). The earlier codex-to-scroll prompts are in git history.

## Canon block (`LEDGER`)

```text
THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends. It is never a bound codex book: no covers, no spine, no pages. It is written like a log: each entry is ONE short line of dark brown iron-gall ink (illegible squiggles, no real letters) running PARALLEL to the rods, and the entries follow one another from top to bottom down the length of the strip, the newest at the bottom. No side-by-side columns and no vertical lines of writing. Open, it is held VERTICALLY: one rod across the top and one across the bottom, both horizontal, the parchment hanging between them. Closed, the two rolls sit side by side, tied with a cord and a small wax seal tag.
```

## edit IV-ledger

```text
Keep the exact drawing style of the attached sheet: vintage 1970s comic book reference sheet, bold black ink outlines, visible halftone dot shading, flat Mediterranean palette (aegean blue #136f9e, terracotta red #bf4a26, olive green #66722c, marble white, sand #f2e7cd, gold accents #c1912b, ink #1c1512) on cream paper. Keep the layout, framing and every element not mentioned below unchanged.
THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends. It is never a bound codex book: no covers, no spine, no pages. It is written like a log: each entry is ONE short line of dark brown iron-gall ink (illegible squiggles, no real letters) running PARALLEL to the rods, and the entries follow one another from top to bottom down the length of the strip, the newest at the bottom. No side-by-side columns and no vertical lines of writing. Open, it is held VERTICALLY: one rod across the top and one across the bottom, both horizontal, the parchment hanging between them. Closed, the two rolls sit side by side, tied with a cord and a small wax seal tag.
Change only the three OPEN ledger studies, (2), (3) and (5), so they follow the canon above. Keep studies (1), (4) and (6) exactly as they are. (2) The ledger held open vertically, one hand gripping the top rod and the other the bottom rod, the parchment between them filled with many short horizontal lines of entries stacked from top to bottom, each line parallel to the rods, with a small red dot in the left margin beside each entry. (3) The same vertical ledger with some of those horizontal entry lines struck through in red. (5) The ledger lying open on a table with one rod at the top and one at the bottom, a meander (Greek key) border ruled around the stack of horizontal entry lines. In each open study the strip is taller than it is wide. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## edit IV-legislators

```text
Keep the exact drawing style of the attached sheet: vintage 1970s comic book reference sheet, bold black ink outlines, visible halftone dot shading, flat Mediterranean palette (aegean blue #136f9e, terracotta red #bf4a26, olive green #66722c, marble white, sand #f2e7cd, gold accents #c1912b, ink #1c1512) on cream paper. Keep the layout, framing and every element not mentioned below unchanged.
THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends. It is never a bound codex book: no covers, no spine, no pages. It is written like a log: each entry is ONE short line of dark brown iron-gall ink (illegible squiggles, no real letters) running PARALLEL to the rods, and the entries follow one another from top to bottom down the length of the strip, the newest at the bottom. No side-by-side columns and no vertical lines of writing. Open, it is held VERTICALLY: one rod across the top and one across the bottom, both horizontal, the parchment hanging between them. Closed, the two rolls sit side by side, tied with a cord and a small wax seal tag.
Keep all five legislators exactly as drawn (faces, clothing, poses, the hourglass, the stone seat, and the ledgers the first four carry). Change only the old man reading on the far right: he now holds his ledger open VERTICALLY in front of him, one hand on the top rod and the other on the bottom rod, both rods horizontal, the parchment between them facing him and covered with short horizontal lines of entries stacked from top to bottom, parallel to the rods. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## edit IV-benches

```text
Keep the exact drawing style of the attached sheet: vintage 1970s comic book reference sheet, bold black ink outlines, visible halftone dot shading, flat Mediterranean palette (aegean blue #136f9e, terracotta red #bf4a26, olive green #66722c, marble white, sand #f2e7cd, gold accents #c1912b, ink #1c1512) on cream paper. Keep the layout, framing and every element not mentioned below unchanged.
THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends. It is never a bound codex book: no covers, no spine, no pages. It is written like a log: each entry is ONE short line of dark brown iron-gall ink (illegible squiggles, no real letters) running PARALLEL to the rods, and the entries follow one another from top to bottom down the length of the strip, the newest at the bottom. No side-by-side columns and no vertical lines of writing. Open, it is held VERTICALLY: one rod across the top and one across the bottom, both horizontal, the parchment hanging between them. Closed, the two rolls sit side by side, tied with a cord and a small wax seal tag.
Keep all seven legislators exactly as drawn (faces, clothing, poses, bags, and how each ledger is held). Change only the writing on the open ledgers: the one carried by the woman in the red dress (second from left), the one carried by the woman in the tan apron (fourth from left), the one carried by the young man in the robe with the Greek key border (far right), and the one the white-bearded elder hands to the youth. On each, erase the vertical lines of writing and draw short HORIZONTAL lines of entries instead, parallel to the two rods and stacked one under another from the top rod to the bottom rod. Each of those ledgers keeps one rod across its top and one across its bottom. Leave the rolled-up ledgers carried by the other figures unchanged. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## edit IV-symbols

```text
Keep the exact drawing style of the attached sheet: vintage 1970s comic book reference sheet, bold black ink outlines, visible halftone dot shading, flat Mediterranean palette (aegean blue #136f9e, terracotta red #bf4a26, olive green #66722c, marble white, sand #f2e7cd, gold accents #c1912b, ink #1c1512) on cream paper. Keep the layout, framing and every element not mentioned below unchanged.
Change exactly one small thing. In row 4 (the row of round pictogram circles), the circle between the bunch of grapes and the anchor contains a tiny scroll open between two vertical rods. Redraw that tiny scroll turned upright inside the same circle: its two rods horizontal, one across the top and one across the bottom, and a few short horizontal ink lines on the parchment between them, parallel to the rods. Do not add any new pictograms or circles. Keep the small sun, crescent moon and star symbols at the far right of row 4 exactly where they are. Every other element stays identical. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## patch IV-ledger:2

Region (905, 55, 1850, 780), erased first (keep ([(905, 55, 1003, 150)],)).

```text
Image 1 is a crop of a vintage 1970s comic book reference sheet in which the old drawing has been erased to plain cream paper. Draw the study described below into that empty space, in exactly the drawing style of image 2, the whole sheet: bold black ink outlines, halftone dot shading, the same colours, line weight and wood tones. Keep any circled number or outline already in image 1 where it is, and leave a margin of plain paper at the crop's edges.
THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends. It is never a bound codex book: no covers, no spine, no pages. It is written like a log: each entry is ONE short line of dark brown iron-gall ink (illegible squiggles, no real letters) running PARALLEL to the rods, and the entries follow one another from top to bottom down the length of the strip, the newest at the bottom. No side-by-side columns and no vertical lines of writing. Open, it is held VERTICALLY: one rod across the top and one across the bottom, both horizontal, the parchment hanging between them. Closed, the two rolls sit side by side, tied with a cord and a small wax seal tag.
Draw study 2: the ledger held open UPRIGHT, centred in the space: one hand grips the top rod and the other hand grips the bottom rod, both rods horizontal with knobbed ends like those in studies 1 and 6 of image 2, the parchment between them taller than it is wide and filled with many short horizontal lines of entries stacked from top to bottom, parallel to the rods, each with a small red dot in the left margin. Every entry is one thin handwritten squiggle in dark brown ink; no line is struck through, underlined or covered by a bar of any colour, and there is no red except the margin dots. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## patch IV-ledger:3

Region (1840, 55, 2752, 780), erased first (keep ([(1845, 55, 1948, 150)],)).

```text
Image 1 is a crop of a vintage 1970s comic book reference sheet in which the old drawing has been erased to plain cream paper. Draw the study described below into that empty space, in exactly the drawing style of image 2, the whole sheet: bold black ink outlines, halftone dot shading, the same colours, line weight and wood tones. Keep any circled number or outline already in image 1 where it is, and leave a margin of plain paper at the crop's edges.
THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends. It is never a bound codex book: no covers, no spine, no pages. It is written like a log: each entry is ONE short line of dark brown iron-gall ink (illegible squiggles, no real letters) running PARALLEL to the rods, and the entries follow one another from top to bottom down the length of the strip, the newest at the bottom. No side-by-side columns and no vertical lines of writing. Open, it is held VERTICALLY: one rod across the top and one across the bottom, both horizontal, the parchment hanging between them. Closed, the two rolls sit side by side, tied with a cord and a small wax seal tag.
Draw study 3: the ledger held open UPRIGHT, centred in the space: one hand grips the top rod and the other hand grips the bottom rod, both rods horizontal with knobbed ends like those in studies 1 and 6 of image 2, the parchment between them taller than it is wide and filled with short horizontal lines of entries stacked from top to bottom, parallel to the rods. Every entry is one thin handwritten squiggle in dark brown ink. Exactly four entries, spread down the strip, have a thin red line struck through them; no other line is struck through, underlined or covered by a bar of any colour. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## patch IV-ledger:5

Region (850, 790, 1992, 1536), erased first (keep ([(850, 850, 950, 950), (1870, 845, 1965, 940)],)).

```text
Image 1 is a crop of a vintage 1970s comic book reference sheet in which the old drawing has been erased to plain cream paper. Draw the study described below into that empty space, in exactly the drawing style of image 2, the whole sheet: bold black ink outlines, halftone dot shading, the same colours, line weight and wood tones. Keep any circled number or outline already in image 1 where it is, and leave a margin of plain paper at the crop's edges.
THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends. It is never a bound codex book: no covers, no spine, no pages. It is written like a log: each entry is ONE short line of dark brown iron-gall ink (illegible squiggles, no real letters) running PARALLEL to the rods, and the entries follow one another from top to bottom down the length of the strip, the newest at the bottom. No side-by-side columns and no vertical lines of writing. Open, it is held VERTICALLY: one rod across the top and one across the bottom, both horizontal, the parchment hanging between them. Closed, the two rolls sit side by side, tied with a cord and a small wax seal tag.
Draw study 5 in the middle of the space: the ledger lying open flat on a surface, seen from above at a slight angle, UPRIGHT in the frame: one rod with knobbed ends across the top and one across the bottom, both horizontal and like those in studies 1 and 6 of image 2, the parchment between them taller than it is wide, with a meander (Greek key) border ruled around a stack of short horizontal lines of entries running from top to bottom, parallel to the rods. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## patch IV-benches:red

Region (440, 670, 760, 980).

```text
This image is a close-up crop from a vintage 1970s comic book reference sheet: bold black ink outlines, halftone dot shading, flat colours on cream paper. Keep the crop's framing, everything at its edges, the line weight, halftone and colours exactly as they are; change only what is described.
A hand holds a ledger scroll: a wooden rod across the top and one across the bottom, the parchment between them. Redraw only the writing on that parchment: erase the vertical ink strokes and draw four or five short HORIZONTAL wavy ink lines instead, stacked one under another from the top rod to the bottom rod, parallel to the rods. Keep the hand, the rods, any tag, the clothing and the background exactly as they are. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## patch IV-benches:apron

Region (1170, 680, 1490, 980).

```text
This image is a close-up crop from a vintage 1970s comic book reference sheet: bold black ink outlines, halftone dot shading, flat colours on cream paper. Keep the crop's framing, everything at its edges, the line weight, halftone and colours exactly as they are; change only what is described.
A hand holds a ledger scroll: a wooden rod across the top and one across the bottom, the parchment between them. Redraw only the writing on that parchment: erase the vertical ink strokes and draw four or five short HORIZONTAL wavy ink lines instead, stacked one under another from the top rod to the bottom rod, parallel to the rods. Keep the hand, the rods, any tag, the clothing and the background exactly as they are. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## patch IV-benches:key

Region (2430, 650, 2760, 920).

```text
This image is a close-up crop from a vintage 1970s comic book reference sheet: bold black ink outlines, halftone dot shading, flat colours on cream paper. Keep the crop's framing, everything at its edges, the line weight, halftone and colours exactly as they are; change only what is described.
A hand holds a ledger scroll: a wooden rod across the top and one across the bottom, the parchment between them. Redraw only the writing on that parchment: erase the vertical ink strokes and draw four or five short HORIZONTAL wavy ink lines instead, stacked one under another from the top rod to the bottom rod, parallel to the rods. Keep the hand, the rods, any tag, the clothing and the background exactly as they are. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## patch IV-symbols:scroll

Region (1950, 1215, 2180, 1450), erased first (disc (2064, 1333, 84)).

```text
Image 1 is a crop of a vintage 1970s comic book reference sheet in which the old drawing has been erased to plain cream paper. Draw the study described below into that empty space, in exactly the drawing style of image 2, the whole sheet: bold black ink outlines, halftone dot shading, the same colours, line weight and wood tones. Keep any circled number or outline already in image 1 where it is, and leave a margin of plain paper at the crop's edges.
Inside the empty black circle, draw one tiny round pictogram in the style of the other pictograms in row 4 of image 2: a small parchment scroll standing UPRIGHT, its two wooden rods with knobbed ends horizontal, one across the top and one across the bottom, the parchment between them taller than it is wide, with three or four short horizontal ink lines parallel to the rods. Keep the circle outline and the background identical. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## Pixel copy

After the patches, the circled numbers 2 and 3 on `IV-ledger` were copied back from the previous sheet: discs of radius 54 px at (956, 107) and 50 px at (1896, 105).
