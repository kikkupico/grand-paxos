# Reference sheet edits (Gemini API)

`tools/reference_sheets.py edit <name>` sends the current sheet and its prompt to `gemini-3-pro-image` (16:9, 2K), and writes attempts to `temp/references/`. `edit <name> <attempt>` refines an attempt with the `<name>:fix` prompt. `accept <name> <file>` copies the chosen attempt into `references/`. The `:fix` prompts below are the last ones used; earlier versions (such as the old woman's ledger on the benches sheet) are in git history.

## IV-ledger

```text
Keep the exact drawing style of the attached sheet: vintage 1970s comic book reference sheet, bold black ink outlines, visible halftone dot shading, flat Mediterranean palette (aegean blue #136f9e, terracotta red #bf4a26, olive green #66722c, marble white, sand #f2e7cd, gold accents #c1912b, ink #1c1512) on cream paper. Keep the layout, framing and every element not mentioned below unchanged.
THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends, like an ancient Greek book-roll with a rod at each end. It is never a bound codex book: no covers, no spine, no pages. Closed, the two rolls sit side by side, tied with a cord and a small wax seal tag. Open, it is held horizontally with one rod in each hand, the parchment stretched between them showing a few columns of dark brown iron-gall ink lines (illegible squiggles, no real letters).
Redraw every ledger study on this sheet as that scroll instead of a codex book, one study per existing slot: (1) the closed ledger, both rolls tied with a cord and a wax seal tag bearing a dolphin emblem, carried by a leather strap; (2) the ledger held open between its two rods, columns of neat ink entries with small red dots in the margin; (3) open, with some entries struck through in red; (4) keep the torn tally scrap exactly as it is; (5) open, with a meander (Greek key) border ruled around one column; (6) closed, with small coloured tags hanging from the rod ends as bookmarks. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## IV-benches

```text
Keep the exact drawing style of the attached sheet: vintage 1970s comic book reference sheet, bold black ink outlines, visible halftone dot shading, flat Mediterranean palette (aegean blue #136f9e, terracotta red #bf4a26, olive green #66722c, marble white, sand #f2e7cd, gold accents #c1912b, ink #1c1512) on cream paper. Keep the layout, framing and every element not mentioned below unchanged.
THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends, like an ancient Greek book-roll with a rod at each end. It is never a bound codex book: no covers, no spine, no pages. Closed, the two rolls sit side by side, tied with a cord and a small wax seal tag. Open, it is held horizontally with one rod in each hand, the parchment stretched between them showing a few columns of dark brown iron-gall ink lines (illegible squiggles, no real letters).
A CLOSED ledger shows TWO separate parchment rolls lying side by side and touching, each wound on its own wooden rod with a knob at both ends (four knobs in all), tied together with a cord; it must not look like a single roll.
Keep all seven legislators exactly as drawn (faces, clothing, poses, bags). Replace every red codex book they hold or carry with the closed ledger scroll: two wooden rods rolled together, tied with a cord, carried in the same hand or tucked under the same arm. The elder handing a ledger to the youth now hands over a closed scroll. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## IV-legislators

```text
Keep the exact drawing style of the attached sheet: vintage 1970s comic book reference sheet, bold black ink outlines, visible halftone dot shading, flat Mediterranean palette (aegean blue #136f9e, terracotta red #bf4a26, olive green #66722c, marble white, sand #f2e7cd, gold accents #c1912b, ink #1c1512) on cream paper. Keep the layout, framing and every element not mentioned below unchanged.
THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends, like an ancient Greek book-roll with a rod at each end. It is never a bound codex book: no covers, no spine, no pages. Closed, the two rolls sit side by side, tied with a cord and a small wax seal tag. Open, it is held horizontally with one rod in each hand, the parchment stretched between them showing a few columns of dark brown iron-gall ink lines (illegible squiggles, no real letters).
A CLOSED ledger shows TWO separate parchment rolls lying side by side and touching, each wound on its own wooden rod with a knob at both ends (four knobs in all), tied together with a cord; it must not look like a single roll.
Keep all five legislators exactly as drawn (faces, clothing, poses, the hourglass, the stone seat). Remove every rectangular red leather book entirely, including the ones clasped against the body or held in a bag: no book shapes may remain. In its place each legislator carries a closed ledger (two rolls tied together) under the arm or with the knobbed rod ends poking up out of the shoulder bag. The old man reading on the right now holds the ledger open between its two rods in both hands, reading the parchment stretched between them. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## IV-symbols

```text
Keep the exact drawing style of the attached sheet: vintage 1970s comic book reference sheet, bold black ink outlines, visible halftone dot shading, flat Mediterranean palette (aegean blue #136f9e, terracotta red #bf4a26, olive green #66722c, marble white, sand #f2e7cd, gold accents #c1912b, ink #1c1512) on cream paper. Keep the layout, framing and every element not mentioned below unchanged.
Change exactly one small thing. In row 4 (the row of round pictogram circles), the circle between the bunch of grapes and the anchor contains a small closed brown book with a green leaf. Inside that same circle, replace the book with a tiny parchment scroll wound on two wooden rods (drawn open a little between its two rods), keeping the green leaf. Do not add any new pictograms or circles. Keep the small sun, crescent moon and star symbols at the far right of row 4 exactly where they are. Every other element stays identical. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## IV-benches:fix

```text
Keep the exact drawing style of the attached sheet: vintage 1970s comic book reference sheet, bold black ink outlines, visible halftone dot shading, flat Mediterranean palette (aegean blue #136f9e, terracotta red #bf4a26, olive green #66722c, marble white, sand #f2e7cd, gold accents #c1912b, ink #1c1512) on cream paper. Keep the layout, framing and every element not mentioned below unchanged.
THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends, like an ancient Greek book-roll with a rod at each end. It is never a bound codex book: no covers, no spine, no pages. Closed, the two rolls sit side by side, tied with a cord and a small wax seal tag. Open, it is held horizontally with one rod in each hand, the parchment stretched between them showing a few columns of dark brown iron-gall ink lines (illegible squiggles, no real letters).
The sheet is correct except for one thing: the black-haired woman third from the left, in the olive green shawl, carries no ledger. Add one: a ledger scroll on two rods, rolled up, held in her right hand in front of her shoulder bag, drawn like the ledgers the others carry. Change nothing else, and keep every other figure's ledger exactly as it is. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```

## IV-ledger:fix

```text
Keep the exact drawing style of the attached sheet: vintage 1970s comic book reference sheet, bold black ink outlines, visible halftone dot shading, flat Mediterranean palette (aegean blue #136f9e, terracotta red #bf4a26, olive green #66722c, marble white, sand #f2e7cd, gold accents #c1912b, ink #1c1512) on cream paper. Keep the layout, framing and every element not mentioned below unchanged.
THE LEDGER (canon): a single long continuous strip of cream parchment wound between two turned wooden rods with knobbed ends, like an ancient Greek book-roll with a rod at each end. It is never a bound codex book: no covers, no spine, no pages. Closed, the two rolls sit side by side, tied with a cord and a small wax seal tag. Open, it is held horizontally with one rod in each hand, the parchment stretched between them showing a few columns of dark brown iron-gall ink lines (illegible squiggles, no real letters).
A CLOSED ledger shows TWO separate parchment rolls lying side by side and touching, each wound on its own wooden rod with a knob at both ends (four knobs in all), tied together with a cord; it must not look like a single roll.
Studies 1, 2, 3 and 4 are correct: keep them exactly. Studies 5 and 6 are still bound codex books and must become scrolls: (5) the ledger lying open on a table between its two rolls, with a meander (Greek key) border ruled around one column of entries; (6) the closed ledger (two rolls tied together) with small coloured cloth tags hanging from the rod knobs as markers and a round dolphin seal. No covers, spines or pages anywhere on the sheet. No readable words, letters or digits anywhere. Do not add numbers, numbered circles or labels that are not already on the sheet.
```
