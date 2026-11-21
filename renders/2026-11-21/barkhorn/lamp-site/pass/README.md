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

## Commit and report

Stage `pass/TINT/` only; message `Pass: TINT GROUP`; pull and merge before pushing, never force. Report the SHA, the time, and the meter lines.
