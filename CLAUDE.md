# grand-paxos

This is the grand art direction for *Distributed Algorithms of Ancient Greece*, the nine-volume illustrated series. The finished site is in the sibling repo `~/Projects/paxos-illustrated`. This repo re-imagines the art as **one island, Paxos**, pre-visualised in Blender and then drawn as a Franco-Belgian comic.

**Read `STATUS.md` before doing anything.** It has the current stage, the decisions still open, how the work got here, and what to do next.

## Layout
- `art-direction-grand.html` is the decision document. The local file is the canonical copy: open it in a browser. The user dropped Artifact publishing on 16 Sep 2026. The old private Artifact (https://claude.ai/artifact/1HDedXGor4CoRNoi8aQ7ho) is stuck at draft 0.1, so don't republish it unless asked.
- `tools/island_maps.py` generates the island options and injects them into the HTML between `<!-- MAP:k -->`, `<!-- STATS:k -->` and `<!-- THUMB:k -->` markers. Never hand-edit the content between those markers.
- `maps/option-{a,b,c,d}{.svg,-height.png,-sites.json}` are generator outputs. Commit them, because they are the spec.
- `sources/` holds the original papers as PDFs (gitignored). Its `README.md` indexes them by volume.

## Commands
- `python3 tools/island_maps.py [a b c d]` regenerates the maps, heightmaps, site JSON and HTML blocks (about 10 s). It prints the site elevations and the sightline checks.
- To render an SVG or the page for a visual check: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars --window-size=1600,1100 --screenshot=<out.png> file://<path>`.

## Environment
- The system `python3` has only `numpy` and `Pillow` (no scipy, skimage or matplotlib), so contouring and pathfinding are hand-written.
- Blender: `/Applications/Blender.app`, with the CLI at `~/.local/bin/blender`.
- The env has `GEMINI_API_KEY`, `TRIPO_API_KEY` and `MESHY_API_KEY`. The old repo's image tool is `paxos-illustrated/tools/gen_panel.py`, which uses `gemini-3-pro-image` with reference images.

## Conventions
- House palette and type (from `paxos-illustrated/assets/paxos-illustrated.css`, inlined in the HTML): ink `#1c1512`, paper `#f2e7cd`, paper-hi `#faf3e0`, aegean `#136f9e`, terra `#bf4a26`, olive `#66722c`, gold `#c1912b`, caption `#ffe36e`. Headings use Optima/Gill Sans; body text uses Georgia.
- The HTML follows the Artifact page contract: no `<!doctype>`, `<html>`, `<head>` or `<body>` tags, no viewport meta, and `<title>` first.
- Decisions use the `fieldset.decision` pattern with IDs `G01…`. Choices are stored in localStorage under the key `paxos-grand-art-direction-v1` and exported as Markdown, which the user pastes back into the session.
- World coordinates are metres, with x pointing east (0–8000) and y pointing south (0–5500). One SVG unit is 5 m. The heightmap maps −120 m to 0 and +480 m to 65535.
