# Planet EARF: the brief for the mockup

The owner's words (2026-10-18): "One thing I'll want to do after the website is done is start mocking up what Planet
EARF will look like: My acrylic-laden listening bar in San Francisco. Featuring EARF products, including speakers and
lighting, as well as a custom-built, back-lit acrylic bar and alcohol shelves, wall panels, etc." And later the same day:
"keep going, start Planet EARF once the site's done."

The reference research, with its sources, is in `research.md` beside this file: listening bars to learn from, acrylic
and back-lit interiors, acoustics with hard surfaces, and what San Francisco's permits and licences ask of each choice.

## Working assumptions (stated so the owner can overturn any of them)

- **Site:** a Hayes Valley corner storefront, near the hi-fi cluster (Phonobar, Le Fantastique). It is 30 x 60 ft
  (about 1,800 sq ft), 14 ft to the slab, a concrete shell with one long street window and a plain door.
- **Capacity:** 49 (Group B, so no Place of Assembly permit). About 40 seats: 12 at the bar, 4 booths, and a listening
  lounge of low chairs.
- **Use:** quiet, kissa-style listening early, with the bar staff playing records; a DJ at the record wall late.
- **Products in the room:**
  - two Atmosphere pairs on low Smoke plinths in the listening room's corners, the horns near seated ear height;
  - a Fog pair in lit niches in the back-bar, among the bottles;
  - Cumulus (the record player) at the DJ desk, set into the record wall;
  - Bell lamps over the bar and on the booth tables, each matching the nearest speaker.
- **The bar:** an 8.4 m front of eight 20 mm cast-acrylic panels in spectrum order (Ember, Dust, Acid, Poison, Ice,
  Haze, Fog, Smoke). Each sits over a white liner with an LED cavity behind it, so it is back-lit with no hot spots.
  The top is dark honed stone, never acrylic, because spirits craze acrylic.
- **Shelves:** 10 mm edge-lit light-guide acrylic, tinted for display and warm white on the working shelves so the
  labels read.
- **Walls:** tinted acrylic slats 50 to 100 mm in front of a dark absorber, on one wall of each facing pair, so no two
  acrylic walls face each other. A floor-to-ceiling record wall of uneven depth serves as the diffuser, with the DJ desk
  set into it.
- **Ceiling:** a translucent micro-perforated acoustic membrane, back-lit in one slowly changing colour. It runs as a
  colour clock: Fog and Ice at opening, Acid and Dust at sunset, Ember and Haze late, Smoke at last call.
- **Entrance:** a plain door with one small neon EARF sign, so the room comes as a surprise.

## Deliverables

1. **A model of the room** that could be built, in the studio's engine (Cycles). The products come from their own CAD:
   Cloud from `spinoffs/barkhorn/cloud.py`, Cumulus and Bell from `spinoffs/barkhorn/companions`. Materials are scanned
   CC0 (stone, concrete, records, upholstery), as the in-their-element scenes used them.
2. **Views**, each judged blind with `critic/PROMPT-promo.md` and pushed through passes as round 31's were:
   - the whole room at night, from the door;
   - the bar front lit, at eye level;
   - the listening corner, with a pair either side of the lounge;
   - the back-bar, with the Fog pair among the lit shelves;
   - the record wall and the DJ desk with Cumulus;
   - the street at night, through the window;
   - the colour clock: one view at four hours.
3. **A floor plan and a long section** to scale, in the fab kit's drawing style (`studio/fabkit/drawings.py`), with
   the seat counts and the acoustic treatment marked.
4. **A materials and lighting board:** each acrylic part (its thickness, tint and lighting method), the stone, the
   absorber and the membrane.
5. **`spinoffs/barkhorn/planet/README.md`:** the concept, the assumptions, what each choice costs in permits and money
   (from the research), and the owner's open questions.

## Where things are

- The engine: `studio/engine` (start with its README). A shot file is the single source of a photograph:
  `python3 studio/engine/render.py SHOT --out IMG --samples N [--scale S] [--crop ...]`, then
  `studio/engine/finish.py` applies the finish once.
- Scene kits: `studio/engine/kit_ext/*_el.py` are the in-their-element scenes (Poly Haven assets through
  `studio/engine/assets.py`). Room 31 (`studio/shots/barkhorn/room31`, `renders/2026-10-18/barkhorn/room31`) is the
  nearest precedent for an interior with the speakers in it.
- Building the speaker's model: `.venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/cloud.py --out
  spinoffs/barkhorn/out-cloud --skip step,stl,drawings`, then `git checkout -- spinoffs/barkhorn/out-cloud
  studio/products` so the build leaves no changes behind. bpy runs under python3.11, and render.py re-execs into it.
- Put the work here: code in `spinoffs/barkhorn/planet/` and `studio/engine/kit_ext/planet_*.py`, shots in
  `studio/shots/barkhorn/planet32/`, renders in `renders/2026-10-18/barkhorn/planet32/` (proofs as JPGs, finals as
  PNGs under 5 MB, else a JPG).

## Process

- Work on branch `r32-planet` (this branch) and push only to it. The coordinator merges it into main.
- Proofs at low samples and scale first, then blind passes. Finals at full size, 256 to 512 samples, with the finish
  applied once. A render must run as a tracked background task, or the container may be reclaimed mid-frame.
- For long frames, message the coordinator (`@parent`) with the full 40-character commit and the shots, and it will
  start render helpers. Never give a short commit name.
- Report to the coordinator at each milestone: the room blocked out, the first proofs, each final, the drawings, and
  the README. Include the head commit and the blind scores.
- Never put a provider key in the repository, and keep each PNG under 5 MB.

## The owner's open questions (from the research)

- the site and its size;
- capacity (49, or 50 and over);
- the licence (a Type 48 bar, or food-led);
- etiquette (quiet, a DJ, or both by the hour), and where the DJ sits;
- how many pairs and which colours, and whether they are fixed or rotate for sale;
- colour: all eight, one dominant, or a room per colour; static, programmed or sound-reactive;
- whether EARF casts the bar panels itself, and the budget;
- the records and the hours;
- whether Cumulus and Bell appear.
