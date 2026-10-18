"""Round 31's uplit pictures: the speakers standing on lights at night, a metre in front of a board-formed concrete wall,
their colours laid up the wall above them (the owner, after the carousel: "Could be cool to see what the speakers look
like with a light placed under them. Imagine the outside wall of a cement opera house, like the one in Chicago on the
river, where the speakers are placed on lights casting upwards on the building at night, casting their color upwards
on the wall, blending light together").

- uplit-<colour>: the site's flip-through viewer's slides, one per colour, 1600 x 1600. One camera, one lamp, one set;
  only the speaker's colour changes from slide to slide.
- facade, facade-portrait: the night hero, the eight in a row at the foot of a monumental concrete wall by a river, each on its
  own uplight, their washes rising and blending; 2880 x 1200 and 4:5.
- study-<placement>-<colour>: where the lamp goes. The cabinet is lined with white batts in voile sleeves, and the
  engine's batting stops light, as the real batts do; so a lamp straight under the speaker lights its own lining and
  little else. The study renders three placements (under, in front, grazing up the face) for the slides' choice.

    python3 spinoffs/barkhorn/uplight31.py               ->  studio/shots/barkhorn/uplight31/*.json
    python3 studio/engine/render.py studio/shots/barkhorn/uplight31/uplit-red.json --out renders/2026-10-18/barkhorn/uplight31/uplit-red.png
"""
import copy, json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'uplight31')
FLAVOUR = {'red': 'cloud-red', 'orange': 'cloud-orange', 'amber': 'cloud-amber', 'green': 'eucalyptus-y2k-green',
           'blue': 'cloud-blue', 'violet': 'cloud-violet', 'ice': 'birch-fog-clear', 'black': 'cloud-black'}
NAME = {'red': 'Ember', 'orange': 'Dust', 'amber': 'Acid', 'green': 'Poison', 'blue': 'Ice', 'violet': 'Haze',
        'ice': 'Fog', 'black': 'Smoke'}
KEYS = list(FLAVOUR)
PRODUCT = 'studio/products/barkhorn-cloud.json'
W, D, H = 0.56, 0.43, 1.19          # the speaker's footprint and height with its horn, metres (the CAD's box)
RENDER = {'samples': 128, 'adaptive': 0.02, 'denoise': True, 'clamp': 10, 'bounces': 12, 'view': 'Khronos PBR Neutral',
          'exposure': 0.6, 'white_balance_k': 5600, 'white_balance_tint': 0.0}
CONCRETE = {'texture': 'concrete_layers_02', 'res': '4k', 'tex_scale': 1.4, 'bump': 1.2, 'vary': 0.22, 'vary_m': 3.5, 'ties': [0.6, 0.62]}   # board-formed, photographed (Poly Haven CC0)
NIGHT = {'kind': 'hdri', 'polyhaven': 'kloppenheim_07_puresky', 'res': '2k', 'strength': 0.6, 'rotation_deg': 0.0}   # an overcast night sky: the ambient and what the water mirrors
WARM = '#FFFFFF'                    # the uplights: a neutral white, so the acrylic alone gives the wall its colour (a warm lamp turned green and blue washes grey)
# post: no white point, only a shoulder above 205 that rolls the hot glow inside a cabinet into 246 keeping its hue (PBR
# Neutral alone bleaches a lit red toward white), a touch of clarity for the concrete's boards, a cored sharpen
FINISH = {'enabled': True, 'white_in': 205, 'white_out': 205, 'peak': 246, 'contrast': 0.05, 'clarity': 0.1, 'sharpen': 0.3}
LENS = 0.08                         # the plinth lens's glow: soft, never a clipped white line                    # the uplights' lamps: a warm white LED, 3500 K or so


def kit(fn, pos, **kw):
    return {'kind': 'kit', 'shape': 'ext', 'module': 'concrete', 'fn': fn, 'position': list(pos), **kw}


def fixture(x, y, lens_r=0.05, can_h=0.05, rotate=(0, 0, 0), glow=6.0):
    """A small black in-ground uplight's can and its lens, the lens a soft glow that lights nothing (the lamp is a
    separate spot)."""
    return [{'kind': 'kit', 'shape': 'cylinder', 'position': [x, y, 0.0], 'rotate': list(rotate), 'radius': lens_r + 0.012,
             'height': can_h, 'material': 'clay', 'color': '#1A1A1B', 'roughness': 0.5},
            {'kind': 'kit', 'shape': 'cylinder', 'position': [x, y, can_h], 'rotate': list(rotate), 'radius': lens_r, 'height': 0.002,
             'material': 'glow', 'color': WARM, 'emit': glow, 'shadow': False}]


def placement(kind, x=0.0, y=0.0, z0=0.0, power=1.0, horn=0.0):
    """The lamp and its fitting for one speaker standing at (x, y) with its base at z0, by placement:
    under: the speaker on a low black plinth whose top is a frosted lens, a spot inside it shining straight up;
    front: a floor uplight a third of a metre in front, tilted back so its beam crosses the face and the horn and
           climbs the wall behind;
    graze: a floor uplight hard against the face, aimed almost straight up, grazing the front panel and the horn."""
    if kind == 'under':
        # the plinth runs on 25 cm in front of the speaker, a lip that holds the horn's emitter (below)
        props = [{'kind': 'kit', 'shape': 'box', 'position': [x, y - LIP / 2, 0.0], 'size': [W + 0.10, D + 0.10 + LIP, z0],
                  'material': 'clay', 'color': '#141415', 'roughness': 0.45, 'ease': 0.012},
                 {'kind': 'kit', 'shape': 'box', 'position': [x, y, z0 - 0.002], 'size': [W + 0.01, D + 0.01, 0.003],
                  'material': 'glow', 'color': WARM, 'emit': LENS, 'shadow': False}]
        # the lamp: a flat panel of LEDs under the lens, the speaker's footprint, on the lens 10 mm below the cabinet's bottom (its feet are 12 mm) (a flat lamp, so no
        # part of the light starts inside the cabinet: a round lamp of any size this close would reach through the
        # bottom panel into the batts)
        lamp = {'type': 'area', 'size_m': [W - 0.08, D - 0.08], 'position': [x, y, z0 + 0.002], 'target': [x, y, z0 + 3.0],
                'spread_deg': 120, 'power_w': 450.0 * power, 'color': WARM}
        # and the fitting's second emitter, sunk in the plinth's lip: a narrow spot aimed up at the horn's front edge,
        # which the cabinet hides from the lamp under it (the batts stop all of that light), so the horn's resin glows;
        # its line clears the cabinet's front face
        if horn > 0:
            fy = y - D / 2 - LIP + 0.03
            lamps = {'': lamp, '-horn': {'type': 'spot', 'position': [x, fy, z0 + 0.002], 'target': [x, y - 0.12, z0 + 1.08],
                                         'cone_deg': 18, 'blend': 0.7, 'radius_m': 0.008, 'power_w': 420.0 * horn, 'color': WARM}}
            return props, lamps
    elif kind == 'front':
        fy = y - D / 2 - 0.34
        props = fixture(x, fy, rotate=(-14, 0, 0))
        lamp = {'type': 'spot', 'position': [x, fy, 0.06], 'target': [x, y + 0.6, 1.5], 'cone_deg': 34, 'blend': 0.45,
                'radius_m': 0.03, 'power_w': 4000.0 * power, 'color': WARM}
    elif kind == 'graze':
        fy = y - D / 2 - 0.09
        props = fixture(x, fy, lens_r=0.035, rotate=(-6, 0, 0))
        lamp = {'type': 'spot', 'position': [x, fy, 0.055], 'target': [x, y + 0.75, 3.2], 'cone_deg': 30, 'blend': 0.45,
                'radius_m': 0.025, 'power_w': 4000.0 * power, 'color': WARM}
    else:
        raise ValueError(kind)
    return props, {'': lamp}


SLIDE = 'under'                     # the slides' placement, from the study (see the README's notes)
LIP = 0.0                           # a lip on the plinth for a horn emitter (none: the horn's mouth faces forward and the cabinet's top hides its underside from any lamp in the plinth; the moon lights it)
Z0 = 0.08                           # the under-lamp's plinth: the speaker stands on its lens
WALL_Y = 1.0                        # the wall's face, a metre behind the speaker's centre


def frame(key, kind=SLIDE, size=(1600, 1600)):
    """One slide: the speaker on its light, a metre in front of the wall, a breath of moonlight so the room is a place."""
    z0 = Z0 if kind == 'under' else 0.0
    props, lamps = placement(kind, z0=z0)
    if kind == 'under':                                   # a narrower spread for the slide: the pool centred over the speaker
        lamps[''] = {**lamps[''], 'spread_deg': 45, 'power_w': 520.0}
    s = {'product': {'def': PRODUCT, 'flavour': FLAVOUR[key],
                     'instances': [{'flavour': FLAVOUR[key], 'position': [0, 0, z0], 'rotate_z': 0, 'hide': ['cloth-disc']}]},
         'set': {'kind': 'stage', 'props': [
             kit('wall', [0.0, WALL_Y + 0.25, 0.0], size=[9.0, 0.5, 7.0], **dict(CONCRETE, bump=3.5, tex_scale=1.0, vary=0.2)),
             kit('paving', [0.0, -1.5, 0.0], size=[12.0, 9.0], texture='granite_tile', res='2k', wet=0.35, puddle_m=2.5, vary=0.2),
         ] + props},
         'sky': dict(NIGHT, strength=0.04),
         'lights': {
             **{'up' + k: v for k, v in lamps.items()},
             # moonlight: a faint cool wash from high in front, so the concrete's boards read where the lamp does not reach
             'moon': {'type': 'area', 'size_m': [4.0, 2.0], 'position': [-1.0, -2.0, 5.0], 'target': [0.0, 0.0, 0.8],
                      'irradiance': 0.35, 'color': '#D4DCF2'}},
         'haze': {'box_m': [-2.5, -0.6, -0.05, 2.5, WALL_Y - 0.02, 4.0], 'density': 0.028, 'anisotropy': 0.7},
         'camera': {'position': [0.2, -3.6, 0.8], 'target': [0.0, 0.6, 1.15], 'lens_mm': 50.0, 'level': True},
         'render': dict(RENDER, exposure=1.35),
         'finish': dict(FINISH),
         'size': list(size),
         'title': f'barkhorn, {NAME[key]}, uplit ({kind}) before a concrete wall'}
    return s


def quay(keys, xs, camera, size, exposure, title, boost=None, power=0.5, spread=120, moon=0.22, pours=(3.6, 1.8)):
    """The night set both kinds of picture share: speakers in a row on a wet granite quay at the foot of an opera house's
    board-formed concrete river front, each on its uplight, the river at the quay's edge behind the camera's side.

    The wall's face is 0.3 m behind the speakers' centres (9 cm behind the cabinets): close, each cabinet
    throws its own tall column of colour, its batts' shadow a dark spine up the middle (at 1.2 m the columns ran
    together into one gradient, at 2.6 m they were lost). `boost`: a lamp's power by colour key (Smoke passes least);
    `power`, `spread`, `moon` the lamps and the moon; `pours` the wall's pours, (width, centre of one), so no joint
    falls behind a speaker."""
    wall_y = 0.3                                          # the wall's face (the plinths' backs are at 0.265)
    rnd = random.Random(31)
    def pour(pos, size):                                  # one pour of the wall, its own stretch of the texture
        return kit('wall', pos, size=size, **dict(CONCRETE, tex_scale=2.0, vary=0.6, vary_m=6.0, bump=1.8,
                                                  tex_offset=[round(rnd.uniform(0, 1), 3), round(rnd.uniform(0, 1), 3), round(rnd.uniform(0, 1), 3)]))
    props = [
        # the wall, board-formed concrete: one face in pours 3.6 m wide, a 12 mm joint between them falling between
        # speakers (no pilasters: their edges cut the washes into hard columns; no plinth course: its top drew a lit line), a deep cornice at
        # 4.8 m, and above it the night sky (the frame has to say it is outdoors)
        pour([0.0, wall_y + 0.75, 0.0], [60.0, 1.2, 5.6]),
        pour([0.0, wall_y - 0.35, 4.8], [60.0, 0.7, 0.8]),
        # the quay: wet granite flags with broad standing water, a wet granite kerb, the river just below
        kit('paving', [0.0, -1.3, 0.0], size=[60.0, 4.2], texture='granite_tile', res='2k', wet=0.65, puddle_m=1.2, puddle_edge=0.22, vary=0.2),
        kit('paving', [0.0, -3.575, 0.0], size=[60.0, 0.35], thick=0.03, texture='granite_tile', res='2k', wet=0.5, puddle_m=0.5, vary=0.4),
        kit('water', [0.0, -18.0, -0.06], size=[80.0, 29.0], ripple=0.12, ripple_m=1.2),
        # the city across the river, behind the camera's back, felt only as warm glows low on the water, near and far
        {'kind': 'kit', 'shape': 'box', 'position': [0.0, -40.0, -0.4], 'size': [80.0, 0.5, 0.3], 'material': 'glow',
         'color': '#FFC98A', 'emit': 3.0, 'shadow': False},
        {'kind': 'kit', 'shape': 'box', 'position': [0.0, -60.0, 0.5], 'size': [120.0, 0.5, 0.4], 'material': 'glow',
         'color': '#FFD2A0', 'emit': 1.5, 'shadow': False},
    ]
    pw, p0 = pours
    for i in range(-int(30 / pw), int(30 / pw) + 1):      # the pours, a 4 mm joint between them
        props.append(pour([round(p0 + i * pw, 3), wall_y + 0.15, 0.0], [pw - 0.004, 0.3, 4.8]))
    lights, insts = {}, []
    for i, (k, x) in enumerate(zip(keys, xs)):
        pr, lamps = placement(SLIDE, x=x, y=0.0, z0=Z0, power=power * (boost or {}).get(k, 1.0))
        lamps[''] = {**lamps[''], 'spread_deg': spread}
        props += pr
        for k_, l_ in lamps.items():
            lights[f'up{i}{k_}'] = l_
        insts.append({'flavour': FLAVOUR[k], 'position': [x, 0.0, Z0], 'rotate_z': 0, 'hide': ['cloth-disc']})
    # moonlight, cool and faint, high over the river at the front right: it finds the horns and the stone
    lights['moon'] = {'type': 'area', 'size_m': [10.0, 6.0], 'position': [4.0, -5.0, 7.5], 'target': [0.0, wall_y, 1.0],
                      'irradiance': moon, 'color': '#C4D0F0'}
    return {'product': {'def': PRODUCT, 'flavour': FLAVOUR[keys[0]], 'instances': insts},
            'set': {'kind': 'stage', 'props': props},
            'sky': dict(NIGHT, strength=0.12),
            'lights': lights,
            'haze': {'box_m': [-25.0, -20.0, -0.5, 25.0, wall_y - 0.02, 16.0], 'density': 0.02, 'anisotropy': 0.7},
            'camera': camera,
            'render': dict(RENDER, samples=160, exposure=exposure),
            'finish': dict(FINISH),
            'size': list(size),
            'title': title}


def facade(size=(2880, 1200), camera=None, exposure=1.0):
    """The night hero: the eight in a row on the quay, 1.2 m apart (0.9 merged their columns)."""
    return quay(KEYS, [(i - 3.5) * 1.2 for i in range(8)],
                camera or {'position': [0.0, -9.4, 0.6], 'target': [0.0, 0.0, 1.1], 'lens_mm': 33.0, 'level': True},
                size, exposure, 'barkhorn, the eight uplit along an opera house\'s concrete river front at night',
                boost={'black': 1.33}, power=0.75, spread=90, moon=0.1)


def slide(key, size=(1600, 1600)):
    """One slide: a speaker alone on the quay, the same set, camera and lamp for all eight (round 31, pass 6: the
    slides moved into the facade's world after five passes in a set of their own never passed 4.5)."""
    return quay([key], [0.0], {'position': [0.15, -5.0, 0.7], 'target': [0.0, 0.2, 0.95], 'lens_mm': 58.0, 'level': True},
                size, 1.0, f'barkhorn, {NAME[key]}, uplit on the quay before a concrete wall', power=0.3, moon=0.5,
                pours=(4.8, 0.0))


def main():
    os.makedirs(OUT, exist_ok=True)
    made = {}
    for k in KEYS:
        made[f'uplit-{k}'] = slide(k)
    for kind in ('under', 'front', 'graze'):
        for k in ('red', 'ice'):
            made[f'study-{kind}-{k}'] = frame(k, kind, size=(1200, 1200))
    made['facade'] = facade()
    made['facade-portrait'] = facade((1440, 1800), {'position': [0.6, -11.5, 1.5], 'target': [0.0, 0.0, 3.6], 'lens_mm': 26.0, 'level': True}, 1.3)
    for n, s in made.items():
        json.dump(s, open(os.path.join(OUT, n + '.json'), 'w'), indent=1)
    print(len(made), 'shots in', os.path.relpath(OUT, ROOT))


if __name__ == '__main__':
    main()
