"""Round 31's launch-page pictures of the Clouds, written as shot files for studio/engine/render.py. The owner, on the
spotlight shots (shoot31.py): "I was thinking more sleek imagery akin to Apple product images, when they announce a
new product and it has a dedicated webpage."

So: the speaker centred on a seamless, sculpted by big soft lights and long strip lights that trace its edges (the
engine's `panel`s: graduated emitters the camera cannot see, which the acrylic's polish mirrors as a clean line), a
glow on the wall behind it, a glossy floor that gives back a faint reflection, and room for type. No props.

- hero-dark-<name>: one per colour, 2560 x 1440, three-quarter view at about eye level, cover off, on a near-black
  seamless; the eight identical but for the colour, so the site can switch between them.
- hero-light-<name>: the same shot on a pale warm-grey seamless (Ember, Ice, Fog).
- lineup: the eight in a row in spectrum order on a glossy black floor, lit from behind so the colours glow, 2880 x 1200.
- macro-<detail>-<name>: 1600 x 1600 details, each in the colour that shows it best.

    python3 spinoffs/barkhorn/studio31.py       ->  studio/shots/barkhorn/studio31/*.json
"""
import copy, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'studio31')
PRODUCT = 'studio/products/barkhorn-cloud.json'
# the Clouds in spectrum order, by name, with their flavour in the product file (finals.py FLAVOUR, keyed by colour)
COLOURS = [('ember', 'cloud-red'), ('dust', 'cloud-orange'), ('acid', 'cloud-amber'), ('poison', 'eucalyptus-y2k-green'),
           ('ice', 'cloud-blue'), ('haze', 'cloud-violet'), ('fog', 'birch-fog-clear'), ('smoke', 'cloud-black')]
FLAVOUR = dict(COLOURS)
LIGHT_ONES = ['ember', 'ice', 'fog']

RENDER = {'samples': 80, 'adaptive': 0.015, 'denoise': True, 'clamp': 4, 'bounces': 16,
          'view': 'Khronos PBR Neutral', 'exposure': 0.0, 'white_balance_k': 5600, 'white_balance_tint': 10.0}
FINISH = {'enabled': True, 'white_in': 235, 'white_out': 238, 'contrast': 0.10, 'clarity': 0.06,
          'sharpen': 0.3, 'sharpen_px': 0.7}


def product(name, rotate=0.0, at=(0.0, 0.0)):
    return {'def': PRODUCT, 'flavour': FLAVOUR[name],
            'instances': [{'position': [at[0], at[1], 0], 'rotate_z': rotate, 'flavour': FLAVOUR[name], 'hide': ['cloth-disc']}]}


def seamless(dark):
    """A wide cove; dark, a near-black that only the glow lights; light, a pale warm grey. Both a little glossy, so the
    floor gives back a soft reflection of the speaker."""
    return {'kind': 'sweep', 'color': '#141416' if dark else '#D9D5CF', 'width': 24.0, 'front': 14.0, 'depth': 3.2,
            'radius': 2.6, 'height': 9.0, 'contact': {'strength': 0.35, 'distance_m': 0.08, 'core_strength': 0.4,
                                                      'core_distance_m': 0.012}}


def strips(level=1.0, recv=('*#0',)):
    """The strip lights: two tall panels behind and to each side, which the acrylic's side edges and faces mirror as
    long clean lines, and one long one overhead for the top's edge and the horn's lip."""
    return {
        'strip-left': {'type': 'panel', 'size_m': [0.22, 3.2], 'orbit': {'azimuth_deg': -118, 'elevation_deg': 8, 'distance_m': 2.6},
                       'target': [0.0, 0.0, 0.6], 'strength': 22.0 * level, 'diffuse': 0.35, 'specular': 1.0, 'receivers': list(recv),
                       'ramp': {'axis': 'z', 'at_m': [-0.4, 0.9, 2.2], 'values': [0.25, 1.0, 0.25]}},
        'strip-right': {'type': 'panel', 'size_m': [0.22, 3.2], 'orbit': {'azimuth_deg': 112, 'elevation_deg': 8, 'distance_m': 2.6},
                        'target': [0.0, 0.0, 0.6], 'strength': 22.0 * level, 'diffuse': 0.35, 'specular': 1.0, 'receivers': list(recv),
                        'ramp': {'axis': 'z', 'at_m': [-0.4, 0.9, 2.2], 'values': [0.25, 1.0, 0.25]}},
        'strip-top': {'type': 'panel', 'size_m': [2.4, 0.4], 'position': [0.0, 0.35, 3.1], 'target': [0.0, 0.0, 0.9],
                      'strength': 10.0 * level, 'diffuse': 0.5, 'specular': 1.0, 'receivers': list(recv),
                      'ramp': {'axis': 'x', 'at_m': [-1.2, 0.0, 1.2], 'values': [0.2, 1.0, 0.2]}},
    }


def hero(name, dark=True):
    s = {'title': f'barkhorn, {name}, launch hero ({"dark" if dark else "light"})', 'size': [2560, 1440],
         'product': product(name, rotate=-36.0), 'set': seamless(dark),
         'camera': {'position': [0.0, -8.4, 1.0], 'target': [0.0, 0.0, 0.6], 'lens_mm': 72.0, 'level': True},
         'sky': {'kind': 'none'}, 'render': dict(RENDER), 'finish': dict(FINISH),
         'materials': {'sweep': {'roughness': 0.2 if dark else 0.28}}}
    L = {
        # the key: a big softbox high and to the left of the camera, the faces' long gradient
        'key': {'type': 'area', 'size_m': [2.4, 1.6], 'orbit': {'azimuth_deg': -42, 'elevation_deg': 32, 'distance_m': 3.4},
                'target': [0.0, 0.0, 0.6], 'irradiance': 2.4 if dark else 1.8, 'color': '#FFF6EC', 'spread_deg': 70,
                'camera': False},
        # a low soft fill from the right, so the shadow side keeps its colour
        'fill': {'type': 'area', 'size_m': [2.0, 2.0], 'orbit': {'azimuth_deg': 55, 'elevation_deg': 6, 'distance_m': 4.0},
                 'target': [0.0, 0.0, 0.55], 'irradiance': 0.35 if dark else 0.6, 'color': '#F2F5FF', 'camera': False},
        # the glow: a lamp behind the speaker facing the wall, a pool of light that fades to the edges of the frame
        'glow': {'type': 'area', 'shape': 'DISK', 'size_m': [0.3, 0.3], 'position': [0.0, 0.42, 0.62],
                 'target': [0.0, 4.0, 1.5], 'spread_deg': 110, 'power_w': 420.0 if dark else 0.0, 'color': '#FFF1E2', 'camera': False,
                 'specular': 0.0},
        # a card high in front, seen only in reflections: a long soft sheen down the faces and into the horn's mouth
        'sheen': {'type': 'panel', 'size_m': [3.0, 1.4], 'position': [-0.9, -3.4, 2.5], 'target': [0.0, 0.0, 0.9],
                  'strength': 5.0, 'diffuse': 0.0, 'specular': 1.0, 'receivers': ['*#0'],
                  'ramp': {'axis': 'z', 'at_m': [1.9, 3.2], 'values': [0.15, 1.0]}},
        **strips(1.0 if dark else 0.7),
    }
    if not dark:
        # a pale room: a soft white dome, so the floor's gloss mirrors light and not a black void, and a broad wash on
        # the seamless, brightest behind the speaker and falling off to the sides
        s['sky'] = {'kind': 'gradient', 'zenith': '#E9E6E1', 'horizon': '#E4E0DA', 'ground': '#BDB8B0', 'strength': 0.75}
        L['wash'] = {'type': 'area', 'size_m': [6.0, 3.0], 'position': [0.0, -2.5, 4.2], 'target': [0.0, 3.0, 1.4],
                     'irradiance': 0.4, 'color': '#FFF8F0', 'camera': False, 'specular': 0.0}
    s['lights'] = L
    return s


# the details: (name, colour, the speaker's turn, camera position, target, lens); each in the colour that shows it best
MACROS = [
    # the horn from the side: its rolled lip at the mouth and the twist-lock cap at its back (Acid: the lip glows gold)
    ('horn', 'acid', 128.0, [1.2, -2.5, 1.3], [0.0, 0.02, 1.1], 150.0),
    # the woofer in its coloured ring, a little off axis (Ice: the blue ring round the grey cone)
    ('woofer', 'ice', -20.0, [0.55, -3.0, 0.62], [0.0, -0.2, 0.49], 185.0),
    # a grip cut through the side, near the top (Poison: green light through the cut's polished walls)
    ('grip', 'poison', -58.0, [0.45, -2.6, 1.3], [0.12, 0.0, 0.765], 230.0),
    # a top corner, level with it: 20 mm of acrylic, its polished edges (Ember)
    ('corner', 'ember', -36.0, [1.3, -2.25, 1.15], [0.10, -0.33, 0.86], 240.0),
    # the amplifier's plate on the back, at an angle (Dust)
    ('amp', 'dust', 214.0, [0.3179, -1.1848, 0.805], [0.0926, -0.1909, 0.505], 85.0),
]


def macro(key, name, rotate, cam, target, lens):
    s = hero(name, True)
    s['title'] = f'barkhorn, {name}, detail: {key}'
    s['size'] = [1600, 1600]
    s['product'] = product(name, rotate=rotate)
    s['camera'] = {'position': cam, 'target': target, 'lens_mm': lens, 'level': False}
    return s


# the lineup: the eight in a row, a hand's width apart, on a glossy black floor
GAP = 0.95


def lineup():
    s = hero('ember', True)
    s['title'] = 'barkhorn, the eight Clouds in a row'
    s['size'] = [2880, 1200]
    xs = [(i - 3.5) * GAP for i in range(8)]
    s['product'] = {'def': PRODUCT, 'flavour': COLOURS[0][1],
                    'instances': [{'position': [x, 0, 0], 'rotate_z': -24.0, 'flavour': fl, 'hide': ['cloth-disc']}
                                  for x, (n, fl) in zip(xs, COLOURS)]}
    s['set'] = dict(seamless(True), color='#0F0F11', width=30.0)
    s['materials'] = {'sweep': {'roughness': 0.14}}
    s['camera'] = {'position': [0.0, -14.0, 1.15], 'target': [0.0, 0.0, 0.56], 'lens_mm': 64.0, 'level': True}
    recv = [f'*#{i}' for i in range(8)]
    L = {
        'key': {'type': 'area', 'size_m': [8.0, 1.6], 'position': [-1.4, -3.6, 2.8], 'target': [0.0, 0.0, 0.6],
                'irradiance': 1.0, 'color': '#FFF6EC', 'spread_deg': 80, 'camera': False, 'receivers': recv},
        # the backlight: a long soft bank behind the row, low, shining through the acrylic toward the camera
        'back': {'type': 'area', 'size_m': [9.0, 0.6], 'position': [0.0, 1.5, 0.45], 'target': [0.0, -2.0, 0.42],
                 'irradiance': 6.0, 'color': '#FFF4E6', 'spread_deg': 90, 'camera': False, 'specular': 0.0},
        # the glow on the wall behind, wide
        'glow': {'type': 'area', 'size_m': [7.0, 0.3], 'position': [0.0, 0.6, 0.3], 'target': [0.0, 4.0, 1.6],
                 'spread_deg': 110, 'power_w': 2400.0, 'color': '#FFF1E2', 'camera': False, 'specular': 0.0},
        'strip-top': {'type': 'panel', 'size_m': [9.0, 0.4], 'position': [0.0, 0.35, 3.1], 'target': [0.0, 0.0, 0.9],
                      'strength': 3.0, 'diffuse': 0.2, 'specular': 1.0, 'receivers': recv},
        'sheen': {'type': 'panel', 'size_m': [9.0, 1.4], 'position': [-0.6, -3.6, 2.6], 'target': [0.0, 0.0, 0.9],
                  'strength': 1.5, 'diffuse': 0.0, 'specular': 1.0, 'receivers': recv,
                  'ramp': {'axis': 'z', 'at_m': [2.0, 3.3], 'values': [0.15, 1.0]}},
    }
    s['lights'] = L
    return s


def main():
    os.makedirs(OUT, exist_ok=True)
    made = {}
    for name, _ in COLOURS:
        made[f'hero-dark-{name}'] = hero(name, True)
    for name in LIGHT_ONES:
        made[f'hero-light-{name}'] = hero(name, False)
    made['lineup'] = lineup()
    for m in MACROS:
        made[f'macro-{m[0]}-{m[1]}'] = macro(*m)
    for n, sh in made.items():
        json.dump(sh, open(os.path.join(OUT, n + '.json'), 'w'), indent=1)
    print(len(made), 'shots in', os.path.relpath(OUT, ROOT))


if __name__ == '__main__':
    main()
