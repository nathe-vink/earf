"""Closest points between the driver's leads and the tray, the plate's opening and the joint screws (read-only)."""
import sys
sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else 'A-nolock']
exec(open('/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/b110/t1canopy/py/probe_lib.py').read())
drv = P['driver']
body_reg = box(-34.0, -51.0, H(7.9), -8.8, 33.0, H(47.9))
inp = drv & box(-40, 33.0, H(0), 0, 60, H(120))
led = drv - body_reg - box(-40, 33.0, H(0), 0, 60, H(120))
def cp(a, b, tag):
    try:
        p1, p2 = a.closest_points(b)
        dist = (p1 - p2).length
        print(f'{tag:42} d {dist:.3f}  at ({p1.X:.2f}, {p1.Y:.2f}, h {p1.Z-ZC:.2f}) / ({p2.X:.2f}, {p2.Y:.2f}, h {p2.Z-ZC:.2f})')
    except Exception as e:
        print(tag, 'err', e)
cp(inp, P['tray-u'], 'input leads | tray-u')
cp(inp, P['tray-wall'], 'input leads | tray-wall')
cp(inp, P['tray-screws'], 'input leads | joint screw+nut')
cp(inp, P['strap'], 'input leads | plate (opening)')
cp(led, P['tray-u'], 'LED leads | tray-u')
cp(led, P['lead-bushing'], 'LED leads | bushing')
cp(led, P['canopy'], 'LED leads | canopy')
cp(led, P['cord'], 'LED leads | cord')
cp(P['cord'], P['canopy-bushing'], 'cord | floor grommet')
cp(P['splices'], P['tray-u'], 'splices | tray-u')
cp(P['lead-bushing'], P['tray-wall'], 'bushing | tray-wall')
# the cord's own conductors versus the LED leads (Class 2 both) and the jacket's end height
cb = P['cord'].bounding_box(); print('cord bbox', round(cb.min.X,2), round(cb.max.X,2), round(cb.min.Y,2), round(cb.max.Y,2), round(cb.min.Z-ZC,2), round(cb.max.Z-ZC,2))
# lead lengths along the lane's polylines (crystal.py:939-949)
import math
def plen(pts):
    return sum(math.dist(pts[k], pts[k+1]) for k in range(len(pts)-1))
for k_, zl_ in enumerate((15.4, 17.6)):
    xo_ = -21.0 - 1.2 + 2.4 * k_
    pts = [(-31.5, 33.0 - 1.0, zl_), (-31.5, 36.5, zl_), (xo_, 36.5, 42.0), (xo_, 36.5, 50.0)]
    L = plen(pts) - 0.0
    print(f'input lead {k_}: case to plate top {L:.1f} mm, left in the box of 300: {300 - L:.0f}')
for k_, (zl_, ye_, zr_) in enumerate(((31.0, -10.3, 26.0), (33.1, 10.3, 23.5))):
    xb_ = -30.1 + 2.2 * k_
    pts = [(-31.5, -51.0, zl_), (-31.5, -53.0, zl_), (xb_, -54.5, 32.0), (xb_, -61.0, 32.0), (-5.6, -61.0, zr_), (-5.6, ye_, zr_), (-2.6, ye_, 26.5), (-2.6, ye_, 28.5)]
    L = plen(pts) + 11.0
    print(f'LED lead {k_}: case to splice incl. 11 strip {L:.1f} mm; surplus of the -XL 300: {300 - L:.0f}')
