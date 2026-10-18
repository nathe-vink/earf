"""Acid, concept A: an acid spring (round 31b; the notes are in acid.md).

The speaker on location in the spirit of Dallol (Ethiopia): a flat plain of terraced crust, white salt at the water's
edge, lemon sulphur and rust iron above it, opaque green acid in the hollows, sulphur and salt chimneys, steam. A hazy
late afternoon (Poly Haven's qwantani_late_afternoon_puresky), its hard sun behind the speaker's left so the golden acrylic is lit
through and rimmed, the crust raked, the steam glowing.
"""
from common import camera, shot as frame, sky, sun_from_sky, finish, piece, portrait_of

HDRI, ROT = 'qwantani_late_afternoon_puresky', -160.0    # its sun behind the speaker's left (azimuth -146)
WATER = -0.1
STAND = -0.07                                   # the salt flat the speaker stands on, 3 cm above the acid


ZONES = [(0.0, '#F1EEDC'), (0.08, '#F0DF62'), (0.22, '#E9C40F'), (0.42, '#DDA712'), (0.6, '#CC7A1E'),
         (0.76, '#A8481A'), (0.92, '#6E2C12')]


def ext(fn, **k):
    return piece('ext', module='acid_el', fn=fn, **k)


def set_props():
    terrain = dict(water=WATER, seed=3, texture='rock_boulder_cracked', terrace=0.045,
                   flat=[0.0, 0.0, 0.6], stand=STAND, zone_scale=0.15, noise_w=1.3, zone_h=0.16, plates=0.35, plate_m=1.1, res='4k',
                   zones=ZONES,
                   pools=[[-0.35, -1.95, 0.2, 0.62], [2.4, 3.8, 0.22, 1.5], [-3.6, 6.5, 0.2, 1.8], [5.5, 9.0, 0.2, 2.2]])
    props = [ext('terrain', **terrain)]
    salt, sulphur, rust = ['#F5F1DC', '#EFE39A', '#DCC646'], ['#F4EA9A', '#EACB1E', '#C9A010'], ['#D9A04A', '#B2642A', '#7E3A1A']
    props += [ext('chimney', position=[-2.0, 4.6, 0.0], height=1.15, radius=0.34, colors=sulphur, seed=2),
              ext('chimney', position=[-1.6, 4.3, 0.0], height=0.55, radius=0.22, colors=salt, seed=5),
              ext('chimney', position=[2.2, 2.6, 0.0], height=0.75, radius=0.3, colors=salt, seed=7),
              ext('chimney', position=[-7.5, 14.0, 0.0], height=1.6, radius=0.6, colors=sulphur, seed=9),
              ext('chimney', position=[11.0, 17.0, 0.0], height=1.2, radius=0.7, colors=rust, seed=11),
              ext('steam', position=[-2.0, 4.6, 1.0], height=3.2, r0=0.14, r1=1.0, lean=[0.9, 0.4], density=5.0, anisotropy=0.6, seed=1),
              ext('steam', position=[-7.5, 14.0, 1.4], height=5.0, r0=0.3, r1=2.0, lean=[1.6, 0.5], density=2.5, anisotropy=0.6, seed=2)]
    return props


def lights():
    return {}


def shot():
    cam = camera(height=0.7, distance=6.5, azimuth=-15.0, lens=65.0, target=(-0.45, 0.0, 0.66), focus=(0.0, -0.21, 0.66), fstop=5.6)
    return frame('acid', set_props(), cam, sky(HDRI, ROT, strength=0.8, res='4k'), 'barkhorn, Acid, at the acid spring',
                 lights=lights(), sun=sun_from_sky(HDRI, ROT, irradiance=10.0), rotate_z=-20.0, samples=512, position=(0.0, 0.0, STAND - 0.003),
                 haze={'box_m': [-60, -30, -1, 60, 120, 12], 'density': 0.0008, 'anisotropy': 0.5, 'color': '#FFFFFF'},
                 fin=finish(contrast=0.05, clarity=0.05, vignette=0.15),
                 exposure=-0.6, look='AgX - Medium High Contrast')


def portrait():
    return portrait_of(shot(), **camera(height=1.0, distance=5.0, azimuth=-15.0, lens=50.0, target=(0.0, 0.0, 0.8),
                                        fstop=5.6))
