#!/bin/bash
# One Core OFF frame for the house ground, any tint, exactly as the Ember OFF of round 5
# (ember-r5b.sh, house8/core-ember-off.png, b588c50d): 128 spp, denoised, lamp off, off its dock, the fill cut, the floor ring.
#   renders/2026-11-20/barkhorn/lamp-site/row-off/core-off.sh TINT      (TINT: orange amber green blue violet ice black)
# Writes row-off/core-<TINT>-off.png and row-off/audit/core-<TINT>-off.txt. Skips what already exists.
set -e
T=${1:?tint key}
case $T in orange|amber|green|blue|violet|ice|black|red) ;; *) echo "unknown tint $T"; exit 1;; esac
ROOT=$(cd "$(dirname "$0")/../../../../.." && pwd)
D=$ROOT/renders/2026-11-20/barkhorn/lamp-site/row-off; mkdir -p $D/audit
S=${TMPDIR:-/tmp}/row-off-$T; mkdir -p $S
FPY=$ROOT/.venv-fab/bin/python
cd $ROOT/spinoffs/barkhorn/companions
n=core-$T-off; f=house-orb-$T
SET="LIGHTS_OFF=1 HOUSE_ROOM_TRANS=1 HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1 HOUSE_BG=1.16"
[ -s $D/audit/$n.txt ] || { env $SET "HOUSE_FLAGS=horn cutter" AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py $f > $S/$n.aud 2>&1 && \
    grep -E "^AUDIT|HIDDENCAST|CASTCHECK|  (in|out) " $S/$n.aud > $D/audit/$n.txt; }
[ -s $D/$n.png ] || { env $SET "HOUSE_FLAGS=horn cutter" EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples 128 > $S/$n.log 2>&1 && \
    $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null; }
ls -la $D/$n.png; date -u
M=$ROOT/renders/2026-11-20/barkhorn/lamp-site/meter
cd $M && $FPY meter.py corners $D/$n.png && $FPY meter.py body ball.png $D/$n.png && $FPY meter.py base $D/$n.png
