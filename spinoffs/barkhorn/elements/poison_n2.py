"""Poison, N2 (round 31g): a toxic algae lake at dawn.

The owner, 2026-10-20: "Took a look at poison. It needs to be outside and incorporate nature. It loses the EARF vibe if
not." A still lake, choked with a vivid green cyanobacteria bloom (a paint-like scum in swirls and streaks), dead trees
standing in it, dry sedge at the shore, mist on the water at first light. The speaker stands on an old, half-sunk
jetty; a weathered sign at the water's edge gives the read: DANGER, TOXIC ALGAE, AVOID CONTACT (generic, no agency's
mark). The Bay Area's lakes close each summer for exactly this.

Scanned (Poly Haven, CC0): modular_wooden_pier, dead_tree_trunk_02, grass_medium_02, boulder_01, brown_mud_leaves_01,
the kloofendal_misty_morning sky. Modelled here (kit_ext/poison_p_el.py): the bloom on the water, the sign.
"""
import json
import math
import os

from common import ROOT, area, asset, camera, finish, ground, piece, portrait_of, shot as frame, sky, sun_from_sky

HDRI, ROT = 'kloofendal_misty_morning_puresky', 200.0
WATER = 0.0
PIER_Z = -2.2                      # the scan's deck stands 2.64 m up; sunk so it is 0.44 m clear of the water
DECK = PIER_Z + 2.64


def ext(module, fn, **k):
    return piece('ext', module=module, fn=fn, **k)


# pass 6: three scans, not one pillar cloned: the broad trunk (02), thin snags (dead_tree_trunk, stood up), a
# root-plate stump half drowned by the jetty; at different depths. (model, x, y, z, scale, rz, rx, ring radius)
TREES = (('dead_tree_trunk_02', -5.5, 9.0, -1.2, 1.6, 30, 84, 0.29), ('dead_tree_trunk', -8.0, 15.0, -0.9, 1.6, 110, 90, 0.12),
         ('dead_tree_trunk_02', 6.5, 13.0, -1.4, 1.9, 200, 86, 0.34), ('dead_tree_trunk', 4.2, 24.0, -0.9, 2.3, 70, 88, 0.16),
         ('dead_tree_trunk_02', -15.0, 26.0, -1.2, 2.6, 150, 87, 0.47), ('dead_tree_trunk', -2.6, 30.0, -0.8, 2.0, 20, 91, 0.14),
         ('dead_tree_trunk', 11.0, 34.0, -0.9, 2.6, 250, 89, 0.18), ('tree_stump_02', 2.9, 9.4, -0.32, 1.0, 140, 0, 0.62))
# where the pier scan's legs and posts meet the water, in its own (glTF x, z) frame (read off its mesh at the waterline)
PIER_FEET = [(-1.21, -5.52), (1.14, -5.52), (0.59, -5.53), (-1.2, -8.48), (-0.48, -8.48), (-0.02, -8.45), (0.61, -8.48),
             (1.16, -8.48)]


def pier_xy(gx, gz, at=(0.4, 4.0), turn=4.0):
    x, y = gx, -gz                                        # glTF y-up to z-up
    c, s_ = math.cos(math.radians(turn)), math.sin(math.radians(turn))
    return round(at[0] + c * x - s_ * y, 3), round(at[1] + s_ * x + c * y, 3)


SPK = (0.75, 11.6)                 # pass 4: the speaker out near the jetty's far end, off-centre on its boards


def set_props():
    # pass 6: real water (Acid B's, kit_ext/acid_rain_el.puddle: clear, IOR 1.33, a film of roughness, gentle ripples)
    # over a murky bottom, and the bloom floating on it as its own surface, open where it thins
    props = [piece('box', size=[400.0, 260.0, 0.05], position=[0.0, 60.0, -0.85], material='card', color='#1E2614'),
             ext('acid_rain_el', 'puddle', size=[400.0, 260.0], position=[0.0, 60.0, 0.0], z=WATER, ring=0.7, ripple=0.35, keep=1.0,
                 roughness=0.02, ripple_m=0.0012, tint_lin=(0.42, 0.5, 0.3), seed=9),
             ext('poison_p_el', 'algae_water', position=[0.0, 60.0, WATER + 0.004], size=[400.0, 260.0], cover=0.7, drift=20.0, scum_rough=0.35, float=True,
                 edge=[0.06, 0.55], lane=[0.45, 1.6],    # pass 7: soft, oily edges; open water along the jetty
                 streak=1.7, scale=0.12, clots=0.45, clot_scale=1.4,
                 greens=['#3E5A10', '#7A9A1C', '#C2D040']),          # pass 4: pea-soup yellow-green, off the speaker's bottle green;
                                                                  # pass 5: more open, glossy water between, a wet sheen on the scum
             ground('brown_mud_leaves_01', size=(14.0, 5.0), position=(0.0, -4.2, -0.12), displace=0.03, relief=0.22,
                    res='2k', flat=False),
             # the old jetty out into the lake, its gantry and rope taken off (pass 4): plain mooring posts
             ext('poison_p_el', 'scan', model='modular_wooden_pier', position=[0.4, 4.0, PIER_Z], rotate=[0, 0, 4], scale=1.0,
                 res='2k', drop=['section_05']),
             # the sign, a supporting player: small, leaning, in the shallows by the jetty, out of focus
             ext('poison_p_el', 'sign', position=[-1.55, 10.2, -0.1], rotate=[0, 0, 26], lean=7.0, size=[0.5, 0.36], post=1.15,
                 bolts=True)]   # pass 5: a size up, nearer; pass 6: clear of the jetty's posts, bolted to its own
    # dead trees standing in the water, fading into the mist
    for model, x, y, z, s, rz, rx, _ in TREES:
        props.append(piece('asset', model=model, position=[x, y, z], rotate=[0, -rx, rz], scale=s, res='2k'))   # stood up
    # pass 5: scum banked round the stumps, the jetty's legs and the sign's post, so they stand in the water, not on it
    props.append(ext('poison_p_el', 'scum_rings', items=[[x, y, r] for _, x, y, _, _, _, _, r in TREES] + [[-1.55, 10.25, 0.06]]
                     + [[*pier_xy(gx, gz), 0.12] for gx, gz in PIER_FEET],
                     width=0.4, color='#A6BC34', seed=7))
    # reeds along the left edge of the jetty, in the shallows
    for x, y, s, rz in ((-2.6, 8.4, 1.5, 0), (-2.3, 9.8, 1.3, 70), (-3.1, 10.6, 1.7, 140), (-2.5, 11.8, 1.4, 30),
                        (-3.5, 12.8, 1.6, 200), (-2.8, 14.0, 1.2, 260), (3.0, 9.0, 1.3, 90), (3.5, 10.4, 1.5, 300)):
        props.append(piece('asset', model='grass_medium_02', position=[x, y, -0.06], rotate=[0, 0, rz], scale=s, res='2k'))
    props.append(ext('smoke_b_el', 'mist', box=[-60.0, -6.0, -0.2, 60.0, 90.0, 4.0], clear_y=4.0, full_y=30.0, density=0.016,
                     ground_boost=5.0, ground_h=0.7, color='#EEF0E8', anisotropy=0.72))
    for x, y, rz, s_ in ((2.2, 9.4, 30, 0.7), (-1.4, 12.8, 110, 0.6), (2.8, 13.4, 200, 0.8), (-1.6, 8.2, 70, 0.5)):
        props.append(piece('asset', model='dry_branches_medium_01', position=[x, y, -0.02], rotate=[0, 0, rz], scale=s_, res='2k'))
    # pass 6: everything standing in the water darkened and wet at its waterline (after the pieces it wets)
    props.append(ext('poison_p_el', 'wetline', models=['modular_wooden_pier', 'dead_tree_trunk', 'tree_stump', 'weathered_planks',
                                                       'dry_branches'], z=WATER, top=0.08, color='#3E3A26', wet_rough=0.22))
    return props


def lights():
    """Acid B's rig (acid_b.py pass 9, 6.0 blind outdoors with this speaker), moved to the speaker on the jetty: a soft
    bounce from the camera's side, two small cards low in front (the horn's throat, the woofer), a rim card behind on
    the sun's side that lights the speaker alone."""
    x, y = SPK
    t = lambda z: (x, y, DECK + z)
    L = {'bounce': area(-40, 8, 3.5, 2.5, '#F1E6B8', size=(2.0, 2.0), target=t(0.5)),
         'throat': area(-8, 4, 2.2, 0.5, '#F1E6B8', size=(0.5, 0.4), target=t(1.15)),
         'low': area(-5, 3, 2.5, 1.5, '#F1E6B8', size=(0.5, 0.5), target=t(0.3)),
         'rim': area(-130, 5, 3.0, 9.0, '#F6DDB0', size=(1.5, 1.5), target=t(0.5))}
    L['rim']['receivers'] = sorted(json.load(open(os.path.join(ROOT, 'spinoffs/barkhorn/out-cloud/render/barkhorn-cloud.json')))['parts'])
    return L


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
