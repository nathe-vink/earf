# The dioramas: a brief (round 31)

Eight editorial images, one for each Atmosphere colour. Each speaker stands in a hand-made miniature world of its own:
its earth setting, built from felt, fabric, paper, wool, glass and resin, and photographed through a tilt-shift lens.
They are for the site (earf.world: each colour's page and the colour picker) and the look book. Each one should be good
enough to run as a luxury house's campaign image.

## The owner, verbatim

- "Would also be good to be able to see any color in a room vs just poison, but have the rooms be suited to the color.
  Doesn't even need to be a room. Could look like a little themed diorama with stop motion type settings, suited to
  each color, like fog on felt fog clouds in the sky."
- "Need cuter, more dreamlike. Tilt shift was the term I was thinking of earlier."
- "I'm imagining using different textures for each setting. Like the ember one could be in the depths of hell, with
  fabric, underlit embers billowing upward."
- "I want some really high quality editorial shit, that really sets each speaker in its appropriate earth setting.
  Something you'd see a luxury brand do."

## What makes the eight one campaign

- **Tilt-shift miniature.** The camera stands above the speaker and looks down 16 to 32 degrees, through a 50 to 100 mm
  lens. Focus falls on the speaker's front face, and the depth of field is a model's: `common.tilt_shift(...,
  miniature=8..16)`. The foreground and the distance melt into soft blur, while a band through the speaker stays crisp.
  Check the speaker's far edges, the horn's rim and the back corners: they must be sharp.
- **Cute and dreamlike.** Make the forms soft, rounded and generous: chunky felt, plump puffs, toy proportions. The set
  is scaled to the speaker as if the speaker were a toy in a toy world, so a toadstool can stand as tall as the
  cabinet and a cloud as wide as the horn. Light should be soft and glowing, with gentle bloom on anything that gives
  light. Let it feel a little unreal, the way a dream does, and never cluttered.
- **Craft, at model scale.** Every piece is a material a model-maker would use, and each world has its own texture
  vocabulary: no two sets lean on the same materials. Set the set's `kit_scale` to about the camera's `miniature`, so
  fibres, weave and grain read as felt and fabric on a model rather than on a building.
- **The speaker is the hero.**
  - Use the product model exactly as it is, in its own flavour. Leave the cover off unless the set wants it on.
  - Show the whole speaker, crisp, with its silhouette clear of clutter, at about 35 to 50 % of the frame's height.
    Place it on a third or centred.
  - Its acrylic should catch the world's light, because that is the point of the colour: light through it, glowing
    edges, coloured light cast on the ground.
  - Nothing sharp stands in front of it. Out-of-focus pieces may frame the edges.
- **One idea of light per world**, motivated by the set (embers below, a low sun, the moon, a lit window, a glow from the
  ground). Keep a rim or glow that separates the speaker from what is behind it.
- **Palette.** Tonal, built around the speaker's own colour, with at most one accent. Rich, never muddy. Lift the blacks
  slightly into the world's own shadow colour (`finish.dream.lift_color`).
- **Finish.** Use `common.finish(...)`: bloom on light sources, a vibrance of 0.1 to 0.25, a lift of 0.02 to 0.06 and a
  vignette of 0.15 to 0.3. Keep it subtle; the set does the work.
- **Wit.** The brand is "sophisticated, but witty" (the owner on the copy). One small joke per set is welcome, if it is
  quiet: a skull hidden in Poison, a roadrunner's streak in Dust.
- **Touchstones for tone, not for copying:**
  - Hermès window displays and Loewe still lifes, for craft and restraint;
  - Laika and Wes Anderson's stop-motion, for felt, fabric and charm;
  - Apple's felt holiday film, for warmth;
  - tilt-shift photographs of real cities, which make the world look like a toy.

## The eight worlds

These are starting points. Each set's session owns its concept, but it must read at once as its atmosphere, and it
should echo its icon's shapes (`spinoffs/barkhorn/icons.py`; the pictograms are in `brand/icons/`).

| Colour (module) | Acrylic, flavour | Line | Icon |
|---|---|---|---|
| Ember (`ember`) | translucent red, `cloud-red` | The part of the fire that stays up late. | flames: three triangles standing on a bar, a campfire |
| Dust (`dust`) | translucent orange, `cloud-orange` | Settles in nicely. | a roadrunner's dust streak: three small circles trailing a flat wedge along the ground |
| Acid (`acid`) | golden yellow, `cloud-amber` | A yellow with opinions. | a drop with two bubbles cut out of it |
| Poison (`poison`) | bottle green, `eucalyptus-y2k-green` | Green, and not the healthy kind. | a skull |
| Ice (`ice`) | ice blue, `cloud-blue` | Keeps its cool. | three icicles hanging from a bar |
| Haze (`haze`) | violet, `cloud-violet` | Dusk, kept indoors. | a sun behind three bars of haze |
| Fog (`fog`) | water-clear, `birch-fog-clear` | Now you see it. | the cloud: three circles on a bar |
| Smoke (`smoke`) | smoked black, `cloud-black` | Where there's smoke. | a plume drifting left to right, as from a train's stack |

- **Ember: the depths of hell, in fabric** (the owner's own picture).
  - Make a cavern of draped crimson, oxblood and black velvet and satin, its folds like rock strata.
  - Below, a fissure of glowing embers; embers billow upward in plumes (`scatter` with `plume`, `glow`) and light
    everything from beneath.
  - Add felt flames shaped like the icon, and a heat haze if it helps.
  - The red acrylic should glow, lit through from below.
- **Dust: a desert at golden hour, in suede, corduroy and sand.**
  - Ribbed corduroy dunes and suede mesas under a big low tissue-paper sun.
  - Felt puffs kicked up in a streak along the ground, as in the icon (the roadrunner's), with dust motes in the
    raking light and long shadows.
  - Palette: terracotta, rust and apricot.
- **Acid: acid rain, in glass and resin.**
  - A wool or felt cloud rains yellow resin drops on fine threads. Below: glossy puddles with ripple rings, and glass
    bubbles.
  - A sour palette, chartreuse to lemon, backlit so the drops glow.
  - Candy-like, slightly toxic, delightful.
- **Poison: a poison garden, in moss, velvet and clay.**
  - Moss flocking, velvet toadstools with felt spots, clay nightshade berries and foxgloves.
  - A glossy green resin swamp with glass bubbles rising, and a crooked tree.
  - A faint glow of spores and low mist. A tiny skull somewhere.
- **Ice: a frozen grotto, in glass and wool.**
  - Glass icicles hang from above as in the icon. Below: cotton-wool snowdrifts, paper snowflakes on threads and a
    frosted glass lake.
  - A cold blue glow from beneath, with silver highlights.
- **Haze: dusk, in layered paper and tulle.**
  - Cut-paper hills recede in graded violets and lilacs, like a paper theatre.
  - A big tissue-paper sun sits low and glowing, with three bands of tulle haze drifting across it (the icon).
  - The sky grades from violet to peach.
- **Fog: a sky of felt clouds on threads, and cotton-wool fog** (the owner's own example).
  - White on pale blue-grey, high-key, like dawn. The clear speaker is half veiled by fog.
  - The softest of the eight. A first sketch is in `fog.py`; make it far better.
- **Smoke: night, in charcoal wool and black card.**
  - A little steam train or a row of chimneys in black lacquered card, with grey wool smoke billowing in the icon's
    plume.
  - A paper moon and warm lit windows.
  - Moody, but cute.

## Process

1. **Get the speaker's model.** It is not in git (it is generated). If
   `spinoffs/barkhorn/out-cloud/render/barkhorn-cloud.glb` is missing, build it (about ten minutes; design your set
   meanwhile):

       .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/cloud.py --out spinoffs/barkhorn/out-cloud --skip step,stl,drawings

   Commit nothing under `spinoffs/barkhorn/out-cloud/`.
2. **Concepts.** Make two or three quick concept proofs, then pick one and say why in your notes.
3. **Proof, look, critique, change.**
   - Proofs: `--scale 0.3 --samples 24`, about a minute or two each.
   - Mid proofs: `--scale 0.5 --samples 64`.
   - Look at every proof yourself, at full size and cropped on the speaker.
   - Ask of each: Does it read at once as its atmosphere? Is it cute and dreamlike? Does the tilt-shift sell the
     miniature? Is the speaker the crisp, well-lit hero, its colour glowing, its silhouette clean? Do the materials read
     as real craft at model scale? Would a luxury house run it (composition, restraint, palette)? Is anything
     distracting: intersections, floating pieces, noise, fireflies, a seam, a piece cut by the frame awkwardly?
   - Iterate until the honest answer is yes. Expect six to ten proof rounds.
4. **Finals.**
   - The landscape frame, 2400 x 1600, at 256 samples or more (more if the glows are noisy).
   - The portrait frame, 4:5, 1600 x 2000, from the same set: `portrait()`, the camera re-framed rather than cropped.
   - Look at both at full size before you call them done.

## Files and commands

| Path | What |
|---|---|
| `spinoffs/barkhorn/dioramas/<name>.py` | your set: `shot()` (landscape) and `portrait()`, built with `common.py`'s helpers |
| `studio/engine/kit_ext/<name>.py` | any kit pieces of your own (`shape: "ext", module: "<name>", fn: ...`; see `kit.py`'s doc) |
| `studio/shots/barkhorn/diorama31/<name>.json`, `<name>-portrait.json` | written by `python3 spinoffs/barkhorn/dioramas/build.py <name>` |
| `renders/2026-10-18/barkhorn/diorama31/<name>.png`, `<name>-portrait.png` | the finals, each with its `.report.json` and `.shot.json` (not `.raw.png` or masks) |
| `spinoffs/barkhorn/dioramas/<name>.md` | your notes: the concept and why, each proof round (what changed and why, briefly), the final settings and render times |

    python3 spinoffs/barkhorn/dioramas/build.py <name>
    python3 studio/engine/render.py studio/shots/barkhorn/diorama31/<name>.json --out OUT.png [--samples N --scale S]

- Kit shapes and materials are documented in `studio/engine/kit.py`. The camera, lights, finish and frame helpers are
  in `common.py`. Every setting a shot file takes is listed in `studio/engine/knobs.py`. A `sweep` gives a paper sky and
  floor; a `stage` gives only your props, if you build your own ground. A `haze` box is a scattering volume (see
  `studio/engine/sets.py`). The sky can be a `gradient`, `none` or `hdri`.
- Edit only your own files. `common.py`, `build.py`, `BRIEF.md`, the engine core (`render.py`, `sets.py`, `lights.py`,
  `kit.py`, `finish.py`, `materials.py`) and other colours' files are shared. If a change to the core is truly needed,
  keep it minimal and backward compatible, put it in its own commit, and say so in your report.
- Proofs live in your scratchpad, not in git. Keep every committed PNG under 5 MB; if a final is larger, commit a
  quality-92 JPG of it instead.
- Never touch the product: its model, its flavours, `studio/products/`, or the speaker's CAD. If the speaker seems
  wrong, say so; don't change it.
