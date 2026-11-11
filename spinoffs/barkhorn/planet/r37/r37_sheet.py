"""Round 37's configuration sheet for the owner: rows the bar and the listening zone, columns the four configurations
(Smoke, Ember, Ice, Mixed), the street and the sink beneath, each labelled. Under 5 MB (a JPG if the PNG is over).

    python3 spinoffs/barkhorn/planet/r37/r37_sheet.py [FINALS_DIR] [OUT]
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
FIN = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'renders/2026-10-20/barkhorn/planet37/finals')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(FIN, 'planet37-configurations.png')

CONFIGS = [('smoke', 'Smoke', 'the house: every product in Smoke'),
           ('ember', 'Ember', 'every product in Ember'),
           ('ice', 'Ice', 'every product in Ice'),
           ('mixed', 'Mixed', 'bar: Ice pair, Dust Domes, Fog R3s / zone: Ember pair, Acid Orbs')]
ROWS = [('bar', 'The bar'), ('listening', 'The listening\nzone')]
CW, CH = 600, 400                      # a cell: each 1200 x 800 final at half size
M, G, LW, TH, FH = 40, 16, 190, 92, 46  # margin, gutter, row-label column, column-heading band, caption band
BG, INK, MUTE = (16, 14, 13), (236, 230, 220), (150, 142, 132)

W = M + LW + 4 * CW + 3 * G + M


def font(size, weight='Medium'):
    for path in (f'/usr/share/fonts/opentype/inter/Inter-{weight}.otf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def main():
    big_w = (4 * CW + 3 * G - G) // 2              # the street and the sink, two cells wide each
    big_h = big_w * 2 // 3
    H = M + 70 + TH + 2 * (CH + FH) + G + FH + big_h + FH + M
    sheet = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(sheet)
    d.text((M, M), 'Planet EARF, round 37: the bar as a showroom', font=font(34, 'SemiBold'), fill=INK)
    d.text((M, M + 44), 'One room, four configurations. Proposals until the owner signs them.', font=font(19, 'Regular'), fill=MUTE)
    y = M + 70
    x0 = M + LW
    for k, (key, name, sub) in enumerate(CONFIGS):
        x = x0 + k * (CW + G)
        d.text((x, y + 22), name, font=font(28, 'SemiBold'), fill=INK)
        d.text((x, y + 58), sub, font=font(15, 'Regular'), fill=MUTE)
    y += TH
    for rkey, rname in ROWS:
        d.multiline_text((M, y + CH // 2 - 28), rname, font=font(22, 'SemiBold'), fill=INK, spacing=6)
        for k, (key, name, sub) in enumerate(CONFIGS):
            p = os.path.join(FIN, f'{rkey}-{key}.png')
            x = x0 + k * (CW + G)
            if os.path.exists(p):
                sheet.paste(Image.open(p).convert('RGB').resize((CW, CH), Image.LANCZOS), (x, y))
            else:
                d.rectangle((x, y, x + CW, y + CH), outline=MUTE); d.text((x + 12, y + 12), f'missing {rkey}-{key}', font=font(16), fill=MUTE)
        y += CH + FH
    y += G
    for k, (key, cap) in enumerate((('street', 'The shopfront at night, from the kerb (Smoke)'),
                                    ('sink', 'The sink in Smoke: polished cast acrylic, 160 thick (it reads as black stone or lacquer at this stage)'))):
        x = x0 + k * (big_w + G)
        p = os.path.join(FIN, f'{key}.png')
        if os.path.exists(p):
            sheet.paste(Image.open(p).convert('RGB').resize((big_w, big_h), Image.LANCZOS), (x, y))
        d.text((x, y + big_h + 12), cap, font=font(18, 'Regular'), fill=INK)
    sheet.save(OUT, optimize=True)
    out = OUT
    if os.path.getsize(OUT) > 5_000_000:
        out = os.path.splitext(OUT)[0] + '.jpg'
        sheet.save(out, quality=90, optimize=True)
        os.remove(OUT)
    print(out, sheet.size, os.path.getsize(out))


if __name__ == '__main__':
    main()
