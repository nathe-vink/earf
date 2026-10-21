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
"""
import copy

import smoke_bridge
import smoke_e10 as B
import smoke_e12 as M
import smoke_impact as I

NEAR = [-1.2, 15.0]                  # E10's burning car, across the gouge's line: the speaker is the fire now


def shot():
    s = copy.deepcopy(B.shot())
    props = s['set']['props']
    rest = [p for p in props[len(smoke_bridge.deck()):] if (p.get('position') or [])[:2] != NEAR]
    for p in rest:
        if p.get('fn') == 'occluder':                                # the contact shadow, down in the trench with it
            p['position'] = [0.0, 0.0, round(I.SINK + 0.012, 3)]
    fire = M.fire()
    fire['position'] = [0.0, 0.0, I.SINK]                           # the solve's floor at the speaker's foot
    props[:] = I.deck() + I.gouge() + rest + [fire]
    for k in ('fire0', 'firerim0'):
        s['lights'].pop(k)
    s['lights'].update(M.firelight(-I.SINK))
    for inst in s['product']['instances']:
        inst['position'] = [inst['position'][0], inst['position'][1], I.SINK]
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
    _aim(p['camera'])
    return p
