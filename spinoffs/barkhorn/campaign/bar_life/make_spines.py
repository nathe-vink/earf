"""The record wall's spines (the owner, 13 Nov: "the records are obviously fake"; the coordinator's 20:19 brief): an atlas
of invented LP spines, each a column 16 px across and 1260 long (0.25 mm a pixel over a 315 mm jacket), read bottom to
top as a spine is. No real artist, title, label, mark or artwork: the names are made from syllables, the catalogue
numbers from letters and digits.

The shares follow the brief: white or off-white 30 %, yellowed cream 15 %, black 22 %, kraft 5 %, printed colours
28 % (real ink colours, medium to strong); thin 12-inch singles plain black or white, no type. Type over 40 to 85 % of
the length at any place, dark on light or light on dark, a small block at one end; the top and bottom 10 to 20 mm
whitened and soft on many; a split now and then.

    python3 spinoffs/barkhorn/campaign/bar_life/make_spines.py   ->  bar_life/tex/spines.jpg, tex/spines.json
"""
import json, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tex')
WPX, LPX = 16, 1260                       # a spine's column: across, along (0.25 mm a pixel)
FONTS = ['/usr/share/fonts/opentype/inter/Inter-Bold.otf', '/usr/share/fonts/opentype/inter/Inter-Medium.otf',
         '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf',
         '/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
         '/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf', '/usr/share/fonts/truetype/freefont/FreeSerifBoldItalic.ttf']
FONTS = [f for f in FONTS if os.path.exists(f)]

# (category, share, grounds): the brief's shares; 'thin' are the singles, drawn without type
CATS = [('white', 0.30, ['#F2F0EA', '#ECE9E1', '#E6E3DA', '#F4F2EE', '#E9E6DF']),
        ('cream', 0.15, ['#E3D6B4', '#D9C9A0', '#E8DDBE', '#D4C29A', '#DDD0AC']),
        ('black', 0.22, ['#141414', '#1A1A1A', '#101010', '#1E1D1C', '#181716']),
        ('kraft', 0.05, ['#A8865E', '#9C7A52', '#B39069', '#8F6F4A']),
        ('colour', 0.28, ['#B3202A', '#1F4E9C', '#E2A400', '#1E7A46', '#D9531E', '#5B2A86', '#00808A', '#7A1F2B',
                          '#22356F', '#C2185B', '#3E6B2F', '#A0522D', '#0E6E9E', '#8C1C13', '#F0C419', '#2B2B6E'])]
INK_DARK = ['#141414', '#1C1C1C', '#2A2420', '#3A1E1A']
INK_LIGHT = ['#F4F2EC', '#EDE6D4', '#E8D9A8']

SYL = ['ka', 'ro', 'mi', 'len', 'dor', 'vas', 'tel', 'ion', 'bra', 'mu', 'sen', 'har', 'lo', 'quin', 'ze', 'pa', 'nor',
       'vel', 'ash', 'tor', 'bel', 'cri', 'fon', 'gal', 'ri', 'sto', 'wen', 'ul', 'mar', 'den', 'pho', 'lis', 'tam', 'oro']
WORDS = ['Night', 'Harbour', 'Blue', 'Hours', 'Quiet', 'Fire', 'Garden', 'Motion', 'Paper', 'Moon', 'Echo', 'Station',
         'Low', 'Light', 'Rooms', 'Salt', 'River', 'Glass', 'Signal', 'North', 'Velvet', 'Dust', 'Ember', 'Weather',
         'Distance', 'Small', 'Hands', 'Slow', 'Static', 'Gold', 'Window', 'Field', 'Summer', 'Tape', 'Second', 'Side']


def name(rnd):
    w = lambda: ''.join(rnd.choice(SYL) for _ in range(rnd.choice([2, 2, 3]))).capitalize()
    return rnd.choice([lambda: f'{w()} {w()}', lambda: f'The {w()}s', lambda: w(), lambda: f'{w()} & {w()}',
                       lambda: f'{w()} {w()} Trio', lambda: f'{w()} Quartet'])()


def title(rnd):
    return ' '.join(rnd.sample(WORDS, rnd.choice([1, 2, 2, 3])))


def catno(rnd):
    return f'{"".join(rnd.choice("ABCDEFGHJKLMNPRSTVW") for _ in range(rnd.choice([2, 3])))} {rnd.randint(100, 9999)}'


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def text_strip(rnd, s, font, fill, ground, height):
    """`s` set along the spine: drawn horizontally into a strip `height` px tall (the spine's width), then turned."""
    f = ImageFont.truetype(font, size=max(6, int(height * rnd.uniform(0.55, 0.72))))
    w = int(f.getlength(s)) + 4
    im = Image.new('RGB', (w, height), ground); d = ImageDraw.Draw(im)
    d.text((2, height / 2), s, font=f, fill=fill, anchor='lm')
    return im


def spine(k, cat, grounds, rnd):
    g = rnd.choice(grounds)
    gr = hexrgb(g)
    im = Image.new('RGB', (WPX, LPX), g)
    light = sum(gr) / 3 > 120
    if cat == 'colour':
        light = sum(gr) / 3 > 150
    thin = cat == 'thin'
    if not thin:
        ink = rnd.choice(INK_DARK if light else INK_LIGHT)
        cover = rnd.uniform(0.40, 0.85)                     # how much of the length the type runs over
        parts = [name(rnd).upper(), '·', title(rnd)] if rnd.random() < 0.7 else [name(rnd), '—', title(rnd).upper()]
        s = '  '.join(parts)
        font = rnd.choice(FONTS)
        strip = text_strip(rnd, s, font, ink, g, WPX)
        L = int(LPX * cover)
        if strip.width > L:                                 # too long: squeeze it to the length it may run over
            strip = strip.resize((L, WPX), Image.LANCZOS)
        rest = LPX - strip.width - 80
        start = rnd.randint(60, max(61, rest)) if rnd.random() < 0.6 else rnd.randint(60, max(61, min(rest, 220)))
        rot = 90 if rnd.random() < 0.6 else -90                # read bottom to top, or top to bottom
        im.paste(strip.rotate(rot, expand=True), (0, LPX - start - strip.width))
        # the small block at one end: a catalogue number, or a little logo square
        end_bottom = rnd.random() < 0.5
        if rnd.random() < 0.6:
            cs = text_strip(rnd, catno(rnd), rnd.choice(FONTS), ink, g, WPX)
            cs = cs.resize((min(cs.width, 140), WPX), Image.LANCZOS)
            y = LPX - 18 - cs.width if end_bottom else 18
            if not (LPX - start - strip.width - 8 < y + cs.width and y < LPX - start + 8):
                im.paste(cs.rotate(rot, expand=True), (0, y))
        else:
            d = ImageDraw.Draw(im); b = rnd.randint(9, 13); y = LPX - 20 - b if end_bottom else 20
            if rnd.random() < 0.5:
                d.rectangle([(WPX - b) // 2, y, (WPX + b) // 2, y + b], fill=ink)
            else:
                d.ellipse([(WPX - b) // 2, y, (WPX + b) // 2, y + b], fill=ink)
        if rnd.random() < 0.25:                             # a thin rule across near one end
            d = ImageDraw.Draw(im); y = rnd.choice([rnd.randint(40, 90), LPX - rnd.randint(40, 90)])
            d.line([(0, y), (WPX, y)], fill=ink, width=2)
    # the card's grain
    px = im.load()
    for y in range(LPX):
        n = rnd.uniform(-4, 4)
        for x in range(WPX):
            r, gg, b = px[x, y]
            v = n + rnd.uniform(-3, 3)
            px[x, y] = (int(min(255, max(0, r + v))), int(min(255, max(0, gg + v))), int(min(255, max(0, b + v))))
    # wear: the ends whitened and soft on many (more on dark grounds, where it shows); a split now and then
    if rnd.random() < (0.75 if not light else 0.45):
        for end in (0, 1):
            if rnd.random() < 0.85:
                L = rnd.randint(40, 80)
                amt = rnd.uniform(0.25, 0.6) if not light else rnd.uniform(0.1, 0.25)
                for y in range(L):
                    yy = y if end == 0 else LPX - 1 - y
                    f = amt * (1 - y / L) ** 1.6
                    for x in range(WPX):
                        if rnd.random() < 0.85:
                            r, gg, b = px[x, yy]; t = f * rnd.uniform(0.5, 1.2)
                            px[x, yy] = (int(r + (238 - r) * t), int(gg + (232 - gg) * t), int(b + (220 - b) * t))
    if rnd.random() < 0.05:
        d = ImageDraw.Draw(im); y0 = rnd.choice([rnd.randint(0, 30), LPX - rnd.randint(120, 300)]); L = rnd.randint(60, 260)
        x = rnd.choice([1, WPX - 2])
        d.line([(x, y0), (x, y0 + L)], fill=(90, 82, 72) if light else (150, 146, 138), width=1)
    return im.filter(ImageFilter.GaussianBlur(0.35))


def main():
    os.makedirs(OUT, exist_ok=True)
    rnd = random.Random(1311)
    per = {'white': 110, 'cream': 60, 'black': 80, 'kraft': 24, 'colour': 110, 'thin': 24}
    atlas = Image.new('RGB', (WPX * sum(per.values()), LPX))
    index = {}; col = 0
    grounds = {c: g for c, _, g in CATS}
    grounds['thin'] = ['#141414', '#151515', '#EFEDE7', '#E9E7E0']
    for cat in ('white', 'cream', 'black', 'kraft', 'colour', 'thin'):
        index[cat] = []
        for j in range(per[cat]):
            atlas.paste(spine(col, cat, grounds[cat], rnd), (col * WPX, 0))
            index[cat].append(col); col += 1
    atlas.save(os.path.join(OUT, 'spines.jpg'), quality=93)
    json.dump({'wpx': WPX, 'lpx': LPX, 'n': col, 'index': index,
               'shares': {c: s for c, s, _ in CATS}}, open(os.path.join(OUT, 'spines.json'), 'w'), indent=1)
    print('spines', col, atlas.size, os.path.getsize(os.path.join(OUT, 'spines.jpg')) // 1024, 'KB')


if __name__ == '__main__':
    main()
