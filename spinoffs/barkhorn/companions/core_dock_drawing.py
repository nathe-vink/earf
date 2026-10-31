"""Core's contact dock (CORE-RECHARGE.md, route b), drawn: a section through Core's base on the dock, and the dock's
plan. A proposal; Core's CAD is unchanged until the owner signs a route.

    python3 spinoffs/barkhorn/companions/core_dock_drawing.py     # writes the SVG and, through Chromium, the PNG
"""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
OUT = os.path.join(ROOT, 'renders', '2026-10-31', 'barkhorn', 'lamps-cordless', 'core-dock-drawing')

D = dict(dock_d=150.0, dock_h=8.0, pocket_d=122.0, pocket_h=1.5, ring_r=(30.0, 44.0), ring_w=4.0,
         base_d=120.0, base_h=30.0, hatch_d=112.0, ball_r=80.0, pin_angle=170.0)
S = 5.0                       # px per mm in the section (the plan at 0.62 of it)
PS = 0.62
INK, MUTED, CUT = '#1C1A18', '#8A847A', '#D9D3C8'


def line(x0, y0, x1, y1, w=1.2, c=INK, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def rect(x, y, w, h, fill=CUT, c=INK, sw=1.4):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>'


def text(x, y, s, size=13, anchor='middle', c=INK, weight='400'):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Helvetica, Arial, sans-serif" font-size="{size}" ' \
           f'text-anchor="{anchor}" fill="{c}" font-weight="{weight}">{s}</text>'


def dim_h(x0, x1, y, label):
    return ''.join([line(x0, y, x1, y, 0.9), line(x0, y - 5, x0, y + 5, 0.9), line(x1, y - 5, x1, y + 5, 0.9),
                    text((x0 + x1) / 2, y - 6, label, 12)])


def dim_v(x, y0, y1, label, left=False):
    return ''.join([line(x, y0, x, y1, 0.9), line(x - 5, y0, x + 5, y0, 0.9), line(x - 5, y1, x + 5, y1, 0.9),
                    text(x - 8 if left else x + 8, (y0 + y1) / 2 + 4, label, 12, 'end' if left else 'start')])


def section(cx, ty):
    """Section through the axis, the table at y = ty (px). Returns svg."""
    p = D; o = []
    dh, ph = p['dock_h'] * S, p['pocket_h'] * S
    r_d, r_p = p['dock_d'] / 2 * S, p['pocket_d'] / 2 * S
    # the dock: its body less the pocket (drawn as two cut pieces and the floor), the rings in it
    top = ty - dh
    o.append(rect(cx - r_d, top + ph, 2 * r_d, dh - ph))
    o.append(rect(cx - r_d, top, r_d - r_p, ph)); o.append(rect(cx + r_p, top, r_d - r_p, ph))
    for r in p['ring_r']:
        for sgn in (-1, 1):
            x = cx + sgn * r * S - p['ring_w'] / 2 * S
            o.append(rect(x, top + ph, p['ring_w'] * S, 2.5 * S, fill='#B9B7B1'))
    # the base, sitting in the pocket on its foot ring
    bt = top + ph - p['base_h'] * S
    rb = p['base_d'] / 2 * S
    o.append(rect(cx - rb, bt, 2 * rb, p['base_h'] * S - 2 * S, fill='#3A3836'))
    o.append(rect(cx - rb + 0.5 * S, top + ph - 2 * S, 3 * S, 2 * S, fill='#3A3836'))          # the foot ring
    o.append(rect(cx + rb - 3.5 * S, top + ph - 2 * S, 3 * S, 2 * S, fill='#3A3836'))
    o.append(rect(cx - p['hatch_d'] / 2 * S, top + ph - 4.5 * S, p['hatch_d'] * S, 2.5 * S, fill='#5C5955'))  # the hatch
    # the pins: on the section's left (the 170 deg line), through the hatch onto the rings
    for r in p['ring_r']:
        x = cx - r * S
        o.append(rect(x - 1.0 * S, top + ph - 9 * S, 2.0 * S, 9 * S, fill='#E0B84A', sw=1.0))
    # the ball, its lower part, sitting in the base's cup
    bc = bt - p['ball_r'] * S + 18 * S
    o.append(f'<path d="M {cx - 70 * S:.1f} {bt - 40 * S:.1f} A {p["ball_r"] * S:.1f} {p["ball_r"] * S:.1f} 0 0 0 '
             f'{cx + 70 * S:.1f} {bt - 40 * S:.1f}" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="6 4"/>')
    # the table and the dock's cable leaving at the back (drawn on the right)
    o.append(line(cx - r_d - 60, ty, cx + r_d + 140, ty, 1.0, MUTED))
    o.append(line(cx + r_d, ty - 3 * S, cx + r_d + 130, ty - 3 * S, 4.0, '#141414'))
    o.append(text(cx + r_d + 135, ty - 3 * S - 26, 'USB-C cable to the adapter', 12, 'end', MUTED))
    # dimensions and callouts
    o.append(dim_h(cx - r_d, cx + r_d, ty + 26, 'dock Ø150'))
    o.append(dim_h(cx - r_p, cx + r_p, ty + 48, 'pocket Ø122 × 1.5'))
    o.append(dim_v(cx - r_d - 14, top, ty, '8', left=True))
    o.append(dim_v(cx + rb + 34, bt, top + ph, 'base 30'))
    lx, ly = cx - r_d - 30, bt + 4 * S
    o.append(text(lx, ly, 'gold spring pins at r 30 and r 44,', 12, 'end'))
    o.append(text(lx, ly + 16, 'on the 170° line, through the hatch', 12, 'end'))
    o.append(line(lx + 4, ly - 4, cx - 44 * S, top + ph - 9 * S, 0.8))
    o.append(text(cx, bt + 13 * S, 'Core’s base 120 × 30: cells, chassis, ballast (unchanged)', 12, 'middle', '#F2EEE8'))
    o.append(text(cx, ty + 74, 'the dock: polished black cast acrylic, two 304 stainless rings pressed in flush', 12, 'middle'))
    o.append(text(cx, bt - 46 * S, 'the ball (unchanged)', 12, 'middle', MUTED))
    return ''.join(o)


def plan(cx, cy):
    p = D; o = []
    S = PS * globals()['S']
    r_d, r_p = p['dock_d'] / 2 * S, p['pocket_d'] / 2 * S
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r_d:.1f}" fill="#2A2927" stroke="{INK}" stroke-width="1.4"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r_p:.1f}" fill="#232220" stroke="#6B6761" stroke-width="1"/>')
    for r in p['ring_r']:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r * S:.1f}" fill="none" stroke="#C9C7C1" stroke-width="{p["ring_w"] * S:.1f}"/>')
    # the cable's notch at the back (up in the plan)
    o.append(rect(cx - 4 * S, cy - r_d - 1, 8 * S, 6 * S, fill='#FFFFFF', c=INK, sw=1.0))
    o.append(line(cx, cy - r_d - 1, cx, cy - r_d - 70, 4.0, '#141414'))
    o.append(dim_h(cx - p['ring_r'][1] * S, cx + p['ring_r'][1] * S, cy + r_d + 26, '− ring Ø88 (4 wide)'))
    o.append(dim_h(cx - p['ring_r'][0] * S, cx + p['ring_r'][0] * S, cy + r_d + 50, '+ ring Ø60 (4 wide)'))
    o.append(text(cx, cy + r_d + 80, 'concentric: Core charges at any rotation', 13))
    o.append(text(cx + 8, cy - r_d - 52, 'back', 12, 'start', MUTED))
    return ''.join(o)


def main():
    W, H = 1900, 980
    body = [f'<rect width="{W}" height="{H}" fill="#F4F1EC"/>',
            text(60, 60, 'Core on its contact dock (CORE-RECHARGE.md, route b): a proposal', 22, 'start', INK, '600'),
            text(60, 88, 'Section through the axis (left) and the dock’s plan (right). Millimeters. Core’s CAD unchanged until '
                         'the owner signs.', 14, 'start', MUTED),
            section(700, 790), plan(1560, 480),
            text(60, H - 40, 'Off the dock the pins are dead (an ideal diode on each input); the rings are powered only '
                             'when the dock sees the lamp’s 47 kΩ sense resistor.', 13, 'start', MUTED)]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT + '.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                                  + ''.join(body) + '</svg>')
    # ImageMagick here has no SVG delegate: Chromium (headless, pre-installed) draws it
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage("
          f"{{viewport:{{width:{W},height:{H}}}}});await p.goto('file://{OUT}.svg');await p.screenshot({{path:'{OUT}.png'}});"
          "await b.close();})();")
    subprocess.run(['node', '-e', js], check=True)
    print(os.path.relpath(OUT + '.png', ROOT))


if __name__ == '__main__':
    main()
