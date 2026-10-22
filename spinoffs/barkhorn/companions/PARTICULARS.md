# Hemisphere North, Hemisphere South and Core: the particulars for earf.world

Read from the fab kits on 2026-10-22, after round 35 (the names, the engineering review's fixes, South, Core's own
battery): `crystal.py`, `out-dome-pendant/bom.md`, `out-hemisphere-south/bom.md`, `out-orb-table/bom.md`,
`components.json`, `hemisphere_thermal.py` and `hemisphere_brightness.py`. Weights come from the CAD solids (acrylic
1.19, aluminium 2.7, steel 7.85, PEEK 1.30 g/cm³), plus estimated weights for the bought parts.
**[UNCONFIRMED]** marks anything not yet measured, tested or quoted. Nothing here has been built yet: these are
design figures. The file names stay as they were (`dome_pendant.py`, `orb_table.py`, the `lamp-dome-*` and
`lamp-orb-*` images), so nothing downstream breaks.

## Hemisphere North, the pendant (was Dome)

| | |
|---|---|
| Size | Shade 200 mm across, 100 mm deep at the rim. Above the crown: a clamp ring, then black fins 80 across and 36 tall, then a cap 40 across; the top of the cap is 160 above the rim. Canopy 150 × 50. Standard drop 600 mm, cut to length (the rim 810 mm below the ceiling as supplied) |
| Weight | Shade about 1.1 kg (its acrylic 0.8; the aluminium collar and clamp ring 0.32). Fixture below the ceiling about 0.5 kg (hub 0.27, fins 0.13). Hanging total about 1.7 kg; canopy with its driver about 0.3 kg **[UNCONFIRMED: computed]** |
| Light | 2700 K, CRI 90 COB (Bridgelux Vero SE 10). Two levels; the owner picks: **about 1,100 lm** at the COB (350 mA, about 9 W), or **about 575 lm** (about 175 mA, about 4.3 W). A reflector in the hub sends about 85 % of it out, so about 935 or 490 lm leave the fitting **[UNCONFIRMED: datasheet and estimate; the light out of each tint is unmeasured]** |
| On the table | With the rim 700 above a table: about 930 lux directly below and about 700 lux across a 90 cm table at 1,100 lm; about 490 and 370 lux at 575 lm **[computed, direct light only]** |
| Cut-off | The COB sits 22 mm up a 46 mm bore. Above about 46° from vertical you can't see the source (from the geometry, not measured) |
| Dimming | Phase-cut (TRIAC), with the driver in the canopy: Mean Well PCD-16-350A for 1,100 lm; a 175 mA driver for 575 lm, still to source. A 0-10 V driver is an option for bars **[UNCONFIRMED: dimmer compatibility; FCC class for home sales]** |
| Heat | Fins above the shade sit in room air. A PEEK ring separates the hub from the shade's collar. Estimated at 1,100 lm in a 35 °C room: hub 52 °C, LED junction 60 °C, collar and the acrylic next to it 42 °C **[UNCONFIRMED: estimate; thermocouple test planned]** |
| Mains | 120 V reaches the driver in the canopy and stops there. The cord carries the LED's 26 V DC (Class 2): a listed 18 AWG 2-conductor in a black textile braid, its grips tested with the fixture's weight. To be listed to UL 1598 (or ETL) **[NOT YET LISTED]** |
| Shades | Swap by hand, no tools, with a quarter-turn bayonet and a detent. The same shades fit Hemisphere South. The shade carries no electrical parts. It is clamped between the collar's flange and a ring on silicone, so a failed bond can't drop it |
| Materials | Shade: three formed layers of cast acrylic (a 9 mm tinted shell, a 3 mm opal liner, a 3 mm tinted skin), polished, vented at the rim, with a black anodised aluminium collar and clamp ring. Hub, fins and pins: black anodised aluminium. PEEK ring. Canopy and cap: black cast acrylic, polished. Black textile cord |
| Tints | Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke, each cast to match its speaker's colour when lit (README, round 32f) |
| Sold separately | Shades, in each tint |

## Hemisphere South, the bowl (new)

| | |
|---|---|
| Size | The same 200 mm shade turned opening up, a bowl 100 deep. A frosted lid 196 across lies on its rim. Below the bowl: a clamp ring, a 60 mm neck, black fins 90 across and 50 tall, and a finial; 226 from the rim to the finial. A 10 mm black rod 450 long runs to the canopy (150 × 50) |
| Weight | Shade about 1.1 kg; fixture with lid and rod about 0.9 kg; hanging about 2.0 kg **[UNCONFIRMED: computed]** |
| Light | A ring of 2700 K, CRI 90 mid-power LEDs on the hub, round the rod, facing up. Twice North's light, because light bounced off a ceiling needs about twice the lumens to feel as bright: **about 2,200 lm** (about 15 W), or **about 1,150 lm** (about 7.7 W) if North takes 575. About 57 % leaves through the mouth and lid as a wash on the ceiling; the rest lights the bowl, which glows in its tint **[UNCONFIRMED: board to make; estimate]** |
| Dimming | Phase-cut (TRIAC), with a Mean Well PCD-class driver in the canopy **[UNCONFIRMED: model to match the board]**; 0-10 V as the bar option |
| Heat | Fins below the bowl in room air, 60 mm under the crown on a neck, with the PEEK ring as North's. Estimated at 2,200 lm in a 35 °C room: hub 50 °C, LED junction 65 °C, collar 41 °C. The fins' warm air rises past the crown: estimated at about 16 K above the room right at the crown at 2,200 lm (11 K at 1,150), so about 51 °C in a 35 °C room, at the limit. The thermocouple test decides it **[UNCONFIRMED: estimate]** |
| Hanging | Rim 450 to 600 below a ceiling 2.6 to 3.2 m high, so the wash spreads. Its light goes to the ceiling, not to a table |
| Shades | The same shades as North, with the same catch: the collar's slots end in a T, so the shade's weight holds it either way up |
| Dust | A 3 mm frosted acrylic lid on the rim, on three small silicone bumpers. It lifts up the rod for wiping |
| Mains | As North's: the driver in the canopy, Class 2 DC down the rod. To be listed to UL 1598 **[NOT YET LISTED]** |

## Core, the table lamp (was Orb)

| | |
|---|---|
| Size | Ball 160 mm across; base 120 across and 48 tall (was 30: the cells lie under the LED); 198 mm tall |
| Weight | About 2.2 kg: the ball 0.75, the base 1.45 (its steel ballast 0.75, its cells 0.25) **[UNCONFIRMED: computed]** |
| Light | Warm-dim, 2200 to 2700 K as it dims, CRI 90+, about 200 lm at full (2.5 W) **[UNCONFIRMED: the LED module is still to choose; the light out of the ball is unmeasured]** |
| Control | Touch the black ring: tap to switch, hold to dim |
| Power | One product, plugged in or not. USB-C (5 V 3 A; a 20 W adapter and a 2 m black fabric cable in the box, the cable out of a notch underneath). It runs while it charges and charges in about 3.5 hours **[UNCONFIRMED: estimate]** |
| Battery | Three LiFePO4 26650 cells (about 29 Wh), standard cells in a holder behind a hatch under the base: four captive screws, a common screwdriver, the user's to replace. About 9 hours at full brightness at the default 90 % charge limit, about 10.5 at a full charge; about 2,000 cycles to 80 % **[UNCONFIRMED: the cells are still to qualify]** |
| Protection | IP44 by design: O-rings at the window, the chassis and the hatch, and a sealed USB-C receptacle, with the ball on or off. No exposed contacts **[UNTESTED]** |
| Safety | One product, certified to IEC/UL 62368-1 with its battery annex; the cells to IEC 62133-2 and UN 38.3. User-replaceable, as EU Regulation 2023/1542 requires of portable batteries in appliances from February 2027 **[NOT YET CERTIFIED]** |
| Materials | The ball: one tinted cast acrylic shell, two formed halves joined at the equator, frosted inside, polished outside, its port lined in black anodised aluminium. The base: black cast acrylic, polished, over an aluminium chassis and a steel ballast. Touch ring and hatch: black anodised aluminium. Silicone seat and foot ring |
| Tints | Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke **[the casts were matched with three layers (12 mm of tint); one 9 mm layer needs the caster to re-match each cast on chips]** |
| Sold separately | Balls, in each tint (a ball lifts off and holds no electrical parts). Replacement cells are standard LiFePO4 26650s |

## Prices

The owner sets the prices. The suggestions (README, round 35):
- Hemisphere North: $795 to $895 with one shade; shades $295 to $345.
- Hemisphere South: $845 to $945 with one shade (a bigger LED and driver, a lid and a rod).
- Core: $595 to $695 with its cells (was $545 to $645 plug-in, plus $95 to $125 for the cartridge).
