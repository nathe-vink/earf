"""Round 35, step 1: how bright is Hemisphere North? (the owner, 2026-10-22: "I want to see a visual approximation of
the change in lumens to see if it's an acceptable amount of light.")

One dim dining room at night, a table 750 high, Hemisphere North hung with its rim 700 over the table, and one camera
at one exposure for every frame, like four photographs taken in that room on one setting. Two light levels at the COB,
about 1,100 lm (the original spec) and about 575 lm (the half-power option), in two shades: Ember (a mid tint) and
Smoke (the darkest). Nothing but the COB's power and the shade's colour changes between frames.

The calibration (README, round 35):
- A Cycles watt of white light is taken as 683 lm (the photometric definition), so an irradiance of 1 W/m2 in the
  engine is 683 lux and a radiance of 1 W/m2/sr is a luminance of 683 cd/m2. Blender's blackbody colours are
  normalised to luminance 1 (checked: 2700 K and white give the same reading), so the 2700 K colour does not move it.
- The COB is a Lambertian disc 10 across (the Vero SE 10's light-emitting surface, about), at its face in the hub, an
  area lamp of P = lumens / 683 W. Through the hub's black 46 bore alone the fitting passes 52 % of that (rendered
  with the fixture's own geometry over a white floor: 573 lm of 1,100 reach the floor, and 569 lux directly below at
  0.78 m, against 573 lux computed from I0 = lumens / pi / d2). The engineered hub has a reflector in the bore that
  passes about 85 % (an estimate for a faceted Miro reflector), so the lamp here is P x 0.85 / 0.521: the reflector's
  light spread like the direct light, inside the same 46 deg cut-off (an approximation).
- The exposure is a camera's: EV100 6.0, about what a phone picks at a dim restaurant table (f/1.8, 1/30 s, ISO 640).
  With 683 cd/m2 a unit and a saturation-based meter (L_max = 1.2 x 2^EV100 cd/m2 maps to 1.0), the engine's exposure
  is log2(683 / 1.2) - EV100 = 9.15 - 6.0 = 3.15 stops.
- The room's own light stays the same in every frame: two frosted wall lights on the back wall (about 120 lm each,
  2400 K), a floor lamp in the far corner (about 150 lm) and two candles on the sideboard (about 12 lm each).

    python3 spinoffs/barkhorn/companions/hemisphere_brightness.py                 # the shots
    PY=python3.11 python3 spinoffs/barkhorn/companions/hemisphere_brightness.py --render [names] [--scale 1.0]
    python3 spinoffs/barkhorn/companions/hemisphere_brightness.py --lux            # the table's illuminance, computed
    python3 spinoffs/barkhorn/companions/hemisphere_brightness.py --sheet
"""
import json, math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lamps-final')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-22', 'barkhorn', 'lamps-final', 'brightness')

LM_PER_W = 683.0
ETA_BORE = 0.521               # measured: the black bore's share (573 lm of 1,100 on the floor)
ETA_REFL = 0.85                # the reflector's, an estimate
EV100 = 6.0
EXPOSURE = round(math.log2(LM_PER_W / 1.2) - EV100, 3)
TABLE_Z, RIM_OVER = 0.75, 0.70
RIM_Z = TABLE_Z + RIM_OVER
COB_MM = 81.5                  # crystal.DOME_LIGHT: the COB's face above the rim
TABLE = (0.0, 0.95)            # the table's centre (x, y); the pendant over it
LEVELS = {'1100': 1100.0, '575': 575.0}
SHADES = {'ember': 'Ember', 'smoke': 'Smoke'}


def cob_w(lm, eta=ETA_REFL):
    return round(lm / LM_PER_W * eta / ETA_BORE, 4)


def kit(shape, material, **k):
    return {'kind': 'kit', 'shape': shape, 'material': material, **k}


def shot(level, shade):
    lm = LEVELS[level]
    tx, ty = TABLE
    s = {
        'title': f'Hemisphere North in {SHADES[shade]} at {lm:,.0f} lm, over a dining table at night',
        'size': [1800, 1200],
        'render': {'samples': 256, 'adaptive': 0.01, 'denoise': True, 'clamp': 10, 'bounces': 24,
                   'transmission_bounces': 20, 'view': 'Khronos PBR Neutral', 'exposure': EXPOSURE,
                   'white_balance_k': 3100},
        'sky': {'kind': 'none'},
        'set': {
            'kind': 'room', 'size': [5.2, 4.6, 2.7], 'center': [0.0, 0.85],
            'floor': {'plank_w': 0.16, 'plank_l': 1.8, 'base': '#6E4E34', 'dark': '#5A3E28', 'light': '#7E5C40',
                      'plank_contrast': 0.7},
            'wall': {'color': '#7D7466'}, 'ceiling': '#E6E0D6',
            'skirting': {'h': 0.12, 'color': '#6E665A'},
            'props': [
                {'kind': 'table', 'position': [tx, ty], 'size': [1.7, 0.9, TABLE_Z], 'color': '#6B4A30'},
                {'kind': 'sideboard', 'position': [0.55, 2.86], 'size': [1.6, 0.42, 0.78], 'color': '#3E2A1C',
                 'wood': 'veneer', 'grain': 0.25, 'turntable': False},
                {'kind': 'frame', 'position': [0.55, 3.15], 'z': 1.55, 'size': [0.7, 0.5], 'art': '#6E3A2A'},
                {'kind': 'lamp', 'position': [-2.15, 2.75], 'height': 1.55, 'shade': '#E8DCC8'},
                # two wall lights either side of the picture (the room's own light): opal cylinders, their glow an
                # emission at the luminance 120 lm gives them (L = lm / (pi A), about 580 cd/m2: 0.85 a unit, so an
                # exitance of 2.7, held at 1.4 so they do not burn out at this exposure), the light itself a point lamp just in front of each
                kit('cylinder', 'glow', color='#FFB878', emit=1.4, radius=0.06, height=0.16, position=[-0.25, 3.09, 1.62]),
                kit('cylinder', 'glow', color='#FFB878', emit=1.4, radius=0.06, height=0.16, position=[1.35, 3.09, 1.62]),
                # the table set for two: plates, glasses, a menu card to read by
                kit('cylinder', 'gloss', color='#F2EEE6', roughness=0.25, radius=0.135, height=0.016,
                    position=[tx - 0.38, ty - 0.12, TABLE_Z]),
                kit('cylinder', 'gloss', color='#F2EEE6', roughness=0.25, radius=0.135, height=0.016,
                    position=[tx + 0.38, ty + 0.12, TABLE_Z]),
                kit('lathe', 'glass', color='#F4F2EE', position=[tx - 0.18, ty - 0.30, TABLE_Z],
                    profile=[[0, 0], [0.035, 0], [0.035, 0.004], [0.004, 0.012], [0.004, 0.10], [0.038, 0.13],
                             [0.042, 0.19], [0.0, 0.19]]),
                kit('lathe', 'glass', color='#F4F2EE', position=[tx + 0.22, ty + 0.30, TABLE_Z],
                    profile=[[0, 0], [0.035, 0], [0.035, 0.004], [0.004, 0.012], [0.004, 0.10], [0.038, 0.13],
                             [0.042, 0.19], [0.0, 0.19]]),
                kit('box', 'paper', color='#F1ECE2', size=[0.15, 0.22, 0.002], position=[tx - 0.05, ty - 0.18, TABLE_Z],
                    rotate_z=12),
                # two candles in glass on the sideboard (a constant, and a scale: about 12 lm each)
                kit('cylinder', 'glow', color='#FFB060', emit=6.0, radius=0.004, height=0.012,
                    position=[0.05, 2.80, 0.78 + 0.075]),
                kit('cylinder', 'gloss', color='#EDE6D8', roughness=0.4, radius=0.022, height=0.075,
                    position=[0.05, 2.80, 0.78]),
                kit('cylinder', 'glow', color='#FFB060', emit=6.0, radius=0.004, height=0.012,
                    position=[0.17, 2.84, 0.78 + 0.06]),
                kit('cylinder', 'gloss', color='#EDE6D8', roughness=0.4, radius=0.022, height=0.06,
                    position=[0.17, 2.84, 0.78]),
                # Hemisphere North, its own lamp off (the COB is the area lamp below); the reflector part hidden, its
                # light carried by the lamp's power (the calibration above)
                {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'dome', 'spots': [[tx, ty, RIM_Z]],
                 'flavour': shade, 'ceiling': 2.7, 'lamp': False, 'shade_glow': 0.0, 'hide': 'reflector'},
            ],
        },
        'lights': {
            'cob': {'type': 'area', 'shape': 'DISK', 'size_m': [0.010, 0.010],
                    'position': [tx, ty, RIM_Z + COB_MM / 1000], 'target': [tx, ty, 0.0],
                    'power_w': cob_w(lm), 'color': 2700, 'camera': False},
            # the room's own light, the same in every frame
            'floorlamp': {'type': 'point', 'position': [-2.15, 2.75, 1.42], 'power_w': round(150 / LM_PER_W, 4),
                          'radius_m': 0.03, 'color': 2400, 'camera': False},
            'sconce1': {'type': 'point', 'position': [-0.25, 2.98, 1.70], 'power_w': round(120 / LM_PER_W, 4),
                        'radius_m': 0.03, 'color': 2400, 'camera': False},
            'sconce2': {'type': 'point', 'position': [1.35, 2.98, 1.70], 'power_w': round(120 / LM_PER_W, 4),
                        'radius_m': 0.03, 'color': 2400, 'camera': False},
            'candle1': {'type': 'point', 'position': [0.05, 2.80, 0.78 + 0.093], 'power_w': round(12 / LM_PER_W, 4),
                        'radius_m': 0.005, 'color': 1900, 'camera': False},
            'candle2': {'type': 'point', 'position': [0.17, 2.84, 0.78 + 0.078], 'power_w': round(12 / LM_PER_W, 4),
                        'radius_m': 0.005, 'color': 1900, 'camera': False},
        },
        'camera': {'position': [-0.62, -0.42, 1.30], 'target': [0.02, 0.95, 1.14], 'lens_mm': 32, 'level': True,
                   'fstop': 4.0, 'focus': [tx, ty, 1.1]},
    }
    return s


def name(level, shade):
    return f'north-{shade}-{level}'


FRAMES = {name(l, s): (l, s) for s in SHADES for l in LEVELS}


def build():
    os.makedirs(SHOTS, exist_ok=True)
    for n, (l, s) in FRAMES.items():
        json.dump(shot(l, s), open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)
        print(n, 'COB', cob_w(LEVELS[l]), 'W; exposure', EXPOSURE)


def render(names, scale, out=RENDERS):
    py = os.environ.get('PY', 'python3')
    os.makedirs(out, exist_ok=True)
    for n in names:
        subprocess.run([py, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
                        '--out', os.path.join(out, n + '.png'), '--scale', str(scale)], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(n, flush=True)


def lux(lm, eta=ETA_REFL, h=RIM_OVER + COB_MM / 1000, cut=46.3):
    """The table's illuminance from the fitting alone (direct light; the room's bounce adds a little), lux: the COB a
    Lambertian source of `lm`, the fitting passing `eta` of it inside the cut-off (the black bore 0.521, as rendered),
    spread like the direct light. Directly below; and the mean over a disc of radius 0.45 (a table for four) and 0.30
    (two places)."""
    I0 = lm / math.pi * eta / ETA_BORE

    def E(r):
        th = math.atan2(r, h)
        return 0.0 if math.degrees(th) > cut else I0 * math.cos(th) ** 4 / h ** 2

    def mean(R, n=400):
        return sum(E(R * (i + 0.5) / n) * 2 * (i + 0.5) / n / n for i in range(n))
    return E(0.0), mean(0.45), mean(0.30)


def report():
    rows = []
    for lvl, lm in LEVELS.items():
        for tag, eta in (('reflector (as rendered)', ETA_REFL), ('black bore (the hub as it was)', ETA_BORE)):
            e0, m45, m30 = lux(lm, eta)
            rows.append((lm, tag, round(lm * eta), round(e0), round(m45), round(m30)))
    print('| COB lm | hub | lm out | lux below | mean, 90 table | mean, 60 |')
    for r in rows:
        print('| {:,.0f} | {} | {:,} | {:,} | {:,} | {:,} |'.format(*r))
    # the bulb it equals, and a bare bulb's light at the same height for comparison
    for w, blm in ((40, 450), (60, 800), (75, 1100), (100, 1600)):
        print(f'bare {w} W bulb ({blm} lm, all round) at {RIM_OVER + COB_MM / 1000:.2f} m: '
              f'{blm / (4 * math.pi) / (RIM_OVER + COB_MM / 1000) ** 2:.0f} lux below')


def sheet():
    order = [name('1100', 'ember'), name('575', 'ember'), name('1100', 'smoke'), name('575', 'smoke')]
    labels = {name('1100', 'ember'): 'Ember, 1,100 lm at the COB (about 935 out): ~930 lux below, ~700 across the table',
              name('575', 'ember'): 'Ember, 575 lm at the COB (about 490 out): ~490 lux below, ~370 across the table',
              name('1100', 'smoke'): 'Smoke, 1,100 lm at the COB: the same light on the table',
              name('575', 'smoke'): 'Smoke, 575 lm at the COB: the same light on the table'}
    tiles = ' '.join(f"-label '{labels[n]}' {os.path.join(RENDERS, n + '.png')}" for n in order)
    out = os.path.join(RENDERS, 'sheet.png')
    subprocess.run(f"montage {tiles} -tile 2x2 -geometry 900x600+6+6 -pointsize 18 -background '#1A1816' "
                   f"-fill '#EDE6DA' -depth 8 {out}", shell=True, check=True)
    subprocess.run(f"convert {out} -gravity north -background '#1A1816' -fill '#EDE6DA' -pointsize 22 -splice 0x46 "
                   f"-annotate +0+10 'Hemisphere North over a dining table at night: one camera, one exposure (EV100 "
                   f"{EV100:g}), the rim 700 over the table' {out}", shell=True, check=True)
    print(out)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--render' in a:
        scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
        out = a[a.index('--out') + 1] if '--out' in a else RENDERS
        render([x for x in a if x in FRAMES] or list(FRAMES), scale, out)
    elif '--lux' in a:
        report()
    elif '--sheet' in a:
        sheet()
    else:
        build()
