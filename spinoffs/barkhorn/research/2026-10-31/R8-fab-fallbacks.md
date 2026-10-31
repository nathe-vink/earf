# R8: Fabrication fallbacks for the first Tropos pair

**Status:** research memo from public web pages only, checked 31 Oct 2026. Nobody was contacted, no forms were submitted and no accounts were created.

**Scope:** routes that do not depend on the 13 shops already asked. This memo builds on:
- **R7**, which covers bonding shops, 5-axis CNC and the basics of in-house bonding;
- **R1**, which covers TruCast stock and colours.

Neither is repeated here except where needed.

**Conventions**
- **[E]** marks an estimate, my arithmetic or a judgement call.
- **[U]** marks something I could not verify on the source page itself, including claims seen only in a search-engine summary.
- Text in "double quotes" is the source's own wording.

**The part, for reference**
- 22 layers of ½" (12.7 mm) TruCast 2423 or 2074.
- Each layer outline is up to 630 × 366 mm (24.8 × 14.4 in). A pair needs 44 layers.
- Nominal stack height is 279 mm before glue lines.
- About 9–10 layer blanks fit on one 48 × 96 in sheet, so a horn needs about 3 sheets [E].

---

## Bottom line

1. **Cutting is not the bottleneck.** Five routes not yet asked can cut 44 layers from EARF's own TruCast in 1–3 weeks: Ace Makerspace's 100 W laser (class 17 Nov), Pololu (online, takes customer acrylic up to 1"), Neal's CNC (Hayward, 5 × 10 ft router), Acrylic Art (Emeryville) and Atlas Contour (SF).
2. **The big online services don't fit.** SendCutSend cuts ½" in clear only and won't take customer sheet; Ponoko stops at 12 mm; Protolabs caps PMMA at 10 × 7 × 2.75 in; OSH Cut cuts metals only; Big Blue Saw is now Xometry, whose instant acrylic quotes stop at 0.254".
3. **Best DIY base:** Ace Makerspace in Oakland ($200 a month, 24/7, small-business use allowed within limits), with Maker Nexus in Sunnyvale ($160 a month, no tool fees) as a second laser.
4. **No Bay Area makerspace has 5-axis.** Autodesk's Pier 9 centre is a research residency, not a route for January.
5. **Bonding and annealing are the real schedule risk.** Run an in-house track in parallel: ~$1.5–3k kit [E] plus a $6,500 forced-air oven that holds one horn; ~3–5 weeks per horn [E].
6. **Use dead weight on spacers, not a vacuum bag.** Röhm says the cement "will foam" below about 0.2 bar absolute.
7. **The four failure modes have documented fixes (Röhm/ACRYLITE):** degas gently and heat at ≤10 °C/h (bubbles); anneal cut layers <24 h before bonding (crazing); test 2423/2074 coupons and tint the cement (colour bleed); dowel holes cut with the outline, no brass pins (misalignment).
8. **Proof:** Tannoy patented this exact horn build in MDF (twelve 35 mm rings glued, then CNC-machined). LA artists Norman Zammitt and Vasa have laminated coloured acrylic since the 1960s. No maker of laminated *acrylic* horns was found [U].
9. **Missed specialists to email:** Acrylic Art, Atlas Contour/Gizmo, Neal's CNC and Piedmont (Union City) in the Bay Area; Acrylic Concepts and OCIP in Southern California.
10. **Monday 2 Nov:** book Ace classes (Shop Basics 5 Nov, laser 17 Nov); order TruCast cut to 48 × 36 in plus a coupon-trial kit; send the DXFs to Pololu, Neal's CNC, Acrylic Art and Atlas Contour for quotes.

---

## Ranked options

| # | Option | What it covers | Cost | Lead time | Confidence |
|---|---|---|---|---|---|
| 1 | **Ace Makerspace**, Oakland (DIY) | Laser-cut all 44 layers on a 100 W laser with a 1300 × 900 mm bed. The 4 × 8 ft router can cut the 19 mm cabinet panels. Small-business use is allowed | $200/mo. Classes: laser $65, Shop Basics $18.50, router $95. Laser $0.50 per minute of firing, about **$220–430 for 44 layers** [E]. Router $6/h or $50/day | Laser from **17 Nov** (4 seats left). Router from **5 Dec**. About 7–14 h of laser time [E] | **Medium.** 100 W is slow on 12.7 mm, so test first; the machine is shared |
| 2 | **In-house bonding and annealing** (§D) | Coupon trials, laminating, annealing, one horn at a time | Kit and gear **~$1.5–3k** [E]. Oven **$6,500** (Despatch DOL-69A, holds one horn), or a used convection oven ~$1–3k [E] | Kit in about 1 week [E]. **3–5 weeks per horn** [E] | **Medium-low** on a first attempt; better after coupons |
| 3 | **Pololu**, Las Vegas (online laser) | Cuts **EARF-supplied** acrylic up to 1" thick, on material up to 48 × 48 in | 3 mm acrylic from $0.15 per inch of cut; thicker "costs more". About **$3–7k for 44 layers** [E]; needs a quote | Quote, ship sheet, cut; same-day rush is offered. About 1–2 weeks overall [E] | **Medium** |
| 4 | **Neal's CNC**, Hayward | Router-cut layers and cabinet panels on a 5 × 10 ft bed; also laser | Quote. Bay Area router time ~$100–175/h, so ~$0.7–2k [E] | Not published [U]; ~1–2 weeks [E] | **Medium-low.** Customer-sheet policy not stated |
| 5 | **Acrylic Art**, Emeryville | Acrylic specialist, "over 34 years". Has CNC routers, laser cutters and thermoforming. Takes one-offs and museum work. Could cut layers, build cabinets, perhaps bond | Quote | [U] | **Medium-low.** Strong fit; bonding method unknown |
| 6 | **Atlas Contour** (linked to Gizmo), SF | Laser, waterjet, plasma and CNC router, including 5-axis routing. EARF may supply the sheet | Quote | "quick turnarounds" [U] | **Medium-low.** No specs published |
| 7 | **Maker Nexus**, Sunnyvale (DIY) | Second laser capacity: two 100 W lasers (24 × 40 in and 700 × 500 mm beds) and a 4 × 4 ft ShopBot router | $160/mo; "never charge a fee for time spent using any tools". Classes are 1–4 h | Class dates [U]. Open 10 am–10 pm daily | **Medium** |
| 8 | **Piedmont Plastics**, Union City | Sheet stock plus custom cutting on a 3-axis router and CNC panel saw | Quote | [U] | **Medium-low.** Its CHEMCAST sheet is not the TruCast colour (R1) |
| 9 | **ePlastics**, San Diego | Sells 2074 ½" and does CNC and laser work to quote | 2074 ½" 48 × 96 sheet: $636.90 each (1–2), $555.84 (3–9). Fabrication minimum $200 | [U], plus 1–3 days freight [E] | **Medium-low** |
| 10 | **SendCutSend** | **Clear** ½" cast parts only, for a full-size rehearsal or dry-fit stack | Instant quote [U] | 2–4 days plus shipping | **High** for clear; **none** for colour |
| 11 | **Noisebridge**, SF (DIY) | Backup 100 W laser | Free entry. $10 per use or per hour. Training is pay-what-you-can, about $20 suggested | Weekly training | **Low-medium** |
| 12 | **Xometry** (includes former Big Blue Saw) | Thick acrylic by manual review; CNC-machined acrylic | Quote | Sheet cutting: standard 3 business days. CNC: from 3 days | **Low** for TruCast colours |

**Ruled out:**
- **Ponoko:** no ½", and it does not take customer sheet.
- **Protolabs:** PMMA is capped at 10 × 7 × 2.75 in.
- **OSH Cut:** metals only.
- **Acme Plastics:** "no customer-supplied material" [U]; its site returned 403.
- **Autodesk Technology Center:** a research residency on the wrong cycle.
- **The Crucible and Hacker Dojo:** no laser or CNC found.

---

## A. Cut-to-DXF services for ½" cast acrylic

### A.1 What matters for this part

**Edge finish: laser or router**
- **Laser:** gives a glossy, "flame-polished" edge, but on 12.7 mm the edge tapers slightly [E] and carries thermal stress.
  - ACRYLITE recommends "annealing acrylic sheet after laser cutting" ([property sheet](https://www.acplasticsinc.com/media/Acrylite%20Premium%20Properties.pdf), [U]: seen in a search summary).
  - US Plastic: "Preliminary annealing before cementing will eliminate or reduce stresses present in machined or saw cut areas… Annealing should be done less than 24 hours before cementing" ([SC-125](https://www.usplastic.com/catalog/files/charts/SC-125.pdf)).
- **Router:** gives square, matte edges that stack more accurately [E].
- Either way, the faces are what get bonded, and those stay as cast.

**Sheet size to order** [E]
- Order TruCast **cut to 48 × 36 in**. The A&C Plastics page for 2423 ½" offers cut-to-size ("We can perform cut-to-size orders with tight tolerances of 1/32 inch"). It shows $835.80, "In Stock" in Houston, TX, and out of stock in Illinois and Colorado ([A&C 2423 ½"](https://www.acplasticsinc.com/product/2423-500-48x-96-trucast-p-2/)).
- 48 × 36 in fits Ace's 1300 × 900 mm laser bed and Pololu's 48 × 48 in limit, and holds about 3 blanks.
- Full 4 × 8 sheets suit routers with 4 × 8 or 5 × 10 beds.

**Registration** [E]
- Put 3–4 dowel holes in every layer's DXF, in waste or hidden areas, cut in the same program as the outline (see §D.4).

**Price check** [E]
- The full-size red (TruCast 2423) costs **$835.80 per 48 × 96 sheet** (A&C, checked 31 Oct). Dark grey 2074 ½" is $569.80 (R1). Allow about 3 sheets per horn plus one spare.

### A.2 Online services

| Service | ½" acrylic? | Colours at ½" | Max part / sheet size | Edge | Price signal | Turnaround | Takes customer sheet? | Would take a 22-layer job? |
|---|---|---|---|---|---|---|---|---|
| **SendCutSend** ([acrylic](https://www.sendcutsend.com/materials/acrylic/), [sizes](https://www.sendcutsend.com/materials/min-max/), [FAQ](https://sendcutsend.com/faq/can-you-cut-material-i-ship-to-yo/)) | Yes: .500" (12.7 mm), "cast acrylic only", laser | **Clear only.** Colours (incl. "Red 2423", "Dark Gray 7074") are ".118″ thickness only" | 44 × 30 in (min 1 × 1 in at ½") | "smooth, flame-polished edges"; ±.009" | Instant online quote [U] | "2-4 days" production | **No:** "does not cut or process raw material that is shipped to us from customers" | Yes for clear. **Use: a rehearsal stack only** |
| **Pololu** ([materials](https://www.pololu.com/docs/0j24/5), [capabilities](https://www.pololu.com/docs/0j24/1), [pricing](https://www.pololu.com/docs/0j24/2), [design](https://www.pololu.com/docs/0j24/4)) | Yes: acrylic up to **1" (25.4 mm)** | Any you send. Its supplier list includes TAP, ePlastics, eStreet and Delvie's | Layouts up to 47.5 × 47.5 in on material up to 48 × 48 in. Customer sheet "should not be longer than 48"" | "laser-polished edge"; kerf ~0.007–0.010" | 3 mm acrylic from $0.15 per inch of cut; thicker "costs more"; masking extra. ½": ~$70–170 per layer [E] | Rush "up to same-day service" | **Yes:** say so in the quote form and wait for the quote before shipping | Yes [E]. **Best online fit** |
| **Ponoko** ([acrylic](https://ponoko.com/laser-cutting/acrylic), [custom material](https://help.ponoko.com/en/articles/4468203-custom-material-orders)) | No: custom sheets 0.1–12 mm, and "Most materials over 9mm thick won't cut through" | Stock "Red Translucent" and "Gray Translucent" at thinner gauges | Not stated for acrylic | Not specified | "Parts start from $50"; custom-material fee $150–500 | Custom material adds 1–3 weeks. Same-day Bay Area delivery for some stock items | **No:** "we do not accept custom materials direct from our customers" (it sources them itself) | No |
| **Xometry**, incl. Big Blue Saw ([acrylic laser](https://www.xometry.com/capabilities/sheet-cutting/acrylic-laser-cutting-service/), [sheet](https://xometry.com/capabilities/sheet-cutting), [CNC acrylic](https://www.xometry.com/capabilities/cnc-machining-service/acrylic/)) | Instant laser quotes: clear 0.100–0.254" only. "Thinner or thicker stock may be possible through manual review" | "We will source it!" via a "Custom" material request | "Platforms up to 10' x 20'" | "flame-polished or frosted" | Quote | Sheet: "3 business days". CNC acrylic from 3 days | Not stated [U] | Possibly, by manual quote [U] |
| **Big Blue Saw** | bigbluesaw.com now redirects to xometry.com. Xometry bought Big Blue Saw's assets on 1 Nov 2021 for $2.5 M ([Xometry](https://investors.xometry.com/news-releases/news-release-details/xometry-integrates-big-blue-saws-software-data-laser-waterjet); [DC360](https://www.digitalcommerce360.com/?p=1010376)) | — | — | — | — | — | — | — |
| **Protolabs** ([extents](https://www.protolabs.com/services/cnc-machining/cnc-machining-maximum-extents/)) | CNC only; PMMA max "10 in. x 7 in. x 2.75 in." | — | Too small | — | — | — | — | No |
| **OSH Cut** ([materials](https://oshcut.com/materials)) | No: metals only ("steel, stainless, aluminum, copper, brass, bronze, and nickel") | — | — | — | — | Standard about 3 business days | — | No |
| **ePlastics**, San Diego ([fabrication](https://www.eplastics.com/plastic-fabrication)) | Yes: in-house CNC ("half-dozen CNC machines") and laser | Sells **2074 ½"** 48 × 96 at $636.90 (1–2) or $555.84 (3–9) (R1 saved page). 2423 ½" not confirmed [U] | Not stated | "Edge Polishing" offered | "minimum order size of $200" | Not stated [U] | Not stated [U] | Likely [E]. Email info@eplastics.com with drawings |
| **Acme Plastics** ([laser](https://www.acmeplastics.com/laser-cutting), returned 403) | Laser "up to .5"" with 1/64" tolerance; routing on sheets up to 5 × 10 ft [U] | Not checked | — | — | "no minimum" [U] | Next-day quote [U] | **No** customer-supplied sheet [U] | Only from its own stock [U] |
| **Delvie's Plastics** ([laser](https://www.delviesplastics.com/c/custom-laser-cutting.html)) | Thickness limit not stated | Its own colours | — | — | Free quote | — | Not stated | [U] |

**Takeaway:** for coloured ½" TruCast, the only proven online route is **Pololu with EARF's own sheet**. Use **SendCutSend clear** for a cheap rehearsal of DXF fit, registration and bonding: it cuts cast acrylic, so it behaves like the real sheet [E].

### A.3 Bay Area laser and router job shops

None of these are on the already-asked list. R7 also lists **Control Plastics** (Menlo Park), **AC Manufacturing** (San Jose), **AJ Solutions** (Fremont) and **Gemmiti** (SF) for machining.

| Shop | What it has | Acrylic and thickness | Customer sheet? | Lead time / price | Contact |
|---|---|---|---|---|---|
| **Neal's CNC**, 1414 & 1424 W. Winton Ave, Hayward 94545 ([site](https://www.nealscnc.com/)) | CNC router with a **5' x 10'** bed, "one of the largest cutting beds in the industry". Also laser cutting and etching; waterjet through a partner | Lists "Acrylic/Plexiglas" for both CNC and laser. Thickness not stated | Not stated [U] | Not stated [U] | 510-783-3156; service@nealscnc.com |
| **Acrylic Art**, 1290 45th St, Emeryville 94608 ([site](https://www.acrylicart.com/); [capabilities](https://www.acrylicart.com/2024/05/14/the-art-and-precision-of-plastic-fabrication-at-acrylic-art/)) | "CNC routers, laser cutters, and thermoforming equipment". "specialists in close tolerance plastics fabrication and CNC machining", "for over 34 years" | Its main material | Not stated [U] | Takes "a one-of-a-kind display piece, a prototype". Quick-quote and RFQ forms | 510.654.0953; 800.479.1278; INFO@ACRYLICART.COM |
| **Atlas Contour**, San Francisco ([home](https://www.atlascontour.com/), [contact](https://www.atlascontour.com/contact)) | "LASER CUTTING - WATER JET - PLASMA CUTTING - CNC ROUTER". The home page also claims 5-axis CNC routing and almost 10 years serving the Bay Area | Not stated | **Yes:** the quote form asks whether you need Atlas to provide materials | "quick turnarounds", "projects of any size" [U] | info@atlascontour.com. Gizmo Art Production lists it as "For Cutting Services Only" ([Gizmo](https://gizmosf.com/)). No street address |
| **Piedmont Plastics** "San Francisco" branch, 33340 Central Ave, Union City 94587 ([branch](https://www.piedmontplastics.com/locations/san-francisco)) | "CNC panel saw, 3-axis router, and CNC upcut rod saw"; custom cut; fabrication | Stocks CHEMCAST (R1/R6) | [U] | [U] | 510-746-2200 |
| **TAP Plastics**, Bay Area stores ([fabrication](https://www.tapplastics.com/product_info/plastics_information/custom_fabrication), returned 403) | A search summary says "TAP Fabrication delivers precision with their computer-driven laser, router, and beam saw" [U] | Sells CHEMCAST colours (R1) | [U] | [U] | Use a store |
| **Automatic Arts**, San Leandro ([site](https://www.automatic-arts.com/)) | Now says it "no longer provides cutting and fabrication services" and refers that work to Neal's CNC | — | — | — | — |
| Directory-only leads [U] | Pagoda Arts Laser Cutting (SF) and Laser Alliance LLC (464 S Hillview Dr, Milpitas) ([guide](https://steampunk-explorer.com/city-guides/san-francisco-bay-area/arts-and-crafts)). A machine-share listing shows a "Boss Laser 150W HP-2436" in Oakland ([you3dit](https://www.you3dit.com/machine_tags/acrylic)) | — | — | — | — |

**Rough price for router cutting:** about 10–15 min per layer, so 7–11 h for 44 layers. At typical $100–175/h that is about $0.7–2k for the pair, before edge work [E].

---

## B. Makerspaces and shared shops

| Space | Laser of 100 W or more | Router with bed ≥ 4 × 4 ft | 5-axis | Price | Training / sign-off | Hours | Commercial work |
|---|---|---|---|---|---|---|---|
| **Ace Makerspace**, 6050 Lowell St #214, Oakland ([home](https://www.acemakerspace.org/)) | "AMT266 Barracuda", "100w CO2", "1300mm x 900mm x 66mm bed"; ".50¢ a min. (firing time only)" ([wiki](https://wiki.acemakerspace.org/laser-cutting/)). About 4 blanks per load [E] | "AMT375 48 x 96 Forest Scientific HSR CNC Router" ([certs](https://wiki.acemakerspace.org/tool-certifications/)). Fees: "1 hour or less = $6", "Half Day – 5 hours = $25", "Full day – 5 to 10 hours = $50" ([fees](https://wiki.acemakerspace.org/?p=15425)) | None | **$200/mo or $2,000/yr** ([membership](https://www.acemakerspace.org/membership/)). Individual memberships only | **Laser:** $65, 3 h, then an online check. Dates Nov 3 (sold out), **Nov 17**, Dec 1, Dec 15, 4 seats each ([class](https://acemakerspace.org/?p=192214)). **Shop Basics:** $18.50, 1 h; **Nov 5 (1 seat left)**, Dec 3 ([class](https://acemakerspace.org/?p=192230)). **Router:** $95, 5 h, needs Shop Basics; **Sat Dec 5**; minimum 3 students ([class](https://www.acemakerspace.org/?p=224017)) | **24/7** for members | **Allowed within limits:** "Ace members can run small businesses out of Ace as long as their use does not exceed the Ace offering"; "If a small business operator needs to have space say 5 days of the week, it is time for them to rent their own space" ([FAQ](https://wiki.acemakerspace.org/?p=16022)). "Prolonged commercial use" needs a larger contribution agreed with staff ([fees](https://wiki.acemakerspace.org/?p=15425)) |
| **Maker Nexus**, 1330 Orleans Dr, Sunnyvale ([home](https://www.makernexus.org/)) | "100W BossLaser LS2440 bed is 24 x 40 inches"; "100W Red Laser bed is 700mm x 500mm"; also a 45 W Epilog ([tools](https://www.makernexus.org/facilities-and-tools)). About 1 blank per load [E] | "a 4'x4' ShopBot CNC router" | None | **Hobbyist $160/mo**; student $100 | "Basic safety classes usually last 1-4 hours on a single day"; members get 30% off ([FAQ](https://www.makernexus.org/faq)). Dates and prices [U] | **10 am–10 pm daily**; closed on major holidays | Selling work is fine ("Many of our members sell their work"), but it "isn't set up for volume manufacturing". "We never charge a fee for time spent using any tools" |
| **Noisebridge**, 272 Capp St, SF ([home](https://www.noisebridge.net/)) | "Kaitian CM1309 100W". "$10 per use or per hour of cutting time"; training pay-what-you-can, $20 suggested ([laser](https://www.noisebridge.net/wiki/Laser_Cutter)). An undated Meetup post says it was upgraded to 150 W with a 3 × 4 ft bed [U] | None found | None | Free entry; donations | Must be trained by an official trainer. The home page says Wednesdays 2–4 pm; the laser page says Sundays | Mon–Thu 2–10 pm; Fri–Sun 11 am–midnight | Not stated [U] |
| **Hacker Dojo**, moving to 3200 Patrick Henry Dr, Santa Clara ([pricing](https://hackerdojo.org/pricing/)) | Not named. The page lists only "Hardware Labs with maker tools and 3D printing" [U] | Not named [U] | None | $150/mo or $1,350/yr | [U] | 24/7 | Not stated |
| **The Crucible**, 1260 7th St, Oakland ([Wikipedia](https://en.wikipedia.org/wiki/The_Crucible_(arts_education_center))) | No evidence. Its site showed only page titles | No evidence | None | [U] | Classes, e.g. machine shop [U] | [U] | [U] |
| **Sun Gallery makerspace**, 1015 E St, Hayward ([page](https://sungallery.org/makerspace/)) | OMTech 100 W, 20 × 28 in | None | None | Memberships planned; free use available | [U] | Fri–Sat 11 am–4 pm | [U] |
| **Idea Fab Labs**, Santa Cruz ([2015 article](https://www.santacruztechbeat.com/2015/03/19/new-makerspace-opening-santa-cruz/)) | In 2015: 100 W, 55 × 35 in | In 2015: 4 × 8 ft router | — | In 2015: $114–120/mo with CNC | — | — | Data is from 2015 [U] |

**Autodesk Technology Center, San Francisco (Pier 9)**
- **Status:** still described at Pier 9 on the Embarcadero (page footer "© 2026") ([tours](https://technologycenterstours.autodesk.com/san-francisco)).
- **Residency:** on 12 May 2026 Autodesk restructured its **Research Residency Program**. It now has an Academic Research Cohort and an Industry Research Network, with prototyping at its San Francisco and Boston centres ([Autodesk Research](https://www.research.autodesk.com/?p=7326)).
- **Application windows** [U]: the programme page returned 403. Search summaries say Industry Research Network applications closed on 1 Aug 2026, with a proposal window of 1 Oct 2026 to 1 Jan 2027.
- **Verdict:** a research programme, not a production route for January 2027 [E].

**5-axis access** (§2 of R7 has the full list):
- No Bay Area makerspace was found with 5-axis.
- The only new 5-axis lead in this memo is **Atlas Contour**'s 5-axis routing (§A.3).

**Practical DIY plan**
- Join Ace now and take Shop Basics on **5 Nov** (1 seat left) or 3 Dec, the laser class on **17 Nov**, and the router class on **5 Dec**.
- If laser time at Ace is contested, add Maker Nexus.
- Do the bonding in EARF's own space, not in a shared one: the cement vapour needs floor-level extraction (§D.5) [E].

---

## C. Bay Area and California acrylic specialists not yet asked

R7 §1.2 already covers Gizmo, Acrylonics, Crystal Craft, CalAquaria, Factory Fish Tanks, Custom Acrylics, Cutting Edge Plastics and Envision. New names:

| Name | Evidence | Laminated or bonded blocks? | How to reach |
|---|---|---|---|
| **Acrylic Art**, Emeryville | Plastics fabrication and CNC "for over 34 years". Clients include "museum spaces"; one-off pieces and prototypes. Google rating 5.0 from 17 reviews ([site](https://www.acrylicart.com/)) | None published [U]. Ask about two-part cement, annealing and a 22-layer laminate | 510.654.0953; INFO@ACRYLICART.COM; RFQ form |
| **Atlas Contour / Gizmo Art Production**, SF | Gizmo builds "glass or acrylic vitrines" with "museum quality polished edges" (R7). Atlas cuts, including 5-axis | None published [U] | info@atlascontour.com; sales@gizmosf.com, 415-222-6181 |
| **Neal's CNC**, Hayward | Large-format router; trade-show and exhibit fabrication | No | 510-783-3156 |
| **Acrylic Concepts** (embedment.com), Van Nuys | Since 1983: "castings, including embedments and awards", "a full line of custom acrylic furniture", pedestals and sculptures. Does casting, routing, sanding and buffing ([Thomasnet](https://www.thomasnet.com/company/acrylic-concepts-30728370/profile)) | Makes **cast** thick blocks (embedments); lamination not stated [U] | (818) 901-8842 |
| **OCIP**, 4811 E La Palma Ave, Anaheim | Routing, laser, "solvent cements and bonding chemicals", capillary and dip cementing, flame polishing; "prototypes to high-volume orders" ([page](https://ocip.com/services/acrylic-services/)) | No | (844) 362-8799; online quote request |
| **Factory Fish Tanks** (R7; location unclear, 805 area code) | "Monolithic casting up to 20 inches (500mm+) thickness"; "Molecular Polymer Bonding"; museum vitrines ([home](https://factoryfishtanks.com/)) | **Claims** thick bonding and casting | (805) 813-8433; hello@factoryfishtanks.com |
| **Eric Zammitt**, artist, Los Angeles | Panels "made of tens of thousands of solid bits of boldly colored acrylic plastic", laminated, wet-sanded and polished; up to 59 × 59 in ([gallery](https://www.srcart.com/artists/eric-zammitt)) | **Yes:** coloured acrylic laminated by hand. Possible paid adviser, not a vendor [E] | Through Scott Richards Contemporary Art, 501 Pacific Ave, SF, (415) 788-5588 |

**Leads that went nowhere**
- **Kritter Tanks (Peninsula):** only 2006–07 forum mentions.
- **TruVu:** moved to Arizona around 2013 ([forum](https://www.nano-reef.com/forums/topic/419120-micro-reefs-aquariums-short-bio-how-when-why-did-we-become-who-we-are-today/); search summary [U]).
- **Weldon Exhibits** (San Rafael area): an exhibit fabricator; acrylic work not shown [U].
- **No California shop advertises annealing-only service.** Ask Acrylic Art, Piedmont or OCIP [U].

---

## D. Do-it-yourself bonding plan for one horn

**Chemistry.** Use **Weld-On 40**: US stock, 100:5 mix, and documented for this use. **ACRIFIX 2R 0190** is the alternative with the most detailed method (Röhm's guideline 311-3), but its US supply is thin.

**Main sources:**
- Röhm/Polyvantis *Joining PLEXIGLAS®* 311-3, 07/24 ([PDF](https://www.plexiglas.de/files/plexiglas-content/pdf/verarbeitungsrichtlinie/311-3-EN-joining-PLEXIGLAS.pdf)), read in full on 31 Oct.
- ACRYLITE reactive-cement brief 1591E, 08/24 ([PDF](https://www.acrylite.co/files/content/acrylite.co/documents/fabrication-briefs/ACRYLITE-Reactive-Cement-Fabrication-Brief.pdf)).
- ACRYLITE annealing page ([page](https://www.acrylite.co/resources/fabrication-manuals/annealing-acrylite-acrylic-sheet)).
- The Weld-On 40 product page ([ePlastics](https://www.eplastics.com/ips40-pt)).

R7 §1.4 holds the strength data and exposure limits.

### D.1 Equipment and consumables

| Item | Why it's needed | Example, with live price | One-horn cost [E] |
|---|---|---|---|
| **Weld-On 40** cement | Two-part polymerising cement | Gallon kit **$197.77** (1–3), "LIMITED AVAILABILITY" ([ePlastics](https://www.eplastics.com/plexiglass/acrylic-accessories/ips40-gal)). $202.29 each when bought in 4s; in stock ([Chemical Concepts](https://www.chemical-concepts.com/product/weld-on-40-reactive-acrylic-adhesive/)). Pint kit **$46.71** ([ePlastics](https://www.eplastics.com/ips40-pt)) | 1 gallon plus 2–3 pints for coupons: **~$300–350**. R7 estimates 1.2–5.8 L per horn |
| or **ACRIFIX 2R 0190** with CA 0020 hardener | The Röhm system; colourants and moderator are documented | 110 g sample **$122.49**, hardener not included ([ibspot](https://ibspot.com/products/acrifix-2r-0190-versatile-110-grams); search listing [U]). Bulk US price [U] | — |
| Degassing pot and pump, **plus a bleed valve and gauge** | Removes mixing bubbles. Röhm: absolute pressure "must never fall below" about 0.2 bar, or the cement "will foam due to evaporating monomer" | VEVOR 5-gallon chamber with 3.5 CFM pump **$159.99** ([Home Depot](https://homedepot.com/p/VEVOR-5-Gal-Vacuum-Chamber-and-3-5-CFM-Pump-Kit-Tempered-Glass-Lid-Vacuum-Degassing-Chamber-Kit-with-250-ml-Oil-Bottle-MCKDZKBT3CFM5YVRLV1/324369894); search listing [U]). Stop at about −0.8 bar (about −23 inHg) on the gauge [E] | ~$200–230 |
| Scale, beakers, stirrers, syringes | ACRYLITE: scale accurate to about 1 g; beakers of glass or polyethylene. Röhm: polyethylene, polypropylene or polyamide syringes | Lab scale, PE/PP beakers, glass rods | ~$100–200 |
| **Spacers and dams** | Röhm: hold heavy layers "about 0.5 to 1.5 mm from the base panel by suitable elastic spacers such as polyethylene cords". ACRYLITE: polyester tape to contain the cement | About 1 mm PE cord or PE/PTFE shims; polyester tape; PE film | ~$60–120 |
| **Registration** | Keeps 22 layers aligned on wet cement | 3–4 stainless or acetal dowels per layer. **No brass or copper:** Röhm says they hinder curing | ~$50–100 |
| **Press** (dead weight, not a vacuum bag) | Weld-On: "Use only enough pressure to remove air bubbles", or the joint is starved. ACRYLITE: clips, clamps or weights | Flat, level table topped with melamine or glass, with stops so layers can't slide (Röhm Fig. 15); steel plates or sandbags | ~$150–400 |
| Polariscope | Röhm: inspect parts "between two polarizing sheets" to see stress | Two polarizer sheets | ~$20–40 |
| **Annealing oven** | Forced air, 150–250 ft/min, held within ±10 °F (ACRYLITE). "A restaurant oven can work" if it circulates air and controls temperature accurately | **Despatch DOL-69A, $6,500.** Inside 762 × 457 × 559 mm; forced air; ±3 °C at 150 °C; 120 V 21.6 A, hard-wired ([Gilson](https://www.globalgilson.com/standard-despatch-electric-oven-6-point-9ft-chamber)). Holds **one** finished horn per cycle | $6.5k plus wiring. A used convection oven is ~$1–3k but must be checked with a data logger [E] |
| **Protective gear** | Weld-On 40 data sheet: "NIOSH-approved organic vapor cartridge respirator with full face-piece is recommended" ([AC Plastics "Weld-On 40 Properties" PDF](https://www.acplasticsinc.com/media/Weld-On%2040%20Properties.pdf); [U]: search summary, the PDF returned 404). Röhm: avoid skin contact | 3M 6800 full facepiece **$159.12** ([Walmart](https://www.walmart.com/ip/16890833); search listing [U]). 6001 organic-vapour cartridges **$23.89/pair** ([Staples](https://staples.com/3m-organic-vapor-cartridge-white-2-pack-6001/product_422397); search listing [U]). Silver Shield 4H laminate gloves **$9.95/pair** ([Darley](https://shop.darley.com/product/silver-shield4h-chemical-resistant-hazmat-gloves-large/01t2E00000QZd7PQAT), checked). A case report says laminate gloves protect against MMA ([article](https://blogs.the-hospitalist.org/content/glove-choice-crucial-job-related-dermatitis)) | ~$250–350 |
| Floor-level extraction and fire safety | Röhm: vapours "are heavier than air", so extract at floor level; ventilation "must be explosion-proof" | Exhaust fan and duct, class-B extinguisher, closed waste bins | ~$300–800 [E] |

**Totals [E]:** about **$1.5–3k without an oven**, or about **$8–10k with the DOL-69A**. R7's fuller list comes to $2–5k and $9–13k.

**Shops that anneal:** none in California advertises an annealing-only service. Crystal Craft anneals heavy-gauge acrylic, but it is on the already-asked list (R7).

### D.2 Annealing rules

| Rule | Röhm 311-3 (GS / cell cast) | ACRYLITE |
|---|---|---|
| Temperature | GS: 80 °C | 180 °F (80 °C) |
| Soak | "thickness in mm divided by 3 is the annealing time in hours, but the minimum is 2 hours" | "one hour per millimeter of thickness" |
| Cool | thickness in mm ÷ 4 hours, at no more than 15 °C/h | thickness ÷ 4 (over 8 mm); take parts out below 140 °F |
| Bonded parts | anneal "within 24 hours of bonding"; heat "no faster than 10 °C per hour. Otherwise there is a risk of bubbles forming in the joint" | let parts "sit at least six hours to avoid bubble formation" first |

**Cycle times for this horn [E]:**
- **Cut layers, 12.7 mm:** Röhm about 4 h soak plus 3 h cool; ACRYLITE about 13 h plus 3 h. One working day either way.
- **Sub-stacks of 5–6 layers (~76 mm):** about 6 h ramp + 25 h soak + 19 h cool, so **about 2 days**.
- **Full stack (~290 mm):** **about 7 days** if the whole stack counts as solid, or about 2 days if the wall thickness (~60 mm) governs. R7 flagged this; ask Polyvantis which applies.

### D.3 Process and time, one horn

| Step | What to do | Time [E] |
|---|---|---|
| 0. Coupon trials (week 1) | Bond two-layer coupons of 2423 and of 2074 offcuts, with clear cement and with tinted cement. Anneal some at 70 °C and some at 80 °C. Check colour bleed, bubbles, how the glue line looks and yellowing (Röhm: yellowing "is more intense at higher temperatures") | 3–4 days |
| 1. Prepare layers | Check stress with the polariscope. Number the layers. Measure each layer's thickness, since cast sheet varies. Remove paper masking (ACRYLITE). Pre-anneal, then bond within 24 h (US Plastic SC-125) | 1 day |
| 2. Build sub-stacks (e.g. 6 + 6 + 5 + 5 layers) | For each joint: dam with polyester tape and lay PE cord spacers. Mix 100:5; pot life about 20 min at 75 °F. Degas no lower than ~0.2 bar absolute. Pour the cement "approximately one-third the distance" across the layer, then lower the next layer "starting from one edge" onto the pins (ACRYLITE). Prick bubbles with fine stainless wire while the cement is liquid. Add the weights. Wait at least 3–4 h before the next joint: Röhm says 3 h; Weld-On gives handling strength at about 4 h. Keep the room at 20–25 °C and never below 15 °C (Röhm) | 2–3 joints per sub-stack per day, sub-stacks in parallel: **2–3 days** |
| 3. Anneal sub-stacks | After at least 6 h and within 24 h. Röhm's fault table cures "crazing within the adhesive" from "post-bonding of thick joints without annealing in between" with "Anneal after each bonding step" | ~2 days. A DOL-69A holds about 5–6 sub-stacks on shelves |
| 4. Join sub-stacks | Three joints, same method; cure 24 h. Röhm: "final bond strength after 24 hours" | 1–2 days |
| 5. Final anneal | Ramp at no more than 10 °C/h | 2–7 days |
| 6. Air path | Machine on 5-axis (R7 list or Atlas Contour) or fair by hand. Then anneal once more before any solvent touches it | 1–2 weeks plus 2–7 days |
| **Total** | | **~3–5 weeks per horn.** Both horns in parallel only if there is oven space: the DOL-69A holds one full horn |

**Glue lines raise the stack.** 21 joints at 0.5–1.5 mm add about 10–30 mm of height before shrinkage (R7). ACRYLITE puts shrinkage at "about 15 – 20% by volume". Adjust the profile spacing in CAD or plan to face the stack [E].

**Fallback if 5-axis time is unavailable [E, engineering idea].**
- Pre-contour each layer's inner edge on a 3-axis router with a ball-end tool before bonding, keeping cement off those edges.
- The stacked inner surface then needs only sanding at the glue lines.
- Check the effect of the steps acoustically before choosing this.

### D.4 Failure modes and how to avoid them

| Failure | Causes (per the sources) | How to avoid it |
|---|---|---|
| **Bubbles** | Röhm: "Entrapped air"; "Excess heat development during polymerisation (evaporating monomer)"; "Air sucked in by shrinking adhesive"; heating for post-anneal "too fast"; vacuum below ~0.2 bar absolute makes it "foam". ACRYLITE: "Uneven surface" | Degas gently with a bleed valve. Pour from one edge and close the layer from one edge (ACRYLITE). Keep the glue line an even 0.5–1.5 mm on PE cord. For layers thicker than 1.5 mm with ACRIFIX, add MO 0070 (≤0.3%). Prick bubbles with wire while liquid. Ramp ≤10 °C/h and wait ≥6 h before annealing. Bonding vertically is an option: "bubbles will rise to the top" (ACRYLITE) |
| **Crazing** | Röhm: "Stress in the material generated by machining"; "Local contact pressure too high"; "Cooling stress due to unskilful annealing"; thick joints bonded again without an anneal in between. ACRYLITE: "a flame-polished edge may craze when it contacts solvent cement". Laser edges carry stress (ACRYLITE [U]) | Pre-anneal cut layers less than 24 h before bonding (US Plastic) and check with polarizers (Röhm). Never polish or flame-polish a surface that will be bonded (ACRYLITE). Spread the weight evenly. Anneal sub-stacks before joining them. Cool at no more than 15 °C/h. Weld-On: anneal "following machining and forming" |
| **Colour bleed and stripes** | Röhm: "Adhesives may induce the colourants contained in coloured PLEXIGLAS® to bleed". Clear 0.5–1.5 mm glue lines show as pale stripes between tinted layers [E]. R1: 2423's transmission differs by maker (TruCast 14.1% vs CHEMCAST 49.85%) | Test coupons in the real sheet first. Röhm: transparent tints can use "all commercially available colourants soluble in organic solvents… provided they do not interfere with the polymerisation", for example MACROLEX. Colour "the required quantity of adhesive… in one go" and add hardener to small portions. Exact matching is "very difficult", so run trials. Buy all sheets from one maker and lot |
| **Misalignment** | Layers slide on wet cement; spacers uneven; holes cut separately from the outline | Cut dowel holes in the same program as each outline. The Tannoy GRF-R build used "computer-cut holes" for 10 mm dowels to "ensure 100% alignment of slices" ([build](https://hilberink.nl/codehans/tannoy127.htm)). Use stainless or acetal pins, not brass. Add stops so the top layer can't slide (Röhm). Check stack height after each joint |
| Others | Yellowing (Röhm: unavoidable, worse at higher anneal temperature). Slow cure below 15 °C. Warping from uneven moisture (Röhm: store parts unmasked for "1 week" or pre-anneal). Curing inhibited by "copper, brass, rubber, adhesive from adhesive tapes" | Anneal at 70–80 °C, chosen after the coupon trial. Keep the shop warm. Pre-anneal everything. Use only glass, stainless, PE or PP tools |

### D.5 Safety essentials
- Wear a full-face organic-vapour respirator and laminate gloves under nitrile, and extract at floor level. MMA vapour is flammable and heavier than air (Röhm).
- Store the cement and catalyst apart [E].
- R7 §1.4 has the exposure limits and the open question on BAAQMD air rules.

---

## E. Proof that stacked lamination works

| Maker / product | What it shows | Can it be a vendor? |
|---|---|---|
| **Tannoy**, US 8,213,658 B2 "Acoustical horn" (priority 2007, granted 2012) | The horn is "machined from a block of medium density fibreboard, itself made up of a number (here twelve) of 35 mm—thick layers 18 glued together"; "The layers each initially are ring-shaped, the aperture in each being smaller than the finished contour"; then "the block is sculpted by CNC machining" ([patent](https://patents.google.com/patent/US8213658B2/en)). **The Tropos method, in MDF** | No |
| **Tannoy GRF-R home build** (Andrew Tilsley) | 14 MDF slices of 32 mm, CNC-cut, with computer-cut dowel holes, glued in one session with PVA, clamped 24 h ([build](https://hilberink.nl/codehans/tannoy127.htm)). A related GRF corner-horn build used 36 layers [U] ([page](https://hilberink.nl/codehans/tannoy126.htm)) | No |
| **Magico Mini, Vapor Sound, early TAD** | 6moons: "By laying up routed-out slices of usually Nordic Birch ply, we get horizontal stripes." Its examples: "the original Magico Mini and Vapor Sound, even a few earlier models by TAD" ([6moons](https://6moons.com/?p=70594)). A search summary of The Absolute Sound says the Mini used "sixteen laminated layers of 17-ply Baltic birch" [U] ([TAS](https://www.theabsolutesound.com/articles/exotica-magico-mini-loudspeaker), returned 403) | No |
| **Kharma Exquisite EXQ-MD-3.0-S** | "high pressure laminate (HPL) in a multi-layer construction that is CNC machined", bonded in upright sheets ([TAS](https://www.theabsolutesound.com/articles/high-end-audio-buyers-guide-2024-kharma-exquisite-exq-md-3-0-s/)) | No |
| **Vasa (Velizar Mihich)**, Los Angeles | Work "built from carefully calibrated layers of colored transparent acrylic"; "pioneering explorations of cast acrylic sculpture" since "the late 1960s"; "He continues to work from his Los Angeles studio" ([Taylor & Graham](https://www.taylorandgraham.com/artworks/11712-vasa-velizar-mihich-cylindrical-column-1997)). A search summary quotes him on "laminating the plastic layers, machining, and polishing" [U] | Possibly as an adviser, through the dealer [E] |
| **Norman Zammitt** (1931–2007) | 1967–69: "Eventually Zammitt laminated thicker sheets to create a solid piece", and he is credited with developing **bubble-free lamination** methods. 1970–72: poles of solid-colour acrylic, "then laminated and polished" ([Wikipedia](https://en.wikipedia.org/wiki/Norman_Zammitt)). The NYT, via Karma, mentions "An early laminated acrylic sculpture" ([Karma / NYT](https://karmakarma.org/press/2024-03-14_the-new-york-times_-norman-zammitt/)). A 2026 show in Los Angeles is listed [U] ([Karma](https://karmakarma.org/exhibitions/norman-zammitt-2026_la/press-release/)) | No (estate) |
| **Eric Zammitt**, Los Angeles | Laminated coloured-acrylic panels made from tens of thousands of pieces ([gallery](https://www.srcart.com/artists/eric-zammitt)) | Possibly as an adviser, through his SF gallery [E] |
| **Ferguson Hill** (UK) | Acrylic horn loudspeakers. The Jetstream horns are 1.65 m tall and cost £72,955; how they are made is not stated ([Core77, 24 Jan 2024](https://www.core77.com/posts/127507/Gigantic-Transparent-Horn-Shaped-Speakers-by-Ferguson-Hill)) | No |
| **Creation Audio C-Horn** | "The 25mm acrylic sides show off the internal workings"; hardwoods "machined to create a wooden sculpture" form the horn ([Mono & Stereo](https://www.monoandstereo.com/?p=20108)) | No |
| **US Enclosure Company** | Clear and tinted acrylic or polycarbonate loudspeaker cabinets, in "any Pantone color"; "100 percent USA manufactured" ([page](https://usenclosure.com/Transparent%20clear%20loudspeaker%20Cabinet%20Walls/Water%20Clear%20Loudspeaker%20Caninet%20Walls.htm)) | Possibly a cabinet vendor; location and capacity [U] |
| Patent US 10,397,695 B2 | "Laminated glass and laminated acrylic loudspeaker enclosure" ([Google Patents](https://patents.google.com/patent/US10397695)) | No |

**Gap:** no commercial or DIY horn made of *laminated acrylic* layers was found [U].

---

## Suggested fallback schedule [E]

| Week of | Track 1: cutting | Track 2: bonding |
|---|---|---|
| 2 Nov | Join Ace; Shop Basics 5 Nov. Order TruCast cut to 48 × 36 in. Send DXFs to Pololu, Neal's CNC, Acrylic Art and Atlas Contour for quotes | Order the Weld-On 40 pints and gallon, degassing kit, gloves, respirator and polarizers. Decide on the oven |
| 9 Nov | Optional clear rehearsal parts from SendCutSend (2–4 days) | Coupon trials on 2423 and 2074 offcuts |
| 16 Nov | Ace laser class 17 Nov, then cut; or receive vendor-cut layers | Prepare and pre-anneal layers |
| 23 Nov – 6 Dec | Router class 5 Dec for cabinet panels | Bond sub-stacks, anneal, join, final anneal (horn 1, then horn 2) |
| 7 Dec – 3 Jan | Machine and finish the air path (R7 shops or Atlas Contour); final anneal | — |
| By mid-Jan | Assembly and tuning (R7 §4) | — |

---

## Sources

**A. Cutting**
- SendCutSend: [acrylic](https://www.sendcutsend.com/materials/acrylic/) · [min/max](https://www.sendcutsend.com/materials/min-max/) · [materials](https://www.sendcutsend.com/materials/) · [customer-material FAQ](https://sendcutsend.com/faq/can-you-cut-material-i-ship-to-yo/)
- Ponoko: [acrylic](https://ponoko.com/laser-cutting/acrylic) · [custom materials](https://help.ponoko.com/en/articles/4468203-custom-material-orders)
- Xometry: [acrylic laser](https://www.xometry.com/capabilities/sheet-cutting/acrylic-laser-cutting-service/) · [sheet cutting](https://xometry.com/capabilities/sheet-cutting) · [CNC acrylic](https://www.xometry.com/capabilities/cnc-machining-service/acrylic/) · [Big Blue Saw integration](https://investors.xometry.com/news-releases/news-release-details/xometry-integrates-big-blue-saws-software-data-laser-waterjet) · [DC360](https://www.digitalcommerce360.com/?p=1010376)
- Others: [Protolabs extents](https://www.protolabs.com/services/cnc-machining/cnc-machining-maximum-extents/) · [OSH Cut](https://oshcut.com/materials)
- Pololu: [materials](https://www.pololu.com/docs/0j24/5) · [capabilities](https://www.pololu.com/docs/0j24/1) · [pricing](https://www.pololu.com/docs/0j24/2) · [design](https://www.pololu.com/docs/0j24/4)
- [A&C TruCast 2423 ½" (cut-to-size)](https://www.acplasticsinc.com/product/2423-500-48x-96-trucast-p-2/) · [ePlastics 2074 ½"](https://www.eplastics.com/ACRY20740-500PM48X96) · [ePlastics fabrication](https://www.eplastics.com/plastic-fabrication) · [Delvie's laser](https://www.delviesplastics.com/c/custom-laser-cutting.html) · [Acme laser (403)](https://www.acmeplastics.com/laser-cutting)
- Bay Area: [Neal's CNC](https://www.nealscnc.com/) · [Automatic Arts](https://www.automatic-arts.com/) · [Atlas Contour](https://www.atlascontour.com/) · [Atlas contact](https://www.atlascontour.com/contact) · [Gizmo](https://gizmosf.com/) · [Acrylic Art](https://www.acrylicart.com/) · [Acrylic Art capabilities](https://www.acrylicart.com/2024/05/14/the-art-and-precision-of-plastic-fabrication-at-acrylic-art/) · [Piedmont Union City](https://www.piedmontplastics.com/locations/san-francisco) · [Laird locations](https://lairdplastics.com/locations/) · [you3dit](https://www.you3dit.com/machine_tags/acrylic) · [Bay Area guide](https://steampunk-explorer.com/city-guides/san-francisco-bay-area/arts-and-crafts)
- Laser capability: [OMTech 100 W](https://ca.omtech.com/blogs/knowledge/how-deep-can-a-100w-co2-laser-engraver-cut) · [LightBurn forum](https://forum.lightburnsoftware.com/t/best-settings-for-cutting-acrylic/41146/23)

**B. Makerspaces**
- Ace Makerspace: [home](https://www.acemakerspace.org/) · [membership](https://www.acemakerspace.org/membership/) · [laser wiki](https://wiki.acemakerspace.org/laser-cutting/) · [certifications](https://wiki.acemakerspace.org/tool-certifications/) · [router fees](https://wiki.acemakerspace.org/?p=15425) · [business FAQ](https://wiki.acemakerspace.org/?p=16022) · [router page](https://www.acemakerspace.org/cnc-router/) · [laser class](https://acemakerspace.org/?p=192214) · [router class](https://www.acemakerspace.org/?p=224017) · [Shop Basics](https://acemakerspace.org/?p=192230) · [retired router](https://wiki.acemakerspace.org/amt028/)
- Maker Nexus: [home](https://www.makernexus.org/) · [tools](https://www.makernexus.org/facilities-and-tools) · [FAQ](https://www.makernexus.org/faq)
- Noisebridge: [home](https://www.noisebridge.net/) · [laser](https://www.noisebridge.net/wiki/Laser_Cutter) · [Meetup](https://www.meetup.com/noisebridge/events/265397559/)
- Others: [Hacker Dojo pricing](https://hackerdojo.org/pricing/) · [The Crucible (Wikipedia)](https://en.wikipedia.org/wiki/The_Crucible_(arts_education_center)) · [Sun Gallery](https://sungallery.org/makerspace/) · [Idea Fab Labs 2015](https://www.santacruztechbeat.com/2015/03/19/new-makerspace-opening-santa-cruz/)
- Autodesk: [tours](https://technologycenterstours.autodesk.com/san-francisco) · [Research Residency update, 12 May 2026](https://www.research.autodesk.com/?p=7326)

**C. Specialists**
- [Acrylic Concepts (Thomasnet)](https://www.thomasnet.com/company/acrylic-concepts-30728370/profile) · [OCIP](https://ocip.com/services/acrylic-services/) · [Factory Fish Tanks](https://factoryfishtanks.com/) · [Eric Zammitt](https://www.srcart.com/artists/eric-zammitt)

**D. Bonding**
- Manufacturer guides: [Röhm 311-3](https://www.plexiglas.de/files/plexiglas-content/pdf/verarbeitungsrichtlinie/311-3-EN-joining-PLEXIGLAS.pdf) · [ACRYLITE 1591E](https://www.acrylite.co/files/content/acrylite.co/documents/fabrication-briefs/ACRYLITE-Reactive-Cement-Fabrication-Brief.pdf) · [ACRYLITE polymerizable cement](https://www.acrylite.co/resources/fabrication-manuals/acrylite-cell-cast-polymerizable-cement) · [ACRYLITE annealing](https://www.acrylite.co/resources/fabrication-manuals/annealing-acrylite-acrylic-sheet) · [ACRYLITE cementing](https://www.acrylite.co/resources/fabrication-manuals/cementing-acrylite) · [US Plastic SC-125](https://www.usplastic.com/catalog/files/charts/SC-125.pdf)
- Weld-On 40: [pint](https://www.eplastics.com/ips40-pt) · [gallon](https://www.eplastics.com/plexiglass/acrylic-accessories/ips40-gal) · [Chemical Concepts](https://www.chemical-concepts.com/product/weld-on-40-reactive-acrylic-adhesive/)
- Equipment and protective gear: [ACRIFIX sample](https://ibspot.com/products/acrifix-2r-0190-versatile-110-grams) · [VEVOR kit](https://homedepot.com/p/VEVOR-5-Gal-Vacuum-Chamber-and-3-5-CFM-Pump-Kit-Tempered-Glass-Lid-Vacuum-Degassing-Chamber-Kit-with-250-ml-Oil-Bottle-MCKDZKBT3CFM5YVRLV1/324369894) · [Gilson DOL-69A](https://www.globalgilson.com/standard-despatch-electric-oven-6-point-9ft-chamber) · [3M 6800](https://www.walmart.com/ip/16890833) · [6001 cartridges](https://staples.com/3m-organic-vapor-cartridge-white-2-pack-6001/product_422397) · [Silver Shield](https://shop.darley.com/product/silver-shield4h-chemical-resistant-hazmat-gloves-large/01t2E00000QZd7PQAT) · [glove case report](https://blogs.the-hospitalist.org/content/glove-choice-crucial-job-related-dermatitis)

**E. Proof**
- [Tannoy patent](https://patents.google.com/patent/US8213658B2/en) · [GRF-R build](https://hilberink.nl/codehans/tannoy127.htm) · [GRF build](https://hilberink.nl/codehans/tannoy126.htm) · [Magico Mini (403)](https://www.theabsolutesound.com/articles/exotica-magico-mini-loudspeaker) · [6moons](https://6moons.com/?p=70594) · [Kharma](https://www.theabsolutesound.com/articles/high-end-audio-buyers-guide-2024-kharma-exquisite-exq-md-3-0-s/)
- [Vasa](https://www.taylorandgraham.com/artworks/11712-vasa-velizar-mihich-cylindrical-column-1997) · [Norman Zammitt (Wikipedia)](https://en.wikipedia.org/wiki/Norman_Zammitt) · [Norman Zammitt / NYT](https://karmakarma.org/press/2024-03-14_the-new-york-times_-norman-zammitt/) · [Karma 2026](https://karmakarma.org/exhibitions/norman-zammitt-2026_la/press-release/)
- [Ferguson Hill](https://www.core77.com/posts/127507/Gigantic-Transparent-Horn-Shaped-Speakers-by-Ferguson-Hill) · [C-Horn](https://www.monoandstereo.com/?p=20108) · [US Enclosure](https://usenclosure.com/Transparent%20clear%20loudspeaker%20Cabinet%20Walls/Water%20Clear%20Loudspeaker%20Caninet%20Walls.htm) · [US10397695B2](https://patents.google.com/patent/US10397695)

### Pages that were blocked or failed (none retried or bypassed)
- **HTTP 403:**
  - acmeplastics.com/laser-cutting
  - tapplastics.com custom-fabrication page
  - autodesk.com research-residency page
  - globalspec.com local listings
  - freepatentsonline.com (the patent was read on Google Patents instead)
  - theabsolutesound.com Magico Mini review
- **HTTP 503:** technologycenters.autodesk.com/locations/pier9
- **HTTP 404:**
  - acplasticsinc.com "Weld-On 40 Properties" PDF
  - atlascontour.com/file-prep
  - noisebridge.net/wiki/Visiting and /wiki/CNC_Router
  - protolabs.com acrylic materials page
  - oshcut.com max-min page
  - xometry.com sheet-cutting-service
  - acemakerspace.org/calendar/list
- **Rendered page titles only:** thecrucible.org pages. A cmtc.com profile redirected to a generic page.
