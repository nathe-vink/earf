# EARF approved pictures: the one list every asset draws from

Started 9 Nov 2026, 21:10 UTC, at the owner's direction ("we need to sequence the work, so the marketing and brand assets use the
right product renders"). Kept by the coordinator. A picture goes on this list only after it passes the blind gate (majority SHOW)
and the studio honesty rules (nothing hidden from the camera standing in frame; one sun, the sky's own; every object casts shadows).
The site, the Brand Book, social, the deck and press use ONLY pictures on this list. When a picture is replaced, the old line moves to
"Pulled" with the reason, and every asset that used it is refreshed in one batch.

## The order of work
1. LOCK EACH PRODUCT'S DESIGN AND MATERIALS. Tropos: locked (base A, no light; the polished horn; one dye per tint from
   tints-trucast.json), except Haze's horn pour (walkthrough 132). Lamps: NOT locked (Core A or B is the owner's call; the lamp kit's
   Ember dye was a stale hand value until 9 Nov, now the speaker's 2423). Mantle: locked as drawn (Strata Float).
2. LOCK THE STUDIO PICTURES OF EACH LOCKED PRODUCT. Tropos: the seven fronts (9 Nov), then the backs, close-ups and wides. Lamps:
   after A/B. Mantle: the day frame is in.
3. ONLY THEN REBUILD THE ASSETS (site, Book, social, deck) from this list, one batch per lock.
Scenes (habitats, night pictures) use the locked models and can run alongside; each enters an asset only after it passes.

## Tropos
| Picture | Source (branch @ commit: path) | Gate | Used by |
|---|---|---|---|
| Seven fronts ("talls"), honest rig round 2 | helpers r33-rollout-c2/c3/c4 and r33-speaker-horn, renders/2026-11-04/barkhorn/rollout/A-polished-tallr2/site-front-off-tall-<k>.png on 63d83f47 | IN GATE 9 Nov ~21:10 | site (hero, cards, product, color, share), Book (fronts), social |
| Turning view, Ember, Dust, Acid, Poison, Ice, Haze | r33-rollout-c3 52ad76ba (Ember 00-04); c4 0a0a83bd (Ember 05-23, Dust); c4 42fa8eee (Acid 00-16); c3 66126d53 (Acid 17-23, Haze); c4 eef18db2 (Poison, Ice): renders/2026-11-04/barkhorn/rollout/A-polished-p2*/turn-<k>-NN.png | PASSED (wf_c0448c65-cd3) | site galleries |
| Turning view, Fog, neutral ground | r33-rollout-c3 a688c59e: A-polished-p2-rc2/turn-fog-00..23.png | IN GATE 9 Nov ~21:00 | site gallery (behind FOG_TURN) |
| Horn from behind, seven | 06b829ce, 52ad76ba, a1322583 (not the failed Acid file), cut 4:5 at x 270-990 | PASSED, audited clean | site galleries; the home's Tropos block (Ember) |
| Amp plate, Ember | 488fbec9 (amp-plate-ember) | PASSED, audited clean | site galleries ("The built-in amplifier, from behind.") |
| Backs (rear three-quarter) | r33-speaker-horn e85bd44f (round 3, bright-field glow) | NOT YET: full-size renders and gate pending | none |
| Wides | r33-speaker-horn 89d95763 (the wide's horn lamp off) | NOT YET: renders and gate pending | none |

## Habitats (scenes)
| Picture | Source | Gate | Used by |
|---|---|---|---|
| Ice, "Out in the snow at dusk." | 0f619953 | PASSED | site (home band, /tropos/ice, /colors/ice), Book |
| Dust, "On rippled sand among desert buttes." | r48-biomes 43c91242: renders/2026-11-03/barkhorn/habitats/dust-portrait-1200x1500-nopanel.jpg | PASSED 3/3 (9 Nov) | site, Book |
| Fog, "In the grass on a hillside, in fog at dawn." | r48-biomes cd5aa4e6: habitats/fog_b-portrait-1200x1500-onesun.jpg (aa1ca856 re-render with the glass's Fresnel loss in its shadows: in gate) | PASSED 3/3 (9 Nov) | site, Book ("In fog at dawn.") |
| Acid | r48-biomes 539c3772 | HOLD 1/3 (rain stops at the speaker; dry; dark cabinet) | none |
| Poison, Ember, Haze | in progress / not started (Haze waits on the horn pour) | | none |

## Lamps
None approved. The unlit Ember pair: HOLD 0/4 (fixing: the liner, the dye, the surround). The lit set, round 3 proxies: in gate.
Core A or B: the owner's call (9 Nov 21:06: the dark border he liked comes from B's nested build).

## Mantle
| Picture | Source | Gate | Used by |
|---|---|---|---|
| Mantle by day (C3e), shown in Ember | 41232b56 (three files) | PASSED | site (/mantle, the home's Mantle band) |
Night picture (Ice Tropos under a Hemisphere pendant): proxy 8 in progress, not approved.

## Pulled (do not use)
| Picture | Why | Pulled |
|---|---|---|
| The old talls (img/rc/<k>-tall.*) and wides | a lamp hidden from the camera standing in frame | 9 Nov |
| 15931e00 talls (tag tallfix) | a hard arched light pool on the backdrop (the grid's hard cone) | 9 Nov 20:25 |
| Backs (rigB, img/rc/<k>-back) | lamps hidden from the camera standing in frame | 9 Nov |
| lamps-unlit (the Smoke pair) | hidden lamps in frame; Smoke is held | 9 Nov |
| Dust habitat 26493989 | an 8 x 3 m bounce panel hidden from the camera in frame | 9 Nov |
| Fog habitat b61474c0 | two suns 100° apart | 9 Nov |
| Fog turn rc1 (pale blue ground) | read as Ice | 9 Nov |
| Every picture in Smoke | Smoke is held | |
