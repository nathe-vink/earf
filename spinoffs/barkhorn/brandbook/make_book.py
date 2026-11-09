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
SITE_PICS = ['hero-1200.jpg', 'hero-portrait.jpg', 'lineup-1200.jpg', 'facade-1200.jpg',
             'lamps-domes-1200.jpg',
             'tt-violet-dusk-1200.jpg', 'tt-amber-studio-1200.jpg', 'red-studio-1200.jpg', 'lamp-dome-800.jpg',
             'inside.jpg'] + \
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


# Pinned to other lanes' commits (read-only), after the owner's rulings of 2026-10-31: Tropos always cover off and
# whole (the horn lane's golden-hour room, covers off); Core cordless (the lamps lane's cordless set). The site's
# macro crops of Tropos are no longer used.
PINNED = {'room.jpg': ('754e16a9852f364fb2ebe8eb752c10ab6bdc0e23', 'renders/2026-10-31/barkhorn/tropos-campaign/tropos-room-golden-hour-off.png'),
          'room-portrait.jpg': ('754e16a9852f364fb2ebe8eb752c10ab6bdc0e23', 'renders/2026-10-31/barkhorn/tropos-campaign/tropos-room-golden-hour-off-portrait.png'),
          'lamp-orb.jpg': ('735e759304b00400750741d5038722a3d4d5f5fb', 'renders/2026-10-31/barkhorn/lamps-cordless/site-img/lamp-orb.jpg'),
          'lamps-orbs.jpg': ('735e759304b00400750741d5038722a3d4d5f5fb', 'renders/2026-10-31/barkhorn/lamps-cordless/site-img/lamps-orbs.jpg'),
          'lamps-unlit.jpg': ('735e759304b00400750741d5038722a3d4d5f5fb', 'renders/2026-10-31/barkhorn/lamps-cordless/site-img/lamps-unlit.jpg'),
          'honest-a-ice.jpg': ('f7f03850edb54dfc9ccbe0cc2655b194cafc1232', 'renders/2026-11-03/barkhorn/base-question/gate2/A-ice-polished-honest.png'),
          'honest-dust-habitat.jpg': ('26493989e2b8f08fb2c359557034fc76ab234753', 'renders/2026-11-03/barkhorn/habitats/dust-portrait-1200x1500.jpg'),
          'honest-front-ember.jpg': ('e624e13e51812301e0a5641ef4fb5b75488e82f1', 'renders/2026-11-04/barkhorn/rollout/A-polished-fix1/site-front-off-tall-ember.png'),
          'honest-front-dust.jpg': ('e624e13e51812301e0a5641ef4fb5b75488e82f1', 'renders/2026-11-04/barkhorn/rollout/A-polished-fix1/site-front-off-tall-dust.png'),
          'honest-front-poison.jpg': ('e624e13e51812301e0a5641ef4fb5b75488e82f1', 'renders/2026-11-04/barkhorn/rollout/A-polished-fix1/site-front-off-tall-poison.png'),
          'honest-front-ice.jpg': ('e624e13e51812301e0a5641ef4fb5b75488e82f1', 'renders/2026-11-04/barkhorn/rollout/A-polished-fix1/site-front-off-tall-ice.png'),
          'honest-front-haze.jpg': ('3d0b613f4321610d6436aae97918d9534f11d857', 'renders/2026-11-04/barkhorn/rollout/A-polished-fix1/site-front-off-tall-haze.png'),
          'honest-front-fog.jpg': ('3d0b613f4321610d6436aae97918d9534f11d857', 'renders/2026-11-04/barkhorn/rollout/A-polished-fix1/site-front-off-tall-fog.png'),
          'honest-front-acid.jpg': ('04d21c5cba15fe98bc77f0e0a38c8c015c357649', 'renders/2026-11-04/barkhorn/rollout/A-polished-fix1/site-front-off-tall-acid.png'),
          'honest-ice-habitat.jpg': ('0f619953f86129dc54183718e2c50419f37ab820', 'renders/2026-11-03/barkhorn/habitats/ice-portrait-1200x1500.jpg')}


def pinned():
    root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, cwd=HERE).stdout.strip()
    for dst, (c, src) in PINNED.items():
        blob = subprocess.run(['git', 'show', f'{c}:{src}'], capture_output=True, cwd=root, check=True).stdout
        save(Image.open(io.BytesIO(blob)), dst)


def save(im, dst, width=1600, q=84):
    if dst.endswith('.png'):
        im.thumbnail((width, width * 4)); im.save(os.path.join(IMG, dst), optimize=True); return
    im = im.convert('RGB'); im.thumbnail((width, width * 4))
    im.save(os.path.join(IMG, dst), quality=q, optimize=True, progressive=True)


def main():
    import shutil
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
    for f in sorted(os.listdir(os.path.join(HERE, 'launch', 'out'))):   # the debut's paper and the one-pager
        if f.endswith('.png') or f == 'earf-teaser-storyboard.jpg':
            save(Image.open(os.path.join(HERE, 'launch', 'out', f)), f.rsplit('.', 1)[0] + '.jpg', width=1400, q=86)
        elif f.startswith('earf-teaser') and f.endswith('.mp4'):
            shutil.copy(os.path.join(HERE, 'launch', 'out', f), os.path.join(IMG, f))
    kso = os.path.join(HERE, 'kickstarter', 'out')   # the Kickstarter kit's pre-launch mockup
    for f in sorted(os.listdir(kso)) if os.path.isdir(kso) else []:
        if f.endswith('.png'):
            save(Image.open(os.path.join(kso, f)), 'ks-' + f[:-4] + '.jpg', width=1600, q=86)
    import shutil   # the motion: the site's turning globe and two of the parked idents (round 27)
    for dst, src in {'globe-turn.mp4': 'site/img/globe-turn.mp4', 'ident-coin.mp4': 'brand/earth-ident-coin-acrylic-paper.mp4',
                     'ident-rise.mp4': 'brand/earth-ident-rise-acrylic-night.mp4'}.items():
        shutil.copy(os.path.join(B, src), os.path.join(IMG, dst))
    pinned()
    print(len(os.listdir(IMG)), 'pictures in', IMG)


if __name__ == '__main__':
    main()
