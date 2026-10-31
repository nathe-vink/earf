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

## The numbers

| | current | Strata | change |
|---|---|---|---|
| the horn assembly (with driver and adaptor) | 8.3 kg | 9.9 kg | +1.6 kg |
| the caldera, against the disc, frame and ring | about 1.4 kg | 2.1 kg | +0.7 kg |
| **a speaker** | **about 71 kg** | **about 73 kg** | **+2.3 kg** |
| the horn (the kit's parts list, prototype) | formed: about $1,500 with its share of tooling | laminated: about $1,570 | about +$70, and no forming tooling ($7,100 to $9,600 saved) |
| the caldera, against the disc, frame, ring and magnets | about $106 a speaker | about $230 a speaker (sheet, cutting, polish, bonding; est.) | about +$125 a speaker |

**Stability:** the stepped horn assembly, at 9.9 kg, sits at the tipping check's 10 kg allowance (README, S7). The
caldera's 2.1 kg is low on the front, below the woofer's center, and moves the center of mass forward by about 3 mm,
which is negligible (est.).

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
