"""Smoke, setting E7: the aftermath on a bridge (the owner, 2026-10-20: "an apocalyptic or riot scene, with cars crashed
and burning on a bridge, billowing black smoke, with the speaker in the foreground"; then "Both need more work and
realism").

A four-lane concrete overpass at blue hour, a city skyline beyond its railings. Wet asphalt and lane markings recede
between Jersey barriers, footways and steel railings, under a row of lit lamp posts. Fifteen to thirty metres back three
burnt-out saloons sit at angles across the lanes: two cold, charred shells on bare rims; one still burning, its fire
deep in the cabin and engine bay, its smoke grey and lit just above the flames, thickening and darkening as it rises and
drifts left across the sky. Firelight and lamplight lie in the wet road. The speaker stands untouched on the deck in the
foreground. An empty aftermath: no people.
"""
from common import area, camera, finish, ground, piece, point, shot as frame, portrait_of, sky
from smoke import SHELL, SPEAKER

SKY = 'sunset_jhbcentral'                   # a city skyline at twilight from a rooftop (Poly Haven, CC0)
SKY_ROT = 0.0
# the wrecks: (x, y, heading in degrees, paint left showing, burning)
WRECKS = [(-1.2, 15.0, 125.0, 0.05, True), (3.6, 21.0, 20.0, 0.12, False), (-3.4, 29.0, 70.0, 0.08, False)]
DECK_HALF = 7.0                             # kerb to kerb half-width: four lanes of 3.5 m


def wreck(x, y, heading, paint_left, seed):
    return piece('ext', module='wreck', fn='sedan', position=[x, y], heading=heading, paint='#2B3036',
                 paint_left=paint_left, crumple=0.3, sag=0.1, seed=seed)


def fire(x, y, heading, seed):
    """The fire in the burning wreck: flames from the cabin and the engine bay, their light and a few embers."""
    import math
    h = math.radians(heading)
    out = []
    for k, (dx, w, d, hgt, z) in enumerate([(-0.3, 1.5, 1.3, 1.6, 0.55), (1.6, 1.0, 1.4, 1.1, 0.6)]):
        out.append(piece('ext', module='wreck', fn='flame', position=[x + dx * math.cos(h), y + dx * math.sin(h), z],
                         size=[w, d, hgt], rotate_z=heading, density=8.0, strength=1.0, scale=0.16, seed=seed + k))
    out.append(piece('scatter', count=50, radius=[0.004, 0.012], position=[x, y, 1.6], material='glow', color='#FF8A30',
                     emit=40.0, seed=seed, plume={'height': 6.0, 'spread': [0.3, 2.2], 'lean': [-2.5, 0.5], 'taper': 0.7}))
    return out


def smoke_column(x, y, seed):
    """The burning wreck's smoke: grey and lit just above the fire, thickening and darkening as it climbs and drifts left."""
    out = []
    for k in range(8):
        t = k / 7
        w = 2.2 + 12.0 * t ** 1.2
        col = '#5A5652' if k == 0 else ('#2C2B2A' if k == 1 else '#141414')
        out.append(piece('ext', module='smoke_el', fn='woodsmoke', position=[x - 10.0 * t ** 1.5, y + 3.0 * t, 1.4 + 2.8 * k],
                         size=[w, w, 3.6], density=(1.5 + 3.5 * min(1.0, 2 * t)) * (1.0 - 0.5 * t), seed=seed + k,
                         scale=0.6 + 1.8 * t, cut=0.4, soft=0.3, anisotropy=0.35, fade=[0.35, 0.35, 0.4], floor=0.0,
                         rise=1.6, color=col, detail_scale=0.2 + 0.4 * t, detail_weight=0.55))
    return out


def deck():
    """The overpass: wet asphalt, lane markings, Jersey barriers, footways, steel railings and lamp posts."""
    D = DECK_HALF
    out = [ground('asphalt_02', size=(2 * D + 4.0, 140.0), position=(0.0, 60.0, 0.0), displace=0.004, relief=False,
                  res='2k', tint='#2C2C2E', tint_mix=0.3, rough_mul=0.3)]
    for k in range(15):
        y = -4.0 + 9.0 * k
        for x in (-3.5, 3.5):
            out.append(piece('box', size=[0.14, 3.0, 0.004], position=[x, y, 0.0], material='clay', color='#C9C7C0'))
    for x in (-D + 0.2, D - 0.2):
        out.append(piece('box', size=[0.12, 140.0, 0.004], position=[x, 60.0, 0.0], material='clay', color='#C9C7C0'))
    jersey = [[-0.3, 0.0], [0.3, 0.0], [0.3, 0.08], [0.1, 0.3], [0.08, 0.81], [-0.08, 0.81], [-0.1, 0.3], [-0.3, 0.08]]
    for s in (-1, 1):
        out.append(piece('extrude', outline=jersey, depth=140.0, position=[s * (D + 0.3), 60.0, 0.0], rotate=[0, 0, 90],
                         material='pbr', texture='concrete_wall_008', tex_scale=2.0, tint='#8C8A86', tint_mix=0.3, ease=0.01))
        # the footway beyond the barrier and the railing at the deck's edge
        out.append(piece('box', size=[1.6, 140.0, 0.2], position=[s * (D + 1.4), 60.0, 0.0], material='pbr',
                         texture='concrete_floor_02', tex_scale=2.0, tint='#7E7C78', tint_mix=0.3))
        for k in range(71):
            out.append(piece('box', size=[0.06, 0.06, 1.1], position=[s * (D + 2.15), -10.0 + 2.0 * k, 0.2], material='foil',
                             color='#4E5156', roughness=0.45))
        for z in (0.75, 1.3):
            out.append(piece('box', size=[0.06, 140.0, 0.06], position=[s * (D + 2.15), 60.0, z], material='foil',
                             color='#4E5156', roughness=0.45))
    return out


def lamps():
    """Lamp posts every 30 m along both footways, their heads lit, each throwing a pool on the wet road."""
    D = DECK_HALF
    out, lights = [], {}
    for k in range(5):
        y = 6.0 + 30.0 * k
        for s in (-1, 1):
            x = s * (D + 1.2)
            out.append(piece('cylinder', radius=0.09, radius_top=0.06, height=9.0, position=[x, y, 0.2], material='foil',
                             color='#5A5D62', roughness=0.5))
            out.append(piece('box', size=[2.0, 0.12, 0.1], position=[x - s * 1.0, y, 9.1], material='foil', color='#5A5D62',
                             roughness=0.5))
            out.append(piece('box', size=[0.7, 0.3, 0.12], position=[x - s * 1.9, y, 9.0], material='foil', color='#3E4044',
                             roughness=0.5))
            out.append(piece('box', size=[0.6, 0.24, 0.02], position=[x - s * 1.9, y, 8.98], material='glow', color='#FFD8A8',
                             emit=60.0))
            lights[f'lamp{k}{s}'] = {'type': 'spot', 'position': [x - s * 1.9, y, 8.9], 'target': [x - s * 3.5, y, 0.0],
                                     'power_w': 2500.0, 'cone_deg': 120.0, 'blend': 0.8, 'color': '#FFD2A0',
                                     'radius_m': 0.3}
    return out, lights


def shot():
    props = deck()
    lp, lights = lamps()
    props += lp
    lights.update({
        'skyfill': {**area(-20, 5, 2.4, 1.6, '#AEB8C8', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'bounce': {**area(-25, 12, 2.0, 4.0, '#C9BBA8', (2.4, 2.4), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 30.0, '#FF9A50', (0.5, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        'kicker_r': {**area(150, 14, 3.0, 20.0, '#FFB070', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
    })
    for i, (x, y, heading, paint_left, burning) in enumerate(WRECKS):
        props.append(wreck(x, y, heading, paint_left, 11 + i))
        if burning:
            props += fire(x, y, heading, 50 + i) + smoke_column(x, y, 60 + 10 * i)
            lights[f'fire{i}'] = point([x, y, 1.3], 9000.0, '#FF7426', 0.9)
    cam = camera(height=0.9, distance=5.0, azimuth=-12, lens=35, target=(0.0, 0.0, 0.85), fstop=4.0, shift_x=0.0,
                 shift_y=0.12)
    cam['clip_end'] = 3000
    return frame('smoke_bridge', props, cam, sky(SKY, rotation_deg=SKY_ROT, strength=0.6),
                 'barkhorn, Smoke, the aftermath on a bridge', lights=lights, rotate_z=18.0, position=(0.0, 0.0, 0.0),
                 samples=512, exposure=0.0,
                 fin=finish(contrast=0.06, clarity=0.04, bloom=0.06, bloom_px=40, threshold=0.85, vignette=0.25))


def portrait():
    sh = shot()
    return portrait_of(sh, **camera(height=0.9, distance=4.2, azimuth=-12, lens=35, target=(0.0, 0.0, 0.85), fstop=4.0,
                                    shift_y=0.14))
