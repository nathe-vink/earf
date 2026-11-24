#!/bin/bash
# Pass v2 (2026-11-24, the coordinator after the critics' two rounds and the owner's answers): one tint's group, full size
# (1600 x 2000), the owner's pours (lamp_site.py's defaults), nothing hidden from the camera in frame.
#   renders/2026-11-24/barkhorn/lamp-site/pass2/pass2.sh TINT GROUP      TINT: red orange amber green blue violet ice black
#   GROUP A pendant OFF, B Core OFF (128 spp); C pendant LIT, D Core LIT (512 spp; one studio and exposure for every tint)
# The grounds: the pendant's is round 2's p6 (wall_left lifted with the camera, the room fitted round every lamp, the key
# re-aimed and +8 %, no key flag); the Core's is c1 (no floor ring, no cutters). The LIT frames: the softboxes SEEN in
# reflections (their real edges), the colour-only denoise; the Core LIT is LIT-g (the owner: "New"), its spot's two cards.
# Switches, until the owner picks (the defaults are today's):
#   PASS_WB=5600|4000   the camera's white balance; 4000 re-gels the studio (HOUSE_GEL 5600:3900) so the ground stays
#   PASS_TOP=A|B        Hemisphere's top in even tiers (crystal.py TOP_TIERS); unset, today's
#   PASS_CARDS=W        the Core LIT spot's two cards' width in m (default 0.025; LIT-g had 0.05 and 0.06)
# THE GATE: each frame's audit runs first; any hidden object in frame (CASTCHECK above 0.0) stops it before the render.
# PASS_AUDIT_ONLY=1: the audit and the gate only, no render.
# Writes pass2/TINT/{hemisphere,core}-TINT-{off,lit}.png and audit/; prints the meters. Skips what exists.
# THE RE-RENDER LIST (v6, the v5 check's (15)): from 2026-11-10 to the v5 fix, the collar's white test read 0.080 against
# mm coordinates, so every Hemisphere picture drew the collar's painted faces black, including faces that take the LEDs'
# light. Every Hemisphere frame of this pass is re-rendered, the LIT ones (GROUP C) included, and so is the live cutaway
# 'How it lights' (renders/2026-11-12/barkhorn/lamp-site/legible/hemisphere-ember-cutaway.png). The white is limited to the
# painted faces in every render now (lamp_site.py), with or without HEMI_COLLAR_CAP.
set -e
T=${1:?tint}; G=${2:?group}
ROOT=$(cd "$(dirname "$0")/../../../../.." && pwd)
D=$ROOT/renders/2026-11-24/barkhorn/lamp-site/pass2/$T; mkdir -p $D/audit
S=${TMPDIR:-/tmp}/pass2-$T-$G; mkdir -p $S
FPY=$ROOT/.venv-fab/bin/python; M=$ROOT/renders/2026-11-20/barkhorn/lamp-site/meter
cd $ROOT/spinoffs/barkhorn/companions
HG="HEMI_COLLAR_CAP=1 HOUSE_ROOM_TRANS=1 HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_LIFT_RX=bg-left,wall_left HOUSE_ROOM_FIT=1 HOUSE_BG=1.16 HOUSE_AIM=key:-0.7,0,0.1;wall_left:0,0,-0.5"
CG="HOUSE_ROOM_TRANS=1 HOUSE_S=0.19 CORE_DOCK=0 HOUSE_ROOM_FIT=1 HOUSE_BG=1.16"
W1=${PASS_CARDS:-0.025}; W2=${PASS_CARDS:-0.025}   # (2.5 cm, the coordinator 2026-11-24 05:11: tests/r2/cards-sheet.jpg)
SPOT="GUIDE_ORB=1 HOUSE_BOUNCE=0,0,0,0,0.19,-0.405,0.03,18,8.5,0.015 HOUSE_BOUNCE_BLEND=0.9 HOUSE_BOUNCE_COLOR=FFF4E8 HOUSE_BOUNCE_CUT=0.01,0.06,0.0262,$W1 HOUSE_BOUNCE_SOFT=0.003 HOUSE_BOUNCE_TOP=0.01,0.10,0.0335,$W2"
LIT="HOUSE_SOFTBOX_SEEN=1 DENOISE_PASSES=RGB HOUSE_SWEEP_AO=0"
case $G in
  A) n=hemisphere-$T-off; f=house-dome-$T; sp=128; mk=shade.png
     E="LIGHTS_OFF=1 $HG HOUSE_LAMP_K=wall_left:1.2,key:1.08 HOUSE_WALL_LL=0.35 HOUSE_WALL_LL_SPREAD=30" ;;
  B) n=core-$T-off; f=house-orb-$T; sp=128; mk=ball.png; E="LIGHTS_OFF=1 $CG" ;;
  C) n=hemisphere-$T-lit; f=house-dome-$T; sp=512; mk=shade.png
     E="$LIT HOUSE_STUDIO=3.5 HOUSE_EV=-5.15 $HG HOUSE_LAMP_K=wall_left:1.2,key:1.08" ;;
  D) n=core-$T-lit; f=house-orb-$T; sp=512; mk=ball.png
     E="$LIT $SPOT HOUSE_LAMP_K=key:0 HOUSE_STUDIO=0.714 HOUSE_EV=-2.85 $CG" ;;
  *) echo "group A B C D"; exit 1 ;;
esac
[ "${PASS_WB:-5600}" = 4000 ] && E="$E HOUSE_WB=4000 HOUSE_GEL=5600:3900"
[ -n "$PASS_TOP" ] && E="$E HEMI_TOP=$PASS_TOP"
A=$D/audit/$n${PASS_TOP:+-top$PASS_TOP}${PASS_WB:+-wb$PASS_WB}.txt   # (one audit file per set of switches)
if [ ! -s $D/$n.png ]; then          # (the audit always runs before a render, with this run's switches)
  env $E AUDIT=1 MASK=$S/m.png python3.11 lamp_site.py $f > $S/$n.aud 2>&1
  echo "SWITCHES $E" > $A
  grep -E "^AUDIT|HIDDENCAST|CASTCHECK|^   (IN FRAME|in|out|practical) |^RAYVIS|^LINK|LAMP_MOVE|LAMPK|ROOM_FIT|HOUSE_WB|HOUSE_GEL|CORE_ABS|BOUNCE" $S/$n.aud >> $A
fi
nz_=$(grep -o "CASTCHECK.*" $A | tr ',' '\n' | grep -v " 0.0" || true)
if [ -n "$nz_" ] || ! grep -q CASTCHECK $A; then
  echo "GATE: $n has a hidden object in frame (or no CASTCHECK); not rendered:"; echo "${nz_:-no CASTCHECK line}"; exit 3
fi
echo "$n castcheck all 0.0"
[ "${PASS_AUDIT_ONLY:-0}" = 1 ] && exit 0
if [ ! -s $D/$n.png ]; then
  t0=$(date +%s)
  env $E EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples $sp > $S/$n.log 2>&1
  $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null
  grep -h "CORE_ABS" $S/$n.log || true; echo "$n $(( $(date +%s) - t0 )) s"; date -u
fi
cd $M && $FPY meter.py corners $D/$n.png && $FPY meter.py body $mk $D/$n.png && $FPY meter.py glowy $mk $D/$n.png
