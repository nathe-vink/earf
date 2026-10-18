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

RENDER = {'samples': 128, 'adaptive': 0.01, 'denoise': True, 'clamp': 4, 'bounces': 16,
          'view': 'Khronos PBR Neutral', 'exposure': 0.0, 'white_balance_k': 5800, 'white_balance_tint': 0.0}
FINISH = {'enabled': True, 'white_in': 235, 'white_out': 238, 'contrast': 0.10, 'clarity': 0.03,
          'sharpen': 0.12, 'sharpen_px': 0.7}


def product(name, rotate=0.0, at=(0.0, 0.0)):
    return {'def': PRODUCT, 'flavour': FLAVOUR[name],
            'instances': [{'position': [at[0], at[1], 0], 'rotate_z': rotate, 'flavour': FLAVOUR[name], 'hide': ['cloth-disc']}]}


def seamless(dark):
    """A wide cove; dark, a near-black that only the glow lights; light, a pale warm grey. Both a little glossy, so the
    floor gives back a soft reflection of the speaker."""
    return {'kind': 'sweep', 'color': '#242424' if dark else '#D9D5CF', 'width': 24.0, 'front': 14.0, 'depth': 5.6,
            'radius': 5.0, 'height': 9.0, 'contact': {'strength': 0.35, 'distance_m': 0.08, 'core_strength': 0.7,
                                                      'core_distance_m': 0.008}}


def strips(level=1.0, recv=('*#0',)):
    """The strip lights: two tall panels behind and to each side, which the acrylic's side edges and faces mirror as
    long clean lines, and one long one overhead for the top's edge and the horn's lip."""
    return {
        'strip-left': {'type': 'panel', 'size_m': [0.15, 3.2], 'orbit': {'azimuth_deg': -77, 'elevation_deg': 8, 'distance_m': 2.2},
                       'target': [0.0, 0.0, 0.6], 'strength': 16.0 * level, 'diffuse': 0.15, 'specular': 1.0, 'receivers': list(recv),
                       'ramp': {'axis': 'z', 'at_m': [-0.4, 0.7, 2.2], 'values': [0.25, 1.0, 0.25]}},
        'strip-right': {'type': 'panel', 'size_m': [0.12, 3.2], 'orbit': {'azimuth_deg': 98, 'elevation_deg': 8, 'distance_m': 2.2},
                        'target': [0.0, 0.0, 0.6], 'strength': 50.0 * level, 'diffuse': 0.35, 'specular': 1.0, 'receivers': list(recv),
                        'ramp': {'axis': 'z', 'at_m': [-0.4, 0.7, 2.2], 'values': [0.25, 1.0, 0.25]}},
        'strip-top': {'type': 'panel', 'size_m': [2.4, 0.4], 'position': [-0.2, -1.0, 2.4], 'target': [0.0, 0.0, 1.2],
                      'strength': 18.0 * level, 'diffuse': 0.5, 'specular': 1.0, 'receivers': list(recv),
                      'ramp': {'axis': 'x', 'at_m': [-1.2, 0.0, 1.2], 'values': [0.1, 1.0, 0.1]}},
    }


def hero(name, dark=True):
    s = {'title': f'barkhorn, {name}, launch hero ({"dark" if dark else "light"})', 'size': [2560, 1440],
         'product': product(name, rotate=-36.0), 'set': seamless(dark),
         'camera': {'position': [0.0, -6.6, 0.95], 'target': [0.0, 0.0, 0.68], 'lens_mm': 60.0, 'level': True},
         'sky': {'kind': 'none'}, 'render': dict(RENDER), 'finish': dict(FINISH),
         'materials': {'sweep': {'roughness': 0.12, 'specular': 0.03}}}
    L = {
        # the key: a big softbox high and to the left of the camera, the faces' long gradient
        'key': {'type': 'area', 'size_m': [2.4, 1.6], 'orbit': {'azimuth_deg': -55, 'elevation_deg': 32, 'distance_m': 3.4},
                'target': [0.0, 0.0, 0.6], 'irradiance': 1.6 if dark else 1.5, 'color': '#FFF6EC', 'spread_deg': 70,
                'camera': False},
        # a low soft fill from the right, so the shadow side keeps its colour
        'fill': {'type': 'area', 'size_m': [2.0, 2.0], 'orbit': {'azimuth_deg': 60, 'elevation_deg': 18, 'distance_m': 4.0},
                 'target': [0.0, 0.0, 0.55], 'irradiance': 0.55 if dark else 0.7, 'color': '#F2F5FF', 'camera': False},
        # the glow: a lamp behind the speaker facing the wall, a pool of light that fades to the edges of the frame
        'glow': {'type': 'area', 'shape': 'DISK', 'size_m': [2.0, 2.0], 'position': [0.0, 0.45, 0.9],
                 'target': [0.0, 4.0, 1.5], 'spread_deg': 130, 'power_w': 300.0 if dark else 0.0, 'color': '#F6F2EC', 'camera': False,
                 'specular': 0.0},
        # a card high in front, seen only in reflections: a long soft sheen down the faces and into the horn's mouth
        'sheen': {'type': 'panel', 'size_m': [4.0, 2.4], 'position': [-0.9, -3.4, 2.5], 'target': [0.0, 0.0, 0.9],
                  'strength': 0.8, 'diffuse': 0.0, 'specular': 1.0, 'receivers': ['*#0'],
                  'ramp': {'axis': 'z', 'at_m': [1.4, 3.2], 'values': [0.05, 0.6]}},
        # a small card in front of the horn, so its mouth mirrors a graded light and not the dark set
        'horn-front': {'type': 'panel', 'size_m': [4.0, 2.6], 'position': [0.2, -2.8, 2.0], 'target': [0.0, 0.0, 1.18],
                       'strength': 0.2, 'diffuse': 0.0, 'specular': 1.0, 'receivers': ['*#0'],
                       'ramp': {'axis': 'z', 'at_m': [0.9, 3.2], 'values': [0.0, 1.0]}},
        'sheen-right': {'type': 'panel', 'size_m': [2.0, 1.2], 'position': [1.6, -2.6, 2.3], 'target': [0.0, 0.0, 0.7],
                        'strength': 3.0, 'diffuse': 0.0, 'specular': 1.0, 'receivers': ['*#0'],
                        'ramp': {'axis': 'z', 'at_m': [1.8, 2.9], 'values': [0.15, 1.0]}},
        # light through the horn from behind it, so its tinted walls glow rather than fall to black
        'horn-back': {'type': 'panel', 'size_m': [0.9, 0.3], 'position': [0.0, 0.9, 1.05], 'target': [0.0, 0.0, 1.1],
                      'strength': 8.0, 'diffuse': 1.0, 'specular': 0.0, 'receivers': ['*#0']},
        **strips(1.0 if dark else 0.7),
    }
    if not dark:
        # a pale room: a soft white dome, so the floor's gloss mirrors light and not a black void, and a broad wash on
        # the seamless, brightest behind the speaker and falling off to the sides
        s['sky'] = {'kind': 'gradient', 'zenith': '#E9E6E1', 'horizon': '#E4E0DA', 'ground': '#BDB8B0', 'strength': 1.0}
        L['wash'] = {'type': 'area', 'size_m': [6.0, 3.0], 'position': [0.0, -2.5, 4.2], 'target': [0.0, 3.0, 1.4],
                     'irradiance': 0.9, 'color': '#FFF8F0', 'camera': False, 'specular': 0.0}
    s['lights'] = L
    return s


# Round 31c: two concepts after seven passes held at 5.0 to 5.5 (the coordinator, on the plateau: change the concept,
# not the knobs). Both cover on (the product's own state: the cloth hides the woofer's dark cone) and both from the
# look book's three-quarter direction (camera about 26 degrees off the speaker's axis), the speaker about 62 % of the
# frame's height. Each is one of the classic ways glass and clear acrylic are photographed.
CAM34 = {'position': [2.85, -5.85, 0.75], 'target': [0.0, 0.0, 0.66], 'lens_mm': 70.0, 'level': True}


def covered(name):
    p = product(name)
    for i in p['instances']:
        i['hide'] = []
    return p


def bright(name):
    """Bright field on white (the iMac G3 and the Cube): the seamless lit high-key behind, so it shines through the tint
    and the colour glows like stained glass; black flags just outside the frame either side, which each vertical edge
    refracts as a crisp dark line; a big scrim overhead for the top; a white card low in front, so the horn's throat
    mirrors a gradient and not black."""
    # cover off: the duel against h7 (round 31c) read the cover's flat disc as a placeholder
    s = {'title': f'barkhorn, {name}, bright field', 'size': [2560, 1440], 'product': product(name),
         'set': {'kind': 'sweep', 'color': '#F3F1EE', 'width': 52.0, 'front': 20.0, 'depth': 6.0, 'radius': 5.0, 'height': 9.0,
                 'contact': {'strength': 0.8, 'distance_m': 0.7, 'core_strength': 0.9, 'core_distance_m': 0.08},
                 'flags': [{'center_m': [-1.4, 0.6, 1.2], 'size_m': [1.2, 1.4], 'normal': [1.0, -0.2, 0.0], 'glossy': False,
                            'off': True},   # its shadow on the cove read as a grey wedge in the corner (the finals),
                           {'center_m': [1.35, 2.1, 1.2], 'size_m': [0.3, 2.4], 'normal': [-0.45, -0.89, 0.0], 'glossy': True}],
                 'bounces': [{'center_m': [0.4, -2.2, 0.6], 'size_m': [2.0, 1.0], 'normal': [-0.15, 0.95, 0.1], 'reflect_only': True}]},
         'camera': dict(CAM34), 'sky': {'kind': 'gradient', 'zenith': '#F2F1EF', 'horizon': '#EEEDEB', 'ground': '#CFCCC8',
                                       'strength': 0.6, 'visible': False},
         'render': dict(RENDER, white_balance_k=5900, white_balance_tint=7.0), 'finish': dict(FINISH),
         'materials': {'sweep': {'roughness': 0.32}}}
    s['lights'] = {
        # the background: two broad lamps on the cove behind, out of frame, lifting it to a clean high-key white
        'bg-left': {'type': 'area', 'size_m': [4.0, 3.0], 'position': [-2.6, 3.2, 3.4], 'target': [-1.5, 6.0, 1.2],
                    'irradiance': 3.6, 'color': '#FFF4E8', 'camera': False, 'specular': 0.0},
        'bg-right': {'type': 'area', 'size_m': [4.0, 3.0], 'position': [2.6, 3.2, 3.4], 'target': [-0.9, 6.0, 1.0],
                     'irradiance': 3.6, 'color': '#FFF4E8', 'camera': False, 'specular': 0.0},
        # a big scrim overhead, a little forward: the top and the horn's crown
        'scrim': {'type': 'area', 'size_m': [2.0, 1.6], 'position': [0.1, 0.4, 2.8], 'target': [0.0, 0.0, 0.8],
                  'irradiance': 1.6, 'color': '#FFFAF4', 'camera': False},
        # a soft frontal key from the camera's side, low in strength: the faces carry their colour, not a white sheet
        'key': {'type': 'area', 'size_m': [1.2, 1.2], 'orbit': {'azimuth_deg': -30, 'elevation_deg': 38, 'distance_m': 4.5},
                'target': [0.0, 0.0, 0.6], 'irradiance': 4.0, 'color': '#FFFAF4', 'camera': False, 'specular': 1.0},
        # a graduated strip the front face mirrors, so it reads as polished cast acrylic
        'front-strip': {'type': 'panel', 'size_m': [0.4, 2.0], 'orbit': {'azimuth_deg': -25, 'elevation_deg': 22, 'distance_m': 3.0},
                        'target': [0.0, 0.0, 0.6], 'strength': 4.0, 'diffuse': 0.0, 'specular': 1.0, 'receivers': ['*#0'],
                        'ramp': {'axis': 'z', 'at_m': [0.2, 1.8], 'values': [0.0, 1.0]}},
        # a small lamp high behind, aimed through the cabinet at the floor in front: the tinted acrylic throws a pool of
        # its colour forward onto the seamless (the lineup's pass n1, and every hero pass, asked for it)
        'back-top': {'type': 'area', 'size_m': [0.8, 0.8], 'orbit': {'azimuth_deg': 200, 'elevation_deg': 30, 'distance_m': 2.5},
                     'target': [0.0, -0.5, 0.0], 'irradiance': 22.0, 'color': '#FFF8F0', 'camera': False},
    }
    return s


def bright2(name):
    """Round 31d, from the set's pass (6.5): the bright field with the speaker standing on the floor and drawn at every
    edge. The flags are seen only in reflections (no shadow on the cove: the left one's shadow was the grey wedge, so it
    is back), wider, and a third high behind the horn for the water-clear frame's outline; a denser, tighter contact; the
    background lamps aimed low, so the wall falls off about ten levels toward the top and the floor at the foot holds;
    more light through the cabinet for Smoke; about 15 % more headroom for type."""
    s = bright(name)
    st = s['set']
    st['contact'] = {'strength': 0.8, 'distance_m': 0.35, 'core_strength': 0.8, 'core_distance_m': 0.03}
    st['flags'] = [
        {'center_m': [-1.5, 0.6, 1.2], 'size_m': [1.4, 2.6], 'normal': [1.0, -0.2, 0.0], 'reflect_only': True},
        {'center_m': [1.35, 2.1, 1.2], 'size_m': [0.6, 2.6], 'normal': [-0.45, -0.89, 0.0], 'reflect_only': True},
        {'center_m': [0.0, 1.6, 2.2], 'size_m': [2.4, 0.8], 'normal': [0.0, -0.8, -0.6], 'reflect_only': True},
    ]
    L = s['lights']
    L['bg-left'].update(size_m=[6.0, 3.0], position=[-4.5, 3.2, 3.4], target=[-3.0, 6.0, 0.3], irradiance=1.8)
    L['bg-right'].update(size_m=[6.0, 3.0], target=[0.3, 6.0, 0.3], irradiance=1.8)
    s['sky']['strength'] = 0.22          # the dome lit the wall evenly to the top; less of it lets the wall fall off
    L['back-top']['irradiance'] = 30.0
    # a low soft bank behind lighting the speaker alone, so light passes through the black and the clear cabinets too
    L['back-low'] = {'type': 'area', 'size_m': [1.2, 0.8], 'orbit': {'azimuth_deg': 175, 'elevation_deg': 8, 'distance_m': 2.0},
                     'target': [0.0, 0.0, 0.45], 'irradiance': 30.0, 'color': '#FFF8F0', 'camera': False, 'receivers': ['*#0']}
    s['camera'] = dict(CAM34, lens_mm=60.0, target=[0.0, 0.0, 0.76])
    s['title'] = f'barkhorn, {name}, bright field (round 31d)'
    return s


def darkfield(name):
    """Dark field on black: no light on the faces; two tall strips behind at grazing angles, so only the edges and
    corners glow (cast acrylic pipes light to its edges); a soft backlight through the body for the colour, the inside
    falling to silhouette."""
    s = {'title': f'barkhorn, {name}, dark field', 'size': [2560, 1440], 'product': covered(name),
         'set': {'kind': 'sweep', 'color': '#0B0B0B', 'width': 24.0, 'front': 14.0, 'depth': 5.0, 'radius': 4.0, 'height': 9.0,
                 'contact': {'strength': 0.3, 'distance_m': 0.06, 'core_strength': 0.6, 'core_distance_m': 0.01}},
         'camera': dict(CAM34), 'sky': {'kind': 'none'},
         'render': dict(RENDER, white_balance_tint=0.0), 'finish': dict(FINISH),
         'materials': {'sweep': {'roughness': 0.15, 'specular': 0.05}}}
    recv = ['*#0']
    s['lights'] = {
        'edge-left': {'type': 'panel', 'size_m': [0.3, 3.2], 'orbit': {'azimuth_deg': -150, 'elevation_deg': 10, 'distance_m': 1.8},
                      'target': [0.0, 0.0, 0.62], 'strength': 30.0, 'diffuse': 1.0, 'specular': 1.0, 'receivers': recv},
        'edge-right': {'type': 'panel', 'size_m': [0.3, 3.2], 'orbit': {'azimuth_deg': 160, 'elevation_deg': 10, 'distance_m': 1.8},
                       'target': [0.0, 0.0, 0.62], 'strength': 30.0, 'diffuse': 1.0, 'specular': 1.0, 'receivers': recv},
        # the backlight: a soft bank right behind the speaker, facing the camera, lighting it alone
        'through': {'type': 'panel', 'size_m': [1.0, 0.9], 'position': [-0.35, 0.9, 0.45], 'target': [0.4, -1.0, 0.45],
                    'strength': 4.0, 'diffuse': 1.0, 'specular': 0.0, 'receivers': recv},
        # a faint glow on the cove behind, so the black has depth
        'glow': {'type': 'area', 'shape': 'DISK', 'size_m': [2.0, 2.0], 'position': [0.0, 0.5, 0.9], 'target': [0.0, 5.0, 1.4],
                 'spread_deg': 120, 'power_w': 140.0, 'color': '#F6F2EC', 'camera': False, 'specular': 0.0},
    }
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


def macro_bright(key, name, rotate, cam, target, lens):
    """A detail in the bright-field studio (round 31c): the hero's light, the camera close."""
    s = bright(name)
    s['title'] = f'barkhorn, {name}, detail: {key} (bright field)'
    s['size'] = [1600, 1600]
    s['product'] = product(name, rotate=rotate)
    s['camera'] = {'position': cam, 'target': target, 'lens_mm': lens, 'level': False}
    # the finals' passes (5.0 to 5.5): each detail reframed on its subject and lit for it
    for path, value in MACRO_FIX.get(key, {}).items():
        d, keys = s, path.split('.')
        for k in keys[:-1]:
            d = d[int(k)] if isinstance(d, list) else d.setdefault(k, {})
        if isinstance(d, list):
            i = int(keys[-1])
            d[i:i + 1] = [value]          # past the end appends (a new flag)
        else:
            d[keys[-1]] = value
    return s


# per detail, by dotted path: what the macro passes asked for (critic/reply-m-*.json)
MACRO_FIX = {
    # turned so the cap and the mouth's rolled lip both face the camera, the cabinet mostly out of frame; the bell's top
    # given a dark edge by a flag overhead; the right flag matte (its glint was a square chip in the throat)
    'horn': {'product.instances.0.rotate_z': 80.0, 'camera.position': [1.0, -2.3, 1.45], 'camera.target': [0.05, 0.02, 1.08],
             'camera.lens_mm': 125.0, 'lights.scrim.irradiance': 0.6, 'set.flags.1.glossy': False,
             'set.flags.2': {'center_m': [0.0, 0.0, 2.3], 'size_m': [1.6, 0.6], 'normal': [0.0, 0.0, -1.0], 'glossy': True}},
}


def lineup_bright():
    """The eight in a row in the bright-field studio: the hero's light stretched along the row, the flags and the
    background lamps moved out to its ends."""
    s = bright('ember')
    s['title'] = 'barkhorn, the eight Clouds in a row (bright field)'
    s['size'] = [2880, 1200]
    xs = [(i - 3.5) * GAP for i in range(8)]
    s['product'] = {'def': PRODUCT, 'flavour': COLOURS[0][1],
                    'instances': [{'position': [x, 0, 0], 'rotate_z': -24.0, 'flavour': fl, 'hide': ['cloth-disc']}
                                  for x, (n, fl) in zip(xs, COLOURS)]}
    s['camera'] = {'position': [0.0, -14.0, 0.85], 'target': [0.0, 0.0, 0.6], 'lens_mm': 58.0, 'level': True}
    st = s['set']
    st['flags'] = []
    # cards seen only in reflections (no shadow: the first, as a plain card, laid a grey band on the floor), the second
    # high in front for the horns' shoulders (the black one crushed to zero without it)
    st['bounces'] = [{'center_m': [0.0, -2.6, 0.6], 'size_m': [9.0, 1.0], 'normal': [0.0, 0.95, 0.15], 'reflect_only': True},
                     {'center_m': [0.0, -1.6, 2.6], 'size_m': [9.0, 1.4], 'normal': [0.0, 0.55, -0.83], 'reflect_only': True}]
    st.update(radius=9.0, depth=11.0, contact={'strength': 0.8, 'distance_m': 0.45, 'core_strength': 1.0, 'core_distance_m': 0.03})
    s['materials'] = {'sweep': {'roughness': 0.32}}
    recv = [f'*#{i}' for i in range(8)]
    L = s['lights']
    L['bg-left'].update(size_m=[8.0, 3.0], position=[-4.5, 3.2, 3.4], target=[-3.0, 6.0, 0.4])
    L['bg-right'].update(size_m=[8.0, 3.0], position=[4.5, 3.2, 3.4], target=[3.0, 6.0, 0.4])
    L['scrim'].update(size_m=[9.0, 1.6], position=[0.0, 0.4, 2.8])
    L['key'].update(size_m=[6.0, 1.6], orbit=None, position=[-1.6, -3.4, 3.0], target=[0.0, 0.0, 0.6])
    L['key'].pop('orbit')
    L['back-top'].update(size_m=[9.0, 1.2], orbit=None, position=[0.0, 3.0, 2.0], target=[0.0, -0.6, 0.0], irradiance=16.0)
    L['back-top'].pop('orbit')
    L['front-strip'].update(size_m=[9.0, 0.5], orbit=None, position=[0.0, -3.0, 1.9], target=[0.0, 0.0, 0.6], receivers=recv,
                            ramp={'axis': 'z', 'at_m': [1.65, 2.15], 'values': [0.0, 1.0]})
    L['front-strip'].pop('orbit')
    return s


def main():
    os.makedirs(OUT, exist_ok=True)
    made = {}
    for name, _ in COLOURS:
        made[f'hero-dark-{name}'] = hero(name, True)
    # round 31c: the studio set is bright field (it won its duel); the dark set stays as h7's record, unrendered
    for name, _ in COLOURS:
        made[f'hero-light-{name}'] = bright2(name)
    made['lineup'] = lineup_bright()
    for name in ('ember', 'ice', 'smoke'):
        made[f'concept-bright-{name}'] = bright(name)
        made[f'concept-darkfield-{name}'] = darkfield(name)
    for m in MACROS:
        made[f'macro-{m[0]}-{m[1]}'] = macro_bright(*m)
    for n, sh in made.items():
        json.dump(sh, open(os.path.join(OUT, n + '.json'), 'w'), indent=1)
    print(len(made), 'shots in', os.path.relpath(OUT, ROOT))


if __name__ == '__main__':
    main()
