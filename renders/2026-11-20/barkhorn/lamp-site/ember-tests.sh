#!/bin/bash
# The Ember tests of the 15:13 notes (the coordinator), full size 1600 x 2000, the approved pours. The house ground with:
# solid softboxes and the room in reflections (launch/house_ground.py), the braided cord, Hemisphere's closed lip and no
# gaskets, the pendant hung free (HOUSE_LIFT 0.25 m, its lamps and the camera with it), Core off its dock (CORE_DOCK=0)
# with the base lifted 0.2 mm. OFF: the house ground as it stands. LIT: the studio taken down and the exposure set for
# the lamp (HOUSE_STUDIO, HOUSE_EV): Hemisphere 0.6 and -3 EV, Core 0.3 and -1 EV (quarter-size sweep: the lit body's
# median chroma 52 and 64). Each frame: its audit (studio lamps in frame, hidden objects, the emitters), the render, the
# Tropos finish.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/house2; mkdir -p $D/audit
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/et; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
one() { n=$1; f=$2; sp=$3; shift 3
  [ -s $D/audit/$n.txt ] || { env "$@" HOUSE_BG=1.16 AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py $f > $S/$n.aud 2>&1 && \
      grep -E "^AUDIT|HIDDENCAST|CASTCHECK|  (in|out) " $S/$n.aud > $D/audit/$n.txt; }
  [ -s $D/$n.png ] || { env "$@" HOUSE_BG=1.16 EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples $sp > /dev/null 2>&1 && \
      $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null && \
      python3 -c "import os,sys; print(sys.argv[1], os.path.getsize(sys.argv[1]))" $D/$n.png; }
}
DOME="HOUSE_S=0.2 HOUSE_LIFT=0.25"; CORE="HOUSE_S=0.19 CORE_DOCK=0"
one hemisphere-ember-off house-dome-red 128 LIGHTS_OFF=1 $DOME
one core-ember-off       house-orb-red  128 LIGHTS_OFF=1 $CORE
one hemisphere-ember-lit house-dome-red 512 HOUSE_STUDIO=0.6 HOUSE_EV=-3 $DOME
one core-ember-lit       house-orb-red  512 HOUSE_STUDIO=0.3 HOUSE_EV=-1 $CORE
echo DONE > $D/done.txt
