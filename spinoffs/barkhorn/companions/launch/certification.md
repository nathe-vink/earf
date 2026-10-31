# Certification: the design side (round 43, 2026-10-31)

What to design in so US listing is simple and cheap, for Hemisphere, Core and Mantle. Labs, prices, FCC, Prop 65 and
California's battery rules are another researcher's, so they are not here.

These are from public sources only:
- UL 1598's 2018 edition, published at law.resource.org; the current edition is the 5th, 2021, so clause numbers may
  have moved;
- UL's and Intertek's summaries of UL 153 and UL 62368-1, which were not read in full;
- 49 CFR 173.185 and a PHMSA interpretation;
- Energy Code Ace and CEC pages on JA8.

**A lab's quote and pre-test review replace all of it.** Nothing here is a lab's opinion.

## Hemisphere

**The cheapest first listing is a plug-in swag under UL 153, fed by a listed Class 2 / LPS plug-in supply.** Mains
never enters the lamp: the lamp is marked "For use with Class 2, __ V, __ W" (UL 153, clause 199.1 in the 2027
revision), and the supply carries its own listing. UL 2108 doesn't apply: it covers permanently connected low-voltage
systems.

**The hardwired version is the later trade and bar version: UL 1598, with a listed UL 8750 / UL 1310 Class 2 driver in
the canopy.** It costs more:
- the mains canopy (field leads, junction-box mounting, grounding, the driver's enclosure);
- for California homes, **JA8** certification of the luminaire. JA8 covers integral-LED luminaires and is enforced
  at installation. A plug-in portable is outside Title 24 Part 6, and Title 20's portable-luminaire rules were voted
  for repeal in 2023.

**What a Class 2 secondary buys under UL 1598 (2018):**

| Rule | Clause | What it means for Hemisphere |
|---|---|---|
| A Class 2 circuit isn't a "risk of fire" | definition | |
| No enclosure needed where nothing is at a shock or fire voltage | 5.3.3 | The shade and the low-voltage parts need not be an enclosure |
| No V-0 rating for a lens or diffuser that isn't an enclosure | 5.7.1.3 | The acrylic shade needs no flame rating |
| No 5VA rating for a polymeric enclosure | 5.7.1.2 | |
| HB at least for plastic that suspends, separates or grounds | 5.7.1.6 to 5.7.1.8 | **The PEEK ring carries the shade:** check it's HB or better (PEEK is V-0) |
| **Acrylic at most 65 °C** | Table 15.1.2, item 20 | Round 41's estimate is 41 °C by the collar in a 35 °C room, so the margin is wide |
| Cord strain relief: 35 lb (15.9 kg) | 5.15.2 | |

**Design changes to make:**
1. **Hang the shade from a support, not from the cord.** Under UL 153, an SPT-2 cord may carry at most 2.5 lb
   (1.1 kg), and Hemisphere hangs at about 1.6 kg (3.5 lb). The options:
   - a fine black steel suspension cable beside the cord, gripped at the cap and the canopy;
   - or a cord with a steel strain member.

   Then the cord carries only current. For the UL 1598 version, a cord with a plug must be at least SJT (11.6.5), so
   the plug-in version stays under UL 153.
2. **Dim on the low-voltage side.** In the plug-in version, an in-line low-voltage dimmer (PWM above 20 kHz, or
   constant-current analog) means no listed mains dimmer and no phase-cut compatibility testing. The ERP driver's
   phase dimming stays for the hardwired version.
3. **Keep the low-voltage side at or under 30 V and Class 2.** The COB runs about 24.6 V at 180 mA.
4. **Grip the cord without clamps.** UL 153 bans clamp-type strain reliefs on SPT-2, SVT and SVTO cords (17.3,
   2027). Use a moulded or knotted grip at the cap and the canopy, as drawn (a listed grip).
5. **Plug-in supply:** a listed Class 2 / LPS constant-voltage adapter (24 to 30 V), plus a small constant-current
   board in the canopy. Or a listed Class 2 constant-current plug-in if one is found at 180 mA.

## Core

**Path: UL 153, with Supplement SA (2022) for battery-powered portable luminaires**, a tabletop lamp included.
- The lithium cells must be UL 1642 or UL 62133-2. Power Sonic's PSL-FP-IFR18650EC lists UL 1642.
- A UL 2054 pack listing shouldn't be needed for listed cells in holders. Confirm this with the lab.
- UL 8750 covers the LED parts. UL 62368-1 is not the route.
- **Trap:** a hand-held light or lantern goes to UL 1576 instead. Core is a table lamp: keep it described as one.

**The trap that matters most is the user-replaceable 18650 cells.** A user can fit a common 4.2 V Li-ion cell (NMC)
or an unprotected cell, and the lab will fault-test exactly that. The CPSC warned about loose 18650s in 2021.

**Design changes to make:**
1. **Monitor and switch each cell.** Core's three cells are in parallel (1S3P). A Li-ion cell at 4.1 V fitted beside two
   LiFePO4 cells at 3.2 V would push them past their 3.65 V limit. The board needs:
   - a FET switch per cell;
   - a check at power-up (each cell between 2.5 and 3.65 V, all within 0.1 V of each other);
   - refusal of a set that fails, with the light blinking.

   Add **reverse-polarity protection** and a **current limit per cell** (a PTC or the per-cell FET).
2. **Charge at most 3.6 V per cell.** The LTC4162-F's LiFePO4 profile is safe for a Li-ion cell too.
3. **No coin cells anywhere,** including any remote. UL 4200A applies (47.4.1, 2027).
4. **Mark the hatch:** "LiFePO4 18650 (3.2 V) only", "Do not mix old and new", and the polarity.
5. **Keep it SELV:** USB-C 5 V, a limited power source, no mains inside, a listed USB-C adapter in the box.

**Shipping (UN 38.3).** The cells' maker supplies the UN 38.3 test summary (49 CFR 173.185(a)), and equipment that
contains tested cells is not retested. But a 2019 PHMSA letter treats cells that are electrically connected with a
circuit board as a "battery", which then needs its own UN 38.3 test.

**Recommendation: ship the three cells in the box beside the lamp** (UN3481, packed with equipment, still the small-
battery exception), not installed. This also shows the buyer the hatch.

## Mantle

**Path: UL 62368-1 (audio/video), with only external listed supplies and nothing inside above ES1 / PS1.**

| Supply | What it feeds | Draw | Class |
|---|---|---|---|
| Rega Neo PSU | the motor | 24 V AC, 350 mA, about 7–8 W | ES1 / PS1 |
| Mean Well GST25A24 (25 W) | LED strip and phono stage | | **PS2** |

PS1 is at most 15 W, and it needs no fire safeguard. The 25 W adapter makes its circuit PS2, which brings a
fire-enclosure and material-flammability evaluation.

**Design changes to make:**
1. **Swap the 25 W LED adapter for one listed LPS adapter of 15 W or less** at 24 V. The strip draws 6.8 W and the phono
   stage about 3 W through the LT3045, so one 12 to 15 W adapter feeds both. That keeps every circuit PS1 and cuts
   the inputs to two.
   - **Check the label:** Mean Well's GST25A24 datasheet claims UL 62368-1 but not LPS or Class 2.
2. **Ask Rega for the Neo PSU's listing certificate.** None was found publicly. If it ships in our box, the lab will
   want it. The fallback is Origin Live's DC motor kit with a listed adapter (`mantle-drive.md`).
3. **The Pro-Ject Phono Box S2 is a finished product, not a recognised component.** The 4th edition of 62368-1 no
   longer accepts legacy-certified parts automatically. At ES1/PS1 the tests are mostly heating and materials, which
   are cheap. Its own 18 V adapter isn't used: the LT3045 feeds it.
4. **Earth and metal:** keep accessible metal (bearing, arm, rear box) at ES1. The star earth at the rear box stays.
5. **Give the lab:** a full parts list with ratings, every supply's certificate or CB report, schematics, UL 94 data
   for the acrylic and the base, the markings and the manual.

**FCC:** Mantle's only clocked circuit is the LED dimmer's 25 kHz PWM. Whether it is a "digital device" (47 CFR
15.3(k)) is for the FCC researcher.

## What to do now

| Product | Change | Cost |
|---|---|---|
| Hemisphere | a suspension cable beside the cord | about $5 a lamp |
| Hemisphere | the plug-in swag version first, under UL 153 | |
| Core | per-cell switching and monitoring on the board, plus reverse polarity | board change |
| Core | cells packed beside the lamp | packaging only |
| Mantle | one 15 W LPS adapter for the light and the phono stage, in place of the 25 W | about the same price |

Cost and timeline: the other researcher is pricing labs. Public figures found here are forum anecdotes ($5k to $20k
for a luminaire), so not quoted.
