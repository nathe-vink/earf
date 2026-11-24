# Hemisphere's top in even tiers: the redraw, after review 2 (2026-11-24)

PROPOSALS for the owner's question ("does it need that many tiers, or is there a way to make the tiers more even in
height and diameter difference?"). CAD: `crystal.py` (TOP_TIERS, GRIP, WHITE_SPLIT; `top` off by default); builds
`dome_pendant.py` (today) and `dome_pendant_topA.py`, `dome_pendant_topB.py` (out-dome-pendant, -topA, -topB: STEP, STL,
drawings, bom.csv); the path by `top_check.py`; heat by `hemisphere_thermal.py` (last table). Hemisphere only.

## 1. The shade release, fixed in the main build (all three tops)

Since 2026-11-11 the white disc under the hub was 95 across on the fixture; the collar's bore is 82, so the shade could
not come off (it needs 9.0 of lowering, 4.0 was free; top_check.py "today-as-built" still shows it blocked). Now V3's
default (`white_split=True`): a white disc 62 across on the fixture (the hub's own size, edge eased 0.5) and the collar
turned with an inward lip at its foot, bore 65 (1.5 radial to the hub and the disc, room for the shade's 1.0 to 1.3 of
tilt on the PEEK land), led in 1 x 45, painted white beneath. From below: the lip and the disc read as one white face
with a 1.5 dark ring at r 31 to 32.5 (it was a 0.5 hairline in the first split). Lead-ins 1 x 45 on the PEEK land's
lower outer edge and the collar's top inner edge. The meshes, the render's copies and bom.csv are regenerated.

## 2. The rules the redraw keeps

1. Every fixture part from the collar's top to 9.5 above it stays inside the collar's 82 bore: the crown's first tier
   is 80 across, as today.
2. The clamp ring is 104 across (it screws on the collar's M96 thread). The even step is 24 across (12 per side).
3. The band the clamp ring presses onto the shade stays 116 across, as today, tapered from 5 thick at the clamp ring to
   a 1.0 land at its rim: the shade's foot ring, sloped, not one more step. Its face on the acrylic and the silicone are
   today's; under 0.5 MPa it bends 0.24 um (today 0.11), the same 2.2 MPa peak at its root.
4. The clamp ring screws down to a shoulder turned on the collar (Ø100, 86 to 92; the crown's hole 100.4), so its
   height, and the collar's top 0.5 over it, are held on the collar. Its thread starts above a relief groove (Ø94.5, 92
   to 93.2); the band's bore is relieved (Ø100.4) below 92, so only the ring is threaded: 10.8 long (A), 8.0 (B), less the
   run-out.
5. The squeeze is then set by the stack (the table below), not by torque.
6. The cord grip is a real part, Lapp 53112005 (M12 x 1.5, nickel-plated brass, cord 2.5 to 6.5, 15 across the flats,
   21 over its seat, 6 of thread; from DigiKey's listing of its datasheet, the datasheet itself not opened here: to
   confirm). The tiers did not need to move: it threads through the crown's 1 floor (102.5 to 103.5) into the hub
   (5 of thread in the aluminium), so the fixture hangs from the hub and the grip clamps the crown down on its pad;
   its body stands in a 21 pocket, its top 124.5 under the cap's 1.0 lid (125).
7. The cap screws onto an M26 x 1 spigot on the crown (no screws through its wall; B's cap wall over the thread about
   2.4, enough for a cap that carries nothing). The order: the hub; the crown on its neck; the grip through the floor
   into the hub, tightened with a thin-wall 15 socket down the pocket; the cord through it and its dome nut tightened;
   the cap screwed on.
8. The suspension cable is the default (the fixture is about 3.5 lb, the SPT-2 cord carries 2.5): its swaged ferrule
   in a counterbore in the hub's neck under the crown's floor at r 9.5, the cable up the pocket beside the grip and out
   through the cap's lid; far above the lip's travel (z 64 to 75).

## 3. The squeeze, with the ring's height held on the collar

The flange-to-band distance is fixed at 16.0 (radial). The acrylic is 12 nominal (skin 3, liner 6, shell 3); the two
1 mm air gaps at the crown take silicone shims, so four silicone rings share the rest.

| Sheet thickness | Four rings each | Nominal | RSS | Worst case |
|---|---|---|---|---|
| ±10 % | 1.3 | 23 % | 9 to 37 % | 0 to 46 % |
| ±10 % | 1.5 | 33 % | 21 to 46 % | 13 to 53 % |
| ±5 % | 1.3 | 23 % | 16 to 30 % | 12 to 35 % |
| ±5 % | 1.5 | 33 % | 27 to 39 % | 23 to 43 % |

So holding the height needs the shade maker to hold the crown's sheet within about ±5 % (or to choose the shims per
shade). The other way, torqued as today, lets the collar's top float: 0.5 proud nominal, ±1.4 at worst (±10 % sheet).

## 4. The two

| | Three even tiers (A) | Four even tiers (B) |
|---|---|---|
| Tiers, mm across x tall | 104 x 11.33, 80 x 11.33, 56 x 11.33 | 104 x 8.5, 80 x 8.5, 56 x 8.5, 32 x 8.5 |
| Steps | 24 across (12 per side) | 24 across (12 per side) |
| Collar's top | 103.33 | 100.5 |
| Lifted, from where it hangs | 8.0 to 9.0 | 8.0 to 9.0 |
| Lowered to come off | 12.8 | 10.0 |
| Weight per shade (collar, clamp ring) | +25 g | +1 g |
| Weight, fixture (crown, cap, hub) | +47 g | -31 g |
| Grip (both) | 33 g brass | 33 g brass |
| Hub, 35 C room (today 50.6) | 50.3 C | 50.2 C |

Both change every shade's collar and clamp ring (and its crown hole), so a shade of one top does not fit another's
fixture. Both come off by solids (top_check.py: hanging seated, lifted 8.0 and 9.0, turned, lowered past the pins and
on 140 down past the carrier; the control, lowered 3 unturned, is held by the pins).

The sheet: top-sheet-v3.jpg.
