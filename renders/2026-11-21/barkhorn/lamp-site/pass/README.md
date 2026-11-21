# The re-render pass (2026-11-21)

Every lamp picture on the house ground, with the owner's pours. The plan is `renders/2026-11-20/barkhorn/lamp-site/plan/rerender-plan.md`; the go-ahead came from the coordinator at 21:59, for every tint but Fog. The pours are `lamp_site.py`'s defaults since 3b180d8c (Haze's Core round 2 since 981bd837), so no pour switches are set here.

## Setup

As `../../../2026-11-20/barkhorn/lamp-site/row-off/README.md`: branch `r32-lamps-final`, `studio/setup.sh`, `bpy` 5.0.1 on `python3.11`, and `.venv-fab`.

## Run, one tint per helper, in order

    renders/2026-11-21/barkhorn/lamp-site/pass/pass.sh TINT A   # pendant OFF, 128 spp, about 25-30 min
    renders/2026-11-21/barkhorn/lamp-site/pass/pass.sh TINT B   # Core OFF, 128 spp, about 25-30 min
    renders/2026-11-21/barkhorn/lamp-site/pass/pass.sh TINT C   # pendant LIT, 512 spp, about 60-70 min
    # D (Core LIT) waits for LIT-g's recipe; the lamps lane adds it here

TINT is one of red, orange, amber, green, blue, violet or black. Fog (ice) waits for its key test.

Each run writes `pass/TINT/{hemisphere,core}-TINT-{off,lit}.png` and `pass/TINT/audit/`, then prints three meters:

- the corners;
- the body: L*/C* of the lower third, middle third and whole;
- `glowy`: the coordinator's tint-agnostic glow, its median L*/C*/h and the share of mask pixels with any channel at or above 250.

Core frames log `CORE_ABS` for Dust, Ice and Haze; the audit keeps that line.

## Checks before committing

- **Audit:** every `out` line 0.0 %. CASTCHECK as in the Ember audits:
  - pendant: house-wall_left 5.45, house-key-flag 18.71;
  - Core: house-floorcard 30.09.
- **Corners (OFF):** within about 1 L* of the Ember OFF of the same lamp.
  - pendant: 83.9 / 93.1 / 84.0 / 92.3 / 96.5 / 88.3;
  - Core: 82.3 / 93.1 / 88.5 / 93.3 / 92.8 / 89.6;
  - the Core's lower corners move with its coloured light.
- **Body (OFF):** against the check-set frame of the same pour, within about 1 L*. The pendant's frames are `../../../2026-11-20/barkhorn/lamp-site/checkset/TINT/` or `row-off/`; the Core's are `checkset/dye/` for Dust, Ice and Haze.
- **Pendant LIT:**
  - Corners against the Ember pendant LIT (house9): TL 16.3, TR 23.6, ML 16.3, MR 22.4, LL 15.9, BR 20.6. Lamps are honest in brightness (one exposure), so the glow differs by tint.
  - Clip share: report it. Above about 1 % of the mask is a clipping tint; name it. The Ember pendant at 0.7x clipped about 3 % at the shade's top in the check set.

## OFF body references: exactly these frames (2026-11-21 22:25)

Use these, not the older row-off frames at the 17 Nov pours. The values are body whole L*/C*; the check-set frames are half size, and the medians hold to about 0.5.

| Tint | Pendant pour | Pendant reference | Whole | Core pour | Core reference | Whole |
|---|---|---|---|---|---|---|
| red | 0.7 | checkset/red/hemi-off-L0.7.png | 37.4/67.1 | 0.5 | house8/core-ember-off.png | 39.3/62.7 |
| orange | 2.1 | checkset/orange/hemi-off-L2.1.png | 54.3/71.7 | 2.6 + mix | checkset/dye/core-orange-off-abs1.0,0.35,2.5-add16-L2.6.png | 53.6/64.9 |
| amber | 3.0 | checkset/amber/hemi-off-L3.0.png | 67.0/63.9 | 2.0 | checkset/amber/core-off-L2.0.png | 65.3/58.1 |
| green | 1.0 | row-off/hemisphere-green-off.png | 29.6/37.8 | 0.45 | none at this pour with today's dye: report the value | - |
| blue | 3.0 | checkset/blue/hemi-off-L3.0.png | 38.4/59.5 | 1.72 + mix | checkset/dye/core-blue-off-abs3.2,0.85,1.19-L1.72.png | 38.6/64.9 |
| violet | 1.0 | checkset/violet/hemi-off-L1.0.png | 22.7/75.8 | 0.5 + mix | checkset/dye/core-violet-off-abs0.89,2.5,1.09.png | 26.8/77.3 |
| black | 1.2 | row-off/hemisphere-black-off.png | 3.4/1.2 | 0.5 | checkset/black/core-off-L0.5.png | 15.2/1.6 |

All paths are under `renders/2026-11-20/barkhorn/lamp-site/`.

## Commit and report

Stage `pass/TINT/` only; message `Pass: TINT GROUP`; pull and merge before pushing, never force. Report the SHA, the time, and the meter lines.
