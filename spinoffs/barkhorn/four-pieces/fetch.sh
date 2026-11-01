#!/bin/sh
# The inputs this scene reads from other lanes' branches, checked out into the working tree and left uncommitted
# (the coordinator: fetch with git checkout <sha> -- <paths>, never merge). Run from the repo root.
set -e
for b in r33-speaker-horn r32-lamps-final r32-turntable-final; do
  git fetch -q origin +refs/heads/$b:refs/remotes/origin/$b
done
# Tropos: the asset (one collection per tint, cover hidden) and the golden-hour room's set pieces
# 2026-11-01: both assets rebuilt (the top bay's lining box had been decimated into a wedge); Strata is the launch design
git checkout c77460f03d0e39956b11097ed4a46887967d7553 -- spinoffs/barkhorn/asset/tropos.blend
# the owner's final Strata (the stepped horn flush, black sleeves, the lit stepped plinth)
git checkout 603a54e2287f5b30b84f209db58c8c2eaaa1b60a -- spinoffs/barkhorn/asset/tropos-strata.blend
# for the -final-2092 frames: the same design in the TruCast stock codes (the owner: "I like the darker colors")
# git checkout a682dc526010b04eca7deef6494b07d33b993c73 -- spinoffs/barkhorn/asset/tropos-strata.blend
git checkout 6770c713 -- spinoffs/barkhorn/room31/pieces.py spinoffs/barkhorn/room31/post.py
# Hemisphere and Core (round 41: the low top, Core on the 30 base) and the kit piece that places them
git checkout origin/r32-lamps-final -- studio/engine/kit.py studio/engine/kit_ext/earf_moon.py \
  studio/products/earf-dome-pendant.json studio/products/earf-orb-table.json \
  spinoffs/barkhorn/companions/out-dome-pendant/render spinoffs/barkhorn/companions/out-orb-table/render
# Mantle (the floating plinth)
git checkout 8f465244 -- studio/products/barkhorn-turntable-float.json spinoffs/barkhorn/companions/out-turntable-float/render
git reset -q
# Hemisphere v3, "color outside" (the owner, 2026-11-01), for the -final-2092-sf frames
git checkout 7c4b5993eb3e9f12cc3e6a092b2987dfd319ff9b -- spinoffs/barkhorn/companions/out-dome-pendant-v3/render studio/products/earf-dome-pendant-v3.json
git reset -q
# Mantle A, Strata Float v3 (the owner, 2026-11-01), for the -final-2092-sf frames
git checkout 1d59abeb1b1c55b971c7c47dba354adcf49917e9 -- studio/products/mantle-strata-v3.json spinoffs/barkhorn/companions/mantle-r48/out-strata-v3/render
git reset -q
