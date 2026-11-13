#!/bin/bash
# hemisphere-ember-inuse.png, pass 2 (the coordinator, 2026-11-13 00:46): the same lamp, height, camera and exposure,
# nothing brightened; the room made real: a scanned oak top in four boards (Poly Haven oak_veneer_01, CC0), a printed
# open book, a stoneware cup with coffee, a chair (Poly Haven dining_chair_02, CC0) pushed in across the table, scanned
# plaster walls and oak-plank floor. The declared 6 W fill unchanged. Then the table's lux re-read (a grey card on it).
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-12/barkhorn/lamp-site/legible
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/legible2; mkdir -p $S
export WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0 DENOISE=1
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
r $S/audit.txt aud $S/audit.txt env ROOM_FILL=6 EV=-0.5 AUDIT=1 MASK=$S/mask.png python3.11 lamp_site.py inuse
r $S/inuse.png env ROOM_FILL=6 EV=-0.5 LAMP_OUT=$S/inuse.png python3.11 lamp_site.py inuse --samples 256 --scale 1.0 > /dev/null 2>&1
r $S/lux.txt aud $S/lux.txt env LUX_SPAN=1.4 LUXPROBE=$S/lux.exr python3.11 lamp_site.py inuse --samples 512
cp $S/inuse.png $D/hemisphere-ember-inuse.png && cp $S/audit.txt $D/audit/hemisphere-ember-inuse.txt && cp $S/mask*.png $D/masks/ 2>/dev/null; grep '^LUX' $S/lux.txt > $D/lux-inuse-pass2.txt && echo DONE > $D/legible2-done.txt
