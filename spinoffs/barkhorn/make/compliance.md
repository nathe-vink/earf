# Tropos: two compliance checks (2026-10-31)

Requested by the coordinator from the compliance research (R3, `spinoffs/barkhorn/research/2026-10-31/R3-compliance.md`
on r46-owner-notes). Both answers are checked against the CAD as drawn (`product.py`, `components.json`). The changes
proposed here are proposals, not yet in the CAD.

## 1. The remote's battery: it is a coin cell. Swap it.

**As drawn:** `hypex-remote` in `components.json`: Hypex's Remote Control H08U001537, RC-5, **its CR2032 included**.
A CR2032 is a coin cell, so this remote brings in Reese's Law (16 CFR 1263, with UL 4200A):
- a battery door secured by a screw, or by two independent and simultaneous motions;
- testing (UL 4200A, about $1,000 to $3,000);
- warnings on the product, the packaging and the manual;
- a General Certificate of Conformity (GCC) for the remote.

Hypex's remote is made in China, and its door's design is not published. EARF would be the importer and certifier.

**The swap:** an infrared remote on two AAA cells that sends Philips RC-5 codes (device 16; power 50, volume up 51,
down 52, mute 53, the codes in `components.json`). Two routes:

| route | what | a pair | to confirm |
|---|---|---|---|
| **Now: a programmable universal remote on 2 x AAA** | any RC-5-capable universal remote with a code-entry or PC setup, programmed with the four codes before it ships | about $20 to $40 (estimate), against $11 for Hypex's: **+$10 to $30 a pair** | that the model can send RC-5 device 16 (a 10-minute test with the FA122 and HFD); a door with a screw is not needed for AAA |
| **Production: EARF's own remote** | a milled aluminium or cast-acrylic body in the speaker's colour, 2 x AAA behind a screwed door, an RC-5 IR module | about $25 to $45 a unit at 100 (estimate), plus about $3,000 to $8,000 of one-off tooling and firmware (estimate) | a quote; the FCC treats it as a digital device in the system's Part 15B test (R3) |

Either way:
- Reese's Law and the UL 4200A test drop away.
- The FCC Part 15B test still covers the remote with the speaker as a system (R3, line 240).
- AAA cells are user-replaceable, which keeps the remote outside California's SB 1215 (R3).
- The Hypex Remote Kit (the receiver, `hypex-remote-kit`) stays as drawn; only the handset changes.

**Recommendation:** order one programmable AAA remote with the first FA122 and test it in the first week. Drop
`hypex-remote` from the parts list once it works. The cost is +$10 to $30 a pair.

## 2. The amplifier compartment as the fire enclosure: it nearly is. Two gaps.

Hypex wants the earthed amplifier in a flame-rated enclosure and leaves end-product compliance to us (R3). Our
cabinet is PMMA, rated UL 94 HB at best, so it cannot be that enclosure.

**As drawn** (`amp_compartment` in `product.py`):
- `amp-box`: 1.5 mm aluminium, folded and welded, black anodised; 125 x 320 inside, 75 deep.
- Its open side has a flange that seals on a 3 mm EPDM gasket against the back's inner face, with ten screws.
- The FA122's aluminium plate is screwed to the back's outside, over the back's cutout.
- The module reaches through the cutout into the box.
- There are three M12 cable glands in the box's front: HF, woofer and IR.
- `earth-bond-kit` (round 35, B3): an M4 stud on a bared spot of the box, a green and yellow lead to the FA122's earth
  point.

**What already meets the rules:**
- **Earthed:** the box is bonded to protective earth through the FA122's earth point. Anodising insulates, so the stud
  must sit on a spot-faced, bared patch with a star washer, as the kit says. Hipot and earth-continuity checks belong in
  the first-article inspection (`fai.md`, E-series).
- **Openings:** the box has none except the glands. A box with no ventilation openings meets the fire-enclosure opening
  rules of IEC/UL 62368-1 trivially. Nothing burning can drop out of its bottom, and there are no top openings.
- **Ventilation:** none is needed, and none should be added. The FA122 is a plate amplifier built to mount in a closed
  speaker cabinet. Its heat leaves through its plate to the room behind the speaker. The box is airtight so the woofer's
  enclosure stays sealed. Confirm the inside temperature at full output in the 62368-1 pre-check (temperature rise),
  with a thermocouple on the module, in a closed cabinet.

**Two gaps:**
1. **The 20 mm ring of acrylic between the box and the plate.** The back's cutout edge is PMMA. It sits between the
   box's flange (on the inner face) and the plate (on the outer face), so the enclosure's sixth side has a 20 mm band of
   acrylic all the way round.
   - Proposal: **a 1 mm aluminium collar** lining the cutout. It is a folded rectangular sleeve 20 mm long, its inner
     end flanged under the box's flange, its outer end butting the plate.
   - The enclosure is then metal from the box to the plate, and the collar is earthed through the box.
   - Cost: about $40 a pair (estimate). It needs the cutout opened by 2 mm each way (a DERIVED change, not a SPEC one).
2. **The glands are nylon.** Common nylon glands are UL 94 V-2, and the fire enclosure's openings should be closed with
   V-1 or better.
   - Proposal: **nickel-plated brass M12 glands** (or nylon glands with a V-0 listing).
   - Cost: about +$15 a pair (estimate).
   - R3 also asks for lead-free brass, which suits this.

**Also check:**
- The EPDM gasket is a few mm of non-rated material at the flange. Small gaskets are generally accepted, but ask the lab
  at the pre-check.
- The IR receiver's cable leaves through its own gland, and it carries only low-voltage signal.
- The plate's acrylic mounting (`amp-screws-acrylic`) is outside the enclosure, which is fine.

**For the schedule** (`make/schedule.md`):
- an EMC pre-scan, half a day, $800 to $1,500;
- FCC Part 15B Class B SDoC, $1,500 to $3,500, with 2 to 4 weeks' lab lead time;
- a 62368-1 safety pre-check (hipot, touch current, temperature rise), $1,000 to $2,500;
- an NRTL listing to UL 62368-1 (about $10,000 to $25,000, 8 to 16 weeks) before selling 100, not before the debut;
- ask Hypex for any CB report on the FA122 first.

All figures are R3's estimates.

## 3. The ground loop: RCA and S/PDIF together (the engineering audit, 2026-11-01)

**The loop.** The FA122s are class I: each is earthed through its mains cord. Hypex's link joins the master and the
slave with a coax on S/PDIF, so the two speakers' grounds are joined twice: through the mains earth and through the
link's shield. A source connected to both speakers by RCA adds a third path. A loop of mains earth, coax shield and RCA
grounds picks up hum, worst with a turntable or a TV on another socket.

**The fix, in the manual and in the box:**
- **The source goes to the master only.** One RCA pair (or the XLRs, balanced, which reject the loop) into the master;
  the slave takes its channel over the link. No RCA to the slave.
- **A 75 Ω S/PDIF isolation transformer in the link** (an inline coax isolator, shipped with the link cable). It breaks
  the shield path between the speakers without touching the safety earth. About $20 to $40 (est.).
- **Never lift the mains earth.** The guidance says so in words. An earth-lift on the mains is a shock hazard and
  voids the listing. Any ground-lift is on the signal side only.

**To check on the first pair:** the hum at the listening seat with a turntable on another socket, with and without the
isolator.

## 4. The FA122 has no CB or UL report on file; the end product needs its own listing

- **Ask Hypex** for the FA122's CB test certificate and report (IEC 62368-1, with the US national differences) and any
  UL or NRTL recognition. The draft request is `rfq/tropos/h-hypex/letter.md`; nothing has been sent.
- **Plan for the end product's listing.** Tropos is sold as a finished mains product, so it needs its own
  IEC/UL 62368-1 evaluation by an NRTL (UL, Intertek ETL, TÜV, CSA). A CB report on the FA122 shortens that work but
  does not replace it. The listed cord set (`mains-cord-nema`) and the metal compartment as fire enclosure (section 2)
  are part of it.
- **The lab's pre-check (January) also covers:** its reading of stability, 8.6.2.2 (the 20 % push) and 8.6.5
  (`stability/README.md`; both designs fail on today's feet); and the L-pad's abnormal heat (section 5).

## 5. The L-pad's heat in the abnormal case

The L-pad's two resistors can dissipate up to about 26 to 31 W with a full-scale HF sine. That is 25.6 W by this
file's arithmetic at 22.4 V (the FA122's 125 W into 4 Ω), and 30.6 W by the audit's. It all sits inside the sealed
compartment, with the capacitor on the resistors' plate.

- **The audit asked for the resistors to be sunk to the FA122's outer plate. As drawn, they cannot be.** The module
  fills the plate's inside face (236 to 324 by 380 to 660 in the CAD), leaving margins of 16 and 18 mm.
- **What is done instead:**
  - The preset limits the HF channel to 10 V, so in use the pad dissipates at most about 5 W (3.2 W in the series
    resistor, 1.9 W across the driver).
  - The capacitor is stood off 3 mm on nylon spacers.
  - The abnormal case (limiter defeated) is tested in FAI E8. The aluminium compartment is the fire enclosure that
    contains it.
- **If the lab wants the abnormal case cooler:** a heatsink plate through the back beside the FA122, with the
  resistors bolted to its inside. That shows on the back, so it is a look change for the owner.
