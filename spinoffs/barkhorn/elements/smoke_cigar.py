"""Smoke, setting E2: after hours in a cigar room (round E, the coordinator's second setting).

A walnut-panelled club room after closing, nearly dark. A worn leather lounge chair turned toward the speaker, a tall
side table beside it, and on the table a heavy crystal ashtray where a cigar rests. Its blue-grey
smoke curls up through the one warm spot left on, which falls on the table and the speaker; the rest of the room drops
off into the dark. No flame: the cigar's ember is a few pixels.
"""
from common import area, asset, camera, finish, ground, piece, shot as frame, portrait_of
from smoke import SHELL, SPEAKER
from smoke_incense import incense

ROOM = {'back': 2.2, 'left': -3.6, 'right': 3.6, 'front': -8.0, 'height': 3.4}
PANEL = 'black_walnut_veneer_01'
FLOOR = 'brown_planks_05'
TABLE = (0.78, 0.12)                     # the tall side table (side_table_tall_01, 0.76 m high), right of the speaker
TOP = 0.762


def box(x0, y0, z0, x1, y1, z1, texture=PANEL, scale=1.2, tint='#3A2A20', mix=0.3):
    return piece('box', size=[x1 - x0, y1 - y0, z1 - z0], position=[(x0 + x1) / 2, (y0 + y1) / 2, z0], material='pbr',
                 texture=texture, tex_scale=scale, tint=tint, tint_mix=mix)


def room():
    R, t = ROOM, 0.2
    b, l, r, f, h = R['back'], R['left'], R['right'], R['front'], R['height']
    return [ground(FLOOR, size=(r - l + 1.0, b - f + 1.0), position=((l + r) / 2, (b + f) / 2, 0.0), displace=0.002,
                   relief=False, res='2k', tint='#2A1C14', tint_mix=0.35),
            box(l - t, b, -0.05, r + t, b + t, h + t), box(l - t, f - t, -0.05, l, b, h + t),
            box(r, f - t, -0.05, r + t, b + t, h + t), box(l - t, f - t, -0.05, r + t, f, h + t),
            box(l - t, f - t, h, r + t, b + t, h + t, tint='#120C08', mix=0.7),
            # a dado rail of brass along the back wall at 0.9 m
            piece('box', size=[r - l, 0.03, 0.025], position=[(l + r) / 2, b - 0.015, 0.9], material='foil',
                  color='#B08A4A', roughness=0.35)]


def table():
    """The side table, the crystal ashtray on it and the cigar resting in its notch, its tip a dull ember."""
    x, y = TABLE
    tip = (x + 0.115, y - 0.03, TOP + 0.045)
    return [asset('side_table_tall_01', (x, y, 0.0), (0, 0, 20), 1.0, res='1k'),
            piece('lathe', profile=[[0.0, 0.0], [0.085, 0.0], [0.092, 0.01], [0.09, 0.042], [0.075, 0.044],
                                    [0.068, 0.018], [0.0, 0.016]], position=[x, y, TOP], material='glass',
                  color='#E8ECEE', roughness=0.02),
            # the cigar across the rim: wrapper, its ash, its ember
            piece('cylinder', radius=0.0095, height=0.13, position=[x + 0.0, y - 0.03, TOP + 0.045],
                  rotate=[0.0, 84.0, 0.0], material='suede', color='#4A2E1C'),
            piece('cylinder', radius=0.0093, height=0.018, position=[x + 0.128, y - 0.03, TOP + 0.046],
                  rotate=[0.0, 84.0, 0.0], material='clay', color='#9C968E'),
            piece('sphere', position=[x + 0.147, y - 0.03, TOP + 0.048], scale=0.004, material='glow', color='#FF6A2A',
                  emit=12.0)], (x + 0.15, y - 0.03, TOP + 0.05)


def shot():
    pieces, tip = table()
    props = room() + pieces + [
        asset('mid_century_lounge_chair', (2.0, 1.2, 0.0), (0, 0, -60), 1.0, res='1k'),
        incense(tip, seed=11, laminar=0.06, n=30, density=50.0, spread=0.07, lean=0.25, curl=0.16, color='#AEB8C8',
                anisotropy=0.5, fade=(1.7, 2.1), branches=((5, 0.08, 0.04), (9, -0.07, -0.05), (14, 0.05, -0.08)), cut=0.5,
                layers=4, wobble=0.5, wobble_freq=10.0, break_scale=0.25, break_cut=0.35, break_floor=0.2)]
    cam = camera(height=1.0, distance=5.4, azimuth=-20, lens=65, target=(0.2, 0.0, 0.75), fstop=4.0, shift_x=0.1)
    lights = {
        'skyfill': {**area(-20, 5, 2.4, 0.8, '#C8BCAA', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'bounce': {**area(-25, 12, 2.0, 3.0, '#C9BBA8', (2.4, 2.4), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 26.0, '#FFB070', (0.5, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        'kicker_r': {**area(150, 14, 3.0, 18.0, '#FFB070', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        # the one warm spot left on: from the ceiling behind the table, so the smoke glows against the dark and the
        # pool falls forward over the table, the speaker's top and the floor
        'spot': {'type': 'spot', 'position': [0.9, 1.7, 3.2], 'target': [0.45, -0.1, 0.7], 'power_w': 700,
                 'cone_deg': 34.0, 'blend': 0.8, 'color': '#FFB070', 'radius_m': 0.06},
        # a whisper of the room: a low warm bounce so the chair and the panelling hold a shape in the dark
        'room': {'type': 'area', 'size_m': [3.0, 2.0], 'position': [-0.5, -2.5, 2.6], 'target': [-0.8, 1.5, 0.6],
                 'irradiance': 0.25, 'color': '#C89A6A'},
    }
    return frame('smoke_cigar', props, cam, {'kind': 'none', 'strength': 0.0}, 'barkhorn, Smoke, after hours in a cigar room',
                 lights=lights, rotate_z=18.0, position=(0.0, 0.0, 0.0), samples=512, exposure=0.0,
                 fin=finish(contrast=0.05, clarity=0.03, bloom=0.03, bloom_px=30, threshold=0.9, vignette=0.25))


def portrait():
    sh = shot()
    return portrait_of(sh, **camera(height=1.0, distance=4.5, azimuth=-20, lens=65, target=(0.2, 0.0, 0.75), fstop=4.0,
                                    shift_x=0.04, shift_y=0.06))
