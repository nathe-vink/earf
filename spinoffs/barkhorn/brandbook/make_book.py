"""Gathers the Brand Book's pictures into book/img/ (JPEG, 1600 px at most) from the site, the brand files, the
mockups in out/ and, read-only, the bar's renders on origin/r33-planet-world. book/index.html is written by hand.

    python3 make_book.py
"""
import os, subprocess, io
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(HERE)
IMG = os.path.join(HERE, 'book', 'img')
SITE = os.path.join(B, 'site', 'img')
KEYS = ['red', 'orange', 'amber', 'green', 'blue', 'violet', 'ice', 'black']
SITE_PICS = ['hero-1200.jpg', 'hero-portrait.jpg', 'lineup-1200.jpg', 'room-1440.jpg', 'facade-1200.jpg', 'macro-horn.jpg',
             'macro-corner.jpg', 'macro-woofer.jpg', 'lamps-orbs-1200.jpg', 'lamps-domes-1200.jpg', 'lamps-unlit-800.jpg',
             'tt-violet-dusk-1200.jpg', 'tt-amber-studio-1200.jpg', 'red-studio-1200.jpg', 'lamp-dome-800.jpg',
             'lamp-orb-800.jpg', 'inside.jpg'] + \
            [f'{k}-habitat-1200.jpg' for k in KEYS] + [f'{k}-studio-light-1200.jpg' for k in KEYS]
BRAND = {'lockup-paper.jpg': 'brand/mark/earf-lockup-render.png', 'lockup-night.jpg': 'brand/mark/earf-lockup-render-night.png',
         'globe-paper.jpg': 'brand/mark/earf-globe-render.png', 'globe-night.jpg': 'brand/mark/earf-globe-render-night.png',
         'globe-flat.png': 'brand/mark/earf-globe-colour.png', 'wordmark-colour.png': 'brand/mark/earf-wordmark-colour.png',
         'lockup-black.png': 'brand/mark/earf-lockup-black.png', 'lockup-white.png': 'brand/mark/earf-lockup-white.png',
         'globe-real.jpg': 'brand/real/earf-real-colour.png', 'globe-real-night.jpg': 'brand/real/earf-real-colour-night.png'}
BAR = {'bar-door.jpg': 'renders/2026-10-22/barkhorn/planet41/finals/door-mother-colour-p3-1200.jpg',
       'bar-street.jpg': 'renders/2026-10-22/barkhorn/planet39/finals/street-1200.jpg',
       'bar-decks.jpg': 'renders/2026-10-20/barkhorn/planet38/finals-best/coins-decks.png',
       'bar-listening.jpg': 'renders/2026-10-20/barkhorn/planet38/finals-best/listening-smoke.png'}


def save(im, dst, width=1600, q=84):
    if dst.endswith('.png'):
        im.thumbnail((width, width * 4)); im.save(os.path.join(IMG, dst), optimize=True); return
    im = im.convert('RGB'); im.thumbnail((width, width * 4))
    im.save(os.path.join(IMG, dst), quality=q, optimize=True, progressive=True)


def main():
    os.makedirs(IMG, exist_ok=True)
    for f in SITE_PICS:
        save(Image.open(os.path.join(SITE, f)), f.replace('-1200', '').replace('-1440', '').replace('-800', ''))
    for f in [f'icon-{n}-light.webp' for n in ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']]:
        save(Image.open(os.path.join(SITE, f)), f.replace('-light.webp', '.png'), width=256)
    for dst, src in BRAND.items():
        save(Image.open(os.path.join(B, src)), dst, width=1200)
    root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, cwd=HERE).stdout.strip()
    for dst, src in BAR.items():
        blob = subprocess.run(['git', 'show', f'origin/r33-planet-world:{src}'], capture_output=True, cwd=root).stdout
        save(Image.open(io.BytesIO(blob)), dst)
    for f in sorted(os.listdir(os.path.join(HERE, 'out'))):
        if f.endswith('.png') and not f.startswith('decal-'):
            save(Image.open(os.path.join(HERE, 'out', f)), f[:-4] + '.jpg', width=1800, q=86)
    for f in ['decal-crate-front.png', 'decal-crate-side.png', 'decal-crate-inside.png']:
        im = Image.open(os.path.join(HERE, 'out', f)).convert('RGBA'); bg = Image.new('RGBA', im.size, (226, 207, 170, 255))
        save(Image.alpha_composite(bg, im), f[:-4] + '.jpg', width=700)
    print(len(os.listdir(IMG)), 'pictures in', IMG)


if __name__ == '__main__':
    main()
