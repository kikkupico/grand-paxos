# Status

_Last updated 16 Sep 2026._

## The brief
1. Every volume's story takes place on the island of Paxos. Volume IX is on its own islet across a strait.
2. The whole island is pre-visualised in Blender. Key architecture gets detailed models: the Great Round, the harbours, the city, the citadel, and so on.
3. Each illustration starts as a Blender pre-vis render and is then turned into a Franco-Belgian comic image.
4. There is one common asset sheet for the whole series, plus an asset sheet for each volume.

## Pipeline (current stage in bold)
1. Rough map: done. The island is a generated elevation field with all 23 sites placed and every check passing.
2. Painted map: tried once (16 Sep 2026) and **kept only as a record** of how it didn't turn out as expected: symbol-sized buildings, invented features, no usable surface detail. It is not used downstream. It lives in §3 of the page (`maps/island-painted.jpg`, with scores measured before the terrain smoothing below).
3. Island blockout in Blender: terrain built (16 Sep 2026). `tools/blender_terrain.py` builds `blender/paxos.blend` (gitignored) straight from the heightmap. Checks are in `blender/terrain-checks.json` and §4 of the page.
4. **Hero architecture: key buildings detailed to human scale (16 Sep 2026).**
   - Detailed: the Great Round (`blender_round.py`, with the user's verandah); the lighthouse and quays, banquet house, agora and stoa, oracle temple, headland city and citadel (`blender_arch.py` components); and doors and windows on every house.
   - All checks pass: `blender/{terrain,buildings,round,detail,sites,vegetation}-checks.json`, §4–6 of the page.
   - **Next:** props, such as ships in the harbours, amphorae, the hourglass and the ledger. Tripo is for props only; ask before any paid API call. Then stage 5, shot pre-vis.
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
  - `settle()` eases ground above 12 m down along the town's shore with a soft falloff. It only lowers, so the shore keeps its slope.
  - `open_sightline()` lowers only the ground within 10 m of the sightline from the Round (eye +8 m) to `PORT`, fading sideways over 140 m. That gives a soft valley, not a cut.
  - `channel()` cuts the neck (t .31, feather 320 m) and the Raft strait (t .905, feather 380 m) with wandering banks.
  - These replaced a cut-and-fill `grade()` ramp, a raised terrace and steep channel faces, which looked like a trench, a sea wall and ruler-straight coasts once viewed in 3D.
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

## Blender scene (`tools/blender_terrain.py`)
- **Run:** `~/.local/bin/blender -b -P tools/blender_terrain.py [-- --render]`. It takes a few seconds and writes `blender/paxos.blend` and `blender/terrain-checks.json`, plus the checks between the page's `<!-- TERRAIN -->` markers. With `--render` it also writes `renders/terrain-{overview,top,col}.png` (gitignored).
- **Terrain mesh:** 880 × 640 vertices at the heightmap pixel centres, 12.5 m apart, Z = elevation (no Displace modifier). The heightmap is read through Blender's image loader as Non-Color and flipped north-first. The outermost 600 m of seabed are eased down to −120 m (only open sea), so there's no table edge.
- **Coordinates:** Blender X = x − 5500, Y = 4000 − y (north is +Y), Z = elevation.
- **Scene:** a sea plane at 0 over a sea floor at −121 m; a placeholder material coloured by elevation, with rock on slopes over ~30°; a sun from the WSW; cameras for the overview, top and the Round's col. Collections: Terrain, Sites (one child collection per volume, one empty per site point with `site_num`, `site_key`, `volume` and `elevation_m` properties), and Cameras & light.
- **Checks:** 563,200 vertices; site heights vs the site list max 0.39 m, mean 0.07 m; north is +Y; every site lands on the terrain.
- **Next:** buildings, vegetation and props, placed at the site empties. Building footprints come from the gazetteer and canon, not the painting.

## Key buildings (`tools/blender_buildings.py`)
- **Run:** `~/.local/bin/blender -b -P tools/blender_buildings.py [-- --render]`. It calls `blender_terrain.build()` first, so it is the full scene build. It writes `blender/paxos.blend`, `blender/buildings-checks.json`, the page's `<!-- BUILDINGS -->` block, and with `--render` `renders/buildings-{round,parliament,cothon,port,city,citadel}.png`.
- **Inputs:** site points, plus `island-sites.json["built"]` from the map generator: the cothon centre, radii and channel bearing; the town's agora and 36 insulae (44 × 30 m); and the Statue Walk path (exported, not yet used).
- **Ground:** reads and edits the terrain mesh heights. `pad()` levels with a smoothstep falloff (the Round, the banquet house, the citadel at its hilltop median). The Round's bowl is dropped below the tiers. The cothon's quay platform is levelled to 2.8 m right up to the basin wall, leaving the channel alone. Other buildings sit on foundations down to their lowest ground. The heightmap itself is never changed.
- **Models:** a `Kit` accumulates boxes, rings, cylinders, cones and gable roofs into one mesh per building, with materials for limestone, ashlar, marble, sand, terracotta, plaster, bronze, timber, paving, canvas, lantern and fortress stone. 9 objects, about 13k faces. They sit in collections by volume under Buildings.
- **Checks:**
  - The Round's east gate faces the banquet house (0°).
  - Land buildings stand on land.
  - The merchant pier tips reach water.
  - The cothon basin is deeper than 3 m.
  - The breakwater is at least 70% over water (100%).
  - No hero footprints overlap.
- **Bugs this stage found:**
  - The cothon channel was cut toward water inside the future basin, so the quay platform sealed it into a closed lake, even on the 2D map. `cothon()` now aims at water beyond the platform, and the map checks gain `cothon_open_to_sea` (a flood fill from the basin must reach the world edge; it fails if the channel is sealed).
  - A levelling gap left hill-height vertices at the basin edge, which rendered as spikes.
- **Rough edges:**
  - Terrain triangulation shows as saw-teeth along levelled edges at 12.5 m cells.
  - Some bare rock remains on the citadel's downhill cut.
  - Buildings are simple blockouts: no openings, no roof tiles, no statues' detail.

## Remaining sites (`tools/blender_sites.py`)
- **Code layout:** called from `blender_buildings.main()` after the key buildings. The shared helpers (`Ground`, `Kit`, materials, `house`, `colonnade`, `B`, `site`) live in `tools/blender_kit.py`, so there's one material set.
- **Builders:**
  - `hamlet` ×3 and `olive_press`: pads, stone houses, a sundial each.
  - `beacon_towers`.
  - `oracle`: a temple in a temenos on a pad; a rock crag with the cave mouth on the steepest side 70 m out; the shepherd's hut.
  - `drummers` and `causeway_markers`: posts along the crest of cells 0–3.5 m high near the strait, ordered by PCA.
  - `statue_walk`: see below.
  - `granaries`: buttressed storehouses turned along the contours.
  - `guild_quarter`: hall, 5 identical lock-houses with nameplates (one misspelled: CVSTOS IIII), quarry benches cut as 6 m terrain steps, stone stacks, loading quay, crane, office.
  - `monastery`: cloister, scriptorium, jetty and raft.
- **The Statue Walk:** the exported least-cost route is Chaikin-smoothed and ends 32 m from the Round, at the gate, not in the bowl. Its bed is the running average of the ground over 9 samples, and the terrain is cut and filled to it. Result: 1.8 km, 29 statues, mean grade 10.5%, steepest 27.7% (40% on raw ground), which would need steps.
- **Checks (`sites-checks.json`):**
  - Sightline self-test: clear 500 m up, blocked through the summit.
  - Hamlet rooftops hidden from each other (rays through the terrain mesh).
  - Beacon fires and drum platforms in sight of their partners.
  - Granaries at least 300 m apart (513).
  - The oracle within 15 m of the local summit (6.4).
  - Lock-houses on land.
  - The monastery jetty reaches water (−8.4 m).
- **Found on the way:** the first self-test's "blocked" ray ran underground, where no surface can block it, so it failed for the wrong reason. Smoothing the switchback path cut corners and raised the steepest grade until the bed was graded.

## The Great Round in detail (`tools/blender_round.py`)
- **User refinement (16 Sep 2026):** the top tier is an inward-facing colonnaded verandah, its floor about 15 ft (4.6 m) above the outside ground. Windows in the ring wall along it look out over the island, with sills (5.5 m above the outside ground) high enough to read as windows, not entrances. The gates stay at ground level and join the cavea below the verandah, at the mid-height walkway, which the verandah bridges.
- **Why:** with a plain high ring wall, the ray check showed the banquet house could not be seen from the tiers (blocked by the Round's floor through the gate, and by terrain).
- **Layout:**
  - Cavea: 7 lower rows (0.5 m rise) from the orchestra (3.5 m below the outside ground) to the walkway at ground level; then a 1.1 m podium and 6 upper rows (0.6 m rise); then the verandah (3 m deep, 50 columns, tiled roof). Treads are 0.8 m.
  - Stairways: 8, with steps of 0.3 m or less.
  - Gate passages are cut through the upper cavea with retaining walls. Doorways are 4 m (to fit under the verandah floor), with pylons, lintel, attic and pediment rising above the wall.
  - Ring wall: WALL_IN 23.4, WALL_OUT 25 m, ashlar brick texture mapped by angle × radius, 48 windows 1.4 × 1.9 m every 5° clear of the pylons.
  - Doors: bronze with panels and bosses. The east gate is open (leaves swung in 80°, bar leaning on the jamb); the others are barred at 1.3 m.
  - 20 statues on inscribed pedestals (orator, scroll and standing poses, 2.1 m). Scale figures of 1.75 m.
- **Kit additions:** `frustum`, `ellipsoid`, `beam` (a box between any two points).
- **Checks (`round-checks.json`):**
  - Canon: 14 tiers, 8 stairways, cardinal gates, 50 m across.
  - Human scale: seat risers, stair risers, drop-bar within reach.
  - Verandah about 15 ft up; window sills ≥ 4.5 m; gates join below the verandah.
  - Ray casts from a person standing at the sill of the nearest window: to the banquet house (16°) and to the merchant quays (41°), blocked by neither the Round nor the terrain. With the eye 0.8 m back from the sill and 1.2 m windows, the banquet ray clipped a pier.
- **Renders:** `renders/buildings-round_{aerial,interior,window,gate,statue}.png`.

## The other hero buildings in detail (`tools/blender_arch.py`)
- **Components:**
  - `column` (Doric: tapered 16-sided shaft, echinus, abacus) and `opening` (a dark door or window on a box face).
  - `temple`: Doric peripteral temple from its column diameter d. Columns 5.5d high, 2.4d apart, three steps with risers of 0.4 m or less, architrave, frieze with triglyphs, cornice, marble pediments under a tiled roof, acroteria, cella with door.
  - `crenellate`, `crenellate_box`, `crenellate_ring` (merlons 1 × 2 m; gaps at most 1 m by rounding the count up) and `portcullis`.
- **Kit upgrades:** `house()` (every house) adds a 2.1 × 1.1 m doorway with lintel on the long face and 0.6 × 0.8 m windows with sills 2 m up on the back (`HOUSE_STATS` counts them). `colonnade()` makes Doric columns.
- **Buildings:**
  - Lighthouse: podium with steps and door, tapering shaft with string courses and slits, gallery and parapet, 8-column lantern room, fire bowl with its flame at 28–29.6 m, bronze cone; top 35.4 m. The 7 quays have bollards, and each captain's post has a lamp post beside it.
  - Banquet house: steps, 4-column porch toward the Round, vestibule, peristyle garden with fountain, andron with 11 couches.
  - Agora and stoa: the generator now places the agora wholly on dry land (map check `agora_on_dry_land`). It had been 22% over the sea as a podium. Blender pads it level; the stoa has Doric columns and 6 shop doors.
  - Oracle: temple 4 × 7 (d 0.8) facing east, with a gateway in the enclosure; the hut has a door.
  - Headland city: crenellated walls and towers, temple 6 × 11 (d 0.9).
  - Citadel: crenellated walls and towers; gatehouse narrowed to 4 m with masonry to 13 m and a raised portcullis; keep with slits, door and merlons; quorum hall as temple 6 × 9 (d 0.9).
- **Checks (`detail-checks.json`):**
  - All seven quays see the lantern, and each captain's post sees its neighbour (rays through the harbour mesh and terrain). Both failed at first: lamp poles stood on the sightlines and the flame sat below the parapet.
  - The banquet andron seats 11.
  - House doors and windows at human scale.
  - Temple columns in Doric proportion; steps and doors at human scale.
  - Citadel merlons cover a standing soldier, crenels 0.6–1.0 m, wall-walk at least 2 m, gate at least 3 × 4 m.
  - The oracle's cave mouth is walk-in height.
- **Renders:** `renders/buildings-detail_{lighthouse,banquet,oracle,citadel,town,city}.png`. The full build and render takes about 2 minutes.

## Vegetation, fields and tracks (`tools/blender_nature.py`)
- **Track network (map generator):** `TRACKS` lists hub-to-hub links in walking order. Hamlets hang off different hubs (press, oracle, beacon), so no track runs hamlet to hamlet.
  - Paths use `least_cost_path(slope_k=150, min_z=.5, passable=causeway corridor)`, which returns `[]` when a target is unreachable.
  - The cothon's site point is its islet, so tracks end on its quay ring. The strait point snaps to the causeway crest.
  - Exported as `built["tracks_m"]` and drawn on the 2D map in place of the old star from the town.
  - Map checks: `tracks_connect_every_mainland_site` counts only reachable tracks and fails when a link is removed; `tracks_unreachable`; `tracks_hamlet_to_hamlet`.
- **Causeway regression found and fixed:** widening the neck channel's banks (for natural coasts) had made the gap longer than the causeway, so the neck wasn't joined. `island()` now walks out from the neck to find landfall at both ends. The new map check `causeway_joins_the_neck` (land flood fill from the oracle reaches the Round) is False on the previous heightmap and True now.
- **Masks per terrain vertex**, stored as mesh attributes `veg_olive`, `veg_maquis`, `veg_pine`, `field`, `track`:
  - Inputs: elevation, slope, chamfer distance to the sea, distance to settlements, value noise.
  - Exclusions: `EXCLUDE_M` circles per site, town insulae, agora, within 7 m of tracks, one cell in from the coast.
  - Tall trees (olives, pines) are zeroed within 30 m of the story sightlines: Round to quays, Round to banquet house, the beacon pair, the drum pair. At 18 m, one tree slipped in through face interpolation.
- **Scatter:** one Geometry Nodes object per species reads the terrain through Object Info, runs Distribute Points on Faces (density = attribute × per-m²) and Instance on Points with random rotation and scale. Low-poly prototypes sit at z = −3000. Cypresses are placed by hand at the oracle, the banquet house and the monastery. About 19k olives, 237k maquis, 9k pines, 25 cypresses.
- **Terrain shader:** farmland parcels (95 × 62 m, rotated 0.6 rad) come from Position → Floor → White Noise → constant ramp, with hedge lines from Fraction, masked by `field`. The `track` attribute adds a dirt tint. Per-vertex parcels had rendered as blobs. Tracks are also draped ribbons (3.6 m, +0.22 m), about 28.7 km.
- **Checks:** from the evaluated instances, no trees in water, no tall trees on building footprints (75% radius), and no tall trees within 8 m of the story sightlines.
- **Renders:** `renders/nature-{overview,parliament,plain,groves}.png`. The full build and render takes about 1 minute.

## Stage 2 files
- `maps/island-reference.svg` is written by `island_maps.py` in its clean mode. It has no numbers, zone numerals, dots, compass, scale bar or offshore depth bands. Built sites are shown as terracotta rectangles.
- `maps/island-reference.png` is written by `painted_map.py reference`: 2200 × 1650, with the 11:8 map letterboxed with 25 units of sea top and bottom to make 4:3, the nearest aspect ratio the image model offers.
- `painted_map.py register <file>` scales the painting to that 4:3 frame, crops the letterbox, and writes `maps/island-painted.jpg` (2200 × 1600, the same frame as the SVG and heightmap). It also writes `island-painted.json`, with land IoU and the percentage of cells wrong by more than 50 m from the coast, and `island-painted-mismatch.png`. The sea classifier counts as water anything blue-dominant, or pale sea-green (green over red, blue at most 30 under red, bright). The first rule missed the painted turquoise and sea-green shallows and scored the painting 0.83, which was wrong. On the painting, only 0.08% of land reads as sea. A self-test on the reference scores IoU 0.994, with 0% beyond 50 m. `register` also writes the scores into the page between `<!-- PAINTED -->` markers.
- Departures in painting v1 that the score doesn't catch: buildings are drawn at symbol size (citadel, city and Round several times too big), the east breakwater appears twice, the town piers and a SW quay reach too far out, the Raft islet has no monastery building, and the Round reads as a theatre. Take building footprints from the site list, not the painting.
- Storage decision: commit `island-painted.jpg` and its JSON as spec. Keep the full-size download out of Git.

## Next steps
1. Props: ships and skiffs in the three harbours, amphorae on the quays, the hourglass, the ledger, statues' detail. Tripo is for props only; ask before any paid API call.
2. Stage 5: shot pre-vis, one camera per panel.
3. Optional: re-lay the Statue Walk with switchbacks or steps on its steep stretch.
4. Optional: names for the town, bays and capes.
