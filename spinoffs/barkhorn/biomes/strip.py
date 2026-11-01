"""The eight habitats side by side, as the coordinator's strip (4870 x 750: eight 600 x 750 portraits, 10 px apart).

    python3 spinoffs/barkhorn/biomes/strip.py OUT.jpg [--smoke NEW_PORTRAIT]

The seven come from the site's live portraits (spinoffs/barkhorn/site/img/<key>-habitat-portrait.jpg, Ember to Fog);
Smoke from --smoke when given (the aligned proof), else its live portrait.
"""
import argparse, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, '..', 'site', 'img')
KEYS = ['red', 'orange', 'amber', 'green', 'blue', 'violet', 'ice', 'black']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('--smoke')
    a = ap.parse_args()
    W, H, G = 600, 750, 10
    strip = Image.new('RGB', (8 * W + 7 * G, H), (244, 241, 236))
    for i, k in enumerate(KEYS):
        p = a.smoke if (k == 'black' and a.smoke) else os.path.join(IMG, f'{k}-habitat-portrait.jpg')
        im = Image.open(p).convert('RGB')
        s = max(W / im.width, H / im.height)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        x0, y0 = (im.width - W) // 2, (im.height - H) // 2
        strip.paste(im.crop((x0, y0, x0 + W, y0 + H)), (i * (W + G), 0))
    strip.save(a.out, quality=90)
    print(a.out, strip.size)


if __name__ == '__main__':
    main()
