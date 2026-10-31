# Tropos "Strata" (a proposal, 2026-10-31)

**The idea:** make lamination the line's signature, and let the cabinet answer the horn. The stepped laminated horn
(22 layers of stock 1/2 in cast sheet, `make/laminated-horn.md`) becomes the hero. The woofer sits in a **caldera**:
three stepped rings of the same 1/2 in sheet in the cabinet's color, so the horn's contour lines begin at the woofer.

The blind critique of the current Tropos (`renders/2026-10-31/barkhorn/design-pass/critique/current-tropos.json`)
asked for exactly this:
- its "cooler #1": lamination as the signature, carried into the cabinet;
- its "#5": drop the flat grille disc;
- its least-realistic #2 (a pasted-on disc) and #7 (a dyed ring round the woofer).

## What changes

| | current | Strata |
|---|---|---|
| horn | formed shell in the horn lot (or stock 3/8 in), with a turned throat piece | **laminated, stepped**: 22 layers of stock 1/2 in plus a boss, each edge polished before bonding (`horn-plan-b`) |
| front of the woofer | a cloth disc on a 12 mm acrylic frame, magnets, and a 6 mm ring in the ring color | **a caldera**: three rings of 1/2 in sheet in the cabinet's color, Ø500 outside, bores Ø400, Ø436 and Ø472, stepping out toward the room, bores and outside edges polished (`caldera-1` to `-3`) |
| grille | the cloth disc | **none** (the woofer's cone and cast basket show). The cloth disc stays an option. |
| everything else | — | unchanged: cabinet, braces, volume, ports, drivers, amplifier, posts |

**Acoustics, kept intact:**
- **Volume and port:** the internal volume and the port are unchanged, because the rings sit outside the front panel's
  face.
- **Horn:** the air path is unchanged (`make/laminated-horn.md`).
- **The woofer:** its cone now sits at the bottom of a 38 mm stepped recess, 400 mm across at its narrowest. That is a
  short waveguide whose smallest bore clears the 393 mm frame. At the 900 Hz crossover the wavelength is 380 mm. The
  recess is under a tenth of it deep and wider than the cone, so it changes the woofer's response by less than the
  cloth disc did (est.). Check it with the first measurement.

## Round two: the blind duel's three changes (2026-10-31)

A blind four-way duel (`renders/2026-10-31/barkhorn/design-pass/critique/duel-1.json`) ranked the designs:

| design | score |
|---|---|
| Strata | **8.0** |
| current | 7.0 |
| Topo | 6.0 |
| Topo Clear | 5.5 |

Its three changes for Strata are now drawn:
1. **A defined, polished front lip.** The mouth's layer is cut 20 mm outside the air path, against 10 on the other
   layers. That gives an even, flat front face round the mouth, polished, so the rim reads as a deliberate edge. It adds
   about 0.27 kg (est.). The other 21 layers are unchanged.
2. **A visible mount.** The posts are now ø16 bronze rods (C93200 or C544), against ø10 stainless tubes. Each has a
   turned collar on the top plate (ø28 × 8) and one under the horn's pad (ø24 × 6), with an M12 thread into the pad's
   insert (`strata-posts`, `strata-collars`).
   - They stay four, at the reviewed positions. "Fewer" (the critic's word) would change the load path the tipping
     check and the posts' modes were worked on. That needs its own structural review first, so it is noted, not
     drawn.
   - They add about 0.65 kg (est.).
3. **The caldera in the horn's rhythm.** The rings' bores are now Ø400, Ø427 and Ø454: 13.5 mm steps, the horn's own
   step at its mouth. Each ring is the horn's 1/2 in, and the edges are polished square like the horn's.

**The build facts are unchanged for the deck:** the horn is still **22 layers of 1/2 in stock cast sheet** (plus the
boss). Only the mouth's layer is cut wider.

## Round three: the duel against the current design (2026-10-31)

A second blind duel (`renders/2026-10-31/barkhorn/design-pass/critique/duel-2.json`) set Strata's round two against
the current design. The same framing was used for both, cover off and the whole speaker in frame.

| | Strata | current |
|---|---|---|
| the studio hero | **7.0** | 5.5 |
| in use (the room at golden hour) | **7.0** | 5.0 |

Strata was preferred in both pairs. The critic's words: "a signature that nothing else on the market has", and the
horns "keep reading as sculpted, intentional objects at room scale".

**Its notes, and what happens to each:**
1. *Calm the cabinet's inside* (fewer, deliberate braces; hide the electronics and wiring). This is the current
   design's critique #8 too (`DETAILS.md`). The braces set the panels' modes, so they are not cut for a picture.
   - What can change without a review: the batts lined up on the ribs' grid, clear clips, and the wiring dressed
     along the braces.
   - Fewer braces needs the panel-mode check re-run first. It is noted, not drawn.
2. *A heavier mount: two or three posts, or a cradle.* The posts are already ø16 bronze with collars (round two).
   Fewer posts changes the load path the tipping check and the posts' modes were worked on, as before. It is noted for
   a structural review, not drawn.
3. *Carry the steps into the cabinet.* The caldera does this at the woofer. In the Ember proof the critic read it as
   clear, because ring and cabinet share the tint. The turned feet in `DETAILS.md` (two 1/2 in discs, a polished edge)
   carry the steps to the floor. Stepped edges on the port and the plate are a possible next step, not drawn.

**What it found least real:** a deep, crisply stepped horn in tinted cast acrylic with optically clean walls, "extremely
hard to machine or cast without stress marks, cloudiness or visible tool paths".
- It is neither cast nor machined from solid. Each layer is cut from 1/2 in sheet and its edge diamond-milled and
  buffed while it is a flat part. The layers are then bonded and the stack annealed (`make/laminated-horn.md`).
- That is the route a flat part's polished edge already proves. The risk is in the 21 bond lines: bubbles and
  crazing at a joint.
- **Before the first pair, a three-layer test stack** is made from the mouth's layers, bonded and annealed, then
  inspected under polarised light for stress and at the bond lines for bubbles. It costs about $150 (est.).
- The critic also saw no driver flange at the throat. The turned adaptor ring and its four screw heads are drawn
  (`hf-adaptor`); a rear three-quarter picture should show them.

**The build facts stay as stated for the deck:** 22 layers of 1/2 in stock cast sheet plus the boss, the mouth's
layer cut 20 mm outside the air path. A speaker is about 74 kg.

## The numbers

| | current | Strata | change |
|---|---|---|---|
| the horn assembly (with driver and adaptor) | 8.3 kg | 9.9 kg | +1.6 kg |
| the caldera, against the disc, frame and ring | about 1.4 kg | 2.1 kg | +0.7 kg |
| the lip and the bronze posts (round two) | — | about 0.9 kg | +0.9 kg |
| **a speaker** | **about 71 kg** | **about 74 kg** | **+3.2 kg** |
| the horn (the kit's parts list, prototype) | formed: about $1,500 with its share of tooling | laminated: about $1,570 | about +$70, and no forming tooling ($7,100 to $9,600 saved) |
| the caldera, against the disc, frame, ring and magnets | about $106 a speaker | about $230 a speaker (sheet, cutting, polish, bonding; est.) | about +$125 a speaker |

**Stability:** the tipping check (README, S7) was worked with 10 kg of horn on top. Strata's horn assembly with its
lip is about **10.2 kg**, so it is just over that allowance, not under it.
- The bronze posts (0.7 kg) sit below it, between the horn and the cabinet.
- The caldera's 2.1 kg is low on the front, below the woofer's center, and moves the center of mass forward by about
  3 mm (est.).

The margin was about 124 N·m forward against a push of 118 N·m. **Re-run S7 with Strata's masses before the first
pair**, and confirm it with the push gauge at first-article inspection. If the margin is short, the front feet move out
by 5 mm.

## How it is made

**The caldera rings:**
- each is CNC-cut from 1/2 in stock sheet, the bore and outside edge diamond-milled then buffed;
- they are faced flat and annealed;
- ring 1 is bonded to the front panel's face with polymerising cement, under dead weight on spacers, and rings 2 and 3
  to it, before the woofer goes in;
- the bond lines show as fine rings in the stepped wall, the same language as the horn.

The woofer still front-mounts through the caldera: the M6 button heads on their brass inserts sit at the bottom of
the first step, inside the Ø400 bore.

**The horn:** as `make/laminated-horn.md` (the stepped route).

## Pictures

- the studio hero, cover off and the whole speaker in frame (the owner, 2026-10-31);
- a macro of the caldera and the terraces;
- one picture in use.

They are in `renders/2026-10-31/barkhorn/design-pass/`, with blind critic scores and duels against the current
design. The CAD is `variants/variants.py` (the caldera) and `horn_options.py` (the horn).
