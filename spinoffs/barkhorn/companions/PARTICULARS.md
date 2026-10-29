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
| Light | **575 lm** at the COB (the owner, 2026-10-22), 2700 K, CRI 90: a Bridgelux Vero SE 10 at about 175 mA (about 4.3 W), behind a faceted reflector in the hub's bore (fitted: the owner's yes), which lets about 85 % of it out: about **490 lm** out of the fitting **[UNCONFIRMED: datasheet scaling and an estimate; the light out of each tint is unmeasured]** |
| On the table | With the rim 700 above a table: about 490 lux directly below and about 370 lux across a 90 cm table **[computed, direct light only]** |
| Cut-off | The COB sits 22 mm up a 46 mm bore. Above about 46° from vertical you can't see the source (from the geometry, not measured) |
| Dimming | Phase-cut (TRIAC), 100 % to 10 %, with the driver in the canopy: a 175 mA Class 2 consumer-class (FCC Part 15B) driver for 575 lm, still to source **[UNCONFIRMED: the part]**. A 0-10 V driver is an option for bars. **575 lm only:** 1,100 lm is not supported on the low top |
| California (JA8) | CRI 90, R9 50 or more (Bridgelux's 90 CRI minimum, ±3), 2700 K, about 87 to 96 lm/W out of the fitting: met by design. Dimming to 10 %, flicker under 30 % and power factor 0.90 or more: to test **[UNCONFIRMED]** |
| Heat | No fins: the black anodised crown and cap above the shade are the heat sink (round 41). A PEEK ring separates the hub from the shade's collar. Estimated at 575 lm in a 35 °C room: hub 49 °C, LED case 50 °C, LED junction 52 °C, collar and the acrylic next to it 41 °C **[UNCONFIRMED: estimate; thermocouple test planned]** |
| Mains | 120 V reaches the driver in the canopy and stops there. The cord carries the LED's 26 V DC (Class 2): a listed 18 AWG 2-conductor in a black textile braid, its grips tested with the fixture's weight. To be listed to UL 1598 (or ETL) **[NOT YET LISTED]** |
| Shades | Swap by hand, no tools, with a quarter-turn bayonet and a detent. The shade carries no electrical parts. It is clamped between the collar's flange and a ring on silicone, so a failed bond can't drop it |
| Materials | Shade: three formed layers of cast acrylic (a 9 mm tinted shell, a 3 mm opal liner, a 3 mm tinted skin), polished, vented at the rim, with a black anodised aluminium collar and clamp ring. Hub, crown, cap and pins: black anodised aluminium (the cap polished). PEEK ring. Canopy: black cast acrylic, polished. Black textile cord |
| Tints | Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke, each cast to match its speaker's colour when lit (README, round 32f) |
| Sold separately | Shades, in each tint |

## Core, the table lamp (was Orb)

| | |
|---|---|
| Size | Ball 160 mm across; base **120 × 30** (round 32f's, again in round 41; 48 in rounds 35 to 39); **180 mm** tall |
| Weight | About **1.46 kg**: the ball 0.76, the base 0.70 (its steel ballast 0.17, its cells 0.13). It tips at about 43° **[UNCONFIRMED: computed]** |
| Light | Warm-dim, 2200 to 2700 K as it dims, CRI 90+, about 200 lm at full (2.5 W) **[UNCONFIRMED: the LED module is still to choose; the light out of the ball is unmeasured]** |
| Control | Touch the black ring: tap to switch, hold to dim |
| Power | One product, plugged in or not. USB-C (5 V 3 A; a 20 W adapter and a 2 m black fabric cable in the box, the cable out of a notch underneath). It runs while it charges and charges in about 2.5 hours **[UNCONFIRMED: estimate]** |
| Battery | Three LiFePO4 18650 cells (about 14.4 to 17.3 Wh), standard cells in holders round the LED, behind a hatch under the base: four captive screws, a common screwdriver, the user's to replace. About **4.7 to 5.6 hours at full brightness** (2.5 W) and 5.8 to 7 at the bar setting (2 W) at the default 90 % charge limit; about 5.2 to 6.2 and 6.5 to 7.8 at a full charge; about 2,000 cycles to 80 % **[UNCONFIRMED: the cells are still to qualify, and their capacity to confirm]** |
| Protection | IP44 by design: O-rings at the window, the chassis and the hatch, and a sealed USB-C receptacle, with the ball on or off. No exposed contacts **[UNTESTED]** |
| Safety | One product, certified to IEC/UL 62368-1 with its battery annex; the cells to IEC 62133-2 and UN 38.3. User-replaceable, as EU Regulation 2023/1542 requires of portable batteries in appliances from February 2027 **[NOT YET CERTIFIED]** |
| Shipping | Each cell about 4.8 to 5.8 Wh (at most 20 Wh), the set at most 17.3 Wh (at most 100 Wh): it ships under the small-battery exception (49 CFR 173.185(c)) as UN3481, contained in equipment, not as fully regulated Class 9 |
| Charger | A switching LiFePO4 charger with power path (Analog Devices LTC4162-F) and a DOE Level VI adapter: a battery charger system to the DOE standard and California Title 20, to be listed in the CEC's MAEDbS under Core's model number **[NOT YET TESTED]** |
| Materials | The ball: one tinted cast acrylic shell, two formed halves joined at the equator, frosted inside, polished outside, its port lined in black anodised aluminium. The base: black cast acrylic, polished, over an aluminium chassis and a steel ballast. Touch ring and hatch: black anodised aluminium. Silicone seat and foot ring |
| Tints | Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke **[the casts were matched with three layers (12 mm of tint); one 9 mm layer needs the caster to re-match each cast on chips]** |
| Sold separately | Balls, in each tint (a ball lifts off and holds no electrical parts). Replacement cells are standard LiFePO4 18650s (LiFePO4 only: the hatch's label says so) |

## Prices

The owner sets the prices; the coordinator set Core's on the owner's "For everything else make your call" (2026-10-25). The suggestions (README, round 35):
- Hemisphere: $795 to $895 with one shade; shades $295 to $345.
- Core: **$650** with its cells (set 2026-10-25; was $545 to $645 plug-in, plus $95 to $125 for the cartridge).
