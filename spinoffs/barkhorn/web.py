"""earf.world, built from the repository (round 31: round 30's draft and its hosting moved here from the working
notes, so any session can rebuild the site).

One page, two views by its address: the home page (#top, and its sections #turn, #atmosphere, #room, #spec, #contact)
and a speaker's page (#speaker-red ... #speaker-black). It is written as it is hosted: a whole document, with what a
browser and a link preview need, a bar saying it is a preview, and kept out of search engines until launch (a meta
tag, an X-Robots-Tag header on every response and a robots.txt that disallows everything), into site/ for Vercel,
which deploys it on every push to main.

- Home: the hero (the eight on an arc, covers off, each a link to its page); the horns, turning as the page scrolls
  and by hand; the eight cards, covers off first, each with its acrylic icon; the room; the particulars; enquiries.
- A speaker's page: a gallery of eight views, its colour picked from the acrylic coins, its particulars, what goes
  with its colour (round 25's idea, sketches for now) and the other seven.
- The header's globe spins once as the page opens, on hover or focus, and when the page changes, never under reduced
  motion; the loader is the acrylic coins rolling.

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
import argparse, json, math, os, shutil, subprocess, sys
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
URL = 'https://www.earf.world'                            # the primary domain (earf.world redirects to it)
TITLE = 'EARF · Atmosphere'
DESC = ('Horn loudspeakers cast in tinted acrylic, in eight colours named for things in the air. '
        'A concept from EARF, not yet for sale.')

CLOUDS = [  # key, number, name, icon, the acrylic, its line, its cover (the look book's)
    ('red', '01', 'Ember', 'ember', 'Translucent red', 'The part of the fire that stays up late.', 'Oxblood'),
    ('orange', '02', 'Dust', 'dust', 'Translucent orange', 'Settles in nicely.', 'Rust'),
    ('amber', '03', 'Acid', 'acid', 'Translucent golden yellow', 'A yellow with opinions.', 'Ochre'),
    ('green', '04', 'Poison', 'poison', 'Translucent bottle green', 'Green, and not the healthy kind.', 'Bottle green'),
    ('blue', '05', 'Ice', 'ice', 'Translucent ice blue', 'Keeps its cool.', 'Deep blue'),
    ('violet', '06', 'Haze', 'haze', 'Translucent violet', 'Dusk, kept indoors.', 'Deep violet'),
    ('ice', '07', 'Fog', 'fog', 'Water-clear', 'Now you see it.', 'White'),
    ('black', '08', 'Smoke', 'smoke', 'Smoked black', "Where there's smoke.", 'Black'),
]
SPEC = [('Height', '1293 mm'), ('Width', '625 mm at the horn, 560 mm at the cabinet'), ('Depth', '420 mm'),
        ('Weight', 'About 72 kg; 62 kg with the horn lifted off'),
        ('Woofer', "15-inch, with two ports in the front's lower corners"), ('Horn driver', '2-inch compression driver'),
        ('Horn', "Cast resin, the cabinet's full depth, 420 mm"),
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
          ('grip', 'poison', 'A grip cut into the side of a Poison cabinet', 'A grip on each side, for the 72 kg.')]
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
            one(first(os.path.join(FIN, f'front-{side}-{k}.png'), at('r8', 'deck-assets', 'photos', f'look2-{k}-{side}.jpg')),
                lambda p, s=side: save(Image.open(p), f'{k}-{s}.jpg', 900, q=80))
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
            lambda p: save(Image.open(p), f'{k}-reel.jpg', 1400, q=84))
        e = ELEMENT[k]                                  # the concept the colour shows in its element
        one(first(os.path.join(E31, f'{e}.png'), os.path.join(E31, f'{e}.jpg')), lambda p: save(Image.open(p), f'{k}-habitat.jpg', 1600, q=84))
        one(first(os.path.join(E31, f'{e}-portrait.png'), os.path.join(E31, f'{e}-portrait.jpg')),
            lambda p: save(Image.open(p), f'{k}-habitat-portrait.jpg', 1000, q=84))
        for tag, names in (('studio', ('hero-dark', 'hero')), ('studio-light', ('hero-light',))):
            one(first(*[os.path.join(ST31, f'{n}-{c}.{e}') for n in names for c in (h, k) for e in ('png', 'jpg')]),
                lambda p, t=tag: (save(Image.open(p), f'{k}-{t}.jpg', 2400, q=84), save(Image.open(p), f'{k}-{t}-1200.jpg', 1200, q=82)))
    one(os.path.join(R30, 'inside.png'), lambda p: save(Image.open(p), 'inside.jpg', 880, q=82))
    one(first(os.path.join(ST31, 'lineup.png'), os.path.join(ST31, 'lineup.jpg')),
        lambda p: (save(Image.open(p), 'lineup.jpg', 2400, q=84), save(Image.open(p), 'lineup-1200.jpg', 1200, q=82)))
    for m, c, *_ in MACROS:                             # the studio's details, each in the colour it was shot in
        one(first(*[os.path.join(ST31, f'macro-{m}-{c}.{e}') for e in ('png', 'jpg')]),
            lambda p, m=m: save(Image.open(p), f'macro-{m}.jpg', 1200, q=84))
    for tag in ('turntable', 'lamp'):
        one(first(os.path.join(C31, f'hero-{tag}.png'), os.path.join(C31, f'hero-{tag}.jpg')),
            lambda p, t=tag: save(Image.open(p), f'next-{t}.jpg', 1400, q=84))
    for tag, names in (('facade', ('facade', 'night', 'opera')), ('facade-portrait', ('facade-portrait', 'night-portrait', 'opera-portrait'))):
        one(first(*[os.path.join(U31, f'{n}.{e}') for n in names for e in ('png', 'jpg')]),
            lambda p, t=tag: (save(Image.open(p), f'{t}.jpg', 2400, q=84), save(Image.open(p), f'{t}-1200.jpg', 1200, q=82)))
    room = first(os.path.join(RM31, 'room.png'), os.path.join(RM31, 'room.jpg'), os.path.join(FIN, 'room.png'))
    one(room, lambda p: save(Image.open(p), 'room.jpg', 1800, q=84))
    port = first(*[os.path.join(os.path.dirname(room), f'room-portrait.{e}') for e in ('png', 'jpg')]) if room else ''
    if port and os.path.exists(port):                   # the room's phone frame travels with it, as the hero's does
        one(port, lambda p: save(Image.open(p), 'room-portrait.jpg', 1000, q=84))
    elif room and os.path.exists(os.path.join(IMG, 'room-portrait.jpg')):
        os.remove(os.path.join(IMG, 'room-portrait.jpg'))
    for f in ('room.jpg', 'ga-front.png', 'ga-right.png'):
        if f == 'room.jpg' and room:
            continue
        one(at('r25', 'site', 'img', f), lambda p, f=f: shutil.copy(p, os.path.join(IMG, f)))
    # the icons, acrylic (icons_real.py's renders, each on its ground made even), a layer for light grounds and one for dark
    for k, num, name, icon, *_ in CLOUDS:
        for tag, ground, dark in (('', rgb(E.PAPER), False), ('-night', rgb(E.NIGHT), True)):
            one(os.path.join(BRAND, 'icons', f'icon-{icon}-render{tag}.png'),
                lambda p, g=ground, d=dark: layer(Image.open(p).resize((256, 256), Image.LANCZOS), g, d).save(
                    os.path.join(IMG, f'icon-{icon}-{"dark" if d else "light"}.jpg'), quality=90))
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
    colour (the photograph's corner)."""
    size = lambda n: Image.open(os.path.join(IMG, n)).size
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
            views[v] = dict(src=f'img/{n}', w=w, h=h)
        if 'inside' not in views:                       # the shared cutaway (Poison's) until a colour has its own
            w, h = size('inside.jpg')
            views['inside'] = dict(src='img/inside.jpg', w=w, h=h, shared=True)
        w, h = size(f'turn-{k}.jpg')
        views['turn'] = dict(src=f'img/turn-{k}.jpg', w=w // 6, h=h // 4)
        meta[k] = views
        corner = np.asarray(Image.open(os.path.join(IMG, f'{k}-on.jpg')).convert('RGB'))[3:19, 3:19].reshape(-1, 3).mean(0)
        panel[k] = '#%02X%02X%02X' % tuple(int(x) for x in corner)
    return meta, panel


def body():
    """The page's head (fonts and style) and body, its pictures as they stand in site/img."""
    meta, panel = image_meta()
    spots = hero_spots()
    word = E.word_svg('currentColor').replace('role="img" aria-label="EARF"', 'aria-hidden="true"').replace('<title>EARF</title>', '')
    coin = {k: i for i, k in enumerate(KEYS)}                 # the coins' sheet is in the speakers' order
    icon_img = lambda icon, name, cls='': (f'<img class="ic only-light {cls}" src="img/icon-{icon}-light.jpg" alt="" width="256" height="256">'
                                           f'<img class="ic only-dark {cls}" src="img/icon-{icon}-dark.jpg" alt="" width="256" height="256">')
    hotspots = ''.join(
        f'<a class="spot" href="#speaker-{k}" style="left:{s["l"]}%;top:{s["t"]}%;width:{s["w"]}%;height:{s["h"]}%">'
        f'<span class="spot-label"><span class="spot-ic">{icon_img(icon, name)}</span><b>{name}</b><span>{num}</span></span>'
        f'<span class="sr">{name}, Atmosphere {num}</span></a>'
        for (k, num, name, icon, *_), s in zip(CLOUDS, spots))
    names = ''.join(f'<li><a href="#speaker-{k}"><span class="coin-dot" style="--i:{coin[k]}"></span>{name}</a></li>'
                    for k, num, name, *_ in CLOUDS)
    turn = ''.join(
        f'<li><div class="spin" data-k="{k}" role="img" aria-label="{name}\'s horn; drag to turn it" '
        f'style="background-image:url(img/turn-{k}.jpg);aspect-ratio:{meta[k]["turn"]["w"]} / {meta[k]["turn"]["h"]}"></div>'
        f'<a href="#speaker-{k}">{name}</a></li>' for k, num, name, *_ in CLOUDS)
    w, h = meta['red']['on']['w'], meta['red']['on']['h']
    cards = ''.join(
        f'<article class="card" style="--panel:{panel[k]}">'
        f'<a class="photo" href="#speaker-{k}" aria-label="{name}, up close">'
        f'<img class="on" src="img/{k}-on.jpg" width="{w}" height="{h}" alt="{name} with its cloth cover on" loading="lazy">'
        f'<img class="off" src="img/{k}-off.jpg" width="{w}" height="{h}" alt="{name} with its cover off, the woofer showing" loading="lazy"></a>'
        f'<div class="about"><p class="num"><span class="card-ic">{icon_img(icon, name)}</span>Atmosphere {num}</p>'
        f'<h3>{name}</h3><p class="line">{line}</p>'
        f'<dl><dt>Acrylic</dt><dd>{tint}</dd><dt>Cover</dt><dd>{cover}</dd></dl>'
        f'<a class="more" href="#speaker-{k}">Up close</a></div></article>'
        for k, num, name, icon, tint, line, cover in CLOUDS)
    spec = ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in SPEC)
    reel = habitats = closer = ''
    sk = next((t for t in ('studio-light', 'studio') if all(t in meta[k] for k in KEYS)), None)   # round 31's bright field won
    if sk:
        sw, sh = meta['red'][sk]['w'], meta['red'][sk]['h']
        im = np.asarray(Image.open(os.path.join(IMG, f'red-{sk}.jpg')).convert('RGB'))
        edge = np.concatenate([im[:6].reshape(-1, 3), im[-6:].reshape(-1, 3), im[:, :6].reshape(-1, 3), im[:, -6:].reshape(-1, 3)]).mean(0)
        light = edge.mean() > 150                       # a pale ground takes dark type
        lineup = ''
        if os.path.exists(os.path.join(IMG, 'lineup.jpg')):
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
                  '    <div class="closer-head"><p class="eyebrow">Take a closer look</p><h2>Cast in colour, all the way through.</h2></div>\n'
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
        coins = ''.join(f'<li><button type="button" aria-label="{name}" aria-current="{str(i == 0).lower()}">'
                        f'<span class="coin-dot" style="--i:{coin[k]}"></span></button></li>'
                        for i, (k, num, name, *_) in enumerate(CLOUDS))
        reel = ('  <section class="band lightband" id="light">\n'
                '    <div class="wrap"><div class="head"><div><p class="eyebrow">Lit from below</p><h2>Put a light under it.</h2>'
                '<p>Cast acrylic carries light to its edges, so a lamp underneath turns the whole cabinet into weather. Keep '
                'scrolling for all eight.</p></div></div></div>\n'
                '    <div class="light-run" id="light-run" style="--n:8">\n'
                '      <div class="light-stage"><div class="wrap light-grid">\n'
                '        <div class="light-pic" role="img" aria-label="Each of the eight speakers standing on a light, one after another">' + ''.join(
                    f'<img src="img/{k}-reel.jpg" width="{rw}" height="{rh}" alt="" loading="lazy"{" style=opacity:1" if i == 0 else ""}>'
                    for i, (k, *_) in enumerate(CLOUDS)) + '</div>\n'
                f'        <div class="light-text"><p class="light-name" id="light-name" aria-live="polite">{first_[2]}</p>'
                f'<p class="light-line" id="light-line">{first_[5]}</p>'
                f'<ol class="light-dots" aria-label="The eight colours">{coins}</ol></div>\n'
                '      </div></div>\n    </div>\n'
                + ('    <div class="wrap">\n' + facade + '    </div>\n' if facade else '') +
                '  </section>')
    if all('habitat' in meta[k] for k in KEYS):
        hw, hh = meta['red']['habitat']['w'], meta['red']['habitat']['h']
        tall = all(os.path.exists(os.path.join(IMG, f'{k}-habitat-portrait.jpg')) for k in KEYS)
        habitats = ('  <section class="band" id="habitats"><div class="wrap">\n'
                    '    <div class="head"><div><p class="eyebrow">In their element</p><h2>Each colour, in its own weather.</h2></div>'
                    '<div class="steps"><button type="button" class="btn" id="hab-prev" aria-label="Previous">&larr;</button>'
                    '<button type="button" class="btn" id="hab-next" aria-label="Next">&rarr;</button></div></div>\n'
                    '    <ul class="habitats" id="hab" tabindex="0" aria-label="The eight in their habitats">' + ''.join(
                        f'<li><a href="#speaker-{k}"><picture>'
                        + (f'<source media="(max-width: 700px)" srcset="img/{k}-habitat-portrait.jpg">' if tall else '') +
                        f'<img src="img/{k}-habitat.jpg" width="{hw}" height="{hh}" loading="lazy" '
                        f'alt="{name}, on location in its own weather"></picture><span><b>{name}</b> {line}</span></a></li>'
                        for k, num, name, icon, tint, line, cover in CLOUDS) + '</ul>\n  </div></section>')
    pair = [('turntable', 'Cumulus', 'A record player. Belt drive, its motor in a pod of its own.',
             'Cumulus, a record player in tinted acrylic, its platter on a plinth of overlapping circles'),
            ('lamp', 'Bell', 'A lamp. The horn&rsquo;s flare, hung mouth down.',
             'Bell, a table lamp whose tinted acrylic shade is the horn&rsquo;s flare turned over')]
    figs = ''
    if all(os.path.exists(os.path.join(IMG, f'next-{t}.jpg')) for t, *_ in pair):
        figs = '\n    <div class="pair">' + ''.join(
            '<figure><img src="img/next-{0}.jpg" width="{1}" height="{2}" loading="lazy" alt="{5}">'
            '<figcaption><b>{3}</b> {4}</figcaption></figure>'.format(t, *Image.open(os.path.join(IMG, f'next-{t}.jpg')).size, n, d, alt)
            for t, n, d, alt in pair) + '</div>'
    nxt = ('  <section class="band"><div class="wrap next">\n    <p class="eyebrow">Next</p>\n'
           '    <h2>The speakers would like some company.</h2>\n'
           '    <p>A record player and a lamp, on the drawing board in the same eight colours, so a whole corner of the room can '
           'match. Or clash, if you prefer.</p>' + figs + '\n  </div></section>')
    data = dict(
        clouds=[dict(k=k, num=num, name=name, icon=icon, tint=tint, line=line, cover=cover, col=MARK[k], hue=HUE.get(k),
                     coin=coin[k], views=meta[k]) for k, num, name, icon, tint, line, cover in CLOUDS],
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
        hotspots += ''.join(
            f'<a class="spot tall-only" href="#speaker-{k}" style="left:{s["l"]}%;top:{s["t"]}%;width:{s["w"]}%;height:{s["h"]}%">'
            f'<span class="sr">{name}, Atmosphere {num}</span></a>'
            for (k, num, name, *_), s in sorted(zip(CLOUDS, ps), key=lambda cs: cs[1]['t'] + cs[1]['h']))
    page = (PAGE.replace('__WORD__', word).replace('__HOTSPOTS__', hotspots).replace('__NAMES__', names)
                .replace('__HERO_TALL__', hero_tall).replace('__ROOM_TALL__', room_tall)
                .replace('__HERO_CLASS__', ' has-tall' if hero_tall else '')
                .replace('__TURN__', turn).replace('__CARDS__', cards).replace('__SPEC__', spec)
                .replace('__REEL__', reel).replace('__HABITATS__', habitats).replace('__CLOSER__', closer).replace('__NEXT__', nxt)
                .replace('__DATA__', json.dumps(data, separators=(',', ':'))))
    cut = page.index('</style>') + len('</style>')
    return page[:cut], page[cut:]


PAGE = r"""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400..700&display=swap">
<style>
/* layout: a showroom in one column of bands; the speakers themselves carry the colour, the page stays paper and ink */
:root {
  --paper: #F2EFEA; --page: #E9E5DE; --ink: #1C1A18; --muted: #5E5A53; --rule: #CFC9BF; --card-ink: #1A1917;
  --ring: rgba(0, 0, 0, 0.25); --on-photo: #1C1A18; --veil: rgba(242, 239, 234, 0.82);
  --blend: multiply;
  --sans: 'Instrument Sans', 'Helvetica Neue', Arial, sans-serif; --mono: 'IBM Plex Mono', 'Courier New', monospace;
  --header: 64px;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper: #1A1917; --page: #141311; --ink: #ECE8E1; --muted: #A39E95; --rule: #34312C; --ring: rgba(255, 255, 255, 0.45);
  --veil: rgba(242, 239, 234, 0.82); --blend: screen; color-scheme: dark } }
:root[data-theme="dark"] { --paper: #1A1917; --page: #141311; --ink: #ECE8E1; --muted: #A39E95; --rule: #34312C;
  --ring: rgba(255, 255, 255, 0.45); --veil: rgba(242, 239, 234, 0.82); --blend: screen; color-scheme: dark }
.only-dark { display: none !important }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .only-dark { display: block !important }
  :root:not([data-theme="light"]) .only-light { display: none !important } }
:root[data-theme="dark"] .only-dark { display: block !important }
:root[data-theme="dark"] .only-light { display: none !important }
* { box-sizing: border-box }
body { margin: 0; background: var(--page); color: var(--ink); font-family: var(--sans); font-size: 17px; line-height: 1.55 }
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 10; background: var(--page) }
.wrap { max-width: 1240px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px)) }
.band { padding-block: 72px }
.band + .band { border-top: 1px solid var(--rule) }
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
.brand .globe { width: 42px; height: 42px; flex: none; background-image: url(img/globe-spin-light.jpg); background-size: 1000% 600%;
  background-position: 0 0; mix-blend-mode: var(--blend) }
:root[data-theme="dark"] .brand .globe { background-image: url(img/globe-spin-dark.jpg) }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .brand .globe { background-image: url(img/globe-spin-dark.jpg) } }
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
.ic { width: 100%; height: 100%; object-fit: contain; mix-blend-mode: var(--blend) }
.coin-dot { width: 22px; height: 22px; flex: none; display: inline-block; background: url(img/coins-light.jpg) calc(var(--i) * 100% / 7) 0 / 800% 100%;
  mix-blend-mode: var(--blend) }
:root[data-theme="dark"] .coin-dot { background-image: url(img/coins-dark.jpg) }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .coin-dot { background-image: url(img/coins-dark.jpg) } }

/* the hero: the eight on their arc; the title on the photograph's paper sky, in its ink whatever the theme */
.hero { padding-block: 0 28px }
.hero-pic { position: relative }
.hero-photo { position: relative; aspect-ratio: 2 / 1; max-width: 100%; background: #ECE7DD; overflow: hidden }
.hero-photo > picture { display: block; width: 100%; height: 100% }
.hero-photo img { display: block; width: 100%; height: 100%; object-fit: cover }
@media (max-width: 700px) { .hero-photo.has-tall { aspect-ratio: 4 / 5 } }
.hero-title { position: absolute; left: 0; right: 0; top: 0; z-index: 1; color: var(--on-photo); pointer-events: none }
.hero-title .wrap { padding-block: clamp(18px, 2.6vw, 44px) 0 }
.hero-title .eyebrow { color: color-mix(in srgb, var(--on-photo) 68%, transparent) }
.hero-title h1 { font-size: clamp(30px, 3.6vw, 58px); max-width: none }
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
.spot-ic .ic { mix-blend-mode: multiply }
.spot-ic .only-dark { display: none !important }
.spot-ic .only-light { display: block !important }
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
.about { padding: 14px 16px 18px; display: grid; gap: 4px; align-content: start; min-width: 0 }
.about .num { margin: 0; display: flex; align-items: center; gap: 8px; font: 500 12px/1.3 var(--mono); letter-spacing: 0.12em; text-transform: uppercase }
.card-ic { width: 34px; height: 34px; flex: none; display: block }
.card .card-ic .ic { mix-blend-mode: multiply }
.card .card-ic .only-dark { display: none !important }
.card .card-ic .only-light { display: block !important }
.about h3 { margin: 0; font-size: 26px; line-height: 1.1; font-weight: 600; letter-spacing: -0.01em }
.about .line { margin: 0 0 8px; font-size: 15px }
.about dl { margin: 0; display: grid; grid-template-columns: auto 1fr; gap: 2px 12px; font-size: 13px; border-top: 1px solid rgba(26, 25, 23, .25); padding-top: 8px }
.about dt { font: 500 11px/1.6 var(--mono); letter-spacing: 0.1em; text-transform: uppercase; opacity: .7 }
.about dd { margin: 0 }
.about .more { margin-top: 10px; color: var(--card-ink); font-weight: 600; font-size: 15px; text-underline-offset: 4px }

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
.macros { list-style: none; margin: 40px 0 0; padding: 0; display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; text-align: left }
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
/* lit from below: a pinned frame the page scrolls through, each colour cross-fading into the next; the coins mark the way */
.lightband { background: #0B0A0C; color: #ECE8E1; padding-bottom: 0 }
.lightband .head p, .lightband .eyebrow { color: #A39E95 }
.light-run { --n: 8; height: calc(var(--n) * 55vh + 45vh); position: relative }
.light-stage { position: sticky; top: calc(var(--header) + env(safe-area-inset-top, 0px)); height: calc(100vh - var(--header));
  display: grid; align-items: center }
.light-grid { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr); gap: clamp(24px, 4vw, 64px); align-items: center; width: 100% }
.light-pic { position: relative; aspect-ratio: 1 / 1; max-width: 100%; width: min(100%, calc(100vh - var(--header) - 96px)); justify-self: center;
  border-radius: 6px; overflow: hidden; background: #000 }
.light-pic img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; will-change: opacity }
.light-text { display: grid; gap: 10px; align-content: center; min-width: 0 }
.light-name { margin: 0; font-size: clamp(40px, 6vw, 84px); line-height: 1; font-weight: 600; letter-spacing: -0.03em }
.light-line { margin: 0; color: #A39E95; font-size: 18px; max-width: 30ch }
.light-dots { list-style: none; margin: 18px 0 0; padding: 0; display: flex; flex-wrap: wrap; gap: 6px }
.light-dots button { width: 36px; height: 36px; padding: 4px; border: 0; border-radius: 50%; background: transparent; cursor: pointer }
.light-dots button[aria-current="true"] { box-shadow: inset 0 0 0 2px #ECE8E1 }
.light-dots .coin-dot { width: 100%; height: 100%; display: block; border-radius: 50%; background-image: url(img/coins-dark.jpg); mix-blend-mode: screen }
.lightband button:focus-visible { outline-color: #ECE8E1 }
.lightband .facade { margin: 0; padding-block: 64px 72px }
@media (max-width: 860px) { .light-grid { grid-template-columns: 1fr; gap: 14px } .light-pic { width: min(100%, calc(100vh - var(--header) - 230px)) }
  .light-name { font-size: 40px } .light-dots { margin-top: 8px } }
@media (prefers-reduced-motion: reduce) { .light-run { height: auto } .light-stage { position: static; height: auto; padding-block: 24px } }
/* the habitats: one campaign picture at a time, snapping along a strip (the portraits on phones) */
.steps { display: flex; gap: 8px }
.steps .btn { padding: 10px 14px }
.habitats { list-style: none; margin: 0; padding: 0 0 6px; display: grid; grid-auto-flow: column; grid-auto-columns: min(86%, 1080px);
  gap: 20px; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; overscroll-behavior-x: contain }
.habitats::-webkit-scrollbar { display: none }
.habitats li { scroll-snap-align: start; min-width: 0 }
.habitats a { display: grid; gap: 10px; color: var(--ink); text-decoration: none; font-size: 15px }
.habitats a span { color: var(--muted) } .habitats a b { color: var(--ink); font-weight: 600; margin-right: 6px }
.habitats img { width: 100%; height: auto; display: block; border-radius: 4px }
.habitats:focus-visible { outline: 2px solid var(--ink); outline-offset: 4px }
@media (max-width: 700px) { .habitats { grid-auto-columns: 84% } }
.room figure { margin: 0; display: grid; gap: 12px }
.room img { width: 100%; height: auto; display: block; border-radius: 4px; max-width: 100% }
.room figcaption { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 6px 24px; font-size: 15px; color: var(--muted) }
.spec-grid { display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); gap: 40px; align-items: start }
.spec dl, .facts { margin: 0; display: grid; grid-template-columns: 150px minmax(0, 1fr); border-top: 2px solid var(--ink) }
.spec dt, .spec dd, .facts dt, .facts dd { padding: 10px 0; border-bottom: 1px solid var(--rule) }
.spec dt, .facts dt { font: 500 13px/1.5 var(--mono); letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted) }
.spec dd, .facts dd { margin: 0 }
.dwg { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; background: #F7F5F1; border-radius: 4px; padding: 14px; margin: 0 }
.dwg img { width: 100%; height: auto; display: block; mix-blend-mode: multiply; max-width: 100% }
.dwg figcaption { grid-column: 1 / -1; font: 500 12px/1.4 var(--mono); letter-spacing: 0.1em; text-transform: uppercase; color: #5E5A53 }
.next { display: grid; gap: 14px }
.next p { margin: 0; max-width: 60ch; color: var(--muted) }
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
.pdp { display: grid; grid-template-columns: minmax(0, 1.12fr) minmax(0, 0.88fr); gap: 44px; align-items: start; padding-block: 18px 64px }
.gallery { display: grid; gap: 12px; min-width: 0 }
.stage { --h: min(78vh, 780px); position: relative; height: var(--h); display: grid; place-items: center }
.stage .shot { position: relative; display: flex; align-items: center; justify-content: center; height: 100%; width: 100%; min-width: 0 }
.stage img { max-width: 100%; max-height: var(--h); width: auto; height: auto; display: block; border-radius: 6px }
.stage .spin { width: min(100%, calc(var(--h) * var(--ar))); border-radius: 6px }
.stage .tag { position: absolute; left: 12px; bottom: 12px; font: 500 12px/1 var(--mono); letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--on-photo); background: var(--veil); border-radius: 999px; padding: 7px 10px }
.thumbs { display: grid; grid-template-columns: repeat(8, minmax(0, 1fr)); gap: 8px }
.thumb { position: relative; aspect-ratio: 4 / 5; border-radius: 4px; overflow: hidden; border: 1px solid var(--rule); padding: 0; cursor: pointer;
  background-color: var(--paper) }
.thumb[aria-selected="true"] { outline: 2px solid var(--ink); outline-offset: 2px }
.cap { margin: 0; color: var(--muted); font-size: 15px; max-width: 62ch }
.buy { position: sticky; top: calc(var(--header) + 24px); display: grid; gap: 18px; min-width: 0; background: var(--page) }
.buy .num { margin: 0; display: flex; align-items: center; gap: 10px; font: 500 13px/1.3 var(--mono); letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted) }
.buy .num .pic { width: 46px; height: 46px; display: block }
.buy h1 { font-size: clamp(40px, 5vw, 64px) }
.buy .line { margin: 0; font-size: 18px }
.price { margin: 0; font-size: 20px; font-weight: 600 }
.price span { font-weight: 400; color: var(--muted); font-size: 16px }
.swatches { display: flex; flex-wrap: wrap; gap: 10px; margin: 0; padding: 0; list-style: none }
.swatches a { display: block; width: 48px; height: 48px; border-radius: 50%; position: relative }
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
.goes { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px }
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

/* the loader and the cursor */
.splash { position: fixed; inset: 0; z-index: 50; background: var(--page); display: grid; place-items: center; cursor: pointer }
.splash canvas { width: min(460px, 86vw); height: 86px }
.trail { position: fixed; inset: 0; z-index: 60; pointer-events: none; width: 100vw; height: 100vh }
html.no-cursor, html.no-cursor * { cursor: none !important }

@media (max-width: 1000px) { .cards { grid-template-columns: repeat(2, minmax(0, 1fr)) } .spec-grid { grid-template-columns: 1fr }
  .pdp { grid-template-columns: 1fr } .buy { position: static } .others ul { grid-template-columns: repeat(4, minmax(0, 1fr)) } }
@media (max-width: 720px) {
  .horns { grid-template-columns: repeat(2, minmax(0, 1fr)) }
  nav ul { gap: 4px 14px } nav a { font-size: 14px }
  .band { padding-block: 52px }
  .thumbs { grid-template-columns: repeat(4, minmax(0, 1fr)) }
  .stage { --h: min(70vh, 118vw) }
  .goes { grid-template-columns: 1fr } .good .art { aspect-ratio: 16 / 9 }
  .brand svg { height: 18px } .brand .globe { width: 36px; height: 36px }
}
@media (max-width: 460px) { .cards { gap: 12px } .about h3 { font-size: 21px } .spec dl, .facts { grid-template-columns: 104px minmax(0, 1fr) }
  nav li.wide { display: none } }
@media (prefers-reduced-motion: reduce) { .photo img, .spot-label { transition: none } }
</style>

<div class="draft"><div class="wrap"><span>Preview of earf.world &middot; a concept, not yet for sale</span></div></div>
<header class="top"><div class="wrap">
  <a class="brand" href="#top" aria-label="EARF, home"><span class="globe" aria-hidden="true"></span>__WORD__</a>
  <nav aria-label="Pages"><ul>
    <li><a href="#atmosphere">Colours</a></li><li><a href="#turn">The horn</a></li><li class="wide"><a href="#spec">Details</a></li>
    <li><a href="#contact">Enquire</a></li>
  </ul></nav>
</div></header>

<main id="home">
  <section class="hero" id="top">
    <div class="hero-pic">
      <div class="hero-title"><div class="wrap"><p class="eyebrow">EARF &middot; Atmosphere</p><h1>Weather for the living room.</h1></div></div>
      <div class="hero-photo__HERO_CLASS__">
        <picture>__HERO_TALL__<img src="img/hero.jpg" srcset="img/hero-1200.jpg 1200w, img/hero.jpg 2400w" sizes="100vw" width="2400" height="1200"
          alt="The eight Atmosphere speakers on a curve, their covers off: red through violet, then the clear Fog and the smoked Smoke, each throwing its colour on the floor"></picture>
        __HOTSPOTS__
      </div>
    </div>
    <div class="wrap hero-foot">
      <p class="lede">Atmosphere is a horn loudspeaker cast in tinted acrylic, in eight colours named for things in the
        air. Most of them, you&rsquo;d usually open a window for.</p>
      <div class="acts"><a class="btn solid" href="#atmosphere">Choose a colour</a><a class="btn" href="#contact">Enquire</a></div>
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
      <p class="hint" id="turn-hint">Drag to turn</p>
    </div>
    <ul class="horns" id="horns">__TURN__</ul>
  </div></section>

  <section class="band" id="atmosphere"><div class="wrap">
    <div class="head">
      <div><p class="eyebrow">Atmosphere</p><h2>Pick your poison.</h2>
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
  <section class="band room" id="room"><div class="wrap">
    <div class="head"><div><p class="eyebrow">At home</p><h2>A pair of Poison.</h2></div></div>
    <figure><picture>__ROOM_TALL__<img src="img/room.jpg" width="1800" height="1012" alt="Two green speakers either side of a walnut sideboard with a record player, low sun from a tall window on the left" loading="lazy"></picture>
      <figcaption><span>Each speaker stands 1293 mm tall and 560 mm wide.</span><span>For scale, the sideboard is 560 mm.</span></figcaption></figure>
  </div></section>

  <section class="band spec" id="spec"><div class="wrap">
    <div class="head"><div><p class="eyebrow">Details</p><h2>The particulars</h2></div></div>
    <div class="spec-grid">
      <dl>__SPEC__</dl>
      <figure class="dwg"><img src="img/ga-front.png" alt="The speaker drawn from the front" loading="lazy"><img src="img/ga-right.png" alt="The speaker drawn from the right" loading="lazy">
        <figcaption>From the fabrication drawings</figcaption></figure>
    </div>
  </div></section>

__NEXT__

  <section class="band" id="contact"><div class="wrap contact">
    <p class="eyebrow">Enquiries</p>
    <h2>Prices, pairs and partnerships.</h2>
    <p>Every pair is made to order, so we quote rather than list. Write for prices and lead times, or if you&rsquo;d like to
      make, stock or collaborate.</p>
    <div class="addr"><code id="addr">hello@earf.world</code><button type="button" class="btn" id="copy">Copy address</button></div>
    <small id="copy-note">The inbox opens soon. Until then, this address won&rsquo;t reach us.</small>
  </div></section>
</main>

<main id="pdp" hidden>
  <div class="wrap">
    <p class="crumbs"><a href="#atmosphere">Atmosphere</a> / <span id="p-crumb"></span></p>
    <div class="pdp">
      <section class="gallery" aria-label="Pictures">
        <div class="stage" id="stage" role="tabpanel" aria-labelledby="thumb-0"></div>
        <div class="thumbs" id="thumbs" role="tablist" aria-label="Views"></div>
        <p class="cap" id="cap"></p>
      </section>
      <aside class="buy" aria-label="This speaker">
        <p class="num"><span class="pic" id="p-icon"></span><span id="p-num"></span></p>
        <h1 id="p-name"></h1>
        <p class="line" id="p-line"></p>
        <p class="price">Price on request <span>&middot; each pair made to order</span></p>
        <ul class="swatches" id="swatches" aria-label="Colour"></ul>
        <p class="pick">Colour: <b id="p-pick"></b></p>
        <div class="acts"><a class="btn solid" href="#contact">Enquire about a pair</a><button type="button" class="btn" id="p-turn">Spin the horn</button></div>
        <dl class="facts" id="facts"></dl>
      </aside>
    </div>
    <section aria-labelledby="goes-title">
      <div class="goes-head"><h2 id="goes-title">Good company</h2><span id="goes-note"></span></div>
      <div class="goes" id="goes" aria-live="polite"></div>
    </section>
    <section class="others" aria-labelledby="others-title">
      <div class="goes-head"><h2 id="others-title">The other seven</h2><span>Same speaker, different weather</span></div>
      <ul id="others"></ul>
    </section>
  </div>
</main>

<footer><div class="wrap">
  <a class="brand" href="#top" aria-label="EARF, home">__WORD__</a>
  <p>Atmosphere horn loudspeakers &middot; Concept renders, not yet for sale &middot; &copy; 2026 EARF</p>
</div></footer>

<script>
const D = __DATA__, BY = Object.fromEntries(D.clouds.map(c => [c.k, c]));
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, TAU = Math.PI * 2;
// lit from below: scrolling through the run cross-fades the eight (each picture lies over the one before and fades in over
// its share of the run); the coins say where you are and jump there. Under reduced motion the coins simply pick one.
const run = document.getElementById('light-run');
if (run) {
  const pics = [...run.querySelectorAll('.light-pic img')], dots = [...run.querySelectorAll('.light-dots button')], last = pics.length - 1;
  const name = document.getElementById('light-name'), line = document.getElementById('light-line');
  let at = -1, queuedL = false;
  const paint = f => {
    pics.forEach((im, i) => { const o = i === 0 ? 1 : Math.min(1, Math.max(0, f - (i - 1))); im.style.opacity = o.toFixed(3); });
    const i = Math.round(f);
    if (i !== at) { at = i; const c = D.clouds[i]; name.textContent = c.name; line.textContent = c.line;
      dots.forEach((d, j) => d.setAttribute('aria-current', String(j === i))); }
  };
  const progress = () => { const r = run.getBoundingClientRect(), span = r.height - innerHeight;
    return Math.min(1, Math.max(0, -r.top / Math.max(1, span))) * last; };
  if (reduce) {
    paint(0);
    dots.forEach((d, i) => d.addEventListener('click', () => paint(i)));
  } else {
    const tick = () => { queuedL = false; paint(progress()); };
    addEventListener('scroll', () => { if (!queuedL) { queuedL = true; requestAnimationFrame(tick); } }, { passive: true });
    addEventListener('resize', tick); tick();
    dots.forEach((d, i) => d.addEventListener('click', () => {
      const r = run.getBoundingClientRect(), span = r.height - innerHeight;
      scrollTo({ top: scrollY + r.top + span * (i / last) + 1, behavior: 'smooth' }); }));
  }
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
  const step = d => { const li = hab.querySelector('li'); hab.scrollBy({ left: d * (li.offsetWidth + 20), behavior: reduce ? 'auto' : 'smooth' }); };
  document.getElementById('hab-prev').addEventListener('click', () => step(-1));
  document.getElementById('hab-next').addEventListener('click', () => step(1));
}
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const dark = () => { const t = document.documentElement.dataset.theme; return t ? t === 'dark' : matchMedia('(prefers-color-scheme: dark)').matches; };
const el = (tag, attrs = {}, html = '') => { const e = document.createElement(tag); for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v); e.innerHTML = html; return e; };

// the header's globe: still; it spins once as the page opens, on hover or focus, and when the page changes
const GLOBES = [...document.querySelectorAll('.brand .globe')];
let spinning = false;
function spinGlobe() {
  if (reduce || spinning) return;
  spinning = true;
  const t0 = performance.now(), T = 1500, N = 60;
  (function f(now) {
    const p = Math.min(1, (now - t0) / T), e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
    const i = Math.round(e * N) % N;
    GLOBES.forEach(g => { g.style.backgroundPosition = `${(i % 10) * 100 / 9}% ${Math.floor(i / 10) * 100 / 5}%`; });
    if (p < 1) requestAnimationFrame(f); else spinning = false;
  })(t0);
}
document.querySelectorAll('.brand').forEach(b => { b.addEventListener('mouseenter', spinGlobe); b.addEventListener('focus', spinGlobe); });

// the horns turn once as they cross the screen, a frame every 15 degrees; dragged, they turn by hand
const TILES = [...document.querySelectorAll('#horns .spin')], N = 24, C = 6, R = 4;
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
if (reduce) document.getElementById('turn-hint').textContent = 'Drag to turn';

// the cards' covers
const on = document.getElementById('cover-on'), off = document.getElementById('cover-off'), cards = document.getElementById('cards');
on.addEventListener('click', () => { on.setAttribute('aria-pressed', 'true'); off.setAttribute('aria-pressed', 'false'); cards.classList.remove('show-off'); });
off.addEventListener('click', () => { off.setAttribute('aria-pressed', 'true'); on.setAttribute('aria-pressed', 'false'); cards.classList.add('show-off'); });
document.getElementById('copy').addEventListener('click', () => {
  const note = document.getElementById('copy-note'), text = document.getElementById('addr').textContent;
  const done = () => { note.textContent = 'Copied. The inbox opens soon.'; };
  const pickText = () => { const r = document.createRange(); r.selectNodeContents(document.getElementById('addr'));
    const s = getSelection(); s.removeAllRanges(); s.addRange(r); note.textContent = 'Selected. Copy it with your keyboard.'; };
  try { navigator.clipboard.writeText(text).then(done, pickText); } catch (e) { pickText(); }
});

// a speaker's page
const VIEWS = [
  ['on', 'Cover on', c => `With its cover on, in ${c.cover.toLowerCase()}.`],
  ['off', 'Cover off', c => `Cover off: the 15-inch woofer, the two ports, and the lining showing through the walls.`],
  ['studio', 'In the studio', c => `${c.name} in the studio, the light coming through its acrylic.`],
  ['studio-light', 'On pale grey', c => `${c.name} in the studio, on a pale ground.`],
  ['back', 'From behind', c => `From behind: the name cut into the back and filled with colour, grips in the sides, the amplifier below.`],
  ['amp', 'The amplifier', c => `The built-in amplifier, a Hypex FusionAmp FA122: analogue and AES in on XLRs with links out, RCA, S/PDIF, optical, and the mains switch.`],
  ['inside', 'Inside', c => `Inside, a corner cut away: the woofer's motor, the batts in their voile sleeves, a port.`],
  ['horn-side', 'Horn, side', c => `The horn in profile: the flare, the driver's pod, four slim posts.`],
  ['horn-back', 'Horn, behind', c => `The horn from behind, its cap twisted shut.`],
  ['turn', 'Turning', c => `Drag to spin it.`],
  ['reel', 'Lit from below', c => `${c.name} on a light, its colour thrown up the wall behind it.`],
  ['habitat', 'At home', c => `${c.name} in its own weather.`],
];
const stage = document.getElementById('stage'), thumbs = document.getElementById('thumbs');
let cur = null, view = 'on', turnFrame = 0, autoTurn = null;
function src(c, v) { return c.views[v]; }
function showView(v, focus) {
  const c = BY[cur]; view = v;
  const s = src(c, v);
  cancelAnimationFrame(autoTurn);
  if (v === 'turn') {
    const sp = el('div', { class: 'spin', role: 'img', 'aria-label': `${c.name}'s horn; drag to spin it`,
      style: `background-image:url(${s.src});aspect-ratio:${s.w} / ${s.h};--ar:${(s.w / s.h).toFixed(4)}` });
    stage.replaceChildren(sp);
    turnFrame = 0; sp.style.backgroundPosition = frameAt(0);
    draggable(sp, (d, start, base) => { if (start) return turnFrame; turnFrame = ((base - d) % N + N) % N; sp.style.backgroundPosition = frameAt(turnFrame); });
    if (!reduce) { const t0 = performance.now(); (function f(now) { const p = Math.min(1, (now - t0) / 2600); turnFrame = Math.round(p * N) % N;
      sp.style.backgroundPosition = frameAt(turnFrame); if (p < 1) autoTurn = requestAnimationFrame(f); })(t0); }
  } else {
    const shot = el('div', { class: 'shot' });
    shot.appendChild(el('img', { src: s.src, width: s.w, height: s.h, alt: VIEWS.find(x => x[0] === v)[2](c) }));
    if (v === 'inside' && s.shared && cur !== 'green') shot.appendChild(el('span', { class: 'tag' }, 'Shown in Poison'));
    stage.replaceChildren(shot);
  }
  document.getElementById('cap').textContent = VIEWS.find(x => x[0] === v)[2](c);
  thumbs.querySelectorAll('button').forEach(b => { const sel = b.dataset.v === v; b.setAttribute('aria-selected', String(sel)); b.tabIndex = sel ? 0 : -1;
    if (sel) stage.setAttribute('aria-labelledby', b.id); if (sel && focus) b.focus(); });
}
function renderPDP(k) {
  const c = BY[k], first = cur === null; cur = k;
  document.getElementById('p-crumb').textContent = c.name;
  document.getElementById('p-num').textContent = `Atmosphere ${c.num}`;
  document.getElementById('p-name').textContent = c.name;
  document.getElementById('p-line').textContent = c.line;
  document.getElementById('p-pick').textContent = c.name;
  document.getElementById('p-icon').innerHTML = `<img class="ic only-light" src="img/icon-${c.icon}-light.jpg" alt="" width="256" height="256"><img class="ic only-dark" src="img/icon-${c.icon}-dark.jpg" alt="" width="256" height="256">`;
  document.getElementById('facts').innerHTML = [
    ['Acrylic', c.tint], ['Cabinet', 'Cast acrylic, 20 mm, tinted through; lined in white'], ['Horn', 'Cast resin, tinted to match'],
    ['Cover', `Cloth disc, ${c.cover.toLowerCase()}`],
    ['Amplifier', 'Hypex FusionAmp FA122, built in'], ['Inputs', 'XLR, RCA, AES, S/PDIF, optical'], ['Size', '1293 high, 625 wide, 420 deep (mm)'],
    ['Weight', 'About 72 kg']].map(([a, b]) => `<dt>${a}</dt><dd>${b}</dd>`).join('');
  document.getElementById('swatches').replaceChildren(...D.clouds.map(o => { const li = el('li');
    const a = el('a', { href: `#speaker-${o.k}`, title: o.name, 'aria-label': o.name, ...(o.k === k ? { 'aria-current': 'true' } : {}) },
      `<span class="coin-dot" style="--i:${o.coin}"></span>`); li.appendChild(a); return li; }));
  thumbs.replaceChildren(...VIEWS.filter(([v]) => c.views[v]).map(([v, label], i) => { const s = src(c, v);
    const b = el('button', { type: 'button', role: 'tab', id: `thumb-${i}`, 'data-v': v, 'aria-label': label, 'aria-controls': 'stage',
      class: 'thumb' + (v === 'turn' ? ' turn' : ''), style: `background:url(${s.src}) ${v === 'turn' ? '0 0 / 600% 400%' : 'center / cover'} no-repeat` });
    b.addEventListener('click', () => showView(v)); return b; }));
  document.getElementById('others').replaceChildren(...D.clouds.filter(o => o.k !== k).map(o => { const li = el('li');
    li.appendChild(el('a', { href: `#speaker-${o.k}` }, `<img src="${o.views.off.src}" alt="" loading="lazy" width="${o.views.off.w}" height="${o.views.off.h}"><span>${o.name}</span>`)); return li; }));
  showView(first ? 'on' : view);
  goesWith(c);
}
thumbs.addEventListener('keydown', e => {
  const i = VIEWS.findIndex(x => x[0] === view);
  if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); showView(VIEWS[(i + (e.key === 'ArrowRight' ? 1 : VIEWS.length - 1)) % VIEWS.length][0], true); }
});
document.getElementById('p-turn').addEventListener('click', () => { showView('turn'); stage.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' }); });

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
  rug: c => `<svg viewBox="0 0 160 120" aria-hidden="true"><rect x="14" y="20" width="132" height="80" rx="10" fill="${c}"/>
    <rect x="24" y="30" width="112" height="60" rx="5" fill="none" stroke="${shade(c, 0.75)}" stroke-width="5"/>
    <path d="M44 48 H116 M44 60 H116 M44 72 H116" stroke="${light(c, 0.3)}" stroke-width="5" stroke-linecap="round"/></svg>`,
};
function goes(c) {
  if (c.hue === null) { const white = c.k === 'ice', acc = white ? hue(4) : hue(0);
    return [['player', 'Monochromatic', white ? '#EEF1F1' : '#2A2826', white ? 'white' : 'black', `All ${white ? 'white' : 'black'}, for the decisive.`],
            ['lamp', 'Accent', acc.col, acc.name.toLowerCase(), `Any of the six will do as an accent. ${acc.name}, for instance.`],
            ['rug', 'Contrast', white ? '#2E2C2A' : '#E4E7E6', white ? 'charcoal' : 'pale grey', 'Its opposite in lightness, to keep things interesting.']]; }
  const comp = hue(c.hue + 3), near = hue(c.hue + 1);
  return [['player', 'Monochromatic', shade(c.col, 0.72), `deep ${c.name.toLowerCase()}`, 'The same colour, a shade deeper, for the fully committed.'],
          ['lamp', 'Complementary', comp.col, comp.name.toLowerCase(), 'Opposite on the colour wheel, so each makes the other look brighter.'],
          ['rug', 'Analogous', near.col, near.name.toLowerCase(), 'Next door on the wheel, for a quieter room.']];
}
const GOODS = { player: 'Record player', lamp: 'Lamp', rug: 'Rug' };
function goesWith(c) {
  document.getElementById('goes-note').textContent = c.hue === null ? `No hue of its own, so it pairs by lightness. The pieces are sketches for now`
    : `Paired by the colour wheel. The pieces are sketches for now`;
  document.getElementById('goes').replaceChildren(...goes(c).map(([id, way, col, cname, why]) => el('figure', { class: 'good' },
    `<div class="art">${ART[id](col)}</div><b>${GOODS[id]}</b><span class="way">${way} <i>&middot;</i> <span class="chip"><span class="dot" style="--c:${col}"></span>${cname}</span></span><p>${why}</p>`)));
}

// the address: #top and the home page's sections, or #speaker-<colour>
const home = document.getElementById('home'), pdp = document.getElementById('pdp');
let last = null;
function route() {
  const h = location.hash.slice(1), m = /^speaker-([a-z]+)$/.exec(h), k = m && BY[m[1]] ? m[1] : null;
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
  if (last !== null && last !== page + (k || '')) spinGlobe();
  last = page === 'speaker' ? 'speaker' : 'home';
}
addEventListener('hashchange', route);

// the loader as the page opens: the six coloured coins uncovered by a rolling coin, Smoke's on light pages and Fog's on dark
const SHEET = { light: new Image(), dark: new Image() };
SHEET.light.src = 'img/coins-light.jpg'; SHEET.dark.src = 'img/coins-dark.jpg';
function loader(then) {
  if (reduce) { then && then(); return; }
  const box = el('div', { class: 'splash', role: 'progressbar', 'aria-label': 'Loading' }), cv = document.createElement('canvas');
  box.appendChild(cv); document.body.appendChild(box);
  const t0 = performance.now(), GO = 2.0, HOLD = 0.35; let done = false;
  const end = () => { if (done) return; done = true; box.remove(); then && then(); };
  box.addEventListener('click', end); addEventListener('keydown', end, { once: true });
  (function frame(now) {
    if (done) return;
    const t = (now - t0) / 1000, x = Math.min(1, t / GO), e = 1 - Math.pow(1 - x, 2.2), dpr = Math.min(2, devicePixelRatio || 1), r = cv.getBoundingClientRect();
    cv.width = Math.round(r.width * dpr); cv.height = Math.round(r.height * dpr);
    const c = cv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0);
    const W = r.width, H = r.height, rad = Math.min(H * 0.34, W / 19), s = 2.7 * rad, x0 = W / 2 - 3 * s, bx = x0 + 6 * s * e;
    const dk = dark(), sheet = dk ? SHEET.dark : SHEET.light, ok = sheet.complete && sheet.naturalWidth > 0, tile = 2 * rad / 0.864;
    c.fillStyle = css('--page'); c.fillRect(0, 0, W, H);
    const coin = (j, cx) => { if (ok) c.drawImage(sheet, 128 * j, 0, 128, 128, cx - tile / 2, H / 2 - tile / 2, tile, tile);
      else { c.fillStyle = j < 6 ? D.hues[j] : css('--ink'); c.beginPath(); c.arc(cx, H / 2, rad, 0, TAU); c.fill(); } };
    c.globalCompositeOperation = ok ? (dk ? 'screen' : 'multiply') : 'source-over';
    c.save(); c.beginPath(); c.rect(0, 0, bx, H); c.clip();
    for (let k = 0; k < 6; k++) coin(D.clouds[k].coin, x0 + k * s);
    c.restore();
    coin(dk ? 6 : 7, bx);
    c.globalCompositeOperation = 'source-over';
    if (t > GO + HOLD) end(); else requestAnimationFrame(frame);
  })(t0);
}

// the cursor's trail (round 22), on a mouse
const fine = matchMedia('(pointer: fine)').matches && !reduce;
const trailOn = fine;
if (fine) {
  const cv = el('canvas', { class: 'trail', 'aria-hidden': 'true' }), hist = []; let hover = 0, hoverTo = 0, inside = false;
  document.body.appendChild(cv); document.documentElement.classList.add('no-cursor');
  addEventListener('pointermove', e => { const now = performance.now() / 1000; hist.push([now, e.clientX, e.clientY]); inside = true;
    while (hist.length > 2 && hist[1][0] < now - 1) hist.shift();
    hoverTo = e.target.closest && e.target.closest('a, button, .spin') ? 1 : 0; });
  document.documentElement.addEventListener('pointerleave', () => { inside = false; });
  const at = tt => { if (tt <= hist[0][0]) return hist[0];
    for (let i = hist.length - 1; i > 0; i--) if (hist[i - 1][0] <= tt) { const a = hist[i - 1], b = hist[i], f = Math.min(1, (tt - a[0]) / Math.max(1e-6, b[0] - a[0]));
      return [0, a[1] + (b[1] - a[1]) * f, a[2] + (b[2] - a[2]) * f]; }
    return hist.at(-1); };
  (function tick() {
    const dpr = Math.min(2, devicePixelRatio || 1), W = innerWidth, H = innerHeight;
    if (cv.width !== Math.round(W * dpr) || cv.height !== Math.round(H * dpr)) { cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr); }
    const c = cv.getContext('2d'); c.setTransform(dpr, 0, 0, dpr, 0, 0); c.clearRect(0, 0, W, H);
    hover += (hoverTo - hover) * 0.25;
    if (trailOn && inside && hist.length) {
      const now = performance.now() / 1000, r = 7;
      for (let k = 6; k >= 1; k--) { const p = at(now - k * 0.07); c.fillStyle = D.hues[k - 1]; c.beginPath(); c.arc(p[1], p[2], r, 0, TAU); c.fill(); }
      const p = at(now); c.fillStyle = css('--ink'); c.beginPath(); c.arc(p[1], p[2], r + 5 * hover, 0, TAU); c.fill();
    }
    requestAnimationFrame(tick);
  })();
}

route();
turnUpdate();
loader(spinGlobe);
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
<meta name="theme-color" content="#F2EFEA" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#121114" media="(prefers-color-scheme: dark)">
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
