#!/bin/bash
# BATCH 1a (2026-11-20, the coordinator): Hemisphere and Core on the house ground, Ember, Fog and Smoke, off and on.
# 12 frames, 1600 x 2000. The house ground: launch/house_ground.py (the Tropos fronts' set, sky, lights, camera and
# finish, scaled around the lamp: Hemisphere s 0.20, Core s 0.19). HOUSE_BG: the sweep-only lamps times one declared
# factor so the paper behind a small lamp reads as behind the speaker. ON: HOUSE_DIM, one declared factor per lamp (the
# studio and sky divided by it, the exposure raised by log2 of it). Each frame: its audit (hidden objects and studio
# lamps in frame, Blender's own camera; the emitter list), the render, the Tropos finish. Reruns skip what exists.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/house; mkdir -p $D/audit
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/b1a; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
BG=${HOUSE_BG:-1.16}; DD=${DIM_DOME:-0.35}; DO=${DIM_CORE:-2}
one() { n=$1; f=$2; sp=$3; shift 3
  [ -s $D/audit/$n.txt ] || { env "$@" HOUSE_BG=$BG AUDIT=1 MASK=$S/m-$n.png python3.11 lamp_site.py $f > $S/$n.aud 2>&1 && \
      grep -E "^AUDIT|HIDDENCAST|CASTCHECK|  (in|out) " $S/$n.aud > $D/audit/$n.txt; }
  [ -s $D/$n.png ] || { env "$@" HOUSE_BG=$BG EXR=0 DENOISE=1 LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py $f --samples $sp > /dev/null 2>&1 && \
      $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null && \
      python3 -c "import os,sys; print(sys.argv[1], os.path.getsize(sys.argv[1]))" $D/$n.png; }
}
for kv in red:ember ice:fog black:smoke; do k=${kv%%:*}; t=${kv##*:}
  one hemisphere-$t-off house-dome-$k ${SPP_OFF:-128} LIGHTS_OFF=1 HOUSE_S=0.2
  one hemisphere-$t-on  house-dome-$k ${SPP_ON:-256}  HOUSE_DIM=$DD HOUSE_S=0.2
  one core-$t-off       house-orb-$k  ${SPP_OFF:-128} LIGHTS_OFF=1 HOUSE_S=0.19
  one core-$t-on        house-orb-$k  ${SPP_ON:-256}  HOUSE_DIM=$DO HOUSE_S=0.19
done
echo DONE > /home/user/earf/renders/2026-11-20/barkhorn/lamp-site/batch1a-done.txt
