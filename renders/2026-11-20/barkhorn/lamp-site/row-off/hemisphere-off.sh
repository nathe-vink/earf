#!/bin/bash
# One Hemisphere OFF frame for the house ground, any tint, exactly as the Ember OFF of round 5
# (ember-r5b.sh, house8/hemisphere-ember-off.png, 4c281bc6): 128 spp, denoised, lamp off, the low sweep lamp at 0.35.
#   renders/2026-11-20/barkhorn/lamp-site/row-off/hemisphere-off.sh TINT      (TINT: orange amber green blue violet ice black)
# Writes row-off/hemisphere-<TINT>-off.png and row-off/audit/hemisphere-<TINT>-off.txt. Skips what already exists.
set -e
T=${1:?tint key}
case $T in orange|amber|green|blue|violet|ice|black|red) ;; *) echo "unknown tint $T"; exit 1;; esac
ROOT=$(cd "$(dirname "$0")/../../../../.." && pwd)
D=$ROOT/renders/2026-11-20/barkhorn/lamp-site/row-off; mkdir -p $D/audit
S=${TMPDIR:-/tmp}/row-off-$T; mkdir -p $S
FPY=$ROOT/.venv-fab/bin/python
cd $ROOT/spinoffs/barkhorn/companions
n=hemisphere-$T-off; f=house-dome-$T
SET="LIGHTS_OFF=1 HOUSE_ROOM_TRANS=1 HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_LIFT_RX=bg-left HOUSE_KEYFLAG=0,60,25,60,2 HOUSE_WALL_LL=0.35 HOUSE_WALL_LL_SPREAD=30 HOUSE_BG=1.16"
[ -s $D/audit/$n.txt ] || { env $SET AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py $f > $S/$n.aud 2>&1 && \
    grep -E "^AUDIT|HIDDENCAST|CASTCHECK|  (in|out) " $S/$n.aud > $D/audit/$n.txt; }
[ -s $D/$n.png ] || { env $SET EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples 128 > $S/$n.log 2>&1 && \
    $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null; }
ls -la $D/$n.png; date -u
M=$ROOT/renders/2026-11-20/barkhorn/lamp-site/meter
cd $M && $FPY meter.py corners $D/$n.png && $FPY meter.py body shade.png $D/$n.png
