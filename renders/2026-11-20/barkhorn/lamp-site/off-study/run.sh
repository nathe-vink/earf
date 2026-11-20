#!/bin/bash
# The off-colour study (the coordinator, 14:57): Hemisphere and Core OFF in the house light, all eight tints, quarter
# size, 64 spp; a mask of the shade's tint shell and of the ball for each
cd /home/user/earf/spinoffs/barkhorn/companions
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/study
FPY=/home/user/earf/.venv-fab/bin/python
r() { n=$1; f=$2; only=$3; shift 3
  [ -s $S/$n-mask.png ] || env "$@" PRODUCT_MASK=$S/$n-mask.png MASK_ONLY=$only python3.11 lamp_site.py $f --scale 0.25 > $S/$n-mask.log 2>&1
  [ -s $S/$n.png ] && return
  env "$@" HOUSE_BG=1.16 EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples ${SPP:-64} --scale 0.25 > $S/$n.log 2>&1 && \
  $FPY launch/house_finish.py $S/$n-raw.png $S/$n.png > /dev/null && echo $n || { echo FAIL $n; tail -3 $S/$n.log; }
}
for k in ${TINTS:-red orange amber green blue violet ice black}; do
  r dome-$k house-dome-$k tint- LIGHTS_OFF=1 HOUSE_S=0.2 $EXTRA_DOME
  r orb-$k  house-orb-$k  ball- LIGHTS_OFF=1 HOUSE_S=0.19 $EXTRA_ORB
done
echo STUDYDONE
