"""Round 38's sheet: the six finals in Smoke on one page, labelled (the owner: "Planet: Smoke, ledge at counter height").

    python3 spinoffs/barkhorn/planet/r38/r38_sheet.py [FINALS_DIR] [OUT]
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
FIN = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'renders/2026-10-20/barkhorn/planet38/finals')
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(FIN, 'planet38-smoke.png')
FRAMES = [('bar-smoke', 'The bar: the pair raised on ledges at counter height, the decks and the request column'),
          ('coins-decks', 'EARFcoin at the decks: the request column, lit from its base'),
          ('listening-smoke', 'The listening zone: the altar pair, a record and a coat'),
          ('street', 'The shopfront at night, from the kerb'),
          ('sink', 'The sink: polished cast acrylic in Smoke, read as black glass'),
          ('coins-door', 'EARFcoin at the door: a coin for each guest')]
CW, CH, M, G, FH = 900, 600, 48, 20, 44
BG, INK, MUTE = (16, 14, 13), (236, 230, 220), (150, 142, 132)


def font(size, weight='Regular'):
    p = f'/usr/share/fonts/opentype/inter/Inter-{weight}.otf'
    return ImageFont.truetype(p, size) if os.path.exists(p) else ImageFont.load_default()


def main():
    W = M * 2 + 2 * CW + G
    H = M + 96 + 3 * (CH + FH) + 2 * G + M
    sheet = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(sheet)
    d.text((M, M), 'Planet EARF, round 38: the house in Smoke', font=font(36, 'SemiBold'), fill=INK)
    d.text((M, M + 48), 'EARFcoin, the lamps\' black hardware, the room lived in. Proposals until the owner signs them.',
           font=font(19), fill=MUTE)
    y = M + 96
    for k, (key, cap) in enumerate(FRAMES):
        x = M + (k % 2) * (CW + G); yy = y + (k // 2) * (CH + FH + G)
        p = os.path.join(FIN, f'{key}.png')
        if os.path.exists(p):
            sheet.paste(Image.open(p).convert('RGB').resize((CW, CH), Image.LANCZOS), (x, yy))
        d.text((x, yy + CH + 12), cap, font=font(18), fill=INK)
    sheet.save(OUT, optimize=True)
    out = OUT
    if os.path.getsize(OUT) > 5_000_000:
        out = os.path.splitext(OUT)[0] + '.jpg'; sheet.save(out, quality=90, optimize=True); os.remove(OUT)
    print(out, sheet.size, os.path.getsize(out))


if __name__ == '__main__':
    main()
