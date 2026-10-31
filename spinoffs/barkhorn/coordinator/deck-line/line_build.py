#!/usr/bin/env python3
"""Build the deck's "line" slide: one room picture, full bleed, with magazine callouts.

usage: line_build.py spec.json outdir
Writes outdir/slide.html (the deck section, image from spec["src"]) and outdir/preview.html
(the same section with the local image and fonts, for Playwright), and prints a contrast report.
Ink is chosen per text block from the picture under it: dark ink on light ground, light on dark.
"""
import json, sys, os, math
from PIL import Image

DARK = (0x1C, 0x1A, 0x18)      # deck ink
LIGHT = (0xF4, 0xF1, 0xEC)     # deck paper
ACC_ON_LIGHT = '#B23A17'       # deck eyebrow on paper
ACC_ON_DARK = '#F08A5D'        # deck eyebrow on dark (home slide)

def lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def lum(rgb):
    r, g, b = rgb
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

LD, LL = lum(DARK), lum(LIGHT)

def ratio(a, b):
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)

class Ground:
    def __init__(self, path, W=1920, H=1080):
        im = Image.open(path).convert('RGB')
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
        self.im = im

    def stats(self, x0, y0, x1, y1, step=3):
        v = []
        for y in range(max(0, int(y0)), min(1080, int(y1)), step):
            for x in range(max(0, int(x0)), min(1920, int(x1)), step):
                v.append(lum(self.im.getpixel((x, y))))
        v.sort()
        n = len(v)
        return v[int(n * 0.03)], v[n // 2], v[int(n * 0.97) - 1]

    def ink(self, box, force=None):
        lo, med, hi = self.stats(*box)
        dark_worst = ratio(LD, lo)      # dark ink is weakest on the darkest ground
        light_worst = ratio(LL, hi)     # light ink is weakest on the brightest ground
        if force == 'dark' or (force is None and dark_worst >= light_worst):
            return 'dark', dark_worst, (lo, med, hi)
        return 'light', light_worst, (lo, med, hi)

def hexc(rgb):
    return '#%02X%02X%02X' % rgb

def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;'))

def build(spec, ground):
    S = spec.get('style', {})
    name_px = S.get('name_px', 34)
    kind_px = S.get('kind_px', 16)
    line_px = S.get('line_px', 22)
    num = S.get('numbers', False)
    leader_w = S.get('leader_w', 1.5)
    report = []
    parts = []
    svg = []

    # header
    h = spec['header']
    hb = (h['x'], h['y'], h['x'] + h['w'], h['y'] + h.get('h', 150))
    ink, cr, st = ground.ink(hb, h.get('ink'))
    col = hexc(DARK if ink == 'dark' else LIGHT)
    acc = ACC_ON_LIGHT if ink == 'dark' else ACC_ON_DARK
    report.append(('header', ink, cr, st))
    align = h.get('align', 'left')
    parts.append(
        f'<div style="position:absolute;left:{h["x"]}px;top:{h["y"]}px;width:{h["w"]}px;'
        f'display:flex;flex-direction:column;gap:14px;text-align:{align}">'
        f'<p style="font-family:\'IBM Plex Mono\', \'Courier New\', monospace;font-size:22px;letter-spacing:4px;'
        f'text-transform:uppercase;color:{acc}">{esc(h["eyebrow"])}</p>'
        f'<h2 style="font-size:{h.get("px", 60)}px;font-weight:600;line-height:1.08;letter-spacing:-0.5px;'
        f'color:{col};text-wrap:balance">{esc(h["title"])}</h2></div>')

    for i, c in enumerate(spec['callouts'], 1):
        lb = c['label']
        lx, ly, lw = lb['x'], lb['y'], lb['w']
        lh = lb.get('h', name_px * 1.2 + kind_px * 1.6 + line_px * 1.35 * lb.get('lines', 1) + 20)
        box = (lx - 6, ly - 6, lx + lw + 6, ly + lh + 6)
        ink, cr, st = ground.ink(box, c.get('ink'))
        col = DARK if ink == 'dark' else LIGHT
        sub = 'rgba(28,26,24,0.78)' if ink == 'dark' else 'rgba(244,241,236,0.84)'
        ring = 'rgba(244,241,236,0.7)' if ink == 'dark' else 'rgba(28,26,24,0.55)'
        report.append((c['id'], ink, cr, st))
        align = lb.get('align', 'left')
        numhtml = (f'<span style="font-family:\'IBM Plex Mono\', \'Courier New\', monospace;font-size:{kind_px}px;'
                   f'letter-spacing:2px;color:{sub};margin-right:14px">{i:02d}</span>') if num else ''
        parts.append(
            f'<div style="position:absolute;left:{lx}px;top:{ly}px;width:{lw}px;display:flex;flex-direction:column;'
            f'gap:6px;text-align:{align}">'
            f'<p style="font-family:\'IBM Plex Mono\', \'Courier New\', monospace;font-size:{kind_px}px;letter-spacing:3px;'
            f'text-transform:uppercase;color:{sub}">{numhtml}{esc(c["kind"])}</p>'
            f'<h3 style="font-size:{name_px}px;font-weight:600;line-height:1.1;letter-spacing:-0.2px;color:{hexc(col)}">'
            f'{esc(c["name"])}</h3>'
            f'<p style="font-size:{line_px}px;line-height:1.35;color:{sub}">{esc(c["line"])}</p></div>')
        # The owner ruled out leader lines and dots (2026-10-31): labels sit beside their objects.
        # Leaders are drawn only if a spec asks for them explicitly.
        if not S.get('leaders', False) or 'anchor' not in c:
            continue
        ax, ay = c['anchor']
        tx, ty = c.get('attach') or (lx - 14 if align == 'left' else lx + lw + 14, ly + kind_px * 0.8)
        pts = c.get('via')
        path = [(ax, ay)] + ([tuple(p) for p in pts] if pts else []) + [(tx, ty)]
        d = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in path)
        stroke = hexc(col)
        svg.append(f'<path d="{d}" fill="none" stroke="{ring}" stroke-width="{leader_w + 2}" stroke-linecap="round"/>')
        svg.append(f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{leader_w}" stroke-linecap="round"/>')
        svg.append(f'<circle cx="{ax}" cy="{ay}" r="6.5" fill="{stroke}" stroke="{ring}" stroke-width="2.5"/>')

    f = spec.get('foot')
    if f:
        fb = (f['x'], f['y'] - 4, f['x'] + f['w'], f['y'] + 26)
        ink, cr, st = ground.ink(fb, f.get('ink'))
        col = 'rgba(28,26,24,0.8)' if ink == 'dark' else 'rgba(244,241,236,0.86)'
        report.append(('foot', ink, cr, st))
        parts.append(
            f'<p style="position:absolute;left:{f["x"]}px;top:{f["y"]}px;width:{f["w"]}px;text-align:{f.get("align", "right")};'
            f'font-family:\'IBM Plex Mono\', \'Courier New\', monospace;font-size:16px;letter-spacing:1.5px;'
            f'color:{col}">{esc(f["text"])}</p>')

    overlay = ('<svg width="1920" height="1080" viewBox="0 0 1920 1080" aria-hidden="true" '
               'style="position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible">'
               + ''.join(svg) + '</svg>') if svg else ''
    return parts, overlay, report

def section(spec, src, parts, overlay):
    img = (f'<img src="{src}" alt="{esc(spec["alt"])}" style="position:absolute;left:0;top:0;width:1920px;'
           f'height:1080px;object-fit:cover;object-position:{spec.get("pos", "50% 50%")}">')
    return (f'<section id="line" data-transition="fade" style="background:#1C1A18;color:#F4F1EC;'
            f'font-family:\'Instrument Sans\', Arial, sans-serif;padding:0">\n'
            + img + '\n' + (overlay + '\n' if overlay else '') + '\n'.join(parts) + '\n'
            + f'<aside>{esc(spec["notes"])}</aside>\n</section>\n')

def main():
    spec = json.load(open(sys.argv[1]))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    ground = Ground(spec['ground'])
    parts, overlay, report = build(spec, ground)
    open(os.path.join(out, 'slide.html'), 'w').write(section(spec, spec['src'], parts, overlay))
    here = os.path.dirname(os.path.abspath(__file__))
    prev = section(spec, os.path.relpath(os.path.abspath(spec['ground']), os.path.abspath(out)), parts, overlay)
    fonts = os.path.relpath(os.path.join(here, 'fonts', 'local.css'), os.path.abspath(out))
    open(os.path.join(out, 'preview.html'), 'w').write(
        '<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="' + fonts + '">'
        '<style>*{margin:0;padding:0;box-sizing:border-box}body{width:1920px;height:1080px;overflow:hidden;'
        'background:#000}section{position:relative;width:1920px;height:1080px;overflow:hidden}'
        'aside{display:none}</style>' + prev)
    worst = 99
    for name, ink, cr, (lo, med, hi) in report:
        flag = '' if cr >= 4.5 else '  <-- below 4.5:1'
        worst = min(worst, cr)
        print(f'{name:12s} {ink:5s} worst-case {cr:4.1f}:1  ground L p3={lo:.3f} med={med:.3f} p97={hi:.3f}{flag}')
    print(f'worst {worst:.1f}:1')

if __name__ == '__main__':
    main()
