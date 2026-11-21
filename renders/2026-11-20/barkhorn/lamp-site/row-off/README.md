# Hemisphere OFF, the other seven tints (helper sessions)

The Ember pendant OFF of round 5 (`../house8/hemisphere-ember-off.png`, commit 4c281bc6) is READY. These frames carry its exact set to the other tints, one tint per helper. They depend on nothing still open:

- The Hemisphere's pour per tint is in `lamp_site.py` (TINT_LOAD, HEMI_MIX).
- The sweep's painted contact term cannot reach a hanging shade. It is an ambient-occlusion term 0.4 m × HOUSE_S 0.2 = 0.08 m deep on the sweep, and the shade's rim hangs 0.306 m above the floor.

## Setup (a fresh cloud container)

1. Check out branch `r32-lamps-final` at the commit the coordinator names (or later).
2. `studio/setup.sh` (idempotent). It installs:
   - `bpy` 5.0.1 on `python3.11`, with numpy 1, for Cycles;
   - `.venv-fab/` (numpy 2, Pillow), for `launch/house_finish.py` and the meters.

   Never install CAD packages into the system Python.
3. Check: `python3.11 -c "import bpy; print(bpy.app.version_string)"` prints 5.0.1.

## Run

    renders/2026-11-20/barkhorn/lamp-site/row-off/hemisphere-off.sh TINT

TINT is one of orange (Dust), amber (Acid), green (Poison), blue (Ice), violet (Haze), ice (Fog) or black (Smoke dark). The script takes only the tint; per-tint loading and lamp mix come from the code.

On 4 cores the audit takes about 2 min and the frame (1600 × 2000, 128 spp) about 25-30 min. The script writes:

- `row-off/hemisphere-TINT-off.png` (about 3 MB)
- `row-off/audit/hemisphere-TINT-off.txt`

It then prints the meters.

## Check before committing

- The audit: every `out` line 0.0 % (no hidden mesh casts into frame). CASTCHECK 0.0 for every entry except house-wall_left 5.45 and house-key-flag 18.71: the Ember OFF audit (house8/audit/hemisphere-ember-off.txt) shows the same two values.
- `meter.py corners`: the six wall and floor patches (TL TR ML MR LL BR, L*/a*/b*). The Ember OFF reads 83.9 / 93.1 / 84.0 / 92.3 / 96.5 / 88.3. The ground must not depend on the tint: each corner within about 1 L* of these. A bigger gap means a set difference; report it, don't commit.
- `meter.py body shade.png`: the shell's L*/C* (lower third, middle third, whole). The Ember OFF reads 25.4 / 28.3 / 25.7 L*. Other tints differ by their pour; report them, there is no target.
- Look at it at half size: the reflections single, the foot closed, cap and cord as in the Ember frame.

## Commit and report

Stage only these two files:

- `row-off/hemisphere-TINT-off.png`
- `row-off/audit/hemisphere-TINT-off.txt`

Message: `Hemisphere TINT OFF (row-off, as Ember round 5)`. Push to `r32-lamps-final`; if rejected, fetch and merge, never force.

Report back:

- the full 40-character SHA and the `date -u` time;
- the six corners and their gaps to the Ember;
- the shell's three L*/C*;
- the audit's pass or fail;
- anything that looks different from the Ember frame.

The frames go to the lamps lane to check before they count.

# Core OFF, the other seven tints (helper sessions, since 2026-11-21 10:00)

These are evidence for the owner's pour question: every tint's Core OFF on the house ground at today's loadings (`CORE_TINT_LOAD`, `CORE_MIX` in `lamp_site.py`). The settings are exactly the Ember Core OFF of round 5 (`../house8/core-ember-off.png`, b588c50d, from `ember-r5b.sh`):

- 128 spp, LIGHTS_OFF
- HOUSE_S 0.19, CORE_DOCK 0
- HOUSE_CUT2 fill,1.0, and the horn cutter flag
- the floor ring (HOUSE_FLOORCARD … -1,1)
- ROOM_TRANS on, BG 1.16
- the sweep's contact term on, as in every OFF frame

Setup is as above. Run:

    renders/2026-11-20/barkhorn/lamp-site/row-off/core-off.sh TINT

It writes `row-off/core-TINT-off.png` and `row-off/audit/core-TINT-off.txt`, then prints three meters:

- the corners;
- the ball (`body ball.png`);
- the base (`base`).

The frame takes about 25-30 min on 4 cores.

Checks before committing:

- **The audit:** every `out` line 0.0 %. CASTCHECK 0.0 for every entry except house-floorcard 30.09; the Ember Core OFF audit (`house8/audit/core-ember-off.txt`) shows the same.
- **The corners:** the Ember Core OFF reads TL 82.3, TR 93.1, ML 88.5, MR 93.3, LL 92.8, BR 89.6 (not the pendant's; the Core's ground differs). Each corner should be within about 1 L*; report any bigger gap and don't commit. The lower corners sit near the ball's coloured shadow, so a dark tint may pull them slightly; say so if it does.
- **The ball:** report its lower third, middle third and whole L*/C*. The Ember reads 41.3/56.2, 37.7/71.0 and 39.3/62.7.
- **The base:** report the meter's line. The Ember reads centre 37.0/55.6, cL 31.7, cR 27.9, lip top 23.1, below L* 20 on 2.0 %. Tints differ; there is no target.
- **The look:** view at half size. The base in its tint, its flanks not smoky; the straight edge across the ball's bottom is the base lip seen through the ball (physical, keep).

Commit `row-off/core-TINT-off.png` and its audit as `Core TINT OFF (row-off, as Ember round 5)`. Report as for the pendant.
