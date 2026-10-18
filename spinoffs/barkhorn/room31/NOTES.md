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
