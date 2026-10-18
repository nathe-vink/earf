# In their element: a brief (round 31b)

Eight campaign images, one for each Atmosphere colour, each with a 4:5 frame. Each one puts the speaker on location in
its element, photographed. They replace round 31's dioramas, which the owner turned down. The bar: promotional images
for a product that sells at about $20,000. They are for earf.world (the home page, each colour's page) and the look
book.

## The owner, verbatim

- On the dioramas: "Smoke is too hard to see and the diorama looks cheap, like a bad video game. I was hoping for more
  texture in a lot of these. The speakers are too stark in contrast to the setting too. Tilt shift may have been a bad
  direction. Lighting in general in a lot of them is off. I don't like the strings in the acid rain. Maybe don't think
  about them so much like dioramas, and think more about placing them in there element, so to speak."
- "Continue to do critic passes until you feel it's in a good enough place for promotional images for a $20K product.
  Install any skills or software you need to make it happen. Tokenmaxx my guy."
- Earlier, still true: "really high quality editorial shit, that really sets each speaker in its appropriate earth
  setting. Something you'd see a luxury brand do"; "It's important to stay on the theme of earth and placing the
  speakers in their respective atmospheres"; "All of them should be looking at the speaker in a way that's more level
  with the speaker, with the speaker turned slightly in either direction depending on the setting." Ember: "a volcanic
  cavern", "well lit by lava pools and lava falls". Dust: "something like a tumbleweed too, with the big flat desert
  plateaus in the back". Poison: "a more lush fern and redwood rainforest". Fog: "the speaker sitting on thick ...
  clouds, with blue skies in the backdrop, a flock of birds in the distance out of focus". Ice: "a snow covered wood
  cabin in the back" (a subtle nod).

## What the eight share

- **A photograph, not a render.** Real places at real scale, built from photographed assets:
  - Poly Haven's environments, PBR textures and scanned models, and ambientCG's textures, all CC0 and fetched and
    cached by `studio/engine/assets.py`;
  - plus anything you model yourself in a `kit_ext` module.
  
  No felt, no miniatures, no tilt-shift, no threads, no flat colours. Every surface needs real micro-texture at the
  scale it is seen.
- **The speaker belongs there.**
  - It is lit by the scene's own light: the photographed sky, a sun lamp matched to the sky's sun
    (`common.sun_from_sky`: one sun, one set of shadows), and the scene's practical light (lava, a window). On location
    a photographer may add a reflector or a soft bounce, motivated and subtle, never a studio key.
  - It stands on the ground: feet sunk a few millimetres into sand, snow or moss (the instance's z, e.g. -0.008), a
    contact shadow, the ground's colour bounced into it, and its own colour thrown onto the ground through its acrylic.
  - It is graded with the scene, never apart from it: one grade, and blacks and whites that match. The owner found the
    speakers "too stark in contrast to the setting".
- **The speaker is the hero.** It reads at a glance: its silhouette clear, its tinted acrylic glowing with the light
  coming through it, crisp in the plane of focus, its colour true. Aim for 35 to 55 % of the frame's height, placed on
  a third or centred, with room for type. Smoke and Fog need the most care: black and clear acrylic disappear against
  the wrong ground. Smoke must read at once.
- **The camera is a photographer's.** At eye level with the speaker (about 0.7 to 1.2 m), a 35 to 85 mm lens, f/2.8 to
  f/8 at real scale, verticals kept straight (`level`). The speaker is turned 10 to 30 degrees one way or the other to
  suit the setting. No miniature depth of field.
- **The light is right.** One idea of light per image, physically coherent: golden hour, blue hour, a shaft through
  mist, lava glow. Its direction, softness and colour should agree everywhere. Use the AgX view, so highlights roll off
  like film.
- **Atmosphere and depth.** Haze, mist, steam, dust or smoke should separate the planes and carry the light, with a
  foreground out of focus where it helps. Hide the seam where the modelled ground meets the photographed sky (haze,
  terrain, framing).
- **Restraint.** A luxury campaign, not a busy scene: a few strong elements, one idea, nothing that competes with the
  speaker. The owner's earlier note still holds: not "both empty and cluttered at the same time".
- **Craft.**
  - No noise, fireflies, banding, tiling, stretched textures, floating or intersecting objects, or obvious repeats of
    one model.
  - The background should be sharp enough for its distance. A 4k sky is the minimum where it shows; use 8k where it is
    in focus, or put it out of focus.
  - Finals: 2400 x 1600 (landscape) and 1600 x 2000 (portrait), at 512 to 1024 samples with the denoiser. Look at each
    at full size before calling it done.

## The eight, and the second concepts

Each image needs a real place on earth that reads at once as its atmosphere. Five colours have two sessions, each with
its own concept; the critic's duels and the owner choose between them.

| Colour | Acrylic, flavour | Line | Concept A | Concept B |
|---|---|---|---|---|
| Ember | translucent red, `cloud-red` | The part of the fire that stays up late. | a volcanic cavern or lava field at blue hour or night: black basalt (columns, ropy pahoehoe), lit by lava pools and a lava fall; embers, heat shimmer, steam | — |
| Dust | translucent orange, `cloud-orange` | Settles in nicely. | the desert at golden hour: wind-rippled red sand, the big flat sandstone plateaus behind (mesas, Monument Valley's spirit), a tumbleweed, dust in the raking light, long shadows | — |
| Acid | golden yellow, `cloud-amber` | A yellow with opinions. | an acid spring: sulphur-yellow mineral terraces and green acid pools in the spirit of Dallol (Ethiopia) or Yellowstone, crusts, steam, a hard sun | acid rain: a storm in sulphurous light over wet black rock, real rain as streaks and splashes (no strings), puddles that mirror the speaker |
| Poison | bottle green, `eucalyptus-y2k-green` | Green, and not the healthy kind. | a lush redwood and fern rainforest: towering fibrous trunks, ferns, moss over a fallen log, a few poisonous toadstools, light in shafts through mist | — |
| Ice | ice blue, `cloud-blue` | Keeps its cool. | snow country at blue hour: deep fresh snow, snow-laden firs, a log cabin far behind with one warm window (the owner's nod) | glacier ice: inside a blue glacier ice cave, or blue icebergs on black volcanic sand (Jökulsárlón's Diamond Beach), light through the ice as through the acrylic |
| Haze | violet, `cloud-violet` | Dusk, kept indoors. | a lavender field at dusk, hills receding in violet haze, the sun low behind the bands of haze (the icon) | coastal or desert hills at blue hour, layer after layer of haze between them, a pale sun sinking into it |
| Fog | water-clear, `birch-fog-clear` | Now you see it. | the owner's picture, made real: on a rocky summit above a sea of clouds, a clear blue sky, a flock of birds far off and out of focus | San Francisco's fog: a headland at dawn with the fog pouring over the coastal hills, gulls far off |
| Smoke | smoked black, `cloud-black` | Where there's smoke. | woodsmoke backlit in a pine forest at dawn: shafts of low sun through the smoke, the black speaker rimmed in light against the glow | high-key: a misty birch wood on a white winter morning, woodsmoke drifting, the black speaker sharp against pale mist |

## Process

1. **Branch.** From the latest main, which carries the toolkit, start a fresh branch: `r31-element-<name>` for concept A,
   or `r31-element-<name>-b` for concept B. Work in `spinoffs/barkhorn/elements/<name>.py` (A) or `<name>_b.py` (B).
   Reuse anything from your diorama work that helps, but commit none of the diorama set to the new branch.
2. **Set up.** Run `studio/setup.sh`. On a python3 newer than 3.11, bpy lives on python3.11 and the renderer switches to
   it. If the speaker's model is missing, build it:

       .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/cloud.py --out spinoffs/barkhorn/out-cloud --skip step,stl,drawings

   Then run `git checkout -- spinoffs/barkhorn/out-cloud studio/products`. Commit nothing under `out-cloud/`.
3. **References.** Look at real photographs of your place and its light (WebSearch) before you build. Choose assets with
   `python3 studio/engine/assets.py search hdris|textures|models WORD`. `python3 studio/engine/assets.py sun HDRI ROT`
   says where a sky's sun is.
4. **Concept proofs.** Make two quick framings or lightings (`--scale 0.3 --samples 32`), choose one, and write down why.
5. **Critic passes.** Follow `critic/PROMPT-promo.md`:
   - Spawn a fresh, blind critic subagent per pass, at proof size (`--scale 0.5 --samples 128`). Make its changes,
     render, and spawn another.
   - Stop when two passes in a row score 8.5 or more and you agree at full size; then hold a blind duel with your best
     earlier frame.
   - If three passes gain less than half a point, change the concept, not the settings.
   - Log every pass in `elements/<name>.md`: its score, its changes and what you did.
6. **Finals.**
   - Landscape 2400 x 1600 and portrait 1600 x 2000, from the same set. The portrait is re-framed, not cropped.
   - Render into `renders/2026-10-18/barkhorn/element31/<name>.png` and `<name>-portrait.png` (`<name>_b...` for
     concept B), each with its `.report.json` and `.shot.json`.
   - Keep each PNG under 5 MB; commit a quality-92 JPG instead if one is larger.
   - Run one more blind critic pass on the final itself.
7. **Report.** Message the coordinator (`session_016Hs9fK3h2VwVeRXpa18b1z`) with send_message when the finals are
   pushed: the branch and commit, the images, the scores pass by pass, render times and anything the owner should know.
   If you're blocked, message early.

## Rules

- **Don't change the product:** not its model, its flavours, `studio/products/`, or the speaker's CAD.
- **Engine changes:** keep any change to the engine core (`render.py`, `sets.py`, `lights.py`, `kit.py`, `finish.py`,
  `materials.py`, `assets.py`) minimal and backward compatible, in its own commit, and say so in your report. Your own
  pieces go in `studio/engine/kit_ext/<name>_el.py`.
- **Software:** install what you need: Python packages (`python3.11 -m pip install --break-system-packages ...`), CC0
  assets, tools. Note each in your notes.
- **Assets:** keep downloads out of git; `studio/assets/cache/` is ignored. Use CC0 assets only, so the repository can
  stay public.
