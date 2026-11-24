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

COVER = ('shell', 'liner', 'skin', 'rim', 'collar', 'clamp', 'gaskets', 'lock-pulled')   # v7: A's lock, its knob pulled
FIXT = ('hub', 'ring', 'pins', 'crown', 'gland', 'grip', 'white-disc', 'carrier', 'board', 'stem')
CONF = {'today-as-built': dict(C.V3, white_split=False), 'today': dict(C.V3),
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
    if 'lock' in P:
        # v7 (the coordinator's decision, (6)): the swap is made with the lock's knob pulled, its pin drawn back 5 along its axis
        import math
        a_ = math.radians(C.GRIP['lock']['angle']); st_ = C.GRIP['lock']['stroke']
        P['lock-pulled'] = Pos(st_ * math.cos(a_), st_ * math.sin(a_), 0) * P['lock']
    top = (C.TOP_TIERS[p['top']]['top'] if p.get('top') else p['collar'][3])
    # lowered from the drawn pose until the pins (z 91 to 95, lifted 8.5 to 82.5 to 86.5) clear the collar's top: top - 91
    # (check 3: A 12.33, B 9.5 from the drawn pose; from where it hangs, 0.5 lower, 11.83 and 9.0), then 0.5 more
    out_ = top - 91.0 + 0.5
    # (review 2: it hangs with each notch's top seated on its pin, 0.5 under the drawn position, so the drawn +7.5
    # and +8.5 are lifts of 8.0 and 9.0 from where it hangs)
    poses = [('hanging (seated)', -0.5, 0), ('lifted 8.0', 7.5, 0), ('lifted 9.0', 8.5, 0), ('lifted 9.0, turned', 8.5, 30)]
    z = 8.5
    while z > -out_:
        z = max(z - 2.0, -out_); poses.append((f'turned, lowered to {z:+.1f}', z, 30))
    poses += [(f'turned, lowered to {-d:+.0f} (off, past the carrier)', -d, 30) for d in (30, 60, 100, 140)]
    print(f'## {name}: collar top {top}, lowered {out_ - 0.5:.2f} below the drawn pose ({out_ - 1.0:.2f} below where it hangs) to come off')
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
    if p.get('white_split'):
        print(f"  the lip's bore Ø{C.WHITE_SPLIT['lip'][0]} against the hub and disc Ø{C.WHITE_SPLIT['disc']}: {(C.WHITE_SPLIT['lip'][0] - C.WHITE_SPLIT['disc']) / 2:.2f} radial")
    # the control: lowered 3 without the turn, the pins must hold it (else the check sees nothing)
    v = sum(overl(Pos(0, 0, -3.0) * P['collar'], P[f]) for f in ('pins',))
    print(f'  control, lowered 3 unturned: collar x pins {v:.0f} mm3 ({"held, as it must be" if v > 1 else "NOT HELD: the check is blind"})')
    if 'lock' in P:
        # v8 (the v7 check's (2)): the knob released at the SEAT (0.5 under the drawn pose): its pin clear in its Ø6.4 hole;
        # a lift of 1.5 from the seat and a turn of 4 deg must both hit the ring
        sv = overl(Pos(0, 0, -0.5) * P['lock'], P['ring'])
        lv = overl(Pos(0, 0, -0.5 + 1.5) * P['lock'], P['ring']); tv = overl(Pos(0, 0, -0.5) * (Rot(0, 0, 4.0) * P['lock']), P['ring'])
        print(f'  the lock released at the seat: in its hole {sv:.2f} mm3 ({"clear" if sv == 0 else "JAMMED"}); lifted 1.5, '
              f'{lv:.1f} mm3; turned 4 deg, {tv:.1f} mm3 ({"blocked, as it must be" if lv > 0 and tv > 0 else "NOT BLOCKED"})')
    # v8 (the v7 check's (1)): keyed, it fits one way only: turned 120 or 240 deg and pushed up its entries, the Ø5 pin meets a
    # 5 wide slot
    for k in (120, 240):
        # (up the entries the shade is turned 30, as in the turned poses above; the wrong way is 30 + 120 or 30 + 240)
        kv = max(overl(Pos(0, 0, dz) * (Rot(0, 0, 30 + k) * P['collar']), P['pins']) for dz in (-6.0, -3.0, 0.0, 4.0))
        print(f'  turned {k} deg (the wrong way), up its entries: collar x pins {kv:.0f} mm3 ({"refused, as it must be" if kv > 1 else "FITS: NOT KEYED"})')


if __name__ == '__main__':
    for n in (sys.argv[1:] or CONF):
        check(n)
