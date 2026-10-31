"""The request-for-quotation pack for the first Tropos pair (2026-10-30): one letter per kind of vendor, each with its
parts table (part, drawing sheet, material, thickness, tint, quantity for 1, 10 and 50 pairs, finish, tolerance), the
drawing sheets to attach as one PDF, and the questions. Built from the Cloud's parts list, so it follows the CAD.

    python3 spinoffs/barkhorn/rfq/tropos/build_rfq.py

Reads spinoffs/barkhorn/out-cloud/bom.csv and drawings/barkhorn-cloud-sheets.pdf (the build of 2026-10-25); writes
<kind>/letter.md, <kind>/parts.csv, <kind>/drawings.pdf beside this file. Files only: nothing here contacts anyone.
"""
import csv, os, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, '..', '..', 'out-cloud'))
SHEETS_PDF = os.path.join(OUT, 'drawings', 'barkhorn-cloud-sheets.pdf')
# the laminated horn (2026-10-31, later) is built apart, in horn_options.py: its parts list and its own drawing set (BHH)
OUT_HO = os.path.normpath(os.path.join(HERE, '..', '..', 'out-horn-options'))
SHEETS_HO = os.path.join(OUT_HO, 'drawings', 'barkhorn-horn-options-sheets.pdf')
HO_SHEET = {'horn-plan-b': 'BHH-005', 'horn-plan-b-smooth': 'BHH-005'}
HO_PAGES = [1, 5, 6]               # its general arrangement, the laminated horns, its notes
SIGN = '[Your name], EARF · earf.world'

# where each part is drawn in the set of 2026-10-25 (40 sheets, BHC-001 to BHC-040); 'DXF' is a cut file only
SHEET = {'left': 5, 'right': 6, 'top': 7, 'bottom': 8, 'front-panel': 9, 'back': 10, 'brace': 11, 'brace-2': 12,
         'woofer-ring': 13, 'port-frame-left': 14, 'port-frame-right': 15, 'disc-frame': 16, 'land-left': 17,
         'land-right': 18, 'land-top': 19, 'land-bottom': 20, 'top-pad': 21, 'lining-bottom-1': 22, 'lining-left-3': 23,
         'lining-right-3': 24, 'lining-top-3': 25, 'rib-': 4, 'lining-left-2': 4, 'lining-right-2': 4, 'lining-back-': 'DXF',
         'port-left': 26, 'port-right': 26, 'waveguide': 26, 'horn-throat': 27, 'horn-pod': 27, 'waveguide-cap': 28,
         'hf-adaptor': 28, 'post-1': 29, 'post-2': 29, 'post-3': 29, 'post-4': 29, 'amp-box': 30, 'ir-bracket': 30,
         'horn-pads': 31, 'horn-saddle': 31, 'back-boss-': 32, 'grip-': 32, 'ir-window': 33, 'horn-tool-prototype': 33,
         'horn-tool-base': 34, 'horn-tool': 34,
         # bought or finished parts with no sheet of their own: where they show in the assembly (1), the section (2) or
         # the exploded view (3)
         'post-sockets': 2, 'post-sleeves': 2, 'rating-plate': 1, 'cloth-disc': 3, 'mark-back': 1, 'back-seal': 2,
         'amp-box-gasket': 2, 'lining-sleeves': 'DXF'}
COMMON = [1, 2, 3, 39, 40]          # the general arrangement, the section, the exploded view and the notes, to everyone

PANEL_TOL = '±0.5 outline, ±0.2 pockets, holes +0.2/0'
CAB_TINT = 'the speaker\'s colour, cabinet lot: Ember (red) and Smoke (black) for the prototype pair'
HORN_TINT = ('the speaker\'s colour, the horn\'s own heavier lot per colour (about 6 to 10 x the cabinet\'s dye; Ember about 10, '
             'Smoke about 7), matched to a chip we approve: Ember and Smoke')
POLISH = 'edges milled square; show edges polished; annealed before cementing'
# the first pair in stock sheet (make/stock-pair.md): Smoke, from TruCast 2064 3/4 in; the horn from 2074 1/2 in
STOCK_CAB = 'Smoke: TruCast 2064 Gray 3/4 in (19 mm) cell-cast, stock (AC Plastics); we buy it or you source it'
STOCK_THIN = 'Smoke: TruCast 2064 Gray cell-cast, stock, in the nearest stock thickness to the one listed'
STOCK_HORN = 'Smoke: TruCast 2074 Dark Gray 1/2 in cell-cast, stock; an Ember horn in 2423 Red 1/2 in as an option'

# kind -> [(bom item prefix, part, material, thickness, tint, finish, tolerance)]; quantities come from the parts list
KINDS = {
    'a-cast-acrylic': [
        ('left', 'shell sides', 'cell-cast acrylic', '20', CAB_TINT, POLISH, PANEL_TOL),
        ('top', 'shell top', 'cell-cast acrylic', '20', CAB_TINT, POLISH + '; 4 post sockets and an M12 thread', PANEL_TOL),
        ('bottom', 'shell bottom', 'cell-cast acrylic', '20', CAB_TINT, POLISH + '; 4 feet insert holes', PANEL_TOL),
        ('front-panel', 'front panel', 'cell-cast acrylic', '20', CAB_TINT, POLISH + '; woofer rebate, port recesses, magnet pockets', PANEL_TOL),
        ('back', 'back (removable)', 'cell-cast acrylic', '20', CAB_TINT, POLISH + '; amplifier cutout and recess; EARF etched (quoted separately)', PANEL_TOL),
        ('brace', 'braces', 'cell-cast acrylic', '20', CAB_TINT, 'edges milled square (inside)', PANEL_TOL),
        ('rib-', 'ribs', 'cell-cast acrylic', '20', CAB_TINT, 'edges milled square (inside)', PANEL_TOL),
        ('land-', 'land strips', 'cell-cast acrylic', '20', CAB_TINT, 'M5 insert holes; the seal groove milled after assembly', PANEL_TOL),
        ('top-pad', 'pad under the top', 'cell-cast acrylic', '20', CAB_TINT, 'M12 thread, an insert hole', PANEL_TOL),
        ('back-boss-', 'brace bosses', 'cast acrylic block, cabinet lot', '36 x 36 x 85', CAB_TINT, 'milled, slotted over the brace; M5 insert hole', '±0.2'),
        ('woofer-ring', 'woofer ring', 'cell-cast acrylic', '6', 'opaque, in the ring colour (Ember: oxblood, about #7A1A1C; Smoke: near-black #141316)', 'face polished; screw-head and disc pockets behind', PANEL_TOL),
        ('disc-frame', 'cloth disc frame', 'cell-cast acrylic', '12', 'black', 'face edge rounded R5; magnet pockets', PANEL_TOL),
        ('port-frame-', 'port frames', 'cell-cast acrylic', '8', CAB_TINT, 'mouth rounded R8 and polished; 4 countersinks', PANEL_TOL),
        ('port-left', 'port tubes', 'cast acrylic tube 121 x 4 wall', '4 (wall)', 'the speaker\'s colour, the cabinet lot, if tinted tube can be had (question 10)', 'inner end flared R8 over a heated mandrel, annealed; bore polished; cemented into its frame', '±0.3'),
        ('grip-', 'grip cups', 'cast acrylic sheet', '3', CAB_TINT, 'drape-formed over a buck; cemented behind the grip slot', '±0.5'),
        ('ir-bracket', 'IR receiver bracket (one a pair)', 'cast acrylic, water-clear', '10', 'clear', 'milled pocket and ledge; 2 bonded M2.5 inserts', '±0.2'),
        ('ir-window', 'IR window, fallback only', 'cast acrylic rod, water-clear', 'ø12 x 20', 'clear', 'bonded through the front panel, faces polished flush', '±0.1'),
    ],
    'b-horn-forming': [
        ('waveguide', 'horn flare', 'cell-cast acrylic sheet, pressure-formed', '10 sheet; formed wall 8.5 to 4.9', HORN_TINT, 'formed over our tooling-board plug, trimmed on 5 axes, rim routed full round and polished, annealed', 'air face as the plug; wall >= 4.0; trim ±0.5'),
        ('horn-throat', 'throat piece', 'cast acrylic block, horn lot', '75 block', HORN_TINT, 'turned and milled (5 axes); bore polished; socket for the flare', 'bore ±0.1; socket +0.2/0'),
        ('horn-pod', 'pod', 'cast acrylic sheet, horn lot, rolled', '6', HORN_TINT, 'rolled to ø200 over a heated mandrel, seam scarfed and cemented, annealed, bore turned true, 3 L-slots milled', 'bore ±0.1'),
        ('waveguide-cap', 'cap', 'cast acrylic sheet, horn lot', '30', HORN_TINT, 'turned; 3 lugs milled; O-ring groove; dome polished', '±0.1'),
        ('horn-pads', 'post pads (4 a horn)', 'cast acrylic sheet, horn lot', '30', HORN_TINT, 'turned; tops milled to the flare; bored for M10 inserts', '±0.2'),
        ('horn-saddle', 'tie-rod saddle', 'cast acrylic sheet, horn lot', '30', HORN_TINT, 'turned; bored 6.5', '±0.2'),
    ],
    'b-horn-tooling': [
        ('horn-tool-prototype', 'forming plug, prototype', 'high-temperature epoxy tooling board (150 C or more)', '628 x 273 x 364', '-', 'cut by 5-axis program from our CAD (the horn\'s air path), sealed and polished, vented 0.6', 'surface ±0.1'),
        ('horn-tool-base', 'forming base plate (carries into production)', 'aluminium 6061 plate', '900 x 640 x 40', '-', 'machined; clamp-frame seal groove; plug bolted from below', '±0.1'),
        ('horn-tool', 'forming plug, production (a later line)', 'aluminium, cast near shape (A356) and machined', '628 x 273 x 364', '-', 'machined all over on 5 axes, polished; oil channels for 85 C; vents 0.6; cored', 'surface ±0.05'),
    ],
    'c-metal': [
        ('amp-box', 'amplifier compartment', 'aluminium 5052 or 6061 sheet', '1.5', 'black anodised', 'folded, corners welded, flange; 3 gland holes; an earth stud on a bared spot', '±0.3'),
        ('hf-adaptor', 'driver adaptor ring', 'aluminium 6061', 'ø184 x 10', 'black anodised', 'turned; 4 countersunk M6 on 101.6; 4 x 5.5 on 170', '±0.1'),
        (('post-1', 'post-2'), 'front horn posts', 'stainless 304 tube 10 x 7', 'ø10', 'natural, satin', 'cut to length, threaded M10 x 1 at the top, deburred', 'length ±0.2'),
        (('post-3', 'post-4'), 'rear horn posts', 'stainless 304 tube 10 x 7', 'ø10', 'natural, satin', 'cut to length, threaded M10 x 1 at the top, deburred', 'length ±0.2'),
        ('post-sockets', 'post sockets and inserts (a set of 8)', 'brass C360', 'ø15 x 15 cups; M10 x 1 inserts 13 x 12', 'natural', 'turned, knurled; cups bored 12 on a 2 floor', '±0.05 on the bore'),
        ('rating-plate', 'rating plate', 'aluminium', '70 x 40 x 1', 'black anodised', 'laser-marked (model, serial, ratings, WEEE bin)', '±0.2'),
    ],
    'd-other': [
        (('lining-bottom-', 'lining-top-', 'lining-left-', 'lining-right-', 'lining-back-'), 'lining batts', 'polyester batt, acoustic grade, about 30 kg/m3, recycled PET', '50 and 100', 'white', 'cut 10 oversize each way; each sewn into a white voile sleeve', '±5'),
        ('lining-sleeves', 'lining sleeves (voile)', 'white polyester voile', '-', 'white', 'sewn to each batt\'s size, seams to the wall', '±5'),
        ('cloth-disc', 'cloth disc covering', 'acoustically transparent knit', '-', 'in the speaker\'s colour', 'stretched over the disc frame and round its edge', '-'),
        ('mark-back', 'EARF on the back', 'laser etch into the back panel', '0.1 deep', 'etch filled in the speaker\'s colour, deeper', 'frosted, 140 wide, from our vector file', '±0.2'),
        ('back-seal', 'back seal', 'EPDM cord 4 mm, 60 Shore A', '4', 'black', 'about 2.7 m a speaker, its ends vulcanised into a loop', 'length ±5'),
        ('amp-box-gasket', 'amplifier compartment gasket', 'EPDM sponge, closed cell', '3', 'black', 'die-cut frame, 15 wide', '±0.5'),
        ('post-sleeves', 'post sleeves (a set of 4)', 'polyurethane, Shore A 90', 'ø12 x 10 x 13', 'black', 'cast or cut', '±0.1'),
    ],
}

# (e) one shop for the whole first pair in stock sheet (2026-10-31, later; research R7): the cabinet as in (a), in stock
# 3/4 in Smoke, and the laminated horn with the horn's small parts (as in (b), from the stock 1/2 in sheet); 'ho:' marks
# a part from the horn options' parts list
def _stock(pre, part, mat, th, tint, fin, tol):
    """Letter (a)'s cabinet line in the stock Smoke sheet: 20 mm becomes 3/4 in; the thinner parts the nearest stock
    thickness; the bosses bonded from two 3/4 in layers; the tube rolled from sheet if tinted tube cannot be had."""
    if pre == 'back-boss-':
        return pre, part, 'stock cell-cast sheet, two 3/4 in layers bonded, then milled', th, STOCK_CAB, fin, tol
    if pre == 'port-left':
        return pre, part, mat, th, 'Smoke, 2064, if tinted tube can be had; otherwise rolled from 1/8 in 2064 sheet', fin, tol
    if tint == CAB_TINT:
        return pre, part, mat, '19 (stock 3/4 in)' if th == '20' else th, STOCK_CAB if th == '20' else STOCK_THIN, fin, tol
    return pre, part, mat, th, tint, fin, tol


KINDS['e-laminated-horn'] = [
    _stock(*line) for line in KINDS['a-cast-acrylic'] if line[0] not in ('ir-window',)
] + [
    ('ho:horn-plan-b', 'laminated horn, stepped (2 a pair)', 'stock cell-cast sheet 1/2 in, 22 layers and a boss',
     '22 x 12.64 pitch (layer + bond line)', STOCK_HORN,
     'layers CNC-cut from our DXF (outline and a rough bore); edges polished before bonding; bonded in sub-stacks with a '
     'polymerising cement, no visible bubble; annealed; the air path cut through on 5 axes from our STEP and polished',
     'air path ±0.1 to the STEP; outline ±0.5; stack 278 ±1 to the mouth'),
    ('ho:horn-plan-b-smooth', 'OPTION: the same horn, outside machined smooth', 'as above', 'as above', STOCK_HORN,
     'as above, then the outside cut on 5 axes to our STEP (outside-smooth.step) and polished; quote as the extra over the stepped',
     'outside ±0.3'),
] + [(pre, part, mat, '25 (two 1/2 in layers)' if th == '30' else th, STOCK_HORN, fin, tol)
     for pre, part, mat, th, tint, fin, tol in KINDS['b-horn-forming'] if pre in ('waveguide-cap', 'horn-pads', 'horn-saddle')] + [
    ('horn-pod', 'pod', 'stock cast sheet, horn colour', '6 (1/4 in)', STOCK_HORN,
     'rolled to ø200 over a heated mandrel, seam scarfed and cemented, annealed, bore turned true, 3 L-slots milled; or turned from a '
     'bonded stack of 1/2 in rings if you would rather', 'bore ±0.1'),
]

INTRO = {
    'a-cast-acrylic': ('cast acrylic fabrication', """I'm writing from EARF, a new hi-fi and lighting maker in San Francisco, for a quote on the acrylic parts of a loudspeaker we are prototyping. Tropos is a horn loudspeaker
whose cabinet is 20 mm cell-cast acrylic, tinted through, so you see into it. The first pair will be in two colours,
Ember (a transparent red) and Smoke (a transparent black). If it goes well, ten pairs follow, then about fifty.

We need the panels cut on a CNC router from our DXF files, edges milled square, the edges that show polished, and the
panels annealed before they are cemented. If you also assemble, we would like a price for the cemented cabinet:
corners, front panel, braces, ribs and land strips cemented with a two-part polymerising cement (ACRIFIX 2R 0190 or
Weld-On 40, no solvent cement), with no visible bubble in any joint; the box annealed again; and the lands' faces, the
bosses' faces and the seal's groove milled in one setup. Quote the cutting and the assembly separately, please.

The tint matters most. We will send colour chips. We need to know whether you can cast or source sheet tinted to them,
and how you keep one pair's panels the same colour."""),
    'b-horn-forming': ('thermoforming the horn', """I'm writing from EARF, a new hi-fi and lighting maker in San Francisco, for a quote on forming the horn of a loudspeaker we are prototyping. Tropos's horn is a
pressure-formed flare in 10 mm cell-cast acrylic, tinted through: a 610 x 346 mouth, about 630 x 366 outside, 238 deep. It is
formed over a male plug whose surface is the horn's air path; the outside is the free face and has to stay glossy. Our
model has the wall at about 8.5 mm at the throat end, thinning to about 6 at the mouth's sides and about 5 in its
corners; 4 mm is the least we can accept. After forming, the flare is annealed, trimmed on a 5-axis router, and its
rim is routed full round and polished.

The other horn parts are turned and milled from the same tinted lot: a throat piece from a 75 mm block, a pod rolled
from 6 mm sheet, a cap, pads and a saddle. They are cemented to the flare with a polymerising cement. If you can do the
whole horn, please quote it as one job; if not, the forming and trimming alone.

For the first pair we supply (or have cut for you by a pattern shop) a tooling-board plug on an aluminium base
plate; if you make such plugs yourselves, please quote one too. The production tool comes later, in aluminium.

A note on the colour. The horn's sheet is not the cabinet's: in each colour it is cast in its own, much heavier dye lot,
so that the formed horn reads deep and nearly opaque, with a dark neck. We estimate about 6 to 10 times the cabinet's
dye (Ember about 10, Smoke about 7), but the lot is matched to a colour chip we approve, not to a multiple. That
changes the forming in a few ways we would like your view on:

- A dark sheet takes up heat differently in an infrared oven. It absorbs more at the surface and heats unevenly through
  10 mm, so the heater settings, the soak time and possibly the forming temperature will differ from clear or lightly
  tinted sheet. Each colour may need its own settings, and the darkest (Smoke, Ember) the most care against surface
  overheating and bubbles. A circulating-air oven may suit it better.
- A dark horn shows less of the wall's thinning by eye, so we will measure the wall with a gauge rather than judge it
  by the colour. Mark-off and scratches show more on a dark gloss face, so we ask for care with the plug's polish and
  in handling.
- The heavier lot is a separate casting per colour, with its own minimum and cost, so the horn's sheet probably cannot
  come from the cabinet's batch. We ask below how you would match the two lots."""),
    'b-horn-tooling': ('the horn\'s forming tool', """I'm writing from EARF, a new hi-fi and lighting maker in San Francisco, for a quote on a thermoforming tool for a loudspeaker horn. For the prototype we want the plug
cut by 5-axis machining from high-temperature epoxy tooling board (rated 150 °C or more), sealed and polished, on a
machined aluminium base plate with a groove for the forming machine's clamp frame. We supply the CAD (STEP) of the
plug's surface, which is the horn's air path, and of the base.

Please also quote, as a separate later line, the production plug in aluminium: cast near shape and machined all over on
5 axes, cored, with oil channels to hold it at about 85 °C and 0.6 mm vents, on the same base plate. We will only order
it once the prototype's measurements confirm the profile. A trim fixture for the 5-axis router, copying the plug, is a
third line if you make those."""),
    'c-metal': ('CNC and sheet-metal work', """I'm writing from EARF, a new hi-fi and lighting maker in San Francisco, for a quote on the metal parts of a loudspeaker we are prototyping. There are six lines: a small folded
and welded aluminium box for the amplifier (1.5 mm, black anodised), a turned aluminium adaptor ring, stainless tube
posts (front and rear) threaded at one end, a set of turned brass sockets and threaded inserts, and an anodised rating plate,
laser-marked. The drawings give every size. The quantities are small for now: one pair first, then ten, then about
fifty."""),
    'd-other': ('other outside work', """I'm writing from EARF, a new hi-fi and lighting maker in San Francisco, for a quote on some smaller jobs for a loudspeaker we are prototyping. The cabinet is clear,
tinted acrylic, so these parts are seen and have to be neat: acoustic polyester batts cut to size and each sewn into a
white voile sleeve; a speaker cloth stretched over a frame; our wordmark laser-etched into the back panel and filled in
the speaker's colour; and a few seals (an EPDM cord loop with a vulcanised joint, a die-cut sponge gasket, small
polyurethane sleeves). Please quote whichever of these you do."""),
    'e-laminated-horn': ('a laminated acrylic horn and its cabinet', """I'm writing from EARF, a new hi-fi and lighting maker in San Francisco, for a quote on the acrylic of a loudspeaker we are prototyping: the cabinet, and a horn laminated from
stock sheet. Your site's "museum-grade acrylic bonding", "controlled lamination process to reduce bubbles and distortion"
and "we bond one-off prototypes", with a 5-axis router and diamond and buff polishing, are exactly what it needs, so we
would like to give you the whole job.

Tropos is a horn loudspeaker in clear tinted cell-cast acrylic, so you see into it. The first pair is in Smoke, from
stock sheet: the cabinet in TruCast 2064 Gray 3/4 in (19 mm; our drawings say 20, and every cut is to the sheet as
measured), the horn in 2074 Dark Gray 1/2 in. We can buy the sheet and have it delivered to you, or you can source it;
please say which you prefer.

**The cabinet** is as our drawings show: panels CNC-cut from our DXF files, edges milled square, the edges that show
polished, annealed before cementing; then corners, front panel, braces, ribs and land strips cemented with a two-part
polymerising cement (ACRIFIX 2R 0190 or Weld-On 40, no solvent cement) with no visible bubble in any joint; the box
annealed again; and the lands' faces, the bosses' faces and the back's seal groove milled in one setup.

**The horn** is 630 x 366 at its mouth and 278 deep, laminated from 22 layers of 1/2 in sheet and a boss (sheet BHH-005):
- each layer cut flat from our DXF (`dxf/layer-01.dxf` to `layer-22.dxf`: its outline, and a rough bore 3 mm inside
  the final air path), faced to the pitch less the bond line, and its outside edge polished before bonding (the
  stepped outside is a terrace a layer, and each edge shows);
- bonded with a polymerising cement in three sub-stacks, then the sub-stacks joined, with no bubble within 5 mm of the
  air path and none visible through the tint. As we read Röhm's and ACRYLITE's guides:
  - the cement is degassed no lower than about 0.2 bar, and the layers are pressed with dead weight on spacers, not in a
    vacuum bag;
  - the cut layers are annealed less than 24 hours before bonding, and no bonded face is polished;
  - no brass or copper is near the cement;
  - the layers register on their bores over a stepped core. We would rather not have dowel holes: through the tint they
    would show as rods in the wall. Tell us if you register another way;
- annealed, and the air path cut through the stack on 5 axes to our STEP (`step/air-path.step`, the horn's inside as a
  solid, from the throat at z = 0), then polished. Its shape is acoustically set and must follow the STEP; the bond lines
  cross it flush.

As an option, the same horn with its outside machined smooth to `step/outside-smooth.step` and polished, the bond lines
running round it as fine rings. Please price it as the extra over the stepped horn. The horn's small parts (pod, cap,
pads, saddle) are from the same sheet.

The pair is for a debut on 19 January, so the dates matter as much as the price: we would order in mid-November."""),
}

Q_BASE = {
    1: 'The unit price of each part at 1 pair, 10 pairs and 50 pairs (the quantities in the table are for those).',
    2: 'Tooling and setup: any one-off charge (fixtures, programming, moulds, mandrels), and what we would own.',
    3: 'Minimum order quantities and, for tinted material, any casting minimum: the least sheet or block you would cast or\n'
       '   buy in a colour, and its cost.',
    4: 'Lead time from order to delivery at each quantity, and for samples first.',
    5: 'Tint matching: can you match our colour chips (we will send them), and how do you prove a match (a swatch for our\n'
       '   approval, a spectrophotometer reading)?',
    6: 'The dye lot: can one pair\'s parts all come from one batch? If not, how are lots matched (to one swatch, each lot\'s\n'
       '   number marked on its parts)?',
    7: 'Packing: how the parts are protected and shipped (the faces are show faces and scratch).',
    8: 'Anything in the drawings you would change to make the parts cheaper or better, before you quote.',
}
# each kind's own wording of the common questions (None drops one; nothing in the tooling or the metal is tinted)
Q_KIND = {
    'a-cast-acrylic': {6: Q_BASE[6] + ' Can you pour the 3, 8 and 20 mm sheet and the block for the bosses in one batch?'},
    'b-horn-forming': {6: Q_BASE[6] + ' Can you pour the horn lot\'s 6, 10 and 30 mm sheet and its 75 mm block in one batch?'},
    'b-horn-tooling': {1: 'The price of each line.', 3: 'Minimum order, if any.',
                       4: 'Lead time from order to delivery for each line.', 5: None, 6: None,
                       7: 'Packing: how the plug and the plate are protected and shipped (any mark on the plug\'s face shows on every '
                          'horn formed over it).'},
    'c-metal': {3: 'Minimum order quantities, and any minimum lot for anodising.', 5: None, 6: None},
    'e-laminated-horn': {3: 'Whether you would source the stock sheet (TruCast 2064 3/4 in, 2074 1/2 in) or take ours, and any '
                            'handling charge.', 5: None,
                         6: 'Both speakers\' parts from one sheet of each code, so the pair matches: is that how you would '
                            'nest them?'},
}

EXTRA_Q = {
    'a-cast-acrylic': ['Whether you would rather cut from our nested sheets (DXF) or nest them yourselves.',
                       'Whether you can source the 121 x 4 tube in the same tint, or should it be rolled from sheet.'],
    'b-horn-forming': ['The press and oven you would use (pressure box, heaters), and whether you have formed 10 mm cast acrylic before, '
                       'in a deep tint.',
                       'How the darker horn lot changes your settings (heater zones, soak time, sheet temperature), and whether you would '
                       'run a trial sheet of each colour first; what that trial costs.',
                       'Whether a heavily tinted lot costs more to buy or cast, its minimum per colour, and whether it can be poured '
                       'with the cabinet\'s lot or must be a separate batch matched to the same chip.',
                       'The wall you expect at the mouth\'s corners, and whether you would recommend 12 mm sheet.',
                       'How many shots you would allow to set the process up on the prototype plug.'],
    'b-horn-tooling': ['How many shots a tooling-board plug lasts at about 170 °C sheet temperature.',
                       'Whether you would cast the production plug or machine it from a block, and its weight cored.'],
    'c-metal': ['Whether the box can be folded from one blank with welded corners, and how you keep the black anodise the same '
                'on the box, the ring and the plate, and from lot to lot.'],
    'd-other': ['Your minimum for a custom-sewn sleeve run, and whether you can cut the batts too.'],
    'e-laminated-horn': [
        'The bond line you can hold on 1/2 in layers (we design to the pitch less your bond line), and whether you would '
        'face each layer or the stack after bonding.',
        'How you anneal the bonded horn: by the stack\'s height (about 290 mm) or by its thickest wall (about 30 mm, 60 at '
        'the boss), how long a cycle takes, and whether annealing the three sub-stacks apart shortens it.',
        'Whether the cement may make the tint bleed at a joint, and whether you would bond two off-cuts of each colour first '
        '(we would pay for that test).',
        'Your 5-axis router\'s reach for a part 630 x 366 x 292, and how you hold the stack while cutting the air path.',
        'The edge finish of the layers: polished, or frosted as an option; and the price difference.',
        'How you would register 22 layers without dowel holes in the wall (on their bores over a stepped core, or waste '
        'ears trimmed off after), and whether a cement tinted to the sheet (Röhm allows a solvent-soluble colourant) is '
        'something you have done.',
        'The earliest date you could deliver the first horn and the cabinet pair, ordering in mid-November, and whether '
        'a delivery by early January for both speakers is realistic.',
    ],
}


def questions(kind):
    """The numbered questions for one kind: the common ones in its own wording, then its own."""
    qs = [Q_KIND.get(kind, {}).get(n, Q_BASE[n]) for n in sorted(Q_BASE)]
    qs = [q for q in qs if q] + EXTRA_Q.get(kind, [])
    return '\n'.join(f'{n}. {q}' for n, q in enumerate(qs, 1))


def rows():
    return list(csv.DictReader(open(os.path.join(OUT, 'bom.csv'))))


def named(item, key):
    """Whether a parts-list item is `key`: the same name, or (a key ending in '-', or 'lining-left-2' and the like) a
    family of names it begins."""
    return item == key or (key.endswith('-') and item.startswith(key)) or (key[-1].isdigit() and item.startswith(key) and item[len(key):].isalpha())


def sheet_of(item):
    for k in sorted(SHEET, key=len, reverse=True):
        if named(item, k):
            return SHEET[k]
    return ''


def qty(r, item):
    q = float(r['qty'])
    if r.get('option', '').startswith('tooling'):
        return '1', '1', '1'
    fmt = lambda v: f'{v:g}'
    return fmt(q), fmt(q * 10), fmt(q * 50)


def table(kind):
    out = []
    bom = rows()
    bom_ho = list(csv.DictReader(open(os.path.join(OUT_HO, 'bom.csv'))))
    for i, (pre, part, mat, th, tint, fin, tol) in enumerate(KINDS[kind], 1):
        if isinstance(pre, str) and pre.startswith('ho:'):
            match = [r for r in bom_ho if r['item'] == pre[3:]]
            if match:
                q = float(match[0]['qty'])
                out.append(dict(no=f'{kind[0].upper()}{i:02d}', part=part, items=pre[3:], sheets=HO_SHEET[pre[3:]],
                                material=mat, thickness_mm=th, tint=tint, qty_1_pair=f'{q:g}', qty_10_pairs=f'{q * 10:g}',
                                qty_50_pairs=f'{q * 50:g}', finish=fin, tolerance_mm=tol))
            continue
        pres = pre if isinstance(pre, tuple) else (pre,)
        match = [r for r in bom if any(named(it.strip(), p) for it in r['item'].split(',') for p in pres)]
        if not match:
            continue
        items = ', '.join(r['item'] for r in match)
        q = [sum(float(qty(r, items)[k]) for r in match) for k in range(3)]
        if any(r.get('option', '').startswith('tooling') for r in match):
            q = [1, 1, 1]
        sheets = sorted({str(sheet_of(it.strip())) for r in match for it in r['item'].split(',') if sheet_of(it.strip()) != ''},
                        key=lambda v: (not v.isdigit(), int(v) if v.isdigit() else 0))
        out.append(dict(no=f'{kind[0].upper()}{i:02d}', part=part, items=items, sheets=', '.join(sheets),
                        material=mat, thickness_mm=th, tint=tint, qty_1_pair=f'{q[0]:g}', qty_10_pairs=f'{q[1]:g}',
                        qty_50_pairs=f'{q[2]:g}', finish=fin, tolerance_mm=tol))
    return out


def pdf_pages(kind, tab):
    pages = set(COMMON)
    for t in tab:
        pages |= {int(s) for s in t['sheets'].split(', ') if s.isdigit()}
    if kind in ('a-cast-acrylic', 'e-laminated-horn'):
        pages |= set(range(4, 22))
    if kind == 'd-other':
        pages |= {4, 10, 16, 22, 23, 24, 25}
    return sorted(pages)


def write(kind):
    d = os.path.join(HERE, kind)
    os.makedirs(d, exist_ok=True)
    tab = table(kind)
    cols = ['no', 'part', 'items', 'sheets', 'material', 'thickness_mm', 'tint', 'qty_1_pair', 'qty_10_pairs', 'qty_50_pairs',
            'finish', 'tolerance_mm']
    with open(os.path.join(d, 'parts.csv'), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); [w.writerow(t) for t in tab]
    pages = pdf_pages(kind, tab)
    with tempfile.TemporaryDirectory() as tmp:
        for p in pages:
            subprocess.run(['pdfseparate', '-f', str(p), '-l', str(p), SHEETS_PDF, os.path.join(tmp, f'{p:03d}.pdf')], check=True)
        extra = []
        if kind == 'e-laminated-horn':             # the laminated horn's own sheets, after the Cloud's
            for p in HO_PAGES:
                subprocess.run(['pdfseparate', '-f', str(p), '-l', str(p), SHEETS_HO, os.path.join(tmp, f'ho{p:03d}.pdf')], check=True)
                extra.append(os.path.join(tmp, f'ho{p:03d}.pdf'))
        subprocess.run(['pdfunite'] + [os.path.join(tmp, f'{p:03d}.pdf') for p in pages] + extra + [os.path.join(d, 'drawings.pdf')], check=True)
    title, body = INTRO[kind]
    md = [f'# Request for quotation: {title}', '', 'To: [vendor]  ', 'From: ' + SIGN + '  ', 'Date: [date]  ',
          'Re: Tropos loudspeaker, prototype pair, then 10 and 50 pairs', '', 'Hello,', '', body, '',
          '## The parts', '',
          ('Each line is one tool, whatever the number of speakers. ' if kind == 'b-horn-tooling' else
           'Quantities are for one pair (two speakers), then 10 and 50 pairs. ') + 'Sheet numbers are in the attached '
          '`drawings.pdf` (our drawing set BHC-001 to BHC-040, issue 2026-10-25; the general arrangement, the section, '
          'the exploded view and the notes are attached to every request). Dimensions in mm.' +
          (' The DXF cut files and the nested sheets come with this letter (`dxf/`), and STEP files of every part too '
           '(`step/`: the bosses, the tubes, the cups and the IR parts have no DXF).' if kind == 'a-cast-acrylic' else
           ' The laminated horn is drawn on our sheet BHH-005 (issue 2026-10-31, attached after the cabinet\'s sheets). Its '
           'layers come as DXF (`dxf/layer-01.dxf` to `layer-22.dxf`, with `layers.csv`), and its air path and smooth outside '
           'as STEP (`step/`); the cabinet\'s DXF cut files and STEP files come with this letter as well.'
           if kind == 'e-laminated-horn' else ' STEP files of every part come with this letter (`step/`).'), '',
          '| no. | part | our part names | sheet | material | thickness | tint | 1 pair | 10 pairs | 50 pairs | finish | tolerance |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for t in tab:
        md.append('| ' + ' | '.join(t[c] for c in cols) + ' |')
    md += ['', '## What I would like to know', '', questions(kind)] + [
        '', 'If any of this is outside what you do, a word to say so is just as useful, and the name of someone who does it '
        'would be very welcome.', '', 'Thank you,', '', SIGN, '',
        '---', '', f'*Attach: `drawings.pdf` (sheets {", ".join(str(p) for p in pages)}'
        + (', then BHH-' + ', BHH-'.join(f'{p:03d}' for p in HO_PAGES) if kind == 'e-laminated-horn' else '') + '), `parts.csv`'
        + (', the DXF and STEP files of the parts listed' if kind in ('a-cast-acrylic', 'e-laminated-horn')
           else ', the STEP files of the parts listed') + '.*', '']
    open(os.path.join(d, 'letter.md'), 'w').write('\n'.join(md))
    return len(tab), pages


if __name__ == '__main__':
    for k in KINDS:
        n, pages = write(k)
        print(f'{k}: {n} lines, drawings.pdf with {len(pages)} sheets')
