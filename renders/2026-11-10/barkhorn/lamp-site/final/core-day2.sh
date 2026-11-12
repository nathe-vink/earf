#!/bin/bash
# core-row-day.png again (the coordinator, 2026-11-11 23:58): the key and fill made two round dots on each ball, pairs of
# eyes across the row. Now ONE overhead strip softbox (KEY_STRIP 3.0 x 0.5 m, above and in front, aimed at the row) and
# the fill off, as for Ember off, so each ball carries one soft arc; studio 12 to hold the frame's brightness. Lamps
# off, daylight (5000 K, the camera at 5000 K), the finals' camera, full size, 256 samples. Same name.
# Pass 2 (the coordinator, 2026-11-12 00:47: with the fill off the row went dark and the bases near-black): the world
# lifted (WORLD_STR 2.8, tinted #BDA999 so the paper stays neutral at 5000 K), which lights evenly and leaves no second
# highlight; the frame back to the first version's brightness (paper 0.44 against 0.45).
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/core-day3; mkdir -p $S/audit $S/masks
export PAPER='#9A9A9A' WORLD='#BDA999' EXR=0 ORBCAM='((0.09,-0.86,0.21),(0.0,0.0,0.10),70.0)'
DAY=(WB=5000 STUDIO_K=5000 LIGHTS_OFF=1 STUDIO=12 EV=-1 KEY_STRIP=3.0,0.5 'KEY_POS=(0.0,-0.6,2.0)' 'KEY_AIM=(0,0,0.10)' STUDIO_OFF=fill WORLD_STR=2.8)
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
r $S/audit/core-row-day.txt aud $S/audit/core-row-day.txt env "${DAY[@]}" AUDIT=1 MASK=$S/masks/core-row-day.png python3.11 lamp_site.py lamps-orbs
r $S/core-row-day.png env "${DAY[@]}" LAMP_OUT=$S/core-row-day.png python3.11 lamp_site.py lamps-orbs --samples 256 --scale 1.0 > /dev/null 2>&1
cp $S/core-row-day.png $D/ && cp $S/audit/core-row-day.txt $D/audit/ && cp $S/masks/*.png $D/masks/ && echo DONE > $D/core-day3-done.txt
