#!/bin/bash
# Two Hemisphere details again (the coordinator, 2026-11-11 22:24), after the Core finals:
#   ember-off  the direct camera, lamp off, daylight (5000 K, camera 5000 K): ONE overhead strip softbox (3.0 x 0.5 m,
#              KEY_STRIP, above and in front) and the fill off, so the shell carries one long soft highlight, not two ovals
#   ember-cap  NEW: lamp off, daylight, close on the stepped satin cap, the gland and the cloth cord; the strip above and
#              behind (the step tops catch it), the fill on for the step sides, its oval on the shell kept out of frame
#   ember-rim  replaces the old one (it showed the cap, lost in the dark): lamp on, from just below the rim plane, close
#              on the mouth's polished chamfered rim and the lit edge, EV -3.5
# 100 mm, 128 samples (the rim 192), denoised, 1600 x 2000. Audits and masks first; renders land in scratch and move into
# place together. Rerun until hemi-fix-done.txt.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/hemi-fix; mkdir -p $S/audit $S/masks
export PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0 DENOISE=1
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
OFF=(WB=5000 STUDIO_K=5000 LIGHTS_OFF=1 STUDIO=12 KEY_STRIP=3.0,0.5 'KEY_POS=(0.0,-0.5,2.2)' 'KEY_AIM=(0,0,0.55)' STUDIO_OFF=fill 'DOMECAM=((0.0,-1.04,0.55),(0.0,0.0,0.55),90.0)')
CAP=(WB=5000 STUDIO_K=5000 LIGHTS_OFF=1 STUDIO=8 KEY_STRIP=3.0,0.6 'KEY_POS=(0.0,0.9,1.5)' 'KEY_AIM=(0,0,0.62)' 'DOMECAM=((0.12,-0.60,0.73),(0.0,0.0,0.645),100.0)')
RIM=(WB=4000 STUDIO_K=4000 EV=-3.5 'DOMECAM=((0.15,-0.50,0.43),(0.0,-0.05,0.535),100.0)')
r $S/audit/hemisphere-ember-off.txt aud $S/audit/hemisphere-ember-off.txt env "${OFF[@]}" AUDIT=1 MASK=$S/masks/hemisphere-ember-off.png python3.11 lamp_site.py dome-red
r $S/audit/hemisphere-ember-cap.txt aud $S/audit/hemisphere-ember-cap.txt env "${CAP[@]}" AUDIT=1 MASK=$S/masks/hemisphere-ember-cap.png python3.11 lamp_site.py dome-red
r $S/audit/hemisphere-ember-rim.txt aud $S/audit/hemisphere-ember-rim.txt env "${RIM[@]}" AUDIT=1 MASK=$S/masks/hemisphere-ember-rim.png python3.11 lamp_site.py dome-red
r $S/hemisphere-ember-off.png env "${OFF[@]}" LAMP_OUT=$S/hemisphere-ember-off.png python3.11 lamp_site.py dome-red --samples 128 --scale 1.0 > /dev/null 2>&1
r $S/hemisphere-ember-cap.png env "${CAP[@]}" LAMP_OUT=$S/hemisphere-ember-cap.png python3.11 lamp_site.py dome-red --samples 128 --scale 1.0 > /dev/null 2>&1
r $S/hemisphere-ember-rim.png env "${RIM[@]}" FSTOP=4 'FOCUS=(0.0,-0.095,0.50)' LAMP_OUT=$S/hemisphere-ember-rim.png python3.11 lamp_site.py dome-red --samples 192 --scale 1.0 > /dev/null 2>&1
cp $S/hemisphere-ember-*.png $D/ && cp $S/audit/*.txt $D/audit/ && cp $S/masks/*.png $D/masks/ && echo DONE > $D/hemi-fix-done.txt
