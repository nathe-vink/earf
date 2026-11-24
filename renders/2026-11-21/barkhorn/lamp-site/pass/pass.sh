#!/bin/bash
# The re-render pass (2026-11-21, the coordinator's go-ahead at 21:59): one tint's group, full size (1600 x 2000), house
# ground, the owner's pours as lamp_site.py's defaults (no pour switches here).
#   renders/2026-11-21/barkhorn/lamp-site/pass/pass.sh TINT GROUP     TINT: red orange amber green blue violet black (ice: Fog waits)
#   GROUP A: pendant OFF, B: Core OFF (as row-off/, 128 spp); C: pendant LIT (as ember-r6-hemi.sh, 512 spp; one studio and
#   exposure for every tint, the rule (a)); D: Core LIT (LIT-g's recipe, once set; see README)
# Writes pass/TINT/{hemisphere,core}-TINT-{off,lit}.png and audit/, prints the meters. Skips what exists.
set -e
T=${1:?tint}; G=${2:?group}
ROOT=$(cd "$(dirname "$0")/../../../../.." && pwd)
D=$ROOT/renders/2026-11-21/barkhorn/lamp-site/pass/$T; mkdir -p $D/audit
S=${TMPDIR:-/tmp}/pass-$T-$G; mkdir -p $S
FPY=$ROOT/.venv-fab/bin/python; M=$ROOT/renders/2026-11-20/barkhorn/lamp-site/meter
cd $ROOT/spinoffs/barkhorn/companions
HOFF="LIGHTS_OFF=1 HOUSE_ROOM_TRANS=1 HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_LIFT_RX=bg-left HOUSE_KEYFLAG=0,60,25,60,2 HOUSE_WALL_LL=0.35 HOUSE_WALL_LL_SPREAD=30 HOUSE_BG=1.16"
COFF="LIGHTS_OFF=1 HOUSE_ROOM_TRANS=1 HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1 HOUSE_BG=1.16"
HLIT="HOUSE_SOFTBOX_SEEN=0 DENOISE_PASSES=RGB HOUSE_STUDIO=3.5 HOUSE_EV=-5.15 HOUSE_SWEEP_AO=0 HOUSE_ROOM_TRANS=1 HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_LIFT_RX=bg-left HOUSE_KEYFLAG=0,60,25,60,2 HOUSE_BG=1.16"
CLIT="GUIDE_ORB=1 HOUSE_BOUNCE=0,0,0,0,0.19,-0.405,0.03,18,8.5,0.015 HOUSE_BOUNCE_BLEND=0.9 HOUSE_BOUNCE_COLOR=FFF4E8 HOUSE_BOUNCE_CUT=0.01,0.06,0.0262,0.05 HOUSE_BOUNCE_SOFT=0.003 HOUSE_BOUNCE_TOP=0.01,0.10,0.0335,0.06 HOUSE_LAMP_K=key:0 HOUSE_SOFTBOX_SEEN=0 DENOISE_PASSES=RGB HOUSE_STUDIO=0.714 HOUSE_EV=-2.85 HOUSE_SWEEP_AO=0 HOUSE_ROOM_TRANS=1 HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1 HOUSE_BG=1.16"   # LIT-g (ember-r6-core-g.sh)
case $G in
  A) n=hemisphere-$T-off; f=house-dome-$T; E=$HOFF; sp=128; FL=""; mk=shade.png ;;
  B) n=core-$T-off; f=house-orb-$T; E=$COFF; sp=128; FL="HOUSE_FLAGS=horn cutter"; mk=ball.png ;;
  C) n=hemisphere-$T-lit; f=house-dome-$T; E=$HLIT; sp=512; FL=""; mk=shade.png ;;
  D) [ "${RUN_D:-0}" = 1 ] || { echo "group D waits for the lamps lane's word (LIT-g full frame): run with RUN_D=1 when told"; exit 2; }; n=core-$T-lit; f=house-orb-$T; E=$CLIT; sp=512; FL="HOUSE_FLAGS=horn cutter"; mk=ball.png ;;
  *) echo "group A B C D"; exit 1 ;;
esac
[ -s $D/audit/$n.txt ] || { env $E ${FL:+"$FL"} AUDIT=1 MASK=$S/m.png python3.11 lamp_site.py $f > $S/$n.aud 2>&1 && \
    grep -E "^AUDIT|HIDDENCAST|CASTCHECK|^   (IN FRAME|in|out|practical) |^RAYVIS|^LINK|CORE_ABS" $S/$n.aud > $D/audit/$n.txt; }
if [ ! -s $D/$n.png ]; then
  t0=$(date +%s)
  env $E ${FL:+"$FL"} EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples $sp > $S/$n.log 2>&1
  $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null
  grep -h "CORE_ABS" $S/$n.log || true; echo "$n $(( $(date +%s) - t0 )) s"; date -u
fi
cd $M && $FPY meter.py corners $D/$n.png && $FPY meter.py body $mk $D/$n.png && $FPY meter.py glowy $mk $D/$n.png
