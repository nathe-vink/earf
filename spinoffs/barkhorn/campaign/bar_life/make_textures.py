"""The bar's life, its printed things (the owner, 2026-11-11: "It looks anemic in soul"): invented record covers (plain
graphic shapes in the eight tints, no real album art, no text), a folded newspaper's page (grey columns, no words), a
book of matches, and the one wry detail, a small tent card that says RESERVED, set at the foot of a speaker's bay.

    python3 spinoffs/barkhorn/campaign/bar_life/make_textures.py      ->  bar_life/tex/*.png
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'tex')
TINTS = {'ember': '#B50404', 'dust': '#D35D17', 'acid': '#C5BC1E', 'poison': '#027614', 'ice': '#1169C1', 'haze': '#500CB4',
         'fog': '#E2E1DF', 'smoke': '#4A4948'}
GROUNDS = ['#1C1B1A', '#E9E3D6', '#2A2622', '#D8CFBE', '#141414', '#EFEBE3', '#3A3530', '#C9BFAE']


def cover(k, n=512):
    """An invented cover: a ground and one or two plain shapes in the tints, each different."""
    rnd = random.Random(k)
    g = GROUNDS[k % len(GROUNDS)]
    im = Image.new('RGB', (n, n), g); d = ImageDraw.Draw(im)
    t = list(TINTS.values())
    a, b = t[k % 8], t[(k * 3 + 2) % 8]
    kind = k % 6
    if kind == 0:
        d.ellipse([n * 0.2, n * 0.2, n * 0.8, n * 0.8], fill=a)
    elif kind == 1:
        for j in range(6):
            d.rectangle([0, n * (0.1 + j * 0.14), n, n * (0.1 + j * 0.14) + n * 0.06], fill=a if j % 2 else b)
    elif kind == 2:
        d.polygon([(n * 0.5, n * 0.15), (n * 0.88, n * 0.85), (n * 0.12, n * 0.85)], fill=a)
        d.ellipse([n * 0.42, n * 0.55, n * 0.58, n * 0.71], fill=g)
    elif kind == 3:
        d.rectangle([n * 0.12, n * 0.12, n * 0.62, n * 0.62], fill=a); d.rectangle([n * 0.38, n * 0.38, n * 0.88, n * 0.88], fill=b)
    elif kind == 4:
        for j in range(5):
            r = n * (0.42 - j * 0.08)
            d.ellipse([n / 2 - r, n / 2 - r, n / 2 + r, n / 2 + r], fill=a if j % 2 == 0 else g)
    else:
        d.rectangle([0, n * 0.62, n, n], fill=a); d.ellipse([n * 0.3, n * 0.3, n * 0.7, n * 0.7], fill=b)
    return im


def newspaper(n=1024):
    """A folded broadsheet's visible half: grey columns of 'type' as fine lines, a block for a photo; no words."""
    im = Image.new('RGB', (n, int(n * 1.4)), '#E4E0D6'); d = ImageDraw.Draw(im)
    rnd = random.Random(7)
    d.rectangle([40, 30, n - 40, 110], fill='#3A3836')            # the masthead band, plain
    cols = 5; cw = (n - 80 - (cols - 1) * 18) / cols
    for c in range(cols):
        x0 = 40 + c * (cw + 18)
        y = 150
        if c in (1, 2):
            d.rectangle([x0, y, x0 + cw, y + 260], fill='#9A968E'); y += 280
        while y < im.size[1] - 40:
            w = cw * (0.6 + 0.4 * rnd.random()) if rnd.random() < 0.12 else cw
            d.line([(x0, y), (x0 + w, y)], fill='#7C7870', width=3); y += 11
            if rnd.random() < 0.05:
                y += 18
    return im


def matches(n=256):
    im = Image.new('RGB', (n, int(n * 1.6)), '#141414'); d = ImageDraw.Draw(im)
    d.rectangle([0, int(n * 1.2), n, int(n * 1.6)], fill='#7A2E1C')      # the striker, a plain band
    d.ellipse([n * 0.3, n * 0.35, n * 0.7, n * 0.75], outline='#C9A040', width=6)
    return im


def reserved(n=512):
    im = Image.new('RGB', (n, n // 2), '#EFEBE3'); d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 44)
    except OSError:
        f = ImageFont.load_default()
    w = d.textlength('RESERVED', font=f)
    d.text(((n - w) / 2, n // 4 - 26), 'RESERVED', fill='#2A2622', font=f)
    d.line([(n * 0.3, n // 4 + 34), (n * 0.7, n // 4 + 34)], fill='#2A2622', width=2)
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for k in range(16):
        cover(k).save(os.path.join(OUT, f'cover-{k:02d}.png'))
    newspaper().save(os.path.join(OUT, 'newspaper.png'))
    matches().save(os.path.join(OUT, 'matches.png'))
    reserved().save(os.path.join(OUT, 'reserved.png'))
    print(sorted(os.listdir(OUT)))
