# Core: recharging with no cord in sight (2026-10-31)

**A proposal for the owner to sign.** It answers the owner's ruling of 2026-10-31 (saved at `r46-owner-notes`
a883091275401471b7fc329927a263c6313e420a): *"the orb definitely looked better without the cord, so lets redo the
design of that to allow for recharging"*.

So **Core stays cordless**, and the v1 plug-in note (`launch/core-v1-plugin.md`) is no longer the recommendation.

Nothing in Core's CAD (`orb_table.py`, `crystal.py`) changes until the owner picks a route. The drawing and the
pictures below are proposals.

Marks used below:
- **[E]** an estimate;
- **[Q]** a public list price, not a quote;
- **[check]** to confirm with the maker.

## In short

**Recommended: (b), the contact dock.** It is a 150 × 8 mm disc of polished black cast acrylic that Core sits on.
- **How it charges:** two stainless rings, set flush in the dock's top, meet two spring pins in Core's base. The rings
  are concentric, so the lamp charges at any rotation and needs no lining up.
- **The cord:** one USB-C cable runs from the dock's back to the adapter, behind the furniture. When Core is lifted off,
  nothing hangs from it.
- **The port:** the USB-C port under the base stays, for travel and service.

**Why the dock:**
- It charges as fast as the cable: about 2.7 h to 90 % at 1.5 A (the review's figure, 2026-11-01).
- It adds no radio, so no new certification beyond the luminaire's own.
- It adds about $30 to $45 [E] to the bill of materials.
- It costs about a week of design [E], not a month.
- Qi (c) would mean an acrylic hatch in place of the aluminum one, moving the steel ballast, a radio approval, and
  slower and hotter charging (below).

**Cutting the engineering cost:**
- The custom LiFePO4 board was estimated at $16k to $40k (`launch/boards.md`).
- No listed, off-the-shelf **LiFePO4, three-cell** lamp module turned up in public search.
- Two ways down:
  1. **v1 on a cordless-lamp OEM's board and a listed Li-ion pack.** About $2k to $5k [E] of OEM changes plus a week
     of integration. It gives up the "standard LiFePO4 cells you can buy anywhere" story. That is a spec change for the
     owner.
  2. **Keep LiFePO4 and the custom board, but buy the design as a fixed-price package.** About $12k to $20k [E].

See §2.

## 1. The routes compared

All four routes keep Core's electronics as they are: one USB-C input into the charger (at 9 V by USB PD since the
review of 2026-11-01, §5), the cells, and the warm-dim LED. They differ only in how that input reaches the base. Core's base is 120 × 30. From below it has:
- a black anodized **aluminum** hatch over the three cells (Ø112);
- a foot ring;
- the USB-C receptacle on a small board in the corner at 170°.

Charge times assume 14.4 Wh of cells charged to the default 90 % limit, and the charger's input efficiency about 90 %.

| | (a) Port only | (b) **Contact dock** | (c) Qi dock | (d) Magnetic USB-C tip |
|---|---|---|---|---|
| What the user does | Plugs a braided USB-C cable into the base's port, under the edge | Sets Core on the dock | Sets Core on the dock | Leaves a magnetic tip in the port; a magnetic cable snaps on |
| Cord seen in use | None, once unplugged | None: the dock's cable leaves from its back | The same as (b) | None, once unplugged; the tip shows as a dot |
| Cord seen while charging | A cable from under the base | The dock's cable, behind it | The same | A cable from under the base |
| Charge time (to 90 %) | about 2.7 h (USB PD 9 V, the charger at 1.5 A: 4.05 Ah to 90 % of 4.5 Ah) | about 2.7 h: the same 9 V | about 4 to 5 h: 5 W BPP, about 3.3 W to the cells | about 2.7 h |
| Runtime off the charger | about 7.8 h at full (1.5 W, §5; 4.7 h at the old 2.5 W), 9.7 h at the bar setting | the same | the same | the same |
| Heat while charging | about 0.5 W in the charger | about 0.5 W; the contacts, about 0.01 W | about 1.5 to 2 W, split between the dock and the base. It needs a ferrite sheet in the base, or the steel ballast and the aluminum chassis heat as eddy loads | about 0.5 W |
| What changes in Core | nothing | two spring pins on the USB-C board, through two holes in the hatch; an ideal diode on each input | the hatch becomes acrylic; a receiver coil and ferrite at the bottom; the ballast moves off the coil; a receiver board | nothing |
| Added parts cost [E] | a 1.2 m braided C-to-C cable, about $8 | dock about $30 to $45 (below); pins about $2 to $4 | transmitter about $8 to $25, receiver about $5 to $15, ferrite, an acrylic hatch, a dock: about $45 to $70 | tip and cable about $8 to $15 |
| Engineering [E] | none | about 5 days: the dock's turned body, its small board and the pins | about 3 to 5 weeks, mostly the receiver's placement and the hatch | none |
| Certification added | none | none beyond the system's DOE charger test, which includes the dock | the transmitter's FCC approval (Part 18 or 15C, [check]); the Qi logo needs WPC certification of the dock; in the EU, RED [check] | none of ours, but third-party magnetic USB-C tips are not USB-IF compliant, and a loose magnetic tip can short a 5 V line on metal. **Rejected** |
| How it looks | the lamp alone; charging looks like a phone | **the lamp on a black plinth, as if it were part of it** | the same as (b) | the lamp alone |

### Why not Qi

The case against Qi is physics before cost:
- Qi works only with no metal between or near the coils.
- Core's bottom is an aluminum hatch, with a steel ballast and an aluminum chassis above it.
- The hatch would have to become acrylic, and the ballast would have to move clear of the coil. That reopens the
  base that round 41 settled.
- Base Power Profile Qi (5 W) charges about half as fast as the cable and turns about 1.5 W more into heat in the base.
  The cells' charge limit is 45 °C.
- Qi's one advantage over the contact dock is no exposed contacts. The dock handles that differently: its rings stay
  dead until a lamp is on them (below).

The parts exist if the owner wants Qi anyway:
- **Prototypes:** Adafruit's Universal Qi transmitter (product 2162) is $26.95 [Q]. Its matching receiver (1901) is
  $14.95 [Q], but it gives only 5 V 500 mA, so about 7 h to charge.
- **Production:** a module its maker says is Qi-certified, such as Pulse/Yageo WM5V or QST QPT-0005 (both "WPC 1.2.x,
  5 W", prices on request; [check] each against WPC's public database).
- **Controllers, if we laid out our own:** NXP's MWCT1101 is €3.60 [Q], STMicro's at about $5.36 [Q].

### The contact dock, as drawn

Drawing: `renders/2026-10-31/barkhorn/lamps-cordless/core-dock-drawing.png`, generated by `core_dock_drawing.py`.

- **The body:** Ø150 × 8, polished black cast acrylic, turned. It has a 1.5 mm pocket Ø122 that the base's foot ring
  sits in, so it locates and won't slide. Its edge is radiused 2.
- **The contacts (revised 2026-11-01, §5):** a 304 stainless disc Ø12 on the axis (+) and a 304 stainless ring at
  r 20, 4 wide (−). Both stand on a turned island 2.0 mm proud of the pocket's floor, their tops lapped. The first
  draft's rings at r 30 and r 44 put the − pin through the USB-C receptacle (r 43 to 50.5 at 170°); the axis and r 20
  are inside the main board's 48 mm ring, clear of it and of the cells.
- **The base's pins:** two gold-plated, low-force spring pins, 1.5 mm of travel, about 0.8 N each at 1.0 mm [E]: one
  on the axis, one at r 20, both on the main board, through two Ø3 holes in the hatch. Their tips sit 0.5 above the
  foot ring's face, so a table never touches them; on the dock the island lifts the contacts 2.0, so each pin works at
  1.5 − 0.5 = 1.0 mm of its travel. One pin on the axis and 1.6 N in all against the lamp's 13 N put no useful tilt
  on it. Off the dock the pins are dead: each input (the USB-C port and the pins) feeds the charger through its own
  ideal diode, so neither can back-feed the other.
- **The dock's board:** a USB PD sink that asks the adapter for 9 V (a standalone PD sink controller, STUSB4500 or
  CH224K class [check]), under its back edge. Its cable exits through a notch in the dock's back. The board has:
  - a resettable fuse;
  - a load switch that powers the rings only when it sees the lamp. The lamp shows a 47 kΩ sense resistor across its
    pins; a coin, a key or a spill reads as a short or an open and wakes nothing.
- **Weight and grip:** the lamp weighs about 1.3 kg [E], about 0.8 N per pin at its working stroke. Silicone dots under
  the dock stop it sliding.
- **The cable:** the same 1.2 m braided C-to-C as (a), and the same listed 20 W adapter. The adapter's listing is its
  maker's.
- **Cost, one-off** [E]:
  - turned body about $20 to $30;
  - rings about $6 to $10;
  - board and parts about $5;
  - silicone dots about $1.
- **At 500** [E]: about $18 to $25.

Price anchors [Q]:
- Mill-Max's magnetic 2-pin pogo header (878-22-002-10-011101) is listed at about ₹915, about $11, for one.
- A generic 2-pin magnetic pogo pair (12 V, 2 A) is about SEK 18.50.

The dock uses plain spring pins and rings instead, because the lamp's weight holds them, with no magnet to pick up
steel dust.

## 2. Cutting the engineering cost

The owner asked for an off-the-shelf, already certified driver and battery so EARF designs an enclosure, not a board.
What public search found:

| Need | Found | Status |
|---|---|---|
| A listed LiFePO4 three-cell lamp module (charger, protection, warm-dim driver, touch) | **nothing** | none in public listings. LiFePO4 is rare in cordless lamps; nearly all use one Li-ion cell or pack |
| A cordless-lamp board (USB-C charging, touch, stepless dimming, protection) | yes, from lamp OEMs: a 35 × 17 mm board for one 18650 or a 3.7 V cell, touch through up to 3 mm, about 500 mA charging (ifuturetech's listing); Ningbo Liangying Electronic Technology showed a USB-C, touch-dimmed 18650 lamp at Light + Building 2024; Inno Casa (Hong Kong) offers customized cordless lamps | cheap (about $2 to $5 a board [E]), but uncertified as a part. Its 500 mA charging would take about 11 h for Core: ask for 1.5 A |
| A listed battery pack | Tenergy sells protected 18650 Li-ion packs, for example the 31001 (1S2P, 5200 mAh, 19.24 Wh), $33.30 at BatteryJunction [Q]. Tenergy's LiFePO4 18650 (30085, 1450 mAh) is sold as a bare cell | ask Tenergy for the UL 2054 / IEC 62133-2 file numbers [check]; none appeared in the listings |
| A listed charger | the 20 W USB-C adapter (bought, listed by its maker) | as now |

### Option 1 (recommended for v1, if the owner accepts Li-ion): the OEM board and a listed pack

- **The electronics:** a lamp OEM adapts its cordless-lamp board to Core:
  - our 48 mm ring;
  - 1.5 A charging;
  - two-channel warm-dim at 1.5 W (§5);
  - the touch on the anodized ring;
  - inputs from both the dock's pins and the USB-C port.
- **The pack:** a listed 1S2P 18650 Li-ion pack (about 19 Wh) on a keyed connector behind the same hatch. It stays
  user-replaceable, as EU Regulation 2023/1542 requires.
- **Runtime:** about 11 h at full brightness (1.5 W) [E].
- **Engineering:** OEM NRE about $2k to $5k [E], plus about a week of our integration, against $16k to $40k.
- **What it gives up:**
  - LiFePO4's margin (it sees no thermal runaway at these sizes);
  - "standard cells you can buy anywhere";
  - the per-cell checks in `certification.md`.
- The pack's own certificates replace the per-cell ones.
- **This is a spec change** (PARTICULARS: "Three LiFePO4 18650 cells"). It is the owner's to sign.

### Option 2: keep LiFePO4, buy the board as a package

- The design as `boards.md` specifies it, bought from a design house at a fixed price, with the LTC4162-F evaluation
  kit as the bench reference.
- About $12k to $20k [E], quoted against the schematic list in `boards.md` §1.
- It keeps Core's battery story whole, and the dock works the same with either option.

## 3. What certification falls on EARF (either option, with the dock)

| Item | Whose | Note |
|---|---|---|
| The luminaire, UL 153 with Supplement SA (battery-operated portable luminaires) | **ours** | the dock, the cable and the adapter go in the test as the charging system |
| The cells or pack: UL 1642 / IEC 62133-2 (UL 2054 for a pack), and UN 38.3 | the maker's, if bought listed | Option 1: the pack's maker; now: the cells' (Power Sonic lists UL 1642) |
| The adapter's listing | its maker's | a listed 20 W USB-C adapter, DOE Level VI |
| The battery-charger system: DOE (10 CFR 430.32(z), Appendix Y) and California's MAEDbS | **ours** | the dock is part of the system under test (`certification.md`) |
| FCC Part 15B (unintentional radiator: the charger and the LED driver switch) | **ours** | a verification test, cheap |
| Qi only: FCC Part 18 or 15C for the transmitter, WPC certification for the logo, EU RED | ours, unless a pre-approved module is used unmodified [check] | the reason (c) costs more than its parts |

## 4. The pictures

- **In use, cordless:** the site's Core set re-rendered with the cable hidden, the same compositions as round 41's
  pass 4. Files: `renders/2026-10-31/barkhorn/lamps-cordless/` (`lamps_cordless.py`).
- **On its dock:** `core-dock-ember.png` in the same folder. It is the Ember hero's frame with the lamp on the 150 × 8
  dock, the dock's cable leaving straight back.
- **Applying the same charging to the two proposals (strata/):**
  - Contour Core's base (Ø120 × 30, an aluminum base) takes the same pins and the same dock. Its drawing is unchanged
    but for the two holes.
  - Core Sample's foot (Ø96) takes a Ø126 dock with the same center disc and r 20 ring.
  - Both docks are described in `strata/README.md`, not yet drawn in CAD.

## 5. The engineering review's fixes for Core (2026-11-01)

From the coordinator's reviewed list (an audit and an independent reviewer). Each fix is now the spec, written here, in
`PARTICULARS.md` and in `components.json` (the BOM's source). **None of them changes how Core looks.** The CAD follows
in the next pass: the cell contacts, the heat path and the pins.

| # | Finding | Fix | Numbers |
|---|---|---|---|
| 6 | **Heat: no path was designed.** The chassis ran +47 to +67 K at 2.1 W, so charging while lit at full in a 35 °C room can't pass | (a) **An efficient LED:** 130 lm/W or better, so 200 lm takes 1.5 W or less. (b) **Firmware foldback:** dim first, then cut the charge current. (c) **A real path:** the LED's board, then the aluminum chassis, then the anodized touch ring, which is the one metal face open to the room. A 2 mm PEEK spacer and an air gap separate the chassis from the cells' bays | Heat in the base at full: about 1.0 W from the LED (1.5 W in, about 35 % out as light) plus about 0.5 W from the charger at 9 V and 1.5 A, about 1.5 W in all, against 2.1 W before [E]. Foldback: chassis NTC at 55 °C → the LED to 70 %; at 60 °C → charge to 0.5 A; the cells' NTC stops charging at 45 °C (as before). Target: chassis 25 K or less over the room at full while charging, so 60 °C in a 35 °C room, with the cells under 45 °C. **To prove on the bench** (thermocouples on the chassis, a cell and the ring) |
| 7 | **The cell holders don't fit.** The Keystone 1042 is 77.1 mm long and its corners land outside the drum. It isn't polarized (that is the 1042P), and it is surface-mount, on a PCB the CAD lacks | **Bare spring contacts in the milled base**, no holder. The − end has a nickel-plated conical spring in a pocket. The + end has a gold-flashed leaf at the bottom of an 8 mm shroud milled 1.5 deep, so only a button top reaches it: a flat-top or reversed cell can't make contact. Leads run in a milled channel to the board | Bay 18.6 wide, 67.5 between contact faces with the spring at mid-stroke (for 65.0 cells plus a 0.8 button and the spring's 1.7) [E, to fit]. Cells: **button-top** LiFePO4 18650s. Power Sonic PSL-FP-IFR18650EC is flat-top: confirm a button-top version or qualify another maker [check] |
| 8 | **One FET per cell is unsafe.** Body diodes let a full cell charge an empty one at about 9 A | **Back-to-back FETs per cell under an ideal-diode controller** (one per cell; Analog Devices LTC4359 class [check]), **off by default**. The MCU runs from a diode-OR of the input and the cells, so it can check each cell before closing its switch | Turn on only within 0.1 V of the others (as before). Cross-current is then limited by the controller's reverse block to its leakage, microamps |
| 9 | **The dock's 5 V budget doesn't close.** It arrives at the LTC4162 at about 4.3 V, which needs 4.5 V | **USB PD at 9 V.** The 20 W adapter offers it. Add a PD sink in the dock and in the lamp's USB-C path. The LTC4162-F accepts up to 35 V in. The dock's geometry is fixed in §1: a center disc and an r 20 ring on a 2.0 island; the pins on the axis and at r 20, clear of the USB-C receptacle; 0.8 N pins, so no tilt | At 9 V and about 0.7 A in, the contacts' and cable's drop is about 0.1 V, leaving 8.9 V against the charger's 4.5 V floor |
| 10 | **A 3.45 V limit doesn't give 90 % on LiFePO4's flat curve, and a voltage fuel gauge won't work** | **Coulomb counting** (a coulomb-counter IC, Analog Devices LTC2941 class [check], re-zeroed at each full charge). The 90 % limit becomes a counted stop: 4.05 Ah of 4.5 Ah. The charge voltage stays 3.6 V | Charge time at 1.5 A: **about 2.7 h to 90 %**, replacing "about 2 hours" everywhere |
| 11 | **Touch electrode** | Baseline tracking (it drifts with the ground: on battery, the cable or the dock); a 50 ms debounce for taps; a 600 ms hold to dim; re-baseline when the input changes. **Test on all three**: battery, cable and dock | |
| 12 | **Stale text** | Core is UL 153 with Supplement SA, not 62368-1. Hemisphere's hardwired listing is UL 1598 for its own shade, not "any shade". Hemisphere's bayonet pins are screwed, not "pressed into the hub" (PARTICULARS, components). The cells are button-top, not "flat top" | |

## Sources (public pages, not quotes)

- Adafruit Universal Qi transmitter, 2162: https://www.adafruit.com/product/2162
- Adafruit Universal Qi receiver, 1901: https://adafruit.com/product/1901
- Pulse/Yageo WM5V 5 W transmitter datasheet: https://www.yageogroup.com/content/datasheet/asset/file/DATASHEET_WM5V_5W_TX
- QST QPT-0005 datasheet (LCSC): https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2404181054_QST-QPT-0005_C6155689.pdf
- NXP MWCT1101 at Farnell: https://ie.farnell.com/nxp/mwct1101clh/wireless-power-transmitter-lqfp/dp/2401867
- Mill-Max magnetic spring-loaded headers at Mouser: https://www.mouser.in/en/c/?series=878
- A 2-pin magnetic pogo connector at Electrokit: https://www.electrokit.com/en/2-pin-female-magnetic-pogo-pin-connector
- A USB-C touch dimmer board for cordless lamps: https://ifuturetech.org/product/type-c-usb-touch-based-stepless-table-lamp-dimming-circuit-board/
- Ningbo Liangying at Light + Building: https://light-building.messefrankfurt.com/frankfurt/en/exhibitor-search.detail.html/ningbo-liangying-electronic-technology-co-ltd/mf_1_0052607098_3664095_10000016202401.html
- Inno Casa on HKTDC: https://sourcing.hktdc.com/en/Product-Detail/LED-Table-Lamp-1Z03JV9DO
- Tenergy 31001 pack: https://www.batteryjunction.com/tenergy-31001-battery-pack
- Tenergy 30085 LiFePO4 cell: https://www.batteryjunction.com/products/tenergy-30085-18650
