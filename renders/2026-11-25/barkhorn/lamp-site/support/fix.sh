#!/bin/bash
# The coordinator's support sweep (2026-11-25, wf_331538ce-038): two live Hemisphere pictures re-rendered with ONLY their
# support fixed, from the code that made them (lamp_site.py at 5e86d76e, checked out on its own as a sparse worktree,
# with lamp_site-5e86d76e.patch applied) and their own recipes (final-mix/mix.sh for the in-use picture, step2.sh for the
# cluster):
#   hemisphere-cluster: every cord run on, straight, to 1.75 m (CORD_TOP), above the frame (its highest edge along any cord
#     is 1.476 m), so none ends in mid-air;
#   hemisphere-ember-inuse: the chair turned to face the table, its seat under it and its back 29 clear of the top (it faced
#     away, its back through the top); the cord run on to a 150 x 50 canopy at the 2.40 ceiling (CORD_TOP 2.35, CANOPY=1);
#     the cup's handle moved out 15.5 to the wall (it ran 13.5 into the cavity).
# Written here, not into final/. Usage: WT=<the worktree> fix.sh
set -e
D=$(cd "$(dirname "$0")" && pwd); cd ${WT:?worktree}/spinoffs/barkhorn/companions
r() { [ -s "$1" ] && return 0; shift; "$@"; }
aud() { o=$1; shift; "$@" > "$o.tmp" 2>&1; mv "$o.tmp" "$o"; }
mkdir -p $D/audit $D/masks
LIT=(WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' WORLD='#BDBDBD' EXR=0)
r $D/audit/hemisphere-ember-inuse.txt aud $D/audit/hemisphere-ember-inuse.txt env "${LIT[@]}" DENOISE=1 ROOM_FILL=6 EV=-0.5 CORD_TOP=2.35 CANOPY=1 AUDIT=1 MASK=$D/masks/hemisphere-ember-inuse.png python3.11 lamp_site.py inuse
r $D/hemisphere-ember-inuse.png env "${LIT[@]}" DENOISE=1 ROOM_FILL=6 EV=-0.5 CORD_TOP=2.35 CANOPY=1 LAMP_OUT=$D/hemisphere-ember-inuse.png python3.11 lamp_site.py inuse --samples 256 --scale 1.0 > /dev/null 2>&1
date -u
LIT2=(WB=4000 STUDIO_K=4000 PAPER='#9A9A9A' EXR=0 DENOISE=1)
r $D/audit/hemisphere-cluster.txt aud $D/audit/hemisphere-cluster.txt env "${LIT2[@]}" STUDIO_OFF=key,fill WORLD='#FFD4A5' WORLD_STR=1.0 CORD_TOP=1.75 AUDIT=1 MASK=$D/masks/hemisphere-cluster.png python3.11 lamp_site.py cluster
r $D/hemisphere-cluster.png env "${LIT2[@]}" STUDIO_OFF=key,fill WORLD='#FFD4A5' WORLD_STR=1.0 CORD_TOP=1.75 LAMP_OUT=$D/hemisphere-cluster.png python3.11 lamp_site.py cluster --samples ${CLUS_SPP:-512} --scale 1.0 > /dev/null 2>&1
date -u
