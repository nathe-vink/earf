#!/bin/bash
cd /home/user/earf/spinoffs/barkhorn/companions
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/match3
r() { [ -s "$1" ] && return 0; shift; "$@"; }
OFF=(PAPER='#9A9A9A' EXR=0 DENOISE=1 WB=5000 STUDIO_K=5000 WORLD='#BDA999' LIGHTS_OFF=1 STUDIO=12 EV=-1 KEY_STRIP=3.0,0.5 STUDIO_OFF=fill,kicker WORLD_STR=2.8 'KEY_POS=(0.0,-0.6,2.45)' 'KEY_AIM=(0,0,0.55)' 'DOMECAM=((0.09,-0.86,0.66),(0.0,0.0,0.55),70.0)')
LIT=(PAPER='#9A9A9A' EXR=0 WB=4000 STUDIO_K=4000 WORLD='#BDBDBD' DENOISE=1)
M="red:1.8:0 orange:9:1 amber:5:2 green:2.3:3 blue:6:4 violet:1.8:5"
for m in $M; do IFS=: read t L i <<< "$m"
  r $S/v-$t.png env "${OFF[@]}" TINT_LOAD_SET=$t:$L LAMP_OUT=$S/v-$t.png python3.11 lamp_site.py dome-$t --samples 128 --scale 0.5
  set -- $(python3 -c "c=2212-(7-$i)*290; print(round((c-156)/2400,4), round((c+156)/2400,4))")
  r $S/l-$t.png env "${LIT[@]}" TINT_LOAD_SET=$t:$L BORDER=$1,$2,0.0,1.0 LAMP_OUT=$S/l-$t.png python3.11 lamp_site.py lamps-domes --samples 256 --scale 1.0
  r $S/t-$t.png env "${LIT[@]}" BORDER=$1,$2,0.0,1.0 LAMP_OUT=$S/t-$t.png python3.11 lamp_site.py lamps-domes --samples 256 --scale 1.0
  r $S/iso-$t.txt sh -c "TINT_LOAD_SET=$t:$L BOUNCES=64 FRAME=dome-$t SPP=128 python3.11 launch/isphere.py 2>&1 | grep ISPHERE > $S/iso-$t.tmp; PAPER='#9A9A9A' TINT_LOAD_SET=$t:$L LUX_SPAN=1.4 LUXPROBE=$S/lux.exr python3.11 lamp_site.py dome-$t --samples 256 2>&1 | grep '^LUXPTS' >> $S/iso-$t.tmp; mv $S/iso-$t.tmp $S/iso-$t.txt"
done
r $S/aud-h.txt sh -c "env PAPER='#9A9A9A' WB=5000 STUDIO_K=5000 WORLD='#BDA999' LIGHTS_OFF=1 STUDIO=12 EV=-1 KEY_STRIP=3.0,0.5 STUDIO_OFF=fill,kicker WORLD_STR=2.8 TINT_LOAD_SET=red:1.8 AUDIT=1 MASK=$S/mask-h.png python3.11 lamp_site.py dome-red > $S/aud-h.txt 2>&1"
echo DONE > $S/p2-done.txt
