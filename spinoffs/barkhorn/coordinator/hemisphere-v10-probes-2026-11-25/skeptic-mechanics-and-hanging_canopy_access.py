"""Skeptic's own check of B1 (the cord clamp's screws and the lever splices can't be worked) on the V10 solids at
58e4f5d036, A without the lock. Builds crystal.north_parts from the scratch tree export and measures, in the canopy's
frame (x on the cables' line, z above the canopy's underside):
  - the saddle screws' heads and the splices against the tray-U (min distance);
  - a Phillips #1 / 2.5 hex tool (shank 5, 60 long) along -x from each screw head: what it hits;
  - a 221-412 lever opened (7.1 more above its lever face, WAGO drawing 8.2 -> 15.3) on each splice: what it hits;
  - the workaround: the channel's two M3 nylon-insert nuts at (13, +-8) reached from below by a 5.5 nut driver (Ø9);
    and how far the channel must drop and move to give the levers and screws room.
Writes ../out/canopy_access.txt"""
import os, sys, time
os.environ['HEMI_LOCK_ON'] = '0'
W = '/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/b110/skeptic-mechanics-and-hanging'
sys.path.insert(0, W + '/tree/spinoffs/barkhorn/companions')
sys.path.insert(0, W + '/tree/studio/fabkit')
import crystal as C
from build123d import Box, Cylinder, Pos, Rot, Align

t0 = time.time()
parts = {q.name: q for q in C.north_parts(dict(C.V3, top='A')) if q is not None and q.solid is not None}
out = []
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)
say('built', len(parts), 'parts in', round(time.time() - t0, 1), 's; LOCK_ON', C.LOCK_ON)
zc = parts['canopy'].solid.bounding_box().min.Z
say('canopy underside zc =', round(zc, 3))
def bb(n):
    b = parts[n].solid.bounding_box()
    return [round(v, 2) for v in (b.min.X, b.min.Y, b.min.Z - zc, b.max.X, b.max.Y, b.max.Z - zc)]
for n in ('cord-clamp', 'splices', 'tray-u', 'tray-wall', 'driver', 'relief-bracket', 'gripper-brackets', 'grippers', 'strap', 'canopy-studs'):
    say(f'  {n:16s} bbox (x0 y0 z0 x1 y1 z1, z above canopy underside):', bb(n))

def vol(a, b):
    try:
        r = a & b
        return r.volume if r is not None else 0.0
    except Exception as e:
        return float('nan')
def dist(a, b):
    try:
        return a.distance_to(b)
    except Exception as e:
        return float('nan')

others = [n for n in parts if n not in ('cord-clamp',)]
say('\nB1 (a): minimum distances')
say('  cord-clamp to tray-u  :', round(dist(parts['cord-clamp'].solid, parts['tray-u'].solid), 3))
say('  splices    to tray-u  :', round(dist(parts['splices'].solid, parts['tray-u'].solid), 3))
say('  splices    to driver  :', round(dist(parts['splices'].solid, parts['driver'].solid), 3))
say('  cord-clamp to driver  :', round(dist(parts['cord-clamp'].solid, parts['driver'].solid), 3))

def cyl_x(y, z, d, x0, x1):
    return Pos(x0, y, z) * (Rot(0, 90, 0) * Cylinder(d / 2, x1 - x0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
def cyl_z(x, y, d, z0, z1):
    return Pos(x, y, z0) * Cylinder(d / 2, z1 - z0, align=(Align.CENTER, Align.CENTER, Align.MIN))

say('\nB1 (b): a tool along -x from each saddle screw head (head face at x 0.2), shank Ø5 (PH1) and Ø2.5 (hex key), 60 long')
for sy in (-8.0, 8.0):
    for d in (5.0, 2.5):
        tool = Pos(0, 0, 0) * cyl_x(sy, zc + 11.0, d, 0.2 - 60.0, 0.2)
        hits = []
        for n, q in parts.items():
            if n == 'cord-clamp':
                continue
            v = vol(tool, q.solid)
            if v and v > 0.01:
                hits.append(f'{n} {v:.1f} mm3')
        # the free length in front of the head
        free = None
        for L in [k * 0.1 for k in range(1, 601)]:
            tt = cyl_x(sy, zc + 11.0, d, 0.2 - L, 0.2)
            if any((vol(tt, parts[n].solid) or 0) > 0.001 for n in ('tray-u', 'tray-wall', 'driver', 'splices', 'cord')):
                free = round(L - 0.1, 1); break
        say(f'  screw y {sy:+.0f}, tool Ø{d}: free length in front of the head {free} mm; a 60 tool hits: {hits}')

say('\nB1 (c): a 221-412 lever opened on each splice: 7.1 more in front of the lever face (x -6.7 -> -13.8), over the')
say('  splice\'s y and z extent (y -13.6..-0.5 and 0.5..13.6, z 28.5..46.8)')
for y0, y1 in ((-13.6, -0.5), (0.5, 13.6)):
    lever = Pos(-13.8, y0, zc + 28.5) * Box(7.1, y1 - y0, 18.3, align=(Align.MIN, Align.MIN, Align.MIN))
    hits = [f'{n} {vol(lever, q.solid):.1f} mm3' for n, q in parts.items() if (vol(lever, q.solid) or 0) > 0.01]
    say(f'  splice y {y0:+.1f}..{y1:+.1f}: the opened lever\'s swept box hits {hits}')

say('\nWorkaround check: the channel\'s two M3 nylon-insert nuts at (13, +-8) under its top flange, from below')
studs = parts['canopy-studs'].solid
for sy in (-8.0, 8.0):
    # nut at z 42.8..46.8 (zc-relative) per the code; a 5.5 AF nut driver, socket Ø9, from 60 below up to the nut's foot
    tool = cyl_z(13.0, sy, 9.0, zc + 42.8 - 60.0, zc + 42.8 - 0.05)
    hits = [f'{n} {vol(tool, q.solid):.2f} mm3' for n, q in parts.items() if (vol(tool, q.solid) or 0) > 0.01]
    say(f'  nut y {sy:+.0f}: a Ø9 nut driver from below hits {hits}')
    tool = cyl_z(13.0, sy, 8.0, zc + 42.8 - 60.0, zc + 42.8 - 0.05)
    hits = [f'{n} {vol(tool, q.solid):.2f} mm3' for n, q in parts.items() if (vol(tool, q.solid) or 0) > 0.01]
    say(f'  nut y {sy:+.0f}: a Ø8 nut driver from below hits {hits}')

open(W + '/out/canopy_access.txt', 'w').write('\n'.join(out) + '\n')
say('done in', round(time.time() - t0, 1), 's')
