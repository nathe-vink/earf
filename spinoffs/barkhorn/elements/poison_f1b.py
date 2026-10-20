"""Poison, F1 pass 7 (round 31h): A4 whole, with more of the wood's poisons, kept quiet.

The duel of proof 6 against the live A4 (poison_f.md): A4 6.53, F1 5.0, all four judges. They marked F1 down for its
oversized, repeated caps crowding the foreground, its flat backlit speaker, its billboard beech and murky bank, and
the clutter of berries and nightshade; they credited A4's sun and shafts, its redwood, its fern bank and its quiet
troop of small caps. So this keeps A4 as it is (poison_a4.py: the set, the sky, the sun and its canopy gaps, the
cards, the troop) and adds, small and set into the ferns where they grow:
- a few more fly agarics round A4's troop, at its scale;
- death caps at the speaker's foot (olive, white skirt, volva);
- one clump of lords-and-ladies in berry, half in the ferns at the right;
- a yew's red arils as a soft accent far back on the right.
Nothing purple: A4's foxgloves go (the owner: "purple plants (foxgloves) look fake").
"""
import copy

import poison as A
import poison_a4 as A4
from common import piece

MORE_CAPS = [(0.32, -1.45, 0.05, 'young', 91, dict(lean=[0.01, 0.0], wash=0.1, dull=0.3, matte=True, orange=True)),
             (-0.55, -1.2, 0.06, 'convex', 92, dict(lean=[-0.015, 0.01], wash=0.05, dull=0.36, matte=True, orange=True, torn=0.2)),
             (0.48, -1.32, 0.022, 'button', 93, dict(warts=260, dull=0.3, matte=True))]
# the final's realism pass (the owner: "Poison needs more realism too"): two death caps only, set into the moss
DEATHCAPS = [(0.42, -0.5, 0.045, 'convex', 81), (0.52, -0.42, 0.035, 'young', 82)]
SORREL = [(-1.25, -0.9, 0.9, 20), (0.95, -0.75, 0.8, 140), (-0.9, -1.75, 0.7, 260), (1.6, -1.4, 0.85, 80), (-1.7, -0.3, 1.0, 310)]
ARUMS = [(1.05, -1.25, 0.34, 41, [0.02, -0.01], 50), (1.12, -1.2, 0.25, 42, [0.03, 0.015], 36), (1.0, -1.17, 0.29, 43, [-0.02, 0.025], 44),
         (1.08, -1.33, 0.22, 44, [0.0, -0.03], 30)]
YEW = dict(position=[2.6, 3.0, 1.6], rotate=[168, 0, 200], scale=0.5)


def extp(fn, position=(0, 0, 0), **k):
    return piece('ext', module='poison_p_el', fn=fn, position=list(position), **k)


def shot():
    s = copy.deepcopy(A4.shot())
    props = s['set']['props']
    props[:] = [p for p in props if p.get('fn') != 'foxglove']           # no purple: the owner's note
    for x, y, R, age, sd, more in MORE_CAPS:
        more = dict(more); z = -0.045 if age != 'button' else -0.02
        props.append(A4.extb('amanita', (x, y, z), cap=R, age=age, seed=sd, **more))
    for x, y, R, age, sd in DEATHCAPS:
        props.append(A4.extb('amanita', (x, y, -0.055), species='phalloides', cap=R, age=age, seed=sd, dull=0.3, matte=True))
    for x, y, H, sd, lean, n in ARUMS:
        props.append(extp('arum', (x, y, -0.01), height=H, seed=sd, lean=lean, berries=n, berry=0.006, club=0.22 + n / 400,
                          missing=0.15, sss=0.45, sss_scale=0.006, berry_rough=0.3))   # translucent, a waxy bloom, gaps
    props.append(extp('yew', arils=40, aril=0.007, seed=9, value=0.7, **YEW))
    # the read (proof 7's judges: "orange mushrooms"): A4 dulled its caps toward brown and dried them so they would not
    # out-shout the speaker; scarlet with white warts they read as fly agarics (F1 p3 on), still at A4's size
    for p in props:
        if p.get('fn') == 'amanita' and p.get('species', 'muscaria') == 'muscaria':
            p['orange'] = False; p['dull'] = 0.15 if p.get('age') == 'old' else 0.04
            p['matte'] = p.get('age') == 'old'; p['wash'] = min(p.get('wash', 0.15), 0.05)
            k = p.get('seed', 1)
            p['cap'] = round(p['cap'] * (1.0, 1.12, 1.25, 1.35)[k % 4], 3)      # a size up from A4's, unevenly: read at 600 px
            # the final's realism pass (the judges: "toy-like, the most saturated thing in frame"): a real cap's wet
            # scarlet lit by the forest, not glowing; some torn; the stems sunk in the duff
            p['dull'] = max(p.get('dull', 0.0), (0.12, 0.18, 0.24, 0.15)[k % 4])
            if k % 3 == 0:
                p['torn'] = max(p.get('torn', 0.0), 0.35)
            p['position'][2] -= 0.012
    # their dapple off: in A4's sun patch the scarlet washed to salmon; in the shade beside it they keep their red
    for p in props:
        if p.get('fn') == 'canopy':
            p['holes'] = [h for h in p['holes'] if abs(h[0] - p['holes'][-2][0]) > 1e-6 or abs(h[1] - p['holes'][-2][1]) > 1e-6]
    # litter and moss over the caps' feet: one strew per group (a strew scatters over the whole ground before it trims
    # to its circle, so one per cap would be millions of points each)
    for k, (x, y, r) in enumerate(((-0.1, -1.35, 0.6), (0.47, -0.46, 0.16))):
        props.append(A.ext('strew', model='moss_01', on=['prop0-kit'], density=5000, up=0.5, scale=[0.5, 1.1], seed=300 + k,
                           patch=0.05, patch_cut=0.3, within=[x, y, r]))
        props.append(A.ext('strew', model='bark_debris_01', on=['prop0-kit'], density=80.0, up=0.5, scale=[0.12, 0.25],
                           seed=400 + k, within=[x, y, r + 0.05]))
    for p in props:
        # A4's own tells (the calibration critics): the moss under the speaker a decal-like mat, its edge now ragged
        if p.get('fn') == 'strew' and p.get('model') == 'moss_01' and p.get('within') == [0.0, 0.0, 0.42]:
            p['within'] = [0.0, 0.0, 0.58]; p['patch'] = 0.07; p['patch_cut'] = 0.35
        # the ferns all one card: each its own scale and lean
        if p.get('fn') == 'plants' and p.get('model') == 'fern_02':
            for i, q in enumerate(p['place']):
                f = 0.78 + 0.44 * ((i * 37) % 100) / 100
                q[3] = round(q[3] * f, 3)
                if len(q) > 6:
                    q[6] = round(q[6] + ((i * 53) % 31) - 15, 1)
    # wood sorrel, the redwood floor's other plant, in clumps between the ferns
    for x, y, sc, rz in SORREL:
        props.append(piece('asset', model='shrub_sorrel_01', position=[x, y, -0.01], rotate=[0, 0, rz], scale=sc, res='2k'))
    # the litter's repeat broken (a second lookup, turned and scaled, under a broad mask)
    props.append(extp('detile', on=['prop0-kit'], turn=37.0, scale=1.37, mask_m=2.5))
    s['title'] = 'barkhorn, Poison F1b, A4 with more of the wood\'s poisons'
    return s


def portrait():
    s = shot()
    p = A.portrait()
    p['set'], p['sun'], p['lights'], p['title'] = s['set'], s['sun'], s['lights'], s['title'] + ' (4:5)'
    return p
