# Circuit boards: what is ready to make (round 43, 2026-10-31)

`first-articles.md` books "Core's board: fab and assembly, 5 boards, $400 [E]" for the week of 23 November. This note
checks whether that can happen, and does the same for Hemisphere and Mantle.

**In short:**
- **Core:** the board exists only as a description. There is no schematic, layout, gerbers, BOM with part numbers or
  pick-and-place file in this branch, on `r32-turntable-final`, or on any branch whose name points to electronics (none
  does). About 4 to 6 weeks of electronics work stands
  between it and an assembler, so **23 November holds only if a contract engineer starts by 2 November.**
- **Hemisphere:** no board of ours in the hardwired version, which is all bought parts. The plug-in swag adds one
  small board, unless a listed plug-in driver is found (it waits on the owner's swag answer).
- **Mantle:** no board of ours. The phono stage, its regulator and the LED dimmer are all bought.

## 1. Core's board

### What exists

Only the function, in `components.json` (`core-board-18650`, and the retired `core-board` it points to),
`certification.md` and `first-articles.md`:

| Block | As specified | Source |
|---|---|---|
| Input | USB-C sink, 5 V 3 A, on a small board in the base's corner (at 170°), joined to the main board by a flex | `core-board`, `core-board-18650` |
| Charger | Analog Devices **LTC4162-F** (LiFePO4), switching, with power path, I²C telemetry, no trickle at rest; a 90 % limit (about 3.45 V) by default, a full-charge mode; at most 3.6 V a cell | `core-board`, `certification.md` |
| Cells | three LiFePO4 18650s in parallel (1S3P), user-replaceable, in three Keystone 1042-type holders | `core-cells-18650`, `core-holder-18650` |
| Protection | a protector (over/under voltage, over current, short circuit); charging held off below 0 °C and above 45 °C by the cells' NTC | `core-board` |
| **Per-cell switching** (new since `certification.md`) | a FET per cell; a power-up check (each cell 2.5 to 3.65 V, all within 0.1 V); refuse a failing set with a blink code; reverse-polarity protection; a current limit per cell | `certification.md`, Core item 1 |
| Fuel gauge | one, asleep when the lamp is off and full | `core-board`, `certification.md` (R3) |
| LED driver | two channels, warm-dim 2200 to 2700 K, about 2.5 W | `core-board` |
| Touch | capacitive, on the anodised ring | `core-board` |
| Test access | two test pads at the cells' + and − behind the hatch; a firmware test mode (a 10 s press while charging turns the LED load off) | `certification.md` (R3) |
| Standby | under 0.1 W at the wall with the cells out, the adapter included | `certification.md` (R3) |
| Shape | a 48 mm ring under the LED, in the middle of the cells' triangle | `core-board-18650` |

### What's missing

| Item | State | Work [E] |
|---|---|---|
| **A microcontroller** | Not named anywhere, but needed: the touch, the per-cell check and blink code, the 90 % limit and test mode over the charger's I²C, and the fuel gauge all need one | part of the schematic |
| **Schematic** | none | 5 to 7 days: the charger's power path and inductor, three per-cell FET switches with sensing, the two-channel constant-current driver, the touch, the MCU, USB-C CC resistors and ESD |
| **Part selection with MPNs** | Only the LTC4162-F is named. Not chosen: the protector, the fuel gauge, the per-cell FETs and sensing, the LED driver, the MCU, the inductor, the connectors, the flex | inside the schematic days |
| **Layout** | none. A 48 mm ring, probably 4 layers, with a switching charger at up to 1.5 A beside the LED's heat; plus the USB-C board and its flex | 4 to 6 days |
| **Gerbers, drill, BOM, pick-and-place, assembly drawing** | none | 1 to 2 days, from the layout tool |
| **Firmware** | none | 6 to 10 days: the touch, dimming, the cell check, the charger set-up, the fuel gauge, sleep, the test mode |
| **Bring-up** on the first 5 boards | | 3 to 5 days, and probably one board revision |

**Total: about 4 to 6 engineer-weeks [E], plus one revision.** At contract rates of $100 to $175 an hour [E, not
quoted], that is roughly **$16k to $40k [E]**, well above the $400 booked, which covers fab and assembly only.

### Timing against `first-articles.md`

- Schematic and parts from 2 November, layout 16 to 20 November, files out about **23 November**: this holds only if
  an engineer starts on **2 November**, with the evaluation kit on the bench in parallel (already planned).
- A realistic date is **early December** for files, so boards in about **late December**. The 4 January "boards in" in
  `first-articles.md` is tight but possible with a quick-turn assembler (below), not with a 3-week overseas one over
  the holidays.
- **The fallback already in `first-articles.md` stands:** the LTC4162 evaluation kit and a hand-wired cell switch
  for the debut, the real board after.
- **Decision for the owner:** hire a contract electronics engineer this week, or accept that the debut's Cores run on
  the evaluation-kit fallback. In either case, the 23 November line in the purchase schedule moves to "files from
  the engineer".

### A trap in the charger's ordering code

The LTC4162 comes in several chemistries; Core needs **the -F (LiFePO4) version**. JLCPCB's catalogue lists the
LTC4162 under part C7451117 as **LTC4162IUFD-L40M#PBF, the Li-ion version: the wrong chemistry for Core** ([JLCPCB
C7451117](https://jlcpcb.com/partdetail/C7451117), from a search result; stock not shown). No -F listing was found at
LCSC or JLCPCB. Confirm the -F ordering code on Analog Devices' LTC4162 page and buy it from Digi-Key, Mouser or ADI
directly. At an overseas assembler it will almost certainly be **consigned** (or bought by them on request as a
"global sourcing" part).

## 2. Assembly quote requests (send once the files exist)

**Not to send yet.** No assembler can quote without the BOM, and the stock questions (is the LTC4162-F in stock or
consigned) depend on it. The texts below are ready for the day the engineer delivers the files. They ask about the
charger and the protection parts by name.

**What's known about the routes (public pages, not quotes):**

| Route | Lead time (as published) | Parts | Notes |
|---|---|---|---|
| **MacroFab** (Houston) | 10-day prototyping advertised; the platform quotes each lead time instantly | turnkey, consigned, or held in inventory; a per-component fee on turnkey parts ([help](https://help.macrofab.com/knowledge/part-sourcing-turnkey-consignment-and-inventory)) | instant online quote from the files; sales quote for volume ([blog](https://www.macrofab.com/blog/macrofab-now-offers-10-day-prototyping)) |
| **Screaming Circuits** (Oregon) | 5 to 10 days economy, 1 to 2 days at a premium (old figures: [Electronic Design](https://www.electronicdesign.com/boards/are-you-screaming-help-prototypes)) | full turnkey, partial turnkey or consigned kit | confirm current terms on their quote page |
| **A Bay Area assembler** (SF Circuits and alike) | assembly 1 to 5 days, sourcing 1 to 3 days ([SF Circuits](https://www.sfcircuits.com/pcb-production-capabilities/pcb-assembly)) | turnkey or consigned | local pickup; useful for a revision in January |
| **JLCPCB** | about 1 to 3 weeks with shipping [E] | their parts library; others by "global sourcing" or consigned | the LTC4162-F is not in their library (above) |
| **PCBWay** | about 2 to 4 weeks with shipping [E] | turnkey with their sourcing, or consigned | |

**Cost [E, not quoted]:** 5 boards about **$300 to $700** at a US quick-turn house with turnkey parts (setup is most
of it), about **$150 to $350** overseas, before parts. 50 boards about **$30 to $45 a board** US and **$15 to $25 a
board** overseas, plus parts (the $34 a board in `components.json` is a 500-off figure). The quotes replace these.

### Short (for a web form)

```
Quote please: PCB assembly, 5 boards (and 50 for comparison). 4-layer rigid board, 48 mm round, plus a small USB-C
board joined by a flex (or FFC); [N] SMT parts, QFN-28 (4 x 5 mm) charger IC, double-sided [Y/N]. Gerbers, BOM with
MPNs, centroid and assembly drawing attached. Please say which parts you stock and which must be consigned,
especially the Analog Devices LTC4162-F (LiFePO4 version, ordering code [CODE]) and the protection parts [LIST].
Lead time and price at 5 and 50? [Your name], [contact line]
```

### Full (for email)

```
Subject: Quote: PCB assembly for a battery LED lamp, 5 and 50 boards

Hello,

We're EARF, a small Bay Area product company. We'd like a quote to assemble the control board of a battery table
lamp: 5 boards for first articles, and 50 for comparison.

The board:
- a 4-layer rigid board, 48 mm round (a ring), and a small USB-C board joined to it by a flex [or an FFC];
- [N] SMT parts, smallest [0402], one QFN-28 (4 x 5 mm, the charger), [one / both] sides;
- a LiFePO4 charger (Analog Devices LTC4162-F, ordering code [CODE]), cell protection and per-cell switching,
  a fuel gauge, a two-channel LED driver, a capacitive touch sensor and a microcontroller.

Attached: gerbers and drill, the BOM with manufacturer part numbers, the centroid (pick-and-place) file and the
assembly drawing.

Could you tell us:
1. The price at 5 and at 50, with your setup and stencil charges shown.
2. Which BOM lines you stock, which you would buy for us, and which we should consign. In particular the LTC4162-F
   and the protection parts ([LIST]).
3. The lead time from files and parts in hand, and whether you can program the microcontroller ([PART], SWD) if we
   send the image.
4. Whether you inspect QFN joints by X-ray, and whether you can run a short functional test we supply.

Thank you,
[Your name]
EARF
[contact line]
```

## 3. Hemisphere

**The hardwired version has no board of ours.** The light is a Bridgelux Vero SE 10 COB in an Ideal Chip-Lok holder on
its heat sink, driven by a bought, listed Class 2 driver in the canopy: the ERP ESS010W-0180-42 (575 lm level), or
the EPtronics LD6W as the alternate (`components.json`: `north-driver-575`). Its own work is the driver bench test
(headroom at Tc 85 °C) in the week of 9 November.

**The plug-in swag version may need one small board.** `certification.md` (Hemisphere, item 5) gives two routes:
- **A listed Class 2 constant-current plug-in at 180 mA.** None found yet. If one turns up, there's no board.
- **A listed 24 to 30 V constant-voltage plug-in plus a small constant-current board in the canopy**, dimmed on the
  low-voltage side (PWM above 20 kHz, or analog).

  That board is simple: one constant-current buck or linear stage, an in-line dimmer input and a connector. About
  **1 to 2 weeks** of work [E], or none if a bought constant-current LED module fits and its PWM frequency is
  confirmed above 20 kHz.

  It waits on the owner's answer on the plug-in swag.

## 4. Mantle

**No board of ours.** Every electronic part is bought and used whole (`turntable_float.py` and its parts list on
`r32-turntable-final`):

| Function | Part | Note |
|---|---|---|
| Phono stage | **Pro-Ject Phono Box S2**, in its own case under the platter | a finished product, not a recognised component (`certification.md`): the lab tests it in place |
| Its supply | an **LT3045 module** (24 V to 18 V) in the rear box | a bought module from Tindie or Amazon. The lab will want its ratings, so buy one with a datasheet; or have a 2-layer LT3045 board made from Analog Devices' reference design (a day of work [E]) |
| Rear box | Hammond 1590A: the arm's lead in, a DPDT bypass toggle, RCA out, an earth post | hand-wired, not a board |
| LED dimmer | **Waveform FilmGrade Flicker-Free dimmer** (part 3081, 25 kHz PWM) in line on the 24 V lead | its PWM frequency to confirm on the datasheet (above anything the phono stage hears) |
| LED adapter | Mean Well GST25A24 today | swap for one listed LPS adapter of 15 W or less (`certification.md`, Mantle item 1) |
| Motor drive | Rega 24 V motor kit and Neo PSU MK2 | the Neo's listing certificate to request from Rega |

What the lab wants for Mantle is a **wiring diagram** (the supplies, the LT3045, the phono stage, the toggle, the star
earth), not board files. About **half a day** to draw it from the parts list.

## What to decide

1. **Core:** hire a contract electronics engineer now (about $16k to $40k [E], 4 to 6 weeks), or run the debut on the
   evaluation-kit fallback and build the real board after. Either way the $400 line in `first-articles.md` covers
   only the 5 boards' fab and assembly.
2. **Hemisphere:** the plug-in swag answer decides whether a small canopy board exists at all.
3. **Mantle:** none for boards. Buy an LT3045 module with a datasheet, and draw the wiring diagram for the lab.
