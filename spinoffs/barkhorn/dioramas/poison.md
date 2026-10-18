# Poison: a poison garden, in moss, velvet and clay (round 31)

*Green, and not the healthy kind.*

## The concept

A moss-flocked clearing at night, with a cold mist lying in it. Around a swamp of glossy green resin that glows from its depth stand velvet toadstools with felt spots, clay nightshade, foxglove spires in velvet and a crooked black tree. Glass bubbles rise off the swamp and spores drift through the air. The bottle green speaker stands at the swamp's edge: its acrylic is lit from inside and throws green light onto the moss at its feet. A small clay skull, the Poison icon, lies in the moss by the speaker's right front foot, beside a sprig of nightshade.

- **Light, one idea:** the garden glows from the ground. The swamp lights the moss around it and, low from the front right, the speaker's face. A moon low behind the garden lights the mist there, so the tree and the foxgloves stand out as silhouettes against a pale backdrop. A cold rim from high behind picks out the speaker's edges and horn.
- **Palette:** apothecary greens and blacks: black-green velvet, moss, emerald resin, and a slate-teal mist. Foxglove violet is the one accent. Bone-coloured felt for the stems, the spots and the skull.
- **Materials:** flock moss (its sheen tinted green, see below), velvet caps and bells, felt stems, spots, throats and lily pads, clay berries and skull, cast resin, glass bubbles, suede bark, and a scattering volume for the mist. No cotton wool, paper or tulle: those belong to the other worlds.
- **The joke:** the skull is the icon itself (a circle over a rectangle, the eyes and nose cut through and the teeth notched), in clay, small enough that you find it on a second look.

## Concepts, and the pick

The first proofs tried three ideas of light on the same set:

- **A, moonlit from behind** (p01 to p03): a big moon behind the speaker. The ground went a flat grey-green and the swamp read as a lamp.
- **B, a moon spot** (p05): a hard spot from behind. Most of it was lost in the speaker's lining, so the speaker went black.
- **C, the glow from the ground and a lit mist behind** (p10 onward): the garden stays dark and the light comes from the swamp, the spores and a backdrop of lit mist.

I picked **C**. It is the only one in which the speaker is the brightest, most saturated thing in the frame. It also gives the backdrop depth: the silhouettes stand against a pale mist instead of disappearing into a black sky.

## Proof rounds (scratchpad, 0.3 to 0.5 scale)

1. **p01, p02:** first layout. The haze was too dense and washed everything grey, the swamp's glow disc was blown out, and the foxglove bells were too small.
2. **p03, p04:** less haze and a darker resin. The kit's flock catches a back light white, so the moss read grey. Added `moss` (kit_ext), which tints the flock's sheen green. The swamp was overlapping glowing blobs, which looked crude.
3. **p05 to p07:** moon spot (concept B), a kidney-shaped extrude for the swamp. The speaker read dull. I found the reason: its lining was not among the light-linked receivers, so its body did not light up. With `lining-*` and the rest of the parts in `SPEAKER`, it glows.
4. **p08, p09:** a rim on the speaker alone and a front-right "glow" from the swamp. Wrote `glow_pool`, an emitter that fades out radially from its centre, so the light seems to come from the swamp's depth.
5. **p10:** dropped the shot-level haze. Added two of my own `mist` volumes: a low bank torn into wisps by noise, and a deep, thin haze behind the garden, lit by a moon low behind it. This was the turning point.
6. **p11 to p13:** foxgloves (fewer, bigger bells), a clump in the middle distance, the low mist moved behind the foreground, more contrast, less lift.
7. **p14 to p16:** the ground rebuilt as a `terrain`: rolling moss, flat where the speaker stands, banks behind, and a bed sunk for the swamp. The swamp is resin poured into that bed, so its shore is the bed's own contour. Cushion moss became `clumps` kept off the resin, and its build went from 111 s to 0.2 s by writing the mesh directly instead of with a bmesh op per ball. Felt lily pads and duckweed on the resin.
8. **p17, c-crops:** traced white shards on the swamp to the moon and the backdrop light mirrored in the resin, and turned off those two lights' specular (the speaker keeps the highlights of its own rim). Dark felt lily pads now silhouette against the glow. Foxglove bells hang outward with pale, freckled felt throats.
9. **p18, p19:** reframed so the swamp sits whole in the frame on the right third. Moved the skull into the focus band beside the speaker's foot. Raised the rim so it reaches the horn. Added a faint green spill from the speaker onto the moss in front of it.
10. **q01 to q07 (portrait):** reframed with a longer lens (105 mm) and a higher target, so the speaker sits centre-left at about 36 % of the frame's height, the swamp bottom right and the tree's crown above. The big toadstool moved a little toward the speaker so its cap frames the left edge.

## Final settings

- Camera (landscape): tilt-shift, elevation 24°, azimuth −20°, 7.3 m, 65 mm, f/2.8 at miniature 11, focus on the speaker's front face. Portrait: 21°, −18°, 8.0 m, 105 mm, the same focus.
- Set: a stage, `kit_scale` 11. Lights: `back` (the mist), `moon`, `key` (dim and cool), `swamp` (a green point, no specular), `spill`, plus `rim` and `glow` with the speaker's parts as receivers.
- Finish: bloom 0.3, saturation 0.12, lift 0.02 toward #0A1A12, vignette 0.25, contrast 0.14.
- Renders: landscape 2400 × 1600 and portrait 1600 × 2000, both at 256 samples. Render times are below.

## Notes

- Kit pieces of my own, in `studio/engine/kit_ext/poison.py`: `toadstool`, `foxglove`, `nightshade`, `skull`, `moss`, `glow_pool`, `mist`, `terrain` (and `ground_z`, which `poison.py` uses to stand its pieces on the ground) and `clumps`. No engine-core change.
- Environment: this container's python3 is 3.13, and `bpy==5.0.1` exists only for 3.11. I ran everything on python3.11 (a symlink first on PATH), and no repo file changed for it.
