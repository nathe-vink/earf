# barkhorn (a working name): Friendly Pressure's horn speaker, in bark

The owner's idea of 2026-10-10 was speakers that look like their reference photograph of Friendly Pressure's horns
(`reference/friendly-pressure-owner-2026-10-10.jpg`, with two more of the same speakers in a bar and a studio beside
it). There are two finishes, birch bark and eucalyptus bark, each with a horn in its bark's colours.

Status: **concept, round 4**. The proportions follow the photograph. The sizes are scaled from its turntable (about
450 wide), and the horn from the cabinet (round 4).

![Where round 4 points](../../renders/2026-10-12/barkhorn/pick.png)

## Round 4: the owner's notes of 2026-10-11 (evening)

| the note | what changed |
|---|---|
| "I like the disc and your color recommendations." | The disc on the bark face is the **standard front** now, not an option: charcoal on birch (apricot the alternative), rust on eucalyptus. The other covers are out of the build; `P['cover']['alternatives']` brings them back as options. |
| "The way it's connected doesn't seem symmetrical or realistic." | **Four posts in the photograph's layout**, symmetric about the centre: a wide pair under the front of the mouth (183 each side of centre, 35 back) and a narrow pair under the driver (35 each side). Each post is stainless lamp tube, 10 x 7, threaded M10 x 1 at both ends. One end screws into a brass insert bonded in a pad cast under the horn; the other into an insert in the cabinet's top. The HF cable runs down inside a rear post, so no wire shows. The horn sits low, as photographed: its rim is 39 above the top (it was 80; the photograph's is about 37). |
| "I'm not sure about the waveguide. The shape ... still seem off." | **The photograph measured again.** Its horn is 629 x 366 outside: 1.72 : 1. Round 1 read 2.1 : 1, so every horn since was about 75 mm too short. Its rim is thin, its flare runs almost to the edge, and its corners are squarer (about 70 mm). The new horn is built to that: 626 x 361, a 10 mm rim rounded over, a 6 mm shell following the flare. It has two possible backs (below). |
| "... and the texture/color still seem off." | **A new resin** (`cast_resin` in `studio/engine/materials.py`): milky where it is thin, deepening toward honey where it is thick or seen edge-on, cloudy, bead-blasted, as the photograph's horn glows. The frames add a soft lamp behind the horn, as the photograph has the room behind it. The tints are below. |
| "Yes take the pressed recycled plastic further." | **Researched and made buildable** (below): who presses it, how stiff it is, how it joins and moulds; a buildable version (`pressed.py`: 8 mm pressed HDPE sheet on the plywood, screwed from inside, never glued) with its own cut files, parts list and drawings (`out-pressed/`); a pattern specification a maker can press to; renders with a new sheet material. |

### The horn, measured again

| | the photograph (scaled from the cabinet, 560 wide) | rounds 1 to 3 | round 4 |
|---|---|---|---|
| outside | 629 x 366 (1.72 : 1) | 633 x 292 (2.17 : 1) | 626 x 361 (1.73 : 1) |
| rim | thin; the flare runs almost to the edge | 10 flat (round 2), up to 30 (pebble) | 10, rounded over |
| corners | about 70 | rounder (superellipse 4.5) | about 70 (superellipse 7) |
| rim above the cabinet's top | about 37 | 80 | 39 |
| supports | four posts: a wide pair in front, a narrow pair behind | three rods: two in front, one behind | four posts, as photographed |

The flare: a 610 x 346 mouth, 200 deep from the 1 in throat, covering about 113 x 82 degrees (round 3's: 612 x 272,
170 deep, about 120 x 75). The mouth's area puts the horn's lower limit near 210 Hz, far below the 800 Hz crossover.

![The photograph beside round 4, from its angle](../../renders/2026-10-12/barkhorn/compare-birch.png)

Seen from the photograph's angle and scaled to the same cabinet (`compare.py`), the horn now matches its width, height
and shape within a few per cent, and the posts stand where the photograph's do: an outer pair in front, an inner pair
behind. One difference is left: the photograph's dark throat is about twice ours (about 50 across against 25). A
compression driver with a 1.4 or 2 in exit, in place of the BMS 4550's 1 in, would match it; it would also change the
flare's throat.

![The horn on four posts, two backs](../../renders/2026-10-12/barkhorn/horn.png)

**Two backs**, the same from the front:

- **Shell** (the photograph's; my pick): the 6 mm shell follows the flare back to a round pod round the driver, closed
  by a cap; the neck round the throat is cast solid, so it deepens to a round halo as the photograph's does. It is the
  sleeker of the two and shows what it is: a horn. Its rear posts stand 148 under the pod (the front pair 55). Resin:
  about 2.4 L.
- **Tub**: the outside runs straight back from the rim to a flat back that hides the driver; the flare is its own skin
  inside, the space between filled with damping foam. All four posts are short (33 and 42) and the rear pair spreads
  wider (120 each side). It hides everything, but it is a 276 mm deep box: from the side it is the bulk round 1's horn
  had. Resin: about 4.9 L.

### The resin, close to

![The cast resin's tints](../../renders/2026-10-12/barkhorn/resin.png)

My picks: **milk on birch** (white, warming to honey where thick, faintly clouded) and **amber on eucalyptus** (cream
clouded with honey: the photograph's own, which takes up the gum's ochre). The red-brown kino read pink at a horn's
thinness and the leaf green as mint; the smoke is quiet but plain.
Cast resin glows only with light behind it, so the frames keep a soft lamp behind the horn, as the photograph has the
room behind it.

### Pressed recycled plastic, taken further

![Faced in pressed recycled plastic](../../renders/2026-10-12/barkhorn/pressed.png)

**What it is.** Coloured flakes of recycled plastic laid out by hand and hot-pressed into sheet, as a coloured record is
pressed. Laid flakes pressed without moving stay as patches; flow draws them into streaks. Makers press it to order:

| maker | plastic | sheets | custom patterns | published price |
|---|---|---|---|---|
| a Precious Plastic sheet-press workspace (many, worldwide) | HDPE, PP | up to 1 x 1 m, 5 to 30 thick (the SPR 2.3 press: 1.2 x 1.2 m) | yes: the buyer chooses the shred and the colours | stock 1 m HDPE sheets about EUR 50 to 60 plus shipping (undated listings, seen 2026-10-11) |
| The Good Plastic Company (Polygood) | recycled polystyrene | 2800 x 1400 and smaller, 10 to 20 thick | over 100 made for brands | about EUR 250 for 1 x 1 m (a resale listing, undated) |
| Smile Plastics (Wales) | recycled PET, HIPS, HDPE | 3000 x 1200, 12 or 20 thick | colour matching, gradients, fleck sizes (a 20-panel minimum on an old page) | panels by quote; samples about GBP 18 (undated) |
| Plasticiet (Rotterdam) | recycled polycarbonate | about 1 x 1 m, 12 to 19 thick | from 10 m2 | about EUR 575 to 625 / m2 (undated) |
| Yemm & Hart (Missouri) | post-consumer HDPE | up to 5 x 12 ft, 1/8 to 2 in thick | colours isolated in the feedstock | by quote; 8 to 12 weeks |

**Why the plywood stays.** Recycled HDPE is about a tenth as stiff as birch plywood (0.5 to 1.5 GPa against about
10). To be as stiff as 18 mm plywood, a panel would have to be about 40 mm thick; the box would go from about 28 kg to
80 and lose about 40 L inside. HDPE also grows 2 to 3.5 mm on an 880 mm panel over 20 degrees and creeps under load.
So the plywood box stays the structure, and the plastic is its face.

**How it is built here** (`pressed.py`; `out-pressed/` holds its cut files, parts list and 17 drawing sheets):

- each side, the top and the back faced in 8 mm pressed HDPE, and strips of it over the shell's front edges;
- each sheet screwed from inside through 8 mm holes in the plywood (stainless No. 8 pan heads and washers, about 150
  apart), never glued: HDPE glues badly (only special acrylics, 3M DP8005 or DP8010, hold at all), and every sheet
  must be free to move;
- 1.5 mm gaps at every corner for that movement; the posts pass through 14 mm holes in the top sheet, free of it;
- the front panel faced in 5 mm of the same sheet instead of bark;
- five 1 m sheets of 8 mm and two of 5 mm for the pair.

**The pattern, as a maker would press it** (to send with an order; a 200 mm sample first, then one full sheet from a
single batch, since colour ratios drift between batches):

- eucalyptus: full-height vertical strips 20 to 80 wide, cut from thin single-colour pressings and laid side by side,
  olive about 35 %, ochre 25 %, rust 20 %, grey 20 %, with a few smaller pieces of cream, brown and green among them.
  Load the mould near its final thickness so the strips do not smear, and keep any flow vertical;
- birch: a milk-white base (natural HDPE milk-bottle flake, about 90 %) with black pieces 2 to 4 x 10 to 40 laid
  horizontally in the top layer, about 3 to 6 % of the face, and a few tan pieces where birch peels.

The renders use a new procedural sheet material (`pressed_eucalyptus_sheet`, `pressed_birch_sheet`): melted flakes at
three sizes, their edges smeared by the press's flow, each strip a little lighter or darker than the next and marbled
inside, a waxy face.

**The moulded enclosure** (the owner's first idea: one moulding that the wires run through). The closest thing made
today is rotomoulding: Technomad rotomoulds one-piece polyethylene speaker shells with the horn, the driver's cavities,
the port and the fixings moulded in, in recycled polyethylene (90 % post-industrial, 10 % post-consumer), and its Berlin model is this speaker's layout (a 15 in
woofer and a compression driver on a horn). Rotomoulding colour-sorted flakes gives a speckled terrazzo, not strips;
moulds run from a few thousand dollars to over a hundred thousand. Compressing the horn itself from flakes is not
realistic: a part this size needs a press of about 200 tonnes, and thick HDPE sinks and warps as it cools. That makes
rotomoulding a production route, after a pair has been built with pressed sheet on plywood.

Sources (searched 2026-10-11; prices are as listed, mostly undated):
[Precious Plastic sheet-press workspace](https://community.preciousplastic.com/library/set-up-a-sheetpress-workspace),
[SPR 2.3](https://community.preciousplastic.com/library/spr---23),
[Bazar HDPE sheet](https://bazar.preciousplastic.com/raw-material/sheets/multi-color-hdpe-sheet-1x1-meter-size-and-8-25-mm-thickness-ready-stock-available/),
[Polygood](https://en.wikipedia.org/wiki/Polygood),
[Polygood sizes](https://thegoodplasticcompany.com/workability/),
[Smile Plastics custom](https://smile-plastics.com/custom/),
[Smile Plastics sizes](https://smile-plastics.com/materials/mawn),
[Plasticiet Karlite](https://www.plasticiet.com/karlite),
[Yemm & Hart patterns](https://yemmhart.com/wordpress/pioneers-in-eco-materials/colorful_plastic_sheet/origins-patterns/),
[HDPE modulus](https://engineeringtoolbox.com/young-modulus-d_417.html),
[birch plywood](https://www.metsagroup.com/globalassets/metsa-wood/dop-documents/dop_metsa_wood_birch_plywood_muf_2019-12-2_en.pdf),
[HDPE movement](https://smile-plastics.com/materials/grey-mist),
[3M DP8010](https://multimedia.3m.com/mws/media/2365938O/3m-scotch-weld-structural-plastic-adhesive-dp8010-blue.pdf),
[HDPE on plywood](https://yemmhart.com/wordpress/pioneers-in-eco-materials/colorful_plastic_sheet/origins-fabrication-installation/),
[Technomad](https://www.svconline.com/news/howttsmade-story-behind-how-technomad-manufactures-its-weather-tech-loudspeakers-364916),
[Technomad Berlin](https://www.fullcompass.com/common/files/11672-TechnomadBerlin9040.pdf),
[rotomould costs](https://www.jinhongmold.com/news/how-much-does-a-rotational-mold-cost/),
[compression pressures](https://books.byui.edu/plastics_materials_a/compression_molding).

## Round 3: the owner's notes of 2026-10-11

| the note | what changed |
|---|---|
| "Maybe bark face with a solid color cloth grille." | Both readings are rendered, on both barks (`../../renders/2026-10-11/barkhorn/front.png`). The first is the front faced in bark under a full cloth grille in one colour, so the bark shows when the grille comes off. The second is a **cloth disc** over the woofer alone, so the bark and the colour show together. The disc is a new option: a 12 mm MDF ring frame on the woofer's ring, the cloth across its face and round its edge, held by magnets, its face 18.5 clear of the cone. |
| "The eucalyptus is sick." | Kept as it is. |
| "The waveguide still needs work." | A **study of five forms** (below; `../../renders/2026-10-11/barkhorn/study.png`). Each is built in the CAD on the same speaker and seen from the front, the side and behind. |
| "Also open to more experimental shit." | **Material experiments** (below; `../../renders/2026-10-11/barkhorn/experiments.png`): the cabinet in pressed recycled plastic, and the waveguide in strata or terrazzo resin. |

![The bark face under a solid colour cloth](../../renders/2026-10-11/barkhorn/front.png)

**My picks for the front:** the disc, charcoal or apricot on birch and rust on eucalyptus. Each takes a colour the
bark already has: birch's lenticels or its peel, the gum's rust strips.

### The waveguide study

![The waveguide study](../../renders/2026-10-11/barkhorn/study.png)

What was wrong with round 2's shell, now that it is seen from every side:

- From the front it reads as a moulded basin, not as frosted resin with any depth.
- From the side, a funnel with a can behind it reads as a megaphone.
- From behind, the pod is a bulb stuck on.

| form | what it is | resin (production) | read |
|---|---|---|---|
| shell (round 2) | a 6 mm shell following the flare, a pod behind round the driver | 1.5 L | thinnest; a megaphone from the side, a bulb from behind |
| lens | thin at its edge, curving back to a round back that holds the driver | about 5 L cast hollow (18 L solid) | one stone, nothing showing; from the front much as the shell |
| slab | a 64 mm slab with fully rounded edges (the photograph's soft rim), the rest of the flare in a tail behind | 6 L solid (about 4 L hollow) | the most presence from the front; a neck and pod behind |
| **pebble** | the slab's rolled rim (30 round the mouth) on the lens's smooth back | about 5 L cast hollow (19 L solid) | the soft rim from the front, a stone from the side and behind |
| round | a round tractrix horn for 400 Hz, its lip rolled back, a closed can behind | 1.1 L | a trumpet; rhymes with the disc, beams more at high frequencies |

The hollow volumes are a 7 mm skin over every face, from the CAD's surface areas. The shell, lens, slab and pebble
share one flare: 612 x 272 at the mouth, 170 deep, about 120 x 75 degrees. They
differ only in how they look and what they weigh. Each was checked against the rods (cut to its underside) and the
driver (no clashes). The round horn is acoustically different: it is axisymmetric, and its coverage narrows as the
frequency rises.

**My pick: the pebble**, in strata resin on eucalyptus and in terrazzo on birch (below). It hides the driver as the
round-1 block did, but tapers to a thin edge, so it reads as one sculpted stone rather than a box. The resin's
thickness shows as a glow and a deepening of colour, which the thin shell could not.

![Where the study points](../../renders/2026-10-11/barkhorn/proposal.png)

### Material experiments

![Material experiments](../../renders/2026-10-11/barkhorn/experiments.png)

- **Pressed recycled plastic** (the owner's vinyl-pressing idea of 2026-10-11). Flakes of coloured HDPE are laid out
  and hot-pressed into sheet, the press's flow drawing them out:
  - eucalyptus: strands of green, ochre, rust and grey stretch into camo strips;
  - birch: black flakes in white stretch into lenticel dashes.

  The sheet is welded, not glued. A cast or rotomoulded cabinet in the same pattern would need ribs or a stone-filled
  resin to be as stiff as the plywood.
- **Strata resin**: the waveguide poured in layers of the gum's colours (sage, cream, honey), each a few centimetres
  thick, their boundaries wavy. It reads as agate and glows where the resin is thick.
- **Terrazzo resin**: milky resin with recycled plastic chips cast through it (black, grey, apricot): birch's
  lenticels again.

These are renders of the idea. The materials are procedural (`pressed_eucalyptus`, `pressed_birch`, `frosted_strata`,
`frosted_terrazzo` in `studio/engine/materials.py`). A sample from a maker comes before any of them is drawn up.

## Round 2: the owner's notes of 2026-10-10

| the note | what changed |
|---|---|
| "It's interesting that you made the waveguides so thick. I kind of like that less of the innards are exposed that way potentially, but it does make it look less sleek and more pudgy." | The waveguide is now a **thin cast shell**. It is 6 mm thick and follows the flare outside as well as in, with a 10 mm rim at the mouth. Behind the throat, a round **pod** 148 across closes round the compression driver, and a cap closes the pod. Nothing inside shows, and the horn reads as one sheet bent into shape (`../../renders/2026-10-10/barkhorn/back-v3.png`). It uses about 1.5 L of resin. It stands on three rods (two under the mouth, one under the pod), each cut to meet the shell's underside. |
| "The eucalyptus looks too pastel and not like the long strips of peely camo-ish bark. Like a eucalyptus after rain." | The bark is redrawn as a smooth-barked gum sheds it, in **layers**. The fresh underbark is streaked deep green, olive, yellow and orange. Over it lie older layers in long vertical strips: straw, rust, grey, then brown. Each strip's edge lifts, with a dark shadow under it and a lit, curled lip. Everything is **wet**: deeper and more saturated, glossy, with rain-darkened runs (`../../renders/2026-10-10/barkhorn/eucalyptus-detail-v3.png`). |
| "Open to ideas on front panel covers" | **Five covers**, each built in the CAD with its own cut files and parts list, and rendered on both barks (below). |

## What the photograph shows, and how it is built here

| in the photograph | here |
|---|---|
| a bass cabinet about 1 : 1.6 | 560 wide, 880 tall, 420 deep, standing on felt glides |
| a thin walnut shell framing a pale front panel set back in it | The shell (sides, top, bottom, back) is 18 mm birch plywood faced in **bark**, wrapped round its front edges. The front panel is set back 24 mm and painted pale. 24 mm is deep enough for a cover to clear the cone. |
| a 15 in black cone in a wide off-white ring, its centre a little above the middle | FaitalPRO 15PR400-8 (treated paper cone, 99 dB), flush in its rebate, its centre 45.7 % down. A 6 mm MDF ring 436 across lies over its frame, with pockets behind for the screw heads. |
| a small square port at the bottom right | A 100 mm square printed port, bottom right, 53 long. The box is about 152 L net, tuned to 38 Hz; f3 is about 44 Hz in half space before room gain (`.venv-fab/bin/python spinoffs/barkhorn/product.py`). |
| a frosted, translucent rounded-rectangle waveguide about 629 x 366 (1.72 : 1), wider than the cabinet, its rim thin, the throat a dark dot near its centre | Since round 4: 626 x 361 outside, a 610 x 346 mouth, a 10 mm rim rounded over. Its flare is 200 deep, with the pod 70 behind it. It is a superellipse waveguide: round at the 1 in throat, squaring toward the mouth (corners about 70), covering about 113 x 82 degrees. It is a 6 mm shell cast in tinted translucent polyurethane, its neck solid, bead-blasted to frost. (Rounds 1 to 3: 633 x 292, read wrongly as 2.1 : 1.) |
| it stands on four slim posts, a wide pair in front and a narrow pair behind, its rim just above the cabinet | Since round 4, four posts in that layout: stainless lamp tube 10 x 7, M10 x 1 into brass inserts in pads under the horn and in the top, the HF cable inside a rear one; the rim 39 above the top. (Rounds 1 to 3: three rods, 80 clear.) |
| (not visible) | A BMS 4550-16 compression driver (polyester diaphragm, 113 dB) sits in the pod. A Hypex FusionAmp FA122 on the cabinet's back crosses at about 800 Hz and pads the HF channel about 14 dB. Part of the pad is a passive L-pad after the amplifier, so its hiss stays inaudible. |

## The two finishes (proposals)

| | shell | front panel | ring | waveguide |
|---|---|---|---|---|
| birch | paper birch: chalk white, dark lenticels in bands, a few scars, apricot where it has peeled | faced in its bark, under a charcoal cloth disc `#2E2C2A` (round 4; the paint behind, pale warm grey `#D8D5CD`) | off-white `#EEEAE2` | milk resin `#F2EEE6`, warming to honey `#D9AE6E` where thick, faintly clouded (round 4) |
| eucalyptus | a smooth-barked gum after rain: underbark streaked green, olive, yellow and orange under strips of straw, rust, grey and brown, wet | faced in its bark, under a rust cloth disc `#9A4526` (round 4; the paint behind, pale sage grey `#CBCFC4`) | cream `#E8E2D4` | cream resin `#EFE5D0` clouded with amber `#D6A04E`, the photograph's own (round 4; round 2's sage read pastel) |

![The birch, three-quarter](../../renders/2026-10-10/barkhorn/birch-v3.png)
![The eucalyptus, three-quarter](../../renders/2026-10-10/barkhorn/eucalyptus-v3.png)

- **The renders.**
  - Both barks are procedural materials (`birch_bark` and `eucalyptus_bark`).
  - The waveguides use a cast translucent resin (`cast_resin`, random-walk subsurface scattering, since round 4;
    `frosted` before), and the covers use `cloth` and `cork`.
  - All of them are in `studio/engine/materials.py`.
  - Photographed CC0 bark (Poly Haven, ambientCG) would need those hosts allowed in the environment's network
    settings.
- **The real finish.**
  - Birch: real bark sheet (*Betula papyrifera*, from fallen or felled trees) laminated with PVA in a vacuum bag and
    sealed matt.
  - Eucalyptus: the shed bark of a smooth-barked gum (a snow or spotted gum) pressed flat and laminated the same way,
    or a UV-printed veneer of it. The wet look is a satin or gloss sealer, which deepens bark's colours as rain does.

  Approve a sample board first.
- **The waveguide** is cast in a two-part silicone mould from a CNC-cut plug, and the cap in a small mould of its own.
  The parts list spreads a mould budget of $900 for the shell and $250 for the cap over the pair. Tinting the resin per
  finish costs nothing more.

## Front covers (options)

Since round 4 the disc on the bark face is the standard front, and the other covers below are out of the build
(`P['cover']['alternatives'] = True` brings them back as options, the disc and the bark face with them).

![The covers on both barks](../../renders/2026-10-10/barkhorn/covers.png)

Each cover sits in the 24 mm recess, 1.5 clear of the shell all round. A grille stands flush with the shell's front on
four pegs into cups in the panel's corners. Its back stays at least 16 clear of the cone at rest, which leaves 4.5 mm
even at twice the woofer's Xmax. The woofer plays only below 800 Hz, so a slotted grille open about a quarter of its
face costs it nothing audible: the air behind it resonates in the slots near 1.9 kHz, over an octave above the
crossover.

| option | what it is | the look |
|---|---|---|
| bare (as now) | the painted panel, the ring and the cone, as photographed | the reference, unchanged |
| cloth grille | acoustically transparent knit stretched over a 6 mm MDF frame (sprayed black), its face 1 back from the shell's front; oatmeal `#DCD6C8` on birch, eucalyptus-leaf green `#6F7F66` on eucalyptus | calm and flat: the bark and the horn carry it alone |
| lenticel grille (birch's own) | 6 mm birch plywood sprayed the panel's colour, cut with 394 round-ended 6 mm slots in rows of short dashes of random length, as birch's lenticels; 24 % open | the woofer hidden behind the bark's own pattern: dark dashes on pale, as on the shell |
| strip grille (eucalyptus's own) | 6 mm spotted-gum plywood (a eucalypt hardwood face), oiled, cut with 124 long vertical slots in columns, bridged at random heights, as the bark's strips; 28 % open | warm timber under the wet bark: the tree's wood in front, its bark round it |
| bark face | the panel faced in the bark itself (1 mm), cut round the ring and the port | a log with a speaker in it; the boldest |
| cork face | 3 mm cork sheet laid on the panel round the ring and the port; dark, as smoked expanded cork | cork is bark too (the cork oak's): a third bark, dark behind the white ring |
| cloth disc (round 3) | the woofer alone covered: a 12 mm MDF ring frame on the woofer's ring, the cloth across its face and round its edge; four magnet pairs hold it, their partners in pockets behind the ring, so the ring's face stays clean without it; any solid colour | a circle of colour on the panel or on its bark face; the bark shows round it |

The slot patterns are seeded, so a rebuild cuts the same panel. Their cut files are in `out/dxf/`, nested on sheets of
their own. The covers' materials are budgets only where the kit has a rate: the cloth, the pegs, the bark, the cork
sheet and the spotted-gum plywood show [PRICE] until a supplier's figure is entered. The woofer's roll height is
proportioned (the datasheet gives none). Confirm on a driver that its roll does not stand proud of its flange before a
grille is fitted.

**My picks:** the **lenticel grille on birch** and the **strip grille on eucalyptus**, each cover drawn from its own
tree. Bare stays the reference for both.

![The eucalyptus from behind: the waveguide's pod and cap](../../renders/2026-10-10/barkhorn/back-v3.png)

## The fabrication package

Built with the fab kit (`studio/fabkit`):

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/product.py
    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/pressed.py --out spinoffs/barkhorn/out-pressed
    python3 spinoffs/barkhorn/frames.py horn            # a comparison sheet (each set is listed in frames.py)
    python3 spinoffs/barkhorn/compare.py renders/2026-10-12/barkhorn/pick/pick-photo-birch.png OUT.png

The waveguide's form is `P['horn']['form']` in `product.py`: `cast` as built today (round 4, the photograph's), its
back `P['horn']['cast']['back']` (`shell` or `tub`); round 3's study forms (`shell`, `lens`, `slab`, `pebble`,
`round`) are still there. `frames.py` builds the study models a set needs into `out/study/` first.

`product.py` writes `out/`:

- STEP and STL;
- DXF cut files for the plywood (three 1525 mm sheets), the MDF ring and the disc's frame;
- the checks (no clashes);
- the parts list (`bom.md`): about $3,520 for the pair at budget rates, before the unpriced items (the bark, the
  cloth, the magnets, the posts' inserts and a few small parts);
- 14 A3 drawing sheets (`out/drawings/barkhorn-sheets.pdf`): the assembly, each sheet part (the ring and the disc's
  frame with their magnet pockets), the cast horn, its cap and the posts, and the notes;
- the render model.

`pressed.py` builds the same speaker faced in pressed recycled plastic into `out-pressed/`: the eight sheet parts a
speaker (sides, top, back, four edge strips) and the panel's face nest on five 1 m sheets of 8 mm HDPE and two of 5 mm
for the pair; the parts list is about $3,480 before the unpriced items (the pressed sheet has no published dated
price); 17 drawing sheets.

The shots are in `studio/shots/barkhorn/`:

- `front`: the pair, as photographed;
- `birch` and `eucalyptus`;
- `eucalyptus-detail`: the bark close to;
- `back`: the waveguide from behind;
- one folder per comparison sheet, one shot per frame: `covers/` (round 2), `front/`, `study/`, `experiments/`,
  `proposal/` (round 3), `horn/`, `resin/`, `pressed/` and `pick/` (round 4).

## Open questions for the owner

1. **The horn's back.** The shell (my pick: the photograph's, the sleeker) or the tub (hides everything, four short
   posts, bulkier)?
2. **The resin.** Milk on birch and amber on eucalyptus (my picks), or another tint from the study?
3. **Pressed recycled plastic.** Go to samples? The next step is a 200 mm sample of each pattern from a sheet-press
   workspace, then one full sheet from a single batch. Rotomoulding (a one-piece moulded shell) is the production
   route after that, with a speckled look rather than strips.
4. **A name.** barkhorn is a placeholder.
5. **Price.** [PAIR PRICE] stays open.
