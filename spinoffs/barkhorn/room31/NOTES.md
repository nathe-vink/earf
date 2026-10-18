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

## The concept

References looked at first (Kinfolk and NORM-style interiors: toned plaster, bare walls, window light raking across
them, oak and walnut, a few real objects). One light idea: low late-afternoon sun (elevation 18 degrees) through a run
of tall French windows down the left wall, from in front of the pair (azimuth -58), so both speakers stand in it alike
(a sun from behind them could not reach the right one past the left one's shadow, or past the back wall) and each lays
its shadow, green where the light came through its horn and cabinet, on the plaster and floor behind it. A sun-free
window off to the right, out of frame, fills the shade side. The view out is a photographed autumn wood (Poly Haven
`autumn_forest_04`) on a plate only the camera sees, so it shows a real place without lighting the room twice.

Camera: 1.05 m high, squared to the back wall, 40 mm, level with a small rise of the lens (verticals straight); each
speaker about half the frame's height; the wall above for the heading.

Assets (all CC0): Poly Haven `laminate_floor_02` (oak boards), `beige_wall_001` (plaster), `walnut_veneer`,
`curly_teddy_natural` (the rug's pile), `modern_arm_chair_01` (the lounge chair), `ceramic_vase_02`,
`autumn_forest_04`. The record player is EARF's own Cumulus in Fog (from `r31-companions`, built here, not committed).

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
