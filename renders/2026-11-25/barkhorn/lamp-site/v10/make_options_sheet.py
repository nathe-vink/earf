"""V10-1's options for the owner beside today's top sheet (v9): writes options-sheet.jpg here.
    .venv-fab/bin/python renders/2026-11-25/barkhorn/lamp-site/v10/make_options_sheet.py"""
import os
import matplotlib
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
TOP = os.path.join(HERE, '..', '..', '..', '..', '2026-11-24', 'barkhorn', 'lamp-site', 'tests', 'r2', 'top-sheet-v9.jpg')
FD = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
FB = ImageFont.truetype(os.path.join(FD, 'DejaVuSans-Bold.ttf'), 34)
F = ImageFont.truetype(os.path.join(FD, 'DejaVuSans.ttf'), 26)
top = Image.open(TOP).convert('RGB'); opt = Image.open(os.path.join(HERE, 'wiring-options.png')).convert('RGB')
H = 2400
top = top.resize((int(top.size[0] * H / top.size[1]), H), Image.LANCZOS)
opt = opt.resize((int(opt.size[0] * H / opt.size[1]), H), Image.LANCZOS)
HEAD = [
    'Hemisphere, the canopy\'s wiring (V10-1, 2026-11-25): the owner\'s choice. Left, today\'s top sheet (v9); right, the canopy as it is drawn today and the two ways to wire it.',
    'Both options: the driver screwed flat by its tabs under the enclosure\'s top; the mains spliced in the outlet box, not the canopy; the cord through a strain relief; a lever splice for its two conductors.',
    'Option 1 keeps the 150 x 50 canopy and moves the cord\'s exit 20 off the centre (toward one cable). Option 2 keeps the cord on the axis and makes the canopy 62 tall (12 more).',
    'Sizes in mm. The bushings\' and the driver\'s tabs\' sizes are as read from Heyco\'s and ERP\'s tables by the reviewer, to confirm on the parts.',
]
G = 30; TH = 30 + 44 * len(HEAD)
S = Image.new('RGB', (top.size[0] + G + opt.size[0], TH + H), (255, 255, 255))
d = ImageDraw.Draw(S)
for k, l in enumerate(HEAD):
    d.text((16, 16 + 44 * k), l, font=FB if k == 0 else F, fill=(0, 0, 0) if k == 0 else (50, 50, 50))
S.paste(top, (0, TH)); S.paste(opt, (top.size[0] + G, TH))
out = os.path.join(HERE, 'options-sheet.jpg'); S.save(out, quality=85); print(out, S.size, os.path.getsize(out))
