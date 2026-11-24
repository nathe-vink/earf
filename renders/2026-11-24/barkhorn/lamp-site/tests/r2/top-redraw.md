# Hemisphere's top in even tiers: the redraw, after review 2 and check 3 (2026-11-24)

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
6. (Check 3) The fixings, for today's top, A and B alike (`fixings`, V3's default; crystal.py GRIP):
   - The cord grip is Lapp 53112005 as its datasheet gives it (DB53112005EN, as the reviewer read it; I could not open
     Lapp's page here: to confirm): M12 x 1.5, 16 across the flats, 17.6 across the corners, 32.5 overall, 12 of thread,
     cord 3.5 to 7. The hub is tapped M12 13 deep from its neck's top (101.5), so all its thread is in the aluminium and
     the cord's pull goes straight into the hub. Its seat 104, its top 124.5, under the cap's 1.0 lid (125): the tiers
     did not move. Its body is drawn as the hex and a round dome to the overall height (its outline to confirm).
   - The crown sits on the neck on its pad, its 2.5 floor held by three M3 x 8 countersunk screws at r 9.25 into the
     neck (keyed and held; flush, so the grip's hex and the socket pass over them).
   - (Addendum (g)) The lamp hangs from TWO suspension cables, symmetric about the axis (0 and 180 deg at r 14), so it
     hangs level. Its centre of mass is on the axis: today 1601 g at z 65.7, A 1682 g at 68.2, B 1581 g at 65.3 (from
     the solids). One cable off the axis would tilt it until that point is under the cable's exit: at r 14, 13.1 / 13.6 /
     13.0 deg (the rim 23 to 24 mm higher on one side). With two, it hangs level; 1 mm of difference in their lengths
     tilts it about 2.0 deg, so the two grippers in the canopy are set to equal length when the lamp is hung. The cord
     carries current only (UL 153: an SPT-2 cord 2.5 lb, the lamp about 3.5).
   - Each cable ends in a swaged M4 x 0.7 threaded stud (a rated part from the cable's maker; Lexco lists an M4 x 0.7
     threaded plug and advises a pull test of the assembly: to confirm for 1.5 mm cable), screwed 8 into the hub, its
     top 4 above the neck in a Ø5 bore in the crown, far above the lip's travel (it ends at 75). The cables run up Ø2
     bores through the crown and the cap's lid, in the crown's metal outside the grip's pocket.
   - The crown is keyed and held by its three screws, not by the cables (a turn of the crown cannot kink them).
   - The cap rests on the crown, located by the cord and the cable through its lid, held down by its own weight (the
     lamp hangs; nothing pulls the cap up). No screws, no thread.
   - The pocket Ø24 takes a thin-wall 16 socket (about 22.5 across) for the grip's body and then its dome nut, clear of
     the countersunk heads; the cables are outside the pocket. The hub is tapped M12 13 deep (to 88.5, through the old
     Ø10 wire bore), so all 12 of the grip's thread are engaged (9.5 in the hub, 2.5 through the crown's floor).
   - The order: the hub; the two studs screwed into the hub; the crown lowered over the cables onto the neck, its three
     screws; the grip screwed into the hub and tightened with the socket down the pocket; the cord through it, its dome
     nut tightened with the same socket; the cap lowered over the cord and the cables; the grippers in the canopy set to
     equal length, the lamp level.
   - (Addendum (l)) The bayonet's pins are a custom turned part (no catalogue pin matches the CAD): stainless 303, a Ø4
     shoulder 4.2 long, an M3 thread 15.8 long through a Ø3.2 clearance in the PEEK (now drawn so) and 6 into the hub.
7. The clamp thread's run-out is a DIN 76 undercut on the collar (Ø93.7, 92 to 95.75, 2.5 pitches); the ring's thread
   has a 1 x 45 lead-in.
8. South's slot entries (dropped in round 38) are left out of the collar with the lip (they cut it, seen from below).

## 3. The squeeze, with the ring's height held on the collar

The flange-to-band distance is fixed at 16.0 (radial). The acrylic is 12 nominal (skin 3, liner 6, shell 3); the two
1 mm air gaps at the crown take silicone shims, so four silicone rings share the rest.

| Sheet thickness | Four rings each | Nominal | RSS | Worst case |
|---|---|---|---|---|
| ±10 % | 1.3 | 23 % | 9 to 37 % | 0 to 46 % |
| ±10 % | 1.5 | 33 % | 21 to 46 % | 13 to 53 % |
| ±5 % | 1.3 | 23 % | 16 to 30 % | 12 to 35 % |
| ±5 % | 1.5 | 33 % | 27 to 39 % | 23 to 43 % |

Cast sheet is held only to ±(0.4 + 0.1t) (ISO 7823-1), about ±10 % here, so the squeeze is set per shade: four silicone
rings, Shore 40, 1.3 free (drawn at 1.0), and the shims picked per shade (1.0, 1.3 or 1.6) from the measured crown
stack so the squeeze lands at 20 to 35 %: a process step in the BOM (hemi-gaskets-4; the gaskets' part note). The other way, torqued as today, lets the collar's top float: 0.5 proud nominal, ±1.4 at worst (±10 % sheet).

## 4. The two

| | Three even tiers (A) | Four even tiers (B) |
|---|---|---|
| Tiers, mm across x tall | 104 x 11.33, 80 x 11.33, 56 x 11.33 | 104 x 8.5, 80 x 8.5, 56 x 8.5, 32 x 8.5 |
| Steps | 24 across (12 per side) | 24 across (12 per side) |
| Collar's top | 103.33 | 100.5 |
| Lifted, from where it hangs | 8.0 to 9.0 | 8.0 to 9.0 |
| Lowered to come off, from the drawn pose (from where it hangs) | 12.33 (11.83) | 9.5 (9.0) |
| Weight per shade against today (collar, clamp ring; silicone) | +22 g; +6 g | −2 g; +6 g |
| Weight, fixture against today (crown, cap, hub) | +64 g | −13 g |
| The grip, screws and cable stud | as today's (check 3's fixings are in all three) | the same |
| Hub, 35 C room (today 50.6) | 50.3 C | 50.2 C |

Both change every shade's collar and clamp ring (and its crown hole). Both come off by solids (top_check.py: hanging seated, lifted 8.0 and 9.0, turned, lowered past the pins and
on 140 down past the carrier; the control, lowered 3 unturned, is held by the pins).

The sheet: top-sheet-v4.jpg (its renders' commands: v4.sh).
