"""Acid, concept A: an acid spring (round 31b; the notes are in acid.md).

The speaker on location in the spirit of Dallol (Ethiopia): a flat plain of terraced crust, white salt at the water's
edge, lemon sulphur and rust iron above it, opaque green acid in the hollows, sulphur and salt chimneys, steam. A hazy
late afternoon (Poly Haven's qwantani_late_afternoon_puresky), its hard sun behind the speaker's left so the golden acrylic is lit
through and rimmed, the crust raked, the steam glowing.
"""
from common import area, camera, shot as frame, sky, sun_from_sky, finish, piece, portrait_of

HDRI, ROT = 'quarry_01_puresky', 154.0                   # a clear sky, its hard sun low on the speaker's left (azimuth -100)
WATER = -0.1
STAND = -0.07                                   # the salt flat the speaker stands on, 3 cm above the acid


ZONES = [(0.0, '#F1EEDC'), (0.08, '#F0DF62'), (0.22, '#E9C40F'), (0.42, '#DDA712'), (0.6, '#CC7A1E'),
         (0.76, '#A8481A'), (0.92, '#6E2C12')]


def ext(fn, **k):
    return piece('ext', module='acid_el', fn=fn, **k)


def set_props():
    terrain = dict(water=WATER, seed=3, texture='acg:Ground093A', terrace=0.03, displace=0.025, grain_w=0.6,
                   flat=[0.0, 0.0, 0.6], stand=STAND, zone_scale=0.18, noise_w=1.4, zone_h=0.6, zone_bias=0.2, res='2k',
                   zones=ZONES, specular=0.25, tex_scale=1.2,
                   acid_colors=[(0.0, '#D2E27E'), (0.35, '#A6D89A'), (1.0, '#5FBFA4')], acid_milk=0.25, ripple=0.14,
                   pools=[[-0.35, -1.95, 0.2, 0.62], [2.4, 3.8, 0.22, 1.5], [-3.6, 6.5, 0.2, 1.8], [5.5, 9.0, 0.2, 2.2]])
    props = [ext('terrain', **terrain)]
    salt, sulphur, rust = ['#F5F1DC', '#EFE39A', '#DCC646'], ['#F4EA9A', '#EACB1E', '#C9A010'], ['#D9A04A', '#B2642A', '#7E3A1A']
    # three vents, each its own form: a tiered sulphur chimney steaming behind on the left, a small salt one to the
    # right, a far one on the horizon
    props += [ext('chimney', position=[-1.1, 9.2, 0.0], height=1.25, radius=0.42, colors=sulphur, seed=2),
              ext('chimney', position=[1.6, 2.2, 0.0], height=0.45, radius=0.26, colors=salt, seed=7),
              ext('chimney', position=[0.6, 19.0, 0.0], height=1.0, radius=0.6, colors=['#F2E6A0', '#E9B52A', '#C9701E'], seed=11),
              ext('steam', position=[0.6, 19.0, 0.9], height=6.0, r0=0.25, r1=2.2, lean=[2.0, 0.8], density=8.0, anisotropy=0.25, seed=3),
              ext('steam', position=[-1.1, 9.2, 1.15], height=4.5, r0=0.12, r1=1.4, lean=[1.4, 0.6], density=20.0,
                  anisotropy=0.25, seed=1)]
    return props


def lights():
    # a reflector a photographer would bring: a warm salt-white bounce from the front left, onto the speaker's face
    return {'bounce': area(-40, 12, 3.0, 1.6, '#FFE6B0', (2.0, 1.5), (0.0, 0.0, 0.7))}


def shot():
    cam = camera(height=0.75, distance=8.5, azimuth=-15.0, lens=85.0, target=(-0.55, 0.0, 0.66), focus=(-0.1, -0.2, 0.66), fstop=2.8)
    return frame('acid', set_props(), cam, sky(HDRI, ROT, strength=1.0, res='4k'), 'barkhorn, Acid, at the acid spring',
                 lights=lights(), sun=sun_from_sky(HDRI, ROT, irradiance=12.0), rotate_z=22.0, samples=512, position=(0.0, 0.0, STAND - 0.003),
                 haze={'box_m': [-60, -30, -1, 60, 120, 12], 'density': 0.003, 'anisotropy': 0.5, 'color': '#F6EAD6'},
                 fin=finish(contrast=0.1, clarity=0.05, vignette=0.2),
                 exposure=-0.3, look='AgX - Medium High Contrast')


def portrait():
    return portrait_of(shot(), **camera(height=1.0, distance=5.0, azimuth=-15.0, lens=50.0, target=(0.0, 0.0, 0.8),
                                        fstop=5.6))
