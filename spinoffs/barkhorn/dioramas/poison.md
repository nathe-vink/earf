# Poison: a redwood forest floor, in moss, felt, corduroy and velvet (round 31)

*Green, and not the healthy kind.*

## The owner's direction (verbatim, via the coordinator)

> "'Poison could be more of a witch's garden,' is what it's suggesting I say. Might be cool. Or a mossy, ferny redwood
> forest with a fallen log and poisonous mushrooms. It's important to stay on the theme of earth and placing the
> speakers in their respective atmospheres, though the yeti and witch ideas are fun, subtle nods."

The coordinator read this as: the setting is the earth one, a mossy, ferny redwood forest floor. The witch's garden is at most a subtle nod.

## The concept

The scene is the floor of a redwood forest in the morning:

- Huge corduroy trunks rise out of the frame, flaring into buttresses at their feet.
- Moss flock lies over everything, with felt ferns among it.
- A fallen redwood lies furred in moss, its broken end a clay face with growth rings.
- Red velvet fly agarics with felt warts stand on the log and around it. Pale death caps stand to the speaker's right.
- Green-gold light falls between the trunks in a shaft onto the speaker, lighting the forest's air behind it. Motes drift in the light.

The bottle green speaker stands in that pool of light, its acrylic lit from inside, and throws green onto the moss at its feet. There are two quiet nods to the witch: a little corked potion bottle with a faint green glow in the moss by the log's end, and the icon's skull in clay beside the speaker's right foot.

- **Light, one idea:** sun through the canopy. A broad spot from high on the left lands on the speaker, with smaller shafts behind and beyond. A scattering volume fills only the forest behind the speaker, so the light shows in the air there, while the air between the lens and the speaker stays clear and the speaker stays crisp. A dim green canopy fill keeps the shadows readable. A warm rim and a low green-gold "glow" light only the speaker.
- **Palette:** moss greens and redwood rust, the gold of the light. Fly agaric red is the one accent.
- **Materials:** flock moss (its sheen tinted green), corduroy bark (the ribs run up the trunks and along the log), felt ferns, stems, warts and potion cork, velvet caps, clay end grain and skull, glass and a faintly glowing resin for the potion.

## Rounds

### First concept: a poison garden at night (p01 to p19, superseded)

Moss, velvet toadstools, foxgloves, nightshade and a glowing resin swamp, before the owner's direction came. What carried over:

- my kit pieces (the terrain, moss clumps, mist volumes, the toadstool, the skull);
- light-linking the speaker's lining, which is what makes its acrylic glow;
- turning off the specular of the world lights, so the speaker keeps its own highlights.

### The redwood forest

1. **f01 to f03:** first layout. The fly agarics and ferns read at once. The scene was too dark and showed no shafts. A trunk blocked the sun's path.
   - Builds fell from 82 s to 14 s: each piece is now built in its own small mesh and then joined, instead of running a bmesh op on one ever-growing mesh. My first attempt at this, indexing the new vertices, scrambled the geometry; joining a separate mesh fixed it.
2. **f04 to f07:** more sun power. The sun moved to the side so its shaft crosses the frame instead of pointing at the lens. A shot-wide haze was veiling the speaker, so I replaced it with a volume that fills only the forest behind it.
3. **f08:** that volume thick enough (0.4 per metre) for the light to show in it, with the canopy fill turned down.
4. **f09:** the near trunks brought in front of the volume, so they read as trunks rising out of the frame and not as fog. The puddle dropped, because it read as a black hole. Death caps moved to the right foreground. Motes turned gold.
5. **f10, f11:** the sun moved off the trunk that was shading the speaker. The potion moved where it can be found. Fewer, smaller motes, and finer ribs on the log.
6. **fq1, fq2 (portrait):** a 106 mm lens, the speaker at about 37 % of the frame's height on the centre line, the log at the left, a blurred fern framing the bottom.

## Final settings

- Camera (landscape 2400 × 1600): tilt-shift, elevation 22°, azimuth −20°, 7.3 m, 60 mm, f/2.8 at miniature 11, focused on the speaker's front face.
- Camera (portrait 1600 × 2000): elevation 20°, azimuth −18°, 8.0 m, 106 mm, the same focus.
- Set: a stage, `kit_scale` 11; the ground a `terrain` of my own.
- Lights:
  - `sun`, a spot of 32 kW with an 11° cone;
  - `sun2` and `shaft0` to `shaft2`, spots of 7 to 16 kW with 5 to 6.5° cones;
  - `canopy`, an area light at 0.6 from above, no specular;
  - `key`, at 0.6;
  - `rim` and `glow`, lighting only the speaker;
  - `spill`, a green point at the speaker's feet.
- Finish: bloom 0.28, saturation 0.14, lift 0.03 toward #141E10, vignette 0.22, contrast 0.12.
- Samples: 256 for both frames. Render times are in the coordinator report.

## Notes

- My kit pieces, all in `studio/engine/kit_ext/poison.py`:
  - `toadstool`, `skull`, `potion`, `moss`, `mist`, `terrain` (with `ground_z`, which the set uses to stand pieces on the ground), `clumps`, `trunk` and `fern`;
  - from the first concept and unused now: `foxglove`, `nightshade` and `glow_pool`.

  I changed nothing in the engine core.
- Environment: this container's python3 is 3.13, and `bpy==5.0.1` exists only for 3.11. I ran everything on python3.11, using a symlink first on PATH, and changed no repo file for it.
- Still to improve:
  - The horn's mouth reads dark, because we look into its throat. It is the product as it is.
  - The upper left of the landscape is a soft haze with little in it.
  - A fern frond touches the speaker's right edge from behind.
