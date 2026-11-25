# V12 for the Hemisphere top (the pick: A without the lock), 25 Nov 2026

From the V11 check of r32 a56c5b8bd6 (wf_6b9b1945-df3: four critics, four skeptics; full result `coordinator/hemisphere-top-v11-critics-2026-11-25.json`), with f7ede2f179 (the tie slots and dimples, drawn after a56c5b8bd6 and outside the check) read against it. Where a skeptic overruled its critic, this list takes the skeptic's view. Line numbers are at a56c5b8bd6, as the reviewers give them. f7ede2f179 adds 7 lines to crystal.py after line 999, so crystal.py's later lines are 7 higher there. This list was itself checked against that result for accuracy and completeness (wf_54a61b62-f48) before it went out.

## Verdict
A without the lock is READY AFTER ONE MORE PASS inside 150 x 50. Nothing visible changes outside. The crown's line moves 30 deg (V12-8), but it stays a dark 0.4 x 0.2 groove that shows in the hand, not from the room. The canopy raises no owner question.

- **No blocker stands.** The one blocking claim, that the splices cannot be worked in place, was refuted. The reviewer modeled the WAGO 221-412's lever backwards. It pivots at the end away from the entries and is lifted by its nose, which sits over the entries (K007's vector outline; WAGO's own photos). Here the entries face down, so the grips are at the bottom, over the ledge, not under the top flange. On K007's outline the levers open clear in all four packages (1.0 to the stud nuts, 0.77 to 0.87 to the channel). What survives is should-fix: the pocket's height against WAGO's real depth, the LED leads' slack, and the ledge under the levers' noses (V12-1).
- **What holds:**
  - The corner is a real step. The strap screws are reachable along -y (more than 250 free from both heads). The driver sits on ERP's holes: 77 x 33, 3.5 from the case's ends and sides, not mirrored, about ±0.3 of float, the washer and nut 0.3 to 0.5 clear of the pocket walls. The tray's joint nuts meet PEM's numbers in 1.0 sheet, and the joint bonds.
  - All four tops have 0 overlaps at zero tolerance with no exemptions, lock on and off. v2 passes only with its legacy exemption (hub/pins 38.8 mm3). The five packages' BOMs and checks rebuild byte-identical. top_check passes (every shade comes off; wrong turns refused, 9 mm3; the control held, 111 mm3; A's lock 0.00 / 14.2 / 40.5), and so does fixings_check.
  - The mirror is right: "on" turns clockwise from below, like a bulb.
  - NOTES 2 is built per top, NOTES 3 carries every V11-10 point, and the wiring diagram is in every package with ERP's lead colors. The -XL is everywhere in the packages, "2-3/4" is gone, an 8-32 centers from r 42 to 46.5, and the input leads are 0.95 or more from any tray face.
  - Heat is unchanged: Tc about 34 to 41 C in a 25 C room, at most 56 C in 40 C air, against ERP's 70.
  - Weights: 1612 / 1712 / 1693 / 1590 g (today / A with the lock / A without / B), the canopy 1034 g, 2.62 to 2.75 kg in all. NOTES' "2.6 to 2.7 kg" holds (A with the lock is 2.75).
  - No live picture is newly wrong.
- **The other packages:** today's top and B are the same as the pick, plus today's mark and clamp ring (V12-8, V12-9) and the cap's wording (V12-8). A with the lock is the same, plus its straps' BOM sizes (V12-5) and its NOTES 2 fitting sentence for the moved line (V12-8); its other lock items stay held (For later).
- **Owner questions:** none from this list.

## First: the splice corner, one redraw

**V12-1 The splice corner, redrawn once:** the channel's ledge, pocket and notches, how the splices are held, and the LED leads. It stays inside the canopy's 150 x 50: the channel, the LED leads' route and ties, and the plate's two studs if they move ((c), V12-2).

- **(a) A ledge that can be made.**
  - As drawn it cannot be formed. It is 27.8 x 7.4 (x -3.4 to 24.4, y 4.6 to 12, z 26.7 to 28.3; crystal.py:995) and merged into both side flanges. But the callout makes it from the 25 x 5.7 window's top edge, bent out (crystal.py:994, :1270-1271).
  - Bent that way at the sheet note's inside R 1.6 (crystal.py:1204), its top lands at z 25.1 or lower, and it ends near y 8.4. That is short of the entries (y 8.7) and of the levers' noses (y 11.8 to 12.8), so it would not hold the splices.
  - Give it a form that can be made, or make it a separate part, and draw it as formed. It must carry both splices, which span x -3.05 to 23.65. A tab bent from today's 25-wide window (x -3 to 22) would leave splice B overhanging its end by 1.65.
  - Relieve the channel's two upper corners: the side flanges and the top flange share faces there with no relief (crystal.py:990-991).
- **(b) The pocket's height.** The ledge's top (z 28.3) to the top flange's underside (z 46.8) is 18.5. WAGO's own sheets give 13.1 x 8.3 x 18.6 (2018) and 13.2 x 8.6 x 18.8 (2023), so a real splice does not fit. Size the pocket from 18.8, with clearance for the sheet parts' general ±0.5. Draw the splices at WAGO's sizes: crystal.py:1011-1015 and the hemi-splice row (components.json:1051) give 18.3 x 13.1 x 8.2 (AutomationDirect's K007 gives 18.3 x 13.0 x 8.2).
- **(c) The levers' open room.**
  - Take it from WAGO's own 3D model or a real part, and keep 2 or more of clearance. K007, today's source, is a distributor's drawing marked "NOT TO SCALE".
  - On K007's outline the levers clear the channel's stud nuts (y 20.95 to 28.05, z 42.8 to 46.8) by only 1.0, in front of both cord levers. A lever that opens to 17 overall already meets them (0.58 to 0.67 mm3; 4.3 to 5.5 mm3 at 19).
  - The real parts take more of it: WAGO's 8.4 to 8.6 height moves the levers' faces 0.2 to 0.4 out, and a real Ø8 nut (V12-12) reaches 0.45 nearer than the drawn Ø7.1.
  - One way: move the studs outside the levers' x span (see V12-2).
- **(d) Room at the noses.** The ledge runs to y 12.0 under noses whose face is at y 12.8. Only about 0.8 of each nose is free for a nail or a small blade (1.0 to 1.2 at WAGO's real height), and the splices rest on their noses. Stop the ledge 2 to 3 short of the levers' faces, or relieve it under each lever, so the splices stand on their bodies. Prove it on the hand mock-up (V12-14).
- **(e) The LED leads inserted at the factory.** UL 1598 5.2.1 asks for every splice to be completed at the factory unless packaging requires otherwise, and OPEN (2) names only the cord (crystal.py:1764-1767). But NOTES 3 (5) ("with the driver's LED leads (they come cut and stripped)", crystal.py:1728-1730) and the wiring diagram's step 4 (hemi_wiring.py:53-55) read as if the installer inserts them too. Insert them at the factory. Say so in NOTES 3, the diagram, the driver row and the splice row.
- **(f) Slack and ties.**
  - Each LED lead is cut to its route plus 11 exactly (135.7 and 148.6, against cuts of 136 and 149). No splice can be wired in hand and pushed in, or taken out. Give each lead 20 to 30 of slack, held by a tie.
  - Tie the run too. Today it passes 2.7 from the canopy's bore round the tray's -y end. Then it runs 68 along y at z 22.5, straight over the strap screws: 1.45 above the screwdriver's shaft and 1.85 above the upper screw's head (crystal.py:977-982). Tie it on the tray's end and along the run, or route it up under the plate.
- **(g) Open notches.** Today's are closed slots (y 6 to 11.5 in a ledge to y 12; crystal.py:996-997), with a 0.5 strip of 1.6 sheet in front of each, and they start at y 6.0, inside the ledge's own R 1.6 bend. Each cord conductor must be fed up through one into an entry that faces down and cannot be seen. Open them to the front, clear of the bend, so a wired splice slides in and out.
- **(h) Colors to lengths.** The - lead (black) goes to A at x 6.75, the + lead (red) to B at x 20.35 (crystal.py:977-980, :1011-1015). Neither the driver row, NOTES 8 nor the diagram says which color is cut to which length; a red lead cut to 136 ends about 13 short of B. Write "black 136, red 149", plus (f)'s slack.
- **(i) How the splices are held, and f7ede2f179 redone.**
  - The side flanges are 27.8 apart and the two splices 26.2 (WAGO: 26.2 to 26.4), so V11's called 0.5 dimples left 0.6 of play.
  - f7ede2f179 draws Ø3 dimples on the side flanges, standing 0.85 and 1.25 proud in 1.6 sheet, a severe form. It also cuts the LED leads' four 1.0 x 3.0 tie slots (x 3.0, 9.8, 16.6, 23.0; y 6.5 to 9.5) in the ledge that cannot be made. They leave webs of 0.4 to 1.05 of 1.6 sheet, and the +x slot is 0.4 from the side flange's face. The dimples fix the play, not the height.
  - Redo both with the new channel:
    - Hold the splices with one tie round both, through two slots in the web (the mechanics skeptic's choice). Once the notches open, nothing else holds them toward +y. With the tie, the dimples can go. If you keep a fit instead, set the side flanges 26.2 +0.2/0 apart with no dimples (the mechanics critic's other fix).
    - Put the LED leads' tie slots where no web round them is narrower than the sheet is thick. On a formed ledge the fingers between the notches are only 1.25 to 3.1 wide, with no room for them (the mechanics skeptic).
    - Make the splice row (components.json:1051) and the channel's callout say how the splices are held; both still say "push fit".
  - This is should-fix because the sheets claim a hold the geometry does not give. No US clause of UL 1598 asks for a fixed splice (6.18.2's "mechanically secure" is the Mexican deviation).
- **(j) The distance to the box.** The splices are 27.1 from the nearer box-screw slot (20.0 with the levers open). Keep them about that far, and print the new figure in OPEN (4), which still gives V10's "21 or more" (crystal.py:1770-1772).
- **(k) (my ask) The sections.** For the V12 check, re-cut canopy-v11-section.png with the levers' real room, the noses over the ledge, a conductor's path up into each entry, and the screwdriver with its handle under the ceiling. V11's draws the screwdriver only to y -61 and the levers as a box.

## Then, in one pass

**V12-2 The channel's top flange at 156 N.** Draw it with V12-1: it is the same part.
- Only the top flange's two studs, at (1, 24.5) and (16, 24.5), hold the channel; the web is not fixed to the plate (crystal.py:924, :990). The flange is now a cantilever about 21 long from the nut to the cord's line. V10's was 9.2, at 120 MPa.
- At UL 1598 17.21.1's 156 N, M is 3120 to 3268 N mm: 236 to 247 MPa on the full 31 x 1.6 section, and about 319 MPa next to the nuts (24 effective width). The prying heel at y 28.5 puts 294 to 556 N on each stud.
- No callout names the steel. Zinc-plated cold-rolled sheet yields at roughly 170 to 280 MPa (UNVERIFIED). At 170 MPa the moment is close to the full plastic moment (3373 N mm), so the pull test, or a later tug, could leave a permanent set. The elastic movement is small (about 0.23 at the cord, plus the plate's 0.08 to 0.33), so the 1.6 limit probably holds.
- Fix: 2.0 or 2.5 sheet (157 or 100 MPa), a formed rib across the top bend, or studs nearer the cord's line, outside the splices' span. Name the grade. After the pull test, look for a set.

**V12-3 PEM edge distances.**
- The upper strap's S-M3-1 at (8, 17) (crystal.py:1006-1008) is 4.0 from the window's bottom edge at z 21 (crystal.py:994). PEM's minimum from the hole's center to an edge is 4.8 (S-M3-1ZI). Its body ends 0.825 from that edge, and 1.9 of metal is left between the hole and the window. The callout checks only "8 or more from the bends" (crystal.py:1272-1273).
- Fix: raise the window's bottom edge to z 21.8 or more (the LED run at z 22.5 rises with it), or move the nut. Have the channel's callout check the upper nut's distance to the window's edge, not only to the bends.
- Every other clinch part meets PEM's numbers. One is open: the plate's tray stud at (-21, 46.3) is 5.8 from the Ø8 lead opening, but that edge is extruded (rolled up 1.6). Ask PEM how a formed edge counts (UNVERIFIED).

**V12-4 The tray's fits.**
- **The folds.** The outer wall's folds sit line-to-line on the U's end walls: 0 gap at y -58 and y 41, over 16 x 17.6 and 16 x 23.6 (crystal.py:933-938). With the inside R 1.0 at the folds (crystal.py:1204), the U's square corners stand off about 0.3 each way (1.0 if pressed flat on one face). With the sheet's ±0.5, the U often will not go in. Give the folds an inside span of 99.3 to 99.6 against the U's 99.0, relieve the U's corners for the R 1.0, and let the serrated joint screws pull the parts together.
- **The driver's +y button head** (Ø5.7 x 1.65, its face at x -36.65; crystal.py:959-965) is 0.35 from the -x gripper bracket's flange edge (x -37), and overlaps it in y and z. V11.md gives 0.35 too. The ±0.5 on sheet parts and the bent flange can close it. Give it 1.0 or more: notch the corner of the bracket's flange, or shift the bracket.

**V12-5 The cord's straps.**
- **The seat.** The stop is real: moved 1.0, the straps touch the web with 0 overlap. But tightened, the seat is a D, 6.0 wide and 5.0 deep (26.1 mm2; crystal.py:1001-1009), because the strap's tip and leg also bound the cord. A 6.0, 6.25 or 6.5 cord loses 7.6, 14.8 or 21.2 % of its section. Narrow the range to about 6.0 to 6.3, or open the legs to about 6.6. Whether 21 % harms the jacket (UL 1598 5.15.1.2) is for the prototype. The slip at 156 N is UNVERIFIED, and the thin end (6.0, squeezed 1.0) is the weak case, so pull-test both ends of the range.
- **The cord.** "6.0 to 6.5 over the braid" still has no maker or sheet (the hemi-cord row says "any (UL listed)", components.json:564). Cloth-covered SVT-B 18/2 is sold at about 0.250 in (Grand Brass, UL E357297), so the range is plausible. Name the cord.
- **The drawing.** TH_ (crystal.py:1206-1276) has no "cord-clamp" entry, so sheet 13 prints only 16 x 13 x 6 and the note. Call out the Ø3.4 hole, the R 3.0 seat, the 1.0 stand-off of the foot and the tip from the web (it sets the squeeze), the bend radii and SM_'s deburr line. Add "cord-clamp" to the square-drawn list (crystal.py:1282): A with the lock's BOM sizes the straps turned, 19 x 26 x 23 against 26 x 16 x 23.
- **Material and plating.** The note says "1.0 zinc-plated spring steel ... its edges rolled" (crystal.py:1144-1145), the BOM's material is plain formed steel sheet, and the CAD's edges are square. Electroplated hardened steel needs a bake against hydrogen embrittlement (ASTM B633 / F1941 practice; the hardness where it starts depends on the edition, UNVERIFIED). A cracked strap loses the cord's only strain relief in the canopy. Spring temper gains nothing here, since each strap stops on the web. Call plain low-carbon steel (or 301/304 stainless), or give the grade, the hardness and the bake. Make the note, the BOM and the CAD agree, edges included.

**V12-6 The LED leads' exit, per UL 1598 5.14.1 (b) or (c).**
- For sheet under 1.1 (the U is 1.0), 5.14.1 asks for (a) the metal's edge rolled at least 120 deg, (b) a non-rubber bushing at least 1.2 thick, or (c) glass sleeving at least 0.25 thick.
- The exit is drawn as a straight Ø7.5 x 1.5 collar on a Ø5 hole, a 90 deg extruded flange (crystal.py:974-975). The leads turn 90 deg 1.5 past it, onto its sheared end (crystal.py:979). The callout cites (a) and gives no angle (crystal.py:1264-1265). A real 120 deg curl on a Ø5 hole would be roughly Ø9.5 to 11 and crowd the outer wall at x -34 (UNVERIFIED).
- Fix: (c), glass sleeving at least 0.25 thick over both leads, fitted at the factory with the cut and the insertion (V12-1(e)); or (b). Name the part, draw it, correct the callout (crystal.py:1264-1265) and the comment at crystal.py:971-973, and add the sleeving to the driver row's FACTORY line (it says nothing of the exit today).

**V12-7 NOTES 3, the service text and the wiring diagram.**
- **The cord step, in hand.** Today the cord is clamped, then cut 40 above the upper strap and its jacket ringed 4 above it, in place (crystal.py:1726-1729; hemi_wiring.py:53-55). There the LED leads cross the window at z 22.5 and the ledge sits just above, so a stripper cannot go round the cord. And 40 above the upper strap's top is z 60, above the plate's underside (48.4), so the cord must be bent before it can be cut. Write the step from the cord's own mark, in hand, before clamping: "ring the jacket 17 above the mark, cut about 55 to 60 above it, strip each conductor 11" (today's corner; recheck on the new one). Say how the cord goes into the straps: thread its end up through both loops, or take each strap off.
- **The measure.** Step (5) measures along a cable from the cap's top to its gripper's lower end (crystal.py:1725-1726). But step (3) keeps the canopy tied 10 to 15 cm below the plate through the cord step (crystal.py:1718-1720). The cable and the cord then pass through the tied canopy's 3 floor, so a tape cannot run along either. The margin that keeps the cord off the load is only about 2.5 to 3.2. Give a method: measure in two parts across the floor and add its 3, or measure down from the ceiling to the cap's top's height and take off 43 (the grippers' lower ends are 43.0 below the ceiling).
- **The tool.** Name a PH1 screwdriver (ISO 7045 M3) with a shaft of 75 or more and a slim handle, worked from the front (-y, the side away from the levers) and tipped slightly at the upper screw. A Ø28 handle on a 60 shaft touches the LED leads at the upper screw. A fist (the probes used Ø72) on that screw's axis, 33 below the ceiling, reaches 3 into the ceiling. Name the same tool and side in the clamp-screws row (components.json:1078), which says only "driven from in front with a screwdriver (120 or more free with the canopy tied down)"; the free room itself is right (more than 250).
- **The LED leads.** Once they come inserted (V12-1(e)), step (5) and the diagram's step 4 ask only for the cord's two conductors.
- **The cable tails.** After "cut the cables about 50 above the grippers" (crystal.py:1723-1724), add "coil the tail inside its bracket's U". A gripper's top is 21.3 under the plate. A 50 tail run straight out the bracket's open side reaches about r 77, past the canopy's bore (r 72). The design comment says so (crystal.py:749); NOTES do not.
- **Inspection and service** (crystal.py:1733-1735). Write: take the shade off first (0.97 to 1.02 kg of the load); loosen the canopy's set screws, lower it and tie it to the cables 10 to 15 cm below the plate, as in (3); with a stubby screwdriver (the box screws are driven straight up at r 44.45, above the tied canopy), take out one box screw and back the other out until the plate hangs on it through its slot, as in (2); undo the box splices; then take the plate off that screw. Never let the plate hang on its leads. Today's text leaves the canopy loose, which step (3) itself warns against. One person can do it: with the shade off, about 1.65 to 1.73 kg hangs on the plate, and 11.5.1 lets a luminaire of 4.54 kg or less come down for access. So no "two-person" line.
- **The diagram's nits.** Two labels are crossed by lines ("(UL 486C)" and "ribbed"). ERP's LED (-) lead and line lead are both black: add one line saying which is which. Naming the box connectors as a part is optional: 6.16.4(b) governs only the lab's sample, and no BOM row supplies C1/C2.

**V12-8 NOTES 2 and the marks (decided).**
- **Keep both marks 0.4 x 0.2, dark. Do not enlarge them.** V11.md's "does not read at all" came from the render rig's metallic black (lamp_site.py:232, metallic 1.0). On a real dielectric anodized black, a 0.4 x 0.2 groove shows in the hand at about 37 % contrast, and not from the room. A laser mark on black anodizing comes out white unless specified, so on each mark's callout (crystal.py:1229-1230, :1235-1236, :1241-1242) write DARK, "no white or light fill", besides "cut before anodizing".
- **Make "lined up" mean "on".**
  - Today the shade's mark is over its keyed entry at 60 deg (the clamp ring, crystal.py:422-426; today's collar, :427-430). The crown's line is over the key pin at 30 deg (crystal.py:661-664).
  - Fitting lines them up at the entry, then turns the shade 30 deg. So on a seated shade they sit 30 deg apart (about 24 sideways), and on a half-fitted one 0 to 30. A fitter who turns a shade to line them up turns it counter-clockwise from below: the move NOTES 2 forbids (crystal.py:1697-1698). A half-fitted shade then falls.
  - Move the crown's line to 60 deg, over the seated shade's mark, on every top: the solid, the callout and the meshes. A shade turned to line them up then turns the "on" way.
  - On every top, check from where a seated shade's mark and the moved line can both be seen. On a seated shade the crown's line's lower end hides from below past about 14 deg (the mechanics critic, F5), and today's mark past 26 to 36 deg. If they show together only from the side, NOTES 2 says "seen from the side".
  - On A and B, the ring's mark lands at 60 deg only through its thread start's clocking (crystal.py:1232-1233), which has no tolerance on the sheet. Give it one: each degree moves the mark about 0.9 sideways at r 52.
- **NOTES 2's fitting steps, rewritten to match** (crystal.py:1690-1699). Drop "while it is still in your hands, find the mark". For A without the lock:

  > "To take one off: hold the shade from below with one hand and the cap with the other; lift the shade as far as it goes (8 to 9 mm), turn it counter-clockwise, seen from below, to the stop, and lower it off. To fit one: hold it up under the lamp and push it up where it goes (it fits one way only; if it will not go up, turn it a third of a turn and try again). Push it up as far as it goes, turn it clockwise, seen from below (as a light bulb goes in), to the stop, and let go: it drops 8 mm and the detent clicks. A shade that is on has the mark on its clamp ring under the line on the crown, and about 11 mm of the crown shows above its clamp ring (about 3 if it has not dropped). IF IT DID NOT DROP AND CLICK, IT IS NOT ON: push it up, turn it to the stop and let it drop. To check a shade, and always before you clean it, try to turn it clockwise without lifting it: a seated shade does not turn; one that turns was not on, so turn it to the stop and let it drop. Never turn a shade counter-clockwise without lifting it first. A shade that has not dropped sits 8 mm high, held only by friction; a push of 2 to 4 N at its rim, such as a cloth while cleaning, can turn it back to its entries, and it falls."

  - The side view is the sheets critic's. On a shade 8 mm high, the part of the crown's lowest step that shows shrinks from 11.3 to 3.3 on A, 11.5 to 3.5 on today's top, and 8.5 to 0.5 on B's first tier. Word it per top.
  - Per top: today's top holds "the cap" and finds "the mark on the top edge of its collar". B holds "its Ø56 tier (not the small cap, held by a magnet only)". Today both their sets print "the cap (B: its Ø56 tier)" (crystal.py:1679).
  - **The lock's text** names the same marks (crystal.py:1684-1685). With the line moved, its "hold it up under the lamp with the mark under the line on the crown" would hold the shade 30 deg off its entries, and it would not go up. So change its fitting sentence now, whatever the owner picks:

    > "To fit one: hold it up under the lamp, pull the knob, and push it up where it goes (it fits one way only; if it will not go up, turn it a third of a turn and try again). Push it up as far as it goes, turn it clockwise, seen from below (as a light bulb goes in), to the stop, and let go: it drops 8 mm. Then let the knob go: it springs fully in. A shade that is on has the mark on its clamp ring under the line on the crown."

    Today it has no third-of-a-turn fallback (the mechanics critic, F8). Its other gaps wait (For later).
- **Today's top: the mark's part.** Its NOTES send the fitter to the clamp ring (crystal.py:1692), but its mark is on the collar, because today's ring is torqued to no set angle. The callout calls a 0.4 x 0.2 groove across a 0.9 x 45 outer chamfer (crystal.py:1229). Today's collar has no chamfer: it is cut only for A and B, under `if sh_` (crystal.py:345-351), so the solid gets a 1.3 x 1.1 corner notch (crystal.py:430). The callout, the solid and NOTES disagree. Cut the 0.9 x 45 chamfer on today's collar and the 0.4 x 0.2 groove across it, as called, and name the collar in today's NOTES. Do not call the drawn notch instead: it is 1.3 deep and 1.1 tall, not the decided 0.4 x 0.2, and leaves only 1.2 of wall to the keyed entry slot. The Ø104 clamp ring, 3 lower, hides today's mark from below past 26 to 36 deg (see the check above).
- **No owner crop now.**

**V12-9 Today's clamp ring (today's top).**
- V11 dropped its nylon-tipped set screw, so today's ring is "held by the silicone's preload" alone (crystal.py:524-527). It has no shoulder and no PTFE slip washer (today's BOM has none; A and B have one).
- The mirror made the fitting turn, clockwise from below, the loosening direction of the right-hand M96 ring. NOTES 2's check twists the same way at every cleaning, and the outer silicone carries the hand's twist into the ring. How much it moves is UNVERIFIED.
- Fix: keep a lock (a set screw, drawn and with a row), add the slip washer as A and B have, or cut a left-hand thread.

**V12-10 fixings_check, and a hand mock-up.**
- What it tests today: a bare Ø6 x 120 shaft along each strap screw (fixings_check.py:56-57) and a box 7.1 in front of each lever's face (fixings_check.py:58-59). It caught a lead moved into the shaft's path. But it passes with the stud nuts 0.05 from the lever box, and it draws the splices at 18.3 x 13.1 x 8.2 and the stud nuts at Ø7.1.
- Add:
  - the named screwdriver's handle (Ø28 to 32) and a hand at each strap screw, with a ceiling plane at the plate's top (h 50) outside a 4 in box's Ø101.6 opening;
  - the levers' room from WAGO's model, grown by V12-1(c)'s 2 of clearance, so a nut 0.05 away fails;
  - room at each lever's nose, over the ledge. The grips are the noses at the entry end, not the splices' tops under the flange;
  - each conductor's straight run up into its entry;
  - the bought parts at their datasheet sizes (WAGO; the real stud nuts, V12-12).
- V11.md says fixings_check "proves" the screwdriver's path and the levers' opening. Say what it proves: a bare shaft and K007's box.
- Put a hand mock-up of the corner on the prototype list (V12-14): the noses caught over the ledge, a conductor fed blind up into a down-facing entry, and the screwdriver and hand at the upper screw under a ceiling.

**V12-11 Stale notes and spelling.**
- **Stale part notes** (the wall's, the U's and the channel's are V10's, the brackets' v8's, the ring's from the 1 Nov review). These print under the V11 callouts in all four sets, so a shop reads two instructions for each part. TH_ only puts the callouts in front of them (crystal.py:1277-1279):
  - the tray wall (crystal.py:1131-1133): "the driver's two PEM FH-M3-6 studs pressed in from outside";
  - the tray's U (:1134-1136): "two joint flanges with PEM S-M3-1 nuts inside the outer wall; the 1/4 in snap bushing";
  - the channel (:1140-1142): "web 28 x 40.4, side flanges 7.4, a top flange to x 20 ... two PEM S-M3-1 nuts for the saddle's screws; the splices' carrier riveted to its web";
  - the gripper brackets (:1103-1106): "M3 nylon-insert nuts", against the bracket-studs row's serrated nuts (components.json:1006);
  - the PEEK ring (:1044-1047): "(0.2 diametral), three Ø3.2", against its callout's 0.4 and 2 x Ø3.2 + 1 x Ø4.3 (:1213-1219). V11.md says this one was fixed. It is the land fit that the gate's 1.64 deg tilt rests on.

  Rewrite each to the V11 part, or drop it.
- **NOTES 6, Light** (crystal.py:1742). "About 1,000 lm at 2700 K (3000 K for Ice and Haze)" contradicts the owner's LED color per tint: Ember 2200 K; Poison and Fog 2700 K; Haze 3000 K; Dust, Acid, Ice and Smoke 4000 K (as Core's NOTES have it, crystal.py:1799-1801). The ring-board row (components.json:878) opens with the same stale phrase before its own per-tint list. This one matters: it would put most tints' LEDs at the wrong CCT.
- **NOTES 5** (crystal.py:1738): "tint, opal, tint" is wrong. From the outside the wall is tint, clear, opal (the 3 tint shell, the 6 clear liner, the 3 opal skin).
- **Small ones:** the skin's "it hides the COB" (crystal.py:479); NOTES 10's "over a table, one a table" (crystal.py:1775); the rim's "+$3 to +$5", which prints as "+3to +5" because matplotlib reads the paired $ as math (crystal.py:507).
- **Spelling.** Each set still prints "aluminium" 12 times, "Aluminium" 10 times (fabkit's "Aluminium 6061", studio/fabkit/model.py:63), "mould" twice (the formed-acrylic titles, crystal.py:101-111) and "COLOUR" once (components.json:878). _us() (crystal.py:1292-1300) rewrites only part notes, and only lowercase "colour". Apply it to everything the packages print, and correct V11.md's "American spelling in every printed Hemisphere note and row".
- **v2 (a record).** "SUPERSEDED, A RECORD" is only NOTES item 1, near the end of the set; sheet 1 still titles it "Hemisphere v2 (alternative)". V11 also changed four of its rows (cord, canopy-bushing, ground-screw, suspension), which now describe V11 parts it does not have: its grommet's row says a Ø7.5 bore, its CAD 6.6 (crystal.py:869). Mark it on sheet 1, and freeze its rows at v9's texts.
- **weights.py** (renders/2026-11-25/barkhorn/lamp-site/v10/weights.py): add a density for the clamp screws (about 1.6 g left out), and drop "lead-bushing".
- **dome_pendant_topA.py** relies on HEMI_LOCK_ON's default (crystal.py:224). Run with HEMI_LOCK_ON=0 exported, it would write A without the lock into the topA folder. Set it in the script.
- **The grommet:** draw its R 1.0 at both ends; its bore runs Ø7.5 straight. For the record: the outlet box and the box connectors are not drawn, and the sheet-metal parts get no flat patterns ("cut files: 0 sheet parts"), so their bend radii exist only in text.

**V12-12 The M3 serrated nuts: DIN 6923 does not cover M3.**
- DIN 6923 covers M5 to M20 only, and it is withdrawn (Westfield's sheet). Yet the bracket-studs and canopy-studs rows order "M3 ... (DIN 6923)" for the nuts that carry the tray's, the channel's and the brackets' bonds (components.json:1006, :1069), and the ground screw's note says the same (crystal.py:1156-1157).
- Suppliers sell M3 serrated flange nuts with a flange of about Ø8 (UNVERIFIED). Name a real part (maker, part number, flange size) and draw it at that size. The CAD draws the brackets' nuts Ø6 x 4, the old nylon-insert size (crystal.py:784-786), and the plate studs' nuts Ø7.1 x 4 (crystal.py:925-926).
- Recheck V12-1(c) with it: the channel's stud nuts sit in front of the levers.

**V12-13 lamp_site.py and RERENDER.md.**
- **The in-use picture.** V11 ported only the CORD_TOP/CANOPY run-on from the support sweep's patch (renders/2026-11-25/barkhorn/lamp-site/support/lamp_site-5e86d76e.patch). lamp_site.py still places the chair at (-0.02, 0.58, 0) turned 180 (lamp_site.py:862) and the cup's handle at cx + 0.046 (lamp_site.py:891-892). The patch's own comments say why: the chair "faced away, its back through the top" and the handle sat "13.5 into the cavity". Port the patch's (-0.02, 0.35) turned 0 and cx + 0.0615. RERENDER.md lists "inuse" (line 17), so a pass-v2 re-render from today's code would bring both faults back.
- **The anodized black (decided).** Write into RERENDER.md: the anodized parts are drawn as a dielectric black, checked against a sample, before pass v2. Today's "cap" material (lamp_site.py:232: #161618, roughness 0.38, metallic 1.0) draws the clamp, crown, gland and hub (lamp_site.py:376-377) and the CANOPY=1 canopy (lamp_site.py:454). On it a 0.4 x 0.2 groove changes the pixels by 1 to 2 levels in 255. A dielectric oxide black (base about 0.025, IOR 1.55, roughness 0.42) shows the same groove 37 % darker. Without the change, pass v2's cap, rim and under views leave out marks the real top shows.
- **The marks line** (RERENDER.md:284-285): the crown's line moves to 60 deg; today's mark as V12-8 sets it.
- **The canopy in frame.** CANOPY=1 draws a plain 150 x 50 cylinder with no floor holes, grommet or set screws (lamp_site.py:452-454). Where pass v2 shows the canopy ("Over a table" with its ceiling, RERENDER.md:287), load the CAD canopy's mesh.

**V12-14 The prototype list.**
- NOTES 9 (6) (crystal.py:1773-1774) and the ground screw's row put tests "on the prototype list", but there is none. "18.2" prints nowhere: it is only in the ground screw's note (crystal.py:1158), and bought parts' notes do not print. launch/first-articles.md, the nearest thing, lists neither 17.39 nor 18.2. UL 1598 6.14.3.1(f) ties a compressive-fastener bond to the 18.2 test, so the record matters.
- Write it as a file in each package, named in NOTES:
  - 17.21.1: 156 N for 1 min, at most 1.6 of movement, at both ends of the cord's range (6.0 and 6.5); then look for a set in the channel's flange (V12-2);
  - 17.39: the green screw's thread, at 1.6 N m;
  - 18.2: the bonding test (the serrated nuts and the joint screws);
  - the half-fit test: let a shade go mid-turn, measure its hold at the rim, and wipe it with a cloth;
  - the hand mock-up of the splice corner (V12-10);
  - an anodized black sample with a 0.4 x 0.2 dark groove, for the render's black and the mark in the hand (V12-8, V12-13).
- Correct the plain -42 in launch/first-articles.md:22 and :156 (it still plans a COB bench) and in PARTICULARS.md:24, which also prints "or 0-10 V". Keep the design's texts phase-cut only (Site texts, below).

## For later: A with the lock (only if the owner leans to it)
- No click: it has no detent (the dimple is cut only without the lock, crystal.py:432-438), so its check is "the knob went fully in".
- GN 617.1, the named alternative, rests out only after a pull and a quarter twist. A knob left at rest after a swap leaves the shade unlocked, and its NOTES would have to say so.
- Its NOTES 2 (crystal.py:1680-1688) has no check before cleaning, no recovery step ("push it up, turn it to the stop and let it drop") and no "never turn it without lifting".
- Its finish is still two: "trim" in studio/products/earf-dome-pendant-topA.json (gloss, roughness 0.04, clear coat 1.0), against lamp_site.py:420's matte 0.78.

## Your points (V11.md)
1. **The marks (V11-13, your question):** keep them 0.4 x 0.2 and dark; see V12-8 and V12-13. Your crops showed nothing because of the rig's metallic black, not because the real mark cannot be seen. 1.0 x 0.5 is not needed: it would show as two dark ticks at a dining table (the sheets critic's probe), a visible change on every top. No owner crop now.
2. **The gate (V11-12):** agreed: no gate, the NOTES warning alone. The real case is worse than your 1.64 deg. A shade pushed up off-center pivots on its nearest pin, and the far pins, 64.5 away, reach a 0.8 gate's 0.2 at only 0.18 deg. No depth works (0.3 to 0.5 passes only 0.44 to 0.62 deg), and a gate just past the entry would give a false stop. The half-fit test goes on the prototype list (V12-14).
3. **The tie slots and dimples (f7ede2f179):** the tie slots sit in the ledge that cannot be made and leave webs of 0.4 to 1.05. The dimples, Ø3 and 0.85 and 1.25 proud in 1.6 sheet, are a severe form and fix the play, not the pocket's height. Redo both with V12-1 (see (i)).
4. **"fixings_check now proves it" (V11-1(a), (c)):** it proves a bare shaft and K007's box; see V12-10.

## Site texts
These are mine, with the site lane. They are here so your texts match.
- **Dimming:** "or 0–10 V" comes off the live line in the next site build; the owner is told now. For you: keep every design text phase-cut only. NOTES 6 is; PARTICULARS.md:24 is not (V12-14).
- **The canopy's weight:** corrected in the same build to about 2.3 lb (1.0 kg), against the site's 0.9 lb (0.4 kg). It does not depend on the pick.
- **After the pick:**
  - "Quarter turn" (the card copy, the one-line description, the Cap fact and Care; the meta descriptions no longer say it) becomes a lift, a 30 deg turn and a lower. Care must also say to turn the shade back on until it drops and clicks, not just change the angle.
  - The Hanging fact names the cord and the canopy but not the two cables every top hangs on. They go in it.
  - The hanging weight: 3.5 lb for today's top and B, about 3.7 lb (1.7 kg) for A without the lock.
  - "Cut to the drop at install" depends on the lab.

## Order
1. V12-1, as one redraw of the splice corner, with V12-2 and V12-3 (the same channel) and V12-12's real nut size (it sets the levers' clearance).
2. The rest, V12-4 to V12-14, in one pass.
3. The V12 check.

**For the lab and ERP.** NOTES 9's OPEN (1) to (6) stand. Change and add:
- (2), UL 1598 5.2.1: once the LED leads are inserted at the factory (V12-1(e)), the cord is the only field splice in the canopy, as (2) already says.
- (4): the splices' new distance from the box-screw slots (V12-1(j)).
- (7), new: UL 1598 5.2.7, "Conductors intended for field connection shall have matching identification by color, number, letter, or other acceptable means." The field joint pairs the cord's ribbed or printed conductor with the driver's red lead, which is not matching identification, and the cord row cites 5.2.7 for that pairing (components.json:564). Ask the lab, or mark the + side to match the cord.
