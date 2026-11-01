# Hemisphere and Core: the particulars for earf.world

**Hemisphere South is dropped** (round 38, the owner, 2026-10-25: "Get rid of south altogether and just call it hemisphere."), and Hemisphere North is now just **Hemisphere**. South's CAD, parts list and renders stay in the repo as a record.

**Round 41 (the owner signed round 40, 2026-10-29):** round 32f's low profiles are back. Hemisphere has the low top (no fins), and Core sits on the 120 × 30 base with three 18650 cells.

Read from the fab kits on 2026-10-22 (updated 2026-10-29 for round 41), after round 36 (the owner's answers: the pendant at 575 lm with the reflector) and round 35 (the names, the engineering review's fixes, Core's own
battery): `crystal.py`, `out-dome-pendant/bom.md`, `out-orb-table/bom.md`,
`components.json`, `hemisphere_thermal.py` and `hemisphere_brightness.py`. Weights come from the CAD solids (acrylic
1.19, aluminium 2.7, steel 7.85, PEEK 1.30 g/cm³), plus estimated weights for the bought parts.
**[UNCONFIRMED]** marks anything not yet measured, tested or quoted. Nothing here has been built yet: these are
design figures. The file names stay as they were (`dome_pendant.py`, `orb_table.py`, the `lamp-dome-*` and
`lamp-orb-*` images), so nothing downstream breaks.

## Hemisphere, the pendant (was Dome, then Hemisphere North)

| | |
|---|---|
| Size | Shade 200 mm across, 100 mm deep at the rim. Above the crown: a clamp ring, then a black crown 80 across and 11.5 tall, then a cap 40 × 14; the top of the cap is **126 mm above the rim** (round 32f's low top). Canopy 150 × 50. Standard drop 600 mm, cut to length (the rim 776 mm below the ceiling as supplied) |
| Weight | Shade and fixture about **1.59 kg**: the shade about 1.1 (its acrylic 0.8; the aluminium collar and clamp ring 0.29), the hub 0.23, the crown 0.14, the cap 0.05. Canopy with its driver about 0.3 kg **[UNCONFIRMED: computed]** |
| Light | The owner's **575 lm** level (2026-10-22): about **590 lm** at the COB on the chosen driver's 180 mA, 2700 K, CRI 90: a Bridgelux Gen 7 Vero 10, the 97 CRI array (BXRC-27H1000-D-7x, datasheet DS90; about 4.4 W; the review of 2026-11-01 corrected "Vero SE 10"), behind a reflector spun to order for the hub's bore (fitted: the owner's yes), which lets about 85 % of it out: about **500 lm** out of the fitting **[UNCONFIRMED: datasheet scaling and an estimate; the light out of each tint is unmeasured]** |
| On the table | With the rim 700 above a table: about 500 lux directly below and about 380 lux across a 90 cm table **[computed, direct light only]** |
| Cut-off | The COB sits 22 mm up a 46 mm bore. Above about 46° from vertical you can't see the source (from the geometry, not measured) |
| Dimming | Phase-cut, forward (TRIAC) or reverse (ELV), 100 % to 1 %, or 0-10 V, with the driver in the canopy: the ERP Power ESS010W-0180-42 (180 mA, 24-42 V, Class 2, FCC Part 15 Class B at 120 V; round 42). One driver serves homes and bars **[REVIEW 2026-11-01: at 180 mA the COB runs about 24.9 V cold and 24.2 V at Tc 85 °C (typical), and a low-Vf bin about 23.0 V, under the driver's 24 V floor. The COBs are ordered by bin (Vf 24.5 V or more at 180 mA and Tc 85 °C), or a driver whose window reaches about 21 V is chosen; to bench-test. The alternate EPtronics LD6W120-36-C0170-TL (22-36 V) dims only to about 15 %]**. **575 lm only:** 1,100 lm is not supported on the low top |
| California (JA8) | CRI 97, R9 93 or more (the 97 CRI array, for margin; review 2026-11-01), 2700 K, about 87 to 96 lm/W out of the fitting: met by design. Dimming to 10 %, flicker under 30 % at every level (the driver's output ripple, checked on the bench) and power factor 0.90 or more: to test **[UNCONFIRMED]** |
| Heat | No fins: the black anodised crown and cap above the shade are the heat sink (round 41). A PEEK ring separates the hub from the shade's collar. Estimated at 575 lm in a 35 °C room: hub 49 °C, LED case 50 °C, LED junction 52 °C, collar and the acrylic next to it 41 °C **[UNCONFIRMED: estimate; thermocouple test planned]** |
| Mains | 120 V reaches the driver in the canopy and stops there. The cord carries the LED's 26 V DC (Class 2): a listed 18 AWG 2-conductor in a black textile braid, its grips tested with the fixture's weight. The canopy's cord grip, cable gripper and screws anchor in a steel crossbar, and the driver and 120 V splices sit in a closed steel enclosure on it; the black acrylic canopy is a cover only (review 2026-11-01). The plug-in swag runs on a 36 to 48 V Class 2 supply and a 180 mA constant-current buck, which covers the COB's 23.0 to 26.9 V (a 24 V supply could not). To be listed to **UL 153 (plug-in) or UL 1598 (hardwired) with its own shades, as the owner chooses** (`launch/certification.md`: the plug-in swag first, with a steel suspension cable carrying the weight; the cord and canopy above describe the hardwired version) **[NOT YET LISTED]** |
| Shades | Swap by hand, no tools, with a quarter-turn bayonet and a detent: three stainless shouldered pins screwed through the PEEK ring into the hub, 4 mm or more of engagement against a centering land (play 0.2 or less), and a stainless safety tether from the hub to the collar as secondary retention (review 2026-11-01). The shade carries no electrical parts. It is clamped between the collar's flange and a ring on silicone, so a failed bond can't drop it |
| Materials | Shade: three formed layers of cast acrylic (a 9 mm tinted shell, a 3 mm opal liner, a 3 mm tinted skin), polished, vented at the rim, with a black anodised aluminium collar and clamp ring. Hub, crown, cap and pins: black anodised aluminium (the cap polished). PEEK ring. Canopy: black cast acrylic, polished, over a steel crossbar and enclosure. Black textile cord |
| Tints | Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke, each cast to match its speaker's colour when lit (README, round 32f) |
| Sold separately | Shades, in each tint |

## Core, the table lamp (was Orb)

| | |
|---|---|
| Size | Ball 160 mm across; base **120 × 30** (round 32f's, again in round 41; 48 in rounds 35 to 39); **180 mm** tall |
| Weight | About **1.46 kg**: the ball 0.76, the base 0.70 (its steel ballast 0.17, its cells 0.12). It tips at about 43° **[UNCONFIRMED: computed]** |
| Light | Warm-dim, 2200 to 2700 K as it dims, CRI 90+, about 200 lm at full from 1.5 W or less (an LED of 130 lm/W or better; review 2026-11-01, was 2.5 W) **[UNCONFIRMED: the LED module is still to choose; the light out of the ball is unmeasured]** |
| Heat | A designed path: the LED's board to the aluminum chassis, its two arms and Ø8 posts through the cell-free corners, and a 0.5 insulating thermal pad to the anodized touch ring (about 0.4 W/K); the cells' bays stay 0.9 or more from it. About 1.5 W in the base at full while charging. Foldback: at 55 °C on the chassis the light dims to 70 %; at 60 °C charging drops to 0.5 A; the cells don't charge above 45 °C. Target: the chassis 25 K or less over the room **[UNCONFIRMED: to prove on the bench]** |
| Control | Touch the black ring: tap to switch, hold to dim (baseline tracking and a 50 ms debounce, tested on battery, cable and dock) |
| Power | Cordless (the owner, 2026-10-31). It charges on its dock, or from USB-C underneath, at 9 V by USB PD from the 20 W adapter in the box (`CORE-RECHARGE.md`; 5 V left too little for the charger). It runs while it charges and charges in about **2.7 hours to 90 %** at 1.5 A **[UNCONFIRMED: computed]** |
| Battery | Three LiFePO4 18650 cells, Power Sonic PSL-FP-IFR18650EC (1.5 Ah, 4.8 Wh each; **14.4 Wh**; its button-top version to confirm), standard **button-top** cells in bays milled in the base, on bare spring contacts (a shrouded + that only a button top reaches; review 2026-11-01), round the LED, behind a hatch under the base: four captive screws, a common screwdriver, the user's to replace. **About five hours a charge** (the copy until the bench proves more; computed since the review of 2026-11-01: about 7.8 h at full brightness, 1.5 W, and 9.7 at the bar setting, 1.2 W, at the default 90 % charge limit (counted by a coulomb counter: LiFePO4's flat curve can't be read by voltage); about 8.6 and 10.8 at a full charge); 2,000 cycles at full depth (the datasheet) **[UNCONFIRMED: computed from the datasheet's rated capacity, at 90 % conversion]** |
| Protection | IP44 by design: O-rings at the window, the chassis and the hatch, and a sealed USB-C receptacle, with the ball on or off. No exposed contacts **[UNTESTED]** |
| Safety | One product, to be listed to **UL 153 with Supplement SA** (battery-operated portable luminaires; `launch/certification.md`, round 43; earlier drafts said IEC/UL 62368-1); the cells to IEC 62133-2 and UN 38.3. User-replaceable, as EU Regulation 2023/1542 requires of portable batteries in appliances from February 2027 **[NOT YET CERTIFIED]** |
| Shipping | Each cell 4.8 Wh (at most 20 Wh), the set 14.4 Wh (at most 100 Wh); the cells carry UN 38.3, IEC 62133 and UL 1642 on their datasheet: it ships under the small-battery exception (49 CFR 173.185(c)) as UN3481, contained in equipment, not as fully regulated Class 9 |
| Charger | A switching LiFePO4 charger with power path (Analog Devices LTC4162-F), each cell behind back-to-back FETs under an ideal-diode controller, off until checked (review 2026-11-01; one FET per cell let cells cross-charge at about 9 A), and a DOE Level VI adapter: a battery charger system to the DOE standard and California Title 20, to be listed in the CEC's MAEDbS under Core's model number **[NOT YET TESTED]** |
| Materials | The ball: one tinted cast acrylic shell, two formed halves joined at the equator, frosted inside, polished outside, its port lined in black anodised aluminium. The base: black cast acrylic, polished, over an aluminium chassis and a steel ballast. Touch ring and hatch: black anodised aluminium. Silicone seat and foot ring |
| Tints | Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke **[the casts were matched with three layers (12 mm of tint); one 9 mm layer needs the caster to re-match each cast on chips]** |
| Sold separately | Balls, in each tint (a ball lifts off and holds no electrical parts). Replacement cells are standard LiFePO4 18650s (LiFePO4 only: the hatch's label says so) |

## Prices

**All prices: owner to set.** Two sources disagree, so neither is a price yet (the brand lane's contradiction sweep,
2026-10-31):
- Hemisphere: **owner to set.** README round 35 suggested $795 to $895 with one shade (shades $295 to $345); the research
  (R4) suggests about $1,200.
- Core: **owner to set.** $650 with its cells was set by the coordinator on 2026-10-25 (was $545 to $645 plug-in, plus
  $95 to $125 for the cartridge); R4 suggests about $750.
