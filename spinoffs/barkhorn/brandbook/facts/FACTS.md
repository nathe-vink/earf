# EARF: the facts of record

Brand lane, r47, 31 October 2026. One page: what is settled, what is planned, and what is still the owner's.
- **Sources:** every line gives its source file and the commit it was read at.
- **Where sources disagree:** `CONTRADICTIONS.md` says which is right and which lane fixes it.
- **The rule:** when a file and this page differ, the file is the source. Raise it, then fix whichever is wrong.

**Branches, as read:**

| Short name | Branch | Commit |
|---|---|---|
| **brand** | r47-brand | fc0b3e1d |
| **owner** | r46-owner-notes (README owner rows, research R1–R10) | 86b09faa |
| **lamps** | r32-lamps-final | f5426f0f |
| **bar** | r33-planet-world | 1717fdd9 |
| **horn** | r33-speaker-horn | a1c61f27 |
| **site** | r47-site-next | 3e647894 |
| **deck** | the EARF Investor Deck, an artifact outside the repo | — |

## Names (settled)

| Fact | Of record | Source |
|---|---|---|
| Company | **EARF**. Not yet registered (owner, "Not yet", 2026-10-31) | owner: README rows 143–144 |
| Loudspeaker | **Tropos** (owner, 2026-10-29; was Atmosphere, then Troposphere) | owner: README:137 |
| Pendant | **Hemisphere** (South dropped, 2026-10-25; one pendant) | owner: README:136 |
| Table lamp | **Core** | brand: `press/core.md` |
| Record player | **Mantle** | brand: `press/mantle.md` |
| The bar | **Planet EARF**: planned, not public (it isn't on the site) | brand: `press/planet-earf.md` |
| The globe | **Mother EARF** | bar: `planet/README.md` |
| The coin | **EARFcoin** | bar, lamps |
| The listening format | **the Session**: one album, start to finish | bar |

## The tints (settled)

Eight, in this order, numbered 01–08:

| | | | | | | | |
|---|---|---|---|---|---|---|---|
| **01** Ember | **02** Dust | **03** Acid | **04** Poison | **05** Ice | **06** Haze | **07** Fog | **08** Smoke |

- **House tint:** Smoke.
- **The first prototypes** are cut from stock sheet: **2423 Red** stands in for Ember, **2064 Gray** for Smoke. Captions
  must say "stock".
- **Sources:** site `web.py:113-120`; lamps `launch/stock-colours.md`.

## Dates

| Date | What | Status | Source |
|---|---|---|---|
| **Spring 2027** | **The debut night: date and venue to be set** (the owner chose C, 2026-10-31). The candidates being sequenced are Thu 18 March and Thu 29 April (`SEQUENCE.md`; 25 March dropped: the Thursday before Easter). It was Tue 19 January; every brand file still says so (`CONTRADICTIONS.md`, row 0) | **owner-pending** | owner r46-owner-notes b3211a43 |
| 16–24 Jan | SF Art Week | fixed | owner R5 |
| 20 Jan / **21–24 Jan** | FOG Design+Art: its gala / the fair, at Fort Mason. Now for meetings with galleries, **without a show** | fixed | owner R5; bar `research-popup.md:144`; owner b3211a43 |
| Week of 2 Nov 2026 | Quote requests sent | planned | lamps `first-articles.md`; horn `make/schedule.md:32` |
| By 16 Nov | Lamp moulds ordered (critical path) | planned | lamps `first-articles.md` |
| About 18 Dec | The first laminated horn | planned | horn `make/schedule.md`, `laminated-horn.md` |
| **7 Dec 2026, 23:59 CET** | Amsterdam Light Festival Ed. 16 call closes | fixed | owner R10; the festival's FAQ |
| 6 weeks before the debut | US Park Police alcohol permit, if the debut is at Fort Mason (was 8 Dec for 19 Jan) | moves with the date | bar `DEBUT-ROOM.md` |
| **31 Dec 2026** | HIGH END Vienna's Start-Up Area closes; it needs a registered company | fixed | owner R5, R9 |
| February–March 2027 | The listening room / pop-up: **planned, not funded** (Vacant to Vibrant's matching takes 2–6 months) | planned | bar `r43/V2V-APPLICATION.md` |
| Mid-February | Prototypes photographed: the first pictures that aren't renders | planned | lamps `first-articles.md` |
| 8 Feb | Fuorisalone's package (€2,000 + VAT) due | fixed | coordinator's calendar facts |
| **12–18 April** / **13–18 April** | Milan Design Week (Fuorisalone) / Salone del Mobile and Euroluce. **Both are right; name which** | fixed | owner R5, R9 |
| Tue 27 April – Thu 27 May | The lamps' Kickstarter | **proposal**, owner pending | brand `kickstarter/README.md` |
| **6–9 May 2027** | HIGH END, Vienna | fixed | owner R5 |
| 25 Nov 2027 – 16 Jan 2028 | Amsterdam Light Festival Ed. 16 | fixed | the festival's FAQ |

## Prices (all owner-pending; nothing is public: the site says "Set at launch")

| Product | Planned (deck) | R4 recommends | R4 Founders' Edition | Source |
|---|---|---|---|---|
| Tropos, a pair | **$19,000 (planned)** | $32,000 | $42,000, 8 pairs (one a tint) | deck; owner `R4:21`; the owner's round-14 decision of $19,000 (README:2502) |
| Mantle | [deck figure] | $9,500 | $12,500, 8 units | owner `R4`, `R9:13` |
| Hemisphere | $1,200 | $1,200 | $1,700, 8 a tint | owner `R4:23` |
| Core | $750 | $750 | $1,100, 8 a tint | owner `R4:24` |

**Superseded (don't use):** Core $650 and Hemisphere $795–895 (lamps `PARTICULARS.md`); Mantle "about $5,000" (owner
`YC-W27-application-draft.md`).

## Sizes and weights (design figures until measured)

| Product | Of record | Source |
|---|---|---|
| **Tropos** | 1293 mm tall; 625 mm wide at the horn, 560 at the cabinet; 423 deep. **About 72 kg; 62 kg with the horn lifted off** (the horn lifts off with its compression driver, 3.6 kg, and adaptor, 0.65 kg; the acrylic horn alone is 4.1–5.7 kg). Precisely: 71–73 kg with the horn, by route; 62–63 kg without (horn lane 858fa0c1). Cabinet 20 mm (the first pair: 19 mm stock 2064). FaitalPRO 15PR400 woofer; B&C DE1085TN 2-inch driver; Hypex FusionAmp FA122, 2 × 125 W; crossover 1 kHz. **Horn:** the first pair's is **laminated, 22 layers of 1/2 in**; production's route is the owner's | site `web.py:126`; brand `press/tropos.md`; horn `make/laminated-horn.md:22,35`, `stock-pair.md:12` |
| **Hemisphere** | 200 mm across; about 1.6 kg hanging; 2700 K, CRI 90; **about 575 lm** (590 at the LED, about 500 out of the shade; lamps aa78e0c7). 1,100 lm was the original spec and isn't supported on the low top that was built | owner README:135; lamps `companions/README.md` |
| **Core** | 160 mm ball, 180 mm tall; **about 1.46 kg** ("about 1.5 kg" in public copy; lamps aa78e0c7, from the current CAD; 2.0 and 2.2 kg were older rounds); **4.7 h** at full brightness at the 90% limit (5.2 h from full, 5.8 h at the bar setting). Public copy: "about five hours" | lamps `first-articles.md`, README round 42; site `web.py:166-168` |
| **Mantle** | 470 × 380 × 194 mm, lid down; about 15.5 kg; Rega RB330 arm; first build with a 2M Blue (the 2M Black for the show unit is open) | brand `press/mantle.md`; lamps `mantle-drive.md:74` |

## Mother EARF, as designed

- **The object:** six slotted discs of 25 mm cast acrylic. Three meridians (green, orange, violet) and three parallels
  (red, blue, yellow), axis at 23.4°, cemented clear where they cross, the rims glowing.
- **Size and cost:** **1.25 m, about 190 kg**, about $9–12k.
- **Colour:** multicolour, the owner's choice of 2026-10-22.
- **Variants:**
  - a **2 m** festival version is **under study** (about 245–485 kg before ballast; figures to confirm);
  - 4 m is an idea drawing only;
  - the 300 mm desk globe is a separate shop item.
- **Not** a sphere, and no continents.
- **Sources:** bar `planet/README.md:339-373`, `r42/housebook/index.html:352`; brand `festival/amsterdam/`.

## Money: the deck's $50,000 use of funds (as now in the deck)

| Line | Amount |
|---|---|
| Tropos (the prototype pair) | $18,500 |
| Hemisphere, Core and Mantle (one of each) | $14,400 |
| Tropos testing | $5,000 |
| Trademarks | $3,600 |
| The debut (crating, transport, photographs) | $4,000 |
| Contingency | $4,500 |
| **Total** | **$50,000** |

- An older split is recorded in owner README:139 ($19,200 / $10,400 / $8,000 / $3,600 / $2,000 / $4,000 / $2,800).
  **Superseded.**
- **Costs of record:**
  - BOMs: Tropos parts $9,577; Hemisphere $4,572; Core $2,027; Mantle $3,815.
  - Tropos prototype pair to 18 January: **about $18,520**, or about $21,300 with contingency (horn `make/schedule.md:102`).
  - Lamps and Mantle to 18 January: **about $15,500** (lamps `first-articles.md:175`).
  - Both run over their lines: see `CONTRADICTIONS.md`.

## Still the owner's to decide

1. **Prices**, all four, and Tropos above all ($19,000 against R4's $32,000).
2. **The horn's production route:** laminated (no tool) or formed over a tool (about $14,500–15,000). This decides what
   the public copy says.
3. **The first-run programme:**
   - the Founding Hundred, as on the site (a number, no money);
   - or deposits (the money pack);
   - or R4's Founders' Edition of 8 pairs.
   Counsel follows.
4. **Hemisphere's first listing:** the plug-in swag (UL 153) or hardwired (UL 1598). The site says 1598.
5. **The debut:** **the date and the venue** (spring 2027; the owner's next question); the room; the lighting version; alcohol through a USPP permit (6 weeks ahead) or zero-proof.
   Where the room, the lamps and the photographs come from, beyond the $4,000 line.
6. **The money gaps:** lamp testing ($18–46k across all four, before sales); the February photo day; the lamps' and
   Tropos's overruns.
7. **Company formation**, which Vienna's Start-Up Area (31 Dec), Kickstarter and the deck's terms need.
8. **Matched or stock tints** for the first run; the 2423 / 2064 stand-ins until then.
9. **Planet EARF named in public**, or not.
10. **Session 00:** the artist, the fee, Ember or Smoke vinyl, $40 or $50.
11. **Amsterdam:** the title, six colours or eight, 2 m or 1.25 m.
12. **The Kickstarter:** the dates, the goal (about $110k est.), the tiers.
