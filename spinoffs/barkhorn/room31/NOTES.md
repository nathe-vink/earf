# Room 31: a pair of Poison at home

The brief (coordinator, 2026-10-18): remake the room shot (`renders/2026-10-18/barkhorn/finals31/room.png`, blind
critic 4.5/10, "reads at once as an archviz render") to the standard of a campaign image for a $20,000 product: a
real living room, photographed as a design magazine or a luxury house would shoot it.

- `room.py` writes the shots (`studio/shots/barkhorn/room31/room.json`, `room-portrait.json`); `DEFAULT` holds the
  settings as they stand.
- `pieces.py` is the set's own kit `ext` module (loaded by path; the one engine change, `kit.py`, lets an ext piece
  name its module by path): the walnut credenza with bookmatched veneer, the deep-pile rug, the wall sockets, the
  cloth-bound books, the exterior plate seen through the glazing, and the photographed oak and plaster laid over the
  room's own floor and walls.
- `card.py` writes the critic's card from a shot; `critic-rN.json` are the critics' replies, verbatim.

## The concept (as shipped)

References looked at first (Kinfolk and NORM-style interiors: toned plaster, bare walls, window light raking across
them, oak and walnut, a few real objects). One light idea: low late-afternoon sun (azimuth -68, elevation 14) through
a run of tall French windows down the left wall, from in front of the pair, so both speakers stand in it alike and
each lays its shadow, green where the light came through its horn and cabinet, on the plaster and floor beside it.
Linen sheers drawn over the front bays turn the rest of the sun into a soft glow; the back bay stays open, for the
view out and for the beams that reach the pair. A cool, sun-free fill from the right (a window out of frame) and a
low bounce card by the camera open the shade. The view out is a photographed autumn wood (Poly Haven
`autumn_forest_04`, turned so its own sun agrees with ours) on a plate only the camera and the gloss see.

Camera: 1.05 m high, squared to the back wall, 40 mm, level with a small rise of the lens (verticals straight); each
speaker about half the frame's height; the wall above for the heading. The portrait (1600 x 2000, for phones) is the
same room with the pair brought in to +-0.92 m round a two-door credenza, 50 mm from 4.1 m, the sun 2 degrees further
round so it still reaches both speakers.

Set: oiled wide-plank oak (Poly Haven `wood_floor`), plaster (`beige_wall_001`, tinted warm white), a walnut credenza
built here with the veneer (`walnut_veneer_02`) laid on across its doors, Cumulus in Fog on it with a vase
(`ceramic_vase_02`) and three cloth-bound books (invented titles), the wall sockets and the mains leads, the sheers.
Out of the landscape after r10: the rug and the lounge chair (`modern_arm_chair_01`, re-dyed); see r10 and r11.

Finish (`post.py`): a green trim 0.3 in the greens' mid-tones, vignette 0.1 stop, bloom 0.03, luminance grain 1.4.

## Passes

| pass | image | blind score | top changes | what was done |
|---|---|---|---|---|
| r1 | finals31/room.png (the frame being replaced) | 4.5 | sun onto the pair; real rug, chair, exterior, veneer; fill from the right; squared camera | the concept above, from scratch |
| r2 | proofs/r2.png (0.5, 128 spp) | 6.0 | c1 sun from the left and behind the pair (az -100, el 14); c2 a bounce for the horn throats; c3 a darker, flatter rug pulled forward; c4 the dark half-cropped chair out; c5 more fill; c6 the record player into the sun | tried c1 literally (p05: az -102, speakers forward): the back wall went flat grey and the cabinets murky, and from behind the right speaker can only be reached past the back wall. Took its intent instead: the sun low from the left, a little in front of the pair's plane (az -75, el 16), so it rakes both fronts and throws each shadow sideways, clear of the other (checked by geometry). c2 bounce card 0.35; c3 rug #A89A82 at y -1.5; c4 the chair re-dyed cognac and turned to face the pair; c5 fill 1.0; c6 record player to x -0.15 |
| r3 | proofs/r3.png | 6.0 | c1 sun back toward the camera side (az -62, el 14) so the horns' green light lands on the wall; c2 sun 30 against fill 0.45, sky 0.45, exposure -0.55 (half a stop of sun/shade was too flat); c3 rug darker, deeper pile, back to y -1.2; c4 warm sun #FFD6A0, cool fill, no tint; c5 plaster bump 0.45 and finer; c6 the credenza's toe-kick not a black hole; c7 exterior calmer, a linen sheer; c8 chair further out | all eight, as given (the az -60 alternative proof agreed with c1); the rug's value cut to 0.62 (a colour tint keeps the scan's light value) |
| r4 | proofs/r4.png | 6.5 | c1 exposure down (every sunlit surface on the view's shoulder); c2 plaster relief back up; c3 a less orange sun; c4 the view out brighter, sunlit; c5 the veneer banded; c6 the pair lit alike (toe-in 6); c7 rug darker; c8 sun az -68 to clear the heading's zone | exposure -0.9; plaster bump 0.8, 1.5 m tile, tint 0.7 (between r3's "less" and r4's "more"); sun #FFE2BC; exterior strength 3.2, turned 116 deg so its own sun agrees with ours (az -62); veneer black_walnut_veneer_02 (crown-cut), grain along the doors; toe-in 6; rug #8E8170 value 0.45; sun az -68. Merged main (vercel.json; the cover's cloth and the batts' shaders) |
| r5 | proofs/r5.png | 6.0 | c1 the cabinets acid-lime (warm sun, no blue); c2 rug brightest, "popcorn"; c3 covers flat; c4 veneer streaked; c5 no green on the floor; c6 exterior soft | found the veneer's streaks were a bug: a new bmesh face has no normal until updated, so every face of the credenza, books and sockets took its side-face UVs and the scan ran constant along the doors (the books' titles never showed either). Fixed; walnut_veneer_02, cathedral grain up the doors. Rug a herringbone wool flatweave; sun #FFE4C8 el 20; white balance 5300; exterior unblurred |
| r6 | proofs/r6.png | 6.0 | c1 sun az -55 so the green lands in frame; c2 tinted shadows; c3 rug darker, herringbone visible; c4 open the shadows; c5 gap between credenza and right speaker; c6 fill more raking; c7 white balance 5700 | **three passes (r4-r6 against r3) gained less than half a point: the concept changed.** Tried a backlit concept first (cA1: sun az -105 el 12, speakers 0.45 m off the wall): the batts stop most of the light and the cabinets go murky. Then concept B, below |
| r7 | proofs/r7.png (concept B: sheers over the glazing) | 6.5 | c1 sun onto the fronts (az -48, el 12); c2 cool fill 0.8; c3 exposure -0.75; c4 bounce 0.3; c5 rug warmer, deeper, back; c6 plaster bump up; c7 sheer over the jamb; c8 record player toward the centre | c1 with the sheers at 10% open put the cabinets in shade (murky, median 47); a kicker hidden behind each speaker did nothing (the batts stop light from behind: the cabinets glow only lit from the front and sides). So the sun must reach the pair: the sheers now leave two gaps where the beams to the speakers come in (two shafts of sun, the rest soft), sun back to az -62 el 14 at 34; c2-c5, c8 as given (rug kept 0.3 m clear of the feet); plaster bump 1.1 at 1.2 m |
| r8 | proofs/r8.png (two shafts through the sheers) | 6.5 | c1 white balance 4700 (Poison lime/olive in a warm grade); c2 plaster relief; c3 exposure -1.0 (sun patch on the shoulder at 233, flat); c4 rug darker, back; c5 floor oiled wide oak, window frame not black; c6 sun az -68 el 17 (horn shadow cut by the edge); c7 the chair as a soft foreground corner; c8 exterior calmer | all, with the sheers' gaps recomputed for the new sun (both frames); white balance 4800; plaster bump 2.4 at 0.8 m, tint 0.5; floor Poly Haven `wood_floor`, coat 0.15; frame #5A564F |
| r9 | proofs/r9-post.png (with the photographic finish, post.py) | 6.5 | c1 the window darker than the room (exterior 6.0, sky 1.0); c2 rug warmer, finer; c3 sun az -76 el 11 through the cabinets' open bays; c4 fill centred on the pair; c5 a bigger bounce for the horn throats; c6 heading over the upper-left wall; c7 floor bounce, the chair as a foreground corner; c8 the sliver of sheer at the edge. The critic also called the symmetrical frontal frame "a configurator view" | **r7-r9 flat at 6.5: the concept changed again (C, the window corner):** the camera, still squared and level, stands 0.55 m toward the glazing with a 35 mm lens, so the left wall and its view recede in the left third with the lounge chair by the glass; the pair and credenza moved 0.35 m clear of the window. c1-c5, c7 (floor bounce) as given; the rug finer (0.25 m tile) and warmer |
| r10 | proofs/r10-post.png (concept C, the window corner) | 6.0 | c1 sun az -62 el 18 so the horns' green lands on the wall; c2 the rug renders grey (its tint lost under the cool white balance), or drop it; c3 the void under the credenza; c4 the chair from behind, touching the left speaker; c5 plaster smeared; c6 the right side dim; c7-c8 exterior sharper and warmer | concept C scored no better and serves the brief less (smaller pair, a cropped chair), so back to the squared, centred frame of r9. Every critic since r2 has called the cropped rug strip and the cropped chair dead weight, and the floor in front of the pair is only about 0.75 m deep in frame: **the rug and the chair are out of the landscape**. c1, c3, c5-c8 as given, the sheers' gaps re-aimed |
| r11 | proofs/r11-post.png (centred, no rug or chair) | 6.5 | c1 sun from behind the pair (az -105) for green on the floor; c2 sunlit plaster flat at 241; c3 fill 1.3 for the covers' colour; c4 interiors lime: white balance 5200 and a green trim; c5 a calm top band; c6 the record player lost against the lit wall; c7 the long sill shadow across the floor; c8 the window's frame and forest too loud | c1 not taken (tried at r5 and as concept A: the batts stop light from behind and the cabinets go murky). c2 wall value 1.3 -> 1.05, bump 2.0; c3 fill 1.3; c4 white balance 5200 and a green trim of 0.15 in the finish (post.py: it moves dE little; the gap to #B2C9A2 is mostly lightness, the product's); c5 not taken (lowering the window heads takes the sun off the right horn); c6 record player to x 0.18 in front of the shaded wall, books right, the vase moved to the left end; c7 the front sheer 35% open; c8 frame #3A3733, exterior 4.0 |
| r12 | proofs/r12-post.png | 6.3 | c1 sun from behind (az -100) again; c2 caustics for green shadows; c3 sunlit plaster flat near white; c4 the same veneer figure on every door; c5 the white socket plates the brightest small things; c6 props bracketing a centred record player; c7 a shadow-gap skirting; c8 trim and vignette lighter | c1 and c2 not taken (backlight tried twice; the engine has no refractive caustics, and the cabinets' tinted shadows come through the volume where no batt stops them). c3 wall value 0.88; c4 one flitch laid on across the doors; c5 socket plates in a plaster tone; c6 record player centred, books left, vase right; c8 trim 0.1, vignette 0.18 |

**Duel 1** (blind, `duel-1.json`): r12 against finals31/room.png, both at 1440 x 810: **7.0 against 5.0, the new frame preferred.**
| r13 | proofs/r13-post.png | 6.5 | c1 green trim 0.3 (the cabinets neon); c2 a mullion's shadow splitting the left cover; c3 sun 48, 0.5 deg; c4 fill 2.2 on the shaded right; c5 the left horn's shadow behind the record player; c6 the window base crushed; c7 vignette 0.1 | c1, c3, c4, c6 (#5A5650), c7 as given; c2: the back bay's vertical bar taken out and the sun moved to az -68 el 14, the sheers' gap re-aimed (checked in a proof: both covers clear); c5 left (moving the pair apart would crowd the frame's edges) |

**Stopping.** Twelve passes on room 31's frames scored 6.0 to 6.5, through three concepts (hard sun across the room; sheers
with the pair in two shafts of sun; the window corner), while the duel against the frame being replaced went 7.0 to
5.0. Every critic named the same speaker items, out of scope here: the woofer cover as a flat disc, the batts as lime
blocks in direct sun, the horn throats crushed to black, the cabinets' black edges. Those now cap the score more than
the set does. The two-in-a-row 8.5 the protocol asks for is out of reach without changing the speaker, so the finals
were rendered from r13's settings with its fixes applied.
| r14 | proofs/r14-post.png (main merged: the cover's new melange cloth and rolled edge; model rebuilt) | 6.5 | c1 sun from behind again (az -105); c2 trim 0.5; c3 fill 3.5 from the right; c4 a waxed floor sheen; c5 the chair back as a foreground corner; c6 vase out of the horn's green beam; c7 window frame darker | the finals were already rendering from this rig. Two passes in a row under +0.5 after the concept changes (r13, r14): the coordinator's stopping rule. Not applied |

## Finals

- `renders/2026-10-18/barkhorn/room31/room.jpg`: 2880 x 1620, 512 spp (adaptive 0.01) with the denoiser, render 8,382 s
  (2 h 20 min on 4 cores), then the finish (`post.py`). The grained PNG came to 7.0 MB, over the 5 MB limit even
  optimised, so the frame ships as a quality-92 JPG (4:4:4, 1.3 MB), as the brief allows.
- `renders/2026-10-18/barkhorn/room31/room-portrait.png`: 1600 x 2000, 512 spp with the denoiser, render 6,518 s
  (1 h 49 min), rendered by a coordinator helper from 493b58f (its sun softened to 0.9 deg, below) and merged from
  `r31-room-portrait` (7696d54); 4.3 MB.

**Final critic** (blind, on the final itself, `critic-final.json`): **6.5**, score if fixed 8.0. Its changes: less fill
into the cabinets, so they show the sun's gradient instead of an even glow; green trim 0.55; the heading wall a little
darker; the left cabinet's top band in a mullion's shadow; a softer sun (0.9 deg) for the hard green-gold column the left
horn's light makes on the credenza's middle door; the plinth gap lifted; the camera 0.35 m right so the jamb leaves.

**Duels** (blind, side by side):
- duel 2 (`duel-2.json`): the final against finals31/room.png, both at 2880: **6.5 against 5.0, the final preferred**;
- duel 3 (`duel-3.json`): the final (at 1440) against r12, the best earlier frame and duel 1's winner: **6.5 against
  6.0, the final preferred**.

All three judges named the same artefact: the column of green-gold light on the middle door (real light, the left
horn's beam through its resin, but hard-edged enough to read as an error). A softer sun would fix it; that costs a
2 h 20 min re-render.

**The softer sun, tried.** All three judges flagged the column, so the landscape was rendered again with the sun at
0.9 deg and more floor bounce under the credenza (8,266 s). Blind critic on it (`critic-final2.json`): 6.5 again.
Blind duel against the 12:23 final (`duel-4.json`): **6.8 for the 12:23 final against 6.5**, preferred for its
crisper sun on the wall and floor. So `room.jpg` stays the 12:23 frame, and `room.json` is set back to it
(0.5 deg, floor bounce 0.55). The portrait, rendered from 493b58f, keeps its 0.9 deg sun (`PORTRAIT` in room.py),
which takes the column off its credenza.

## Scores, pass by pass

| pass | blind score |
|---|---|
| r1 (finals31, the frame replaced) | 4.5 |
| r2, r3 | 6.0, 6.0 |
| r4 | 6.5 |
| r5, r6 | 6.0, 6.0 |
| r7, r8, r9 (concept B) | 6.5, 6.5, 6.5 |
| r10 (concept C) | 6.0 |
| r11, r12, r13, r14 (B, centred) | 6.5, 6.3, 6.5, 6.5 |
| landscape final | 6.5 |
| landscape final, softer sun (not shipped) | 6.5 |

Duels: r12 vs finals31 7.0 to 5.0; final vs finals31 6.5 to 5.0; final vs r12 6.5 to 6.0; final vs softer-sun final
6.8 to 6.5.
