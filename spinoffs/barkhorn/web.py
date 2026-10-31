"""earf.world, built from the repository (round 31: round 30's draft and its hosting moved here from the working
notes, so any session can rebuild the site).

One page, laid out as a shop since round 34 (the owner, 2026-10-22: "Do a pass so it works more like an e-commerce site
in terms of the information architecture. A home page that highlights each product line, and then product detail pages
where users can browse colors. The product detail pages are where we'll have sections for complementary, analogous, and
monochromatic colors"). Its views, by address: the home page (#top: the lines, the colours, the light, the eight in
their element, the room, enquiries); a line's page (#speakers, #lighting, #turntable); a colour's page (#colour-poison:
everything made in it); and a product's page (#speaker-poison, #hemisphere-poison, #core-poison, #mantle-poison; the old #dome-, #orb- and
#turntable- addresses still answer), its
pictures in the colour picked, the eight to pick from, and what goes with that colour across every line, by the colour
wheel: its complement, its neighbours, and itself. The old addresses (#atmosphere, #turn, #spec, #lamps) still answer. It is written as it is hosted: a whole document, with what a
browser and a link preview need, a bar saying it is a preview, and kept out of search engines until launch (a meta
tag, an X-Robots-Tag header on every response and a robots.txt that disallows everything), into site/ for Vercel,
which deploys it on every push to main.

- Home: the hero (the eight on an arc, covers off, each a link to its page); the three lines; the eight colours; lit
  from below; in their element; the room; enquiries.
- Speakers: the eight cards, covers off first; in the studio; the horns, turning as the page scrolls and by hand; the
  particulars. Lighting: Hemisphere and Core, each in its eight. Turntable: Mantle, or its concept until its
  pictures are in.
- A product's page: its pictures in the colour picked, the eight coins, its particulars, and its colour's company.
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
ELEMENT['green'] = 'poison_g5'   # the owner (2026-10-22): "Poison: put the deadly green one live" - death caps and a deer's bones (G5 p4)
ELEMENT['black'] = 'smoke_e12r_p19h'  # the owner (2026-10-22): "render p19's finals and put the meteor on the site" - the
                                      # speaker come down like a meteor on the overpass, the fire behind it and its trench
                                      # smouldering (E12r p19; E10's bridge before it, E9 p5 before that); p19h is p19's
                                      # own frames finished again with E12r p27h's eased shimmer, its sparks straight (the
                                      # owner, 2026-10-25: "make your call")
PLACES = {  # where each concept stands: the speaker page leads with it ("Ember on a lava field at blue hour.")
    'ember': 'on a lava field at blue hour, the crust cracked to its glow',
    'dust': 'on rippled sand in the Southwest at golden hour',
    'acid': 'by the acid springs of Dallol', 'acid_b': 'in acid rain on black lava',
    'poison': 'on a redwood forest floor, among ferns', 'poison_a3': 'on a redwood forest floor, among ferns, foxgloves and fly agarics',
    'poison_a4': 'on a redwood forest floor, behind a troop of fly agarics, among ferns and foxgloves',
    'poison_f1b': 'on a redwood forest floor, among fly agarics, ferns and the berries of lords-and-ladies',
    'poison_g5': 'on a redwood forest floor, among death caps and a deer\'s bones',
    'ice': 'in snow country at blue hour', 'ice_b': 'on a black-sand beach among icebergs at sunrise',
    'haze': 'in a lavender field at dusk', 'haze_b': 'before layered hills in evening light',
    'fog': 'on a summit above a sea of cloud', 'fog_b': 'on a headland above the fog at dawn',
    'smoke': 'in a pine wood at dawn, in shafts of woodsmoke', 'smoke_b': 'in a misty birch wood',
    'smoke_e6': 'on a cracked salt flat, black smoke climbing from the horizon',
    'smoke_e9': 'on a city bridge at dusk, a wrecked car burning behind it',
    'smoke_e10': 'on a city overpass at blue hour, a burnt-out car still burning behind it',
    'smoke_e12r_p19': 'on a city overpass at dusk, come down like a meteor, the road torn open and burning behind it',
    'smoke_e12r_p19h': 'on a city overpass at dusk, come down like a meteor, the road torn open and burning behind it',
}
LP = os.path.join(ROOT, 'renders', '2026-10-22', 'barkhorn', 'lamps-pdp')   # each lamp in each colour (lamps_pdp.py)
# round 39's pass 3 (r32-lamps-final): the lamps as drawn in rounds 35 to 39 (Hemisphere's fins, Core's 48 mm base), each
# in each colour as p3-lamp-<lamp>-<flavour>.png, and the rows as p3-<row>.png; its heroes beat round 32f's 2-0 each
LP3 = os.path.join(ROOT, 'renders', '2026-10-22', 'barkhorn', 'lamps-pdp-r35')
# round 41's pass 4: the same shots with the lamps back in round 32f's profiles (the owner, 2026-10-29: Hemisphere's low
# top, Core's 30 mm base), as p4-...; it goes first where it has the picture
LP4 = os.path.join(ROOT, 'renders', '2026-10-29', 'barkhorn', 'lamps-pdp-r41')
TTR = os.path.join(ROOT, 'renders', '2026-10-22', 'barkhorn', 'turntable')  # the record player, round 34's finals
URL = 'https://www.earf.world'                            # the primary domain (earf.world redirects to it)
LINEUP_SHOWN = False          # the studio's eight in a row repeated the hero (the site critic, 2026-10-18); it stays in the look book
TITLE = 'EARF · Tropos'
DESC = ('Horn loudspeakers, lamps and a record player cast in tinted acrylic, in eight colours from Ember to Smoke. '
        'In development at EARF, not yet for sale.')

CLOUDS = [  # key, number, name, icon, the acrylic, its line, its cover (the look book's)
    ('red', '01', 'Ember', 'ember', 'Translucent red', 'The last light of the fire.', 'Oxblood'),
    ('orange', '02', 'Dust', 'dust', 'Translucent orange', 'A long, dry afternoon.', 'Rust'),
    ('amber', '03', 'Acid', 'acid', 'Translucent golden yellow', 'A yellow with an edge.', 'Ochre'),
    ('green', '04', 'Poison', 'poison', 'Translucent bottle green', 'Bottle green. Keep out of reach.', 'Bottle green'),
    ('blue', '05', 'Ice', 'ice', 'Translucent ice blue', 'Glacier blue, and in no hurry.', 'Deep blue'),
    ('violet', '06', 'Haze', 'haze', 'Translucent violet', 'Dusk, kept indoors.', 'Deep violet'),
    ('ice', '07', 'Fog', 'fog', 'Water-clear', 'Water-clear. Almost not there.', 'White'),
    ('black', '08', 'Smoke', 'smoke', 'Smoked black', 'Smoked glass, for after dark.', 'Black'),
]
CARE = ('Care', 'Dust with a soft microfibre cloth; wash with water and a drop of mild soap, then dry. No glass cleaner, alcohol '
        'or solvents: they craze acrylic. Fine scratches polish out.')   # the acrylic makers' own advice, and the warranty's exclusion
SPEC = [('Height', '1293 mm'), ('Width', '625 mm at the horn, 560 mm at the cabinet'),
        ('Depth', '423 mm overall, 420 mm at the cabinet'),
        ('Weight', 'About 72 kg; 62 kg with the horn lifted off'),
        ('Woofer', "FaitalPRO 15PR400, 15-inch, with two ports in the front&rsquo;s lower corners"),
        ('Horn driver', 'B&amp;C DE1085TN, 2-inch compression driver'),
        ('Horn', "Formed from the same tinted cast acrylic as its cabinet, a turned acrylic throat; the cabinet&rsquo;s full depth"),
        ('Amplifier', 'Hypex FusionAmp FA122, built in: two channels of 125 W, crossed at 1 kHz in its DSP'),
        ('Bass', 'To about 51 Hz at &minus;3 dB, before the room adds its own; the ports tuned to 38 Hz'),
        ('Loudness', 'Up to about 115 dB at 1 m, each'),
        ('Inputs', 'XLR (and a link out), RCA, AES, S/PDIF coaxial and optical; USB to set it up'),
        ('Lining', 'Polyester batts in white voile, 100 mm at the top and the bottom'),
        ('Price', 'Set at launch; each pair is made to order'), CARE,
        ('Figures', 'Design figures, from the drawings and their simulation; measured ones follow with the first pair')]
MACROS = [('corner', 'ember', 'The top corner of an Ember cabinet, the horn above it',
           'The corner: two 20 mm walls, cast in one colour and cemented.'),
          ('amp', 'dust', "Hypex's FA122 amplifier on the back of a Dust cabinet", 'The amplifier, built in: Hypex&rsquo;s FA122.'),
          ('horn', 'acid', "The Acid horn from the side, its driver's pod and the flare",
           'The horn: its flare, and its driver&rsquo;s pod behind it.'),
          ('woofer', 'ice', 'The 15-inch woofer through an Ice cabinet', 'The 15-inch woofer, behind the cloth when the cover&rsquo;s on.'),
          ]   # the grip (Poison) left the row of details with the lineup: four read as a set
# the lamps (round 32d), the owner's picks of 2026-10-19 ("sick lamps. Add them to the site as well"): a pendant whose
# tinted cover comes off on a quarter turn, and a table lamp whose ball sits low in a black acrylic base, both cast in the
# eight tints, frosted within. Round 32f took the owner's notes: black hardware (no brass), the Orb plugged in with a
# battery cartridge as its option, each tint cast to read as its speaker's when lit. Their particulars are the fab kits'
# (companions/PARTICULARS.md). The band shows once every picture in LAMP_PICS is in site/img (made from
# renders/2026-10-19/barkhorn/lamps-site/). Round 35, the owner's names (2026-10-22, yes): the pendant is Hemisphere (today's
# Dome), the table lamp Core, the record player Mantle; and Core works plugged in or not, on a built-in battery its owner
# can replace (the cartridge dropped). The owner (2026-10-25): "Get rid of south altogether and just call it hemisphere":
# the bowl-shaped South is dropped, and the pendant, Hemisphere North until then, is Hemisphere
SLUG = {'dome': 'hemisphere', 'orb': 'core', 'turntable': 'mantle'}   # each product's address; the old keys still answer
LAMPS = [  # key, name, kind, its line, the hero's alt, particulars
    ('dome', 'Hemisphere', 'Pendant', 'Hung low over the bar. A quarter turn takes its shade off, and another puts a new colour on.',
     'Hemisphere lit, its Ember shade glowing beneath a black hub',
     [('Size', '200 mm across'), ('Shade', 'Cast acrylic in three layers, tinted, with a frosted layer between'),
      ('Light', '2700 K, CRI 90, its source shielded inside the hub'), ('Fitting', 'Black anodised aluminium, with a quarter-turn catch'),
      ('Hanging', 'A 600 mm drop as standard, cut to length; a black acrylic canopy 150 mm across'),
      ('Mains', '120 V, dimmable; listing to UL 1598 to follow'),
      ('Shades', 'In all eight colours, sold singly'),
      ('Care', 'A quarter turn takes the shade off to wash: water and a drop of mild soap, then dry. No glass cleaner, alcohol or solvents: they craze acrylic.'),
      ('Figures', 'Design figures; they may change before production')]),
    ('orb', 'Core', 'Table lamp', 'A ball of tinted acrylic sitting low in a black acrylic base. Plugged in, it stays put; unplugged, it goes where the conversation is.',
     'Core lit in Ember, sitting low in its black acrylic base',
     [('Size', '160 mm ball, 180 mm tall'), ('Weight', 'About 1.5 kg'),
      ('Light', '2200 to 2700 K, warmer as it dims'), ('Control', 'Touch the black ring: tap to switch, hold to dim'),
      ('Power', 'USB-C, cable and adapter included; about five hours cordless at full brightness, longer dimmed, on cells you can replace yourself'),
      ('Rating', 'Designed to meet IP44, for terraces and spilt drinks'),
      ('Shades', 'In all eight colours, sold singly'), CARE, ('Figures', 'Design figures; they may change before production')]),
]
LAMP_PICS = {  # name: (its width on the page at 1x, the alt where the band doesn't write one)
    'lamp-dome': (800, None), 'lamp-orb': (800, None),
    'lamps-orbs': (1200, 'Eight Core lamps in a row, lit, in spectrum order: Ember, Dust, Acid, Poison, Ice, Haze, Fog and Smoke'),
    'lamps-domes': (1200, 'Eight Hemisphere pendants hung in a row at one height, lit, one in each colour'),
    'lamps-unlit': (800, 'A Core and a Hemisphere in Smoke, switched off: dark, polished acrylic, pale at the centre'),
}
TT = dict(name='Mantle', kind='Record player', route='mantle',             # round 34's (companions/README.md "Round 34"): its words when it lands
          line='A record player that floats on its own light.',
          facts=[('Plinth', 'Cast acrylic, 25 mm, tinted through; it floats 40 mm over the base'),
                 ('Base', 'Cast acrylic, edge-lit from within, dimmable'), ('Drive', 'Belt, its motor in a heavy pod of its own'),
                 ('Speeds', '33 and 45, by a button'), ('Arm', 'Rega RB330'), ('Cartridge', 'Ortofon 2M Black'),
                 ('Phono stage', 'Built in, for moving-magnet cartridges, with a line out and a switch to bypass it'),
                 ('Cover', 'Tinted acrylic, hinged'), ('Size', '470 wide, 380 deep, 194 high with the lid down (mm)'),
                 ('Weight', 'About 15.5 kg'), CARE, ('Figures', 'Design figures; they may change before production')])
# round 34's final (companions/README.md "Round 34: the record player, final (Mantle)", r32-turntable-final)
LINES = [  # the shop's three lines: key, name, what's in it, its line
    ('speakers', 'Speakers', 'Tropos', 'A powered horn loudspeaker in eight colours of cast acrylic.'),
    ('lighting', 'Lighting', 'Hemisphere and Core', 'A pendant and a table lamp in the speakers&rsquo; acrylic, frosted within.'),
    ('turntable', 'Turntable', 'Mantle', 'A record player in the same eight colours, lit from underneath.'),
]
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
    # (round 41's pass 4 first, then round 39's pass 3: the two heroes are their Ember frames, the rows their own)
    for name, (w, _) in LAMP_PICS.items():
        src = first(os.path.join(LP4, f'p4-{name}-ember.png' if name.startswith('lamp-') else f'p4-{name}.png'),
                    os.path.join(LP3, f'p3-{name}-ember.png' if name.startswith('lamp-') else f'p3-{name}.png'),
                    os.path.join(ROOT, 'renders', '2026-10-19', 'barkhorn', 'lamps-site', f'{name}.png'))
        if src:
            im = Image.open(src)
            save(im, f'{name}.jpg', 2 * w, q=84); save(im, f'{name}-{w}.jpg', w, q=84)
            made.append(name)
    # round 34, the shop: each lamp in each colour for its page and its cards (lamps_pdp.py; Ember's is round 32f's hero)
    for lamp in ('dome', 'orb'):
        for k in KEYS:
            fl = HABITAT[k]
            one(first(os.path.join(LP4, f'p4-lamp-{lamp}-{fl}.png'), os.path.join(LP3, f'p3-lamp-{lamp}-{fl}.png'),
                      os.path.join(LP, f'lamp-{lamp}-{fl}.png'),
                      os.path.join(ROOT, 'renders', '2026-10-19', 'barkhorn', 'lamps-site', f'lamp-{lamp}.png') if fl == 'ember' else ''),
                lambda p, lamp=lamp, k=k: (save(Image.open(p), f'{lamp}-{k}.jpg', 1600, q=84), save(Image.open(p), f'{lamp}-{k}-card.jpg', 640, q=82)))
    # the record player (round 34) as its pictures arrive: each colour in the studio, at dusk and in the phone's frame
    for k in KEYS:
        fl = HABITAT[k]
        one(os.path.join(TTR, f'studio-{fl}.png'), lambda p, k=k: (save(Image.open(p), f'tt-{k}-studio.jpg', 2400, q=84),
                                                                   save(Image.open(p), f'tt-{k}-studio-1200.jpg', 1200, q=82)))
        one(os.path.join(TTR, f'dusk-{fl}.png'), lambda p, k=k: (save(Image.open(p), f'tt-{k}-dusk.jpg', 2400, q=84),
                                                                 save(Image.open(p), f'tt-{k}-dusk-1200.jpg', 1200, q=82)))
        one(os.path.join(TTR, f'studio-{fl}-closed.png'), lambda p, k=k: save(Image.open(p), f'tt-{k}-closed.jpg', 2400, q=84))
        one(os.path.join(TTR, f'tall-{fl}.png'), lambda p, k=k: (save(Image.open(p), f'tt-{k}-tall.jpg', 1200, q=84),
                                                                 save(Image.open(p), f'tt-{k}-card.jpg', 640, q=82)))
    for n in ('open', 'detail', 'pod'):
        one(os.path.join(TTR, f'{n}.png'), lambda p, n=n: (save(Image.open(p), f'tt-{n}.jpg', 2400, q=84),
                                                           save(Image.open(p), f'tt-{n}-1200.jpg', 1200, q=82)))
    # until then its line shows Mantle's own proof (round 34, lit at dusk) or, before that, the concept it is drawn from
    # (round 31c's R3 Float, lit at dusk), at its own size
    one(first(os.path.join(TTR, 'proof', 'dusk-haze.png'),
              os.path.join(ROOT, 'renders', '2026-10-18', 'barkhorn', 'companions2', 'concepts', 'concept-r3-dusk.png')),
        lambda p: save(Image.open(p), 'tt-concept.jpg', None, q=88))
    one(os.path.join(TTR, 'proof', 'studio-haze.png'), lambda p: save(Image.open(p), 'tt-proof-studio.jpg', None, q=88))
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


def image_meta():
    """The pictures as they stand in site/img: each speaker's views (src, w, h), the inside shot, and each card's panel
    colour (the photograph's foot, where the panel meets it)."""
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
        if SPIN and all(os.path.exists(os.path.join(IMG, 'spin', f'{k}-{i:02d}.webp')) for i in range(SPIN_N)):
            mid = f'spin/{k}-{SPIN_HOME:02d}.webp'
            w, h = size(mid)
            views['spin'] = dict(src=f'img/{mid}', w=w, h=h, n=SPIN_N, home=SPIN_HOME, base=f'img/spin/{k}-', **ground(mid))
        views.update(campaign_views('speaker', k))
        w, h = size(f'turn-{k}.jpg')
        views['turn'] = dict(src=f'img/turn-{k}.jpg', w=w // 6, h=h // 4, **ground(f'turn-{k}.jpg', (0, 0, w // 6, h // 4)))
        meta[k] = views
        corner = np.asarray(Image.open(os.path.join(IMG, f'{k}-on.jpg')).convert('RGB'))[-18:-3].reshape(-1, 3).mean(0)   # where the photograph meets its panel
        panel[k] = '#%02X%02X%02X' % tuple(int(x) for x in corner)
    return meta, panel


def product_meta():
    """The lamps' and the record player's pictures as they stand in site/img: for each product, each colour's views
    (src, w, h), its card (the 4:5 frame the shop's grids use), and where a colour has no picture of its own yet, Ember's
    with a note saying so ('shown'). The record player is None until its pictures are in."""
    pic = lambda n, **k: dict(src=f'img/{n}', w=Image.open(os.path.join(IMG, n)).width, h=Image.open(os.path.join(IMG, n)).height, **k) \
        if os.path.exists(os.path.join(IMG, n)) else None
    out = {}
    for lamp, shared in (('dome', [('row', 'lamps-domes.jpg'), ('unlit', 'lamps-unlit.jpg')]),
                         ('orb', [('row', 'lamps-orbs.jpg'), ('unlit', 'lamps-unlit.jpg')])):
        cols = {}
        for k in KEYS:
            own = pic(f'{lamp}-{k}.jpg')
            hero, card, shown = (own, pic(f'{lamp}-{k}-card.jpg'), None) if own else (pic(f'{lamp}-red.jpg'), pic(f'{lamp}-red-card.jpg'), 'red')
            if not hero:
                continue
            views = {'hero': dict(hero, bg=ground(hero['src'][4:])['bg'], **({'shown': shown} if shown else {}))}   # the stage
            # carries the picture's own ground on past its sides (round 35: the page's paper beside a 4:5 lamp drew its edges)
            views.update({v: pic(n) for v, n in shared if pic(n)})
            views.update(campaign_views(lamp, k))
            cols[k] = dict(views=views, card=dict(card or hero, **({'shown': shown} if shown else {})))
        out[lamp] = cols
    tt = {}
    for k in KEYS:
        if not pic(f'tt-{k}-studio.jpg'):
            continue
        views = {'studio': dict(pic(f'tt-{k}-studio.jpg'), fill=True, **({'tall': pic(f'tt-{k}-tall.jpg')} if pic(f'tt-{k}-tall.jpg') else {}))}
        if pic(f'tt-{k}-dusk.jpg'):
            views['dusk'] = dict(pic(f'tt-{k}-dusk.jpg'), fill=True)
        if pic(f'tt-{k}-closed.jpg'):
            views['closed'] = dict(pic(f'tt-{k}-closed.jpg'), fill=True)
        views.update({n: pic(f'tt-{n}.jpg') for n in ('open', 'detail', 'pod') if pic(f'tt-{n}.jpg')})
        tt[k] = dict(views=views, card=pic(f'tt-{k}-card.jpg') or pic(f'tt-{k}-studio.jpg'))
    out['turntable'] = tt if len(tt) == len(KEYS) else None
    return out


def webp(rel):
    """A WebP copy of a site picture (img/<name>.jpg -> img/<name>.webp, quality 84), made when missing or older; its
    path, or the JPEG's if it can't be made. About half the bytes (round 47, mobile speed); the JPEGs stay for downloads."""
    if not rel.endswith('.jpg'):
        return rel
    src, out = os.path.join(SITE, rel), os.path.join(SITE, rel[:-4] + '.webp')
    if not os.path.exists(src):
        return rel
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
        Image.open(src).convert('RGB').save(out, 'WEBP', quality=84, method=4)
    return rel[:-4] + '.webp'


def thumbs(data):
    """Round 47 (mobile speed): each gallery view's thumbnail as a small picture of its own (site/img/thumb/, 168 px
    square, cover-cropped; a turning horn's first frame), set as the view's `th`, so the strip under a product's
    pictures no longer fetches every full-size picture (1.5 MB on Tropos's page). Made when missing or older than its
    picture."""
    os.makedirs(os.path.join(IMG, 'thumb'), exist_ok=True)
    def one(v):
        if not isinstance(v, dict) or 'src' not in v or not v['src'].startswith('img/'):
            return
        src = os.path.join(SITE, v['src'])
        name = v['src'][4:].replace('/', '-').rsplit('.', 1)[0] + '.webp'
        out = os.path.join(IMG, 'thumb', name)
        if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
            im = Image.open(src).convert('RGB')
            if v['src'].startswith('img/turn-'):
                im = im.crop((0, 0, v['w'], v['h']))
            s = 168 / min(im.size)
            im = im.resize((max(168, round(im.width * s)), max(168, round(im.height * s))), Image.LANCZOS)
            x, y = (im.width - 168) // 2, (im.height - 168) // 2
            im.crop((x, y, x + 168, y + 168)).save(out, 'WEBP', quality=72, method=6)
        v['th'] = f'img/thumb/{name}'
        if not v['src'].startswith('img/turn-'):        # the gallery's pictures as WebP (the turning horn stays a sprite)
            v['src'] = webp(v['src'])
            for t in ('tall', 'card'):
                if isinstance(v.get(t), dict) and 'src' in v[t]:
                    v[t]['src'] = webp(v[t]['src'])
    for c in data['clouds']:
        for v in c['views'].values():
            one(v)
    for L in data['lamps'].values():
        for col in L['colours'].values():
            for v in col['views'].values():
                one(v)
    if data['tt']:
        for col in data['tt']['colours'].values():
            for v in col['views'].values():
                one(v)


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
                                           '')     # one theme by choice: the dark icons were fetched and never shown
    icon_paper = lambda icon: f'<img class="ic" src="img/icon-{icon}-light.webp" alt="" width="256" height="256">'   # on a pale pill in either theme
    rank = lambda boxes: {i: 2 + r for r, i in enumerate(sorted(range(len(boxes)), key=lambda i: boxes[i]['t'] + boxes[i]['h']))}
    zs = rank(spots)                                    # in number order for the keyboard, the front rank's boxes over the back's
    hotspots = ''.join(
        f'<a class="spot" href="#speaker-{name.lower()}" style="left:{s["l"]}%;top:{s["t"]}%;width:{s["w"]}%;height:{s["h"]}%;z-index:{zs[i]}">'
        f'<span class="spot-label"><span class="spot-ic">{icon_paper(icon)}</span><b>{name}</b><span>{num}</span></span>'
        f'<span class="sr">{name}, Tropos {num}</span></a>'
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
        f'<div class="about"><p class="num">Tropos {num}</p>'
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
                    f'<img data-src="img/{k}-reel.jpg" width="{rw}" height="{rh}" alt="{name} standing on a light, its colour thrown up the wall behind it"'
                    f'{" class=on" if i == 0 else ""} decoding="async">' for i, (k, num, name, *_) in enumerate(CLOUDS)) + '</figure>\n'
                f'        <div class="light-text"><div class="light-intro">{intro}</div>\n'
                f'          <div class="light-colour"><p class="num" id="light-num">Tropos {first_[1]}</p>'
                f'<p class="light-name" id="light-name">{first_[2]}</p><p class="light-line" id="light-line">{first_[5]}</p>\n'
                f'            <div class="light-coins" role="radiogroup" aria-label="The eight colours"><span class="ring" aria-hidden="true"></span>{coins}</div></div>\n'
                '        </div>\n      </div>\n    </div>\n'
                + facade +
                '  </section>')
    if all('habitat' in meta[k] for k in KEYS):
        hw, hh = meta['red']['habitat']['w'], meta['red']['habitat']['h']
        tall = all(os.path.exists(os.path.join(IMG, f'{k}-habitat-portrait.jpg')) for k in KEYS)
        habitats = ('  <section class="band" id="habitats"><div class="wrap">\n'
                    '    <div class="head"><div><p class="eyebrow">In their element</p><h2>Each colour, where it began.</h2></div></div>\n'
                    '    <div class="hab-frame">\n'
                    '    <ul class="habitats" id="hab" tabindex="0" aria-label="The eight in their habitats">' + ''.join(
                        f'<li><a href="#speaker-{name.lower()}"><picture>'
                        + (f'<source media="(max-width: 700px)" srcset="img/{k}-habitat-portrait.jpg">' if tall else '') +
                        f'<img src="img/{k}-habitat.jpg" srcset="img/{k}-habitat-1200.jpg 1200w, img/{k}-habitat.jpg {hw}w" '
                        f'sizes="(max-width: 700px) 84vw, min(86vw, 1080px)" width="{hw}" height="{hh}" loading="lazy" '
                        f'alt="{name}, on location"></picture><span><b>{name}</b></span></a></li>'
                        for k, num, name, icon, tint, line, cover in CLOUDS) + '</ul>\n'
                    f'    <button type="button" class="nav prev" id="hab-prev" aria-label="Previous">{CHEV_L}</button>'
                    f'<button type="button" class="nav next" id="hab-next" aria-label="Next">{CHEV_R}</button>\n'
                    '    </div>\n  </div></section>')
    pm = product_meta()
    lamps_shown = all(os.path.exists(os.path.join(IMG, f'{n}.jpg')) for n in LAMP_PICS)
    def pic(name, alt, cls=''):
        w, h = Image.open(os.path.join(IMG, f'{name}.jpg')).size
        w1 = LAMP_PICS[name][0]
        return (f'<img{cls} src="img/{name}-{w1}.jpg" srcset="img/{name}-{w1}.jpg {w1}w, img/{name}.jpg {w}w" '
                f'sizes="(max-width: 720px) 100vw, 50vw" width="{w}" height="{h}" loading="lazy" alt="{alt or LAMP_PICS[name][1]}">')
    def big(name, alt, sizes='(max-width: 720px) 100vw, 50vw'):      # a 4:5 picture and its card-sized cut
        w, h = Image.open(os.path.join(IMG, name)).size
        card = name.replace('.jpg', '-card.jpg')
        srcset = (f' srcset="img/{card} {Image.open(os.path.join(IMG, card)).width}w, img/{name} {w}w" sizes="{sizes}"'
                  if os.path.exists(os.path.join(IMG, card)) else '')
        return f'<img src="img/{name}"{srcset} width="{w}" height="{h}" loading="lazy" alt="{alt}">'
    # a product's eight, as links to its page in each colour
    dots = lambda route: ('<ul class="dots-row" aria-label="Colours">' + ''.join(
        f'<li><a href="#{SLUG.get(route, route)}-{name.lower()}" aria-label="{name}" title="{name}"><span class="coin-dot" style="--i:{coin[k]}"></span></a></li>'
        for k, num, name, *_ in CLOUDS) + '</ul>')
    def ptile(route, name, kind, line, img, alt):
        return (f'<article class="ptile"><a class="ph" href="#{SLUG.get(route, route)}-ember">{big(img, alt)}</a>'
                f'<div class="pt-body"><h3>{name}<small>{kind}</small></h3><p class="line">{line}</p>{dots(route)}'
                f'<a class="more" href="#{SLUG.get(route, route)}-ember">See {name}</a></div></article>')
    # the lighting line: Hemisphere and Core, each with its eight, then the rows, and the pair switched off beside
    # Core's word on its battery (round 35: plugged in or not, the cartridge dropped)
    lighting = ('  <section class="band lamps" id="lamps"><div class="wrap">\n'
                '    <div class="head"><div><p class="eyebrow">Lighting</p><h2>The same eight, lit from within.</h2>\n'
                '      <p>A pendant and a table lamp in the speakers&rsquo; acrylic, frosted inside, so the colour glows and the '
                'source never shows. Every shade comes off by hand.</p></div></div>\n'
                '    <div class="ptiles">' + ''.join(ptile(k_, name, kind, line, f'{k_}-red.jpg', alt)
                                                    for k_, name, kind, line, alt, facts in LAMPS) + '</div>\n'
                '    <figure class="eight">' + pic('lamps-domes', None) + pic('lamps-orbs', None) +
                '<figcaption>In the speakers&rsquo; order: Ember, Dust, Acid, Poison, Ice, Haze, Fog and Smoke.</figcaption></figure>\n'
                '    <div class="lamp-duo solo"><figure>' + pic('lamps-unlit', None) + '<figcaption>Off, in Smoke.</figcaption></figure>'
                '<div class="lamp-note"><h3>Plugged in or not.</h3><p>Core runs from its cable or from the cells in its base: '
                'about five hours without the cable at full brightness, longer dimmed, and when the cells tire, you change the cells, not the lamp.</p></div></div>\n'
                '  </div></section>') if lamps_shown and pm['dome'] and pm['orb'] else ''
    # the turntable line: the record player in its eight once its pictures are in; until then the concept, and a word
    tt = pm['turntable']
    if tt:
        # its line laid out as the lamps' is: its tile beside it at dusk, then its eight as links to its page in each colour,
        # then two details (round 34's finals; the arm's close-up stays on its page, where the stand-in arm reads small)
        def tfig(img, alt, cap, sizes='(max-width: 720px) 100vw, 50vw'):
            w, h = Image.open(os.path.join(IMG, img)).size
            half = img.replace('.jpg', '-1200.jpg')
            srcset = f' srcset="img/{half} 1200w, img/{img} {w}w" sizes="{sizes}"' if os.path.exists(os.path.join(IMG, half)) else ''
            return f'<figure><img src="img/{img}"{srcset} width="{w}" height="{h}" loading="lazy" alt="{alt}"><figcaption>{cap}</figcaption></figure>'
        cw, ch = Image.open(os.path.join(IMG, 'tt-red-card.jpg')).size
        eight = ''.join(f'<li><a href="#{SLUG["turntable"]}-{name.lower()}"><img src="img/tt-{k}-card.jpg" width="{cw}" height="{ch}" '
                        f'loading="lazy" alt="{TT["name"]} in {name}"><span><span class="coin-dot" style="--i:{coin[k]}"></span>{name}</span></a></li>'
                        for k, num, name, *_ in CLOUDS)
        turntable = ('  <section class="band" id="record"><div class="wrap">\n'
                     f'    <div class="head"><div><p class="eyebrow">Turntable</p><h2>{TT["name"]}.</h2><p>A record player in the speakers&rsquo; '
                     'acrylic. Its tinted plinth floats 40&nbsp;mm over a base that glows at its edge. The motor stands apart in a pod of its '
                     'own, and the phono stage is built in.</p></div></div>\n'
                     '    <div class="lamp-duo solo tt-duo">' + ptile('turntable', TT['name'], TT['kind'], TT['line'], 'tt-ice-tall.jpg',
                                                                    f'{TT["name"]} in Fog, its base glowing') +
                     tfig('tt-violet-dusk.jpg', f'{TT["name"]} in Haze at dusk, its lid raised and the edge of its base lit violet',
                          'In Haze, at dusk.', '(max-width: 720px) 100vw, 60vw') + '</div>\n'
                     f'    <ul class="tt-eight" aria-label="{TT["name"]} in its eight colours">{eight}</ul>\n'
                     '    <div class="tt-details">' +
                     tfig('tt-open.jpg', f'{TT["name"]} in Smoke from the left, its lid raised, the motor&rsquo;s brass pod under the plinth',
                          'The lid raised. Its hinges sit on brass inserts, so no screw cuts the acrylic.') +
                     tfig('tt-pod.jpg', f'Close on {TT["name"]}&rsquo;s motor in its brass pod, standing through the base under the floating plinth',
                          'The motor stands apart, in a brass pod on soft feet, so its hum stays out of the plinth.') + '</div>\n'
                     '  </div></section>')
    else:
        def fig(img, alt, cap):
            w, h = Image.open(os.path.join(IMG, img)).size
            return (f'<figure class="concept"><img src="img/{img}" width="{w}" height="{h}" loading="lazy" alt="{alt}">'
                    f'<figcaption>{cap}</figcaption></figure>')
        figs = ([fig('tt-proof-studio.jpg', f'{TT["name"]} in Haze with its lid raised: a violet plinth floating on clear posts over a violet base',
                     f'{TT["name"]} in Haze, its lid raised.')] if os.path.exists(os.path.join(IMG, 'tt-proof-studio.jpg')) else [])
        figs.append(fig('tt-concept.jpg', f'{TT["name"]} in Haze at dusk, its lid raised: a violet plinth floating over a base whose edge glows',
                        f'{TT["name"]} in Haze, lit at dusk.'))
        turntable = ('  <section class="band" id="record"><div class="wrap soon-wrap">\n'
                     f'    <div class="head"><div><p class="eyebrow">Turntable</p><h2>{TT["name"]}, next.</h2>\n'
                     '      <p>A record player in the same eight colours. Its tinted plinth floats on clear posts over a base that '
                     'glows at its edge. The phono stage is built in, and the motor stands apart. More of it when there&rsquo;s more to show.</p></div></div>\n'
                     '    <div class="concepts">' + ''.join(figs) + '</div>\n'
                     '    <div class="acts"><a class="btn" href="#contact">Enquire</a></div>\n'
                     '  </div></section>')
    # the home page's lines and colours
    def tile(key, name, what, line, img, alt, go, soon=False):
        w, h = Image.open(os.path.join(IMG, img)).size
        return (f'<a class="tile" href="#{key}">' + ('<span class="soon">Soon</span>' if soon else '') +
                f'<img src="img/{img}" width="{w}" height="{h}" loading="lazy" alt="{alt}">'
                f'<span class="t-body"><span class="eyebrow">{name}</span><b class="t-name">{what}</b><span class="t-line">{line}</span>'
                f'<span class="t-go">{go}</span></span></a>')
    sp_img = next((f'{k}-habitat-portrait.jpg' for k in ('violet', 'green', 'red') if os.path.exists(os.path.join(IMG, f'{k}-habitat-portrait.jpg'))), 'hero-1200.jpg')
    tiles = [tile('speakers', LINES[0][1], LINES[0][2], LINES[0][3], sp_img, 'Haze, the violet speaker, before layered hills in evening light', 'See the speakers')]
    if lighting:
        tiles.append(tile('lighting', LINES[1][1], LINES[1][2], LINES[1][3], 'dome-red.jpg', 'Hemisphere lit in Ember', 'See the lighting'))
    tiles.append(tile('turntable', LINES[2][1], LINES[2][2], LINES[2][3], 'tt-ice-tall.jpg' if tt else 'tt-concept.jpg',
                      f'{TT["name"]}, the record player' if tt else f'{TT["name"]} in Haze at dusk, its base glowing',
                      'See the record player' if tt else 'See where it stands', soon=not tt))
    lines = ('  <section class="band" id="lines"><div class="wrap">\n'
             '    <div class="head"><div><p class="eyebrow">The lines</p><h2>One acrylic, three ways to use it.</h2></div></div>\n'
             f'    <div class="lines">{"".join(tiles)}</div>\n  </div></section>')
    colours = ('  <section class="band" id="colours"><div class="wrap">\n'
               '    <div class="head"><div><p class="eyebrow">By colour</p><h2>Eight colours, every line.</h2>\n'
               '      <p>Each colour runs through everything we make, so a room can be one colour or three.</p></div></div>\n'
               '    <ul class="shopcol">' + ''.join(
                   f'<li><a href="#colour-{name.lower()}"><span class="coin-dot" style="--i:{coin[k]}"></span><b>{name}</b></a></li>'
                   for k, num, name, icon, tint, line, cover in CLOUDS) + '</ul>\n  </div></section>')
    data = dict(
        clouds=[dict(k=k, num=num, name=name, icon=icon, tint=tint, line=line, cover=cover, col=MARK[k], hue=HUE.get(k),
                     coin=coin[k], views=meta[k], place=PLACES.get(ELEMENT[k], 'on location'))
                for k, num, name, icon, tint, line, cover in CLOUDS],
        hues=E.HUES, care=CARE[1],
        lamps={k_: dict(name=name, kind=kind, line=line, facts=facts, colours=pm[k_], route=SLUG[k_]) for k_, name, kind, line, alt, facts in LAMPS} if lighting else {},
        tt=dict(TT, colours=tt) if tt else None, view3d=view3d(),
        campaign=[{x: c[x] for x in ('product', 'view', 'after', 'label', 'caption', 'alt')} for c in CAMPAIGN])
    thumbs(data)
    # a phone frame of the hero or the room, where one was made (re-framed, not cropped); with the hero's, its links
    # give way on phones to the names under it, the boxes being the landscape frame's
    tall = lambda f: os.path.exists(os.path.join(IMG, f))
    hero_tall = ('<source media="(max-width: 700px)" data-srcset="img/hero-portrait.webp">' if tall('hero-portrait.jpg') else '')
    for f in ('hero.jpg', 'hero-1200.jpg', 'hero-portrait.jpg'):
        webp('img/' + f)
    room_tall = ('<source media="(max-width: 700px)" srcset="img/room-portrait.jpg">' if tall('room-portrait.jpg') else '')
    if hero_tall:
        hotspots = hotspots.replace('class="spot"', 'class="spot wide-only"')
    if hero_tall and tall('hero-spots-portrait.json'):    # the phone frame's own boxes: the back rank first, so the front's lie over it
        ps = json.load(open(os.path.join(IMG, 'hero-spots-portrait.json')))
        ps = ps['portrait'] if isinstance(ps, dict) else ps
        zp = rank(ps)
        hotspots += ''.join(
            f'<a class="spot tall-only" href="#speaker-{name.lower()}" style="left:{s["l"]}%;top:{s["t"]}%;width:{s["w"]}%;height:{s["h"]}%;z-index:{zp[i]}">'
            f'<span class="sr">{name}, Tropos {num}</span></a>'
            for i, ((k, num, name, *_), s) in enumerate(zip(CLOUDS, ps)))
    lead = {}                                           # each product page's first picture: wide, and its phone frame
    for c in data['clouds']:
        v = c['views'].get('habitat') or c['views'].get('on')
        lead[f"speaker-{c['name'].lower()}"] = [v['src'], (v.get('tall') or {}).get('src')]
        for L in data['lamps'].values():
            col = L['colours'].get(c['k'])
            if col:
                lead[f"{L['route']}-{c['name'].lower()}"] = [col['views']['hero']['src'], None]
        if data['tt'] and c['k'] in data['tt']['colours']:
            v = data['tt']['colours'][c['k']]['views']['studio']
            lead[f"mantle-{c['name'].lower()}"] = [v['src'], (v.get('tall') or {}).get('src')]
    wl_form, wl_page = waitlist_html()
    page = (PAGE.replace('__WORD__', word).replace('__HOTSPOTS__', hotspots).replace('__NAMES__', names)
                .replace('__HERO_TALL__', hero_tall).replace('__ROOM_TALL__', room_tall)
                .replace('__HERO_CLASS__', ' has-tall' if hero_tall else '')
                .replace('__TURN__', turn).replace('__CARDS__', cards).replace('__SPEC__', spec).replace('__DWG__', dwg)
                .replace('__REEL__', reel).replace('__HABITATS__', habitats).replace('__CLOSER__', closer)
                .replace('__LINES__', lines).replace('__COLOURS__', colours).replace('__LIGHTING__', lighting).replace('__TURNTABLE__', turntable)
                .replace('__PRESS__', press_html()).replace('__JOURNAL__', journal_html()).replace('__JOURNAL_BAND__', journal_band())
                .replace('__WAITLIST__', wl_form).replace('__PRIVACY__', wl_page)
                .replace('__FOOT_PRIVACY__', '<a href="#privacy">Privacy</a>' if WAITLIST else '')
                .replace('__FONTS__', open(os.path.join(HERE, 'webfonts', 'fonts.css')).read().strip())
                .replace('__LEAD__', json.dumps(lead, separators=(',', ':'))).replace('__STILL__', still).replace('__POSTER__', poster).replace('__POSTER_NIGHT__', poster_night).replace('__DATA__', json.dumps(data, separators=(',', ':'))))
    if not VIEW3D:      # the 3D view's markup and script stay out of the page entirely while it is off
        page = re.sub(r'\n *<!--3D-->.*?<!--/3D-->', '', page, flags=re.S)
        page = re.sub(r'/\*3D\*/.*?/\*/3D\*/', '', page, flags=re.S)
        page = re.sub(r'//3D\n.*?///3D', 'function v3sync() {}\nfunction v3close() {}', page, flags=re.S)
    cut = page.index('</style>') + len('</style>')
    return page[:cut], page[cut:]


# round 47 (the site's next pass, 2026-10-31): a press page, a journal, and a waitlist kept switched off. The press page
# states only what the site and the READMEs already say; its two slots (who's behind it, and whom the press write to)
# stay out of the page until the owner fills them here, and the page says nothing in their place.
PRESS = {
    'founder': None,     # SLOT, the owner's: e.g. ('Name', 'Founder', 'A line on them, in their words'); None leaves it off the page
    'contact': None,     # SLOT, the owner's: the press address, e.g. 'press@earf.world' (earf.world has no mail records yet)
}
BOILER_SHORT = ('EARF is a San Francisco maker of hi-fi and lighting in cast acrylic, tinted all the way through, in eight '
                'colours from Ember to Smoke. Its first four pieces are Tropos, a powered horn loudspeaker; Hemisphere, a '
                'pendant lamp; Core, a cordless table lamp; and Mantle, a record player.')
BOILER_LONG = (BOILER_SHORT + ' Every piece is cut, formed and cemented from the same acrylic, so a speaker, a lamp and a '
               'record player can share one colour or take three. All four are in development and not yet for sale: each is '
               'drawn for making, and the first pair of Tropos will be built as production will build it, then measured. '
               'Planet EARF, a listening bar in San Francisco, is planned.')
PRESS_PICS = [  # file in site/img, what it shows (the link's words and the picture's alt)
    ('hero.jpg', 'The eight Tropos speakers on a curve, covers off, Ember to Smoke'),
    ('room.jpg', 'A pair of Tropos in Poison at home, covers on, by a tall window'),
    ('red-habitat.jpg', 'Tropos in Ember on a lava field at blue hour'),
    ('violet-habitat.jpg', 'Tropos in Haze before layered hills in evening light'),
    ('black-habitat.jpg', 'Tropos in Smoke on a city overpass at dusk'),
    ('facade.jpg', 'The eight on lights at the foot of a concrete wall by a river at night'),
    ('red-studio-light.jpg', 'Tropos in Ember in the studio, on a pale ground'),
    ('dome-red.jpg', 'Hemisphere lit, its Ember shade beneath a black hub'),
    ('orb-red.jpg', 'Core lit in Ember, low in its black acrylic base'),
    ('lamps-domes.jpg', 'Eight Hemisphere pendants in a row, lit, one in each colour'),
    ('tt-violet-dusk.jpg', 'Mantle in Haze at dusk, its lid raised and its base lit'),
    ('tt-red-studio.jpg', 'Mantle in Ember in the studio, its lid raised'),
]
LOGOS = ['earf-lockup-black.svg', 'earf-lockup-black.png', 'earf-lockup-white.svg', 'earf-lockup-white.png',
         'earf-lockup-colour.svg', 'earf-lockup-colour.png', 'earf-globe-colour.svg', 'earf-globe-colour.png',
         'earf-globe-black.svg', 'earf-globe-black.png', 'earf-wordmark-black.svg', 'earf-wordmark-white.svg']
JOURNAL = [  # slug, date, title, standfirst, card picture (site/img), and the body: ('p', html) or ('fig', file, alt, caption)
    ('eight-colours', '2026-10-31', 'Eight colours, all the way through',
     'Paint is a decision you can sand off. Tint is one you live with.', 'violet-habitat-1200.jpg', [
        ('p', 'Every EARF piece is cast acrylic with its colour mixed in before the sheet sets. So the colour runs to the '
              'edge, and the edge is where it shows best: cast acrylic carries light along its length and lets it out '
              'wherever it is cut.'),
        ('p', 'There are eight. Six go round the painter&rsquo;s wheel: Ember, Dust, Acid, Poison, Ice and Haze. Two have no '
              'hue at all. Fog is water-clear, almost not there; Smoke is smoked glass, for after dark.'),
        ('fig', 'red-habitat.jpg', 'Tropos in Ember on a lava field at blue hour, the crust cracked to its glow',
         'Ember, on a lava field at blue hour.'),
        ('p', 'Each one began somewhere, and we went looking for it. Ember on a lava field at blue hour, the crust cracked to '
              'its glow. Dust on rippled sand at golden hour. Acid in acid rain on black lava. Poison on a redwood floor, '
              'among death caps and a deer&rsquo;s bones. Smoke on a city overpass, come down like a meteor.'),
        ('fig', 'black-habitat.jpg', 'Tropos in Smoke on a city overpass at dusk, the road torn open and burning behind it',
         'Smoke, on an overpass at dusk.'),
        ('p', 'The same eight run through everything we make. The lamps&rsquo; shades are cast so that, lit from within, '
              'each reads as its speaker does by day; Mantle&rsquo;s plinth is the same sheet again. A room can be one '
              'colour, or three.'),
        ('p', 'If three, the wheel helps. Every colour&rsquo;s page shows the company it keeps: its opposite, its '
              'neighbours, and itself in the other lines. Fog and Smoke, having no hue, pair with each other: the same '
              'acrylic, light and dark. <a href="#colours">See the eight</a>.'),
     ]),
    ('the-horn', '2026-10-31', 'How the horn is formed',
     'A horn is a shape that does an amplifier&rsquo;s job. Here is how ours will be made.', 'amber-horn-side.jpg', [
        ('p', 'Long before amplifiers, a horn was how a small sound filled a large room. Tropos&rsquo;s is formed from the '
              'same tinted acrylic as its cabinet, and how it is formed decides how it sounds.'),
        ('p', 'The air path came first. Its profile was worked out by simulation before any acrylic was cut, and the tool '
              'is cut to that profile. Everything else serves it.'),
        ('fig', 'macro-horn.jpg', 'The Acid horn from the side: its flare, and its driver&rsquo;s pod behind it',
         'The flare, and the driver&rsquo;s pod behind it.'),
        ('p', 'The sheet is cast acrylic, 10&nbsp;mm, from a dye lot about three times as strong as the cabinet&rsquo;s, so a '
              'thinner wall reads as deep as the 20&nbsp;mm beside it. It is heated to about 170&nbsp;&deg;C until it is '
              'rubbery all the way through. Cast sheet doesn&rsquo;t melt; it gives.'),
        ('p', 'Then it is blown into a shallow bubble, a plug rises into it, and a pressure box closes over the top at 4 bar '
              'while vacuum draws through fine vents in the plug. The plug is the horn&rsquo;s air path, so the face '
              'that lies on the tool is the face the sound sees, and it is exact. The outside touches nothing, so it '
              'keeps the sheet&rsquo;s own gloss.'),
        ('p', 'Why over a plug and not into a mould: the sheet thins as it stretches, and over a plug it thins toward the '
              'mouth, where the shape wants it thin. Into a mould, it would thin toward the throat, where it can least '
              'afford to.'),
        ('p', 'The horn is annealed, trimmed on a five-axis router, and its rim routed round and polished. The throat is '
              'turned from a solid block of the same lot and cemented on, both air faces cut to one surface so they '
              'meet without a step. Behind it, in a pod whose cap twists off by hand, sits a 2-inch compression driver. '
              'Above 1&nbsp;kHz the horn carries the music; below, the 15-inch woofer does.'),
        ('p', 'The first horns off the tool will be cut open and measured at thirty points. If the corners come out thin, '
              'the next sheet is 12&nbsp;mm. <a href="#turn">The horn, turning</a>.'),
     ]),
    ('planet-earf', '2026-10-31', 'Planet EARF',
     'A listening bar in San Francisco. Planned: no address yet, and no opening night.', 'planet-street-1200.jpg', [
        ('p', 'Somewhere to hear the speakers properly, with a drink, among people who came for the same reason.'),
        ('fig', 'planet-street.jpg', 'A narrow shopfront at dusk, EARF on the glass, a warm room of records behind it',
         'A first drawing of the street front.'),
        ('p', 'The room we are drawing is narrow: one shopfront, one long room. Board-formed concrete, Douglas fir beams, '
              'blackened steel. The acrylic stays clear, frosted or smoked, thick and polished at the edge, so that the '
              'speakers are the colour in the room and nothing else is.'),
        ('p', 'The bar runs down one side, records fill the wall at the back, and a pair stands at the far end where it can '
              'be heard rather than seen. Core sits on every table. It is dim, but never so dim you can&rsquo;t read a '
              'sleeve.'),
        ('fig', 'planet-room.jpg', 'A long, dim room: the bar on the left, Core lamps on small tables, a pair of speakers at '
                                   'the far end, a large ringed globe hung overhead',
         'Inside, as drawn so far.'),
        ('p', 'Nothing here is final, and all of it is a render. When there is an address, it will be on this page first.'),
     ]),
]
# the pictures the journal brings from elsewhere in the repository (Planet EARF's, from its own session's renders): the
# file in site/img, its source under renders/, and its width; a picture whose source is not to hand is kept as it is
JOURNAL_PICS = [('planet-street.jpg', 'renders/2026-10-22/barkhorn/planet39/finals/street-2400.jpg', 2400),
                ('planet-street-1200.jpg', 'renders/2026-10-22/barkhorn/planet39/finals/street-1200.jpg', 1200),
                ('planet-room.jpg', 'renders/2026-10-22/barkhorn/planet41/finals/door-mother-colour-p3-2400.jpg', 2400)]
# the waitlist: ready, and off until the owner picks a provider (launch/waitlist-options.md) and its privacy notice is
# approved (launch/policies-draft.md, section 4). With WAITLIST False the page carries no form, no notice and no route.
WAITLIST = False
WAITLIST_ACTION = ''     # the provider's endpoint, once chosen: e.g. a Buttondown embed URL, or /api/waitlist (a Vercel function)
WAITLIST_FIELD = 'email'  # the field name the provider expects for the address
PRIVACY_DATE = '[OWNER: the date it goes live]'
PRIVACY = [  # the notice, as drafted in launch/policies-draft.md (section 4), for counsel
    ('What we collect', 'Your email address, and which pieces you tick, if any. Nothing else is asked for. Like any website, '
     'ours is served by a host (Vercel) that logs the address your browser connects from, for security; we keep no '
     'cookies and run no analytics or advertising trackers.'),
    ('Why', 'To write to you about EARF: when there is something new to see, and when the pieces you ticked can be ordered. '
     'Nothing else, and we don&rsquo;t sell, rent or swap the list.'),
    ('Who holds it', 'The list is kept for us by [OWNER: the provider, once chosen], which sends our emails and stores the '
     'list on its servers in [OWNER: its location]. It may use it only to provide that service to us.'),
    ('Leaving, and seeing what we hold', 'Every email has a link to unsubscribe. To see, correct or delete what we hold, '
     'write to [OWNER: the address]; we will do it within 30 days.'),
    ('Do Not Track', 'We track no one across sites, so a browser&rsquo;s Do Not Track signal changes nothing here: there '
     'is nothing for it to turn off.'),
    ('Children', 'The list is not meant for anyone under 16, and we don&rsquo;t knowingly keep their addresses.'),
    ('Changes', 'If this notice changes, the new one goes here with its date; a change in what we do with your address '
     'will be emailed to you before it takes effect.'),
    ('Who we are', '[OWNER: the legal name and postal address of the company], San Francisco, California.'),
]


# round 47: Tropos turning, path-traced (spin47.py): the front arc, about 46 degrees either side of face-on in nine frames
# (-20 to +60 degrees of turn from the stills' own angle, which stands 26 degrees off the face), in the studio's
# bright field, dragged on the product's page in place of the real-time 3D view (the critic's round 2 kept the arc: the
# profile and the back read muddy). SPIN False keeps it off; on, a colour shows it once its nine frames are in site/img/spin/.
SPIN = True       # on (2026-10-31): critic round 3 scored the front arc level with the stills (6 against 6); critic/LOG.md
SPIN_SRC = os.path.join(ROOT, 'renders', '2026-10-31', 'barkhorn', 'spin47')
SPIN_ARC, SPIN_W = [i % 36 for i in range(-2, 7)], 600     # spin47's file numbers, from -20 to +60 degrees of turn
SPIN_N, SPIN_HOME = len(SPIN_ARC), 2                        # it opens on frame 2, the stills' own angle
SPIN_NAME = {'red': 'ember', 'orange': 'dust', 'amber': 'acid', 'green': 'poison', 'blue': 'ice', 'violet': 'haze', 'ice': 'fog', 'black': 'smoke'}


# round 47: slots for the campaign finals (the product sessions', 2026-10-31), empty until the owner picks. Each entry
# adds one picture to a product's gallery: `product` the page's id ('speaker', 'dome' for Hemisphere, 'orb' for Core),
# `view` its key, `src` the render under the repository ({name} for each colour's name, e.g. ember, when the picture is
# per colour; without it the one picture shows on every colour's page), `after` the view it follows ('' to lead),
# `label` the thumbnail's name, `caption` and `alt` (with {name} for the colour). To swap one in: add the entry, then
# `python3 web.py --images`. Example (not live):
#   dict(product='speaker', view='campaign', src='renders/2026-10-31/barkhorn/tropos-campaign/{name}.png', after='habitat',
#        label='Campaign', caption='{name}, ...', alt='Tropos in {name} ...')
CAMPAIGN = []


def make_campaign():
    """The campaign slots' pictures: site/img/campaign/<product>-<view>-<key>.jpg (2400 wide) and -1200.jpg, or
    <product>-<view>.jpg for one shared picture; a source not to hand keeps what is there."""
    made = []
    os.makedirs(os.path.join(IMG, 'campaign'), exist_ok=True)
    for c in CAMPAIGN:
        for k, name in (SPIN_NAME.items() if '{name}' in c['src'] else [(None, None)]):
            p = os.path.join(ROOT, c['src'].format(name=name))
            if not os.path.exists(p):
                continue
            base = f"campaign/{c['product']}-{c['view']}" + (f'-{k}' if k else '')
            im = Image.open(p)
            made += [save(im, base + '.jpg', 2400, q=84), save(im, base + '-1200.jpg', 1200, q=82)]
    return made


def campaign_views(product, k):
    """The campaign pictures in site/img for a product's page in colour `k`, as gallery views."""
    out = {}
    for c in CAMPAIGN:
        if c['product'] != product:
            continue
        for f in (f"campaign/{product}-{c['view']}-{k}.jpg", f"campaign/{product}-{c['view']}.jpg"):
            if os.path.exists(os.path.join(IMG, f)):
                w, h = Image.open(os.path.join(IMG, f)).size
                out[c['view']] = dict(src=f'img/{f}', w=w, h=h, fill=True)
                break
    return out


def make_spin():
    """Each colour's turning frames for the site, from spin47's renders where the arc's nine are in:
    site/img/spin/<key>-NN.webp, 00 at -20 degrees of turn to 08 at +60 (02 is the stills' angle)."""
    made = []
    os.makedirs(os.path.join(IMG, 'spin'), exist_ok=True)
    for f in os.listdir(os.path.join(IMG, 'spin')):     # frames from an earlier, longer turn
        if not re.fullmatch(r'[a-z]+-0[0-8]\.webp', f):
            os.remove(os.path.join(IMG, 'spin', f))
    for k, name in SPIN_NAME.items():
        src = [os.path.join(SPIN_SRC, name, f'f-{i:02d}.png') for i in SPIN_ARC]
        if not all(os.path.exists(p) for p in src):
            continue
        for i, p in enumerate(src):
            im = Image.open(p).convert('RGB')
            im = im.resize((SPIN_W, round(im.height * SPIN_W / im.width)), Image.LANCZOS)
            im.save(os.path.join(IMG, 'spin', f'{k}-{i:02d}.webp'), 'WEBP', quality=80, method=6)
            made.append(f'spin/{k}-{i:02d}.webp')
    return made


# round 47: the 3D view (viewer/, its README). Each product with a model in viewer/dist/ (site/3d/ once on) gets a "View in 3D" on its page; the
# finishes come from the engine's product file (what the renders were painted with), simplified to what a browser
# paints, and each colour's acrylic is the engine's own: the colour it reaches after a distance (Beer's law), which is
# three.js's attenuation. VIEW3D False takes the button off everywhere.
VIEW3D = False     # off (2026-10-31): a blind critic scored its frames 3.5 to 4 against the renders' 6.5 to 7, "hurt" beside them (viewer/README.md)
FLAVOUR3D = {'red': 'cloud-red', 'orange': 'cloud-orange', 'amber': 'cloud-amber', 'green': 'eucalyptus-y2k-green',
             'blue': 'cloud-blue', 'violet': 'cloud-violet', 'ice': 'birch-fog-clear', 'black': 'cloud-black'}   # finals.py's


def view3d():
    """The 3D view's spec for each product whose model is in viewer/dist (by the product's route), and each colour's tints."""
    out = {}
    if not VIEW3D or not os.path.exists(os.path.join(HERE, 'viewer', 'dist', 'tropos.glb')):
        return out
    eng = json.load(open(os.path.join(ROOT, 'studio', 'products', 'barkhorn-cloud.json')))
    simple = {'satin_paint': 0.45, 'plastic': 0.45, 'gloss_plastic': 0.18, 'rubber': 0.8, 'treated_paper': 0.7, 'ecoat': 0.42,
              'doped_cloth': 0.85, 'cloth': 0.95, 'batting': 0.95, 'opaque_acrylic': 0.12}
    fin = {}
    for name, m in eng['materials'].items():
        p, col = m.get('preset', ''), m.get('color', '#888888')
        if p in ('$bark', '$horn_preset') or name in ('bark', 'horn', 'print', 'amp-label', 'amp-foil'):
            continue
        f = dict(color=col if not col.startswith('$') else '#888888', roughness=m.get('roughness', simple.get(p, 0.5)))
        if p in ('metal', 'black_oxide'):
            f.update(metal=1, color='#2A2A2A' if p == 'black_oxide' else col, roughness=m.get('roughness', 0.4))
        if p == 'emit':
            f.update(emit=m.get('strength', 2) / 3)
        if p in ('batting', 'cloth', 'doped_cloth'):
            f.update(sheen=0.6)
        if p == 'batting':
            f.update(color='#EFF0EE')
        if p == 'opaque_acrylic':
            f.update(coat=1)
        fin[name] = f
    tints = {}
    for k, fl in FLAVOUR3D.items():
        v = eng['flavours'][fl]
        tints[k] = dict(deep=v['materials']['bark']['deep'], horn=v['horn_deep'], disc=v['disc'])
    out['speaker'] = dict(src='3d/tropos.glb', finishes=fin, tints=tints,
                          # the walls 20 mm and the horn 6 to 8.5, each seen through twice; their depth grows across a face
                          acrylic={'bark': dict(deep='deep', radius=0.025, roughness=0.02, thickness=0.035),
                                   'horn': dict(deep='horn', radius=0.01, roughness=0.03, thickness=0.012)},
                          # inside, lit through a wall: the lining's light has crossed one already
                          inside={'lining': dict(through='deep', light=0.5, dim=0.42), 'driver-frame': dict(through='deep', light=0.6),
                                  'driver-motor': dict(through='deep', light=0.6)},
                          tinted={'ring': 'disc', 'disc': 'disc', 'mark-tint': 'disc'}, hide=['disc'],   # cover off, as the cards open
                          ground='#F3F1EC', azimuth=14, elevation=-2, aim=0.55, fov=20,
                          label='Tropos in {name}, in 3D, cover off. Drag or use the arrow keys to turn it; plus and minus to come closer.')
    return out


def press_html():
    """The press page: who we are in two lengths, the slots (only once filled), the particulars, the names, the pictures."""
    nb = lambda t: re.sub(r'(\d) (mm|kg|Hz)\b', '\\1\u00a0\\2', t)
    sheet = lambda title, kind, facts: (f'<section class="sheet"><h3>{title}<small>{kind}</small></h3><dl>' +
                                        ''.join(f'<dt>{a}</dt><dd>{nb(b)}</dd>' for a, b in facts if a not in ('Care',)) + '</dl></section>')
    sheets = (sheet('Tropos', 'Powered horn loudspeaker', [x for x in SPEC if x[0] not in ('Lining',)]) +
              ''.join(sheet(name, kind, facts) for k_, name, kind, line, alt, facts in LAMPS) +
              sheet(TT['name'], TT['kind'], TT['facts']))
    slots = ''
    if PRESS['founder']:
        n, role, about = PRESS['founder']
        slots += f'<div class="slot"><p class="eyebrow">Behind it</p><p><b>{n}</b>, {role}. {about}</p></div>'
    if PRESS['contact']:
        slots += (f'<div class="slot"><p class="eyebrow">Press enquiries</p><p><a href="mailto:{PRESS["contact"]}">'
                  f'{PRESS["contact"]}</a></p></div>')
    slots = slots or ('<!-- press slots: the founder and the press address go here once the owner fills PRESS in web.py; '
                      'nothing shows until then -->')
    size = lambda f: Image.open(os.path.join(IMG, f)).size
    def dl(f, what):
        w, h = size(f); kb = os.path.getsize(os.path.join(IMG, f)) // 1024
        small = f.replace('.jpg', '-1200.jpg'); small = small if os.path.exists(os.path.join(IMG, small)) else f
        card = f.replace('.jpg', '-card.jpg'); thumb = card if os.path.exists(os.path.join(IMG, card)) else small
        tw, th = size(thumb)
        return (f'<li><figure><img src="img/{thumb}" width="{tw}" height="{th}" loading="lazy" alt="{what}">'
                f'<figcaption>{what}. <a href="img/{f}" download>JPEG, {w}&thinsp;&times;&thinsp;{h}, {kb:,}&nbsp;KB</a></figcaption></figure></li>')
    pics = ''.join(dl(f, what) for f, what in PRESS_PICS if os.path.exists(os.path.join(IMG, f)))
    zkb = os.path.getsize(os.path.join(SITE, 'press', 'earf-logos.zip')) // 1024 if os.path.exists(os.path.join(SITE, 'press', 'earf-logos.zip')) else 0
    logos = (f'<p class="logo-dl"><a class="btn" href="press/earf-logos.zip" download>The marks, SVG and PNG ({zkb:,}&nbsp;KB)</a>'
             '<span>The lockup, the globe and the wordmark, in black, white and colour.</span></p>') if zkb else ''
    kit = os.path.join(SITE, 'press', 'earf-press-kit.pdf')       # viewer/presskit.mjs prints it from this page
    if os.path.exists(kit):
        logos += (f'<p class="logo-dl"><a class="btn" href="press/earf-press-kit.pdf" download>This page as a PDF '
                  f'({os.path.getsize(kit) // 1024:,}&nbsp;KB)</a><span>Four pages: who we are, the names, the particulars, the pictures.</span></p>')
    tints = ''.join(f'<li><span class="coin-dot" style="--i:{i}"></span><b>{name}</b><span>{tint}</span></li>'
                    for i, (k, num, name, icon, tint, line, cover) in enumerate(CLOUDS))
    return f'''
<main id="press" hidden>
  <div class="wrap">
    <p class="crumbs"><a href="#top">Home</a> / Press</p>
    <div class="ed-head"><p class="eyebrow">Press</p><h1>EARF, for the record.</h1>
      <p class="lede">Who we are in two lengths, the particulars, and the pictures at full size. Nothing is built yet, so every
        picture is a render; we&rsquo;d be glad if you said so.</p></div>
    <section class="ed-band" aria-labelledby="pr-about"><h2 id="pr-about">About EARF</h2>
      <div class="boiler"><div><p class="eyebrow">In one breath</p><p id="boiler-short">{BOILER_SHORT}</p>
        <button type="button" class="btn copy-text" data-copy="boiler-short">Copy</button></div>
      <div><p class="eyebrow">In a paragraph</p><p id="boiler-long">{BOILER_LONG}</p>
        <button type="button" class="btn copy-text" data-copy="boiler-long">Copy</button></div></div>
      <p class="copied" aria-live="polite"></p>
      {slots}
    </section>
    <section class="ed-band" aria-labelledby="pr-names"><h2 id="pr-names">Names and colours</h2>
      <p class="ed-note">EARF in capitals. Tropos, Hemisphere, Core and Mantle each take a capital, and so do the colours:
        Tropos in Ember, not in ember. Every piece comes in all eight.</p>
      <ul class="tints">{tints}</ul>
    </section>
    <section class="ed-band" aria-labelledby="pr-facts"><h2 id="pr-facts">The particulars</h2>
      <p class="ed-note">Design figures, from the drawings and their simulation; measured ones follow the first builds.
        Prices are set at launch.</p>
      <div class="sheets">{sheets}</div>
    </section>
    <section class="ed-band" aria-labelledby="pr-pics"><h2 id="pr-pics">Pictures</h2>
      <p class="ed-note">Free to use in writing about EARF, credited &ldquo;Render: EARF&rdquo;. Please don&rsquo;t crop
        out the colour or alter it.</p>
      {logos}
      <ul class="dl-grid">{pics}</ul>
    </section>
  </div>
</main>'''


def journal_band():
    """The home page's three latest posts, above the enquiries."""
    posts = [p for p in JOURNAL if os.path.exists(os.path.join(IMG, p[4]))][:3]
    if not posts:
        return ''
    return ('  <section class="band" id="from-journal"><div class="wrap">\n'
            '    <div class="head"><div><p class="eyebrow">Journal</p><h2>Notes from the bench.</h2></div>'
            '<a class="btn" href="#journal">All notes</a></div>\n'
            f'    <ul class="jlist jband">{"".join(journal_card(*p[:5]) for p in posts)}</ul>\n  </div></section>')


def journal_when(d):
    y, m, dd = d.split('-')
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
             'December'][int(m) - 1]
    return f'<time datetime="{d}">{int(dd)} {month} {y}</time>'


def journal_card(slug, d, title, stand, pic, h='b'):
    w, hh = Image.open(os.path.join(IMG, pic)).size
    return (f'<li><a class="jcard" href="#journal-{slug}"><img src="img/{pic}" width="{w}" height="{hh}" loading="lazy" alt="">'
            f'<span class="eyebrow">{journal_when(d)}</span><b>{title}</b><span>{stand}</span></a></li>')


def journal_html():
    """The journal: an index of its posts, then each post, one at a time (#journal, #journal-<slug>)."""
    when = journal_when
    def fig(f, alt, cap):
        if not os.path.exists(os.path.join(IMG, f)):
            return ''
        w, h = Image.open(os.path.join(IMG, f)).size
        half = f.replace('.jpg', '-1200.jpg')
        srcset = f' srcset="img/{half} 1200w, img/{f} {w}w" sizes="(max-width: 760px) 100vw, 720px"' if os.path.exists(os.path.join(IMG, half)) and w > 1200 else ''
        return f'<figure><img src="img/{f}"{srcset} width="{w}" height="{h}" loading="lazy" alt="{alt}"><figcaption>{cap} A render.</figcaption></figure>'
    card = journal_card
    posts = [p for p in JOURNAL if os.path.exists(os.path.join(IMG, p[4]))]
    index = ''.join(card(s, d, t, st, pic) for s, d, t, st, pic, body in posts)
    arts = ''
    for i, (slug, d, title, stand, pic, body) in enumerate(posts):
        nxt = posts[(i + 1) % len(posts)]
        text = ''.join(f'<p>{b[1]}</p>' if b[0] == 'p' else fig(*b[1:]) for b in body)
        arts += (f'<article class="post" id="journal-{slug}" data-title="{re.sub("&[a-z]+;", "", title)}" hidden>'
                 f'<p class="crumbs"><a href="#top">Home</a> / <a href="#journal">Journal</a></p>'
                 f'<header><p class="eyebrow">{when(d)}</p><h1>{title}</h1><p class="stand">{stand}</p></header>'
                 f'<div class="post-body">{text}</div>'
                 f'<p class="post-next">Next: <a href="#journal-{nxt[0]}">{nxt[2]}</a></p></article>')
    return f'''
<main id="journal" hidden>
  <div class="wrap">
    <div class="jindex" id="journal-index">
      <p class="crumbs"><a href="#top">Home</a> / Journal</p>
      <div class="ed-head"><p class="eyebrow">Journal</p><h1>Notes from the bench.</h1>
        <p class="lede">How things are made, why they look the way they do, and what comes next.</p></div>
      <ul class="jlist">{index}</ul>
    </div>
    {arts}
  </div>
</main>'''


def waitlist_html():
    """The waitlist's form for the enquiries band, and its privacy notice as a page; both '' while WAITLIST is off."""
    if not WAITLIST:
        return '', ''
    picks = ''.join(f'<label><input type="checkbox" name="interest" value="{v}"> {v}</label>'
                    for v in ('Tropos', 'Hemisphere', 'Core', 'Mantle', 'Planet EARF'))
    form = f'''
    <form class="waitlist" id="waitlist" action="{WAITLIST_ACTION}" method="post" novalidate>
      <h3>Hear first.</h3>
      <p>One email when there&rsquo;s something new to see, and one when it can be ordered. That&rsquo;s all.</p>
      <div class="wl-row"><label for="wl-email" class="sr">Email address</label>
        <input id="wl-email" name="{WAITLIST_FIELD}" type="email" autocomplete="email" required placeholder="you@example.com" aria-describedby="wl-note">
        <button class="btn solid" type="submit">Join the list</button></div>
      <fieldset><legend>Most interested in (optional)</legend>{picks}</fieldset>
      <input type="text" name="website" tabindex="-1" autocomplete="off" class="hp" aria-hidden="true">
      <p class="wl-note" id="wl-note">Unsubscribe from any email. <a href="#privacy">How we keep your address</a>.</p>
      <p class="wl-status" id="wl-status" role="status"></p>
    </form>'''
    page = ('\n<main id="privacy" hidden><div class="wrap"><p class="crumbs"><a href="#top">Home</a> / Privacy</p>'
            '<div class="ed-head"><p class="eyebrow">Privacy</p><h1>Your address, and what we do with it.</h1>'
            f'<p class="lede">In effect from {PRIVACY_DATE}. Short, because we keep very little.</p></div><dl class="policy">' +
            ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in PRIVACY) + '</dl></div></main>')
    return form, page


def make_editorial():
    """The press kit's zip of marks (site/press/earf-logos.zip) and the journal's pictures from elsewhere in the
    repository; a source not to hand keeps what is there."""
    import zipfile
    os.makedirs(os.path.join(SITE, 'press'), exist_ok=True)
    marks = [os.path.join(BRAND, 'mark', f) for f in LOGOS if os.path.exists(os.path.join(BRAND, 'mark', f))]
    if marks:
        with zipfile.ZipFile(os.path.join(SITE, 'press', 'earf-logos.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
            for f in marks:                     # dated, so the same marks make the same zip
                z.writestr(zipfile.ZipInfo(os.path.basename(f), (2026, 10, 31, 0, 0, 0)), open(f, 'rb').read(), zipfile.ZIP_DEFLATED)
    made = []
    for name, srcp, w in JOURNAL_PICS:
        p = os.path.join(ROOT, srcp)
        if os.path.exists(p):
            made.append(save(Image.open(p), name, w, q=84))
    return made


PAGE = r"""
<script>function heroIn() {     // the hero's sources, set on home only, so another view's first load doesn't fetch it
  document.querySelectorAll('.hero-photo [data-srcset]').forEach(e => { e.srcset = e.dataset.srcset; delete e.dataset.srcset; });
  document.querySelectorAll('.hero-photo img[data-src]').forEach(e => { e.src = e.dataset.src; delete e.dataset.src; }); }</script>
<script>(function (d, h) {                               // round 47: the view's first picture, fetched first (the hero on home only)
  const L = __LEAD__, m = /^#([a-z]+-[a-z]+)$/.exec(h), add = (href, set, media) => { const l = d.ownerDocument.createElement('link');
    l.rel = 'preload'; l.as = 'image'; l.fetchPriority = 'high'; if (href) l.href = href; if (set) { l.imageSrcset = set; l.imageSizes = '100vw'; }
    if (media) l.media = media; d.ownerDocument.head.appendChild(l); };
  const home = !h || h === '#' || !/^#(speaker|hemisphere|core|mantle|dome|orb|turntable|colour|journal|press|privacy|speakers|lighting|turntable|tropos|atmosphere|turn|spec|lamps|record|closer)\b/.test(h);
  d.dataset.home = home ? '1' : '';
  if (home) { add('img/hero-portrait.webp', null, '(max-width: 700px)'); add(null, 'img/hero-1200.webp 1200w, img/hero.webp 2400w', '(min-width: 701px)'); }
  else if (m && L[m[1]]) { const [wide, tall] = L[m[1]]; if (tall) { add(tall, null, '(max-width: 700px)'); add(wide, null, '(min-width: 701px)'); } else add(wide); }
})(document.documentElement, location.hash)</script>
<script>(function (d) { d.classList.add('opening');      // the opening's choice, made before anything paints: whether it plays, and by day or night
  if (/^#(speaker|dome|orb|turntable|colour)-|^#(speakers|lighting|turntable|tropos|atmosphere|turn|spec|lamps|record|press|journal|privacy)$|^#journal-/.test(location.hash)
      || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  d.classList.add('intro');
  if (matchMedia('(prefers-color-scheme: dark)').matches) { d.classList.add('night'); document.querySelector('meta[name="theme-color"]').content = '#100F12'; }
})(document.documentElement)</script>
<link rel="preload" href="fonts/instrument-sans-400-700-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>__FONTS__</style>
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
.brand .globe { width: 42px; height: 42px; flex: none; background: url(__STILL__) center / 100% 100% no-repeat }
html.globe-live .brand .globe { background-size: 1000% 600%; background-position: 0 0;    /* the turning sprite, after load */
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
.vh { position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; border: 0 }   /* a line page's h1, for screen readers: its first band's h2 is the visible title */
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
.hero-foot .status { flex-basis: 100%; margin: 0; color: var(--muted); font-size: 14px }   /* the plain word, once, near the top */
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
html.globe-live header.top.on-dark .brand .globe { background-image: url(img/globe-spin-dark.webp);
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
   the lamps switched off beside Core's word on its battery (round 35) */
.lamp-pair { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px }
.lamp { display: grid; gap: 12px; align-content: start; min-width: 0 }
.lamp img, .eight img, .lamp-duo img { width: 100%; height: auto; display: block; border-radius: 6px; background: #F1EDE8; max-width: 100% }
.lamp h3 { margin: 4px 0 0; display: flex; align-items: baseline; gap: 12px; font-size: 26px; line-height: 1.1; font-weight: 600; letter-spacing: -0.01em }
.lamp h3 small { font: 500 12px/1.3 var(--mono); letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted) }
.lamp .line { margin: 0 0 6px; color: var(--muted); max-width: 52ch }
.eight { margin: 32px 0 0; display: grid; gap: 12px }
.lamp-duo { display: grid; grid-template-columns: 15fr 8fr; gap: 24px; margin-top: 24px; align-items: start }   /* 3:2 and 4:5 at one height */
.lamp-duo figure { margin: 0; display: grid; gap: 10px; min-width: 0 }
.lamp-duo.solo { grid-template-columns: 8fr 15fr; align-items: center }
.tt-duo .ptile .ph img { border-radius: 6px }
.tt-eight { list-style: none; margin: 40px 0 0; padding: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 24px 16px }
.tt-eight a { display: grid; gap: 10px; color: inherit; text-decoration: none; min-width: 0 }
.tt-eight img { width: 100%; height: auto; display: block; border-radius: 6px; background: #F1EDE8; max-width: 100% }
.tt-eight a > span { display: flex; align-items: center; gap: 8px; font-size: 15px }
.tt-eight a:hover > span, .tt-eight a:focus-visible > span { text-decoration: underline; text-underline-offset: 3px }
.tt-details { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; margin-top: 40px }
.tt-details figure { margin: 0; display: grid; gap: 10px; min-width: 0 }
.tt-details img { width: 100%; height: auto; display: block; border-radius: 6px; background: #F1EDE8; max-width: 100% }
.tt-details figcaption { font-size: 15px; color: var(--muted) }
@media (max-width: 720px) { .lamp-duo.tt-duo { grid-template-columns: minmax(0, 1fr) } .tt-eight { grid-template-columns: repeat(2, minmax(0, 1fr)) }
  .tt-details { grid-template-columns: minmax(0, 1fr) } }
.lamp-note { display: grid; gap: 10px; max-width: 44ch; min-width: 0 }
.lamp-note h3 { margin: 0; font-size: 22px; letter-spacing: -0.01em }
.lamp-note p { margin: 0; color: var(--muted) }
.eight figcaption, .lamp-duo figcaption { font-size: 15px; color: var(--muted) }
@media (max-width: 720px) { .lamp-pair, .lamp-duo { grid-template-columns: minmax(0, 1fr) } }
.pair { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; margin-top: 14px }
.pair figure { margin: 0; display: grid; gap: 10px }
.pair img { width: 100%; height: auto; display: block; border-radius: 4px; max-width: 100% }
.pair figcaption { font-size: 15px; color: var(--muted) } .pair figcaption b { color: var(--ink); font-weight: 600; margin-right: 6px }
@media (max-width: 720px) { .pair { grid-template-columns: 1fr } }
.promise { list-style: none; margin: 0; padding: 0; display: grid; gap: 24px }
.promise li { display: grid; gap: 8px; align-content: start; padding-top: 16px; border-top: 1px solid var(--rule); min-width: 0 }
.promise b { font-weight: 600; font-size: 18px }
.promise span { color: var(--muted); line-height: 1.6 }
.stages { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 32px }      /* where it stands: three steps in a row */
@media (max-width: 860px) { .stages { grid-template-columns: minmax(0, 1fr); gap: 24px } }
.contact { display: grid; gap: 18px }
.contact .addr { display: flex; flex-wrap: wrap; align-items: center; gap: 12px }
.contact code { font: 500 clamp(20px, 3vw, 30px)/1.2 var(--mono); user-select: all; word-break: break-all }
.contact small { color: var(--muted); font-size: 14px }
.contact small:empty { display: none }
footer { padding-block: 40px 56px; border-top: 1px solid var(--rule) }
footer .wrap { display: flex; flex-wrap: wrap; gap: 18px 32px; align-items: center; justify-content: space-between }
footer p { margin: 0; font: 500 12px/1.5 var(--mono); letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted) }
.foot-nav { display: flex; flex-wrap: wrap; gap: 8px 22px }
.foot-nav a { font-size: 15px; color: var(--ink); text-underline-offset: 4px }

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
.stage .spinner { cursor: grab; touch-action: pan-y } .stage .spinner.dragging { cursor: grabbing }
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
/*3D*/.v3d-box { position: absolute; inset: 0; z-index: 3; border-radius: 6px; overflow: hidden; background: #F3F1EC; touch-action: none; cursor: grab }
.v3d-box:active { cursor: grabbing } .v3d-box:focus-visible { outline: 2px solid var(--ink); outline-offset: 3px }
.v3d-box canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block }
.frame.three .nav, .frame.three .count { visibility: hidden }
.v3d-btn { position: absolute; z-index: 4; top: 12px; right: 12px; min-height: 40px; padding: 0 14px; border: 0; border-radius: 999px; cursor: pointer;
  font: 500 12px/1 var(--mono); letter-spacing: 0.1em; text-transform: uppercase; color: var(--on-photo); background: var(--veil);
  box-shadow: 0 1px 8px rgba(0, 0, 0, 0.14) }
.v3d-btn:hover { box-shadow: inset 0 0 0 1.5px var(--on-photo), 0 1px 8px rgba(0, 0, 0, 0.14) } .v3d-btn:focus-visible { outline: 2px solid var(--ink); outline-offset: 2px }
.v3d-hint { position: absolute; z-index: 1; left: 12px; bottom: 12px; margin: 0; pointer-events: none; font: 500 12px/1 var(--mono); letter-spacing: 0.1em;
  text-transform: uppercase; color: var(--on-photo); background: var(--veil); border-radius: 999px; padding: 7px 10px }
.v3d-load { position: absolute; inset: 0; z-index: 1; display: grid; place-items: center; margin: 0; pointer-events: none;
  font: 500 13px/1.4 var(--mono); letter-spacing: 0.08em; color: var(--muted) } .v3d-load:empty { display: none }/*/3D*/
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
.price span { font-weight: 400; color: var(--muted); font-size: 16px; white-space: nowrap }   /* the unit wraps whole */
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
  .spec dd, .facts dd { padding: 2px 0 10px } .swatches { gap: 6px } .swatches a { width: 36px; height: 36px } }
/* phones: the pages behind one Menu button (five names and the mark wrapped the header onto two lines at 390) */
.menu { display: none; font: 500 14px/1 var(--sans); color: var(--ink); background: transparent; border: 1px solid currentColor;
  border-radius: 999px; padding: 9px 14px; cursor: pointer }
@media (max-width: 460px) {
  .menu { display: inline-flex; align-items: center }
  nav ul { display: none; position: absolute; left: 0; right: 0; top: 100%; flex-direction: column; gap: 0; background: var(--page);
    padding: 4px max(16px, env(safe-area-inset-right, 0px)) 12px max(16px, env(safe-area-inset-left, 0px)); border-bottom: 1px solid rgb(0 0 0 / .08) }
  nav.open ul { display: flex }
  nav ul a { display: block; padding: 12px 0; font-size: 17px }
  header.top.on-dark nav ul { background: rgb(11 12 16 / .97); border-bottom-color: rgb(255 255 255 / .06) }
  header.top.on-dark .menu { color: #ECE8E1 }
}
/* the shop (round 34): the lines and the colours on the home page, a line's products, a colour's page, and the
   company a colour keeps (its complement, its neighbours, itself), all as cards in the 4:5 frame */
.lines { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px }
.tile { position: relative; display: grid; grid-template-rows: auto 1fr; border-radius: 6px; overflow: hidden; background: #F1EDE8;
  color: var(--ink); text-decoration: none; min-width: 0 }
.tile img { width: 100%; height: auto; aspect-ratio: 4 / 5; object-fit: cover; display: block; max-width: 100% }
.tile .t-body { padding: 16px 18px 20px; display: grid; gap: 4px; align-content: start; min-width: 0 }
.tile .eyebrow { margin: 0 }
.tile .t-name { font-size: 26px; line-height: 1.1; font-weight: 600; letter-spacing: -0.01em }
.tile .t-line { color: var(--muted); font-size: 15px }
.tile .t-go { margin-top: 10px; font-weight: 600; font-size: 15px; text-decoration: underline; text-underline-offset: 4px }
.tile:hover .t-go { text-decoration-thickness: 2px }
.tile .soon { position: absolute; top: 12px; left: 12px; z-index: 1; font: 500 12px/1 var(--mono); letter-spacing: 0.1em;
  text-transform: uppercase; background: var(--veil); backdrop-filter: blur(6px); padding: 7px 10px; border-radius: 999px }
.shopcol { display: grid; grid-template-columns: repeat(8, minmax(0, 1fr)); gap: 14px; margin: 0; padding: 0; list-style: none }
.shopcol a { display: grid; justify-items: center; align-content: start; gap: 6px; color: var(--ink); text-decoration: none;
  text-align: center; min-width: 0 }
.shopcol .coin-dot { width: min(72px, 100%); height: auto; aspect-ratio: 1 }
.shopcol b { font-weight: 600; font-size: 16px; margin-top: 4px }
.shopcol small { color: var(--muted); font-size: 13px; line-height: 1.35 }
.shopcol a:hover b { text-decoration: underline; text-underline-offset: 4px }
.ptiles { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px }
.ptiles.one { grid-template-columns: minmax(0, 1fr); max-width: 760px }
.ptile { display: grid; gap: 12px; align-content: start; min-width: 0 }
.ptile .ph img { width: 100%; height: auto; display: block; border-radius: 6px; background: #F1EDE8; max-width: 100% }
.ptile h3 { margin: 4px 0 0; display: flex; align-items: baseline; gap: 12px; font-size: 26px; line-height: 1.1; font-weight: 600;
  letter-spacing: -0.01em }
.ptile h3 small { font: 500 12px/1.3 var(--mono); letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted) }
.ptile .line { margin: 0; color: var(--muted); max-width: 52ch }
.ptile .more { justify-self: start; color: var(--ink); font-weight: 600; font-size: 15px; text-underline-offset: 4px }
.dots-row { display: flex; flex-wrap: wrap; gap: 6px; margin: 0; padding: 0; list-style: none }
.dots-row a { display: block; width: 28px; height: 28px; border-radius: 50% }
.dots-row .coin-dot { width: 100%; height: 100%; display: block }
.concepts { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr)); gap: 24px }
.concept { margin: 0; display: grid; gap: 10px; align-content: start; min-width: 0 }
.concept img { width: 100%; height: auto; border-radius: 6px; display: block }
.concept figcaption { font-size: 14px; color: var(--muted) }
.soon-wrap .acts { margin-top: 24px }
.colour-head { display: flex; align-items: center; gap: 22px; padding-block: 18px 16px }
.colour-head .coin-big { width: 96px; height: 96px; flex: none }
.colour-head .coin-big .coin-dot { width: 100%; height: 100%; display: block }
.colour-head h1 { font-size: clamp(40px, 5vw, 64px) }
.colour-head .num { margin: 0 0 6px; font: 500 13px/1.3 var(--mono); letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted) }
.colour-head .line { margin: 8px 0 0; font-size: 18px }
.company { padding-block: 32px 8px }
#p-company .company:first-child { padding-top: 56px }
.company .goes-head span { max-width: 60ch }
.pgrid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px }
.pcard { position: relative; display: grid; gap: 8px; align-content: start; color: var(--ink); text-decoration: none; min-width: 0 }
.pcard img { width: 100%; height: auto; aspect-ratio: 4 / 5; object-fit: cover; border-radius: 6px; display: block; background: #F1EDE8;
  max-width: 100% }
.pcard b { font-weight: 600; font-size: 17px; line-height: 1.2 }
.pcard .pc-col { display: flex; align-items: center; gap: 6px; font-size: 14px; color: var(--muted) }
.pcard .pc-col .coin-dot { width: 16px; height: 16px }
.pcard .tag { position: absolute; left: 8px; top: 8px; font: 500 11px/1 var(--mono); letter-spacing: 0.1em; text-transform: uppercase;
  background: var(--veil); padding: 6px 8px; border-radius: 999px }
.pcard:hover b { text-decoration: underline; text-underline-offset: 4px }
.pick-ic { display: inline-block; width: 1.3em; height: 1.3em; vertical-align: -0.3em; margin-left: 6px }
.pick-ic:empty { display: none }
.more-line { padding-block: 32px 72px; margin: 0; color: var(--muted) }
.more-line:empty { padding-block: 0 48px }

/* round 47: the press page, the journal, the waitlist and its notice; in the shop's paper and ink, a column for reading */
.ed-head { padding-block: 18px 8px; max-width: 760px }
.ed-head h1 { font-size: clamp(38px, 5vw, 64px) }
.ed-band { padding-block: 40px; border-top: 1px solid var(--rule); margin-top: 32px; display: grid; gap: 18px }
.ed-band h2 { font-size: clamp(24px, 2.6vw, 32px) }
.ed-note { margin: 0; max-width: 64ch; color: var(--muted) }
.boiler { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px }
.boiler p:not(.eyebrow) { margin: 0 0 14px; max-width: 62ch }
.copied { margin: 0; min-height: 1.5em; color: var(--muted); font-size: 14px }
.slot p { margin: 0 }
.tints { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px 24px }
.tints li { display: grid; grid-template-columns: auto 1fr; gap: 0 10px; align-items: center }
.tints span:last-child { grid-column: 2; color: var(--muted); font-size: 14px }
.sheets { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 32px 48px }
.sheet h3 { margin: 0 0 10px; font-size: 22px; display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap }
.sheet h3 small, .jcard .eyebrow { font: 500 12px/1.3 var(--mono); letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted) }
.sheet dl { margin: 0; display: grid; grid-template-columns: 120px minmax(0, 1fr); gap: 6px 16px; font-size: 15px; border-top: 1px solid var(--rule); padding-top: 10px }
.sheet dt { font: 500 12px/1.6 var(--mono); letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted) }
.sheet dd { margin: 0 }
.logo-dl { margin: 0; display: flex; flex-wrap: wrap; align-items: center; gap: 10px 16px } .logo-dl span { color: var(--muted); font-size: 15px }
.dl-grid { list-style: none; margin: 8px 0 0; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px 18px }
.dl-grid figure { margin: 0 } .dl-grid img { width: 100%; height: auto; aspect-ratio: 3 / 2; object-fit: cover; border-radius: 6px; display: block; background: #F1EDE8 }
.dl-grid figcaption { margin-top: 8px; font-size: 14px; line-height: 1.45 } .dl-grid a { color: var(--ink); text-underline-offset: 3px; white-space: nowrap }
.jlist { list-style: none; margin: 32px 0 80px; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 32px 20px }
.jband { margin: 0 }
.share-note { margin: 8px 0 0; min-height: 1.4em; font-size: 14px; color: var(--muted); word-break: break-all }
/* the press page printed (viewer/presskit.mjs makes site/press/earf-press-kit.pdf from it): the words and the
   particulars, the pictures as a contact sheet, nothing to click */
@media print {
  @page { size: A4; margin: 16mm 14mm }
  body { background: #FFF; font-size: 10.5pt }
  header.top, footer, .crumbs, .copy-text, .copied, .logo-dl, .flyer, .splash, body::before { display: none !important }
  #press .ed-head h1 { font-size: 30pt } #press .lede { font-size: 12pt }
  #press .ed-band { break-inside: auto; padding-block: 14pt; margin-top: 10pt }
  #press .sheets { grid-template-columns: 1fr 1fr; gap: 14pt 24pt } #press h2, #press .sheet h3 { break-after: avoid }
  #press .sheet dt, #press .sheet dd { break-inside: avoid } #press .coin-dot { print-color-adjust: exact; -webkit-print-color-adjust: exact }
  #press .dl-grid { grid-template-columns: repeat(4, 1fr); gap: 8pt } #press .dl-grid li { break-inside: avoid }
  #press .dl-grid figcaption { font-size: 7.5pt } #press .dl-grid a { text-decoration: none; color: #555 }
  #press .boiler { grid-template-columns: 1fr; gap: 10pt } #press [aria-labelledby="pr-pics"] { break-before: page }
}
.jcard { display: grid; gap: 8px; color: var(--ink); text-decoration: none }
.jcard img { width: 100%; height: auto; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 6px; display: block; margin-bottom: 6px; background: #F1EDE8 }
.jcard .eyebrow { margin: 0 } .jcard b { font-size: 22px; line-height: 1.15; font-weight: 600; letter-spacing: -0.01em } .jcard > span:last-child { color: var(--muted) }
.jcard:hover b { text-decoration: underline; text-underline-offset: 4px }
.post { max-width: 720px; margin: 0 auto; padding-bottom: 72px }
.post header { padding-block: 24px 8px } .post h1 { font-size: clamp(36px, 5vw, 58px) }
.post .stand { margin: 14px 0 28px; font-size: 21px; line-height: 1.4; color: var(--muted) }
.post-body p { margin: 0 0 1.1em; font-size: 18px; line-height: 1.65 }
.post-body a, .post-next a, .policy a { color: var(--ink); text-underline-offset: 3px }
.post-body figure { margin: 32px 0 }
.post-body img { width: 100%; height: auto; display: block; border-radius: 4px }
.post-body figcaption { margin-top: 8px; font-size: 14px; color: var(--muted) }
.post-next { margin: 40px 0 0; padding-top: 18px; border-top: 1px solid var(--rule) }
.waitlist { margin-top: 28px; padding-top: 28px; border-top: 1px solid var(--rule); display: grid; gap: 12px; max-width: 640px }
.waitlist h3 { margin: 0; font-size: 24px } .waitlist p { margin: 0 }
.wl-row { display: flex; flex-wrap: wrap; gap: 10px }
.wl-row input { flex: 1 1 260px; min-width: 0; font: 400 17px/1.2 var(--sans); padding: 12px 16px; border: 1px solid var(--ink); border-radius: 999px; background: #FFF; color: var(--ink) }
.waitlist fieldset { border: 0; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: 6px 18px }
.waitlist legend { padding: 0; margin-bottom: 6px; font-size: 15px; color: var(--muted) }
.waitlist label { font-size: 15px } .waitlist .hp { position: absolute; left: -9999px; width: 1px; height: 1px }
.wl-note, .wl-status { font-size: 14px; color: var(--muted) } .wl-note a { color: var(--ink) }
.policy { max-width: 760px; margin: 24px 0 80px; display: grid; gap: 4px 0 }
.policy dt { margin-top: 18px; font-weight: 600 } .policy dd { margin: 0; color: var(--ink); line-height: 1.6 }
@media (max-width: 900px) { .sheets, .boiler { grid-template-columns: minmax(0, 1fr) } .tints { grid-template-columns: repeat(2, minmax(0, 1fr)) }
  .dl-grid, .jlist { grid-template-columns: repeat(2, minmax(0, 1fr)) } }
@media (max-width: 560px) { .dl-grid, .jlist { grid-template-columns: minmax(0, 1fr) } .sheet dl { grid-template-columns: 96px minmax(0, 1fr) } }
.more-line a { color: var(--ink); text-underline-offset: 4px }
@media (max-width: 960px) { .shopcol { grid-template-columns: repeat(4, minmax(0, 1fr)) } .pgrid { grid-template-columns: repeat(2, minmax(0, 1fr)) } }
@media (max-width: 720px) {
  .lines { grid-template-columns: minmax(0, 1fr); gap: 12px }
  .tile { grid-template-columns: minmax(0, 2fr) minmax(0, 3fr); grid-template-rows: none }
  .tile img { height: 100% }
  .ptiles { grid-template-columns: minmax(0, 1fr) }
  .colour-head .coin-big { width: 72px; height: 72px }
}
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
  <nav aria-label="Pages" id="nav"><button type="button" class="menu" aria-expanded="false" aria-controls="nav-list">Menu</button><ul id="nav-list">
    <li><a href="#speakers" data-nav="speakers">Speakers</a></li><li><a href="#lighting" data-nav="lighting">Lighting</a></li>
    <li><a href="#turntable" data-nav="turntable">Turntable</a></li><li class="wide"><a href="#colours" data-nav="colours">Colours</a></li>
    <li><a href="#journal" data-nav="journal">Journal</a></li>
    <li><a href="#contact">Enquire</a></li>
  </ul></nav>
</div></header>

<main id="home">
  <section class="hero" id="top">
    <div class="hero-pic">
      <div class="hero-title"><div class="wrap"><p class="eyebrow">EARF &middot; Tropos</p><h1>Something in the air.</h1></div></div>
      <div class="hero-photo__HERO_CLASS__">
        <picture>__HERO_TALL__<img data-src="img/hero.jpg" fetchpriority="high" data-srcset="img/hero-1200.webp 1200w, img/hero.webp 2400w" sizes="100vw" width="2400" height="1200"
          alt="The eight Tropos speakers on a curve, their covers off: red through violet, then the clear Fog and the smoked Smoke, each throwing its colour on the floor"></picture>
        __HOTSPOTS__
      </div>
      <script>if (document.documentElement.dataset.home) heroIn()</script>
    </div>
    <div class="wrap hero-foot">
      <p class="lede">Tropos is a horn loudspeaker cast in tinted acrylic, in eight colours from Ember to Smoke.</p>
      <div class="acts"><a class="btn solid" href="#speakers">See the speakers</a><a class="btn" href="#colours">See the colours</a></div>
      <p class="status">In development and not yet for sale; until the first are built, every picture here is a render.</p>
    </div>
    <div class="wrap"><ul class="cast" aria-label="The eight, in spectrum order">__NAMES__</ul></div>
  </section>

__LINES__
__COLOURS__
__REEL__
__HABITATS__
  <section class="band room" id="room">
    <div class="wrap"><div class="head"><div><p class="eyebrow">At home</p><h2>A pair in Poison.</h2></div></div></div>
    <figure><picture>__ROOM_TALL__<img src="img/room.jpg" srcset="img/room-1440.jpg 1440w, img/room.jpg 2880w" sizes="100vw" width="2880" height="1620" alt="Two green speakers either side of a walnut sideboard with a record player, low sun from a tall window on the left" loading="lazy"></picture>
      <figcaption class="wrap"><span>Covers on, by a tall window.</span><span>Each stands 1293&nbsp;mm tall, 560&nbsp;mm wide at the cabinet.</span></figcaption></figure>
  </section>

  <section class="band" id="progress"><div class="wrap">
    <div class="head"><div><p class="eyebrow">Progress</p><h2>Drawn to be made.</h2></div></div>
    <ol class="promise stages">
      <li><b>Drawn.</b><span>Tropos is drawn for making, part by part: more than eighty of them, each with its fabrication
        drawing. The horn&rsquo;s profile and the cabinet&rsquo;s bass were worked out by simulation before any acrylic was cut.</span></li>
      <li><b>Next, the first pair.</b><span>Built as production will build it: the horn formed from the cabinet&rsquo;s own
        tinted acrylic, the back screwed to the braces. A prototype is there to test the making.</span></li>
      <li><b>Then, measured.</b><span>In a room, by ear and by microphone. The design figures on these pages give way to
        measured ones. The lamps and Mantle come next, the same way.</span></li>
    </ol>
  </div></section>

__JOURNAL_BAND__
  <section class="band" id="contact"><div class="wrap contact">
    <p class="eyebrow">Enquiries</p>
    <h2>Write to us.</h2>
    <p>Everything is made to order, so we quote rather than list. From launch, write here for prices and lead times.
      Trade and stockists: the same address.</p>
    <div class="addr"><code id="addr">hello@earf.world</code><button type="button" class="btn" id="copy">Copy address</button></div>
    <small id="copy-note"></small>
__WAITLIST__
  </div></section>
</main>

<main id="line" hidden>
  <div class="lineview" data-line="speakers">
    <div class="wrap"><p class="crumbs"><a href="#top">Home</a> / Speakers</p><h1 class="vh">Speakers</h1></div>
  <section class="band" id="tropos"><div class="wrap">
    <div class="head">
      <div><p class="eyebrow">Tropos</p><h2>Eight things in the air.</h2>
        <p>Each cabinet is cast acrylic, 20 mm thick and tinted all the way through. The lining shows through the walls,
          so we dressed it in white voile.</p></div>
      <div class="seg" role="group" aria-label="The speakers' covers">
        <button type="button" id="cover-off" aria-pressed="true">Cover off</button>
        <button type="button" id="cover-on" aria-pressed="false">Cover on</button>
      </div>
    </div>
    <div class="cards show-off" id="cards">__CARDS__</div>
  </div></section>
__CLOSER__
  <section class="band" id="turn"><div class="wrap">
    <div class="head">
      <div><p class="eyebrow">The horn</p><h2>The oldest amplifier is a shape.</h2>
        <p>Long before there were amplifiers, a horn was how a small sound filled a large room: the gramophone&rsquo;s, or a
          cupped hand&rsquo;s. Ours is formed from the same tinted acrylic as its cabinet, its driver in a pod whose cap twists
          off by hand. Above 1&nbsp;kHz the horn carries the music; below, a 15-inch woofer takes it, each on its own channel
          of the amplifier inside. A horn wastes little, so a little power goes a long way.</p></div>
    </div>
    <ul class="horns" id="horns">__TURN__</ul>
  </div></section>
  <section class="band spec" id="spec"><div class="wrap">
    <div class="head"><div><p class="eyebrow">Details</p><h2>The particulars</h2></div></div>
    <div class="spec-grid">
      <dl>__SPEC__</dl>
      <figure class="dwg">__DWG__
        <figcaption>From the fabrication drawings</figcaption></figure>
    </div>
  </div></section>
  </div>
  <div class="lineview" data-line="lighting">
    <div class="wrap"><p class="crumbs"><a href="#top">Home</a> / Lighting</p><h1 class="vh">Lighting</h1></div>
__LIGHTING__
  </div>
  <div class="lineview" data-line="turntable">
    <div class="wrap"><p class="crumbs"><a href="#top">Home</a> / Turntable</p><h1 class="vh">Turntable</h1></div>
__TURNTABLE__
  </div>
</main>

<main id="colour" hidden>
  <div class="wrap">
    <p class="crumbs"><a href="#top">Home</a> / <a href="#colours">Colours</a> / <span id="c-crumb"></span></p>
    <div class="colour-head"><span class="coin-big" id="c-coin"></span>
      <div><p class="num" id="c-num"></p><h1 id="c-name"></h1><p class="line" id="c-line"></p></div></div>
    <ul class="swatches" id="c-swatches" aria-label="Colour"></ul>
    <section class="company" aria-labelledby="c-in"><div class="goes-head"><h2 id="c-in"></h2><span id="c-in-note"></span></div>
      <div class="pgrid" id="c-products"></div></section>
    <div id="c-company"></div>
  </div>
</main>

<main id="pdp" hidden>
  <div class="wrap">
    <p class="crumbs"><a href="#top">Home</a> / <a id="p-line-link" href="#speakers">Speakers</a> / <span id="p-crumb"></span></p>
    <div class="pdp">
      <section class="gallery" aria-label="Pictures">
        <div class="frame">
          <div class="stage" id="stage" role="tabpanel" aria-labelledby="thumb-0" tabindex="0"></div>
          <button type="button" class="nav prev" id="g-prev" aria-label="Previous picture"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M11.5 3.5 6 9l5.5 5.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
          <button type="button" class="nav next" id="g-next" aria-label="Next picture"><svg viewBox="0 0 18 18" aria-hidden="true"><path d="M6.5 3.5 12 9l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
          <span class="count" id="g-count" aria-hidden="true"></span>
          <!--3D-->
          <div class="v3d-box" id="v3d-box" hidden tabindex="0" role="application" aria-roledescription="3D view" aria-label="3D view">
            <p class="v3d-hint" aria-hidden="true">Drag to turn</p><p class="v3d-load" id="v3d-load" aria-live="polite"></p></div>
          <button type="button" class="v3d-btn" id="v3d" hidden aria-pressed="false" aria-controls="v3d-box">View in 3D</button>
          <!--/3D-->
        </div>
        <div class="thumbs" id="thumbs" role="tablist" aria-label="Pictures"></div>
        <p class="cap" id="cap" aria-live="polite"></p>
      </section>
      <aside class="buy" aria-label="This product">
        <p class="num"><span id="p-num"></span></p>
        <h1 class="named"><span id="p-name"></span><span class="pic" id="p-icon"></span></h1>
        <p class="line" id="p-line"></p>
        <p class="price">Priced at launch <span id="p-unit">&middot; each pair made to order</span></p>
        <ul class="swatches" id="swatches" aria-label="Colour"></ul>
        <p class="pick">Colour: <b id="p-pick"></b><span class="pick-ic" id="p-pick-ic"></span></p>
        <div class="acts"><a class="btn solid" id="p-enquire" href="#contact">Enquire about a pair</a><button type="button" class="btn" id="p-share">Copy link</button></div>
        <p class="share-note" id="p-share-note" aria-live="polite"></p>
        <dl class="facts" id="facts"></dl>
      </aside>
    </div>
    <div id="p-company"></div>
    <p class="more-line" id="p-more"></p>
  </div>
</main>
__PRESS__
__JOURNAL__
__PRIVACY__

<footer><div class="wrap">
  <a class="brand" href="#top" aria-label="EARF, home">__WORD__</a>
  <nav class="foot-nav" aria-label="More"><a href="#progress">Progress</a><a href="#journal">Journal</a><a href="#press">Press</a><a href="#contact">Enquiries</a>__FOOT_PRIVACY__</nav>
  <p>EARF &middot; San Francisco &middot; In development, not yet for sale &middot; The pictures are renders &middot; &copy; 2026</p>
</div></footer>

<script>
const D = __DATA__, BY = Object.fromEntries(D.clouds.map(c => [c.k, c]));
const SLUG = Object.fromEntries(D.clouds.map(c => [c.name.toLowerCase(), c.k])), keyOf = w => SLUG[w] || (BY[w] ? w : null);
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches, TAU = Math.PI * 2;
// round 47 (mobile speed): pictures well below the fold load as they come within a screen of view, not on the browser's
// own (generous) lazy distance; anything that can wait for the page waits for its load event
const afterLoad = f => { if (document.readyState === 'complete') f(); else addEventListener('load', f, { once: true }); };
const lateIO = 'IntersectionObserver' in window && new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { lateIO.unobserve(e.target); show_(e.target); } }), { rootMargin: '600px 0px' });
const show_ = img => { if (img.dataset.src) { img.src = img.dataset.src; delete img.dataset.src; } };
const later = img => { if (lateIO) lateIO.observe(img); else show_(img); };
document.querySelectorAll('img[data-src]:not(.hero-photo img)').forEach(later);
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
      const c = D.clouds[i]; nameEl.textContent = c.name; lineEl.textContent = c.line; numEl.textContent = `Tropos ${c.num}`;
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
// round 47: the sprite (165 KB) comes after the page has loaded; until then the globe is its still first frame
const globeLive = () => document.documentElement.classList.add('globe-live');
if (document.readyState === 'complete') setTimeout(globeLive, 300); else addEventListener('load', () => setTimeout(globeLive, 300), { once: true });
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
  const done = () => { note.textContent = 'Copied.'; };
  const pickText = () => { const r = document.createRange(); r.selectNodeContents(document.getElementById('addr'));
    const s = getSelection(); s.removeAllRanges(); s.addRange(r); note.textContent = 'Selected.'; };
  try { navigator.clipboard.writeText(text).then(done, pickText); } catch (e) { pickText(); }
});

// the press page's paragraphs, copied as text
document.querySelectorAll('.copy-text').forEach(b => b.addEventListener('click', () => {
  const t = document.getElementById(b.dataset.copy).textContent, note = b.closest('section').querySelector('.copied');
  try { navigator.clipboard.writeText(t).then(() => { note.textContent = 'Copied.'; }, () => { note.textContent = 'Select the text to copy it.'; }); }
  catch (e) { note.textContent = 'Select the text to copy it.'; }
}));
// the waitlist (when switched on): sent in the background where the provider allows it, else posted as a form
const wl = document.getElementById('waitlist');
if (wl) wl.addEventListener('submit', e => {
  const st = document.getElementById('wl-status'), em = wl.querySelector('input[type=email]');
  if (!em.value || !em.checkValidity()) { e.preventDefault(); st.textContent = 'That address doesn’t look right.'; em.focus(); return; }
  if (wl.website.value || !wl.action) { e.preventDefault(); st.textContent = 'Thank you.'; return; }
  e.preventDefault(); st.textContent = 'Sending…';
  fetch(wl.action, { method: 'POST', body: new FormData(wl), mode: 'no-cors' })
    .then(() => { wl.reset(); st.textContent = 'You’re on the list. We’ll write when there’s something to say.'; },
          () => { st.textContent = 'That didn’t go through. Try again in a moment.'; });
});

// a product's page (round 34, the shop): its pictures as a shop shows them, one at a time (the arrows, a swipe, the arrow
// keys, or the strip of thumbnails), in the colour picked; Tropos's open on the photograph in its element
const SPEAKER_VIEWS = [
  ['habitat', 'In its element', c => `${c.name} ${c.place}.`, c => `In its element, ${c.place}.`],
  ['on', 'Cover on', c => `With its cover on, in ${c.cover.toLowerCase()}.`],
  ['off', 'Cover off', c => `Cover off: the 15-inch woofer, the two ports, and the lining showing through the walls.`],
  ['spin', 'Turn it', c => `${c.name} in the studio; drag across it to turn it.`, c => `In the studio. Drag across it to turn it; every frame is a render.`],
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
const LAMP_VIEWS = {
  dome: [['hero', 'Lit', (c, s) => s ? `Hemisphere lit, shown in ${BY[s].name}; its ${c.name} shade is cast in the same way.` : `Hemisphere lit, its ${c.name} shade glowing beneath a black hub.`,
          (c, s) => s ? `Shown lit in ${BY[s].name}; the ${c.name} shade is cast the same way.` : `Lit, in ${c.name}.`],
         ['row', 'All eight', () => 'Eight Hemispheres hung in a row, lit, one in each colour.'],
         ['unlit', 'Off', () => 'A Core and a Hemisphere in Smoke, switched off: dark, polished acrylic, pale at the centre.']],
  orb: [['hero', 'Lit', (c, s) => s ? `Core lit, shown in ${BY[s].name}; its ${c.name} ball is cast in the same way.` : `Core lit in ${c.name}, sitting low in its black acrylic base.`,
         (c, s) => s ? `Shown lit in ${BY[s].name}; the ${c.name} shade is cast the same way.` : `Lit, in ${c.name}.`],
        ['row', 'All eight', () => 'Eight Core lamps in a row, lit, in spectrum order.'],
        ['unlit', 'Off', () => 'A Core and a Hemisphere in Smoke, switched off: dark, polished acrylic, pale at the centre.']],
};
const TT_VIEWS = [['studio', 'In the studio', c => `${D.tt.name} in ${c.name}, its lid raised.`],
                  ['closed', 'Lid down', c => `${D.tt.name} in ${c.name}, its lid down.`],
                  ['dusk', 'At dusk', c => `${D.tt.name} in ${c.name} at dusk, its base glowing.`],
                  ['open', 'Cover open', () => 'Its cover open.'], ['detail', 'Arm and platter', () => 'The arm and the platter.'],
                  ['pod', 'The motor apart', () => 'The motor in its own pod, standing clear of the plinth.']];
// the campaign slots (CAMPAIGN in web.py): each one's view placed in its product's list, after the view it names
for (const c of D.campaign || []) {
  const list = c.product === 'speaker' ? SPEAKER_VIEWS : LAMP_VIEWS[c.product]; if (!list) continue;
  const row = [c.view, c.label, x => c.alt.replace('{name}', x.name), x => c.caption.replace('{name}', x.name)];
  const at = c.after ? list.findIndex(v => v[0] === c.after) + 1 : 0; list.splice(at > 0 || !c.after ? at : list.length, 0, row);
}
const PRODUCTS = [
  { id: 'speaker', line: 'speakers', lineName: 'Speakers', route: 'speaker', kind: 'Horn loudspeaker', name: c => c.name,
    num: c => `Tropos ${c.num}`, copy: c => c.line, views: k => BY[k].views, VIEWS: SPEAKER_VIEWS,
    card: k => { const o = BY[k].views.off; return o.tall || o.card || o; }, unit: 'each pair made to order', ask: 'Enquire about a pair',
    facts: c => [['Acrylic', c.tint], ['Cabinet', 'Cast acrylic, 20 mm, tinted through; lined in white'], ['Horn', 'Formed from the same tinted acrylic as the cabinet'],
      ['Cover', `Cloth disc, ${c.cover.toLowerCase()}`], ['Drivers', '15-inch woofer; 2-inch compression driver on the horn'],
      ['Amplifier', 'Hypex FusionAmp FA122, built in: 2 &times; 125 W, crossed at 1 kHz'], ['Bass', 'To about 51 Hz (&minus;3 dB) before the room; a design figure, measured with the first pair'],
      ['Inputs', 'XLR, RCA, AES, S/PDIF coaxial and optical'], ['Size', '1293 high, 625 wide, 423 deep (mm)'], ['Weight', 'About 72 kg'], ['Care', D.care]],
    title: c => `Tropos in ${c.name}` },
  ...Object.entries(D.lamps).map(([id, L]) => ({ id, line: 'lighting', lineName: 'Lighting', route: L.route || id, kind: L.kind, name: () => L.name,
    num: () => `Lighting &middot; ${L.kind}`, copy: () => L.line, views: k => (L.colours[k] || {}).views, VIEWS: LAMP_VIEWS[id],
    card: k => L.colours[k].card, unit: 'made to order', ask: 'Enquire', facts: c => [...L.facts, ['Colour', c.name]],
    title: c => `${L.name} in ${c.name}` })),
  ...(D.tt ? [{ id: 'turntable', line: 'turntable', lineName: 'Turntable', route: D.tt.route || 'turntable', kind: D.tt.kind, name: () => D.tt.name,
    num: () => 'Turntable', copy: () => D.tt.line, views: k => (D.tt.colours[k] || {}).views, VIEWS: TT_VIEWS,
    card: k => D.tt.colours[k].card, unit: 'made to order', ask: 'Enquire', facts: c => [...D.tt.facts, ['Colour', c.name]],
    title: c => `${D.tt.name} in ${c.name}` }] : []),
];
const PBY = Object.fromEntries(PRODUCTS.map(p => [p.route, p]));
const icons = c => `<img class="ic only-light" src="img/icon-${c.icon}-light.webp" alt="" width="256" height="256">`;
const stage = document.getElementById('stage'), thumbs = document.getElementById('thumbs'), phone = matchMedia('(max-width: 700px)');
let P = PRODUCTS[0], cur = null, view = 'habitat', turnFrame = 0, autoTurn = null;
const vw = () => P.views(cur) || {};
function src(c, v) { return vw()[v]; }
const say = (c, v) => P.VIEWS.find(x => x[0] === v)[2](c, (vw()[v] || {}).shown);
const tell = (c, v) => { const x = P.VIEWS.find(x => x[0] === v); return (x[3] || x[2])(c, (vw()[v] || {}).shown); };   // the caption
const shown = c => P.VIEWS.map(x => x[0]).filter(v => vw()[v] && !(v === 'studio' && vw()['studio-light']));   // the bright studio won
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
  } else if (v === 'spin') {         // round 47: path-traced frames, dragged round; one turn on arrival, never under reduced motion
    const fr = i => `${s.base}${String(i).padStart(2, '0')}.webp`, home = s.home ?? 0;
    pic = el('img', { class: 'fit spinner' + (s.edge === 'cut' ? ' cut' : ''), src: s.src, width: s.w, height: s.h, alt: say(c, v), draggable: 'false', style: `--ar:${ar}` });
    const frames = Array.from({ length: s.n }, (_, i) => { const im = new Image(); im.decoding = 'async'; im.src = fr(i); return im; });
    let at = home; const show = i => { at = Math.max(0, Math.min(s.n - 1, Math.round(i))); pic.src = frames[at].src; };
    // the whole arc across about half the stage; a drag to the right turns its face to the right
    draggable(pic, (d, start, base) => { if (start) { cancelAnimationFrame(autoTurn); return at; }
      show(base - d * 9 * (s.n - 1) / Math.max(240, stage.clientWidth * 0.5)); });
    if (!reduce) Promise.all(frames.map(f => f.decode().catch(() => {}))).then(() => { if (!pic.isConnected) return;
      const t0 = performance.now(); (function f(now) { const p = Math.min(1, (now - t0) / 3200);   // a sway: left, right, home
        const k = Math.sin(2 * Math.PI * p); show(home + (k > 0 ? (s.n - 1 - home) : home) * k);
        if (p < 1 && pic.isConnected) autoTurn = requestAnimationFrame(f); })(t0); });
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
  if (s.shown) stage.appendChild(el('span', { class: 'tag' }, `Shown in ${BY[s.shown].name}`));
  stage.style.background = ground(v);
  document.getElementById('cap').textContent = tell(c, v);
  document.getElementById('g-count').textContent = `${i + 1} / ${list.length} · Render`;   // labelled on the picture itself
  thumbs.querySelectorAll('button').forEach(b => { const sel = b.dataset.v === v; b.setAttribute('aria-selected', String(sel)); b.tabIndex = sel ? 0 : -1;
    if (!sel) return;
    stage.setAttribute('aria-labelledby', b.id);
    thumbs.scrollTo({ left: b.offsetLeft - (thumbs.clientWidth - b.offsetWidth) / 2, behavior: reduce ? 'auto' : 'smooth' });
    if (focus) b.focus({ preventScroll: true }); });
  afterLoad(() => { for (const n of [list[(i + 1) % list.length], list[(i + list.length - 1) % list.length]]) {   // the neighbours load
    const t = src(c, n); if (t && n !== 'turn' && n !== 'spin') new Image().src = (phone.matches && t.tall ? t.tall : t).src; } });   // once the page has
}
function go(d, focus) { const list = shown(BY[cur]); showView(list[(list.indexOf(view) + d + list.length) % list.length], focus); }
const MORE = {
  speaker: 'More on the speaker: <a href="#turn">the horn</a>, <a href="#closer">the studio</a> and <a href="#spec">the particulars</a>.',
  dome: 'Also in Lighting: <a href="#core-ember">Core</a>, a table lamp in the same eight.',
  orb: 'Also in Lighting: <a href="#hemisphere-ember">Hemisphere</a>, a pendant in the same eight.',
  turntable: 'See it beside the speakers: <a href="#speakers">Tropos</a>.',
};
function renderProduct(Pr, k) {
  const c = BY[k]; P = Pr; cur = k;
  document.title = `${P.title(c)} · EARF`;
  const ll = document.getElementById('p-line-link'); ll.textContent = P.lineName; ll.href = `#${P.line}`;
  document.getElementById('p-crumb').textContent = P.id === 'speaker' ? c.name : P.title(c);
  document.getElementById('p-num').innerHTML = `${P.num(c)} &middot; In development`;   // the plain word on every product, once
  document.getElementById('p-name').textContent = P.name(c);
  document.getElementById('p-line').textContent = P.copy(c);
  document.getElementById('p-pick').textContent = c.name;
  document.getElementById('p-icon').innerHTML = P.id === 'speaker' ? icons(c) : '';         // the colour's own icon: by the
  document.getElementById('p-pick-ic').innerHTML = P.id === 'speaker' ? '' : icons(c);     // name it is, else by the colour
  document.getElementById('p-unit').innerHTML = `&middot; ${P.unit}`;
  document.getElementById('p-enquire').textContent = P.ask;
  document.getElementById('facts').innerHTML = P.facts(c).map(([a, b]) => `<dt>${a}</dt><dd>${b}</dd>`).join('');
  document.getElementById('swatches').replaceChildren(...D.clouds.map(o => { const li = el('li');
    li.appendChild(el('a', { href: `#${P.route}-${o.name.toLowerCase()}`, title: o.name, 'aria-label': o.name, ...(o.k === k ? { 'aria-current': 'true' } : {}) },
      `<span class="coin-dot" style="--i:${o.coin}"></span>`)); return li; }));
  thumbs.replaceChildren(...shown(c).map((v, i) => { const s = src(c, v), label = P.VIEWS.find(x => x[0] === v)[1];
    const b = el('button', { type: 'button', role: 'tab', id: `thumb-${i}`, 'data-v': v, 'aria-label': label, 'aria-controls': 'stage',
      class: 'thumb' + (v === 'turn' ? ' turn' : ''), style: s.th ? `background:url(${s.th}) center / cover no-repeat`
        : `background:url(${s.src}) ${v === 'turn' ? '0 0 / 600% 400%' : 'center / cover'} no-repeat` });
    b.addEventListener('click', () => showView(v)); return b; }));
  showView(shown(c)[0]);                              // Tropos opens on its photograph in its element, the rest on their hero
  company(document.getElementById('p-company'), k, P.id, true);
  document.getElementById('p-more').innerHTML = MORE[P.id] || '';
  v3sync();
}
// "Copy link": the product's own page for link previews (/s/<address>, its card in its colour), which forwards here
document.getElementById('p-share').addEventListener('click', () => {
  const url = `${location.origin}/s/${location.hash.slice(1)}`, note = document.getElementById('p-share-note');
  const say = t => { note.textContent = t; setTimeout(() => { note.textContent = ''; }, 2400); };
  try { navigator.clipboard.writeText(url).then(() => say('Link copied.'), () => say(url)); } catch (e) { say(url); }
});
//3D
// the 3D view (round 47): offered where the product has a model and the browser has WebGL 2; fetched only on the tap;
// the colour coins repaint it in place; any failure puts the pictures back and says why
const V3 = D.view3d || {}, has3d = !!window.WebGL2RenderingContext;
const v3btn = document.getElementById('v3d'), v3box = document.getElementById('v3d-box'), v3load = document.getElementById('v3d-load'), frameEl = stage.parentElement;
let v3 = null, v3for = null, v3busy = false;
const v3label = () => (V3[P.id].label || '{name}, in 3D').replace('{name}', BY[cur].name);
function v3close() {
  if (v3) v3.dispose(); v3 = null; v3for = null; v3box.hidden = true; v3load.textContent = '';
  frameEl.classList.remove('three'); v3btn.setAttribute('aria-pressed', 'false'); v3btn.textContent = 'View in 3D';
}
function v3sync() {
  v3btn.hidden = !(V3[P.id] && has3d);
  if ((v3 || frameEl.classList.contains('three')) && v3for !== P.id && !v3busy) v3close();
  if (v3) { v3.tint(V3[P.id].tints[cur]); v3box.setAttribute('aria-label', v3label()); }
}
v3btn.addEventListener('click', async () => {
  if (frameEl.classList.contains('three')) { v3close(); return; }
  if (v3busy) return;
  const spec = V3[P.id], pid = P.id; v3busy = true;
  frameEl.classList.add('three'); v3box.hidden = false; v3box.setAttribute('aria-label', v3label());
  v3btn.setAttribute('aria-pressed', 'true'); v3btn.textContent = 'Back to pictures'; v3load.textContent = 'Loading the model';
  try {
    const m = await import('./3d/viewer.js');
    if (!m.supported()) throw new Error('no WebGL 2');
    const v = await m.open(v3box, spec, spec.tints[cur], { reduce, onProgress: p => { v3load.textContent = `Loading the model, ${Math.round(p * 100)}%`; } });
    if (!frameEl.classList.contains('three') || P.id !== pid) { v.dispose(); }      // closed, or another product, while it loaded
    else { v3 = v; v3for = pid; v3.tint(spec.tints[cur]); v3load.textContent = ''; v3box.focus({ preventScroll: true }); }
  } catch (e) {
    v3close(); v3btn.hidden = true; document.getElementById('cap').textContent = 'The 3D view could not start in this browser; the pictures are all here.';
  }
  v3busy = false;
});
v3box.addEventListener('keydown', e => { if (e.key === 'Escape') { e.preventDefault(); v3close(); v3btn.focus(); } });
///3D
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
stage.addEventListener('pointerdown', e => { if (view !== 'turn' && view !== 'spin' && e.isPrimary) { sx = e.clientX; sy = e.clientY; } });
stage.addEventListener('pointerup', e => { if (sx === null) return; const dx = e.clientX - sx, dy = e.clientY - sy; sx = null;
  if (Math.abs(dx) > 40 && Math.abs(dx) > 1.2 * Math.abs(dy)) go(dx < 0 ? 1 : -1); });
stage.addEventListener('pointercancel', () => { sx = null; });

// the company a colour keeps, by the painter's wheel of six (round 25's idea, made the shop's in round 34): its
// complement opposite, its two neighbours, and itself in every line. Fog and Smoke have no hue: each is the other's
// complement, light against dark, and sits easiest beside the cool tints (Fog: Ice, Haze) or the deep ones (Smoke: Haze, Ember)
const HUE6 = { red: 0, orange: 1, amber: 2, green: 3, blue: 4, violet: 5 }, AT6 = Object.fromEntries(Object.entries(HUE6).map(([k, h]) => [h, k]));
function relations(k) {
  const h = HUE6[k];
  if (h === undefined) return { comp: [k === 'ice' ? 'black' : 'ice'], ana: k === 'ice' ? ['blue', 'violet'] : ['violet', 'red'], neutral: true };
  return { comp: [AT6[(h + 3) % 6]], ana: [AT6[(h + 5) % 6], AT6[(h + 1) % 6]], neutral: false };
}
function pcard(Pr, k) {
  const c = BY[k], im = Pr.card(k);
  const a = el('a', { class: 'pcard', href: `#${Pr.route}-${c.name.toLowerCase()}` },
    `<img data-src="${im.src}" width="${im.w}" height="${im.h}" alt="">` + (im.shown ? `<span class="tag">Shown in ${BY[im.shown].name}</span>` : '') +
    `<b>${Pr.id === 'speaker' ? `Tropos, ${c.name}` : Pr.name(c)}</b>` +
    `<span class="pc-col"><span class="coin-dot" style="--i:${c.coin}"></span>${Pr.id === 'speaker' ? Pr.kind : `${Pr.kind} in ${c.name}`}</span>`);
  a.querySelector('img').alt = Pr.title(c); later(a.querySelector('img'));
  return a;
}
// a row's cards for some colours: this product in each first, then the other lines' in each, as many as a row holds
function picks(cols, pid, k, max = 4) {
  const order = [...PRODUCTS.filter(x => x.id === pid), ...PRODUCTS.filter(x => x.id !== pid)], out = [];
  for (const Pr of order) for (const c of cols) if (!(Pr.id === pid && c === k) && Pr.views(c)) out.push([Pr, c]);
  return out.slice(0, max);
}
function block(id, title, note, cards) {
  const sec = el('section', { class: 'company', 'aria-labelledby': id });
  sec.appendChild(el('div', { class: 'goes-head' }, `<h2 id="${id}">${title}</h2><span>${note}</span>`));
  const g = el('div', { class: 'pgrid' }); cards.forEach(([Pr, c]) => g.appendChild(pcard(Pr, c))); sec.appendChild(g);
  return sec;
}
// each opposite pair's own line, written once for it (the critics: one sentence on every page read as a template)
const PAIR = { 'green|red': 'Red and green, minus the Christmas.', 'blue|orange': 'Orange and blue: each looks hotter, or colder, for the other.',
               'amber|violet': 'Yellow and violet: the sun, and the dusk it leaves.', 'black|ice': 'Clear and smoked: the same acrylic, light and dark.' };
function company(box, k, pid, mono) {
  const c = BY[k], r = relations(k), names = cs => cs.map(x => BY[x].name).join(' and '), pair = PAIR[[k, r.comp[0]].sort().join('|')] || '';
  const out = [
    block(`${box.id}-comp`, 'Complementary', r.neutral
      ? `${c.name} has no hue of its own, so it pairs by lightness with ${names(r.comp)}. ${pair}`
      : `${names(r.comp)}, opposite on the colour wheel. ${pair}`, picks(r.comp, pid, k)),
    block(`${box.id}-ana`, 'Analogous', r.neutral
      ? `${names(r.ana)}, the tints it sits easiest beside.`
      : `${names(r.ana)}, either side of it on the wheel.`, picks(r.ana, pid, k))];
  if (mono) out.push(block(`${box.id}-mono`, 'Monochromatic', `${c.name} in the other lines.`, picks([k], pid, k)));
  box.replaceChildren(...out);
}
// a colour's page: everything made in it, then its complement and its neighbours
function renderColour(k) {
  const c = BY[k];
  document.title = `${c.name} · EARF`;
  document.getElementById('c-crumb').textContent = c.name;
  document.getElementById('c-num').textContent = `Colour ${c.num} of 8`;
  document.getElementById('c-name').textContent = c.name;
  document.getElementById('c-line').textContent = c.line;
  document.getElementById('c-coin').innerHTML = `<span class="coin-dot" style="--i:${c.coin}"></span>`;
  document.getElementById('c-swatches').replaceChildren(...D.clouds.map(o => { const li = el('li');
    li.appendChild(el('a', { href: `#colour-${o.name.toLowerCase()}`, title: o.name, 'aria-label': o.name, ...(o.k === k ? { 'aria-current': 'true' } : {}) },
      `<span class="coin-dot" style="--i:${o.coin}"></span>`)); return li; }));
  document.getElementById('c-in').textContent = `In ${c.name}`;
  document.getElementById('c-in-note').textContent = `Every line, in ${c.tint.toLowerCase()} acrylic.`;
  document.getElementById('c-products').replaceChildren(...PRODUCTS.filter(Pr => Pr.views(k)).map(Pr => pcard(Pr, k)));
  company(document.getElementById('c-company'), k, 'speaker', false);
}

// the address: the home page and its sections; a line (#speakers, #lighting, #turntable, the speakers' band
// #tropos, and the old #atmosphere, #turn, #spec and #lamps on theirs); a colour (#colour-poison); or a product
// in a colour (#speaker-poison, #hemisphere-poison, #core-poison, #mantle-poison; round 35's names: the old #dome-,
// #orb- and #turntable- addresses are rewritten to them)
const OLD = { dome: 'hemisphere', orb: 'core', turntable: 'mantle' };
const home = document.getElementById('home'), pdp = document.getElementById('pdp');
const lineMain = document.getElementById('line'), colourMain = document.getElementById('colour'), MAINS = { home, line: lineMain, colour: colourMain, pdp };
['press', 'journal', 'privacy'].forEach(n => { const m = document.getElementById(n); if (m) MAINS[n] = m; });
const LINE_OF = { speakers: 'speakers', tropos: 'speakers', atmosphere: 'speakers', turn: 'speakers', spec: 'speakers', closer: 'speakers',
                  lighting: 'lighting', lamps: 'lighting', turntable: 'turntable', record: 'turntable' };
const LINE_NAME = { speakers: 'Speakers', lighting: 'Lighting', turntable: 'Turntable' };
const TITLE0 = document.title;
let last = null;
const showMain = name => { Object.entries(MAINS).forEach(([n, m]) => { m.hidden = n !== name; }); if (name !== 'pdp' && typeof v3close === 'function') v3close(); };
// the phones' Menu: opens and closes the pages' list; any page chosen, Escape, or a new address closes it
const navEl = document.getElementById('nav'), menuBtn = navEl.querySelector('.menu');
const menuOpen = o => { navEl.classList.toggle('open', o); menuBtn.setAttribute('aria-expanded', String(o)); };
menuBtn.addEventListener('click', () => menuOpen(!navEl.classList.contains('open')));
navEl.querySelectorAll('ul a').forEach(a => a.addEventListener('click', () => menuOpen(false)));
addEventListener('hashchange', () => menuOpen(false));
addEventListener('keydown', e => { if (e.key === 'Escape' && navEl.classList.contains('open')) { menuOpen(false); menuBtn.focus(); } });
const navAt = which => document.querySelectorAll('nav a[data-nav]').forEach(a => {
  if (a.dataset.nav === which) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); });
function route() {
  let h = location.hash.slice(1);
  let m, page;
  const o = /^(dome|orb|turntable)-([a-z]+)$/.exec(h);
  if (o && PBY[OLD[o[1]]]) { h = `${OLD[o[1]]}-${o[2]}`; history.replaceState(null, '', '#' + h); }
  if ((m = /^(speaker|hemisphere|core|mantle)-([a-z]+)$/.exec(h)) && PBY[m[1]] && keyOf(m[2]) && PBY[m[1]].views(keyOf(m[2]))) {
    page = h; showMain('pdp'); renderProduct(PBY[m[1]], keyOf(m[2]));
    if (!(last || '').startsWith(m[1] + '-')) scrollTo(0, 0);
    navAt(PBY[m[1]].line);
  } else if ((m = /^colour-([a-z]+)$/.exec(h)) && keyOf(m[1])) {
    page = h; showMain('colour'); renderColour(keyOf(m[1])); scrollTo(0, 0); navAt('colours');
  } else if (MAINS.press && h === 'press' || MAINS.privacy && h === 'privacy') {      // round 47: the press page, the privacy notice
    page = h; showMain(h); document.title = `${h === 'press' ? 'Press' : 'Privacy'} · EARF`; scrollTo(0, 0); navAt(null);
  } else if (MAINS.journal && (m = /^journal(?:-([a-z0-9-]+))?$/.exec(h)) && (!m[1] || document.getElementById(h))) {   // the journal and its posts
    page = h; showMain('journal');
    document.getElementById('journal-index').hidden = !!m[1];
    MAINS.journal.querySelectorAll('.post').forEach(a => { a.hidden = a.id !== h; });
    document.title = m[1] ? `${document.getElementById(h).dataset.title} · EARF` : 'Journal · EARF';
    scrollTo(0, 0); navAt('journal');
  } else if (LINE_OF[h] || /^(turntable|mantle)-/.test(h)) {         // Mantle's own addresses, before its page exists
    const L = LINE_OF[h] || 'turntable'; page = 'line-' + L; showMain('line');
    lineMain.querySelectorAll('.lineview').forEach(v => { v.hidden = v.dataset.line !== L; });
    document.title = `${LINE_NAME[L]} · EARF`;
    const target = document.getElementById(h);
    if (target && !LINE_NAME[h] && !/^(turntable|mantle)-/.test(h)) target.scrollIntoView(); else scrollTo(0, 0);
    navAt(L); ask();
  } else {
    page = 'home'; showMain('home'); document.title = TITLE0; heroIn();
    const target = h && document.getElementById(h);
    if (target && h !== 'top') target.scrollIntoView(); else if (last !== 'home' || h === 'top') scrollTo(0, 0);
    navAt(h === 'colours' ? 'colours' : null); ask();
  }
  last = page;
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
  const speakerOf = a => { const k = a && (a.dataset.k || keyOf((/#(?:speaker|dome|orb|turntable|colour)-([a-z]+)/.exec(a.getAttribute('href') || '') || [])[1])); return k && BY[k] ? BY[k].col : null; };
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


# round 47: a page per address for link previews. The site is one page whose views are #addresses, which a link
# preview never sees, so each product in each colour, each colour, the press page and each journal post gets a small
# page of its own at /s/<address>: its own card (Open Graph and Twitter: title, words, a 1200 x 630 picture in that
# colour, the colour as theme-color), schema.org data (a Product with no offer, as nothing is priced; an Article for a
# post), and a forward to the view itself. "Copy link" on a product's page gives this address.
def share_pages():
    from html import escape
    os.makedirs(os.path.join(SITE, 's'), exist_ok=True)
    os.makedirs(os.path.join(IMG, 'og'), exist_ok=True)
    def card(src, out, mode='crop'):
        im = Image.open(os.path.join(IMG, src)).convert('RGB')
        if mode == 'crop':                               # fill 1200 x 630, centred, a little above the middle
            s = max(1200 / im.width, 630 / im.height)
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            x, y = (im.width - 1200) // 2, int((im.height - 630) * 0.25)
            im = im.crop((x, y, x + 1200, y + 630))
        else:                                            # a tall picture, its edges carried out to the card's sides
            from PIL import ImageFilter
            im = im.resize((round(im.width * 630 / im.height), 630), Image.LANCZOS)
            a = np.asarray(im).astype(np.float32)
            left, right = np.median(a[:, :8], 1), np.median(a[:, -8:], 1)      # each row's own edge colour
            x0 = (1200 - im.width) // 2
            g = np.empty((630, 1200, 3), np.float32); g[:, :x0 + 8] = left[:, None]; g[:, x0 + 8:] = right[:, None]
            bg = Image.fromarray(g.astype(np.uint8)).filter(ImageFilter.GaussianBlur(6))
            ramp = np.clip(np.minimum(np.arange(im.width), np.arange(im.width)[::-1]) / 40.0, 0, 1)   # its sides feathered in
            mask = Image.fromarray((np.tile(ramp, (630, 1)) * 255).astype(np.uint8))
            bg.paste(im, (x0, 0), mask); im = bg
        im.save(os.path.join(IMG, 'og', out), quality=84, optimize=True, progressive=True)
        return f'img/og/{out}'
    def page(route, title, desc, img, alt, tint, kind, ld):
        t, d = escape(title), escape(desc)
        html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="{tint}">
<link rel="canonical" href="{URL}/s/{route}">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="EARF">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{URL}/s/{route}">
<meta property="og:image" content="{URL}/{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{escape(alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{URL}/{img}">
<script type="application/ld+json">{json.dumps(ld, separators=(',', ':'))}</script>
<meta http-equiv="refresh" content="0; url=/#{route}">
<script>location.replace('/#{route}')</script>
<style>body{{margin:0;font:17px/1.5 system-ui,sans-serif;background:#F4F1EC;color:#1C1A18;display:grid;place-items:center;min-height:100vh}}a{{color:inherit}}</style>
</head>
<body><main><p><a href="/#{route}">{t}</a></p></main></body>
</html>
"""
        open(os.path.join(SITE, 's', f'{route}.html'), 'w').write(html)
        return route
    brand = {'@type': 'Brand', 'name': 'EARF'}
    def product(name, colour, desc, img, extra=()):
        return {'@context': 'https://schema.org', '@type': 'Product', 'name': f'{name} in {colour}', 'brand': brand,
                'color': colour, 'description': desc, 'image': f'{URL}/{img}', 'category': extra[0] if extra else None,
                'additionalProperty': [{'@type': 'PropertyValue', 'name': 'Status', 'value': 'In development, not yet for sale'}]}
    made = []
    for k, num, name, icon, tint, line, cover in CLOUDS:
        low, col = name.lower(), MARK[k]
        img = card(f'{k}-habitat-1200.jpg', f'speaker-{k}.jpg')
        desc = f'{line} Tropos {num}, a powered horn loudspeaker cast in {tint.lower()} acrylic. In development, not yet for sale.'
        made.append(page(f'speaker-{low}', f'Tropos in {name} · EARF', desc, img, f'Tropos in {name}, {PLACES.get(ELEMENT[k], "on location")}',
                         col, 'product', product('Tropos', name, desc, img, ('Loudspeakers',))))
        for lk, lname, kind, lline, alt, facts in LAMPS:
            src = f'{lk}-{k}.jpg' if os.path.exists(os.path.join(IMG, f'{lk}-{k}.jpg')) else f'{lk}-red.jpg'
            img = card(src, f'{lk}-{k}.jpg', 'pad')
            desc = f'{lline} {kind} in {name}. In development, not yet for sale.'
            made.append(page(f'{SLUG[lk]}-{low}', f'{lname} in {name} · EARF', desc, img, f'{lname} lit, in {name}', col, 'product',
                             product(lname, name, desc, img, ('Lighting',))))
        if os.path.exists(os.path.join(IMG, f'tt-{k}-studio-1200.jpg')):
            img = card(f'tt-{k}-studio-1200.jpg', f'tt-{k}.jpg')
            desc = f'{TT["line"]} {TT["kind"]} in {name}. In development, not yet for sale.'
            made.append(page(f'mantle-{low}', f'{TT["name"]} in {name} · EARF', desc, img, f'{TT["name"]} in {name}', col, 'product',
                             product(TT['name'], name, desc, img, ('Turntables',))))
        img = card(f'{k}-studio-light-1200.jpg', f'colour-{k}.jpg')
        desc = f'{line} {name}: {tint.lower()} cast acrylic, in every EARF line.'
        made.append(page(f'colour-{low}', f'{name} · EARF', desc, img, f'Tropos in {name} in the studio', col, 'website',
                         {'@context': 'https://schema.org', '@type': 'WebPage', 'name': f'{name} · EARF', 'description': desc}))
    img = card('hero-1200.jpg', 'press.jpg')
    made.append(page('press', 'Press · EARF', BOILER_SHORT, img, 'The eight Tropos speakers on a curve, Ember to Smoke', '#F4F1EC', 'website',
                     {'@context': 'https://schema.org', '@type': 'Organization', 'name': 'EARF', 'url': URL, 'description': BOILER_SHORT,
                      'logo': f'{URL}/apple-touch-icon.png'}))
    for slug, d, title, stand, pic, body in JOURNAL:
        if not os.path.exists(os.path.join(IMG, pic)):
            continue
        plain = re.sub('&[a-z]+;', lambda m: {'&rsquo;': '’', '&nbsp;': ' ', '&deg;': '°'}.get(m.group(), ''), title)
        stand_ = re.sub('&[a-z]+;', lambda m: {'&rsquo;': '’', '&nbsp;': ' '}.get(m.group(), ''), stand)
        img = card(pic, f'journal-{slug}.jpg')
        made.append(page(f'journal-{slug}', f'{plain} · EARF', stand_, img, plain, '#F4F1EC', 'article',
                         {'@context': 'https://schema.org', '@type': 'Article', 'headline': plain, 'description': stand_,
                          'datePublished': d, 'image': f'{URL}/{img}', 'author': {'@type': 'Organization', 'name': 'EARF'},
                          'publisher': {'@type': 'Organization', 'name': 'EARF'}}))
    return made


def build():
    """The whole site into site/: the page as a document, the favicons, robots.txt and vercel.json."""
    # the 3D view's files (viewer/dist, from viewer/build.mjs: three.js and Tropos's compressed CAD) go into site/3d only
    # while VIEW3D is on; off, there is no site/3d, so the CAD is never deployed (the coordinator, 2026-10-31)
    # the type, self-hosted since round 47 (Instrument Sans and IBM Plex Mono, both SIL OFL; webfonts/, Google Fonts'
    # latin and latin-ext cuts): no third-party stylesheet in the way of the first paint
    shutil.copytree(os.path.join(HERE, 'webfonts'), os.path.join(SITE, 'fonts'), dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('fonts.css'))
    d3, src3 = os.path.join(SITE, '3d'), os.path.join(HERE, 'viewer', 'dist')
    if os.path.exists(d3):
        shutil.rmtree(d3)
    if VIEW3D and os.path.exists(src3):
        shutil.copytree(src3, d3)
    make_editorial()
    share_pages()
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
        print('pictures made:', len(make_images(a.sources)) + len(make_spin()) + len(make_campaign()))
    print(build())


if __name__ == '__main__':
    main()
