# barkhorn, uplit (round 31)

The speakers on lights at night before board-formed concrete: one slide per colour for the site's colour viewer
(`uplit-<key>.png`, 1600 x 1600, the same camera, lamp and set for all eight, so only the colour changes) and the night
hero (`facade.png`, 2880 x 1200; `facade-portrait.png`, 1440 x 1800). Shots from `spinoffs/barkhorn/uplight31.py`;
the set's concrete, wet granite and river are kit pieces in `studio/engine/kit_ext/concrete.py` over Poly Haven CC0
scans (`concrete_layers_02`, `granite_tile`, the sky `kloppenheim_07_puresky`). Keys as in `finals.py`: red Ember,
orange Dust, amber Acid, green Poison, blue Ice, violet Haze, ice Fog, black Smoke.

## What the light really does (the lining)

The cabinet is lined with white batts in voile sleeves, and the engine's batting stops light as real batts do. The lamp
is a flat panel of LEDs inside the speaker's footprint, on the plinth's lens 10 mm under the cabinet's bottom, so no
part of the light starts inside the cabinet. (The first proofs used a round spot whose 0.12 m source reached up
through the bottom panel into the batts; their neat column of colour was light that could not have got there. Caught
and rebuilt in pass 1.)

- **Straight up, nothing passes.** The bottom batts stop it all, and the wall right above each speaker stays dark: a
  spine of shadow up the middle of each wash.
- **The colour leaves round the batts:** through the tinted acrylic walls, and through the strip of the bottom panel by
  the ports, where the batts stop short. It fans up the wall in a V either side of the spine, deeper in colour at the
  V's edges, where it crossed more acrylic.
- **The cabinet glows from inside.** Light entering by the ports lights the interior and the lining's faces; seen
  through the tinted front it is the speaker's colour, burning toward white at the ports.
- **The horn gets none of it.** Its mouth faces forward and the cabinet's top hides its underside from any lamp at the
  plinth (a second emitter aimed from the plinth's lip only lit the woofer); the moon lights it.
- **Smoke passes least,** so its wash is faint; **Fog** passes nearly white.
- Translucent batts (subsurface 3 cm deep) changed nothing visible.
- The engine cannot show acrylic carrying light along inside its walls to glow at their edges (no caustics), so a real
  cabinet would likely show a little more colour on its edges than these do.

Placements tried (pass 0): under (chosen), a floor uplight in front (throws the cabinet's shadow up the wall, white spill
round it, colour only above the horn), grazing up the face (a thin stripe, the woofer blown white).

## The critic

Fresh, blind critics under `critic/PROMPT-promo.md`, staged by `spinoffs/barkhorn/critic/stage_promo.py` with
`card-uplight31.yaml`; every reply in `spinoffs/barkhorn/critic/rounds/2026-10-18/uplight31-*.json`, every pass in
`spinoffs/barkhorn/critic/LOG.md`.

| Frame | Passes (blind score) |
|---|---|
| facade | 4.0, 5.5, 5.0, 5.0, 4.5, 5.0, 5.5 (first full size), 5.5, **6.5** (the final, pass 10) |
| uplit-red (the slides' critic frame) | 3.5, 4.0, 4.5, 3.5, 4.5 (own set), 4.5 (the quay), 6.5 (first full size), 5.5, **5.5** (the final, pass 9) |

The bar (two passes in a row at 8.5) was not reached. The scores settled at 5 to 6.5 and swung about a point between
critics; late passes contradicted earlier ones (the wall moved closer by two critics, back to a metre by the next).
What every critic repeated and the frames still carry: the cabinet's interior burning toward pink-white at the ports,
the horns dark (true to the cabinet), eight identical copies in a row, and a rendered rather than photographed feel.

## Times (4 CPU cores, Cycles)

facade 2880 x 1200 at 256 samples: 79 to 85 min. uplit 1600 x 1600 at 384 samples: 41 min.
