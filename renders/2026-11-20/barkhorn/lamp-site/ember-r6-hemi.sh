#!/bin/bash
# Hemisphere Ember LIT, round 6 (2026-11-21, the coordinator's GO at 08:16 after the critics): as ember-r5b.sh's LIT
# frame, plus HOUSE_SOFTBOX_SEEN=0, the four softboxes flagged off the lamp (face and housing hidden from glossy and
# transmission rays; their edges were denoiser seams in the shell, house8/check/), and the denoiser guided by the colour
# alone (DENOISE_PASSES=RGB: the albedo guide carries reflected edges sharply through the polished shell, faint in the
# colour, and OIDN drew them as seams; house8/check/dn-*). Writes house9/.
cd /home/user/earf/spinoffs/barkhorn/companions
D=/home/user/earf/renders/2026-11-20/barkhorn/lamp-site/house9; mkdir -p $D
S=/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/et9; mkdir -p $S
FPY=/home/user/earf/.venv-fab/bin/python
n=hemisphere-ember-lit
[ -s $D/$n.png ] || { env HOUSE_SOFTBOX_SEEN=0 DENOISE_PASSES=RGB HOUSE_STUDIO=3.5 HOUSE_EV=-5.15 HOUSE_SWEEP_AO=0 HOUSE_ROOM_TRANS=1 \
    HOUSE_S=0.2 HOUSE_LIFT=0.25 HOUSE_LIFT_RX=bg-left HOUSE_KEYFLAG=0,60,25,60,2 HOUSE_BG=1.16 EXR=0 DENOISE=1 \
    LAMP_OUT=$S/$n-raw.png python3.11 lamp_site.py house-dome-red --samples 512 > $S/$n.log 2>&1 && \
  $FPY launch/house_finish.py $S/$n-raw.png $D/$n.png > /dev/null && ls -la $D/$n.png && date -u; }
