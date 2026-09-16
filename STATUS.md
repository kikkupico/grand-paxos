# Status: grand art direction

_Last updated 16 Sep 2026._

## The brief (the user's four expectations)
1. Every volume's story takes place on the island of Paxos, except perhaps Volume IX.
2. The whole island is pre-visualised in Blender. Key architecture gets detailed models: the Volume V chamber (the Great Round), the Volume IV circular harbour, and so on.
3. Each illustration starts as a Blender pre-vis render and is then turned into a Franco-Belgian comic image.
4. There is one common asset sheet for the whole series, plus an asset sheet for each volume.

The user explicitly allowed starting afresh. Nothing from the old per-volume art is assumed to carry over, except the locked Volume V decisions below.

## Pipeline (current stage in bold)
1. **Rough map: B chosen and refined. Next is stage 2.**
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
- Moved the work out of `paxos-illustrated` (whose .git is already 911 MB) into this repo. The papers were copied to `sources/` and are gitignored.

## Locked canon to honour (from `paxos-illustrated/paxos-art-direction.html`)
- **D01, period:** "Lamport's Pastiche". The look is classical Greek, plus exactly the objects the paper names, treated as advanced Paxon crafts: a parchment codex ledger, iron-gall ink, a glass hourglass.
- **D02, the chamber is the Great Round:** an open-air circular assembly theatre (after the ekklesiasteria at Metapontum and Paestum), about 50 m across, sunk into a windswept saddle of the hill above the sea. It has about 14 rows of limestone tiers, 8 radial stairways, a mid-height walkway ring, a sand orchestra with a marble kerb, and a high ashlar ring wall. There are four monumental gateways at the cardinal points, each with bronze-plated double doors and an oak drop-bar. Statues of past legislators stand outside the wall. Oratory has to be visibly impossible, which is why messengers exist.
- **D05, the island:** a Delos-type marble trading port, not Cycladic whitewash. Places: the harbour (stone quays, an outbound merchantman); the agora (stoa, cheese stalls, goat pen by the fountain, a sundial on a pillar); the Statue Walk (town to the Round's main gate, lined with statues); the banquet house (a garden dining house a stone's throw outside the Round's **east** gate, **visible from the tiers**); the scribes' hall; a present-day dig site in the ruined Round; Paxos in decline.

## The page as it stands (`art-direction-grand.html`)
1. **Scope table:** what each volume becomes on one island. Volume I becomes three hamlets A, K and M (after the chart's a, k, m), hidden from one another. Volume II becomes the headland city. Volume III's Delphi becomes a summit oracle. Volume IV's two islands become two halves split by a strait or causeway. Volume VI's Knossos granary becomes storehouses on the lowland plain. Volume VII's citadel is built on the ruins of the Volume II city. Volume VIII is the Round in ruins, plus lock-houses and ledger cliffs.
2. **Gazetteer:** 16 numbered sites with ground rules, defined in the generator as `SITES`/`RULES`, plus the Statue Walk road.
3. **Four layouts on the same 8 × 5.5 km world:**
   - **A · Crescent:** hills round a north-facing bay. Passes every check.
   - **B · Twin Lobes (CHOSEN, refined 16 Sep):** two hill masses joined by a curved sand causeway, about 605 m long with its crest at 1.4–2.0 m: dry in calm weather, awash in winter. The Round sits in a real col on the citadel peninsula's neck at 142 m, between a new citadel knoll to the north and the western highland. It sees sea WNW and ESE (165° in total), has the cothon in view, and is 647 m and a 92 m climb from the town. The banquet house is on a graded terrace 160 m due east of the Round and 27 m below it. All 12 checks pass. About 14.8 km².
   - **C · Caldera:** a broken ring round a lagoon, with an oracle cone that has vapours. Fails "sea on both sides of the Round" (it sees 210° as one continuous arc). Its Santorini look clashes with D05.
   - **D · Ridge Spine:** modelled on the real Paxoi (the Lakka bay, the Antipaxos islet, the west cliffs). Passes every check. It has the least iconic silhouette, and the real island is in the Ionian Sea, not the Aegean.
   A, C and D were **not regenerated** after the B refinement. Their SVGs, JSON and Measured panels come from the generator at commit cdc025b. Rerunning them now would apply the new Round/banquet rules and change them.
   Each map has volume filter chips, a heightmap view, and a "Measured" panel with the check results.
4. **Circular harbour:** a Carthage-type cothon (a basin about 300 m across with 7 quays, a central islet with a lantern tower and a channel about 44 m wide), set inside the Delos-type port. It serves Volumes IV, V and VII.
5. **Scale, time and Volume IX.**
6. **Blender handoff spec:** see below.
7. **Decisions export.** The locked choices are pre-checked in the HTML, and a "Decided" box sits under the pipeline.
The page text now follows ERAS.md: the scope table rows VII and VIII, site 16 renamed "Italian guild lock-houses", and §5's four phases.

## Locked decisions (chosen 16 Sep 2026, in chat rather than via the page export)
**`ERAS.md` refines G05** (agreed in a side thread): one generation (about 40 years) in a Hellenistic Delos-type port, four additive phases, the Volume VII citadel on the same footprint as the Volume II city, and the Volume VIII "Romans" as the resident Italian guild. Read it before touching eras or assets. It also lists pending text edits to `paxos-illustrated/volumes.md`, which haven't been made yet.

- **G01 World scope: A, one island.**
- **G02 Island form: B, Twin Lobes.** Options A, C and D stay on the page as the record.
- **G03 Circular harbour: A, a cothon inside the main port.**
- **G04 World scale: B, 8 × 5.5 km as drafted.**
- **G05 Time across volumes: A, one terrain with era collections.** Ruins are variants.
- **G06 Volume IX: A, off-island on a misty northern coast.** Reopened by ERAS.md: the alternative is a monastery on the east lobe's north shore, cut off when the causeway is awash. Waiting for the user.
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
- Option extras go through the overrides dict: `round_radius`, `round_saddle`, and `causeway` as `(ctrl, sea_before)`.
- The town is insulae on a street grid squared to the cothon, with an open agora. Badges search for a spot that clears every symbol and sits nearer their own site than any other.
- Known rough edges:
  - The search results depend on the rough positions passed in.
  - B's town climbs the slope between the cothon and the Round, and the agora rect is partly hidden under badge 10 and the walk.
  - The causeway still reads fairly straight at map scale.

## Blender import spec (from the page)
- **Grid:** 641 × 441 vertices, 8000 × 5500 m, so one face per heightmap pixel.
- **Displace modifier:** texture `maps/option-<k>-height.png`, Non-Color, Strength 600, Midlevel 0.2.
- **Site empties:** Blender X = x − 4000, Blender Y = 2750 − y, Z = elevation.
- **Check this on the first import:** option B's citadel empty must land on the northern peninsula, on land. If it lands in water to the south, the image V axis is flipped.

## Next steps
1. Done: decisions locked, and map B refined. **Not yet republished.** The live Artifact is still draft 0.1, byte-identical to commit cdc025b apart from the service wrapper. The Artifact tool refuses a republish until the saved live copy has been Read line by line, and because of the inline map SVGs that's about 265k tokens. Options: do that read once, publish to a new URL (then update CLAUDE.md), or slim the page first by moving the SVGs out into `files`.
2. Get the user's answer on G06 (Volume IX off-island, or the east-lobe monastery). If it goes on the island, add a site to `SITES`/`RULES` and to option B.
3. Optional: names for the town, bays and capes on map B.
4. Stage 2: write the painted-map prompt with the chosen SVG as the layout reference (Gemini image model, as in `paxos-illustrated/tools/gen_panel.py`).
5. Stage 3: build the Blender scene from the heightmap and sites JSON, following the spec above. `.blend` files are gitignored (G07).
