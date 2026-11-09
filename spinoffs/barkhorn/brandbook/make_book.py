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
         'globe-flat.png': 'brand/mark/earf-globe-colour.png', 'wordmark-color.png': 'brand/mark/earf-wordmark-color-mark.png',
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
          'honest-a-ice.jpg': ('f7f03850edb54dfc9ccbe0cc2655b194cafc1232', 'renders/2026-11-03/barkhorn/base-question/gate2/A-ice-polished-honest.png'),
          'honest-front-ember.jpg': ('4fcc28f879d93486c22844a2630b17df1b2e6013', 'renders/2026-11-04/barkhorn/rollout/A-polished-tallr6/site-front-off-tall-ember.png'),
          'honest-front-dust.jpg': ('5c8371479a9a2fd63a497c7fc7d4ddb7d6e18ac2', 'renders/2026-11-04/barkhorn/rollout/A-polished-tallr6/site-front-off-tall-dust.png'),
          'honest-front-poison.jpg': ('766f299df9326d6b77b3ab9a96d782aeb320329c', 'renders/2026-11-04/barkhorn/rollout/A-polished-tallr3/site-front-off-tall-poison.png'),
          'honest-front-ice.jpg': ('48dcfd298e39c6e36477a85a9d42e2ecce747968', 'renders/2026-11-04/barkhorn/rollout/A-polished-tallr6/site-front-off-tall-ice.png'),
          'honest-front-haze.jpg': ('94b4534a7684c55e0b3420728f09d12dc6c283f3', 'renders/2026-11-04/barkhorn/rollout/A-polished-tallr3/site-front-off-tall-haze.png'),
          'honest-front-fog.jpg': ('4e89a8340d5de6efbe02286b639d081432db84f1', 'renders/2026-11-04/barkhorn/rollout/A-polished-tallr6/site-front-off-tall-fog.png'),
          'honest-front-acid.jpg': ('7d741bd64b16731318a1fc724dd5453aefefc66b', 'renders/2026-11-04/barkhorn/rollout/A-polished-tallr6/site-front-off-tall-acid.png'),
          'honest-ice-habitat.jpg': ('0f619953f86129dc54183718e2c50419f37ab820', 'renders/2026-11-03/barkhorn/habitats/ice-portrait-1200x1500.jpg'),
          'honest-amp-ember.jpg': ('488fbec9ed6764c60893e0a2798a6feba9ad296f', 'renders/2026-11-04/barkhorn/rollout/A-polished-p2-backfix/amp-plate-ember.png'),
          'honest-mantle-day.jpg': ('41232b56c60d1980a5ee3de0dddd8344ffb85fee', 'renders/2026-11-03/barkhorn/mantle-r48/a5-day-ember-2423-c3e.png'),
          'honest-dust-habitat.jpg': ('43c91242f3d29b3da0bb4da4f16ddc0bc30616d1', 'renders/2026-11-03/barkhorn/habitats/dust-portrait-1200x1500-nopanel.jpg'),}


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
    for n in ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']:   # the chips: the brand icons in the Mark values
        subprocess.run(['rsvg-convert', '-w', '256', '-h', '256', os.path.join(B, 'brand', f'icon-{n}.svg'),
                        '-o', os.path.join(IMG, f'icon-{n}.png')], check=True)
    for dst, src in BRAND.items():
        save(Image.open(os.path.join(B, src)), dst, width=1600 if dst == 'wordmark-color.png' else 1200)
    save(Image.open(os.path.join(B, 'brand/mark/earf-lockup-colour.png')), 'lockup-color.png', width=250)   # the header mark
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
    prune()
    fix_dims()
    print(len(os.listdir(IMG)), 'pictures in', IMG)


def fix_dims():
    """Write every img's width and height from the file itself (2026-11-09), so lazy images hold their space."""
    import re
    p = os.path.join(HERE, 'book', 'index.html'); s = open(p).read()
    def one(mm):
        tag, f = mm.group(0), mm.group(1)
        fp = os.path.join(IMG, f)
        if not os.path.exists(fp) or not f.lower().endswith(('.jpg', '.png')):
            return tag
        w, h = Image.open(fp).size
        tag = re.sub(r'\s(width|height)="\d+"', '', tag)
        return tag[:-1] + f' width="{w}" height="{h}">'
    open(p, 'w').write(re.sub(r'<img src="img/([A-Za-z0-9._-]+)"[^>]*>', one, s))


def prune():
    """Keep only what book/index.html references (2026-11-09): anything else in img/ would be published with the page."""
    import re
    used = set(re.findall(r'img/([A-Za-z0-9._-]+)', open(os.path.join(HERE, 'book', 'index.html')).read()))
    for f in os.listdir(IMG):
        if f not in used:
            os.remove(os.path.join(IMG, f))
    missing = sorted(u for u in used if not os.path.exists(os.path.join(IMG, u)))
    if missing:
        raise SystemExit('missing from img/: ' + ', '.join(missing))


if __name__ == '__main__':
    main()
