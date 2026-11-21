#!/bin/bash
# Core Ember LIT re-balanced (2026-11-21). The full frame from ember-r5b.sh read glow L* 42.5 against Hemisphere's 36.2
# (its quarter estimate had said 35.9). Glow Y ratio 0.092/0.128 = 0.72, so -0.48 EV; the studio raised by 1/0.72 to
# hold the walls: studio 0.84 at -3.08 EV. Otherwise exactly as ember-r5b.sh. Writes house8/core-ember-lit-b.png.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/house8
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/et8; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
n=core-ember-lit-b
[ -s $D/$n.png ] || { env HOUSE_STUDIO=0.84 HOUSE_EV=-3.08 HOUSE_SWEEP_AO=0 HOUSE_ROOM_TRANS=1 HOUSE_S=0.19 CORE_DOCK=0 \
    HOUSE_CUT2=fill,1.0 HOUSE_FLOORCARD=0.0755,2.5,0.0005,-1,1 "HOUSE_FLAGS=horn cutter" HOUSE_BG=1.16 EXR=0 DENOISE=1 \
    LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py house-orb-red --samples 512 > $S/$n.log 2>&1 && \
  $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null && ls -la $D/$n.png && date -u; }
