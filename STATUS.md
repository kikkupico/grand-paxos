# Status

_Last updated 16 Sep 2026._

## The brief
1. Every volume's story takes place on the island of Paxos. Volume IX is on its own islet across a strait.
2. The whole island is pre-visualised in Blender. Key architecture gets detailed models: the Great Round, the harbours, the city, the citadel, and so on.
3. Each illustration starts as a Blender pre-vis render and is then turned into a Franco-Belgian comic image.
4. There is one common asset sheet for the whole series, plus an asset sheet for each volume.

## Pipeline (current stage in bold)
1. Rough map: done. The island is a generated elevation field with all 23 sites placed and every check passing.
2. **Painted map: in progress, waiting for the user.** The user makes the image by hand in the Gemini web UI (no API calls) from `maps/island-reference.png` and the prompt in `prompts/painted-map.md`, then brings the file back. Next: run `python3 tools/painted_map.py register <file>`, check the coastline score and the mismatch image, and put the painting on the page.
3. Island blockout in Blender: the heightmap displaces a Grid, empties come from the sites JSON, then sculpting.
4. Hero architecture: the Round, the three harbours, the headland city, the citadel, the granary, the guild hall and the lock-houses are hand-modelled. Tripo is used only for props (statues, amphorae, ships, the hourglass).
5. Shot pre-vis: one camera per panel, rendered as clay plus a line pass.
6. Comic pass: ligne claire over the pre-vis, checked against the asset sheets.

## Decisions
- **One island, the Dependency Spine.** It is laid out along the dependency graph between the papers. Walking from the NW tip reads the volumes in order, I to IX, and every volume comes after the ones it builds on. Four other layouts were explored and dropped; they're in git history before the commit that removed `art-direction-grand.html`.
- **Volumes are numbered in walking order**, which is also dependency and story order: I Disordered Sundials, II Sleeping Shepherd, III Passable Season, IV Part-time Parliament, V Generals Before the Walls, VI Ledger of Many Decrees, VII Citadel of Iron Quorums, VIII Quarries of the Roman Guilds, IX Raft Monks.
- **World:** 11 × 8 km, about 18.5 km² of land.
- **Time:** one terrain and one generation in five phases, one per graph band and island zone, with buildings only added. See `ERAS.md`.
- **Every site belongs to one volume.** Kinds of place several volumes need are built per volume: III's cothon (the lantern harbour), IV's merchant quays and town, VII's walled harbour, VIII's guild hall, I's beacons and III's drummers.
- **3D files:** `.blend`, `.glb` and renders are gitignored, and renders go to R2.

Canon for the period, the Great Round and the Parliament's port is in §5 of the page.

Still open:
- The comic style isn't defined beyond "Franco-Belgian". One candidate is Jacques Martin's *Alix*, which is ligne claire set in antiquity.
- The contents of the common and per-volume asset sheets aren't defined yet.

## The page (`art-direction-grand-island-shape.html`)
The sections are:
1. The reading order: a generated table (`ORDER`) plus the five phases.
2. The map: volume chips, a heightmap view, the legend, "where things fall", strengths and costs, and Measured (`MAP`, `STATS`).
3. The 23-site gazetteer.
4. The places each volume builds for itself.
5. The canon.
6. The decisions.
7. The Blender spec.

## Generator notes (`tools/island_maps.py`)
- **Terrain:** `island()` builds the terrain from primitives (`blob`, `ridge`) along `AXIS` (1500,1300)→(9800,7200), with domain warp (`warp`) and value noise (`finish`). Each volume zone is a "bead" at a fraction of the axis, with an offset across it, and bays are cut into the notches between beads. It returns rough site positions, the cothon hint and rule overrides.
- **Placement:** `build()` snaps the cothon to the shore and carves it (basin, islet, channel to deep water), snaps each site to its `RULES` band (elevation range, distance to sea), and runs `place_by_sight()`:
  - The Round stays pinned at `ROUND_COL` (`round_radius` 0), in the col between two knolls. `is_saddle()` confirms it.
  - The banquet house goes 120 m or more east of the Round, within 60 m north or south, lower, and visible from it.
  - Each `sight_pairs` headland pair (`beacons`, `drummers`) moves its second point until it sees the first.
  - Hamlets K and M are moved until they're hidden from the hamlets already placed.
- **Hand-shaped ground:**
  - A narrow crest through the col makes it fall away to both coasts.
  - A valley runs from the col to the NE coast.
  - `grade()` makes a coastal flat for the town and a graded descent from the Round to `PORT`, computed from those two points so the quays stay in view.
  - `channel()` cuts the neck (t .31) and the Raft strait (t .905).
  - `causeway()` lays a Bézier tombolo across the neck.
  - `keep_islands()` drowns stray islets.
- **Checks** (`checks()`, written to the JSON and the page):
  - Hamlets hidden, beacon and drum pairs in sight, the banquet house in view and due east.
  - Sea on both sides of the Round, the quays in view (`harbour_of`), the Round in a saddle and clear of the town.
  - The causeway dry in calm weather with its crest at 3 m or less (measured over former sea).
  - The monastery on its own land mass (`land_component`).
  - `dependency_order()`: every `DEPENDS` edge holds along the axis, and the `BANDS` don't overlap.
- **Drawing:** contours use hand-written marching squares, then Chaikin smoothing and RDP simplification. Roads are least-cost Dijkstra paths on a 25 m grid. The town is insulae on a street grid. Badges search for a spot that clears every symbol and sits nearer their own site than any other.
- **Rough edges:**
  - The middle of the island is hand-engineered. If the terrain changes, re-check the saddle and harbour-view results.
  - The south-east lobe reads as one mass, so its four zones show through the numerals more than the coastline.
  - The causeway still reads fairly straight at map scale.

## Blender import spec
- **Grid:** 881 × 641 vertices, 11000 × 8000 m, so one face per heightmap pixel (`maps/island-height.png` is 880 × 640).
- **Displace modifier:** Non-Color, Strength 600, Midlevel 0.2.
- **Site empties:** Blender X = x − 5500, Blender Y = 4000 − y, Z = elevation.
- **Check this on the first import:** site 23's empty (the Raft monastery) must land on the small SE islet. If it lands NW, the image V axis is flipped.

## Stage 2 files
- `maps/island-reference.svg` is written by `island_maps.py` in its clean mode. It has no numbers, zone numerals, dots, compass, scale bar or offshore depth bands. Built sites are shown as terracotta rectangles.
- `maps/island-reference.png` is written by `painted_map.py reference`: 2200 × 1650, with the 11:8 map letterboxed with 25 units of sea top and bottom to make 4:3, the nearest aspect ratio the image model offers.
- `painted_map.py register <file>` scales the painting to that 4:3 frame, crops the letterbox, and writes `maps/island-painted.jpg` (2200 × 1600, the same frame as the SVG and heightmap). It also writes `island-painted.json`, with land IoU and the percentage of cells wrong by more than 50 m from the coast, and `island-painted-mismatch.png`. The sea classifier treats blue-dominant pixels as sea. A self-test on the reference itself scored IoU 0.993, with 0% beyond 50 m.
- Storage decision: commit `island-painted.jpg` and its JSON as spec. Keep the full-size download out of Git.

## Next steps
1. Register the user's painting, iterate on the prompt if the score is poor, then add the painting to the page (optionally with the site badges overlaid in the same viewBox).
2. Optional: names for the town, bays and capes; larger map symbols.
3. Stage 3: build the Blender scene from `island-height.png` and `island-sites.json`, following the spec above.
