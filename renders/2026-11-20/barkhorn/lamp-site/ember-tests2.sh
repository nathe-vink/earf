#!/bin/bash
# The Ember tests again after the critics of 19:56 (ember-tests2.sh). Was: the Ember tests of the 15:13 notes (the coordinator), full size 1600 x 2000, the approved pours. The house ground with:
# solid softboxes and the room in reflections (launch/house_ground.py), the braided cord, Hemisphere's closed lip and no
# gaskets, the pendant hung free (HOUSE_LIFT 0.25 m, its lamps and the camera with it), Core off its dock (CORE_DOCK=0)
# with the base lifted 0.2 mm. OFF: the house ground as it stands. LIT: the studio taken down and the exposure set for
# the lamp (HOUSE_STUDIO, HOUSE_EV): Hemisphere 0.6 and -3 EV, Core 0.3 and -1 EV (quarter-size sweep: the lit body's
# median chroma 52 and 64). Each frame: its audit (studio lamps in frame, hidden objects, the emitters), the render, the
# Tropos finish.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/house4; mkdir -p $D/audit
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/et4; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
one() { n=$1; f=$2; sp=$3; shift 3
  [ -s $D/audit/$n.txt ] || { env "$@" HOUSE_BG=1.16 AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py $f > $S/$n.aud 2>&1 && \
      grep -E "^AUDIT|HIDDENCAST|CASTCHECK|  (in|out) " $S/$n.aud > $D/audit/$n.txt; }
  [ -s $D/$n.png ] || { env "$@" HOUSE_BG=1.16 EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples $sp > /dev/null 2>&1 && \
      $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null && \
      python3 -c "import os,sys; print(sys.argv[1], os.path.getsize(sys.argv[1]))" $D/$n.png; }
}
# 19:56: the Core's floor cutters (the Tropos horn cutter on the horn, a second 1.0 m right on the fill, both shading the
# floor alone through light-linked copies: LL 92.8 and BR 89.0 against the Tropos's 94.0 and 87.4), 768 segments on
# the base, the black cloth cord; LIT balanced from one light-group render (launch/lit_balance.py): the glow under
# R 248 on most of it, Ember's hue (h 39), the two lamps matched (Core L* 44.6 C 89 h 40, pendant 46.2 C 88 h 39) and
# their walls alike (L* 13-18, h 76-81): Core studio 0.8 at -3.5 EV, Hemisphere studio 3 at -5 EV.
CORE="HOUSE_S=0.19 CORE_DOCK=0 HOUSE_CUT2=fill,1.0"
# The pendant (the coordinator 20:28, option a): a flag on the key's floor copy (bearings 0-60, 25-60 degrees down,
# 2 m out at full scale) for the bottom right, and a low sweep lamp at the left (0.35 W/m2, 30 degree spread) for the
# lower left: quarter-size corners LL 96.5, BR 88.3 against the Tropos's 94.0 and 87.4; the shade's light and shadow
# untouched (both on the sweep alone), nothing in reflections or through glass
DOME="HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_LIFT_RX=bg-left HOUSE_KEYFLAG=0,60,25,60,2 HOUSE_WALL_LL=0.35 HOUSE_WALL_LL_SPREAD=30"
one core-ember-off       house-orb-red  128 LIGHTS_OFF=1 $CORE "HOUSE_FLAGS=horn cutter"
one core-ember-lit       house-orb-red  512 HOUSE_STUDIO=0.8 HOUSE_EV=-3.5 $CORE "HOUSE_FLAGS=horn cutter"
[ -n "$CORE_ONLY" ] && exit 0
one hemisphere-ember-off house-dome-red 128 LIGHTS_OFF=1 $DOME
one hemisphere-ember-lit house-dome-red 512 HOUSE_STUDIO=3 HOUSE_EV=-5 $DOME
echo DONE > $D/done.txt
