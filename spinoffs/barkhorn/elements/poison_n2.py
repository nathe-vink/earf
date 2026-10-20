"""Poison, N2 (round 31g): a toxic algae lake at dawn.

The owner, 2026-10-20: "Took a look at poison. It needs to be outside and incorporate nature. It loses the EARF vibe if
not." A still lake, choked with a vivid green cyanobacteria bloom (a paint-like scum in swirls and streaks), dead trees
standing in it, dry sedge at the shore, mist on the water at first light. The speaker stands on an old, half-sunk
jetty; a weathered sign at the water's edge gives the read: DANGER, TOXIC ALGAE, AVOID CONTACT (generic, no agency's
mark). The Bay Area's lakes close each summer for exactly this.

Scanned (Poly Haven, CC0): modular_wooden_pier, dead_tree_trunk_02, grass_medium_02, boulder_01, brown_mud_leaves_01,
the kloofendal_misty_morning sky. Modelled here (kit_ext/poison_p_el.py): the bloom on the water, the sign.
"""
import math

from common import area, asset, camera, finish, ground, piece, portrait_of, shot as frame, sky, sun_from_sky

HDRI, ROT = 'kloofendal_misty_morning_puresky', 200.0
WATER = 0.0
PIER_Z = -2.2                      # the scan's deck stands 2.64 m up; sunk so it is 0.44 m clear of the water
DECK = PIER_Z + 2.64


def ext(module, fn, **k):
    return piece('ext', module=module, fn=fn, **k)


TREES = ((-5.5, 9.0, 1.6, 30, 84), (-9.0, 16.0, 2.2, 110, 88), (6.5, 13.0, 1.9, 200, 86),
         (12.0, 22.0, 2.4, 70, 89), (-15.0, 26.0, 2.6, 150, 87), (3.0, 30.0, 2.8, 20, 88))
# where the pier scan's legs and posts meet the water, in its own (glTF x, z) frame (read off its mesh at the waterline)
PIER_FEET = [(-1.21, -5.52), (1.14, -5.52), (0.59, -5.53), (-1.2, -8.48), (-0.48, -8.48), (-0.02, -8.45), (0.61, -8.48),
             (1.16, -8.48)]


def pier_xy(gx, gz, at=(0.4, 4.0), turn=4.0):
    x, y = gx, -gz                                        # glTF y-up to z-up
    c, s_ = math.cos(math.radians(turn)), math.sin(math.radians(turn))
    return round(at[0] + c * x - s_ * y, 3), round(at[1] + s_ * x + c * y, 3)


SPK = (0.75, 11.6)                 # pass 4: the speaker out near the jetty's far end, off-centre on its boards


def set_props():
    props = [ext('poison_p_el', 'algae_water', position=[0.0, 60.0, WATER], size=[400.0, 260.0], cover=0.62, drift=20.0, scum_rough=0.35,
                 streak=1.7, scale=0.12, clots=0.45, clot_scale=1.4,
                 greens=['#3E5A10', '#7A9A1C', '#C2D040']),          # pass 4: pea-soup yellow-green, off the speaker's bottle green;
                                                                  # pass 5: more open, glossy water between, a wet sheen on the scum
             ground('brown_mud_leaves_01', size=(14.0, 5.0), position=(0.0, -4.2, -0.12), displace=0.03, relief=0.22,
                    res='2k', flat=False),
             # the old jetty out into the lake, its gantry and rope taken off (pass 4): plain mooring posts
             ext('poison_p_el', 'scan', model='modular_wooden_pier', position=[0.4, 4.0, PIER_Z], rotate=[0, 0, 4], scale=1.0,
                 res='2k', drop=['section_05']),
             # the sign, a supporting player: small, leaning, in the shallows by the jetty, out of focus
             ext('poison_p_el', 'sign', position=[-1.2, 10.2, -0.1], rotate=[0, 0, 26], lean=9.0, size=[0.5, 0.36], post=1.15)]   # pass 5: a size up, nearer
    # dead trees standing in the water, fading into the mist
    for x, y, s, rz, rx in TREES:
        props.append(piece('asset', model='dead_tree_trunk_02', position=[x, y, -1.2], rotate=[0, -rx, rz], scale=s, res='2k'))   # stood up
    # pass 5: scum banked round the stumps, the jetty's legs and the sign's post, so they stand in the water, not on it
    props.append(ext('poison_p_el', 'scum_rings', items=[[x, y, 0.18 * s] for x, y, s, _, _ in TREES] + [[-1.2, 10.25, 0.06]]
                     + [[*pier_xy(gx, gz), 0.12] for gx, gz in PIER_FEET],
                     width=0.4, color='#A6BC34', seed=7))
    # reeds along the left edge of the jetty, in the shallows
    for x, y, s, rz in ((-2.6, 8.4, 1.5, 0), (-2.3, 9.8, 1.3, 70), (-3.1, 10.6, 1.7, 140), (-2.5, 11.8, 1.4, 30),
                        (-3.5, 12.8, 1.6, 200), (-2.8, 14.0, 1.2, 260), (3.0, 9.0, 1.3, 90), (3.5, 10.4, 1.5, 300)):
        props.append(piece('asset', model='grass_medium_02', position=[x, y, -0.06], rotate=[0, 0, rz], scale=s, res='2k'))
    props.append(ext('smoke_b_el', 'mist', box=[-60.0, -6.0, -0.2, 60.0, 90.0, 4.0], clear_y=10.0, full_y=45.0, density=0.016,
                     ground_boost=5.0, ground_h=0.7, color='#EEF0E8', anisotropy=0.72))
    for x, y, rz, s_ in ((2.2, 9.4, 30, 0.7), (-1.4, 12.8, 110, 0.6), (2.8, 13.4, 200, 0.8), (-1.6, 8.2, 70, 0.5)):
        props.append(piece('asset', model='dry_branches_medium_01', position=[x, y, -0.02], rotate=[0, 0, rz], scale=s_, res='2k'))
    return props


def lights():
    """Poison A's rig (poison.py, the final that scored 6.5 blind with this speaker), moved to the speaker on the jetty:
    the cool reflector, the warm diffuse bounce, the card overhead."""
    x, y = SPK
    def orb(az, el, d):
        return {'azimuth_deg': az, 'elevation_deg': el, 'distance_m': d}
    return {'reflector': {'type': 'area', 'size_m': [2.0, 1.5], 'target': [x, y, DECK + 0.7], 'irradiance': 3.0,
                          'color': '#EEF0E0', 'orbit': orb(-35, 10, 2.8)},
            'bounce': {'type': 'area', 'size_m': [2.0, 1.5], 'target': [x, y, DECK + 0.6], 'irradiance': 3.5, 'color': '#E8D9B0',
                       'orbit': orb(10, 25, 2.5), 'specular': 0.0},
            'card': {'type': 'area', 'size_m': [2.0, 2.0], 'target': [x, y, DECK + 1.1], 'irradiance': 1.0, 'color': '#F0F2E6',
                     'orbit': orb(60, 45, 2.5), 'specular': 0.3}}


def shot():
    x, y = SPK
    # low, from along the jetty: the boards lead to the speaker, turned three-quarter
    cam = camera(height=DECK + 0.6, distance=5.4, azimuth=-6.0, lens=35.0, target=(x - 0.5, y, DECK + 0.7),
                 focus=(x, y, DECK + 0.6), fstop=3.5)
    return frame('poison', set_props(), cam, sky(HDRI, ROT, strength=0.35, res='4k'), 'barkhorn, Poison N2, the algae lake',
                 lights=lights(), sun={'azimuth_deg': -100.0, 'elevation_deg': 11.0, 'irradiance': 40.0, 'angle_deg': 0.8, 'color': '#FFC98C'}, rotate_z=-38.0,
                 position=(x, y, DECK - 0.003), fin=finish(contrast=0.08, clarity=0.05, vignette=0.18))


def portrait():
    x, y = SPK
    return portrait_of(shot(), **camera(height=DECK + 0.7, distance=5.6, azimuth=-6.0, lens=42.0,
                                        target=(x - 0.2, y, DECK + 0.95), focus=(x, y, DECK + 0.6), fstop=5.6))
