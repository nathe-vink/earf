"""Smoke, setting E4: black smoke in a pale studio (the owner, 2026-10-20: "Maybe studio for the smoke isn't right, since
it should really be black smoke").

The same column as E3, but black: sooty smoke that absorbs light rather than scattering it, so it reads dark against a
pale grey seamless, as ink does in water. The smoked black speaker stands on the same pale floor, lit soft from the
front-left, its dark acrylic clean against the light ground.
"""
from common import area, camera, finish, piece, shot as frame, portrait_of
from smoke import SHELL, SPEAKER
from smoke_studio import column

PAPER = '#C8C5C0'


def shot():
    props = [piece('box', size=[24.0, 24.0, 0.02], position=[0.0, 0.0, -0.02], material='clay', color=PAPER),
             piece('box', size=[24.0, 0.05, 10.0], position=[0.0, 5.0, 0.0], material='clay', color=PAPER),
             column(color='#0A0A0A', density=60.0, cut=0.36, fade_in=(0.12, 0.45))]
    cam = camera(height=0.6, distance=5.2, azimuth=-20, lens=65, target=(0.0, 0.0, 0.9), fstop=5.6, shift_x=0.0,
                 shift_y=-0.05)
    lights = {
        'skyfill': {**area(-20, 5, 2.4, 2.0, '#E4E6EA', (4.0, 3.0), (0.0, 0.0, 0.6)), 'receivers': SPEAKER},
        'kicker': {**area(-150, 22, 3.0, 20.0, '#F2EEE8', (0.5, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        'kicker_r': {**area(150, 14, 3.0, 14.0, '#F2EEE8', (0.6, 2.4), (0.0, 0.0, 0.8)), 'receivers': SHELL},
        # the key: a big soft box high front-left, lighting the speaker, the smoke and the paper alike
        'key': area(-45, 40, 4.0, 6.0, '#F4F2EE', (3.0, 3.0), (0.0, 0.0, 0.8)),
        # the paper behind, lit evenly so the floor runs into the wall without a seam
        'wall': {'type': 'area', 'size_m': [8.0, 3.0], 'position': [0.0, 2.0, 4.5], 'target': [0.0, 5.0, 1.0],
                 'irradiance': 5.0, 'color': '#F0EEEA', 'specular': 0.0},
    }
    return frame('smoke_studio_black', props, cam, {'kind': 'none', 'strength': 0.0},
                 'barkhorn, Smoke, black smoke in a pale studio', lights=lights, rotate_z=18.0, position=(0.0, 0.0, 0.0),
                 samples=512, exposure=0.0, fin=finish(contrast=0.05, clarity=0.03, vignette=0.1))


def portrait():
    sh = shot()
    return portrait_of(sh, **camera(height=0.6, distance=4.4, azimuth=-20, lens=65, target=(0.0, 0.0, 0.9), fstop=5.6,
                                    shift_y=0.0))
