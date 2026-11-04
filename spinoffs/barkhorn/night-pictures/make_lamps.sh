#!/usr/bin/env bash
# The recipe for the night pictures' lamp files (the coordinator, 2026-11-04 01:47, point 7): the .blend files that
# make_shot.py points at are built here, from the lamps lane's own rig at a named SHA, so nothing depends on one
# container.
#
#   bash spinoffs/barkhorn/night-pictures/make_lamps.sh LAMPS_WORKTREE OUT_DIR
#     LAMPS_WORKTREE: a checkout of r32-lamps-final at LAMPS_SHA below (a sparse worktree of studio/ and
#                     spinoffs/barkhorn/companions/ is enough), with its lamp meshes built first:
#       .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/dome_pendant.py --out spinoffs/barkhorn/companions/out-dome-pendant
#       .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/companions/orb_table.py --out spinoffs/barkhorn/companions/out-orb-table
#
# The lamps exactly as the lamps lane's file has them (the coordinator, 01:28: one scale, 0.0065 W a lumen; never one
# part scaled alone): the Hemisphere's COB 3.2 W for its 490 lm and its liner at 11.5 W/m2, both at the rig's own
# 2700 K; no COB_W, no LAMP_CCT. Fog (clear) shells, so the speaker's colour is the only colour.
set -euo pipefail
LAMPS_SHA=26400e7c767bf626eb9e746e6141571aa8a431e5
WT=$1; OUT=$2
HERE=$(cd "$(dirname "$0")" && pwd)
have=$(git -C "$WT" rev-parse HEAD)
if [ "$have" != "$LAMPS_SHA" ]; then echo "make_lamps: $WT is at $have, not $LAMPS_SHA" >&2; exit 1; fi
mkdir -p "$OUT"
env -u COB_W -u LAMP_CCT -u CORE_EMIT python3.11 "$HERE/lamp_export.py" "$WT" hemi-fog-night "$OUT/hemi-fog-night.blend" > "$OUT/hemi-fog-night.log" 2>&1
echo "hemi-fog-night.blend from $LAMPS_SHA"
# the Core, for the wall picture only, on the same scale: about 560 lm out, 3.6 W at 0.0065 W/lm, over its core's
# 0.0408 m2 (pi x 0.0408 x 28 = 3.6 W); the lamps lane's own CORE_EMIT (0.05) was set by eye, far under that
CORE_EMIT=28 env -u COB_W -u LAMP_CCT python3.11 "$HERE/lamp_export.py" "$WT" core-fog-night-nested "$OUT/core-fog-night-nested.blend" > "$OUT/core-fog-night-nested.log" 2>&1
echo "core-fog-night-nested.blend from $LAMPS_SHA (CORE_EMIT 28)"
# the pendant's ceiling canopy from the same CAD (night_room.py places it where the cord meets the ceiling)
cp "$WT/spinoffs/barkhorn/companions/out-dome-pendant/stl/canopy.stl" "$OUT/hemi-canopy.stl"
echo "hemi-canopy.stl from $LAMPS_SHA"
