#!/bin/bash
# The coordinator, 19:43: Hemisphere and Core OFF in Fog (ice) and Smoke (black) at 800 x 1000 (--scale 0.5), the
# approved pours and the new rig of ember-tests.sh (solid softboxes, the room in reflections, the braid, the closed lip,
# no gaskets, the pendant hung free, Core off its dock, the base lifted, 768 segments on the base: REV_SEG). Tests, not
# finals. Each frame: its audit, the render, the Tropos finish.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/house3; mkdir -p $D/audit
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/fs; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
one() { n=$1; f=$2; sp=$3; shift 3
  [ -s $D/audit/$n.txt ] || { env "$@" HOUSE_BG=1.16 AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py $f --scale 0.5 > $S/$n.aud 2>&1 && \
      grep -E "^AUDIT|HIDDENCAST|CASTCHECK|  (in|out) " $S/$n.aud > $D/audit/$n.txt; }
  [ -s $D/$n.png ] || { env "$@" HOUSE_BG=1.16 EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples $sp --scale 0.5 > /dev/null 2>&1 && \
      $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null && \
      python3 -c "import os,sys; print(sys.argv[1], os.path.getsize(sys.argv[1]))" $D/$n.png; }
}
DOME="HOUSE_S=0.2 HOUSE_LIFT=0.25"; CORE="HOUSE_S=0.19 CORE_DOCK=0"
one hemisphere-fog-off   house-dome-ice   128 LIGHTS_OFF=1 $DOME
one core-fog-off         house-orb-ice    128 LIGHTS_OFF=1 $CORE
one hemisphere-smoke-off house-dome-black 128 LIGHTS_OFF=1 $DOME
one core-smoke-off       house-orb-black  128 LIGHTS_OFF=1 $CORE
echo DONE > $S/done.txt
