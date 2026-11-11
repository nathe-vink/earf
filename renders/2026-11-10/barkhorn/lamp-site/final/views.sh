#!/bin/bash
# More Hemisphere views (the owner, 2026-11-11 15:25): the final set's recipe (the LED per tint, the shell per tint, the
# paper #9A9A9A, studio and camera at 4000 K, studio 1, EV -2, the LED faces the only emitters), 1600 x 2000, the
# denoiser on the beauty (DENOISE=1), 128 samples (the rim detail 192).
#   -direct  level with the middle of the shade, square on, 90 mm, the shade about 60 % of the width
#   -under   35 deg below the rim's plane, 30 deg round, 60 mm, looking up into the shade
#   ember-off  the -direct camera, the lamp off, a daylight studio (5000 K, the camera at 5000 K, the studio x4)
#   cluster  all eight at different heights, 2000 x 2000; the row again at its name
#   ember-rim  close on the rim and the black cap, 85 mm at f/2.8, focused on the cap
# Audits and masks first. Skips what is done; rerun until views-done.txt.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-10/barkhorn/lamp-site/final
export WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0 DENOISE=1
DIR='((0.0,-1.04,0.55),(0.0,0.0,0.55),90.0)'
UND='((0.287,-0.496,0.10),(0.0,0.0,0.52),60.0)'
RIM='((0.17,-0.46,0.70),(0.0,0.0,0.565),85.0)'
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
T="red:ember orange:dust amber:acid green:poison blue:ice violet:haze ice:fog black:smoke"
# photometry with the Ø95 disc and the closed carrier (the coordinator, 16:18): Hemisphere's lumens below/above the rim
# plane and the table's lux 0.5 m down, per tint; Core's lines carried over from the set's photometry
P=$D/photometry-hemisphere.txt
if [ ! -s $P ]; then
  for kv in $T; do k=${kv%%:*}; n=${kv##*:}
    echo "hemisphere $n: $(BOUNCES=64 FRAME=dome-$k SPP=128 python3.11 launch/isphere.py 2>&1 | grep ISPHERE)"
    echo "hemisphere $n: $(LUXPROBE=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/lux-$n.exr python3.11 lamp_site.py dome-$k --samples 256 2>&1 | grep LUX)"
  done > $P.tmp && mv $P.tmp $P
  { grep '^core' $D/photometry.txt; cat $P; } > $D/photometry.txt.new && mv $D/photometry.txt.new $D/photometry.txt
fi
for kv in $T; do k=${kv%%:*}; n=${kv##*:}
  r $D/audit/hemisphere-$n-direct.txt aud $D/audit/hemisphere-$n-direct.txt env DOMECAM="$DIR" AUDIT=1 MASK=$D/masks/hemisphere-$n-direct.png python3.11 lamp_site.py dome-$k
  r $D/audit/hemisphere-$n-under.txt aud $D/audit/hemisphere-$n-under.txt env DOMECAM="$UND" AUDIT=1 MASK=$D/masks/hemisphere-$n-under.png python3.11 lamp_site.py dome-$k
done
r $D/audit/hemisphere-ember-off.txt aud $D/audit/hemisphere-ember-off.txt env LIGHTS_OFF=1 STUDIO=4 STUDIO_K=5000 WB=5000 DOMECAM="$DIR" AUDIT=1 MASK=$D/masks/hemisphere-ember-off.png python3.11 lamp_site.py dome-red
r $D/audit/hemisphere-ember-rim.txt aud $D/audit/hemisphere-ember-rim.txt env DOMECAM="$RIM" AUDIT=1 MASK=$D/masks/hemisphere-ember-rim.png python3.11 lamp_site.py dome-red
for kv in $T; do k=${kv%%:*}; n=${kv##*:}
  r $D/hemisphere-$n-direct.png env DOMECAM="$DIR" LAMP_OUT=$D/hemisphere-$n-direct.png python3.11 lamp_site.py dome-$k --samples 128 --scale 1.0 > /dev/null 2>&1
done
for kv in $T; do k=${kv%%:*}; n=${kv##*:}
  r $D/hemisphere-$n-under.png env DOMECAM="$UND" LAMP_OUT=$D/hemisphere-$n-under.png python3.11 lamp_site.py dome-$k --samples 128 --scale 1.0 > /dev/null 2>&1
done
r $D/hemisphere-ember-off.png env LIGHTS_OFF=1 STUDIO=4 STUDIO_K=5000 WB=5000 DOMECAM="$DIR" LAMP_OUT=$D/hemisphere-ember-off.png python3.11 lamp_site.py dome-red --samples 128 --scale 1.0 > /dev/null 2>&1
r $D/hemisphere-ember-rim.png env FSTOP=2.8 FOCUS='(0.0,-0.045,0.60)' DOMECAM="$RIM" LAMP_OUT=$D/hemisphere-ember-rim.png python3.11 lamp_site.py dome-red --samples 192 --scale 1.0 > /dev/null 2>&1
# the cluster (the owner, 2026-11-11 16:25): all eight at different heights, 2000 x 2000
r $D/audit/hemisphere-cluster.txt aud $D/audit/hemisphere-cluster.txt env AUDIT=1 MASK=$D/masks/hemisphere-cluster.png python3.11 lamp_site.py cluster
r $D/hemisphere-cluster.png env LAMP_OUT=$D/hemisphere-cluster.png python3.11 lamp_site.py cluster --samples 128 --scale 1.0 > /dev/null 2>&1
# the row again, at its name, with the Ø95 disc (the coordinator, 16:18)
r $D/hemisphere-row.png env LAMP_OUT=$D/hemisphere-row.png python3.11 lamp_site.py lamps-domes --samples 256 --scale 1.0 > /dev/null 2>&1
echo DONE > $D/views-done.txt
