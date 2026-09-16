# Eras: one generation, walked from the north-west

_Decided with the user on 16 Sep 2026. This replaces the earlier four-phase plan._

## The rule
On map E, **the walk from the north-west tip is the dependency order, the story order and the volume numbering.**
- **Setting:** one generation (about 40 island years) in a Hellenistic, Delos-type free port, with a resident Italian merchant guild.
- **Five phases:** the five bands of the dependency graph, which are also the five zones of the island. Each phase happens in its own zone, further south-east than the last.
- **Only additions:** buildings are added, never demolished. Zones already passed get older (weathering, more statues, cut cliffs), but they don't change shape.
- **Looking back only:** a volume's text may refer to anything behind the walker, meaning lower-numbered volumes. It refers forward only as a narrator's hint.

## Renumbering
Volumes are numbered in walking order. Within a band, the graph's top-to-bottom order decides.

| New | Title | Published as |
|---|---|---|
| I | The Disordered Sundials | I |
| II | The Curse of the Sleeping Shepherd | III |
| III | The Passable Season | IV |
| IV | The Part-time Parliament | V |
| V | The Generals Before the Walls | II |
| VI | The Ledger of Many Decrees | VI |
| VII | The Citadel of Iron Quorums | VII |
| VIII | The Quarries of the Roman Guilds | VIII |
| IX | The Reformation of the Raft Monks | IX |

`tools/island_maps.py` holds this as `PUBLISHED_VOL`. Map E and `art-direction-grand-island-shape.html` use the new numbers. Maps A–D and the grand page's scope table and 16-site gazetteer still use the published numbers.

## Phases (new numbering)
| Phase | Years | Zone on map E | Volumes | What happens there |
|---|---|---|---|---|
| 1 · The hamlets | 0–8 | First lobe, 0–2.3 km | I, II | Hamlets with no common clock, each hidden from the others (I). The shepherd's curse at the summit oracle (II). The neck and the col are still empty. |
| 2 · The passable season | 8–14 | The neck, 2.6–3.6 km | III | The navigators' doctrine at the lantern harbour. The causeway that winter seas close. |
| 3 · The Parliament | 14–22 | The col, 4.8–5.5 km | IV | The Round is built in the col, then the Statue Walk, the merchant quays and the town. |
| 4 · Siege and ledger | 22–30 | Either side of the spine, 6.3–7.1 km | V, VI | Two things happen at once, facing each other across the spine. Traitor commanders besiege the headland city, which proves the 3f+1 bound (V). The granary clerks keep the ledger under a standing consul (VI). |
| 5 · Citadel, guild, Raft | 30–40 | The far lobe and the islet, 7.8–9.9 km | VII, VIII, IX | The citadel above its own harbour combines V's bound with VI's views (VII). The Italian guild's hall, lock-houses and quarry cliffs (VIII). The monks cross the strait to the islet (IX). |

The distances come from the generated reading-order table on `art-direction-grand-island-shape.html`.

## What never changes (the common asset sheet)
- The terrain, coastline and causeway.
- The building kit: ashlar, marble, timber quays.
- Costume, ship types and palette.

In Blender, each phase is one collection covering one zone. Later phases add a weathering pass to the earlier zones.

## Changes for `paxos-illustrated` (not yet made)
Section names below use the **published** numbers, as they appear in `volumes.md` today.
- **Renumber** the volumes in `volumes.md`, `volume-N.html`, `index.html`, the cover prompts and `detangled-graph.yaml` (its ids and tour order), including every in-text "Volume N" cross-reference.
- **Published II (new V):** "three centuries before the citadel of Volume VII was built on top of it" becomes "a few years before the citadel of Volume VII was built on it". "It" is the bound. The siege now comes after the Parliament.
- **Published IV (new III):** "two islands cut apart by a storm" becomes the island's two halves, cut apart at the neck when winter seas cover the causeway.
- **Published VII:** "For five hundred years the 3f+1 Law of Volume II…" becomes "Since the siege, the 3f+1 Law of Volume V…".
- **Published VIII:** "Roman engineers" become the Italian guild's engineers, and they work in their own guild hall. "Decades of micro-decrees" becomes "years of micro-decrees".
- **Published IX:** "sailed north" becomes "crossed the strait to the islet".
- **D05's present-day dig and "Paxos in decline":** these survive only as a narrator's frame and aren't modelled.
