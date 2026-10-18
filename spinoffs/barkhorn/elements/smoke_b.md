# Smoke, concept B: high-key (round 31b)

A misty birch wood on a pale winter morning: chalk-white trunks receding into the mist, fresh snow, woodsmoke drifting
in thin sheets from a fire out of frame, soft light from an overcast sky. The smoked-black speaker stands sharp against
the pale mist, black on white. Its line: "Where there's smoke." Set: `smoke_b.py`; its own pieces:
`studio/engine/kit_ext/smoke_b_el.py`.

## Set and assets

- Sky: Poly Haven `snow_field` (overcast snow field, CC0), 4k, turned 200 degrees; no sun lamp (an overcast morning
  has no shadows to sharpen).
- Ground: `snow` piece, Poly Haven `snow_02`'s height and normals (4k, true displacement near the lens) under a clean
  white skin of our own: the scan's colour carries dark twigs that tile. Faint subsurface and a fine sparkle.
- Birches: Poly Haven has no birch, so `birches` builds them: tapered, slightly crooked tubes (some clumps of two or
  three stems from one foot), barked procedurally (chalk white with grey and cream patches, short dark lenticels,
  black scars, a blackened fissured foot) over `bark_willow`'s scanned normals for micro-relief. 9 placed trunks near
  the speaker, 70 more receding to 60 m, one close to the lens at the left edge, out of focus.
- Mist: `mist`, a scattering volume clear in front of the speaker and thickening to 0.07 per metre by 26 m, denser near
  the ground. The engine's homogeneous haze veiled the speaker itself grey (proof 1), so the mist starts behind it.
- Woodsmoke: `smoke`, thin volume sheets (1.4 to 1.8 m deep) of wisps (the ridges of a distorted noise) inside
  broader drifts, banded about a height and fading in from the left. A thick box averaged the wisps into a flat grey
  wall (tests t1 to t6); thin sheets keep the structure.
- Ground cover: Poly Haven `grass_medium_01` scattered and drained to dry straw (`dry_scatter`), and three small
  `dry_branches_medium_01`.
- A black flag (negative fill) out of frame on the camera's side, seen by reflections: the speaker's front mirrors
  black instead of the white wood behind the lens, so the smoked acrylic reads deep (proof 3 read mid-grey).

## Concept proofs (0.3 scale, 32 samples)

- Overcast (`snow_field`) against a low sun through the mist (`birchwood`, sun lamp from its sun). Little to choose at
  this density of mist: the sun gave a touch more modelling and nothing of its own. Chose **overcast**: it is the
  brief's high key (soft, shadowless, black on white), and it stays clear of concept A, which is backlit smoke at dawn.
- Proofs 1 to 5 then fixed the mist veiling the speaker, the invisible smoke, the bark (lenticels too sparse), the
  trunks (too thick and parallel: thinner, leaning, clumps), the snow's tiled dark twigs, the foreground trunk (too big)
  and the branches (scanned pile far too big; now three small ones).

## Critic passes (critic/PROMPT-promo.md; 0.5 scale, 128 samples unless noted)

| Pass | Frame | Score | Top changes | What I did |
|---|---|---|---|---|
