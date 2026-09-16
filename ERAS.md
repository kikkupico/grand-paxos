# Eras: one island, eras close together

_Agreed with the user on 16 Sep 2026, in a side thread. The main session hasn't applied this yet._

## Decision
- There is one island, Paxos, for every volume. G01 A and G02 B still stand.
- Eras stay, to show the story's temporal dependencies. G05 A is kept, with this refinement: **the eras sit close together (about one generation, roughly 40 years), so the island's look barely changes between them.**
- The period is Hellenistic, a Delos-type free port (matching D05). Delos after 166 BC had a resident Italian merchant community with its own guilds and its own "Agora of the Italians", so Volume VIII's "Roman guilds" fit this period as residents, not as a later empire.
- The papers' own 36-year span (1978–2014) roughly maps onto the island's years. One idea: Leslie arrives young in Volume I and is old by Volume IX.

## Map order vs story order
Option E lays the island out in **dependency order** (NW→SE: I+III, IV, V, then II/VI/VII/VIII, then IX). The phases below are **story time**. They disagree for Volume II, which sits downstream of V on the map but is a phase-1 siege. That's deliberate: the map shows what builds on what, and the phases show what happened when.

## Phases
| Phase | Island years | Volumes | Visual differences |
|---|---|---|---|
| 1 · Before the Round | 0–10 | I, II, III, IV | Hamlets and tracks. The headland city has plain walls and a siege camp outside (II). Summit oracle (III). Navigators at the cothon, winter causeway (IV). The Round's saddle has scaffolding or an unfinished ring. |
| 2 · The Parliament | 12–22 | V, VI | The Round is finished; the Statue Walk has only a few statues. New granary storehouses on the plain (VI, a contemporary rival reform). |
| 3 · Citadel & guilds | 22–32 | VII, VIII | The citadel is a **separate fortress** further along the island, above its own harbour and sea wall. The Volume II headland city still stands, just older. The Italian guild has its own hall, quarry office and lock-houses. The ledger cliffs are heavily cut. The Round's marble is weathered; more statues line the walk. |
| 4 · Reformation | 32–40 | IX | Everything from phase 3, plus the Raft monastery on its islet across the strait (option E). |

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
- **II:** "three centuries before the citadel of Volume VII was built on top of it" becomes "a generation before the citadel of Volume VII was built on it". "It" is the 3f+1 bound, not the ground, because the citadel is its own site on map E.
- **VII:** "For five hundred years the 3f+1 Law…" becomes "since the siege": the law was correct but unaffordable for a generation.
- **VIII:** the "Roman engineers" become the resident Italian merchant guild's engineers, and they work in the **guild's own hall**, not the "ruined chamber" of the Round.
- **IV / V / VII harbours (map E):** the lantern round-robin happens at IV's own cothon at the neck, V's galley leaves from the merchant quays below the Round, and VII's inquisitors land at the citadel's walled harbour.
- **IX:** "sailed north" becomes "crossed to the island": the monks withdraw to the Raft islet across the strait at the SE end of the island (option E, G06 B, decided 16 Sep 2026).
- **D05's present-day dig site and "Paxos in decline":** keep them only as a narrator's frame (a few sepia panels), not a modelled era.

## Map order vs shared places (decided 16 Sep 2026)
On map E every site belongs to exactly one volume, so a walk from the NW corner reads the papers in dependency order (`DEPENDS`/`BANDS` in `tools/island_maps.py`). Places that were shared are rebuilt per volume: IV has the cothon, V its merchant quays and town, VII a walled harbour, and VIII a guild hall. I's beacons and IV's drummers are separate pairs. The earlier "citadel on the same footprint as II's city" idea is dropped.

## What was updated in this repo
All of it is done: STATUS.md, `SITES_E` (23 sites, one volume each), the page's scope table and gazetteer, and §5's phases.
