# Ember: the depths of hell, in fabric (round 31)

The owner's picture: "the ember one could be in the depths of hell, with fabric, underlit embers billowing upward."

## The concept

A cavern whose walls are bands of velvet and satin laid one above the next, crimson, oxblood, black and scarlet, their
folds running level like rock strata. A river of glowing orange satin runs through a fissure in the black-red velvet
floor, behind the speaker, between rolls of velvet. The red speaker stands on a velvet ledge ringed with felt coals,
some glowing and some burnt out. To its left, the Ember icon as a campfire: three flames, each cut from three layers of
felt (scarlet, orange, a gold heart), standing on a felt log; a smaller one sits near the lens on the right. Embers rise
from the fissure and the fires in plumes and drift right, some close enough to the lens to blur into bokeh. Velvet
stalactites hang from the roof (they show in the portrait).

- **Light, from below.** No key from above. The light comes from the fissure (point lights low over the satin), the
  coals round the speaker's feet, which light the acrylic from its bottom edge up, a low spot from the coals' side up
  through the horn, the river behind it (the rim), and the campfires. A 0.05 W/m² crimson fill from above only keeps
  the darkest velvet from going to pure black.
- **Wit.** A devil's toasting fork (a trident) leans from the speaker's ledge into the campfire, a marshmallow on its
  middle tine. "The part of the fire that stays up late."
- **Palette.** Crimson, oxblood and black velvet, the speaker's own red; the one accent is the gold-orange of the embers
  and the felt flames' hearts. Blacks lifted into a deep crimson (`#36060F`).

## Why this concept

The first three proofs tried theatre curtains (vertical folds), a lava river crossing the foreground, and a wide pool.
The curtains read as a stage, not a cave; hanging bands with level folds (`strata()`) read as rock at once and are still
plainly cloth. A river in the foreground became a blurred pink band across the frame (at a miniature depth of field
anything a metre off the focus plane melts), so the river moved behind the speaker, where it backlights the acrylic and
draws a glowing line under the strata. The speaker on a ledge with coals at its feet is the clearest way to light it
from below without a shape competing with it.

## Proof rounds (scratchpad proofs, 0.3 to 0.5 scale)

1. Curtains, a satin river across the foreground, gold bokeh: the river blew out to a pink band, the bokeh was too big
   and yellow, the campfire was under the floor (the icon's coordinates put the log below z = 0; fixed in the ext).
2. Smaller frame on the speaker, river banks: still a bright wall across the bottom.
3. River moved to pass the speaker's left, a branch behind it, coals in front, the fire into frame: read as a fairground.
4. Walls rebuilt as strata (bands on their sides): the cave reads. A big pink arc remained at lower left.
5. to 8. Found it: a tube with `flat` < 1 stands its wide axis upright, so the river and its banks were standing
   ribbons that curled at the ends. Flat ribbons now (`flat` 8 for the satin, 1.7 for the velvet banks). The campfire
   into the focus plane beside the speaker, where the layered felt reads; the fork beside it.
9. to 12. A 50 mm lens closer in (more cavern behind the same speaker); a scattering haze tried at 0.035, 0.012 and
   0.005 per metre and dropped: it veiled the velvet's folds and the blacks into one red-brown murk and cost 40 % more
   render time.
13. to 17. The floor from black to a black-red velvet (black velvet's white-tinted sheen turned grey at this grazing
   angle); embers dimmed from 30 to 9 so they read orange, not as white stars; stalactites; a spot up through the horn.
18. to 23. A front crack (read as a sausage), then a lake of rippled satin round the speaker's island (read as a plate,
   then as pink jelly). Both dropped: the coal ring alone lights the base better and keeps the silhouette clean.
24. to 28. Exposure up, a hearth light on the campfire's log, a second small campfire near the lens on the right for
   depth, coals as felt balls in two tones, the marshmallow bigger. The speaker checked at full resolution cropped: crisp
   from the horn's rim to the feet.

The portrait has its own camera (58 mm, 5.0 m, 17°, a 0.1 lens shift up) so the speaker stays at about 40 % of the
height with the stalactites overhead, rather than a wider lens that left it at 25 %.

## Final settings

- Landscape: 2400 × 1600, 256 samples; camera 50 mm, 19° down, azimuth −16°, 6.1 m from (0.15, 0.4, 0.72), focus
  (0.15, −0.05, 0.7), f/2.8 at miniature 11; kit_scale 11; view Khronos PBR Neutral, exposure +0.25.
- Portrait: 1600 × 2000, 256 samples; 58 mm, 17° down, azimuth −12°, 5.0 m from (0, 0.4, 0.75), shift_y 0.1.
- Finish: bloom 0.35 (46 px, threshold 0.7), vibrance 0.15, lift 0.025 in `#36060F`, vignette 0.25.
- Render times: see below.

## Environment notes

- `studio/setup.sh` pins `bpy==5.0.1`, which only exists for Python 3.11; the container's `python3` is 3.13. bpy 5.0.1,
  numpy 1.26, Pillow and SciPy were installed into the system Python 3.11 and every render was run with `python3.11`.
  The CAD venv was made with Python 3.12.

## What I'd still improve

- The embers are small balls; a soft streak (motion blur on the rising ones) would make them billow more like sparks.
- The marshmallow is barely legible at the landscape's size; a toasted, two-tone one would read better.
- The floor in the lower fifth of both frames is quiet; a few more out-of-focus embers lying on it would carry the glow
  forward.
