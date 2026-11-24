#!/bin/bash
# Round 2 of the critics' tests (2026-11-24, the coordinator 01:03): one frame from a base recipe plus the switches in $X.
#   X='HOUSE_AIM=key:-0.5,0,0.5 ...' renders/2026-11-24/barkhorn/lamp-site/tests/r2.sh NAME BASE TINT [SPP] [SCALE] [BORDER]
# BASE: hoff  pendant OFF, the pass's ground with wall_left lifted, the room fitted, no key flag (round 1's hb1/hc)
#       coff  Core OFF, no ring, no cutters, the room fitted
#       hlit  pendant LIT exactly as pass C (rule (a)'s studio and exposure)
#       clit  Core LIT as round 1's e2: pass D with the softboxes seen
# Writes tests/r2/NAME.png and r2/audit/NAME.txt (the audit's CASTCHECK must read 0.0), prints the meters on the frame
# scaled to 1600 x 2000. DENOISE=0 in X renders without the denoiser. Skips what exists.
set -e
N=${1:?name}; BASE=${2:?base}; T=${3:?tint}; SP=${4:-128}; SC=${5:-0.5}; B=${6:-}
ROOT=$(cd "$(dirname "$0")/../../../../.." && pwd)
D=$ROOT/renders/2026-11-24/barkhorn/lamp-site/tests/r2; mkdir -p $D/audit
S=${TMPDIR:-/tmp}/r2-$N; mkdir -p $S
FPY=$ROOT/.venv-fab/bin/python; M=$ROOT/renders/2026-11-20/barkhorn/lamp-site/meter
cd $ROOT/spinoffs/barkhorn/companions
KF=HOUSE_KEYFLAG=0,60,25,60,2; RING=HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1; FL=""; DN=1
case $BASE in
  hoff) f=house-dome-$T; mk=shade.png; E="LIGHTS_OFF=1 HOUSE_ROOM_TRANS=1 HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_WALL_LL=0.35 HOUSE_WALL_LL_SPREAD=30 HOUSE_BG=1.16 HOUSE_LIFT_RX=bg-left,wall_left HOUSE_ROOM_FIT=1" ;;
  coff) f=house-orb-$T; mk=ball.png; E="LIGHTS_OFF=1 HOUSE_ROOM_TRANS=1 HOUSE_S=0.19 CORE_DOCK=0 HOUSE_BG=1.16 HOUSE_ROOM_FIT=1" ;;
  hlit) f=house-dome-$T; mk=shade.png; E="HOUSE_SOFTBOX_SEEN=0 DENOISE_PASSES=RGB HOUSE_STUDIO=3.5 HOUSE_EV=-5.15 HOUSE_SWEEP_AO=0 HOUSE_ROOM_TRANS=1 HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_LIFT_RX=bg-left $KF HOUSE_BG=1.16" ;;
  clit) f=house-orb-$T; mk=ball.png; FL="HOUSE_FLAGS=horn cutter"; E="GUIDE_ORB=1 HOUSE_BOUNCE=0,0,0,0,0.19,-0.405,0.03,18,8.5,0.015 HOUSE_BOUNCE_BLEND=0.9 HOUSE_BOUNCE_COLOR=FFF4E8 HOUSE_BOUNCE_CUT=0.01,0.06,0.0262,0.05 HOUSE_BOUNCE_SOFT=0.003 HOUSE_BOUNCE_TOP=0.01,0.10,0.0335,0.06 HOUSE_LAMP_K=key:0 HOUSE_SOFTBOX_SEEN=1 DENOISE_PASSES=RGB HOUSE_STUDIO=0.714 HOUSE_EV=-2.85 HOUSE_SWEEP_AO=0 HOUSE_ROOM_TRANS=1 HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 $RING HOUSE_BG=1.16" ;;
  *) echo "base: hoff coff hlit clit"; exit 1 ;;
esac
for kv in $X; do [ "${kv%%=*}" = DENOISE ] && DN=${kv#*=}; done
X2=$(for kv in $X; do [ "${kv%%=*}" = DENOISE ] || printf '%s\n' "$kv"; done)
# (HOUSE_LAMP_K in X replaces the base's: the Core LIT's key:0 is kept by adding it there)
[ -s $D/audit/$N.txt ] || { env $E ${FL:+"$FL"} $X2 ${B:+BORDER=$B} AUDIT=1 MASK=$S/m.png python3.11 lamp_site.py $f --scale $SC > $S/$N.aud 2>&1 && \
    grep -E "^AUDIT|HIDDENCAST|CASTCHECK|^   (IN FRAME|in|out|practical) |^RAYVIS|^LINK|LAMP_MOVE|LAMPK|ROOM_FIT|HOUSE_WB|HOUSE_GEL|HOUSE_CAM|HEMI_TOP|HEMI_LOCK|CORE_ABS|BORDER|LIGHTSET" $S/$N.aud > $D/audit/$N.txt; }
nz_=$(grep -o "CASTCHECK.*" $D/audit/$N.txt | tr ',' '\n' | grep -v " 0.0" | grep ": " || true)   # (an empty {} is clean)
[ -n "$nz_" ] && echo "$nz_" | sed "s/^/$N castcheck NOT ZERO: /" || echo "$N castcheck all 0.0"
if [ ! -s $D/$N.png ]; then
  t0=$(date +%s)
  env $E ${FL:+"$FL"} $X2 ${B:+BORDER=$B} EXR=0 DENOISE=$DN LAMP_OUT=$S/$N-raw.png python3.11 lamp_site.py $f --samples $SP --scale $SC > $S/$N.log 2>&1
  $FPY launch/house_finish.py $S/$N-raw.png $D/$N.png > /dev/null
  echo "$N $(( $(date +%s) - t0 )) s"; date -u
fi
[ -n "$B" ] && exit 0
$FPY -c "from PIL import Image; Image.open('$D/$N.png').convert('RGB').resize((1600, 2000), Image.LANCZOS).save('$S/$N.png')"
cd $M && $FPY meter.py corners $S/$N.png && $FPY meter.py body $mk $S/$N.png
case $BASE in coff) $FPY $ROOT/renders/2026-11-24/barkhorn/lamp-site/tests/base.py $S/$N.png ;; *lit) $FPY meter.py glowy $mk $S/$N.png ;; esac
