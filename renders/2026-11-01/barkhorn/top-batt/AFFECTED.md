# Which published images carry the top batt's wedge (2026-11-01)

**Only pictures rendered from the linked asset are affected:** `tropos.blend` as built at 8e44484e, before the fix in
c77460f0.
- The studio engine (`studio/engine/render.py`) never collapses a mesh. It reads the CAD's render model whole, so
  nothing it rendered has the wedge.
- The biomes lane's own asset builder (`tropos_lib.py`) leaves meshes under 4,000 faces whole, so its frames are clean
  too. Since 38ff63d (22:13), though, biomes links this lane's asset.

| image | rendered by | wedge? | at its published size |
|---|---|---|---|
| The covers-off room, golden hour (754e16a9: `tropos-room-golden-hour-off.png` and `-portrait`): the deck's home slide, the site's At home band, the brand book's `room.jpg` and `room-portrait.jpg` | studio engine | **no** | clean: the top batts are rectangles |
| The cover-on room (`tropos-room-golden-hour.png`) | studio engine | no | the cover is on, and the engine mesh is whole |
| Strata finals (`design-strata.png`, `design-strata-room.png`), every design-pass proof, the horn-choice finals | studio engine | no | — |
| `four-pieces-day` (1920 and 3840), r48-four-pieces fe292a3d | the linked asset | **yes** | **plainly visible**: the owner saw it at 1920 |
| `four-pieces-dusk` (1920 and 3840), the same | the linked asset | **yes** | **plainly visible**: the lamps' light makes it brighter |
| four-pieces proofs r6 and r7 (`proofs/r6-*.png`, the v3 rounds) | the linked asset | yes | visible; proofs only |
| biomes `planet-earf-pano` (1200, 2400, master 4800), r48-biomes d672199 | the linked asset | **yes** | **visible at 2400** in Ice and Haze, faint in the others; at 1200 a pale fleck |
| biomes `seam-acid-ember-cg-1800` (a3a5fb3) | the linked asset | **yes** | **visible** in Acid; Ember is too dark to show it |
| biomes `seam-poison-fog-plates-1800` (326116d) | the linked asset | **yes** | faint in Poison and Fog |
| biomes `proof7-pano`, `proof7-planet` | the linked asset | yes | proofs only |

**To re-render:** four-pieces day and dusk, and the three biomes frames (the pano and two seams). Each lane re-links
`tropos.blend` at c77460f0 or later; or, for Strata, `tropos-strata.blend`.

**Not checked from here:** the brand lane's pins. Its book pins only `room.jpg` and `room-portrait.jpg` from 754e16a9,
which are clean. The site lane's branch is not fetchable here; if it took a four-pieces or biomes frame, that frame is
affected.
