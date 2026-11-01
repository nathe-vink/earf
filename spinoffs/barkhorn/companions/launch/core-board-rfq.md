# Core's board: the request to design houses (draft, 2026-11-01)

**A draft only: nothing has been sent.** Calling and sending are outward and parked with logistics.

The owner signed it on 2026-11-01 (r46-owner-notes 5b63e05b): "Core battery: A, LiFePO4", with the board bought as
a fixed-price design, estimated at **$12,000 to $20,000**.

The scope comes from:
- `boards.md` §1, the function and the missing work;
- the engineering review's fixes (`CORE-RECHARGE.md` §5 and §6);
- the signed contact dock.

The reference for the charger is Analog Devices' LTC4162-F evaluation board [check its demo-board number on ADI's
LTC4162 page], which is already planned for the bench.

**Who to send it to:** a fixed-price electronics design house, two or three of them for comparison. They must have
done battery products to UL standards; ask for references. The names are to choose when logistics opens.

## The request (for email)

```
Subject: Fixed-price design: the control board of a LiFePO4 battery table lamp (UL 153 with Supplement SA)

Hello,

We're EARF, a small Bay Area product company. We'd like a fixed-price quote to design the control board of a
cordless table lamp, from schematic to a bring-up-tested board, ready for a UL 153 Supplement SA listing. We'll own
the design files outright.

What the board does (each item is a requirement, not a suggestion):
1. Power in, two ways, each through its own ideal diode: a USB-C receptacle (service and travel) and two spring pins
   to a charging dock. Both negotiate 9 V by USB PD from a 20 W adapter (a PD sink on the lamp's USB-C path; the
   dock has its own PD sink).
2. Charger: Analog Devices LTC4162-F (the LiFePO4 version) with power path, 1.5 A, 3.6 V per cell; the lamp runs
   while it charges.
3. Cells: three LiFePO4 18650s in parallel (1S3P), user-replaceable, on bare spring contacts in the base. Per cell:
   back-to-back FETs under an ideal-diode controller (an LTC4359 or similar), OFF by default. A microcontroller,
   powered from a diode-OR of the input and the cells, checks each cell (2.5 to 3.65 V, all within 0.1 V) before
   closing its switch, and refuses a set that fails, with a blink code. Reverse-polarity protection and a current
   limit per cell. (One FET per cell is not acceptable: body-diode cross-charging.)
4. Gauge: coulomb counting (an LTC2941 or similar), re-zeroed at each full charge; a default 90 % stop (4.05 of
   4.5 Ah, counted, not by voltage); a full-charge mode.
5. Protection: over and under voltage, over current, short circuit; no charge below 0 C or above 45 C (the cells'
   NTC). Thermal foldback from an NTC on the LED's aluminium chassis: at 55 C the light dims to 70 %, at 60 C charge
   current drops to 0.5 A.
6. LED driver: two channels, warm-dim 2200 to 2700 K, up to 1.5 W (an LED module of 130 lm/W or better).
7. Touch: capacitive, on an anodised aluminium ring insulated from the chassis, with baseline tracking, a 50 ms
   debounce and a 600 ms hold; re-baseline when the input changes; it must work on battery, on the cable and on the
   dock.
8. Test access: pads at the cells' + and -, and a firmware test mode (a 10 s press while charging turns the LED load
   off) for the lab.
9. Standby: under 0.1 W at the wall with the cells out, the adapter included (DOE battery-charger rules).
10. Shape: a 48 mm round main board under the LED (the middle of the cells' triangle), a small USB-C board in a
    corner on a flex, and a 46 mm pin board carrying the two dock pins. We'll send the CAD (STEP) and the keep-outs.
11. The dock's own small board, in the same quote: a PD sink asking 9 V, a resettable fuse, and a load switch that
    powers the dock's contacts only when it sees the lamp's 47 kOhm sense resistor across them.

Deliverables, at a fixed price with payment by milestone:
- schematic and BOM with manufacturer part numbers (second sources where you can);
- layout (we expect 4 layers for the main board), Gerbers, drill, centroid, assembly drawing;
- firmware with source (touch, dimming, cell checks, charger set-up, gauge, foldback, sleep, test mode);
- bring-up of 5 assembled boards with a short test report (charge, the cell checks, foldback, standby);
- one board revision included;
- a design-for-compliance review against UL 153 with Supplement SA, FCC Part 15B and the DOE battery-charger test,
  so the lab finds nothing it could have.

Please tell us: the fixed price and what it excludes; the milestones and their payments; the schedule from a kick-off
(we'd like files within about 4 to 6 weeks); who would do the work; two references for battery products you've
designed to a UL listing; and your terms on IP (we need to own it).

We can send the CAD, the parts we've chosen so far (the LTC4162-F, the Power Sonic PSL-FP-IFR18650EC cells and
their UL 1642 summary, the adapter) and our certification notes under NDA.

Thank you,
[Name], EARF
[contact line]
```

## Short (for a web form)

```
Fixed-price design quote: control board for a LiFePO4 battery table lamp (UL 153 Supplement SA). LTC4162-F charger
(1.5 A), 3 x 18650 LiFePO4 in parallel with per-cell back-to-back FETs and ideal-diode controllers (off by default,
MCU-checked), coulomb-counter gauge, USB PD 9 V in from USB-C and a charging dock (ideal-diode OR), 2-channel
warm-dim LED driver to 1.5 W, capacitive touch, thermal foldback; 48 mm round main board + USB-C board on a flex +
pin board, and a small dock board. Deliverables: schematic, BOM, layout, Gerbers, firmware with source, bring-up of
5 boards, one revision, a compliance review. We own the IP. Fixed price, milestones, schedule, references? [Name], EARF
```

## What to compare in the replies

- **Price:** the fixed price against the $12k to $20k estimate.
- **Scope:** what is excluded. The usual gaps are firmware, the revision, certification support and parts for the
  bring-up boards.
- **Schedule:** against the first articles (`first-articles.md`).
- **Track record:** experience with battery products listed to UL, judged from the references.
- **Ownership:** IP terms (assignment, not a licence), and the files in our own repository.
