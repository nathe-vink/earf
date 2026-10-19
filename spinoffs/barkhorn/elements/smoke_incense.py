"""Smoke, setting E1: incense in a concrete hall (round E, the owner 2026-10-19: "I just don't think the forest is a
good setting for smoke"; the coordinator's three settings, this one first).

A dark board-formed concrete room. In its right wall, in front of the speaker, a long slot lets in one slab of low
sun, which cuts across the room past the speaker and lands on the back wall behind it, a bright bar the speaker stands
against. On the floor beside the speaker a small bronze burner holds an
incense stick; its thread of smoke rises straight, then breaks into curls as it climbs through the slab of sun, where it
glows. No fire: the stick's ember is a few pixels. The speaker keeps A's rig (its fills and kickers linked to it alone).
"""
import math, random

from common import area, camera, finish, ground, piece, shot as frame, portrait_of
from smoke import SHELL, SPEAKER

ROOM = {'back': 2.4, 'left': -4.0, 'right': 3.2, 'front': -8.0, 'height': 4.6}
WALL = 'wood_textured_concrete'          # board-formed concrete (Poly Haven, CC0)
FLOOR = 'concrete_floor_02'
BURNER = (1.1, 0.5)                      # the burner, on the floor right of and a little behind the speaker
SUN = {'azimuth_deg': 45.0, 'elevation_deg': 15.0, 'irradiance': 30.0, 'angle_deg': 0.5, 'color': '#FFD2A0'}
SLOT = {'y': (-2.4, 0.4), 'z': (1.75, 2.05)}   # the slot in the right wall the sun comes through


def box(name, x0, y0, z0, x1, y1, z1, texture=WALL, scale=1.6):
    return piece('box', size=[x1 - x0, y1 - y0, z1 - z0], position=[(x0 + x1) / 2, (y0 + y1) / 2, z0], material='pbr',
                 texture=texture, tex_scale=scale, tint='#5C5752', tint_mix=0.25, name=name)


def room():
    """The hall: walls 0.3 m thick round the floor, a ceiling, and the right wall built round its slot."""
    R, t = ROOM, 0.3
    b, l, r, f, h = R['back'], R['left'], R['right'], R['front'], R['height']
    (y0, y1), (z0, z1) = SLOT['y'], SLOT['z']
    return [ground(FLOOR, size=(r - l + 1.0, b - f + 1.0), position=((l + r) / 2, (b + f) / 2, 0.0), displace=0.002,
                   relief=False, res='2k', tint='#4E4B48', tint_mix=0.2),
            box('back', l - t, b, -0.05, r + t, b + t, h + t),
            box('left', l - t, f - t, -0.05, l, b, h + t),
            box('front', l - t, f - t, -0.05, r + t, f, h + t),
            box('ceiling', l - t, f - t, h, r + t, b + t, h + t),
            # the right wall: below the slot, above it, and either side of it
            box('right-low', r, f - t, -0.05, r + t, b + t, z0),
            box('right-high', r, f - t, z1, r + t, b + t, h + t),
            box('right-front', r, f - t, z0 - 0.01, r + t, y0, z1 + 0.01),
            box('right-back', r, y1, z0 - 0.01, r + t, b + t, z1 + 0.01)]


def burner():
    """A small bronze incense burner (a low bowl of ash) with one stick leaning in it, its tip a dull ember."""
    x, y = BURNER
    tip = (x - 0.05, y + 0.02, 0.255)
    return [piece('lathe', profile=[[0.0, 0.0], [0.045, 0.0], [0.06, 0.012], [0.068, 0.035], [0.064, 0.045],
                                    [0.058, 0.04], [0.0, 0.034]], position=[x, y, 0.0], material='foil',
                  color='#6B4A2E', roughness=0.45),
            piece('cylinder', radius=0.0016, height=0.23, position=[x + 0.01, y - 0.005, 0.03], rotate=[-6.0, -14.0, 0.0],
                  material='clay', color='#6E3B26'),
            piece('sphere', position=list(tip), scale=0.0018, material='glow', color='#FF6A2A', emit=40.0)], tip


def incense(tip, seed=7, laminar=0.3, n=46, density=220.0, spread=0.045, lean=0.18, curl=0.12, color='#D9DADC',
            anisotropy=0.2, fade=(1.6, 2.3), branches=((12, 0.1, 0.05), (18, -0.08, -0.06)), cut=0.38, **extra):
    """The smoke: one thread rising straight from the tip for `laminar` metres, then breaking into curls that widen
    (`spread`) and lean left (`lean`) as they climb; finer strands peel off it at `branches` (point, dx, dy)."""
    rnd = random.Random(seed)
    x0, y0, z0 = tip
    main, radii = [], []
    ph = [rnd.uniform(0, 6.28) for _ in range(4)]
    for i in range(n):
        z = z0 + 0.04 * i
        h = z - z0
        k = max(0.0, h - laminar)                   # turbulence grows above the laminar thread
        a = 0.015 * k + curl * k ** 1.4
        x = x0 - lean * k ** 1.3 + a * math.sin(7.0 * h + ph[0] + 2.0 * math.sin(2.3 * h)) + 0.4 * a * math.sin(15.0 * h + ph[1])
        y = y0 + 0.6 * a * math.cos(6.0 * h + ph[2]) + 0.3 * a * math.sin(13.0 * h + ph[3])
        main.append([round(x, 4), round(y, 4), round(z, 4)])
        radii.append(round(0.0025 + 0.004 * min(h, max(laminar, 0.05)) / max(laminar, 0.05) + spread * k ** 1.2, 4))
    strands = [{'points': main, 'radii': radii, 'density': density}]
    for j, (start, dx, dy) in enumerate(branches):
        pts, rr = [main[start]], [radii[start]]
        for i in range(1, 22):
            z = main[start][2] + 0.045 * i
            s = i / 21
            pts.append([round(main[start][0] + dx * s * 2.2 + 0.05 * s * math.sin(9 * s + j), 4),
                        round(main[start][1] + dy * s * 2.2 + 0.04 * s * math.cos(8 * s + j), 4), round(z, 4)])
            rr.append(round(radii[start] * (0.7 + 1.2 * s), 4))
        strands.append({'points': pts, 'radii': rr, 'density': density / 3})
    return piece('ext', module='smoke_el', fn='ribbon', strands=strands, layers=extra.pop('layers', 3), scale=0.035, cut=cut, soft=0.3,
                 rise=2.5, laminar=laminar, laminar_blend=0.15, fade=list(fade), color=color, anisotropy=anisotropy,
                 detail=5.0, distortion=0.8, seed=seed, **extra)


def shot():
    pieces, tip = burner()
    props = room() + pieces + [incense(tip)]
    cam = camera(height=1.0, distance=5.6, azimuth=-20, lens=65, target=(0.2, 0.0, 0.75), fstop=4.0, shift_x=0.1)
    lights = {
        # A's rig, scaled to the room: a soft fill from the camera side, a bounce, two kickers rimming the shell
        'skyfill': {**area(-20, 5, 2.4, 1.2, '#B8BCC4', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'bounce': {**area(-25, 12, 2.0, 4.0, '#C9BBA8', (2.4, 2.4), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 30.0, '#FFD2A0', (0.5, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        'kicker_r': {**area(150, 14, 3.0, 20.0, '#FFD2A0', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        # the room's own soft light from the slot's bounce, over the floor (gives the speaker its contact shadow)
        'room': {'type': 'area', 'size_m': [3.0, 3.0], 'position': [0.0, -1.0, 4.4], 'target': [0.0, -0.5, 0.0],
                 'irradiance': 0.6, 'color': '#C8C2BA'},
    }
    return frame('smoke_incense', props, cam, {'kind': 'none', 'strength': 0.0}, 'barkhorn, Smoke, incense in a concrete hall',
                 sun=SUN, lights=lights, rotate_z=18.0, position=(0.0, 0.0, 0.0), samples=512, exposure=0.0,
                 fin=finish(contrast=0.05, clarity=0.03, bloom=0.03, bloom_px=30, threshold=0.9, vignette=0.2))


def portrait():
    sh = shot()
    return portrait_of(sh, **camera(height=1.0, distance=4.6, azimuth=-20, lens=65, target=(0.2, 0.0, 0.75), fstop=4.0,
                                    shift_x=0.04, shift_y=0.06))
