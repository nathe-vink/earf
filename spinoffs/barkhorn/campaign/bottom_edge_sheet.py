"""The bottom-edge sheets for the owner (v2, 2026-11-09): one view's crops side by side, each at 2x by pixel doubling
(nearest neighbour, so no resampling and no ringing), titled with the product, the view, the floor and the scale, and
the seam measured as bright pixels against black on all three channels (not red alone).

    python3 spinoffs/barkhorn/campaign/bottom_edge_sheet.py OUT.png "TITLE" "NOTE" LABEL=IMG [LABEL=IMG ...]

The seam is counted on every tile (see seam()). A label starting with "test" is drawn in red: a test, not an option.
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
BOLD = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'


def lum(a):
    return a[..., :3].astype(float) @ np.array([0.2126, 0.7152, 0.0722])


def seam(img):
    """Bright against black: pixels in the crop's lower half of luma above 200 with a pixel below 60 within 2 px
    straight above or below them. A soft shadow edge has no such step; a lit line against a dark edge or skirt does.
    Luma takes all three channels, so a white line counts as much as a red one."""
    L = lum(img)
    H = L.shape[0]
    dark = L < 60
    near = np.zeros_like(dark)
    for dy in (-2, -1, 1, 2):
        near |= np.roll(dark, dy, 0)
    m = (L > 200) & near
    m[: H // 2] = False
    m[-2:] = False
    return int(m.sum())


def main():
    out, title, note = sys.argv[1:4]
    tiles = [a.split('=', 1) for a in sys.argv[4:]]
    f, fb = ImageFont.truetype(FONT, 40), ImageFont.truetype(BOLD, 46)
    rows = []
    for label, path in tiles:
        im = Image.open(path).convert('RGB')
        a = np.array(im)
        n = seam(a)
        im2 = im.resize((im.width * 2, im.height * 2), Image.NEAREST)
        rows.append((label + f'   ·   seam: {n} px', im2, label.startswith('test')))
    W = max(r[1].width for r in rows)
    pad, lh = 24, 58
    tl = title.split('\n') + note.split('\n')
    Ht = pad + len(tl) * lh + pad + sum(lh + r[1].height + pad for r in rows)
    sheet = Image.new('RGB', (W + 2 * pad, Ht), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    y = pad
    for k, t in enumerate(tl):
        d.text((pad, y), t, fill=(0, 0, 0) if k < len(title.split('\n')) else (70, 70, 70), font=fb if k == 0 else f)
        y += lh
    y += pad
    for label, im2, test in rows:
        d.text((pad, y), label, fill=(190, 20, 20) if test else (0, 0, 0), font=f)
        y += lh
        sheet.paste(im2, (pad, y))
        y += im2.height + pad
    sheet.save(out, optimize=True)
    print(out, sheet.size)


if __name__ == '__main__':
    main()
