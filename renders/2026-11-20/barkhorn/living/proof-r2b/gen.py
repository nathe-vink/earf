"""Round-2 proof 2 of A: p15 (the wall stretch, +0.15), p125 (camera 1.25 m), p115s (camera 1.15 m, the sofa 0.4 m nearer);
and for the port probe, A with the left speaker only (onlyL) and the right only (onlyR)."""
import copy, json, os, sys
sys.path.insert(0, '/home/user/earf/spinoffs/barkhorn/campaign')
import living_room as L
od = sys.argv[1]
C0 = L.CHAIR
def make(name, z=1.5, sofa_dy=0.0, only=None, size=(960, 640)):
    L.CHAIR = (C0[0], C0[1] - sofa_dy, C0[2])
    s = L.SHOTS['living-a']('ember')
    s['camera'] = copy.deepcopy(s['camera']); s['camera']['position'] = [*s['camera']['position'][:2], z]
    if only is not None:
        for blk in s['products'][:2]:
            blk['instances'] = [blk['instances'][only]]
    s['size'] = list(size)
    json.dump(s, open(os.path.join(od, f'{name}.json'), 'w'), indent=1)
    print(name, s['camera']['position'], 'sofa y', L.CHAIR[1], [len(b['instances']) for b in s['products']])
make('p15'); make('p125', z=1.25); make('p115s', z=1.15, sofa_dy=0.4)
make('onlyL', only=0); make('onlyR', only=1)
