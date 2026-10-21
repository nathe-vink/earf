"""Smoke, setting E11: the salt pan, the smoke billowing up from behind the speaker (the owner, 2026-10-21, having seen
E10's smoke test: "That smoke looks good. What if the smoke was billowing from the back of the speaker, and that was
set in the salt flats?").

E6's salt pan (smoke_pan.py) whole, less its far tower and the layers rolling in from it: the white crust to the
horizon, the low sun from the front-left, the cloud shadow with the sun's gap on the foreground, the camera and the
lights on the speaker. In the tower's place, a plume solved with E10's solver (plume_sim.py: MacCormack velocity, the
soot thinning with age) from a source 1 m across hidden just behind the cabinet, with no flame: smoke billows up past
the speaker's back and sides, climbs, and leans away on a light wind, its sunlit side toward the camera, as if the
speaker itself were pouring it out.

The solve (salt/sim in the scratchpad; plume_salt2.npz): 10 x 6 x 8 m at 0.05 m, 12 s, wind 2.2 m/s at 10 m. Its
confinement is set by the plume's size as well as the grid's: the bridge's per-metre strength (eps x dx = 0.5), tuned on
a fire 4 m long, made this plume a fuzzy ball with no lobes (plume_salt, look e11_fine_w50); a third of it (0.16) rolls
real billows (coarse test e11_t2a).
"""
import copy
import math

import smoke_pan as P
from common import piece

CACHE = 'renders/2026-10-21/barkhorn/plume/plume_salt2.npz'
ROT = 18.0                     # the speaker's turn (E6's rotate_z)
BEHIND, SIDE = 0.85, 0.0       # the source's centre (1 m across) from the speaker's: behind its back, toward its right
WIND = 50.0                    # the sim's downwind (+x) turned: away from the camera, a little right (looks e11_s2_w45/60)


def plume():
    """Soot grey-brown (the bridge's #5A5650 at its density made a black wall that swallowed the speaker, look
    e11_s1_w25), so the low sun models the billows; the lobes' edges firm, scattering less forward than the bridge's so
    their sunlit and shaded sides part; the sub-grid tatter light (the solve has the detail; e11_t2a)."""
    a = math.radians(ROT)
    x = -math.sin(a) * BEHIND + math.cos(a) * SIDE
    y = math.cos(a) * BEHIND + math.sin(a) * SIDE
    return piece('ext', module='plume', fn='plume', cache=CACHE, position=[round(x, 4), round(y, 4), 0.0],
                 rotate_z=WIND, density=4.0, strength=0.0, color='#7A746C', anisotropy=0.2, edge=[0.04, 0.3],
                 detail=0.5, detail_scale=0.08, detail_octaves=3.0, breakup=0.35, breakup_scale=0.4,
                 breakup_octaves=2.0, seed=3)


def shot():
    s = copy.deepcopy(P.shot())
    props = s['set']['props']
    props[:] = [p for p in props if p.get('fn') != 'woodsmoke'] + [plume()]
    s['title'] = 'barkhorn, Smoke E11, the salt pan with smoke billowing from behind the speaker'
    return s


def portrait():
    sh = shot()
    p = P.portrait()
    p['set'], p['title'] = sh['set'], sh['title'] + ' (4:5)'
    return p
