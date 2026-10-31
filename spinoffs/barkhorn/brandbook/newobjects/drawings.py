"""Dimensioned drawings of the six, as SVG (then PNG through Chromium). Run: python3 drawings.py
Views are orthographic, first angle; dimensions in mm. Every figure is from six.py's dims."""
import math, os
from contours import layers

INK, MUTED, PAPER, RULE = '#1C1A18', '#5E5A53', '#F4F1EC', '#B9B2A6'
TINT = dict(ember='#C92118', dust='#E06718', acid='#E2AA15', poison='#367424', ice='#2584BE', haze='#5B3197', fog='#D5DFE0', smoke='#57545F')
ORDER = ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']
W, H = 1400, 900

class D:
    def __init__(s, title, sub, num):
        s.e, s.title, s.sub, s.num = [], title, sub, num
    def add(s, x): s.e.append(x)
    def line(s, x1, y1, x2, y2, w=1.4, c=INK, dash=None):
        s.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    def rect(s, x, y, w, h, fill='none', sw=1.4, op=1, dash=None):
        s.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" fill-opacity="{op}" stroke="{INK}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    def circle(s, cx, cy, r, fill='none', sw=1.4, op=1, dash=None):
        s.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" fill-opacity="{op}" stroke="{INK}" stroke-width="{sw}"' + (f' stroke-dasharray="{dash}"' if dash else '') + '/>')
    def poly(s, pts, fill='none', sw=1.2, op=1, close=True):
        d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        s.add(f'<{"polygon" if close else "polyline"} points="{d}" fill="{fill}" fill-opacity="{op}" stroke="{INK}" stroke-width="{sw}"/>')
    def text(s, x, y, t, size=13, anchor='middle', c=INK, mono=True, rot=0):
        fam = "'IBM Plex Mono', monospace" if mono else "'Instrument Sans', sans-serif"
        tr = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ''
        s.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" fill="{c}" text-anchor="{anchor}"{tr}>{t}</text>')
    def dimh(s, x1, x2, y, label, ext_from=None):
        if ext_from is not None:
            s.line(x1, ext_from, x1, y + 5, 0.7, MUTED); s.line(x2, ext_from, x2, y + 5, 0.7, MUTED)
        s.line(x1, y, x2, y, 0.8, MUTED)
        for x, d in ((x1, 1), (x2, -1)):
            s.poly([(x, y), (x + 8 * d, y - 3), (x + 8 * d, y + 3)], fill=MUTED, sw=0)
        s.text((x1 + x2) / 2, y - 6, label, 12, c=INK)
    def dimv(s, y1, y2, x, label, ext_from=None):
        if ext_from is not None:
            s.line(ext_from, y1, x - 5, y1, 0.7, MUTED); s.line(ext_from, y2, x - 5, y2, 0.7, MUTED)
        s.line(x, y1, x, y2, 0.8, MUTED)
        for y, d in ((y1, 1), (y2, -1)):
            s.poly([(x, y), (x - 3, y + 8 * d), (x + 3, y + 8 * d)], fill=MUTED, sw=0)
        s.text(x - 8, (y1 + y2) / 2, label, 12, c=INK, rot=-90)
    def label(s, x, y, t):
        s.text(x, y, t.upper(), 11, c=MUTED)
    def svg(s):
        tb = (f'<rect x="{W-430}" y="{H-110}" width="400" height="80" fill="none" stroke="{INK}" stroke-width="1"/>'
              f'<text x="{W-415}" y="{H-80}" font-family="Instrument Sans" font-size="22" font-weight="600" fill="{INK}">{s.title}</text>'
              f'<text x="{W-415}" y="{H-56}" font-family="IBM Plex Mono" font-size="11" fill="{MUTED}">{s.sub.upper()}</text>'
              f'<text x="{W-415}" y="{H-40}" font-family="IBM Plex Mono" font-size="10" fill="{MUTED}">MM · FIRST ANGLE · PROPOSAL 2026-10-31 · EARF NO-{s.num}</text>')
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
                f'<rect width="{W}" height="{H}" fill="{PAPER}"/><rect x="20" y="20" width="{W-40}" height="{H-40}" fill="none" stroke="{INK}" stroke-width="1.5"/>'
                + ''.join(s.e) + tb + '</svg>')

def moho():
    d = D('Moho', 'record weight · four layers 1/2" · brass core', '01'); k = 5.5
    x0, y0 = 220, 560; w, h = 66 * k, 50.8 * k
    tints = ['ember', 'acid', 'ice', 'smoke']
    for i, t in enumerate(tints):
        d.rect(x0, y0 - (i + 1) * 12.7 * k, w, 12.7 * k, fill=TINT[t], op=0.35, sw=1.2)
    d.rect(x0 + (66 - 25) / 2 * k, y0 - h, 25 * k, h, fill='#B08D57', op=0.35, sw=1, dash='6 4')
    d.rect(x0 + (66 - 7.6) / 2 * k, y0 - 22 * k, 7.6 * k, 22 * k, sw=1, dash='4 3')
    d.line(x0 + 3 * k, y0, x0 + 13 * k, y0, 3, PAPER); d.line(x0 + 53 * k, y0, x0 + 63 * k, y0, 3, PAPER)
    d.dimh(x0, x0 + w, y0 + 50, 'Ø 66', ext_from=y0 + 2)
    d.dimv(y0 - h, y0, x0 - 40, '50.8 (4 × 12.7)', ext_from=x0 - 2)
    d.dimh(x0 + (66 - 25) / 2 * k, x0 + (66 + 25) / 2 * k, y0 - h - 30, 'Ø 25 brass', ext_from=y0 - h - 2)
    d.text(x0 + w + 20, y0 - 11 * k, 'spindle bore Ø 7.6 × 22', 11, 'start', MUTED)
    d.text(x0 + w + 20, y0 + 4, 'relieved ring: rests on the label', 11, 'start', MUTED)
    d.label(x0 + w / 2, y0 + 110, 'Front elevation (section through the core dashed)')
    cx, cy = 980, 380
    d.circle(cx, cy, 33 * k, fill=TINT['smoke'], op=0.3); d.circle(cx, cy, 12.5 * k, fill='#B08D57', op=0.35, dash='6 4'); d.circle(cx, cy, 3.8 * k, dash='4 3')
    d.dimh(cx - 33 * k, cx + 33 * k, cy + 33 * k + 40, 'Ø 66', ext_from=cy)
    d.label(cx, cy + 33 * k + 95, 'Plan')
    return d

def lithos():
    d = D('Lithos', 'floor lamp · 87 rings 1/2" · nine clear guides', '02'); k = 0.6
    x0, base_y = 300, 820
    d.rect(x0 - 160 * k, base_y - 20 * k, 320 * k, 20 * k, fill=INK, op=0.85)
    counts = [10, 14, 7, 16, 9, 12, 8, 11]
    y = base_y - 20 * k
    tints = list(reversed(ORDER))
    g = 5.6
    for i, (n, t) in enumerate(zip(counts, tints)):
        d.rect(x0 - 55 * k, y - g * k, 110 * k, g * k, fill='#FFFFFF', op=0.9, sw=0.8); y -= g * k
        hh = n * 12.65 * k
        d.rect(x0 - 55 * k, y - hh, 110 * k, hh, fill=TINT[t], op=0.45, sw=1); y -= hh
    d.rect(x0 - 55 * k, y - g * k, 110 * k, g * k, fill='#FFFFFF', op=0.9, sw=0.8); y -= g * k
    top = y
    d.line(x0 - 38 * k, top, x0 - 38 * k, base_y - 20 * k, 0.9, MUTED, '6 4'); d.line(x0 + 38 * k, top, x0 + 38 * k, base_y - 20 * k, 0.9, MUTED, '6 4')
    d.dimv(top, base_y, x0 - 160 * k - 40, '≈ 1,120 overall', ext_from=x0 - 60 * k)
    d.dimh(x0 - 55 * k, x0 + 55 * k, top - 22, 'Ø 110', ext_from=top - 2)
    d.dimh(x0 - 160 * k, x0 + 160 * k, base_y + 34, 'Ø 320 steel base', ext_from=base_y)
    d.text(x0 + 55 * k + 18, top + 30, 'uplight in the bore, ≈ 900 lm 2700 K (est.)', 11, 'start', MUTED)
    d.text(x0 + 55 * k + 18, top + 160, 'clear 3030 guide, 5.6, edge-lit from the bore', 11, 'start', MUTED)
    d.text(x0 + 55 * k + 18, top + 290, 'bands: 7 to 16 rings of 12.65 (bonded)', 11, 'start', MUTED)
    d.text(x0 + 55 * k + 18, top + 420, 'bore Ø 76: LED line and tube', 11, 'start', MUTED)
    cx, cy, s = 1000, 360, 1.2
    d.circle(cx, cy, 160 * s, fill=INK, op=0.08); d.circle(cx, cy, 55 * s, fill=TINT['ember'], op=0.4); d.circle(cx, cy, 38 * s, fill=PAPER, dash='6 4')
    d.dimh(cx - 38 * s, cx + 38 * s, cy + 6, 'Ø 76')
    d.dimh(cx - 160 * s, cx + 160 * s, cy + 160 * s + 40, 'Ø 320', ext_from=cy)
    d.label(cx, cy + 160 * s + 95, 'Plan')
    d.label(x0, 870, 'Elevation')
    return d

def ionos():
    d = D('Ionos', 'radio and streamer · nine layers 1/2" · a turning top', '03'); k = 2.6
    x0, y0 = 120, 640; w = 200 * k
    for i in range(9):
        t = 'fog' if i == 4 else 'smoke'
        d.rect(x0, y0 - (i + 1) * 12.7 * k, w, 12.7 * k, fill=TINT[t], op=0.9 if i == 4 else 0.45, sw=1.1)
    d.rect(x0 + (200 - 100) / 2 * k, y0 - 9 * 12.7 * k, 100 * k, 12.7 * k, fill=TINT['smoke'], op=0.25, sw=1.4, dash='5 3')
    d.dimh(x0, x0 + w, y0 + 50, '200', ext_from=y0 + 2)
    d.dimv(y0 - 9 * 12.7 * k, y0, x0 - 38, '115 (9 × 12.7)', ext_from=x0 - 2)
    d.dimh(x0 + 50 * k, x0 + 150 * k, y0 - 9 * 12.7 * k - 28, 'Ø 100 top disc turns', ext_from=y0 - 9 * 12.7 * k - 2)
    d.text(x0 + w + 16, y0 - 4.5 * 12.7 * k + 4, '← clear layer, lit: the line', 11, 'start', MUTED)
    d.label(x0 + w / 2, y0 + 110, 'Front')
    sx = 860; sk = 2.6
    d.rect(sx, y0 - 115 * sk, 110 * sk, 115 * sk, fill=TINT['smoke'], op=0.35)
    d.rect(sx + 110 * sk - 4, y0 - 100 * sk, 4, 85 * sk, fill='#9AA0A6', sw=0.8)
    d.rect(sx + 12 * sk, y0 - 100 * sk, 80 * sk, 70 * sk, sw=0.9, dash='6 4')
    d.text(sx + 52 * sk, y0 - 62 * sk, 'pocket: computer, DAC, sensor', 10, c=MUTED)
    d.dimh(sx, sx + 110 * sk, y0 + 50, '110', ext_from=y0 + 2)
    d.text(sx + 110 * sk + 14, y0 - 60 * sk, 'back plate: line, optical, coax, USB-C', 11, 'start', MUTED)
    d.label(sx + 55 * sk, y0 + 110, 'Side (section)')
    return d

def cairn():
    d = D('Cairn', 'bookends · five layers 1/2" · two tints · satin sawn sides', '04'); k = 2.6
    x0, y0 = 160, 600
    slabs = [(160, 0, 'smoke'), (140, 8, 'smoke'), (120, -6, 'ember'), (100, 9, 'smoke'), (80, -4, 'smoke')]
    for i, (sw_, off, t) in enumerate(slabs):
        cx = x0 + 80 * k + off * k
        d.rect(cx - sw_ / 2 * k, y0 - (i + 1) * 12.7 * k, sw_ * k, 12.7 * k, fill=TINT[t], op=0.45, sw=1.2)
    d.rect(x0 + 30 * k, y0, 120 * k, 2 * k, fill='#9AA0A6', sw=0.8)
    d.dimh(x0, x0 + 160 * k, y0 + 50, '160', ext_from=y0 + 2)
    d.dimv(y0 - 5 * 12.7 * k, y0, x0 - 38, '63.5 (5 × 12.7)', ext_from=x0 - 2)
    d.text(x0 + 160 * k + 16, y0 + 6, '2 stainless tongue, 120 × 100', 11, 'start', MUTED)
    d.text(x0 + 160 * k + 16, y0 - 2.5 * 12.7 * k, 'slabs offset ±4 to 9', 11, 'start', MUTED)
    d.label(x0 + 80 * k, y0 + 110, 'Front')
    px, py = 880, 300; pk = 2.2
    for (sw_, off, t), dd in zip(slabs, [120, 110, 100, 90, 80]):
        d.rect(px + (80 + off - sw_ / 2) * pk, py + (60 - dd / 2) * pk, sw_ * pk, dd * pk, fill=TINT[t], op=0.18, sw=1)
    d.dimv(py, py + 120 * pk, px - 30, '120', ext_from=px)
    d.label(px + 80 * pk, py + 120 * pk + 60, 'Plan')
    return d

def bedrock():
    d = D('Bedrock', 'record stand · end-plates 2 × 1/2" · three steel rails', '05'); k = 1.3
    x0, y0 = 120, 640
    prof = [(0, 0), (300, 0), (300, 150), (250, 150), (250, 185), (180, 185), (180, 215), (90, 215), (90, 230), (0, 230)]
    d.poly([(x0 + x * k, y0 - y * k) for x, y in prof], fill=TINT['haze'], op=0.35, sw=1.4)
    for rx, ry in [(40, 30), (260, 30), (150, 120)]:
        d.circle(x0 + rx * k, y0 - ry * k, 10 * k, fill='#9AA0A6', op=0.8, sw=1)
    d.rect(x0 + 18 * k, y0 - 315 * k - 5, 270 * k, 315 * k, sw=0.7, dash='6 5')
    d.text(x0 + 150 * k, y0 - 300 * k, 'an LP, 315 sq.', 10, c=MUTED)
    d.dimh(x0, x0 + 300 * k, y0 + 45, '300', ext_from=y0 + 2)
    d.dimv(y0 - 230 * k, y0, x0 - 34, '230', ext_from=x0 - 2)
    d.label(x0 + 150 * k, y0 + 100, 'End elevation (rails Ø 20)')
    fx, fk = 760, 1.1
    for px in (0, 470 - 25.4):
        d.rect(fx + px * fk, y0 - 230 * fk, 25.4 * fk, 230 * fk, fill=TINT['haze'], op=0.45)
        d.line(fx + (px + 12.7) * fk, y0 - 230 * fk, fx + (px + 12.7) * fk, y0, 0.8, INK)
    for ry in (30, 120):
        d.rect(fx + 25.4 * fk, y0 - (ry + 10) * fk, 419.2 * fk, 20 * fk, fill='#9AA0A6', op=0.6, sw=0.9)
    d.dimh(fx, fx + 470 * fk, y0 + 45, '470', ext_from=y0 + 2)
    d.dimh(fx + 25.4 * fk, fx + 444.6 * fk, y0 - 230 * fk - 26, '419 between plates', ext_from=y0 - 230 * fk)
    d.label(fx + 235 * fk, y0 + 100, 'Front elevation (bond line at 12.7)')
    return d

def relief():
    d = D('Relief', 'lit relief · twelve contour layers 1/4" · 600 square', '06'); k = 1.15
    cx, cy = 400, 450
    d.rect(cx - 300 * k, cy - 300 * k, 600 * k, 600 * k, fill=TINT['ice'], op=0.08, sw=1.4)
    for lev, loops in layers():
        for l in loops:
            d.poly([(cx + x * k, cy - y * k) for x, y in l[::3]], fill=TINT['ice'], op=0.05, sw=0.9)
    d.dimh(cx - 300 * k, cx + 300 * k, cy + 300 * k + 36, '600', ext_from=cy + 300 * k)
    d.dimv(cy - 300 * k, cy + 300 * k, cx - 300 * k - 34, '600', ext_from=cx - 300 * k)
    d.label(cx, cy - 300 * k - 24, 'Front: the twelve contours')
    sx, sy, sk = 860, 470, 1.5
    import numpy as np
    from contours import grid, LEVELS
    xs, Hh = grid(); row = Hh[len(xs) // 2 + 15]; top = Hh.max()
    pts = []
    for i in range(0, len(xs), 2):
        lev = min(LEVELS, int(row[i] / top * (LEVELS + 0.4) + 0.5))
        pts.append((sx + (xs[i] + 300) * sk * 0.55, sy - (6 + lev * 5.6) * sk))
    poly = [(sx, sy)] + [(pts[0][0], sy - 6 * sk)] + pts + [(pts[-1][0], sy)]
    d.poly(poly, fill=TINT['ice'], op=0.3, sw=1)
    d.rect(sx, sy, 600 * sk * 0.55, 6 * sk, fill='#9AA0A6', op=0.8, sw=0.8)
    d.dimv(sy - (6 + 12 * 5.6) * sk, sy + 6 * sk, sx - 26, '≈ 73', ext_from=sx)
    d.text(sx, sy + 40, 'Section, horizontal ×0.55: 12 × 5.6 layers on a 6 backing', 11, 'start', MUTED)
    d.text(sx, sy - 120 * sk, 'grazing LED bar in the top of the frame ↓', 11, 'start', MUTED)
    return d

if __name__ == '__main__':
    os.makedirs('drawings', exist_ok=True)
    for f in (moho, lithos, ionos, cairn, bedrock, relief):
        d = f()
        open(f'drawings/{f.__name__}.svg', 'w').write(d.svg())
        print('drew', f.__name__)
