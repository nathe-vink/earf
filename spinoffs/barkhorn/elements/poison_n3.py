"""Poison, N3 (round 31g): a volcanic crater, the poison in the air.

The owner, 2026-10-20: "Took a look at poison. It needs to be outside and incorporate nature. It loses the EARF vibe if
not." The speaker stands on the grey ash rim of a crater; below it a milky turquoise-green acid lake, yellow sulphur
crusted only round the vents at its shore, and sulphur fumes drifting across the frame. It must read as Poison, not
Acid: the yellow kept to the crusts, the water and the fumes in the greens, the sky overcast.

Built from Acid's terrain (kit_ext/acid_el.py: the crust, the lake, the vents, the far crater wall), re-coloured, with
Smoke's volumes (kit_ext/smoke_b_el.py: plume, smoke) for the fumes; scanned boulders (Poly Haven) on the rim.
Pass 2: proof 1 read as a calm lake (the vents too far to register), so the fumaroles now fume a few metres from the
speaker, a TOXIC GAS sign stands at the path's edge, and thick haze replaces the painted-looking far wall.
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
                   flat=[0.0, 0.0, 4.2], stand=STAND, zone_scale=0.35, noise_w=0.9, zone_h=3.0, zone_bias=0.0, res='2k',
                   zones=ZONES, specular=0.05, roughness_min=0.85, tex_scale=0.9,
                   acid_colors=[(0.0, '#B9D8B4'), (0.35, '#8CCBB2'), (0.7, '#5DB7A8'), (1.0, '#3E9C90')], acid_milk=0.45,
                   acid_edge=0.25, acid_deep=0.3, ripple=0.06,
                   # the crater floor: the rim falls away beyond the speaker into one broad lake
                   pools=[[0.0, 34.0, 5.5, 15.0], [-16.0, 34.0, 5.0, 12.0], [16.0, 36.0, 5.0, 12.0]])
    props = [ext('acid_el', 'terrain', **terrain)]
    sulphur = ['#CFC27A', '#B09A3A', '#7A6A2A']     # pass 2: duller, the crust dusted with ash
    # pass 2: the fumaroles brought to the speaker. Sulphur vents a few metres off, crusted yellow, fuming across the
    # frame behind it; the far vents at the shore crusted, their plumes dropped (their boxes showed against the open sky)
    for x, y, h, r, sd in ((1.7, 2.3, 0.4, 0.45, 11), (2.7, 3.5, 0.6, 0.65, 12), (0.9, 3.7, 0.22, 0.28, 13),
                           (-7.0, 19.0, 0.9, 1.0, 2), (4.0, 18.5, 0.7, 0.8, 5)):
        props.append(ext('acid_el', 'chimney', position=[x, y, (STAND if y < 10 else WATER + 0.05) - 0.05], height=h, radius=r,
                         colors=sulphur, tex_scale=1.1, seed=sd))
    for (x, y), z, H, lean, w, dens, sd in (((1.7, 2.3), STAND, 4.5, 1.2, 0.2, 2.2, 1), ((2.7, 3.5), STAND, 6.0, 1.8, 0.28, 1.8, 2),
                                            ((0.9, 3.7), STAND, 3.0, 0.8, 0.12, 1.6, 5),
                                            ):
        props.append(ext('poison_p_el', 'plume_at', base=[x, y], height=H, lean=lean, bend=1.4, width=w, spread=0.32,
                         density=dens, color='#ECEBD8', absorb_color='#B4B08A', anisotropy=0.5, seed=sd, z=z))
    # the warning at the path's edge; one boulder on the rim (the far wall dropped: the haze closes the view)
    props += [ext('poison_p_el', 'sign', position=[-1.45, -0.45, -0.02], rotate=[0, 0, 22], lean=5.0, size=[0.48, 0.34],
                  post=1.15, warning='gas'),
              asset('rock_09', (-2.3, 1.6, -0.15), rotate=(0, 0, 40), scale=12.0)]
    return props


def lights():
    return {'bounce': area(-35, 12, 3.0, 1.2, '#E8ECE0', (2.0, 1.5), (0.0, 0.0, 0.7)),
            'throat': area(14, 4, 2.2, 1.2, '#EEF2E8', (0.7, 0.5), (0.05, -0.05, 1.12))}


def shot():
    cam = camera(height=1.05, distance=4.6, azimuth=-14.0, lens=40.0, target=(0.0, 0.5, 0.75), focus=(0.0, 0.0, 0.66), fstop=8.0)
    return frame('poison', set_props(), cam, sky(HDRI, ROT, strength=0.9, res='4k'), 'barkhorn, Poison N3, the crater',
                 lights=lights(), sun=sun_from_sky(HDRI, ROT, irradiance=2.0, angle_deg=6.0), rotate_z=-18.0,
                 position=(0.0, 0.0, STAND - 0.003),
                 haze={'box_m': [-600, -600, -50, 600, 600, 200], 'density': 0.01, 'anisotropy': 0.4, 'color': '#DCE4D2'},
                 fin=finish(contrast=0.1, clarity=0.05, vignette=0.2))


def portrait():
    return portrait_of(shot(), **camera(height=0.9, distance=6.0, azimuth=-12.0, lens=50.0, target=(0.0, 3.0, 0.9),
                                        focus=(0.0, 0.0, 0.66), fstop=5.6))
