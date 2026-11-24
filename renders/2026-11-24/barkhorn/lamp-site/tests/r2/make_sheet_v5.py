"""The Hemisphere top sheet v5 (check 4, 2026-11-24), built from v5.sh's frames.

Run with the CAD venv's Python (it has Pillow and matplotlib's DejaVu fonts), from anywhere:
    .venv-fab/bin/python renders/2026-11-24/barkhorn/lamp-site/tests/r2/make_sheet_v5.py
Writes top-sheet-v5.jpg next to this file.
"""
import os
import matplotlib
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
FB = ImageFont.truetype(os.path.join(FD, 'DejaVuSans-Bold.ttf'), 30)
F = ImageFont.truetype(os.path.join(FD, 'DejaVuSans.ttf'), 24)
INK, GREY, SOFT = (0, 0, 0), (40, 40, 40), (60, 60, 60)

# per column: the frame, its title, its labels (mm), the hanging weight from the v5 solids
COLS = [
    ('v5-today', 'Today', ['clamp ring 104 across x 5 tall', 'collar top 96 across x 3', 'crown 80 across x 11.5',
                           'cap 40 across x 14', 'foot ring 10.9 tall', 'hangs 1598 g']),
    ('v5-A', 'A: three even tiers', ['ring 10.8 + the collar\'s 0.5, 104 across', 'crown 80 across x 11.3',
                                     'cap 56 across x 11.3', 'steps of 24 across (12 per side)',
                                     'foot ring 10.9 tall, sloped', 'hangs 1679 g']),
    ('v5-B', 'B: four even tiers', ['ring 8.0 + the collar\'s 0.5, 104 across', 'crown 80 and 56 across x 8.5 each',
                                    'cap 32 across x 8.5', 'steps of 24 across (12 per side)',
                                    'foot ring 10.9 tall, sloped', 'hangs 1577 g']),
]
FOOT = [
    'All three use the fixed shade release: a smaller white disc on the hub and a white lip on the collar, inside the shade\'s top.',
    'A and B change every shade\'s collar (a Ø100 shoulder: the acrylic\'s hole Ø100.4 against Ø96.4) and clamp ring, with four',
    '    silicone rings and shims picked per shade (against two).',
    'All three hang from two rated cables 35 apart, drawn beside the cord: level once the two are set equal at the canopy',
    '    (1 mm out tips it about 1.6 deg).',
    'The collar is black anodised, its lip painted white beneath; the crown\'s inside is dim from below, lit only through the mouth.',
    'Hemisphere, Ember, off. Level views: one camera 1.6 m off, 200 mm lens.',
]
BELOW = [
    ('v5-below', 'From below: 0.29 m under the rim, 3 cm off the axis, 40 mm lens'),
    ('v5-below35', 'From below, 35 deg off the axis, 50 mm lens (its foot cropped)'),
]
BELOW_NOTE = [
    'One picture serves all three tops: the lip, the disc and the carrier are the same in each.',
    'The studio\'s lamps are off and there is no room; an even white dome, the camera at 6504 K, tint 0.',
    'The black disc in the middle is the LED carrier (Ø56); it hides the white disc (Ø62) from straight below.',
]


def load(name):
    return Image.open(os.path.join(HERE, name + '.png')).convert('RGB')


def fit(im, w):
    return im.resize((w, int(im.size[1] * w / im.size[0])), Image.LANCZOS)


full = [load(c) for c, _, _ in COLS]
W, H = full[0].size
crop = [fit(load(c + '-x2'), W) for c, _, _ in COLS]
CH = crop[0].size[1]
G = 20
SW = 3 * W + 2 * G
BW = (SW - G) // 2
# the 35 deg view's bottom 7 % is cropped: the floor's edge stood in it
bel = [load(b) for b, _ in BELOW]
bel[1] = bel[1].crop((0, 0, bel[1].size[0], int(bel[1].size[1] * 0.93)))
bel = [fit(im, BW) for im in bel]
BH = max(b.size[1] for b in bel)
TH = 52 + 32 * max(len(l) for _, _, l in COLS) + 16
FT = 16 + 32 * len(FOOT)
BN = 16 + 32 * len(BELOW_NOTE)

S = Image.new('RGB', (SW, TH + H + 50 + CH + 50 + BH + BN + FT), (255, 255, 255))
d = ImageDraw.Draw(S)
for i, ((c, t, ls), fi, ci) in enumerate(zip(COLS, full, crop)):
    x = i * (W + G)
    d.text((x + 8, 10), t, font=FB, fill=INK)
    for k, l in enumerate(ls):
        d.text((x + 8, 52 + k * 32), l, font=F, fill=GREY)
    S.paste(fi, (x, TH))
    d.text((x + 8, TH + H + 10), 'the top, 1.8x', font=F, fill=GREY)
    S.paste(ci, (x, TH + H + 50))
y = TH + H + 50 + CH
for i, ((b, t), bi) in enumerate(zip(BELOW, bel)):
    x = i * (BW + G)
    d.text((x + 8, y + 10), t, font=F, fill=GREY)
    S.paste(bi, (x, y + 50))
y += 50 + BH + 8
for l in BELOW_NOTE:
    d.text((8, y), l, font=F, fill=SOFT); y += 32
y += 8
for l in FOOT:
    d.text((8, y), l, font=F, fill=SOFT); y += 32
out = os.path.join(HERE, 'top-sheet-v5.jpg')
S.save(out, quality=88)
print(out, S.size, os.path.getsize(out))
