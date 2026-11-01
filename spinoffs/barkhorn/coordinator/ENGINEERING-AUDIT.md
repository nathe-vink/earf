# Engineering audit of the line (2026-11-01)

The owner asked, 2026-11-01 00:20 UTC: **"Are the mechanics and electronic aspects of each of the products legit?"**

How it was checked:
- Workflow wf_32ea5a79-234 ran an audit per product, each by an engineer reading the branch's own files and doing the
  arithmetic.
- An independent reviewer then tried to refute each audit: it re-derived the numbers and checked the named parts
  against datasheets.
- A completeness pass looked for what nobody had checked.
- The raw results are in `engineering-audit/2026-11-01/` (`<product>-audit.json`, `<product>-review.json`).

The verdicts below are the reviewed ones. "Not yet sound" means *buildable in principle, but not as drawn*. Nothing
was found to be fake.

## Verdicts

### Tropos: not yet sound (mechanically); the electro-acoustics are legitimate

**Real:**
- Parts: FaitalPRO 15PR400-8, B&C DE1085TN-16, and the Hypex FusionAmp FA122 (auto-ranging mains).
- The box, port, horn-loading, crossover and power arithmetic reproduce from the datasheets.

**Blocks a safe prototype:**
1. **Stability.** IEC 62368-1 8.6.2.2 pushes with 20 % of the weight at the top. S7 used 13 %. On the 420 × 560
   footprint both horns very likely fail in every direction:
   - Strata: -23 % forward, -34 % back, -11 % side;
   - current: -19 %, -37 %, -11 %.
2. **The horn's retention.** The post feet stand loose in sleeved sockets, and one M6 tie rod is the only hold-down.
   The horn starts to lift at 23–46 N at its top (Strata).

**Open:**
- No DSP preset exists, though both drivers depend on one. The preset can also be changed by any owner (fix: Hypex's
  filter password).
- No measurements.
- The FA122 has no CB/UL report on file.
- Abnormal heat: the L-pad dissipates up to 30.6 W inside the sealed compartment.
- FAI test levels exceed the woofer's Xmax.
- No listed mains cord set.
- The woofer torque is over M6 capacity.
- An RCA + S/PDIF ground loop.
- Transit.

**Owner:** the speaker lane, list sent 02:30 UTC. Base changes that alter the look come back to the owner.

### Hemisphere: not yet sound → fixed in spec (367709bf) and CAD (5e4b7aba, 0 clashes)

**Real:** a Gen 7 Vero 10 (BXRC-27G1000-D-73, datasheet DS90) on an ERP 180 mA driver; 2.7 W runs cool.

**Fixed:**
- Order the COB by voltage bin. A low bin is about 23.0 V, under the driver's 24 V floor.
- The 97-CRI part for JA8.
- Screwed shouldered pins (4.0 mm engagement), a centering land (0.2 play) and a steel tether.
- A steel crossbar and closed driver enclosure under the acrylic canopy, which is a cover only.
- A 36–48 V Class 2 supply for the swag.

**Bench:** bin and driver regulation hot; ripple and flicker; LM-79 (the fixture gives somewhat less than the LED's
575 lm).

### Core: not yet sound → architecture fixed in spec and CAD; the board is still to design

**Real:** certified LiFePO4 cells.

**Fixed:**
- A 130 lm/W LED: 200 lm at 1.5 W or less, with foldback.
- A drawn heat path: chassis arms to the touch ring, about 20 K over the room estimated, against a 25 K target.
- Milled button-top bays with a shrouded + contact.
- Back-to-back FETs per cell.
- USB PD at 9 V. At 5 V only about 4.3 V reached the charger, which needs 4.5.
- A redrawn dock: a center disc and a ring, with low-force pins.
- Coulomb counting, giving about 2.7 h to 90 %.

**Open:**
- The board itself (schematic, layout, firmware).
- Bench thermal and touch tests.
- The CAD still draws the old charging cable lying out of the base's notch. Remove it from the drawn assembly, as the
  owner's cordless ruling says. Close the notch only if the dock is signed.

### Mantle: not yet sound

**Real:**
- Bought parts: Rega RB330 (222 mm), Rega's 24 V motor kit with the Neo PSU, Pro-Ject Phono Box S2 and Ortofon 2M.
- The bearing's Hertz contact checks out, with a static margin of about 1.8×.
- The rigid posts remove the old 25–36 Hz float.

**Open:**
1. **The drive ratio.** The files size the pulley for 250 rpm, i.e. the motor driven at 50 Hz. If the US Neo drives it
   at 60 Hz, the platter turns at 40 rpm. Bench the motor on the actual Neo, then turn the pulley; about 32.8 mm for
   300 rpm.
2. Strata has no rear panel, though the RCA jacks, earth, switch and DC inlet are bought. It has no wiring or earth
   drawing and no rating label.
3. The LED strip doesn't fit its slot (8 mm into 5 mm, 2 mm corners). Use a strip of 5 W/m or less.
4. The DPDT bypass leaves 23.5 kΩ on the cartridge. Use a 4PDT or a relay.
5. The bearing:
   - 2.5 ml of oil for about 1.2 ml of space, and no vent;
   - the spindle is 304 in the BOM but 440C on the drawing;
   - the clamp preload swings about 3 kN over 20 K.
6. The feet sit near 190 Hz, so they don't isolate. Drop the claim or redesign them.
7. The lid may stop the arm. Check against the real RB330 counterweight.
8. The motor mount is not Rega's method (Rega hard-mounts it).
9. The platter screws bear on acrylic at 13–42 MPa.
10. Outcrop's S2 tunnel has no room for its plugs, and its tripod is unstable.

**Owner:** the Mantle lane, which is stopped. The fix list is to send when the owner picks A or B.

### Mother EARF (the bar globe): not yet sound

**Real:** the day look, colored shadows under a hard spot. That is physics and works today.

**Missing:**
- A hang point, rigging and a secondary. The latest plan is a plinth, but the cradle and armature are undefined.
- Structure: 22 of 23 pieces are held by cement alone. The 2D files can't cut the 60° meridian joints.
- Handling: assembled, the globe can't pass the plan's 32 in doors.
- The lit rims are a shader with no physical source.
- Fire: about 5 GJ of non-FR PMMA, CFC 807 (SFFD), unanswered.
- The plinth sits on the lantern's 7 Hz floated floor.

**Route:**
- A demountable bolted armature with floating clamps, so the cement is cosmetic.
- The plinth anchored to the floated slab, with the acoustician's mounts.
- The day look.
- A 300 mm lit test piece before any glow is promised.
- An SFFD pre-application meeting.

**Owner:** the bar lane, stopped. It's the owner's call when to resume.

## Claims corrected because of this audit
- **Deck v32–v33 (risks, light):**
  - Testing is "planned", not "booked".
  - Tropos's amplifier runs on mains inside its own compartment, so not every product uses an external supply.
  - Core uses cells, not a listed pack.
  - "575 lumens" is the LED's figure.
- **Site and brand lanes:** asked to sweep the same claims.

## Completeness pass (what no review had checked)

- **HIGH: Core's battery compartment as a drop-safe and fire-safe enclosure: UL 153 Supplement SA's drop programme and the acrylic around the cells** (Core, including the Core ball, which is sold separately). Documented: Core's listing route is UL 153 with Supplement SA (r32-lamps-final:spinoffs/barkhorn/companions/launch/certification.md; PARTICULARS.md). Full text in completeness.json.
- **MEDIUM: Chemical compatibility and stress cracking beyond the cleaning card: thread-locker on stressed acrylic, bar spirits and sanitisers, and cement vapour sealed into cemented cavities** (Hemisphere, Core, Mantle (Tropos already has a control)). Documented FOR TROPOS ONLY: crazing is risk A1 in r33-speaker-horn:spinoffs/barkhorn/make/horn-risks.md. Full text in completeness.json.
- **MEDIUM: Transit, packaging and owner set-up: the shipping plan hands the owner the joints the reviews found weakest** (Tropos, Mantle, Core, Hemisphere, Mother desk globe). Documented ONLY AS A CONCEPT: r47-brand:spinoffs/barkhorn/brandbook/PACKAGING.md proposes crates and ISTA 3A/3B tests ('every size, stock and test below is a proposal'). Full text in completeness.json.
- **MEDIUM: Lithium transport mode for Core: four documents, two answers, and the 2026 air state-of-charge rule** (Core (sales, spare cells, returns and warranty shipments)). Documented, AND CONTRADICTORY. Full text in completeness.json.
- **LOW: ESD and EMC design inside acrylic bodies that give no shielding** (Core, Mantle, Tropos, Hemisphere, Mother desk globe). No review examined this. Full text in completeness.json.
