#!/bin/bash
# The four Ember frames, round 5 as one set (2026-11-21, after the coordinator's two code audits), into house8/.
# Code defaults since 42c1604e: Core's base 6 mm along its normals, lip closed, both passes tinted, lip end and foot
# polished (BASE_FIX); Hemisphere's clear shell closed at its foot (CLEAR_CLOSE); the studio lamps hidden from glossy
# and transmission rays (HOUSE_LAMP_RAYVIS 0); the softbox faces never cut by the floor cutters (HOUSE_FACE_UNCUT); the
# room round the whole sweep (HOUSE_ROOM_BIG). Here: the walls seen through glass (HOUSE_ROOM_TRANS=1); Core's floor
# ring in the sweep's colour without its contact term (HOUSE_FLOORCARD ALB -1).
# OFF as ember-r5.sh (the sweep's painted contact shadow kept: the Tropos ground was matched with it).
# LIT as ember-r5-lit.sh (matched glows: Core studio 0.6 at -2.6 EV, Hemisphere 3.5 at -5.15; the sweep's contact shadow
# off; Hemisphere's low sweep lamp off).
# Replaces house7/ (its Core OFF, 35d059fe, predates the second audit) and the placeholder scheme of ember-r5*.sh.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/house8; mkdir -p $D/audit
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/et8; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
one() { n=$1; f=$2; sp=$3; shift 3
  [ -s $D/audit/$n.txt ] || { env "$@" HOUSE_BG=1.16 AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py $f > $S/$n.aud 2>&1 && \
      grep -E "^AUDIT|HIDDENCAST|CASTCHECK|  (in|out) " $S/$n.aud > $D/audit/$n.txt; }
  [ -s $D/$n.png ] || { env "$@" HOUSE_BG=1.16 EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples $sp > $S/$n.log 2>&1 && \
      $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null && ls -la $D/$n.png && date -u; }
}
ALL="HOUSE_ROOM_TRANS=1"
CORE="HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1"
DOME="HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_LIFT_RX=bg-left HOUSE_KEYFLAG=0,60,25,60,2"
one core-ember-off       house-orb-red  128 LIGHTS_OFF=1 $ALL $CORE "HOUSE_FLAGS=horn cutter"
one hemisphere-ember-off house-dome-red 128 LIGHTS_OFF=1 $ALL $DOME HOUSE_WALL_LL=0.35 HOUSE_WALL_LL_SPREAD=30
one core-ember-lit       house-orb-red  512 HOUSE_STUDIO=0.6 HOUSE_EV=-2.6 HOUSE_SWEEP_AO=0 $ALL $CORE "HOUSE_FLAGS=horn cutter"
one hemisphere-ember-lit house-dome-red 512 HOUSE_STUDIO=3.5 HOUSE_EV=-5.15 HOUSE_SWEEP_AO=0 $ALL $DOME
