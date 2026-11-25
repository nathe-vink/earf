"""Skeptic's check of S2's premise: in the band (the shade lifted 8.0 to 9.0 above its seat, turned 30 -> 0), does the
Kipp K0310.05 ball (Ø3, free tip at r 41.7 with the body flush to the PEEK land at r 40.8, Kipp H 0.9) ride the collar's
plain bore, pushed in about 0.7? A without the lock, V10 solids at 58e4f5d036. The collar is moved as top_check.py moves
it (Pos(0,0,dz) * Rot(0,0,rot)); seated is dz -0.5. For each pose: the ball sphere's overlap with the collar and the
push-in found by stepping the ball inward until it clears. Writes ../out/detent_band.txt"""
import os, sys, math
os.environ['HEMI_LOCK_ON'] = '0'
W = '/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/b110/skeptic-mechanics-and-hanging'
sys.path.insert(0, W + '/tree/spinoffs/barkhorn/companions')
sys.path.insert(0, W + '/tree/studio/fabkit')
import crystal as C
from build123d import Sphere, Pos, Rot

P = {q.name: q.solid for q in C.north_parts(dict(C.V3, top='A')) if q is not None and q.solid is not None}
collar = P['collar']
out = []
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)
def ov(a, b):
    r = a & b
    return r.volume if r is not None else 0.0
pz = C.V3['pin_z']
def ball(rc):   # ball centre at r rc, 90 deg, z pz
    return Pos(0, rc, pz) * Sphere(1.5)
free_rc = 41.7 - 1.5
def pushin(dz, rot):
    c = Pos(0, 0, dz) * (Rot(0, 0, rot) * collar)
    if ov(ball(free_rc), c) < 1e-4:
        return 0.0
    for k in range(1, 121):
        rc = free_rc - 0.01 * k
        if ov(ball(rc), c) < 1e-4:
            return round(0.01 * k, 2)
    return None
say('pose (dz from drawn; seated -0.5), rot -> ball push-in (mm)')
for dz in (-0.5, 0.5, 1.5, 2.5, 4.5, 7.5, 8.0, 8.5):
    say(f'  lowering/drop path, rot 0, dz {dz:+.1f} (lift {dz + 0.5:.1f}): push-in {pushin(dz, 0.0)}')
for dz in (7.5, 8.0, 8.5):
    for rot in (30.0, 22.5, 15.0, 7.5, 2.0, 0.0):
        say(f'  band, lift {dz + 0.5:.1f}, turned {rot:4.1f}: push-in {pushin(dz, rot)}')
open(W + '/out/detent_band.txt', 'w').write('\n'.join(out) + '\n')
