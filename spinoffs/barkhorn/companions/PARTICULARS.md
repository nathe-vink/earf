# Dome and Orb: the particulars for earf.world

Read from the fab kits on 2026-10-20, after round 32f (black hardware, the plug-in Orb with its battery cartridge, the
tints cast to the speakers' hues): `crystal.py`, `out-dome-pendant/bom.md`, `out-orb-table/bom.md` and
`components.json`. Weights are computed from the CAD solids (acrylic 1.19, aluminium 2.7, steel 7.85 g/cm³) plus the
bought parts' estimated weights. **[UNCONFIRMED]** marks anything not yet measured, tested or quoted. Nothing here has
been built yet: these are design figures.

## Dome, the pendant

| | |
|---|---|
| Size | Cover 200 mm across, 100 mm deep at the rim; the hub and its cap add 26 mm above the crown. Canopy 150 × 50 mm. Standard drop 600 mm, cut to length (the rim 776 mm below the ceiling as supplied) |
| Weight | Cover about 0.9 kg (its acrylic 0.8, the aluminium collar 0.12). The fixture below the ceiling about 0.7 kg (the aluminium hub 0.58). Hanging total about 1.6 kg; canopy with its driver about 0.3 kg **[UNCONFIRMED: computed]** |
| Light | 2700 K, CRI 90 COB (Bridgelux Vero SE 10), about 1,100 lm at the LED **[UNCONFIRMED: the datasheet's figure at 700 mA; the light out of the tinted cover is lower and differs by tint, unmeasured]** |
| Cut-off | The COB sits 22 mm up a 46 mm bore in the hub: no direct view of the source above about 46° from the vertical (geometry, not measured) |
| Dimming | Phase-cut (TRIAC), by a Mean Well PCD-16-700B driver in the canopy **[UNCONFIRMED: leading-edge dimmers to be confirmed]** |
| Mains | 120 V, to be listed as a fixture to UL 1598 (or ETL) **[NOT YET LISTED]**. The driver is UL 8750 Class 2 |
| Covers | Swap by hand, no tools: a quarter-turn bayonet with a detent. The cover holds no electrical parts |
| Materials | The cover: three-layer cast acrylic (a tinted shell 9 mm, a frosted liner 2.5 mm, a tinted skin 3 mm), polished, bonded to a black anodised aluminium collar. The hub (the COB's heat sink) and its pins black anodised aluminium, satin; the canopy and the cap over the cord grip black cast acrylic, polished. Black textile cord. No brass |
| Tints | Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke, each cast so it matches its speaker's colour when lit (README, round 32f) |
| Sold separately | Covers, in each tint |

## Orb, the table lamp

| | |
|---|---|
| Size | Ball 160 mm across; base 120 mm across; 180 mm tall |
| Weight | About 2.0 kg: the ball 1.1, the base 0.9 (its steel ballast 0.66). With the cartridge about 2.2 kg **[UNCONFIRMED: computed]** |
| Light | Warm-dim, 2200 to 2700 K as it dims, CRI 90+, about 200 lm at full (2.5 W) **[UNCONFIRMED: the LED module is to be chosen; output out of the ball unmeasured]** |
| Control | Touch the black ring: tap to switch, hold to dim |
| Power | Plug-in as standard: USB-C PD, a slim black fabric cable (2 m) out of a notch underneath at the back, so the base sits flat, and a 20 W USB-C adapter in the box |
| Cordless (option) | A battery cartridge slides into a bay under the base from the back, held by magnets and a detent, flush with the drum: about 22 Wh (one Li-ion pouch cell, 6,000 mAh at 3.7 V), about 10 hours at the bar setting (2 W) **[UNCONFIRMED: computed from capacity; the cell is to be chosen]**. It charges in the lamp over the USB-C, or on the staff tray through two gold pads underneath, about 3 hours **[UNCONFIRMED: estimated]**. Without it, a blanking cap closes the bay |
| Protection | IP44 by design: the base sealed by O-rings, the USB-C receptacle sealed, with the ball on or off **[UNTESTED]** |
| Safety | The plug-in Orb is a low-voltage lamp on a listed adapter (UL 62368-1). The cartridge to IEC 62133-2 and UN38.3 for shipping **[NOT YET CERTIFIED]** |
| Materials | The ball: three-layer cast acrylic (a tinted shell 9 mm, a frosted liner 2.5 mm, a tinted skin 3 mm), polished, its port lined in black anodised aluminium. The base black cast acrylic, polished, over an aluminium chassis and a steel ballast; the touch ring black anodised aluminium, satin. A silicone seat and foot ring |
| Tints | Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke, each cast so it matches its speaker's colour when lit (README, round 32f) |
| Sold separately | Balls, in each tint (the ball lifts off: it holds no electrical parts). The battery cartridge. The staff charging tray (for six) **[a product of its own, not yet designed]** |

## Prices

The owner's to set. The suggestions (README, rounds 32d and 32f):
- Dome $795 to $895 with one cover; covers $295 to $345.
- Orb (plug-in) $545 to $645; balls $245 to $295; the battery cartridge $95 to $125.
