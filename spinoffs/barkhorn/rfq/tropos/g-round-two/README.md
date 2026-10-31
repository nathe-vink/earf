# Tropos's quote requests, round two (2026-10-31)

Round one (`../a-cast-acrylic` to `../f-layer-cutting`) covers the acrylic, the horn, the metal and a first letter for
the small jobs (`../d-other`). Round two gives each small job its own letter and names a source for every part of the
first pair that the parts list still calls "any". **Public web research only: nobody has been contacted, no form
filled, no account opened.** Every shop below is a candidate to confirm on its own site before anything is sent.

The letters are in `letters.md`, each with a short web-form version and an email version.

**Attachments:**
- `../d-other/drawings.pdf`: the lining's sheets 4 and 22 to 25, the disc frame's 16, the back's 10;
- the amplifier compartment's sheet 30, from `../c-metal/drawings.pdf`, for the gasket;
- the lining DXFs (`spinoffs/barkhorn/out-cloud/dxf/`, `lining-*`);
- the wordmark's vector file.

## The four jobs

| job | parts (`out-cloud/bom.md`) | candidates (from public pages) | route | notes |
|---|---|---|---|---|
| **1. Lining sleeves** (sewing) | `lining-sleeves`, and the batts `lining-*` (32 a pair) | **Maylin Sewing Company**, 4044 San Leandro St, Oakland: in-house cut and sew, cutting to packing ([Maker's Row guide](https://makersrow.com/blog/apparel-manufacturers-oakland-ca/)) | its own site or phone (not checked here) | minimums not published |
| | | **D.A.D. Sewing House**, San Francisco: cut and sew for designers, including interior soft goods ([Maker's Row guide](https://makersrow.com/blog/find-reliable-garment-manufacturer-san-francisco/)) | its site's contact form (to find) | soft goods named, the best fit |
| | | **Stitch It**, Oakland: prototype sewing ([Gust](https://gust.com/companies/stitch_it)) | not found | from round one; unconfirmed |
| **1b. The batts themselves** | `lining-*` (about 2 m² a speaker, 50 and 100 mm) | **FoamOrder**: 100 % polyester Dacron wrap in sheets and rolls, volume discounts ([page](https://www.foamorder.com/batting/dacron-wrap)); **Sailrite** CushionRite, thermally bonded 100 % polyester, 55 in rolls ([page](https://www.sailrite.com/Batting-83-Thick-55-Wide)); **Monacor MDM-2**, speaker wadding 630 x 330 x 35 mm, from European distributors ([audiophonics](https://www.audiophonics.fr/en/absorbents/monacor-mdm-2-speaker-damping-polyester-130g-63x33x35cm-set-x2-p-1365.html)) | online orders; FoamOrder's email in `letters.md` | **No US maker of speaker-grade polyester batts at 50 to 100 mm was found.** The route is to stack upholstery batting to the thickness, then check its density on the first cabinet. |
| **2. Cloth disc** (cloth, and fitting it) | `cloth-disc` over `disc-frame` | **Parts Express** grille cloth by the yard: Mellotone Premium Black 64 in, black, grey and white 70 in ([black 70 in](https://www.parts-express.com/Speaker-Grill-Cloth-Black-Yard-70-Wide-260-335), [Mellotone](https://www.parts-express.com/Mellotone-Premium-Black-Speaker-Grill-Cloth-Yard-64-Wide-260-332)) | online, with the electronics | one yard of black for the Smoke pair |
| | | **Michael's Custom Built Upholstery**, San Rafael: a full-service upholstery shop ([listing](https://telli.com/marin/biz/34446)) | phone (from the listing) | panels not mentioned; ask |
| | | **In-house**: contact adhesive at the back of the ring, about 20 minutes a disc | — | likely the fastest for two discs; a shop for 20+ |
| **3. Etched wordmark** | `mark-back` (and the `rating-plate` on aluminium) | **Ponoko**, Oakland: online laser cutting and engraving, with a guide to colour-filling laser detail ([colour fill](https://www.ponoko.com/blog/ponoko/add-colour-to-your-laser-cut-detail/)) | online quote, hello@ponoko.com | bed size against a 518 x 838 panel to confirm |
| | | **Zap'O Marks, Inc.**, 3851 Charter Park Dr, Suite S, San Jose: laser marking and engraving for Northern California ([profile](https://directory.designnews.com/zap-o-marks-inc-comp228851.html)) | 408-264-8610 | also the right shop for the anodised rating plate |
| | | **Neal's CNC**, Hayward: laser cutting and etching, acrylic listed (R8) | 510-783-3156 | can also cut the horn's layers (`../f-layer-cutting`) |
| **4. Seals and gaskets** | `back-seal`, `amp-box-gasket`, `cap-o-ring`, `post-sleeves`, `gasket` | **Bay Seal Company**, Hayward: spliced O-rings and gaskets, EPDM stocked, custom moulding, extrusion and lathe-cut ([SEMI](https://semi.org/en/resources/member-directory/bay-seal-company)) | [get-a-quote](https://www.bayseal.com/get-a-quote/), info@bayseal.com, 510-732-7000 (round one) | ask first; whether it vulcanises EPDM cord is not stated |
| | | **Bay Rubber Company**, Concord: a fabricating distributor and contract maker since 1952 ([Made in California](https://www.cmtc.com/made-in-california-profile/bay-rubber-company)) | its site, bayrubber.com | the die-cut sponge frame |
| | | **Global O-Ring and Seal**, Houston: vulcanised rings from cord, small quantities ([vulcanised rings](https://www.globaloring.com/vulcanized-rings/)) | [RFQ](https://www.globaloring.com/rfq/), 832-448-5550 (round one) | the fallback for the cord loop |

## Every part still sourced as "any": a named source

These are stock parts. A catalogue order needs no letter. The SKUs are to pick at ordering, and prices are the parts
list's estimates.

| part (`bom.md`) | what | named source | note |
|---|---|---|---|
| `cloth-disc-magnets` | 15 x 3 N42 discs, steel discs | K&J Magnetics (US); or McMaster-Carr | K&J sells inch sizes: 5/8 x 1/8 in (15.9 x 3.2) is the nearest; the pockets take it |
| `hf-pad`, `hf-capacitor`, `terminals` | 25 W wirewound resistors (Vishay Dale RH-25 kind), a 33 µF 100 V film capacitor, 6.3 mm terminals | Digi-Key or Mouser (resistors, terminals); Parts Express (film capacitors) | order with the FA122s in week 1 |
| `lead-hf`, `lead-woofer`, `link-cable` | silicone 2 x 0.5 mm² cable, 2 x 1.5 mm² speaker cable, a 5 m 75 Ω RCA coax | Parts Express | with the electronics |
| `cable-glands` | M12 glands for 3 to 6.5 mm | McMaster-Carr: **nickel-plated brass**, not nylon (`make/compliance.md`) | three a speaker |
| `cap-o-ring` | 182 x 2 mm EPDM 70 | Global O-Ring and Seal, or McMaster-Carr (metric O-rings) | a standard size to confirm; if not, a vulcanised loop as the back seal |
| `post-sleeves` | polyurethane 90A, ø12 x 10 x 13 | McMaster-Carr: polyurethane rod or tube, cut | or a stock flanged bushing |
| `gasket` | 1.5 mm closed-cell foam strip | McMaster-Carr | — |
| `lining-tape` | VHB 4910 dots | McMaster-Carr or Uline (3M VHB) | — |
| `back-screws`, `port-screws`, `woofer-fixings`, `hf-fixings`, `amp-fixings`, `amp-box-fixings`, `earth-bond`, `tie-rod`, `loom` | stainless screws, thread-forming screws for plastics, threaded rod, a knurled nut, an earth stud and lead | McMaster-Carr | one order |
| `back-inserts`, `feet-inserts`, `woofer-fixings` inserts | knurled brass inserts M4, M5, M6, M8 | McMaster-Carr | **bonded with epoxy after the last anneal and cementing.** R8: no brass near the polymerising cement, which inhibits its cure |
| `feet` | M8 levelling feet, 40 mm swivel base | McMaster-Carr | — |
| `cement` | Weld-On 40 or ACRIFIX 2R 0190 | ePlastics (Weld-On 40 gallon kit $197.77, "limited availability", R8), Chemical Concepts, or TAP Plastics stores | the cabinet shop may supply its own |
| `remote` | an AAA RC-5 remote, in place of Hypex's coin-cell one (`make/compliance.md`) | a programmable universal remote (Parts Express or a big-box retailer) | test RC-5 device 16 with the FA122 |
| `rating-plate` | 70 x 40 x 1 anodised aluminium, laser-marked | Zap'O Marks (above), or Ponoko | the CE, UKCA and FCC marks only once earned |
| `mark-back` | the etched wordmark | job 3 above | — |

**Covered elsewhere:**
- the woofer, the FA122, the HF driver and the remote kit (named suppliers in `bom.md`);
- every acrylic, horn and metal part (`../a-` to `../f-`).
