# The contradiction sweep: 31 October 2026

Brand lane, r47. **Read-only across the other lanes.** Nothing in another lane's files was edited; the coordinator
routes those fixes. Paths are under `spinoffs/barkhorn/`.

**Branches read:**
- brand: r47-brand fc0b3e1d
- owner: r46-owner-notes 86b09faa
- lamps: r32-lamps-final f5426f0f
- bar: r33-planet-world 1717fdd9
- horn: r33-speaker-horn a1c61f27
- site: r47-site-next 3e647894
- deck: the slides quoted by the coordinator

`FACTS.md` holds what's right where it's settled.

## The top ten, by impact

| # | What | One side | The other | Which is right | Fix |
|---|---|---|---|---|---|
| **1** | **The debut date, in a vendor letter** | horn `rfq/tropos/e-laminated-horn/letter.md:45`: "a debut on **21 January**". Also horn `make/schedule.md:4,22` and `make/README.md:16`; lamps `launch/first-articles.md:87,108,130` ("21 to 24 January"; the "21 Jan" readiness row; "Cash out by week for 21 January"); owner `R2:361,375`, `R7:10,511` ("19–21 Jan"), the YC draft:181 | bar `r43/DEBUT-ROOM.md:5`; lamps `debut-night-lighting.md:3`; site `web.py:2838`; owner `R9:3`: **Tuesday 19 January 2027** | **19 January.** The RFQ letter would give a shop the wrong date. Both build schedules count their float to the 21st, so the real float is **two days shorter**, and the lamps' "18 Jan, hung for an evening" leaves none | **horn** (RFQ letter, schedule), **lamps** (first-articles), research (R2, R7, YC) |
| **2** | **The horn, in public copy** | site `web.py:129,2073` and live `site/index.html:775,834,945`: "formed from the same tinted cast acrylic"; the journal post on forming the horn (`web.py:974-976`); deck: "on a formed acrylic horn"; brand `press/tropos.md:5,18` | horn `make/schedule.md:22`, `laminated-horn.md:22`; site's dark post `web.py:1175,1192`; deck's "first" slide: **the January pair's horn is 22 layers of 1/2 in stock sheet**, first horn mid-December | **Both, for different horns.** The first pair is laminated; production's route is the owner's. Public copy must not call the debut pair's horn "formed" | **site** (live copy, journal), **deck** (Tropos slide), brand (press sheet, once the owner decides). *The brand lane's release, pitches, gallery letter and Vienna draft are fixed in this commit* |
| **3** | **Lamps and Mantle against the $50k** | deck: Hemisphere, Core and Mantle **$14,400** | lamps `first-articles.md:175`: "**Total to 18 January: about $15,500**"; +$530 if the debut Mantle uses the 2M Black (:183) | **The cash table**, which is newer and itemised. It is about $1,100–1,630 over, out of the $4,500 contingency | **lamps** to re-cut, or the coordinator to move the line |
| **4** | **Tropos against the $50k** | deck: Tropos **$18,500** | horn `make/schedule.md:102-104`: "about **$18,520** … with the contingency … about **$21,300**" (laminated, no tool); owner `R2:87,353`: $9,577 parts + $9,600 tooling = $19,177 (the formed route) | **The horn schedule**: it is the route being built. It's at the line with no margin, and over it with its own contingency | **horn** and the coordinator |
| **5** | **The debut's money** | deck: "Debut night (crating, transport, photographs) **$4,000**", and no line for the room | bar `DEBUT-ROOM.md:81`: the Firehouse "**$4,200–6,500**", plus officers; lamps `debut-night-lighting.md:27`: Full "$9,650–10,250", Middle "$4,950–5,450"; brand `photo/BUDGET.md`: the night shoot about $2.9k lean | **Unfunded.** The $4,000 covers crating, transport and photographs only. The room and any extra lamps need money from somewhere | **owner** (a budget decision); bar and lamps keep their ranges |
| **6** | **Testing** | deck: "Tropos testing **$5,000**", nothing for the lamps | lamps `lab-rfq/README.md:41-42`: R3 puts all four at "about **$18–46k** to first sales"; Core alone $3–8.5k (FCC, DOE Appendix Y, CEC **before any California sale**) | **R3.** The lamps can't be sold, at the debut or on Kickstarter, without FCC, DOE and CEC. The Kickstarter goal carries it (`kickstarter/ECONOMICS.md`); the $50k doesn't | **owner** |
| **7** | **Tropos's price** | deck: "**$19,000 a pair (planned)**"; bar `POPUP.md`, `NUMBERS.md` break-evens; YC draft:242 | owner `R4:21`: "**$32,000** / pair", Founders' $42,000 (8 pairs); `R9:12`; horn `make/laminated-horn.md:197`: "on a **$20,000** pair" | **Owner-pending.** $19,000 is the owner's last decision on record (round 14, README:2502). R4 recommends $32,000. The horn's $20,000 is a third figure | **owner**; then horn (its $20,000) and bar (its break-evens) |
| **8** | **The first-run programme** | site `web.py:2921-2922,2938` (a dark page): "One of the first hundred pairs … **No money changes hands**"; brand `money/founding-terms.html`: refundable deposits, with counsel's questions | owner `R4:139`: a **Founders' Edition of 8 pairs** at $42,000; `R2:69`: dated deposits December–January | **Three programmes.** The owner picks one, then counsel. *The brand lane's release now says so instead of promising a deposit* | **owner**, then site / brand / research |
| **9** | **The pop-up's dates and money** | bar `r42/POPUP.md:17-18`, `NUMBERS.md:125`, `r42/README.md:35`, and the public **`r42/housebook/index.html:131,145`**: "an 8-week pop-up from **19 January**, $22k–36k, from the $50k product raise"; `r43/V2V-APPLICATION.md:87,122`: "We would like 19 January 2027" | bar `V2V-APPLICATION.md:20,23,37,185`: the $50k "**does not pay for the pop-up**"; V2V suits "a **February-to-spring** run" | **February–March, not from the $50k** (the coordinator, 31 Oct). The V2V application's own text, which goes to the programme, still asks for 19 January | **bar** |
| **10** | **The lamps' public particulars** | lamps `companions/PARTICULARS.md:15,27,29,54-55`: Core "About **2.0 kg** … about 2.2 kg", Hemisphere "about **1,100 lm**", "To be listed to **UL 1598**", Core **$650**, Hemisphere **$795–895**; site `web.py:160`: "listing to UL 1598 to follow"; YC draft:109-111: Mantle "About **$5,000**" | owner README:135, 138: Core about 1.5 kg; Hemisphere 575 lm; lamps `certification.md:17`: **the plug-in swag under UL 153** first; R4: $750 / $1,200 / $9,500 | **The newer figures** (1.46–1.5 kg, 575 lm, R4's prices pending). The listing route is unresolved (FACTS, owner decision 4) | **lamps** (PARTICULARS), **site** (the UL line), research (YC) |

## The rest

| # | What | One side | The other | Right | Fix |
|---|---|---|---|---|---|
| 11 | Mother EARF's object | owner `R10:12,16,18,193,219-220`: "the 2 m globe", a 4 m globe, "A 2 m **sphere** at 190 kg … walls about 12.7 mm", wind loads for a sphere | bar `planet/README.md:339-373`, housebook: six slotted discs, **1.25 m**, ~190 kg | **The bar.** R10's wall and wind maths don't apply. The Amsterdam text is already written to the discs | research (R10 note) |
| 12 | Mother EARF's colour | bar `planet/README.md:343`: "The owner's choice (2026-10-22): the site's multicolour" | the same file, :353, :368-373: the Smoke version, and "the multicolour variant … kept for comparison only … not recommended" | **Multicolour** (the owner) | bar: mark 347-373 superseded |
| 13 | Tropos's weight without the horn | site `web.py:126`: "About 72 kg; **62 kg** with the horn lifted off" (a 10 kg horn) | horn `laminated-horn.md:35`: the horn "4.1 kg" formed, "5.7 kg" stepped; :170 "assumed 10 kg" as a tipping allowance | **About 66–68 kg** without the horn (est.), until weighed | site; brand `press/tropos.md`, `PACKAGING.md` follow |
| 14 | Laminated-horn layers | horn `make/plan-b.md:15,27`: "**14** layers of … 20 mm sheet" | horn `laminated-horn.md:22`, `build_rfq.py:208`; site's dark post: "**22** layers of 1/2 in" | **22** (plan-b says "since redrawn") | horn (plan-b note); brand `MEDIA-PLAN.md`'s "14 to 22" → 22 |
| 15 | The laminated horn's depth | owner `R7:12,301,376`: "630 × 366 × **238** mm" | horn `laminated-horn.md:23`: "**278** deep" (22 × 12.64) | **278** (238 is the formed flare) | research (R7) |
| 16 | The laminated route's cost | horn `laminated-horn.md:196-197`: "$60,000 to $160,000 more across the run … about **$600 to $800** a pair" | its own arithmetic over 100 pairs: $600–1,600 | **$600–1,600** | horn |
| 17 | The $50k's older split | owner README:139: $19,200 / $10,400 / $8,000 / $3,600 / $2,000 / $4,000 / $2,800 | deck: $18,500 / $14,400 / $5,000 / $3,600 / $4,000 / $4,500 | **The deck** | research (note the row as superseded) |
| 18 | Mantle's cost in the deck | deck (per lamps README:1661): $2,775 | lamps README:1659: **$3,815**; `mantle-bom-changes.md:65`: +$65 or so | **$3,815+** | lamps note → coordinator (deck) |
| 19 | Tropos pairs at the pop-up | bar `POPUP.md:146`: "**two** Tropos pairs from EARF's own stock" | deck: one prototype pair ($18,500) | **One** | bar |
| 20 | Planet EARF's size | bar `planet/README.md:111,195,264`: 49 people; "38 seats" and "28 seats" | bar `r42/housebook/index.html:127`: "Seats **55**, occupant load 133" for 2,800 sq ft | **The housebook** (r42, newer) | bar |
| 21 | The Session's schedule | bar `planet/README.md:221`: Tue–Thu, 8 pm, six chairs | bar housebook :208: "Two a night … Eight of the eleven chairs" | **The housebook** | bar |
| 22 | Old names | bar `planet/README.md:196-213,302-303`: "Four **Atmosphere** speakers, the Hemisphere **North** pendants"; horn `rfq/tropos/README.md:3`: "(the **Cloud**…)" | owner: Tropos; Hemisphere | **Tropos, Hemisphere** (round logs may keep history) | bar; horn (internal only) |
| 23 | Coin cost | bar `POPUP.md:53`: "about $5 each"; `planet/README.md:237`: $6–9 | lamps `launch/coin-quote.md:45,51`: "about **$8–12** a coin" at 200 | **$8–12** (a quote by route) | bar |
| 24 | The V2V grant | bar `POPUP.md:153,24`: $3,000–12,000, "3 months free" | bar `V2V-APPLICATION.md:141`: "$2,000 to $10,000 … free rent is not stated" | **V2V-APPLICATION** (read 31 Oct) | bar |
| 25 | The desk globe's price | bar `POPUP.md:54`: $450–550 | lamps `companions/README.md:827,889-890`: $650–850; $495–595; $395–450 | Unsettled (a proposal) | bar and lamps agree one |
| 26 | Core's runtime against the owner's | owner README:138: "**5–6 hours**" | lamps, with the chosen cell: **4.7 h** at full brightness at 90%; 5.8 h at the bar setting. Site: "about five hours" | "About five hours" is defensible at full; the owner's 5–6 holds only at the bar setting. Tell the owner | lamps (to tell the owner) |
| 27 | Mantle's cartridge | lamps `companions/README.md:224`: "Now the 2M **Black**" | lamps `mantle-drive.md:74`, `first-articles.md:56,151`: the 2M **Blue** for the first build | **Blue first**; which unit plays at the debut is open (+$530) | lamps |
| 28 | Horn fallback | owner YC:383,389: "two formed halves cemented together" as the fallback | horn `make/plan-b.md:33`: B (halves) "Not recommended"; A (laminated) recommended | **plan-b** | research (YC) |
| 29 | The cabinet sheet | site `web.py:2112`: "two **20 mm** walls" | horn `stock-pair.md:12`: the first pair in TruCast 2064 at **3/4 in (19 mm)** | Both: design 20 mm, the first pair 19 mm | none (note only) |
| 30 | Milan's dates | brand files: "12–18 April" (Milan Design Week); brand `partners/`: "13–18 April (Salone)" | owner R5, R9: Fuorisalone 12–18, Salone and Euroluce 13–18 | **Both right.** Name which event | brand (keep the names straight) |

## Fixed in this commit (the brand lane's own files)

| File | What changed |
|---|---|
| `press/releases/RELEASE-MARCH.md` and its PDF (now built by `make_release.py`) | The horn is "made from the cabinet's own tinted acrylic", and the first pair's is "22 layers … stacked". Production's route is left to the owner. The Founding Hundred line no longer promises a deposit; it names the three programmes for the owner and counsel |
| `press/releases/PITCHES-PRINT.md` (Wallpaper\*) | "formed" → "built from the cabinet's own tinted sheet, 22 layers deep" |
| `brandbook/money/GALLERY-LETTERS.md` (FUMI) | "formed" → "built" |
| `brandbook/money/applications/high-end-vienna-start-up.md` | "formed" → "built" |
| `brandbook/kickstarter/README.md`, open question 4 | Core is about 1.46–1.5 kg (2.2 kg was superseded); runtime 4.7 / 5.8 h |

**Left for the owner's horn decision, in the brand lane** (each says "formed"; one pass once the owner chooses):
- `press/tropos.md` (it mirrors the site);
- `brandbook/launch/LAUNCH-GRID.md` (post 7);
- `brandbook/launch/STORYBOARD.md` and the teaser's caption frame;
- `brandbook/launch/MEDIA-PLAN.md`'s angle;
- `brandbook/money/applications/idsa-idea-2027.md`;
- `brandbook/money/applications/emergent-ventures.md`;
- the Brand Book's text.

## Consistent everywhere checked

- **FOG:** 21–24 January (the gala 20 January).
- **HIGH END Vienna:** 6–9 May; the Start-Up Area closes 31 December.
- **Amsterdam:** closes 7 December.
- **RFQs:** the week of 2 November.
- **The eight tints:** their names and order.
- **Specs:**
  - Tropos's drivers, amplifier, crossover and height;
  - the BOMs: $9,577 / $4,572 / $2,027 / $3,815;
  - Hemisphere 200 mm, 2700 K, CRI 90;
  - Core 160 mm, 180 mm tall.
- **Names:** Tropos, Hemisphere, Core and Mantle in all public copy.
- **The site:** no sustainability claims (the Mother EARF promise stays in `launch/held-back.md`).
