# Eras: one island, eras close together

_Agreed with the user on 16 Sep 2026, in a side thread. The main session hasn't applied this yet._

## Decision
- There is one island, Paxos, for every volume. G01 A and G02 B still stand.
- Eras stay, to show the story's temporal dependencies. G05 A is kept, with this refinement: **the eras sit close together (about one generation, roughly 40 years), so the island's look barely changes between them.**
- The period is Hellenistic, a Delos-type free port (matching D05). Delos after 166 BC had a resident Italian merchant community with its own guilds and its own "Agora of the Italians", so Volume VIII's "Roman guilds" fit this period as residents, not as a later empire.
- The papers' own 36-year span (1978–2014) roughly maps onto the island's years. One idea: Leslie arrives young in Volume I and is old by Volume IX.

## Phases
| Phase | Island years | Volumes | Visual differences |
|---|---|---|---|
| 1 · Before the Round | 0–10 | I, II, III, IV | Hamlets and tracks. The headland city has plain walls and a siege camp outside (II). Summit oracle (III). Navigators at the cothon, winter causeway (IV). The Round's saddle has scaffolding or an unfinished ring. |
| 2 · The Parliament | 12–22 | V, VI | The Round is finished; the Statue Walk has only a few statues. New granary storehouses on the plain (VI, a contemporary rival reform). |
| 3 · Citadel & guilds | 22–32 | VII, VIII | The headland city is rebuilt as the fortified citadel **on the same footprint** (not ruins). Italian guild hall, quarry office and lock-houses. The ledger cliffs are heavily cut. The Round's marble is weathered; more statues line the walk. |
| 4 · Reformation | 32–40 | IX | Everything from phase 3, plus the Raft monastery, if IX goes on the island (see below). |

## What stays the same in every phase (the common asset sheet)
- The terrain, coastline, causeway and cothon.
- The road network and town fabric.
- Costume, ship types, materials and palette.

## What can change between phases
- Buildings get **added** (never demolished), and construction moves from scaffolding to finished.
- Walls get strengthened.
- Weathering and quarry cuts increase.
- The statue count grows.
- Banners, props and cast change.

In Blender, the eras are small additive collections on one scene, not separate island states.

## Text changes for `paxos-illustrated/volumes.md`
- **II:** "three centuries before the citadel of Volume VII" becomes "a generation before".
- **VII:** "For five hundred years the 3f+1 Law…" becomes "since the siege": the law was correct but unaffordable for a generation.
- **VIII:** the "Roman engineers" become the resident Italian merchant guild's engineers.
- **IX:** "sailed north" becomes a withdrawal to the north shore of the east lobe, cut off by the causeway in winter. Only do this if IX moves onto the island; otherwise G06 A (off-island misty north coast) stands. **Still open.**
- **D05's present-day dig site and "Paxos in decline":** keep them only as a narrator's frame (a few sepia panels), not a modelled era.

## What to update in this repo
- **`STATUS.md`:** add a note to G05: "eras close together, additive only; see ERAS.md".
- **`tools/island_maps.py` `SITES`:**
  - Site 6 becomes "Headland city (II) → fortified citadel (VII), same footprint".
  - Site 16 becomes "Italian guild lock-houses" (drop "Roman").
  - If IX goes on the island, add a monastery site on the east lobe's north coast.
- **`art-direction-grand.html`:**
  - Scope table: change Volume VII from "built on the ruins" to "rebuilt on the same footprint".
  - Scope table: change Volume VIII from "Round in ruins" to "Round weathered, guild quarter".
  - Section 5 (scale, time and Volume IX): describe the four close phases.
- **Terrain:** no change. The work on map B (the Round's col, the causeway checks, the banquet house to the east) goes on as before.
