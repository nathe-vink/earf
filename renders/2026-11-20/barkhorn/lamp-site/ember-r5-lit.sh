#!/bin/bash
# The two Ember LIT frames, round 5 (the coordinator 03:31, the critics on round 4): re-balanced after the softbox fix
# from one light-group pass each (quarter, 256 spp; launch/lit_balance.py), glows matched within 0.1 L* and the walls
# within about 1: Core studio 0.6 at -2.6 EV (glow L* 35.9, C* 77.0, R >= 250 on 0.5 % after a 3x3 median; walls TL 15.8,
# TR 24.9), Hemisphere studio 3.5 at -5.15 EV (36.0, 78.1, 0.0 %; 16.9, 24.7). Hemisphere's low sweep lamp
# (HOUSE_WALL_LL) off in LIT, so its brightest floor is the lamp's own pool. Otherwise as ember-r5.sh.
# (ember-r5.sh was made to skip LIT by 12-byte placeholders in house7/; a file under 1 KB counts as missing here, so
# this script overwrites them.)
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/house7; mkdir -p $D/audit
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/et7; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
big() { [ -f "$1" ] && [ "$(stat -c%s "$1")" -gt 1000 ]; }
one() { n=$1; f=$2; sp=$3; shift 3
  big $D/audit/$n.txt || { env "$@" HOUSE_BG=1.16 AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py $f > $S/$n.aud 2>&1 && \
      grep -E "^AUDIT|HIDDENCAST|CASTCHECK|  (in|out) " $S/$n.aud > $D/audit/$n.txt; }
  big $D/$n.png || { env "$@" HOUSE_BG=1.16 EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples $sp > $S/$n.log 2>&1 && \
      $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null && ls -la $D/$n.png && date -u; }
}
ALL="HOUSE_ROOM_TRANS=1 HOUSE_SWEEP_AO=0"
CORE="HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0 HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1"
DOME="HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_LIFT_RX=bg-left HOUSE_KEYFLAG=0,60,25,60,2"
one core-ember-lit       house-orb-red  512 HOUSE_STUDIO=0.6 HOUSE_EV=-2.6 $ALL $CORE "HOUSE_FLAGS=horn cutter"
one hemisphere-ember-lit house-dome-red 512 HOUSE_STUDIO=3.5 HOUSE_EV=-5.15 $ALL $DOME
