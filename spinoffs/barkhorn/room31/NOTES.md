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
