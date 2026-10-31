# R3: EARF US compliance path (Tropos, Hemisphere, Core, Mantle)

Prepared 31 Oct 2026 for EARF (San Francisco). Scope: the cheapest credible route to the first US direct-to-consumer sales, with costs and timelines.

**How to read this.** Every factual claim links to its source. Figures marked **(est.)** are EARF planning estimates, not published prices; labs and NRTLs rarely publish listing fees. This is research, not legal advice. Have counsel or the chosen lab confirm the items in section 10 before committing money.

**Research limits.** The shared web-search budget ran out partway through. After that, only known primary-source URLs and links found on them were fetched directly. Several sites refused automated access: eCFR (bot check), leginfo.legislature.ca.gov, intertek.com, copper.org, the Mike Holt forums and DTSC. Those checks were not bypassed. Equivalent primary text came from Cornell LII where it exists.

---

## 0. Bottom line

1. **No federal law found in this research requires UL, ETL or CSA listing to sell these four products to consumers.**
   - OSHA's NRTL rule binds employers, not manufacturers ([OSHA NRTL FAQ](https://www.osha.gov/nationally-recognized-testing-laboratory-program/frequently-asked-questions)).
   - UL standards are voluntary unless a regulation incorporates them ([Compliancegate](https://www.compliancegate.com/led-lighting-safety-standards-united-states/)).
   - Listing becomes effectively mandatory in three places:
     - **Hardwired luminaires**, under the electrical code at installation (NEC 410.6, [IAEI](https://iaeimagazine.org/2010/november2010/does-ul-list-led-tube-lamps-and-led-edison-screw-type-base-lamps/)).
     - **The City of Los Angeles**, which requires approval of all electrical equipment "sold, installed or advertised for sale" in the city ([LADBS](https://dbs.lacity.gov/node/2559)).
     - **Retailers, marketplaces and insurers**.
2. **The legally mandatory items are small and cheap:**
   - FCC Part 15B Supplier's Declaration of Conformity (SDoC) for all four products, about **$1.5–3.5k each** ([Compatible Electronics cost guide](https://www.celectronics.com/Resources/EMC-Testing-Cost-Guide)).
   - For **Core**: the federal battery-charger standard, DOE certification and a California MAEDbS listing ([10 CFR 430.32(z)](https://www.law.cornell.edu/cfr/text/10/430.32), [20 CCR 1606](https://www.law.cornell.edu/regulations/california/20-CCR-1606), [20 CCR 1608](https://www.law.cornell.edu/regulations/california/20-CCR-1608)).
   - For **Core's cells**: UN 38.3 documentation for shipping ([49 CFR 173.185](https://www.law.cornell.edu/cfr/text/49/173.185)).
   - California battery rules: Core avoids the **SB 1215** fee if its cells stay user-removable, but those cells fall under the **AB 2440** battery stewardship scheme.
   - **Prop 65**, but only once EARF has 10 or more employees ([CA AG](https://oag.ca.gov/prop65/faq)).
   - CPSC general duties, plus **Reese's Law** if the Tropos remote uses a coin or button cell ([16 CFR 1263](https://www.law.cornell.edu/cfr/text/16/part-1263)).
3. **Cheapest credible path:**
   - FCC-test all four at a US lab.
   - Ship Hemisphere **plug-in first** with a listed Class 2 driver.
   - Put a listed external supply on Mantle and Core.
   - Use lead-free brass and an AAA remote on Tropos.
   - Do the DOE and CEC filings for Core.
   - Bind product-liability insurance.
   - NRTL-list each product before scaling past roughly 100 units, or earlier if a retailer or Los Angeles demand it.
   - For the **hardwired Hemisphere**, use UL's **Limited Production Certification for lighting**: one inspection visit, no recurring fees ([UL](https://www.ul.com/offerings/limited-production-certification-lighting-products)).
4. **Budget (est.):**
   - About **$18–46k** to first sales across all four products.
   - About **$28–70k** more to NRTL-list all four.
   - About **$5–20k a year** ongoing.
   - Section 9 gives the investor-deck line.

---

## 1. What is mandatory and what is market-driven

### 1.1 FCC Part 15 (mandatory, federal)

**What triggers it.** A *digital device* is any unintentional radiator that "generates and uses timing signals or pulses at a rate in excess of 9,000 pulses (cycles) per second" using digital techniques ([47 CFR 15.3(k)](https://www.law.cornell.edu/cfr/text/47/15.3)). Tropos (DSP) and Core (MCU and charger) qualify, and so does Mantle if its motor speed control is digital. "Other Class B digital devices" and "all other devices" are authorised by **SDoC** (or certification) before marketing ([47 CFR 15.101](https://www.law.cornell.edu/cfr/text/47/15.101)).

**LED lighting (Hemisphere).** FCC staff guidance KDB 640677 treats RF LED lighting devices as Part 15 *unintentional radiators*. They must meet conducted and radiated limits, with radiated emissions measured from at least 30 to 1000 MHz ([ARRL summary of KDB 640677](https://www.arrl.org/news/fcc-s-oet-clarifies-emissions-compliance-testing-for-rf-led-lighting-devices); [In Compliance](https://incompliancemag.com/fcc-clarifies-emissions-requirements-for-led-lights/)).

**Mantle.** If Mantle used a purely analogue DC motor with no digital logic, it would be an *incidental radiator*; the FCC's own examples include "dc motors" ([15.3(n)](https://www.law.cornell.edu/cfr/text/47/15.3)). An incidental radiator needs no equipment authorisation, only good engineering practice. A crystal or MCU speed control makes Mantle a digital device.

**IR remote.** Infrared is not "RF energy", which the FCC defines as 9 kHz to 3,000,000 MHz ([15.3(u)](https://www.law.cornell.edu/cfr/text/47/15.3)). A 940 nm IR LED works at about 320 THz. The remote's microcontroller can still be a digital device. Battery-only devices whose highest frequency is below 1.705 MHz are exempt, but not if they can run from AC power ([15.103(h)](https://www.law.cornell.edu/cfr/text/47/15.103)).

**Exemptions that do not help.** The appliance exemption covers devices "utilized exclusively in an appliance, e.g., microwave oven, dishwasher" ([15.103(d)](https://www.law.cornell.edu/cfr/text/47/15.103)), which does not fit hi-fi or lamps. Core charges and probably runs while connected to its AC adapter, so the 1.705 MHz battery-only exemption is unlikely to apply ([15.103(h)](https://www.law.cornell.edu/cfr/text/47/15.103)).

**Modules do not exempt the end product.** Subassemblies are not tested on their own, "unless marketed as part of a system", in which case the system must comply ([15.101(e)](https://www.law.cornell.edu/cfr/text/47/15.101)). Hypex says end-product compliance "falls to the manufacturer of said end product" ([Hypex Fusion manual](https://cdn.hypex.nl/media/df/df/c2/1678368740/Fusion%20Manual%20R4.pdf)). Bought-in **external switching power supplies** are themselves Class B devices needing their own SDoC ([15.101](https://www.law.cornell.edu/cfr/text/47/15.101)), so buy ones that already have it.

**Paperwork.**
- Compliance information goes in the manual or on a separate sheet: product ID, compliance statement, and the **US** responsible party's name, address and contact details ([47 CFR 2.1077](https://www.law.cornell.edu/cfr/text/47/2.1077)).
- The device carries the two-condition Part 15 statement ([15.19](https://www.law.cornell.edu/cfr/text/47/15.19)).
- The FCC logo is optional for SDoC ([Compliancegate](https://compliancegate.com/fcc-unintentional-radiators)).
- EARF in San Francisco can be the responsible party.

**Pre-orders are allowed.** Conditional sales are permitted with a prominent disclosure that delivery depends on authorisation. EARF must keep ownership and records for 60 months, and nothing may be physically delivered until SDoC testing is done ([47 CFR 2.803](https://www.law.cornell.edu/cfr/text/47/2.803)).

**Lab choice.** Today an accredited lab is **not** required for SDoC ([Compliancegate](https://compliancegate.com/fcc-unintentional-radiators); [Compliance Testing LLC](https://compliancetesting.com/?p=3501)). The FCC's pending Third FNPRM, scheduled for vote on 29 Oct 2026, proposes requiring SDoC equipment to be tested by recognised or accredited labs. Labs in non-reciprocal countries would lose recognition after a transition ending 1 Dec 2028 ([DLA Piper](https://www.dlapiper.com/en/insights/publications/2026/10/fcc-to-vote-on-limiting-equipment-authorization-testing)). The vote outcome was not confirmed in this research. Testing at an accredited US lab avoids the issue either way.

### 1.2 Safety listing (NRTL): when it is actually required

| Driver | What it says | Applies to EARF |
|---|---|---|
| Federal/OSHA | OSHA's authority "is limited to employers"; OSHA does not require manufacturers to certify products ([OSHA FAQ](https://www.osha.gov/nationally-recognized-testing-laboratory-program/frequently-asked-questions)) | Only when a business customer uses the product at work |
| NEC 410.6 (code) | Since NEC 2008, "all luminaires and lampholders" must be listed ([IAEI](https://iaeimagazine.org/2010/november2010/does-ul-list-led-tube-lamps-and-led-edison-screw-type-base-lamps/)). California's 2025 Electrical Code (Title 24 Part 3) took effect 1 Jan 2026 ([DGS](https://www.dgs.ca.gov/bsc/codes)) and adopts the 2023 NEC ([DGS 2025 CEC text](https://www.dgs.ca.gov/-/media/Divisions/BSC/02-Codes/2025-CEC_2025-07-01.docx)) | **Hardwired Hemisphere**: an inspector can reject an unlisted fixture. Plug-in lamps are not part of a permitted installation, so in practice they are not inspected (inference). |
| City of Los Angeles | "All electrical equipment sold, installed or advertised for sale in the City of Los Angeles" must be approved by LADBS ([LADBS](https://dbs.lacity.gov/node/2559)). A recognised-lab listing mark satisfies this; otherwise LADBS's own lab approval is needed ([LADBS bulletin P/EC 2020-013](https://dbs.lacity.gov/sites/default/files/efs/forms/pc17/ib-p-ec-2020-013-electrical-equipment-approval-requirements.pdf)) | All four if shipped to LA addresses. How LA enforces this against out-of-city online sellers is unclear. |
| Washington State | Listing applies to equipment "used in such installations"; utilisation equipment is exempt unless the 1993 NEC required listing. The general sale ban covers only spa and pool equipment ([RCW 19.28.010](https://app.leg.wa.gov/RCW/default.aspx?cite=19.28.010)) | Low risk for plug-in products |
| Marketplaces and retailers | Marketplaces such as Amazon "might require compliance with the relevant standard" ([Compliancegate](https://www.compliancegate.com/led-lighting-safety-standards-united-states/)) | Market-driven |
| Insurers | Premiums depend on product type, supply-chain position and claims ([Insureon](https://www.insureon.com/small-business-insurance/product-liability/cost)). Applications for consumer electronics commonly ask about certification (inference, not sourced) | Market-driven |

**Any NRTL mark carries the same weight.** OSHA "does not mandate the use of a specific NRTL mark" and treats NRTLs recognised for the same standard as capable of certifying to it ([OSHA FAQ](https://www.osha.gov/nationally-recognized-testing-laboratory-program/frequently-asked-questions)). A cheaper NRTL is legally as good as UL.

### 1.3 Which standard applies to which product

**Tropos and Mantle: UL 62368-1** (audio/video and ICT). UL 62368-1 replaced UL 60065 and UL 60950-1 for new certifications from 20 Dec 2020 ([Electronic Design](https://electronicdesign.com/home/article/21199571/new-external-power-supply-standards-62368-to-replace-60950-and-60065-update); [Mouser](https://www.mouser.in/applications/62368-1-safety-transition-critical-update/)).

Hypex's own installation rules for Tropos are strict ([Hypex manual](https://cdn.hypex.nl/media/df/df/c2/1678368740/Fusion%20Manual%20R4.pdf)):
- The FusionAmp "must be earthed".
- Its compartment "should be constructed of V-1 class material", with V-0 layers either side of the module, or be V-0 throughout.
- Conductive enclosure parts should be bonded to protective earth.

The acrylic cabinet therefore cannot be the amp's fire enclosure unless the specific acrylic grade carries a V-1 or V-0 rating. This was not verified; check the sheet's UL 94 "yellow card".

**Hemisphere, plug-in: UL 153** (Portable Electric Luminaires). **Hemisphere, hardwired: UL 1598** (Luminaires). Both use **UL 8750** for LED drivers and modules: Intertek describes UL 8750 as used together with UL 1598 when certifying an LED luminaire ([Intertek](https://www.intertek.com/lighting/standards/ul-8750/)). Class 2 power units fall under **UL 1310**, "Class 2 Power Units" ([OSHA BACL scope](https://www.osha.gov/nationally-recognized-testing-laboratory-program/BACL)). Whether a cord-connected pendant is evaluated under UL 153 or UL 1598 should be confirmed with the NRTL (section 10).

**Core: UL 153 with Supplement SA**, added 26 Sep 2022 for luminaires powered "only from integral single-use or rechargeable batteries". It explicitly covers tabletop luminaires, and lithium cells must meet **UL 1642 or UL 62133-2** ([UL](https://www.ul.com/news/ul-153-expanded-add-battery-operated-portable-luminaires)).
- The 13th edition of 3 Apr 2024 clarified power-supply requirements for USB-powered portable luminaires ([LightNOW](https://www.lightnowblog.com/2024/12/ul-153-revised-for-portable-lamps/)).
- A 2025 revision, effective 3 Apr 2027, adds three things ([Intertek SUN](https://w3inte.intertek.com.mx/siteassets/resources/sun/2025/ul-153-sun-rev-2-24-2025-ed-4-3-2027.pdf)):
  - photobiological assessment for battery-operated luminaires;
  - rules for LED portable luminaires with cords thinner than 18 AWG;
  - UL 4200A accessibility for any coin cells.

**Battery standards:**
- **UL 2054** ("Household and Commercial Batteries") is the pack-level standard ([OSHA UL scope](https://www.osha.gov/nationally-recognized-testing-laboratory-program/ul)).
- **UL 1642 and UL 62133-2** apply to cells.
- None is legally required for sale. They become de facto required inside a UL 153 listing.

### 1.4 Batteries and shipping (Core; Tropos remote)

**UN 38.3 (mandatory, DOT).** Every lithium cell or battery type must pass UN 38.3 ([49 CFR 173.185](https://www.law.cornell.edu/cfr/text/49/173.185)):
- Batteries are tested even if their cells already passed.
- Manufacturers *and later distributors* must "make a test summary available".
- Button cells installed in equipment are exempt from the summary requirement.

The cheap route is to buy branded cells and get the cell maker's test summary. If EARF builds its own multi-cell *pack*, the pack needs its own UN 38.3 test.

**Shipping exceptions.** The small-battery exception covers lithium-ion cells of at most 20 Wh and batteries of at most 100 Wh ([173.185(c)](https://www.law.cornell.edu/cfr/text/49/173.185)). Core's cells are about 5.7 Wh each (17 Wh ÷ 3). There is also a "low production run" exception for 100 cells or fewer a year. It requires Packing Group I packaging and bars passenger aircraft, so it is not useful for direct-to-consumer shipping ([173.185(e)](https://www.law.cornell.edu/cfr/text/49/173.185)).

**USPS (Packaging Instruction 9D)** ([USPS Pub. 52](https://pe.usps.com/text/pub52/pub52apxc_032.htm)):
- Lithium-ion batteries in or with equipment can go by air or surface.
- A mailpiece may hold at most 8 cells or 2 batteries.
- **No lithium mark is needed for "no more than four lithium-ion cells or two batteries installed in the equipment"**.
- Cells packed loose *with* the lamp need the UN3481 mark.
- Ship Core with its cells installed.

### 1.5 Energy rules (federal DOE and California Energy Commission)

**Core's embedded charger is regulated.** DOE defines a battery charger as including "battery chargers embedded in other consumer products" ([10 CFR 430.2](https://www.law.cornell.edu/cfr/text/10/430.2)). Since 13 Jun 2018 every charger must meet a maximum unit energy consumption, or UEC ([430.32(z)](https://www.law.cornell.edu/cfr/text/10/430.32)). At Ebatt ≈ 17 Wh:
- 3 cells in parallel (3.2 V, Class 2, below 4 V): limit is 0.1440×17+2.95 ≈ **5.40 kWh/yr**.
- 3 cells in series (9.6 V, Class 3, 4–10 V): limit is 0.0255×17+1.16 ≈ **1.59 kWh/yr**.

Manufacturers must test a sample and file certification reports ([10 CFR 429.39](https://www.law.cornell.edu/cfr/text/10/429.39)).

**External power supplies (Core's USB-C adapter, Mantle's adapter)** must meet **Level VI**, in force since 10 Feb 2016 ([430.32(w)](https://www.law.cornell.edu/cfr/text/10/430.32)). Under DOE rules, to "manufacture" includes to **import**, so if EARF imports adapters itself, EARF owns the DOE certification ([10 CFR 430.2](https://www.law.cornell.edu/cfr/text/10/430.2)).

**Hemisphere's LED driver is outside the EPS standard.** DOE's EPS definition excludes devices designed only to power LEDs ([430.2](https://www.law.cornell.edu/cfr/text/10/430.2)).

**California Title 20:**
- **Core:**
  - Federally regulated battery chargers must be filed in **MAEDbS** ([20 CCR 1606](https://www.law.cornell.edu/regulations/california/20-CCR-1606), Table X).
  - An appliance in scope may be sold in California only if it appears in MAEDbS ([20 CCR 1608](https://www.law.cornell.edu/regulations/california/20-CCR-1608)).
  - Each unit must be marked with brand, model and date of manufacture (year plus month) ([20 CCR 1607(b)](https://www.law.cornell.edu/regulations/california/20-CCR-1607)).
- **Adapters:** external power supplies are excepted from the MAEDbS filing but must carry the federal efficiency marking ([1606](https://www.law.cornell.edu/regulations/california/20-CCR-1606); [1607(d)(8)](https://www.law.cornell.edu/regulations/california/20-CCR-1607)).
- **Tropos and Mantle are out of scope.** Title 20 covers "compact audio products", which by definition include "an amplifier and radio tuner" ([20 CCR 1602](https://www.law.cornell.edu/regulations/california/20-CCR-1602); [1601(v)](https://www.law.cornell.edu/regulations/california/20-CCR-1601)). Neither product has a tuner.
- **Hemisphere is out of scope.** Title 20's luminaire category covers only torchieres, metal halide, under-cabinet and GU24 luminaires ([1601(n)](https://www.law.cornell.edu/regulations/california/20-CCR-1601)).

**Title 24 Part 6 (2025 Energy Code)** applies to permits submitted from 1 Jan 2026 ([CEC](https://www.energy.ca.gov/programs-and-topics/programs/building-energy-efficiency-standards/2025-building-energy-efficiency)). Whether a hardwired integrated-LED pendant installed in a California home needs JA8 high-efficacy certification **was not verified** (section 10).

### 1.6 California chemical and battery rules

**Prop 65 and the C360 brass.**
- **Who must comply.** Businesses with 9 or fewer employees are exempt. Violations carry penalties of up to $2,500 per day, and private enforcers can sue after a 60-day notice ([CA AG FAQ](https://oag.ca.gov/prop65/faq)).
- **Why it matters for Tropos.** Lead is listed for cancer and reproductive harm, and the Prop 65 fact sheet names brass fittings as a source ([P65Warnings](https://www.p65warnings.ca.gov/fact-sheets/lead-and-lead-compounds)). C360 free-machining brass is 2.5–3.7% lead ([Wikipedia: Brass](https://en.wikipedia.org/wiki/Brass)).
- **When a warning is needed.** It turns on exposure, not on lead content. The maximum allowable dose level for lead is **0.5 µg/day** ([27 CCR 25805](https://www.law.cornell.edu/regulations/california/27-CCR-25805)).
- **Does lead-free brass avoid the warning?** Usually, but not automatically, because Prop 65 sets no lead-content threshold. A 2001 Prop 65 agreement had key makers cut lead to 1.5% or warn. California defines lead-free plumbing brass as at most 0.25% lead ([Wikipedia: Brass](https://en.wikipedia.org/wiki/Brass)). A lead-free alloy with a mill certificate, or inserts that cannot be touched in normal use, supports a no-warning position.
- **If a warning is needed:**
  - The new short-form warning must name a chemical, for example "Risk of cancer from exposure to lead…".
  - It became operative 1 Jan 2025; the old short form is allowed only on products "manufactured and labeled prior to January 1, 2028" ([27 CCR 25603](https://www.law.cornell.edu/regulations/california/27-CCR-25603)).
  - Online sales also need the warning on the product page, a "WARNING" hyperlink, or a prominent notice before checkout ([27 CCR 25602(b)](https://www.law.cornell.edu/regulations/california/27-CCR-25602)).
- **Other likely sources.** Vinyl and PVC goods also carry lead ([P65Warnings](https://www.p65warnings.ca.gov/fact-sheets/lead-and-lead-compounds)), which matters for lamp and power cords.

**SB 1215 (covered battery-embedded products, or CBEP).**
- **What it is.** Since 1 Jan 2026 consumers pay a recycling fee when buying a product whose battery is "not designed to be easily removed by the user with no more than commonly used household tools" ([CalRecycle](https://calrecycle.ca.gov/electronics/embeddedbatteries/)).
- **What the fee is.** It is **1.5% of the retail price, capped at $15**. Retailers register a CBE fee account with CDTFA, collect the fee, may keep 3%, and file quarterly or annually ([CDTFA](https://www.cdtfa.ca.gov/taxes-and-fees/covered-electronic-waste-recycling-fee/covered-battery-embedded.htm)).
- **Manufacturer duties for a CBEP:** annual notices to retailers and CalRecycle, brand and chemistry labelling from 2026, and annual reports from 1 Jul 2027 ([CalRecycle](https://calrecycle.ca.gov/electronics/embeddedbatteries/)). CalRecycle sets the rate each 1 October for the next year ([CDTFA](https://www.cdtfa.ca.gov/taxes-and-fees/covered-electronic-waste-recycling-fee/covered-battery-embedded.htm)); EARF should check the 2027 rate.
- **What counts as "easily removed".** CalRecycle's January 2026 implementation webinar says the regulations count Phillips, flat or cross-head screwdrivers, coins and hex keys as common household tools. A battery is easily removed if it is "marketed for removal", if "instructions or warranty allow it", or if no tools are needed. It is **not** easily removable if a label or manual tells users not to remove it ([CalRecycle webinar, 21 Jan 2026](https://www2.calrecycle.ca.gov/Docs/Web/138253)).
- **Result for EARF.** **Core, as specified (user-replaceable cells), is outside SB 1215.** Its manual must not discourage removal.

**AB 2440 (battery stewardship, "loose battery" programme).**
- **What it covers.** Loose batteries, batteries "designed to be easily removed" with household tools, and batteries packaged with products. The *producer* is the battery's manufacturer or its brand owner or licensee ([Beveridge & Diamond](https://www.bdlaw.com/publications/california-passes-two-new-bills-to-overhaul-states-battery-extended-producer-responsibility-program-and-broadly-expand-states-e-waste-program/)).
- **Deadline.** Producers must participate in an approved stewardship plan **by 1 Apr 2027**, and retailers may not sell batteries from non-listed producers ([Beveridge & Diamond](https://www.bdlaw.com/publications/california-passes-two-new-bills-to-overhaul-states-battery-extended-producer-responsibility-program-and-broadly-expand-states-e-waste-program/)).
- **Regulations are still draft.** CalRecycle's draft rules were still in informal rulemaking at a 16 Jun 2026 workshop. They add a definition of "brand" for "batteries sold with products and batteries currently lacking a trademark", and labelling obligations run to a **1 Jan 2031** deadline ([CalRecycle workshop document](https://www2.calrecycle.ca.gov/PublicNotices/Documents/18271)).
- **Result for EARF.** Core's cells, and any cell included with the Tropos remote, are covered batteries. If EARF uses **cells from a brand-name maker that is already a participating producer**, the obligation should sit with that maker. Confirm this against the final "brand" definition.

### 1.7 CPSC and labelling

**Duties that apply to every product.**
- Report to CPSC within **24 hours** of learning of a defect that could create a substantial product hazard, an unreasonable risk of serious injury or death, or a failure to meet a rule. No injury needs to have happened ([CPSC](https://www.cpsc.gov/Business--Manufacturing/Recall-Guidance/Duty-to-Report-to-the-CPSC-Your-Rights-and-Responsibilities)).
- A General Certificate of Conformity (GCC) is needed only for products subject to a CPSC rule. Third-party testing is not required for general-use products. From **8 Jul 2026** most importers must eFile certificates ([CPSC GCC](https://www.cpsc.gov/Business--Manufacturing/Testing-Certification/General-Certificate-of-Conformity)).
- None of the four products is a children's product, so no Children's Product Certificate or tracking-label regime applies.

**Reese's Law (Tropos remote, only if it uses a coin or button cell).** A button or coin cell is "a single cell battery with a diameter greater than the height" ([16 CFR 1263.2](https://www.law.cornell.edu/cfr/text/16/1263.2)). Any product containing one must meet:
- **ANSI/UL 4200A** ([16 CFR 1263.3](https://www.law.cornell.edu/cfr/text/16/1263.3));
- a secure battery compartment and ingestion warnings on the product, packaging and manual;
- **child-resistant packaging** of the cells under the Poison Prevention Packaging Act (16 CFR 1700.15/1700.20) ([15 USC 2056e and notes](https://www.law.cornell.edu/uscode/text/15/2056e)).

It is therefore a CPSC rule, which triggers a GCC, plus eFiling if EARF imports the finished remote. Hypex's remote ships with "a battery … included" of unstated type, and Hypex says it is made in China ([Hypex](https://www.hypex.nl/hypex-remote-control)).

**Origin claims.** An unqualified "Made in USA" claim must be "all or virtually all" US content. Hypex modules and imported parts call for a qualified claim such as "Made in USA from imported parts" or "Assembled in USA" (where assembly is substantial). The FTC can levy civil penalties ([FTC](https://www.ftc.gov/business-guidance/resources/complying-made-usa-standard)).

---

## 2. Matrix: product × requirement

Legend:
- **M** = legally mandatory for sale (federal or California).
- **C** = required by the electrical code at installation.
- **L** = City of Los Angeles sale rule.
- **Mk** = market-driven (retailers, insurers).
- **–** = not applicable.

Costs carry their source or **(est.)**. Times are calendar time.

| Requirement | Tropos (powered speaker) | Hemisphere (LED pendant) | Core (cordless lamp) | Mantle (record player) | Cost basis | Time |
|---|---|---|---|---|---|---|
| FCC Part 15B SDoC test and paperwork | **M**, Class B digital (DSP) | **M**, LED driver is a Part 15 unintentional radiator | **M**, MCU and charger | **M** if digital motor control; **–** if purely analogue DC motor (incidental radiator) | **$1.5–3.5k** per product; pre-scan **$0.8–1.5k** per half day ([Compatible Electronics](https://www.celectronics.com/Resources/EMC-Testing-Cost-Guide)) | Lab lead time 2–4 weeks ([same](https://www.celectronics.com/Resources/EMC-Testing-Cost-Guide)); about 1 week to report **(est.)** |
| FCC SDoC for bought-in adapters | – | Plug-in Class 2 driver: supplier's SDoC | **M**, supplier's SDoC; EARF's if EARF imports | **M**, supplier's SDoC | $0 if bought compliant | – |
| NRTL listing (UL, ETL, CSA, BACL…) | **Mk + L**, UL 62368-1: **$10–25k (est.)** | Plug-in: **Mk + L**, UL 153, **$6–15k (est.)**. Hardwired: **C**, UL 1598 with UL 8750/1310 parts; UL Limited Production route **$5–12k (est.)** | **Mk + L**, UL 153 Supplement SA: **$8–20k (est.)** | **Mk + L**, UL 62368-1 with an external listed supply (low-voltage product): **$4–10k (est.)** | Plus NRTL follow-up services, **$2–5k/yr per site (est.)** | 8–16 weeks **(est.)** |
| LA approval without a listing | **L**: LADBS Laboratory Approval $694 (simple equipment, e.g. light fixtures) to $1,250 (complex), General Approval $1,389–1,528, plus $104/h beyond included hours, plus 65%/yr renewal ([LADBS fees](https://dbs.lacity.gov/sites/default/files/efs/pdf/forms/etl/application-package-for-electrical-equipment-testing-evaluation-and-approval-pc-elec-app-12.pdf)) | same | same | same | Published (PDF shows superseded and current figures side by side; higher set assumed current) | 1–5 months ([LADBS](https://dbs.lacity.gov/sites/default/files/efs/forms/pc17/ib-p-ec-2020-013-electrical-equipment-approval-requirements.pdf)) |
| Cell and pack safety standards (UL 1642, UL 62133-2, UL 2054) | – (remote cells are the battery maker's) | – | **Mk**, required inside a UL 153 listing: $0 with recognised cells; custom pack **$10–25k (est.)** | – | | Custom pack 8–12 weeks **(est.)** |
| UN 38.3 and DOT/USPS shipping | Installed button cell exempt from the test summary | – | **M**: $0 with the cell maker's test summary; custom pack test **$5–15k (est.)** | – | [173.185](https://www.law.cornell.edu/cfr/text/49/173.185) | – |
| DOE battery charger (UEC) and certification | – | – | **M** | – | Appendix Y test **$1.5–4k (est.)** | 3–6 weeks **(est.)** |
| DOE external power supply Level VI | – (internal power supply) | – (LED-only drivers excluded) | **M**, adapter: supplier's duty (EARF's if importer) | **M**, adapter: same | $0 if bought certified | – |
| CEC Title 20 MAEDbS listing and marking | – | – | **M**: MAEDbS listing plus date/model/brand marking | Adapter marking only | Filing fee not verified; admin **$0–1k (est.)** | 2–4 weeks **(est.)** |
| Title 24 JA8 (CA residential) | – | **C?** hardwired only, **unverified** | – | – | **$3–8k (est.)** if needed | – |
| Prop 65 | **M only with ≥10 employees**: C360 brass and cords | **M at ≥10 employees**: cord | **M at ≥10 employees**: cord, brass | **M at ≥10 employees**: cord, brass | $0 while exempt; XRF tests and label/web edits **$0.5–3k (est.)** | 1–3 weeks **(est.)** |
| SB 1215 CBEP fee | – | – | **– if cells are user-removable and marketed so**; otherwise **M** (1.5%, max $15, CDTFA account, notices, reports) | – | [CDTFA](https://www.cdtfa.ca.gov/taxes-and-fees/covered-electronic-waste-recycling-fee/covered-battery-embedded.htm) | – |
| AB 2440 battery stewardship | **M for the battery's producer** if a cell is included | – | **M for the cells' producer** (EARF, if own-brand or unbranded) | – | Fees not yet published; **$0–2k/yr (est.)** | Statute: by 1 Apr 2027 |
| CPSC 15(b) reporting | **M** | **M** | **M** | **M** | $0 (process) | 24 hours when triggered |
| Reese's Law (16 CFR 1263) and GCC | **M if coin/button-cell remote**: UL 4200A tests **$1–3k (est.)**; **–** with an AAA remote | – | – | – | | 2–4 weeks **(est.)** |
| FTC origin claims | **M** if making origin claims | same | same | same | $0 | – |
| Product-liability insurance | **Mk** | **Mk** | **Mk** | **Mk** | Median for manufacturers: $50/month GL, $126/month BOP ([Insureon](https://www.insureon.com/manufacturers-business-insurance/cost)); EARF mix **$1.5–6k/yr (est.)** | 1–2 weeks **(est.)** |

---

## 3. Minimal path to the first 10 sales, and to 100

Common to all four products:
- Bind product-liability insurance ($1M/$2M is the common choice: [Insureon](https://www.insureon.com/small-business-insurance/product-liability/cost)).
- Write the FCC compliance sheets.
- Set up a CPSC 15(b) incident log.
- Avoid unqualified "Made in USA" claims.
- Take pre-orders under 47 CFR 2.803 while testing runs ([2.803](https://www.law.cornell.edu/cfr/text/47/2.803)).

**Tropos, first 10:**
1. Make three design fixes:
   - a metal or V-0 amp compartment, with the earthed IEC inlet and bonding that Hypex requires ([Hypex manual](https://cdn.hypex.nl/media/df/df/c2/1678368740/Fusion%20Manual%20R4.pdf));
   - lead-free brass, or inserts that cannot be touched;
   - an AAA-powered remote.
2. Run a half-day EMC pre-scan, then the FCC Part 15B Class B test of the speaker and remote as a system.
3. Run a 62368-1 safety pre-check: hipot, touch current, temperature rise ([pre-compliance safety](https://www.celectronics.com/product-safety-testing/pre-compliance-safety-testing)), **$1–2.5k (est.)**.
4. Do not market to the City of LA until listed, or apply for LADBS approval.
- **Cost:** about $4–9k **(est.)**. **Time:** 4–8 weeks **(est.)**.

**Tropos, to 100:** NRTL listing to UL 62368-1, **$10–25k (est.)** plus follow-up services. Bundle it with the other products at one NRTL.

**Hemisphere, first 10:**
1. Ship the **plug-in version only**. Use a listed Class 2 / LPS LED supply, for example Mean Well LPC-60: constant-current, "Class 2 power unit", "Pass LPS", UL 1310 ([datasheet](https://www.meanwell.com/Upload/PDF/LPC-60/LPC-60-SPEC.PDF)). Add a listed cord set.
2. FCC-test the shipped configuration (driver plus luminaire).
3. For a hardwired commission inside the first 10, choose one of:
   - **(a) UL Limited Production Certification (lighting).** "One visit for inspection" and witnessed application of the UL Mark, "no recurring costs or fees", and a "convertible option" to full listing later ([UL info sheet](https://ul.com/sites/default/files/2024-10/CS805385_Limited_Production_Lighting_InfoSheet_FINAL.pdf); [UL](https://www.ul.com/offerings/limited-production-certification-lighting-products)).
   - **(b) A per-site field evaluation.** See section 6.
- **Cost:** plug-in about $3–6k **(est.)**; add $5–12k **(est.)** for a limited-production hardwired batch.

**Hemisphere, to 100:** UL 153 listing for the plug-in version and UL 1598 for the hardwired version. One family listing at one NRTL, using listed driver and canopy parts, **$6–15k (est.)**.

**Core, first 10:**
1. Use **branded LiFePO4 18650 cells** that are recognised to UL 1642 or UL 62133-2 and come with UN 38.3 summaries ([UL 153 Supplement SA](https://www.ul.com/news/ul-153-expanded-add-battery-operated-portable-luminaires); [173.185](https://www.law.cornell.edu/cfr/text/49/173.185)). Keep them as loose cells in a holder rather than an EARF-built pack.
2. Use a Phillips-screw or coin-slot battery door, and say "user-replaceable" in the manual, which keeps Core outside SB 1215 ([CalRecycle webinar](https://www2.calrecycle.ca.gov/Docs/Web/138253)).
3. Buy a listed USB-C adapter that is already DOE Level VI and FCC compliant from a US source.
4. Run the FCC test, charging and lit.
5. Run the DOE battery-charger test, certify to DOE, then file in MAEDbS **before the first California sale** ([1608](https://www.law.cornell.edu/regulations/california/20-CCR-1608)).
6. Mark brand, model and date of manufacture ([1607(b)](https://www.law.cornell.edu/regulations/california/20-CCR-1607)).
7. Ship with cells installed ([USPS PI 9D](https://pe.usps.com/text/pub52/pub52apxc_032.htm)).
- **Cost:** about $5–10k **(est.)**. **Time:** 4–8 weeks **(est.)**.

**Core, to 100:**
- UL 153 Supplement SA listing, **$8–20k (est.)**.
- Settle AB 2440 producer status before 1 Apr 2027.
- Stay ahead of the April 2027 UL 153 revision (photobiological assessment).

**Mantle, first 10:**
1. Use a listed, Level VI, FCC-compliant external adapter with ES1/LPS output, so the turntable is low-voltage.
2. FCC-test it if the motor control is digital.
3. Optionally run a 62368-1 pre-check, **$1–2k (est.)**.
- **Cost:** about $2–6k **(est.)**. **Time:** 3–6 weeks **(est.)**.

**Mantle, to 100:** UL 62368-1 listing, **$4–10k (est.)**. With mains outside the box, it is the cheapest listing of the four.

**Prop 65 trigger for all:** once EARF reaches 10 employees, publish warnings or reformulate, including website warnings ([27 CCR 25602](https://www.law.cornell.edu/regulations/california/27-CCR-25602)).

---

## 4. Using pre-certified modules: what they save and what they don't

**What they don't save:**
- **FCC:** there is no modular shortcut for unintentional radiators outside PCs. The finished system must be tested ([15.101(e)](https://www.law.cornell.edu/cfr/text/47/15.101)). Pre-authorised adapters just keep the adapter's own SDoC off EARF's books.
- **Hypex FusionAmp:** the product pages and manual reviewed show **no UL recognition or CB certificate**. Hypex states that end-product compliance is the OEM's job, and it gives fire-enclosure and earthing rules referencing EN-IEC 62368-1 ([Hypex FA253](https://www.hypex.nl/products/amplifier-families/fusion-amplifier-family/fusionamp-fa253); [manual](https://cdn.hypex.nl/media/df/df/c2/1678368740/Fusion%20Manual%20R4.pdf)). Ask Hypex for any CB or test report; none was found here.

**What they do save:**
- **Safety:** components already listed or recognised (driver, adapter, cells) shrink the NRTL's scope. Moving mains voltage outside the product (Mantle, Core, plug-in Hemisphere) removes most shock and fire testing. EARF estimates this at **30–60% off the listing fee and fewer failure loops (est.)**.
- **Energy:** a Level VI adapter bought already certified carries its own DOE duties ([430.32(w)](https://www.law.cornell.edu/cfr/text/10/430.32)). An LED-only driver sits outside the EPS standard altogether ([430.2](https://www.law.cornell.edu/cfr/text/10/430.2)).

---

## 5. Labs in California, and what they charge

| Lab | Where | Relevant scope | Published pricing |
|---|---|---|---|
| **BACL** (Bay Area Compliance Laboratories) | 1274 Anvilwood Ave, **Sunnyvale** ([OSHA](https://www.osha.gov/nationally-recognized-testing-laboratory-program/BACL)) | **OSHA NRTL** for UL 62368-1, UL 153, UL 1598, UL 8750 and UL 1310, covering all four end products ([OSHA](https://www.osha.gov/nationally-recognized-testing-laboratory-program/BACL)). A2LA ISO 17025 for EMC, safety and lighting; FCC TCB; **CEC-approved lab and third-party certifier for battery chargers, external power supplies and portable luminaires**; LADBS-recognised ([BACL](https://www.baclcorp.com/accreditations/)) | None; quote only |
| **UL Solutions** | 47173 Benicia St, **Fremont** (and Brea) ([OSHA](https://www.osha.gov/nationally-recognized-testing-laboratory-program/ul)) | NRTL; field evaluation body (IAS FEB-107, [IAS](https://cdn-v2.iasonline.org/wp-content/uploads/2017/05/FEB-107-Cert.pdf)); Limited Production Certification | None |
| **Intertek (ETL)** | 1365 Adams Ct, **Menlo Park** (and Lake Forest) ([OSHA](https://www.osha.gov/nationally-recognized-testing-laboratory-program/its)) | NRTL for UL 62368-1, UL 153, UL 1598 and UL 2054 (UL 8750 not on its OSHA list); FEB-108 ([IAS](https://www.iasonline.org/wp-content/uploads/2017/09/FEB-108.pdf)) | None (site blocks automated access) |
| **Element** (absorbed NTS; nts.com now redirects to elementdefense.com) | **Fremont**: EMI/EMC and product safety; San Jose: RF/EMC; Irvine ([Element](https://www.element.com/locations)) | Irvine is an NRTL for UL 62368-1 ([OSHA](https://www.osha.gov/nationally-recognized-testing-laboratory-program/element)) | None |
| **CKC Laboratories** | New EMC lab in **Fremont** ([CKC](https://www.ckc.com/)) | EMC, FCC TCB, safety | None |
| **Compatible Electronics** | Lake Forest, Newbury Park, Brea (Southern California) ([CE](https://www.celectronics.com/)) | FCC Part 15B, 62368-1 pre-compliance, ISO 17025 | **Part 15B Class B SDoC $1,500–3,500; pre-compliance half day $800–1,500; lead time 2–4 weeks** ([cost guide](https://www.celectronics.com/Resources/EMC-Testing-Cost-Guide)) |
| CSA (Irvine), TÜV SÜD (San Diego), Nemko (Carlsbad) | Southern California NRTL sites ([CSA](https://www.osha.gov/nationally-recognized-testing-laboratory-program/csa); [TÜV SÜD](https://www.osha.gov/nationally-recognized-testing-laboratory-program/tuvam); [NRTL list](https://www.osha.gov/nationally-recognized-testing-laboratory-program/current-list-of-nrtls)) | CSA and TÜV SÜD list UL 62368-1, UL 153, UL 1598 and UL 8750 | None |
| **LADBS Electrical Test Lab** | Los Angeles (municipal) | City approval, valid in LA only | **$694–1,528 per application, $104/h beyond included hours, 65%/yr renewal, labels from $0.11 each** ([LADBS](https://dbs.lacity.gov/sites/default/files/efs/pdf/forms/etl/application-package-for-electrical-equipment-testing-evaluation-and-approval-pc-elec-app-12.pdf)) |

**Typical figures, combining published and estimated:**
- **Pre-scan:** $0.8–1.5k per half day (published).
- **Full FCC Part 15B test:** $1.5–3.5k (published).
- **NRTL listing:** $4–25k per product depending on complexity, plus $2–5k a year in follow-up per factory **(est.)**. No NRTL publishes list prices.
- **BACL** combines NRTL scope for all four end-product standards with CEC-approved battery-charger and external-power-supply testing ([BACL](https://www.baclcorp.com/accreditations/)), so Core's safety and energy work could sit in one lab.

---

## 6. The field-evaluation route for a small first run

**What it is.** A field evaluation is an inspection by a Field Evaluation Body (under NFPA 790/791) that ends in a field label and report ([UL](https://www.ul.com/resources/field-evaluations-unlisted-and-modified-electrical-equipment); [ECM](https://www.ecmweb.com/national-electrical-code/article/20901413/what-is-a-field-evaluation-body-and-what-do-they-do)). It is built for custom or installed equipment:
- The FEB can do an initial evaluation **at the factory before shipping**, but the final evaluation happens at the installation site ([ECM](https://www.ecmweb.com/national-electrical-code/article/20901413/what-is-a-field-evaluation-body-and-what-do-they-do); [TÜV Rheinland](https://www.tuv.com/content-media-files/usa/pdfs/1020-field-evaluation-service-(fes)-for-u.s.-and-canada/tuv_rheinland_01_field_evaluation_services.pdf)).
- Being an NRTL "does not automatically make the FEB acceptable" to the local authority ([ECM](https://www.ecmweb.com/national-electrical-code/article/20901413/what-is-a-field-evaluation-body-and-what-do-they-do)).
- Prices are quote-only ([UL](https://www.ul.com/services/field-evaluations)).

**Where it fits:**
- For the **hardwired Hemisphere at a known address**, such as a showroom or the first commissions. In Los Angeles the published option is LADBS **Field One-Time Approval**: $1,181 for simple equipment, plus mileage, and "limited to the field conditions, intended for a specific job address" ([LADBS](https://dbs.lacity.gov/sites/default/files/efs/forms/pc17/ib-p-ec-2020-013-electrical-equipment-approval-requirements.pdf); [fees](https://dbs.lacity.gov/sites/default/files/efs/pdf/forms/etl/application-package-for-electrical-equipment-testing-evaluation-and-approval-pc-elec-app-12.pdf)).
- **Not for direct-to-consumer shipping across the country.** Paying an evaluation per installation does not scale.

**Better for a batch: Limited Production Certification.**
- **UL.** For lighting, there is one inspection visit, UL witnesses the Mark being applied, and there are no follow-up fees ([UL](https://ul.com/sites/default/files/2024-10/CS805385_Limited_Production_Lighting_InfoSheet_FINAL.pdf)). Each unit gets "a dedicated label with a UL Mark and a unique serial number" ([UL](https://www.ul.com/insights/limited-production-certification-ess-installation)).
- **Intertek.** Its equivalent reportedly requires all production within a contiguous 3-month period ([Intertek](https://www.intertek.com/industrial-equipment/limited-production-certification/); from a search summary, page not fetched directly).
- **Tropos.** Ask UL whether Limited Production Certification is offered for UL 62368-1 audio products; this was not verified.

---

## 7. Product-liability insurance

**Published medians:**
- Manufacturers buying through Insureon pay a median of **$50/month ($600/yr)** for general liability, which usually includes product liability, and **$126/month ($1,517/yr)** for a business owner's policy (updated 21 Jul 2025) ([Insureon](https://www.insureon.com/manufacturers-business-insurance/cost)).
- 85% of Insureon customers choose **$1M per occurrence / $2M aggregate**. The California median for "product liability" is $42/month ([Insureon](https://www.insureon.com/small-business-insurance/product-liability/cost)).

**What EARF should budget.** Those medians come mostly from very small, low-risk businesses. Mains-powered audio and a lithium-cell lamp sold nationally will price higher: budget **$1.5–6k a year** for $1M/$2M with products-completed operations at under $1M revenue, rising with sales **(est.)**. Listing, a battery-safety file and a recall plan all help underwriting **(est.)**.

---

## 8. Design changes that cut cost or risk

1. **Lead-free brass (all products).** Specify a lead-free machinable brass and get mill certificates, for example a silicon brass. California defines lead-free plumbing brass as at most 0.25% lead ([Brass](https://en.wikipedia.org/wiki/Brass)). This removes C360's 2.5–3.7% lead from the Prop 65 analysis (exposure limit 0.5 µg/day, [25805](https://www.law.cornell.edu/regulations/california/27-CCR-25805)) at little piece-price cost **(est.)**.
2. **External listed supplies.** Use an ES1/LPS adapter for Mantle, a Level VI USB-C PD adapter for Core, and a Class 2 driver for Hemisphere (plug-in, or in a listed canopy). Mains then stays outside the acrylic, which simplifies listing and fire-enclosure issues.
3. **Tropos fire enclosure.** Use a metal (earthed) or V-0 amp compartment, as Hypex requires ([manual](https://cdn.hypex.nl/media/df/df/c2/1678368740/Fusion%20Manual%20R4.pdf)), rather than relying on the acrylic. Optional: evaluate a DC-input amplifier fed by an external listed supply to make Tropos a low-voltage product. Not verified with Hypex.
4. **AAA remote instead of a coin cell.** This avoids Reese's Law testing, warnings, child-resistant packaging and eFiling ([16 CFR 1263](https://www.law.cornell.edu/cfr/text/16/part-1263); [CPSC GCC](https://www.cpsc.gov/Business--Manufacturing/Testing-Certification/General-Certificate-of-Conformity)). Include brand-name AAA cells so the battery maker is the AB 2440 producer.
5. **Core battery architecture.**
   - **Use loose branded, recognised cells, not an EARF pack.** A custom pack would trigger its own UN 38.3 test and pack-level certification ([173.185](https://www.law.cornell.edu/cfr/text/49/173.185); [UL 153 Supplement SA](https://www.ul.com/news/ul-153-expanded-add-battery-operated-portable-luminaires)).
   - **Keep the cells removable with household tools and say so.** That keeps Core outside SB 1215 ([CalRecycle](https://www2.calrecycle.ca.gov/Docs/Web/138253)).
   - **Consider a parallel layout.** At about 17 Wh the DOE limit is 5.40 kWh/yr for 3.2 V parallel cells against 1.59 kWh/yr for 9.6 V series cells ([430.32(z)](https://www.law.cornell.edu/cfr/text/10/430.32)). Parallel also avoids imbalance when users mix old and new cells. This is EARF's engineering call.
   - **Add a keyed holder, per-cell protection and LiFePO4 charge termination.** These reduce misuse risk from users fitting other 18650 chemistries **(engineering judgement)**.
6. **Hemisphere launch order.** Launch plug-in first. Take hardwired orders only with Limited Production Certification or a full UL 1598 listing.
7. **One NRTL and one factory for everything.** Follow-up inspection fees are charged per site **(est.)**. BACL covers all four end-product standards in Sunnyvale ([OSHA](https://www.osha.gov/nationally-recognized-testing-laboratory-program/BACL)).
8. **Accredited US EMC lab.** This hedges against the FCC's proposed rules on lab location and accreditation ([DLA Piper](https://www.dlapiper.com/en/insights/publications/2026/10/fcc-to-vote-on-limiting-equipment-authorization-testing)).
9. **Claims discipline.** Say "Designed and assembled in San Francisco", not "Made in USA" ([FTC](https://www.ftc.gov/business-guidance/resources/complying-made-usa-standard)).

---

## 9. Budget line for the investor deck (all **est.** except where noted)

> **Regulatory and certification: ~$50–120k over the first 18 months** (first-sales work plus four listings plus part of a year's follow-up).
> - **~$18–46k** to first sales: FCC SDoC for four products ($6–14k), EMC pre-scans ($3–6k), safety pre-checks ($3–7.5k), DOE and CEC filings for Core ($1.5–4k), legal and labels ($2–5k), first-year product-liability insurance ($0.6–6k), and one retest ($1.5–3.5k). Lab rates per [Compatible Electronics](https://www.celectronics.com/Resources/EMC-Testing-Cost-Guide).
> - **~$28–70k** to NRTL-list all four products before scaling past about 100 units each: Tropos $10–25k, Hemisphere $6–15k, Core $8–20k, Mantle $4–10k.
> - **~$5–20k a year** ongoing: NRTL follow-up, insurance growth, AB 2440 stewardship fees and retests.
> - **Optional:** $5–12k for a limited-production hardwired Hemisphere batch; $1–3k if the remote keeps a coin cell.
> - **Timing:** first deliveries about 6–10 weeks after design freeze; full listings 3–6 months.

---

## 10. Open items to confirm before spending

1. **Hardwired Hemisphere and Title 24.** Does a hardwired integrated-LED pendant in a California home need JA8 certification under the 2025 Energy Code? Ask the CEC hotline or a California lighting rep.
2. **Plug-in pendant standard.** Should the cord-connected pendant be evaluated under UL 153 or UL 1598? What are UL 153 Supplement SA's numeric battery-energy limits relative to Core's 17 Wh? Ask the NRTL.
3. **AB 2440 producer status.** Read the final "brand" definition once adopted. Confirm whether branded cells shipped in Core make the cell maker, not EARF, the producer.
4. **Hypex documentation.** Does Hypex hold a CB report for the FusionAmp? What battery does its remote use?
5. **Acrylic flammability.** What is the UL 94 rating of the chosen tinted cast acrylic? It bears on Hemisphere diffusers and the Tropos cabinet.
6. **FCC 29 Oct 2026 meeting.** What did the FCC adopt on test-lab rules and on SDoC accreditation?
7. **California lighting RoHS.** Does the state's restriction on hazardous substances in general-purpose lights (Health & Safety Code §25210.9 ff.) reach integrated-LED luminaires? The DTSC page was not reachable.
8. **CalRecycle 2027 fee.** What rate did CalRecycle set on 1 Oct 2026 for 2027? This matters only if any product becomes a CBEP.
