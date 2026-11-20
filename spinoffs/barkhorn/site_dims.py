"""The two dimension drawings for the site (the coordinator, 20 Nov 14:33), made from the lanes' own SVGs without
redrawing: the workshop header lines are dropped, every "X mm (Y in)" label is set inches first ("Y in (X mm)") by
reordering its own glyphs (the same characters, so the same width and center), the blank margin is cropped, and a 2x
picture is rendered for the page. The SVG stays the file a visitor opens to enlarge.

  python3 site_dims.py <tropos-dims.svg> <mantle-dimensions.svg>
writes dims-site/tropos-dims.svg, .png and dims-site/mantle-dims.svg, .png next to this file.
Sources: r33-speaker-horn renders/2026-11-20/barkhorn/dims/tropos-dims.svg; r48-mantle-design
spinoffs/barkhorn/companions/mantle-r48/drawings/mantle-dimensions.svg.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'dims-site')
HEADERS = {'tropos': ('TROPOS', 'Overall dimensions'), 'mantle': ('Mantle (Strata Float v3)', 'Dimensions from the CAD', 'Deck ', 'Height ', 'Millimeters rounded')}
LABEL = re.compile(r'^(.*?)(\d+(?:\.\d+)?) mm \((\d+(?:\.\d+)?) in\)$')


def inches_first(group, text):
    m = LABEL.match(text)
    if not m:
        return group
    prefix, mm, inch = m.groups()
    new = f'{prefix}{inch} in ({mm} mm)'
    assert sorted(new) == sorted(text), (text, new)
    uses = list(re.finditer(r'<use xlink:href="#([^"]+)"(?: transform="translate\(([-\d.]+) 0\)")?/>', group))
    assert len(uses) == len(text), ('glyph count', text, len(uses))
    xs = [float(u.group(2) or 0) for u in uses]
    adv = {}
    for i, ch in enumerate(text[:-1]):
        adv.setdefault(ch, xs[i + 1] - xs[i])
    glyph = {ch: uses[i].group(1) for i, ch in enumerate(text)}
    x = xs[len(prefix)]
    out = [u.group(0) for u in uses[:len(prefix)]]
    for i, ch in enumerate(new[len(prefix):]):
        out.append(f'<use xlink:href="#{glyph[ch]}" transform="translate({x:.6f} 0)"/>' if x else f'<use xlink:href="#{glyph[ch]}"/>')
        if i < len(new) - len(prefix) - 1:
            x += adv[ch]
    a, b = uses[0].start(), uses[-1].end()
    return (group[:a] + '\n     '.join(out) + group[b:]).replace(f'<!-- {text} -->', f'<!-- {new} -->', 1)


def site_svg(src, name):
    s = open(src).read()
    def each(m):
        tid, text, body = m.group(1), m.group(2).replace('\n', ' '), m.group(0)
        if any(text.startswith(h) for h in HEADERS[name]):
            return ''
        return inches_first(body, text)
    s, n = re.subn(r'<g id="(text_\d+)">\s*<!-- (.*?) -->.*?</g>\s*</g>', each, s, flags=re.S)
    assert n, name
    assert not any(h in s for h in ('Strata Float', 'Drawn from the CAD', 'TROPOS --')), name
    return s


def render(svg_path, png_path, width=2400):
    """Render with Chromium; crop the viewBox to the drawn pixels (matplotlib's white page out) and render again at full width."""
    import subprocess
    from PIL import Image, ImageOps
    js = r"""
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [svg, png, W] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +W, height: 1000 } });
  await p.setContent(`<html><body style="margin:0;background:#fff">${fs.readFileSync(svg, 'utf8').replace(/^<\?xml[^>]*>\s*<!DOCTYPE[^>]*>/, '')}</body></html>`);
  await p.evaluate(W => { const s = document.querySelector('svg'), vb = s.viewBox.baseVal; s.setAttribute('width', W); s.setAttribute('height', Math.round(W * vb.height / vb.width)); }, +W);
  await (await p.$('svg')).screenshot({ path: png }); await b.close(); })();
"""
    run = os.path.join(OUT, '_render.cjs'); open(run, 'w').write(js)
    shoot = lambda: subprocess.check_call(['node', run, svg_path, png_path, str(width)])
    s = open(svg_path).read()
    vb = [float(v) for v in re.search(r'viewBox="([^"]*)"', s).group(1).split()]
    shoot()
    im = Image.open(png_path).convert('L'); k = im.width / vb[2]
    x0, y0, x1, y1 = ImageOps.invert(im).point(lambda v: 255 if v > 12 else 0).getbbox()
    pad = 14 * k
    nb = [vb[0] + (x0 - pad) / k, vb[1] + (y0 - pad) / k, (x1 - x0 + 2 * pad) / k, (y1 - y0 + 2 * pad) / k]
    s = re.sub(r'<svg ([^>]*?)width="[^"]*" height="[^"]*" viewBox="[^"]*"',
               lambda m: f'<svg {m.group(1)}width="{nb[2]:.1f}pt" height="{nb[3]:.1f}pt" viewBox="{nb[0]:.3f} {nb[1]:.3f} {nb[2]:.3f} {nb[3]:.3f}"', s, count=1)
    open(svg_path, 'w').write(s)
    shoot(); os.remove(run)


def main(tropos, mantle):
    os.makedirs(OUT, exist_ok=True)
    for name, src in (('tropos', tropos), ('mantle', mantle)):
        svg = os.path.join(OUT, f'{name}-dims.svg')
        open(svg, 'w').write(site_svg(src, name))
        render(svg, os.path.join(OUT, f'{name}-dims.png'))
        print(name, os.path.getsize(svg), os.path.getsize(os.path.join(OUT, f'{name}-dims.png')))


if __name__ == '__main__':
    main(*sys.argv[1:3])
