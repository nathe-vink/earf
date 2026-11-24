# Hemisphere's top in even tiers: the redraw, after review 2 and checks 3 and 4 (v5, 2026-11-24)

PROPOSALS for the owner's question ("does it need that many tiers, or is there a way to make the tiers more even in
height and diameter difference?"). CAD: `crystal.py` (TOP_TIERS, GRIP, WHITE_SPLIT; `top` off by default); builds
`dome_pendant.py` (today) and `dome_pendant_topA.py`, `dome_pendant_topB.py` (out-dome-pendant, -topA, -topB: STEP, STL,
drawings, bom.csv); the path by `top_check.py`; heat by `hemisphere_thermal.py` (last table). Hemisphere only.

## 1. The shade release, fixed in the main build (all three tops)

Since 2026-11-11 the white disc under the hub was 95 across on the fixture; the collar's bore is 82, so the shade could
not come off (it needs 9.0 of lowering, 4.0 was free; top_check.py "today-as-built" still shows it blocked). Now V3's
default (`white_split=True`): a white disc 62 across on the fixture (the hub's own size, edge eased 0.5) and the collar
turned with an inward lip at its foot, bore 65 (1.5 radial to the hub and the disc, room for the shade's 1.35 to 1.5 of
tilt on the PEEK land; at the land's maximum tilt late in the lowering the lip comes within 0.13 to 0.42 of the disc:
a light rub at worst), led in 1 x 45, painted white beneath. From below: the lip and the disc read as one white face
with a 1.5 dark ring at r 31 to 32.5 (it was a 0.5 hairline in the first split). Lead-ins 1 x 45 on the PEEK land's
lower outer edge and the collar's top inner edge. The meshes, the render's copies and bom.csv are regenerated.

## 2. The rules the redraw keeps

1. Every fixture part from the collar's top to 9.5 above it stays inside the collar's 82 bore: the crown's first tier
   is 80 across, as today.
2. The clamp ring is 104 across (it screws on the collar's M96 thread). The even step is 24 across (12 per side).
3. The band the clamp ring presses onto the shade stays 116 across, as today, tapered from 5 thick at the clamp ring to
   a 1.0 land at its rim: the shade's foot ring, sloped, not one more step. Its face on the acrylic and the silicone are
   today's; under 0.5 MPa it bends 0.24 um (today 0.11), the same 2.2 MPa peak at its root.
4. The clamp ring screws down to a shoulder turned on the collar (Ø100, 86 to 92; the acrylic's hole 100.4, against
   today's 96.4), so its height, and the collar's top 0.5 over it, are held on the collar. The thread's run-out is a DIN
   76 undercut (Ø93.7, 92 to 95.75); the band's bore is relieved (Ø100.4) below 92, so only the ring is threaded. The
   collar's threaded length is 7.58 (A) and 4.75 (B); full-thread engagement with the ring 6.68 (A, about 4.5 turns) and
   3.85 (B, about 2.5; v6, the v5 check's (9)). The thread carries only the preload: the shade's weight rests on the collar's flange through the
   inner silicone, not on the thread. Lead-ins: the ring's bore at its leading edge (z 92), the collar's top
   outer edge down to the thread's root.
5. The squeeze is then set by the stack (the table below), not by torque.
6. The fixings (v5, after checks 3 and 4), for today's top, A and B alike (V3's default; crystal.py GRIP):
   - The cord grip: Lapp 53112005 as its datasheet gives it (DB53112005EN, as the reviewer read it; I could not open
     Lapp's page here: to confirm): M12 x 1.5, 16 across the flats with its corners turned to 17.6, 32.5 overall, 12 of
     thread, cord 3.5 to 7. The hub is tapped M12 13 deep from its neck's top (101.5, through the old Ø10 wire bore), so
     9.5 of its thread are in the hub and the rest through the crown's 2.5 floor; the cord's pull goes into the hub. Its
     seat 104, its top 124.5 under the cap's lid (125): the tiers did not move. It is turned by a slotted (pass-through)
     16 mm socket, the cord in its slot: the dome nut off, the body torqued into the hub, the dome nut on and tightened.
   - The crown sits on the neck metal to metal (a film of thermal compound; no pad, which would creep under the
     screws and the grip), held and keyed by three M2.5 countersunk screws at r 9.25, at 90, 210 and
     330 deg (clear of the cables), flush in its floor, their heads inside the Ø24 pocket.
   - The lamp hangs level from TWO cables, symmetric about the axis at r 17.5 (0 and 180 deg). Its centre of mass is on
     the axis (v5: today 1598 g at z 65.8, A 1679 g at 68.2, B 1577 g at 65.3, from the solids, the cables and their stud ends left out). One cable at r 17.5 would tilt
     it about 16 deg (16.2 / 16.8 / 16.1). With two it hangs level once their lengths are set equal at the canopy's
     locks: the lamp hung, a level across the rim, the two lengths equal to about ±0.25 mm (1 mm out tilts it about
     1.6 deg), the cord left slack. The cord carries current only (UL 153: an SPT-2 cord 2.5 lb, the lamp about 3.5).
   - Each cable is an nVent CADDY Speed Link SLK15L2SE250: 1.5 mm bare electrogalvanized wire (1.5 is its whole
     diameter; the Ø2.4 bores pass it; a coated cable must stay under 2.2), a 1/4 in threaded stud end, 44 lb rated at a
     5:1 static safety factor, cULus (its datasheet's table). The stud's
     length and its body's size are not on the sheet: drawn as a 1/4-20 thread 12 long under a Ø9 x 16 body with an 8 hex,
     to confirm on the part. It screws into the hub (1/4-20 tapped 13, its body in a Ø10 bore, its top 0.5 under the hub's
     face, Loctite 243), and the assembly is pull-tested. The wires run up Ø2.4 bores in the crown (4.3 clear of the
     pocket, their exits rounded) and through the cap's lid (today and A) or beside the cap (B: its Ø32 cap is too small
     to carry them with real walls, so the wires leave the crown's top just outside it) to the canopy. There each passes
     through its own SLK locking device (the system's rated wedge lock: it slides to shorten, holds under load, releases
     with its key), the two 35 apart either side of the cord grip, the tails looped round the strap. Kept at 35: 50 to 60
     would halve the sensitivity, but only with the cables out beside the cap, no longer one stem (check 4 (19)).
   - The cap is keyed to the crown by a Ø2 dowel and held down by a Ø2 x 2 magnet over a steel disc (both at r 14; in B
     their holes stand 1.0 from the pocket); its pocket Ø20 over the dome nut. In a swap, hold the cap: keyed to the crown,
     it is the handle (check 4 (18): at the 9.0 lift the collar's top leaves only 2.5 / 1.84 mm of the crown's Ø80 tier
     in today's top and A, a pinch point; B's Ø56 tier stands 6.5 clear).
   - The order: the hub; the two stud ends into the hub; the crown down over the wires onto the neck, its three screws;
     the grip, as above; the cap down over the cord (and the wires) onto its dowel; the cables through the locks in the canopy, levelled.
   - The shade's tether, drawn: an M3 eye screw radially into the hub at z 81 (between the lip's highest point in the
     lift, 75, and the PEEK ring, 86), at 90 deg (clear of the slots and pins); a 1 mm stainless tether with a snap hook to
     an eye turned on the collar's bore at z 68, above the lip. In a swap it is unhooked once the shade is turned and
     lowered a hand's width.
   - The bayonet's pins are a custom turned part (no catalogue pin matches the CAD): stainless 303, a Ø4 shoulder 4.2
     long, an M3 thread 15.8 long through a Ø3.2 clearance in the PEEK and 6 into the hub.
7. The clamp thread's run-out is a DIN 76 undercut on the collar (Ø93.7, 92 to 95.75, 2.5 pitches); the ring's thread
   has a 1 x 45 lead-in.
8. South's slot entries (dropped in round 38) are left out of the collar with the lip (they cut it, seen from below).

## 3. The squeeze, with the ring's height held on the collar

The flange-to-band distance is fixed at 16.0 (radial). The acrylic is 12 nominal (skin 3, liner 6, shell 3); the two
1 mm air gaps at the crown take silicone shims, so four silicone rings share the rest.

| Sheet thickness | Four rings each, no shims | Nominal | RSS | Worst case |
|---|---|---|---|---|
| ISO 7823-1 (±1.4 RSS, ±2.4 worst) | 1.3 | 23 % | loose (−4) to 50 % | loose to 69 % |
| ISO 7823-1 | 1.5 | 33 % | 10 to 57 % | loose to 73 % |
| ±5 % (if held by the supplier) | 1.3 | 23 % | 16 to 30 % | 12 to 35 % |
| ±5 % | 1.5 | 33 % | 27 to 39 % | 23 to 43 % |

(Rounds before v5 wrote ±10 % for the first two rows; the standard's figure is wider, so fixed rings cannot hold it.)

Cast sheet is held only to ±(0.4 + 0.1t) (ISO 7823-1): ±0.7, ±1.0 and ±0.7 for the three sheets here (±2.4 at worst,
±1.4 RSS). So the squeeze is set per shade: two 1.3 gaskets and two shims, the shims picked from 0 (left out), 0.5, 1.0,
1.6, 2.2 and 2.9 from the measured crown stack so the squeeze lands at 20 to 35 % over the whole RSS range (at the
thinnest worst-case stack it reaches 38 %): a process step in the BOM (hemi-gaskets-4). A 0.25 PTFE slip washer sits
under the clamp ring's band, which turns against it while tightening. (Today's top keeps two 1.0 gaskets and the torque.)

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
| Hub, 35 C room (today 50.6) | 50.3 C | 50.2 C (the heat model counts the tiers' outsides; the v5 neck and floor change nothing it counts) |

Both change every shade's collar and clamp ring (and its crown hole). Both come off by solids (top_check.py: hanging seated, lifted 8.0 and 9.0, turned, lowered past the pins and
on 140 down past the carrier; the control, lowered 3 unturned, is held by the pins).

The sheet: top-sheet-v4.jpg (its renders' commands: v4.sh).

## 5. v5 additions (check 4)

- The white faces (a Ø62 disc on the hub and a lip on the collar, bore 65, both inside the shade's top) show only where
  the hub is seen from below or cut open: the cutaway 'How it lights'
  (renders/2026-11-12/barkhorn/lamp-site/legible/hemisphere-ember-cutaway.png) and the from-below views on the sheet.
  The level and in-use views do not show them (behind the opal, or out of sight). The paint is in the BOM, in the
  parts' notes: the disc white powder coat (white-disc), the lip painted white beneath on the black-anodised collar.
- The render's collar shader had a units bug (its white test read 0.080 against mm coordinates, 80.0); fixed, so v5
  frames paint white only the lip's underside (normal z < −0.3).
- What B gives up for its Ø32 cap: the two cables leave the crown beside the cap, not through it, and the cap's Ø2 key
  and magnet holes at r 14 stand 3.0 from its Ø20 pocket but only 1.0 from its outside (5.0 in today's Ø40 cap, 13 in A's
  Ø56). The crown's cable bores stand 4.3 from the
  pocket in all three.
- Hanging weights for v5 (section 2, rule 6): 1598 / 1679 / 1577 g, from the rebuilt solids (v4: 1601 / 1682 / 1581).
- The heat row is not rerun: the heat model counts the tiers' outer areas and their stack, which v5 does not change.
- The coordinator's v4 check, items 16 to 23:
  - (16) The tether's snap hook is drawn: a Ø6 ring of 1.0 wire through the collar's eye, now a 2 mm tab with a Ø1.6
    hole at r 39.5, z 68. In the swap: turn the shade, lower it a hand's width, unclip the hook; no tools.
  - (17) The cable is bare: 1.5 is its whole diameter (electrogalvanized, no coating), through Ø2.4 bores; the stud end
    comes swaged on by nVent. A black-coated cable must stay under 2.2 outside.
  - (18) The cap is the handle in a swap (keyed to the crown by its dowel).
  - (19) The spacing stays 35; the gripper is the SLK's own locking device, one per cable, in the canopy.
  - (20) fixings_check.py (spinoffs/barkhorn/companions) checks every part of the top against every other at zero
    tolerance. The only overlaps left are threads in their tapped holes, at the volumes their engagement gives (the two
    studs 270 mm3, the three crown screws 24, the three pins 39, the eye screw 3). It found the tether drawn into the
    collar's eye; fixed with the tab and the hook.
  - (21) No pad: the crown sits on the neck metal to metal with a film of thermal compound (a pad would creep under the
    screws and the grip). The CAD always drew it so; the texts now agree.
  - (22) The thread engagement and the load path are corrected in rule 4; the cord's BOM row now names the two cables
    and the grip under the cap.
  - (23) The screws went to 90/210/330.

## 6. v6: the hanging (the v5 check, items 1 to 16)

The fixings of section 2, rule 6 are replaced where this section differs.

- (1) THE ANCHOR, a part whose maker publishes its shape. Each cable is 1/16 in (1.59) 7x7 stainless (Cable Grippers Inc.'s
  bulk cable). Its hub end is a Nicopress 871-1-C copper stop sleeve, swaged with the 51-C-887 tool. Nicopress's own data
  sheet names the part and the tool; its size (13/64 x 7/32 in, about Ø5.2 x 5.6) and its 430 lb typical holding strength
  come from a distributor's copy of Nicopress's table, to confirm. It bears up under a Ø5.6 x 6 counterbore in the hub's
  bottom face. In V3 (the light on a stem) the hub is solid there from z 60 to the neck, so the cable runs up a Ø2.4 hole
  through it, then through the crown and the cap. The white disc closes the counterbores. No turning, no thread, no tool
  inside the lamp. The old stud's tap ran into the hub's light chamber; it is gone.
- (2) THE CANOPY, right side up: open at the top against the ceiling, its 3 mm floor closed below with the cord's gland in
  its centre. The canopy is a cover, held to the strap by two flush black set screws in its wall; the strap carries the
  load. The locks are Cable Grippers MGR-M10-MM. Their chart gives 17.1 mm long without the plunger, a Ø11.9 body and an
  M10 thread. Their table gives MGR on 1/16 in stainless 7x7 as 312 lb minimum break in independent tests, 50 lb a cable
  at 5:1, against the lamp's 3.7 lb on two. Each is threaded up into a steel L bracket under the strap, plunger down, 1 mm
  above a Ø6 hole in the canopy's floor. The cable passes through that hole: push the plunger from below and the cable
  slides; let go and it grips. The grippers sit at r 40, clear of the driver's enclosure, which is now turned across the
  cables' line (64 along it, 92 across). The cables splay from their exits (r 16; B r 18.5) to r 40. With the splay, 1 mm
  of length difference tilts the lamp 1.46 / 1.47 / 1.39 deg (today, A, B; parallel cables would give 1.79 / 1.79 / 1.55).
- (3) THE CORD is set 2 mm longer than the cables between its grips. The cables stretch about 0.05 mm under the lamp, so
  the cord carries none of it. Over the 600 drop it bows about 21 mm to one side, and is drawn so. Installing: the lamp
  hung and levelled on the cables, feed the cord until it bows, then tighten the canopy's grip.
- (4) THE TETHER: 1.5 mm 7x7 stainless rope, 125 mm between its two screws.
  - The hub end: an M4 button screw radially into the hub at z 80, 90 deg, clamps a crimped loop, the hub's eye. That is
    above the lip's 75 in the lift and under the PEEK's 86.
  - The clip: a 4 x 40 stainless snap hook (DIN 5299 C) on that eye. It stands on the lip's top along the bore, its ends at
    r 38.8 and its middle at r 33.3.
  - The rope runs round the lip's top, under the pins and the land, to an M3 button screw through the collar's wall at
    z 70, 270 deg. That hole is tapped through from outside, under the shade's flange. The v5 eye tab is dropped.
  - Clearance: the shade turns and lowers 100 mm before the rope goes taut.
  - In a swap: lower the shade a hand's width, then unclip at the hub, which is then clear of the collar. The step is in
    NOTES_DOME.
  - If the bayonet failed, the shade's drop onto the tether peaks at about 1.3 kN. That is a stiff elastic estimate that
    leaves out the rope's own give. It is under the rope's 2.2 kN (a seller's figure) and the snap's 1.9 kN (the lowest
    seller listing; sellers list 1.9 to 5.8 kN). It holds once; it is not a margin of 10.
- (5) The cables render bare stainless grey; the copper sleeves are hidden in the hub.
- (6) The clamp ring's lead-in is now cut after the band's union.
- (7) Thin walls:
  - Today's and A's cables sit at r 16, so today's Ø40 cap keeps 2.8 mm round them.
  - B's cables sit at r 18.5, 1.3 mm clear of its Ø32 cap's side.
  - The dowel and magnet sit at r 15.5, 2.5 mm from the crown's Ø24 pocket.
  - B's cap is held by a Ø1.5 magnet at r 14 only (1.25 mm from the pocket and the fillet), with no dowel.
- (8) The swap: hold the cap in today's top and A; hold the Ø56 tier in B. The texts now agree: crystal.py, NOTES_DOME,
  the cap's note and this note.
- (9) Texts and BOM:
  - The clamp's note is now the shoulder and the shims; torque applies to today's top only.
  - The PTFE slip washer is drawn and is a BOM row (hemi-slip-washer); in the drawing it takes 0.25 of the outer gasket's
    1.0.
  - The silicone row lists the shim set.
  - The suspension row is rewritten.
  - NOTES_DOME names the grippers and the pull test.
  - The thread engagement is 6.68 (A) and 3.85 (B).
- (10) The build's clash check no longer exempts any fixing:
  - Tapped holes are drawn at the thread's major Ø, so threads touch and never overlap.
  - fabkit builds all three tops with 0 clashes.
  - fixings_check.py reports no overlap at zero tolerance.
  - dome_pendant_v2 and South keep the old pairs (TOUCHING_DOME_LEGACY).
- (11) to (13) The sheet:
  - The 35 deg view is cropped above the shade, where the cord and cables ended in mid-air.
  - The footer's sentence on the crown's inside is gone.
  - The dome is shot at Blender's neutral (6500 K, tint 10).
- (14) The white paint is a BOM row (hemi-white-paint): the disc's powder coat, and the lip masked and painted beneath.
- (15) The collar's white is limited to its painted faces in every render, with or without HEMI_COLLAR_CAP. For pass v2:
  every lit picture made since 2026-11-10 drew those faces black, so the lit pictures join the re-render list.
- (16) The weights now include the cables inside the lamp and the sleeves (section 7).

## 7. v6 weights (the v5 check's (16))

From the v6 solids, everything that hangs from the cables: today 1620 g at z 66.0, A 1701 g at 68.4, B 1598 g at 65.5. These
include the tether and its snap, the slip washer, the two stop sleeves and the cables inside the lamp (2.2 g); v5 left out
its stud ends. The cables' own weight above the lamp hangs from the grippers. The lamp is about 3.7 lb, on two cables rated
50 lb each.
