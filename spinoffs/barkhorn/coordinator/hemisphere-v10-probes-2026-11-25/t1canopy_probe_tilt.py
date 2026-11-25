"""Tool-access detail: which parts block a O6 shaft tilted below horizontal from each saddle screw's head, and which
features of the tray come closest to the input and LED leads (read-only)."""
import os, sys, json
sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else 'A-nolock']
exec(open('/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/b110/t1canopy/py/probe_lib.py').read())
for sy in (-8.0, 8.0):
    for ang in (0, 20, 33, 45, 50, 53, 55, 58, 60, 65, 70, 80, 90):
        shaft = cyl('x', (sy, H(11.0)), 6.0, 0.2 - 120.0, 0.2)
        shaft = shaft.rotate(Axis((0.2, sy, H(11.0)), (0, 1, 0)), -ang)
        bb = shaft.bounding_box()
        hit = [(n, round(vol(shaft, P[n]), 2)) for n in names if n not in ('cord-clamp', 'canopy') and bbo(shaft, P[n], 0.0) and vol(shaft, P[n]) > 1e-6]
        print(f'y{sy:+.0f} tilt {ang:2d}: shaft x {bb.min.X:.1f}..{bb.max.X:.1f} h {bb.min.Z-ZC:.1f}..{bb.max.Z-ZC:.1f} hits {hit}')
