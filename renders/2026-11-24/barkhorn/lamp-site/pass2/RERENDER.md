# Pass v2: the re-render list (v7, the v6 check's (13))

From 2026-11-10 03:02 UTC to the v5 fix (fd997614, 2026-11-24 12:14 UTC), lamp_site.py's hemisphere() tested the collar's
white at z < 0.080 against mm coordinates, so the collar's painted faces rendered black in every picture it drew. Some of
those faces take the LEDs' light. Since v6, lamp_site.py paints only the painted faces (the lip's foot and the flange's
inner face, every down-facing face below z 80), with or without HEMI_COLLAR_CAP.

Since v7, the CAD's own render export draws the same: the paint as a 0.05 film (crystal.py's white-paint), the cables
stainless. The studio product files are written from the CAD's finishes when each package is rebuilt.

## What hemisphere() draws: re-render every one that is live

- the house dome views (house-dome-*: the off frames, the lit frames, the from-below views)
- lamps-domes* (the rows)
- cluster
- cutaway ('How it lights'; the LIVE masters are in final/, not legible/: see the v9 section below)
- inuse
- trio-*
- dome (the single dome over its pool)

Also re-render the other lane's bar frames made through lamp_site.py's hemisphere(); that lane lists them.

## v8 additions (the v7 check's (9))

What pass v2 renders: the top the owner picks (HEMI_TOP=A, or unset for today's top, or B) on the v8 hanging (two 1/16 in
stainless cables on stop sleeves, the cord 2 mm longer than the cables, the canopy out of frame), HEMI_COLLAR_CAP=1, the collar's white on
its painted faces. If the owner keeps A's lock, A renders from out-dome-pendant-topA (the lock, its cables at 105/285); if not, from
out-dome-pendant-topA-nolock (no lock, the cables at 0/180, the detent), chosen with HEMI_LOCK=0. HEMI_LOCK=0 is the
no-lock answer's switch, not a way to hide the lock in the lock answer's pictures.

The other lane's frames made through hemisphere() (that lane re-renders them):
- a50e8da167: bar-hero, bar-backbar and its portrait, bar-pendants
- main 862cd845e4: tropos-bar

The live site files (each with its -800, -th and -under variants where it has them): hemisphere-<tint> for every tint,
hemisphere-cluster, hemisphere-<tint>-direct, hemisphere-<tint>-under, and the cutaway.
V10 (the v9 check): also derived from the final/ masters by site_fix.py, so the site lane rebuilds them after the re-render:
card-hemisphere-*, home-hemisphere-* and tile-hemisphere-* (24 files on main), hemisphere-ember-off, -cap, -rim and
-table, and hemisphere-row. Pass v2's re-renders go back to the owner before they go live: he approved pictures with the
black collar faces inside the window (coordinator/lamps-final-off-sheet-2026-11-21.jpg, bar-picture-now-and-new-2026-11-22.jpg).
If the owner keeps A's lock, add one picture that shows the knob: every site camera hides it.

The cutaway 'How it lights' (v9, the v8 check's V9-6): the LIVE cutaway, its phone cut and the in-use picture come from
final/ (site_v2.py:2212, LIGHTS_DIR), not legible/:
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ember-cutaway.png (live)
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ember-cutaway-phone.png (live)
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ember-inuse.png (live)
- renders/2026-11-12/barkhorn/lamp-site/legible/hemisphere-ember-cutaway.png (with -phone): a later draft, not live
- lamp_site.py's 'cutaway' and 'inuse' frames draw them

Also re-rendered or rerun (v9): renders/2026-11-16/barkhorn/lamp-site/discs/ice6-acid5-old-new.png,
renders/2026-11-20/barkhorn/lamp-site/off-study/off-table-sheet.png, and renders/2026-11-21/barkhorn/lamp-site/pass/
photometry.md, photometry.raw and photometry.sh (the photometry's record, its raw numbers and its script).

The photometry IS rerun (isphere.py), after the re-render, from the same painted faces.

## The photometry made through it: rerun with isphere.py

- renders/2026-11-10/barkhorn/lamp-site/final/photometry.txt (the published figures)
- renders/2026-11-10/barkhorn/lamp-site/final/photometry-hemisphere.txt
- renders/2026-11-16/barkhorn/lamp-site/final-mix/photometry-mix.txt
- renders/2026-11-16/barkhorn/lamp-site/final-mix/photometry-mix.raw

## Every Hemisphere picture committed in that window

(v9: the paths are those at HEAD; 20 listed in v7 have since been deleted and are dropped.)

Masks, audits and Core-only frames are left out. Which of them are live is the site's call; any that are live are
re-rendered.

- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-acid-direct.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-acid-under.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-acid.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-cluster.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-dust-direct.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-dust-under.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-dust.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ember-below.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ember-cap.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ember-direct.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ember-off.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ember-rim.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ember-under.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ember.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-fog-direct.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-fog-under.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-fog.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-haze-direct.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-haze-under.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-haze.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ice-direct.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ice-under.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-ice.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-poison-direct.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-poison-under.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-poison.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-row.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-smoke-direct.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-smoke-under.png
- renders/2026-11-10/barkhorn/lamp-site/final/hemisphere-smoke.png
- renders/2026-11-10/barkhorn/lamp-site/proofs/hemi-ember-below.png
- renders/2026-11-10/barkhorn/lamp-site/proofs/hemi-ember.png
- renders/2026-11-10/barkhorn/lamp-site/proofs/hemi-ice.png
- renders/2026-11-10/barkhorn/lamp-site/proofs/r2/hemi-ember-amber.png
- renders/2026-11-10/barkhorn/lamp-site/proofs/r2/hemi-ember-below-amber.png
- renders/2026-11-10/barkhorn/lamp-site/proofs/r2/hemi-ember-below-warm.png
- renders/2026-11-10/barkhorn/lamp-site/proofs/r2/hemi-ember-warm.png
- renders/2026-11-10/barkhorn/lamp-site/proofs/r2/hemi-ice-amber.png
- renders/2026-11-10/barkhorn/lamp-site/proofs/r2/hemi-ice-warm.png
- renders/2026-11-12/barkhorn/lamp-site/legible/hemisphere-ember-cutaway-phone.png
- renders/2026-11-12/barkhorn/lamp-site/legible/hemisphere-ember-cutaway.png
- renders/2026-11-12/barkhorn/lamp-site/legible/hemisphere-ember-inuse.png
- renders/2026-11-15/barkhorn/lamp-site/off-match/dye-match.png
- renders/2026-11-15/barkhorn/lamp-site/off-match/lit-correction.png
- renders/2026-11-15/barkhorn/lamp-site/off-match/off-match.png
- renders/2026-11-15/barkhorn/lamp-site/off-match/smoke-pair.png
- renders/2026-11-15/barkhorn/lamp-site/off-match/tints-off-v2.png
- renders/2026-11-15/barkhorn/lamp-site/off-match/tints-off-v3.png
- renders/2026-11-15/barkhorn/lamp-site/off-match/tints-off.png
- renders/2026-11-15/barkhorn/lamp-site/smoke-2700/smoke-2700-proof.png
- renders/2026-11-15/barkhorn/lamp-site/smoke-choice/smoke-choice-sheet.png
- renders/2026-11-16/barkhorn/lamp-site/discs/smoke-before-after-stretched.png
- renders/2026-11-16/barkhorn/lamp-site/discs/smoke-before-after.png
- renders/2026-11-16/barkhorn/lamp-site/final-mix/hemisphere-cluster.png
- renders/2026-11-16/barkhorn/lamp-site/final-mix/hemisphere-row.png
- renders/2026-11-16/barkhorn/lamp-site/hemi-match/hemi-match-sheet.png
- renders/2026-11-16/barkhorn/lamp-site/mix/mix-sheet.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/amber/hemi-lit-L2.1.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/amber/hemi-lit-L3.0.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/amber/hemi-lit-L5.0.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/amber/hemi-off-L2.1.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/amber/hemi-off-L3.0.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/black/hemi-lit-L1.2.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/blue/hemi-lit-L3.0.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/blue/hemi-lit-L6.0.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/blue/hemi-off-L2.1.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/blue/hemi-off-L3.0.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/fog/hemi-off-key0.6.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/fog/hemi-off-key1.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/green/hemi-lit-L0.55.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/green/hemi-lit-L0.7.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/green/hemi-lit-L1.0.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/green/hemi-off-L0.5.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/green/hemi-off-L0.55.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/green/hemi-off-L0.6.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/green/hemi-off-L0.7.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/orange/hemi-lit-L2.1.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/orange/hemi-lit-L3.0.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/orange/hemi-off-L2.1.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/red/hemi-lit-L0.7.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/red/hemi-lit-L1.0.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/red/hemi-off-L0.7.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/red/hemi-off-L1.0.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/violet/hemi-lit-L1.0.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/violet/hemi-lit-L1.8.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/violet/hemi-off-L0.7.png
- renders/2026-11-20/barkhorn/lamp-site/checkset/violet/hemi-off-L1.0.png
- renders/2026-11-20/barkhorn/lamp-site/drawings/hemisphere-dimensions.png
- renders/2026-11-20/barkhorn/lamp-site/ember-faults/cord-braid-fullsize.png
- renders/2026-11-20/barkhorn/lamp-site/ember-faults/dots-base-nogaskets-noclear.png
- renders/2026-11-20/barkhorn/lamp-site/ember-faults/lit-balance-sweep.png
- renders/2026-11-20/barkhorn/lamp-site/ember-faults/rim-line-open-vs-closed-lip.png
- renders/2026-11-20/barkhorn/lamp-site/house/hemisphere-ember-off.png
- renders/2026-11-20/barkhorn/lamp-site/house/hemisphere-ember-on.png
- renders/2026-11-20/barkhorn/lamp-site/house/hemisphere-fog-off.png
- renders/2026-11-20/barkhorn/lamp-site/house2/hemisphere-ember-lit.png
- renders/2026-11-20/barkhorn/lamp-site/house2/hemisphere-ember-off.png
- renders/2026-11-20/barkhorn/lamp-site/house3/hemisphere-fog-off.png
- renders/2026-11-20/barkhorn/lamp-site/house3/hemisphere-smoke-off.png
- renders/2026-11-20/barkhorn/lamp-site/house4/hemisphere-ember-lit.png
- renders/2026-11-20/barkhorn/lamp-site/house4/hemisphere-ember-off.png
- renders/2026-11-20/barkhorn/lamp-site/house5/base-left-airgap-right-contact-quarter.png
- renders/2026-11-20/barkhorn/lamp-site/house8/hemisphere-ember-lit.png
- renders/2026-11-20/barkhorn/lamp-site/house8/hemisphere-ember-off.png
- renders/2026-11-20/barkhorn/lamp-site/house9/hemisphere-ember-lit.png
- renders/2026-11-20/barkhorn/lamp-site/off-study/ember-pours-dark-lit.png
- renders/2026-11-20/barkhorn/lamp-site/off-study/ember-pours-dark-off.png
- renders/2026-11-20/barkhorn/lamp-site/off-study/ember-pours-house-off.png
- renders/2026-11-20/barkhorn/lamp-site/row-off/hemisphere-amber-off.png
- renders/2026-11-20/barkhorn/lamp-site/row-off/hemisphere-black-off.png
- renders/2026-11-20/barkhorn/lamp-site/row-off/hemisphere-blue-off.png
- renders/2026-11-20/barkhorn/lamp-site/row-off/hemisphere-green-off.png
- renders/2026-11-20/barkhorn/lamp-site/row-off/hemisphere-ice-off.png
- renders/2026-11-20/barkhorn/lamp-site/row-off/hemisphere-orange-off.png
- renders/2026-11-20/barkhorn/lamp-site/row-off/hemisphere-violet-off.png
- renders/2026-11-21/barkhorn/lamp-site/pass/amber/hemisphere-amber-lit.png
- renders/2026-11-21/barkhorn/lamp-site/pass/amber/hemisphere-amber-off.png
- renders/2026-11-21/barkhorn/lamp-site/pass/black/hemisphere-black-lit.png
- renders/2026-11-21/barkhorn/lamp-site/pass/black/hemisphere-black-off.png
- renders/2026-11-21/barkhorn/lamp-site/pass/blue/hemisphere-blue-lit.png
- renders/2026-11-21/barkhorn/lamp-site/pass/blue/hemisphere-blue-off.png
- renders/2026-11-21/barkhorn/lamp-site/pass/cards/hemisphere-acid.jpg
- renders/2026-11-21/barkhorn/lamp-site/pass/cards/hemisphere-dust.jpg
- renders/2026-11-21/barkhorn/lamp-site/pass/cards/hemisphere-ember.jpg
- renders/2026-11-21/barkhorn/lamp-site/pass/cards/hemisphere-haze.jpg
- renders/2026-11-21/barkhorn/lamp-site/pass/cards/hemisphere-ice.jpg
- renders/2026-11-21/barkhorn/lamp-site/pass/cards/hemisphere-poison.jpg
- renders/2026-11-21/barkhorn/lamp-site/pass/cards/hemisphere-smoke.jpg
- renders/2026-11-21/barkhorn/lamp-site/pass/green/hemisphere-green-lit.png
- renders/2026-11-21/barkhorn/lamp-site/pass/green/hemisphere-green-off.png
- renders/2026-11-21/barkhorn/lamp-site/pass/ice/hemisphere-ice-lit.png
- renders/2026-11-21/barkhorn/lamp-site/pass/ice/hemisphere-ice-off.png
- renders/2026-11-21/barkhorn/lamp-site/pass/orange/hemisphere-orange-lit.png
- renders/2026-11-21/barkhorn/lamp-site/pass/orange/hemisphere-orange-off.png
- renders/2026-11-21/barkhorn/lamp-site/pass/red/hemisphere-red-lit.png
- renders/2026-11-21/barkhorn/lamp-site/pass/red/hemisphere-red-off.png
- renders/2026-11-21/barkhorn/lamp-site/pass/violet/hemisphere-violet-lit.png
- renders/2026-11-21/barkhorn/lamp-site/pass/violet/hemisphere-violet-off.png
- renders/2026-11-24/barkhorn/lamp-site/tests/d0.png
- renders/2026-11-24/barkhorn/lamp-site/tests/d1.png
- renders/2026-11-24/barkhorn/lamp-site/tests/d2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/e1.png
- renders/2026-11-24/barkhorn/lamp-site/tests/e2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/h0.png
- renders/2026-11-24/barkhorn/lamp-site/tests/hb1.png
- renders/2026-11-24/barkhorn/lamp-site/tests/hb2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/hb3.png
- renders/2026-11-24/barkhorn/lamp-site/tests/hc.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/c1.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/c2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/c3.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/c4.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/c5.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/cards-sheet.jpg
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/cards25-green.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/cards38-green.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/lit2048.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/lit2048nd-median2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/lit2048nd.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/lvl-A-x2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/lvl-A.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/lvl-B-x2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/lvl-B.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/lvl-today-x2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/lvl-today.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/p1.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/p2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/p3.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/p4.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/p5.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/p6.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/top-sheet-v2.jpg
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/top-sheet-v3.jpg
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/top-sheet-v4.jpg
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/top-sheet.jpg
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/top0-x2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/topA-x2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/topA.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/topB-x2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/topB.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v3-A-x2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v3-A.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v3-B-x2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v3-B.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v3-today-x2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v3-today.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v4-A-below.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v4-A-x2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v4-A.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v4-B-below.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v4-B-x2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v4-B.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v4-today-below.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v4-today-x2.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/v4-today.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/wb-sheet-4b.jpg
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/wb-sheet.jpg
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/wb4000-black.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/wb4000-ice.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/wb4000-red.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/wb4000gel-black.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/wb4000gel-ice.png
- renders/2026-11-24/barkhorn/lamp-site/tests/r2/wb4000gel-red.png

## V11 (the V10 check's V11-18): the cord's and the cables' tops

THE RULE: the cord's and the cables' tops never show in frame. Since V10 the cord's mesh (cord-v6) ends its jacket 750 above
the rim, inside the canopy (V11: the render's mesh leaves out its two conductors), and the cables end at 765.1. That is out of
frame in every single-lamp frame, but not in a group: the cluster's front-row rims at 0.42 to 0.62 m put the ends at about 1.15
to 1.39 m, in frame. So either run them on past the frame's edge, or end them at a canopy on a ceiling:
- lamp_site.py: CORD_TOP=<m> runs the cord and both cables on, straight, to that height (world); CANOPY=1 adds the 150 x 50
  canopy there (for a frame with a ceiling). The same switches as the support sweep's patch to 5e86d76e (fa2d6ff2b0), which
  made the live cluster (CORD_TOP=1.75) and the in-use picture (CORD_TOP=2.35 CANOPY=1).
- The one-way marks (V11-13: a line on the crown's lowest tier at 30 deg, a groove on A's and B's clamp ring or today's collar
  chamfer at 60 deg) are in the meshes from V11: re-exported with top_tiers.py.
- After the owner's pick: add the dims drawing on r47-site-next to the list (it shows the cord alone, no cables).
- For pass v2: show the canopy once, for example "Over a table" with its ceiling.
