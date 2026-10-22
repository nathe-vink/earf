"""Smoke, setting E12r: the meteor on the road. The owner, 2026-10-21: "I meant it would look cool if the speaker was
enveloped in this particular fire/smoke, like it's an asteroid that just burned through the atmosphere and came crashing
into a road or salt flats." E12 is the salt flats; this is the road, and the fire he pointed at is the bridge's own.

E10's overpass at blue hour (smoke_e10.py: its camera, lamps, wet deck, the two cold wrecks and the far fires), less its
near burning car: the speaker is the fire now. It came down along the near lane and skidded: E8's gouge
(smoke_impact.py; the owner, 2026-10-20: "like the speaker slid along the asphalt and ground it up, like an asteroid
might") runs twenty metres back from it to where it struck, the asphalt torn up in plates along both lips, the sub-base
bare and scorched in the trench, debris thrown wide, plates shoved up and over at its end. The speaker stands sunk in
the trench's end and E12's fire wraps it (the flow round the speaker, its skin burning: E12's solve fits as made, the
speaker turned the same and the camera eight degrees round from E6's), its smoke rolling up and away to the right.

p2, after proof 1: E9's far fires are gone too (a riot's, not a crash's: one sat at road level by the left railing
with nothing under it, the other just behind a cold wreck, so it read as burning); the torn road is darkened to read as
asphalt and its bared aggregate (the slabs' and chips' broken faces came out "pale cream, like concrete blocks dumped
in a line": the kit's tints shift hue only).

p4, after proof 3's critics (realism 6 and 5; the duels with E9 split): "the fire hardly lights anything", "no warm pool
on the asphalt", the box "spotless, upright, level ... dropped in", "procedural Voronoi" rubble "laid in a tidy row" with
"no gravel, grit or dust", "no crater or depression, no radial cracking ..., no scorching". So: the fire is the key, its
lamps up among the flames and four times as strong (E12's were made for a salt pan in daylight); the flames brighter, so
their cores clip; the speaker canted, pitched forward onto its face as it dug in; the road charred, cracked out from it
and round it, sooted and dusted; the torn asphalt black right through, its broken edges rounded and showing its stones,
the plates of every size, scattered off the lips, some on their backs and some fallen in, and loose rubble down the
trench's floor.

p5, after proof 4's critics (realism 5 and 5, the duels with E9 split again): "the fire barely lights the scene ... no
pool of light fading with distance" (the frame's foreground lay wholly inside the pool its high lamps spread: the light
now comes mostly from low in the flames, so the pool falls away within the frame, under a cooler white balance that
keeps the dusk blue-grey round it); "the flames ... beside and behind it, not on it", "still isn't enveloped" (meteor_d:
the fire on its front corners and foot too, as the owner asked, "enveloped in this particular fire/smoke"), with a lamp
for them on its face; "a vintage CRT television" (the fire behind it glowed in its smoked horn like a screen: the fire
is unseen through its clear parts); "no embers"; the slabs "cut paving tiles", "boards" (the heave lower and thinner,
the chips less rounded, their broken edges lighter than their tops, as asphalt's stones are); "perfectly upright"
(canted further); the trench's walls, a pale ruled line, gone.
"""
import copy
import math

import smoke_bridge
import smoke_e10 as B
import smoke_e12 as M
import smoke_impact as I
from common import piece, point

NEAR = [-1.2, 15.0]                  # E10's burning car, across the gouge's line: the speaker is the fire now
# the torn asphalt (impact.py): black right through, its stones in the broken edges, the sub-base grey under it
ASPHALT = dict(top_value=0.4, under_tint='#1C1C1C', under_value=0.3, side='asphalt_02', side_value=0.9)
TILT = [6.0, -2.5]                   # the speaker pitched forward onto its face as it dug in, and to its left
WB = (4800, 10.0)                    # the white point: the dusk blue-grey round the fire's warm pool (p4's read pink throughout)
STRENGTH = 420.0                     # the flames (E12's 220 on a sunlit pan): the cores clip at dusk
CACHE = 'renders/2026-10-21/barkhorn/plume/meteor_d.npz'   # meteor_c with fire on the speaker's front corners and foot


def torn(gouge):
    """E8's gouge (smoke_impact.gouge) torn as a meteor would tear it: see the p4 note above."""
    for p in gouge:
        fn = p.get('fn')
        if fn == 'trench':
            p['value'] = 0.45
        elif fn == 'slabs':
            p.update(ASPHALT, crumble=1.2)
            if p['count'] == 90:                                     # along the lips
                p.update(count=130, spread=0.7, flip=0.12, fallen=0.12, size_power=1.6)
            else:                                                    # the heave in front: thinner, lower, more of them
                p.update(thickness=0.045, size=0.45, count=28, tilt=40.0, tilt_min=15.0)
        elif fn == 'debris':
            if p.get('fine'):                                        # the grit: crushed stone, grey
                p.update(under_tint='#1C1C1C', under_value=0.6)
            else:
                p.update(ASPHALT, crumble=0.3, count=min(p['count'], 300))
    # loose rubble down the trench's floor (p3: "as smooth and clean as the undamaged road"), clear of the speaker
    return gouge + [piece('ext', module='impact', fn='debris', y0=I.Y0 + 6.0, y1=-0.9, count=260, reach=0.6, inner=0.0,
                          z=-0.32, seed=19, rotate_z=I.FLIP, crumble=0.5, **ASPHALT)]


def marks(deck_len):
    """The blow's marks on the road round the speaker (smoke_el.impact on the deck's slabs either side and in front,
    and on the trench): charred black near it, sooted further, cracked out from it and round it, and dusted with what
    it threw."""
    # the char reaches past the fire's hottest light: within a metre and a half its lamps lit the black as bright as the
    # open road (a top-down test without them showed it there), so a scorch that small read as none
    road = dict(module='smoke_el', fn='impact', centre=[0.0, 0.0], char=[1.0, 2.6], jag=0.8, soot=4.5, soot_mix=0.55,
                cracks=[0.9, 3.8], crack_count=13.0, crack_width=0.012, crack_bump=0.6, dust=[1.6, 5.5], dust_mix=0.5,
                seed=4)
    return [piece('ext', on=f'prop{i}-kit', **road) for i in (0, 1, 3)] + \
        [piece('ext', module='smoke_el', fn='impact', on=f'prop{deck_len}-kit', centre=[0.0, 0.0], char=[0.5, 2.0],
               jag=0.7, soot=3.0, soot_mix=0.5)]


def firelight():
    """The fire as the scene's key at dusk: a lamp in the flames on each flank and one behind, at their middle height,
    warm, hidden from the lens, from rays through glass and from reflections as E12's are (smoke_e12.firelight). E12's
    own, made for a salt pan in daylight, sat just above this road at 260 W and lit nothing (p3: "the asphalt right
    beside the flames stays cool grey"): these light a pool on the road falling away over a few metres, the rubble's
    faces toward the flames and the box's flanks, and throw the rubble's shadows away from it. A flame is a tall
    source, so each flank's light comes from two lamps, low and high, most of it high: one lamp at its middle laid a
    hot spot at its foot that lit the charred road there as bright as the open road. They leave the smoke to a lamp of
    its own, low in the flames and weaker (the look at full strength lit the column's foot like a fireball)."""
    a = math.radians(M.ROT)
    out = {}
    for k, (x, y, z, w, v) in enumerate([(-0.6, 0.1, 0.55, 600.0, False), (-0.6, 0.1, 1.5, 300.0, False),
                                         (0.6, 0.15, 0.5, 600.0, False), (0.6, 0.15, 1.4, 300.0, False),
                                         (0.0, 0.55, 1.3, 500.0, False), (0.0, -0.4, 0.8, 180.0, False),
                                         (0.0, 0.35, 0.8, 600.0, 'only')]):
        out[f'flame{k}'] = dict(point([round(x * math.cos(a) - y * math.sin(a), 3),
                                       round(x * math.sin(a) + y * math.cos(a), 3), round(z + I.SINK, 3)], w, '#FF7A2E',
                                      0.3 if v is False else 0.5),
                                camera=False, transmission=False, specular=0.0, volume=v)
    return out


def shot():
    s = copy.deepcopy(B.shot())
    props = s['set']['props']
    rest = [p for p in props[len(smoke_bridge.deck()):] if (p.get('position') or [])[:2] != NEAR
            and not (p.get('module') == 'plume')]                   # the near car's fire and the far fires
    for p in rest:
        if p.get('fn') == 'occluder':                                # the contact shadow, down in the trench with it
            p['position'] = [0.0, 0.0, round(I.SINK + 0.012, 3)]
    fire = M.fire(CACHE)
    fire['position'] = [0.0, 0.0, I.SINK]                           # the solve's floor at the speaker's foot
    fire['strength'] = STRENGTH
    deck = [p for p in I.deck() if p.get('size', [0.0])[0] != 0.03]   # the trench's walls in section: firelit, a pale
    fire['through_glass'] = False                                     # ruled line along the lip (the trench has walls)
    embers = piece('scatter', count=60, radius=[0.002, 0.006], position=[0.0, 0.0, 0.9], material='glow',
                   color='#FF8A30', emit=40.0, seed=27, plume={'height': 3.5, 'spread': [0.2, 1.4], 'lean': [1.2, 0.4],
                                                              'taper': 0.7})
    props[:] = deck + torn(I.gouge()) + rest + [fire, embers] + marks(len(deck))
    for k in ('fire0', 'firerim0', 'farfire0', 'farfire1'):
        s['lights'].pop(k)
    s['lights'].update(firelight())
    # the bounce on the speaker's face is the fire-lit road's now, warm (p3: "a flat, neutral grey light")
    s['lights']['bounce'].update(color='#D9A27A', irradiance=3.0)
    for inst in s['product']['instances']:
        inst['position'] = [inst['position'][0], inst['position'][1], I.SINK]
        inst['tilt'] = TILT
    s['finish']['grain'] = 3.5                                       # p3: "grain-free and lens-clean"
    s['render']['white_balance_k'], s['render']['white_balance_tint'] = WB
    _aim(s['camera'])
    s['title'] = 'barkhorn, Smoke E12r, the meteor on the road: the speaker skidded to rest in its gouge, burning'
    return s


def _aim(cam):
    """E10's framing on the speaker sunk in the trench: the aim and the focus down with it (the look at E10's own had its
    foot out of frame)."""
    for k in ('target', 'focus'):
        cam[k] = [cam[k][0], cam[k][1], round(cam[k][2] + I.SINK, 4)]


def portrait():
    sh = shot()
    p = B.portrait()
    p['set'], p['lights'], p['product'], p['title'] = sh['set'], sh['lights'], sh['product'], sh['title'] + ' (4:5)'
    p['finish'] = sh['finish']
    _aim(p['camera'])
    return p
