"""The catalogue views relit (round 31): the front of each of the eight colours, cover on and off, as promotional
images for a $20,000 pair. One rig for all sixteen, written here; the colours differ only where the colour needs it
(the sweep's tint, a fraction of a stop). Notes and critic passes: catalogue31.md.

    python3 spinoffs/barkhorn/catalogue31.py            writes studio/shots/barkhorn/lookbook31/look-{k}-{on,off}.json
    python3 spinoffs/barkhorn/catalogue31.py stage IMG --tag T --shot SHOT --stage DIR
                                                        a blind critic pass: the image, its card, the measuring tool and
                                                        the prompt (critic/PROMPT-promo.md, between its rules), staged
    python3 spinoffs/barkhorn/catalogue31.py save REPLY --tag T
                                                        the critic's reply kept with the set's rounds

The rig, as a product photographer would set it (camera at azimuth +26 degrees, the speaker's front toward -y):
- key: one large softbox camera-left, high, feathered across the front, so the cover and the lining fall off left to
  right and the side panel sits about a stop under the front;
- front scrim: a graduated panel the front's acrylic mirrors (it looks front-left and up), bright at the top, so the
  20 mm sheet shows as a sheet of glass without hiding the lining behind it;
- side flag: a black card behind and right, the side panel's mirror, so the side reads a deep clean colour, with a
  strip light in front of it whose line lands on the near vertical edge; a strip over the horn for its rim;
- horn fill: a gridded light just over the lens into the horn's mouth, so the throat holds shape;
- sweep: lit on its own (lamps that light only the paper), a glow behind the horn falling off to the top and sides;
- a dark studio (the world near black), so every light on the product is one of these; fine grain in post.
"""
import argparse, copy, json, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'lookbook31')

# the colours by key (finals.py's keys), their flavour and an exposure trim (EV); one paper for all eight (PAPER)
COLOURS = {
    'red':    dict(flavour='cloud-red',            ev=0.0),
    'orange': dict(flavour='cloud-orange',         ev=0.0),
    'amber':  dict(flavour='cloud-amber',          ev=0.0),
    'green':  dict(flavour='eucalyptus-y2k-green', ev=0.0),
    'blue':   dict(flavour='cloud-blue',           ev=0.0),
    'violet': dict(flavour='cloud-violet',         ev=0.0),
    'ice':    dict(flavour='birch-fog-clear',      ev=-0.6),
    'black':  dict(flavour='cloud-black',          ev=0.0),
}

# the lamps that draw lines (edge, rim) light only these, so the paper's gloss never mirrors them
CABINET = ['right', 'left', 'front-panel', 'top', 'bottom', 'back']
# the whole speaker, for a lamp that must light it and not the paper (no second shadow on the sweep)
SPEAKER = CABINET + ['lining-*', 'rib-*', 'brace*', 'land-*', 'waveguide*', 'hf-*', 'grip-*', 'post*', 'port*', 'woofer*',
                     'cloth-disc', 'amp*', 'feet*', 'tie-rod*', 'top-pad', 'cap-o-ring', 'cable-glands', 'lead-*', 'mark-back',
                     'rating-plate*', 'back-*']
# the speaker less its lining: the lamps through and beside it, so the white batts are not the brightest thing on it
SHELL = [p for p in SPEAKER if p != 'lining-*']
HORN = ['waveguide', 'waveguide-cap']

RIG = {
    'size': [1080, 2160],
    'camera': {'position': [1.2, -2.5, 1.0], 'target': [0.0, 0.05, 0.52], 'lens_mm': 90.0, 'level': True,
               'shift_x': -0.0245, 'shift_y': -0.015,
               'fstop': 6.3, 'focus': [0.28, -0.21, 0.6]},
    'sky': {'kind': 'gradient', 'zenith': '#2B2A28', 'horizon': '#2F2D2B', 'ground': '#1B1A19', 'strength': 0.15},
    'set': {'kind': 'sweep', 'width': 18.0, 'front': 5.0, 'depth': 5.5, 'radius': 2.8, 'height': 5.5,
            'contact': {'strength': 0.9, 'distance_m': 0.32, 'core_strength': 0.95, 'core_distance_m': 0.015},
            'flags': [
                # the side panel's mirror (it looks behind-right and down, azimuth 158 to 161): black on the floor
                # there and standing behind it, seen only in reflections, so the side reads a deep clean colour
                {'center_m': [1.6, 1.8, 0.005], 'size_m': [1.6, 2.4], 'normal': [0.0, 0.0, 1.0], 'reflect_only': True,
                 'color': '#060606'},
                {'center_m': [1.8, 2.7, 1.3], 'size_m': [3.0, 2.6], 'normal': [-0.37, -0.93, 0.0], 'reflect_only': True,
                 'color': '#060606'},
                {'center_m': [1.6, -1.2, 1.2], 'size_m': [2.0, 2.0], 'normal': [-0.8, 0.6, 0.0], 'reflect_only': True,
                 'color': '#060606'},
                # the horn's top mirrors up and toward the camera: a black card overhead
                {'center_m': [0.0, -0.6, 2.6], 'size_m': [2.5, 2.0], 'normal': [0.0, 0.3, -1.0], 'reflect_only': True,
                 'color': '#080808'},
            ]},
    'lights': {
        'key': {'type': 'area', 'size_m': [1.8, 2.2], 'orbit': {'azimuth_deg': -35, 'elevation_deg': 22, 'distance_m': 1.5},
                'target': [-0.55, 0.0, 0.9], 'irradiance': 5.2, 'color': '#FFF5E8', 'spread_deg': 50},
        'fill': {'type': 'area', 'size_m': [2.0, 2.0], 'orbit': {'azimuth_deg': 40, 'elevation_deg': 15, 'distance_m': 4.0},
                 'target': [0.0, 0.0, 0.6], 'irradiance': 1.1, 'color': '#FFF2E6', 'specular': 0.3},
        # through-light: a softbox behind the speaker, so the light that sells tinted acrylic, the light through it,
        # is in the picture: a rim on every edge, the horn's resin lit from behind; linked to the speaker, since the
        # paper's gloss drew it as a streak beside the cabinet
        'back': {'type': 'area', 'size_m': [1.2, 1.0], 'orbit': {'azimuth_deg': 180, 'elevation_deg': 20, 'distance_m': 2.0},
                 'target': [0.0, -0.3, 0.3], 'irradiance': 2.4, 'color': '#FFF8F0',
                 'receivers': SHELL},
        # the same light on the paper alone, diffuse only (so its gloss draws no streak): what crosses the tinted
        # acrylic lands on the floor in front of the base, coloured
        'pool': {'type': 'area', 'size_m': [1.2, 1.0], 'orbit': {'azimuth_deg': 160, 'elevation_deg': 35, 'distance_m': 2.0},
                 'target': [0.1, -0.4, 0.0], 'irradiance': 1.0, 'color': '#FFF8F0', 'specular': 0.0, 'receivers': ['sweep']},
        # the camera-side face lit through: a kicker on the speaker alone
        'kick': {'type': 'area', 'size_m': [1.2, 1.8], 'orbit': {'azimuth_deg': 100, 'elevation_deg': 20, 'distance_m': 1.8},
                 'target': [0.28, 0.0, 0.6], 'irradiance': 2.0, 'color': '#FFF8F0', 'receivers': SHELL},
        # the front's acrylic mirrors the floor front-left (azimuth -27, 4 to 20 degrees down): a graduated card
        # lying there, seen only in reflections, a soft sheen up the lower front
        'scrim': {'type': 'panel', 'size_m': [1.6, 3.0], 'position': [-0.75, -2.2, 0.004], 'target': [-0.75, -2.0, 2.0],
                  'strength': 0.9, 'color': '#FFFFFF', 'diffuse': 0.0,
                  'ramp': {'axis': 'y', 'at_m': [-3.6, -1.6], 'values': [1.0, 0.25]}},
        # a long soft sheen down the front's acrylic, so it reads as a glossy slab and not a tinted outline
        'sheen': {'type': 'panel', 'size_m': [0.4, 2.0], 'position': [-1.4, -1.6, 0.6], 'target': [0.0, 0.0, 0.5],
                  'strength': 0.6, 'color': '#FFFFFF', 'diffuse': 0.0,
                  'ramp': {'axis': 'z', 'at_m': [-0.4, 1.6], 'values': [1.0, 0.2]}},
        # the top's 20 mm edge mirrors front-left, level: a white card far off, a crisp line along the top
        'topline': {'type': 'panel', 'size_m': [1.8, 0.5], 'position': [-1.0, -2.1, 0.95], 'target': [0.0, -0.1, 0.9],
                    'strength': 1.8, 'color': '#FFFFFF', 'diffuse': 0.0},
        # a faint graduated sheen in front of the side's black flag: a clear colour keeps its deep side, a smoked one
        # shows a surface instead of a black slab
        'sidesheen': {'type': 'panel', 'size_m': [0.8, 2.0], 'position': [1.1, 2.3, 0.6], 'target': [0.28, 0.0, 0.5],
                      'strength': 0.6, 'color': '#FFFFFF', 'diffuse': 0.0,
                      'ramp': {'axis': 'z', 'at_m': [-0.4, 1.6], 'values': [0.15, 1.0]}},
        # a 1 cm strip standing in the plane the near vertical edge mirrors (through the camera's mirror image and that
        # edge), so its reflection is a line on the edge at every height
        'edge': {'type': 'area', 'size_m': [0.06, 1.2], 'position': [0.42, 0.135, 0.6], 'target': [0.28, -0.21, 0.6],
                 'power_w': 0.2, 'color': '#FFFFFF', 'diffuse': 0.0, 'receivers': CABINET},
        # the horn's upper rim mirrors up and toward the camera
        'rim': {'type': 'area', 'size_m': [1.4, 0.3], 'position': [0.3, -0.5, 2.0], 'target': [0.05, 0.0, 1.2],
                'power_w': 12, 'color': '#FFFFFF', 'diffuse': 0.1, 'receivers': HORN},
        'horn': {'type': 'area', 'size_m': [1.4, 0.7], 'position': [0.8, -1.4, 1.35],
                 'target': [0.05, 0.0, 1.12], 'irradiance': 2.6, 'color': '#FFF8F0', 'spread_deg': 40, 'specular': 1.0},
        'paper': {'type': 'area', 'size_m': [0.5, 0.5], 'position': [-0.35, 0.75, 0.5], 'target': [-0.8, 2.4, 2.4],
                  'power_w': 210, 'color': '#FFF0E2', 'receivers': ['sweep'], 'spread_deg': 140},
        # the paper on the key side, so it falls off gently and does not go grey
        'wall': {'type': 'area', 'size_m': [4.0, 2.0], 'position': [-1.5, 1.0, 3.5], 'target': [-1.2, 5.0, 2.6],
                 'irradiance': 1.8, 'color': '#FFF0E2', 'receivers': ['sweep']},
        'wash': {'type': 'area', 'size_m': [4.0, 1.5], 'position': [0.4, -1.4, 3.0], 'target': [0.0, -0.4, 0.0],
                 'irradiance': 0.5, 'color': '#FFF0E2', 'receivers': ['sweep']},
    },
    'render': {'samples': 256, 'adaptive': 0.01, 'denoise': True, 'clamp': 8, 'bounces': 32,
               'glossy_bounces': 16, 'transmission_bounces': 32, 'view': 'Khronos PBR Neutral', 'exposure': 0.0,
               'white_balance_k': 5600, 'white_balance_tint': 3.0},
    'finish': {'enabled': True, 'white_in': 236, 'white_out': 236, 'contrast': 0.2, 'clarity': 0.05,
               'sharpen': 0.3, 'sharpen_px': 0.7, 'grain': 1.5, 'grain_px': 1.0},
}


# The paper (the coordinator, after a full-site critic pass: four studio looks across the product pictures, and the home
# cards, which take their panel colour from these frames' foot, reading a dingy grey): the studio's warm pale paper of
# round 31c's bright field, one neutral backdrop for all eight (no tint per colour), lit high-key by lamps that light
# the paper alone (the speaker's own light is the rig's, as it won), to about #F2EFEA at the feet and #EDE9E3 on the wall
# with no more than about ten levels to the corners. Smoke and Fog part from the pale ground by the rig's own black
# cards, which the side and the edges mirror (31c's tall dark strip was tried: its shadow drew a streak on the cove).
PAPER = {
    'color': '#F7F0E8',
    'flags': [],
    'lights': {
        'bg-left': {'type': 'area', 'size_m': [4.0, 3.0], 'position': [-2.6, 3.2, 3.4], 'target': [-1.5, 6.0, 1.2],
                    'irradiance': 0.7, 'color': '#FFF4E8', 'specular': 0.0, 'receivers': ['sweep']},
        'bg-right': {'type': 'area', 'size_m': [4.0, 3.0], 'position': [2.6, 3.2, 3.4], 'target': [-0.9, 6.0, 1.0],
                     'irradiance': 1.1, 'color': '#FFF4E8', 'specular': 0.0, 'receivers': ['sweep']},
        # the cove's far left and its upper wall, which every frame sees past the speaker's key side
        'wall_left': {'type': 'area', 'size_m': [10.0, 5.0], 'position': [-6.0, 0.5, 5.5], 'target': [-8.0, 5.5, 4.7],
                      'irradiance': 4.5, 'color': '#FFF0E2', 'specular': 0.0, 'receivers': ['sweep']},
        'bg-high': {'type': 'area', 'size_m': [6.0, 3.0], 'position': [0.0, 1.0, 6.5], 'target': [-1.5, 5.5, 5.0],
                    'irradiance': 0.2, 'color': '#FFF4E8', 'specular': 0.0, 'receivers': ['sweep']},
        'floor': {'type': 'area', 'size_m': [6.0, 4.0], 'position': [0.0, -2.0, 4.5], 'target': [0.0, 0.5, 0.0],
                  'irradiance': 0.7, 'spread_deg': 50, 'color': '#FFF4E8', 'specular': 0.0, 'receivers': ['sweep']},
    },
    # the tinted look's paper lamps, retuned for the pale paper: the glow behind and the key side's wall are off (they
    # drove the wall past white), the floor's wash a little down
    'tune': {'paper': {'power_w': 0.0}, 'wall': {'irradiance': 0.0}, 'wash': {'irradiance': 0.5}},
}


def shot(k, cover):
    c = COLOURS[k]
    s = copy.deepcopy(RIG)
    inst = {'position': [0, 0, 0], 'rotate_z': 0, 'flavour': c['flavour']}
    if not cover:
        inst['hide'] = ['cloth-disc']
    s['product'] = {'def': 'studio/products/barkhorn-cloud.json', 'flavour': c['flavour'], 'instances': [inst]}
    s['set']['color'] = PAPER['color']
    s['set']['flags'] += copy.deepcopy(PAPER['flags'])
    s['lights'].update(copy.deepcopy(PAPER['lights']))
    for n, kv in PAPER['tune'].items():
        s['lights'][n].update(kv)
    s['render']['exposure'] = c['ev']
    s['title'] = f'barkhorn, cover {"on" if cover else "off"} (catalogue31, {k})'
    return s


# the gallery's other stages (the owner, round 31: the 1:2 fronts "feel odd and out of place" beside the 3:2 and 4:5
# pictures): the same rig and the same light from the same camera position (so the same perspective), reframed by lens
# and lens shift only. The engine fits the sensor's 36 mm to the frame's width, so a frame of another height-to-width
# ratio needs the lens scaled to hold the speaker at its share of the height; each was then centred by its box in the
# frame (render.py's parts_2d): the 1:2 at 65 % of the height (16/17 % margins left and right, 24 % above, 11 % below);
# the 3:2 at 70 % of the height and 24 % of the width, centred (38 % each side, 15 % above and below); the 4:5 at 70 %
# of the height, centred across, a little low (16 % above, 14 % below), for phones
FRAMES = {
    '': {'size': [1080, 2160]},
    # the 3:2 sees far more of the set: the sweep wider and taller (its end showed at 18 m), and the paper on the key
    # side, which only it sees, lifted by a lamp of its own (it read as a dirty grey third of the frame)
    'wide': {'size': [1920, 1280], 'lens_mm': 32.3, 'shift_x': -0.011, 'shift_y': 0.025,
             'set': {'width': 40.0, 'height': 9.0},
             'lights': {'wall_far': {'type': 'area', 'size_m': [8.0, 4.0], 'position': [-8.0, 0.5, 6.0],
                                     'target': [-11.5, 5.5, 5.5], 'irradiance': 3.0, 'color': '#FFF0E2',
                                     'specular': 0.0, 'receivers': ['sweep']},
                        # and the foot of the cove's curve far to the left, at the frame's edge (a grey dip to 205)
                        'cove_far': {'type': 'area', 'size_m': [6.0, 3.0], 'position': [-6.0, 0.0, 3.0],
                                     'target': [-8.6, 4.0, 0.7], 'irradiance': 4.5, 'color': '#FFF0E2',
                                     'specular': 0.0, 'receivers': ['sweep']}}},
    'tall': {'size': [1440, 1800], 'lens_mm': 60.5, 'shift_x': -0.027, 'shift_y': 0.012},
}


def framed(s, f):
    """Shot s reframed for the frame `f` ('' the 1:2, 'wide' 3:2, 'tall' 4:5)."""
    F = FRAMES[f]
    s = copy.deepcopy(s)
    s['size'] = list(F['size'])
    for key in ('lens_mm', 'shift_x', 'shift_y'):
        if key in F:
            s['camera'][key] = F[key]
    s['set'].update(copy.deepcopy(F.get('set', {})))
    s['lights'].update(copy.deepcopy(F.get('lights', {})))
    # a colour's exposure trim (Fog's -0.6 EV, for its white cloth) is the speaker's, not the paper's: the paper's lamps
    # make it good, so every colour stands on the same paper
    ev = s['render'].get('exposure', 0.0)
    for l in s['lights'].values():
        if l.get('receivers') == ['sweep'] and ev:
            for key in ('irradiance', 'power_w'):
                if key in l:
                    l[key] = round(l[key] * 2 ** -ev, 4)
    if f:
        s['title'] = s['title'].replace('(catalogue31,', f'(catalogue31 {f},')
    return s


# The detail views (finals.py's horn-side, horn-back, back, amp and inside) on the same paper (the coordinator: every
# product picture in one studio look): each from its own template, its camera and its light as they were tuned, the
# paper set under it and lit by two lamps on the paper alone (the cove's wall and its floor), their strength set per
# view (their cameras see the cove differently) to the catalogue's paper: about 240 at the floor, 236 on the wall.
DETAILS = {'horn-side': 'horn21/horn-{k}-side.json', 'horn-back': 'horn21/horn-{k}-back.json',
           'back': 'site30/back-{k}.json', 'amp': 'site30/detail-{k}.json', 'inside': 'site30/inside.json'}
DETAILS_OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'details31')
DETAIL_PAPER = {
    'd-wall': {'type': 'area', 'size_m': [4.0, 2.0], 'position': [0.0, -0.8, 3.2], 'target': [0.0, 1.5, 1.4],
               'irradiance': 1.0, 'color': '#FFF4E8', 'specular': 0.0, 'receivers': ['sweep']},
    'd-floor': {'type': 'area', 'size_m': [4.0, 3.0], 'position': [0.0, -1.8, 3.5], 'target': [0.0, -0.5, 0.0],
                'irradiance': 1.0, 'spread_deg': 60, 'color': '#FFF4E8', 'specular': 0.0, 'receivers': ['sweep']},
}
DETAIL_GAIN = {'horn-side': {'d-wall': 0.35, 'd-floor': 0.15}, 'horn-back': {'d-wall': 0.35, 'd-floor': 0.15},
               'back': {'d-wall': 0.35, 'd-floor': 0.15}, 'amp': {'d-wall': 0.35, 'd-floor': 0.15},
               'inside': {'d-wall': 0.35, 'd-floor': 0.15}}


def detail(view, k):
    """Detail view `view` of colour k on the paper."""
    s = json.load(open(os.path.join(ROOT, 'studio', 'shots', 'barkhorn', DETAILS[view].format(k=k))))
    fl = COLOURS[k]['flavour']
    s['product']['flavour'] = fl                                   # the cutaway's template is one colour's
    for inst in s['product'].get('instances', []):
        inst['flavour'] = fl
    s['set']['color'] = PAPER['color']
    for n, l in DETAIL_PAPER.items():
        l = copy.deepcopy(l)
        l['irradiance'] = round(l['irradiance'] * DETAIL_GAIN[view][n], 4)
        s['lights'][n] = l
    s['title'] = f'barkhorn, {view} (details31, {k}, on the paper)'
    return s


NAMES = {'red': 'Ember (red)', 'orange': 'Dust (orange)', 'amber': 'Acid (golden yellow)', 'green': 'Poison (bottle green)',
         'blue': 'Ice (a translucent blue)', 'violet': 'Haze (violet)', 'ice': 'Fog (water-clear)', 'black': 'Smoke (smoked black)'}
ROUNDS = os.path.join(HERE, 'critic', 'rounds', '2026-10-18')


def _lamp(n, l):
    where = (f"position {l['position']}" if 'position' in l else
             f"orbit az {l['orbit']['azimuth_deg']} el {l['orbit']['elevation_deg']} at {l['orbit']['distance_m']} m")
    size = l.get('size_m')
    power = (f"irradiance {l['irradiance']} W/m2 at its target" if 'irradiance' in l else
             f"power {l['power_w']} W" if 'power_w' in l else f"peak radiance {l.get('strength')}")
    extra = []
    for k in ('spread_deg', 'diffuse', 'specular', 'receivers', 'ramp', 'shape', 'color'):
        if k in l:
            extra.append(f'{k} {l[k]}')
    return f"- lights.{n}: {l['type']} {size} m, {where}, aimed at {l.get('target')}, {power}; " + ', '.join(extra)


def card(sh, k, cover):
    """The critic's card: what the frame is for, what is fixed, what may change, and the settings as they stand."""
    L = [f'# Card', '',
         f"What it is for: a catalogue view of one colour, {NAMES[k]}, for a brand's site: the colour cards (cropped narrow "
         'and tall), the first picture in that colour\'s gallery and the look book. The speaker three-quarter from the front, '
         + ('cover on (a cloth disc over the woofer)' if cover else 'cover off (the woofer shows)') +
         ', on a paper sweep tinted to suit its colour, in a 1080 x 2160 frame. Seven sister images show the other colours '
         '(Ember red, Dust orange, Acid golden yellow, Poison bottle green, Ice blue, Haze violet, Fog water-clear, Smoke '
         'smoked black) with the same rig, so framing and light stay one set: a change must suit all eight.', '',
         'Fixed (never yours to change): the speaker itself, its shape, colour, materials and parts: a 1293 mm tall horn '
         'loudspeaker, a cabinet of 20 mm tinted cast acrylic, lined inside with white polyester batts in voile sleeves '
         'between the ribs, under a horn of tinted resin with a black compression driver at its throat; sold at about '
         '$20,000 a pair. The cover\'s cloth and the lining\'s shaders are being reworked elsewhere: name problems there '
         'under out_of_scope.', '',
         'May change: the sweep (colour, size, curve), the light (direction, size, number, power, colour, flags and '
         'reflectors), the camera (framing, lens, height) and the finish (post). Lengths in metres; the speaker stands on '
         'the origin, its front toward -y, z up; the cabinet is about 0.56 m wide (x), 0.43 m deep (y) and 0.9 m tall, '
         'the horn above it to 1.29 m. The dark mass at the horn\'s throat is the tinted resin\'s own depth (it is '
         'thickest there; hiding the driver leaves it as dark), so it is fixed. Azimuth is measured from the front (-y), positive toward +x (camera side).', '',
         '## Settings', '',
         f"- camera: position {sh['camera']['position']}, target {sh['camera']['target']}, lens {sh['camera']['lens_mm']} mm, "
         f"level (verticals vertical), shift_x {sh['camera']['shift_x']}, shift_y {sh['camera']['shift_y']} (in units of the "
         f"frame's long side), f/{sh['camera'].get('fstop', 0)} focused at {sh['camera'].get('focus')}",
         f"- set: sweep, colour {sh['set']['color']}, width {sh['set']['width']}, floor to the curve "
         f"{sh['set']['depth'] - sh['set']['radius']} m behind the speaker, curve radius {sh['set']['radius']}, contact "
         f"shadow {sh['set']['contact']}",
         f"- sky (the studio's ambient, seen nowhere): {sh['sky']['zenith']} at strength {sh['sky']['strength']}"]
    for i, f in enumerate(sh['set'].get('flags', [])):
        L.append(f"- set.flags.{i}: black card {f['size_m']} m at {f['center_m']} facing {f['normal']}, seen only in "
                 'reflections (no shadow)')
    for n, l in sh['lights'].items():
        L.append(_lamp(n, l))
    R = sh['render']
    L += [f"- render: {R['samples']} samples (proofs at half size), bounces {R['bounces']} (glossy {R['glossy_bounces']}, "
          f"transmission {R['transmission_bounces']}), clamp {R['clamp']}, view {R['view']}, exposure {R['exposure']} EV, "
          f"white balance {R['white_balance_k']} K",
          f"- finish (post): {json.dumps(sh['finish'])} (grain in sRGB levels)", '',
          'Lamps never show to the camera; a panel is an emissive card seen only in reflections (or lighting at its '
          '`diffuse` share). `receivers` limits a lamp to those parts (light linking).']
    return '\n'.join(L) + '\n'


def prompt_text():
    t = open(os.path.join(ROOT, 'critic', 'PROMPT-promo.md')).read()
    return t.split('\n---\n')[1].strip() + '\n'


def stage(a):
    d = os.path.abspath(a.stage); os.makedirs(d, exist_ok=True)
    sh = json.load(open(a.shot))
    k = next(k for k, c in COLOURS.items() if c['flavour'] == sh['product']['flavour'])
    cover = 'cloth-disc' not in json.dumps(sh['product'])
    img, cd, tool = (os.path.join(d, f'render-{a.tag}.png'), os.path.join(d, f'card-{a.tag}.md'),
                     os.path.join(d, 'measure.py'))
    shutil.copy(a.img, img); open(cd, 'w').write(card(sh, k, cover)); shutil.copy(os.path.join(ROOT, 'critic', 'measure.py'), tool)
    pr = os.path.join(d, 'PROMPT.txt'); open(pr, 'w').write(prompt_text())
    print(json.dumps({'image': img, 'card': cd, 'tool': f'python3.11 {tool}', 'prompt': pr}, indent=1))


def save(a):
    os.makedirs(ROUNDS, exist_ok=True)
    txt = open(a.reply).read()
    j = json.loads(txt[txt.index('{'):txt.rindex('}') + 1])
    out = os.path.join(ROUNDS, f'catalogue31-{a.tag}.json')
    json.dump(j, open(out, 'w'), indent=1)
    print(os.path.relpath(out, ROOT), 'score', j['stage1']['score'], j['verdict'])


def write():
    os.makedirs(OUT, exist_ok=True)
    for k in COLOURS:
        for cover in (True, False):
            for f in FRAMES:
                name = f'look-{k}-{"on" if cover else "off"}' + (f'-{f}' if f else '') + '.json'
                json.dump(framed(shot(k, cover), f), open(os.path.join(OUT, name), 'w'), indent=1)
    print(f'{len(COLOURS) * 2 * len(FRAMES)} shots in', os.path.relpath(OUT, ROOT))
    os.makedirs(DETAILS_OUT, exist_ok=True)
    for k in COLOURS:
        for view in DETAILS:
            json.dump(detail(view, k), open(os.path.join(DETAILS_OUT, f'{view}-{k}.json'), 'w'), indent=1)
    print(f'{len(COLOURS) * len(DETAILS)} shots in', os.path.relpath(DETAILS_OUT, ROOT))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what', nargs='?', default='write', choices=['write', 'stage', 'save'])
    ap.add_argument('path', nargs='?')
    ap.add_argument('--tag'); ap.add_argument('--shot'); ap.add_argument('--stage')
    a = ap.parse_args()
    if a.what == 'stage':
        a.img = a.path; stage(a)
    elif a.what == 'save':
        a.reply = a.path; save(a)
    else:
        write()


if __name__ == '__main__':
    main()
