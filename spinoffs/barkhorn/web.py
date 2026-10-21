"""earf.world, built from the repository (round 31: round 30's draft and its hosting moved here from the working
notes, so any session can rebuild the site).

One page, two views by its address: the home page (#top, and its sections #turn, #atmosphere, #room, #spec, #contact)
and a speaker's page (#speaker-ember ... #speaker-smoke, by name; the colour keys still answer). It is written as it is hosted: a whole document, with what a
browser and a link preview need, a bar saying it is a preview, and kept out of search engines until launch (a meta
tag, an X-Robots-Tag header on every response and a robots.txt that disallows everything), into site/ for Vercel,
which deploys it on every push to main.

- Home: the hero (the eight on an arc, covers off, each a link to its page); the horns, turning as the page scrolls
  and by hand; the eight cards, covers off first, each with its acrylic icon; the room; the particulars; enquiries.
- A speaker's page: a gallery of eight views, its colour picked from the acrylic coins, its particulars, what goes
  with its colour (round 25's idea, sketches for now) and the other seven.
- The header's globe keeps turning, never under reduced motion. The page opens on it: the acrylic globe large in the
  middle of a plain ground, turning, which flies and shrinks into its place at the top left as the ground is drawn in
  behind it, and goes on turning there (the owner, 2026-10-19). The opening follows the system's setting: paper and the
  paper render by day, near-black and the night render (its glowing edges) when the system is dark; the page beneath
  stays paper either way, one theme by choice.

The owner, of round 30's words: "the sites copy needs a lot of work. It's a lot of AI slop, using my words verbatim,
and dumb things like 'watch the horns turn' and stating the obvious like 'eight horned speakers in colored acrylic.'
The brand needs to be sophisticated, but witty. Also remove pricing for now and make it a contact for details type of
thing." So every line is written again (CLOUDS, SPEC and the page below): each colour has a line of its own, and no
price is shown anywhere; a pair is quoted on request.

    python3 spinoffs/barkhorn/web.py                    the page, from the pictures already in site/img
    python3 spinoffs/barkhorn/web.py --images [--sources DIR]
                                                        the pictures too: from the repository's renders and icons, and
                                                        from DIR (the working notes') the look book's photographs
                                                        (r8/deck-assets/photos), round 25's room and drawings
                                                        (r25/site/img) and the coins' renders (r46/coins) where it has
                                                        them; a picture whose source is not to hand is kept as it is
"""
import argparse, base64, io, json, math, os, re, shutil, subprocess, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import earth as E                                         # noqa: E402
import marks as M                                         # noqa: E402

SITE = os.path.join(HERE, 'site')
IMG = os.path.join(SITE, 'img')
BRAND = os.path.join(HERE, 'brand')
R30 = os.path.join(ROOT, 'renders', '2026-10-17', 'barkhorn', 'site30')
TURN = os.path.join(ROOT, 'renders', '2026-10-15', 'barkhorn', 'turn23')
# round 31: the final pictures (finals.py), the spotlight and the carousel (shoot31.py), and round 31b's: each colour
# in its element (elements/), the hero and the room made again to the promotional critic's bar (hero31.py, room31/)
FIN = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'finals31')
S31 = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'shoot31')
U31 = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'uplight31')     # each colour lit from below: the reel
E31 = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'element31')     # each colour on location, in its element
H31 = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'hero31')        # the eight on their arc, relit
RM31 = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'room31')       # the pair at home, photographed
ST31 = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'studio31')    # the studio's: heroes, the lineup, macros
C31 = os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'companions')   # the record player and the lamp
HABITAT = {'red': 'ember', 'orange': 'dust', 'amber': 'acid', 'green': 'poison', 'blue': 'ice', 'violet': 'haze',
           'ice': 'fog', 'black': 'smoke'}
ELEMENT = dict(HABITAT)       # which concept each colour shows in its element: A (<name>), or B (<name>_b) once it wins
ELEMENT['violet'] = 'haze_b'  # the layered hills beat the lavender field in a blind duel, 2 to 1 (6.2 to 5.9)
ELEMENT['amber'] = 'acid_b'   # acid rain on black lava beat the acid spring at Dallol in a blind duel, 2 to 1 (6.3 to 5.4)
ELEMENT['ice'] = 'fog_b'      # the headland above the fog at dawn beat the summit above a sea of cloud in a blind duel, 3 to 0 (6.7 to 4.7)
ELEMENT['green'] = 'poison_f1b'  # the owner's pick (2026-10-20): A4's wood without the foxgloves, more caps and the arum's berries, after a realism pass
ELEMENT['black'] = 'smoke_e6'    # the owner's pick (2026-10-20): the salt flat, black smoke climbing from the horizon
PLACES = {  # where each concept stands: the speaker page leads with it ("Ember on a lava field at blue hour.")
    'ember': 'on a lava field at blue hour, the crust cracked to its glow',
    'dust': 'on rippled sand in the Southwest at golden hour',
    'acid': 'by the acid springs of Dallol', 'acid_b': 'in acid rain on black lava',
    'poison': 'on a redwood forest floor, among ferns', 'poison_a3': 'on a redwood forest floor, among ferns, foxgloves and fly agarics',
    'poison_a4': 'on a redwood forest floor, behind a troop of fly agarics, among ferns and foxgloves',
    'poison_f1b': 'on a redwood forest floor, among fly agarics, ferns and the berries of lords-and-ladies',
    'ice': 'in snow country at blue hour', 'ice_b': 'on a black-sand beach among icebergs at sunrise',
    'haze': 'in a lavender field at dusk', 'haze_b': 'before layered hills in a hazy evening light',
    'fog': 'on a summit above a sea of cloud', 'fog_b': 'on a headland above the fog at dawn',
    'smoke': 'in a pine wood at dawn, in shafts of woodsmoke', 'smoke_b': 'in a misty birch wood',
    'smoke_e6': 'on a cracked salt flat, black smoke climbing from the horizon',
}
URL = 'https://www.earf.world'                            # the primary domain (earf.world redirects to it)
COMPANIONS_SHOWN = False      # Cumulus and Bell stay off the page while their second designs are drawn (the owner, 2026-10-18)
LINEUP_SHOWN = False          # the studio's eight in a row repeated the hero (the site critic, 2026-10-18); it stays in the look book
TITLE = 'EARF · Atmosphere'
DESC = ('Horn loudspeakers cast in tinted acrylic, in eight colours from Ember to Smoke. '
        'In development at EARF, not yet for sale.')

CLOUDS = [  # key, number, name, icon, the acrylic, its line, its cover (the look book's)
    ('red', '01', 'Ember', 'ember', 'Translucent red', 'The last light of the fire.', 'Oxblood'),
    ('orange', '02', 'Dust', 'dust', 'Translucent orange', 'The colour of a long, dry afternoon.', 'Rust'),
    ('amber', '03', 'Acid', 'acid', 'Translucent golden yellow', 'A yellow with an edge.', 'Ochre'),
    ('green', '04', 'Poison', 'poison', 'Translucent bottle green', 'Bottle green, with a hint of menace.', 'Bottle green'),
    ('blue', '05', 'Ice', 'ice', 'Translucent ice blue', 'Glacier blue, and perfectly composed.', 'Deep blue'),
    ('violet', '06', 'Haze', 'haze', 'Translucent violet', 'Dusk, kept indoors.', 'Deep violet'),
    ('ice', '07', 'Fog', 'fog', 'Water-clear', 'Water-clear. Almost not there.', 'White'),
    ('black', '08', 'Smoke', 'smoke', 'Smoked black', 'Smoked glass, for after dark.', 'Black'),
]
SPEC = [('Height', '1293 mm'), ('Width', '625 mm at the horn, 560 mm at the cabinet'),
        ('Depth', '423 mm overall, 420 mm at the cabinet'),
        ('Weight', 'About 72 kg; 62 kg with the horn lifted off'),
        ('Woofer', "15-inch, with two ports in the front's lower corners"), ('Horn driver', '2-inch compression driver'),
        ('Horn', "Cast resin, the cabinet's full depth, its cap 3 mm proud"),
        ('Amplifier', 'Hypex FusionAmp FA122, built in: two channels, crossed at 800 Hz'),
        ('Inputs', 'XLR (and a link out), RCA, AES, S/PDIF coaxial and optical; USB to set it up'),
        ('Lining', 'Recycled polyester batts in white voile, 100 mm at the top and the bottom'),
        ('Price', 'On request: each pair is made to order')]
MACROS = [('corner', 'ember', 'The top corner of an Ember cabinet, the horn above it',
           'The corner: two 20 mm walls, cast in one colour and cemented.'),
          ('amp', 'dust', "Hypex's FA122 amplifier on the back of a Dust cabinet", 'The amplifier, built in: Hypex&rsquo;s FA122.'),
          ('horn', 'acid', "The Acid horn from the side, its driver's pod and the flare",
           'The horn: cast resin, its driver in a pod whose cap twists off.'),
          ('woofer', 'ice', 'The 15-inch woofer through an Ice cabinet', 'The 15-inch woofer, behind the cloth when the cover&rsquo;s on.'),
          ]   # the grip (Poison) left the row of details with the lineup: four read as a set
# the lamps (round 32d), the owner's picks of 2026-10-19 ("sick lamps. Add them to the site as well"): a pendant whose
# tinted cover comes off on a quarter turn, and a table lamp whose ball sits low in a black acrylic base, both cast in the
# eight tints, frosted within. Round 32f took the owner's notes: black hardware (no brass), the Orb plugged in with a
# battery cartridge as its option, each tint cast to read as its speaker's when lit. Their particulars are the fab kits'
# (companions/PARTICULARS.md). The band shows once every picture in LAMP_PICS is in site/img (made from
# renders/2026-10-19/barkhorn/lamps-site/)
LAMPS = [  # key, name, kind, its line, the hero's alt, particulars
    ('dome', 'Dome', 'Pendant', 'Hung low over the bar. A quarter turn takes its cover off, and another puts a new colour on.',
     'The Dome pendant lit, its Ember cover glowing beneath a black hub',
     [('Size', '200 mm across'), ('Shade', 'Cast acrylic, tinted outside and frosted within'),
      ('Light', '2700 K, its source shielded inside the hub'), ('Fitting', 'Black anodised aluminium, with a quarter-turn catch'),
      ('Covers', 'In all eight colours, sold singly')]),
    ('orb', 'Orb', 'Table lamp', 'A ball of tinted acrylic sitting low in a black acrylic base. Plugged in, it stays put; with its battery, it goes where the conversation is.',
     'The Orb table lamp lit in Ember, sitting low in its black acrylic base',
     [('Size', '160 mm ball, 180 mm tall'), ('Weight', '2.0 kg'),
      ('Light', '2200 to 2700 K, warmer as it dims, under a black touch ring'),
      ('Power', 'USB-C, cable and adapter included; cordless for about ten hours with its battery cartridge, sold separately'), ('Rating', 'IP44, for terraces and spilt drinks'),
      ('Balls', 'In all eight colours, sold singly')]),
]
LAMP_PICS = {  # name: (its width on the page at 1x, the alt where the band doesn't write one)
    'lamp-dome': (800, None), 'lamp-orb': (800, None),
    'lamps-orbs': (1200, 'Eight Orbs in a row, lit, in spectrum order: Ember, Dust, Acid, Poison, Ice, Haze, Fog and Smoke'),
    'lamps-domes': (1200, 'Eight Dome pendants hung in a row at one height, lit, one in each colour'),
    'lamps-unlit': (800, 'An Orb and a Dome in Smoke, switched off: dark, polished acrylic with a pale core'),
    'lamp-cartridge': (900, 'The Orb in Ember, its battery cartridge slid half out of the back of its black acrylic base'),
}
KEYS = [c[0] for c in CLOUDS]
MARK = {key: col for key, line, num, name, col in M.SPEAKERS if line == 'Cloud'}
HUE = {'red': 0, 'orange': 1, 'amber': 2, 'green': 3, 'blue': 4, 'violet': 5}   # the painter's wheel, from red
rgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def save(im, name, width=None, q=82):
    im = im.convert('RGB')
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    path = os.path.join(IMG, name)
    if name.endswith('.png'):
        im.save(path, optimize=True)
    else:
        im.save(path, quality=q, optimize=True, progressive=True)
    return name, im.size


CHEV_L = '<svg viewBox="0 0 18 18" aria-hidden="true"><path d="M11.5 3.5 6 9l5.5 5.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV_R = '<svg viewBox="0 0 18 18" aria-hidden="true"><path d="M6.5 3.5 12 9l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FIELD = (250, 249, 246)      # the studio's bright field, as its frames' edges measure (the median of the eight heroes')


def field(im, top, bottom, side, ground=FIELD):
    """A bright-field frame's edges blended into one flat ground, over these fractions of its height and width: the
    sweep falls off to grey at its corners, and the page's band behind it is one colour."""
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    h, w = a.shape[:2]
    def ramp(n, lo, hi):                                # 0 at each edge, 1 inside, a cosine between
        i = np.arange(n, dtype=np.float32)
        t = np.minimum(np.clip(i / max(1.0, lo * n), 0, 1), np.clip((n - 1 - i) / max(1.0, hi * n), 0, 1))
        return 0.5 - 0.5 * np.cos(np.pi * t)
    m = (ramp(h, top, bottom)[:, None] * ramp(w, side, side)[None, :])[..., None]
    return Image.fromarray((a * m + np.float32(ground) * (1 - m)).round().clip(0, 255).astype(np.uint8))


def widen(im, ar, band=120, decay=300.0, vsig=40.0):
    """A studio frame made wider (to `ar`, width over height) by carrying its backdrop on past each side: the colour and
    the horizontal slope of a band at each edge, smoothed hard down the frame so no row streaks, run outwards with the
    slope levelling off, and grain like the frame's own laid over the new parts. The gallery's stage then holds a tall
    frame edge to edge instead of beside a blurred copy of itself."""
    from scipy.ndimage import gaussian_filter, gaussian_filter1d
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    h, w = a.shape[:2]
    W = int(round(h * ar))
    if W <= w:
        return im.convert('RGB')
    padL = (W - w) // 2; padR = W - w - padL
    sm = gaussian_filter(a, sigma=(3, 3, 0))
    t = np.arange(band, dtype=np.float32); tm = t.mean(); den = float(((t - tm) ** 2).sum())
    def edge(xs, pad):                                  # xs: the band's columns from the edge inwards
        seg = sm[:, xs]
        slope_in = ((seg - seg.mean(1, keepdims=True)) * (t - tm)[None, :, None]).sum(1) / den
        e = gaussian_filter1d(seg.mean(1) - slope_in * tm, vsig, axis=0)
        s = gaussian_filter1d(-slope_in, vsig, axis=0)
        d = np.arange(1, pad + 1, dtype=np.float32)
        return e[:, None, :] + s[:, None, :] * (decay * (1 - np.exp(-d / decay)))[None, :, None]
    left = edge(np.arange(band), padL)[:, ::-1]
    right = edge(np.arange(w - 1, w - 1 - band, -1), padR)
    out = np.concatenate([left, a, right], axis=1)
    sig = float((a[:, :band] - sm[:, :band]).std())
    g = gaussian_filter(np.random.default_rng(7).normal(0, 1, (h, W)).astype(np.float32), 0.7)
    mask = np.ones((h, W), np.float32); mask[:, padL:padL + w] = 0
    out += (g / (g.std() + 1e-6) * sig * mask)[..., None]
    return Image.fromarray(out.clip(0, 255).round().astype(np.uint8))


def cutout(im, ground):
    """A render on a flat ground as a picture with its own transparency: the most transparent colours that, laid over
    that ground, give the render back. It then sits on any page colour with no blend mode, which Safari drops in places
    (inside a frosted header, for one)."""
    v = np.asarray(im, np.float32)
    G = np.float32(ground)
    up = np.where(v > G, (v - G) / np.maximum(255 - G, 1), 0)
    dn = np.where(v < G, (G - v) / np.maximum(G, 1), 0)
    a = np.clip((np.maximum(up, dn).max(2) - 3 / 255) / (1 - 3 / 255), 0, 1)     # the ground's own grain goes
    c = np.where(a[..., None] > 0, G + (v - G) / np.maximum(a, 1e-6)[..., None], 0)
    return Image.fromarray(np.dstack([np.clip(c, 0, 255), a * 255]).round().astype(np.uint8), 'RGBA')


def layer(im, ground, dark):
    """A render as a layer for any page colour: on light grounds a multiply layer (the render over the ground it was
    made on, that ground made white); on dark a screen layer (the light the render adds to its ground)."""
    v = np.asarray(im.convert('RGB')).astype(float)
    G = np.array(ground, float)
    out = (v - G) / (255 - G) * 255 if dark else v / G * 255
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def hero_spots():
    """Where each Cloud stands in the hero, as fractions of the frame: its middle, its sides and its top and foot,
    projected from hero.py's arc through the engine's level camera (render.py: looking level, the lens shifted). A hero
    that brings its own boxes (round 31b's hero31/spots.json, copied beside the picture as img/hero-spots.json) uses
    those instead, so the links follow whatever arc and camera made the picture."""
    own = os.path.join(IMG, 'hero-spots.json')
    if os.path.exists(own):
        d = json.load(open(own))
        return d['landscape'] if isinstance(d, dict) else d
    R, CY, STEP, n = 5.0, -4.6, 0.92, 8
    C, T, lens, sensor, W, H = (0.0, -9.6, 1.75), (0.0, -0.4, 0.55), 46.0, 36.0, 2560, 1280
    tilt = math.atan2(T[2] - C[2], T[1] - C[1])
    sy, k = math.tan(tilt) * lens / sensor, lens / sensor * W
    out = []
    for i in range(n):
        th = (i - (n - 1) / 2) * STEP / R
        x, y = R * math.sin(th), CY + R * math.cos(th)
        P = lambda px, pz: ((px - C[0]) / (y - C[1]) * k + W / 2, H / 2 - ((pz - C[2]) / (y - C[1]) * k - sy * W))
        (l, _), (r, _), (_, top), (_, foot) = P(x - 0.34, 0.6), P(x + 0.34, 0.6), P(x, 1.33), P(x, -0.02)
        out.append(dict(l=round(l / W * 100, 2), w=round((r - l) / W * 100, 2), t=round(top / H * 100, 2),
                        h=round((foot - top) / H * 100, 2)))
    return out


def make_images(sources=None):
    """The page's pictures, into site/img: from the repository's renders and icons, and from `sources` the photographs,
    the room, the drawings and the coins where it has them. A picture whose source is not to hand is kept as it is."""
    os.makedirs(IMG, exist_ok=True)
    at = lambda *p: os.path.join(sources, *p) if sources else ''
    made = []
    def one(path, fn):
        if path and os.path.exists(path):
            fn(path); made.append(os.path.basename(path))
    def first(*paths):                                  # the final if it is there, else the round's picture
        return next((p for p in paths if p and os.path.exists(p)), None)
    hero = first(os.path.join(H31, 'hero.png'), os.path.join(H31, 'hero.jpg'), os.path.join(FIN, 'hero.png'), os.path.join(R30, 'hero.png'))
    one(hero, lambda p: (save(Image.open(p), 'hero.jpg', 2400, q=82), save(Image.open(p), 'hero-1200.jpg', 1200, q=80)))
    # the hero's own link boxes and its phone frame travel with it, and a picture without them leaves none behind
    for name, src in (('hero-spots.json', 'spots.json'), ('hero-portrait.jpg', 'hero-portrait.png'), ('hero-spots-portrait.json', 'spots-portrait.json')):
        theirs = os.path.join(os.path.dirname(hero), src) if hero else ''
        if theirs and src.endswith('.png') and not os.path.exists(theirs):    # a frame over 5 MB ships as a JPG
            theirs = theirs[:-4] + '.jpg'
        if theirs and os.path.exists(theirs):
            if name.endswith('.json'):
                shutil.copy(theirs, os.path.join(IMG, name)); made.append(src)
            else:
                one(theirs, lambda p: save(Image.open(p), name, 1200, q=82))
        elif hero and os.path.exists(os.path.join(IMG, name)):
            os.remove(os.path.join(IMG, name))
    for k in KEYS:
        for side in ('on', 'off'):
            # the cards' tall frame (1:2): cut from the 4:5 front when it is in (the drivers made real, on the paper the
            # gallery shares), else the 1:2 render from before the drivers
            cut = first(*[os.path.join(FIN, f'front-{side}-tall-{k}.{e}') for e in ('png', 'jpg')])
            if cut:
                one(cut, lambda p, s=side: save((lambda im: im.crop(((im.width - im.height // 2) // 2, 0,
                                                                     (im.width + im.height // 2) // 2, im.height)))(Image.open(p)),
                                                  f'{k}-{s}.jpg', 900, q=80))
            else:
                one(first(os.path.join(FIN, f'front-{side}-{k}.png'), at('r8', 'deck-assets', 'photos', f'look2-{k}-{side}.jpg')),
                    lambda p, s=side: save(Image.open(p), f'{k}-{s}.jpg', 900, q=80))
            # the gallery's, at the stage's shapes (3:2, and 4:5 on phones): the fronts rendered at those shapes when they are
            # in, else the tall front with its backdrop carried on past its sides
            for shape, ar, px in (('wide', 1.5, 1800), ('tall', 0.8, 1000)):
                own = first(*[os.path.join(FIN, f'front-{side}-{shape}-{k}.{e}') for e in ('png', 'jpg')])
                if own:
                    one(own, lambda p, s=side, sh=shape, w=px: save(Image.open(p), f'{k}-{s}-{sh}.jpg', w, q=84))
                else:
                    one(first(os.path.join(FIN, f'front-{side}-{k}.png')),
                        lambda p, s=side, sh=shape, a=ar, w=px: save(widen(Image.open(p), a), f'{k}-{s}-{sh}.jpg', w, q=84))
        for tag, fin, old in (('back', f'back-{k}.png', f'back-{k}.png'), ('amp', f'amp-{k}.png', f'detail-{k}.png')):
            one(first(os.path.join(FIN, fin), os.path.join(R30, old)), lambda p, t=tag: save(Image.open(p), f'{k}-{t}.jpg', 880, q=82))
        for tag in ('side', 'back'):
            one(first(os.path.join(FIN, f'horn-{tag}-{k}.png'), at('r8', 'deck-assets', 'photos', f'hornc-{k}-{tag}.jpg')),
                lambda p, t=tag: save(Image.open(p), f'{k}-horn-{t}.jpg', 1000, q=84))
        one(first(os.path.join(FIN, f'turn-{k}.jpg'), os.path.join(TURN, f'sprite-{k}.jpg')),
            lambda p: shutil.copy(p, os.path.join(IMG, f'turn-{k}.jpg')))
        one(os.path.join(FIN, f'inside-{k}.png'), lambda p: save(Image.open(p), f'{k}-inside.jpg', 880, q=82))
        h = HABITAT[k]
        one(first(*[os.path.join(U31, f'{n}-{c}.{e}') for n in ('uplit', 'uplight', 'reel', 'frame') for c in (k, h) for e in ('png', 'jpg')]),
            lambda p: save(Image.open(p), f'{k}-reel.jpg', 1600, q=82))     # shown at up to 58vw: 2x at 1440
        e = ELEMENT[k]                                  # the concept the colour shows in its element
        one(first(os.path.join(E31, f'{e}.png'), os.path.join(E31, f'{e}.jpg')),        # the strip shows it 1080 wide: 2x, and a 1x
            lambda p: (save(Image.open(p), f'{k}-habitat.jpg', 2400, q=82), save(Image.open(p), f'{k}-habitat-1200.jpg', 1200, q=82)))
        one(first(os.path.join(E31, f'{e}-portrait.png'), os.path.join(E31, f'{e}-portrait.jpg')),
            lambda p: save(Image.open(p), f'{k}-habitat-portrait.jpg', 1200, q=82))
        for tag, names in (('studio', ('hero-dark', 'hero')), ('studio-light', ('hero-light',))):
            one(first(*[os.path.join(ST31, f'{n}-{c}.{e}') for n in names for c in (h, k) for e in ('png', 'jpg')]),
                lambda p, t=tag: (lambda im: (save(im, f'{k}-{t}.jpg', 2400, q=84), save(im, f'{k}-{t}-1200.jpg', 1200, q=82)))(
                    field(Image.open(p), 0.14, 0.05, 0.22) if t == 'studio-light' else Image.open(p)))
    one(os.path.join(R30, 'inside.png'), lambda p: save(Image.open(p), 'inside.jpg', 880, q=82))
    one(first(os.path.join(ST31, 'lineup.png'), os.path.join(ST31, 'lineup.jpg')),       # its horizon kept below the horns
        lambda p: (lambda im: (save(im, 'lineup.jpg', 2400, q=84), save(im, 'lineup-1200.jpg', 1200, q=82)))(field(Image.open(p), 0.25, 0.07, 0.06)))
    for m, c, *_ in MACROS:                             # the studio's details, each in the colour it was shot in
        one(first(*[os.path.join(ST31, f'macro-{m}-{c}.{e}') for e in ('png', 'jpg')]),
            lambda p, m=m: save(Image.open(p), f'macro-{m}.jpg', 720, q=84))    # a quarter of the column: 2x at 1440
    for tag in ('turntable', 'lamp'):
        one(first(os.path.join(C31, f'hero-{tag}.png'), os.path.join(C31, f'hero-{tag}.jpg')),
            lambda p, t=tag: save(Image.open(p), f'next-{t}.jpg', 1400, q=84))
    for tag, names in (('facade', ('facade', 'night', 'opera')), ('facade-portrait', ('facade-portrait', 'night-portrait', 'opera-portrait'))):
        one(first(*[os.path.join(U31, f'{n}.{e}') for n in names for e in ('png', 'jpg')]),
            lambda p, t=tag: (save(Image.open(p), f'{t}.jpg', 2400, q=84), save(Image.open(p), f'{t}-1200.jpg', 1200, q=82)))
    room = first(os.path.join(RM31, 'room.png'), os.path.join(RM31, 'room.jpg'), os.path.join(FIN, 'room.png'))
    one(room, lambda p: (save(Image.open(p), 'room.jpg', 2880, q=82), save(Image.open(p), 'room-1440.jpg', 1440, q=82)))   # full bleed: 2x at 1440
    port = first(*[os.path.join(os.path.dirname(room), f'room-portrait.{e}') for e in ('png', 'jpg')]) if room else ''
    if port and os.path.exists(port):                   # the room's phone frame travels with it, as the hero's does
        one(port, lambda p: save(Image.open(p), 'room-portrait.jpg', 1000, q=84))
    elif room and os.path.exists(os.path.join(IMG, 'room-portrait.jpg')):
        os.remove(os.path.join(IMG, 'room-portrait.jpg'))
    for f in ('room.jpg', 'ga-front.png', 'ga-right.png'):
        if f == 'room.jpg' and room:
            continue
        one(at('r25', 'site', 'img', f), lambda p, f=f: shutil.copy(p, os.path.join(IMG, f)))
    # the icons, acrylic (icons_real.py's renders), each cut out of the ground it was rendered on so it sits on any page
    # colour with no blend mode. Water-clear Fog all but vanished on paper, so its edges are darkened by what its dark
    # render lights; smoked Smoke likewise on night, so its body is lifted by how dark its light render draws it
    paper, night = rgb(E.PAPER), rgb(E.NIGHT)
    for k, num, name, icon, *_ in CLOUDS:
        pair = [os.path.join(BRAND, 'icons', f'icon-{icon}-render{t}.png') for t in ('', '-night')]
        if not all(os.path.exists(p) for p in pair):
            continue
        L, D = (np.asarray(Image.open(p).convert('RGB').resize((256, 256), Image.LANCZOS)).astype(np.float32) for p in pair)
        if icon == 'fog':
            lit = np.clip((D.mean(2) - np.mean(night)) / (255 - np.mean(night)), 0, 1)[..., None]
            L = L * (1 - 0.6 * lit ** 1.6)
        if icon == 'smoke':
            body = np.clip((np.mean(paper) - L.mean(2)) / np.mean(paper), 0, 1)[..., None]
            D = D + 0.3 * body * (200 - D)
        cutout(L, paper).save(os.path.join(IMG, f'icon-{icon}-light.webp'), quality=90, method=6)
        cutout(D, night).save(os.path.join(IMG, f'icon-{icon}-dark.webp'), quality=90, method=6)
        made.append(f'icon-{icon}')
    # the header's globe: its sheet of 60 frames cut out of its white and its black grounds (it showed a square wherever
    # the blend mode was dropped), at 84 px a frame
    for tag, ground in (('light', (255, 255, 255)), ('dark', (0, 0, 0))):
        src = os.path.join(BRAND, 'site', f'globe-spin-{tag}.jpg')
        if os.path.exists(src):
            im = cutout(Image.open(src).convert('RGB'), ground).convert('RGBa').resize((840, 504), Image.LANCZOS).convert('RGBA')
            im.save(os.path.join(IMG, f'globe-spin-{tag}.avif'), quality=60)
            im.save(os.path.join(IMG, f'globe-spin-{tag}.webp'), quality=70, alpha_quality=80, method=6)
            made.append(f'globe-spin-{tag}')
    # the opening's globe: the same render's turn (brand/mark/earf-globe-render-spin.webm, 120 frames in 4 s), cropped to
    # the globe at 360 px, as VP9 and H.264 tagged BT.709, and its first frame as decoded (WebP, q80); made once with
    # ffmpeg into brand/site, and the same again from the night render (earf-globe-render-night-spin.webm) for a dark system:
    #   -vf "crop=492:492:112:112,scale=360:360:flags=lanczos:out_color_matrix=bt709" (-crf 34 VP9, -crf 23 x264)
    for name in ('globe-turn.webm', 'globe-turn.mp4', 'globe-turn-poster.webp',
                 'globe-turn-night.webm', 'globe-turn-night.mp4', 'globe-turn-night-poster.webp'):
        src = os.path.join(BRAND, 'site', name)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(IMG, name))
            made.append(name)
    # the lamps' pictures (the companions session's finals, at full size), each at twice its page width and at once
    for name, (w, _) in LAMP_PICS.items():
        src = os.path.join(ROOT, 'renders', '2026-10-19', 'barkhorn', 'lamps-site', f'{name}.png')
        if os.path.exists(src):
            im = Image.open(src)
            save(im, f'{name}.jpg', 2 * w, q=84); save(im, f'{name}-{w}.jpg', w, q=84)
            made.append(name)
    # the coins, in the icons' order, one sheet for each ground (round 30's renders, at 800 px on E.PAPER and E.NIGHT)
    order = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
    for tag, ground, dark in (('paper', (242, 238, 232), False), ('night', (17, 16, 19), True)):
        files = [at('r46', 'coins', f'{icon}-{tag}.png') for icon in order]
        if all(f and os.path.exists(f) for f in files):
            sheet = Image.new('RGB', (128 * 8, 128))
            for j, f in enumerate(files):
                sheet.paste(layer(Image.open(f).resize((128, 128), Image.LANCZOS), ground, dark), (128 * j, 0))
            sheet.save(os.path.join(IMG, f'coins-{"dark" if dark else "light"}.jpg'), quality=90)
            made.append(f'coins-{tag}')
    return made


def image_meta():
    """The pictures as they stand in site/img: each speaker's views (src, w, h), the inside shot, and each card's panel
    colour (the photograph's foot, where the panel meets it)."""
    size = lambda n: Image.open(os.path.join(IMG, n)).size

    def ground(n, box=None):
        """The colours round a picture's edge, so the stage can carry its ground past it: five down the left side, five
        down the right, then the top's and the bottom's (the top's again where the subject runs off the bottom), as hex;
        and how its edges run: 'busy' for a close-up whose subject runs off the sides (a blurred copy of it fills the
        stage instead), 'cut' for one whose subject runs off the bottom (it sits on the stage's foot)."""
        im = Image.open(os.path.join(IMG, n)).convert('RGB')
        a = np.asarray(im.crop(box) if box else im).astype(np.float32)
        h, lum = a.shape[0], a.mean(2)
        side = lambda e: [np.median(e[h * i // 5:h * (i + 1) // 5].reshape(-1, 3), 0) for i in range(5)]
        top, bot = a[:8].reshape(-1, 3), a[-8:].reshape(-1, 3)
        cut = lum[-8:].std() > 20
        busy = np.concatenate([lum[:, :8].ravel(), lum[:, -8:].ravel()]).std() > 14 or lum[:8].std() > 8
        hexes = ''.join('%02x%02x%02x' % tuple(int(round(float(x))) for x in c)
                        for c in side(a[:, :8]) + side(a[:, -8:]) + [np.median(top, 0), np.median(top if cut else bot, 0)])
        return dict(bg=hexes, **({'edge': 'busy'} if busy else {'edge': 'cut'} if cut else {}))
    meta, panel = {}, {}
    for k in KEYS:
        views = {}
        for v, n in (('on', f'{k}-on.jpg'), ('off', f'{k}-off.jpg'), ('studio', f'{k}-studio.jpg'), ('studio-light', f'{k}-studio-light.jpg'),
                     ('back', f'{k}-back.jpg'), ('amp', f'{k}-amp.jpg'),
                     ('horn-side', f'{k}-horn-side.jpg'), ('horn-back', f'{k}-horn-back.jpg'), ('inside', f'{k}-inside.jpg'),
                     ('reel', f'{k}-reel.jpg'), ('habitat', f'{k}-habitat.jpg')):
            if not os.path.exists(os.path.join(IMG, n)):
                continue                                # round 31's pictures appear as they arrive
            w, h = size(n)
            views[v] = dict(src=f'img/{n}', w=w, h=h, **ground(n))
        if 'inside' not in views:                       # the shared cutaway (Poison's) until a colour has its own
            w, h = size('inside.jpg')
            views['inside'] = dict(src='img/inside.jpg', w=w, h=h, **ground('inside.jpg'), shared=True)
        if 'habitat' in views and os.path.exists(os.path.join(IMG, f'{k}-habitat-portrait.jpg')):
            w, h = size(f'{k}-habitat-portrait.jpg')    # its phone frame, for the stage's phone shape
            views['habitat']['tall'] = dict(src=f'img/{k}-habitat-portrait.jpg', w=w, h=h)
        for v in ('on', 'off'):                         # the cover frames widened to the stage's shapes: they fill it, as the habitat does
            if v in views and all(os.path.exists(os.path.join(IMG, f'{k}-{v}-{s}.jpg')) for s in ('wide', 'tall')):
                (w, h), (tw, th) = size(f'{k}-{v}-wide.jpg'), size(f'{k}-{v}-tall.jpg')
                card = dict(src=views[v]['src'], w=views[v]['w'], h=views[v]['h'])     # the tall frame stays for the small cards
                views[v] = dict(src=f'img/{k}-{v}-wide.jpg', w=w, h=h, fill=True, tall=dict(src=f'img/{k}-{v}-tall.jpg', w=tw, h=th), card=card)
        w, h = size(f'turn-{k}.jpg')
        views['turn'] = dict(src=f'img/turn-{k}.jpg', w=w // 6, h=h // 4, **ground(f'turn-{k}.jpg', (0, 0, w // 6, h // 4)))
        meta[k] = views
        corner = np.asarray(Image.open(os.path.join(IMG, f'{k}-on.jpg')).convert('RGB'))[-18:-3].reshape(-1, 3).mean(0)   # where the photograph meets its panel
        panel[k] = '#%02X%02X%02X' % tuple(int(x) for x in corner)
    return meta, panel


def body():
    """The page's head (fonts and style) and body, its pictures as they stand in site/img."""
    meta, panel = image_meta()
    spots = hero_spots()
    with Image.open(os.path.join(IMG, 'globe-spin-light.webp')) as sp:     # the loader's first frame, inline (a few KB)
        fw, fh = sp.width // 10, sp.height // 6
        buf = io.BytesIO(); sp.crop((0, 0, fw, fh)).save(buf, 'WEBP', quality=90, method=6)
    still = 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()
    inline = lambda name: (('data:image/webp;base64,' + base64.b64encode(open(os.path.join(IMG, name), 'rb').read()).decode())
                           if os.path.exists(os.path.join(IMG, name)) else still)
    poster, poster_night = inline('globe-turn-poster.webp'), inline('globe-turn-night-poster.webp')   # the opening's first frames
    word = E.word_svg('currentColor').replace('role="img" aria-label="EARF"', 'aria-hidden="true"').replace('<title>EARF</title>', '')
    coin = {k: i for i, k in enumerate(KEYS)}                 # the coins' sheet is in the speakers' order
    icon_img = lambda icon, name, cls='': (f'<img class="ic only-light {cls}" src="img/icon-{icon}-light.webp" alt="" width="256" height="256">'
                                           f'<img class="ic only-dark {cls}" src="img/icon-{icon}-dark.webp" alt="" width="256" height="256">')
    icon_paper = lambda icon: f'<img class="ic" src="img/icon-{icon}-light.webp" alt="" width="256" height="256">'   # on a pale pill in either theme
    rank = lambda boxes: {i: 2 + r for r, i in enumerate(sorted(range(len(boxes)), key=lambda i: boxes[i]['t'] + boxes[i]['h']))}
    zs = rank(spots)                                    # in number order for the keyboard, the front rank's boxes over the back's
    hotspots = ''.join(
        f'<a class="spot" href="#speaker-{name.lower()}" style="left:{s["l"]}%;top:{s["t"]}%;width:{s["w"]}%;height:{s["h"]}%;z-index:{zs[i]}">'
        f'<span class="spot-label"><span class="spot-ic">{icon_paper(icon)}</span><b>{name}</b><span>{num}</span></span>'
        f'<span class="sr">{name}, Atmosphere {num}</span></a>'
        for i, ((k, num, name, icon, *_), s) in enumerate(zip(CLOUDS, spots)))
    names = ''.join(f'<li><a href="#speaker-{name.lower()}"><span class="coin-dot" style="--i:{coin[k]}"></span>{name}</a></li>'
                    for k, num, name, *_ in CLOUDS)
    turn = ''.join(
        f'<li><div class="spin" data-k="{k}" role="img" aria-label="{name}\'s horn; drag to turn it" '
        f'data-bg="img/turn-{k}.jpg" style="aspect-ratio:{meta[k]["turn"]["w"]} / {meta[k]["turn"]["h"]}"></div>'
        f'<a href="#speaker-{name.lower()}">{name}</a></li>' for k, num, name, *_ in CLOUDS)
    on = meta['red']['on'].get('card', meta['red']['on']); w, h = on['w'], on['h']        # the cards keep the tall frame
    cards = ''.join(
        f'<article class="card" style="--panel:{panel[k]}">'
        f'<a class="photo" href="#speaker-{name.lower()}" aria-label="{name}, up close">'
        f'<img class="on" src="img/{k}-on.jpg" width="{w}" height="{h}" alt="{name} with its cloth cover on" loading="lazy">'
        f'<img class="off" src="img/{k}-off.jpg" width="{w}" height="{h}" alt="{name} with its cover off, the woofer showing" loading="lazy"></a>'
        f'<div class="about"><p class="num">Atmosphere {num}</p>'
        f'<h3 class="named">{name}<span class="card-ic">{icon_img(icon, name)}</span></h3><p class="line">{line}</p>'
        f'<dl><dt>Acrylic</dt><dd>{tint}</dd><dt>Cover</dt><dd>{cover}</dd></dl>'
        f'<a class="more" href="#speaker-{name.lower()}">Up close</a></div></article>'
        for k, num, name, icon, tint, line, cover in CLOUDS)
    nb = lambda t: re.sub(r'(\d) (mm|kg|Hz)\b', '\\1\u00a0\\2', t)      # a number never parts from its unit
    spec = ''.join(f'<dt>{a}</dt><dd>{nb(b)}</dd>' for a, b in SPEC)
    dwg = ''                                            # the two views drawn at one scale: each as wide as its share of the row
    for f, alt in (('ga-front.png', 'The speaker drawn from the front'), ('ga-right.png', 'The speaker drawn from the right')):
        gw, gh = Image.open(os.path.join(IMG, f)).size
        dwg += f'<img src="img/{f}" width="{gw}" height="{gh}" style="flex:{gw / gh:.4f} 1 0" alt="{alt}" loading="lazy">'
    reel = habitats = closer = ''
    sk = next((t for t in ('studio-light', 'studio') if all(t in meta[k] for k in KEYS)), None)   # round 31's bright field won
    if sk:
        sw, sh = meta['red'][sk]['w'], meta['red'][sk]['h']
        im = np.asarray(Image.open(os.path.join(IMG, f'red-{sk}.jpg')).convert('RGB'))
        edge = np.concatenate([im[:6].reshape(-1, 3), im[-6:].reshape(-1, 3), im[:, :6].reshape(-1, 3), im[:, -6:].reshape(-1, 3)]).mean(0)
        light = edge.mean() > 150                       # a pale ground takes dark type
        lineup = ''
        if LINEUP_SHOWN and os.path.exists(os.path.join(IMG, 'lineup.jpg')):
            lw, lh = Image.open(os.path.join(IMG, 'lineup.jpg')).size
            lineup = ('    <figure class="lineup"><img src="img/lineup.jpg" srcset="img/lineup-1200.jpg 1200w, img/lineup.jpg 2400w" '
                      f'sizes="(max-width: 1240px) 100vw, 1240px" width="{lw}" height="{lh}" loading="lazy" '
                      + ('alt="All eight in a row in spectrum order on a white floor, each throwing its colour onto it">' if light else
                         'alt="All eight in a row in spectrum order, on a black floor that mirrors them">') +
                      '<figcaption>All eight, in spectrum order.</figcaption></figure>\n')
        if all(os.path.exists(os.path.join(IMG, f'macro-{m}.jpg')) for m, *_ in MACROS):
            lineup += ('    <ul class="macros" aria-label="Details">' + ''.join(
                f'<li><figure><img src="img/macro-{m}.jpg" width="{Image.open(os.path.join(IMG, f"macro-{m}.jpg")).width}" '
                f'height="{Image.open(os.path.join(IMG, f"macro-{m}.jpg")).height}" '
                f'loading="lazy" alt="{alt}"><figcaption>{cap}</figcaption></figure></li>' for m, c, alt, cap in MACROS) + '</ul>\n')
        hid = ' aria-hidden="true"'
        closer = (f'  <section class="band closer{" light" if light else ""}" id="closer" style="--closer:#%02X%02X%02X"><div class="wrap">\n' % tuple(int(x) for x in edge) +
                  '    <div class="closer-head"><p class="eyebrow">In the studio</p><h2>Cast in colour, all the way through.</h2></div>\n'
                  f'    <div class="closer-stage" style="aspect-ratio:{sw} / {sh}">' + ''.join(
                      f'<img class="{"on" if i == 0 else ""}" src="img/{k}-{sk}.jpg" srcset="img/{k}-{sk}-1200.jpg 1200w, img/{k}-{sk}.jpg 2400w" '
                      f'sizes="(max-width: 1240px) 100vw, 1240px" width="{sw}" height="{sh}" loading="lazy" '
                      f'alt="{name} in the studio{" on white" if light else ""}, the light coming through its acrylic"{"" if i == 0 else hid}>'
                      for i, (k, num, name, *_) in enumerate(CLOUDS)) + '</div>\n'
                  '    <div class="picker">\n      <div class="dots" role="radiogroup" aria-label="Colour">' + ''.join(
                      f'<button type="button" role="radio" aria-checked="{str(i == 0).lower()}" aria-label="{name}" tabindex="{0 if i == 0 else -1}">'
                      f'<span class="coin-dot" style="--i:{coin[k]}"></span></button>'
                      for i, (k, num, name, *_) in enumerate(CLOUDS)) + '</div>\n'
                  f'      <p class="picked" id="closer-cap" aria-live="polite"><b>{CLOUDS[0][2]}</b> {CLOUDS[0][5]}</p>\n    </div>\n'
                  + lineup + '  </div></section>')
    if all('reel' in meta[k] for k in KEYS):
        rw, rh = meta['red']['reel']['w'], meta['red']['reel']['h']
        first_ = CLOUDS[0]
        facade = ''
        if os.path.exists(os.path.join(IMG, 'facade.jpg')):
            fw, fh = Image.open(os.path.join(IMG, 'facade.jpg')).size
            portrait = ('<source media="(max-width: 700px)" srcset="img/facade-portrait-1200.jpg 1200w, img/facade-portrait.jpg 2400w">'
                        if os.path.exists(os.path.join(IMG, 'facade-portrait.jpg')) else '')
            facade = ('    <figure class="facade"><picture>' + portrait +
                      f'<img src="img/facade.jpg" srcset="img/facade-1200.jpg 1200w, img/facade.jpg 2400w" sizes="(max-width: 1240px) 100vw, 1240px" '
                      f'width="{fw}" height="{fh}" loading="lazy" alt="A concrete wall by a river at night, the eight standing along its foot '
                      'on lights, their colours washing up the wall and running into one another"></picture></figure>\n')
        # each colour's light as it falls on the wall in its photograph (sampled), and how bright that photograph really is
        glow = {'red': ('235 67 66', 1.0), 'orange': ('235 94 45', 1.0), 'amber': ('235 154 36', 1.0), 'green': ('136 234 131', 0.57),
                'blue': ('73 174 235', 0.98), 'violet': ('143 112 235', 0.72), 'ice': ('218 234 235', 1.0), 'black': ('146 181 235', 0.28)}
        coins = ''.join(f'<button type="button" role="radio" aria-checked="{str(i == 0).lower()}" tabindex="{0 if i == 0 else -1}" '
                        f'aria-label="{name}" data-k="{k}" data-glow="{glow[k][0]}" data-a="{glow[k][1]}"><span class="coin-dot" style="--i:{coin[k]}"></span></button>'
                        for i, (k, num, name, *_) in enumerate(CLOUDS))
        intro = ('<p class="eyebrow">Lit from below</p><h2>Put a light under it.</h2>'
                 '<p>Cast acrylic carries light to its edges, so a lamp underneath fills the whole cabinet with colour.</p>')
        reel = ('  <section class="band lightband" id="light">\n'
                f'    <div class="wrap light-head">{intro}</div>\n'           # on phones the heading stands above the run
                '    <div class="light-run" id="light-run">\n'
                '      <div class="light-stage">\n'
                '        <div class="light-glow" aria-hidden="true"></div>\n'
                '        <figure class="light-pic">' + ''.join(
                    f'<img src="img/{k}-reel.jpg" width="{rw}" height="{rh}" alt="{name} standing on a light, its colour thrown up the wall behind it"'
                    f'{" class=on" if i == 0 else ""} loading="lazy" decoding="async">' for i, (k, num, name, *_) in enumerate(CLOUDS)) + '</figure>\n'
                f'        <div class="light-text"><div class="light-intro">{intro}</div>\n'
                f'          <div class="light-colour"><p class="num" id="light-num">Atmosphere {first_[1]}</p>'
                f'<p class="light-name" id="light-name">{first_[2]}</p><p class="light-line" id="light-line">{first_[5]}</p>\n'
                f'            <div class="light-coins" role="radiogroup" aria-label="The eight colours"><span class="ring" aria-hidden="true"></span>{coins}</div></div>\n'
                '        </div>\n      </div>\n    </div>\n'
                + facade +
                '  </section>')
    if all('habitat' in meta[k] for k in KEYS):
        hw, hh = meta['red']['habitat']['w'], meta['red']['habitat']['h']
        tall = all(os.path.exists(os.path.join(IMG, f'{k}-habitat-portrait.jpg')) for k in KEYS)
        habitats = ('  <section class="band" id="habitats"><div class="wrap">\n'
                    '    <div class="head"><div><p class="eyebrow">In their element</p><h2>Each colour, out in the world.</h2></div></div>\n'
                    '    <div class="hab-frame">\n'
                    '    <ul class="habitats" id="hab" tabindex="0" aria-label="The eight in their habitats">' + ''.join(
                        f'<li><a href="#speaker-{name.lower()}"><picture>'
                        + (f'<source media="(max-width: 700px)" srcset="img/{k}-habitat-portrait.jpg">' if tall else '') +
                        f'<img src="img/{k}-habitat.jpg" srcset="img/{k}-habitat-1200.jpg 1200w, img/{k}-habitat.jpg {hw}w" '
                        f'sizes="(max-width: 700px) 84vw, min(86vw, 1080px)" width="{hw}" height="{hh}" loading="lazy" '
                        f'alt="{name}, on location"></picture><span><b>{name}</b> {line}</span></a></li>'
                        for k, num, name, icon, tint, line, cover in CLOUDS) + '</ul>\n'
                    f'    <button type="button" class="nav prev" id="hab-prev" aria-label="Previous">{CHEV_L}</button>'
                    f'<button type="button" class="nav next" id="hab-next" aria-label="Next">{CHEV_R}</button>\n'
                    '    </div>\n  </div></section>')
    pair = [('turntable', 'Cumulus', 'A record player. Belt drive, its motor in a pod of its own.',
             'Cumulus, a record player in tinted acrylic, its platter on a plinth of overlapping circles'),
            ('lamp', 'Bell', 'A lamp. The horn&rsquo;s flare, hung mouth down.',
             'Bell, a table lamp whose tinted acrylic shade is the horn&rsquo;s flare turned over')]
    figs = ''
    if COMPANIONS_SHOWN and all(os.path.exists(os.path.join(IMG, f'next-{t}.jpg')) for t, *_ in pair):
        figs = '\n    <div class="pair">' + ''.join(
            '<figure><img src="img/next-{0}.jpg" width="{1}" height="{2}" loading="lazy" alt="{5}">'
            '<figcaption><b>{3}</b> {4}</figcaption></figure>'.format(t, *Image.open(os.path.join(IMG, f'next-{t}.jpg')).size, n, d, alt)
            for t, n, d, alt in pair) + '</div>'
    lamps_shown = all(os.path.exists(os.path.join(IMG, f'{n}.jpg')) for n in LAMP_PICS)
    def pic(name, alt, cls=''):
        w, h = Image.open(os.path.join(IMG, f'{name}.jpg')).size
        w1 = LAMP_PICS[name][0]
        return (f'<img{cls} src="img/{name}-{w1}.jpg" srcset="img/{name}-{w1}.jpg {w1}w, img/{name}.jpg {w}w" '
                f'sizes="(max-width: 720px) 100vw, 50vw" width="{w}" height="{h}" loading="lazy" alt="{alt or LAMP_PICS[name][1]}">')
    lamps = ('  <section class="band lamps" id="lamps"><div class="wrap">\n'
             '    <div class="head"><div><p class="eyebrow">In good company</p><h2>The same eight, lit from within.</h2>\n'
             '      <p>A pendant and a table lamp in the speakers&rsquo; acrylic, frosted inside, so the colour glows and the '
             'source never shows. Every cover comes off by hand.</p></div></div>\n'
             '    <div class="lamp-pair">' + ''.join(
                 f'<article class="lamp">{pic("lamp-" + k, alt)}<h3>{name}<small>{kind}</small></h3><p class="line">{line}</p>'
                 '<dl class="facts">' + ''.join(f'<dt>{t}</dt><dd>{d}</dd>' for t, d in facts) + '</dl></article>'
                 for k, name, kind, line, alt, facts in LAMPS) + '</div>\n'
             '    <figure class="eight">' + pic('lamps-domes', None) + pic('lamps-orbs', None) +
             '<figcaption>In spectrum order, as the speakers: Ember, Dust, Acid, Poison, Ice, Haze, Fog and Smoke.</figcaption></figure>\n'
             '    <div class="lamp-duo"><figure>' + pic('lamp-cartridge', None) +
             '<figcaption>Slide in the cartridge and it goes cordless for about ten hours.</figcaption></figure>'
             '<figure>' + pic('lamps-unlit', None) + '<figcaption>Off, in Smoke.</figcaption></figure></div>\n'
             '  </div></section>') if lamps_shown else ''
    nxt = ('  <section class="band"><div class="wrap next">\n    <p class="eyebrow">Next</p>\n'
           '    <h2>In good company.</h2>\n'
           '    <p>A record player and a lamp are on the drawing board, cast in the same eight colours.</p>' + figs +
           '\n  </div></section>') if COMPANIONS_SHOWN else lamps
    goes_sec = ('    <section aria-labelledby="goes-title">\n'
                '      <div class="goes-head"><h2 id="goes-title">Good company</h2><span id="goes-note"></span></div>\n'
                '      <div class="goes" id="goes" aria-live="polite"></div>\n'
                '    </section>\n') if COMPANIONS_SHOWN else ''
    data = dict(
        clouds=[dict(k=k, num=num, name=name, icon=icon, tint=tint, line=line, cover=cover, col=MARK[k], hue=HUE.get(k),
                     coin=coin[k], views=meta[k], place=PLACES.get(ELEMENT[k], 'on location'))
                for k, num, name, icon, tint, line, cover in CLOUDS],
        hues=E.HUES)
    # a phone frame of the hero or the room, where one was made (re-framed, not cropped); with the hero's, its links
    # give way on phones to the names under it, the boxes being the landscape frame's
    tall = lambda f: os.path.exists(os.path.join(IMG, f))
    hero_tall = ('<source media="(max-width: 700px)" srcset="img/hero-portrait.jpg">' if tall('hero-portrait.jpg') else '')
    room_tall = ('<source media="(max-width: 700px)" srcset="img/room-portrait.jpg">' if tall('room-portrait.jpg') else '')
    if hero_tall:
        hotspots = hotspots.replace('class="spot"', 'class="spot wide-only"')
    if hero_tall and tall('hero-spots-portrait.json'):    # the phone frame's own boxes: the back rank first, so the front's lie over it
        ps = json.load(open(os.path.join(IMG, 'hero-spots-portrait.json')))
        ps = ps['portrait'] if isinstance(ps, dict) else ps
        zp = rank(ps)
        hotspots += ''.join(
            f'<a class="spot tall-only" href="#speaker-{name.lower()}" style="left:{s["l"]}%;top:{s["t"]}%;width:{s["w"]}%;height:{s["h"]}%;z-index:{zp[i]}">'
            f'<span class="sr">{name}, Atmosphere {num}</span></a>'
            for i, ((k, num, name, *_), s) in enumerate(zip(CLOUDS, ps)))
    page = (PAGE.replace('__WORD__', word).replace('__HOTSPOTS__', hotspots).replace('__NAMES__', names)
                .replace('__HERO_TALL__', hero_tall).replace('__ROOM_TALL__', room_tall)
                .replace('__HERO_CLASS__', ' has-tall' if hero_tall else '')
                .replace('__TURN__', turn).replace('__CARDS__', cards).replace('__SPEC__', spec).replace('__DWG__', dwg)
                .replace('__REEL__', reel).replace('__HABITATS__', habitats).replace('__CLOSER__', closer).replace('__NEXT__', nxt).replace('__GOES__', goes_sec)
                .replace('__LAMPS_NAV__', '<li class="wide"><a href="#lamps">Lamps</a></li>' if lamps_shown else '')
                .replace('__STILL__', still).replace('__POSTER__', poster).replace('__POSTER_NIGHT__', poster_night).replace('__DATA__', json.dumps(data, separators=(',', ':'))))
    cut = page.index('</style>') + len('</style>')
    return page[:cut], page[cut:]


PAGE = r"""
<script>(function (d) { d.classList.add('opening');      // the opening's choice, made before anything paints: whether it plays, and by day or night
  if (location.hash.startsWith('#speaker-') || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  d.classList.add('intro');
  if (matchMedia('(prefers-color-scheme: dark)').matches) { d.classList.add('night'); document.querySelector('meta[name="theme-color"]').content = '#100F12'; }
})(document.documentElement)</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400..700&display=swap">
<style>
/* layout: a showroom in one column of bands; the speakers themselves carry the colour, the page stays paper and ink */
:root {
  --paper: #ECE8E1; --page: #F4F1EC; --ink: #1C1A18; --muted: #5E5A53; --rule: #D6D0C6; --card-ink: #1A1917;
  --ring: rgba(0, 0, 0, 0.25); --on-photo: #1C1A18; --veil: rgba(242, 239, 234, 0.82);
  --blend: multiply;
  --sans: 'Instrument Sans', 'Helvetica Neue', Arial, sans-serif; --mono: 'IBM Plex Mono', 'Courier New', monospace;
  --header: 64px;
}
:root { color-scheme: light }                     /* one theme by choice: every photograph here stands on a pale ground */
.only-dark { display: none !important }
* { box-sizing: border-box }
body { margin: 0; background: var(--page); color: var(--ink); font-family: var(--sans); font-size: 17px; line-height: 1.55 }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--page) }
.wrap { max-width: 1240px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px)) }
.band { padding-block: 72px }
.band + .band { border-top: 0 }
section[id] { scroll-margin-top: calc(var(--header) + 16px) }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap }
a:focus-visible, button:focus-visible { outline: 2px solid var(--ink); outline-offset: 3px }
.draft { background: var(--ink); color: var(--page); font: 500 13px/1.4 var(--mono); letter-spacing: 0.08em; text-transform: uppercase }
.draft .wrap { padding-block: 8px; display: flex; flex-wrap: wrap; gap: 4px 16px; justify-content: space-between }
.draft button { font: inherit; letter-spacing: inherit; text-transform: inherit; color: inherit; background: none; border: 0;
  padding: 0; cursor: pointer; text-decoration: underline; text-underline-offset: 3px }
header.top { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5; background: color-mix(in srgb, var(--page) 92%, transparent);
  backdrop-filter: blur(8px); border-bottom: 1px solid var(--rule) }
header.top .wrap { display: flex; align-items: center; justify-content: space-between; gap: 16px; min-height: var(--header) }
.brand { display: inline-flex; align-items: center; gap: 10px; color: var(--ink); text-decoration: none }
.brand .globe { width: 42px; height: 42px; flex: none; background-size: 1000% 600%; background-position: 0 0;
  background-image: url(img/globe-spin-light.webp);
  background-image: image-set(url(img/globe-spin-light.avif) type("image/avif"), url(img/globe-spin-light.webp) type("image/webp")) }
.brand svg { display: block; height: 22px; width: auto }
nav ul { display: flex; flex-wrap: wrap; gap: 6px 22px; margin: 0; padding: 0; list-style: none }
nav a { color: var(--ink); text-decoration: none; font-size: 15px; font-weight: 500 }
nav a:hover, nav a[aria-current="page"] { text-decoration: underline; text-underline-offset: 4px }
.eyebrow { margin: 0 0 10px; font: 500 13px/1.3 var(--mono); letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted) }
h1 { margin: 0; font-size: clamp(36px, 5.6vw, 72px); line-height: 1.0; font-weight: 600; letter-spacing: -0.03em; text-wrap: balance }
h2 { margin: 0; font-size: clamp(30px, 4vw, 46px); line-height: 1.05; font-weight: 600; letter-spacing: -0.02em; text-wrap: balance }
.lede { margin: 16px 0 0; max-width: 46ch; font-size: 19px }
.head { display: flex; flex-wrap: wrap; gap: 16px 32px; align-items: end; justify-content: space-between; margin-bottom: 32px }
.head p { margin: 10px 0 0; max-width: 58ch; color: var(--muted) }
.hint { font: 500 13px/1.4 var(--mono); letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted) }
.btn { display: inline-flex; align-items: center; gap: 8px; font: 500 15px/1 var(--sans); color: var(--ink); background: transparent;
  border: 1px solid var(--ink); border-radius: 999px; padding: 12px 18px; cursor: pointer; text-decoration: none }
.btn.solid { background: var(--ink); color: var(--page) }
.btn:hover { box-shadow: inset 0 0 0 1px var(--ink) }
.ic { width: 100%; height: 100%; object-fit: contain }
.coin-dot { width: 22px; height: 22px; flex: none; display: inline-block; background: url(img/coins-light.jpg) calc(var(--i) * 100% / 7) 0 / 800% 100%;
  mix-blend-mode: var(--blend) }

/* the hero: the eight on their arc; the title on the photograph's paper sky, in its ink whatever the theme */
.hero { padding-block: 0 28px }
.hero-pic { position: relative }
.hero-photo { position: relative; aspect-ratio: 2 / 1; max-width: 100%; background: #F1EDE8; overflow: hidden }
.hero-photo > picture { display: block; width: 100%; height: 100% }
.hero-photo img { display: block; width: 100%; height: 100%; object-fit: cover }
@media (max-width: 700px) { .hero-photo.has-tall { aspect-ratio: 4 / 5 } }
.hero-title { position: absolute; left: 0; right: 0; top: 0; z-index: 1; color: var(--on-photo); pointer-events: none }
.hero-title .wrap { padding-block: clamp(18px, 2.6vw, 44px) 0 }
.hero-title .eyebrow { color: color-mix(in srgb, var(--on-photo) 68%, transparent) }
.hero-title h1 { font-size: clamp(34px, 5vw, 80px); max-width: none }
.hero-foot { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px 32px; padding-block: 24px 0 }
.hero-foot .lede { margin: 0 }
.acts { display: flex; flex-wrap: wrap; gap: 10px }
.spot { position: absolute; display: block; border-radius: 10px; color: var(--on-photo); text-decoration: none; z-index: 2 }
.spot-label { position: absolute; left: 50%; top: calc(100% + 10px); transform: translate(-50%, -6px); display: inline-flex;
  align-items: center; gap: 8px; padding: 6px 12px 6px 6px; border-radius: 999px; background: var(--veil);
  backdrop-filter: blur(6px); font-size: 15px; white-space: nowrap; opacity: 0; transition: opacity .2s ease, transform .2s ease;
  pointer-events: none }
.spot-label > span:last-child { font: 500 12px/1 var(--mono); letter-spacing: 0.08em; opacity: .7 }
.spot-ic { width: 26px; height: 26px; display: block }
.spot:hover .spot-label, .spot:focus-visible .spot-label { opacity: 1; transform: translate(-50%, 0) }
.spot:focus-visible { outline: 2px solid var(--on-photo); outline-offset: 2px }
.cast { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 18px; margin: 22px 0 0; padding: 18px 0 0; list-style: none;
  border-top: 1px solid var(--rule) }
.cast a { display: inline-flex; align-items: center; gap: 8px; color: var(--ink); text-decoration: none; font-weight: 500; font-size: 15px }
.cast a:hover { text-decoration: underline; text-underline-offset: 4px }
@media (max-width: 860px) {
  .hero-title { position: static; color: var(--ink); pointer-events: auto }
  .hero-title .wrap { padding-block: 26px 18px }
  .hero-title .eyebrow { color: var(--muted) }
  .hero-title h1 { font-size: clamp(32px, 8vw, 44px) }
  .spot-label { display: none }
}
.spot.tall-only { display: none }
@media (max-width: 700px) { .spot.wide-only { display: none } .hero-photo.has-tall .spot.tall-only { display: block } }

/* the horns turning */
.horns { margin: 0; padding: 0; list-style: none; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px }
.horns li { display: grid; gap: 6px }
.horns a { color: var(--ink); font-size: 15px; font-weight: 500; text-decoration: none }
.horns a:hover { text-decoration: underline; text-underline-offset: 4px }
.spin { width: 100%; max-width: 100%; border-radius: 4px; background-size: 600% 400%; background-position: 0 0; background-repeat: no-repeat;
  cursor: grab; touch-action: pan-y }
.spin.dragging { cursor: grabbing }

/* the cards */
.seg { display: inline-flex; border: 1px solid var(--ink); border-radius: 999px; overflow: hidden }
.seg button { font: 500 14px/1 var(--sans); color: var(--ink); background: transparent; border: 0; padding: 10px 16px; cursor: pointer }
.seg button[aria-pressed="true"] { background: var(--ink); color: var(--page) }
.cards { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 18px }
.card { background: var(--panel); color: var(--card-ink); border-radius: 6px; overflow: hidden; display: grid; grid-template-rows: auto 1fr }
.photo { position: relative; display: block; aspect-ratio: 900 / 1827; max-width: 100% }
.photo img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; transition: opacity .35s ease }
.photo .off { opacity: 0 }
.show-off .photo .on { opacity: 0 }
.show-off .photo .off { opacity: 1 }
.about { padding: 14px 16px 18px; display: grid; grid-template-rows: auto auto 1fr auto auto; gap: 4px; min-width: 0 }  /* the line takes the slack, so a row's specs and links align */
.photo { color: var(--card-ink) }
.about .num { margin: 0; display: flex; align-items: center; gap: 8px; font: 500 12px/1.3 var(--mono); letter-spacing: 0.12em; text-transform: uppercase }
.about h3.named { display: flex; align-items: center; gap: 0.3em }
.card-ic { width: 1.15em; height: 1.15em; flex: none; display: block }
.card .card-ic .only-dark { display: none !important }
.card .card-ic .only-light { display: block !important }
.about h3 { margin: 0; font-size: 26px; line-height: 1.1; font-weight: 600; letter-spacing: -0.01em }
.about .line { margin: 0 0 8px; font-size: 15px }
.about dl { margin: 0; display: grid; grid-template-columns: auto 1fr; align-content: start; gap: 2px 12px; font-size: 13px; border-top: 1px solid rgba(26, 25, 23, .25); padding-top: 8px }
.about dt { font: 500 12px/1.5 var(--mono); letter-spacing: 0.08em; text-transform: uppercase; opacity: .82 }
.about dd { margin: 0 }
.about .more { margin-top: 10px; align-self: end; justify-self: start; color: var(--card-ink); font-weight: 600; font-size: 15px; text-underline-offset: 4px }

/* a closer look: one colour at a time on the studio's dark seamless (a launch page's), picked from the coins below */
.closer { background: var(--closer, #0B0B0C); color: #F5F3EF; text-align: center }
.band.closer, .band.closer + .band, .band.lightband, .band.lightband + .band { border-top: 0 }
.closer .eyebrow { color: #9B978F }
.closer-head { display: grid; justify-items: center; margin-bottom: 4px }
.closer-head h2 { max-width: 20ch }
.closer-stage { position: relative; max-width: 100%; margin: 0 auto;
  -webkit-mask-image: linear-gradient(to right, transparent, #000 7%, #000 93%, transparent), linear-gradient(transparent, #000 7%, #000 93%, transparent);
  -webkit-mask-composite: source-in; mask-image: linear-gradient(to right, transparent, #000 7%, #000 93%, transparent),
  linear-gradient(transparent, #000 7%, #000 93%, transparent); mask-composite: intersect }
.closer-stage img { position: absolute; inset: 0; width: 100%; height: 100%; display: block; object-fit: cover; opacity: 0; transition: opacity 520ms ease }
.closer-stage img.on { opacity: 1 }
.picker { display: grid; justify-items: center; gap: 12px; margin-top: 6px }
.dots { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px }
.dots button { width: 44px; height: 44px; padding: 5px; border: 0; border-radius: 50%; background: transparent; cursor: pointer }
.dots button[aria-checked="true"] { box-shadow: inset 0 0 0 2px #F5F3EF }
.dots .coin-dot { width: 100%; height: 100%; display: block; border-radius: 50%; background-image: url(img/coins-dark.jpg); mix-blend-mode: screen }
.closer .picked { margin: 0; color: #9B978F; font-size: 15px } .closer .picked b { color: #F5F3EF; margin-right: 8px; font-weight: 600 }
.closer button:focus-visible { outline-color: #F5F3EF }
.closer.light { color: #1A1917 } .closer.light .eyebrow, .closer.light .picked, .closer.light .lineup figcaption { color: #6B675F }
.closer.light .picked b { color: #1A1917 } .closer.light button:focus-visible { outline-color: #1A1917 }
.macros { list-style: none; margin: 40px 0 0; padding: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; text-align: left }
.macros figure { margin: 0 } .macros img { width: 100%; height: auto; display: block; max-width: 100% }
.macros figcaption { font-size: 14px; line-height: 1.4; margin-top: 8px; color: #9B978F } .closer.light .macros figcaption { color: #6B675F }
@media (max-width: 900px) { .macros { grid-template-columns: repeat(2, minmax(0, 1fr)) } }
.closer.light .dots .coin-dot { background-image: url(img/coins-light.jpg); mix-blend-mode: multiply }
.closer.light .dots button[aria-checked="true"] { box-shadow: inset 0 0 0 2px #1A1917 }
/* a bright field falls off to grey at its corners: feather the frames into the band */
.closer.light .closer-stage, .closer.light .lineup img {
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 5%, #000 95%, transparent), linear-gradient(180deg, transparent, #000 5%, #000 95%, transparent);
  -webkit-mask-composite: source-in;
  mask-image: linear-gradient(90deg, transparent, #000 5%, #000 95%, transparent), linear-gradient(180deg, transparent, #000 5%, #000 95%, transparent);
  mask-composite: intersect }
.lineup { margin: 56px 0 0; display: grid; gap: 12px }
.lineup img { width: 100%; height: auto; display: block; max-width: 100% }
.lineup figcaption { color: #9B978F; font-size: 15px }
@media (max-width: 460px) { .dots { gap: 4px } .dots button { width: 38px; height: 38px; padding: 4px } }
@media (prefers-reduced-motion: reduce) { .closer-stage img { transition: none } }
.facade { margin: 0 0 56px }
.facade img { width: 100%; height: auto; display: block; border-radius: 4px; max-width: 100% }
/* lit from below: the run pins one room. Scrolling picks the colour, a quarter of a screen each, and time plays the change
   (the lamp goes off, the next comes on: no frame mixes two colours); the colour's light spills past the photograph onto
   the page; only the photograph's slow push follows the scroll itself */
@property --glow { syntax: '<color>'; inherits: true; initial-value: transparent }
@property --glow2 { syntax: '<color>'; inherits: true; initial-value: transparent }
.lightband { --ink: #ECE8E1; background: #0B0C10; color: #ECE8E1; padding-block: 0 clamp(56px, 8vw, 112px) }
.lightband .eyebrow, .lightband .num { color: #A39E95 }
.light-head { display: none }
.light-run { position: relative; height: calc(100svh - var(--header) + 8 * 25svh) }
.light-stage { position: sticky; top: calc(var(--header) + env(safe-area-inset-top, 0px)); height: calc(100svh - var(--header));
  display: grid; grid-template-columns: min(58vw, calc(100svh - var(--header))) minmax(0, 1fr); grid-template-rows: 100%;
  overflow: hidden; isolation: isolate; transition: --glow .9s ease, --glow2 .9s ease }
.light-stage.dip { transition-duration: .16s }
.light-glow { position: absolute; inset: 0; z-index: -1; pointer-events: none;
  background: radial-gradient(ellipse 62vw 80% at calc(min(58vw, 100svh - var(--header)) / 2) 58%, var(--glow), var(--glow2) 40%, transparent 72%) }
.light-pic { grid-column: 1; position: relative; margin: 0; width: 100%; height: 100%; max-width: 100%;
  -webkit-mask-image: linear-gradient(to right, transparent, #000 10%, #000 90%, transparent), linear-gradient(to bottom, transparent, #000 8%, #000 86%, transparent);
  -webkit-mask-composite: source-in;
  mask-image: linear-gradient(to right, transparent, #000 10%, #000 90%, transparent), linear-gradient(to bottom, transparent, #000 8%, #000 86%, transparent);
  mask-composite: intersect }
.light-pic img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; scale: var(--push, 1);
  transition: opacity .16s cubic-bezier(.4, 0, 1, 1) }
.light-pic img.on { opacity: 1; transition: opacity .56s cubic-bezier(.16, 1, .3, 1) }
.light-pic.wake img.on { transition-duration: 1.1s }
.light-text { grid-column: 2; display: flex; flex-direction: column; justify-content: space-between; min-width: 0;
  padding: clamp(40px, 9vh, 88px) max(16px, calc((100vw - 1240px) / 2 + 16px)) clamp(40px, 9vh, 88px) clamp(24px, 4vw, 56px) }
.light-intro h2 { font-size: clamp(30px, 3.2vw, 46px) }
.light-intro p:last-child, .light-head p:last-child { margin: 14px 0 0; color: #A39E95; font-size: 17px; line-height: 1.55; max-width: 34ch }
.light-colour .num { margin: 0 0 12px; font: 500 13px/1.3 var(--mono); letter-spacing: 0.14em; text-transform: uppercase }
.light-name { margin: 0; font-size: clamp(56px, 6.6vw, 96px); line-height: .95; font-weight: 600; letter-spacing: -0.035em }
.light-line { margin: 12px 0 0; color: #A39E95; font-size: 18px; line-height: 1.45; max-width: 30ch; min-height: calc(2 * 1.45em) }
.light-name, .light-line, .light-colour .num { transition: opacity .42s cubic-bezier(.16, 1, .3, 1), translate .42s cubic-bezier(.16, 1, .3, 1) }
.light-colour.swap .light-name, .light-colour.swap .light-line, .light-colour.swap .num { opacity: 0; translate: 0 8px; transition-duration: .12s }
.light-coins { position: relative; display: flex; gap: 4px; margin: 28px 0 0 -7px }
.light-coins button { width: 44px; height: 44px; padding: 7px; border: 0; border-radius: 50%; background: transparent; color: #ECE8E1; cursor: pointer; flex: none }
.light-coins .coin-dot { width: 100%; height: 100%; display: block; border-radius: 50%; background-image: url(img/coins-dark.jpg); mix-blend-mode: screen }
.light-coins .ring { position: absolute; left: 0; top: 0; width: 44px; height: 44px; border-radius: 50%; box-shadow: inset 0 0 0 2px #ECE8E1;
  translate: calc(var(--at, 0) * 48px) 0; transition: translate .36s cubic-bezier(.2, .8, .2, 1); pointer-events: none }
.light-coins button:focus-visible { outline: 2px solid #ECE8E1; outline-offset: 2px }
.lightband .facade { margin: 0; opacity: .15; transition: opacity 1.2s ease;
  -webkit-mask-image: linear-gradient(to bottom, transparent, #000 12%, #000 88%, transparent); mask-image: linear-gradient(to bottom, transparent, #000 12%, #000 88%, transparent) }
.lightband .facade.seen { opacity: 1 }
.lightband .facade img { width: 100%; height: auto; display: block; border-radius: 0; max-width: 100% }
@media (max-width: 860px) {
  .light-head { display: block; padding-block: 56px 24px }
  .light-head h2 { font-size: clamp(30px, 8vw, 40px) }
  .light-intro { display: none }
  .light-stage { grid-template-columns: minmax(0, 1fr); grid-template-rows: auto minmax(0, 1fr) }
  .light-glow { background: radial-gradient(ellipse 90vw 60% at 50% 48%, var(--glow), var(--glow2) 45%, transparent 80%) }
  .light-pic { grid-column: 1; height: min(125vw, calc(100svh - var(--header) - 200px));
    -webkit-mask-image: linear-gradient(to bottom, transparent, #000 7%, #000 84%, transparent); -webkit-mask-composite: source-over;
    mask-image: linear-gradient(to bottom, transparent, #000 7%, #000 84%, transparent); mask-composite: add }
  .light-pic img { object-position: 50% 55% }
  .light-text { grid-column: 1; justify-content: end; padding: 0 max(16px, env(safe-area-inset-right, 0px)) 20px max(16px, env(safe-area-inset-left, 0px)) }
  .light-colour .num { display: none }
  .light-name { font-size: 40px; line-height: 1 }
  .light-line { font-size: 17px; line-height: 1.4; margin-top: 8px; min-height: calc(2 * 1.4em) }
  .light-coins { margin: 14px 0 0; justify-content: space-between; gap: 0 }
  .light-coins .ring { translate: calc(var(--at, 0) * (100vw - 32px - 44px) / 7) 0 }
}
@media (prefers-reduced-motion: reduce) {
  .light-run { height: auto } .light-stage { position: relative; top: 0; transition: none }
  .light-pic img, .light-pic img.on, .light-pic.wake img.on { transition: opacity .15s linear; scale: 1 }
  .light-name, .light-line, .light-coins .ring { transition: none }
  .lightband .facade { opacity: 1; transition: none }
}
/* the header over the dark band */
header.top { transition: background-color .3s ease, border-color .3s ease }
header.top.on-dark { background: rgb(11 12 16 / .92); backdrop-filter: blur(20px); border-bottom-color: rgb(255 255 255 / .06) }
header.top.on-dark .brand, header.top.on-dark nav a { color: #ECE8E1 }
header.top.on-dark .brand .globe { background-image: url(img/globe-spin-dark.webp);
  background-image: image-set(url(img/globe-spin-dark.avif) type("image/avif"), url(img/globe-spin-dark.webp) type("image/webp")) }
/* the habitats: one campaign picture at a time, snapping along a strip (the portraits on phones) */
#habitats { overflow-x: clip }
#habitats > .wrap { container-type: inline-size }
.hab-frame { position: relative; --col: min(86cqw, 1080px); --mid: calc(var(--col) / 3); margin-right: calc(50cqw - 50vw) }
.hab-frame .nav { top: var(--mid); transition: opacity .2s ease }
.hab-frame .nav.prev { left: 14px } .hab-frame .nav.next { right: auto; left: calc(var(--col) - 58px) }
.hab-frame .nav[aria-disabled="true"] { opacity: 0; pointer-events: none }
.habitats { list-style: none; margin: 0; padding: 0 0 6px; display: grid; grid-auto-flow: column; grid-auto-columns: var(--col);
  gap: 20px; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; overscroll-behavior-x: contain; padding-right: 96px;
  -webkit-mask-image: linear-gradient(90deg, #000 calc(100% - 96px), transparent); mask-image: linear-gradient(90deg, #000 calc(100% - 96px), transparent) }
.habitats::-webkit-scrollbar { display: none }
.habitats li { scroll-snap-align: start; min-width: 0 }
.habitats a { display: grid; gap: 10px; color: var(--ink); text-decoration: none; font-size: 15px }
.habitats a span { color: var(--muted) } .habitats a b { color: var(--ink); font-weight: 600; margin-right: 6px }
.habitats img { width: 100%; height: auto; display: block; border-radius: 4px }
.habitats:focus-visible { outline: 2px solid var(--ink); outline-offset: 4px }
@media (max-width: 700px) { .hab-frame { --col: 84cqw; --mid: calc(var(--col) * 0.625) }
  .habitats { padding-right: 40px; -webkit-mask-image: linear-gradient(90deg, #000 calc(100% - 40px), transparent); mask-image: linear-gradient(90deg, #000 calc(100% - 40px), transparent) } }
.room figure { margin: 0; display: grid; gap: 14px }
.room img { width: 100%; height: auto; display: block; max-width: 100% }
.room figcaption { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 6px 24px; font-size: 15px; color: var(--muted); width: 100% }
.spec-grid { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); gap: 40px; align-items: start }
.spec dl, .facts { margin: 0; display: grid; grid-template-columns: 150px minmax(0, 1fr); border-top: 2px solid var(--ink) }
.spec dt, .spec dd, .facts dt, .facts dd { padding: 10px 0; border-bottom: 1px solid var(--rule) }
.spec dt, .facts dt { font: 500 13px/1.5 var(--mono); letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted) }
.spec dd, .facts dd { margin: 0 }
.dwg { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 12px 20px; background: #F7F5F1; border-radius: 4px; padding: 18px; margin: 0; max-width: 620px }
.dwg img { min-width: 0; width: 0; height: auto; display: block; mix-blend-mode: multiply }
.dwg figcaption { flex: 1 0 100%; font: 500 12px/1.4 var(--mono); letter-spacing: 0.1em; text-transform: uppercase; color: #5E5A53 }
.next { display: grid; gap: 14px }
.next p { margin: 0; max-width: 60ch; color: var(--muted) }
/* the lamps: the pair side by side, each a tall picture over its name, line and particulars; the eight in a row;
   the cartridge and the lamps switched off beneath (round 32f's catch, black on black, is left out) */
.lamp-pair { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px }
.lamp { display: grid; gap: 12px; align-content: start; min-width: 0 }
.lamp img, .eight img, .lamp-duo img { width: 100%; height: auto; display: block; border-radius: 6px; background: #F1EDE8; max-width: 100% }
.lamp h3 { margin: 4px 0 0; display: flex; align-items: baseline; gap: 12px; font-size: 26px; line-height: 1.1; font-weight: 600; letter-spacing: -0.01em }
.lamp h3 small { font: 500 12px/1.3 var(--mono); letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted) }
.lamp .line { margin: 0 0 6px; color: var(--muted); max-width: 52ch }
.eight { margin: 32px 0 0; display: grid; gap: 12px }
.lamp-duo { display: grid; grid-template-columns: 15fr 8fr; gap: 24px; margin-top: 24px; align-items: start }   /* 3:2 and 4:5 at one height */
.lamp-duo figure { margin: 0; display: grid; gap: 10px; min-width: 0 }
.eight figcaption, .lamp-duo figcaption { font-size: 15px; color: var(--muted) }
@media (max-width: 720px) { .lamp-pair, .lamp-duo { grid-template-columns: minmax(0, 1fr) } }
.pair { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; margin-top: 14px }
.pair figure { margin: 0; display: grid; gap: 10px }
.pair img { width: 100%; height: auto; display: block; border-radius: 4px; max-width: 100% }
.pair figcaption { font-size: 15px; color: var(--muted) } .pair figcaption b { color: var(--ink); font-weight: 600; margin-right: 6px }
@media (max-width: 720px) { .pair { grid-template-columns: 1fr } }
.contact { display: grid; gap: 18px }
.contact .addr { display: flex; flex-wrap: wrap; align-items: center; gap: 12px }
.contact code { font: 500 clamp(20px, 3vw, 30px)/1.2 var(--mono); user-select: all; word-break: break-all }
.contact small { color: var(--muted); font-size: 14px }
footer { padding-block: 40px 56px; border-top: 1px solid var(--rule) }
footer .wrap { display: flex; flex-wrap: wrap; gap: 18px 32px; align-items: center; justify-content: space-between }
footer p { margin: 0; font: 500 12px/1.5 var(--mono); letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted) }

/* a speaker's page */
.crumbs { padding-block: 22px 0; font-size: 15px; color: var(--muted) }
.crumbs a { color: var(--ink); text-underline-offset: 4px }
.pdp { display: grid; grid-template-columns: minmax(0, 1.62fr) minmax(0, 0.82fr); gap: 40px; align-items: start; padding-block: 18px 64px }
.gallery { display: grid; gap: 12px; min-width: 0 }
/* the pictures, one at a time on a stage the photograph's shape (3:2, and 4:5 on phones), each carried to the stage's
   edges on its own ground: the colours down its sides, or above and below it */
.frame { position: relative; min-width: 0 }
.stage { position: relative; aspect-ratio: 3 / 2; width: 100%; max-width: 100%; container-type: size; display: grid; place-items: center;
  overflow: hidden; border-radius: 6px; background: var(--paper); touch-action: pan-y; -webkit-user-select: none; user-select: none }
.stage:focus-visible { outline: 2px solid var(--ink); outline-offset: 3px }
.stage > * { grid-area: 1 / 1; position: relative; z-index: 1 }   /* the picture over its blurred fill, explicitly */
.stage > .blur { z-index: 0 }
.stage .fill, .stage .fill img { width: 100%; height: 100%; display: block; object-fit: cover }
.stage .fit { width: min(100cqw, calc(100cqh * var(--ar))); max-width: 100%; aspect-ratio: var(--ar); height: auto; display: block; border-radius: 0;
  -webkit-user-drag: none;
  -webkit-mask-image: linear-gradient(to right, transparent, #000 3%, #000 97%, transparent), linear-gradient(transparent, #000 3%, #000 97%, transparent);
  -webkit-mask-composite: source-in; mask-image: linear-gradient(to right, transparent, #000 3%, #000 97%, transparent),
  linear-gradient(transparent, #000 3%, #000 97%, transparent); mask-composite: intersect }
.stage .fit.cut { align-self: end;
  -webkit-mask-image: linear-gradient(to right, transparent, #000 3%, #000 97%, transparent), linear-gradient(transparent, #000 3%);
  mask-image: linear-gradient(to right, transparent, #000 3%, #000 97%, transparent), linear-gradient(transparent, #000 3%) }
.stage .blur { width: 100%; height: 100%; background: center / cover no-repeat; filter: blur(28px) saturate(1.1); transform: scale(1.15) }
.stage .in { animation: g-in 0.24s ease-out }
@keyframes g-in { from { opacity: 0 } }
.stage .tag { position: absolute; z-index: 2; left: 12px; bottom: 12px; font: 500 12px/1 var(--mono); letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--on-photo); background: var(--veil); border-radius: 999px; padding: 7px 10px }
.nav { position: absolute; top: 50%; translate: 0 -50%; z-index: 2; width: 44px; height: 44px; border-radius: 50%; border: 0; padding: 0;
  display: grid; place-items: center; color: var(--on-photo); background: var(--veil); cursor: pointer; box-shadow: 0 1px 8px rgba(0, 0, 0, 0.14) }
.nav.prev { left: 12px } .nav.next { right: 12px }
.nav svg { width: 18px; height: 18px; display: block }
.nav:hover { box-shadow: inset 0 0 0 1.5px var(--on-photo), 0 1px 8px rgba(0, 0, 0, 0.14) }
.nav:focus-visible { outline: 2px solid var(--ink); outline-offset: 2px }
.count { position: absolute; right: 12px; bottom: 12px; z-index: 2; font: 500 12px/1 var(--mono); letter-spacing: 0.08em; color: var(--on-photo);
  background: var(--veil); border-radius: 999px; padding: 7px 10px; pointer-events: none }
.thumbs { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(56px, 84px); gap: 8px; overflow-x: auto; scrollbar-width: none;
  padding: 4px; margin: -4px; position: relative; scroll-snap-type: x proximity }
.thumbs::-webkit-scrollbar { display: none }
.thumb { aspect-ratio: 1; border-radius: 4px; border: 1px solid var(--rule); padding: 0; cursor: pointer; background-color: var(--paper);
  scroll-snap-align: start; opacity: 0.8; transition: opacity 0.15s }
.thumb:hover, .thumb[aria-selected="true"] { opacity: 1 }
.thumb[aria-selected="true"] { outline: 2px solid var(--ink); outline-offset: 2px }
.cap { margin: 0; color: var(--muted); font-size: 15px; max-width: 62ch }
.buy { position: sticky; top: calc(var(--header) + 24px); display: grid; gap: 18px; min-width: 0; background: var(--page) }
.buy .num { margin: 0; display: flex; align-items: center; gap: 10px; font: 500 13px/1.3 var(--mono); letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted) }
.buy h1.named { display: flex; align-items: center; gap: 0.3em }
.buy h1 .pic { width: 1.05em; height: 1.05em; flex: none; display: block }
.buy h1 { font-size: clamp(40px, 5vw, 64px) }
.buy .line { margin: 0; font-size: 18px }
.price { margin: 0; font-size: 20px; font-weight: 600 }
.price span { font-weight: 400; color: var(--muted); font-size: 16px }
.swatches { display: flex; flex-wrap: wrap; gap: 8px; margin: 0; padding: 0; list-style: none }
.swatches a { display: block; width: 40px; height: 40px; border-radius: 50%; position: relative }
.swatches a[aria-current="true"] { outline: 2px solid var(--ink); outline-offset: 3px }
.swatches .coin-dot { width: 100%; height: 100%; display: block }
.pick { margin: -6px 0 0; font-size: 15px; color: var(--muted) }
.pick b { color: var(--ink) }
.acts { display: flex; flex-wrap: wrap; gap: 10px }
.facts { grid-template-columns: 120px minmax(0, 1fr); font-size: 15px }
.goes-head { display: flex; flex-wrap: wrap; align-items: baseline; justify-content: space-between; gap: 6px 20px; margin: 0 0 14px;
  border-top: 2px solid var(--ink); padding-top: 14px }
.goes-head h2 { font-size: 24px }
.goes-head span { font-size: 14px; color: var(--muted) }
.goes { display: grid; grid-template-columns: repeat(2, minmax(0, 380px)); gap: 16px }
.good { margin: 0; display: grid; gap: 8px; align-content: start }
.good .art { aspect-ratio: 4 / 3; display: grid; place-items: center; border-radius: 6px; background: var(--paper) }
.good .art svg { width: 78%; height: auto; display: block }
.good b { font-size: 18px; font-weight: 600 }
.good .way { font-size: 15px } .good .way i { font-style: normal; color: var(--muted) }
.good p { margin: 0; font-size: 14px; color: var(--muted); max-width: 40ch }
.good .chip { display: inline-flex; align-items: center; gap: 7px; font-size: 14px }
.good .chip .dot { width: 12px; height: 12px; border-radius: 50%; background: var(--c); box-shadow: inset 0 0 0 1px var(--ring); display: inline-block }
.others { padding-block: 48px 72px }
.others ul { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 12px; margin: 0; padding: 0; list-style: none }
.others a { display: grid; gap: 8px; color: var(--ink); text-decoration: none; font-weight: 500; font-size: 15px }
.others img { width: 100%; height: auto; aspect-ratio: 900 / 1827; object-fit: cover; border-radius: 4px; display: block; max-width: 100% }
.others a:hover span { text-decoration: underline; text-underline-offset: 4px }

/* the opening: the acrylic globe large in the middle of a plain ground, turning, flies and shrinks onto the header's
   globe while the ground, a circle on the globe, closes in behind it. The ground is the render's own paper as its film
   decodes (#F1ECE7), or on a dark system the night render's black (#100F12), so the film's edge never shows; shown only
   when the page's first script asks for it */
.splash, .flyer { display: none }
html.intro.night { background: #100F12 }                              /* so nothing pale shows before the ground is drawn */
html.intro .splash { display: block; position: fixed; inset: 0; z-index: 50; background: #F1ECE7 }
html.intro.night .splash, html.night .flyer video { background: #100F12 }
html.intro .flyer { --big: min(36vmin, 200px); display: block; position: fixed; z-index: 51; left: 50%; top: 50%;
  width: var(--big); height: var(--big); margin: calc(var(--big) / -2) 0 0 calc(var(--big) / -2) }
.flyer video { display: block; width: 100%; height: 100%; object-fit: cover; clip-path: circle(50%); background: #F1ECE7 }
html.intro .brand .globe { visibility: hidden }                       /* the flying globe lands on it, then hands over */
.hero-photo img { transition: opacity .5s ease }
html.opening .hero-photo img { opacity: 0 }
/* the cursor: a dot where the pointer is and a ring that follows it, opening over anything to press, tinted with the
   speaker it leads to; the dot takes the colour of the text beneath it, so it reads on paper, photographs and the dark */
.cur { position: fixed; left: 0; top: 0; z-index: 70; pointer-events: none; border-radius: 50%; opacity: 0; transition: opacity .25s ease }
html.cursor .cur { opacity: 1 }
html.cursor, html.cursor * { cursor: none !important }
.cur-dot { width: 6px; height: 6px; margin: -3px 0 0 -3px; background: var(--cur, var(--ink)) }
.cur-ring { width: 34px; height: 34px; margin: -17px 0 0 -17px;
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--cur, var(--ink)) 38%, transparent);
  transition: width .32s cubic-bezier(.2, .7, .2, 1), height .32s cubic-bezier(.2, .7, .2, 1), margin .32s cubic-bezier(.2, .7, .2, 1),
    background-color .3s ease, box-shadow .3s ease, opacity .25s ease }
.cur-ring.on { width: 54px; height: 54px; margin: -27px 0 0 -27px; background: color-mix(in srgb, var(--tint, var(--ink)) 20%, transparent);
  box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--tint, var(--ink)) 70%, transparent) }
.cur-ring.drag::before, .cur-ring.drag::after { content: ""; position: absolute; top: 50%; width: 6px; height: 6px; margin-top: -3px;
  border: solid var(--cur, var(--ink)); border-width: 0 0 1.5px 1.5px }
.cur-ring.drag::before { left: 8px; transform: rotate(45deg) }
.cur-ring.drag::after { right: 8px; transform: rotate(-135deg) }
@media (prefers-reduced-motion: reduce) { html.intro .splash, html.intro .flyer { display: none } html.opening .hero-photo img { opacity: 1 } }

@media (max-width: 1000px) { .cards { grid-template-columns: repeat(2, minmax(0, 1fr)) } .spec-grid { grid-template-columns: 1fr }
  .pdp { grid-template-columns: 1fr } .buy { position: static } .others ul { grid-template-columns: repeat(4, minmax(0, 1fr)) } }
@media (max-width: 720px) {
  .horns { grid-template-columns: repeat(2, minmax(0, 1fr)) }
  nav ul { gap: 4px 14px } nav a { font-size: 14px }
  .band { padding-block: 52px }
  .goes { grid-template-columns: 1fr } .good .art { aspect-ratio: 16 / 9 }
  .brand svg { height: 18px } .brand .globe { width: 36px; height: 36px }
}
@media (max-width: 700px) { .stage { aspect-ratio: 4 / 5 } .nav { width: 40px; height: 40px } .nav.prev { left: 8px } .nav.next { right: 8px }
  .count { right: 8px; bottom: 8px } .stage .tag { left: 8px; bottom: 8px } }
@media (max-width: 460px) { .cards { gap: 12px } .about h3 { font-size: 21px } .about dl { display: none }
  .spec dl, .facts { grid-template-columns: minmax(0, 1fr) } .spec dt, .facts dt { padding: 10px 0 0; border-bottom: 0 }
  .spec dd, .facts dd { padding: 2px 0 10px } .swatches { gap: 6px } .swatches a { width: 36px; height: 36px }
  nav li.wide { display: none } }
@media (prefers-reduced-motion: reduce) { .photo img, .spot-label, .thumb { transition: none } .stage .in { animation: none } }
</style>

<div class="splash" aria-hidden="true"></div>
<div class="flyer" role="progressbar" aria-label="Loading"><video muted playsinline loop autoplay preload="auto" aria-hidden="true" tabindex="-1"></video></div>
<script>(function (d, v) { if (!d.classList.contains('intro')) return;     // the day's film or the night's, and only that one fetched
  const night = d.classList.contains('night'), f = night ? 'globe-turn-night' : 'globe-turn';
  v.poster = night ? '__POSTER_NIGHT__' : '__POSTER__';
  v.innerHTML = `<source src="img/${f}.webm" type='video/webm; codecs="vp9"'><source src="img/${f}.mp4" type="video/mp4">`;
})(document.documentElement, document.querySelector('.flyer video'))</script>
<noscript><style>html.opening .hero-photo img { opacity: 1 }</style></noscript>
<header class="top"><div class="wrap">
  <a class="brand" href="#top" aria-label="EARF, home"><span class="globe" aria-hidden="true"></span>__WORD__</a>
  <nav aria-label="Pages"><ul>
    <li><a href="#atmosphere">Colours</a></li><li><a href="#turn">The horn</a></li><li class="wide"><a href="#spec">Details</a></li>
    __LAMPS_NAV__<li><a href="#contact">Enquire</a></li>
  </ul></nav>
</div></header>

<main id="home">
  <section class="hero" id="top">
    <div class="hero-pic">
      <div class="hero-title"><div class="wrap"><p class="eyebrow">EARF &middot; Atmosphere</p><h1>Something in the air.</h1></div></div>
      <div class="hero-photo__HERO_CLASS__">
        <picture>__HERO_TALL__<img src="img/hero.jpg" fetchpriority="high" srcset="img/hero-1200.jpg 1200w, img/hero.jpg 2400w" sizes="100vw" width="2400" height="1200"
          alt="The eight Atmosphere speakers on a curve, their covers off: red through violet, then the clear Fog and the smoked Smoke, each throwing its colour on the floor"></picture>
        __HOTSPOTS__
      </div>
    </div>
    <div class="wrap hero-foot">
      <p class="lede">Atmosphere is a horn loudspeaker cast in tinted acrylic, in eight colours from Ember to Smoke.</p>
      <div class="acts"><a class="btn solid" href="#atmosphere">The colours</a><a class="btn" href="#contact">Enquire</a></div>
    </div>
    <div class="wrap"><ul class="cast" aria-label="The eight, in spectrum order">__NAMES__</ul></div>
  </section>

__CLOSER__

  <section class="band" id="turn"><div class="wrap">
    <div class="head">
      <div><p class="eyebrow">The horn</p><h2>The oldest amplifier is a shape.</h2>
        <p>Long before there were amplifiers, a horn was how a small sound filled a large room: the gramophone&rsquo;s, the
          megaphone&rsquo;s, a cupped hand&rsquo;s. Ours is cast in resin tinted to match its cabinet, and its driver lives in a
          pod whose cap twists off by hand.</p></div>
    </div>
    <ul class="horns" id="horns">__TURN__</ul>
  </div></section>

  <section class="band" id="atmosphere"><div class="wrap">
    <div class="head">
      <div><p class="eyebrow">The colours</p><h2>Choose your atmosphere.</h2>
        <p>Each cabinet is cast acrylic, 20 mm thick and tinted all the way through. The lining shows through the walls,
          so we dressed it in white voile.</p></div>
      <div class="seg" role="group" aria-label="The speakers' covers">
        <button type="button" id="cover-off" aria-pressed="true">Cover off</button>
        <button type="button" id="cover-on" aria-pressed="false">Cover on</button>
      </div>
    </div>
    <div class="cards show-off" id="cards">__CARDS__</div>
  </div></section>

__REEL__
__HABITATS__
  <section class="band room" id="room">
    <div class="wrap"><div class="head"><div><p class="eyebrow">At home</p><h2>A pair in Poison.</h2></div></div></div>
    <figure><picture>__ROOM_TALL__<img src="img/room.jpg" srcset="img/room-1440.jpg 1440w, img/room.jpg 2880w" sizes="100vw" width="2880" height="1620" alt="Two green speakers either side of a walnut sideboard with a record player, low sun from a tall window on the left" loading="lazy"></picture>
      <figcaption class="wrap"><span>Covers on, by a tall window.</span><span>Each stands 1293&nbsp;mm tall and 560&nbsp;mm wide.</span></figcaption></figure>
  </section>

  <section class="band spec" id="spec"><div class="wrap">
    <div class="head"><div><p class="eyebrow">Details</p><h2>The particulars</h2></div></div>
    <div class="spec-grid">
      <dl>__SPEC__</dl>
      <figure class="dwg">__DWG__
        <figcaption>From the fabrication drawings</figcaption></figure>
    </div>
  </div></section>

__NEXT__

  <section class="band" id="contact"><div class="wrap contact">
    <p class="eyebrow">Enquiries</p>
    <h2>Prices, pairs and partnerships.</h2>
    <p>Everything here is made to order, so we quote rather than list. Write for prices and lead times, or if you&rsquo;d like to
      make, stock or collaborate.</p>
    <div class="addr"><code id="addr">hello@earf.world</code><button type="button" class="btn" id="copy">Copy address</button></div>
    <small id="copy-note">The inbox opens at launch.</small>
  </div></section>
</main>

<main id="pdp" hidden>
  <div class="wrap">
    <p class="crumbs"><a href="#atmosphere">Atmosphere</a> / <span id="p-crumb"></span></p>
    <div class="pdp">
      <section class="gallery" aria-label="Pictures">
        <div class="frame">
          <div class="stage" id="stage" role="tabpanel" aria-labelledby="thumb-0" tabindex="0"></div>
          <button type="button" class="nav prev" id="g-prev" aria-label="Previous picture"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M11.5 3.5 6 9l5.5 5.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
          <button type="button" class="nav next" id="g-next" aria-label="Next picture"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M6.5 3.5 12 9l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
          <span class="count" id="g-count" aria-hidden="true"></span>
        </div>
        <div class="thumbs" id="thumbs" role="tablist" aria-label="Pictures of this speaker"></div>
        <p class="cap" id="cap" aria-live="polite"></p>
      </section>
      <aside class="buy" aria-label="This speaker">
        <p class="num"><span id="p-num"></span></p>
        <h1 class="named"><span id="p-name"></span><span class="pic" id="p-icon"></span></h1>
        <p class="line" id="p-line"></p>
        <p class="price">Price on request <span>&middot; each pair made to order</span></p>
        <ul class="swatches" id="swatches" aria-label="Colour"></ul>
        <p class="pick">Colour: <b id="p-pick"></b></p>
        <div class="acts"><a class="btn solid" href="#contact">Enquire about a pair</a></div>
        <dl class="facts" id="facts"></dl>
      </aside>
    </div>
__GOES__    <section class="others" aria-labelledby="others-title">
      <div class="goes-head"><h2 id="others-title">The other seven</h2><span>Same speaker, a different air</span></div>
      <ul id="others"></ul>
    </section>
  </div>
</main>

<footer><div class="wrap">
  <a class="brand" href="#top" aria-label="EARF, home">__WORD__</a>
  <p>Atmosphere horn loudspeakers &middot; In development, not yet for sale; the pictures are renders &middot; &copy; 2026 EARF</p>
</div></footer>

<script>
const D = __DATA__, BY = Object.fromEntries(D.clouds.map(c => [c.k, c]));
const SLUG = Object.fromEntries(D.clouds.map(c => [c.name.toLowerCase(), c.k])), keyOf = w => SLUG[w] || (BY[w] ? w : null);
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, TAU = Math.PI * 2;
// lit from below: scrolling picks the colour (a quarter of a screen each) and time plays the change; the coins are a
// radio group that switch the lamp and move the run to that colour; the header darkens over the band
const run = document.getElementById('light-run');
if (run) {
  const stageL = run.querySelector('.light-stage'), fig = run.querySelector('.light-pic'), pics = [...fig.querySelectorAll('img')];
  const coins = [...run.querySelectorAll('.light-coins button')], group = run.querySelector('.light-coins'), colour = run.querySelector('.light-colour');
  const nameEl = document.getElementById('light-name'), lineEl = document.getElementById('light-line'), numEl = document.getElementById('light-num');
  const N = pics.length, OFF = reduce ? 0 : 160, ON = reduce ? 150 : 560;
  let at = -1, want = 0, busy = false, woke = false, quiet = false, quietT = 0, queuedL = false;
  const glowOf = i => { const b = coins[i], a = 0.30 * +b.dataset.a; return [`rgb(${b.dataset.glow} / ${a.toFixed(3)})`, `rgb(${b.dataset.glow} / ${(a * 0.45).toFixed(3)})`]; };
  const light = (i, dim) => { const [g1, g2] = glowOf(i); stageL.classList.toggle('dip', dim);
    stageL.style.setProperty('--glow', dim ? 'transparent' : g1); stageL.style.setProperty('--glow2', dim ? 'transparent' : g2); };
  const mark = i => { group.style.setProperty('--at', i); coins.forEach((b, j) => { b.setAttribute('aria-checked', String(j === i)); b.tabIndex = j === i ? 0 : -1; }); };
  function show(i) {                                  // one switch at a time, then straight to the latest
    want = i; mark(i);
    if (busy || i === at) return;
    busy = true; const prev = at; at = i;
    if (prev >= 0) { pics[prev].classList.remove('on'); light(prev, true); colour.classList.add('swap'); }
    setTimeout(() => {
      const c = D.clouds[i]; nameEl.textContent = c.name; lineEl.textContent = c.line; numEl.textContent = `Atmosphere ${c.num}`;
      colour.classList.remove('swap'); pics[i].classList.add('on'); light(i, false);
      setTimeout(() => { busy = false; if (want !== at) show(want); }, ON);
    }, prev >= 0 ? OFF : 0);
  }
  const pinTop = () => parseFloat(getComputedStyle(stageL).top) || 0;
  const span = () => Math.max(1, run.offsetHeight - stageL.offsetHeight);
  const zoneAt = () => { const y = pinTop() - run.getBoundingClientRect().top, s = span();
    fig.style.setProperty('--push', (1 + 0.06 * Math.min(1, Math.max(0, y / s))).toFixed(4));
    let i = Math.min(N - 1, Math.max(0, Math.floor(y / (s / N))));
    if (i !== want) { const edge = (i > want ? i : i + 1) * s / N; if (Math.abs(y - edge) < 16) i = want; }   // a little hysteresis
    return i; };
  const tickL = () => { queuedL = false; const i = zoneAt(); if (woke && !quiet && i !== want) show(i); };
  if (!reduce) {
    addEventListener('scroll', () => { if (!queuedL) { queuedL = true; requestAnimationFrame(tickL); } }, { passive: true });
    addEventListener('resize', tickL);
  }
  // Ember is lit in the page itself (without script, and under reduced motion); on the moving path the room starts dark
  // and, when it is well in view, the first lamp comes up slowly
  if (reduce) { at = 0; light(0, false); woke = true; }
  else {
    pics[0].classList.remove('on');
    new IntersectionObserver((es, ob) => { if (!es.some(e => e.isIntersecting)) return; ob.disconnect(); woke = true;
      fig.classList.add('wake'); show(zoneAt()); setTimeout(() => fig.classList.remove('wake'), 1300); }, { threshold: 0.35 }).observe(stageL);
  }
  const jump = i => { show(i); if (reduce || !woke) return;
    const r = run.getBoundingClientRect(), s = span(), pinned = r.top <= pinTop() + 1 && r.bottom >= innerHeight - 1;
    quiet = true; clearTimeout(quietT);
    scrollTo({ top: scrollY + r.top - pinTop() + (i + 0.5) * s / N, behavior: pinned ? 'instant' : 'smooth' });
    const done = () => { quiet = false; removeEventListener('scrollend', done); };
    if (pinned) quietT = setTimeout(done, 80); else { addEventListener('scrollend', done, { once: true }); quietT = setTimeout(done, 1400); } };
  coins.forEach((b, i) => b.addEventListener('click', () => jump(i)));
  group.addEventListener('keydown', e => { const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key];
    const i = k ? (want + k + N) % N : e.key === 'Home' ? 0 : e.key === 'End' ? N - 1 : -1;
    if (i < 0) return; e.preventDefault(); jump(i); coins[i].focus(); });
  const fac = document.querySelector('.lightband .facade');
  if (fac) new IntersectionObserver((es, ob) => { if (es.some(e => e.isIntersecting)) { fac.classList.add('seen'); ob.disconnect(); } }, { threshold: 0.35 }).observe(fac);
  const band = document.getElementById('light'), bar = document.querySelector('header.top');
  if (band && bar) { const over = () => { const r = band.getBoundingClientRect(), h = bar.getBoundingClientRect().bottom;
      bar.classList.toggle('on-dark', r.top <= h + 1 && r.bottom > h); };
    addEventListener('scroll', over, { passive: true }); over(); }
}
// a closer look: the dots pick a colour and the pictures cross-fade; the arrow keys step through them, as in a radio group
const closer = document.getElementById('closer');
if (closer) {
  const pics = [...closer.querySelectorAll('.closer-stage img')], dots = [...closer.querySelectorAll('.dots button')];
  let at = 0;
  const pick = (i, focus) => { at = i; const c = D.clouds[i];
    pics.forEach((p, j) => { p.classList.toggle('on', j === i); if (j === i) p.removeAttribute('aria-hidden'); else p.setAttribute('aria-hidden', 'true'); });
    dots.forEach((d, j) => { d.setAttribute('aria-checked', String(j === i)); d.tabIndex = j === i ? 0 : -1; if (j === i && focus) d.focus(); });
    document.getElementById('closer-cap').innerHTML = `<b>${c.name}</b> ${c.line}`; };
  dots.forEach((d, i) => d.addEventListener('click', () => pick(i)));
  closer.querySelector('.dots').addEventListener('keydown', e => { const k = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: 7, ArrowUp: 7 }[e.key];
    if (k) { e.preventDefault(); pick((at + k) % 8, true); } });
}
// the habitats' strip: the arrows move it a picture at a time
const hab = document.getElementById('hab');
if (hab) {
  const prev = document.getElementById('hab-prev'), next = document.getElementById('hab-next');
  const step = d => { const li = hab.querySelector('li'); hab.scrollBy({ left: d * (li.offsetWidth + 20), behavior: reduce ? 'auto' : 'smooth' }); };
  const ends = () => { prev.setAttribute('aria-disabled', String(hab.scrollLeft < 8));
    next.setAttribute('aria-disabled', String(hab.scrollLeft > hab.scrollWidth - hab.clientWidth - 8)); };
  prev.addEventListener('click', () => step(-1)); next.addEventListener('click', () => step(1));
  hab.addEventListener('scroll', ends, { passive: true }); addEventListener('resize', ends); ends();
}
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const el = (tag, attrs = {}, html = '') => { const e = document.createElement(tag); for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v); e.innerHTML = html; return e; };

// the header's globe keeps turning: a turn every 4 s through its 60 frames, on one clock, which the opening's globe sets
// as it lands so the turn carries on from the film's own angle; still under reduced motion
const GLOBES = [...document.querySelectorAll('.brand .globe')], GLOBE_TURN = 4000;
let turn0 = performance.now(), globeAt = -1;
const setTurn = sec => { turn0 = performance.now() - (sec * 1000) % GLOBE_TURN; };
if (!reduce) (function globeTurn(now) {
  const i = Math.floor((((now - turn0) % GLOBE_TURN) + GLOBE_TURN) % GLOBE_TURN / GLOBE_TURN * 60) % 60;
  if (i !== globeAt) { globeAt = i; GLOBES.forEach(g => { g.style.backgroundPosition = `${(i % 10) * 100 / 9}% ${Math.floor(i / 10) * 100 / 5}%`; }); }
  requestAnimationFrame(globeTurn);
})(turn0);

// the horns turn once as they cross the screen, a frame every 15 degrees; dragged, they turn by hand
const TILES = [...document.querySelectorAll('#horns .spin')], N = 24, C = 6, R = 4;
const lend = t => { if (t.dataset.bg) { t.style.backgroundImage = `url(${t.dataset.bg})`; delete t.dataset.bg; } };
if ('IntersectionObserver' in window) { const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { lend(e.target); io.unobserve(e.target); } }),
  { rootMargin: '900px 0px' }); TILES.forEach(t => io.observe(t)); } else TILES.forEach(lend);
const frameAt = (k) => `${(k % C) * 100 / (C - 1)}% ${Math.floor(k / C) * 100 / (R - 1)}%`;
const drag = new Map();
function turnUpdate() {
  const vh = innerHeight;
  for (const t of TILES) {
    const r = t.getBoundingClientRect();
    if (r.bottom < -vh || r.top > 2 * vh) continue;
    const p = reduce ? 0 : Math.min(0.9999, Math.max(0, (vh - r.top) / (vh + r.height)));
    const k = ((Math.floor(p * N) + (drag.get(t) || 0)) % N + N) % N;
    if (t._k !== k) { t._k = k; t.style.backgroundPosition = frameAt(k); }
  }
}
let queued = false;
const ask = () => { if (!queued) { queued = true; requestAnimationFrame(() => { queued = false; turnUpdate(); }); } };
addEventListener('scroll', ask, { passive: true }); addEventListener('resize', ask);
function draggable(t, onFrames) {
  let x0 = null, base = 0;
  t.addEventListener('pointerdown', e => { x0 = e.clientX; base = onFrames(0, true); t.setPointerCapture(e.pointerId); t.classList.add('dragging'); });
  t.addEventListener('pointermove', e => { if (x0 !== null) onFrames(Math.round((e.clientX - x0) / 9), false, base); });
  const end = () => { x0 = null; t.classList.remove('dragging'); };
  t.addEventListener('pointerup', end); t.addEventListener('pointercancel', end);
}
TILES.forEach(t => draggable(t, (d, start, base) => {
  if (start) return drag.get(t) || 0;
  drag.set(t, base - d); turnUpdate(); }));

// the cards' covers
const on = document.getElementById('cover-on'), off = document.getElementById('cover-off'), cards = document.getElementById('cards');
on.addEventListener('click', () => { on.setAttribute('aria-pressed', 'true'); off.setAttribute('aria-pressed', 'false'); cards.classList.remove('show-off'); });
off.addEventListener('click', () => { off.setAttribute('aria-pressed', 'true'); on.setAttribute('aria-pressed', 'false'); cards.classList.add('show-off'); });
document.getElementById('copy').addEventListener('click', () => {
  const note = document.getElementById('copy-note'), text = document.getElementById('addr').textContent;
  const done = () => { note.textContent = 'Copied. The inbox opens at launch.'; };
  const pickText = () => { const r = document.createRange(); r.selectNodeContents(document.getElementById('addr'));
    const s = getSelection(); s.removeAllRanges(); s.addRange(r); note.textContent = 'Selected.'; };
  try { navigator.clipboard.writeText(text).then(done, pickText); } catch (e) { pickText(); }
});

// a speaker's page: its pictures as a shop shows them, the photograph in its element first, then the rest one at a time
// (the arrows, a swipe, the arrow keys, or the strip of thumbnails)
const VIEWS = [
  ['habitat', 'In its element', c => `${c.name} ${c.place}.`],
  ['on', 'Cover on', c => `With its cover on, in ${c.cover.toLowerCase()}.`],
  ['off', 'Cover off', c => `Cover off: the 15-inch woofer, the two ports, and the lining showing through the walls.`],
  ['studio-light', 'In the studio', c => `${c.name} in the studio, on a pale ground.`],
  ['studio', 'In the studio', c => `${c.name} in the studio, the light coming through its acrylic.`],
  ['back', 'From behind', c => `From behind: the name cut into the back and filled with colour, grips in the sides, the amplifier below.`],
  ['amp', 'The amplifier', c => `The built-in amplifier, a Hypex FusionAmp FA122: analogue and AES in on XLRs with links out, RCA, S/PDIF, optical, and the mains switch.`],
  ['horn-side', 'Horn, side', c => `The horn in profile: the flare, the driver's pod, four slim posts.`],
  ['horn-back', 'Horn, behind', c => `The horn from behind, its cap twisted shut.`],
  ['inside', 'Inside', c => `Inside, a corner cut away: the woofer's motor, the batts in their voile sleeves, a port.`],
  ['reel', 'Lit from below', c => `${c.name} on a light, its colour thrown up the wall behind it.`],
  ['turn', 'Turning', c => `${c.name}'s horn, all the way round.`],
];
const stage = document.getElementById('stage'), thumbs = document.getElementById('thumbs'), phone = matchMedia('(max-width: 700px)');
let cur = null, view = 'habitat', turnFrame = 0, autoTurn = null;
function src(c, v) { return c.views[v]; }
const say = (c, v) => VIEWS.find(x => x[0] === v)[2](c);
const shown = c => VIEWS.map(x => x[0]).filter(v => c.views[v] && !(v === 'studio' && c.views['studio-light']));   // the bright studio won
// the stage's ground for a picture: its sides' colours when it is narrower than the stage, its top's and bottom's when wider
// (a close-up has a blurred copy of itself instead, and one cut off at the foot sits on the stage's foot under its top's colour)
function ground(v) {
  const s = src(BY[cur], v);
  if (!s || !s.bg || s.edge === 'busy' || s.fill) return '';
  const c = s.bg.match(/.{6}/g).map(h => '#' + h), stops = cs => cs.map((x, i) => `${x} ${10 + 20 * i}%`).join(', ');
  if (v === 'habitat') return c[10];
  return s.w / s.h <= stage.clientWidth / Math.max(1, stage.clientHeight)
    ? `linear-gradient(${stops(c.slice(0, 5))}) left / 51% 100% no-repeat, linear-gradient(${stops(c.slice(5, 10))}) right / 51% 100% no-repeat`
    : s.edge === 'cut' ? c[10] : `linear-gradient(${c[10]} 50%, ${c[11]} 50%)`;
}
new ResizeObserver(() => { if (cur) stage.style.background = ground(view); }).observe(stage);
function showView(v, focus) {
  const c = BY[cur], list = shown(c), i = list.indexOf(v); view = v;
  const s = src(c, v), ar = (s.w / s.h).toFixed(4);
  cancelAnimationFrame(autoTurn);
  let pic;
  if (v === 'turn') {
    pic = el('div', { class: 'fit spin' + (s.edge === 'cut' ? ' cut' : ''), role: 'img', 'aria-label': `${c.name}'s horn; drag to spin it`, style: `background-image:url(${s.src});--ar:${ar}` });
    turnFrame = 0; pic.style.backgroundPosition = frameAt(0);
    draggable(pic, (d, start, base) => { if (start) return turnFrame; turnFrame = ((base - d) % N + N) % N; pic.style.backgroundPosition = frameAt(turnFrame); });
    if (!reduce) { const t0 = performance.now(); (function f(now) { const p = Math.min(1, (now - t0) / 2600); turnFrame = Math.round(p * N) % N;
      pic.style.backgroundPosition = frameAt(turnFrame); if (p < 1) autoTurn = requestAnimationFrame(f); })(t0); }
  } else if (v === 'habitat' || s.fill) {
    pic = el('picture', { class: 'fill' }, (s.tall ? `<source media="(max-width: 700px)" srcset="${s.tall.src}" width="${s.tall.w}" height="${s.tall.h}">` : '')
      + `<img src="${s.src}" width="${s.w}" height="${s.h}" alt="" draggable="false">`);
    pic.querySelector('img').alt = say(c, v);
  } else {
    pic = el('img', { class: 'fit' + (s.edge === 'cut' ? ' cut' : ''), src: s.src, width: s.w, height: s.h, alt: say(c, v), draggable: 'false', style: `--ar:${ar}` });
  }
  if (!reduce) pic.classList.add('in');
  stage.replaceChildren(pic);
  if (s.edge === 'busy' && v !== 'habitat') stage.prepend(el('div', { class: 'blur', 'aria-hidden': 'true', style: `background-image:url(${s.src})` }));
  if (v === 'inside' && s.shared && cur !== 'green') stage.appendChild(el('span', { class: 'tag' }, 'Shown in Poison'));
  stage.style.background = ground(v);
  document.getElementById('cap').textContent = say(c, v);
  document.getElementById('g-count').textContent = `${i + 1} / ${list.length}`;
  thumbs.querySelectorAll('button').forEach(b => { const sel = b.dataset.v === v; b.setAttribute('aria-selected', String(sel)); b.tabIndex = sel ? 0 : -1;
    if (!sel) return;
    stage.setAttribute('aria-labelledby', b.id);
    thumbs.scrollTo({ left: b.offsetLeft - (thumbs.clientWidth - b.offsetWidth) / 2, behavior: reduce ? 'auto' : 'smooth' });
    if (focus) b.focus({ preventScroll: true }); });
  for (const n of [list[(i + 1) % list.length], list[(i + list.length - 1) % list.length]]) {   // the neighbours load while this one is looked at
    const t = src(c, n); if (n !== 'turn') new Image().src = (phone.matches && t.tall ? t.tall : t).src; }
}
function go(d, focus) { const list = shown(BY[cur]); showView(list[(list.indexOf(view) + d + list.length) % list.length], focus); }
function renderPDP(k) {
  const c = BY[k], first = cur === null; cur = k;
  document.getElementById('p-crumb').textContent = c.name;
  document.getElementById('p-num').textContent = `Atmosphere ${c.num}`;
  document.getElementById('p-name').textContent = c.name;
  document.getElementById('p-line').textContent = c.line;
  document.getElementById('p-pick').textContent = c.name;
  document.getElementById('p-icon').innerHTML = `<img class="ic only-light" src="img/icon-${c.icon}-light.webp" alt="" width="256" height="256"><img class="ic only-dark" src="img/icon-${c.icon}-dark.webp" alt="" width="256" height="256">`;
  document.getElementById('facts').innerHTML = [
    ['Acrylic', c.tint], ['Cabinet', 'Cast acrylic, 20 mm, tinted through; lined in white'], ['Horn', 'Cast resin, tinted to match'],
    ['Cover', `Cloth disc, ${c.cover.toLowerCase()}`],
    ['Amplifier', 'Hypex FusionAmp FA122, built in'], ['Inputs', 'XLR, RCA, AES, S/PDIF, optical'], ['Size', '1293 high, 625 wide, 423 deep (mm)'],
    ['Weight', 'About 72 kg']].map(([a, b]) => `<dt>${a}</dt><dd>${b}</dd>`).join('');
  document.getElementById('swatches').replaceChildren(...D.clouds.map(o => { const li = el('li');
    const a = el('a', { href: `#speaker-${o.name.toLowerCase()}`, title: o.name, 'aria-label': o.name, ...(o.k === k ? { 'aria-current': 'true' } : {}) },
      `<span class="coin-dot" style="--i:${o.coin}"></span>`); li.appendChild(a); return li; }));
  thumbs.replaceChildren(...shown(c).map((v, i) => { const s = src(c, v), label = VIEWS.find(x => x[0] === v)[1];
    const b = el('button', { type: 'button', role: 'tab', id: `thumb-${i}`, 'data-v': v, 'aria-label': label, 'aria-controls': 'stage',
      class: 'thumb' + (v === 'turn' ? ' turn' : ''), style: `background:url(${s.src}) ${v === 'turn' ? '0 0 / 600% 400%' : 'center / cover'} no-repeat` });
    b.addEventListener('click', () => showView(v)); return b; }));
  document.getElementById('others').replaceChildren(...D.clouds.filter(o => o.k !== k).map(o => { const li = el('li');
    const f = o.views.off.card || o.views.off;
    li.appendChild(el('a', { href: `#speaker-${o.name.toLowerCase()}` }, `<img src="${f.src}" alt="" loading="lazy" width="${f.w}" height="${f.h}"><span>${o.name}</span>`)); return li; }));
  showView(shown(c)[0]);                              // each speaker opens on its photograph in its element
  goesWith(c);
}
document.getElementById('g-prev').addEventListener('click', () => go(-1));
document.getElementById('g-next').addEventListener('click', () => go(1));
const keys = (e, focus) => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); go(e.key === 'ArrowRight' ? 1 : -1, focus); }
  else if (e.key === 'Home' || e.key === 'End') { e.preventDefault(); const l = shown(BY[cur]); showView(l[e.key === 'Home' ? 0 : l.length - 1], focus); }
};
thumbs.addEventListener('keydown', e => keys(e, true));
stage.addEventListener('keydown', e => keys(e, false));
// a swipe across the stage turns the page; on the turning horn a drag spins it instead
let sx = null, sy = 0;
stage.addEventListener('pointerdown', e => { if (view !== 'turn' && e.isPrimary) { sx = e.clientX; sy = e.clientY; } });
stage.addEventListener('pointerup', e => { if (sx === null) return; const dx = e.clientX - sx, dy = e.clientY - sy; sx = null;
  if (Math.abs(dx) > 40 && Math.abs(dx) > 1.2 * Math.abs(dy)) go(dx < 0 ? 1 : -1); });
stage.addEventListener('pointercancel', () => { sx = null; });

// what goes with a colour (round 25): never another speaker, but the things round it, by the painter's wheel
const CH = D.clouds.filter(c => c.hue !== null).sort((a, b) => a.hue - b.hue), hue = h => CH[((h % 6) + 6) % 6];
const shade = (hex, k) => '#' + [1, 3, 5].map(i => Math.round(parseInt(hex.slice(i, i + 2), 16) * k).toString(16).padStart(2, '0')).join('');
const light = (hex, k) => '#' + [1, 3, 5].map(i => { const v = parseInt(hex.slice(i, i + 2), 16); return Math.round(v + (255 - v) * k).toString(16).padStart(2, '0'); }).join('');
const INK = '#1C1A18';
const ART = {
  player: c => `<svg viewBox="0 0 160 120" aria-hidden="true"><rect x="8" y="22" width="144" height="84" rx="8" fill="${c}"/>
    <rect x="8" y="98" width="144" height="8" rx="3" fill="${shade(c, 0.78)}"/>
    <circle cx="66" cy="62" r="34" fill="${INK}"/><circle cx="66" cy="62" r="24" fill="none" stroke="#3A3733" stroke-width="1.5"/>
    <circle cx="66" cy="62" r="10" fill="${light(c, 0.35)}"/><circle cx="66" cy="62" r="2" fill="${INK}"/>
    <circle cx="128" cy="38" r="7" fill="${shade(c, 0.7)}"/><path d="M128 38 L122 84 L108 92" fill="none" stroke="#D9D6D0" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="132" y="84" width="10" height="10" rx="2" fill="${shade(c, 0.7)}"/></svg>`,
  lamp: c => `<svg viewBox="0 0 160 120" aria-hidden="true"><path d="M44 52 A36 34 0 0 1 116 52 Z" fill="${c}"/>
    <rect x="40" y="50" width="80" height="6" rx="3" fill="${shade(c, 0.8)}"/><rect x="77" y="56" width="6" height="42" fill="${INK}"/>
    <ellipse cx="80" cy="102" rx="26" ry="8" fill="${shade(c, 0.8)}"/><ellipse cx="80" cy="99" rx="26" ry="8" fill="${c}"/></svg>`,
};
function goes(c) {
  if (c.hue === null) { const white = c.k === 'ice', acc = white ? hue(4) : hue(0);
    return [['player', 'Monochromatic', white ? '#EEF1F1' : '#2A2826', white ? 'white' : 'black', `All ${white ? 'white' : 'black'}.`],
            ['lamp', 'Accent', acc.col, acc.name.toLowerCase(), `One of the six as an accent: ${acc.name}, say.`]]; }
  const comp = hue(c.hue + 3);
  return [['player', 'Monochromatic', shade(c.col, 0.72), `deep ${c.name.toLowerCase()}`, 'The same colour, a shade deeper.'],
          ['lamp', 'Complementary', comp.col, comp.name.toLowerCase(), 'Opposite on the colour wheel, so each sets the other off.']];
}
const GOODS = { player: 'Record player', lamp: 'Lamp' };
function goesWith(c) {
  if (!document.getElementById('goes')) return;       // off the page while the companions are redrawn
  document.getElementById('goes-note').textContent = c.hue === null ? `No hue of its own, so it pairs by lightness. Sketches, for now.`
    : `Paired by the colour wheel. Sketches, for now.`;
  document.getElementById('goes').replaceChildren(...goes(c).map(([id, way, col, cname, why]) => el('figure', { class: 'good' },
    `<div class="art">${ART[id](col)}</div><b>${GOODS[id]}</b><span class="way">${way} <i>&middot;</i> <span class="chip"><span class="dot" style="--c:${col}"></span>${cname}</span></span><p>${why}</p>`)));
}

// the address: #top and the home page's sections, or #speaker-<colour>
const home = document.getElementById('home'), pdp = document.getElementById('pdp');
let last = null;
function route() {
  const h = location.hash.slice(1), m = /^speaker-([a-z]+)$/.exec(h), k = m ? keyOf(m[1]) : null;
  const page = k ? 'speaker' : 'home';
  if (k) {
    const was = last; home.hidden = true; pdp.hidden = false; renderPDP(k);
    if (was !== 'speaker') scrollTo(0, 0);
  } else {
    const was = last; home.hidden = false; pdp.hidden = true;
    const target = h && document.getElementById(h);
    if (target && h !== 'top') target.scrollIntoView(); else if (was === 'speaker' || h === 'top') scrollTo(0, 0);
    ask();
  }
  last = page === 'speaker' ? 'speaker' : 'home';
}
addEventListener('hashchange', route);

// the opening: the acrylic globe turns large in the middle of its ground until the hero's photograph is decoded (at
// least 0.9 s, so it is seen, and never more than 4.5 s), then flies and shrinks onto the header's globe while the
// ground, a circle centred on it, closes in behind it; the photograph fades up beneath as it goes, and the header's
// globe takes over at the film's angle, the flyer fading off it (briefly by day, the same render; longer by night, when
// the glowing night globe gives way to the day's)
function opening() {
  const root = document.documentElement, splash = document.querySelector('.splash'), flyer = document.querySelector('.flyer');
  const film = flyer && flyer.querySelector('video'), hero = document.querySelector('.hero-photo img');
  const target = document.querySelector('header.top .brand .globe'), night = root.classList.contains('night');
  let finished = false, landed = false;
  const done = () => { if (finished) return; finished = true;
    if (film && film.currentTime) setTurn(film.currentTime);
    if (splash) splash.remove(); if (flyer) flyer.remove();
    if (night) { const tc = document.querySelector('meta[name="theme-color"]'); if (tc) tc.content = '#F4F1EC'; }
    root.classList.remove('intro', 'night'); if (target) target.style.visibility = '';
    requestAnimationFrame(() => root.classList.remove('opening')); };
  const land = () => { if (finished || landed) return; landed = true;   // the ground is behind the globe now, all of it
    if (film && film.currentTime) setTurn(film.currentTime);
    target.style.visibility = 'visible'; splash.remove();
    flyer.animate([{ opacity: 1 }, { opacity: 0 }], { duration: night ? 300 : 120, easing: 'ease-out', fill: 'forwards' }).finished.then(done, done); };
  if (!root.classList.contains('intro') || !splash || !flyer || !target || !hero || reduce) { done(); return; }
  if (film && film.play) film.play().catch(() => {});
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const ready = (hero.decode ? hero.decode() : Promise.resolve()).catch(() => {});
  Promise.race([Promise.all([ready, wait(900)]), wait(4500)]).then(() => {
    if (finished) return;
    const a = flyer.getBoundingClientRect(), b = target.getBoundingClientRect();
    const ax = a.left + a.width / 2, ay = a.top + a.height / 2, bx = b.left + b.width / 2, by = b.top + b.height / 2;
    const R = Math.hypot(Math.max(ax, innerWidth - ax), Math.max(ay, innerHeight - ay)) + 2, T = 1000;
    const easing = 'cubic-bezier(.7, 0, .2, 1)';
    root.classList.remove('opening');                                 // the photograph fades up as the ground goes
    if (!flyer.animate || !b.width) { done(); return; }
    flyer.animate([{ transform: 'none' }, { transform: `translate(${bx - ax}px, ${by - ay}px) scale(${b.width / a.width})` }],
      { duration: T, easing, fill: 'forwards' });
    splash.animate([{ clipPath: `circle(${R}px at ${ax}px ${ay}px)` }, { clipPath: `circle(${b.width / 2}px at ${bx}px ${by}px)` }],
      { duration: T, easing, fill: 'forwards' }).finished.then(land, done);
    setTimeout(done, T + 800);                                        // in case an animation never reports
  });
  setTimeout(done, 7000);                                             // never longer than this
}

// the cursor, on a mouse: a dot exactly where the pointer is, in the colour of the text beneath it, and a ring that follows
// a beat behind; over anything to press the ring opens, tinted with the speaker it leads to, and over a horn that turns
// it shows which way it goes
if (matchMedia('(pointer: fine)').matches && !reduce) {
  const root = document.documentElement, dot = el('div', { class: 'cur cur-dot', 'aria-hidden': 'true' }), ring = el('div', { class: 'cur cur-ring', 'aria-hidden': 'true' });
  document.body.append(dot, ring);
  let x = -99, y = -99, rx = -99, ry = -99, sc = 1, scTo = 1, last = performance.now(), under = null;
  const speakerOf = a => { const k = a && (a.dataset.k || keyOf((/#speaker-([a-z]+)/.exec(a.getAttribute('href') || '') || [])[1])); return k && BY[k] ? BY[k].col : null; };
  addEventListener('pointermove', e => {
    if (e.pointerType && e.pointerType !== 'mouse') return;
    x = e.clientX; y = e.clientY; root.classList.add('cursor');
    if (e.target === under || !e.target.closest) return;
    under = e.target;
    const ink = getComputedStyle(under).color, hit = under.closest('a, button, [role="tab"], .spin, #stage, summary, label');
    root.style.setProperty('--cur', ink);
    ring.style.setProperty('--tint', speakerOf(hit && (hit.closest('[data-k]') || hit)) || ink);
    ring.classList.toggle('on', !!hit);
    ring.classList.toggle('drag', !!(under.closest('.spin') || (under.closest('#stage') && view === 'turn')));
  }, { passive: true });
  addEventListener('pointerdown', () => { scTo = 0.84; }); addEventListener('pointerup', () => { scTo = 1; });
  root.addEventListener('pointerleave', () => root.classList.remove('cursor'));
  addEventListener('blur', () => root.classList.remove('cursor'));
  (function tick(now) {
    const dt = Math.min(0.05, Math.max(0.001, (now - last) / 1000)); last = now;
    const f = 1 - Math.exp(-dt * 18); rx += (x - rx) * f; ry += (y - ry) * f; sc += (scTo - sc) * (1 - Math.exp(-dt * 26));
    dot.style.transform = `translate3d(${x}px, ${y}px, 0)`;
    ring.style.transform = `translate3d(${rx.toFixed(1)}px, ${ry.toFixed(1)}px, 0) scale(${sc.toFixed(3)})`;
    requestAnimationFrame(tick);
  })(last);
}

route();
turnUpdate();
opening();
</script>
"""

HEAD = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#F4F1EC">
<meta name="color-scheme" content="light">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="EARF">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{URL}/">
<meta property="og:image" content="{URL}/img/hero-1200.jpg">
<meta name="twitter:card" content="summary_large_image">
<style>
/* the base a host would give: no margin, pictures inside their boxes, [hidden] hidden, the phone's insets */
:root {{ padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px) }}
body {{ margin: 0; font: 14px/1.4 system-ui, -apple-system, sans-serif }}
img {{ max-width: 100% }}
[hidden] {{ display: none !important }}
</style>
"""


def favicons():
    """favicon.svg (the small black cut, its ink paper-white on dark tabs), favicon-32.png, apple-touch-icon.png (the
    colour globe on paper, 180 px)."""
    svg = open(os.path.join(BRAND, 'mark', 'small', 'earf-globe-black-32.svg')).read()
    if 'prefers-color-scheme' not in svg:
        svg = svg.replace('>', '><style>path,circle,ellipse,polygon{fill:#1C1A18}'
                          '@media (prefers-color-scheme: dark){path,circle,ellipse,polygon{fill:#F2EFEA}}</style>', 1)
    open(os.path.join(SITE, 'favicon.svg'), 'w').write(svg)
    shutil.copy(os.path.join(BRAND, 'mark', 'small', 'earf-globe-black-32.png'), os.path.join(SITE, 'favicon-32.png'))
    g = Image.open(os.path.join(BRAND, 'mark', 'earf-globe-colour.png')).convert('RGBA').resize((150, 150), Image.LANCZOS)
    t = Image.new('RGBA', (180, 180), (242, 239, 234, 255))
    t.alpha_composite(g, (15, 15))
    t.convert('RGB').save(os.path.join(SITE, 'apple-touch-icon.png'))


def build():
    """The whole site into site/: the page as a document, the favicons, robots.txt and vercel.json."""
    head, rest = body()
    open(os.path.join(SITE, 'index.html'), 'w').write(HEAD + head.strip() + '\n</head>\n<body>\n' + rest.strip() + '\n</body>\n</html>\n')
    favicons()
    open(os.path.join(SITE, 'robots.txt'), 'w').write('User-agent: *\nDisallow: /\n')
    json.dump({
        'cleanUrls': True,
        'headers': [
            {'source': '/(.*)', 'headers': [{'key': 'X-Robots-Tag', 'value': 'noindex, nofollow'},
                                            {'key': 'X-Content-Type-Options', 'value': 'nosniff'},
                                            {'key': 'Referrer-Policy', 'value': 'strict-origin-when-cross-origin'}]},
            {'source': '/img/(.*)', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=3600, must-revalidate'}]},
        ],
        # only main deploys: round 31's twenty-odd working branches each built a preview on every push, until the
        # plan's daily allowance ran out and main could not deploy (Vercel: "Deployment rate limited")
        'git': {'deploymentEnabled': {'r31-*': False, 'r32-*': False, 'claude/*': False}},
    }, open(os.path.join(SITE, 'vercel.json'), 'w'), indent=2)
    n = sum(len(f) for _, _, f in os.walk(SITE))
    kb = int(subprocess.run(['du', '-sk', SITE], capture_output=True, text=True).stdout.split()[0])
    return f'{os.path.relpath(SITE, ROOT)}: {n} files, {kb / 1024:.1f} MB'


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--images', action='store_true', help='make the pictures too, from the renders and icons (and --sources)')
    ap.add_argument('--sources', metavar='DIR', help="the working notes' folder, for the photographs, room, drawings and coins")
    a = ap.parse_args()
    if a.images:
        print('pictures made:', len(make_images(a.sources)))
    print(build())


if __name__ == '__main__':
    main()
