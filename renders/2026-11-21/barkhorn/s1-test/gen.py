"""The audit's S1 test (2026-11-21): the approved tallr7 fronts, Ember and Fog, three ways.
   a: as approved (the shot file unchanged)
   b: one light model: refractive and reflective caustics on, the acrylics' shadow-ray shortcut cut
      (living_ext.no_glass_shadows), filter_glossy 0, clamp 0
   c: b with the sweep's painted contact term off (strength and core 0)
    python3 gen.py OUTDIR"""
import copy, json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..'))
SRC = ROOT + '/renders/2026-11-04/barkhorn/rollout/A-polished-tallr7/site-front-off-tall-{t}.shot.json'
od = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
for t in ('ember', 'fog'):
    a = json.load(open(SRC.format(t=t)))
    b = copy.deepcopy(a)
    b['render'].update(caustics_refractive=True, caustics_reflective=True, filter_glossy=0.0, clamp=0)
    b['set'].setdefault('props', []).append({'kind': 'kit', 'shape': 'ext', 'path': 'spinoffs/barkhorn/campaign/living/living_ext.py',
                                             'fn': 'no_glass_shadows'})
    c = copy.deepcopy(b)
    c['set']['contact'] = {**c['set']['contact'], 'strength': 0.0, 'core_strength': 0.0}
    for k, s in (('a', a), ('b', b), ('c', c)):
        s['title'] = f"S1 test {k}: {s.get('title', '')}"
        json.dump(s, open(os.path.join(od, f'{t}-{k}.json'), 'w'), indent=1)
