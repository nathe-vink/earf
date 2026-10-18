# barkhorn round 31: the drivers as they are made

The owner, 2026-10-18 (evening): "The drivers in the images are starting to look really fake relative to everything
else." This note records what the fitted parts look like, where that came from, and what the model and the render
materials now do about it. Every datasheet number in `components.json` is unchanged; what was added is marked below.

## Sources

| | What | Seen how |
|---|---|---|
| F1 | FaitalPRO 15PR400 product page, faitalpro.com/en/products/LF_Loudspeakers/product_details/index.php?id=101060100 | opened |
| F2 | FaitalPRO's product photograph, faitalpro.com/products/files/15PR400/15PR400_photo_magnify.jpg | looked at |
| F3 | FaitalPRO's dimension drawing, faitalpro.com/products/files/15PR400/8/15PR400_drawing_8.pdf | looked at |
| F4 | FaitalPRO datasheet, faitalpro.com/en/products/LF_Loudspeakers/product_details/datasheet.php?id=101060100 | read |
| PE | Parts Express listing (the 4 ohm), parts-express.com, 294-1270 | snippet |
| B1 | B&C DE1085TN product page, bcspeakers.com/en/products/hf-driver/2/8/DE1085TN | opened |
| B2 | B&C's photograph, bcspeakers.com/uploads/products/images/2017_04_10_22_17_02_399_DE1085_img_00.jpg | looked at |
| B3 | B&C's drawing, bcspeakers.com/uploads/products/dataSheetDrawings/2016-09-08-15-29-52-501-de1085-drawing.png | looked at |
| AX | audioXpress test bench, DE1085TN on the ME60 | snippet |

Thomann's page could not be reached from the container; the maker's own pages could.

## FaitalPRO 15PR400-8: what the eye reads

- **Cone**: treated paper, a matte charcoal black with a fine felted fibre that shows in a raking light, deep and
  near straight-sided; no moulded ribs or rings (F2, PE). Kept: the model's slight curve (u^0.85), no ribs.
- **Surround**: "accordion, 4 waves", treated polycotton (F1, F4); in F2 four shallow concentric rolls of doped cloth,
  low sheen, sitting in a step inside the flange's raised inner lip. Was: one half roll of featureless rubber.
- **Dust cap**: no figure published; in F2 a shallow dome in the cone's own black, a little glossier. Kept the convex
  cap (cap_d 100, cap_h 14, both proportioned), doped glossier than the cone.
- **Basket**: die-cast aluminium, eight straight spokes (F3, PE), big windows, black with a fine sandy texture
  (e-coat or powder: F2, inferred), cooling fins cast round the motor so that the back is 150 across (F3). Was: six
  spokes, no fins.
- **Motor**: a neodymium slug inside the finned casting; a round label at the back (F3). The label is not modelled.
- **Flange**: eight slotted holes, 9.5 x 7.4, at 45 degrees (F3); "flange and gasket" 13.1 thick (F3, F4), so a gasket
  comes on it; no front logo (F2).
- **Terminals**: push terminals on a black block on a spoke near the motor, two chrome spring posts (F2, F3, F4).

### Where the datasheet and components.json differ (not changed: a spec question for the owner)

- Bolt circle: F3 draws 374; `components.json` has 375 (the panel's holes, the ring's pockets and the inserts use it).
- Sd: F4 gives 857 cm2; `components.json` has 805 (it drives the surround's radius and the acoustic model).
- Voice coil: F4 gives 77 mm (3 in); the model proportions its coil (coil_d unset, about 56); not seen in any render.

## B&C DE1085TN-16

- **Front**: a flat face with four M6 holes on 102 round a plain 2 in bore (B1, B3). What the phase plug's face looks
  like down the exit is not published; drawn as B&C's plugs usually are: a domed bullet ringed by annular slots.
- **Body**: a squat matte black cylinder with a bright satin-aluminium band round its middle (the motor plate's edge),
  the back a cast black heat sink of parallel fins (AX: "injection-moulded aluminium heatsink"), chrome push
  terminals at its sides, the + one red (B2, AX).

## What changed

**Geometry** (`studio/fabkit/speaker/drivers.py`; only at render detail, `detail` > 6, so the drawings' outlines are
as they were):

- the cone driver: spokes counted and phased by `spokes` / `spoke_phase`; an accordion surround (`waves`, `wave_h`);
  the flange's slots (`bolt_slot`) on `bolt_d` at `bolt_phase`; M6 button-head screws in them (`screw`, a piece
  `screws`); the gasket behind the flange (`gasket_t`, a piece `gasket`, 0.05 shy of both faces so no face is
  coplanar with the panel's); the motor's cooling fins (`fins`, `fin_h`, to 149 across); a terminal block on the
  lower spoke with two chrome posts (`terminals`: depth, radius; a piece `terminals`), where the woofer's lead ends.
- the compression driver: the exit's bore with a bright machined chamfer (piece `exit`); the phase plug as a domed
  bullet and three rings with dark slots between them (`plug_rings`); the bright band round the body (piece `band`);
  the heat sink's fins across the back; two terminal posts in pockets at the back's sides (piece `terminals`); all
  inside the 154 x 86 envelope.

**Part data** (`components.json`, added, nothing changed): spokes 8, bolt_slot 9.5 x 7.4, screw 10.5 x 3.3 (ISO
7380 M6), waves 4, wave_h 2.5, fins 24, fin_h 12. `product.py` passes the product's own: bolt_phase 0.5 (the panel's
holes), spoke_phase 0.5 (a spoke straight down, for the lead), gasket_t (P['gasket']), terminals (68, 115).

**Render materials** (`studio/engine/materials.py`, new presets; `product.py`'s finish table): `treated_paper`
(fibre bump, radial streaks read in the piece's own box, colour drift, a low sheen and a soft coat lobe),
`doped_cloth` (semi-gloss coat over a faint weave, a highlight along each wave), `ecoat` (satin black over a fine cast
grain and a slow waviness), `black_oxide` (screws), `opaque_acrylic` (the ring: polished, IOR 1.49, a little light into
the body, its colour unchanged). New finishes: driver-screw, driver-gasket, driver-terminal, driver-bright.
