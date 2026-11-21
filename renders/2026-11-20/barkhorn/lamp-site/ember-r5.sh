#!/bin/bash
# The four Ember frames, round 5 (the coordinator 03:12 and 03:23, after the code audit): Core's base 6 mm along its
# normals with the lip closed and both passes tinted (BASE_FIX, default), the studio lamps hidden from glossy and
# transmission rays so only their softbox faces show (HOUSE_LAMP_RAYVIS 0, default), the room's walls and ceiling seen
# through glass too (HOUSE_ROOM_TRANS=1), Core's floor ring in the sweep's colour and roughness without its contact
# term (HOUSE_FLOORCARD ALB -1). LIT: the sweep's painted contact shadow off (HOUSE_SWEEP_AO=0); OFF keeps it (the
# Tropos ground was matched with it). Quarter check of the base: flanks C* 26.2 / 21.4, 9.9 % below L* 20.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/house7; mkdir -p $D/audit
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/et7; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
one() { n=$1; f=$2; sp=$3; shift 3
  [ -s $D/audit/$n.txt ] || { env "$@" HOUSE_BG=1.16 AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py $f > $S/$n.aud 2>&1 && \
      grep -E "^AUDIT|HIDDENCAST|CASTCHECK|  (in|out) " $S/$n.aud > $D/audit/$n.txt; }
  [ -s $D/$n.png ] || { env "$@" HOUSE_BG=1.16 EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples $sp > $S/$n.log 2>&1 && \
      $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null && ls -la $D/$n.png && date -u; }
}
ALL="HOUSE_ROOM_TRANS=1"
CORE="HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1"
DOME="HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_LIFT_RX=bg-left HOUSE_KEYFLAG=0,60,25,60,2 HOUSE_WALL_LL=0.35 HOUSE_WALL_LL_SPREAD=30"
one core-ember-off       house-orb-red  128 LIGHTS_OFF=1 $ALL $CORE "HOUSE_FLAGS=horn cutter"
one hemisphere-ember-off house-dome-red 128 LIGHTS_OFF=1 $ALL $DOME
one core-ember-lit       house-orb-red  512 HOUSE_STUDIO=0.8 HOUSE_EV=-3.5 HOUSE_SWEEP_AO=0 $ALL $CORE "HOUSE_FLAGS=horn cutter"
one hemisphere-ember-lit house-dome-red 512 HOUSE_STUDIO=3 HOUSE_EV=-5 HOUSE_SWEEP_AO=0 $ALL $DOME
