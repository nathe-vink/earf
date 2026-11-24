"""The shade's way on and off, checked by solids (2026-11-24, after the critics found today's shade trapped and the first
even-tier draw locked on). For each top: the cover (shade, collar, clamp ring, gaskets, the white ring) moved against the
fixture (hub, PEEK ring, pins, crown, gland, grip, white disc, carrier, board, stem) along the bayonet's path: hanging; lifted
7.5 and 8.5 (the pins' shoulders, z 91 to 95, into the turn passage, 82.5 to 87.5); at 8.5 turned 30 deg; then lowered,
turned, until the pins are out of the collar's top. Prints every overlap above 1 mm3 by pair. Run with the CAD venv:
    .venv-fab/bin/python spinoffs/barkhorn/companions/top_check.py [today] [today-fixed] [A] [B]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'studio', 'fabkit'))
import crystal as C
from build123d import Pos, Rot

COVER = ('shell', 'liner', 'skin', 'rim', 'collar', 'clamp', 'gaskets', 'white-ring')
FIXT = ('hub', 'ring', 'pins', 'crown', 'gland', 'grip', 'white-disc', 'carrier', 'board', 'stem')
CONF = {'today': dict(C.V3), 'today-fixed': dict(C.V3, white_split=True),
        'A': dict(C.V3, top='A', white_split=True), 'B': dict(C.V3, top='B', white_split=True)}


def overl(a, b):
    ba, bb = a.bounding_box(), b.bounding_box()
    if (ba.max.X < bb.min.X or bb.max.X < ba.min.X or ba.max.Y < bb.min.Y or bb.max.Y < ba.min.Y
            or ba.max.Z < bb.min.Z or bb.max.Z < ba.min.Z):
        return 0.0
    return (a & b).volume


def check(name):
    p = CONF[name]
    P = {q.name: q.solid for q in C.north_parts(p) if q.solid is not None}
    top = (C.TOP_TIERS[p['top']]['top'] if p.get('top') else p['collar'][3])
    out_ = top - 90.5 + 0.5                       # net lowering below hanging until the pins clear the collar's top, +0.5
    poses = [('hanging', 0, 0), ('lifted 7.5', 7.5, 0), ('lifted 8.5', 8.5, 0), ('lifted 8.5, turned', 8.5, 30)]
    z = 8.5
    while z > -out_:
        z = max(z - 2.0, -out_); poses.append((f'turned, lowered to {z:+.1f}', z, 30))
    poses += [(f'turned, lowered to {-d:+.0f} (off, past the carrier)', -d, 30) for d in (30, 60, 100, 140)]
    print(f'## {name}: collar top {top}, lowering needed {out_ - 0.5:.1f} net below hanging')
    bad = 0
    for lab, dz, rot in poses:
        hits = []
        for c in COVER:
            if c not in P:
                continue
            m = Pos(0, 0, dz) * (Rot(0, 0, rot) * P[c])
            for f in FIXT:
                if f in P:
                    v = overl(m, P[f])
                    if v > 1.0:
                        hits.append(f'{c} x {f} {v:.0f} mm3')
        bad += bool(hits)
        print(f'  {lab:28s} ' + ('clear' if not hits else 'BLOCKED: ' + '; '.join(hits)))
    print(f'  => {"comes off" if not bad else "does NOT come off"}')
    # the control: lowered 3 without the turn, the pins must hold it (else the check sees nothing)
    v = sum(overl(Pos(0, 0, -3.0) * P['collar'], P[f]) for f in ('pins',))
    print(f'  control, lowered 3 unturned: collar x pins {v:.0f} mm3 ({"held, as it must be" if v > 1 else "NOT HELD: the check is blind"})')


if __name__ == '__main__':
    for n in (sys.argv[1:] or CONF):
        check(n)
