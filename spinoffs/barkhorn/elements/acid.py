"""Acid, concept A: an acid spring (round 31b; the notes are in acid.md).

The speaker on location in the spirit of Dallol (Ethiopia): a flat plain of terraced crust, white salt at the water's
edge, lemon sulphur and rust iron above it, opaque green acid in the hollows, sulphur and salt chimneys, steam. A hazy
late afternoon (Poly Haven's qwantani_late_afternoon_puresky), its hard sun behind the speaker's left so the golden acrylic is lit
through and rimmed, the crust raked, the steam glowing.
"""
from common import area, camera, shot as frame, sky, sun_from_sky, finish, piece, portrait_of

HDRI, ROT = 'quarry_01_puresky', 179.0                   # a clear sky, its hard sun low behind the speaker's left (azimuth -125)
WATER = -0.1
STAND = -0.07                                   # the salt flat the speaker stands on, 3 cm above the acid


ZONES = [(0.0, '#F1EEDC'), (0.08, '#F0DF62'), (0.22, '#E9C40F'), (0.42, '#DDA712'), (0.6, '#CC7A1E'),
         (0.76, '#A8481A'), (0.92, '#6E2C12')]


def ext(fn, **k):
    return piece('ext', module='acid_el', fn=fn, **k)


def set_props():
    terrain = dict(water=WATER, radius=286.0, seed=3, texture='acg:Ground093A', terrace=0.03, displace=0.014, grain_w=0.6,
                   flat=[0.0, 0.0, 0.6], stand=STAND, zone_scale=0.18, noise_w=1.4, zone_h=0.6, zone_bias=0.08, res='2k',
                   zones=ZONES, specular=0.08, roughness_min=0.8, tex_scale=0.7,
                   acid_colors=[(0.0, '#D2E27E'), (0.3, '#A6D89A'), (0.65, '#5FBFA4'), (1.0, '#2E9C8E')], acid_milk=0.2,
                   acid_edge=0.12, acid_deep=0.12, ripple=0.14,
                   pools=[[-0.35, -1.95, 0.2, 0.62], [2.4, 3.8, 0.22, 1.5], [-3.6, 6.5, 0.2, 1.8], [5.5, 9.0, 0.2, 2.2]])
    props = [ext('terrain', **terrain)]
    salt, sulphur, rust = ['#F5F1DC', '#EFE39A', '#DCC646'], ['#F4EA9A', '#EACB1E', '#C9A010'], ['#D9A04A', '#B2642A', '#7E3A1A']
    # two vents of different forms: a sulphur chimney steaming behind on the left, a broad low rust-ochre mound far off;
    # and an escarpment on the horizon for scale (at 278 m, inside the camera's 300 m clip, at the size a 60 m ridge
    # 1.6 km off would have: a still frame cannot tell the two apart)
    props += [ext('chimney', position=[-1.1, 9.2, 0.0], height=1.25, radius=0.42, colors=sulphur, seed=2),
              ext('chimney', position=[0.6, 19.0, 0.0], height=0.6, radius=1.3, colors=['#F2E6A0', '#E0A63A', '#B8642A'],
                  tex_scale=1.2, seed=11),
              ext('steam', position=[-1.1, 9.2, 1.12], height=4.5, r0=0.1, r1=1.4, lean=[1.6, 0.6], density=9.0,
                  anisotropy=0.6, seed=1),
              ext('steam', position=[0.6, 19.0, 0.5], height=4.0, r0=0.15, r1=1.0, lean=[1.5, 0.6], density=6.0,
                  anisotropy=0.6, seed=3),
              ext('ridge', distance=278.0, height=10.5, span=[-30.0, 22.0], tint='#7A4A30', tint_mix=0.7, tex_scale=5.0, seed=4)]
    return props


def lights():
    # a reflector a photographer would bring: a warm salt-white bounce from the front left, onto the speaker's face
    return {'bounce': area(-40, 12, 3.0, 1.6, '#FFE6B0', (2.0, 1.5), (0.0, 0.0, 0.7))}


def shot():
    cam = camera(height=0.75, distance=8.5, azimuth=-15.0, lens=85.0, target=(-0.55, 0.0, 0.66), focus=(-0.1, -0.2, 0.66), fstop=2.8)
    return frame('acid', set_props(), cam, sky(HDRI, ROT, strength=0.8, res='4k'), 'barkhorn, Acid, at the acid spring',
                 lights=lights(), sun=sun_from_sky(HDRI, ROT, irradiance=12.0), rotate_z=22.0, samples=512, position=(0.0, 0.0, STAND - 0.003),
                 haze={'box_m': [-300, -30, -3, 300, 300, 200], 'density': 0.0012, 'anisotropy': 0.5, 'color': '#F6EAD6'},
                 fin=finish(contrast=0.15, clarity=0.05, vignette=0.25),
                 exposure=-0.5, look='AgX - Medium High Contrast')


def portrait():
    return portrait_of(shot(), **camera(height=1.0, distance=5.0, azimuth=-15.0, lens=50.0, target=(0.0, 0.0, 0.8),
                                        fstop=5.6))
