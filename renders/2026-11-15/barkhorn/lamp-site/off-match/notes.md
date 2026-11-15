# Off match: Hemisphere and Core switched off in one rig (2026-11-15)

The owner: "I think it's important for off on hemi and core to match colors." The choice sheet's two off rows could not
be compared, because they were shot in different rigs. Here both lamps are in ONE rig: the day row's strip (3.0 x 0.5 m,
1.9 m above and 0.6 m in front of the lamp's middle), the world lifted (2.8, #BDA999), no fill, no kicker, 5000 K, the
camera at 5000 K, studio 12, EV -1, paper #9A9A9A. The camera is the same distance (0.86 m) and lens (70 mm) for both,
and everything is set by env switches; no file was changed (off-match.sh). The colors are the median sRGB of the body,
away from highlights (measure.py: Hemisphere's lower flanks, Core's lower ball).

## Why the same glass reads differently off

- Behind Hemisphere's 3 mm tinted layer: 6 mm of clear acrylic, then the opal diffuser, which scatters only on its
  inside face, then the hollow, open at the mouth. Room light reaches the inside through the mouth and comes back out
  through the dye once, and the backdrop partly shows through the shade.
- Behind Core's 6 mm tinted wall (half the loading, the same optical depth): an air gap, then the white opal core,
  scattering outward. The ball is closed but for a 40 mm port, so the light it returns has crossed the dye twice.
- So dense tints read lighter on Hemisphere. The two rigs in the choice sheet added more: Hemisphere's off rig lit the
  world at about 0.24 and Core's day row at 2.8.

## Smoke strengths, off (one rig)

| Smoke | Hemisphere | Core | Hemisphere minus Core |
|---|---|---|---|
| 0.3x (now) | 58, 59, 59 | 44, 46, 47 | +14 |
| 0.5x | 41, 42, 43 | 22, 23, 24 | +19 |
| 0.8x | 27, 28, 29 | 7, 8, 8 | +20 |
| 1.2x | 19, 20, 20 | 3, 3, 4 | +16 |
| 2.0x | 16, 15, 16 | | |
| 3.0x | 15, 14, 15 | | |
| 0.6x | | 15, 16, 17 | |
| 0.65x | | 12, 14, 14 | |

Fog now: Hemisphere 101, 100, 100 against Core 107, 107, 106 (-6): a match.

## The Smoke answer for all three of his points

Not whiter than Fog lit, no warm LED, and the off colors matching:
- Hemisphere Smoke 2.0x and Core Smoke 0.6x, so DIFFERENT strengths on the two lamps.
- Off they match: 16, 15, 16 against 15, 16, 17.
- Lit, both read gray beside Fog (237, 223, 208 and 212, 192, 172): Hemisphere 46, 53, 56; Core 136, 138, 140.
- Light out against today's Smoke, with the same LED: Hemisphere 241 lm (84 %); Core 26.1 lm (74 %).
- Both are dark smoked glass when off, darker than today's Smoke (58 on Hemisphere, 44 on Core).
- Hemisphere's off color bottoms out near 15 (2.0x and 3.0x read alike), so a darker match isn't possible.
- At one strength on both lamps the off colors never match: Hemisphere stays 14 to 20 lighter.
- The lit pair doesn't match each other: Hemisphere reads darker gray than Core.

`smoke-pair.png` shows the pair, off in this rig and lit in the rows' rig.

## The other tints, off, at today's strengths (`tints-off.png`)

| Tint | Hemisphere | Core | Verdict |
|---|---|---|---|
| Ember | 73, 14, 13 | 63, 0, 0 | close; Hemisphere slightly lighter |
| Dust | 96, 29, 9 | 95, 13, 0 | close; Hemisphere a little less saturated |
| Acid | 78, 70, 9 | 71, 62, 0 | matches |
| Poison | 12, 33, 15 | 1, 14, 3 | Hemisphere lighter |
| Ice | 3, 43, 84 | 0, 31, 76 | close |
| Haze | 31, 26, 73 | 6, 11, 64 | Hemisphere visibly lighter and lilac: the largest gap |
| Fog | 101, 100, 100 | 107, 107, 106 | matches |
| Smoke | 58, 59, 59 | 44, 46, 47 | Hemisphere lighter |

The same cause runs through all of them: the dense, dark tints read lighter on Hemisphere.

## Audits and emitters

- Audits: Hemisphere (dome-black) and Core (orb-black) in this rig, hidden objects none, hidden lights in frame 0.0.
  The lit pair cells use the rows' rig, whose audits read the same (the choice sheet).
- Emitters, off: the strip key (hidden) and the lifted world. Lit: the LED faces (24 per Hemisphere, 1 per Core), and
  the hidden key and fill.
