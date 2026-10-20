"""The site's coins, re-rendered as EARFcoin blanks (round 33; the owner: "The existing coin render needs to be updated.
Each coin has the same square reflection on it, which makes them look flat all over again.").

Round 30's coins (icons_real.py --coin) were each rendered alone, square on and orthographic under globe_real's square
softbox, so all eight mirrored the same square. These are the EARFcoin's body (coin.py: 40 x 6, rims rounded 1.5,
reeded) with no globe and no words, all eight in one row in one scene: one soft round light, a camera straight above
and far enough back (perspective) that the light's reflection moves along the row, so no two coins carry the same one.
Each coin lies a degree or two off flat and turned, as coins lie on a table. On paper (E.PAPER) the face shows its
colour by transmission over the ground with a faint contact shadow; on night (E.NIGHT) each rim glows its colour from a
band of light inside it, as before.

Each coin is cut out centred in an 800 px square, filling it as round 30's did (its diameter 0.86 of the square), and
the ground made even and exactly the page's (web.layer multiplies the paper tiles and screens the night ones).

    python3 spinoffs/barkhorn/companions/site_coins.py                      # the two shots
    python3.11 spinoffs/barkhorn/companions/site_coins.py --render [--scale 1.0]   then the tiles and the sprite
"""
import json, math, os, random, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'coin')
OUT = os.path.join(ROOT, 'renders', '2026-10-20', 'barkhorn', 'coin', 'site-coins')
ORDER = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
GROUNDS = {'paper': '#F2EFEA', 'night': '#121114'}      # earth.PAPER, earth.NIGHT
PITCH, D = 0.050, 0.040
FILL = 0.86                      # the coin's diameter, of its square (round 30's tiles)
TILE = 800
H = 0.9                          # the camera's height (m): the row 0.4 long under it
PX_M = TILE * FILL / D           # pixels a metre at the coins
W_M = len(ORDER) * PITCH + 0.03
SIZE = [int(round(W_M * PX_M / 8)) * 8, 1056]
LENS = 36.0 * H / W_M
# on night each face glows faintly in its colour (round 30's NEON faces: the hues 0.15, Fog kept clear, Smoke dark)
# (Smoke's -1: a black disc in it, so its face stays dark under its glowing rim, as round 30's did)
FACE_GLOW = {k: 0.12 for k in ORDER} | {'fog': 0.04, 'smoke': -1}


def xs():
    return [(i - (len(ORDER) - 1) / 2) * PITCH for i in range(len(ORDER))]


def shot(ground):
    rnd = random.Random(30)
    night = ground == 'night'
    spots = []
    for x, fl in zip(xs(), ORDER):
        tilt = rnd.uniform(1.0, 2.0)
        a = rnd.uniform(0, 360)
        rx, ry = tilt * math.cos(math.radians(a)), tilt * math.sin(math.radians(a))
        spots.append({'position': [x, 0.0, (D / 2) * math.sin(math.radians(tilt))], 'flavour': fl,
                      'rotate': [round(rx, 2), round(ry, 2), round(rnd.uniform(0, 360), 1)]})
    props = [{'kind': 'kit', 'shape': 'ext', 'module': 'earf_coin', 'fn': 'coin', 'spots': spots, 'face': 'blank',
              'edge': 'reeded', **({'rim_glow': 1.6, 'face_glow': FACE_GLOW} if night else {})}]
    return {'title': f'The site\'s coins, {ground}', 'size': SIZE,
            'camera': {'position': [0.0, -0.0005, H], 'target': [0.0, 0.0, 0.0], 'lens_mm': round(LENS, 2), 'level': False,
                       'fstop': 0},
            'set': {'kind': 'sweep', 'color': GROUNDS[ground], 'width': 4.0, 'front': 2.0, 'depth': 1.5, 'radius': 0.6,
                    'height': 2.0, 'props': props},
            'sky': {'kind': 'gradient', 'zenith': '#CFCDC9', 'horizon': '#D6D4CF', 'ground': '#6A665F',
                    'strength': 0.12 if night else 0.55},
            # one soft round source high over the row's middle, a little behind it: its mirror image in the table lies
            # just past the coins' far edge, so each rim catches the light on the side facing that point (the left
            # coins' arcs to the right, the middle's at the top, the right's to the left) and no face mirrors it
            'lights': {'key': {'type': 'area', 'shape': 'DISK', 'size_m': [0.25, 0.25], 'position': [0.0, 0.18, 1.6],
                               'target': [0.0, 0.0, 0.0], 'irradiance': 0.5 if night else 2.2, 'color': '#FFF5E8'}},
            'render': {'samples': 160, 'adaptive': 0.01, 'denoise': True, 'clamp': 10, 'bounces': 16,
                       'view': 'Khronos PBR Neutral', 'exposure': 0.0, 'white_balance_k': 5600}}


def build():
    os.makedirs(SHOTS, exist_ok=True)
    for g in GROUNDS:
        json.dump(shot(g), open(os.path.join(SHOTS, f'site-coins-{g}.json'), 'w'), indent=1)


def tiles(ground, src):
    """Each coin centred in an 800 px square, the ground evened: a smooth surface fitted to the ground round the coin
    (outside 0.62 of the square) divided out (paper) or taken away (night), and the page's ground put in its place."""
    import numpy as np
    from PIL import Image
    v = np.asarray(Image.open(src).convert('RGB')).astype(float)
    Hh, Ww = v.shape[:2]
    target = np.array([int(GROUNDS[ground][i:i + 2], 16) for i in (1, 3, 5)], float)
    made = []
    fpx = LENS / 36.0 * Ww
    for x, fl in zip(xs(), ORDER):
        cx, cy = Ww / 2 + fpx * x / (H - 0.006), Hh / 2           # projected from the coins' top faces, 6 up
        x0, y0 = int(round(cx - TILE / 2)), int(round(cy - TILE / 2))
        t = v[y0:y0 + TILE, x0:x0 + TILE]
        yy, xx = np.mgrid[:TILE, :TILE] / TILE - 0.5
        rr = np.hypot(yy, xx)
        g = rr > 0.47                                            # outside the coin (0.43) and its contact shadow
        A = np.stack([np.ones_like(xx), xx, yy, xx * xx, yy * yy, xx * yy], -1)
        out = np.empty_like(t)
        for c in range(3):
            coef, *_ = np.linalg.lstsq(A[g], t[..., c][g], rcond=None)
            fit = A @ coef
            out[..., c] = t[..., c] / fit * target[c] if ground == 'paper' else t[..., c] - fit + target[c]
        # and beyond the coin and its contact shadow or glow, exactly the page's ground (a soft edge from 0.45 to 0.49
        # of the square), so no tile shows as a box once multiplied or screened onto the page
        m = np.clip((rr - 0.45) / 0.04, 0, 1)[..., None]
        out = out * (1 - m) + target * m
        f = os.path.join(OUT, f'{fl}-{ground}.png')
        Image.fromarray(np.clip(out, 0, 255).round().astype(np.uint8)).save(f)
        made.append(f)
    return made


def sprite():
    """The tiles as the site lays them (web.py: 128 px a coin, a row a ground, multiplied or screened), beside round
    30's sprites, for the look before handing them over."""
    from PIL import Image
    rows = []
    for g in GROUNDS:
        im = Image.new('RGB', (128 * 8, 128))
        for j, fl in enumerate(ORDER):
            im.paste(Image.open(os.path.join(OUT, f'{fl}-{g}.png')).convert('RGB').resize((128, 128), Image.LANCZOS), (128 * j, 0))
        p = os.path.join(OUT, f'sprite-{g}.png'); im.save(p); rows.append(p)
    old = [os.path.join(ROOT, 'spinoffs', 'barkhorn', 'site', 'img', f'coins-{k}.jpg') for k in ('light', 'dark')]
    cmp_ = os.path.join(OUT, 'compare.png')
    subprocess.run(['convert', '-background', '#888', old[0], rows[0], old[1], rows[1], '-splice', '0x6', '-append', cmp_],
                   check=True)
    return cmp_


if __name__ == '__main__':
    a = sys.argv[1:]
    build()
    if '--render' in a:
        os.makedirs(OUT, exist_ok=True)
        scale = a[a.index('--scale') + 1] if '--scale' in a else '1.0'
        for g in GROUNDS:
            src = os.path.join(OUT, f'row-{g}.png')
            subprocess.run([sys.executable, os.path.join(ROOT, 'studio', 'engine', 'render.py'),
                            os.path.join(SHOTS, f'site-coins-{g}.json'), '--out', src, '--scale', scale], check=True,
                           stdout=subprocess.DEVNULL)
            if scale == '1.0':
                print('\n'.join(tiles(g, src)))
        if scale == '1.0':
            print(sprite())
