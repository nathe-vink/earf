"""Smoke, setting E8: the speaker came down like an asteroid (the owner, 2026-10-20: "The bridge could be a lot cooler if
it looked like the speaker slid along the asphalt and ground it up, like an asteroid might. It needs way more realism
though, like a movie still").

E7's overpass at blue hour, its wrecks burning further back under billowing black smoke. Down the near lane runs a
gouge a metre wide and a third of a metre deep, twenty metres from where the speaker struck the road at a shallow
angle to where it ploughed to rest: asphalt torn up in plates along both lips, the grey sub-base and aggregate bare and
scorched in the trench, debris thrown wide, finer with distance, and a low haze of dust and smoke still rising from it,
thickest just behind the speaker. The speaker stands at the trench's end, unhurt, grit only round its feet.

Shot as a film still: the camera low beside the trench so it leads the eye to the speaker, a 40 mm lens wide open with
the focus on the speaker, haze in layers, embers in the air, one motivated key (the fire) and a cool fill from the sky,
a filmic grade and fine grain.
"""
from common import area, camera, finish, piece, point, shot as frame, portrait_of, sky
from smoke import SHELL, SPEAKER
from smoke_bridge import DECK_HALF, SKY, SKY_ROT, fire, lamps, smoke_column, wreck

Y0, Y1 = -21.0, 1.2                        # the impact point and the gouge's end
LIP = 0.75                                 # half the opening at road level
SINK = -0.3                                # the speaker's base in the trench's end
# the gouge is built along +y from its impact (Y0) to its end (Y1) and turned half round, so in the frame it runs
# away behind the speaker toward the wrecks, and the speaker skidded toward the lens
FLIP = 180.0
# the wrecks, clear of the gouge's line: (x, y, heading, paint left, burning)
WRECKS = [(-3.4, 16.0, 125.0, 0.05, True), (3.8, 20.0, 20.0, 0.12, False), (-4.2, 29.0, 70.0, 0.08, False)]


def deck():
    """E7's deck with the gouge open down the near lane: the road in three slabs round it, the rest as E7's."""
    import smoke_bridge
    D = DECK_HALF
    road = dict(material='pbr', texture='asphalt_02', tex_scale=4.0, tint='#2C2C2E', tint_mix=0.3, rough_mul=0.3)
    out = [piece('box', size=[D + 2.0 - LIP, 150.0, 0.3], position=[-(LIP + (D + 2.0 - LIP) / 2), 55.0, -0.3], **road),
           piece('box', size=[D + 2.0 - LIP, 150.0, 0.3], position=[(LIP + (D + 2.0 - LIP) / 2), 55.0, -0.3], **road),
           piece('box', size=[2 * LIP, 130.0 + Y0, 0.3], position=[0.0, (130.0 - Y0) / 2, -0.3], **road),
           piece('box', size=[2 * LIP, 10.0, 0.3], position=[0.0, -Y1 - 5.0, -0.3], **road),
           # the trench's walls in section: the asphalt course, 8 cm, dark over the lighter base below it
           *[piece('box', size=[0.03, Y1 - Y0, 0.08], position=[s * (LIP - 0.012), -(Y0 + Y1) / 2, -0.08],
                   material='pbr', texture='asphalt_02', tex_scale=2.0, tint='#1C1C1E', tint_mix=0.5) for s in (-1, 1)]]
    rest = smoke_bridge.deck()[1:]                       # lane markings, barriers, footways, railings
    # no lane marking across the gouge
    rest = [q for q in rest if not (q.get('shape') == 'box' and q['size'][1] == 3.0 and abs(q['position'][0]) < LIP + 0.2
                                    and -Y1 < q['position'][1] < -Y0)]
    return out + rest


def gouge():
    common = dict(y0=Y0, y1=Y1, lip=LIP, depth=0.34, ramp=5.0)
    return [piece('ext', module='impact', fn='trench', width=1.3, end=0.8, ragged=0.05, texture='gravel_concrete',
                  tex_scale=0.7, tint='#4A4640', tint_mix=0.45, seed=3, grooves=0.06, rotate=[0, 0, FLIP], **common),
            piece('ext', module='impact', fn='slabs', count=90, thickness=0.06, tilt=40.0, tilt_min=6.0, size=0.6, seed=5, rotate_z=FLIP, **common),
            piece('ext', module='impact', fn='debris', y0=Y0, y1=Y1, count=420, reach=4.5, forward=0.7, ahead=6.0, seed=7, rotate_z=FLIP),
            # fines: gravel and grit sprayed ahead along the slide, and a dust skirt round the base
            piece('ext', module='impact', fn='debris', y0=Y0 + 10.0, y1=Y1, count=1400, reach=2.5, forward=0.8, ahead=5.0,
                  inner=0.6, seed=17, rotate_z=FLIP, fine=True),
            # the heave at its leading edge: plates shoved up and over in front of the speaker
            piece('ext', module='impact', fn='slabs', y0=Y1 - 0.9, y1=Y1 + 0.8, lip=0.45, depth=0.34, ramp=0.1, count=18,
                  thickness=0.07, tilt=60.0, tilt_min=30.0, size=0.42, seed=13, rotate_z=FLIP),
            # scorch along both lips: the road blackened where it was ground up
            piece('ext', module='impact', fn='scorch', position=[0.0, -((Y0 + Y1) / 2 + 0.6), 0.003],
                  size=[3.6, Y1 - Y0 + 2.5], strength=0.85, scale=0.5),
            # grit round the speaker's feet, on the trench floor
            piece('ext', module='impact', fn='debris', y0=-0.9, y1=-0.4, count=60, reach=0.45, inner=0.3, z=SINK, seed=9, rotate_z=FLIP)]


def haze():
    """Dust and smoke still rising from the gouge, thickest just behind the speaker, and the bridge's air in layers."""
    out = []
    for i, (y, l, dens, h) in enumerate([(1.8, 3.0, 0.7, 1.4), (5.0, 5.0, 0.45, 1.2), (11.0, 8.0, 0.3, 1.0)]):
        out.append(piece('ext', module='smoke_el', fn='woodsmoke', position=[0.0, y, SINK], size=[2.4, l, h], density=dens,
                         seed=80 + i, scale=0.35, cut=0.5, soft=0.3, anisotropy=0.65, fade=[0.4, 0.3, 0.6], floor=0.0,
                         rise=1.6, color='#8A7E74', detail_scale=0.1, detail_weight=0.5))
    out.append(piece('ext', module='smoke_el', fn='woodsmoke', position=[0.0, 30.0, -0.3], size=[30.0, 60.0, 8.0],
                     density=0.03, seed=89, scale=6.0, cut=0.2, soft=0.5, anisotropy=0.5, fade=[0.2, 0.2, 0.5], floor=0.01,
                     rise=1.2, color='#6A625C', detail_scale=1.5, detail_weight=0.4))
    # embers in the air between the fire and the lens
    out.append(piece('scatter', count=140, radius=[0.0015, 0.007], material='glow', color='#FF8A30', emit=60.0, seed=91,
                     **{'in': [-5.0, 5.0, 0.5, 4.0, 20.0, 6.0]}))
    return out


def shot():
    props = deck() + gouge() + haze()
    # a burning fragment thrown off at the impact, close by the lens at left: the key on the speaker's face
    props.append(piece('ext', module='wreck', fn='flame', position=[0.2, -2.9, 0.02], size=[0.5, 0.4, 0.55], density=6.0,
                       strength=60.0, scale=0.08, seed=33))
    props.append(piece('box', size=[0.45, 0.3, 0.06], position=[0.2, -2.9, 0.0], rotate=[0, 8, 25], material='clay',
                       color='#0E0C0B'))
    lp, lights = lamps()
    props += lp
    props.append(piece('ext', module='smoke_el', fn='occluder', position=[0.0, 0.0, SINK + 0.012], radius=0.42, sx=1.0,
                       sy=0.85, rotate_z=26.0))
    lights.update({
        'keyfire': {'type': 'point', 'position': [0.2, -2.9, 0.35], 'power_w': 600.0, 'color': '#FF8A3C', 'radius_m': 0.2,
                    'specular': 0.15, 'receivers': SPEAKER},
        # a cool fill from the sky, and the fire's key on the speaker's flank
        'skyfill': {**area(-20, 10, 2.4, 2.0, '#8EA4C6', (4.0, 3.0), (0.0, 0.0, 0.3)), 'receivers': SPEAKER},
        'bounce': {**area(-25, 12, 2.0, 2.0, '#C9BBA8', (2.4, 2.4), (0.0, 0.0, 0.3)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 40.0, '#FF9A50', (0.5, 2.4), (0.0, 0.0, 0.5)), 'receivers': SHELL},
        'kicker_r': {**area(150, 14, 3.0, 28.0, '#FFB070', (0.6, 2.4), (0.0, 0.0, 0.5)), 'receivers': SHELL},
    })
    for i, (x, y, heading, paint_left, burning) in enumerate(WRECKS):
        props.append(wreck(x, y, heading, paint_left, 11 + i))
        if burning:
            props += fire(x, y, heading, 50 + i) + smoke_column(x, y, 60 + 10 * i)
            lights[f'fire{i}'] = point([x, y, 1.3], 30000.0, '#FF7426', 0.9)
            lights[f'firerim{i}'] = {'type': 'area', 'size_m': [1.0, 1.0], 'position': [x * 0.4, y * 0.4, 1.0],
                                     'target': [0.0, 0.0, 0.5], 'irradiance': 30.0, 'color': '#FF8A3A', 'receivers': SHELL}
    # low beside the gouge, looking along it to the speaker; 40 mm wide open, focus on the speaker
    cam = camera(height=2.3, distance=4.6, azimuth=10, lens=30, target=(0.0, 0.0, 0.4), fstop=2.8, shift_x=0.0,
                 shift_y=0.1)
    cam['clip_end'] = 3000
    return frame('smoke_impact', props, cam, sky(SKY, rotation_deg=SKY_ROT, strength=0.5),
                 'barkhorn, Smoke, the speaker came down like an asteroid', lights=lights, rotate_z=26.0,
                 position=(0.0, 0.0, SINK), samples=512, exposure=0.0,
                 fin={**finish(contrast=0.16, clarity=0.05, saturation=0.0, bloom=0.16, bloom_px=60, threshold=0.7,
                               vignette=0.3), 'grain': 3.5})


def portrait():
    sh = shot()
    return portrait_of(sh, **camera(height=0.42, distance=4.6, azimuth=-7, lens=40, target=(0.0, 0.0, 0.45), fstop=2.0,
                                    shift_y=0.16))
