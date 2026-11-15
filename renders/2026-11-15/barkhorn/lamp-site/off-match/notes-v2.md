# Off match, v2: the method checked, Core corrected (2026-11-15, evening)

Supersedes the Core numbers in notes.md, tints-off.png and the choice sheet's Core off row. The Hemisphere numbers there
stand.

## The method, and how it was checked

- The shade's layers are nested with real 1 mm air gaps (crystal.py `GAP = 1.0`; bom.csv line 9, the vent that "lets
  the air gaps between the layers breathe"). The model keeps them.
- The reference is plain refraction through the glass, checked converged: the same cell at 1024 samples, no denoiser,
  the mean over the body. Hemisphere Fog: converged 101 = today's 101, so Hemisphere's off renders are right.
- Core Fog: converged plain refraction 91 against today's 107; Core Smoke 0.3x: 34 against 45. Core's ball today lets
  shadow rays through its glass (thin_shadow) AND traces the refraction, so room light reaching its opal is counted
  twice. Core's off and daylight renders read 11 to 16 levels too bright.
- Two "fixes" that let rays pass the glass (thin_shadow on Hemisphere, a transparent filter) read 126 to 128 for
  Hemisphere Fog. That is brighter than the bare opal (110), which only reflections could exceed. They skip refraction
  and the light the layers trap and guide, and are wrong here.
- Core's own light is not affected. Its light out is 64.6 lm for Fog with today's ball, with plain refraction, and in
  the scratch rig. So Core's lit frames and photometry stand.

The fix for later, on the coordinator's go: Core's ball as plain refracting glass (no thin_shadow on its two faces).
It was tried in a scratch copy only; lamp_site.py is unchanged.

## A: dye matches (dye-match.png)

The off colors are median sRGB in the one off rig; the lit colors are the rows' rig. Light out is against today's.

| | Hemisphere off | Core off | Hemisphere lit | Core lit | Light out, Hemisphere / Core |
|---|---|---|---|---|---|
| Smoke now (0.3x / 0.3x) | 58, 59, 59 | 34, 35, 36 | 209, 210, 210 | 170, 171, 171 | 287 / 35.2 lm |
| Smoke: Hemisphere 1.2x, Core 0.45x | 19, 20, 20 | 19, 20, 21 | 125, 131, 134 | 154, 156, 156 | 86 % / 85 % |
| Haze now (1x / 1x) | 31, 26, 73 | 3, 7, 51 | 198, 143, 198 | 147, 81, 153 | 254.4 / 27.3 lm |
| Haze: Hemisphere 1.6x, Core 0.6x | 19, 21, 60 | 22, 13, 64 | 154, 98, 194 | 178, 124, 161 | 97 % / 117 % |
| Poison now | 12, 33, 15 | 2, 9, 3 | 18, 183, 87 | 0, 121, 53 | |

- **Smoke** matches within 1 level. Lit, Hemisphere reads gray and Core a dimmer neutral (154) beside Fog (212, 192,
  172).
- **Haze** matches within 8 (green). Lit, the two drift apart: Hemisphere bluer, Core pinker.
- Haze could also be met by Core alone at about 0.45x (0.4x: 38, 22, 72 against Hemisphere's 31, 26, 73, within 7).
  That would leave Hemisphere unchanged but make Core much paler.
- **Poison** has no match within 6. Core's green blocks red entirely (0), while Hemisphere's glass reflections hold it
  near 12. A lighter Core raises green only (0.4x: 0, 38, 8).
- Hemisphere's floor near 15 is real: plain refraction holds it, from the four glass faces' own reflections.

## B: the opal grade, off

A denser grade (Perspex Opal 1T04, T 30 %; 069, T 9 %; R estimated about 63 % and 84 %) changes Hemisphere's off color
by at most 5 levels in this rig: Fog 101 to 100; Haze 31, 26, 73 to 23, 23, 68. In the evenly lit room the opal is lit
from inside (through the mouth) about as much as from outside, and R + T is about 0.93 for every grade. So a whiter
lining does not make the off colors match. Lit stands, as the coordinator said.

## The eight tints, off (tints-off-v2.png)

Hemisphere is from today's renders, Core by plain refraction.

| Tint | Hemisphere | Core | Gap (largest channel) |
|---|---|---|---|
| Ember | 73, 14, 13 | 50, 0, 0 | 23 |
| Dust | 96, 29, 9 | 79, 6, 0 | 23 |
| Acid | 78, 70, 9 | 58, 50, 0 | 20 |
| Poison | 12, 33, 15 | 2, 9, 3 | 24 |
| Ice | 3, 43, 84 | 0, 23, 63 | 21 |
| Haze | 31, 26, 73 | 3, 7, 51 | 28 |
| Fog | 101, 100, 100 | 91, 91, 90 | 10 |
| Smoke | 58, 59, 59 | 34, 35, 36 | 24 |

With Core corrected, every tint reads lighter on Hemisphere when off, by 20 to 28 levels except Fog (10). Hemisphere's
open bowl and four glass faces lift and grey every tint. Ember, Dust and Ice are no longer "close": the rule fails for
all but Fog, so it is one systematic choice, not three fixes. Either every Core dye lighter, or every Hemisphere dye
denser, within Hemisphere's floor.

## Finals that show a lamp off or in daylight

- Core, too bright today (needs the fix): `core-row-day.png`, `core-base-options-day.png`.
- Hemisphere, standing: `hemisphere-ember-off.png`, `hemisphere-ember-cap.png`.

## Audits and emitters

As off-match: hidden objects none, hidden lights in frame 0.0, in the off rig; the lit cells use the rows' rig.
Emitters off: the strip key (hidden) and the lifted world. Lit: the LED faces and the hidden key and fill.
