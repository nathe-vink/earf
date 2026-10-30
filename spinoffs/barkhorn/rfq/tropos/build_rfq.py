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
HORN_TINT = 'the speaker\'s colour, horn lot (about 3 x the cabinet\'s dye, matched on a swatch): Ember and Smoke'
POLISH = 'edges milled square; show edges polished; annealed before cementing'

# kind -> [(bom item prefix, part, material, thickness, tint, finish, tolerance)]; quantities come from the parts list
KINDS = {
    'a-cast-acrylic': [
        ('left', 'shell sides', 'cell-cast acrylic', '20', CAB_TINT, POLISH, PANEL_TOL),
        ('top', 'shell top', 'cell-cast acrylic', '20', CAB_TINT, POLISH + '; 4 post sockets and an M12 thread', PANEL_TOL),
        ('bottom', 'shell bottom', 'cell-cast acrylic', '20', CAB_TINT, POLISH + '; 4 feet insert holes', PANEL_TOL),
        ('front-panel', 'front panel', 'cell-cast acrylic', '20', CAB_TINT, POLISH + '; woofer rebate, port recesses, magnet pockets', PANEL_TOL),
        ('back', 'back (removable)', 'cell-cast acrylic', '20', CAB_TINT, POLISH + '; amplifier cutout and recess; EARF etched (see d)', PANEL_TOL),
        ('brace', 'braces', 'cell-cast acrylic', '20', CAB_TINT, 'edges milled square (inside)', PANEL_TOL),
        ('rib-', 'ribs', 'cell-cast acrylic', '20', CAB_TINT, 'edges milled square (inside)', PANEL_TOL),
        ('land-', 'land strips', 'cell-cast acrylic', '20', CAB_TINT, 'M5 insert holes; the seal groove milled after assembly', PANEL_TOL),
        ('top-pad', 'pad under the top', 'cell-cast acrylic', '20', CAB_TINT, 'M12 thread, an insert hole', PANEL_TOL),
        ('back-boss-', 'brace bosses', 'cast acrylic block, cabinet lot', '36 x 36 x 85', CAB_TINT, 'milled, slotted over the brace; M5 insert hole', '±0.2'),
        ('woofer-ring', 'woofer ring', 'cell-cast acrylic', '6', 'opaque, in the ring colour (Ember: oxblood, about #7A1A1C; Smoke: near-black #141316)', 'face polished; screw-head and disc pockets behind', PANEL_TOL),
        ('disc-frame', 'cloth disc frame', 'cell-cast acrylic', '12', 'black', 'face edge rounded R5; magnet pockets', PANEL_TOL),
        ('port-frame-', 'port frames', 'cell-cast acrylic', '8', CAB_TINT, 'mouth rounded R8 and polished; 4 countersinks', PANEL_TOL),
        ('port-left', 'port tubes', 'cast acrylic tube 121 x 4 wall', '4 (wall)', CAB_TINT + ' (tinted tube: ask)', 'inner end flared R8 over a heated mandrel, annealed; bore polished; cemented into its frame', '±0.3'),
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

INTRO = {
    'a-cast-acrylic': ('cast acrylic fabrication', """I'm writing for a quote on the acrylic parts of a loudspeaker we are prototyping. Tropos is a horn loudspeaker
whose cabinet is 20 mm cell-cast acrylic, tinted through, so you see into it. The first pair will be in two colours,
Ember (a transparent red) and Smoke (a transparent black). If it goes well, ten pairs follow, then about fifty.

We need the panels cut on a CNC router from our DXF files, edges milled square, the edges that show polished, and the
panels annealed before they are cemented. If you also assemble, we would like a price for the cemented cabinet:
corners, front panel, braces, ribs and land strips cemented with a two-part polymerising cement (ACRIFIX 2R 0190 or
Weld-On 40, no solvent cement), with no visible bubble in any joint; the box annealed again; and the lands' faces, the
bosses' faces and the seal's groove milled in one setup. Quote the cutting and the assembly separately, please.

The tint matters most. We will send colour chips. We need to know whether you can cast or source sheet tinted to them,
and how you keep one pair's panels the same colour."""),
    'b-horn-forming': ('thermoforming the horn', """I'm writing for a quote on forming the horn of a loudspeaker we are prototyping. Tropos's horn is a
pressure-formed flare in 10 mm cell-cast acrylic, tinted through: a 610 x 346 mouth, about 630 x 366 outside, 238 deep. It is
formed over a male plug whose surface is the horn's air path; the outside is the free face and has to stay glossy. Our
model has the wall at about 8.5 mm at the throat end, thinning to about 6 at the mouth's sides and about 5 in its
corners; 4 mm is the least we can accept. After forming, the flare is annealed, trimmed on a 5-axis router, and its
rim is routed full round and polished.

The other horn parts are turned and milled from the same tinted lot: a throat piece from a 75 mm block, a pod rolled
from 6 mm sheet, a cap, pads and a saddle. They are cemented to the flare with a polymerising cement. If you can do the
whole horn, please quote it as one job; if not, the forming and trimming alone.

For the first pair we supply (or have cut for you; see the tooling letter) a tooling-board plug on an aluminium base
plate. The production tool comes later, in aluminium."""),
    'b-horn-tooling': ('the horn\'s forming tool', """I'm writing for a quote on a thermoforming tool for a loudspeaker horn. For the prototype we want the plug
cut by 5-axis machining from high-temperature epoxy tooling board (rated 150 °C or more), sealed and polished, on a
machined aluminium base plate with a groove for the forming machine's clamp frame. We supply the CAD (STEP) of the
plug's surface, which is the horn's air path, and of the base.

Please also quote, as a separate later line, the production plug in aluminium: cast near shape and machined all over on
5 axes, cored, with oil channels to hold it at about 85 °C and 0.6 mm vents, on the same base plate. We will only order
it once the prototype's measurements confirm the profile. A trim fixture for the 5-axis router, copying the plug, is a
third line if you make those."""),
    'c-metal': ('CNC and sheet-metal work', """I'm writing for a quote on the metal parts of a loudspeaker we are prototyping. There are six: a small folded
and welded aluminium box for the amplifier (1.5 mm, black anodised), a turned aluminium adaptor ring, stainless tube
posts threaded at one end, a set of turned brass sockets and threaded inserts, and an anodised rating plate,
laser-marked. The drawings give every size. The quantities are small for now: one pair first, then ten, then about
fifty."""),
    'd-other': ('other outside work', """I'm writing for a quote on some smaller jobs for a loudspeaker we are prototyping. The cabinet is clear,
tinted acrylic, so these parts are seen and have to be neat: acoustic polyester batts cut to size and each sewn into a
white voile sleeve; a speaker cloth stretched over a frame; our wordmark laser-etched into the back panel and filled in
the speaker's colour; and a few seals (an EPDM cord loop with a vulcanised joint, a die-cut sponge gasket, small
polyurethane sleeves). Please quote whichever of these you do."""),
}

QUESTIONS = """1. The unit price of each part at 1 pair, 10 pairs and 50 pairs (the quantities in the table are for those).
2. Tooling and setup: any one-off charge (fixtures, programming, moulds, mandrels), and what we would own.
3. Minimum order quantities and, for tinted material, any casting minimum: the least sheet or block you would cast or
   buy in a colour, and its cost.
4. Lead time from order to delivery at each quantity, and for samples first.
5. Tint matching: can you match our colour chips (we will send them), and how do you prove a match (a swatch for our
   approval, a spectrophotometer reading)?
6. The dye lot: can one pair's parts all come from one batch? If not, how are lots matched (to one swatch, each lot's
   number marked on its parts)? Can you pour 6, 10, 20, 30 and 75 mm in one batch?
7. Packing: how the parts are protected and shipped (the faces are show faces and scratch).
8. Anything in the drawings you would change to make the parts cheaper or better, before you quote."""

EXTRA_Q = {
    'a-cast-acrylic': ['9. Whether you would rather cut from our nested sheets (DXF) or nest them yourselves.',
                       '10. Whether you can source the 121 x 4 tube in the same tint, or should it be rolled from sheet.'],
    'b-horn-forming': ['9. The press and oven you would use (pressure box, heaters), and whether you have formed 10 mm cast acrylic before.',
                       '10. The wall you expect at the mouth\'s corners, and whether you would recommend 12 mm sheet.',
                       '11. How many shots you would allow to set the process up on the prototype plug.'],
    'b-horn-tooling': ['9. How many shots a tooling-board plug lasts at about 170 °C sheet temperature.',
                       '10. Whether you would cast the production plug or machine it from a block, and its weight cored.'],
    'c-metal': ['9. Whether the box can be folded from one blank with welded corners, and the anodising colour match.'],
    'd-other': ['9. Your minimum for a custom-sewn sleeve run, and whether you can cut the batts too.'],
}


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
    for i, (pre, part, mat, th, tint, fin, tol) in enumerate(KINDS[kind], 1):
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
    if kind == 'a-cast-acrylic':
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
        subprocess.run(['pdfunite'] + [os.path.join(tmp, f'{p:03d}.pdf') for p in pages] + [os.path.join(d, 'drawings.pdf')], check=True)
    title, body = INTRO[kind]
    md = [f'# Request for quotation: {title}', '', 'To: [vendor]  ', 'From: ' + SIGN + '  ', 'Date: [date]  ',
          'Re: Tropos loudspeaker, prototype pair, then 10 and 50 pairs', '', 'Hello,', '', body, '',
          '## The parts', '',
          'Quantities are for one pair (two speakers), then 10 and 50 pairs. Sheet numbers are in the attached '
          '`drawings.pdf` (our drawing set BHC-001 to BHC-040, issue 2026-10-25; the general arrangement, the section, '
          'the exploded view and the notes are attached to every request). Dimensions in mm.' +
          (' The DXF cut files and the nested sheets come with this letter (`dxf/`).' if kind == 'a-cast-acrylic' else '') +
          (' STEP files of every part come with this letter (`step/`).' if kind != 'a-cast-acrylic' else ''), '',
          '| no. | part | our part names | sheet | material | thickness | tint | 1 pair | 10 pairs | 50 pairs | finish | tolerance |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for t in tab:
        md.append('| ' + ' | '.join(t[c] for c in cols) + ' |')
    md += ['', '## What I would like to know', '', QUESTIONS] + EXTRA_Q.get(kind, []) + [
        '', 'If any of this is outside what you do, a word to say so is just as useful, and the name of someone who does it '
        'would be very welcome.', '', 'Thank you,', '', SIGN, '',
        '---', '', f'*Attach: `drawings.pdf` (sheets {", ".join(str(p) for p in pages)}), `parts.csv`'
        + (', the DXF files of the parts listed' if kind == 'a-cast-acrylic' else ', the STEP files of the parts listed') + '.*', '']
    open(os.path.join(d, 'letter.md'), 'w').write('\n'.join(md))
    return len(tab), pages


if __name__ == '__main__':
    for k in KINDS:
        n, pages = write(k)
        print(f'{k}: {n} lines, drawings.pdf with {len(pages)} sheets')
