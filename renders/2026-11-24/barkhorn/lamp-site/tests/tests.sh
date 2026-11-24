#!/bin/bash
# The critics' quarter-size tests (2026-11-24, the coordinator's list after the pass's critic round): Ember, half scale
# (800 x 1000, a quarter of the pixels), each with its audit (CASTCHECK must read 0.0 for every hidden object).
#   renders/2026-11-24/barkhorn/lamp-site/tests/tests.sh NAME
# Writes tests/NAME.png (finished, half scale) and audit/NAME.txt, and prints the meters on the frame scaled back to
# 1600 x 2000 (the meters' boxes are full-scale pixels). Skips what exists.
set -e
N=${1:?name}
ROOT=$(cd "$(dirname "$0")/../../../../.." && pwd)
D=$ROOT/renders/2026-11-24/barkhorn/lamp-site/tests; mkdir -p $D/audit
S=${TMPDIR:-/tmp}/t24-$N; mkdir -p $S
FPY=$ROOT/.venv-fab/bin/python; M=$ROOT/renders/2026-11-20/barkhorn/lamp-site/meter
cd $ROOT/spinoffs/barkhorn/companions
# the pass's recipes (pass.sh), the hidden key flag taken out of the pendant's so each test adds what it tests
HOFF="LIGHTS_OFF=1 HOUSE_ROOM_TRANS=1 HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_WALL_LL=0.35 HOUSE_WALL_LL_SPREAD=30 HOUSE_BG=1.16"
COFF="LIGHTS_OFF=1 HOUSE_ROOM_TRANS=1 HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 HOUSE_BG=1.16"
KF=HOUSE_KEYFLAG=0,60,25,60,2; RING=HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1; WL="HOUSE_LIFT_RX=bg-left,wall_left HOUSE_ROOM_FIT=1"
SP=${SP:-128}; FL=""
case $N in
  h0)    f=house-dome-red; E="$HOFF HOUSE_LIFT_RX=bg-left $KF"; mk=shade.png ;;                  # the pass as rendered
  hb1)   f=house-dome-red; E="$HOFF $WL HOUSE_KEY_AIM=-0.5,0,0.5"; mk=shade.png ;;                 # (b i) the key re-aimed
  hb2)   f=house-dome-red; E="$HOFF $WL HOUSE_KEY_AIM=-1.0,0,1.0"; mk=shade.png ;;                 # (b i) further
  hb3)   f=house-dome-red; E="$HOFF $WL HOUSE_KEYFLAG=0,60,25,60,0.6 HOUSE_KEYFLAG_REAL=1"; mk=shade.png ;;   # (b ii) a real flag at 0.12 m
  hc)    f=house-dome-red; E="$HOFF $WL $KF"; mk=shade.png ;;                                       # (c) wall_left lifted, the room fitted
  d0)    f=house-orb-red; E="$COFF $RING"; FL="HOUSE_FLAGS=horn cutter"; mk=ball.png ;;              # (d) as now
  d1)    f=house-orb-red; E="$COFF"; FL="HOUSE_FLAGS=horn cutter"; mk=ball.png ;;                    # (d) no ring
  d2)    f=house-orb-red; E="$COFF HOUSE_CUT_REAL=1"; FL="HOUSE_FLAGS=horn cutter"; mk=ball.png ;;   # (d) no ring, real cutters
  *) echo "h0 hb1 hb2 hb3 hc d0 d1 d2"; exit 1 ;;
esac
[ -s $D/audit/$N.txt ] || { env $E ${FL:+"$FL"} AUDIT=1 MASK=$S/m.png python3.11 lamp_site.py $f --scale 0.5 > $S/$N.aud 2>&1 && \
    grep -E "^AUDIT|HIDDENCAST|CASTCHECK|^   (IN FRAME|in|out|practical) |^RAYVIS|^LINK|KEY_AIM|KEYFLAG_REAL|CUT_REAL|ROOM_FIT" $S/$N.aud > $D/audit/$N.txt; }
grep -o "CASTCHECK.*" $D/audit/$N.txt | tr ',' '\n' | grep -v " 0.0" | sed "s/^/$N castcheck NOT ZERO: /" || echo "$N castcheck all 0.0"
if [ ! -s $D/$N.png ]; then
  t0=$(date +%s)
  env $E ${FL:+"$FL"} EXR=0 DENOISE=1 LAMP_OUT=$S/$N-raw.png python3.11 lamp_site.py $f --samples $SP --scale 0.5 > $S/$N.log 2>&1
  $FPY $ROOT/spinoffs/barkhorn/companions/launch/house_finish.py $S/$N-raw.png $D/$N.png > /dev/null
  echo "$N $(( $(date +%s) - t0 )) s"; date -u
fi
$FPY -c "from PIL import Image; Image.open('$D/$N.png').convert('RGB').resize((1600, 2000), Image.LANCZOS).save('$S/$N-full.png')"
cp $S/$N-full.png $S/$N.png; cd $M && $FPY meter.py corners $S/$N.png && $FPY meter.py body $mk $S/$N.png
[ $mk = ball.png ] && $FPY $D/base.py $S/$N.png || true
