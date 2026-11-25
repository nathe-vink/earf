"""My proposal tried on the V10 solids (Aoff): a GATE, a 0.8 step down from each band's ceiling just past its entry
(1.0 in the key's 7.5 tall band), 4 deg of arc long, from the bore to the slot's floor. Check (1) the fit and the
removal at the stop (drawn +8.5: the pins on the band's floor) pass it; (2) a shade resting on the ceiling (drawn +7.5)
or lifted less than 0.8 cannot be turned back past it to its entries; (3) the seat and the rest of the path unchanged."""
import json, math
B = '/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/b110/mechanics'
from build123d import import_brep, Pos, Rot, Cylinder, Align, Box
P = {n: import_brep(f'{B}/brep/Aoff/{n}.brep') for n in ('collar', 'pins')}
al = (Align.MIN, Align.MIN, Align.MIN)
def sector(r0, r1, a0, a1, z0, z1):
    """an annular sector r0..r1 from angle a0 (deg, CCW from above) about 3.2 mm of arc wide, z0..z1"""
    h = z1 - z0
    ring = Pos(0, 0, z0) * (Cylinder(r1, h, align=(Align.CENTER, Align.CENTER, Align.MIN)) - Cylinder(r0, h + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    slab = Pos(25.0, 1.6, z0 + h / 2) * Box(50.0, 3.2, h + 4)
    return Rot(0, 0, a0) * (ring & slab)
gate = None
for a in (0, 120, 240):
    key = (a == 0)
    w2 = 3.5 if key else 2.5
    e = math.degrees(math.atan(w2 / 43.0))
    top = 88.75 if key else 87.5
    d = 1.0 if key else 0.8
    g = sector(41.0, 45.6, a + e, a + e + 4.0, top - d, top + 0.01)
    gate = g if gate is None else gate + g

collar_g = P['collar'] + gate
def ov(dz, rot):
    m = Pos(0, 0, dz) * (Rot(0, 0, rot) * collar_g)
    i = m & P['pins']
    return i.volume if i is not None else 0.0
print('the stop (+8.5 drawn = 9.0 from the seat), turned 0..30:', max(ov(8.5, r) for r in range(0, 31)))
for dz in (8.4, 8.3, 8.2, 8.0, 7.7, 7.5):
    hits = [(r, round(ov(dz, r), 3)) for r in range(0, 31, 1)]
    first = next((r for r, v in hits if v > 1e-6), None)
    print(f'  at {dz:+.1f} drawn ({dz + 0.5:.1f} above the seat): turned from the notch toward the entries, first blocked at {first} deg; '
          f'max overlap {max(v for r, v in hits):.3f} mm3')
print('the seat (-0.5), turn 0:', round(ov(-0.5, 0.0), 6), '; lowered off at +30 deg from +8.5 to -13:',
      max(ov(z, 30) for z in [8.5 - 0.5 * k for k in range(0, 44)]))
