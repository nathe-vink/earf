"""The six chosen objects: dimensions, process, BOM at a run of 100 (est.), price. Run: python3 six.py > SIX.md
Rates (est. unless sourced): cast sheet per ft2, from R1 (r46-owner-notes, read 2026-10-31): 1/2" $26.12 (AC Plastics,
$835.80 a 48x96), 3/8" $21.26, 1/4" (0.220") $8.34 (Canal, $267), 1/8" $4.44 (Canal, $142); 3030 Glass Green 1/4" priced
as 1/4" colour. Offcut 25%. Shop time $100 an hour (the companions' kit rate band $90-120). Price about 2.2-2.4x landed
for direct sales (the line's multiple, est.)."""
FT2 = 0.09290304  # m2
SHEET = {'1/2': 26.12, '3/8': 21.26, '1/4': 8.34, '1/8': 4.44}
RATE = 100

def sheet(kind, m2, offcut=1.25):
    return SHEET[kind] * m2 / FT2 * offcut

OBJECTS = [
 dict(key='moho', name='Moho', what='A record weight', tag='The boundary between the crust and the mantle; it sits on a record, on Mantle or any turntable.',
  concept=("Four discs of half-inch cast sheet, bonded into one puck 66 mm across and 51 mm tall, each layer a different tint, "
           "with a brass core you see through the colour. It sits on the label over the spindle and presses the record flat. Turned and "
           "polished, it shows its strata at the edge like a sawn core; the order of the tints is chosen at the shop, from the line's eight. "
           "Its blanks are the discs left over from boring Lithos's rings, so it costs almost nothing in sheet."),
  dims=[('Diameter', '66 mm'), ('Height', '50.8 mm (4 × 12.7)'), ('Brass core', 'Ø 25 mm, full height, C360'), ('Spindle bore', 'Ø 7.6 × 22 mm, in the brass'),
        ('Contact', 'a relieved ring under it, Ø 40–60 mm, so it rests on the label, not the grooves'), ('Weight', 'about 390 g (acrylic 175 g, brass 215 g; est.)')],
  process='Laminate four 75 mm squares (polymerising cement, pressed, annealed); turn to Ø 66; bore Ø 25 and press in the brass; bore the spindle hole; diamond-turn and flame-polish the edge and top.',
  bom=[('Sheet: four 75 mm squares of 1/2" (or Lithos\'s cores, near free)', lambda: sheet('1/2', 4 * 0.075**2)), ('Brass rod, Ø 1", 2"', lambda: 8),
       ('Cement', lambda: 1.5), ('Turning, boring, pressing: 15 min', lambda: RATE * 0.25), ('Polishing: 6 min', lambda: RATE * 0.1),
       ('A felt-lined card tube with the tint card', lambda: 4)],
  price=135, role='The entry price: a gift, a Kickstarter add-on, a thing for every record shop counter.'),
 dict(key='lithos', name='Lithos', what='A floor lamp, a core sample', tag='Rock, in layers: a drill core stood on end.',
  concept=("A column 110 mm across and 1.12 m tall, made of 87 rings of half-inch cast sheet in eight bands of the line's tints, in "
           "uneven thicknesses like a real core. Between every band sits a quarter-inch layer of near-clear 3030 sheet. A warm LED line in "
           "the bore lights those clear layers from inside, and their polished outer edges glow: **the boundaries between the strata are lines "
           "of light**, while the tinted bands stay deep. An LED uplight in the top of the bore washes the ceiling, which is the light you "
           "read by. The column stands on a blackened steel disc."),
  dims=[('Column', 'Ø 110 mm outside, Ø 76 mm bore, 1,100 mm of acrylic'), ('Height overall', 'about 1,120 mm'), ('Base', 'blackened steel, Ø 320 × 20 mm'),
        ('Bands', 'eight tints, 6 to 16 rings each (87 rings of 12.7 mm), with nine 5.6 mm clear light-guide layers'),
        ('Light', 'uplight about 900 lm, 2700 K, CRI 90 (est.); glow line about 6 W; two channels, dimmable'), ('Weight', 'about 21 kg (acrylic 7 kg, base 12.6 kg; est.)'),
        ('Listing', 'UL 153 (a portable lamp), with its own Class 2 driver')],
  process='Rings laser- or CNC-cut from sheet (their cores become Moho); bonded in eight bands with the clear guides between, annealed; bored and turned true; the outside polished; stacked on a threaded aluminium tube through the base.',
  bom=[('Sheet: 87 rings from 115 mm squares of 1/2"', lambda: sheet('1/2', 87 * 0.115**2)), ('Clear 3030 guides: nine from 1/4"', lambda: sheet('1/4', 9 * 0.115**2)),
       ('Ring cutting, outsourced, about $2 each', lambda: 96 * 2), ('Lamination in bands: 3 h', lambda: RATE * 3), ('Boring, turning, polishing: 3 h', lambda: RATE * 3),
       ('Steel base, cut and blackened', lambda: 110), ('Aluminium core tube', lambda: 25), ('LEDs, drivers, dimmer, cord', lambda: 95),
       ('Assembly and test: 1 h', lambda: RATE), ('A crate', lambda: 80)],
  price=3600, role='The statement piece: the signature of lamination made into light. Hotels and the bar\'s corners; a numbered edition.'),
 dict(key='ionos', name='Ionos', what='A radio and streamer', tag='The ionosphere carries radio round the curve of the Earth.',
  concept=("A block of nine bonded layers of one tint, 200 × 110 × 115 mm, with a near-clear layer at its middle lit from inside, so "
           "a single line of light runs round it. You tune by turning the top: the uppermost disc, 100 mm across, turns on a bearing, "
           "clicking from station to station, and the line of light brightens as a station locks. Push the disc to play or pause. It streams "
           "and plays internet radio into Tropos or any amplifier, through line, optical and coaxial outputs on an aluminium plate at the back. "
           "No screen, no speaker, no handle."),
  dims=[('Block', '200 W × 110 D × 115 H mm (nine layers of 12.7 mm)'), ('Top disc', 'Ø 100 × 12.7 mm, on a bearing, 24 detents'),
        ('Light', 'a 5.6 mm clear 3030 layer at mid-height, edge-lit from inside'), ('Inside', 'a machined pocket: a single-board computer, a DAC board, a magnetic angle sensor'),
        ('Outputs', 'RCA line, optical, coaxial; USB-C power'), ('Weight', 'about 2.4 kg (est.)'), ('Compliance', 'FCC Part 15B on the product; the Wi-Fi module carries its own grant')],
  process='Laminate the block, machine the pocket and the top recess, polish all faces; turn the top disc; fit the electronics, sensor and bearing; back plate in anodised aluminium.',
  bom=[('Sheet: nine layers of 1/2", 200 × 110', lambda: sheet('1/2', 9 * 0.2 * 0.11)), ('Top disc and clear layer', lambda: sheet('1/2', 0.11**2) + sheet('1/4', 0.2 * 0.11)),
       ('Lamination, pocket machining, polishing: 2.5 h', lambda: RATE * 2.5), ('Top disc turning: 25 min', lambda: RATE * 0.4),
       ('Single-board computer (2 GB class)', lambda: 50), ('DAC board with outputs', lambda: 70), ('Angle sensor, bearing, detent', lambda: 18),
       ('Power supply, sockets, back plate', lambda: 55), ('Edge-light LEDs', lambda: 6), ('Assembly and test: 1 h', lambda: RATE),
       ('FCC 15B, amortised over 100', lambda: 30), ('A box', lambda: 25)],
  price=1450, role='A listening object below Tropos\'s price: a gift for the hi-fi crowd, a hotel room\'s radio, the add-on that makes a pair complete.'),
 dict(key='cairn', name='Cairn', what='Bookends', tag='Stones stacked to mark a way.',
  concept=("Five slabs of half-inch sheet, each smaller than the one below and set a little off its centre, bonded into a stepped stack "
           "like stones on a trail. Two tints to a pair, never a rainbow: Smoke with one layer of Ember, say. The slabs' faces are the sheet's "
           "own polish; their sawn sides are left satin, so the strata read as matte lines between bright faces. A stainless tongue under the "
           "bottom slab goes under the books and holds them."),
  dims=[('Each', 'about 160 W × 120 D × 64 H mm (five layers of 12.7 mm)'), ('Slabs', '160×120, 140×110, 120×100, 100×90, 80×80 mm, offset ±8 mm'),
        ('Tongue', '2 mm stainless, 120 × 100 mm, let into the base'), ('Weight', 'about 1.1 kg each (est.)')],
  process='Slabs laser-cut; faces left as cast; sides sawn and sanded to a satin; bonded in a jig; the tongue let in flush; silicone feet.',
  bom=[('Sheet: five slabs of 1/2", two tints (each bookend)', lambda: 2 * sheet('1/2', 0.16*0.12 + 0.14*0.11 + 0.12*0.10 + 0.10*0.09 + 0.08*0.08)),
       ('Laser cutting: 2 × 9 min', lambda: RATE * 0.3), ('Satin sides, bonding: 2 × 20 min', lambda: RATE * 0.67),
       ('Stainless tongues and feet', lambda: 14), ('A box for the pair', lambda: 12)],
  price=395, role='A gift at a gift\'s price, made largely from the larger pieces\' offcuts.'),
 dict(key='bedrock', name='Bedrock', what='A record stand', tag='The solid rock under everything.',
  concept=("Two end-plates, each two half-inch layers bonded into one inch of colour, cut to a stepped profile so the strata show along "
           "every edge, joined by three brushed steel rails. It holds about eighty records upright, spines up, for flicking through. Bars "
           "and hotel rooms buy them by the dozen; at home it stands on the floor beside the turntable."),
  dims=[('Overall', '230 H × 300 D × 470 W mm'), ('End-plates', '25.4 mm (2 × 12.7), stepped profile'), ('Rails', 'three, Ø 20 mm stainless, 420 mm between plates'),
        ('Holds', 'about 80 LPs (est.)'), ('Weight', 'about 6 kg (est.)')],
  process='Laminate the plate blanks; CNC the stepped profile and the rail seats; polish the edges; rails through-bolted with recessed cap screws into threaded inserts.',
  bom=[('Sheet: four plate blanks of 1/2", 240 × 310', lambda: sheet('1/2', 4 * 0.24 * 0.31)), ('Lamination: 30 min', lambda: RATE * 0.5),
       ('CNC profile and polish: 1.5 h', lambda: RATE * 1.5), ('Stainless rails and fasteners', lambda: 44), ('Feet', lambda: 2),
       ('Assembly: 20 min', lambda: RATE * 0.33), ('A box', lambda: 30)],
  price=890, role='Trade and hospitality: bars, record shops and hotel suites order in numbers.'),
 dict(key='relief', name='Relief', what='A lit relief for a wall', tag='A landscape, drawn in its contour lines.',
  concept=("A square of contour layers, each a quarter-inch sheet of one tint cut to a level of an imagined landscape, stacked twelve high "
           "on a backing so the panel rises 67 mm at its peaks. A hidden LED bar along the top of its frame washes light down across it: the "
           "polished contour edges catch the light and draw the landscape in lines of colour, and the steps scatter sound. It is a lit relief "
           "first; any acoustic figure waits for a measurement."),
  dims=[('Panel', '600 × 600 mm, up to 67 mm deep (12 layers of 5.6 mm)'), ('Backing', 'aluminium composite, 6 mm, on a French cleat'),
        ('Light', 'a concealed 24 V grazing bar along the top, about 12 W, 2700 K (est.)'), ('Weight', 'about 13 kg (est.)'),
        ('Sound', 'a stepped scattering surface; untested (est. from depth: above about 1.3 kHz)')],
  process='Each layer laser-cut from its own sheet, nested so the offcuts feed the smaller layers; stacked and bonded on registration pins; edges left as laser-polished; bonded to the backing; the light bar in the frame.',
  bom=[('Sheet: twelve layers of 1/4", nested (10% offcut)', lambda: sheet('1/4', 12 * 0.6 * 0.6, offcut=1.10)), ('Laser cutting: 2.5 h', lambda: RATE * 2.5),
       ('Stacking and bonding: 2 h', lambda: RATE * 2), ('Backing and cleat', lambda: 75), ('LED bar, diffuser, driver', lambda: 70),
       ('Assembly and test: 1 h', lambda: RATE), ('A crate', lambda: 60)],
  price=2600, role='For rooms: hotel lobbies, studios, bars and listening rooms; specified by interior designers.'),
]

def main():
    p = print
    p("# EARF new objects: the six\n")
    p("Brand lane, 31 October 2026. **Proposals for the owner; nothing is ordered or tested.** All costs are est. at a run of")
    p("100 unless a source is named (rates in `six.py`'s header). Prices are proposals at about 2.2–2.4× landed. Generated by `six.py`.\n")
    p("| | What | Price (est.) | Landed (est.) | Margin |\n|---|---|---|---|---|")
    for o in OBJECTS:
        t = sum(f() for _, f in o['bom'])
        p(f"| **{o['name']}** | {o['what']} | ${o['price']:,} | ${t:,.0f} | {(o['price'] - t) / o['price']:.0%} |")
    for o in OBJECTS:
        t = sum(f() for _, f in o['bom'])
        p(f"\n## {o['name']}: {o['what'].lower()}\n\n*{o['tag']}*\n\n{o['concept']}\n")
        p("| Dimension | |\n|---|---|")
        for a, b in o['dims']:
            p(f"| {a} | {b} |")
        p(f"\n**Materials and process.** {o['process']}\n")
        p("| BOM line (a run of 100, est.) | USD |\n|---|---|")
        for a, f in o['bom']:
            p(f"| {a} | ${f():,.0f} |")
        p(f"| **Landed** | **${t:,.0f}** |\n\n**Price:** ${o['price']:,} (est.), {o['price'] / t:.1f}× landed. **Its role:** {o['role']}")

if __name__ == '__main__':
    main()
