"""Gathers the Brand Book's pictures into book/img/ from the approved list only, and fails on anything else.
book/index.html is written by hand.

The approved pictures (coordinator, 2026-11-10): Tropos in the eight colors with black rods (the speaker lane's tallr7
fronts and the horn from behind, r33-speaker-horn 370de3da), the Ember amplifier plate (cropped to the amplifier, so the
undecided rating plate is out of frame), the mark (the rendered globe A3 and its lockups and turn, the flat coins, the
chips), the black-rods habitats of Ice and Fog (r48-biomes 2904138e), and the drawn mockups (scenes/: the card, the
stationery, the crate decals, EARFcoin and the nine social posts), redrawn with the current mark and colors.

    python3 make_book.py
"""
import io, os, re, shutil, subprocess
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(HERE)
IMG = os.path.join(HERE, 'book', 'img')
TINTS = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
RODS = '370de3dafc36945fefed58e4b043fb0c604cd5d0'          # r33-speaker-horn: black rods, eight colors
ROLL = 'renders/2026-11-04/barkhorn/rollout'
BIOMES = '2904138ecb8f93d2709f32a987250c08f11c947b'                                    # r48-biomes: Ice and Fog in their elements, black rods
PINNED = {**{f'tropos-front-{t}.jpg': (RODS, f'{ROLL}/A-polished-tallr7/site-front-off-tall-{t}.png') for t in TINTS},
          'tropos-back-ember.jpg': (RODS, f'{ROLL}/A-polished-p2-p2b/horn-back-ember.png'),
          'tropos-ice-snow.jpg': (BIOMES, 'renders/2026-11-03/barkhorn/habitats/ice-portrait-1200x1500-blackrods.jpg'),
          'tropos-fog-habitat.jpg': (BIOMES, 'renders/2026-11-03/barkhorn/habitats/fog_b-portrait-1200x1500-r2-blackrods.jpg'),
          'tropos-amp-ember.jpg': ('488fbec9ed6764c60893e0a2798a6feba9ad296f', f'{ROLL}/A-polished-p2-backfix/amp-plate-ember.png')}
CROP = {'tropos-amp-ember.jpg': (0.40, 0.0, 1.0, 1.0)}      # left, top, right, bottom, of the frame
BRAND = {'globe-render.jpg': 'brand/mark/earf-globe-render.png', 'globe-render-night.jpg': 'brand/mark/earf-globe-render-night.png', 'lockup-render.jpg': 'brand/mark/earf-lockup-render.png',
         'lockup-render-night.jpg': 'brand/mark/earf-lockup-render-night.png',
         'globe-flat.png': 'brand/mark/earf-globe-tiles.png', 'globe-flat-night.png': 'brand/mark/earf-globe-tiles-night.png',
         'lockup-flat.png': 'brand/mark/earf-lockup-tiles.png', 'lockup-black.png': 'brand/mark/earf-lockup-black.png'}
MOCKUPS = {'card.jpg': 'card.png', 'stationery.jpg': 'stationery.png', 'coin.jpg': 'coin.png', 'social.jpg': 'social9.png'}
DECALS = ['decal-crate-front', 'decal-crate-inside', 'decal-crate-side']
ALLOWED = (set(PINNED) | set(BRAND) | set(MOCKUPS) | {f'icon-{t}.png' for t in TINTS} | {f'{d}.jpg' for d in DECALS} |
           {'lockup-color.png', 'globe-turn.mp4'})


def git_blob(commit, path):
    root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, cwd=HERE).stdout.strip()
    return subprocess.run(['git', 'show', f'{commit}:{path}'], capture_output=True, cwd=root, check=True).stdout


def save(im, dst, width=1600, q=84):
    if dst.endswith('.png'):
        im.thumbnail((width, width * 4)); im.save(os.path.join(IMG, dst), optimize=True); return
    im = im.convert('RGB'); im.thumbnail((width, width * 4))
    im.save(os.path.join(IMG, dst), quality=q, optimize=True, progressive=True)


def main():
    os.makedirs(IMG, exist_ok=True)
    for dst, (c, src) in PINNED.items():
        im = Image.open(io.BytesIO(git_blob(c, src)))
        if dst in CROP:
            l, t, r, b = CROP[dst]; W, H = im.size
            im = im.crop((round(l * W), round(t * H), round(r * W), round(b * H)))
        save(im, dst, width=1000)
    for t in TINTS:                                       # the chips, in the speakers' colors
        subprocess.run(['rsvg-convert', '-w', '256', '-h', '256', os.path.join(B, 'brand', f'icon-{t}.svg'),
                        '-o', os.path.join(IMG, f'icon-{t}.png')], check=True)
    for dst, src in BRAND.items():
        save(Image.open(os.path.join(B, src)), dst, width=1600 if dst == 'wordmark-color.png' else 1200, q=90)
    save(Image.open(os.path.join(B, 'brand/mark/earf-lockup-tiles.png')), 'lockup-color.png', width=500)   # the header
    shutil.copy(os.path.join(B, 'site/img/globe-turn.mp4'), os.path.join(IMG, 'globe-turn.mp4'))     # the A3 turn
    for dst, src in MOCKUPS.items():                     # the mockups, drawn from scenes/ by shoot.cjs
        save(Image.open(os.path.join(HERE, 'out', src)), dst, width=1800, q=86)
    for d in DECALS:
        im = Image.open(os.path.join(HERE, 'out', d + '.png')).convert('RGBA'); bg = Image.new('RGBA', im.size, (226, 207, 170, 255))
        save(Image.alpha_composite(bg, im), d + '.jpg', width=700)
    prune()
    fix_dims()
    print(len(os.listdir(IMG)), 'pictures in', IMG)


def fix_dims():
    """Write every img's width and height from the file itself, so lazy images hold their space."""
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
    """img/ holds what book/index.html uses, all of it on the approved list; anything else fails the build."""
    used = set(re.findall(r'img/([A-Za-z0-9._-]+)', open(os.path.join(HERE, 'book', 'index.html')).read()))
    bad = sorted(used - ALLOWED)
    if bad:
        raise SystemExit('not on the approved list: ' + ', '.join(bad))
    for f in os.listdir(IMG):
        if f not in used:
            os.remove(os.path.join(IMG, f))
    missing = sorted(u for u in used if not os.path.exists(os.path.join(IMG, u)))
    if missing:
        raise SystemExit('missing from img/: ' + ', '.join(missing))


if __name__ == '__main__':
    main()
