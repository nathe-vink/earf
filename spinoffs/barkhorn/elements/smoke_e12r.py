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

p6, after proof 5's critics (realism 5 and 5; it beat E9 in both orders, the first meteor proof to): "the fire lights
almost nothing around it ... no falloff and no shadows cast by the fire" (a strong lamp above the flames, so their light
reaches the road, the cars and the rubble's rims ten metres off and throws their shadows outward; the low ones weaker,
and rubble strewn over the pit's floor, "a clean tray"); the embers "tiny, sharp, round dots ... a starfield" (fewer,
finer, bunched low, each drawn out along its path as a spark smears in an exposure); the rubble "thin, flat,
clean-edged plates ... slate tiles or cardboard" with "a glossy, slate-like sheen" (thick crumbling lumps, matte); "no
halation" (bloom); "upright and level" (rolled further over onto its left); the scorch "a flat dark streak ... like a
decal" (fainter), the cracks and dust bolder; the lamp on its face gone (it turned E12's black cabinet bronze). Its
first look's rubble came out as crystals and crumpled paper (every face tented, flat-shaded): the tops are flat again,
only the broken edges tented, shaded smooth across the gentle edges, the undersides and edges darker; and rubble strewn
either side of its foot, where the low flames lit the pit's floor as two flat orange shelves. And the speaker and its
whole fire turned 25 degrees: face on, its horn's mouth read as a screen (every read test: "an old CRT television ... on
top of a dark box"); turned, it shows its flare and its driver, and both blind duels of the two looks chose it ("reads
as a horn loudspeaker"), its smoke now rising straight up out of the crash.

p7, after proof 6's critics (realism 5 and 5; it beat p5, 7 to 6, but lost both duels with E9, 4 to 6, where p5 had won
both): the rubble "sharp, faceted, near-black shards ... a heap of coal or low-poly rocks", "thin, clean-edged tan slabs
... broken plasterboard" (impact.py's rough: each piece's broken edges a fracture's face, uneven but whole; tried close
up first); "an even, fine dried mud crack pattern ... on a smooth, light pinkish-beige surface" whose "warm tint does not
fade with distance" (the cracks and dust back to p5's, and the fire's high lamp lower and weaker so its light falls away
within a metre or two, the low ones stronger); "its horn knocked crooked" (the roll back to p5's); the turned horn on its
posts "a stage spotlight or a camera on a stand", the woofer hidden (meteor_e: the speaker solved turned, against the
wind as before, so the smoke leans away right again instead of rising "a mushroom ... an explosion cloud", its face
quieter so the woofer shows through thinner flames); the embers "identical round dots ... to the top of the frame"
(longer streaks, each tilted, lower and denser over the fire); and "no heat haze" (finish.haze, the speaker kept still).
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
ASPHALT = dict(top_value=0.28, under_tint='#1C1C1C', under_value=0.2, side='asphalt_02', side_value=0.6, top_rough=1.0,
               side_rough=1.0, flat_tops=True, smooth=30.0, rough=0.07)
TILT = [6.0, -2.5]                   # the speaker pitched forward onto its face as it dug in, and a little to its left
                                     # (p6's -6 read as "its horn knocked crooked ... being destroyed rather than arriving")
TURN = 25.0                          # the speaker turned so the horn shows its flare (face on, it read as "a vintage CRT
                                     # television"): meteor_e is solved with it so, against the same wind
# the shimmer over the fire (finish.haze), in each frame's fractions: the rising air either side of and above the
# speaker, the speaker itself kept still
HAZE = dict(box=[0.34, 0.2, 0.68, 0.9], px=2.0, scale=6.0, exclude=[[0.42, 0.55, 0.59, 0.93]])
HAZE_PORTRAIT = dict(box=[0.33, 0.25, 0.68, 0.8], px=2.0, scale=6.0, exclude=[[0.4, 0.54, 0.61, 0.79]])
WB = (4800, 10.0)                    # the white point: the dusk blue-grey round the fire's warm pool (p4's read pink throughout)
STRENGTH = 420.0                     # the flames (E12's 220 on a sunlit pan): the cores clip at dusk
CACHE = 'renders/2026-10-21/barkhorn/plume/meteor_e.npz'   # meteor_d with the speaker turned 25 degrees against the wind,
                                                            # its face quieter so the woofer shows


def torn(gouge):
    """E8's gouge (smoke_impact.gouge) torn as a meteor would tear it: see the p4 note above."""
    for p in gouge:
        fn = p.get('fn')
        if fn == 'trench':
            p['value'] = 0.45
        elif fn == 'slabs':
            p.update(ASPHALT, crumble=2.0)
            if p['count'] == 90:                                     # along the lips: thick crumbling lumps (p5: "thin,
                p.update(count=130, spread=0.7, flip=0.12, fallen=0.12, size_power=1.6, thickness=0.1)   # even sheets")
            else:                                                    # the heave in front: lower, more of them
                p.update(thickness=0.09, size=0.45, count=28, tilt=40.0, tilt_min=15.0)
        elif fn == 'debris':
            if p.get('fine'):                                        # the grit: crushed stone, grey
                p.update(under_tint='#1C1C1C', under_value=0.6)
            else:
                p.update(ASPHALT, crumble=0.6, count=min(p['count'], 300))
        elif fn == 'scorch':                                         # p5: "a flat dark streak ... like a decal"
            p['strength'] = 0.55
    # loose rubble down the trench's floor (p3: "as smooth and clean as the undamaged road"), clear of the speaker, and
    # over the floor of its pit in front of it, on the slope up to the road in three bands (p5: "a smooth, orange-lit
    # sloped floor with straight edges ... a clean tray")
    pit = [piece('ext', module='impact', fn='debris', y0=y0, y1=y0 + 0.75, count=70, reach=0.55, inner=0.0, z=z,
                 seed=31 + i, rotate_z=I.FLIP, crumble=0.3, **ASPHALT)
           for i, (y0, z) in enumerate([(-0.6, -0.3), (-0.35, -0.2), (-0.1, -0.09)])]
    # and either side of it, where the low flames light the pit's floor (p6's look: two flat orange shelves)
    pit.append(piece('ext', module='impact', fn='debris', band=[-0.45, 0.45], count=90, reach=0.55, inner=0.4, z=I.SINK,
                     seed=35, rotate_z=I.FLIP, crumble=0.3, **ASPHALT))
    return gouge + pit + [piece('ext', module='impact', fn='debris', y0=I.Y0 + 6.0, y1=-0.9, count=260, reach=0.6,
                                inner=0.0, z=-0.32, seed=19, rotate_z=I.FLIP, crumble=0.5, **ASPHALT)]


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
    a = math.radians(M.ROT + TURN)
    out = {}
    # p6: and the fire's whole light from above it, strong, so it reaches the road, the cars and the rubble's rims ten
    # metres off and throws their shadows outward (p5: "the fire lights almost nothing around it"); the low ones weaker,
    # so its pit is no longer a lit tray
    # p7: lower and weaker (p6's lit the whole foreground evenly, "the warm light covers the whole foreground", read as a
    # grade and not a fire's light: from lower its light falls away faster), the low ones stronger
    for k, (x, y, z, w, v) in enumerate([(-0.6, 0.1, 0.55, 500.0, False), (-0.6, 0.1, 1.5, 300.0, False),
                                         (0.6, 0.15, 0.5, 500.0, False), (0.6, 0.15, 1.4, 300.0, False),
                                         (0.0, 0.55, 1.3, 500.0, False), (0.0, 0.1, 1.2, 2500.0, False),
                                         (0.0, 0.35, 0.8, 600.0, 'only')]):
        out[f'flame{k}'] = dict(point([round(x * math.cos(a) - y * math.sin(a), 3),
                                       round(x * math.sin(a) + y * math.cos(a), 3), round(z + I.SINK, 3)], w, '#FF7A2E',
                                      0.5 if w >= 2500.0 or v == 'only' else 0.3),
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
            p['rotate_z'] = p.get('rotate_z', 0.0) + TURN
    fire = M.fire(CACHE)
    fire['position'] = [0.0, 0.0, I.SINK]                           # the solve's floor at the speaker's foot
    fire['strength'] = STRENGTH
    deck = [p for p in I.deck() if p.get('size', [0.0])[0] != 0.03]   # the trench's walls in section: firelit, a pale
    fire['through_glass'] = False                                     # ruled line along the lip (the trench has walls)
    embers = piece('scatter', count=45, radius=[0.0012, 0.003], position=[0.0, 0.0, 0.9], material='glow',
                   color='#FF8A30', emit=60.0, seed=27, plume={'height': 1.8, 'spread': [0.2, 1.0], 'lean': [0.9, 0.3],
                                                              'taper': 0.5, 'power': 3.0, 'streak': 30.0, 'swirl': 0.35})
    props[:] = deck + torn(I.gouge()) + rest + [fire, embers] + marks(len(deck))
    for k in ('fire0', 'firerim0', 'farfire0', 'farfire1'):
        s['lights'].pop(k)
    s['lights'].update(firelight())
    # the bounce on the speaker's face is the fire-lit road's now, warm (p3: "a flat, neutral grey light")
    s['lights']['bounce'].update(color='#D9A27A', irradiance=3.0)
    for inst in s['product']['instances']:
        inst['position'] = [inst['position'][0], inst['position'][1], I.SINK]
        inst['tilt'] = TILT
        inst['rotate_z'] = inst['rotate_z'] + TURN
    s['finish']['grain'] = 3.5                                       # p3: "grain-free and lens-clean"
    s['render']['white_balance_k'], s['render']['white_balance_tint'] = WB
    s['finish']['dream'].update(bloom=0.32, bloom_px=60)               # p5: "no halation, lens glare"
    s['finish']['dream']['haze'] = HAZE                                # p6: "no heat haze bending the railing behind them"
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
    p['finish'] = copy.deepcopy(sh['finish'])
    p['finish']['dream']['haze'] = HAZE_PORTRAIT
    _aim(p['camera'])
    return p
