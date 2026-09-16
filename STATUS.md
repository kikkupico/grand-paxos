# Status: grand art direction

> **Volume numbers.** On 16 Sep 2026 the volumes were renumbered in walking order on map E: I Sundials, II Sleeping Shepherd (published III), III Passable Season (published IV), IV Parliament (published V), V Generals (published II), VI–IX unchanged. See ERAS.md. The history and the A–D notes below use the **published** numbers; the map E notes, ERAS.md and the island-shape page use the **new** ones.

_Last updated 16 Sep 2026._

## The brief (the user's four expectations)
1. Every volume's story takes place on the island of Paxos, except perhaps Volume IX.
2. The whole island is pre-visualised in Blender. Key architecture gets detailed models: the Volume V chamber (the Great Round), the Volume IV circular harbour, and so on.
3. Each illustration starts as a Blender pre-vis render and is then turned into a Franco-Belgian comic image.
4. There is one common asset sheet for the whole series, plus an asset sheet for each volume.

The user explicitly allowed starting afresh. Nothing from the old per-volume art is assumed to carry over, except the locked Volume V decisions below.

## Pipeline (current stage in bold)
1. **Rough map: E (Dependency Spine) chosen on 16 Sep 2026 and built, with every check passing. Next is stage 2.**
2. Painted map: an image model fills in detail from the chosen SVG (vegetation, town fabric, coves, cliffs).
3. Island blockout in Blender: the heightmap displaces a Grid, empties come from the sites JSON, then sculpting.
4. Hero architecture: the Round, the cothon, the headland city and citadel, the granary and the lock-houses are hand-modelled. Tripo is used only for props (statues, amphorae, ships, the hourglass).
5. Shot pre-vis: one camera per panel, rendered as clay plus a line pass.
6. Comic pass: ligne claire over the pre-vis, checked against the asset sheets.

## How we got here
- **Session of 16 Sep 2026 in `paxos-illustrated`.** That repo holds the published nine-volume site, with art made volume by volume. `volumes.md` summarises the nine stories. `paxos-art-direction.html` is the Volume V art direction, with decisions D01–D19 locked.
- Built `art-direction-grand.html` with island layout options. Instead of drawing the maps by hand, `tools/island_maps.py` builds each option as a real elevation field. From that one field it produces the SVG map, a 16-bit heightmap for Blender, and site coordinates, so stage 3 doesn't have to trace an image.
- **Conflict found:** in the current text only Volumes V and VIII take place on Paxos. Volumes I (Andros/Kea islands), III (Delphi), IV (two islands split by a storm) and VI (Knossos) teach their lesson through the distance between separate places. We kept the user's one-island premise, made it decision G01, and wrote a table showing what each volume becomes on one island. Those separations turned into ground rules for the sites.
- A reviewer pointed out that the page claimed line-of-sight properties that nothing checked. We added ray-cast sightline tests, and the generator now searches for site positions that pass them. This changed the result: option B as first drawn failed two tests (the banquet house wasn't visible from the Round, and there was sea on only one side), so the terrain was reshaped. Option A's hamlets could see each other, so they were moved.
- **Later on 16 Sep:** the user proposed laying the island out along a Detangled graph of the dependencies between the papers (a NW→SE chain: I+III → IV → V → II beside VI → VII beside IX, with VIII next to them), with the Raft islet detached. We built it as option E. The user said to tailor the shape to the graph, not to copy the real Paxos. B was kept as the measured fallback. The user then dropped the shared II/VII site: every volume gets its own zone in the graph's order, and places they had shared are rebuilt per volume.
- Moved the work out of `paxos-illustrated` (whose .git is already 911 MB) into this repo. The papers were copied to `sources/` and are gitignored.

## Locked canon to honour (from `paxos-illustrated/paxos-art-direction.html`)
- **D01, period:** "Lamport's Pastiche". The look is classical Greek, plus exactly the objects the paper names, treated as advanced Paxon crafts: a parchment codex ledger, iron-gall ink, a glass hourglass.
- **D02, the chamber is the Great Round:** an open-air circular assembly theatre (after the ekklesiasteria at Metapontum and Paestum), about 50 m across, sunk into a windswept saddle of the hill above the sea. It has about 14 rows of limestone tiers, 8 radial stairways, a mid-height walkway ring, a sand orchestra with a marble kerb, and a high ashlar ring wall. There are four monumental gateways at the cardinal points, each with bronze-plated double doors and an oak drop-bar. Statues of past legislators stand outside the wall. Oratory has to be visibly impossible, which is why messengers exist.
- **D05, the island:** a Delos-type marble trading port, not Cycladic whitewash. Places: the harbour (stone quays, an outbound merchantman); the agora (stoa, cheese stalls, goat pen by the fountain, a sundial on a pillar); the Statue Walk (town to the Round's main gate, lined with statues); the banquet house (a garden dining house a stone's throw outside the Round's **east** gate, **visible from the tiers**); the scribes' hall; a present-day dig site in the ruined Round; Paxos in decline.

## The pages as they stand
**`art-direction-grand-island-shape.html`** (carved out on 16 Sep 2026) is map E's page. It holds §1 the reading-order table (generated, `ORDER:e`), §2 the map with volume chips, legend, "where things fall" and Measured (`MAP:e`, `STATS:e`), §3 the 23-site gazetteer, §4 the shared places rebuilt per volume, and §5 the Blender spec.

**`art-direction-grand.html`** is the decision document. Its sections:
1. **Scope table:** what each volume becomes on one island. Volume I becomes three hamlets A, K and M (after the chart's a, k, m), hidden from one another. Volume II becomes the headland city. Volume III's Delphi becomes a summit oracle. Volume IV's two islands become two halves split by a strait or causeway. Volume VI's Knossos granary becomes storehouses on the lowland plain. Volume VII's citadel is built on the ruins of the Volume II city. Volume VIII is the Round in ruins, plus lock-houses and ledger cliffs.
2. **Gazetteer:** the 16 shared sites of maps A–D, with a link to E's 23-site gazetteer on the island-shape page.
3. **Five layouts.** A–D use an 8 × 5.5 km world; E uses 11 × 8 km:
   - **A · Crescent:** hills round a north-facing bay. Passes every check.
   - **B · Twin Lobes (previous choice, now the fallback; refined 16 Sep):** two hill masses joined by a curved sand causeway, about 605 m long with its crest at 1.4–2.0 m: dry in calm weather, awash in winter. The Round sits in a real col on the citadel peninsula's neck at 142 m, between a new citadel knoll to the north and the western highland. It sees sea WNW and ESE (165° in total), has the cothon in view, and is 647 m and a 92 m climb from the town. The banquet house is on a graded terrace 160 m due east of the Round and 27 m below it. All 12 checks pass. About 14.8 km².
   - **C · Caldera:** a broken ring round a lagoon, with an oracle cone that has vapours. Fails "sea on both sides of the Round" (it sees 210° as one continuous arc). Its Santorini look clashes with D05.
   - **D · Ridge Spine:** modelled on the real Paxoi (the Lakka bay, the Antipaxos islet, the west cliffs). Passes every check. It has the least iconic silhouette, and the real island is in the Ionian Sea, not the Aegean.
   - **E · Dependency Spine (CHOSEN):** the zones run along the axis `E_AXIS` (1500,1300)→(9800,7200). Walking NW→SE reads the papers in dependency order.
     - **I + II** (new numbering): the NW lobe: hamlets, press, I's beacon pair across the NE bay, and II's oracle summit (~325 m).
     - **III:** the neck, cut by `channel()`, with III's own cothon (the lantern harbour) on the SW shore, the drummers' pair, and a causeway (395 m, crest 1.3–1.8 m).
     - **IV:** the Round in a col at `E_ROUND` (5384,4132), 187 m, between two knolls. A valley and a graded descent lead down to IV's merchant quays at `E_PORT`, with the town on a graded coastal flat.
     - **V beside VI:** V's besieged headland city and siege camps on the NE side face VI's granary plain on the SW, as in the graph.
     - **VII and VIII:** VII's citadel above its own walled harbour on the NE; VIII's guild hall, lock-houses running across the ridge, and the ledger cliffs on the SW.
     - **IX:** the Raft islet across a strait (`channel()` at t .905). Stray islets are drowned by `keep_islands()`.
     - **Checks:** all pass, including "each volume after the ones it builds on (9 links)" and "the graph's five bands don't overlap".
   A, C and D were **not regenerated** after the B refinement. Their SVGs, JSON and Measured panels come from the generator at commit cdc025b. Rerunning them now would apply the new Round/banquet rules and change them.
   Each map has volume filter chips, a heightmap view, and a "Measured" panel with the check results.
4. **Circular harbour:** a Carthage-type cothon (a basin about 300 m across with 7 quays, a central islet with a lantern tower and a channel about 44 m wide). On A–D it sits inside the one shared port. On E it is Volume IV's own harbour, and V and VII have separate harbours.
5. **Scale, time and Volume IX.**
6. **Blender handoff:** the general recipe, with a link to E's exact numbers on the island-shape page.
7. **Decisions export.** The locked choices are pre-checked in the HTML, and a "Decided" box sits under the pipeline.
The page text follows ERAS.md: scope-table rows VII and VIII, and §5's five phases.

## Locked decisions (chosen 16 Sep 2026, in chat rather than via the page export)
**`ERAS.md` (compressed and revised 16 Sep 2026):** on map E, the walk from the NW tip is the dependency order, the story order *and* the volume numbering. The volumes are renumbered (see the note at the top). One generation (about 40 years) in five phases, one per graph band and island zone: 1 hamlets (I, II), 2 passable season (III), 3 Parliament (IV), 4 siege and ledger side by side (V, VI), 5 citadel, guild and Raft (VII, VIII, IX). Only additions; volumes look back, never ahead. The pending `paxos-illustrated` changes (the renumbering itself and the wording) are listed in ERAS.md.

- **G01 World scope: A, one island.**
- **G02 Island form: E, Dependency Spine** (chosen 16 Sep, replacing B, which stays on the page as the measured fallback). Options A, C and D stay on the page as the record.
- **G03 Circular harbour: B (revised 16 Sep with map E).** The cothon is the Passable Season's own lantern harbour. The Parliament has merchant quays and the Citadel a walled harbour, so no site is shared.
- **G04 World scale: 11 × 8 km for E** (A–D stay at 8 × 5.5 km).
- **G05 Time across volumes: A, one terrain.** One generation in five phases, walked NW→SE in story order (see ERAS.md).
- **G06 Volume IX: B, on an islet on the map** (option E's Raft islet, across a strait at the SE end). This reverses the earlier "off-island" answer; the user confirmed it with the E direction.
- **G07 3D files: gitignored.** `.blend`, `.glb` and renders stay out of Git, and renders go to R2 as in the old repo.

Also still open:
- The comic style isn't defined beyond "Franco-Belgian". One candidate is Jacques Martin's *Alix*, which is ligne claire set in antiquity.
- The contents of the common and per-volume asset sheets aren't defined yet.

## Generator notes (`tools/island_maps.py`)
- Each option is a function that builds terrain from primitives (`blob`, `ridge`, `ring`) with domain warp (`warp`) and value noise (`finish`). It returns rough site positions, a hint for the cothon's position, and any rule overrides. `build()` then snaps the cothon to the shore and carves it (basin, islet, channel to deep water), snaps each site to its `RULES` band (elevation range, distance to sea), and runs `place_by_sight()`:
  - The Round goes to the candidate within `round_radius` (default 900 m, 250 m for B) at least 500 m from the town (`ROUND_TOWN_MIN`) that maximises the score: sea seen, two opposed sea arcs, harbour in view, and +300 if `is_saddle()` when `round_saddle` is set.
  - The banquet house goes 120 m or more east of the Round, within 60 m north or south, lower, and visible from it.
  - Hamlets K and M are moved until they're hidden from the hamlets already placed.
  - The second beacon is moved until it's in sight of the first.
- `checks()` writes its results to the sites JSON under `"checks"` and to the page's "Measured" panels.
- Contours use hand-written marching squares, then Chaikin smoothing and RDP simplification. Roads are least-cost Dijkstra paths on a 25 m grid, avoiding water and steep slopes.
- Terrain tools added for B: `grade()` cuts and fills a ramp (the banquet terrace), and `causeway()` lays a Bézier tombolo whose crest and width wander, with shallows fading to the deep. `sea_before` records where the bar crosses former sea, and `measure_causeway()` measures it there.
- Option extras go through the overrides dict: `round_radius` (0 means keep the snapped rough position; E uses that), `round_saddle`, `causeway` as `(ctrl, sea_before)`, `axis` + `order` (the dependency-order check) and `zones` (faint volume numerals on the map).
- `set_world(w, h)` is called first in every option function; the SVG size, compass, scale bar and badge bounds all derive from `W`/`H`. Option E passes its own site list via `rules["sites"]` (`SITES_E`); every loop skips sites an option doesn't place. `harbour_of(loc)` gives the harbour the Round must see (V's `port` on E, else the cothon). `sight_pairs` names the headland pairs to place and check (E: `beacons`, `drummers`). `dependency_order()` checks every `DEPENDS` edge and the `BANDS` sequence along `axis`. Both use the new volume numbers; `PUBLISHED_VOL` maps them back.
- Also added for E: `channel()` cuts a noisy strait square across the axis; `keep_islands()` drowns land not connected to the anchor points; `land_component()` is a flood fill; `dependency_order()` projects sites onto the axis.
- The town is insulae on a street grid squared to the cothon, with an open agora. Badges search for a spot that clears every symbol and sits nearer their own site than any other.
- Known rough edges:
  - The search results depend on the rough positions passed in.
  - B's town climbs the slope between the cothon and the Round, and the agora rect is partly hidden under badge 10 and the walk.
  - The causeway still reads fairly straight at map scale.
  - E's middle is hand-engineered: the Round is pinned (`round_radius` 0), and the graded descent is computed from `E_ROUND`/`E_PORT`. If the terrain above changes, re-check the saddle and harbour-view results.
  - E's symbols render smaller on the page (its viewBox is 2200 wide against 1600 for A–D).
  - E's south-east lobe reads as one mass; its four zones are marked by the numerals more than by the coastline.

## Blender import spec (from the page; option E)
- **Grid:** 881 × 641 vertices, 11000 × 8000 m, so one face per heightmap pixel (`maps/option-e-height.png` is 880 × 640).
- **Displace modifier:** Non-Color, Strength 600, Midlevel 0.2.
- **Site empties:** Blender X = x − 5500, Blender Y = 4000 − y, Z = elevation.
- **Check this on the first import:** site 23's empty (the Raft monastery) must land on the small SE islet. If it lands NW, the image V axis is flipped.
- Option B, if it's ever revived: 641 × 441 vertices, 8000 × 5500 m, X = x − 4000, Y = 2750 − y.

## Next steps
1. Done: decisions locked; map B refined, then option E built and chosen. The page is the local `art-direction-grand.html` (Artifact publishing dropped; see CLAUDE.md).
2. When the user asks, apply ERAS.md's changes to `paxos-illustrated`: renumber the volumes across `volumes.md`, `volume-N.html`, the index, prompts and `detangled-graph.yaml`, and make the wording changes.
3. Optional: names for the town, bays and capes on map E; enlarge E's symbols.
4. Stage 2: write the painted-map prompt with `maps/option-e.svg` as the layout reference (Gemini image model, as in `paxos-illustrated/tools/gen_panel.py`).
5. Stage 3: build the Blender scene from `option-e-height.png` and `option-e-sites.json`, following the spec above. `.blend` files are gitignored (G07).
