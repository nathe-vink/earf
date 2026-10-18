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
| 1 (P1) | 4.5 | contact shadow; light through the acrylic; matte chimneys; a pool with depth and ripple; camera lower, longer lens; harder light; crust plates not stripes; visible steam, clear silhouette | P1 was lit by two suns: before main's fix (b49838c) the sun lamp shone from the opposite side to the sky's sun. Fixed by merging main and turning the sky so its sun is behind the speaker's left (azimuth -146). Contact shadow and a gold-tinted cast shadow now show (the resin's shadow rays are tinted). The chimneys' gloss was a bug (the wet-crust term applied to them); the fix written then did not apply (found at pass 4 and fixed there). Pool: less milky (subsurface 0.12), clear over its first 6 cm, ripples up. Camera 0.7 m, 6.5 m, 65 mm. Sun 10, sky 0.8, haze 0.0008. Crust: Voronoi plates (1.1 m), 4k texture, specular 0.3. Steam rebuilt as a widening, leaning plume broken into wisps. The rust mound moved off the silhouette. The sun to azimuth -110, as asked, washed the crust white with sheen at grazing angles, so it went back behind the speaker |
| 2 (P2) | 5.0 | the cabinet in its own shade (lum 29, brown-black); a flat neutral sky; a hard horizon; gumdrop chimneys, two cut by the frame; steam a smear at the edge; plastic crust; the speaker near frontal; the horizon on the cabinet's top | Sky changed to `evening_road_01_puresky` (warm, with cloud), turned so the sun is low on the speaker's left and a little behind (azimuth -115, 14 degrees up). A warm salt-white bounce (a reflector, 2 x 1.5 m, from the front left). Haze 0.003/m, warm. Speaker turned +22 (37 degrees to the camera: its left side shows). Camera 0.5 m, 9 m, 85 mm, f/4. Three chimneys, each its own form (tiered), none at the frame's edges; one steam plume from the far left chimney, in frame (steam absorbs nothing now: it had gone grey). Crust specular 0.15 asked (the setting was not wired until pass 4), texture at 0.9 m |
| 3 (P3) | 4.5 | no hard sun (no cast shadows, no rim, no whites: p99 204); a neutral grey sky; the crust a painted relief map with hard plates; tiered chimneys read procedural; steam barely visible; a clay-like rust bank in the foreground; tones compressed | **Three passes gained under half a point (4.5, 5.0, 4.5), so the approach changed, not the settings** (the brief's rule). The cause the three critics agree on: a crust coloured in bands by height reads as a painted map, under a sky with no hard sun. Now: the crust is a scanned eroded crust (ambientCG `Ground093A`, its knobbly lips like Dallol's salt terraces), truly displaced 2.5 cm, coloured by slow noise and the scan's own relief so edges follow the grain (height only sets salt at the water's edge; no plates); terraces 3 cm. A clear sky with a hard low sun (`quarry_01_puresky`, sun azimuth -100, 10 degrees up, irradiance 12): long raking shadows. Camera 0.75 m (over the rust bank), 8.5 m, 85 mm, f/2.8. Acid milky turquoise to lime. Chimneys untiered, on the same scan; a second plume far back; plume density x3. Exposure -0.3, finish contrast 0.1, vignette 0.2 |
| 4 (P4) | 5.0 | the crust like crumpled oily foil with sky glints in its hollows; a flat grey sky; no cast shadow and a dark body; steam from behind the vents; plaster chimneys and a snow-pile cone; a flat pool; an empty horizon; veiled tones | Found that the crust's `specular` and the chimneys' matte setting had never been wired (an edit that silently missed): now they are, with a roughness floor (crust 0.8, chimneys 0.85) and specular 0.08 and 0.1. Scan tile 0.7 m, displacement 1.4 cm. Sun moved behind the speaker's left (azimuth -125, 10 degrees up), sky strength 0.8. The snow-pile cone removed; the far vent a broad low rust-ochre mound; steam from the vent top, denser. Pool clear over 12 cm, deepening to #2E9C8E. An escarpment on the horizon (`ridge`), placed at 278 m: the engine's camera clips at 300 m, so it stands at the size a 60 m ridge 1.6 km away would have. Haze 0.0012/m in a box tall enough that its top never shows. Exposure -0.5, contrast 0.15, vignette 0.25 |
| 5 (P5) | 5.0 | the crust like crumpled foil (thousands of glints); no shadow from the speaker; a flat sky; foreground as bright as the midground; a clay chimney; painted steam; a weak horizon haze; a uniform pool rim | The foil had two causes, found in crops: the scan's normal map (bump now 0.3, specular 0.02, roughness at least 0.95, tile 1.4 m), and, the larger, the acid sheet lying a few millimetres over a very flat displaced crust, so a film of rippled water glinted between the bumps everywhere. Fixed at the source: the ground now steps 2.5 cm at every shore (a tanh step), so crust stands clear and pools sink; the wet band narrowed to 8 mm. Sun behind left (azimuth -150), irradiance 14, bounce 0.8, sky 0.7. The front pool enlarged to fill the foreground. The vent lower (0.9 m) with orange at its mouth; the far plume thin and leaning another way. Haze 0.003/m from 15 m out, warmer. Ripples halved. Vignette 0.3. (The speaker's acrylic lets shadow rays through tinted, by its material, so its cast shadow is light: the product's material is fixed) |
