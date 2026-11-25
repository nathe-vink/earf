"""The V10 detent with a real ball: Kipp K0310.05 (M5 x 12, ball Ø3, H 0.9 = its free projection and its stroke,
F1 6 N, F2 11 N; Kipp's table, dl/kipp/K0310.txt). The plunger's body flush with the PEEK land (r 40.8) as the CAD draws
it, so the free ball's tip is at r 41.7 (the CAD draws a Ø3 x 0.8 cylinder, tip r 41.6). Against the A-without-the-lock
collar (the same dimple in today's and B's). (1) At the seat (the cover 0.5 under its drawn pose): the ball's clearance,
with the slot cut 0.05 / 0.10 low or high and the plunger 0.1 proud. (2) Along the swap: the retraction the ball needs
at each pose (bisection on its radial position), so it stays within its 0.9 stroke. Usage: detent.py [Aoff|today|B]"""
import sys, json, math
cfg = sys.argv[1] if len(sys.argv) > 1 else 'Aoff'
B = '/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/b110/mechanics'
from build123d import import_brep, Pos, Rot, Sphere
collar = import_brep(f'{B}/brep/{cfg}/collar.brep')
A = math.radians(90.0)

def ball(rc, z):
    return Pos(rc * math.cos(A), rc * math.sin(A), z) * Sphere(1.5)

def ov(dz, rot, rc, zb=93.0):
    m = Pos(0, 0, dz) * (Rot(0, 0, rot) * collar)
    i = m & ball(rc, zb)
    return i.volume if i is not None else 0.0

H = 0.9
rc_free = 40.8 + H - 1.5          # the ball's center, free (tip at 41.7)
print(f'## {cfg}: Kipp K0310.05 ball Ø3, free tip r {rc_free + 1.5:.2f}')
for lab, zb, rc in (('nominal', 93.0, rc_free), ('slot cut 0.05 low (ball 0.05 higher in it)', 93.05, rc_free),
                    ('slot 0.10 low', 93.10, rc_free), ('slot 0.05 high', 92.95, rc_free), ('slot 0.30 high', 92.70, rc_free),
                    ('plunger 0.1 proud', 93.0, rc_free + 0.1), ('plunger 0.1 proud, slot 0.05 low', 93.05, rc_free + 0.1)):
    v = ov(-0.5, 0.0, rc, zb)
    # the clearance: how far the ball can move out radially before it touches
    lo, hi = 0.0, 1.0
    if v > 1e-7:
        print(f'  seat, {lab}: OVERLAP {v:.5f} mm3'); continue
    for _ in range(30):
        mid = (lo + hi) / 2
        if ov(-0.5, 0.0, rc + mid, zb) > 1e-7:
            hi = mid
        else:
            lo = mid
    # and vertically: how far up and down before it touches
    up = dn = None
    for sgn in (1, -1):
        lo2, hi2 = 0.0, 2.0
        for _ in range(30):
            mid = (lo2 + hi2) / 2
            if ov(-0.5, 0.0, rc, zb + sgn * mid) > 1e-7:
                hi2 = mid
            else:
                lo2 = mid
        if sgn == 1:
            up = lo2
        else:
            dn = lo2
    print(f'  seat, {lab}: clear; radial room {lo:.3f}, room up {up:.3f}, down {dn:.3f}')

# the lift out of the seat: the cover lifted d from the seat (dz = -0.5 + d): the ball's retraction needed
print('  lift from the seat (turn 0): d, retraction needed')
for d in (0.0, 0.25, 0.5, 0.75, 0.8, 0.9, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 6.0, 8.0, 9.0):
    dz = -0.5 + d
    if ov(dz, 0.0, rc_free) <= 1e-7:
        print(f'    d {d:.2f}: 0'); continue
    lo, hi = 0.0, 1.5
    for _ in range(30):
        mid = (lo + hi) / 2
        if ov(dz, 0.0, rc_free - mid) > 1e-7:
            lo = mid
        else:
            hi = mid
    print(f'    d {d:.2f}: {hi:.3f}' + ('  BEYOND THE 0.9 STROKE' if hi > 0.9 else ''))
# along the turn and the lowering: worst retraction
worst = 0.0; wpose = None
poses = [(z, r) for z in (7.5, 8.0, 8.5) for r in range(0, 31, 3)] + [(z, 30) for z in [8.5 - 0.5 * k for k in range(1, 46)]]
for dz, rot in poses:
    if ov(dz, rot, rc_free) <= 1e-7:
        continue
    lo, hi = 0.0, 1.5
    for _ in range(25):
        mid = (lo + hi) / 2
        if ov(dz, rot, rc_free - mid) > 1e-7:
            lo = mid
        else:
            hi = mid
    if hi > worst:
        worst, wpose = hi, (dz, rot)
print(f'  turn and lowering: the worst retraction {worst:.3f} at {wpose}' + ('  BEYOND THE STROKE' if worst > 0.9 else ' (within the 0.9 stroke)'))
