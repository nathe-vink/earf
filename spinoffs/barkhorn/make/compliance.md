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
  (`stability/README.md`; both designs fail on today's feet); and the HF channel's abnormal case, now without an L-pad (section 5).

## 5. The L-pad is gone: the HF channel attenuated in the DSP (the engineering audit, 2026-11-01)

**The problem:** the passive L-pad could dissipate 25 to 31 W inside the sealed compartment with a full-scale HF sine.
That is 25.6 W by this file's arithmetic at the FA122's 22.4 V, and 30.6 W by the audit's. A first answer, capping the
HF channel at 10 V, cost 7 to 8 dB of the horn's headroom.

**The answer: no L-pad.** The 6 dB the horn needs comes off in the FA122's DSP. The 33 uF series capacitor stays,
stood off 3 mm on nylon spacers.

| | the L-pad | DSP only |
|---|---|---|
| heat in the compartment, abnormal case | 25.6 to 30.6 W | **0 W** (beyond the amplifier's own) |
| the HF channel's headroom | full only with the pad's heat; 10 V if capped (about 110 dB at 1 m) | **the FA122's full 22.4 V: 31 W into the driver, about 123 dB at 1 m**, past the woofer's 117 |
| the driver in the abnormal case (limiter defeated) | 8.9 W | **31 W, within its 140 W (AES) rating**; the heat is in its own motor in the pod, outside the sealed box |
| hiss at 1 m | the pad's 6 dB below | **about 8 to 10 dB SPL** (the reviewer: about 8; about 10 at 50 uV of amplifier noise), below a quiet room's 25 to 30 dB, and lower again at the seat |
| protection if the preset is lost | the capacitor (300 Hz, first order) | the same capacitor |
| parts | two 25 W resistors and a plate, about $24 | none |

**Checks:**
- FAI E8: a full-scale HF sine with the limiter defeated, with thermocouples on the pod and the boss;
- the hiss measured at 1 m on the first pair.

## 6. DRAFT (2026-11-13): the FA123 in place of the FA122

> **OPEN until Hypex answers: the bridged load.** Channels 1 and 2 bridged (BTL) drive the 15PR400-8, whose lowest
> impedance is 5.55 ohm in the model (5.9 on FaitalPRO's sheet): inside Hypex's 4 ohm BTL minimum, under its 8 ohm
> recommendation. Nothing below is final until Hypex has confirmed it. (`fa123.md`)

What changes in sections 2 to 5 if the FA123 is fitted (the CAD: `product.py`, `out-cloud/`, built 2026-11-13):

- **Section 2, the compartment as the fire enclosure.** The same construction, 45 mm longer: 125 x 75 x 365 inside,
  z 298.5 to 696.5 with its flange, the gasket frame 158 x 398. Still 1.5 mm 5052, earthed through the amplifier's
  earth point, the plate the only opening and the plate itself metal. The cutout leaves 14.5 mm to the box's ends and
  20 mm behind the module, against Hypex's 3 mm to any conductive part. No ventilation, as before.
- **Heat (the 62368-1 temperature-rise pre-check).** Idle about 11 W against the FA122's 7.5 (the NC100HF's 3.5 W
  added); at 1/8 of rated power, with the soft clip at 125 W into 8 ohm, about 13 W against 9. Measure the rise at full
  output, the box sealed, an ambient of 35 C at most (Hypex's limit), as already planned. Hypex's thermal limiter
  (-6 dB) and shutdown protect the amplifier; the NC100HF has no over-temperature protection of its own, and is rated
  20 W continuous at 25 C: above the 1 kHz crossover its programme power is a few watts.
- **Section 4, the certificate.** Ask Hypex for the FA123's CB test certificate and report (IEC 62368-1, with the US
  national differences) in place of the FA122's. The end product still needs its own listing.
- **The rating engraving.** The input rating stays 350 W maximum (Hypex gives the same figure for both); the
  engraving moves 45 mm lower with the plate's lower edge (z 298.5 to 317.25).
- **Section 5, the HF channel.** The NC100HF swings about the FA122's 22 V in an FA123 (limited by the NC122MP's
  supply): about 31 W into the DE1085TN-16, within its 140 W. The 33 uF series capacitor stays; no L-pad.
- **The plate's mount holes.** Ten M4 inserts, five a side, 5 in from the plate's edges and evenly spaced (175, 87.5,
  0): a PLACEHOLDER drawn from the FA122's rule; a retailer's square-on photograph of the FA123 agrees with it to the
  photograph's resolution (about 0.5 mm). Confirm against Hypex's drilling drawing before the back is cut.
