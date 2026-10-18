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
import copy, json, os

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
CONCRETE = {'texture': 'concrete_layers_02', 'res': '4k', 'bump': 1.2, 'vary': 0.22, 'vary_m': 3.5}   # board-formed, photographed (Poly Haven CC0)
NIGHT = {'kind': 'hdri', 'polyhaven': 'kloppenheim_07_puresky', 'res': '2k', 'strength': 0.6, 'rotation_deg': 0.0}   # an overcast night sky: the ambient and what the water mirrors
WARM = '#FFF2DE'                    # the uplights' lamps: a warm white LED, 3500 K or so


def kit(fn, pos, **kw):
    return {'kind': 'kit', 'shape': 'ext', 'module': 'concrete', 'fn': fn, 'position': list(pos), **kw}


def fixture(x, y, lens_r=0.05, can_h=0.05, rotate=(0, 0, 0), glow=6.0):
    """A small black in-ground uplight's can and its lens, the lens a soft glow that lights nothing (the lamp is a
    separate spot)."""
    return [{'kind': 'kit', 'shape': 'cylinder', 'position': [x, y, 0.0], 'rotate': list(rotate), 'radius': lens_r + 0.012,
             'height': can_h, 'material': 'clay', 'color': '#1A1A1B', 'roughness': 0.5},
            {'kind': 'kit', 'shape': 'cylinder', 'position': [x, y, can_h], 'rotate': list(rotate), 'radius': lens_r, 'height': 0.002,
             'material': 'glow', 'color': WARM, 'emit': glow, 'shadow': False}]


def placement(kind, x=0.0, y=0.0, z0=0.0, power=1.0):
    """The lamp and its fitting for one speaker standing at (x, y) with its base at z0, by placement:
    under: the speaker on a low black plinth whose top is a frosted lens, a spot inside it shining straight up;
    front: a floor uplight a third of a metre in front, tilted back so its beam crosses the face and the horn and
           climbs the wall behind;
    graze: a floor uplight hard against the face, aimed almost straight up, grazing the front panel and the horn."""
    if kind == 'under':
        props = [{'kind': 'kit', 'shape': 'box', 'position': [x, y, 0.0], 'size': [W + 0.10, D + 0.10, z0], 'material': 'clay',
                  'color': '#141415', 'roughness': 0.45, 'ease': 0.004},
                 {'kind': 'kit', 'shape': 'box', 'position': [x, y, z0 - 0.002], 'size': [W + 0.06, D + 0.06, 0.003],
                  'material': 'glow', 'color': WARM, 'emit': 1.2, 'shadow': False}]
        lamp = {'type': 'spot', 'position': [x, y, z0 + 0.004], 'target': [x, y + 0.05, z0 + 3.0], 'cone_deg': 100, 'blend': 0.5,
                'radius_m': 0.12, 'power_w': 40000.0 * power, 'color': WARM}
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
    return props, lamp


SLIDE = 'under'                     # the slides' placement, from the study (see the README's notes)
Z0 = 0.08                           # the under-lamp's plinth: the speaker stands on its lens
WALL_Y = 1.0                        # the wall's face, a metre behind the speaker's centre


def frame(key, kind=SLIDE, size=(1600, 1600)):
    """One slide: the speaker on its light, a metre in front of the wall, a breath of moonlight so the room is a place."""
    z0 = Z0 if kind == 'under' else 0.0
    props, lamp = placement(kind, z0=z0)
    s = {'product': {'def': PRODUCT, 'flavour': FLAVOUR[key],
                     'instances': [{'flavour': FLAVOUR[key], 'position': [0, 0, z0], 'rotate_z': 0, 'hide': ['cloth-disc']}]},
         'set': {'kind': 'stage', 'props': [
             kit('wall', [0.0, WALL_Y + 0.25, 0.0], size=[9.0, 0.5, 7.0], **CONCRETE),
             kit('paving', [0.0, -1.5, 0.0], size=[12.0, 9.0], texture='concrete_pavement', res='2k', wet=0.35, puddle_m=1.5, vary=0.2),
         ] + props},
         'sky': dict(NIGHT, strength=0.12),
         'lights': {
             'up': lamp,
             # moonlight: a faint cool wash from high in front, so the concrete's boards read where the lamp does not reach
             'moon': {'type': 'area', 'size_m': [4.0, 2.0], 'position': [-2.5, -6.0, 6.0], 'target': [0.0, WALL_Y, 1.2],
                      'irradiance': 0.3, 'color': '#D4DCF2'}},
         'haze': {'box_m': [-6.0, -6.0, -0.05, 6.0, WALL_Y - 0.02, 6.5], 'density': 0.012, 'anisotropy': 0.3},
         'camera': {'position': [0.3, -2.45, 0.6], 'target': [0.04, 0.5, 1.75], 'lens_mm': 22.0, 'level': True},
         'render': dict(RENDER),
         'size': list(size),
         'title': f'barkhorn, {NAME[key]}, uplit ({kind}) before a concrete wall'}
    return s


def facade(size=(2880, 1200), camera=None, exposure=2.4):
    """The night hero: the eight in a row on the quay before an opera house's concrete river front, each on its uplight.
    They stand 2.5 m out from the wall, not 1 m as in the slides: the light that leaks up through each shell fans out,
    so further out its wash on the wall is broader and taller and meets its neighbours' (a proof at 1 m gave eight thin
    flames that never touched)."""
    gap = 1.2                                             # the speakers' spacing
    xs = [(i - 3.5) * gap for i in range(8)]
    wall_y = 2.6                                          # the wall's face
    props = [
        # the wall, one pour of board-formed concrete: a plinth course, shallow pilasters between pairs of speakers and
        # far along the front, a deep cornice band at 11 m, the wall going on up out of the frame
        kit('wall', [0.0, wall_y + 0.6, 0.0], size=[60.0, 1.2, 24.0], **CONCRETE),
        kit('wall', [0.0, wall_y - 0.12, 0.0], size=[60.0, 0.24, 0.6], **CONCRETE),
        kit('wall', [0.0, wall_y - 0.3, 11.0], size=[60.0, 0.6, 1.6], **CONCRETE),
        # the quay: wet flags, a stone kerb, the river a step below
        kit('paving', [0.0, -0.4, 0.0], size=[60.0, 6.0], texture='granite_tile', res='2k', wet=0.8, puddle_m=1.0, vary=0.2),
        {'kind': 'kit', 'shape': 'box', 'position': [0.0, -3.48, -0.45], 'size': [60.0, 0.16, 0.45], 'material': 'clay',
         'color': '#3A3936', 'roughness': 0.6},
        kit('water', [0.0, -18.0, -0.4], size=[80.0, 29.0], ripple=0.22, ripple_m=1.4),
        # the city across the river, far behind the camera's back, is felt only as a warm glow low on the water
        {'kind': 'kit', 'shape': 'box', 'position': [0.0, -40.0, -0.4], 'size': [80.0, 0.5, 0.3], 'material': 'glow',
         'color': '#FFC98A', 'emit': 0.6, 'shadow': False},
    ]
    for i in range(-6, 7):                                # pilasters every two speakers, on along the front
        props.append(kit('wall', [i * 2 * gap, wall_y - 0.15, 0.0], size=[0.7, 0.3, 11.0], **CONCRETE))
    lights, insts = {}, []
    for i, (k, x) in enumerate(zip(KEYS, xs)):
        pr, lamp = placement(SLIDE, x=x, y=0.0, z0=Z0)
        props += pr
        lights[f'up{i}'] = lamp
        insts.append({'flavour': FLAVOUR[k], 'position': [x, 0.0, Z0], 'rotate_z': 0, 'hide': ['cloth-disc']})
    # moonlight, cool and faint, high over the river
    lights['moon'] = {'type': 'area', 'size_m': [10.0, 6.0], 'position': [-14.0, -30.0, 22.0], 'target': [0.0, wall_y, 3.0],
                      'irradiance': 0.08, 'color': '#C4D0F0'}
    s = {'product': {'def': PRODUCT, 'flavour': FLAVOUR[KEYS[0]], 'instances': insts},
         'set': {'kind': 'stage', 'props': props},
         'sky': dict(NIGHT, strength=0.07),
         'lights': lights,
         'haze': {'box_m': [-25.0, -20.0, -0.5, 25.0, wall_y - 0.35, 16.0], 'density': 0.006, 'anisotropy': 0.3},
         'camera': camera or {'position': [0.9, -16.0, 1.0], 'target': [0.0, 0.0, 1.9], 'lens_mm': 30.0, 'level': True},
         'render': dict(RENDER, samples=160, exposure=exposure),
         'size': list(size),
         'title': 'barkhorn, the eight uplit along an opera house\'s concrete river front at night'}
    return s


def main():
    os.makedirs(OUT, exist_ok=True)
    made = {}
    for k in KEYS:
        made[f'uplit-{k}'] = frame(k)
    for kind in ('under', 'front', 'graze'):
        for k in ('red', 'ice'):
            made[f'study-{kind}-{k}'] = frame(k, kind, size=(1200, 1200))
    made['facade'] = facade()
    made['facade-portrait'] = facade((1440, 1800), {'position': [0.6, -11.5, 1.5], 'target': [0.0, 0.0, 3.6], 'lens_mm': 26.0, 'level': True}, 2.9)
    for n, s in made.items():
        json.dump(s, open(os.path.join(OUT, n + '.json'), 'w'), indent=1)
    print(len(made), 'shots in', os.path.relpath(OUT, ROOT))


if __name__ == '__main__':
    main()
