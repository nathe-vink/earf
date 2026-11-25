# V11 for the Hemisphere top (the pick: A without the lock), 25 Nov 2026

From the V10 check of r32 58e4f5d036 (wf_66362728-04b: four critics, four skeptics; full result `coordinator/hemisphere-top-v10-critics-2026-11-25.json`, the reviewers' probe scripts in `coordinator/hemisphere-v10-probes-2026-11-25/`). This list was itself checked against that result for accuracy and completeness (wf_3d1f606e-7d9) before it went out.

## Verdict
A without the lock is NOT READY. The canopy's inside must be re-laid out; text fixes alone won't do it.

- **What holds:**
  - T1 is the right layout: the cord centered in 150 x 50, the bonded steel tray as the barrier, the mains spliced in the box, heat well under ERP's limits, the ground in the box.
  - The bayonet, the Ø3 detent and the swap pass at zero tolerance.
  - The four top packages have 0 overlaps at zero tolerance. v2, a record, passes only with its legacy exemption (hub/pins 38.8 mm3).
  - The BOM rebuilds identical, and the weights check to the gram.
- **Owner questions:**
  - The canopy work (V11-1, V11-2, V11-4 to V11-10) fits inside 150 x 50 with nothing visible changing outside, so it raises no owner question unless that changes.
  - The one-way marks (V11-13) are a visible change on every top; they go to the owner.

## First: the re-laid-out canopy, with V11-3 alongside

**V11-1 (blocking) The cord corner, redesigned** so an installer can do NOTES 3 on site, with ordinary tools, with the canopy tied down.

Today there are only two ways in:
- unbolt the tray and let it hang on its mains leads (NOTES must never ask for that);
- drop the channel off its two plate studs. Its nuts at (13, ±8) can be reached from below with a nut driver once the canopy is tied down, but this needs LED-lead slack the CAD does not give. If the new corner drops down, set V11-6's factory cut to leave that slack.

- **(a) The saddle's screws.**
  - Problem: their heads (x 0.2 to 2.0) face the tray's inner wall (x -7), 7.2 away along their axis. A 6 x 120 shaft first clears at about 54 deg below that axis, with the canopy and its grommet lowered.
  - Why +x won't do: it leaves only about 30 to the gripper bracket, too short for a screwdriver. Also, heads facing +x at |y| 10 or more (to clear the gripper) hit the channel's side flanges: their inner faces are at |y| 12.4 (x 4.6 to 12); a 5.5 head at |y| 10 reaches |y| 12.75, and a 6 shaft there spans |y| 7 to 13.
  - What works: ±y has 60 or more free and is open with the canopy tied down. Face the screws along ±y, widen the channel, drive the screws from below, or use a listed cord grip.
- **(b) A defined, limited squeeze.**
  - Problem: the saddle bottoms on the web as a closed Ø6.0, so a 5.5 to 6.0 cord is not held and a 6.5 one is squeezed only 0.5.
  - Name the cord's real outside diameter over its braid, from the maker's sheet. Size the clamp for a set squeeze over that range (for example, the seat about 1 below the smallest cord), or narrow the range, or use a listed strain relief.
  - Keep a stop, so the pressure stays limited (UL 1598 5.15.1.2).
  - Name the clamp (maker and part), or draw it as a made part: its row says "any (a two-hole strap)" and it has no drawing.
  - The prototype's pull test is UL 1598 17.21.1: 156 N for 1 min, at most 1.6 of movement.
- **(c) The splices.**
  - The two WAGO 221-412 levers face the tray from 0.3, and they open to 15.3 tall (WAGO 221-412_K007).
  - The named 221-500 carrier is 77.6 x 17.5 x 25.5, longer than the canopy's 45.4 inside height. The 221-502 is 52.8 x 18.1 x 16.9. Neither fits the 10.0 between the web and the tray.
  - Three things describe no real part: the CAD's "1.5 plate"; the channel callout's 2 x Ø3.2 rivet holes (called at crystal.py:1203-1206 but not cut, with no row for rivets); and the row's "riveted".
  - Give the splices a real fixed place with room for the levers, named and drawn as the real part.
  - Keep them at least 21 from the box-screw openings, as today. That is the distance the wiring critic judged fine; the 4.3 slots exceed UL 1598 6.17.2.4's 1.6 for an opening in a barrier, so the lab must accept the spacing. Or close those openings (see V11-8).
  - Whether the box and the canopy count as one wiring compartment goes to the lab.
- **(d) NOTES 3's cut.**
  - Problem: cut 4 above the saddle's top, the conductors end at h 19, while the splice entries are at h 28.5 and WAGO strips 11.
  - Write: "cut it about 35 above the saddle's top; ring and strip the jacket 4 above the saddle's top; strip each conductor 11". Check it against the new corner.
- **(e) The LED leads outside the tray.**
  - Give them tie points, and no hanging loop once they are cut to length (V11-6).
  - Today the canopy's floor clears the channel's sheared bottom edge by 2.0, one lead's thickness, and the run at y -61 is 2.7 from the canopy's wall.
- **(f) (my ask)** Show the new corner in sections, with the screwdriver's and the levers' room drawn, for the V11 check.
- **(g) Teach fixings_check what this check found by hand.**
  - Add a screwdriver along each site-driven screw's axis (the probes used Ø5 x 60 and Ø6 x 120), and the swing of each lever splice's lever (open, 15.3 tall), both with the canopy tied down.
  - Draw the bought parts at their datasheet sizes.
  - Clear its FIX list (fixings_check.py:14-18 names "canopy-bushing" twice, plus the parts V10 removed).
  - PEM edge distances, the saddle's squeeze, real part sizes and the stud pattern stay hand checks for the V11 check.

**V11-2 (blocking) The driver on ERP's holes.**
- **The holes.**
  - ERP p.11 fig. 7 gives 77 x 33, 3.5 from the case's ends and sides. On the CAD case (y -51 to 33, h 7.9 to 47.9) that is (29.5, 44.4) and (-47.5, 11.4).
  - The studs are drawn at (27.7, 44.4) and (-49.7, 11.1), 1.8 and 2.2 off, and the -y hole breaks out of the case's end.
  - A real case on the drawn studs spans y -53 to 31 and lands in the U's -y joint flange and its screw and nut.
- **Tolerance.**
  - Two fixed M3 studs (major Ø2.87 to 2.98) in ERP's Ø3.2 holes need their spacing held to about ±0.2. The sheet's general ±0.5 on each stud allows up to ±1.0, so the driver will not reliably go on.
  - Tolerance the two studs to each other (77.0 and 33.0, ±0.05), or use one stud and a loose screw in a clearance hole.
  - Tolerance the gripper brackets' and the channel's stud patterns to each other the same way.
- **Nuts.**
  - Use a plain M3 nut and washer on ERP's plastic tabs: serrated flange nuts bite in and the joint creeps.
  - Size the nut to ERP's pocket (its wall is about 3.4 from the hole's center) and to the stud that stands past the wall and the tab (3.2 today; recheck with the stud V11-4 picks).
- **Pockets.** Draw the two equal, about 7 x 7.5 to the step, as fig. 7 has them.

**V11-3 NOTES 2 by the top actually built.** This is blocking for today's top's and B's packages; A without the lock already prints the right text. It is a V10 regression: v9 worded it conditionally.
- **The fault.** NOTES 2 now branches on the module's LOCK_ON. So today's top, B and v2 print the lock's knob steps and "the shade can no longer be lifted, turned or lowered". That is a false safety claim: they have the detent, not the lock. A with the lock prints "AND CLICKS", though it has no detent.
- **The fix.** Branch on TOP_TIERS[top].get('lock') and build NOTES per product.
- **For A with the lock**, NOTES 2 ends: "...and let go: it drops 8 mm. Then let the knob go: it springs fully in. IF THE SHADE DID NOT DROP, OR THE KNOB DOES NOT GO FULLY IN, IT IS NOT ON." Its knob step drops "at the back of the top" (the ceiling box sets which way the knob points) and "with the cap hand" (say what V11-19(a) says).
- **Build commands.** Correct them at dome_pendant_topA.py:7 and dome_pendant_topB.py:7: they name dome_pendant.py, which would write today's top into the A or B folder.

**V11-4 The tray's joint.** This is should-fix in all three lenses; it is listed here because the joint is redrawn with the canopy.
- **The joint cannot be made as drawn.** The S-M3-1's 6.35 head is wider than the 5-wide joint flanges. The -y flange keeps 0.1 of metal at its free edge, the +y flange's hole is an open notch, and the real collar runs into the end walls and the bottom.
- **Redraw it.** Fold the outer wall's ends over the U's end walls with the nuts in the end walls, or rivet or spot-weld it, or fold the tray in one piece. The flanges sit in the 6 and 7 end gaps beside the driver's base, so they cannot simply be widened.
- **The wall's studs.**
  - At ERP's holes they sit 4.0 and 5.0 from the 1.0 wall's edges, against FH/FHS-M3's 5.6. With the holes 33 apart in a 42-tall wall, no FH-M3 position works.
  - Options: FHL-M3 (3.3 is PEM's figure for FHL-M3-8; whether an FHL-M3-6 exists is UNVERIFIED), a low button-head M3 from outside (its head 0.35 clear of the gripper bracket's flange), or a rivet nut.
- **The other clinch parts, to PEM's published minimums.**
  - The plate's FH-M3-8 at (-21, 45.5) is 5.0 from the 8 mm opening's edge (PEM asks 5.6).
  - The web's S-M3-1 collars reach |y| 11.2, where the bend starts at about 10.8.
- **The bond.**
  - The ground screw's note (crystal.py:1107-1111) says the tray, the channel and the gripper brackets bond through their studs' serrated nuts. Their rows order M3 nylon-insert nuts (components.json hemi-bracket-studs, hemi-canopy-studs).
  - Either order serrated nuts or washers on those studs, or rely on UL 1598 6.14.3.1(f) and put the 18.2 bonding test on the prototype list. Make the note and the rows say the same.
  - The redrawn joint keeps the tray's two parts bonded.

## Then, in one pass

**V11-5 The LED leads' exit.**
- **No Heyco part fits.**
  - SB 250-040 has a 3.2 bore and SB 250-2 a 3.6 bore; the two 18 AWG leads need about 3.9 to 4.0.
  - SB 312-3 (bore 4.8) needs a 7.9 hole, its body is 7.9 tall, and its Ø9.5 head would come within about 0.25 of the outer wall.
- **The fix.**
  - Use UL 1598 5.14.1 (a), a smooth rolled edge, or (c), glass sleeving over the leads through a deburred hole, or another exit.
  - Name the real part and draw it at its real size: crystal.py:950-952 draws a Ø4.8 bore and Ø9.5 heads in a Ø6.4 hole, which match no Heyco part.
  - Rewrite the row (components.json:1079-1087: "flanges Ø9.5; the exact number from Heyco's table").

**V11-6 The driver's order code and leads.**
- **The code.** Put ESS010W-0180-42-XL in the BOM's model field itself, and in the 'Light' note, which also prints the plain -42. A plain -42's 152 leads would leave about 110 in the box, under 6.15.1.6's 150.
- **The LED leads.** The -XL's are 300 too. Have them cut at the factory, with the dimming leads, to the lengths the new corner's routes take (104 and 126 today, including the strip), and stripped 11. Say so in the driver row and in NOTES.

**V11-7 Edges.**
- The 120 V input leads in the +y end gap pass about 0.65 (real 2.0 leads) from the joint flange's sheared top edge. The CAD's 0.08 is an artifact of the lead's end disc.
- Add a general deburr-and-break-edges note to every sheet-metal part's callout: tray, channel, brackets and plate. Today only the plate's opening says "deburred".
- Tie the input leads (UL 1598 5.1.3, 5.14.1).

**V11-8 One box: 4 in boxes only**, as NOTES ask (ears 3-1/2 in apart, r 44.45).
- **The text.** Drop "2-3/4 to" from NOTES 3, the box-screw row and the strap callout. A 3-1/2 in box, with ears 2-3/4 in apart, puts the lead opening's lip on its wall.
- **The slots.** Re-cut them so an 8-32 screw can center on either side of r 44.45 (the mechanics critic's "about r 42 to 46.5"). Today the slots' end arcs are centered at r 44.45, so a screw can center only 0.07 past it.
- **If closing the openings is how V11-1(c) is met,** close them only as far as the box ears' real spacing tolerance allows, or cover them another way. A round 4.3 hole lets an 8-32 screw move only ±0.065 (ears 88.77 to 89.03 apart); the real tolerance is UNVERIFIED.
- **The box.** Name its depth, and check that the opening's lip falls inside a 4 in box (about 2.9 to spare).

**V11-9 A wiring diagram with assembly instructions.** This is required for a lamp shipped with its cord unconnected (UL 1598 6.15.1.3; Table 20.1.1 item 1.33).
- **Show:**
  - the cord's identified conductor to the red (+) lead;
  - the two WAGOs;
  - the box splices with a named UL 486C connector (6.16.4(b));
  - the grounding conductor under the green screw.
- **The green screw's thread.**
  - By volume, the extruded hole in the 1.6 plate gives 2.5 to 2.66 of thread: about 2 to 2.5 full threads against UL 1598 6.14.2.11's two, not the row's "about 3.5 threads".
  - Either put a first-article test on the prototype list (17.39, at 1.6 N m) or use a clinch nut, and correct the row.

**V11-10 NOTES 3's hanging and service steps.**
- **Canopy first.** Thread the cables up through its two floor holes and the cord through its grommet before the grippers. The cables end in the hub's stop sleeves, so the canopy goes on from their free ends.
- **Support the plate.** While the plate is wired under the box, give it a temporary support, such as hanging it on one box screw through a slot.
- **Tie the canopy** 10 to 15 cm below the plate, not 5. At 5, the plungers are only about 7 to 9 above its rim, too little for a finger.
- **The cord's bow** is about 2 to 3 cm, more on long drops (not "about 21 mm").
- **The 480 minimum's reason:** below it, the cables rub the canopy's floor holes.
- **For B,** measure from the height of the cap's top, not where the cables leave the crown. That point is 8.5 lower; measured there, the cord comes out about 11 longer than its run and bows about 5 cm.
- **Leveling.**
  - Hold the lamp up before pushing a plunger to level it.
  - Level it with a shade on: across the cables nothing adjusts, so each shade sets that itself.
  - On the shade's drawing, add a balance spec: its center within 0.3 of its axis, checked on a two-point stand.
- **The cables.** After leveling, cut them about 50 above the grippers with cable cutters, leaving enough to re-level. Give the supplied cable length in the suspension row.
- **Re-leveling.** Set the cord again after any re-leveling.
- **Set screws.** "Tighten the canopy's two set screws in turn, a little at a time."
- **Inspection and service.** UL 1598 11.5.1 relies on this paragraph. Lower the canopy by its two set screws, hold the plate, and take out the two box screws; never let the plate hang on its leads. It would put 2.6 to 2.7 kg on two spliced 18 AWG leads. Say how the driver is replaced: the plate comes down, because the driver's input leads are spliced in the box.

**V11-11 Heights, and the detent's plunger.**
- **Faces to locate in the rim-plane datum.** A's and B's collar sheets are located (the Ø100 shoulder at z 86 to 92). Still unlocated:
  - today's collar (no shoulder; only 116 and 43.5);
  - the hub ("radial at z 93" with no face; its bottom face is z 60);
  - the PEEK ring ("at z 93"; it runs z 86 to 100).
  Give each one face in that datum.
- **The plunger** (today's top, A without the lock, B).
  - On the PEEK ring's sheet: "plunger body flush with the land to 0.1 under; more than 0.2 proud, its body scrapes the collar's bore".
  - In the CAD, draw its ball 0.9 proud (Kipp K0310.05's H), not 0.8 (crystal.py:595).

**V11-12 The half-fitted shade (your point 2).**
- **No ramp.** A ramp cannot seat itself: the detent's drag (0.10 to 0.24 N m) beats a slope-0.4 ramp (0.04 to 0.10 N m). Drop the prototype ramp test.
- **The gate: a tolerance stack now.**
  - The gate is a step down from each band's ceiling just past its entry, 0.8 deep (1.0 in the key's taller band) and about 4 deg of arc long.
  - Count the shade's tilt on its land: the Ø82 bore on the Ø81.6 land over 14 allows up to about 1.6 deg, about 1.2 mm of height at the pins' r 43. The gate has only 0.2 of clearance at full lift (9.0 against 8.8), and that assumes no tilt.
  - If the stack passes, draw the gate and put a printed mock-up on the prototype list. If it fails, the NOTES warning stays alone.
- **Mirror the slots** so "on" turns like a light bulb: entries at 60/180/300, with the pins, the detent and the lock unchanged. Today a "tighten it" twist on a loose shade takes it off.
- **NOTES 2 for the no-lock tops,** in the mechanics critic's text. Swap clockwise and counter-clockwise if the slots are mirrored, and name the mark where V11-13 puts it:
  > "To take one off: hold the shade from below with one hand and the cap (B: its Ø56 tier) with the other; lift the shade as far as it goes (8 to 9 mm), turn it clockwise, seen from below, to the stop, and lower it off. To fit one: while it is still in your hands, find the mark on its collar; hold it up under the lamp with the mark under the line on the crown (it fits one way only; if it will not go up, turn it a third of a turn and try again). Push it up as far as it goes, turn it counter-clockwise, seen from below, to the stop, and let go: it drops 8 mm and the detent clicks. IF IT DID NOT DROP AND CLICK, IT IS NOT ON: push it up, turn it to the stop and let it drop. To check a shade, and always before you clean it, try to turn it counter-clockwise without lifting it: a seated shade does not turn; one that turns was not on, so turn it to the stop and let it drop. Never turn a shade clockwise without lifting it first. A shade that has not dropped sits 8 mm high, held only by friction; a push of 2 to 4 N at its rim, such as a cloth while cleaning, can turn it back to its entries, and it falls."

  ("About 2 N" in today's text is the low end: the measured hold is 1.6 to 4.5 N at the rim.)

**V11-13 The one-way marks.**
- **The shade's mark.** The collar's arrow is on an up-facing ring (r 42 to 47, 0.5 above the clamp ring), so a fitter pushing the shade up cannot see it. Put the mark on a face seen from below or the side: the clamp ring's side, with its thread start clocked to the collar's as the lock build does, or the collar's 0.9 x 45 outer chamfer.
- **The crown's line.** It sits on the lowest tier's side and shows from about half the directions around the lamp.
- **Finish and size.** A laser mark on black anodizing comes out white unless specified. Specify both marks dark, and give each a size.
- **In the model and to the owner.** Put both marks in the CAD solids and meshes, and render one close crop of each for the owner's next Hemisphere message.

**V11-14 Callouts against the CAD.**
- **The brackets' flange holes:** called Ø3.4, cut Ø3.0, so brackets made from the STEP cannot go over M3 studs.
- **The channel's rivet holes:** settled by V11-1(c).
- **The canopy's floor hole:** called Ø12.0, cut Ø12.5.
- **The grommet:**
  - say how it is held;
  - give its edge radius;
  - draw it, since it is "to make";
  - open its bore to about Ø7.5. Today's Ø6.6 leaves 0.05 a side on a Ø6.5 cord that slides 10 to 15 cm through it. Change the row and NOTES "Wiring" too.
- **The canopy's 1.0 x 30 deg lead-in:** cut it in the CAD.
- **The channel's web:** noted 40.4, drawn 43.4.
- **Bend radii:** give them on the sheet-metal parts' sheets; today only the plate rim's "inside R 2" is given. Name how the plate's rim is formed.
- **In the CAD:**
  - draw each LED lead as one solid; one run is detached at the lapped corner at (-5.6, -61);
  - put the channel's two PEM nuts in the channel's part, not in "cord-clamp";
  - draw the screws at their ordered length: the tray and saddle screws are drawn 4.5 and 5.0 against M3 x 6.

**V11-15 Stale printed texts.**
- **The ring:** "0.2 diametral" (it is 0.4) and "three Ø3.2" (it is 2 x Ø3.2 + 1 x Ø4.3).
- **The collar:** "work either way up" (it is keyed, one way).
- **The plate:** "(hemi-canopy-strap)".
- **Makers:**
  - the canopy set screws' maker, "any (PEM for the nuts)": there are no nuts;
  - the box screws' maker, "supplied with the junction box" (components.json:989): it is the outlet box, as the row's own text says.
- **The suspension row:** "up through the hub, crown and cap" (components.json:725). On B the cables pass beside its Ø32 cap.
- **The clamp ring's nylon-tipped set screw:** draw it with a row, or drop it. Call out its M96 x 1.5 thread where there is no lock.
- **NOTES 1:** "the notes below describe the COB build".
- **OPEN (2):** quote 5.2.1's sentence.
- **American spelling in the printed notes:** "aluminium", "anodised", "mould", "colour", "centre", "equalising"; NOTES 7 has "anodized aluminium".

**V11-16 A with the lock (held).**
- **Datum:** its datum line says 0 deg is the cables' line, while its cables sit at 105/285. Fix the line.
- **Crowfoot:** the lock row names a 17 mm crowfoot for its 16 AF lock nut.
- **Finish:** crystal.py:526 and the render JSON say "anodised", while lamp_site.py:420 draws one matte black. Make them one.
- **BOM sizes:** bom.py:42-48 reads p.solid; read p.detail, as drawings.py:1021 does.
- **Everything else for the lock** (v8 S2 to S4, v9, the one-person swap) stays held for his answer.

**V11-17 v2 (a record).** It prints V10's rows and NOTES over v9's enclosure. Freeze it at v9's texts, or mark it superseded on its first sheet.

**V11-18 RERENDER.md.** Line 37's V10 paragraph says nothing about the cord.
- **The cord and cable tops.**
  - cord-v6 now ends its jacket at z 745, with two bare conductors to 754.5; the cables end at 765.1.
  - Line 26's "the canopy out of frame" holds for single-lamp frames, but not for the cluster. Its front-row rims at 0.42 to 0.62 m put the cord and cable ends at about 1.15 to 1.39 m, in frame (at least Poison's and Smoke's).
  - Write the rule in: the cord's and the cables' tops never show in frame. Run them on past the frame's edge, or end them at a canopy on a ceiling.
  - Port today's CORD_TOP / CANOPY run-on (fa2d6ff2b0's patch to the old 5e86d76e code) into the current lamp_site.py, and run the cables on too.
  - Drop V10's two splayed conductor ends from the render mesh, so a run-on cord shows no stubs.
- **Line 26:** "the cord 2 mm long" becomes "the cord 2 mm longer than the cables".
- **The marks:** add them once V11-13 sets them.
- **After the pick:** add the dims drawing on r47-site-next to the list; it shows the cord alone, no cables.
- **For pass v2:** show the canopy once, for example "Over a table" with its ceiling.

## The owner's pages (the lock sheet v10, before I send it)

**V11-19**
- **(a) The swap line.** It now states a one-hand method that your own open list (top-redraw.md:434-435) says cannot be done. Say what holds: the knob is held out through the lift, the turn and the lower while it turns with the shade, and we have not yet shown one person can do that while steadying the top. GN 617.1, which has a rest position, is the alternative.
- **(b) Wording.**
  - "keeps the shade from being lifted";
  - "in 5 the cables hang where they do in 2";
  - drop "A's cables: 105/285 deg with the lock, 0/180 without";
  - say that only A can take the lock;
  - say that the lock does not help a half-fitted shade;
  - add one line: the knob always points along the cables' line, one of two opposite ways, set by the ceiling box.
  - Optional: lay the sheet out 3 x 2, which doubles its size on a phone.
- **(c) The cord's lean in frame 2 against frame 5: no re-render.** The lock frames vary too (frame 4 is as straight as frame 5), and nothing in the design sets which way the cord bows.
- **(d) The top sheet, only if it is re-sent.**
  - weights 1612/1693/1712/1590 g (today / A without the lock / A with the lock / B);
  - "anodised" becomes "anodized";
  - drop "at the back of its clamp ring" (the ceiling box sets which way the knob points);
  - bring its lock line ("pull it to lift and turn the shade") in line with the lock sheet.

## Your three points
1. **11.5.3 to the lab under 11.5.1:** agreed, for the reason your NOTES and V10.md give. You may add that over the tray the driver blocks the rod 0.5 below the plate.
2. **The ramp:** see V11-12.
3. **The cord top into the canopy:** confirmed; see V11-18. No live picture is wrong because of V10. The live cluster and in-use frames use the old cord, and today's fixes run it out of frame and up to a canopy.

## Site texts
These wait for the owner's pick, except Dimming, which I take to him now.
- **Dimming:** the live line says "Phase-cut (leading or trailing edge) or 0–10 V". V10 cut the 0-10 V leads, so "or 0–10 V" goes.
- **The canopy's weight:** about 2.25 lb (1.0 kg), against the site's 0.9 lb (0.4 kg). This was already wrong at v9.
- **"Quarter turn"** becomes a lift, a 30 deg turn and a lower.
- **The Hanging line:** the two cables go in it.
- **"Cut to the drop at install":** depends on the lab.

## Order
1. V11-1, V11-2 and V11-4, as one re-laid-out canopy, with V11-3 (a NOTES 2 code fix) alongside.
2. V11-5 to V11-18, in one pass.
3. V11-19 (text only). You can do it first if it's quicker, since it unblocks my message to the owner.
4. The V11 check.

**For the lab and ERP.** V10's three questions stand. Add:
- whether the box and the canopy count as one wiring compartment (V11-1(c));
- for the clause 15 temperature test, ERP's Tc point: on the label face, 0.8 from the tray's inner wall. The estimated Tc is 34 to 41 C in a 25 C room, and at most 56 C in 40 C air, against ERP's 70.
