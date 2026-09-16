# Stage 2 prompt: the painted map

## How to use it
1. Run `python3 tools/painted_map.py reference`. It writes `maps/island-reference.png` at 2200 × 1650 (4:3).
2. In the Gemini web UI, choose the image model, attach `maps/island-reference.png`, and paste the prompt below. Ask for 4:3 at the highest resolution offered.
3. Download the full-size image and run `python3 tools/painted_map.py register <file>`. It crops and scales the image back into the map's frame as `maps/island-painted.jpg`, then scores how well the painted coastline sits on the heightmap in `maps/island-painted.json`. Red in `maps/island-painted-mismatch.png` shows where the painting strays more than 50 m.
4. If the score is poor, try the fixes at the bottom of this file.

## Prompt

```
Repaint the attached map as a finished, hand-painted illustrated map of an imaginary Greek island. The attached image is a strict layout: keep its framing, coastline, landmasses, bays, straits, islets and hill positions exactly where they are. Do not rotate, crop, zoom, mirror or move anything, and fill the whole frame edge to edge. The flat blue strips along the top and bottom edges are open sea.

View: straight top-down, like a map. No perspective tilt, horizon or sky.

How to read the layout:
- Land colour bands are elevation. Pale sand is beaches and coastal lowland, the greens are rising hills, and the grey-brown patches are bare limestone summits. Keep every hill where its bands are.
- The thin dark line is the coastline. The pale blue edge just offshore is shallow water.
- The long curved spit between the first (north-west) landmass and the second is a low sand causeway, barely above the waves.
- The small south-east islet is separated from the main island by open water. Keep that gap.
- Small terracotta rectangles are single buildings. The dense cluster of them on the north-east coast of the middle landmass is the harbour town.
- The white circle with four small gold squares is an open-air circular assembly theatre, only 50 m across, sitting in the saddle between two hills. Paint it tiny, as a pale stone ring of tiers.
- The blue circle with a white central islet, on the south shore of the north-west landmass, is a round walled harbour basin with a small lighthouse islet in the middle.
- The small black comb shape on the north-east coast is a stone merchant quay.
- The two dark red shapes are a walled hill-town on a headland and a larger fortified citadel further east.
- The black arc at the east tip is a curved harbour breakwater.
- The small white ring in the south-east is a stone guild hall.
- The black hatch marks on the south coast are quarried sea cliffs.
- The white wiggly line from the town up to the theatre is a paved processional way. The thin dashed lines are mule tracks.

Setting: a prosperous Hellenistic trading island in the Aegean, around 150 BC, in the style of Delos. Buildings are ochre limestone and white marble with terracotta roofs, not whitewashed Cycladic cubes.

Landscape: olive groves and stone-walled terraces on the gentle slopes. Dark maquis scrub and umbrella pines on the hills. Bare pale limestone crags on the summits. Golden wheat fields on the low plain of the south-east landmass. Sandy coves, and rocky sea cliffs along the south-west-facing coasts. Water goes from turquoise shallows at the shore to deep Aegean blue offshore. Add a few tiny sailing ships near the harbours with small white wakes.

Scale: the island is about 11 km across. Every building is tiny. Towns read as fine textured clusters and the theatre as a small ring, never as big icons.

Style: Franco-Belgian ligne claire illustration, as in a classic European comic album's endpaper map. Clean, confident dark-brown ink outlines, flat gouache colour with a light watercolour paper texture, warm Mediterranean afternoon light. Palette: warm paper cream (#f2e7cd), dark ink brown (#1c1512), Aegean blue (#136f9e), terracotta (#bf4a26), olive green (#66722c) and ochre gold (#c1912b). Not photographic, not 3D-rendered, no heavy gradients or glow.

Strictly no text, letters, numbers, labels, legend, compass rose, scale bar, border, frame, cartouche, sea monsters, or clouds over the land.

Output the same 4:3 aspect ratio as the attached image, at the highest resolution available.
```

## If the result drifts
- **The coast moved or the island was redrawn.** Start a fresh chat. Attach the reference again and add at the top: "Trace the coastline of the attached image exactly; this is a colouring and texturing job, not a redesign."
- **Text or a compass appeared.** Reply: "Remove all text, labels and the compass; change nothing else."
- **Buildings are too big.** Reply: "Make all buildings about a third of their current size; keep everything else."
- **It came back in a different aspect ratio.** Ask again for 4:3. `register` warns when the ratio is off, and the score will show the distortion.
