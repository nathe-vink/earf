"""Build one package's parts and save the canopy group's solids as BREP for the probes (read-only on the lane's code)."""
import os, sys, time, json
TREE = '/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/b110/t1canopy/tree'
OUT = '/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/b110/t1canopy/brep'
pkg = sys.argv[1]   # today, A-lock, A-nolock, B
os.environ['HEMI_LOCK_ON'] = '0' if pkg == 'A-nolock' else '1'
sys.path.insert(0, os.path.join(TREE, 'spinoffs/barkhorn/companions')); sys.path.insert(0, os.path.join(TREE, 'studio/fabkit'))
import crystal as C
from build123d import export_brep
top = {'today': None, 'A-lock': 'A', 'A-nolock': 'A', 'B': 'B'}[pkg]
p = dict(C.V3, top=top) if top else dict(C.V3)
t = time.time()
parts = C.north_parts(p)
print('built', pkg, round(time.time() - t, 1), 's')
d = os.path.join(OUT, pkg); os.makedirs(d, exist_ok=True)
info = {}
for q in parts:
    if q is None or q.solid is None:
        continue
    bb = q.solid.bounding_box()
    info[q.name] = dict(group=getattr(q, 'group', None), bb=[round(v, 3) for v in (bb.min.X, bb.min.Y, bb.min.Z, bb.max.X, bb.max.Y, bb.max.Z)],
                        vol=round(q.solid.volume, 3))
    export_brep(q.solid, os.path.join(d, q.name + '.brep'))
json.dump(info, open(os.path.join(d, 'info.json'), 'w'), indent=1)
print('saved', len(info))
