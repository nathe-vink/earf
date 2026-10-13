"""The barkhorn stickers: one die-cut sticker for each speaker in the look book, all drawn from one grammar.

The grammar is the speaker reduced to its parts, in proportion: the horn (a rounded rectangle, 626 x 361 mm), its
throat (a dark dot), the cabinet (560 x 880), the cover over the woofer (a disc 437 across, its centre 45.7 % down)
and the two ports (100 mm squares in the bottom corners). A style changes three things and nothing else: the
cabinet's surface (a pattern code: bands, dashes, lines, rings, patches, veins, or a flat tint for acrylic), the
horn's fill (the same pattern, lightened, where the pattern is cast into it; else its tint), and the cover's colour.
Every sticker sits on a white die-cut edge with a hairline outline, so it reads on any ground.

    python3 spinoffs/barkhorn/stickers.py        writes stickers/<key>.svg and stickers/sheet.html
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'stickers')

# the parts, in sticker units (1 unit = 4.89 mm), on a 160 x 294 sticker
HORN = dict(x=16, y=16, w=128, h=74, r=18)
THROAT = dict(cx=80, cy=53, r=8)
CAB = dict(x=23, y=98, w=114, h=180)
DISC = dict(cx=80, cy=180, r=44.5)
PORTS = [(34, 245), (106, 245)]
PORT = 20
EDGE = 9                                        # the die-cut's white margin round the parts
INK = '#1A1817'                                 # the throat and the ports

# the covers, as in product.py
OAT, GRAPHITE, CHARCOAL, PEWTER, MIST, STONE = '#CFC8BA', '#4B4844', '#2E2C2A', '#7A807E', '#C8CACA', '#8E8981'


def light(hx, t=0.45):
    """A colour moved `t` of the way to white (a pattern cast into clear resin reads lighter than the sheet)."""
    r, g, b = (int(hx[i:i + 2], 16) for i in (1, 3, 5))
    return '#%02X%02X%02X' % tuple(round(c + (255 - c) * t) for c in (r, g, b))


# --- surfaces: each returns SVG drawn in a box of w x h at the origin (clipped to the part by the caller) ----------
def flat(fill, frame=None):
    def draw(w, h, lift=0.0):
        s = f'<rect width="{w}" height="{h}" fill="{light(fill, lift)}"/>'
        if frame:                                # acrylic: its edges and a brace, darker, seen through the walls
            s += (f'<rect x="3" y="3" width="{w - 6}" height="{h - 6}" fill="none" stroke="{light(frame, lift)}" stroke-width="3"/>'
                  f'<rect x="3" y="{h * 0.17:.1f}" width="{w - 6}" height="3" fill="{light(frame, lift)}"/>'
                  f'<rect x="3" y="{h * 0.8:.1f}" width="{w - 6}" height="3" fill="{light(frame, lift)}"/>') if h > 100 else (
                  f'<rect x="2.5" y="2.5" width="{w - 5}" height="{h - 5}" rx="14" fill="none" stroke="{light(frame, lift)}" stroke-width="2.5"/>')
        return s
    return draw


def bands(stops):
    """Vertical bands, [(colour, share), ...] across the width."""
    def draw(w, h, lift=0.0):
        tot, x, s = sum(f for _, f in stops), 0.0, ''
        for hx, f in stops:
            bw = w * f / tot
            s += f'<rect x="{x:.1f}" width="{bw + 0.4:.1f}" height="{h}" fill="{light(hx, lift)}"/>'
            x += bw
        return s
    return draw


def marks(base, ink, items, kind='dash'):
    """Short marks on a ground: dashes (x, y, length) across, or lines (x, width) up the whole height."""
    def draw(w, h, lift=0.0):
        s = f'<rect width="{w}" height="{h}" fill="{light(base, lift)}"/>'
        for it in items:
            if kind == 'dash':
                x, y, ln = it
                s += f'<rect x="{x * w / 114:.1f}" y="{y * h / 180:.1f}" width="{ln * w / 114:.1f}" height="5" rx="2.5" fill="{light(ink, lift)}"/>'
            elif kind == 'line':
                x, lw = it
                s += f'<rect x="{x * w / 114:.1f}" width="{lw}" height="{h}" fill="{light(ink, lift)}"/>'
            elif kind == 'ring':
                y, rh = it
                s += f'<rect y="{y * h / 180:.1f}" width="{w}" height="{rh}" fill="{light(ink, lift)}"/>'
        return s
    return draw


def layered(*draws):
    def draw(w, h, lift=0.0):
        return ''.join(d(w, h, lift) for d in draws)
    return draw


def dots(ink, items, size=(7, 2.6)):
    """Small marks over another surface (lenticels, flecks), (x, y) in cabinet units."""
    def draw(w, h, lift=0.0):
        return ''.join(f'<rect x="{x * w / 114:.1f}" y="{y * h / 180:.1f}" width="{size[0]}" height="{size[1]}" rx="1.3" fill="{light(ink, lift)}"/>'
                       for x, y in items)
    return draw


def shapes(base, items):
    """Patches on a ground: [(colour, path in cabinet units), ...] (scaled to the part)."""
    def draw(w, h, lift=0.0):
        s = f'<rect width="{w}" height="{h}" fill="{light(base, lift)}"/>'
        for hx, d in items:
            s += f'<path d="{d}" transform="scale({w / 114:.4f} {h / 180:.4f})" fill="{light(hx, lift)}"/>'
        return s
    return draw


def veins(base, items):
    """Strokes on a ground: [(colour, width, path in cabinet units), ...]."""
    def draw(w, h, lift=0.0):
        s = f'<rect width="{w}" height="{h}" fill="{light(base, lift)}"/>'
        for hx, sw, d in items:
            s += (f'<path d="{d}" transform="scale({w / 114:.4f} {h / 180:.4f})" fill="none" stroke="{light(hx, lift)}" '
                  f'stroke-width="{sw}" stroke-linecap="round" vector-effect="non-scaling-stroke"/>')
        return s
    return draw


# --- the twelve -------------------------------------------------------------------------------------------------
BIRCH_DASHES = [(10, 14, 26), (66, 22, 18), (92, 44, 14), (6, 60, 14), (8, 140, 20), (84, 132, 20), (40, 164, 22)]
EUCALYPTUS = bands([('#4E6B2C', 26), ('#C2963A', 20), ('#C25E2C', 28), ('#8A877C', 22), ('#D2B77A', 18)])
BIRCH = marks('#EEEAE0', '#22201C', BIRCH_DASHES)
MANZANITA = shapes('#6A2117', [('#9AAA55', 'M-2 104 C14 98 34 106 38 124 C42 142 32 152 38 170 C40 180 20 184 -2 182 Z'),
                               ('#C9743E', 'M84 12 C96 4 112 10 114 24 C116 38 100 46 90 42 C80 38 76 22 84 12 Z')])
STRIPED = marks('#ECEFE8', '#5A7536', [(12, 3.2), (30, 3.2), (48, 3.2), (66, 3.2), (84, 3.2), (100, 3.2)], kind='line')
PHOENIX = layered(marks('#E8935A', '#B4432C', [(18, 3.6), (46, 3.6), (74, 3.6), (100, 3.6)], kind='line'),
                  dots('#3C2E2A', [(28, 22), (84, 150), (54, 166)], size=(9, 3.6)))
CHERRY = layered(marks('#6E2418', '#3A2C26', [(24, 10), (140, 10), (162, 8)], kind='ring'),
                 dots('#D88A3E', [(16, 28), (78, 143), (40, 164)], size=(12, 3.6)))
WHITE_VEINS = marks('#7E8A44', '#E8ECE2', [(38, 3), (84, 3)], kind='line')
REDVEIN = layered(marks('#7E8A44', '#C4673C', [(18, 3.6), (60, 3.6), (100, 3.6)], kind='line'),
                  lambda w, h, lift=0.0: WHITE_VEINS(w, h, lift).split('/>', 1)[1])
COBALT = veins('#F3F4F1', [('#1D3C9A', 5, 'M-6 44 C26 20 50 78 86 46 C104 30 118 54 122 32'),
                           ('#1D3C9A', 3, 'M-6 150 C24 128 62 182 120 140')])

LOOKS = [
    # key, number, name, cabinet surface, horn (surface, lightened by) or tint, cover
    ('eucalyptus', '01', 'Eucalyptus', EUCALYPTUS, (EUCALYPTUS, 0.4), GRAPHITE),
    ('birch', '02', 'Birch', BIRCH, (BIRCH, 0.35), OAT),
    ('autumn', '03', 'Autumn Birch', BIRCH, (flat('#F2B705'), 0.0), OAT),
    ('manzanita', '04', 'Manzanita', MANZANITA, (MANZANITA, 0.35), GRAPHITE),
    ('striped', '05', 'Striped Maple', STRIPED, (STRIPED, 0.3), MIST),
    ('phoenix', '06', 'Phoenix Maple', PHOENIX, (PHOENIX, 0.35), STONE),
    ('cherry', '07', 'Tibetan Cherry', CHERRY, (CHERRY, 0.35), GRAPHITE),
    ('redvein', '08', 'Redvein Maple', REDVEIN, (REDVEIN, 0.35), STONE),
    ('green', '09', 'Green Acrylic', flat('#35633A', '#22432A'), (flat('#4E7D42', '#35633A'), 0.0), GRAPHITE),
    ('smoke', '10', 'Smoke', flat('#2B2A2F', '#18171B'), (flat('#4A4950', '#2B2A2F'), 0.0), CHARCOAL),
    ('ice', '11', 'Frosted Ice', flat('#C5CFD5', '#AAB6BD'), (flat('#F1F4F5', '#AAB6BD'), 0.0), PEWTER),
    ('cobalt', '12', 'Cobalt Marble', COBALT, (COBALT, 0.0), MIST),
]


def sticker(key, surface, horn, cover):
    """One sticker's SVG."""
    hs, lift = horn
    H, C = HORN, CAB
    e = EDGE
    cut = (f'<rect x="{H["x"] - e}" y="{H["y"] - e}" width="{H["w"] + 2 * e}" height="{H["h"] + 2 * e}" rx="{H["r"] + e}"/>'
           f'<rect x="{C["x"] - e}" y="{C["y"] - e}" width="{C["w"] + 2 * e}" height="{C["h"] + 2 * e}" rx="5"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="160" height="294" viewBox="0 0 160 294" role="img" aria-label="barkhorn {key}">'
            f'<defs><clipPath id="h-{key}"><rect x="{H["x"]}" y="{H["y"]}" width="{H["w"]}" height="{H["h"]}" rx="{H["r"]}"/></clipPath>'
            f'<clipPath id="c-{key}"><rect x="{C["x"]}" y="{C["y"]}" width="{C["w"]}" height="{C["h"]}"/></clipPath></defs>'
            # the die-cut: a hairline round the white margin
            f'<g fill="none" stroke="#000000" stroke-opacity="0.16" stroke-width="2">{cut}</g><g fill="#FFFFFF">{cut}</g>'
            f'<g clip-path="url(#c-{key})"><g transform="translate({C["x"]} {C["y"]})">{surface(C["w"], C["h"])}</g></g>'
            f'<g clip-path="url(#h-{key})"><g transform="translate({H["x"]} {H["y"]})">{hs(H["w"], H["h"], lift)}</g></g>'
            f'<circle cx="{THROAT["cx"]}" cy="{THROAT["cy"]}" r="{THROAT["r"]}" fill="{INK}"/>'
            f'<circle cx="{DISC["cx"]}" cy="{DISC["cy"]}" r="{DISC["r"]}" fill="{cover}" stroke="#FFFFFF" stroke-opacity="0.14" stroke-width="1.5"/>'
            + ''.join(f'<rect x="{x}" y="{y}" width="{PORT}" height="{PORT}" fill="{INK}"/>' for x, y in PORTS)
            + '</svg>')


def main():
    os.makedirs(OUT, exist_ok=True)
    cells = []
    for key, num, name, surface, horn, cover in LOOKS:
        svg = sticker(key, surface, horn, cover)
        open(os.path.join(OUT, f'{key}.svg'), 'w').write(svg + '\n')
        cells.append(f'<figure>{svg}<figcaption><b>{num}</b> {name}</figcaption></figure>')
    open(os.path.join(OUT, 'sheet.html'), 'w').write(
        '<!doctype html><meta charset="utf-8"><title>barkhorn stickers</title><style>'
        'body{margin:0;padding:48px;background:#1C1B19;font:14px/1.4 "IBM Plex Mono",monospace;color:#B9B4AA}'
        '.grid{display:grid;grid-template-columns:repeat(6,160px);gap:40px 48px}figure{margin:0}'
        'figcaption{margin-top:10px;letter-spacing:.06em;text-transform:uppercase}b{color:#F1EDE4;font-weight:500}'
        '</style><div class="grid">' + ''.join(cells) + '</div>\n')
    print(f'{len(LOOKS)} stickers in {os.path.relpath(OUT)}')


if __name__ == '__main__':
    main()
