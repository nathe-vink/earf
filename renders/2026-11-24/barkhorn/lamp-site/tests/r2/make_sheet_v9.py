"""The Hemisphere top sheet v9 (the v8 check, 2026-11-25), built from v9.sh's frames.

Run with the CAD venv's Python (it has Pillow and matplotlib's DejaVu fonts), from anywhere:
    .venv-fab/bin/python renders/2026-11-24/barkhorn/lamp-site/tests/r2/make_sheet_v9.py
Writes top-sheet-v9.jpg next to this file.
"""
import os
import matplotlib
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
FB = ImageFont.truetype(os.path.join(FD, 'DejaVuSans-Bold.ttf'), 30)
F = ImageFont.truetype(os.path.join(FD, 'DejaVuSans.ttf'), 24)
INK, GREY, SOFT = (0, 0, 0), (40, 40, 40), (60, 60, 60)

# per column: the frame, its title, its labels (mm), the hanging weight from the v9 solids
COLS = [
    ('v9-today', 'Today', ['clamp ring 104 across x 5 tall', 'collar top 96 across x 3', 'crown 80 across x 11.5',
                           'cap 40 across x 14', 'foot ring 10.9 tall', 'NO positive lock (its 5 tall ring cannot', 'take one): the J-slot and a detent only', 'hangs 1607 g']),
    ('v9-A', 'A: three even tiers, without the lock', ['ring 10.8 + the collar\'s 0.5, 104 across', 'crown 80 across x 11.3',
                                     'cap 56 across x 11.3', 'steps of 24 across (12 per side)',
                                     'foot ring 10.9 tall, sloped', 'its cables at 0/180; the J-slot and a detent',
                                     'with the lock: the row below (1708 g)', 'hangs 1688 g']),
    ('v9-B', 'B: four even tiers', ['ring 8.0 + the collar\'s 0.5, 104 across', 'crown 80 and 56 across x 8.5 each',
                                    'cap 32 across x 8.5', 'steps of 24 across (12 per side)',
                                    'foot ring 10.9 tall, sloped', 'cables beside the cap; the cap on a magnet',
                                    'only, its Ø56 tier the handle', 'NO positive lock (its 8 tall ring cannot take',
                                    'one): the J-slot and a detent only', 'hangs 1586 g']),
]
FOOT = [
    'All three use the fixed shade release: a smaller white disc on the hub and a white lip on the collar, inside the shade\'s top.',
    'A and B change every shade\'s collar (a Ø100 shoulder: the acrylic\'s hole Ø100.4 against Ø96.4) and clamp ring, with four',
    '    silicone rings and shims picked per shade (against two).',
    'All three hang from two rated stainless cables (32 apart; B 35) on stop sleeves in the hub, splayed to grippers 96 apart',
    '    in the canopy: level once the two are set equal (1 mm out tips it about 1.3 deg). The cord is set 2 mm longer, so it bows about 2 cm.',
    'The bayonet is keyed (one Ø6 pin on its own M4 thread, one 7 wide slot): every shade fits one way only.',
    'A can carry a lock (Ganter GN 617; the owner decides) at the back of its clamp ring, its Ø21 matte black knob 29 out (the row',
    '    above): pull it to lift and turn the shade. Without it, and on TODAY\'S TOP AND B (rings 5 and 8 tall), THERE IS NO POSITIVE',
    '    LOCK: the shade holds by the J-slot (a lift, a turn and a lower against its weight) and a ball detent.',
    'The collar is black anodised; its foot beneath the lip and its flange face inside are painted white.',
    'Hemisphere, Ember, off. Level views: one camera 1.6 m off, 200 mm lens.',
]
LOCK = [
    ('lock-1-hidden', 'A WITH THE LOCK, as drawn: its knob behind the crown, its cables on the lock\'s line'),
    ('lock-2-profile', 'A with the lock, the lamp turned 79 deg: the knob in profile (same camera)'),
]
BELOW = [
    ('v9-below', 'From below: 0.29 m under the rim, 3 cm off the axis, 40 mm lens'),
    ('v9-below35', 'From below, 35 deg off the axis, 50 mm lens (cropped above the shade and at its foot)'),
]
BELOW_NOTE = [
    'The lip, the disc and the carrier are the same in all three tops, so one picture from below serves them (not the tops).',
    'In the 35 deg view the black stem runs down from the hub to the carrier.',
    'The studio\'s lamps are off and there is no room; an even white dome, the camera at Blender\'s neutral (6500 K, tint 10).',
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
# the 35 deg view cropped: its bottom 7 % (the floor's edge stood in it) and its top 18 % (the cord and the cables end
# there in mid-air, the canopy out of frame; the v5 check's (11))
bel = [load(b) for b, _ in BELOW]
bel[1] = bel[1].crop((0, int(bel[1].size[1] * 0.18), bel[1].size[0], int(bel[1].size[1] * 0.93)))
bel = [fit(im, BW) for im in bel]
BH = max(b.size[1] for b in bel)
lk = [fit(load(b), BW) for b, _ in LOCK]
LH = max(b.size[1] for b in lk)
TH = 52 + 32 * max(len(l) for _, _, l in COLS) + 16
FT = 16 + 32 * len(FOOT)
BN = 16 + 32 * len(BELOW_NOTE)

S = Image.new('RGB', (SW, TH + H + 50 + CH + 50 + LH + 50 + BH + BN + FT), (255, 255, 255))
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
for i, ((b, t), bi) in enumerate(zip(LOCK, lk)):
    x = i * (BW + G)
    d.text((x + 8, y + 10), t, font=F, fill=GREY)
    S.paste(bi, (x, y + 50))
y += 50 + LH
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
out = os.path.join(HERE, 'top-sheet-v9.jpg')
S.save(out, quality=88)
print(out, S.size, os.path.getsize(out))
