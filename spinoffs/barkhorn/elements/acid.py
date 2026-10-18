"""Acid, concept A: an acid spring (round 31b; the notes are in acid.md).

The speaker on location in the spirit of Dallol (Ethiopia): a flat plain of terraced crust, white salt at the water's
edge, lemon sulphur and rust iron above it, opaque green acid in the hollows, sulphur and salt chimneys, steam. A hazy
late afternoon (Poly Haven's qwantani_late_afternoon_puresky), its hard sun behind the speaker's left so the golden acrylic is lit
through and rimmed, the crust raked, the steam glowing.
"""
from common import area, camera, shot as frame, sky, sun_from_sky, finish, piece, portrait_of

HDRI, ROT = 'evening_road_01_puresky', 166.0             # its sun low on the speaker's left, a little behind (azimuth -115)
WATER = -0.1
STAND = -0.07                                   # the salt flat the speaker stands on, 3 cm above the acid


ZONES = [(0.0, '#F1EEDC'), (0.08, '#F0DF62'), (0.22, '#E9C40F'), (0.42, '#DDA712'), (0.6, '#CC7A1E'),
         (0.76, '#A8481A'), (0.92, '#6E2C12')]


def ext(fn, **k):
    return piece('ext', module='acid_el', fn=fn, **k)


def set_props():
    terrain = dict(water=WATER, seed=3, texture='rock_boulder_cracked', terrace=0.045,
                   flat=[0.0, 0.0, 0.6], stand=STAND, zone_scale=0.15, noise_w=1.3, zone_h=0.16, plates=0.35, plate_m=1.1, res='4k',
                   zones=ZONES, specular=0.15, rough_mul=1.25, tex_scale=0.9,
                   pools=[[-0.35, -1.95, 0.2, 0.62], [2.4, 3.8, 0.22, 1.5], [-3.6, 6.5, 0.2, 1.8], [5.5, 9.0, 0.2, 2.2]])
    props = [ext('terrain', **terrain)]
    salt, sulphur, rust = ['#F5F1DC', '#EFE39A', '#DCC646'], ['#F4EA9A', '#EACB1E', '#C9A010'], ['#D9A04A', '#B2642A', '#7E3A1A']
    # three vents, each its own form: a tiered sulphur chimney steaming behind on the left, a small salt one to the
    # right, a far one on the horizon
    props += [ext('chimney', position=[-1.1, 9.2, 0.0], height=1.25, radius=0.42, colors=sulphur, tiers=4, seed=2),
              ext('chimney', position=[1.6, 2.2, 0.0], height=0.45, radius=0.26, colors=salt, tiers=2, seed=7),
              ext('chimney', position=[0.6, 19.0, 0.0], height=1.0, radius=0.6, colors=rust, tiers=3, seed=11),
              ext('steam', position=[-1.1, 9.2, 1.15], height=4.5, r0=0.12, r1=1.4, lean=[1.4, 0.6], density=7.0,
                  anisotropy=0.25, seed=1)]
    return props


def lights():
    # a reflector a photographer would bring: a warm salt-white bounce from the front left, onto the speaker's face
    return {'bounce': area(-40, 12, 3.0, 2.2, '#FFE6B0', (2.0, 1.5), (0.0, 0.0, 0.7))}


def shot():
    cam = camera(height=0.5, distance=9.0, azimuth=-15.0, lens=85.0, target=(-0.55, 0.0, 0.66), focus=(-0.1, -0.2, 0.66), fstop=4.0)
    return frame('acid', set_props(), cam, sky(HDRI, ROT, strength=1.0, res='4k'), 'barkhorn, Acid, at the acid spring',
                 lights=lights(), sun=sun_from_sky(HDRI, ROT, irradiance=7.0), rotate_z=22.0, samples=512, position=(0.0, 0.0, STAND - 0.003),
                 haze={'box_m': [-60, -30, -1, 60, 120, 12], 'density': 0.003, 'anisotropy': 0.5, 'color': '#F3E2C4'},
                 fin=finish(contrast=0.05, clarity=0.05, vignette=0.15),
                 exposure=-0.6, look='AgX - Medium High Contrast')


def portrait():
    return portrait_of(shot(), **camera(height=1.0, distance=5.0, azimuth=-15.0, lens=50.0, target=(0.0, 0.0, 0.8),
                                        fstop=5.6))
