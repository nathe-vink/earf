# Fresh engineering review of the baseline CAD (round 48)

A fresh reviewer given only the drawing sheets, bom.md, cutlist.csv, checks.json and turntable_float.py.

I reviewed the turntable-float package: sheets 1-6 and 12-15 in full, and only the title blocks of the pod-ring, pod-mat and parts-list sheets (7-11, 16-18). I also read turntable_float.py, bom.md, cutlist.csv and checks.json. checks.json says "ok" because it only looks for clashes. It does not check any of the problems below.

**1. The 10 least buildable details (worst first)**

1. **The light slot leaves 1 mm of base.** The base is 10 mm thick and the slot is cut 9 mm deep from below, so 1 mm of acrylic spans 300-390 mm. Cast 10 mm sheet varies by about ±0.8 mm, so the cutter will break through in places, under the printed band.
   - At 60 LEDs/m the pitch is about 17 mm, but the LEDs sit only 12 mm from the edge, so the edge will show bright spots. The runs stop 40 mm short of the corners and there is none along the back, so the glow is a broken U.
   - Fix: a 15 mm base with a slot 6 mm deep and 25 mm in from the edge, a dotless COB strip, and runs that go round the corners. Or cement on a separate edge-lit perimeter strip.
2. **The motor sits on the shelf but the platter sits on rubber.** The pulley-to-platter height passes through the levelling feet, the Sorbothane (which creeps), the lid's weight and the base. The pulley's own height passes through the mat and the pad stacks.
   - The pod is 2.4 kg on soft pads 44 mm apart, with the belt pulling about 90 mm up. The tipping moment (about 0.18 N·m) is close to what its weight resists (about 0.26 N·m), so the pulley will tilt and the belt will walk.
   - The belt wraps only about 90° of the pulley: sin β = 130.3/184.7 gives β = 0.78 rad, and π − 2β ≈ 1.58 rad. The belt path is about 1001 mm, not the 1025 in the BOM.
   - Fix: hang Rega's motor from the plinth on Rega's own grommets, as a Rega does. Or keep the pod but put it on hard cones and make the plinth rigid.
3. **The float is tuned to the wrong frequency, and its bolts don't add up.**
   - Load per bushing with the lid on: plinth 4.5 + platter 1.7 + bearing 0.5 + arm 0.45 + lid 2.2 ≈ 9.4 kg, so 2.35 kg each, not 1.8 kg. That is about 103 kPa.
   - Stiffness: shape factor about 0.5, so k ≈ 1.5 MPa × 223 mm² / 5.6 mm ≈ 60 kN/m. That gives f ≈ 25 Hz, and about 36 Hz once the nut clamps the second bushing. That boosts the 25-40 Hz band where speaker feedback lives instead of isolating it. (Arm and cartridge resonance is about 7.6 Hz: 19.7 g at 22 µm/mN.)
   - The bolt is drawn threaded into the plinth's insert and also carrying a nut. An M6×70 also runs about 3 mm too long for a 12 mm blind insert.
   - The bolt heads sit 1.8 mm above the shelf, so screwing the feet in 2 mm grounds the float.
   - Fix: either make it rigid (studs locked into the plinth, torqued, isolation in the feet) or a real 3-5 Hz spring float. Use studs, not bolts.
4. **The bearing mounting will crack the plinth.** The M4 insert holes (Ø6 at r = 22) leave 2.8 mm of acrylic beside the Ø32.4 bore.
   - Clearance of 3-5 µm is too tight; 8-12 µm is normal.
   - The spindle is 304 in the BOM but 440C on sheet 13.
   - Nothing seals the oil for transit.
   - Static cannot bleed off "through the oil film", because oil insulates.
   - Fix: thread the housing (M30×1.5) and clamp it with a nut and washer under the plinth, or use a Ø70 flange with screws at r = 28. Add a filler plug and a shipping procedure.
5. **The platter, hub and spindle are assembled in the wrong order.** The brass hub is only bonded into the acrylic, which expands about 3.7× as much as brass. Then the spindle is pressed into a hub that is already bonded, which loads the bond.
   - Fix: make the hub and spindle as one shrink-fit sub-assembly with a flange. Locate the platter on a spigot and hold it with 3-6 M4 screws. A balance spec of 2 g·mm (about 1.2 µm) is pointless at 0.55 Hz.
6. **The plinth stock can't give a flat 25 mm.** Cast 25 mm sheet varies ±1.5-2 mm. The laminated prototype (2 × 12.7) is to be "machined to 25.4", which leaves no stock to face. Bonding 0.16 m² with 2R 0190 will trap bubbles and show a bond line through the tint.
   - Fix: buy 30 mm, fly-cut both faces to 25 and anneal before polishing. Vacuum-laminate only if the bond line is meant to show.
7. **The arm mounting and height are not designed.** One nut clamping 25 mm of acrylic will creep and loosen. The thread reach is UNCONFIRMED, and no sheet gives the arm height. The record surface works out about 25.8 mm above the plinth top, which needs checking against Rega's spacer range.
   - Fix: use the RB330's three-point mount into brass inserts, or bond in a 25 mm metal arm-board puck. Dimension the spacer stack and the 222 ±0.2 distance.
8. **The lid is too heavy for its hinges.**
   - It weighs 2.21 kg: 0.31 m² × 6 mm × 1190.
   - At 45° it needs about 2.2 × 9.81 × 0.127 ≈ 2.7 N·m, or 1.4 N·m per hinge. Debut hinges are made for lids of about 1 kg.
   - Open is 78°, which is 12° short of upright, but the notes say 12° past it.
   - The hinge block is drawn without its slot, and the cutlist says "1 for the set" when two are needed.
   - Fix: a 4-5 mm lid or friction hinges with a stated torque rating.
9. **Power and earthing will hum.** One adapter is split by a Y lead between the 25 kHz PWM dimmer and the phono regulator, so they share a return path. The LT3045 tops out at 500 mA, which matches the S2's 18 V 500 mA rating. There are three separate supplies and a dimmer hanging in the lead.
   - The LED wattage disagrees: 4.7 W in the notes, 6.8 W in the BOM.
   - Fix: a separate supply (or an LC filter plus a separate return) for the phono stage, and one DC inlet on the rear box.
10. **Thin webs, and servicing from underneath.**
    - The Ø96 pod hole leaves a 16 mm web to the left edge and 19 mm to the back, and the hinge inserts go into that 19 mm.
    - Reaching the phono stage's switches, the arm nut or the wiring means tipping the whole unit and undoing four nuts underneath.
    - A bare acrylic platter, plinth and lid will build up a lot of static.
    - Fix: move the pod hole inboard, add a service hatch or route the switches to the rear box, and give the platter an antistatic treatment or offer a mat.

**2. Missing from the drawings**

- **Bearing and platter assembly:** section A-A is cut at x = 235 and misses the bearing at x = 210. There is no bearing assembly section and no drawing of the bushes. Fits, run-out and finishes are missing (h5 is stated but no H-fits, perpendicularity or Ra), and so are the oil level, the pulley's grub screw and bore, and how the motor mounts in the cup.
- **Arm setup:** no arm height or VTA stack-up, and no alignment reference.
- **Wiring:** no wiring diagram or earth scheme, no cable strain relief where cables cross from the floating plinth to the base, and no Neo-to-motor connector.
- **Assembly and QC:** no torques, no transit locks or packaging, no levelling procedure, and no QC targets (wow and flutter under 0.1 %, speed, rumble).
- **Compliance:** no rating label, serial number, or FCC/CE/UKCA/WEEE marks.
- **Parts list errors:** the posts are a "tinted tube 40×40×44" in the BOM but clear rod 30 × 34.4 in the drawing, and the mark is 40 wide in one place and 44 in another.

**3. Ways to make it more distinctive**

1. **Make the floating posts as stacked layers.** Build the four posts, or the whole float, from 3-5 mm discs in graded tints, so their edges read as contour lines like the horn.
2. **Build a strobe into the platter.** Laser-etch strobe marks on the underside of the platter rim and edge-light them with an LED synced to the mains. It is useful and it glows.
3. **Treat the plinth's edge as layers.** Make the bond line deliberate: three or five laminations of alternating tints, faced and polished. That turns the hard lamination problem into the signature.
4. **Make the visible hardware look finished.** The tint shows everything, so vapour-polish the drilled holes and lay out the brass housing, inserts and studs as a visible pattern. Etch contour rings around the bearing.
5. **Pair the colours across parts.** Choose the platter, plinth and lid from contrasting tints of the eight, so the colours mix where they overlap. A stacked arm rest and cue knob would carry the horn's layers up to where the hand goes.

Scratch crops of the title blocks are in /tmp/claude-0/-home-user-earf/58f35c76-5e68-5534-a6b1-a1673938f4d8/scratchpad/cadrev/.
