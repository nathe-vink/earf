#!/bin/bash
# The pour CHECK SET (2026-11-21, the coordinator after the eight-tint critics): per tint, the pendant and Core at
# candidate loadings, OFF and LIT, half size (800 x 1000), on the house ground, for the owner.
#   renders/2026-11-20/barkhorn/lamp-site/checkset/checkset.sh TINT [SET]   (red orange amber green blue violet black)
# SET (optional, round 2): the frames to render instead of the tint's default list, e.g. "hemi:lit:0.7 core:off:2.0"
# Loadings are given directly: HEMI_LOAD (the 3 mm shade, a multiple of the base pour; lamp_site.py TINT_LOAD) and
# CORE_LOAD (the 6 mm ball and its base, absolute: 0.5 = the chart figure; today's value is 0.5 x CORE_TINT_LOAD).
# OFF exactly as row-off/ (Ember round 5 OFF); LIT exactly as round 6 (ember-r6-hemi.sh, ember-r6-core.sh), the same
# studio and exposure for every pour and tint, so a lighter pour shows what it does to the glow.
# Writes checkset/TINT/{hemi,core}-{off,lit}-L<load>.png. Skips what exists.
set -e
T=${1:?tint key}
ROOT=$(cd "$(dirname "$0")/../../../../.." && pwd)
D=$ROOT/renders/2026-11-20/barkhorn/lamp-site/checkset/$T; mkdir -p $D
S=${TMPDIR:-/tmp}/checkset-$T; mkdir -p $S
FPY=$ROOT/.venv-fab/bin/python
cd $ROOT/spinoffs/barkhorn/companions
# per tint: today's pendant / Core, then the frames to render as LAMP:STATE:LOAD (LOAD the HEMI_LOAD or CORE_LOAD)
case $T in
  red)    SET="hemi:off:1.0 hemi:off:0.7 core:off:0.75 hemi:lit:1.0 core:lit:0.75" ;;                            # today hemi 1.8, core 0.5 (lit: round 6)
  blue)   SET="hemi:off:3.0 hemi:off:2.1 core:off:2.25 hemi:lit:6.0 core:lit:1.5 hemi:lit:3.0 core:lit:2.25" ;;  # today hemi 6, core 1.5
  violet) SET="hemi:off:1.0 hemi:off:0.7 core:off:0.75 hemi:lit:1.8 core:lit:0.5 hemi:lit:1.0 core:lit:0.75" ;;  # today hemi 1.8, core 0.5
  amber)  SET="hemi:off:3.0 hemi:off:2.1 core:off:1.0 hemi:lit:5.0 core:lit:1.5 hemi:lit:3.0 core:lit:1.0" ;;    # today hemi 5, core 1.5
  green)  SET="hemi:off:0.7 hemi:lit:1.0 core:lit:0.3 hemi:lit:0.7" ;;                                         # today hemi 1.0, core 0.3
  orange) SET="hemi:off:2.1 core:off:0.8 hemi:lit:3.0 core:lit:1.5 hemi:lit:2.1 core:lit:0.8" ;;                 # today hemi 3, core 1.5; 0.8 the 16 Nov 1.6x
  black)  SET="core:off:0.45 core:off:0.6 hemi:lit:1.2 core:lit:0.3 core:lit:0.45" ;;                          # today hemi 1.2, core 0.3
  *) echo "unknown tint $T"; exit 1 ;;
esac
[ -n "${2:-}" ] && SET="$2"   # round 2: an explicit list replaces the default
echo "SET: $SET"
HOFF="LIGHTS_OFF=1 HOUSE_ROOM_TRANS=1 HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_LIFT_RX=bg-left HOUSE_KEYFLAG=0,60,25,60,2 HOUSE_WALL_LL=0.35 HOUSE_WALL_LL_SPREAD=30 HOUSE_BG=1.16"
COFF="LIGHTS_OFF=1 HOUSE_ROOM_TRANS=1 HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1 HOUSE_BG=1.16"
HLIT="HOUSE_SOFTBOX_SEEN=0 DENOISE_PASSES=RGB HOUSE_STUDIO=3.5 HOUSE_EV=-5.15 HOUSE_SWEEP_AO=0 HOUSE_ROOM_TRANS=1 HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_LIFT_RX=bg-left HOUSE_KEYFLAG=0,60,25,60,2 HOUSE_BG=1.16"
CLIT="HOUSE_LAMP_K=key:0 HOUSE_SOFTBOX_SEEN=0 DENOISE_PASSES=RGB HOUSE_STUDIO=0.714 HOUSE_EV=-2.85 HOUSE_SWEEP_AO=0 HOUSE_ROOM_TRANS=1 HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1 HOUSE_BG=1.16"
M=$ROOT/renders/2026-11-20/barkhorn/lamp-site/meter
for it in $SET; do
  IFS=: read lamp state ld <<< "$it"
  n=$lamp-$state-L$ld; [ -s $D/$n.png ] && { echo "have $n"; continue; }
  if [ $lamp = hemi ]; then f=house-dome-$T; LV="HEMI_LOAD=$ld"; mk=shade.png; [ $state = off ] && E=$HOFF || E=$HLIT
  else f=house-orb-$T; LV="CORE_LOAD=$ld"; mk=ball.png; [ $state = off ] && E=$COFF || E=$CLIT; fi
  [ $state = off ] && sp=128 || sp=256
  FL=""; [ $lamp = core ] && FL="HOUSE_FLAGS=horn cutter"
  t0=$(date +%s)
  env $E $LV ${FL:+"$FL"} EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples $sp --scale 0.5 > $S/$n.log 2>&1
  $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null
  echo "$n $(( $(date +%s) - t0 )) s"; date -u
  ( cd $M && $FPY meter.py corners $D/$n.png && $FPY meter.py body $mk $D/$n.png && { [ $state = lit ] && $FPY meter.py pair $mk $D/$n.png || true; } )
done
