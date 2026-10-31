# First articles and bench tests (round 43, 2026-10-31)

What to make first, and the tests each must pass before a run is ordered. **The pass marks are ours:**
- where a standard sets a limit, it is named, and our mark sits inside it;
- where none does, the mark is what a good product in the class achieves.

**Equipment that any of these need (about $600 in all, an estimate):**
- a Type K thermocouple logger with 8 channels;
- a lux meter;
- a flicker meter (or a photodiode and a USB scope);
- a USB-C power meter with PD;
- a bench supply;
- a 1 kHz / 3150 Hz test LP and a strobe disc;
- a laptop audio interface with REW (free).

## Hemisphere

**First articles:**
- one complete pendant with a **Smoke** shade, the darkest, which absorbs the most heat;
- one spare **Fog** shade, the palest;
- three COBs from the production bin;
- the ERP ESS010W-0180-42 and the EPtronics LD6W120-36-C0170-TL, so the alternate can be swapped in the same hour.

| Test | How | Pass |
|---|---|---|
| **Driver headroom** | Each of the three COBs on the ERP driver at 120 V. Measure the COB voltage and current at Tc 25 °C (cold start), then at Tc 85 °C (the hub on a hot plate, or the fixture enclosed until Tc reads 85). Repeat at 108 V and 132 V mains. | Current 171 to 189 mA (±5 %) at every point, and COB voltage at least **24.5 V** at 85 °C, so the driver keeps a margin over its 24 V floor. If any COB fails, use the EPtronics (22 to 36 V) or a higher-voltage COB bin. |
| **Closed shade at full output** | Thermocouples as in round 35's plan: the COB's Tc point, the hub, the crown and cap, the collar, the clamp ring, the acrylic at the crown at 5 and 20 mm from the clamp ring (inside and outside), and the rim. Then: hang at the standard drop in a closed room or chamber at 25 °C, then at 35 °C; log every minute until it changes less than 1 K in 30 minutes, and at least 4 h; repeat in a mock 100 mm ceiling recess. | Acrylic at most **50 °C** (our margin; UL 1598's limit for acrylic is 65 °C). Tc at most 85 °C. Crown and cap at most 60 °C (touchable). Round 41's estimate: acrylic 41 °C, Tc 50 °C. |
| **Dimming** | On three common dimmers: Lutron Diva CL, Leviton Decora SureSlide, and a Lutron Caséta. Dim from 100 % to the lowest setting. Measure flicker percent and frequency at 100 %, 50 % and 10 %, and noise at 1 m. | No visible flicker, no dropout, no pop-on. Flicker under **30 %** below 200 Hz at 10 %, and noise under **24 dBA**: both the JA8 marks. |
| **Light on the table** | Rim 700 mm over a table; lux meter at the centre and at the ends of a 90 cm span. | At least 450 lux at the centre (round 42 computes about 500). |
| **The cord and the catch** | A 35 lb pull for 1 min at the cap and at the canopy (UL 1598 5.15.2). Then 200 shade swaps on the bayonet; then a knock test (tap the rim with a finger, 20 times). | The cord doesn't move at either grip. The detent holds, with no wear on the pins or slots, and no shade drops. |

## Core

**First articles:**
- two complete lamps (Ember and Smoke);
- twelve PSL-FP-IFR18650EC cells;
- two Li-ion 18650s (Samsung 35E kind) for the misuse test;
- the 20 W USB-C adapter from the box.

| Test | How | Pass |
|---|---|---|
| **Runtime** | Charge full, then to the default 90 % limit; run at full brightness (2.5 W, measured at the board) in a 25 °C room until cut-off. Repeat at the bar setting (2 W). | **At least 4.5 h** at full brightness at 90 % (expect 4.7) and at least 5.0 h from full (expect 5.2). At least 5.5 h at the bar setting at 90 % (expect 5.8). |
| **Charge time and temperature** | From cut-off, charge on the 20 W adapter with the lamp on at full brightness (the worst case), in a 25 °C room and then a 35 °C room. Thermocouples on each cell's skin, the board and the base's underside. | 90 % in at most 2.5 h with the lamp off. Cell skin at most **45 °C** (the cell's charge limit) in the 35 °C room; at most 40 °C in the 25 °C room. Base underside at most 45 °C. |
| **Charge cut-outs** | Warm the cells' NTC above 45 °C, and cool a cell below 0 °C. | Charging stops in both cases and resumes when back in range. |
| **The wrong cell** (per-cell switching; `certification.md`) | Fit one Li-ion cell at 4.1 V beside two LiFePO4 at 3.2 V. Then one cell reversed. Then a set mixed between 2.8 and 3.4 V. | The lamp refuses the set (a blink code), and no current over 0.1 A flows between cells. No cell rises above 3.65 V. No heat or damage. |
| **Splash (IP44)** | IEC 60529 IPX4: oscillating tube, 10 min, ball on; then ball off. | No water past the O-rings at the window, the chassis or the hatch. It works after drying. |
| **Stability and touch** | An 8° incline in every direction (UL 153's portable stability). The touch ring with a dry hand, a damp hand and a glass set on the ring. | Doesn't tip; computed tip angle is 43°. Taps register every time; the glass doesn't switch it. |

## Mantle

**First articles:**
- one complete player in Ember;
- the turned bearing set (spindle, two bushes, carbide ball, thrust plate);
- two pulleys (33 and 45 diameters, calculated for the 310 platter rim);
- the Rega 24 V motor kit and Neo PSU (`mantle-drive.md`);
- the RB330 arm and a 2M Blue.

| Test | How | Pass |
|---|---|---|
| **Speed** | Test LP at 3150 Hz into REW, or a speed app with a strobe disc, 10 min warm. Trim with the Neo. | Mean speed within **±0.1 %** of 33.33 and 45 after trim. Drift at most 0.1 % over 30 min. |
| **Wow and flutter** | The same 3150 Hz band, DIN/IEC weighted, read in REW or a W&F meter. | At most **0.10 %** weighted (a good belt drive is 0.05 to 0.10). |
| **Rumble** | Silent groove of a test LP, through the phono stage, DIN-B weighted, relative to 1 kHz at 5 cm/s. | At least **65 dB** below (−65 dB or better; Rega's P3 class is about −70). |
| **Hum and noise** | The arm resting in the silent groove, motor running, the base light on and off, A-weighted. | At least 70 dB below 5 cm/s. The base light adds less than 1 dB and no tone in the audio band (its PWM is at 25 kHz). |
| **Isolation and resonance** | Tap the plinth and record with the arm on a still record. Arm and cartridge resonance from the test LP's sweep. | The plinth's float around 15 to 20 Hz, damped within 0.5 s. Arm resonance 8 to 12 Hz. |
| **The bearing** | Spin-down from 33.33 with the belt off; run for 100 h. | Spin-down at least 3 min. No noise or wear in the oil after 100 h. |
| **The lid and the light** | The lid at any angle from 15° to 80°, 50 cycles. Base light uniformity by eye and a photo at three exposures. | The lid holds every angle. No hot spots at the slot's ends, and the printed band hides the strip from above. |

## Order of work

**Weeks 1 to 2:**
- Core's runtime and charge tests, on bought cells and a bench board;
- Hemisphere's driver headroom, on bought COBs and drivers.

Neither waits for formed acrylic.

**Weeks 3 to 6:** the formed parts arrive (RFQs 01 and 02). Then:
- the closed-shade temperature test;
- the IP44 test;
- the swap test.

**Mantle:** the bearing and pulleys are the long pole. Turn them first, and test speed and rumble on a plain MDF
plinth while the acrylic is made.

## The dates (added 2026-10-31)

**The targets, from the research:**
- the San Francisco debut night, **Tuesday 19 January 2027**, just before FOG Design+Art (21 to 24 January);
- prototypes photographed by mid-February 2027;
- Milan Design Week, 12 to 18 April;
- High End Vienna, 6 to 9 May.

**Assumptions:** today is 31 October 2026, and the owner sends the RFQs in the week of 2 November. Most shops close
from about 21 December to 3 January, which takes two of the eleven weeks to 19 January. The lamps are to be hung and run for an evening about 14 January
(`debut-night-lighting.md`), so the build has about ten and a half weeks, eight and a half of them working. The lead times
below are typical for small shops, not quotes: the RFQs ask for the real ones.

| Week of | Hemisphere | Core | Mantle |
|---|---|---|---|
| 2 Nov | RFQs 01, 03, 04 sent. Order 3 COBs, both drivers, the reflector's spinner quote. Ask for tinted sheet chips (stock tints) | RFQs 02, 03, 04 sent. Order 12 cells and a bench LiFePO4 board (LTC4162 evaluation kit). Start the board's per-cell switching design | RFQ 05 sent; bearing and pulley added to RFQ 04. Order the Rega motor kit, Neo PSU, RB330 and 2M Blue (all in stock) |
| 9 Nov | **Driver bench test** (headroom at Tc 85 °C), and the go or no-go on the ERP driver | **Runtime and charge bench tests** on the evaluation kit | Bench-run the Rega motor on its board. **Bearing and pulley ordered** |
| 16 Nov | Quotes back; **moulds ordered** (shell, liner, skin: about 4 weeks) | Quotes back; **ball mould ordered** (about 4 weeks). Board layout | Quotes back; plinth, base and lid ordered from flat sheet |
| 23 Nov | Tinted sheet ordered: a **stock tint** nearest each target, unless the mill's custom tint lands in time | Board sent to fab and assembly (about 3 weeks) | |
| 7 Dec | Turned and anodised aluminium in | Base, ring and hatch in | **Bearing and pulley in**; speed and rumble on an MDF test plinth |
| 14 Dec | **Moulds in**; first forming trials before the shutdown, if the former can | **Ball mould in**; first halves formed | Acrylic parts in; assembly; **speed, wow and flutter, rumble** |
| 21 Dec – 3 Jan | shutdown | shutdown | shutdown (bench tests at home continue) |
| 4 Jan | Shades formed, bonded, polished | Balls joined and polished; **boards in**, firmware | A working player |
| 11 Jan | **Closed-shade temperature test** (4 h); cord and catch | Runtime and charge on the real board; wrong-cell test; IP44 | Lid and light; the 100 h bearing run starts |
| About 14 Jan | Hung and run for an evening (in the room, or the workshop) | An evening's runtime | Played for an evening |
| **19 Jan** | **Possible** (about even odds): only if the moulds are in before the shutdown | **Possible as a working prototype**: the ball's joint finish may not be final | **Likely**: no moulds, bought drive |
| mid-Feb | **Photographed** | **Photographed** | **Photographed** |

**The float (recounted for 19 January, round 43):**
- **Hemisphere: none before the test evening.** The closed-shade test runs in the week of 11 January, and the test
  evening is 14 January. A late mould pushes it past the test evening, but not past the debut: there are five days
  from 14 to 19 January.
- **Core: about a week.** The ball and board are in by 4 January.
- **Mantle: about three weeks.** It plays in the week of 4 January.

**The critical path, in order of risk:**
1. **The moulds:** the three shade moulds and the ball mould. Ordered by 16 November they land about 14 December,
   and every week later moves Hemisphere and Core past the shutdown. If the former can't make the dates, ask about
   free-blowing the shell (RFQ 01, question 10).
2. **The tinted sheet.** A mill's custom tint is weeks and a pallet. **For January, use the stock colours nearest each
   tint** (the stock-colour study), and save the matched casts for Milan.
3. **Mantle's bearing and pulley.** Nothing off the shelf replaces them (`mantle-drive.md`). Ordered by 9 November,
   they are in by 7 December.
4. **The driver bench test** (week of 9 November). If the ERP driver fails headroom, the EPtronics is on the bench the
   same week, so it costs days, not weeks.
5. **Core's board.** Per-cell switching is new design work. Use the evaluation kit and a hand-wired cell switch for
   the debut night if the board slips.

**After the debut night:**
- **mid-February:** photographs of all three;
- **March:** the tints cast to match, if the owner orders them in January;
- **12 to 18 April:** Milan with matched tints;
- **6 to 9 May:** High End Vienna with Mantle.

## Cash out by week for the 19 January debut (added 2026-10-31)

This covers one working Hemisphere, one Core and one Mantle in **stock Ember** (2423), from 2 November to 14 January (the test evening).

**Sources:**
- the BOMs: Hemisphere $4,572, Core $2,027, Mantle (turntable-float) $3,815;
- R1's sheet prices;
- `mantle-drive.md`'s retail prices.

**[E]** marks an estimate. Quotes replace every made-part figure. "Returnable" means unopened stock from a distributor
or retailer, usually within 30 days, sometimes with a restocking fee. Anything cut, turned or tooled to our drawing is
not returnable.

### Paid early: the critical path (by 16 November)

| Week of | Item | Supplier type | Amount | If we stop |
|---|---|---|---|---|
| 2 Nov | Colour chips, and a 1/2" off-cut each of 2423, 2064, 2074 | sheet retailers (Canal, eStreet, AC) | $150 [E] | spent |
| 2 Nov | Hemisphere bench: 3 Vero SE 10 COBs, 2 ERP ESS010W-0180-42, 1 EPtronics LD6W, 3 wall dimmers | electronics distributors | $170 [E] | returnable unopened; most will be opened for the test |
| 2 Nov | Core bench: 12 PSL-FP-IFR18650EC cells, an LTC4162 evaluation kit, 2 Li-ion cells for the misuse test | electronics distributors | $200 [E] | mostly returnable unopened |
| 2 Nov | Bench equipment: thermocouple logger, lux and flicker meter, USB-C power meter, test LP | instrument retailers | $600 [E] | returnable 30 days; keeps its value |
| 2 Nov | **Mantle's bought drive:** Rega 24 V motor kit $265, Neo PSU $445, RB330 $675, 2M Blue $220, Phono Box S2 $269 | hi-fi retailers (Audio Advisor, Upscale) | **$1,874** | returnable unopened, 30 days (check each store) |
| 9 Nov | **Mantle's bearing and pulley,** turned: spindle, housing, bushes, ball, thrust plate, platter hub, pulley | CNC turning shop (RFQ 04) | **$374** BOM, $400–600 a one-off [E] | not returnable once cut |
| 16 Nov | **The moulds:** Hemisphere's shell, liner and skin ($3,900), Core's ball ($1,500) | acrylic former (RFQ 01, 02) | **$5,400** | not refundable once cut; often a 50 % deposit at order, the rest on first articles |
| | **Subtotal by 16 November** | | **about $8,800** [E] | about $2,800 of it returnable; the moulds and the turned parts are not |

### Waits for quotes (23 November to 15 December)

| Week of | Item | Supplier type | Amount | If we stop |
|---|---|---|---|---|
| 23 Nov | Stock Ember sheet: 3/8" and 1/2" 48×96, 1/8" and 1/4" | AC Plastics (TruCast) | $1,800 [E] + LTL freight about $200 [E] | full sheets returnable with a fee before cutting |
| 23 Nov | Core's board: fab and assembly, 5 boards | PCB assembler | $400 [E] | not returnable |
| 7 Dec | Hemisphere's machined parts and the rest of its bought parts (collar, clamp, hub, crown, cap, PEEK ring, rim, canopy, cord, driver, reflector) | CNC and anodise shop (RFQ 04); distributors | $672 (BOM, less moulds) | made parts not returnable |
| 7 Dec | Core's made and bought parts (base, ring, chassis, ballast, hatch, window, cable, adapter, seals) | acrylic and CNC shops (RFQ 03, 04); distributors | $527 (BOM, less the mould) | made parts not returnable |
| 7 Dec | Mantle's acrylic and remaining parts: plinth (laminated), base, lid, posts, platter, pod rings, belt, feet, hinges, fixings | acrylic fabricator (RFQ 05); retailers | $567 made + $600 bought (BOM) | made parts not returnable |
| | **Subtotal, 23 November to 15 December** | | **about $4,800** [E] | |
| | **Subtotal by 15 December** | | **about $13,600** [E] | |

### After 15 December

| Item | Amount |
|---|---|
| Finishing: polishing, anodise re-runs, bonding, the forming of the shades and ball on the moulds | in the made-part figures above, if quoted so; else about $500 [E] |
| Shipping and couriers | about $300 [E] |
| Contingency, 15 % of the made parts and moulds | about $1,100 [E] |
| **Total to 14 January** | **about $15,500** [E] |

### Option, not in the total: the debut night's lighting

Six more Hemispheres and ten more Cores (`debut-night-lighting.md`), on the moulds already paid for: 6 × $672 +
10 × $527 + $80 spare cells, so **about $9,400** [E], paid in December.

**Notes:**
- The total uses Mantle's 2M Blue; the 2M Black for the show unit adds $530.
- In Smoke, the sheet is about $600 less.
