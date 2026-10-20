"""Poison, N3 (round 31g): a volcanic crater, the poison in the air.

The owner, 2026-10-20: "Took a look at poison. It needs to be outside and incorporate nature. It loses the EARF vibe if
not." The speaker stands on the grey ash rim of a crater; below it a milky turquoise-green acid lake, yellow sulphur
crusted only round the vents at its shore, and sulphur fumes drifting across the frame. It must read as Poison, not
Acid: the yellow kept to the crusts, the water and the fumes in the greens, the sky overcast.

Built from Acid's terrain (kit_ext/acid_el.py: the crust, the lake, the vents, the far crater wall), re-coloured, with
Smoke's volumes (kit_ext/smoke_b_el.py: plume, smoke) for the fumes; scanned boulders (Poly Haven) on the rim.
"""
from common import area, asset, camera, finish, piece, portrait_of, shot as frame, sky, sun_from_sky

HDRI, ROT = 'kloofendal_overcast_puresky', 40.0
WATER = -2.6                                    # the lake, well below the rim
STAND = 0.0

# by height above the water: a pale scum line, sulphur at the shore (only there), then grey ash all the way up
ZONES = [(0.0, '#D8E2C8'), (0.03, '#E6D45A'), (0.08, '#C9B23A'), (0.16, '#8E8A72'), (0.3, '#6E6C64'), (0.6, '#5A5954'),
         (1.0, '#4A4946')]


def ext(module, fn, **k):
    return piece('ext', module=module, fn=fn, **k)


def set_props():
    terrain = dict(water=WATER, radius=286.0, seed=7, texture='rock_ground_02', terrace=0.004, displace=0.02, grain_w=0.5,
                   flat=[0.0, 0.0, 2.0], stand=STAND, zone_scale=0.35, noise_w=0.9, zone_h=3.0, zone_bias=0.0, res='2k',
                   zones=ZONES, specular=0.05, roughness_min=0.85, tex_scale=0.9,
                   acid_colors=[(0.0, '#B9D8B4'), (0.35, '#8CCBB2'), (0.7, '#5DB7A8'), (1.0, '#3E9C90')], acid_milk=0.45,
                   acid_edge=0.25, acid_deep=0.3, ripple=0.06,
                   # the crater floor: the rim falls away beyond the speaker into one broad lake
                   pools=[[0.0, 34.0, 5.5, 15.0], [-16.0, 34.0, 5.0, 12.0], [16.0, 36.0, 5.0, 12.0]])
    props = [ext('acid_el', 'terrain', **terrain)]
    sulphur = ['#EFE39A', '#E2C628', '#B8960E']
    # sulphur vents at the shore, fuming
    for x, y, h, r, sd in ((-7.0, 19.0, 0.9, 1.0, 2), (4.0, 18.5, 0.7, 0.8, 5), (10.0, 23.0, 1.1, 1.2, 8)):
        props.append(ext('acid_el', 'chimney', position=[x, y, WATER + 0.05], height=h, radius=r, colors=sulphur,
                         tex_scale=1.1, seed=sd))
    # the fumes: green-grey plumes from the vents, bent over by the wind, and a drifting layer across the frame
    for (x, y), lean, sd in (((-7.0, 19.0), 7.0, 1), ((4.0, 18.5), 6.0, 2), ((10.0, 23.0), 8.0, 3)):
        props.append(ext('poison_p_el', 'plume_at', base=[x, y], height=9.0, lean=lean, bend=1.6, width=0.7, spread=0.5,
                         density=0.9, color='#D6E2C4', absorb_color='#9AAA84', anisotropy=0.45, seed=sd, z=WATER))
    props.append(ext('smoke_b_el', 'smoke', box=[-30.0, 3.0, -2.0, 30.0, 45.0, 6.0], drift=-20.0, height=1.2, thickness=3.5,
                     density=0.06, color='#DCE6CC', absorb_color='#A4B290', anisotropy=0.35, seed=4))
    # the crater's far wall, grey rock, closing the view; boulders on the rim by the speaker
    props += [ext('acid_el', 'ridge', distance=95.0, height=34.0, span=[-55.0, 50.0], tint='#5E5C56', tint_mix=0.7,
                  tex_scale=3.0, seed=9),
              asset('rock_09', (-1.6, 1.1, -0.12), rotate=(0, 0, 40), scale=14.0),
              asset('rock_09', (2.1, 2.4, -0.15), rotate=(0, 0, 200), scale=20.0)]
    return props


def lights():
    return {'bounce': area(-35, 12, 3.0, 1.2, '#E8ECE0', (2.0, 1.5), (0.0, 0.0, 0.7)),
            'throat': area(14, 4, 2.2, 1.2, '#EEF2E8', (0.7, 0.5), (0.05, -0.05, 1.12))}


def shot():
    cam = camera(height=1.05, distance=4.6, azimuth=-14.0, lens=40.0, target=(0.0, 0.5, 0.75), focus=(0.0, 0.0, 0.66), fstop=8.0)
    return frame('poison', set_props(), cam, sky(HDRI, ROT, strength=0.9, res='4k'), 'barkhorn, Poison N3, the crater',
                 lights=lights(), sun=sun_from_sky(HDRI, ROT, irradiance=2.0, angle_deg=6.0), rotate_z=-18.0,
                 position=(0.0, 0.0, STAND - 0.003),
                 haze={'box_m': [-300, -30, -6, 300, 300, 200], 'density': 0.0007, 'anisotropy': 0.4, 'color': '#DCE4D2'},
                 fin=finish(contrast=0.1, clarity=0.05, vignette=0.2))


def portrait():
    return portrait_of(shot(), **camera(height=0.9, distance=6.0, azimuth=-12.0, lens=50.0, target=(0.0, 3.0, 0.9),
                                        focus=(0.0, 0.0, 0.66), fstop=5.6))
