# EARF approved pictures: the one list every asset draws from

Started 9 Nov 2026, 21:10 UTC, at the owner's direction ("we need to sequence the work, so the marketing and brand assets use the
right product renders"). Kept by the coordinator. A picture goes on this list only after it passes the blind gate (majority SHOW)
and the studio honesty rules (nothing hidden from the camera standing in frame; one sun, the sky's own; every object casts shadows).
The site, the Brand Book, social, the deck and press use ONLY pictures on this list. When a picture is replaced, the old line moves to
"Pulled" with the reason, and every asset that used it is refreshed in one batch.

## The order of work
1. LOCK EACH PRODUCT'S DESIGN AND MATERIALS. Tropos: locked (base A, no light; the polished horn; one dye per tint from
   tints-trucast.json), except Haze's horn pour (walkthrough 132). Lamps: DESIGN LOCKED 9 Nov 21:12 (the owner: Core B, "assuming we're still
   using the same materials we would use for the speakers and mantle": the outer ball in the speaker's TruCast tints, one dye per tint;
   a 3 mm white opal inner ball, the same opal as Hemisphere's diffuser); the lamps lane to confirm the CAD, BOM and stock in writing.
   The lamp kit's Ember dye was a stale hand value until 9 Nov, now the speaker's 2423. Mantle: locked as drawn (Strata Float).
2. LOCK THE STUDIO PICTURES OF EACH LOCKED PRODUCT. Tropos: the seven fronts (9 Nov), then the backs, close-ups and wides. Lamps:
   in Core B. Mantle: the day frame is in.
3. ONLY THEN REBUILD THE ASSETS (site, Book, social, deck) from this list, one batch per lock.
Scenes (habitats, night pictures) use the locked models and can run alongside; each enters an asset only after it passes.

## Tropos
Lights audit (9 Nov 21:40, from each shot.json): the turning views, the horn-backs and the amp plate are lit by key, fill and wash
(area lights) plus background lamps linked to the sweep (flagged background lights); chunks 4 and 05 (06b829ce, 52ad76ba) also carry
the old glow lamp, tested to make only a noise-level difference. No specular-only source in any of them. The tallr2 fronts carried
three specular-only panels (scrim, sheen, topline at diffuse 0): withdrawn from the re-shoot (21:34) so the fronts are lit only by
lights a real studio could use.
| Picture | Source (branch @ commit: path) | Gate | Used by |
|---|---|---|---|
| Seven fronts ("talls"), honest rig round 2 | helpers r33-rollout-c2/c3/c4 and r33-speaker-horn, renders/2026-11-04/barkhorn/rollout/A-polished-tallr2/site-front-off-tall-<k>.png on 63d83f47 | FAILED 9 Nov 21:24: Ember, Acid, Ice 3/3 NO; Dust 1/3 (21:28); Fog 2/3 SHOW (founder, skeptic; photo NO), kept only as a fallback since the set is re-shot on one rig; Poison, Haze 0/3 (21:31: the lower side face milky, see-through fails). Re-shoot A-polished-glint under way (r33-speaker-horn 4094b6ed + a flag for the lower-side veil) | none until the re-shoot passes; the site and the Book wait for it |
| Turning view, Ember, Dust, Acid, Poison, Ice, Haze | r33-rollout-c3 52ad76ba (Ember 00-04); c4 0a0a83bd (Ember 05-23, Dust); c4 42fa8eee (Acid 00-16); c3 66126d53 (Acid 17-23, Haze); c4 eef18db2 (Poison, Ice): renders/2026-11-04/barkhorn/rollout/A-polished-p2*/turn-<k>-NN.png | PASSED (wf_c0448c65-cd3) | site galleries |
| Turning view, Fog, neutral ground | r33-rollout-c3 a688c59e: A-polished-p2-rc2/turn-fog-00..23.png | PASSED 3/3 (9 Nov 21:11; the stage at the rendered 211,212,207) | site gallery (FOG_TURN on) |
| Horn from behind, seven | 06b829ce, 52ad76ba, a1322583 (not the failed Acid file), cut 4:5 at x 270-990 | PASSED, audited clean | site galleries; the home's Tropos block (Ember) |
| Amp plate, Ember | 488fbec9 (amp-plate-ember) | PASSED, audited clean | site galleries ("The built-in amplifier, from behind.") |
| Backs (rear three-quarter) | r33-speaker-horn e85bd44f (round 3, bright-field glow) | NOT YET: full-size renders and gate pending | none |
| Wides | r33-speaker-horn 89d95763 (the wide's horn lamp off) | NOT YET: renders and gate pending | none |

## Habitats (scenes)
The shadow rule (9 Nov 21:25, biomes 3122f00c, proven by a slab test): until then a tinted wall passed tr² × volume to shadow rays (the tint
three times, the Fresnel loss twice). From now on each face carries √0.92 and the welded volume gives the tint once. Files made under
the old rule are marked; each is re-rendered under the new rule and gated against its passed file before it is swapped.
| Picture | Source | Gate | Used by |
|---|---|---|---|
| Ice, "Out in the snow at dusk." | 0f619953 | PASSED (old shadow rule: re-render under 3122f00c's rule queued; this file stays until it passes) | site (home band, /tropos/ice, /colors/ice), Book |
| Dust, "On rippled sand among desert buttes." | r48-biomes 43c91242: renders/2026-11-03/barkhorn/habitats/dust-portrait-1200x1500-nopanel.jpg | PASSED 3/3 (9 Nov; old shadow rule: re-render under 3122f00c's rule queued; this file stays until it passes) | site, Book |
| Fog, "In the grass on a hillside, in fog at dawn." | r48-biomes aa1ca856: habitats/fog_b-portrait-1200x1500-onesun.jpg (sha256 9f1fa543...; the glass's Fresnel loss in its shadows: the inside a touch dimmer) | PASSED 2/2 (9 Nov 21:21, photo and skeptic) | site, Book ("In fog at dawn."), swapping in tonight's push |
| Acid | r48-biomes 539c3772 | HOLD 1/3 (rain stops at the speaker; dry; dark cabinet) | none |
| Poison, Ember, Haze | in progress / not started (Haze waits on the horn pour) | | none |

## Lamps
None approved. The unlit Ember pair: HOLD 0/4 (fixing: the liner, the dye, the surround). The lit set, round 3 proxies: in gate.
Core B, decided by the owner 9 Nov 21:12 (the dark border he liked comes from B's nested build). Every lamp picture is re-rendered as B.

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
| tallr2 talls (A-polished-tallr2, all seven) | a thin white line on the right side face at mid-height (a strip of lit sweep between the floor flag and the slanted upright card), and a milky lower side face below a hard diagonal (the camera-right fill card in its mirror path) | 9 Nov 21:24 |
| Backs (rigB, img/rc/<k>-back) | lamps hidden from the camera standing in frame | 9 Nov |
| lamps-unlit (the Smoke pair) | hidden lamps in frame; Smoke is held | 9 Nov |
| Dust habitat 26493989 | an 8 x 3 m bounce panel hidden from the camera in frame | 9 Nov |
| Fog habitat b61474c0 | two suns 100° apart | 9 Nov |
| Fog turn rc1 (pale blue ground) | read as Ice | 9 Nov |
| Fog habitat cd5aa4e6 (same path) | superseded by aa1ca856, the same frame with the glass's real light loss in its shadows; not a fault | 9 Nov 21:21 |
| Every picture in Smoke | Smoke is held | |
