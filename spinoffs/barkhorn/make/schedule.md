# Tropos: a dated schedule to a first horn and an assembled pair (2026-10-31)

The coordinator's targets (not commitments):
- a San Francisco debut in FOG Design+Art week, **21 to 24 January 2027**;
- prototypes photographed by **mid-February**;
- Milan Design Week, **12 to 18 April**;
- High End Vienna, **6 to 9 May**.

All durations are estimates from the repo (the tooling board's 3 to 4 weeks, R1's and R3's figures) plus ordinary shop
times. Nothing has been quoted. Week 1 starts Monday 2 November. The plan loses about a week to Thanksgiving (26 Nov)
and two to Christmas and New Year.

## The answer

| route for the horn | first horn | the pair assembled | 21 January | mid-February | April |
|---|---|---|---|---|---|
| **Laminated from stock 1/2 in sheet** (`laminated-horn.md`) | about **18 December** | about **8 to 13 January** | **yes, with about a week to spare**, if everything is ordered in the first week of November | yes | yes |
| **Formed from stock 3/8 in sheet** (9.5 mm: 2423 and 2064 are stocked at 3/8 in, R1), after a passing quarter trial | about **22 January** | about **29 January to 5 February** | **no** | **yes**, if the trial passes first time | yes |
| Formed, if the trial fails and the horn goes laminated | about 20 January | about 1 February | no | yes, just | yes |
| **Formed or laminated in a custom deep lot** (a colour match and a pallet pour) | about mid-March | about late March | no | no | **only April**, with little margin |

- **For 21 January, build the laminated horn.** It needs no tooling and no custom pour. It starts the day the stock
  sheet arrives.
- The formed horn cannot make January. Its plug, its trial and its full plug run in series, about eight weeks before
  the first shot.
- The custom deep lot is an April item at the earliest. The first pair should be in stock colours either way.

## The critical path (the laminated pair for 21 January)

| week of | what | depends on | risk to the date |
|---|---|---|---|
| **2 Nov** (week 1) | Order the chips and the 1/2 in off-cuts (R1 §5, about $100). Send the RFQs (`rfq/tropos/`, once the owner releases them). Order 2 x FA122, the remote kit and the drivers. Book the EMC pre-scan and the FCC lab slot for early February. | the owner's go | **The start date.** Every week lost here is a week lost at the end. |
| 9 Nov | Chips and off-cuts in hand. Settle what 1/2 in looks like against the 3 mm chip (R1 §1.2) and pick the sheet (`stock-pair.md`). | the chips | A vendor whose 1/2 in is far deeper than expected means a thinner or lighter code. That costs a week at most. |
| 16 Nov | Quotes back. Purchase orders: cabinet shop, horn layers (the same shop), sheet. | quotes | **The cement.** No Bay Area shop says publicly that it does polymerising joints (vendors.md). If none will, E&F cuts and polishes, and EARF bonds in-house with ACRIFIX 2R 0190 (a jig and a week of practice). |
| 23 Nov | Stock sheet delivered (LTL, 1 to 2 weeks). Amplifiers and drivers delivered (1 to 3 weeks if stocked). | the orders | **The FA122's lead time.** Hypex sells through dealers. A backorder of 6 to 8 weeks would push the pair to mid-February. Order on day one; ask two dealers. |
| 30 Nov | Cut: the cabinet's panels and the horn's 22 layers, nested. | sheet | — |
| 7 Dec | Bond the horn's stack in three sub-stacks, then join them. Bond the cabinets. | jigs | **Bond lines** (C2 x 22, `laminated-horn.md`): reject and re-cut a layer rather than fill a void. |
| 14 Dec | Anneal both. 5-axis the horn's air path; polish. First horn about **18 December**. | the 5-axis shop | 5-axis time before Christmas. Book it in November. |
| 21 Dec to 1 Jan | Holidays. The second horn's machining, if the shop is open. | — | Two weeks. |
| 4 Jan | The second horn. Cabinets back. Assemble: drivers, amps, the remote, wiring (`assembly.md`, about 7.4 hours a speaker). | parts | — |
| 11 Jan | First-article inspection (`fai.md`). DSP voicing in HFD (2 to 3 days with a microphone). **Pair assembled about 8 to 13 January.** Photograph. | — | About **one week of float** before 21 January. |
| 18 Jan | Ship to the venue. FOG week **21 to 24 January**. | — | Show the pair as a prototype (see below). |

## The formed horn in parallel (for mid-February)

| week of | what |
|---|---|
| 16 Nov | Purchase order for the quarter-trial plug ($1,928) and base. The 5-axis program from the CAD (`out-horn-options/`). |
| 7 Dec | Trial plug delivered (2 to 3 weeks). Three trial shots in stock 3/8 in sheet: clear, then 2423 and 2064 (`forming-trial.md`). |
| 14 Dec | Gauge, scan, decide. If it passes, order the full plug (3 to 4 weeks, so mid-January after the holidays). |
| 18 Jan | Full plug in hand. First full shots, trim, anneal, cement the throat piece. |
| 25 Jan | First formed horn. The second in the week after. Fit it to the laminated pair's cabinets, which are already done. |
| early Feb | The formed pair, to photograph beside the laminated one by mid-February. The owner chooses the route from the real thing. |

## Cash out by week: the laminated Smoke pair for 21 January

**Sources:**
- The parts list's prices: `out-cloud/bom.md`, for 2.
- R1's sheet prices: AC Plastics, 31 October.
- The shop labour: `assembly.md`, the first pair at x 1.5.
- The laminated horn's shop work: `laminated-horn.md`.

"est." marks an estimate with no price behind it. No freight or tax is included unless it is listed. Shops are assumed to
take **50 % at order and the balance on delivery**, which is common but must be confirmed with each.

**Week 1 must be paid at once.** These are parts from stock, all quoted: the FA122s, the drivers, the remote and the chips.
Everything from 16 November waits for quotes.

| week of | item | supplier type | amount | if we stop |
|---|---|---|---|---|
| **2 Nov (week 1: pay now)** | 2 x Hypex FA122 plate amplifiers | Hypex dealer (EU, e.g. soundimports.eu) | $844.80 | returnable unopened on the dealer's terms, return freight ours (est.); they resell easily |
| | 2 x FaitalPRO 15PR400 woofers | pro-audio distributor (US) | $388.00 | usually returnable unopened (est.); resellable |
| | 2 x B&C DE1085TN compression drivers | pro-audio distributor (US) | $1,024.00 | usually returnable unopened (est.); resellable |
| | Hypex remote kit, a programmable AAA remote (in place of the coin-cell one, `compliance.md`), the link cable | Hypex dealer, any | $67 (the remote est. $30) | the kit as above; the remote returnable |
| | HF L-pads, film capacitors, leads, terminals | electronics distributor | about $100 | returnable, small |
| | Chips and 1/2 in off-cuts (R1 §5) | Canal, eStreet, ePlastics, Delvie's | about $103 | **no** |
| | Freight and import on the electronics | — | about $150 (est.) | **no** |
| | **week 1** | | **about $2,680** | about $250 is sunk; the rest returnable or resellable |
| **9 Nov** (after the chips) | TruCast 2064 3/4 in, 3 sheets (the cabinets; buy all three, 2 needed) | AC Plastics | $3,009.60 | uncut full sheets only by agreement, a restocking fee likely (est. 15 to 25 %) |
| | TruCast 2064 1/2 in and .220, one sheet each (rings, frames, grips, disc frames) | AC Plastics | $800.80 | as above |
| | TruCast 2074 1/2 in, 1 sheet (the two horns' 22 layers, nested) | AC Plastics | $569.80 | as above |
| | LTL freight for the sheets | freight | about $450 (est.) | **no** |
| | **week of 9 Nov** | | **about $4,830** | |
| **16 Nov** (after quotes) | Cabinet shop: cutting, edges, polymerising cement, annealing for the pair, **50 % deposit** | acrylic fabricator | $1,875 (of $3,750) | refundable only before cutting starts |
| | Horn shop: 44 layers cut and faced, edges, bonding, anneal, 5-axis air path, polish, plus the bonding jig, **50 % deposit** | acrylic fabricator, 5-axis | $2,000 (of est. $4,000) | as above |
| | Pods, caps, pads, saddles (`bom.md`, $755), **50 %** | acrylic fabricator | $378 | as above |
| | Ports and grips (`bom.md`, $485), **50 %** | acrylic former | $243 | as above |
| | Amp boxes, HF adaptors, posts, the boxes' aluminium collars (`bom.md` and `compliance.md`), **50 %** | sheet metal and lathe shop | $300 (of est. $600) | as above |
| | Hardware, seals, inserts, brass glands, batts, voile, cement, VHB, rating plates, the back's etching, the IR bracket and window | online, any | about $870 | mostly returnable, small |
| | Book the EMC and FCC lab for late January and February | test lab | $0 (no deposit expected, est.) | — |
| | **week of 16 Nov** | | **about $5,670** | |
| **by 16 November** | | | **about $13,180** | |
| 23 Nov to 30 Nov | Deliveries: sheet, electronics | — | — | — |
| 7 Dec | Metal parts delivered: balance | metal shop | $300 | — |
| 14 Dec | First horn: a progress payment | horn shop | $1,000 (est.) | — |
| **by 15 December** | | | **about $14,480** | |
| 4 Jan | Cabinets delivered: balance | cabinet shop | $1,875 | — |
| | Second horn: horn shop balance | horn shop | $1,000 (est.) | — |
| | Small acrylic parts: balances | acrylic shops | $621 | — |
| 11 Jan | A measurement microphone for voicing (UMIK-1 class) | any | about $100 (est.) | returnable |
| 18 Jan | Crates or padded covers, and a van to the venue in San Francisco | any | about $500 (est.) | — |
| **total, 2 Nov to 18 Jan** | | | **about $18,600** | |
| a contingency, 15 % | | | about $2,800 | |
| **with the contingency** | | | **about $21,400** | |

**Not in the table:**
- **The assembly** (about 15 hours a pair, `assembly.md`) is EARF's own time, not cash.
- **An Ember horn in stock 2423** alongside, to show at the debut: about $2,600 more. That is one sheet ($835.80) and its
  shop work (est. $1,750), half of it by 16 November.
- **Compliance**, all after 18 January (`compliance.md`):
  - EMC pre-scan, $800 to $1,500;
  - safety pre-check, $1,000 to $2,500;
  - FCC Part 15B, $1,500 to $3,500;
  - about $3,300 to $7,500 in late January and February.
- **The formed horn's route in parallel** (for mid-February): the quarter trial's $3,450 from 16 November, then the full
  plug's $7,100 in mid-December.

**What it means for January.** About **$13,200 must be spent by 16 November** and about $14,500 by 15 December. All of
it is the owner's own money, since a Kiva loan takes 9 to 11 weeks and a community lender 2 to 6. Of the week-1 spend,
only about $250 is sunk if the project stops: the electronics and drivers return or resell. The sheet and the shops'
deposits are the real commitment, and they start in the week of 9 November.

## Compliance in the schedule (`compliance.md`, R3)

| when | what | cost |
|---|---|---|
| week 1 | Book the lab: an EMC pre-scan and FCC Part 15B Class B (SDoC). 2 to 4 weeks' lead time. | — |
| week 1 | Order the AAA remote, not Hypex's coin-cell one. | +$10 to $30 a pair |
| week 4 (with the cabinets) | The amp box's aluminium collar and brass glands. | about $55 a pair |
| about 25 Jan | EMC pre-scan, half a day, on the assembled pair. | $800 to $1,500 |
| about 25 Jan | 62368-1 safety pre-check: hipot, touch current, temperature rise. | $1,000 to $2,500 |
| about 8 Feb | FCC Part 15B Class B test of the speaker and remote as a system; SDoC issued about late February. | $1,500 to $3,500 |
| before selling 100 | NRTL listing to UL 62368-1 (8 to 16 weeks). | $10,000 to $25,000 |

**At the debut**, the pair is not yet FCC-authorised. FCC rules (47 CFR 2.803, to confirm with the lab) allow an
unauthorised device to be **displayed** with a notice that it has not been authorised and may not be sold or leased
until it is. Take expressions of interest, not consumer orders, until the SDoC is issued, about late February. Check
deposits and pre-orders with the lab or counsel.

## What would move the dates

- **Earlier:** order the sheet and the FA122s from stock on day one, before the chips settle the colour. 2423 and 2064
  at 1/2 in cost about $836 and $570 a sheet, so the risk of buying a wrong sheet is small against a week.
- **Later:** no shop for polymerising cement; an FA122 backorder; a 5-axis shop booked through December.
- **April and May:** Milan wants the owner's chosen horn in the chosen colour. A custom deep lot ordered by mid-January
  (a 2 to 5 week colour match, then a pallet pour of 4 to 6 weeks) reaches a formed or laminated horn by late March.
  That is tight for Milan and comfortable for Vienna.
