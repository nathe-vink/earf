#!/bin/bash
# Core's finals again (the coordinator, 2026-11-11, after the Hemisphere views): core-<tint>.png x8 and core-row.png at
# their names with the own-colour base B (lamp_site's default since 3e38954b: the whole base in its own colour, R12 lip),
# lamp on, run.sh's settings (studio 0.5, EV -1, 4000 K, paper #9A9A9A, ORBCAM, full size, 256 samples). Plus
# core-row-day.png: the row with the lamps off in a daylight studio (5000 K, the camera at 5000 K, studio 3). Renders
# land in scratch and move into place when all are done, so the old frames stay until the set is whole. Rerun until
# core-final-done.txt.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/core-final; mkdir -p $S/audit $S/masks
export WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0
export ORBCAM='((0.09,-0.86,0.21),(0.0,0.0,0.10),70.0)'
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
T="red:ember orange:dust amber:acid green:poison blue:ice violet:haze ice:fog black:smoke"
DAY="WB=5000 STUDIO_K=5000 LIGHTS_OFF=1 STUDIO=3 EV=-1"
for kv in $T; do k=${kv%%:*}; n=${kv##*:}
  r $S/audit/core-$n.txt aud $S/audit/core-$n.txt env STUDIO=0.5 EV=-1 AUDIT=1 MASK=$S/masks/core-$n.png python3.11 lamp_site.py orb-$k
done
r $S/audit/core-row.txt aud $S/audit/core-row.txt env STUDIO=0.5 EV=-1 AUDIT=1 MASK=$S/masks/core-row.png python3.11 lamp_site.py lamps-orbs
r $S/audit/core-row-day.txt aud $S/audit/core-row-day.txt env $DAY AUDIT=1 MASK=$S/masks/core-row-day.png python3.11 lamp_site.py lamps-orbs
for kv in $T; do k=${kv%%:*}; n=${kv##*:}
  r $S/core-$n.png env STUDIO=0.5 EV=-1 LAMP_OUT=$S/core-$n.png python3.11 lamp_site.py orb-$k --samples 256 --scale 1.0 > /dev/null 2>&1
done
r $S/core-row.png env STUDIO=0.5 EV=-1 LAMP_OUT=$S/core-row.png python3.11 lamp_site.py lamps-orbs --samples 256 --scale 1.0 > /dev/null 2>&1
r $S/core-row-day.png env $DAY LAMP_OUT=$S/core-row-day.png python3.11 lamp_site.py lamps-orbs --samples 256 --scale 1.0 > /dev/null 2>&1
cp $S/core-*.png $D/ && cp $S/audit/*.txt $D/audit/ && cp $S/masks/*.png $D/masks/ && echo DONE > $D/core-final-done.txt
