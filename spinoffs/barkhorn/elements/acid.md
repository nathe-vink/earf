# Acid, concept A: at the acid spring (round 31b)

*A yellow with opinions.*

## The owner, verbatim

> "the diorama looks cheap, like a bad video game. I was hoping for more texture in a lot of these. The speakers are too
> stark in contrast to the setting too. Tilt shift may have been a bad direction. Lighting in general in a lot of them
> is off. I don't like the strings in the acid rain. Maybe don't think about them so much like dioramas, and think more
> about placing them in there element, so to speak."

> "Continue to do critic passes until you feel it's in a good enough place for promotional images for a $20K product."

## The place

Dallol, in Ethiopia's Danakil Depression: the most acid ground on earth (springs below pH 2), and naturally the
colours of this speaker. Real photographs looked at first (Wikimedia Commons, `ET_Afar_asv2018-01` series): a dead flat
plain to the horizon; crusted terraces in lemon sulphur, white salt at every water's edge, rust and ochre iron above;
opaque, milky lime-to-green pools that mirror a pale hazy sky; knobbly yellow and white chimneys; a hard sun through
haze.

## How it is built

- **Sky:** Poly Haven `qwantani_late_afternoon_puresky` (a pure sky, no photographed ground, so the modelled crust runs
  to its horizon): hazy, warm at the horizon, a hard sun 19 degrees up. `aarfontein_pan` (a salt pan at dawn) was
  tried first: too dim and cold, and a farmhouse on its horizon.
- **Ground** (`studio/engine/kit_ext/acid_el.py`, `terrain`): a height field (broad swells, 4.5 cm terraces, raised salt
  rims where the acid has dried) on a polar grid 320 m across, about 1 cm cells under the speaker and coarser toward the
  horizon, so the plain meets the sky's horizon with no seam. Its colour comes from its height above the acid and a slow
  noise (salt, lemon, sulphur, ochre, rust), multiplied over Poly Haven's `rock_boulder_cracked` texture for its cracks,
  grain and relief.
- **Acid:** generated with the ground, only where the ground dips under the water level, carrying each point's depth:
  clear at the very edge, pale lime over the shallows, green in the deep, milky (subsurface) and glossy with a faint
  breeze. A volume under a refracting surface was tried first and went dark, because Cycles drops refracted caustics
  so the sun never reached it.
- **Chimneys:** knobbly columns (noise on noise, a cauliflower crust), coloured by the same shader in salt, sulphur or
  rust.
- **Steam:** volumes over two chimneys, noise-broken and stretched upward.

## Concept proofs

- A: the sun from the left (azimuth -100), front-lit speaker: its colour reads, the crust is flat.
- B: the sun behind (azimuth -160): the terraces rim-lit, the acrylic's edges glow, the front darker.
- Chosen: between them, the sun behind the speaker's left (azimuth -146): the crust raked and rim-lit, the acrylic lit
  through, enough light on the front.

## Critic passes

| Pass | Score | Top changes | What I did |
|---|---|---|---|
