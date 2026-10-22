"""Smoke, setting E12: the meteor. The owner, 2026-10-21, on E10's fire-and-smoke tests: "I meant it would look cool if
the speaker was enveloped in this particular fire/smoke, like it's an asteroid that just burned through the atmosphere
and came crashing into a road or salt flats." (E11 had read his first note as smoke rising behind the speaker.)

E6's salt pan (smoke_pan.py), less its far tower: the crust to the horizon, the low sun from the front-left, the cloud
shadow, the camera and the lights on the speaker. The speaker has just come down. It ploughed a trench in from the back
left, its spoil heaped along both banks, and stopped in a crater with a heaved, broken rim, sunk to its foot; the crust
is burnt black round it and along the trench, sooted wider, glowing in its cracks near the crater, and slabs of it lie
thrown out ahead, the way it was going. It is still burning: flames lick up its sides and back and the black smoke rolls
off it and away on a light wind.

The fire is E10's solver (plume_sim.py) with the speaker in it as a solid the flow goes round, so the fire wraps it and
no smoke stands inside its clear acrylic, and its skin burning, strongest at its foot, less on the face the camera sees
(a first look, m1, hid the speaker's face in flame); a ring of fire round its foot, set 0.2 m behind it. meteor_c:
10 x 7 x 8 m at 0.05 m, 12 s, wind 1.4 m/s, confinement 3.2 (the small plume's law, eps x dx 0.16), the box's ends
taking the smoke back hard (meteor_a's 8 x 5 m box filled up: its smoke went round the periodic ends and came back in
upwind, and stood as a second column at the far end). In meteor_b's 2.2 m/s the plume's foot ran along the ground and
rose again downwind like a second fire (12% of the smoke below 1.2 m); in 1.4 the column stands up off the speaker and
bends over high (2%). The volume is placed by the solid, so the speaker stands in the
hole the flow left for it (placed by the fire's centre, meteor_a's proofs had it 0.2 m in front of the speaker). The
flames are E9's: black-body from 1100 to 2100 K, broken into hard-edged tongues. The cracks' glow is seen but not
sampled as a light (a linked emission made the pan's 14 M triangles lights: the first proofs died at 14 GB).

p6, after proof 5's critics (realism 4 and 4, both head-to-heads lost to the live bridge, though only this answered the
brief): the rubble's faces carried the cracks' glow, "a regular orange web ... like a wireframe shader" (the debris now
take the crust without it, and fewer cracks glow); the flames "far too bright and white for a daylight exposure" (half
as strong); the speaker "spotless and perfectly upright ... as if someone placed it there" (canted forward, as E12r);
"almost no orange glow from the flames right next to it" (the lamps up among the flames, half as strong again, and
unseen by the smoke); "a ruler-straight dark line where the cracked ground stops" (the pan's edge: E6's horizon haze,
dropped with its smoke banks, is back).

p7: meteor_d, the fire on its front corners and foot too (both sets of critics: the flames "never pass in front of the
box", "glowing cards beside it"; the owner's "enveloped"), unseen through its clear parts (the flames behind it showed
through the smoked acrylic as pale tan panels). (A lamp for the front flames, 0.4 m off its face, turned the black
cabinet bronze in proof 7: gone.)
"""
import copy
import math

import smoke_pan as P
from common import piece, point

CACHE = 'renders/2026-10-21/barkhorn/plume/meteor_d.npz'          # p7: meteor_c with fire on its front and foot too
ROT = 18.0                     # the speaker's turn (E6's)
WIND = 50.0                    # the sim's downwind (+x) turned: away from the camera, a little right
SINK = 0.16                    # the speaker's foot below the crust: it stopped in its crater (p2-p3's 0.10 in a 0.12 m
                               # bowl read as standing on the surface, "a glowing ring at its base, not a pit")
CRATER = [0.0, 0.0, 0.7, 0.2, 0.09, 0.2]                         # x, y, r, depth, rim, rim width
TILT = [4.0, -1.5]                                               # the speaker canted forward as it dug in (E12r's)
TRENCH = [-2.6, 6.2, -0.15, 0.55, 0.36, 0.05, 0.13, 0.08]        # from, to, half-width, depth there and here, rim
AHEAD = math.degrees(math.atan2(TRENCH[3] - TRENCH[1], TRENCH[2] - TRENCH[0]))   # the way it was travelling


def fire(cache=CACHE):
    """The fire as a volume: E10's plume shader with E9's flames, the box's floor at the crater's, its solid on the
    speaker; `cache` the solve (E12r's p5 tries meteor_d, the fire on its front too)."""
    return piece('ext', module='plume', fn='plume', cache=cache, anchor='solid', position=[0.0, 0.0, -SINK], rotate_z=WIND,
                 density=4.5, strength=110.0, color='#8F857B', anisotropy=0.4, cool=1100.0, hot=2100.0,
                 flame_floor=0.25, tongues=0.9, tongue_scale=0.12, tongue_edge=[0.42, 0.62], edge=[0.02, 0.22],
                 detail=2.5, detail_scale=0.1, detail_octaves=4.0, breakup=0.45, breakup_scale=0.35,
                 breakup_octaves=2.0, tongue_octaves=3.0, seed=3)


def impact(ground_name):
    """The crash's marks on the crust. The heat in the cracks a few patches close round the foot (p2-p3's, at twice the
    strength and over 1.3 m, laced the whole crater in an even orange web; p4's 3 within 0.85 m all but vanished)."""
    return piece('ext', module='smoke_el', fn='impact', on=ground_name, centre=CRATER[:2], char=[0.9, 1.7], jag=0.8,
                 soot=3.5, soot_mix=0.6, furrow=TRENCH[:5], glow=4.0, glow_r=0.9, glow_patch=[0.56, 0.7],
                 debris={'count': 90, 'size': [0.04, 0.22], 'spread': [0.65, 2.6], 'ahead': round(AHEAD, 1), 'seed': 3})


def firelight(drop=SINK):
    """The flames' light: low on both flanks and behind, warm, on the speaker, the crater and the crust; `drop`, how far
    the speaker's foot is sunk. Hidden from the lens, from rays through glass and from reflections: p2's lamps, 0.35 m
    balls 0.17 m off the cabinet's sides, showed through its clear acrylic as a pale disc over half its face (and p4's,
    still mirrored in it, as a small one by the woofer); and at 520 W they turned the whole pan orange (E6's is grey),
    so half that. The flames' own glow is what the glossy parts reflect. p6: up among the flames, half as strong again
    (p5: "almost no orange glow from the flames right next to it"), and unseen by the smoke (E12r's look: lamps inside
    the plume's foot lit it like a fireball)."""
    a = math.radians(ROT)
    out = {}
    for k, (x, y, z, w) in enumerate([(-0.6, 0.1, 0.8, 400.0), (0.6, 0.15, 0.75, 400.0), (0.0, 0.55, 0.95, 300.0)]):
        out[f'flame{k}'] = dict(point([round(x * math.cos(a) - y * math.sin(a), 3),
                                       round(x * math.sin(a) + y * math.cos(a), 3), round(z - drop, 3)], w, '#FF7A2E', 0.25),
                                camera=False, transmission=False, specular=0.0, volume=False)
    return out


def shot():
    s = copy.deepcopy(P.shot())
    props = s['set']['props']
    # E6's smoke banks go, its haze toward the horizon stays: it hides the pan's far edge
    props[:] = [p for p in props if p.get('fn') != 'woodsmoke' or p['size'][0] >= 1500]
    g = next(p for p in props if p.get('shape') == 'ground')
    g['dents'], g['furrows'] = [CRATER], [TRENCH]
    for p in props:
        if p.get('fn') == 'occluder':                                # the contact shadow, down in the crater with it
            p['position'] = [p['position'][0], p['position'][1], round(p['position'][2] - SINK, 3)]
    props += [{**fire(), 'through_glass': False}, impact(f'prop{props.index(g)}-kit')]
    for inst in s['product']['instances']:
        inst['position'] = [inst['position'][0], inst['position'][1], round(inst['position'][2] - SINK, 3)]
        inst['tilt'] = TILT
    s['lights'].update(firelight())
    s['title'] = 'barkhorn, Smoke E12, the meteor: the speaker come down burning on the salt pan'
    return s


def portrait():
    sh = shot()
    p = P.portrait()
    p['set'], p['lights'], p['product'], p['title'] = sh['set'], sh['lights'], sh['product'], sh['title'] + ' (4:5)'
    return p
