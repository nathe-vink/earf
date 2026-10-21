"""Smoke, setting E10: one bigger pass on E9's smoke and its car (the owner, 2026-10-21, after E9 went live: "Smoke still
doesn't look that good"; his pick from the results page, "one bigger pass on the smoke and the car").

E9 whole (smoke_riot.py: the overpass at blue hour, its camera and lamps, the far fires) with its two tells answered:
- the smoke. E9's solver smeared away every eddy smaller than a few cells and its confinement spun the rest up at the
  grid's one scale, so every billow came out the same size ("cotton-ball", "metaball" lobes, "no sheared wisps").
  plume_c is solved again (plume_sim.py) with the velocity advected by MacCormack, which keeps the small eddies;
  random kicks inside the smoke at two scales, which break the lobes into many sizes; the soot thinning with age, so
  old edges go wispy; on a finer grid in a longer box, with a stronger wind for a leaning, sheared column. The
  render's own detail noise is turned down to match, since the sim now carries the detail itself.
- the car. E9's read as "a crude slab", "a flat slab with a tube on top". sedan2 (kit_ext/wreck.py) is the shell a car
  fire leaves: wheel arches, the cabin open where the glass went, pressed-steel pillars and a sagging roof, seat
  frames and a steering wheel inside, five-spoke rims standing in their melted tyres, the paint burnt to ash on top and
  rust down the sides.
"""
import copy

import smoke_riot as R

CACHE = 'renders/2026-10-21/barkhorn/plume/plume_c.npz'
# the near plume's render: the sim now carries the small scales, so the noise that faked them is turned down
NEAR = dict(detail=1.0, detail_scale=0.12, detail_octaves=3.0, breakup=0.25, breakup_scale=0.5, edge=[0.02, 0.3])


def shot():
    s = copy.deepcopy(R.shot())
    for p in s['set']['props']:
        if p.get('module') == 'wreck' and p.get('fn') == 'sedan':
            p['fn'] = 'sedan2'
            p.pop('sag', None)
        if p.get('module') == 'plume' and p.get('seed') == 3:          # the near fire's column (the far ones keep E9's)
            p['cache'] = CACHE
            p.update(NEAR)
    s['title'] = 'barkhorn, Smoke E10, the bridge with the smoke solved again and a burnt-out car'
    return s


def portrait():
    sh = shot()
    p = R.portrait()
    p['set'], p['lights'], p['title'] = sh['set'], sh['lights'], sh['title'] + ' (4:5)'
    return p
