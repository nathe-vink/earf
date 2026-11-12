# Tropos detail pass (2026-11-12)

**What this is:** finish and detail only, under the owner's bar ("classy and refined and not cheap"; the coordinator's
brief of 08:59, items A to H).
- No signed shape or size changes.
- Everything below is in the CAD (`cloud.py` switches it on; `product.py` and `variants/variants.py` draw it).
- It is also in the parts list (`out-cloud/bom.csv`, `rfq/tropos/PARTS-FINAL-DESIGN.md`), the engine files
  (`studio/products/barkhorn-cloud.json`, `barkhorn-variants.json`) and the asset (`asset/tropos-strata.blend` and its
  manifest).
- Before and after, Ice: `renders/2026-11-12/barkhorn/detail-pass/`.

| | item | was | now | why it can be done |
|---|---|---|---|---|
| A | **feet** | zinc-bright stems and round nuts under a black pad | stem and M8 jam nut (13 across flats, 5 thick) black oxide, the swivel base black, the pad satin black NBR | a stock option of the same foot; nothing bright under the cabinet |
| B | **back screws** | 22 M5 button heads, black, on nylon washers; 4 along the top and the bottom (pitch 167 there, 137 up the sides) | 24 M5 x 30 countersunk socket heads (ISO 10642, A2 black), flush (the head 0.1 under the face), in 90 degree countersinks; 5 along the top and the bottom (pitch 125), 7 up each side (137), 4 into the braces' bosses | the back is 20 mm cast acrylic: a countersink cut with a single-flute cutter and polished, no washer, 1.5 N m. The back seats hard on the lands and the cord seal seals it, so the screws only hold it there |
| B | **woofer's eight screws** | M6 ISO 7380 button heads, 10.5 x 3.3, black oxide | M6 x 25 black ultra-low heads, 13 across, 1.8 high | **flush is not possible** (see below) |
| C | **ports' flanges** | 140 square, R10 corners, four black M4 countersunk screws in tapped holes | a round ring 140 across, the same 8 thick, one 1.5 x 45 degree chamfer round its outer front edge, diamond-polished; cemented into a round recess, flush, no screws | the tube, the frame's thickness and so the port's length are unchanged: the tuning is unchanged. The port needs no service: the back comes off for everything inside |
| D | **the HF lead** | up the Cloud's cable post, then a loose-looking diagonal run in the pod, black rubber, which caught the sweep as two pale lines through the horn | up the cable post's 7 bore its whole length (the Strata rod, rear, x 240); in the pod in black braid, square runs only: back along the floor, up behind the driver's motor to its terminals, two clear clips | numbers below |
| E | **inside the cabinet** | the IR board on a clear bracket in the open gap under the brace; its lead across the middle; leads in black rubber; the terminals bright | the IR board in a cup in the lining's colour, in a pocket in the bottom batt's front face, 40 left of centre (clear of the bottom rib); its lead, sleeved in the same colour, in a groove under the batt and up the gap in front of the back's lower batt; every lead in black braided PET sleeve; the woofer's and the HF driver's terminals booted black; the tie rod black | see "Where the eye sees from" |
| F | **rating plate** | a 70 x 40 black anodised plate with two screws, printed white | engraved in the back's outer face over the compartment's black flange, in the 19 mm band under the FA122's plate: grey on black, no plate, no screws | every line kept (below) |
| G | **amp plate** | Hypex's FA122 plate | unchanged and uncovered: it sheds the amplifier's heat | the one bright bought part (its XLR shells, RCAs, labels) |
| H | **lining** | the polyester batts (white; black in Smoke) | unchanged, except the bottom batt's pocket and groove for the IR (item E) | |

## A. Feet

The approved build stands on its own feet (base A).
- **Each foot:** an M8 stem in a bonded insert, a jam nut locking it, and a 40 mm swivel base on a pad.
- **Now:** the stem and nut are black oxide, the base black, the pad satin black NBR.
- **From the floor:** the eye sees black only, the nut a hex, as in the CAD.

Parts: `levelling-feet-black`, $22 a set of 4, was $18 (estimate).

## B. Screws

**The back.**
- The screws are evenly spaced round the edge:
  - 7 up each side at 137;
  - 5 along the top and the bottom at 125 (it was 4, at 167, which read as gaps);
  - the 4 tie screws into the braces' bosses as before.
- Countersunk socket heads, black, flush.
- **Acrylic and countersunk heads:** a cone can wedge and craze the acrylic. Three things prevent it:
  - the countersink is cut 0.4 over the head and polished;
  - the head sits 0.1 under the face with no washer;
  - the screw is torqued to 1.5 N m. The back seats on the milled lands, so the screw never draws the back down
    against a gasket.

Parts: `back-screws-flush`, $14 a speaker, was $10. Machining: 24 countersinks on the back's own CNC operation.

**The woofer.**
- The FaitalPRO 15PR400's cast flange has **slots** (9.5 x 7.4) for its eight screws, not round holes. A countersink
  cannot seat in a slot. Countersinking the slots means machining the bought driver's frame, which we will not do.
- So the screws stay just proud: black ultra-low heads 13 across (wide enough to cover the slot) and 1.8 high, where
  the button heads were 3.3.

Parts: `m6-acrylic-inserts-low`, $20 a set of 8 with the inserts, was $14.

## C. Ports

- The square flange with four corner screws is gone.
- **The ring:** a round ring 140 across, cut from the same 8 mm sheet.
  - Its bore is the port's.
  - Its mouth is rounded R8 as before.
  - One 1.5 x 45 degree chamfer runs round its outer front edge, diamond-polished: one line of light.
- **Fitting:** the ring is cemented into a round recess 140.5 across and 9 deep, flush with the panel. The bond is on its
  back face, behind the ring.
- **Tuning unchanged:** the tube, its flares and its length are untouched, so the box still tunes to fb.
- **Service:** the port's length is found on the first sample, which is dry-fitted before it is cemented. Nothing inside
  is reached through a port; the back comes off.

Parts: `port-fixings` out, −$5 a speaker. The cement is in the cement line.

## D. The HF lead in a post

**The route.**
- The approved build's rear posts are ø16 aluminium rods.
- The cable post (rear, x 240) is now bored 7 through its whole length. The lead goes up the bore from the gland under
  the top, through the pad's bore and the pod's floor.
- That leaves about 120 mm in the pod, from the floor to the driver's terminals, which no post can hide. The pod sits
  between the post's top and the driver.
- That run is now:
  - in black braided sleeve;
  - in square runs: straight back along the pod's floor, then straight up behind the driver's motor (the motor hides
    it from the front);
  - held by two clear clips on bonded pads;
  - ended in a black boot on the terminal.
- Nothing hangs.

**The numbers.**

| | |
|---|---|
| post | ø16, 6061-T6, black anodised; bore 7 |
| bending stiffness | I = 3,099 mm4 against 3,217 solid: **96 %** |
| thread | M12 x 1.25 (fine) at the top; root ø10.47; wall under the root **1.7**; 47.6 mm2 there, about **11 kN** to yield, against a horn of about 9 kg on four posts |
| lead | 2 x 0.5 mm2 silicone, 5 across; 6 in its sleeve over the pod's run only; **51 %** of the bore's area bare, **73 %** sleeved where it enters |
| assembly | pulled up from the compartment's end with the ferrules on, before the compartment's 2-way connector is crimped |

**Why not the alternative.** The coordinator's alternative was a black cloth-braided cable along the back of a post, as
a designed part. It is not needed: the lead fits the bore.

## E. Inside the cabinet: where the eye sees from

**The IR receiver.** It must see the room through the front panel's tint, so it cannot go behind anything opaque.
- It now sits in a cup in the lining's own colour (12 mm opaque cast acrylic: opal white, black in Smoke; closed round
  and behind the board, two holes for the eye and the LED). A black cup was tried first: against the white batts it read
  as a black mark low in the front (the first after frame), so the cup and its lead now take the batt's colour.
- The cup sits in a pocket cut in the front face of the bottom batt, between the ports, 72 up.
- It is 40 left of centre as you face the front. At the centre the bottom rib is in the way.

From each side of the speaker:
- **From the front, at any height:** a face in the batt's colour with two small dots, set into the batt, behind the
  tinted panel.
- **From the sides:** the side panels show the bottom batt's end; the cup is inside the pocket.
- **From behind:** the back's lower batt covers it.

**Its lead.**
- It drops out of the cup's back in a 12 x 24 channel cut down the bottom batt's front face, below the pocket.
- It runs in a 12 x 12 groove under the bottom batt to the batt's back end (the clash check found the first route, a
  10 x 10 groove alone, passing through the batt where the lead drops).
- It rises in the 10 mm gap in front of the back's lower batt, which hides it from behind.
- It passes forward under the amplifier's compartment and up the compartment's front, where the woofer hides it from the
  front, to the third gland.
- From the front, it is visible only in the open band between the bottom batt and the first brace (72 to 200 up),
  looking straight back: there it is black braid against the black back batt.

**The other leads.** All three (HF, woofer, IR) are now in black braided PET sleeve. Black heat-shrink covers the
ends. Each lead runs along a batt's face or an edge on the loom's tie bases, on the routes the CAD already had: the HF
lead up the back's upper batt's inner face, the woofer's under the motor to the basket's lower spoke.

**Woofer terminals.** They take fully insulated 6.3 mm push-on terminals in black nylon boots, which cap them. The HF
driver's take the same.

**The tie rod.** It is visible in the pod through a polished horn, so it is now black-coated A2, with its nut and
washer.

**What the eye still sees inside, as designed:**
- the woofer's basket (black);
- the compartment (black anodised);
- the glands (black);
- the brass sockets of the Cloud's posts. These are hidden in the approved build: the Strata rods stand in their own
  collars.

## F. The rating marking

**What changes.**
- The separate plate and its two screws are gone.
- The same lines are laser-engraved 0.1 deep in the back's outer face, in the band under the FA122's plate. Behind that
  band is the compartment's black anodised flange (158 wide, 19 tall), so the frosted engraving reads grey on black.

**Every required line is kept:**
- EARF TROPOS;
- HORN LOUDSPEAKER, ACTIVE, MODEL TR-1, S/N TR1-26-000127 (engraved per unit at the back's last operation);
- 100-120V~ / 200-240V~, 50-60 Hz, 350 W MAX (the FA122's own rating);
- DESIGNED IN SAN FRANCISCO, CALIFORNIA;
- the WEEE bin.

The CE, UKCA and FCC marks are added when earned, as before.

**Durability.** An engraving passes IEC 62368-1's rub test (F.3.10) as a mark in the material.

Parts: `rating-plate` ($10) out, `rating-engraving` (about 3 minutes on the cabinet shop's laser, $4) in.

## G. The amplifier plate

**No change.** It stays uncovered, because it sheds the FA122's heat.

**The bright bought part.** It is the one bright part of the back, as Hypex makes it: the XLR shells, the RCAs' rings,
the grey label strips, the rating sticker's foil.

**A plain plate** is the coordinator's question for the owner.

## H. Lining

No change, except the bottom batt's pocket and groove (E).

## What cannot be done, and why

**The woofer's screws cannot be flush.** The bought cast flange has slots. They are now low black heads instead.

**The HF lead cannot be hidden for its last 120 mm.** No post reaches the driver: the pod is between the post's top and
the driver's terminals, and the pod is clear acrylic. That run is now short, square, sleeved black, clipped and partly
behind the motor.
