# Bake-off results (2026-11-19)

Blind vote by Chris on the page https://claude.ai/artifact/VgN4nGuFEpHpV1ST72KdDi. Letters revealed from `key.json` after voting.

## Winner: OpenAI image generation through the Codex CLI (`O-ras`)

| Generator | Points (best 2, second 1) | Best picks |
|---|---|---|
| O-ras: OpenAI via Codex, traced | 11 | 4 of 5 |
| R-vec: Recraft V4 Styles vector, traced | 2 | 1 of 5 |
| R-ras: Recraft V4 Styles raster, traced | 0 | 0 of 5 |

Recraft also broke the brief's 3-4 color limit on every image (5-6 colors). Cost: Recraft $1.08 of $5; Codex runs on the ChatGPT plan.

## Per bird

| Bird | Best | Second | Notes from the vote |
|---|---|---|---|
| American Kestrel | B (O-ras-23) | C (O-ras-11) | B is closest to the vision. Liked the pop of blue in A (R-vec-23). |
| Black Skimmer | C (O-ras-11) | D (O-ras-23) | Likes the negative space in both. Try a Klein-blue bill tip instead of black. |
| Brown Pelican | A (R-vec-23) | D (O-ras-23) | D has the best bill but loses detail small; A is a little sloppy large. Try the eye of A or B (R-ras-23) on D. |
| Eastern Screech-Owl | none | none | All fail. Wants a straight-ahead (frontal) portrait. F (R-ras-11) was least bad. |
| Great Blue Heron | C (O-ras-11) | - | Head of B (R-ras-11), neck of C. C reads best small. |
| Northern Bobwhite | B (O-ras-23) | - | - |

## Decision

Generate the full set of 30 with the Codex route: reference photo measurements in `references.json`, the shared prompt template in `run.py`, then `trace_icon.py` into the house frame and palette. Apply the notes above as prompt changes. Draw the Eastern Screech-Owl (and the Barn Owl) as frontal portraits, as the brief allows for owls.
