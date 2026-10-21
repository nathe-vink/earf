"""Smoke, setting E10: one bigger pass on E9's smoke and its car (the owner, 2026-10-21, after E9 went live: "Smoke still
doesn't look that good"; his pick from the results page, "one bigger pass on the smoke and the car").

E9 whole (smoke_riot.py: the overpass at blue hour, its camera and lamps, the far fires) with its two tells answered:
- the smoke. E9's billows were all one size and smooth ("cotton-ball", "metaball lobes"): its solver smeared away the
  small eddies and its vorticity confinement spun up the rest at the grid's one scale. plume_d is solved again
  (plume_sim.py) with the velocity advected by MacCormack, which keeps the small eddies, the soot thinning with age so
  old smoke goes wispy, a stronger wind for a leaning, sheared column, on a finer grid (0.12 m against 0.14) in a
  longer box. A first try that also kicked the smoke at random on small scales made a grainy fog with no column (t10a);
  without the kicks the same solver rolls dense, churning smoke with texture on every scale (the looks in sim10: l2_e9
  against la_e9). The confinement is per grid cell, so it weakens as the grid gets finer: the test's 2.5 at 0.2 m, kept
  at 0.12 m (plume_c), left a smooth, lit dome over the fire; scaled to the grid (4.2) the dome breaks up (le_2.5 against
  le_4.2). All three fires use it, the far ones scaled up as before.
- the car. E9's read as "a crude slab", "a flat slab with a tube on top". sedan2 (kit_ext/wreck.py) is the shell a car
  fire leaves: wheel arches, the cabin open where the glass went, pressed-steel pillars and a sagging roof, seat
  frames and a steering wheel inside, five-spoke rims standing in their melted tyres, the paint burnt to ash on top and
  rust down the sides. All three wrecks are sedan2.
"""
import copy

import smoke_riot as R

CACHE = 'renders/2026-10-21/barkhorn/plume/plume_d.npz'
NEAR = {}                     # E9's render settings: on the new solver's smoke they read as churning, not as lobes


def shot():
    s = copy.deepcopy(R.shot())
    for p in s['set']['props']:
        if p.get('module') == 'wreck' and p.get('fn') == 'sedan':
            p['fn'] = 'sedan2'
            p.pop('sag', None)
        if p.get('module') == 'plume':                                  # all three fires; the near one's render as set
            p['cache'] = CACHE
            if p.get('seed') == 3:
                p.update(NEAR)
    s['title'] = 'barkhorn, Smoke E10, the bridge with the smoke solved again and a burnt-out car'
    return s


def portrait():
    sh = shot()
    p = R.portrait()
    p['set'], p['lights'], p['title'] = sh['set'], sh['lights'], sh['title'] + ' (4:5)'
    return p
