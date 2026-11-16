# Core matched to Hemisphere, switched off (2026-11-16, Step A)

The owner, 16 Nov: "Smoke darker yes, match other lamps, stronger sheet." The coordinator's direction: move Core, not
Hemisphere. Each Core gets a lighter dye until its off color meets Hemisphere's as built. Smoke is the one tint where
both move (Hemisphere 1.2x, Core 0.6x). Scratch cells only, with the corrected method (lamp_site.py since 9a6a2913), in
the one off rig. The lit cells are the rows' rig and exposure.

`core-match-sheet.png` has four rows: Hemisphere off as built (Smoke 1.2x); Core off with the dye matched; Core lit as
built today; Core lit matched.

| Tint | Core dye (x the stock pour) | Hemisphere off | Core off, matched | Largest gap | Core lit, today > matched | Core light out |
|---|---|---|---|---|---|---|
| Ember | 1 > **0.33** | 96, 14, 10 | 104, 4, 6 | 10 | 226, 84, 71 > 232, 133, 111 | 44.7 > 57.8 lm |
| Dust | 3 > **1.6** | 126, 37, 6 | 112, 41, 0 | 14 (red) | 215, 126, 86 > 209, 158, 125 | 51.1 > 62.2 lm |
| Acid | 3 > **1.35** | 100, 90, 10 | 100, 92, 1 | 9 | 189, 178, 108 > 196, 189, 146 | 63.2 > 76.1 lm |
| Poison | 1 > **0.6** | 9, 38, 15 | 0, 38, 7 | 9 (red) | 0, 122, 54 > 1, 153, 66 | 29.8 > 38.1 lm |
| Ice | 3 > **1.6** | 2, 55, 108 | 0, 60, 99 | 9 | 49, 144, 194 > 124, 171, 195 | 38.9 > 52.0 lm |
| Haze | 1 > **0.55** | 35, 31, 94 | 41, 24, 91 | 7 | 149, 82, 153 > 183, 132, 163 | 33.0 > 42.3 lm |
| Fog | 1 (unchanged) | 131, 130, 130 | 117, 117, 116 | 14 | 213, 193, 173 (same) | 95.1 lm |
| Smoke | 0.3 > **0.6** (Hemisphere 0.3 > **1.2**) | 20, 20, 21 | 17, 19, 20 | 3 | 172 > 138, 141, 142 | 52.7 > 35.1 lm (Hemisphere 378 > 260) |

Where the builds stop a closer match:
- **Core's ceiling.** Its white opal core behind the clear ball reads about 117 when off, even with a clear shell
  (Fog at 1x and 0.4x both read 117). Hemisphere reads lighter in its pale tints, so Dust's red stays 14 under and
  Fog 14 under.
- **Poison.** Core's green dye takes out red entirely (0), while Hemisphere's glass faces return some (9).
- **Ember, Acid, Ice, Haze** are within 7 to 10 in their largest channel and within 6 in the others. Finer steps
  would close them a little; they read alike at a glance.

Lit, every matched Core glows paler and lighter, closer to Hemisphere's look (Ember 84 > 133 in green). Its light out
rises 21 to 34 %, except Smoke, which is darker by choice.

## Fog

- **Leave the 14 levels (recommended).** Both read as clear-white glass when off; Core cannot get lighter.
- **The other way:** a breath of gray in Hemisphere's Fog shell (about 0.1x of Smoke's dye) to bring it to about 117.
  - It dims Hemisphere Fog's lit glow by roughly 10 %.
  - It touches every Hemisphere Fog picture (fog-direct, fog-under, the row, the cluster).

## "Stronger sheet"

The owner's words also say "stronger sheet". The direction above doesn't address it. If it means a denser opal sheet,
v2 measured that it moves Hemisphere off by at most 5 levels, and it would cost light and every Hemisphere picture. To
confirm before Step B.

## Audits and emitters

- Audit: Core off (orb-red at 0.33x) in the off rig, hidden lights in frame 0.0. The lit cells use the rows' rig.
- Emitters off: the strip key (hidden) and the lifted world.
- Emitters lit: the LED faces, plus the hidden key and fill.
