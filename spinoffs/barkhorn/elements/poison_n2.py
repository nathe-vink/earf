"""Poison, N2 (round 31g): a toxic algae lake at dawn.

The owner, 2026-10-20: "Took a look at poison. It needs to be outside and incorporate nature. It loses the EARF vibe if
not." A still lake, choked with a vivid green cyanobacteria bloom (a paint-like scum in swirls and streaks), dead trees
standing in it, dry sedge at the shore, mist on the water at first light. The speaker stands on an old, half-sunk
jetty; a weathered sign at the water's edge gives the read: DANGER, TOXIC ALGAE, AVOID CONTACT (generic, no agency's
mark). The Bay Area's lakes close each summer for exactly this.

Scanned (Poly Haven, CC0): modular_wooden_pier, dead_tree_trunk_02, grass_medium_02, boulder_01, brown_mud_leaves_01,
the kloofendal_misty_morning sky. Modelled here (kit_ext/poison_p_el.py): the bloom on the water, the sign.
"""
from common import area, asset, camera, finish, ground, piece, portrait_of, shot as frame, sky, sun_from_sky

HDRI, ROT = 'kloofendal_misty_morning_puresky', 200.0
WATER = 0.0
PIER_Z = -2.2                      # the scan's deck stands 2.64 m up; sunk so it is 0.44 m clear of the water
DECK = PIER_Z + 2.64


def ext(module, fn, **k):
    return piece('ext', module=module, fn=fn, **k)


def set_props():
    props = [ext('poison_p_el', 'algae_water', position=[0.0, 20.0, WATER], size=[120.0, 90.0], cover=0.74, drift=20.0, scum_rough=0.3,
                 streak=1.7, scale=0.12, clots=0.45, clot_scale=1.4,
                 greens=['#1A3E10', '#357A1A', '#6AAE24']),
             # the near shore: mud and leaves, dipping under the bloom at its edge
             ground('brown_mud_leaves_01', size=(14.0, 5.0), position=(0.0, -4.2, -0.12), displace=0.03, relief=0.22,
                    res='2k', flat=False),
             # the old jetty out into the lake, the speaker on its boards
             piece('asset', model='modular_wooden_pier', position=[0.4, 4.0, PIER_Z], rotate=[0, 0, 4], scale=1.0, res='2k'),
             ext('poison_p_el', 'sign', position=[-1.25, -0.5, -0.1], rotate=[0, 0, -24], lean=7.0, size=[0.48, 0.34], post=1.15)]
    # dead trees standing in the water, fading into the mist
    for x, y, s, rz, rx in ((-5.5, 9.0, 1.6, 30, 84), (-9.0, 16.0, 2.2, 110, 88), (6.5, 13.0, 1.9, 200, 86),
                            (12.0, 22.0, 2.4, 70, 89), (-15.0, 26.0, 2.6, 150, 87), (3.0, 30.0, 2.8, 20, 88)):
        props.append(piece('asset', model='dead_tree_trunk_02', position=[x, y, -0.4], rotate=[0, -rx, rz], scale=s, res='2k'))   # stood up
    # dry sedge along the shore and in the shallows
    for x, y, s, rz in ((-2.8, -2.0, 1.6, 0), (-2.1, -1.4, 1.3, 70), (2.3, -1.6, 1.5, 140), (3.1, -0.8, 1.7, 30),
                        (-3.6, -0.6, 1.4, 200), (1.6, -2.4, 1.2, 260), (-0.9, -2.6, 1.0, 90), (4.2, -1.9, 1.5, 300)):
        props.append(piece('asset', model='grass_medium_02', position=[x, y, -0.06], rotate=[0, 0, rz], scale=s, res='2k'))
    props += [piece('asset', model='boulder_01', position=[-2.6, -2.6, -0.35], rotate=[0, 0, 40], scale=0.7, res='2k'),
              piece('asset', model='boulder_01', position=[2.9, -3.0, -0.45], rotate=[0, 0, 210], scale=0.55, res='2k'),
              # mist lying on the water, thicker with distance
              ext('smoke_b_el', 'mist', box=[-60.0, -6.0, -0.2, 60.0, 80.0, 12.0], clear_y=-4.0, full_y=24.0, density=0.05,
                  ground_boost=3.5, ground_h=1.8, color='#EEF0E8', anisotropy=0.72)]
    for x, y, rz, s_ in ((1.8, 0.4, 30, 0.7), (-0.4, 2.6, 110, 0.6), (2.6, 3.4, 200, 0.8), (-2.2, 1.2, 70, 0.5)):
        props.append(piece('asset', model='dry_branches_medium_01', position=[x, y, -0.02], rotate=[0, 0, rz], scale=s_, res='2k'))
    return props


def lights():
    return {'bounce': area(-30, 12, 3.0, 1.0, '#F2EDE2', (2.0, 1.5), (0.4, 1.0, DECK + 0.7)),
            'key': {**area(-40, 55, 3.0, 1.4, '#F4EEE2', (1.6, 1.6), (0.4, 1.0, DECK + 0.5)), 'volume': False},
            'throat': area(14, 6, 2.4, 0.9, '#F4F0E6', (0.7, 0.5), (0.45, 0.95, DECK + 1.12))}


def shot():
    cam = camera(height=DECK + 0.95 - 0.0, distance=5.2, azimuth=-14.0, lens=40.0, target=(0.4, 1.0, DECK + 0.75),
                 focus=(0.4, 1.0, DECK + 0.66), fstop=3.5)
    return frame('poison', set_props(), cam, sky(HDRI, ROT, strength=1.0, res='4k'), 'barkhorn, Poison N2, the algae lake',
                 lights=lights(), sun={'azimuth_deg': 165.0, 'elevation_deg': 9.0, 'irradiance': 5.0, 'angle_deg': 2.5, 'color': '#FFCF98'}, rotate_z=-16.0,
                 position=(0.4, 1.0, DECK - 0.003), fin=finish(contrast=0.08, clarity=0.05, vignette=0.18))


def portrait():
    return portrait_of(shot(), **camera(height=DECK + 0.95, distance=5.4, azimuth=-14.0, lens=45.0,
                                        target=(0.4, 1.0, DECK + 0.95), focus=(0.4, 1.0, DECK + 0.66), fstop=5.6))
