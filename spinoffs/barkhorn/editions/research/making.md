# Objects and bubbles inside cast acrylic: how it is made

Research note for EARF special editions (objects inside the acrylic, designed air bubbles). Public reading only, all sources accessed 2026-10-31. Status markers:

- **[confirmed]**: read on the cited page or datasheet.
- **[snippet]**: seen only in a search-result excerpt; the page itself was not opened or would not load.
- **[derived]**: calculated here from cited numbers.
- **[unconfirmed]**: general knowledge or a single weak source. Check it before relying on it.

---

## 0. The numbers that matter

| Item | Value | Status |
|---|---|---|
| PMMA refractive index | n_D ≈ 1.49 (1.4927 measured) | confirmed |
| Critical angle, PMMA to air | ≈ 42.2° | derived |
| MMA monomer refractive index / boiling point | 1.414 / ≈ 100–101 °C | snippet |
| ACRIFIX 2R 0190 (liquid) refractive index | ≈ 1.44 | confirmed |
| Polymerization shrinkage, MMA to PMMA | ≈ 21 vol % | confirmed (one study) |
| Lucite embedment autoclave | ≈ 140 psi N₂ (≈ 9.7 bar), 8–10 h; > 12 atm cited elsewhere | confirmed |
| Embedment exotherm | ≈ 300 °F (≈ 150 °C) | confirmed (vendor) |
| Annealing, cast acrylic | 80 °C, 1 h per mm (min 2 h); cool to < 60 °C | confirmed |
| ACRIFIX 2R 0190 post-bond anneal | 2–4 h at 70–80 °C; > 70 °C may yellow | confirmed |
| Cast acrylic continuous service | −40 to 180 °F (≈ −40 to 82 °C) | confirmed |
| Vicat softening, cast PMMA | ≥ 105 °C (≈ 115 °C on some sheets) | snippet |
| PMMA flammability | UL 94 HB typical (lowest tier) | snippet |

---

## 1. Casting objects into PMMA (the Lucite embedment trade)

### 1.1 Process and chemistry

The trade casts a syrup of PMMA powder dissolved in liquid MMA monomer. It is poured into a mold in layers. The object is set by hand on a partly cured layer and covered, and the block is finished in a heated pressure vessel. Wikipedia says the mix is "thick, opaque" and milky, which makes it hard to centre objects on several levels. It describes curing "with heat and pressure exceeding 12 atmospheres" for up to about seven hours, oversize casting to allow for "variable shrinkage", then belt-sanding and buffing ([Wikipedia, Acrylic embedment](https://en.wikipedia.org/wiki/Acrylic_embedment), accessed 2026-10-31) [confirmed]. The technique goes back to Armand G. Winfield in the early 1940s and was in mass production by 1945 (same source) [confirmed].

A working US caster, USAcrylic Awards, publishes its own numbers [confirmed] ([usacrylicawards.com, How are embedments made](https://usacrylicawards.com/how-are-embedments-made), accessed 2026-10-31):

- monomer-to-polymer ratio of 70/30 to 30/70, depending on the item;
- autoclave at about 140 psi of nitrogen for 8–10 hours, temperature set by the item;
- a reaction that can reach about 300 °F (≈ 150 °C);
- molds about 25 % larger than the finished piece, for grinding and polishing.

**Why pressure kettles and water baths.** MMA bulk polymerization accelerates by itself. As the mass thickens, polymer radicals stop terminating, so the rate and the heat output rise together. This is the gel or Trommsdorff effect, which is much stronger for MMA than for styrene. In thick sections the heat can boil the monomer ([UCLouvain thermochemical model of MMA casting](https://research.dial.uclouvain.be/bitstreams/86bed08b-0ff8-48e8-8f04-4fdfd92b5fe5/download), accessed 2026-10-31) [snippet]. MMA boils at about 100–101 °C at 1 atm ([webqc.org MMA](https://www.webqc.org/compound-C5H8O2-C5H8O2.html); [Fisher Scientific MMA](https://www.fishersci.com/shop/products/methyl-methacrylate-99-stab-thermo-scientific/AAA13030AE), accessed 2026-10-31) [snippet]. That is well below the ≈ 150 °C exotherm the vendor reports.

Raising the pressure does two things. It raises the monomer's boiling point, and it shrinks any bubbles that remain. The second effect is how the resin hobby uses pressure pots: a pot "will not completely remove the trapped air but shrinks it" until the bubbles cannot be seen ([Smooth-On support](https://support.smooth-on.com/knowledgebase.php?article=47); [Art Molds, pressure pot](https://www.artmolds.com/blogs/techniques/degassing-resin-castings-with-a-pressure-pot), accessed 2026-10-31) [snippet]. Pressure has to be held until the part gels, or the bubbles grow back.

A patent gives embedment casting conditions of 30–120 °C and 1–50 bar ([US patent, embedment casting composition](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8022135), accessed 2026-10-31) [snippet]. Polysciences sells an MMA embedding kit that cures thermally, "preferably under pressure", under anaerobic conditions. Oxygen inhibits the cure ([Polysciences kit](https://polysciences.com/products/methyl-methacrylate-embedding-and-casting-kit), accessed 2026-10-31) [confirmed]. The public page gives no temperature, time or catalyst ratio.

**Shrinkage.** Pure MMA shrinks about 21 % by volume when it polymerizes. That is why PMMA products are made in stages ([Effects of prepolymerized particle size… dental resins, PMC3977089](https://pmc.ncbi.nlm.nih.gov/articles/PMC3977089), accessed 2026-10-31) [confirmed, one study]. A syrup that already contains polymer shrinks less, roughly in proportion to its monomer fraction. A patent example reports 3.0 % volume shrinkage for a meth(acryl) syrup at about 30 % solids ([US patent, (meth)acryl syrup](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6191229), accessed 2026-10-31) [snippet; that figure is much lower than a simple fraction rule predicts, so treat it as unconfirmed]. For the 70/30 to 30/70 syrups the trade uses, the simple rule gives about 6–15 % [derived, unconfirmed].

**Thickness and cure time.** Nothing found states a hard thickness limit for acrylic embedments. Large blocks are made layer by layer over a day and then autoclaved for 8–10 h (USAcrylic, above). The best published rule comes from the polyester-resin trade: keep each layer no deeper than 40 mm to avoid exotherm stress cracks (Voss c. 1980, cited in [Moore 2006, NatSCA News 10](https://natsca.org/sites/default/files/publications/NatSCA%20News%20Issue%2010-7_0.pdf), accessed 2026-10-31) [confirmed for polyester; unconfirmed for MMA].

### 1.2 What survives inside

Published lists from US Acrylic Awards ([Dos and don'ts of acrylic embedding](https://usacrylicawards.com/the-dos-and-donts-of-acrylic-embedding), accessed 2026-10-31) [confirmed] and Midton, UK ([midton.com/embedment](https://midton.com/embedment/), accessed 2026-10-31) [confirmed].

**Works:**

- Metal ("often casts well").
- Coins, badges, circuit boards, glass vials, sports turf, mechanical parts, textiles and leather.
- Dried botanicals, after a pre-treatment assessment.
- A french fry, shown clear after a year.

**Fails:**

| Item | Why |
|---|---|
| Injection-moulded plastics (pens, key fobs, model parts) | Warp or bubble at the ≈ 300 °F exotherm |
| Rubber | Bleeds and clouds |
| Fresh flowers, leaves, bread | Cloud or brown the block |
| Painted enamel and coins | Paint peels, wrinkles or bleeds |
| Highly polished metal | Acrylic does not wet it; leaves a silvery "cavitation" layer |
| Phones and anything with cracks or air gaps | Air is pulled out during the cure and leaves flaws |
| Objects holding moisture, porous or water-sensitive items | Listed by Midton as non-embeddable |

Cold weather can also crack a block that shrinks around a rigid object.

A Lucite deal-toy maker states the rule bluntly: "most products cannot be 'embedded' in solid Lucite – they melt." It sells a sandwich ("entrapment"/"encasement") at about half the cost instead ([LuciteTombstones, entrapment](https://lucitetombstones.com/acrylic-lucite-product_entrapment_encasement/), accessed 2026-10-31) [confirmed]. That is EARF's lamination route (section 3).

**Monomer as a solvent.** MMA monomer is a strong solvent, and polystyrene and SAN-type plastics are expected to swell or dissolve in it. No source opened here states that directly, so it is **[unconfirmed]**. The vendors blame heat for plastic failures; solvent attack probably adds to it. Test every plastic part in liquid monomer or cement before committing.

### 1.3 Drying and sealing organics

The natural-history conservation literature has the clearest account of how embedded specimens fail. It is written for polyester resin, but the mechanisms apply to MMA ([Moore 2006, NatSCA News 10](https://natsca.org/sites/default/files/publications/NatSCA%20News%20Issue%2010-7_0.pdf), accessed 2026-10-31) [confirmed]:

- The exotherm forces air out of body cavities as bubbles.
- A dry specimen keeps shrinking after the resin hardens and pulls away from it. The gap shows as a **silvering** that hides the specimen. That silver is a thin air film, the same physics as section 4.3.
- Any moisture left in the specimen forms an "emulsive mist" around it.
- Resin clears membranous tissue. Blue lycaenid butterfly wings lose their iridescence because the resin's refractive index (given as 1.5–1.75) is close to that of the scales.

Moore's remedies:

1. Freeze-dry to "absolute dryness". Use deionised water, or a calcitic film forms.
2. For fragile items, dehydrate through acetone and pre-soak in raw resin, which also displaces air from recesses.
3. Coat wings before embedding. Measured initial loss of iridescence: about 5–20 % with hair lacquer, matting spray or acrylic lacquer, against 100 % uncoated. Dilute PVA (5 % in ethanol) turned the blue slightly purple.

Craft guidance for flowers in resin agrees [snippet] ([plasticranger, preserve flowers in resin](https://plasticranger.com/how-to-preserve-flowers-in-resin/), accessed 2026-10-31):

- Fresh petals are about 80–90 % water.
- Silica gel or freeze-drying keeps form and colour best.
- Two or three light coats of clear acrylic spray stop tannins bleeding.

For EARF, two cautions follow. An acrylic spray sealer is itself PMMA-based and can soften in MMA or in the cement. A barrier with a different chemistry, such as PVA or shellac, may protect better, but that is **[unconfirmed]**: test it. Vacuum-impregnating the sealer helps pull air out of recesses before bonding. That last step is inferred from Moore's acetone pre-soak, so it is **[unconfirmed]**.

### 1.4 UV yellowing and fading

**The PMMA.** PMMA itself barely yellows. ACRYLITE describes its sheet as "naturally UV-stable… stable from within" ([ACRYLITE, why doesn't it yellow](https://www.acrylite.co/resources/knowledge-base/article/why-doesn-t-acrylite-acrylic-sheet-yellow), accessed 2026-10-31) [confirmed]. The maker gives 30-year warranties on select grades, some for "no visible yellowing" ([ARCAT spec, ACRYLITE](https://www.arcat.com/sdspecs/htm04/08_84_00evo.htm), accessed 2026-10-31) [snippet].

**The adhesive and the casting.** These are the weak links. The ACRIFIX 2R 0190 datasheet says the joint can yellow if the hardener is above 3 %, if thinner is used, or if it is annealed above 70 °C. It can also whiten from micro-cracks if it is not annealed at all ([ACRIFIX 2R 0190 Technical Information, Ref. 391-19, 06/24](https://www.zenit.cz/public/media/Plasty/Zenit_Technicky_List_Plasty_Lepidla_Acrifix_2R-190_EN.pdf), accessed 2026-10-31) [confirmed].

**The specimens.** Insect colours fade even when the matrix does not. In a Smithsonian fading study, blues and reds changed most, shifting toward yellow, and iridescent specimens changed more at high humidity ([MCI Smithsonian abstract](https://mci.si.edu/node/1217986), accessed 2026-10-31) [snippet]. Pigmented scales fade; structural colours do not, though UV breaks them down over time ([Conservation DistList 1996](https://cool.culturalheritage.org/byform/mailing-lists/cdl/1996/0727.html), accessed 2026-10-31) [snippet]. The scarlet of fly agaric fades to orange as its pigment breaks down (Moore 2006) [confirmed].

Plant chlorophyll browns and fades in light. That is general knowledge, not found in a source this round **[unconfirmed]**.

**What to do.** A UV-absorbing cast grade (for example "UVA" cast acrylic per ASTM D4802, sold as such by [Trident Plastics](https://plastics.tridentplastics.com/viewitems/acrylic/cell-cast-acrylic-astm-d4802-cat-a-1-finish-1-uva), accessed 2026-10-31 [snippet]) shields organics inside. It does not stop visible-light fading.

---

## 2. US embedment shops and published prices

| Shop | Location / claim | Published prices, minimums, lead time | Status |
|---|---|---|---|
| **USAcrylic Awards** ([usacrylicawards.com](https://usacrylicawards.com/lucite-embedments)) | Casts, cures and finishes in the USA, about 40 years | Badge embedment 5 × 3.5 in: $160.75 for 1, $90.05 for 2+, $72.35 for 6+, $62.70 for 16+, $54.70 for 50+; ships 2 weeks after art approval, rush extra ([badge page](https://usacrylicawards.com/lucite-badge-embedment)). Shaped blocks (iceberg, half-barrel, hard hat) have a **6-piece minimum**; "normal production 7–10 days" ([iceberg](https://usacrylicawards.com/iceberg-shaped-lucite-embedment)). May ask for a sample or test pour before quoting. | confirmed (badge); snippet (others) |
| **LuciteTombstones.com** ([site](https://lucitetombstones.com/)) | "Made in U.S.A.", 42+ years of deal toys; phone 401 area code (Rhode Island) | Entrapment (sandwich) plaques: 4 × 5 × 1.5 in from $90.42 (6) to $60.44 (250); 4 × 4 × 1.5 in from $68.95 to $38.75; minimum stated as both "6 or 12" and "25 pc"; minimum production 7 days; custom entrapments quote-only ([entrapment page](https://lucitetombstones.com/acrylic-lucite-product_entrapment_encasement/)) | confirmed |
| **Clear Image, Inc.** ([clearimageinc.com](https://clearimageinc.com/)) | US-made for 40+ years, "one of a handful of embedding companies still manufacturing in America"; laser work through an Arizona business; sells through promo distributors | Layered pours, cured under controlled temperature and pressure; embeds coins, badges, pressed flowers; no prices or minimums published | confirmed |
| **Em-Bed-It, Inc.** ([embeditinc.com](https://www.embeditinc.com/)) | Since 1973, deal toys in-house; Pittsburgh, PA per a business directory ([leadiq](https://leadiq.com/c/em-bed-it-inc/5a1da2962300005b00946cf2)) | Site returned 503; nothing published found | snippet / unconfirmed |
| **Midton** (UK, for reference) ([midton.com](https://midton.com/embedment/)) | Lochgilphead and Glasgow | Autoclave cure; test embedment advised; "at the client's own risk"; no prices | confirmed |

All accessed 2026-10-31. None of the names suggested in the brief ("Crystal Images", "Sun Acrylics", "Plastic Creations", "Gemini") turned up as embedment casters in these searches. Treat them as unverified. The trade is small and sells mainly through award and promotional distributors.

**Read-across for EARF.** A cast embedment costs about $55–160 per piece in single-object sizes. Lead time is 2 weeks plus the time to ship objects in. Every caster disclaims risk on organics and plastics.

---

## 3. EARF's lamination route: pocket, seal, bond, anneal

### 3.1 The cements

**ACRIFIX 2R 0190** (Röhm/Polyvantis) [confirmed] ([datasheet 391-19, 06/24](https://www.zenit.cz/public/media/Plasty/Zenit_Technicky_List_Plasty_Lepidla_Acrifix_2R-190_EN.pdf), accessed 2026-10-31).

| Property | Value |
|---|---|
| Composition | PMMA dissolved in MMA, 30–32 % solids |
| Hardener | ACRIFIX CA 0020, 3–6 % |
| Viscosity | 1600–2000 mPa·s |
| Density | ≈ 1.02 g/cm³ |
| Refractive index (liquid) | ≈ 1.44 |
| Flash point | ≈ 10 °C |
| Pot life / cure, 200 g at 20 °C | ≈ 25 / 60 min at 3 % hardener; ≈ 20 / 50 min at 5 % |
| Machining after cure | Machine after 3–6 h; sand and polish after 24 h |
| Tensile shear strength | 30–40 MPa unannealed; 45–55 MPa after 5 h at 80 °C (PLEXIGLAS XT) |

The datasheet's handling instructions:

- **Degassing:** let the bubbles rise in the covered pot, or pull them out "in a vacuum desiccator (min. 200 mbar)".
- **Before bonding:** internally stressed parts must be annealed first, or they stress-crack.
- **Closed cavities:** the cement "must not get into closed cavities… since the curing process is severely hampered at such sites, and there is a risk of stress cracking". If a cavity cannot be avoided, flush it with air for at least 20 minutes. This bears directly on sections 3.3 and 4.
- **After bonding:** anneal 2–4 h at 70–80 °C in a forced-air oven.
- **Tint:** the cement takes ACRIFIX CO colour pastes, so a tinted joint can match tinted sheet.

**Weld-On 40** (IPS/SCIGRIP) [snippet]:

- Two-part reactive acrylic.
- Working time about 20 min at 73 °F; fixture in 2 h; full cure in 24–72 h ([Perigee Direct](https://www.perigeedirect.com/products/weld-on-40-reactive-acrylic-adhesive-low-voc); [Chemical Concepts](https://www.chemical-concepts.com/product/weld-on-40-reactive-acrylic-adhesive/), accessed 2026-10-31).
- Bond strength reported as 2,600 psi at 24 h and 4,000 psi at 1 week at 73 °F, from the AC Plastics property sheet. That sheet returned 404, so this is snippet only.
- Vendors describe it as gap-filling, curing clear, and suited to a "bubble-free, crystal-clear, solid block look".
- No published refractive index or shrinkage value was found **[unconfirmed]**.

### 3.2 Annealing schedule

ACRYLITE gives the cast-acrylic schedule [confirmed] ([ACRYLITE annealing manual](https://www.acrylite.co/resources/fabrication-manuals/annealing-acrylite-acrylic-sheet); [tech brief](https://www.acrylite.co/tech-briefs/annealing-acrylic.html), accessed 2026-10-31):

- Heat to **80 °C (180 °F)**, just below the deflection temperature.
- Hold **1 h per mm of thickness**, with a minimum of 2 h. For example 9.5 mm takes 9.5 h heating and 2.5 h cooling, at about 22 °F/h.
- Above 8 mm, cooling time in hours equals thickness in mm ÷ 4.
- Do not unload above 60 °C.
- Machining alone needs only 2 h heating and 2 h cooling.
- **After cementing, wait at least 6 h before annealing**, or the solvent in the joint will bubble.

ACRYLITE also says to anneal before cementing so the joint does not craze, and again afterwards for strength ([ACRYLITE, when to anneal](https://www.acrylite.co/resources/knowledge-base/article/when-should-i-anneal-the-acrylic), accessed 2026-10-31) [confirmed]. Another fabrication note suggests annealing less than 24 h before cementing [snippet]. AC Plastics' display-case guide gives a gentler 5–6 h at 145 °F (63 °C), cooled slowly to 110 °F, before and after cementing ([TruVue Optium fabrication, AC Plastics](https://www.acplasticsinc.com/media/documents/TruVue%20Optium%20Case%20Fabrication.pdf), accessed 2026-10-31) [snippet].

**For an EARF laminate with an object inside:**

1. Anneal the milled sheets at 80 °C, 1 h/mm.
2. Bond.
3. Wait 6–24 h.
4. Anneal at **70 °C**, the lower end of the ACRIFIX range, to avoid yellowing. Hold for about 1 h per mm of total thickness, cool at about 10–15 °C/h, and unload below 60 °C.

For a 40 mm stack that means about 40 h at temperature. A forum report of a roughly 40-hour full cycle for 1/4 in sheet with a slow ramp shows that long cycles are normal ([eng-tips PMMA annealing](https://eng-tips.com/threads/pmma-annealing.343800), accessed 2026-10-31) [snippet]. The step-4 hold is **[derived]**; the 70 °C ceiling follows the ACRIFIX note.

### 3.3 Making the pocket disappear

Light reflects at a boundary in proportion to ((n₁ − n₂)/(n₁ + n₂))². PMMA (n = 1.4927, [Shimadzu application note](https://www.shimadzu.com/opt/products/ref/ref-app03.html), accessed 2026-10-31 [confirmed]) against air gives about 3.9 % per surface. Against a fully cured MMA-based cement, which is itself PMMA, the difference is close to zero [derived].

The ≈ 1.44 printed for ACRIFIX is the *liquid* value. The cured cement is PMMA and should sit near 1.49, but no cured value is published **[unconfirmed]**. Against PMMA, a mismatch of 0.01 reflects about 0.001 % per surface, which cannot be seen. A mismatch of 0.05 reflects about 0.03 %, faint but visible as a ghost edge in a polished block [derived].

So the pocket walls vanish only when two conditions hold:

1. The pocket is completely filled with cured cement, with no air film. Any air left at a milled wall shows as Moore's "silvering".
2. The milled wall is smooth enough that the fill wets it without trapping micro-bubbles in tool marks. Polishing the walls is not needed for the optics once they are filled, because the index match hides tool marks. But they must be clean, and roughened walls bond better: ACRIFIX recommends grit 320–400 on cast sheet.

**Risks of backfilling a pocket with polymerizing cement:**

- **Shrinkage.** Monomer in the cement shrinks as it cures, around 21 % × 0.7 ≈ 14–15 % by volume for a 30 % solids syrup [derived, unconfirmed]. In a deep, closed pocket that pulls voids or stresses the object. Fill in shallow layers. Leave a vent or sprue to feed the shrinkage, then mill it off.
- **Closed cavities.** ACRIFIX warns the cure is "severely hampered" in a closed cavity and causes stress cracking. A backfilled pocket must be filled and cured open, before the cover sheet goes on, or vented.
- **Exotherm.** Small volumes stay cool. A large pocket fill behaves like a casting (section 1.1).
- **Crazing.** Solvent or monomer on an unannealed machined edge crazes. Anneal the milled sheet before any cement touches it.

An alternative fill is a clear epoxy or polyester casting resin. Its index is quoted at about 1.50–1.56 for polyester, from the NatSCA table, so it will not match PMMA as closely. A 1.55 resin in PMMA reflects about 0.04 % per surface: faintly visible [derived].

### 3.4 What annealing does to an object inside

Eighty degrees for many hours will:

- drive out residual water as vapour, giving bubbles or mist around the object;
- soften waxes and some sealers;
- expand the object differently from the PMMA, which can crack the bond.

The ACRYLITE Champagne sculptures show the vapour effect at full strength. Haunschmidt soaks laser-cut ACRYLITE FF in water for 2–3 weeks, then heats it with IR heaters, and bubbles nucleate throughout ([ACRYLITE, light sculptures like bubbling champagne](https://www.acrylite.co/applications/artistic-design/light-sculptures-reminiscent-of-bubbling-champagne), accessed 2026-10-31) [confirmed]. In other words, moisture in the sheet or in the object plus heat produces bubbles.

For EARF this means:

- Dry the object and the sheets before bonding. A desiccated, freeze-dried object is the target.
- Use the lower annealing temperature with organics. 70 °C is still a lot for pigments: run a sacrifice piece.

The ≈ 150 °C exotherm of Lucite casting is far harsher, which is one reason lamination suits organics better than casting.

---

## 4. Bubbles by design

### 4.1 Mating hemispheres

No published example was found of milling matching hemispheres in two acrylic faces and bonding them to trap spherical voids **[unconfirmed whether it is done commercially]**. The nearest documented relatives:

- Haunschmidt's heat-nucleated bubbles: random, and controlled only by heating time (above).
- 1970s Lucite blocks "with bubble inclusions" ([Chairish listing](https://www.chairish.com/product/16230694/solid-lucite-block-sculpture), accessed 2026-10-31) [snippet].
- Vasa Mihich's laminated plexiglas spheres, which are laminated but have no voids ([1stdibs](https://www.1stdibs.com/furniture/decorative-objects/sculptures/vasa-mihich-laminated-acrylic-multi-plane-sphere-flourescent-colors/id-f_787490), accessed 2026-10-31) [snippet].
- Microfluidics, which routinely seals open channels milled in PMMA with a flat cover sheet. It is the same idea at small scale.

**Keeping cement out of the void.** ACRIFIX's own warning settles it: a polymerizing cement must not enter a sealed cavity. Options:

1. **Cement on the flats only, with a dam.**
   - Mill a shallow relief groove, about 1–2 mm, around each hemisphere's rim.
   - Apply a measured bead of cement well outside the groove so the squeeze-out runs into the groove and not the sphere.
   - Microfluidics uses the same trick with solvent "retention grooves", which "greatly reduce" solvent-induced deformation of channels ([Wan et al., JoVE 2017, PMC5352265](https://pmc.ncbi.nlm.nih.gov/articles/PMC5352265), accessed 2026-10-31) [confirmed].
   - Risk: the sphere is sealed with monomer vapour inside. ACRIFIX advises at least 20 min of air flushing, so add a drilled vent to the sphere, flush it, then plug the vent with cement and polish.
2. **Solvent-assisted thermal bonding.** Wan et al. bond PMMA with 100 % ethanol at **70 °C, 2,300 kPa (≈ 23 bar), 2 min**. They cite Tg of cast acrylic as about 100–110 °C [confirmed]. Ethanol is a mild solvent; aggressive conditions round off channel walls. Bonding a large face at 23 bar needs a hydraulic press, about 23 t for a 100 × 100 mm face [derived].
3. **Thermal (diffusion) bonding.** Microfluidic studies bond PMMA near or above Tg:
   - 70–110 °C at 1.6–3.8 MPa for 2–8 min ([VJS study](https://vjs.ac.vn/index.php/jst/article/download/16577/2543254743/2543259004), accessed 2026-10-31) [snippet];
   - 108 °C recommended to limit channel distortion [snippet];
   - one group bonds at 165 °C under low pressure ([NTU](https://scholars.lib.ntu.edu.tw/handle/123456789/69348), accessed 2026-10-31) [snippet].

   Above Tg the voids sag and the faces distort, so larger hemispheres are at risk. Bonds with no adhesive are optically perfect, but they need flat, clean faces and a heated press. Lower-temperature CO₂-assisted bonding has been reported at about 40 °C [snippet, same NTU source].

The sheets must be dry (section 3.4). Water in cast PMMA plus heat makes new, unplanned bubbles.

### 4.2 Drilled channels, vacuum and pressure

Drilled channels can be plugged with a short rod and cement to make long, thin air "threads". Do this after annealing the drilled sheet, and polish the drilled bore so it reads as a clean silver line. Drilled bores are typically frosted unless polished; this is general practice **[unconfirmed]**.

Air sealed at room temperature rises in pressure by about 18 % at 70 °C (343/293 K) [derived], which stresses the walls of large voids during annealing. Air sealed at altitude, or shipped by air, behaves the same way. The effect is small for millimetre voids in thick PMMA **[derived, unconfirmed for large voids]**.

### 4.3 Why an air sphere inside PMMA looks silver

Total internal reflection happens when light in the denser medium meets a boundary at more than the critical angle θc = arcsin(n₂/n₁) ([UNSW Physclips, Total internal reflection](https://www.animations.physics.unsw.edu.au/jw/light/Total-internal-reflection.htm); [LibreTexts 2.9.05](https://phys.libretexts.org/Workbench/PhysClips_Light/02:_Geometrical_Optics/2.09:_Appendix/2.9.05:_Total_internal_reflection), accessed 2026-10-31) [confirmed]. For PMMA (1.49) to air, θc = arcsin(1/1.49) ≈ **42.2°** [derived]. The textbook case is an air bubble in water (θc ≈ 48.6°), which "shines" for the same reason [snippet, same sources].

Seen from outside, the outer ring of an air sphere in PMMA reflects totally, so it looks like a mirror ring with a clearer centre. For a sphere, rays from the viewer hit the surface at more than 42° outside a radius of sin(42.2°) ≈ 0.67 of the sphere's radius. About **55 % of the disc's area** looks silver [derived]. A lower-index fill makes the ring thinner. A water-filled void (1.33 in 1.49) has θc ≈ 63° and a much fainter ring [derived].

### 4.4 Subsurface laser engraving (SSLE)

SSLE focuses a pulsed laser inside a transparent block to make micro-fracture points. A Röhm-family patent reports that *doped* PMMA engraved with better precision than lead crystal, in three dimensions too ([US patent, laser subsurface engraving of plastic bodies](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7704586), accessed 2026-10-31) [snippet]. Crystal sellers claim acrylic "cannot be subsurface-engraved by the same process" and softens at high dot density ([Beyond Memories](https://beyond-memories.com/blogs/beyond-memories/subsurface-laser-engraving-explained), accessed 2026-10-31) [snippet; commercially biased].

Plain cast PMMA probably gives fuzzier, melt-type points than K9 glass, and points near the surface risk cracking it out. That conclusion is **[unconfirmed]**: test with a vendor.

Retail SSLE crystals cost about $39–299 per piece. Awards suppliers add about $14 per piece for a subsurface imprint and charge hourly for 3D modelling ([Beyond Memories cost](https://beyond-memories.com/blogs/beyond-memories/how-much-does-3d-crystal-engraving-cost), accessed 2026-10-31) [snippet].

### 4.5 "Controlled" bubbles in casting resin

The resin hobby works to remove bubbles: vacuum degassing before the pour, a pressure pot during the cure ([Smooth-On](https://support.smooth-on.com/knowledgebase.php?article=47), accessed 2026-10-31) [snippet]. Deliberate bubbles are made the other way round: skip the pressure, inject air with a needle into gelling resin, or, as Moore does in reverse, move them with a needle before gelation (Moore 2006) [confirmed for moving bubbles]. These give organic, irregular bubbles. Milled hemispheres give geometric ones.

---

## 5. Heat, and what must never go inside

### 5.1 Acrylic's limits

| Limit | Value | Status |
|---|---|---|
| ACRYLITE cast, continuous service | −40 to 180 °F (≈ 82 °C) | confirmed ([ACRYLITE service temperatures](https://www.acrylite.co/resources/knowledge-base/article/what-are-the-recommended-continuous-service-temperatures-for-acrylite-acrylic-sheet), accessed 2026-10-31) |
| ACRYLITE extruded, continuous service | −30 to 160 °F (71 °C) | confirmed (same page) |
| Vicat softening, GS cast | ≥ 105 °C | snippet ([Klefinghaus datasheet](https://www.klefinghaus.de/datasheet/DOK_DATA_Datenblatt-Acrylglas_SEN_AIN_V4.pdf), accessed 2026-10-31) |
| Vicat softening, other cast sheet | ≈ 115 °C | snippet ([builditsolar](https://www.builditsolar.com/References/Glazing/physicalpropertiesAcrylic.pdf), accessed 2026-10-31) |
| Tg, cast acrylic | ≈ 100–110 °C | confirmed (Wan et al.) |
| Flammability | UL 94 HB is the usual rating: it burns at a limited horizontal rate and does not self-extinguish | snippet ([specialchem LG PMMA](https://www.specialchem.com/plastics/product/lg-chem-lg-pmma-hi835h), accessed 2026-10-31) |

A bonded laminate with an object inside should stay below the 70 °C anneal ceiling in service. Annealing temperatures are what *relax* stress, so service near 70–80 °C slowly moves the bonded block [derived].

### 5.2 Never inside a lamp or speaker block

- **Undried organics, wood, paper, leather, foams, rubber.** They outgas when warm (mist, bubbles, silvering) and keep shrinking (Moore 2006; USAcrylic) [confirmed].
- **Unknown plastics.** They may warp at temperature or be attacked by monomer [confirmed for heat, unconfirmed for monomer].
- **Polished or large rigid metal near the surface, or anything with a high CTE mismatch.** Polished metal debonds and silvers (USAcrylic) [confirmed]. Large metal or glass parts crack the block in cold weather [confirmed, USAcrylic]. PMMA expands roughly 5–9 times more than steel or glass, which is why [unconfirmed figure, general knowledge].
- **Anything flammable near an LED driver or LED board.**
- **Magnetic media (cassette tape, cards) near speaker magnets.** Erasure needs a field of about 2–5 × the tape's coercivity; 300 Oe tape is typical of older formats ([Fujifilm degauss note](https://asset.fujifilm.com/www/co/files/2020-03/347d42e6726e8969827ac1f90f92d490/Degauss-Data-Tape_01-11.pdf), accessed 2026-10-31) [snippet]. Stray fields of 10–50 Oe can already partially erase and imprint tape ([IASA stray-field measurements](https://www.iasa-web.org/book/export/html/834), accessed 2026-10-31) [snippet]. A dipole field falls roughly with the cube of distance [unconfirmed here, standard physics]. Keep tape objects several magnet diameters from any driver magnet, or show them in a non-speaker edition.
- **Batteries, or anything that can vent.**

### 5.3 LED heat in an acrylic lamp

LED design guides target a junction temperature of about 85 °C ([Electronic Design, LED light engine](https://www.electronicdesign.com/technologies/industrial/boards/article/21796133/fundamentals-of-led-light-engine-design), accessed 2026-10-31) [snippet]. The board and heat sink then sit only a few degrees below that, which is above acrylic's 82 °C continuous limit [derived]. Acrylic optics transmit more than 90 % (same source) [snippet].

So:

- Keep LEDs on a metal heat sink with an air gap to the acrylic.
- Never bond a hot LED board directly into the block.
- Keep embedded objects away from the light-entry face.
- Measure the acrylic's surface temperature at full power in a closed room before release.

### 5.4 UL, briefly

UL 1598 covers luminaires and UL 8750 covers LED equipment and drivers, used together ([Intertek UL 8750](https://www.intertek.com/lighting/standards/ul-8750/), accessed 2026-10-31) [snippet]. Under UL 1598 (4th ed., 2018), an LED lens or diffuser that serves as an enclosure needs at least a **V-0** rating when live parts are spaced more than 0.8 mm away. Otherwise it needs 5VA ([UL 1598 4th ed., law.resource.org](https://law.resource.org/pub/us/cfr/ibr/inc/ul/ul.s1598.4.2018.pdf), accessed 2026-10-31) [snippet; a historical edition, check the current one].

Typical PMMA is only HB. The inference is that an acrylic body should not be the electrical enclosure. Put the driver and mains wiring in a metal or rated enclosure, and keep the acrylic decorative. That is an interpretation, **[unconfirmed]**; confirm with a certification lab. Speakers with built-in amplifiers fall under UL/IEC 62368-1 **[unconfirmed, not researched here]**.

---

## Open items to confirm before a first edition

1. Cured refractive index and volume shrinkage of ACRIFIX 2R 0190 and Weld-On 40. Ask Polyvantis/Plaskolite and IPS for the full TDS.
2. Whether a hemisphere-pair void survives a 70 °C anneal with no cement creep into it. Bond test coupons at 5, 10 and 20 mm sphere diameters.
3. Sealer compatibility: acrylic spray, shellac and PVA on a test object, soaked 24 h in mixed ACRIFIX.
4. SSLE sample in EARF's tinted cast sheet from a US vendor.
5. Quotes from Clear Image and Em-Bed-It for a cast comparison piece. Use a metal object; organics only after a sample pour.
