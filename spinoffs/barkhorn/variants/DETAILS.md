# Tropos: the real details (2026-10-31, the design pass)

The owner asked for "realistic": buildable in every detail, and pictured as a real object. This note takes each detail
the coordinator listed and does three things:
- says how the current design makes it, with its drawing in the Cloud's set (`out-cloud/drawings/`, BHC-0nn) and its
  part in `out-cloud/bom.md`;
- checks it with a number where one matters;
- says what the design pass changes, if anything. The proposals are in `STRATA.md` and `TOPO.md`.

The blind critique that drives the changes is `renders/2026-10-31/barkhorn/design-pass/critique/current-tropos.json`;
its ten least realistic details are marked "critique #n".

| detail | how it is made now (drawing, part) | the check | the design pass |
|---|---|---|---|
| **Rear panel** | The back is a removable 20 mm panel on lands and the braces' bosses: 22 M5 button heads into bonded brass inserts, over a 4 mm EPDM cord seal (BHC-010, `back`, `back-seal`). The FA122's aluminium plate sits in its cutout with the plate's own mains inlet, switch and signal inputs, as Hypex makes them, so no extra jacks are cut. The rating plate is beside it (`rating-plate`). EARF is etched above, colour-filled (`mark-back`). | The seal holds the box airtight for the port tuning, and the 22 screws give one per 115 mm of perimeter. | Unchanged. The pictures must show it: the critic never saw the back. A rear three-quarter detail render is in the plan. |
| **The IR window** | The receiver sits behind the front panel's own tint, low and centred between the ports, on a clear bracket. The fallback is a clear ø12 rod bonded through the panel (`ir-bracket`, `ir-window`, BHC-030 and 033). | IR at 940 nm passes tinted cast sheet well. The fallback exists if the darkest tint blocks it. | Unchanged. |
| **The plate amplifier: mounting and cooling** | The FA122 plate is outside on the back. It is held by eight M4 inserts, with M4 × 16 screws in nylon shoulder washers through holes opened to 5.5 so it can slide (acrylic grows 0.4 mm more than aluminium over 315 mm at +25 K), on 3 mm EPDM tape. Inside, its module is closed in an earthed aluminium box (`amp-box`, BHC-030; `make/compliance.md`). | **Heat:** class D at about 90 %. Full output (2 × 125 W) is about 25 W of loss, music at a tenth of that about 5 W, and standby 0.5 W. All of it leaves through the plate, a heatsink in room air. The four-hour heat test is in `make/fai.md`. | Add the aluminium collar and brass glands from `compliance.md`. |
| **Internal bracing** | Two full braces (`brace`, `brace-2`) with windows, and ribs on the sides, back, top and bottom (`rib-*`, BHC-004, 011, 012), all 20 mm cast sheet, cemented. The lining's batts sit between the ribs in voile sleeves. | The panels' first modes sit above the woofer's band as braced (round 35). | **Critique #8** (the inside reads as a workshop): line the batts up on the ribs' grid, with clear clips, no tape showing. It is a drawing and an assembly rule, not a part. |
| **Feet and floor protection** | Four M8 levelling feet, a 40 mm swivel base on a rubber pad, in bonded M8 inserts in the bottom (`feet`, `feet-inserts`). The front and back feet sit 25 mm from the edges for tipping. | Each foot carries about 175 N, 71 kg over four. The 40 mm pad loads the floor at about 0.14 MPa, safe on oak or tile. | **Critique #10** (tiny pins): turned feet in the horn's tint, ø50 × 25, a stack of two 1/2 in discs with a polished edge, on a stainless M8 stud and a felt glide. They read at a 1.3 m speaker's scale. About $40 a set (est.). |
| **How the horn sits on its posts** | Four 304 stainless tubes, ø10 × 7, in brass sockets bonded in the top, each centred by a PU 90A sleeve. Their M10 × 1 ends thread into inserts in the horn's acrylic pads (`post-*`, `post-sockets`, `post-sleeves`, `horn-pads`, BHC-029 and 031). A tie-rod with a knurled nut holds the horn down. | The assembly weighs 8.3 kg (formed) or 9.9 kg (stepped), about 25 N a post, an axial stress under 1 MPa. Buckling is far off at these lengths (60 to 130 mm). | **Critique #4 and #5** (thin rods, the horn hovers): posts ø16 bronze, the same fixings at M12, with the HF cable inside the rear left post (below). They read as able to carry a 10 kg horn. About +$60 a pair (est.). |
| **Fixing the drivers** | **Woofer:** front-mounted in a rebate, on M6 brass inserts bonded in 8.5 holes, with M6 × 25 button heads and a 1.5 mm closed-cell gasket (`woofer-fixings`, `gasket`). **HF driver:** on a turned aluminium adaptor ring (`hf-adaptor`, four M6 countersunk on 101.6), the adaptor to the horn's boss on four M5 into inserts (`hf-fixings`). | The woofer's flange holds by eight M6 at 15 N·m into knurled inserts (the inserts' pull-out is well above). | **Critique #3** (the throat collar reads as a blob): the turned adaptor and its four screw heads are shown, as they are drawn. That is a render fix (the formed horn's throat piece is real but its outline was smoothed). |
| **Grille or none** | A cloth disc on a 12 mm acrylic ring frame, held by four neodymium magnets in the panel and four steel discs in the frame (`cloth-disc`, `disc-frame`, `cloth-disc-magnets`). | — | **Critique #2 and cooler #5:** in Strata, none. The woofer sits in the stepped caldera, its cone and basket seen. The disc stays an option for homes with children. |
| **The cable from the horn to the cabinet** | The HF lead runs up the cabinet's back batt and through an M12 gland under the top. It then climbs the **cable post**, a 7 mm bore in one rear post, into the pod (`lead-hf`, `cable-glands`). | Hidden by design already. | **Critique #5** saw two driver rods and a wire because of the formed horn's pod and tie-rod. With ø16 bronze posts the cable post is the only path, and the tie-rod hides in the rear pair. |
| **The rating plate** | Black anodised aluminium, 70 × 40 × 1, laser-marked (model, serial, ratings, WEEE bin), on two M3 into inserts beside the plate amplifier (`rating-plate`). It carries no CE, UKCA or FCC marks until earned. | — | Unchanged. |
| **The edge finishes** | Show edges are polished: diamond-milled then buffed. The stepped horn's layers are polished before bonding. Inside edges are milled square. No flame polish near a joint (`make/laminated-horn.md`). | — | **Critique #1** (the edges draw black): a polished edge in tinted cast sheet is its brightest, most saturated line. That is a render fix: the edges need their own material (higher roughness for milled, a polished bevel, so light pipes along the sheet). It is listed for the realism pass. |
| **The bond lines, shown honestly** | Polymerising cement (ACRIFIX 2R 0190 or Weld-On 40), 0.5 to 1.5 mm, dead weight on spacers, annealed (`make/laminated-horn.md`). | 21 joints in the stepped horn. | **Critique #9** (every layer perfect): render each bond line as a 0.5 mm layer of slightly different index (1.48 against 1.49) with a faint haze, and let the layers' thickness vary ±0.2 mm. That is a realism-pass item. |

## The realism pass (the picture side)

These come from the critique and the coordinator's list. Each is a change to the engine's materials or the shots,
not the object.

| item | now | to do |
|---|---|---|
| tint absorption, calibrated | from the site's hexes | from the seller's own light transmission (`make/stock_tints.py`, e.g. 2064 at 29.3 % total), as in the stock flavours |
| IOR | 1.5 | 1.49 (PMMA) |
| polished and saw-cut edges | one material | edges as their own material: polished (rough 0.02) or milled (rough 0.25 with a fine bevel) |
| bond lines | a 0.2 mm air gap | a 0.5 mm cement layer, index 1.48, faint haze |
| wear | none | a very faint fingerprint and micro-scratch roughness map on top faces, at grazing light only |
| caustics | colored shadows already (the acrylic tints shadow rays through its volume) | no MNEE: Cycles' MNEE ignores volume absorption and throws a white caustic (the lamps lane). Keep the tinted shadow rays, and path-traced refractive caustics only where a pool of light must show |
| scale cues | few | a hand, a record sleeve, a chair: one per scene |
