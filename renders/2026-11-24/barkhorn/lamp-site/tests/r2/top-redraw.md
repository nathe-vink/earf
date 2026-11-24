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
6. The fixings (as of v7), for today's top, A and B alike (V3's default; crystal.py GRIP and its comment):
   - The cord grip: Lapp 53112005 (M12 x 1.5, 16 AF, 32.5 overall, 12 of thread), tapped 13 deep into the hub from the
     neck's top, 9.5 of its thread in the hub; turned by a slotted 16 socket.
   - The crown sits metal to metal on the neck (a film of thermal compound, no pad), held by three M2.5 countersunk
     screws at r 9.25, 90/210/330 deg.
   - The cap: today's and A's keyed by a Ø2 dowel and held by a Ø2 magnet at r 15.5, the handle in a swap; B's held by a
     Ø1.5 magnet only, its Ø56 tier the handle.
   - The hanging (sections 6 and 8): two 1/16 in stainless cables on Nicopress stop sleeves in the hub's bottom face, up
     through the hub, crown and cap (beside B's cap), splayed to Cable Grippers MGR-M10-MM grippers at r 48 in the canopy,
     on U brackets riveted under its mounting plate; the cord 2 mm slack.
   - The detent: an M5 ball spring plunger in the PEEK ring (90 deg, z 93), its ball in a dimple in the collar's bore.
   - The shade's secondary retention: being redesigned (section 8).
   - The bayonet's pins: custom turned (stainless 303, a Ø4 shoulder, M3 thread 15.8 long), in M3 holes 7.5 deep.
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

## 8. v7 (the v6 check, items 1 to 14)

- (1), (2) THE SECONDARY RETENTION.
  - Why the tether went: it blocked the swap. Its snap, on the lip under the PEEK ring, let the shade rise only about 6.0 of
    the 7.5 to 8.0 needed. Its parts weren't rated for a drop: the rope breaks at 1.26 to 1.37 kN, and the snap's maker
    rates it 500 N static.
  - The alternative anchor, under the hub, would hang it in the ring board's light.
  - So the coordinator decided (17:39 UTC) on a positive lock in place of the tether. The tether is gone: its parts,
    screws, BOM row and texts.
  - THE LOCK: Ganter GN 617-5-M10X1-AK, an indexing plunger with no rest position, so it cannot be left pulled. JW Winco's
    table gives a Ø5 H7 pin, M10 x 1, a Ø21 knob, about 45 overall, a 5 stroke and a spring of about 7 N rising to 17 N.
  - Where it sits: threaded radially into the collar's wall at 105 deg, z 96.5, through a Ø10.5 hole in A's clamp ring.
    The hole is drilled through the collar's M10 hole once the ring is screwed down to its shoulder. The lock nut sits on a
    Ø20 spot face.
  - What it blocks: its pin enters a Ø5.1 hole in the PEEK ring, to r 36.3, so with the knob released the shade cannot be
    lifted, turned or lowered. top_check: lifted 1, 20 mm3 into the ring; turned 2 deg, 28 mm3.
  - Swapping: pull the knob, lift, turn, lower. Pulled, its tip stands at r 41.3, clear of the land (r 40.8) and the crown
    (r 40). top_check runs the whole swap with it pulled: A comes off.
  - Fitting: pull it, lift, turn, let go. It springs into its hole as the shade settles home. The PEEK ring's top outer
    edge is led in 1.2 x 45, so a pin let go early rides down onto the land.
  - Reach: the knob stands at the back of the top (r 66 to 81), opposite the level views' camera, where the crown hides it.
    A hand reaches it over the shade from behind; the section drawing shows the path.
  - Light path: none of the lock is in it, and none of it shows from below.
  - Balance: the lock (about 30 g at r 60) moves A's centre of mass 1.2 off the axis. Across the two cables' line it would
    tip the lamp about 1.1 deg, and the levelling could not take it up. So A's cables are turned to 105/285 deg, the lock's
    line: the offset now lies along them (0.00 across), and the levelling takes it up (about 0.9 mm of cable). The canopy's
    grippers, brackets and enclosure turn with them, and the cap's key and magnet move to 15/195 deg, clear of the cables.
    In the level views, A's two cables now stand nearly one behind the other.
  - ONLY A TAKES IT. Its M10 needs a clamp ring at least 10.5 tall, and today's is 5 and B's 8. The collar under them is
    covered by the acrylic. Today's top and B keep the bayonet with an M5 ball detent and have no positive lock. That is
    open, if either is picked.
  - (7) THE SHADE UNDER GRAVITY ALONE, the lock never engaged: it hangs on its three pins, each seated against its notch's
    top (z 95.5 in the collar's frame) by the shade's weight. To leave, the shade must be lifted 8.0 to 9.0 against its
    weight into the turn passage (82.5 to 87.5), turned 30 deg and lowered; nothing moves it the other way. top_check's
    control: lowered 3 unturned, the pins hold it (99 mm3 into the collar). The pins are Ø4 stainless shoulders: about 4 kN
    each in shear, against 11 N. The lock adds a block against a release by hand (cleaning, a half-finished swap), which
    the J-slot alone does not stop.
- (3) THE CANOPY. The strap is now a round mounting plate, 1.6 steel, Ø140, with a rim turned down 12, screwed to the 4 in
  box by its two 8-32 screws at y -+44.45 (drawn).
  - The driver's enclosure hangs on four 6 mm standoffs below the plate, so the screws' heads sit in the gap. It goes on
    after the plate is screwed up.
  - The grippers sit at r 48. Each is threaded up through the 24 x 24 foot of a U bracket and held by an M10 nylon-insert
    nut (ISO 10511, 16 AF, 8 tall, its own part).
  - Each bracket's legs run across the cables' line, so the nut is open to a spanner from both sides. Its inner leg is
    2.4 mm from the enclosure.
  - The brackets' two inward flanges are riveted under the plate by four Ø3.2 blind rivets each (drawn).
  - The canopy hangs on two M4 x 8 flush set screws (90/270 deg) into clinch nuts in the plate's rim (drawn).
- (4) LEVELLING. Each gripper's knurled safety nut is drawn. The procedure, in crystal.py, NOTES and the BOM:
  1. Screw the plate to the box and hang the lamp, with the canopy resting on the cables below the plate.
  2. Loosen each safety nut, push the plunger and slide the cable until a 200 mm level across the rim reads level to 1 deg
     (the rim's sides within 3.5 mm of each other below the ceiling).
  3. Tighten the safety nuts.
  4. Set the cord's 2 mm of slack and tighten its grip.
  5. Slide the canopy up and fix its set screws.
  The cable tails, about 50 mm, coil in the brackets. With the grippers at r 48, 1 mm of cable tilts the lamp
  1.27 / 1.29 / 1.29 deg (today, A, B), about 4.5 mm across the rim.
- (5) THE STOP SLEEVE.
  - Nicopress gives a stop sleeve about 50 % of the cable's rated break, typical: about 1.07 kN on 1/16 7x7. The 430 lb
    figure had no source and is gone.
  - Each cable assembly is proof-loaded to 90 N (5 x the lamp) for 1 min before fitting.
  - The counterbore is now 8 deep, against the sleeve's 5.6 before swaging, which lengthens it.
- (6) B's cables now sit at r 17.6. That leaves 1.2 mm of the Ø40 neck round each hole and 0.8 mm clear of the Ø32 cap.
- (7) THE PAINT: every down-facing face of the collar below z 80, about 8,460 mm2:
  - the foot beneath the lip (r 33.5 to 48), and
  - the flange's inner face under the shade (r 48 to 58).
  The render already painted these, and NOTES and the disc's note said so. The BOM now agrees, and the CAD draws the
  paint as a 0.05 mm film (white-paint), so its own render export shows it. The photometry is rerun with the pass v2 list
  (item 13), from the same painted faces.
- (8) Texts and BOM:
  - The brackets have their own row; the set screws and clinch nuts, the M10 nuts, the rivets and the box screws are rows.
  - The grippers' price is the pair.
  - Section 2's rule 6 is rewritten.
  - NOTES names the Ø62 disc and the painted lip and flange face.
  - The sheet says "between".
  - The squeeze reads "each 1.3 free" next to the shims, "the outer gasket drawn at 0.75 under the slip washer", and 38 %
    at the thickest stack.
- (9) THE DETENT (today's top and B; A has the lock) is drawn: an M5 x 12 ball spring plunger through the PEEK ring at 90 deg, z 93, its end in a Ø5.4
  clearance in the hub, its ball tip in a Ø2.6 dimple in the collar's bore. It is clear of the pins' taps (30/150/270).
- (10) The pins' M3 holes are 7.5 deep for 6.0 of thread, so each pin seats on its shoulder.
- (11) THREAD CALLOUTS (size, drill, depth) are in the notes of the hub, ring, collar, crown, canopy, plate and brackets,
  and so on the drawings' notes.
- (12) The section drawing is redrawn: the legend outside the plot, the missing parts and their names, dimensions.
- (13) Pass v2's re-render list: pass2/RERENDER.md. It covers the frame kinds hemisphere() draws, every Hemisphere
  picture committed in the window, and the photometry files. The CAD's render export now draws the cables stainless and
  the paint white.
- (14) The sheet says which top has the lock. B's header gains its cables beside the cap, its magnet-only cap and its Ø56 handle.
- Zero clashes: fixings_check.py over all three tops, with the lock, plunger, ring, clamp, nuts, rivets, screws and paint added.
- The notes not acted on (no action unless cheap): the crown's 0.61 land by each countersink, B's magnet pocket 0.45 to
  0.56 from the cap's edge, and B's cap unkeyed. They are as they were, and the last is now stated as B's choice.

## 9. v7 weights

From the v7 solids, the cables inside the lamp included: today 1608 g at z 65.9, A 1717 g at z 68.8 (1.2 off the axis
along its cables: the lock), B 1586 g at z 65.4. The tether is gone; A carries the lock, and today's top and B the
detent.
