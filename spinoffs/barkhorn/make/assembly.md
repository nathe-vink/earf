# Tropos: the assembly sequence, with times (2026-10-31)

This is the order one speaker is built in and the hours each step takes, so the budget's labour line rests on
something. The times are estimates for a skilled acrylic fabricator and a speaker builder, at the 10-pair rate. The
first pair takes about 1.5 times as long. Hands-off oven and cure times are listed but not charged.

**Rates (budget):**
- **Shop**: an acrylic fabricator's or machine shop's time, $100 an hour.
- **EARF**: our own assembly and test, $60 an hour.

## The cabinet (the acrylic shop)

| # | step | hours | notes |
|---|---|---|---|
| 1 | CNC-route the 20 mm panels, braces, ribs, lands and pad from three nested sheets; the 8, 6 and 12 mm parts | 1.5 | DXF nests in `out-cloud/dxf/` |
| 2 | Mill the edges square; polish the show edges (the shell's, the front panel's, the back's) | 2.5 | no flame polish near a future joint |
| 3 | Anneal the panels: 80 °C, an hour for each 3 mm, slow cool | 0.3 | 8 h in the oven |
| 4 | Cement the ribs to their panels, flat | 0.8 | polymerising cement; 1 h cure |
| 5 | Cement the shell on a jig: the corners, the front panel (set back 24), the braces, the lands, the bosses, the pad | 3.0 | no visible bubble in any joint; 4 h cure |
| 6 | Anneal the box | 0.3 | 8 h in the oven |
| 7 | Mill the lands' faces, the bosses' faces and the seal's groove in one setup | 1.0 | the back seats on all of them |
| 8 | Bond the inserts: 8 x M6 (woofer), 22 x M5 (back), 4 x M8 (feet), 8 x M4 (amplifier plate), the tie rod's | 1.2 | epoxy, in clearance holes; 12 h cure |
| 9 | Laser-etch EARF on the back and fill it in the colour | 0.5 | |
| 10 | Form and cement the grip cups | 0.6 | |
| 11 | Make the ports: flare the tubes' inner ends on the mandrel, anneal, cement into their frames | 0.8 | the length set on the first sample |
| | **the cabinet** | **12.5** | **$1,250** |

## The horn (the forming shop, then EARF)

| # | step | hours | notes |
|---|---|---|---|
| 12 | The flare, the throat piece, the pod, the cap and the pads | (quoted) | the forming shop's price a horn, `rfq/tropos/b-horn-forming/` |
| 13 | Cement the flare into the throat piece's socket on the centring jig; cement the pod onto the spigot; cement the pads (through the jig off the top's sockets) and the saddle | 1.0 | 4 h cure; a borescope at the joint |
| 14 | Bond the posts' M10 inserts and the adaptor's M5 inserts | 0.3 | 12 h cure |
| 15 | Anneal the assembled horn | 0.2 | 5 h in the oven |
| | **the horn's assembly** | **1.5** | **$90** |

## The speaker (EARF)

| # | step | hours | notes |
|---|---|---|---|
| 16 | The lining: the batts in their sleeves (sewn outside), placed on dots of VHB | 1.0 | |
| 17 | The amplifier's compartment: earth stud and bond lead, the L-pad and the capacitor on their plate, three glands, the gasket; screwed to the back; the FA122 on its inserts | 1.2 | earth continuity checked here |
| 18 | The loom: the leads through their glands, the IR receiver and its cable (in the master), tied | 0.8 | |
| 19 | The woofer in its rebate on its gasket; the ring and its magnets; the cloth disc | 0.6 | |
| 20 | The ports, from the front | 0.3 | |
| 21 | The horn: the driver to its adaptor, the adaptor to the boss, the cap twist-locked; the posts, sockets and sleeves; the tie rod | 1.0 | |
| 22 | The back on: the seal cord in its groove, 22 screws, evenly | 0.3 | |
| 23 | The feet, set and levelled | 0.2 | |
| 24 | Test: load the preset in HFD; sweep, polarity, impedance, a buzz sweep 20 to 200 Hz, a 30-minute burn-in; the pair matched (`make/fai.md`) | 1.0 | |
| 25 | Clean, inspect, photograph, pack | 1.0 | |
| | **the speaker** | **7.4** | **$444** |

## The labour line

| | a speaker | a pair (10-pair rate) | the first pair (x 1.5) |
|---|---|---|---|
| the cabinet (shop) | $1,250 | $2,500 | $3,750 |
| the horn's assembly (EARF) | $90 | $180 | $270 |
| the speaker (EARF) | $444 | $888 | $1,332 |
| **labour** | **$1,784** | **$3,568** | **$5,352** |

This is on top of the parts list's $9,577 a pair. The parts list's made parts are priced on material and setup, not
machining time. The forming shop's price for the horn (its forming, trimming and machining) and the outside work
(sleeves, seals) come with their quotes. With the first pair's labour, the first pair's parts and labour come to about
$14,900, before the forming shop's quote and the prototype's tooling ($7,109).
