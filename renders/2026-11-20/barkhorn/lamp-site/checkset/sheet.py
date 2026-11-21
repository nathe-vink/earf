"""sheet.py TINT [TROPOS_IMAGE]: the owner's sheet for one tint's pour check set (2026-11-21).
Columns: the Tropos front (if given), then the pendant's pours (today first), then the Core's (today first).
Rows: OFF over LIT. Each cell 400 x 500 (the half-size frame at half again), labelled with the lamp, the pour (x base
for the pendant, absolute for the Core) and today's mark; an empty cell where a frame was not rendered.
Today's frames come from the full-size renders (row-off/, house8/, house9/) scaled down; the rest from checkset/TINT/.
Writes checkset/sheet-TINT.png. Run with the .venv-fab python."""
import os, sys, glob, re
from PIL import Image, ImageDraw, ImageFont
T = sys.argv[1]; trop = sys.argv[2] if len(sys.argv) > 2 else None
HERE = os.path.dirname(os.path.abspath(__file__)); LS = os.path.dirname(HERE); D = os.path.join(HERE, T)
TODAY = {'red': (1.8, 0.5), 'orange': (3.0, 1.5), 'amber': (5.0, 1.5), 'green': (1.0, 0.3), 'blue': (6.0, 1.5),
         'violet': (1.8, 0.5), 'black': (1.2, 0.3)}[T]
NAME = {'red': 'Ember', 'orange': 'Dust', 'amber': 'Acid', 'green': 'Poison', 'blue': 'Ice', 'violet': 'Haze', 'black': 'Smoke'}[T]
def today(lamp, state):
    word = 'hemisphere' if lamp == 'hemi' else 'core'
    if T == 'red':
        p = os.path.join(LS, 'house8' if state == 'off' else 'house9', f'{word}-ember-{state}.png')
    else:
        p = os.path.join(LS, 'row-off', f'{word}-{T}-off.png') if state == 'off' else None
    return p if p and os.path.exists(p) else None
cols = []
for lamp, tl in (('hemi', TODAY[0]), ('core', TODAY[1])):
    loads = sorted({float(re.search(r'L([0-9.]+)\.png', f).group(1)) for f in glob.glob(os.path.join(D, f'{lamp}-*-L*.png'))} | {tl},
                   key=lambda v: (v != tl, -v))
    cols += [(lamp, v, v == tl) for v in loads]
CW, CH, TH = 400, 500, 40
W = CW * (len(cols) + (1 if trop else 0)); H = TH + 2 * CH
sh = Image.new('RGB', (W, H), (250, 248, 245)); dr = ImageDraw.Draw(sh)
try: fnt = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
except Exception: fnt = ImageFont.load_default()
x = 0
if trop:
    im = Image.open(trop).convert('RGB'); im.thumbnail((CW, 2 * CH)); sh.paste(im, (x + (CW - im.width) // 2, TH + (2 * CH - im.height) // 2))
    dr.text((x + 8, 10), f'{NAME} Tropos', fill=(20, 20, 20), font=fnt); x += CW
for lamp, v, is_today in cols:
    lab = f"{'Hemisphere' if lamp == 'hemi' else 'Core'} {v:g}{'x' if lamp == 'hemi' else ''}{'  (today)' if is_today else ''}"
    dr.text((x + 8, 10), lab, fill=(20, 20, 20), font=fnt)
    for r, state in enumerate(('off', 'lit')):
        p = os.path.join(D, f'{lamp}-{state}-L{v:g}.png')
        if not os.path.exists(p):
            p = os.path.join(D, f'{lamp}-{state}-L{v}.png')
        if not os.path.exists(p) and is_today:
            p = today(lamp, state)
        y = TH + r * CH
        if p and os.path.exists(p):
            sh.paste(Image.open(p).convert('RGB').resize((CW, CH), Image.LANCZOS), (x, y))
        else:
            dr.rectangle([x + 2, y + 2, x + CW - 3, y + CH - 3], outline=(200, 200, 200)); dr.text((x + 12, y + 12), f'{state.upper()} not rendered', fill=(150, 150, 150), font=fnt)
    x += CW
out = os.path.join(HERE, f'sheet-{T}.png'); sh.save(out, optimize=True); print(out, sh.size)
