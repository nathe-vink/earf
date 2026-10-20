"""Round 33, EARFcoin (the owner, 2026-10-20: "One idea I had before bed: EARFcoin. Acrylic coins with the EARF globe on
them that can be exchanged for a song request. Each guest gets one."). The site's acrylic coins (icons_real.py --coin,
the loader and the colour picker) made real: a disc of cast acrylic in each speaker's tint, 40 across and 6 thick, its
edges rounded 1.5 and polished, the globe in the middle and GOOD FOR ONE SONG round the rim. Every number here is a
proposal until the owner signs it.

A tinted coin shows both faces at once, so the two never overlap: the globe sits inside 25 across, and the words in a
band from 15 to 17 from the centre, each reading the right way from the front. Three ways to put the globe on (FACES):

- engraved (A): the globe's line drawing (earth.edge_lines, the brand's stroke mark) laser-engraved 0.2 deep into the
  BACK face, mirrored in the file, so from the front it reads the right way round as frosted lines 6 mm down in the
  tint. The cheapest, and the most acrylic.
- printed (B): the six-colour globe (earth.disc_shapes, flush, the colour mark) UV-printed on the back face of a Fog
  (water-clear) coin, colour first and a white underlay over it, sealed; read through the clear.
- cast (C): the one-colour mosaic (earth.disc_shapes, seamed) cut from 1 mm tinted sheet and set mid-thickness in a
  clear cast resin coin, an embedment: the guest's colour is the globe, floating.

The words are engraved into the FRONT face in each case (frosted, 0.12 deep, IBM Plex Mono SemiBold, the site's mono),
GOOD FOR ONE SONG over the top and EARF under the bottom. The edge (EDGES) is plain (rounded and polished) or reeded
(100 grooves milled across it, as money is).

The frame (mm): the coin lies on its back face, z up from 0 (the back face) to 6 (the front), x right and y away from
a viewer at the front, so seen from above the art reads as drawn (x right, y up).

    .venv-fab/bin/python spinoffs/barkhorn/companions/coin.py            # the study model (every face and edge), the
                                                                         # request column and the laser files
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
BARKHORN = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, BARKHORN)

# --- the proposal (mm) ----------------------------------------------------------------------------------------------
D, T, ROUND = 40.0, 6.0, 1.5            # across, thick, the edges' radius (a casino chip is 39 x 3.3, 10 g)
GLOBE_D = 25.0                          # the globe, inside the words
WORDS_R = (15.0, 16.9)                  # the words' band: from the top's baseline to its caps' tops (Plex caps 0.698 em)
TRACK = 0.30                            # the words' tracking (mm a letter)
WORDS_TOP, WORDS_BOTTOM = 'GOOD FOR ONE SONG', 'EARF'
ALT_TOP = 'ONE COIN · ONE SONG'         # the one alternative offered
ENGRAVE = (0.03, 0.22)                  # the globe's engraving in the back face (z, from the back: its frost, a hair in)
WORDS_Z = (T - 0.12, T - 0.03)          # the words' engraving in the front face
PRINT = (-0.030, -0.006, -0.060, -0.034)   # the print under the back: colour z0, z1; white underlay z0, z1
INLAY = (T / 2 - 0.5, T / 2 + 0.5)      # the cast-in globe, 1 mm sheet at mid-thickness
REEDS, REED_R, REED_DEPTH = 100, 0.45, 0.30
DENSITY = 1.19                          # g/cm3, cast acrylic

FACES = ('engraved', 'printed', 'cast')
EDGES = ('plain', 'reeded')
FONT = os.path.join(ROOT, 'studio', 'fabkit', 'fonts', 'IBMPlexMono-SemiBold.ttf')

# The column the requests stack in, at the decks (mm): a water-clear cast tube on a base; coins drop in at the top and
# the lowest one is pushed out through a slot at the foot, so the queue plays from the bottom up
COL = dict(tube_od=50.0, tube_id=42.0, tube_h=210.0, base_d=96.0, base_h=24.0, slot_h=6.8, slot_w=41.6, notch_w=22.0,
           seat=4.0, ring_h=8.0)


def mass_g():
    return math.pi * (D / 2) ** 2 * T / 1000 * DENSITY      # ~9 g; the rounds take off about 0.2


# --- the art (shapely, mm, centred, y up as seen from the front) ----------------------------------------------------
def _flip(g):
    from shapely import affinity
    return affinity.scale(g, 1, -1, origin=(0, 0))


def globe_lines(d=GLOBE_D):
    """The globe's line drawing (the brand's stroke mark, earth.strokes_body) as filled areas, d across."""
    import earth as E
    from shapely import affinity
    w = E.STROKE['w']
    k = 1 / (1 + w / 2)
    lines = affinity.scale(E.edge_lines(), k, k, origin=(0, 0))
    g = lines.buffer(w * k / 2, cap_style='round', join_style='round', quad_segs=6)
    s = (d / 2) / max(abs(v) for v in g.bounds)
    return _flip(affinity.scale(g, s, s, origin=(0, 0))).simplify(0.01)


def globe_discs(d=GLOBE_D):
    """The six-colour globe (the colour mark: flush discs) as [(name, swatch, polygon)], d across, each piece clear of
    those before it so no two print colours lie on one another."""
    import earth as E
    from shapely import affinity
    from shapely.ops import unary_union
    gs = E.disc_shapes(flush=True)
    sil = unary_union([g for g in gs if g is not None])
    s = (d / 2) / max(abs(v) for v in sil.bounds)
    out, taken = [], None
    for name, col, g in zip(E.RING_NAMES, E.RING, gs):
        if g is None:
            continue
        g = _flip(affinity.scale(g, s, s, origin=(0, 0))).buffer(0)
        if taken is not None:
            g = g.difference(taken)
        taken = g if taken is None else taken.union(g)
        out.append((name, col, g.simplify(0.01)))
    return out


def globe_solid(d=GLOBE_D):
    """The one-colour globe (the discs seamed: pieces with the lines between them clear), d across."""
    import earth as E
    from shapely import affinity
    g = E.disc_shapes(flush=False)[0]
    s = (d / 2) / max(abs(v) for v in g.bounds)
    return _flip(affinity.scale(g, s, s, origin=(0, 0))).simplify(0.01)


def _glyphs(text, cap):
    """Each letter of `text` as (shapely geometry in mm, advance in mm), the caps `cap` tall, baseline at y 0."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.recordingPen import RecordingPen
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    f = TTFont(FONT)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    em = cap / (f['OS/2'].sCapHeight / f['head'].unitsPerEm)
    k = em / f['head'].unitsPerEm
    out = []
    for ch in text:
        name = cmap[ord(ch)]
        pen = RecordingPen(); gs[name].draw(pen)
        rings, cur = [], []
        for op, args in pen.value:
            if op == 'moveTo':
                cur = [args[0]]
            elif op == 'lineTo':
                cur.append(args[0])
            elif op == 'qCurveTo':
                pts = list(args)
                if pts[-1] is None:
                    pts = pts[:-1]
                p0 = cur[-1]
                ctrl, end = pts[:-1], pts[-1]
                # implied on-curve points between consecutive off-curve ones
                segs = []
                for i, c in enumerate(ctrl):
                    e = end if i == len(ctrl) - 1 else ((c[0] + ctrl[i + 1][0]) / 2, (c[1] + ctrl[i + 1][1]) / 2)
                    segs.append((c, e))
                for c, e in segs:
                    for t in (0.25, 0.5, 0.75, 1.0):
                        u = 1 - t
                        cur.append((u * u * p0[0] + 2 * u * t * c[0] + t * t * e[0], u * u * p0[1] + 2 * u * t * c[1] + t * t * e[1]))
                    p0 = e
            elif op in ('closePath', 'endPath'):
                if len(cur) > 2:
                    rings.append([(x * k, y * k) for x, y in cur])
                cur = []
        # even-odd: outer rings and holes by containment
        polys = [Polygon(r).buffer(0) for r in rings]
        g = None
        for p in sorted(polys, key=lambda p: -p.area):
            g = p if g is None else (g.difference(p) if g.contains(p) else g.union(p))
        out.append((g if g is not None else Polygon(), gs[name].width * k))
    return out


def arc_text(text, r_base, top=True, cap=None, track=TRACK):
    """`text` round an arc centred at 12 o'clock (top: reading clockwise, the letters' feet on r_base) or at 6 o'clock
    (reading left to right, their feet out on r_base and their tops in)."""
    from shapely import affinity
    from shapely.ops import unary_union
    cap = cap or (WORDS_R[1] - WORDS_R[0])
    gl = _glyphs(text, cap)
    widths = [a + track for _, a in gl]
    total = sum(widths) - track
    r_mid = r_base + (cap / 2 if top else -cap / 2)
    span = total / r_mid
    out, s = [], 0.0
    for (g, a), w in zip(gl, widths):
        c = s + a / 2
        g = affinity.translate(g, -a / 2, 0)                 # the letter centred on its own x
        if top:
            th = math.pi / 2 + span / 2 - c / r_mid
            g = affinity.rotate(g, th - math.pi / 2, origin=(0, 0), use_radians=True)
            g = affinity.translate(g, r_base * math.cos(th), r_base * math.sin(th))
        else:
            th = 3 * math.pi / 2 - span / 2 + c / r_mid
            g = affinity.rotate(g, th + math.pi / 2, origin=(0, 0), use_radians=True)
            g = affinity.translate(g, r_base * math.cos(th), r_base * math.sin(th))
        out.append(g)
        s += w
    return unary_union(out)


def words(top=WORDS_TOP, bottom=WORDS_BOTTOM):
    """The rim's words, as engraved in the front face (read from the front)."""
    from shapely.ops import unary_union
    r0, r1 = WORDS_R
    g = arc_text(top, r0, top=True)
    if bottom:
        g = unary_union([g, arc_text(bottom, r1, top=False)])
    return g


def art_check():
    """The layout's clearances: the globe inside its circle, the words in their band, the two never overlapping."""
    from shapely.geometry import Point
    g, w = globe_lines(), words()
    return dict(globe_r=round(max(Point(0, 0).distance(Point(p)) for p in g.convex_hull.exterior.coords), 2),
                words_r=[round(min(Point(0, 0).distance(Point(p)) for q in w.geoms for p in q.exterior.coords), 2),
                         round(max(Point(0, 0).distance(Point(p)) for q in w.geoms for p in q.exterior.coords), 2)],
                overlap=round(g.intersection(w).area, 4), flat_face_r=D / 2 - ROUND, mass_g=round(mass_g(), 1))


# --- the solids (build123d) -----------------------------------------------------------------------------------------
def _extrude(g, z0, z1):
    """A shapely (multi)polygon extruded from z0 to z1, holes kept."""
    from build123d import Polyline, make_face, extrude, Wire, Face, Compound, Plane, Pos
    import build123d as bd
    solids = []
    for p in getattr(g, 'geoms', [g]):
        if p.is_empty or p.area < 1e-4:
            continue
        outer = Wire.make_polygon([(x, y, 0) for x, y in list(p.exterior.coords)[:-1]], close=True)
        holes = [Wire.make_polygon([(x, y, 0) for x, y in list(h.coords)[:-1]], close=True) for h in p.interiors
                 if len(h.coords) > 3]
        f = Face(outer, holes)
        solids.append(Pos(0, 0, z0) * extrude(f, z1 - z0))
    return Compound(solids)


def body(edge='plain'):
    """The coin: a disc D x T, both edges rounded ROUND; reeded, REEDS grooves across its edge."""
    from build123d import Cylinder, fillet, Axis, Pos, Align
    c = Cylinder(D / 2, T, align=(Align.CENTER, Align.CENTER, Align.MIN))
    c = fillet(c.edges(), ROUND)
    if edge == 'reeded':
        from build123d import Compound
        r = D / 2 + REED_R - REED_DEPTH
        grooves = [Pos(r * math.cos(2 * math.pi * i / REEDS), r * math.sin(2 * math.pi * i / REEDS), -1) *
                   Cylinder(REED_R, T + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)) for i in range(REEDS)]
        c = c - Compound(grooves)
    return c


def disc_blank():
    """What the laser cuts: the plain disc, before its edges are rounded."""
    from build123d import Cylinder, Align
    return Cylinder(D / 2, T, align=(Align.CENTER, Align.CENTER, Align.MIN))


def art_solids():
    """Every face's art as solids in the coin's frame: {name: (solid, finish)}."""
    out = {'globe-engraved': (_extrude(globe_lines(), *ENGRAVE), 'fill'),
           'words': (_extrude(words(), *WORDS_Z), 'frost'),
           'underlay': (_extrude(_underlay(), PRINT[2], PRINT[3]), 'print-white'),
           'globe-cast': (_extrude(globe_solid(), *INLAY), 'inlay')}
    for name, col, g in globe_discs():
        out[f'print-{name.lower()}'] = (_extrude(g, PRINT[0], PRINT[1]), f'print-{name.lower()}')
    return out


def _underlay():
    from shapely.ops import unary_union
    return unary_union([g for _, _, g in globe_discs()]).buffer(-0.08)      # choked under the colour, so no white halo


# --- the request column ---------------------------------------------------------------------------------------------
def column_parts(p=COL):
    """The request column: a clear tube standing in a smoked acrylic base, a brass ring at its top. The base's slot under
    the tube lets the lowest coin out at the front, pushed by a finger through the notch at the back."""
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
    from kit import Part, Machined, Bought, cyl, box
    od, idi, th = p['tube_od'], p['tube_id'], p['tube_h']
    bd_, bh, sh, sw, nw, seat = p['base_d'], p['base_h'], p['slot_h'], p['slot_w'], p['notch_w'], p['seat']
    floor = bh - seat - sh                  # the slot's floor: the lowest coin lies on it
    base = cyl('z', (0, 0), bd_, 0, bh)
    base = base - cyl('z', (0, 0), od + 0.2, bh - seat, bh + 1)               # the tube's socket
    base = base - cyl('z', (0, 0), idi, floor, bh + 1)                      # the coins' well, through to the slot
    base = base - box(-sw / 2, -bd_, floor, sw / 2, 0, floor + sh)          # the slot, out at the front (-y)
    base = base - box(-nw / 2, 0, floor, nw / 2, bd_, floor + sh)           # the finger notch, at the back
    tube = cyl('z', (0, 0), od, bh - seat, bh - seat + th) - cyl('z', (0, 0), idi, bh - seat - 1, bh - seat + th + 1)
    z1 = bh - seat + th
    ring = cyl('z', (0, 0), od + 6, z1 - p['ring_h'] + 2, z1 + 2) - cyl('z', (0, 0), idi, z1 - p['ring_h'], z1 + 3) \
        - (cyl('z', (0, 0), od + 0.2, z1 - p['ring_h'], z1) - cyl('z', (0, 0), idi - 0.01, z1 - p['ring_h'] - 1, z1 + 1))
    return [
        Part('base', base, Machined('cast-acrylic', 'cnc-mill', setup_usd=150.0), finish='smoke-base', group='base',
             notes=['turned and milled from 25 mm Smoke cast acrylic (24 finished), all faces polished; the socket 4 deep '
                    'takes the tube; the slot 6.8 tall lets one coin out at the front; the notch at the back takes a '
                    'finger to push it']),
        Part('tube', tube, Machined('cast-acrylic', 'lathe', setup_usd=60.0), finish='clear', group='tube',
             notes=['cast acrylic tube 50 x 4 wall (42 bore: 1 mm round a 40 coin), water-clear, cut square and its ends '
                    'polished; bonded into the base\'s socket (Acrifix 1R 0192 or Weld-On 16); 210 long holds 33 coins']),
        Part('ring', ring, Machined('brass', 'lathe'), finish='brass', group='tube',
             notes=['brass, satin: a cap ring over the tube\'s top, bonded; the coins drop in through it']),
        Part('feet', None, Bought('column-feet'), render=False),
    ], floor


# --- the laser files ------------------------------------------------------------------------------------------------
def laser_files(out, n_across=None):
    """The shop's files for one coin and for a sheet of them: SVG and DXF, mm, the coin seen from the side each layer is
    lasered from. CUT (the outline), ENGRAVE_BACK (the globe, mirrored: the coin lies front face down for it),
    ENGRAVE_FRONT (the words, as read). And the print file for B (the six colours and the white, mirrored, as the
    printer sees the back face), and the inlay's cut file for C."""
    import ezdxf
    from shapely import affinity
    os.makedirs(out, exist_ok=True)
    gl, wd = globe_lines(), words()
    mirror = lambda g: affinity.scale(g, -1, 1, origin=(0, 0))
    layers = {'CUT': ('circle', D / 2), 'ENGRAVE_BACK': mirror(gl), 'ENGRAVE_FRONT': wd}
    colours = {'CUT': '#FF0000', 'ENGRAVE_BACK': '#0000FF', 'ENGRAVE_FRONT': '#000000'}

    def svg_paths(g, colour, fill=True):
        out_ = []
        for p in getattr(g, 'geoms', [g]):
            if p.is_empty:
                continue
            d = ''
            for ring in [p.exterior] + list(p.interiors):
                cs = list(ring.coords)
                d += 'M' + 'L'.join(f'{x:.3f},{-y:.3f}' for x, y in cs) + 'Z'
            out_.append(f'<path d="{d}" fill="{colour if fill else "none"}" fill-rule="evenodd" '
                        f'stroke="{"none" if fill else colour}" stroke-width="0.01"/>')
        return ''.join(out_)

    def write_one(name, groups, size=D + 4):
        h = size / 2
        body_ = ''
        for lname, g, colour, fill in groups:
            if isinstance(g, tuple):
                body_ += (f'<g id="{lname}"><circle cx="0" cy="0" r="{g[1]}" fill="none" stroke="{colour}" '
                          f'stroke-width="0.01"/></g>')
            else:
                body_ += f'<g id="{lname}">{svg_paths(g, colour, fill)}</g>'
        open(os.path.join(out, name + '.svg'), 'w').write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}mm" height="{size}mm" viewBox="{-h} {-h} {size} {size}">'
            f'{body_}</svg>\n')
        doc = ezdxf.new('R2010', setup=True); doc.units = ezdxf.units.MM
        msp = doc.modelspace()
        for lname, g, colour, fill in groups:
            doc.layers.add(lname)
            if isinstance(g, tuple):
                msp.add_circle((0, 0), g[1], dxfattribs={'layer': lname})
                continue
            for p in getattr(g, 'geoms', [g]):
                for ring in [p.exterior] + list(p.interiors):
                    msp.add_lwpolyline(list(ring.coords), close=True, dxfattribs={'layer': lname})
                if fill and lname.startswith(('ENGRAVE', 'PRINT', 'INLAY')):
                    hatch = msp.add_hatch(dxfattribs={'layer': lname})
                    hatch.paths.add_polyline_path(list(p.exterior.coords), is_closed=True, flags=1)
                    for ring in p.interiors:
                        hatch.paths.add_polyline_path(list(ring.coords), is_closed=True, flags=16)
        doc.saveas(os.path.join(out, name + '.dxf'))
        return [os.path.join(out, name + e) for e in ('.svg', '.dxf')]

    made = []
    # A, the coin: the cut, the back's globe (mirrored), the front's words; and each side's file on its own, as run
    made += write_one('coin-A-all-layers', [('CUT', layers['CUT'], '#FF0000', False),
                                            ('ENGRAVE_BACK', layers['ENGRAVE_BACK'], '#0000FF', True),
                                            ('ENGRAVE_FRONT', layers['ENGRAVE_FRONT'], '#000000', True)])
    made += write_one('coin-A-1-cut', [('CUT', layers['CUT'], '#FF0000', False)])
    made += write_one('coin-A-2-back-globe-MIRRORED', [('REF_CUT', layers['CUT'], '#FF0000', False),
                                                        ('ENGRAVE_BACK', layers['ENGRAVE_BACK'], '#0000FF', True)])
    made += write_one('coin-A-3-front-words', [('REF_CUT', layers['CUT'], '#FF0000', False),
                                               ('ENGRAVE_FRONT', layers['ENGRAVE_FRONT'], '#000000', True)])
    # B, the print on the back (mirrored), colour and the white underlay as separate channels
    groups = [('REF_CUT', layers['CUT'], '#FF0000', False)]
    for name, col, g in globe_discs():
        groups.append((f'PRINT_{name.upper()}', mirror(g), col, True))
    groups.append(('PRINT_WHITE_UNDERLAY', mirror(_underlay()), '#DDDDDD', True))
    made += write_one('coin-B-back-print-MIRRORED', groups)
    # C, the inlay: cut from 1 mm tinted sheet (as seen from the front)
    made += write_one('coin-C-inlay-cut', [('INLAY_CUT', globe_solid(), '#0000FF', False)])
    made += nest(out)[0]
    return made


def nest(out, sheet=(600.0, 400.0), gap=3.0, margin=10.0):
    """A sheet of coins for the laser bed (600 x 400, a common bed and a half-sheet cut from 1220 x 610): the cuts and
    each face's engraving on registered layers, with the jig's datum. The coins are cut first; the sheet's skeleton is
    left in the bed as the jig, the coins flipped back into their holes for the back's globe (mirrored)."""
    import ezdxf
    from shapely import affinity
    pitch = D + gap
    nx = int((sheet[0] - 2 * margin + gap) // pitch)
    ny = int((sheet[1] - 2 * margin + gap) // pitch)
    gl = affinity.scale(globe_lines(), -1, 1, origin=(0, 0))
    wd = words()
    doc = ezdxf.new('R2010', setup=True); doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    for l in ('SHEET', 'CUT', 'ENGRAVE_FRONT', 'ENGRAVE_BACK_MIRRORED'):
        doc.layers.add(l)
    msp.add_lwpolyline([(0, 0), (sheet[0], 0), (sheet[0], sheet[1]), (0, sheet[1])], close=True, dxfattribs={'layer': 'SHEET'})
    svg = [f'<rect x="0" y="0" width="{sheet[0]}" height="{sheet[1]}" fill="none" stroke="#999" stroke-width="0.3"/>']
    for i in range(nx):
        for j in range(ny):
            cx, cy = margin + D / 2 + i * pitch, margin + D / 2 + j * pitch
            msp.add_circle((cx, cy), D / 2, dxfattribs={'layer': 'CUT'})
            svg.append(f'<circle cx="{cx:.2f}" cy="{sheet[1] - cy:.2f}" r="{D / 2}" fill="none" stroke="#F00" stroke-width="0.2"/>')
            for lname, g in (('ENGRAVE_FRONT', wd), ('ENGRAVE_BACK_MIRRORED', gl)):
                for p in getattr(g, 'geoms', [g]):
                    for ring in [p.exterior] + list(p.interiors):
                        msp.add_lwpolyline([(x + cx, y + cy) for x, y in ring.coords], close=True, dxfattribs={'layer': lname})
            for p in getattr(gl, 'geoms', [gl]):
                d = ''.join('M' + 'L'.join(f'{x + cx:.2f},{sheet[1] - (y + cy):.2f}' for x, y in r.coords) + 'Z'
                            for r in [p.exterior] + list(p.interiors))
                svg.append(f'<path d="{d}" fill="#00F" fill-rule="evenodd"/>')
    doc.saveas(os.path.join(out, 'nest-600x400.dxf'))
    open(os.path.join(out, 'nest-600x400.svg'), 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{sheet[0]}mm" height="{sheet[1]}mm" '
        f'viewBox="0 0 {sheet[0]} {sheet[1]}">{"".join(svg)}</svg>\n')
    return [os.path.join(out, 'nest-600x400' + e) for e in ('.dxf', '.svg')], nx * ny


# --- the cost of a coin (estimates, not quotes) ---------------------------------------------------------------------
# Shop rates fall with the run: a laser or CNC hour at about $120 for 500 coins, $100 for 1,000 and $80 for 5,000
# (2026, US job shops; a quote replaces them). The sheet at the kit's rate for cast acrylic ($19 a m2 a mm), nested 104
# to a 600 x 400; a one-off setup (CAM, the laser jig, the CNC's vacuum fixture, a first article) spread over the run;
# 5 % scrap on the whole.
RUNS = (500, 1000, 5000)
RATE = {500: 120.0, 1000: 100.0, 5000: 80.0}
SECONDS = dict(laser=12 + 20 + 10, edge=40, edge_plain=25)
FILL = {500: 0.45, 1000: 0.35, 5000: 0.25}   # the engravings paint-filled (globe black, words white) through the masking:
                                             # flooded, scraped, dried, before the peel
SETUP_USD = 600.0
FACE_EXTRA = {'engraved': (0.0, 0.0), 'printed': ({500: 0.9, 1000: 0.7, 5000: 0.45}, 200.0),
              'cast': ({500: 11.0, 1000: 8.5, 5000: 6.0}, 900.0)}       # B: UV print, white and seal; C: an embedment


def costs(face='engraved', edge='reeded'):
    """{run: {line: usd a coin}} for a run of each size in RUNS."""
    sheet = 0.6 * 0.4 * 19.0 * T / 104
    out = {}
    for n in RUNS:
        r = RATE[n] / 3600
        extra, setup_x = FACE_EXTRA[face]
        line = {'sheet': sheet, 'laser': SECONDS['laser'] * r,
                'edge': SECONDS['edge' if edge == 'reeded' else 'edge_plain'] * r,
                'paint fill': FILL[n] if face == 'engraved' else 0.0,
                'polish': {500: 0.40, 1000: 0.30, 5000: 0.20}[n], 'check and bag': 0.15,
                'setup': (SETUP_USD + setup_x) / n}
        if extra:
            line['face'] = extra[n]
        line['scrap 5 %'] = 0.05 * sum(line.values())
        line['total'] = sum(line.values())
        out[n] = {k: round(v, 2) for k, v in line.items()}
    return out


def costs_md():
    L = []
    for face, edge in (('engraved', 'reeded'), ('engraved', 'plain'), ('printed', 'reeded'), ('cast', 'reeded')):
        c = costs(face, edge)
        L.append(f"| {face}, {edge} | " + ' | '.join(f"${c[n]['total']:.2f}" for n in RUNS) + ' |')
    pick = costs()
    rows = [k for k in pick[1000] if k != 'total']
    detail = ['| a coin (the pick), USD | ' + ' | '.join(f'{n:,}' for n in RUNS) + ' |', '|---|---|---|---|']
    detail += [f'| {k} | ' + ' | '.join(f'{pick[n][k]:.2f}' for n in RUNS) + ' |' for k in rows]
    detail += ['| **total** | ' + ' | '.join(f"**{pick[n]['total']:.2f}**" for n in RUNS) + ' |']
    head = ['| face, edge | ' + ' | '.join(f'{n:,} coins' for n in RUNS) + ' |', '|---|---|---|---|']
    return '\n'.join(detail) + '\n\n' + '\n'.join(head + L)


# --- the render materials and flavours -------------------------------------------------------------------------------
def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _srgb(v):
    v = max(0.0, min(1.0, v))
    return 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055


def tint_deep(swatch, passes=2.0, k=1.0):
    """The coin's `deep` (the colour after RADIUS of its acrylic) so that light crossing it `passes` times (down to the
    paper and back) comes out near the swatch: each channel the swatch's linear value to the 1/passes. `k` scales the
    density (above 1, denser)."""
    rgb = [int(swatch[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(_srgb(max(_lin(c), 1e-4) ** (k / passes)) * 255):02X}' for c in rgb)


# Smoke cast lighter than its swatch (a transparent grey, as Perspex 9T20 is beside the speakers' black): at the
# swatch's density the coin rendered L 4 on paper and its globe was lost (round 33's tint check)
TINT_K = {'Ember': 1.0, 'Dust': 1.0, 'Acid': 1.0, 'Poison': 1.0, 'Ice': 1.0, 'Haze': 1.0, 'Fog': 1.0, 'Smoke': 0.55}
FILL_WHITE = ('Smoke',)                # black lines would vanish in Smoke: its globe is filled white
RADIUS = 0.006                         # the tint's `deep` is the colour after 6 mm, the coin's thickness


def variants():
    import earth as E
    import common as C
    out = {}
    for key, name, *_ in C.COLOURS:
        sw = E._C[name]
        if name == 'Fog':
            deep = '#F2F7F7'
        else:
            deep = tint_deep(sw, k=TINT_K[name])
        out[key] = {'deep': deep, 'inlay': tint_deep(sw, passes=1.0, k=TINT_K[name] * 0.9), 'swatch': sw}
        if name in FILL_WHITE:
            out[key]['materials'] = {'fill': {'color': '#EEEEEA', 'roughness': 0.8, 'specular': 0.2}}
    return out


def materials():
    import earth as E
    m = {
        'coin': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$deep', 'radius': RADIUS, 'roughness': 0.03},
        # the words' engraving in the front face, paint-filled white (seen directly, not through the tint)
        'frost': {'preset': 'satin_paint', 'color': '#EEEEEA', 'roughness': 0.8, 'specular': 0.2},
        # the globe's engraving in the back, paint-filled black (the lead's test after the concept sheet: frost alone or a
        # white fill, seen through the tint against white paper, all but vanished; black reads in every tint as the
        # brand's black stroke mark, like the leading in stained glass). Smoke's is white (FILL_WHITE)
        'fill': {'preset': 'satin_paint', 'color': '#1C1A18', 'roughness': 0.5, 'specular': 0.3},
        'inlay': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '$inlay', 'radius': 0.001, 'roughness': 0.03,
                  'ior': 1.02},
        'print-white': {'preset': 'satin_paint', 'color': '#F4F3EF', 'roughness': 0.5, 'specular': 0.2},
        'clear': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#EEF4F4', 'radius': 0.05, 'roughness': 0.02},
        'smoke-base': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#6E6B72', 'radius': 0.012, 'roughness': 0.03},
        'brass': {'preset': 'metal', 'color': '#B8945A', 'roughness': 0.3},
    }
    for name, col in zip(E.RING_NAMES, E.RING):
        m[f'print-{name.lower()}'] = {'preset': 'satin_paint', 'color': col, 'roughness': 0.5, 'specular': 0.2}
    return m


# --- the study model: every face and edge in one GLB, which the kit piece (studio/engine/kit_ext/earf_coin.py) picks
# from by name ------------------------------------------------------------------------------------------------------
STUDY = os.path.join(HERE, 'out-coin-study')
COLUMN = os.path.join(HERE, 'out-coin-column')


def study_parts():
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
    from kit import Part, Bought
    ps = [Part(f'body-{e}', body(e), Bought('coin'), finish='coin') for e in EDGES]
    for n, (s, f) in art_solids().items():
        ps.append(Part(n, s, Bought('coin'), finish=f))
    return ps


def build_study():
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
    import kit as K
    import render as fk_render
    ps = study_parts()
    prod = K.Product('earf-coin-study', 'EARFcoin study', 'every face and edge', params={}, parts=lambda P: ps,
                     materials=materials(), variants=variants(), origin=(0, 0, 0))
    fk_render.write(prod, ps, STUDY, engine_file=os.path.join(STUDY, 'earf-coin-study.json'), proof=False)
    cps, floor = column_parts()
    prod = K.Product('earf-coin-column', 'EARFcoin request column', 'the request column', params={}, parts=lambda P: cps,
                     materials=materials(), variants=variants(), origin=(0, 0, 0))
    fk_render.write(prod, cps, COLUMN, engine_file=os.path.join(COLUMN, 'earf-coin-column.json'), proof=False)
    return floor


if __name__ == '__main__':
    import json
    print(json.dumps(art_check()))
    if '--costs' in sys.argv:
        print(costs_md())
    elif '--art' not in sys.argv:
        print('column floor', build_study())
        print('laser files:', len(laser_files(os.path.join(HERE, 'out-earf-coin', 'laser'))))
