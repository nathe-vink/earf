#!/bin/bash
# Making Hemisphere's light legible (the owner, 2026-11-12: "I'm having trouble understanding how the hemisphere lighting
# works based on the renders"; the coordinator's brief 23:50). Ember, the approved asset (lamp_site.py's ring engine:
# the 24 LED faces the only emitters in the lamp).
#   A  hemisphere-ember-cutaway.png, 2000 x 2000: the lit lamp cut in half on the vertical plane through its axis, the
#      near half removed (lamp_site.section(): the CAD solids cut and capped, the shade's three layers capped between
#      their radii, the 11 LEDs of the removed half removed with it), three-quarter, the finals' studio (paper #9A9A9A,
#      studio 1 at 4000 K, the camera at 4000 K, EV -2); five labels added after (label.py)
#   B  hemisphere-ember-inuse.png, 2400 x 1600: the rim 0.5 m over a pale oak table in a dim room, from a seat; the lamp
#      the only light but a declared 6 W ceiling panel (ROOM_FILL) for the walls; the camera at 4000 K, EV -0.5
# 192 / 256 samples, denoised. Audits first. Rerun until legible-done.txt.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-12/barkhorn/lamp-site/legible; mkdir -p $D/audit $D/masks
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/legible-final; mkdir -p $S
export WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0 DENOISE=1
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
r $D/audit/hemisphere-ember-cutaway.txt aud $D/audit/hemisphere-ember-cutaway.txt env AUDIT=1 MASK=$D/masks/hemisphere-ember-cutaway.png python3.11 lamp_site.py cutaway
r $D/audit/hemisphere-ember-inuse.txt aud $D/audit/hemisphere-ember-inuse.txt env ROOM_FILL=6 EV=-0.5 AUDIT=1 MASK=$D/masks/hemisphere-ember-inuse.png python3.11 lamp_site.py inuse
r $S/cutaway-raw.png env LAMP_OUT=$S/cutaway-raw.png python3.11 lamp_site.py cutaway --samples 192 --scale 1.0 > $S/cutaway.log 2>&1
r $D/hemisphere-ember-inuse.png env ROOM_FILL=6 EV=-0.5 LAMP_OUT=$D/hemisphere-ember-inuse.png python3.11 lamp_site.py inuse --samples 256 --scale 1.0 > /dev/null 2>&1
python3 $D/label.py $S/cutaway-raw.png $S/cutaway.log $D/hemisphere-ember-cutaway.png && echo DONE > $D/legible-done.txt
