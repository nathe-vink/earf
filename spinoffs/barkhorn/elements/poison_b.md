# Poison, concept B: the poisonous forest (round 31b)

*Green, and not the healthy kind.*

## The direction

- **The owner on concept A (2026-10-18, evening), verbatim:** "Poison isn't reading as poisonous. Needs shrooms around it, or a snake, or both. Or other poisonous things. I guess snakes are venomous haha."
- **The coordinator's brief:** keep the forest (photoreal, no diorama), and make the poison unmistakable:
  - fly agarics at several ages and death caps at the speaker's feet, modelled convincingly;
  - a green pit viper coiled beside the speaker, in focus, as an element of the picture, not a gag;
  - dart frogs, foxgloves and nightshade where they help;
  - a damp, moody green forest, low sun through the canopy and a little mist, the green acrylic glowing where the light comes through.

## The set

- **From A:** the forest. Poly Haven `mossy_forest` behind, a modelled redwood with displaced `metasequoia_bark`, `fern_02` scans, `forest_leaves_02` duff, the canopy sheet that breaks the sun into shafts, and the mist.
- **New pieces** in `studio/engine/kit_ext/poison_b_el.py`:
  - **`amanita`:** a fly agaric at five ages (button, young, convex, plane, old and torn), or a death cap. The fly agaric has a viscid red cap fading toward orange at the margin, the veil's warts denser at the centre, free gills with short lamellulae between them, a drooping ring, a fibrous stem stained toward its foot, and the volva's rings on the bulb. The death cap has an olive cap and a cup volva.
  - **`viper`:** a coiled Trimeresurus about 0.7 m long. Keeled scales (Voronoi), a pale belly and flank stripe by the surface's facing, a rust tail tip, a broad flat head, amber eyes with slit pupils, the neck raised in an S. It drops onto whatever lies below it.
  - **`dartfrog`:** a green-and-black D. auratus.
  - **`foxglove`, `nightshade`, `moss_pad`.**
- **The viper's perch:** a Poly Haven `tree_stump_02` scan at half size.

## Passes

| Pass | Score | Verdict | Main changes asked | What I did |
|---|---|---|---|---|
| 1 | 5.0 | iterate | The sunlit foreground duff outshines the speaker (123 vs 67); the acrylic milky and flat-lit; the agarics too many, glossy and uniform; the viper a rubber toy; mist only in the shafts; the horn crushed; the frog and death caps unreadable; f/8 at 35 mm reads as a diorama | Foreground holes closed, duff albedo ×0.5. Reflector 3.5 → 2, smaller reflection scrims, the rim raised for the horn's lip. Seven agarics (two at the feet, a clump of five), caps rougher and darker. The viper rougher and duller. Mist from 1.2 m behind at 0.09, denser low, plus a thin near layer. Death caps at the speaker's right foot; the frog at the stump; one foxglove and the nightshade removed. Camera 50 mm f/4 at 4.6 m, 0.5 m high: a compromise between the critic's 5.5 m f/2.8 and keeping the poisons legible, since at 5.5 m they were lost. The light stays from the front-left: in A, light from behind could not pass the lining. |
| 2 | 5.0 | iterate | The sun pool on the duff in front, not the speaker (117 vs 64); the horn opaque; the viper a toy; the agarics evenly spaced on bare duff; the death caps unreadable; the floor bare and swept; foxgloves symmetrical; the trunk flat | The coordinator's notes too: visible scales, a heat-pit head, slack loops, viscid caps with washed-off warts, a striate margin, sorrel and moss on the floor, sun on the acrylic. A sun-only render showed the sun from behind-left only grazed the speaker's front, so the sun moved to −75° (front-left), elevation 30°: the body now glows. Foxgloves first blocked the beam; now four grouped behind at the left, out of its path. A new `sorrel` piece (redwood sorrel, Oxalis oregana: trifoliate heart leaflets, instanced by geometry nodes) carpets the floor in patches; moss cushions round the mushroom bases. A tight clump of four agarics, tilted, bulbs sunk; warts washed off in patches; a striate margin. Death caps darker olive. The viper's coil slack, scales 4 mm, olive dorsal, subsurface, satin. A warm panel behind the horn. Bark displaced 18 cm. |
| 3 | 5.5 | iterate | The horn's back panel drew a rectangle in the mist; the pool and reflector paled the acrylic; the horn wanted a reflection; the sorrel was a uniform carpet; the snake's scales and pose; no contact ring at the plinth, the death caps hidden; the trunk sliver missing | Sun 30 → 21, reflector 2 → 1; the horn backlight returned with `volume: false` (a new engine knob, a1f2639); sorrel varied in size and colour, some folded, with a 0.58 m bare ring round the speaker; death caps forward into a dapple; frog onto the stump; a stronger scale bump; trunk tint 0.5 |
| 4 | 5.0 | iterate | No sun pool on the body (66 against 77 in the right shaft); the right shaft and ferns compete; the viper a smooth toy, the frog a beetle; a softbox in the horn (217); the near foreground too bright; agarics waxy and the moss a hard disc; death caps pale; the trunk flat, foxgloves in a row | A tight 0.42 m pool on the upper face, sun 28; the right shaft holes closed or moved deep, rear mist 0.09 → 0.07; reflector 0.5; scrim3 2.5 → 1.2; viper girth 4.8 → 3.8 cm, deeper seams, a shade per scale, roughness 0.38, coat 0.25; death caps olive (#8C8A5E at the rim); moss thinned with ragged edges (`feather` on the strew); trunk tint 0.35 |
| 5 | 5.0 | iterate | The speaker now darker than the mist and the ground (31 against 53 and 58): the tight pool lit only its top; the horn a black mirror with one hot highlight; the viper, agarics and foxgloves still read as CG; the death caps and frog lost | Stopped: passes 4 and 5 gained −0.5 and 0. The finals come from pass 3's rig (5.5), with one mechanical change, its own top note: the horn's back panel kept out of the mist (`volume: false`) |
