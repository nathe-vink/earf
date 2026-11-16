#!/bin/bash
cd /home/user/earf/spinoffs/barkhorn/companions
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/match2
r() { [ -s "$1" ] && return 0; shift; "$@"; }
OFF=(PAPER='#9A9A9A' EXR=0 DENOISE=1 WB=5000 STUDIO_K=5000 WORLD='#BDA999' LIGHTS_OFF=1 STUDIO=12 EV=-1 KEY_STRIP=3.0,0.5 STUDIO_OFF=fill,kicker WORLD_STR=2.8 'KEY_POS=(0.0,-0.6,2.0)' 'KEY_AIM=(0,0,0.10)' 'ORBCAM=((0.09,-0.86,0.21),(0.0,0.0,0.10),70.0)')
LIT=(PAPER='#9A9A9A' EXR=0 WB=4000 STUDIO_K=4000 WORLD='#BDBDBD' STUDIO=0.5 EV=-1)
M="red:0.33:0 orange:1.6:1 amber:1.35:2 green:0.6:3 blue:1.6:4 violet:0.55:5 black:0.6:7"
for m in $M; do IFS=: read t L i <<< "$m"
  r $S/v-$t.png env "${OFF[@]}" TINT_LOAD_SET=$t:$L LAMP_OUT=$S/v-$t.png python3.11 lamp_site.py orb-$t --samples 128 --scale 0.5
  x0=$(python3 -c "c=1200+($i-3.5)*261; print(round((c-156)/2400,4), round((c+156)/2400,4))")
  set -- $x0
  r $S/l-$t.png env "${LIT[@]}" TINT_LOAD_SET=$t:$L BORDER=$1,$2,0.0,1.0 LAMP_OUT=$S/l-$t.png python3.11 lamp_site.py lamps-orbs --samples 256 --scale 1.0
  r $S/iso-$t.txt sh -c "TINT_LOAD_SET=$t:$L FRAME=orb-$t SPP=256 python3.11 launch/isphere.py 2>&1 | grep ISPHERE > $S/iso-$t.txt"
done
# Core lit today, corrected method (the approved rows were rendered before the fix; the glass is the same within 2)
for m in red:0 orange:1 amber:2 green:3 blue:4 violet:5 ice:6 black:7; do t=${m%%:*}; i=${m##*:}
  x0=$(python3 -c "c=1200+($i-3.5)*261; print(round((c-156)/2400,4), round((c+156)/2400,4))"); set -- $x0
  r $S/t-$t.png env "${LIT[@]}" BORDER=$1,$2,0.0,1.0 LAMP_OUT=$S/t-$t.png python3.11 lamp_site.py lamps-orbs --samples 256 --scale 1.0
done
r $S/aud-c.txt sh -c "env PAPER='#9A9A9A' WB=5000 STUDIO_K=5000 WORLD='#BDA999' LIGHTS_OFF=1 STUDIO=12 EV=-1 KEY_STRIP=3.0,0.5 STUDIO_OFF=fill,kicker WORLD_STR=2.8 TINT_LOAD_SET=red:0.33 AUDIT=1 MASK=$S/mask-c.png python3.11 lamp_site.py orb-red > $S/aud-c.txt 2>&1"
echo DONE > $S/p2-done.txt
