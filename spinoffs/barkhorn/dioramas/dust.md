# Dust: golden hour in a suede desert (round 31)

The set is `dust.py`; the frames are `studio/shots/barkhorn/diorama31/dust.json` and `dust-portrait.json`.

## Concept

A desert at golden hour, built from suede, corduroy and sand. A big low paper sun, glowing in rings, sets behind a
slim butte of cut suede on a paper sky. Corduroy dunes roll between, their ribs running along the crests, and the floor
is sand. The real sun is low behind the speaker's right and in frame, so the orange acrylic glows amber at its edges and
every piece throws a long shadow to the left. Beside the speaker is the icon in wool felt: three puffs at the fat end of
a flat wedge thinning along the ground, with a line of roadrunner footprints running out of its point to the right.
Something just went past. Motes hang in the light, and a little sage corduroy saguaro is the one accent.

## Rounds

Proofs at `--scale 0.3 --samples 24` (about 45 s each, 30 s before the haze) unless marked mid (`0.5 / 64`, about 5 min).

1. **First set.** Camera from the front left, sun behind the speaker's left, lathe mesas. Muddy and all one tone, no raking
   shadows. The motes read as snow (160, too bright), the puffs were small and white, the mesas were squat pancakes,
   and the paper sun was cut off at the corner.
2. **Sun behind the right, in frame.** The sun now reads, but blows out to white. The mesas look like flowerpots and
   the dunes like flat discs. Motes cut to 55, dim.
3. **Halo rings, slimmer mesas.** Still no shadows at all: the paper sky card stood in the sun's path and its shadow
   covered the whole set at 12 degrees. The card and the paper sun no longer cast shadows (`shadow: False`).
4. **Shadows.** Long shadows appear, and the speaker throws orange onto the sand. But the tissue sun was lit through from
   behind by the sun lamp and blew out, so the sun is now paper that glows of its own (`emit`), not tissue.
5. **My own kit pieces** (`studio/engine/kit_ext/dust.py`): `dunes`, a corduroy sheet over ridges (a gentle windward
   slope, a steep slip face, a wandering crest) that fades into the floor at its edges, its ribs running along the
   crests like wind ripples; and `strata`, irregular slabs of cut suede stacked on a rounded talus. The dunes now read
   at once.
6. **Raking sun from the right (azimuth 122), warm haze, wool puffs.** At a haze density of 0.035 it was a dust storm.
7. **Haze at 0.008.** Golden air, long shadows to the left. But the speaker's sunlit side faced away from the camera,
   so it read flat.
8. **Camera moved to the front right (azimuth 20), speaker turned to face it (16 degrees).** The acrylic reads amber now.
   But the puffs overlapped the speaker, the sun was cut by the frame, and the speaker was small.
9. **Reframed.** Speaker on the left third at about 40 % of the frame height, the streak clear of it to the right,
   the footprints running out of frame. Still cake-like mesas.
10. **Mid proof.** The mood works and the footprints land as the joke. But one mesa sat right above the speaker, the
    sun was still cut, and the palette was muddy brown.
11. **Long low mesas and one slim butte**, the sun moved in behind the butte (it is setting), and a little sage
    corduroy saguaro as the one accent: it says "desert" in a word, toy-like.
12. **Saguaro clear of the edge, warmer puffs (`#E8955A`), a faint glow on the sky card, a stronger rim.**
13. and 14 (mid). Pebbles in the near foreground, twice: both times they fell below the frame, so they were dropped.
    The empty sand with the speaker's long shadow is cleaner. At full size the haze veiled the speaker.
15. **Haze only behind the speaker** (its box starts at y = 0.9, thicker at 0.012): the hero is clear and saturated,
    while the distance keeps its air. Accepted.

Portrait: `portrait_of` at a 55 mm lens left the speaker at 18 % of the height (the 4:5 frame sees much taller). Rebuilt
at 95 mm from azimuth 6, 7.5 m: the speaker at about 38 %, the big sun above it, the butte to its right. The longer lens
gives a shallower field, so the background melts more than in the landscape. The footprints fall outside this frame;
the cloud carries the icon.

## Choices and why

- **The sun behind and to the right, in frame.** One idea of light: the low sun is the paper sun you see, so the long
  shadows and the glow on the acrylic are motivated by it.
- **The paper sun is opaque paper glowing of its own, not tissue.** Lit from behind by the real sun lamp, tissue blew
  out to white. Rings of paper, each glowing less than the one inside it, make the halo the way a model-maker would.
- **The camera from the front right.** From the left, the speaker's sunlit side faced away and it read flat.
- **The haze only behind the speaker.** It gives the distance air without veiling the hero.
- **No cover**, as the brief defaults.
