#!/bin/sh
# The inputs this scene reads from other lanes' branches, checked out into the working tree and left uncommitted
# (the coordinator: fetch with git checkout <sha> -- <paths>, never merge). Run from the repo root.
set -e
for b in r33-speaker-horn r32-lamps-final r32-turntable-final; do
  git fetch -q origin +refs/heads/$b:refs/remotes/origin/$b
done
# Tropos: the asset (one collection per tint, cover hidden) and the golden-hour room's set pieces
git checkout 8e44484e -- spinoffs/barkhorn/asset/tropos.blend
git checkout 6770c713 -- spinoffs/barkhorn/room31/pieces.py spinoffs/barkhorn/room31/post.py
# Hemisphere and Core (round 41: the low top, Core on the 30 base) and the kit piece that places them
git checkout origin/r32-lamps-final -- studio/engine/kit.py studio/engine/kit_ext/earf_moon.py \
  studio/products/earf-dome-pendant.json studio/products/earf-orb-table.json \
  spinoffs/barkhorn/companions/out-dome-pendant/render spinoffs/barkhorn/companions/out-orb-table/render
# Mantle (the floating plinth)
git checkout 8f465244 -- studio/products/barkhorn-turntable-float.json spinoffs/barkhorn/companions/out-turntable-float/render
git reset -q
