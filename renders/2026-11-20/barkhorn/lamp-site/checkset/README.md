# Pour check set (2026-11-21)

The owner's pour question, put as real renders on the house ground: per tint, the pendant and Core at today's pour and at candidate pours, OFF and LIT, at half size (800 × 1000). It was asked for by the coordinator after the eight-tint critic pass. One helper per tint.

## Setup

As `../row-off/README.md`:

- branch `r32-lamps-final`;
- `studio/setup.sh`;
- `bpy` 5.0.1 on `python3.11`;
- `.venv-fab` for `house_finish.py` and the meters.

## Run

    renders/2026-11-20/barkhorn/lamp-site/checkset/checkset.sh TINT

TINT is one of red (Ember), orange (Dust), amber (Acid), green (Poison), blue (Ice), violet (Haze) or black (Smoke). Fog is not in the set: its fix is light on the product, not a pour.

The script writes `checkset/TINT/{hemi,core}-{off,lit}-L<pour>.png` and prints each frame's meters.

How the pours and settings are set:

- **Pendant pour (`HEMI_LOAD`):** a multiple of the base pour, as `TINT_LOAD` in `lamp_site.py`.
- **Core pour (`CORE_LOAD`):** the ball and base together, absolute; 0.5 is the chart figure. Today's Core is 0.5 × `CORE_TINT_LOAD`.
- **OFF frames:** exactly as `row-off/`, at 128 spp.
- **LIT frames:** exactly as round 6 (`ember-r6-hemi.sh` and `ember-r6-core.sh`), at 256 spp: softboxes unseen, colour-only denoise, the Core's key off. The studio and exposure are the same for every pour and tint, so the LIT row shows what a pour does to the glow. A lighter pour glows brighter, and may clip in light tints.

## What each tint renders

Today's OFF comes from the full-size frames already made. For Ember, today's LIT does too (house9).

| Tint | Today (pendant / Core) | New OFF | New LIT | Frames | Est. min (4 cores) |
|---|---|---|---|---|---|
| Ember (red) | 1.8 / 0.5 | pendant 1.0 (as built), 0.7; Core 0.75 (deeper) | pendant 1.0; Core 0.75 | 5 | about 45 |
| Ice (blue) | 6 / 1.5 | pendant 3 (as built), 2.1; Core 2.25 (deeper) | today both; pendant 3; Core 2.25 | 7 | about 70 |
| Haze (violet) | 1.8 / 0.5 | pendant 1.0 (as built), 0.7; Core 0.75 (deeper) | today both; pendant 1.0; Core 0.75 | 7 | about 70 |
| Acid (amber) | 5 / 1.5 | pendant 3 (as built), 2.1; Core 1.0 (a step lighter) | today both; pendant 3; Core 1.0 | 7 | about 70 |
| Poison (green) | 1.0 / 0.3 | pendant 0.7 | today both; pendant 0.7 | 4 | about 45 |
| Dust (orange) | 3 / 1.5 | pendant 2.1; Core 0.8 | today both; pendant 2.1; Core 0.8 | 6 | about 60 |
| Smoke (black) | 1.2 / 0.3 | Core 0.45, 0.6 (darker) | today both; Core 0.45 | 5 | about 50 |

The times assume about 7 min per OFF frame and 12 min per LIT frame at half size; they are estimates, not measured.

Assumptions to confirm:

- **Dust's "16 Nov 1.6x Core" read as Core 0.8** (1.6 × 0.5). If it meant something else, change the `orange` line.
- **Acid's Core step is lighter**, toward the lemon Tropos. A deeper step would be 2.25.
- **Ice's and Haze's hue: corrected after the renders.** I wrote that a pour does not move hue. That is false for Ice, and for Haze lit. Ice's hue moves with its pour: OFF h 300.8 at 6x, 288 at 3x, 278 at 2.1x; LIT 290 to 253. Haze's lit hue moves 322 to 340. A dense pour pins one channel near zero, which shifts the hue; the critics' measurements, 2026-11-21.

## Round 2

`checkset.sh TINT "LAMP:STATE:LOAD ..."` renders an explicit list instead of the tint's default.

## Checks and commit

Each frame's corners should match today's frames of the same lamp within about 1 L*. The lower corners of the Core move with its coloured light, as in `row-off/`.

Commit `checkset/TINT/` as `Pour check set: TINT`, pulling and merging before pushing. Report the per-frame meter lines.

## Sheet

    .venv-fab/bin/python renders/2026-11-20/barkhorn/lamp-site/checkset/sheet.py TINT [TROPOS_FRONT_IMAGE]

It writes `checkset/sheet-TINT.png`:

- columns: the Tropos front, then the pendant's pours (today first), then the Core's (today first);
- rows: OFF over LIT;
- each cell 400 × 500, labelled with lamp, pour and "(today)".
