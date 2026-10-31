# R6: Where to make EARF's acrylic parts and products (US/California, Mexico or Asia)

Compiled 2026-10-31 for EARF, San Francisco: hi-fi and lighting in cell-cast acrylic, tinted through, in eight custom colours.

**Ground rules**
- Public web only. Nobody was contacted, and no forms were filled in or accounts created.
- Every tariff fact carries its own date.
- **(est.)** marks my own estimate or arithmetic. Every other claim is linked to its source.
- "Search snippet" means the claim came from a web-search result because the page itself could not be opened.

**Research limits (read first)**
- **Search budget.** The web-search budget, shared by every agent in this session, ran out partway through. The following therefore rest on fewer sources than planned, and no other workaround was used:
  - Taiwanese and Vietnamese casters and fabricators (§2.4);
  - Mexico–US freight prices (§4.2);
  - Mexican quality signals (§1.3).
- **Pages that could not be read:**
  - Alibaba (HTTP 410 or an empty page).
  - TAP Plastics and Acme Plastics (403).
  - White & Case and the Congressional Research Service (403).
  - The Cornell-hosted 2006 Chemcast catalogue (503).
  - federalregister.gov, which showed a bot check. It was not bypassed. The same Federal Register notice was read instead from the Government Publishing Office's govinfo PDF and from the Federal Register API.
- **Custom-colour minimums.** No **current** published custom-colour minimum was found for any North American caster. The ~2,500 lb figure comes from Plastiglas's own 2006 Chemcast catalogue (§1.1). Confirm it before relying on it.

---

## TL;DR and recommendation

| Stage | Where | Core moves |
|---|---|---|
| **Prototypes** (now to Q1 2027) | **California, Bay Area-centred** | <ul><li>Stock cell-cast colours from US stock: Plastiglas CHEMCAST via Piedmont (Union City, CA) or TAP Plastics, Reynolds R-Cast stock colours, Plaskolite OPTIX G.</li><li>Local CNC and polishing (e.g., Cutting Edge Plastics, Laguna Hills).</li><li>Horn and dome trials with Reynolds Polymer (which forms "trumpet shapes" and spheres).</li><li>Aluminium turned and anodised in the US.</li><li>Electronics assembled in-house in San Francisco.</li></ul> |
| **~10 sets** | **California** | <ul><li>Start colour development with Plastiglas: colour-bank matching, through Piedmont.</li><li>Collapse the design to as few colour × thickness combinations as possible.</li><li>Run benchmark requests for quotes (RFQs) to one Taiwanese and two Chinese casters.</li><li>Meet Mexican suppliers at **Plastimagen México, 10–13 Nov 2026, Mexico City**.</li></ul> |
| **~50 sets** | **"Mexican sheet, Californian hands"** | <ul><li>Custom-colour sheet from **Plastiglas (Mexico)**. It is duty-free if it is certified as USMCA-originating, which polymerisation in Mexico makes likely (est.).</li><li>Fabrication, cementing, annealing and assembly in California.</li><li>Horn and domes from Reynolds or another qualified thick-forming shop.</li><li>Aluminium parts made in the US.</li><li>Pilot one flat part with a **Tijuana** fabricator to build a Mexican option for later volume.</li></ul> |
| **Asia** | **Benchmark and backup only (for now)** | <ul><li>As of 31 Oct 2026, Chinese PMMA sheet pays **~44%**: 6.5% MFN, plus 25% Section 301 List 2, plus 12.5% Section 301 "forced-labour".</li><li>Chinese LED lamps pay ~41.4%, and Chinese loudspeakers 20% assembled or ~37.5% as parts.</li><li>**Taiwan pays ~10% all-in**, and Vietnam MFN + 12.5%.</li><li>Ocean freight is ~30–40 days door to door, at $7.5–8.4k per 40 ft container (late Oct 2026).</li></ul> |

**How to bring the custom-colour minimum down, ranked:**

1. **Prototype in stock colours.** There is no minimum, and Plastiglas lists 17 standard colours.
2. **Ask Plastiglas for colour-bank matches.** Its 2006 policy says it searches its colour bank first, to avoid development cost.
3. **Design for few combinations.** The 2006 minimum applies per colour **and** size **and** thickness. Use one thickness and one sheet size per colour.
4. **Put custom colours on high-volume parts.** Two 10 mm horns per set could use about **3,000 lb across 50 sets** (est.).
5. **Ask about "customized short orders"**, which Plastiglas advertises. Also ask about splitting one batch across thicknesses, and about Piedmont or TAP co-stocking the colour.
6. **Use a low-minimum Asian caster** only for low-volume colours, preferably from Taiwan for duty.

---

## 0. What EARF needs, by region

| Need | California / US | Mexico | China | Taiwan / Vietnam |
|---|---|---|---|---|
| Custom-colour cell-cast sheet, 3–30 mm | US casters: [Spartech Polycast](https://spartech.com/product-type/cell-cast-acrylic) (custom colours quoted), [Reynolds R-Cast](https://www.reynoldspolymer.com/commercial/r-cast-acrylic-thin-gauge-sheet/) (custom by special order). No California caster was found. | [Plastiglas](https://www.piedmontplastics.com/suppliers/plastiglas-de-mexico) ("largest in North America") and [Plaskolite Matamoros](https://plaskolite.com/contact-us/news/press-releases/detail/plaskolite-starts-cell-cast-acrylic-production) | Many casters. Listed minimums run from 10 kg to 2 t ([Made-in-China](https://www.made-in-china.com/factory/acrylic-solid-sheet.html)). | Not verified (§2.4) |
| Thick sheet 20–30 mm, and blocks | Reynolds thick sheet, 25–102 mm, clear ([Reynolds](https://www.reynoldspolymer.com/commercial/r-cast-acrylic-thick-gauge-sheet/)) | Plastiglas up to 1.250" / 32 mm ([2011 deck](https://mail.interstateplastics.com/docs/Plastiglas-Presentation.pdf); [datasheet](https://new.avanceytec.com.mx/img/cms/0100-0010-0050/LAMINA-DE-ACRILICO-PLASTIGLAS-CRISTAL-VERDE-Y-COLORES.pdf)) | Alands 1–50 mm, Shengdalong 2–35 mm, Jinbao listings to 300 mm (§2.2) | Not verified |
| CNC, polishing, annealing | Plenty, e.g. [Cutting Edge Plastics](https://www.cuttingedgeplastics.com/) (California) | Point-of-purchase (POP) display and sign shops: CNC router, laser, polishing, bending ([Acriland](https://www.acriland.com)) | [Wetop](https://wetopacrylic.com/): ±0.2 mm, diamond polishing | Not verified |
| Polymerising (two-part) cement | [Reynolds](https://www.reynoldspolymer.com/) (bonding is a core capability); [Emco](https://www.emcoplastics.com/) ("museum quality gluing") | Not advertised by any Mexican shop found | Not advertised explicitly | Not verified |
| Deep forming of 10 mm cast (the horn) | [Reynolds](https://www.reynoldspolymer.com/capabilities/forming/) ("trumpet shapes", spheres); [ADA](https://www.acrylicdesign.com/) (vacuum and drape forming) | [Acrílicos Profesionales de Monterrey](https://acrilicosprofesionales.com) (thermoforming; gauge not stated) | Wetop (thermoforming; gauge not stated) | Not verified |
| Domes and spheres | Reynolds (spheres) | [Acrilfrasa](https://acrilfrasa.com) (skylight domes, not optical parts) | Not verified | Not verified |
| Turning, and black anodised aluminium | Make in the US. Imported aluminium parts pay Section 232 duty of 25–50% (§3.4). | 232 applies | 232 plus List 3 (§3.4) | 232 applies |
| Electronics assembly | In-house in San Francisco | Not verified at this scale | n/a | n/a |
| Duty on an assembled speaker (8518.22) | 0 | 0 if USMCA-qualifying, otherwise 10% | 20% | Taiwan 10%, Vietnam 12.5% |
| Typical time to San Francisco | Days | Tijuana 1–2 days; Mexico City area ~5–8 days (est.) | 30–40 days by sea, door to door; 8–10 days by air ([Freightos](https://www.freightos.com/shipping-routes/shipping-from-china-to-the-united-states/)) | Similar to China (est.) |

---

## 1. Mexico

### 1.1 Cell-cast acrylic makers

**Plastiglas de México (Grupo Verzatec)**
- **Ownership.**
  - Grupo Unigel sold 100% of Plastiglas to Grupo Verzatec. The sale closed on 5 June; the article reporting it is dated 20 Sep 2024 ([LexLatin](https://lexlatin.com/noticias/grupo-unigel-vende-plastiglas-mexico-grupo-verzatec-mexico); [Greenberg Traurig, Sep 2024](https://www.gtlaw.com/es/news/2024/09/press-releases/greenberg-traurig-mexico-advises-grupo-unigel-on-plastiglas-de-mexico-sale)).
  - Verzatec lists Plastiglas among its business units as a leader in cell-cast acrylic sheet in North America ([Verzatec](https://www.verzatec.com/unidades-de-negocio)).
- **Scale.**
  - Piedmont calls it "the largest manufacturer of cell cast acrylic sheet in North America", with "two large factories and five production lines, all based in Mexico", serving customers since 1959 ([Piedmont](https://www.piedmontplastics.com/suppliers/plastiglas-de-mexico)).
  - The company's 2011 deck gives these figures ([2011 Unigel/Plastiglas deck](https://mail.interstateplastics.com/docs/Plastiglas-Presentation.pdf); dated, so treat as history):
    - capacity of 32.5 million lb a year, ≈14,700 t (est., conversion);
    - Ocoyoacac (State of Mexico) 21.5 M lb, and "San Luis" 11 M lb;
    - 60% share of the Mexican market;
    - exports to the US and Canada since 1990.
- **Range.**
  - CHEMCAST cell-cast sheet in "standard and custom colors", described as "customized short orders made to exact specifications". Its markets include furniture, POP, museums and marine ([Piedmont](https://www.piedmontplastics.com/suppliers/plastiglas-de-mexico)).
  - In 2011 ([deck](https://mail.interstateplastics.com/docs/Plastiglas-Presentation.pdf)):
    - thickness 0.060" to 1.250";
    - sheets from 48×72" up to 80×120";
    - custom, fluorescent and pearl colours;
    - "thick" and "extra-thick gauge";
    - an impact-modified **Furniture Grade**: 0.590" standard; 0.472" and 0.708" on request; shown in custom colours;
    - a two-layer **Bi-Color** sheet in 0.944" and 1.250".
  - A 2019 distributor datasheet lists **17 standard colours in 3–12 mm** ([Avance y Tec datasheet](https://new.avanceytec.com.mx/img/cms/0100-0010-0050/LAMINA-DE-ACRILICO-PLASTIGLAS-CRISTAL-VERDE-Y-COLORES.pdf)).
- **Thickness tolerance, an important design input.**
  - The same datasheet allows, on 48×96" sheet ([datasheet](https://new.avanceytec.com.mx/img/cms/0100-0010-0050/LAMINA-DE-ACRILICO-PLASTIGLAS-CRISTAL-VERDE-Y-COLORES.pdf)):
    - 10 mm nominal: 8.30–10.80 mm;
    - 24 mm nominal: 21.79–24.58 mm;
    - 32 mm nominal: 29.61–33.32 mm.
  - These bands match the ASTM D4802 commercial tolerances printed by Polycast. For example, 1.000" sheet is +0.023/−0.087" ([Polycast catalogue](https://modernplastics.com/wp-content/uploads/2015/03/Polycast-General-Catalog.pdf)).
  - So design slots, rebates and cement joints for the measured thickness, or buy "close tolerance" sheet. Polycast offers close-tolerance sheet ([Polycast](https://modernplastics.com/wp-content/uploads/2015/03/Polycast-General-Catalog.pdf)).
- **US channel.**
  - Piedmont keeps each location stocked with CHEMCAST and has worked with Plastiglas for 20+ years, including co-developing marine grades ([Piedmont](https://www.piedmontplastics.com/suppliers/plastiglas-de-mexico)).
  - Piedmont's "San Francisco" branch is at 33340 Central Ave, **Union City, CA** ([Piedmont locations](https://www.piedmontplastics.com/locations)).
  - TAP Plastics sells CHEMCAST transparent colours cut to size to ±1/32" ([TAP](https://www.tapplastics.com/product/plastics/cut_to_size_plastic/acrylic_sheets_transparent_colors/519); search snippet, the page returned 403).
- **Custom-colour policy (2006 Chemcast catalogue, the only published version found)** ([Chemcast catalogue](https://courses.cit.cornell.edu/mae2250/Emerson/Chemcast_Acrylic_brochure.pdf); search snippet, the PDF returned 503):
  - A new custom colour needs a minimum of **2,500 lb ("one standard pallet ±10% batch production")**.
  - Later orders of the same colour **in identical size and thickness** need the same minimum batch.
  - An existing colour in a thickness not previously offered counts as development.
  - Plastiglas "first will initially search its color bank for identical or very close matches".
  - Cancelling an approved custom colour carries a **100% charge**.
  - This matches the ~2,500 lb risk EARF already knows about. Get current terms in writing.

**Plaskolite, Matamoros (Tamaulipas)**
- **The plant.**
  - Trinseo's December 2022 restructuring included closing its PMMA sheet site in Matamoros. It sold the land, buildings and equipment for ≈$19.0 M, and the sale closed in May 2023 ([Trinseo 10-K FY2023](https://www.sec.gov/Archives/edgar/data/1519061/000155837024001604/tse-20231231x10k.htm), via search summary).
  - The buyer was Plaskolite, and the site covers about 11 acres ([Signs of the Times](https://signsofthetimes.com/plaskolite-to-acquire-manufacturing-facility-in-mexico/amp/)).
- **Production.** Cell-cast production of the **OPTIX G Series** began about three months after the purchase. Colours, textures and custom thicknesses were expected by Q4 2023 ([Plaskolite, 14 Jul 2023](https://plaskolite.com/contact-us/news/press-releases/detail/plaskolite-starts-cell-cast-acrylic-production)).
- **Colours.** Today's catalogue lists Black 2025, Gray I35 and White B26, with "Custom colors available". It adds that non-stock colours or sizes "may require a minimum quantity order", without giving a number ([OPTIX G colored](https://plaskolite.com/catalog/optix-g-series-cell-cast-colored-acrylic)).
- **Why it matters.** Plaskolite is a **second Mexican cell-cast source**, worth asking for its custom-colour minimum.

**Others (not confirmed as casters)**
- **Plásticos Especiales GAREN (Tetla, Tlaxcala).**
  - It sells "láminas de acrílico CELL CAST" alongside polycarbonate and polystyrene sheet. It claims 30+ years and 27 branches. Its site does not say whether it casts the sheet itself ([GAREN](https://www.garen.com.mx)).
  - A directory says its sheet is cast from MMA ([Directorio de Fábricas](https://www.directoriodefabricas.com/mexico/fabricantes-de-acrilicos-en-mexico.html)).
- **Listed as "manufacturer and distributor", process not stated** ([Cosmos](https://www.cosmos.com.mx/producto/acrilico-cast-1h3g/)):
  - Mundo Acrílico Hypar (Querétaro);
  - MIDSA (Monterrey);
  - PQI de Occidente (Jalisco);
  - Procell.
- **Plásticos Beraca** sells clear cast sheet in **2–50 mm from one piece** ([Cosmos](https://www.cosmos.com.mx/producto/acrilico-cast-1h3g/)).

### 1.2 Fabricators, furniture and display makers by city

None of these sites mentions any of the following, which is the key gap:
- polymerising (two-part) cement;
- annealing;
- aquarium-grade bonding;
- deep forming of thick cast sheet.

All listings are as published; none was verified in person. The directory list was updated in August 2024.

| City | Company | What they make | Public quality signals |
|---|---|---|---|
| CDMX | [Acriland](https://www.acriland.com) | POP displays, boxes, commercial furniture | <ul><li>Router CNC and laser.</li><li>"Cut, bend, polish and assemble".</li><li>25+ years.</li><li>Brand logos: Colgate, Kimberly-Clark, Neutrogena, Häagen-Dazs.</li><li>Quotes in under 24 h.</li></ul> |
| CDMX | Tesacril ([directory](https://www.directoriodefabricas.com/mexico/fabricantes-de-acrilicos-en-mexico.html)) | Cosmetic displays and POP | <ul><li>Sheet stock 2–24 mm clear and 3–6 mm colour.</li><li>Its site returned 503.</li></ul> |
| CDMX | Fraser ([directory](https://www.directoriodefabricas.com/mexico/fabricantes-de-acrilicos-en-mexico.html)) | Displays, showcases, bulk-candy containers | None published |
| CDMX | Acrílicos Nolasco ([directory](https://www.directoriodefabricas.com/mexico/fabricantes-de-acrilicos-en-mexico.html)) | Sheet, tube, rod, boxes, lecterns | None published |
| Edomex/CDMX | [Acrilfrasa](https://acrilfrasa.com) | Sheet and parts, skylight domes, partitions | Laser cutting; no clients named |
| Monterrey | [Acrílicos Profesionales de Monterrey](https://acrilicosprofesionales.com) | Custom parts to customer drawings | <ul><li>**Thermoforming.**</li><li>Laser cutting.</li><li>30+ years.</li><li>No certifications listed.</li></ul> |
| Monterrey | Acrideas Modernas; Disamex ([directory](https://www.directoriodefabricas.com/mexico/fabricantes-de-acrilicos-en-mexico.html)) | Advertising and decorative articles; screen printing (serigraphy) | None published |
| Guadalajara | Acrilic Products; Acrílicos Jessi; Acrílicos Newton ([directory](https://www.directoriodefabricas.com/mexico/fabricantes-de-acrilicos-en-mexico.html)) | Displays, signs, awards; sheet including mirror | None published |
| Tijuana | [Acrílicos del Pacífico / Acrylart](https://acrylart.com.mx) | Design-to-delivery custom acrylic; also stainless steel and polycarbonate | <ul><li>CNC router and laser.</li><li>"19+ years".</li><li>Ships "to any part of Mexico and the USA".</li></ul> |

**Minimums.** None of the fabricators publishes a minimum. Among sheet sellers, Beraca sells from one piece ([Cosmos](https://www.cosmos.com.mx/producto/acrilico-cast-1h3g/)).

**Assessment.** Mexico's proven asset for EARF is **the sheet**. Its fabrication base, as visible online, is POP and signage. It could do flat CNC parts and polishing soon. Furniture-grade cementing and thick forming need supplier development and audits in person.

### 1.3 How a small foreign brand engages

1. **Through US distributors.** This is the easiest route.
   - Piedmont stocks CHEMCAST at each branch, including Union City, CA ([Piedmont](https://www.piedmontplastics.com/suppliers/plastiglas-de-mexico); [locations](https://www.piedmontplastics.com/locations)). EARF does no importing, and custom orders can ride on the distributor's replenishment flow. That last point is an assumption to confirm.
2. **Directly with Plastiglas.** It has exported to the US since 1990 ([2011 deck](https://mail.interstateplastics.com/docs/Plastiglas-Presentation.pdf)). EARF would need:
   - a US customs broker;
   - a USMCA certification of origin from Plastiglas, to claim the "S" duty-free rate and the forced-labour 301 exemption (§3);
   - a cross-border carrier.
3. **Meet them in person.**
   - [Plastimagen México](https://www.plastimagen.com.mx/) runs **10–13 Nov 2026** at Centro Banamex, Mexico City, with 740 exhibitors.
   - [Expo Publicitas](https://www.expopublicitas.com/) runs **19–21 May 2027** for POP and retail display makers.
4. **Mexican fabricators directly.** Send a drawing and a sample part, and visit before ordering. Websites invite direct quotes, e.g. Acriland's under-24-hour promise ([Acriland](https://www.acriland.com)).
5. **Shelter companies, for later stages.**
   - These run a Mexican legal entity, hiring, payroll and customs for a foreign firm's own cell. [Tecma](https://www.tecma.com/) (Tijuana, Juárez, Monterrey, León, Torreón, Mexicali, San Luis Potosí) says it suits "any size". [IVEMSA](https://www.ivemsa.com/) says it does **not** do contract manufacturing.
   - This route fits a captive EARF cell at hundreds of sets a year, not 50 sets (est.).
6. **Agents.** No Mexico-based sourcing agent for acrylic was verified, because the search budget ran out.

---

## 2. Asia (China, Taiwan, Vietnam)

### 2.1 Published minimums from cast-sheet makers

| Source | Location | Published minimum | Custom-colour terms | Thickness | Notes |
|---|---|---|---|---|---|
| [Made-in-China factory list](https://www.made-in-china.com/factory/acrylic-solid-sheet.html) (snapshot 31 Oct 2026) | Jiangxi, Zhejiang, Shandong, Guangdong, Shanghai | **10 kg to 36 t**; most **500–1,000 kg** | — | Up to 30 mm in some listings | Listing prices are roughly **US$1.2–3/kg**, mostly $1.5–2.5/kg |
| Jumei ([same list](https://www.made-in-china.com/factory/acrylic-solid-sheet.html)) | Jiangxi | 500 pieces or 500 kg | — | 3–5 mm listings | A long-running Chinese caster |
| [Zhejiang Shengdalong](https://shengdalong.en.made-in-china.com/product/ZSRQpNDKXUkt/China-Colored-Cast-Acrylic-Sheet.html) | Lanxi, Jinhua | **2 t** (24 sheets per its FAQ) | "Custom colours offered" | 2–35 mm | <ul><li>**Offers 60% or 100% virgin MMA.**</li><li>Lists "cell or continuous cast".</li><li>80 t a day.</li><li>TÜV audit.</li></ul> |
| [Alands](https://alandsacrylic.com/en/acrylic-sheet/color-acrylic-sheet/colored-acrylic-sheets/) | Jinan | **1,000 kg per order; colours and specs can be mixed** | No separate rule | 1–50 mm; up to 2050×3050 mm | Claims 100% virgin MMA; ISO 9001 |
| [Jinbao](https://www.jinbaoplastic.com/my/the-spectrum-of-possibilities-cast-acrylic-sheet-colors-design-trends.html) | Jinan; founded 1996 | — | <ul><li>Matches Pantone or RAL, or a physical sample.</li><li>Says the cast custom-colour minimum is "much lower" than for extruded sheet.</li></ul> | A listing says 1–300 mm | — |
| [Wetop guide](https://wetopacrylic.com/guide/pantone-color-matching-acrylic-oem/) (16 Jul 2026, updated Sep 2026) | Shenzhen | 100 pieces per design (finished products) | <ul><li>Custom-tinted material needs **a separate mill-batch minimum per colour**.</li><li>**$200** is the "published low-end" one-time colour fee.</li><li>No universal ΔE: agree it in the PO.</li></ul> | — | A fabricator, not a caster |
| [Baidu B2B wiki](https://b2bwiki.baidu.com/en/encyclopedic/custom-colored-acrylic-sheet) (updated 15 Jul 2026) | — | Custom colours "usually start at **10–20 sheets**" | <ul><li>2–6 weeks.</li><li>"ΔE<1.5 is industry standard".</li><li>Beware metamerism.</li></ul> | — | Generic and unverified; use only as a negotiating anchor |
| Alibaba listings ([showroom](https://www.alibaba.com/showroom/cast-acrylic-sheet.html); search snippets only) | — | <ul><li>Coloured cast sheet 14–18 mm: 200.</li><li>Jumei coloured board 2.5–40 mm: **1,000 kg**.</li><li>Clear cast 20–30 mm: 500.</li></ul> | — | — | Pages could not be fetched |

**Reading.** Chinese casters publish minimums **order-based, from 0.5 to 2 t**, and some let colours be mixed (Alands). Custom tint is quoted per colour. Asking for **~10–20 sheets or 200–500 kg per colour** looks realistic, against ~1,134 kg (2,500 lb) at Plastiglas (est., from the listings above). The landed cost then has to absorb China's tariffs (§3).

### 2.2 Thick cast sheet (20–30 mm) and blocks

- **Alands:** 1–50 mm ([Alands](https://alandsacrylic.com/en/acrylic-sheet/color-acrylic-sheet/colored-acrylic-sheets/)).
- **Shengdalong:** 2–35 mm ([listing](https://shengdalong.en.made-in-china.com/product/ZSRQpNDKXUkt/China-Colored-Cast-Acrylic-Sheet.html)).
- **From the [Made-in-China list](https://www.made-in-china.com/factory/acrylic-solid-sheet.html):**
  - Shandong Yingchuang, 1–30 mm;
  - Zhanjiang Kingstar, "thick solid sheet for aquarium projects", 500 kg minimum.
- **Jinbao:** a listing says 1–300 mm ([Jinbao](https://www.jinbaoplastic.com/my/the-spectrum-of-possibilities-cast-acrylic-sheet-colors-design-trends.html)).
- **For comparison:**
  - Reynolds' R-Cast thick sheet is 25–102 mm, clear, up to 72×186" ([Reynolds](https://www.reynoldspolymer.com/commercial/r-cast-acrylic-thick-gauge-sheet/)).
  - Polycast offered pre-shrunk sheet from 0.060" to 4.250", and composite castings above 4.5" ([Polycast catalogue](https://modernplastics.com/wp-content/uploads/2015/03/Polycast-General-Catalog.pdf)).
- **Tolerance on thick sheet** runs to tenths of a millimetre or more; 24 mm nominal is 21.79–24.58 mm ([datasheet](https://new.avanceytec.com.mx/img/cms/0100-0010-0050/LAMINA-DE-ACRILICO-PLASTIGLAS-CRISTAL-VERDE-Y-COLORES.pdf)). For blocks and turned parts, plan to machine to size.

### 2.3 High-end fabricators (furniture and luxury display)

| Firm | Location | Profile and quality signals |
|---|---|---|
| [JAYI Acrylic](https://www.jayiacrylic.com/) | Huizhou, Guangdong | <ul><li>Founded 2004; about 150 workers.</li><li>Custom acrylic furniture and luxury displays (cosmetics, perfume, watches, jewellery).</li><li>Brand logos include Target, Macy's, YSL, Swarovski, Sony and Samsung.</li><li>Inspection steps: sample confirmation, 2+ mid-production checks, final random inspection, 100% raw-material QC.</li></ul> |
| [Wetop](https://wetopacrylic.com/) | Shenzhen (works) and Dongguan (office) | <ul><li>Since 2008; 5,000 m²; 65+ staff; ISO 9001:2015.</li><li>CNC, laser, bending and bonding, **diamond polishing, thermoforming**, assembly.</li><li>**±0.2 mm**, or ±0.1 mm on critical fits.</li><li>Paid sample $200–500 in 3–5 days; production 15–20 days after approval.</li><li>Payment 30/70.</li><li>Also makes cast-acrylic tables and chairs.</li></ul> |
| [Acrylictogo](https://acrylictogo.com/buyers-faq/) | Shenzhen | <ul><li>Since 2009.</li><li>Lead times:<ul><li>10–15 working days for fewer than 200 pieces;</li><li>25–30 for complex parts;</li><li>**35–40 with wood, metal or LED parts**;</li><li>samples in 3–10 days.</li></ul></li></ul> |
| [Reynolds Polymer](https://www.reynoldspolymer.com/), Asia site | Rayong, Thailand | Thick-acrylic specialist with a site in Asia; useful if EARF ever moves thick parts offshore |
| [Nippura](https://www.nippura.com/) | Kagawa, Japan; five plants, including a new Ehime plant from 1 Apr 2026 | World-class aquarium panels. A reference point for thick forming quality, though not a likely partner at EARF's scale (est.). |

### 2.4 Taiwan and Vietnam: not verified

The search budget ran out before any Taiwanese or Vietnamese cell-cast producer, or high-end fabricator, could be verified. The tariff arithmetic makes **Taiwan the Asian origin worth an RFQ**: its forced-labour 301 duty is capped so that MFN plus 301 = 10% (§3.2). Vietnam pays MFN + 12.5%. Treat both as open RFQ items, not findings.

### 2.5 Quality signals and pitfalls (Asia)

- **Material.**
  - Ask for **cell cast, 100% virgin MMA**, with a certificate. Shengdalong sells **60% or 100% virgin MMA** and lists "cell **or continuous** cast", so specify both explicitly ([listing](https://shengdalong.en.made-in-china.com/product/ZSRQpNDKXUkt/China-Colored-Cast-Acrylic-Sheet.html)).
  - Specify the ASTM D4802 tolerance class or a "close tolerance" grade ([Polycast](https://modernplastics.com/wp-content/uploads/2015/03/Polycast-General-Catalog.pdf)).
- **Colour.**
  - Put the ΔE limit, light source and **measurement thickness** in the PO. Wetop says there is no universal threshold; one Chinese reference cites ΔE<1.5, and warns of metamerism ([Wetop](https://wetopacrylic.com/guide/pantone-color-matching-acrylic-oem/); [Baidu wiki](https://b2bwiki.baidu.com/en/encyclopedic/custom-colored-acrylic-sheet)).
  - A through-tinted transparent colour looks darker in thicker sheet. Approve colour at production thickness (est., engineering note).
- **Forming behaviour.** Unshrunk cast sheet shrinks about 2% and thickens about 4% when heated to forming temperature ([Polycast](https://modernplastics.com/wp-content/uploads/2015/03/Polycast-General-Catalog.pdf)). A horn tool proven on one caster's sheet may need retuning on another's (est.).
- **Commercial terms.**
  - Paid samples first ($200–500 at Wetop); 30/70 payment ([Wetop](https://wetopacrylic.com/)).
  - Inspect before shipment: JAYI describes its own steps ([JAYI](https://www.jayiacrylic.com/)).
- **Hidden costs.**
  - Tariffs of 20–44% on China (§3).
  - 30–40 days by sea, and US West Coast port risk (§4).
  - De minimis is still suspended, so small sample shipments pay full duty (§3.5).

---

## 3. Tariffs and trade, as of 31 Oct 2026 (US import side)

### 3.1 What changed, with dates

| Date | Event | Source |
|---|---|---|
| 20 Feb 2026 | **Supreme Court, *Learning Resources v. Trump* (6–3):** the International Emergency Economic Powers Act (IEEPA) does not authorise tariffs. This voids the 2025 fentanyl tariffs on China, Mexico and Canada, and the "reciprocal" tariffs. | [Cornell LII](https://www.law.cornell.edu/supremecourt/text/24-1287); [CRS LSB11398](https://www.congress.gov/crs-product/LSB11398) |
| 24 Feb 2026 | CBP stops collecting IEEPA duties. A **Section 122** 10% surcharge starts for 150 days. USMCA-eligible goods and Section 232 goods are exempt. | [GHY](https://www.ghy.com/trade-compliance/us-10-section-122-tariff-in-effect-feb-24-ieepa-tariffs-directed-to-wind-down-de-minimis-suspension-continues/) |
| 11 Mar 2026 | USTR opens **"excess-capacity" Section 301** investigations into 16 economies, including **China, Mexico, Taiwan, Vietnam, Thailand and Japan**. Sectors named include **plastics**. Hearings ran 5–8 May. | [EY](https://taxnews.ey.com/news/2026-0623-us-trade-representative-initiates-section-301-investigations-into-structural-excess-capacity-comment-period-and-hearings-announced) |
| 6 Apr 2026 | **Section 232 metals duties now apply to full customs value**: 50% for articles made entirely or almost entirely of metal, 25% for derivatives. | [GHY](https://www.ghy.com/trade-compliance/us-adjusts-section-232-tariffs-on-aluminum-steel-and-copper-full-customs-value-now-applies/) |
| 24 Jun 2026 | CBP keeps de minimis suspended under its own authority. The statutory repeal follows on 1 Jul 2027. | [Dutylane](https://dutylane.com/tariff/policy/de-minimis) (search summary) |
| 1 Jul 2026 | **USMCA joint review:** the US declines to extend. Reviews now happen every year. The agreement stays in force, but terminates on 1 Jul 2036 unless extended. | [DLA Piper, 16 Jul 2026](https://www.dlapiper.com/en-us/insights/publications/2026/07/united-states-declines-to-extend-the-usmca) |
| **24 Jul 2026** | **Section 301 "forced-labour" tariffs on 60 economies replace Section 122.** <ul><li>**China 12.5%**, **Vietnam 12.5%**, **Mexico 10%** (USMCA-qualifying goods exempt).</li><li>**Taiwan 10% net of MFN.**</li><li>They **stack** on the existing China 301 duties. Section 232 goods are exempt.</li><li>Notice: 91 FR 47318, published 28 Jul 2026.</li></ul> | [Federal Register notice 2026-15181 (govinfo PDF)](https://www.govinfo.gov/content/pkg/FR-2026-07-28/pdf/2026-15181.pdf); [EY](https://taxnews.ey.com/news/2026-1603-ustr-takes-final-action-imposing-tariffs-on-60-trading-partners-as-section-122-tariffs-expire); [Honigman](https://www.honigman.com/alert-3462) |
| 23–28 Sep 2026 | The US–China **truce is extended to 10 Jan 2027**. Port fees on China-linked vessels are "likely" postponed, but USTR had not ruled as of 30 Sep. | [NBC](https://www.nbcnews.com/business/economy/us-china-extend-trade-truce-trump-rcna599525) (search); [Freightos, 30 Sep](https://www.freightos.com/freight-resources/china-us-truce-to-reduce-some-tariffs-and-likely-postpone-port-fees-september-30-2026-update/) |
| 6 Oct 2026 | Phase 3 of CBP's refund process for IEEPA duties (CAPE) opens. About $134.7 bn of refunds had been accepted and about $122 bn certified by mid-September. | [C.H. Robinson](https://www.chrobinson.com/en-us/resources/insights-and-advisories/client-advisories/2026q3/09-17-26-cbp-cape-phase-3-ieepa-refunds/) |
| 30 Oct 2026 | **HTS 2026 Revision 22** in effect. The rates below are from it. | [USITC HTS](https://hts.usitc.gov/) (REST release list) |
| **10 Nov 2026 (upcoming)** | **178 remaining China 301 exclusions expire** unless USTR extends them. | [Thomson Reuters](https://tax.thomsonreuters.com/blog/section-301-exclusions-expiration/) (search) |

**Primary-text detail.** The notice says China gets "12.5 percent tariffs on products of China", and Mexico gets "10 percent". Taiwan's rate is set so that, where the MFN rate is below 10%, "the sum of the MFN tariff and the Section 301 tariff shall be 10 percent".

The new duties apply on top of other subchapter III Chapter 99 duties. That includes the China 301 lists, headings 9903.88.xx. See U.S. note 52(a) in the [govinfo PDF](https://www.govinfo.gov/content/pkg/FR-2026-07-28/pdf/2026-15181.pdf).

**Note.** Holland & Knight's table shows China and Vietnam at "13%" ([H&K](https://www.hklaw.com/en/insights/publications/2026/07/and-the-tariff-beat-goes-on)). The Federal Register text says 12.5%.

**Exemptions.** The general exemption list in HTS note 52(b) has 701 provisions. Checked against the [current Chapter 99](https://hts.usitc.gov/reststop/file?release=currentRelease&filename=Chapter%2099), it contains **no Chapter 39, 76 or 94 lines and no 8518 lines**. So PMMA sheet, plastic articles, loudspeakers and lamps are all covered.

### 3.2 Duty by HTS line and origin (rates in force 31 Oct 2026; HTS Rev. 22)

- MFN rates come from the USITC HTS. China list membership comes from HTS Chapter 99, U.S. note 20 ([Chapter 99 PDF](https://hts.usitc.gov/reststop/file?release=currentRelease&filename=Chapter%2099)).
- "Forced-labour 301" (FL-301) rates are from the [Federal Register notice](https://www.govinfo.gov/content/pkg/FR-2026-07-28/pdf/2026-15181.pdf).
- Totals are simple ad valorem sums (est.). Classification of EARF's actual products needs a broker or a binding ruling.

| HTS | Item | MFN | Mexico, USMCA-qualifying | Mexico, not qualifying | China (MFN + China 301 + FL-301) | Taiwan | Vietnam |
|---|---|---|---|---|---|---|---|
| 3920.51.50 | PMMA sheet, not flexible | 6.5% | **0%** | 16.5% | 6.5 + **25 (List 2, 9903.88.02)** + 12.5 = **44.0%** | **10%** | 19.0% |
| 3926.90.99 | Other plastic articles (e.g. acrylic parts) | 5.3% | 0% | 15.3% | 5.3 + 7.5 (List 4A) + 12.5 = **25.3%** | 10% | 17.8% |
| 8518.21.00 / 8518.22.00 | Loudspeakers in enclosure | Free | 0% | 10% | 0 + 7.5 (List 4A) + 12.5 = **20.0%** | 10% | 12.5% |
| 8518.90.81 | Loudspeaker parts (if enclosures ship empty; classification to confirm) | Free | 0% | 10% | 0 + 25 (List 3) + 12.5 = **37.5%** | 10% | 12.5% |
| 8518.40.20 | Audio amplifiers | Free | 0% | 10% | 0 + 25 (List 3) + 12.5 = **37.5%** | 10% | 12.5% |
| 9405.11.80 / 9405.21.80 / 9405.42.84 | LED luminaires and lamps, not of base metal | 3.9% | 0% | 13.9% | 3.9 + 25 (List 3) + 12.5 = **41.4%** | 10% | 16.4% |
| 9405.21.60 | LED table lamps of base metal other than brass | 6% | 0% | 16% | 6 + 25 (List 3) + 12.5 = 43.5% | 10% | 18.5% |
| 9405.99.40 | Lamp parts, other | 6% | 0% | 16% | 6 + 25 (List 3) + 12.5 = 43.5% | 10% | 18.5% |
| 8504.40.95 | Power supplies and LED drivers | Free | 0% | 10% | 0 + 25 (List 3) + 12.5 = 37.5% | 10% | 12.5% |
| 8507.60.00 | Lithium-ion batteries | 3.4% | 0% | 13.4% | 3.4 + **25 (9903.91.06, from 1 Jan 2026)** + 12.5 = 40.9% | 10% | 15.9% |
| 7616.99.51 | Machined aluminium articles | 2.5% | **Section 232 applies** (§3.4) | 232 | 2.5 + 25 (List 3) + **232 at 25–50%**; FL-301 exempt because 232 applies | 2.5 + 232 | 2.5 + 232 |

- **Mexico, USMCA-qualifying.** Every dutiable line above lists "S" (USMCA) as Free in the special column; the 8518 and 8504 lines are Free at MFN anyway. Qualifying goods are also exempt from FL-301 ([Zonos](https://zonos.com/docs/guides/country-guides/united-states/section-301-forced-labor); [Honigman](https://www.honigman.com/alert-3462)).
- **Taiwan.** Per the notice, the total is 10% where MFN is below 10%. Taiwan-specific exemptions in Annex II, Part K were not checked line by line.

### 3.3 Mexico and USMCA notes

- **Rule of origin.** Plastiglas polymerises sheet in Mexico. It owned a sister MMA plant in 2011 ([2011 deck](https://mail.interstateplastics.com/docs/Plastiglas-Presentation.pdf)), so its sheet very likely originates in Mexico (est.). Get its **USMCA certification of origin** before relying on 0%.
- **Finished goods.** A speaker or lamp assembled in Mexico from Asian drivers and European amplifier modules may or may not qualify. This needs a product-specific origin analysis, which was not done here.
- **Risk.**
  - USMCA now gets an **annual** review ([DLA Piper](https://www.dlapiper.com/en-us/insights/publications/2026/07/united-states-declines-to-extend-the-usmca)).
  - Mexico is one of the 16 economies in the pending **excess-capacity 301**, and "plastics" is a named sector ([EY](https://taxnews.ey.com/news/2026-0623-us-trade-representative-initiates-section-301-investigations-into-structural-excess-capacity-comment-period-and-hearings-announced)).
  - USMCA-qualifying sheet stays the most tariff-robust import option (est.).

### 3.4 Aluminium parts and Section 232

- Derivative aluminium products under 7616.99.51 (7616.99.5130, 5140 and 5190) are listed in HTS note 19 to Chapter 99, headings 9903.85.04, .07 and .08 ([Chapter 99](https://hts.usitc.gov/reststop/file?release=currentRelease&filename=Chapter%2099)).
- Since 6 Apr 2026, 232 duty is charged on **full customs value** ([GHY](https://www.ghy.com/trade-compliance/us-adjusts-section-232-tariffs-on-aluminum-steel-and-copper-full-customs-value-now-applies/)):
  - **50%** for articles made entirely or almost entirely of metal (Annex I-A);
  - **25%** for derivatives (Annex I-B).
- 232 goods are exempt from FL-301 ([Honigman](https://www.honigman.com/alert-3462)). But Chinese 7616.99.51 is also on **List 3** ([Chapter 99](https://hts.usitc.gov/reststop/file?release=currentRelease&filename=Chapter%2099)).
- **Conclusion:** turn and anodise aluminium in the US.

### 3.5 In litigation, pending or about to change

- **FL-301 challenged at the Court of International Trade (CIT).**
  - Burlap and Barrel and Collective Horology filed a proposed class action.
  - Learning Resources, hand2mind and five other businesses argue the tariffs are a pretext ([Morgan Lewis, 27 Jul 2026](https://www.morganlewis.com/pubs/2026/07/us-administration-rebuilds-global-tariff-program-under-section-301)).
  - Keep entry records in case refunds follow.
- **Section 122.** Litigation continues at the Federal Circuit ([Honigman](https://www.honigman.com/alert-3462)).
- **Existing China 301 lists.** The Supreme Court declined to review the appeals decision upholding them ([Honigman](https://www.honigman.com/alert-3462)).
- **Excess-capacity 301.** Results were pending as of late July, and any new duties would stack on FL-301 ([H&K](https://www.hklaw.com/en/insights/publications/2026/07/and-the-tariff-beat-goes-on)). No outcome was found by 31 Oct; verify, because the search ran out.
- **US–China.**
  - The truce runs to **10 Jan 2027** ([Freightos](https://www.freightos.com/freight-resources/china-us-truce-to-reduce-some-tariffs-and-likely-postpone-port-fees-september-30-2026-update/)).
  - 178 China 301 exclusions expire **10 Nov 2026** ([Thomson Reuters](https://tax.thomsonreuters.com/blog/section-301-exclusions-expiration/)).
  - The truce text mentions cutting tariffs on "$30B" of trade to MFN levels "pending legal procedures"; which products are covered is unknown ([Freightos](https://www.freightos.com/freight-resources/china-us-truce-to-reduce-some-tariffs-and-likely-postpone-port-fees-september-30-2026-update/)).
- **De minimis.** Still suspended, so prototype parts from Asia pay full duty ([GHY](https://www.ghy.com/trade-compliance/us-10-section-122-tariff-in-effect-feb-24-ieepa-tariffs-directed-to-wind-down-de-minimis-suspension-continues/); [Dutylane](https://dutylane.com/tariff/policy/de-minimis)).
- **Not checked.** Whether any Section 232 semiconductor measure reaches imported amplifier modules or LED drivers. The FL-301 exemption list mentions "semiconductors" among 232 categories ([Honigman](https://www.honigman.com/alert-3462)).

---

## 4. Logistics to San Francisco

### 4.1 What a "pallet minimum" weighs and holds

PMMA weighs about 1.19 kg/m² per millimetre of thickness (est., from density). This is consistent with Polycast's **6.16 lb/ft² for 1.000"** sheet ([Polycast](https://modernplastics.com/wp-content/uploads/2015/03/Polycast-General-Catalog.pdf)), and with Plastiglas's **43.5 kg for a 12 mm 1.2×2.4 m sheet** ([datasheet](https://new.avanceytec.com.mx/img/cms/0100-0010-0050/LAMINA-DE-ACRILICO-PLASTIGLAS-CRISTAL-VERDE-Y-COLORES.pdf)).

| Thickness | One 4×8 ft sheet (est.) | Sheets in 2,500 lb (est.) |
|---|---|---|
| 3 mm | 10.6 kg / 23 lb | ~107 |
| 6 mm | 21.2 kg / 47 lb | ~53 |
| 10 mm | 35.4 kg / 78 lb | **~32** |
| 20 mm | 70.8 kg / 156 lb | ~16 |
| 25 mm | 88.4 kg / 195 lb | ~13 |
| 30 mm | 106 kg / 234 lb | ~11 |

**Horn (est.).** For a 630×366×238 mm horn, a blank of about 1.2 × 0.95 m (≈1.14 m²) allows for the draw and the clamp. At 10 mm that is ≈13.6 kg of sheet per horn. Two horns per set over 50 sets come to ≈1,360 kg (≈3,000 lb). **The horn colour alone would consume more than one 2,500 lb batch.**

**All eight colours (est.).** Eight colours at 2,500 lb each is 20,000 lb (≈9.1 t), or ≈256 sheets of 10 mm 4×8.

### 4.2 Mexico to San Francisco (estimates; no public quotes found)

| Origin | Route and road distance (est.) | Door-to-door time (est.) | Cost logic (est.) |
|---|---|---|---|
| Tijuana | Otay Mesa crossing, then I-5; ≈830 km / 515 mi (760 km great-circle) | 1–2 days, plus border time | ATRI's 2025 truck operating cost is **$2.336/mile** ([ATRI, published 15 Jul 2026](https://truckingresearch.org/atri-research/operational-costs-of-trucking/)). That gives ≈$1,200 at cost for a full truck, before margin, drayage and brokers on both sides. |
| Plastiglas Ocoyoacac / Mexico City area | Via Laredo ≈3,900 km, or via Nogales ≈3,500 km (great-circle 3,030 km) | **5–8 days** full truckload (FTL); 7–12 days less-than-truckload (LTL) or consolidated | US leg Laredo to SF ≈1,700 mi × $2.34 ≈ **$4,000** at cost, plus the Mexican leg and crossing. A single pallet goes LTL for far less but more slowly. |
| Plaskolite Matamoros | Via Brownsville or Laredo; ≈3,300+ km | 5–7 days | Same logic as above |

- **Border.** Otay Mesa's commercial lanes run 6 am–10 pm, and Laredo's World Trade Bridge 7 am–midnight ([CBP Border Wait Times](https://bwt.cbp.gov/), snapshot 30 Oct 2026).
- **Practical shortcut.** Buy through **Piedmont**, which already runs inventory programmes stocking CHEMCAST at each branch ([Piedmont](https://www.piedmontplastics.com/suppliers/plastiglas-de-mexico)). Ask whether an EARF custom batch can ride on the Union City replenishment.

### 4.3 Asia to San Francisco (late October 2026)

- **Full containers.** Drewry's World Container Index (WCI) had Shanghai to Los Angeles at **$7,514 per 40 ft (FEU)** on **29 Oct 2026**, down 6% on the week; the composite was $4,429 ([Drewry](https://www.drewry.co.uk/supply-chain-advisors/supply-chain-expertise/world-container-index-assessed-by-drewry)). Freightos's FBX01 index (Asia to US West Coast) was **$8,368/FEU** on 28 Oct ([Freightos](https://www.freightos.com/freight-resources/union-approves-la-long-beach-port-strike-container-rates-still-under-pressure-october-28-2026-update/)).
- **Part loads (LCL).** Freightos says LCL per cubic metre "is often about double" the full-container (FCL) rate ([Freightos route page](https://www.freightos.com/shipping-routes/shipping-from-china-to-the-united-states/)). That implies roughly **$220–250 per m³** for the main leg, plus origin and destination fees (est., from $7.5–8.4k ÷ ~67 m³ × 2).
- **Air.** Freightos's air index (FAX), China to North America, was **$7.13/kg** on 28 Oct 2026 ([Freightos](https://www.freightos.com/freight-resources/union-approves-la-long-beach-port-strike-container-rates-still-under-pressure-october-28-2026-update/)). Freightos's undated rules of thumb are lower: express about $5/kg under ~150 kg, and air about $3/kg for 150–500 kg ([route page](https://www.freightos.com/shipping-routes/shipping-from-china-to-the-united-states/)).
- **Transit.** Ocean is about 30–40 days door to door; LCL adds 1–2 weeks; air about 8–10 days; express about 3 days ([route page](https://www.freightos.com/shipping-routes/shipping-from-china-to-the-united-states/)). 2026 averages are 19–47 days for FCL and 22–50 days for LCL door to door, and 4–11 days for air ([Freightos calculator](https://www.freightos.com/freight-resources/transit-time-calculator/)).
- **Risks.**
  - A watchmen's union at Los Angeles/Long Beach (LA/LB) authorised a strike that "could be called as soon as November 1st" ([Freightos](https://www.freightos.com/freight-resources/union-approves-la-long-beach-port-strike-container-rates-still-under-pressure-october-28-2026-update/)).
  - Congestion in the Far East is "tying up more than 8% of global capacity" ([Freightos, 30 Sep](https://www.freightos.com/freight-resources/china-us-truce-to-reduce-some-tariffs-and-likely-postpone-port-fees-september-30-2026-update/)).
- **Heavy sheet versus parts (est.).**
  - A 2,500 lb pallet of Chinese sheet at listing prices of $1.5–2.5/kg ([Made-in-China](https://www.made-in-china.com/factory/acrylic-solid-sheet.html)) is worth ≈$1,700–2,800 FOB. By air at $7.13/kg it would cost ≈$8,100 to fly. **Sheet goes only by sea.**
  - Finished, higher-value parts can justify air.

### 4.4 Summary

| From | Sheet: cost and time (est.) | Finished parts: cost and time (est.) | Duty (§3.2) |
|---|---|---|---|
| California and US distributors | Local delivery, 1–3 days | Days | 0 |
| Mexico, Tijuana | ≈$1–2k per truck; 1–2 days | Same | 0 if USMCA, else MFN + 10% |
| Mexico, Mexico City area | ≈$4–6k+ per truck; 5–8 days, or a cheaper pallet by LTL | Same | Same |
| China / Taiwan / Vietnam | $7.5–8.4k per FEU, or ~$220–250/m³ LCL; 30–50 days | Air at ~$7/kg, 8–10 days | China 20–44%, Taiwan 10%, Vietnam 12.5% + MFN |

---

## 5. Turnkey partners and specialists

### 5.1 United States

| Firm | Where | Why relevant |
|---|---|---|
| [Reynolds Polymer Technology](https://www.reynoldspolymer.com/) | Grand Junction, CO; Rayong, Thailand | <ul><li>Design and engineering, casting, **bonding**, **forming**, machining, finishing and QC.</li><li>OEM work; 35+ years.</li><li>[Forming](https://www.reynoldspolymer.com/capabilities/forming/): spheres and **"trumpet shapes"** in proprietary large ovens.</li><li>[Thin R-Cast](https://www.reynoldspolymer.com/commercial/r-cast-acrylic-thin-gauge-sheet/) stock colours.</li><li>[Thick R-Cast](https://www.reynoldspolymer.com/commercial/r-cast-acrylic-thick-gauge-sheet/) up to 102 mm.</li><li>**First call for the horn, domes and thick blocks.**</li></ul> |
| [Acrylic Design Associates](https://www.acrylicdesign.com/) ("A Taylor Company") | Minneapolis, MN | <ul><li>Design and engineering, prototyping, machining, laser, **vacuum and drape forming**, production, warehousing and fulfilment.</li><li>OEM products; ~50 years; 42,223+ projects.</li></ul> |
| [Plexi-Craft](https://www.plexi-craft.com/) | New York and Chicago | <ul><li>Acrylic furniture "hand-crafted … for over 60 years".</li><li>Custom orders and a trade programme.</li><li>A benchmark for furniture-grade cementing and polish.</li></ul> |
| [Cutting Edge Plastics](https://www.cuttingedgeplastics.com/) | Laguna Hills, CA | <ul><li>In-house CNC, **polishing**, bending, assemblies and museum vitrines.</li><li>"One-off prototypes through full production runs"; 20+ years.</li><li>Names SpaceX and Medtronic as past partners.</li></ul> |
| [Emco Industrial Plastics](https://www.emcoplastics.com/) | New Jersey | Drape and vacuum forming; "museum quality gluing" |
| [Ray Products](https://www.rayplastics.com/) | Ontario, CA | <ul><li>Heavy-gauge pressure forming up to 10×6 ft; vacuum forming 10×18 ft.</li><li>ISO 9001:2015; robotic trimming.</li><li>Ask about cast-acrylic experience.</li></ul> |
| US casters for custom colour | [Spartech Polycast](https://spartech.com/product-type/cell-cast-acrylic) (extensive colour database, custom quoted); [ACRYLITE](https://www.acrylite.co/) (Röhm; lists Polyvantis Sanford LLC, Sanford, ME) | Get their minimums to compare with Plastiglas |

### 5.2 Mexico

- **Turnkey.** No turnkey contract manufacturer for acrylic products was verified.
- **Candidates for a pilot part:**
  - [Acrylart](https://acrylart.com.mx) (Tijuana): design to delivery, CNC and laser, ships to the US.
  - [Acriland](https://www.acriland.com) (Mexico City): consumer-brand POP; CNC, laser, polishing, bending, assembly.
  - [Acrílicos Profesionales de Monterrey](https://acrilicosprofesionales.com): thermoforming.
- **Captive cell.** For an EARF-run cell at higher volume, use a shelter company ([Tecma](https://www.tecma.com/), [IVEMSA](https://www.ivemsa.com/)).

### 5.3 Asia

- [JAYI](https://www.jayiacrylic.com/): furniture and luxury displays.
- [Wetop](https://wetopacrylic.com/): ±0.2 mm, thermoforming, diamond polishing, ISO 9001.
- [Acrylictogo](https://acrylictogo.com/buyers-faq/): integrates LED and metal parts.
- For thick work: Reynolds' Rayong site, and [Nippura](https://www.nippura.com/) in Japan.

### 5.4 The horn (10 mm cast, ~630×366×238 mm) and domes

- **Forming data.**
  - Forming temperature is **140–180 °C** ([Plastiglas datasheet](https://new.avanceytec.com.mx/img/cms/0100-0010-0050/LAMINA-DE-ACRILICO-PLASTIGLAS-CRISTAL-VERDE-Y-COLORES.pdf)), or about 320 °F ([Polycast](https://modernplastics.com/wp-content/uploads/2015/03/Polycast-General-Catalog.pdf)).
  - The sheet shrinks ≈2% and thickens ≈4% on heating ([Polycast](https://modernplastics.com/wp-content/uploads/2015/03/Polycast-General-Catalog.pdf)).
- **Engineering notes (est.).**
  - Depth over width is 238/366 ≈ 0.65, so expect marked thinning at the deepest corners. Specify a minimum wall in the drawing.
  - Form over a **male (drape) mould** if the inside surface is acoustically critical.
  - Fall back to two formed halves cemented with polymerising cement if one-piece yield is poor.
- **Who.** Ask Reynolds first (trumpet shapes and spheres), then ADA and Emco (drape and vacuum).

---

## 6. Recommendation

### 6.1 Prototypes: California, stock colours, no minimums

- **Sheet.** Stock CHEMCAST from Piedmont in Union City or from TAP, plus Reynolds stock colours. Reynolds' thin-gauge stock colours ([Reynolds](https://www.reynoldspolymer.com/commercial/r-cast-acrylic-thin-gauge-sheet/)):
  - opaque Black 2025, Blue 2114, Yellow 2037, Green 2108, Red 2157 and White 7420;
  - transparent Gray 2064 and Bronze 2412;
  - fluorescent colours.
- **Fabrication.**
  - In-house, or Cutting Edge Plastics.
  - Horn and domes: Reynolds or ADA.
  - Aluminium: US turning and anodising (§3.4).
  - Electronics: in-house in San Francisco.
- **Why.** Zero duty, turnaround in days, and no colour risk while the design is still moving.

### 6.2 About 10 sets: still California; start the colour programme

1. **Freeze the palette as a colour × thickness × sheet-size matrix.** Aim for **one thickness per custom colour**, because the 2006 minimum applies per colour, size and thickness ([Chemcast catalogue](https://courses.cit.cornell.edu/mae2250/Emerson/Chemcast_Acrylic_brochure.pdf)). Keep 20–30 mm blocks in clear or stock colours where you can.
2. **Through Piedmont, ask Plastiglas for:**
   - **colour-bank matches** to the eight targets;
   - the **current** custom minimum;
   - whether "customized short orders" ([Piedmont](https://www.piedmontplastics.com/suppliers/plastiglas-de-mexico)) can cover a colour;
   - whether one batch can be split across thicknesses or sizes;
   - whether Piedmont would co-stock an EARF colour.
3. **Ask Plaskolite** for its OPTIX G custom-colour minimum ([Plaskolite](https://plaskolite.com/catalog/optix-g-series-cell-cast-colored-acrylic)), and **Spartech/Polycast** for theirs ([Spartech](https://spartech.com/product-type/cell-cast-acrylic)).
4. **Send a benchmark RFQ in Asia.** Use one Taiwanese caster (10% duty) and two Chinese casters (for example Alands, which mixes colours within 1 t, and Shengdalong). Specify:
   - cell cast, 100% virgin MMA;
   - ΔE limit at production thickness;
   - D4802 tolerance class;
   - paid samples.
5. **Visit Plastimagen (10–13 Nov 2026, Mexico City)** to meet Plastiglas and screen fabricators.

### 6.3 About 50 sets: Mexican sheet, Californian fabrication

- **Material.** Plastiglas custom colours, USMCA-certified, so 0% duty and outside FL-301 ([Federal Register notice](https://www.govinfo.gov/content/pkg/FR-2026-07-28/pdf/2026-15181.pdf)). Deliver through Piedmont.
- **Absorbing the minimum.** Assign custom colours to the **high-volume parts first**. The horn colour can use a whole batch: ≈3,000 lb across 50 sets (est.).
- **Making.** Fabrication, cementing, annealing and assembly in California. Horn and domes from Reynolds, or a qualified thermoformer. Aluminium in the US.
- **Mexico option.** Pilot a flat CNC-and-polish part in **Tijuana**, 1–2 days from San Francisco (est.). Scale Mexican fabrication only once a shop proves it can cement and finish to standard.
- **Asia.** Use only if a **Taiwanese** source proves itself on colour and quality. Do not move to China for now:
  - 25–44% duty on acrylic parts, sheet and lamps (§3.2);
  - a pending excess-capacity 301;
  - the truce ending 10 Jan 2027;
  - 30–50 days of transit.

### 6.4 Cutting the custom-colour minimum: tactics and their effect (est.)

| Tactic | Effect on 8 colours × 2,500 lb = 20,000 lb |
|---|---|
| Prototype in stock colours | No minimum before the design is frozen |
| Match to the Plastiglas colour bank, or adopt a standard colour for 1–3 of the 8 | Each standard colour adopted removes a 2,500 lb batch and the development cost |
| One thickness and size per colour | Avoids multiplying the minimum by the number of thicknesses |
| Custom colours on high-volume parts only; clear, black or stock colours on low-volume and hidden parts | Fewer custom batches, and each one used up faster |
| Share the batch (Piedmont/TAP co-stock, or a partner brand) | A partner absorbs part of each 2,500 lb; to negotiate |
| Low-minimum Asian caster for 1–3 low-volume colours (10–20 sheets per the generic reference; 1 t mixable at Alands) | Smaller batches, but duty of 10% (Taiwan), 19% (Vietnam) or 44% (China) on sheet, plus 30–50 days |
| Accept the minimum as inventory | 2,500 lb of 10 mm ≈ 32 sheets of 4×8; budget storage; the 100% cancellation rule applies |

### 6.5 Questions to put in every RFQ

- Cell cast or continuous cast? Percentage of virgin MMA? Certificate of analysis?
- Thickness tolerance class (D4802), or close-tolerance option?
- Minimum per colour, and is it per thickness or per size? Colour fee? Lead time? Retained colour standard?
- ΔE limit, light source and measurement thickness.
- Annealing practice: after machining and before cementing? Which polymerising cement? Joint test samples?
- Thermoforming: oven size, maximum blank, mould material, gauge experience with 10 mm cast, wall-thickness reporting.
- USMCA certification of origin (Mexico), or country of origin and HTS line (Asia).

---

## Not verified, and open questions

- The current custom-colour minimum at Plastiglas, Plaskolite, Spartech and Reynolds. Only the 2006 Plastiglas policy was found.
- Taiwanese and Vietnamese casters and fabricators (search budget exhausted).
- Mexican fabricators' real capability in polymerising cement, annealing and thick forming.
- Mexico–US freight quotes; all such figures above are estimates.
- USMCA origin for EARF's finished products.
- Any Section 232 semiconductor duty on amplifier modules.
- The outcome of the excess-capacity 301 after July 2026.
