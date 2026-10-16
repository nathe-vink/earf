"""Storyboards and contact sheets of the brand's motion and marks, for iterating and critiquing (round 25).

The owner: "Keep spitballing ideas and refining. Invoke whatever brand and animation skills you need and set up a
pipeline for iterating and critiquing and polish." This is the pipeline's eye. It plays the globe page's scenes frame by
frame (earth.py's __frame, as the videos do) and lays a scene out on one sheet: its frames at even times, each labelled
with its time, and under them its motion, the share of the picture that changes from one frame to the next at 30 frames
a second, so a stop, a hitch or a rush shows as a line a critic (or the owner) can point at. The marks go on a sheet the
same way, each style in every rail, so a critic sees the system at once. The sheets are what critic/PROMPT-brand.md
judges.

    python3 storyboard.py ident coin [--style discs] [--ground paper] [--n 12] [--out PATH]
    python3 storyboard.py scene core [--opts '{"ground": "night"}'] [--t1 2.4] [--out PATH]
    python3 storyboard.py marks [--styles discs acrylic even] [--out PATH]
    python3 storyboard.py svgs LABEL=FILE.svg[@#RRGGBB] ... [--cols 5] [--bg '#F2EFEA'] [--out PATH]
    python3 storyboard.py sizes LABEL=FILE.svg[@#RRGGBB] ... [--out PATH]   each at 300, 64, 32 and 16 px
    python3 storyboard.py check SHEET.json REPLY.json   a critic's motion tests against a sheet's sidecar
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import earth as E                                        # noqa: E402

FPS, W, H = 30, 960, 540                                 # the frames as captured
INK, MUTED, SHEET = (28, 26, 24), (110, 106, 98), (222, 220, 215)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def _font(px):
    try:
        return ImageFont.truetype(FONT, px)
    except OSError:
        return ImageFont.load_default()


def capture(scene, opts, t1=None, fps=FPS, w=W, h=H, page=None):
    """Every frame of a scene from 0 to t1 (default: the scene's own end) as PIL images, and their times."""
    tmp = tempfile.mkdtemp(prefix='story-')
    html = os.path.join(tmp, 'earth.html')
    open(html, 'w').write(page or E.standalone())
    js = os.path.join(tmp, 'cap.js')
    open(js, 'w').write(f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: {w}, height: {h} }}, deviceScaleFactor: 1 }});
  await p.goto('file://{html}#capture', {{ waitUntil: 'load' }});
  const o = {json.dumps(opts)};
  const end = await p.evaluate(([s, o]) => window.__frame(s, 0, o), ['{scene}', o]);
  const t1 = {json.dumps(t1)} ?? end, n = Math.floor(t1 * {fps} + 1e-6) + 1;
  for (let i = 0; i < n; i++) {{
    await p.evaluate(([s, t, o]) => window.__frame(s, t, o), ['{scene}', i / {fps}, o]);
    await p.screenshot({{ path: '{tmp}/f' + String(i).padStart(4, '0') + '.png' }});
  }}
  let marks = [];                                        // an ident's phases: its own (IDENTS[k].marks), then the globe whole, aside, EARF
  if ('{scene}' === 'ident') marks = await p.evaluate(k => {{ const T = identTimes(k), I = IDENTS[k];
    return [...(I.marks ? I.marks() : []), [I.dur, 'whole'], [T.move0, 'aside'], [T.word0, 'EARF']]; }}, o.kind);
  await b.close(); console.log(JSON.stringify({{ n, end, marks }}));
}})();
""")
    r = subprocess.run(['node', js], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-3000:])
    info = json.loads(r.stdout.strip().splitlines()[-1])
    frames = [Image.open(os.path.join(tmp, f'f{i:04d}.png')).convert('RGB') for i in range(info['n'])]
    shutil.rmtree(tmp)
    capture.marks = [tuple(m) for m in info.get('marks', [])]
    return frames, [i / fps for i in range(info['n'])], info['end']


def motion(frames):
    """The share of the picture that changes from each frame to the next (mean absolute difference, 0 to 1, on a
    small grey copy), one value per step."""
    g = [np.asarray(f.convert('L').resize((240, 135)), float) / 255 for f in frames]
    return [float(np.abs(b - a).mean()) for a, b in zip(g, g[1:])]


def _trace(m, times, picks, width, height=120, marks=()):
    """The motion as a line across the sheet, the storyboard's frames ticked on it, and `marks` (time, label) as
    dashed rules (where one phase hands over to the next)."""
    img = Image.new('RGB', (width, height), SHEET)
    d, f = ImageDraw.Draw(img), _font(13)
    x0, x1, y0, y1 = 56, width - 16, 14, height - 28
    t_end = times[-1] or 1
    X = lambda t: x0 + (x1 - x0) * t / t_end
    top = max(m) if m and max(m) > 0 else 1
    Y = lambda v: y1 - (y1 - y0) * v / top
    d.line([(x0, y1), (x1, y1)], fill=MUTED)
    for t, lab in marks:
        x = X(t)
        for yy in range(y0, y1, 6):
            d.line([(x, yy), (x, yy + 3)], fill=(150, 146, 138))
        d.text((x + 3, y0 - 2), lab, fill=MUTED, font=_font(11))
    pts = [(X((times[i] + times[i + 1]) / 2), Y(v)) for i, v in enumerate(m)]
    if len(pts) > 1:
        d.line(pts, fill=INK, width=2)
    for t in picks:
        d.line([(X(t), y1), (X(t), y1 + 5)], fill=INK, width=2)
    for k in range(0, int(t_end * 2) + 1):
        t = k / 2
        d.text((X(t) - 8, y1 + 8), f'{t:g}s', fill=MUTED, font=f)
    d.text((6, y0), 'motion', fill=MUTED, font=f)
    return img


STILL = 0.002                                            # under this share of the picture changing, a step is still


def metric(side, name, window):
    """A motion metric over a window of a sheet's sidecar: longest_still (s), peak, mean, or settle (s)."""
    t, m, dt = side['times'], side['motion'], 1 / side.get('fps', FPS)
    t0, t1 = window
    steps = [(t[i] + t[i + 1]) / 2 for i in range(len(m))]
    sel = [(tt, v) for tt, v in zip(steps, m) if t0 <= tt <= t1]
    if not sel:
        return None
    if name == 'peak':
        return max(v for _, v in sel)
    if name == 'mean':
        return sum(v for _, v in sel) / len(sel)
    if name == 'longest_still':
        best = run = 0
        for _, v in sel:
            run = run + 1 if v < STILL else 0
            best = max(best, run)
        return best * dt
    if name == 'settle':
        for tt, v in reversed(sel):
            if v >= STILL:
                return tt + dt / 2
        return sel[0][0]
    raise SystemExit(f'unknown metric {name}')


def check(side_path, reply_path):
    side, reply = json.load(open(side_path)), json.load(open(reply_path))
    ops = {'<': lambda a, b: a < b, '<=': lambda a, b: a <= b, '>': lambda a, b: a > b, '>=': lambda a, b: a >= b,
           'between': lambda a, b: b[0] <= a <= b[1]}
    out = []
    for c in reply.get('changes', []):
        acc = c.get('accept') or {}
        if acc.get('kind') == 'motion':
            v = metric(side, acc['metric'], acc.get('window', [0, side['times'][-1]]))
            ok = v is not None and ops[acc['op']](v, acc['value'])
            out.append(f"c{c.get('rank')}: {acc['metric']} {acc.get('window')} = {v if v is None else round(v, 4)} "
                       f"{acc['op']} {acc['value']}: {'PASS' if ok else 'FAIL'}")
        elif acc:
            out.append(f"c{c.get('rank')}: look ({acc.get('at')}): {acc.get('check')}")
    return out


def board(frames, times, title, n=12, cols=4, tw=400, picks=None, marks=(), note=''):
    """The sheet: a title, n frames at even times (or at `picks`), each with its time, and the motion trace."""
    m = motion(frames)
    if picks is None:
        picks = [times[-1] * k / (n - 1) for k in range(n)]
    idx = [min(range(len(times)), key=lambda i: abs(times[i] - t)) for t in picks]
    th = round(tw * frames[0].height / frames[0].width)
    rows, pad, head = (len(idx) + cols - 1) // cols, 14, 54
    width = cols * tw + (cols + 1) * pad
    tr = _trace(m, times, [times[i] for i in idx], width, marks=marks)
    img = Image.new('RGB', (width, head + rows * (th + 26 + pad) + tr.height + pad), SHEET)
    d = ImageDraw.Draw(img)
    d.text((pad, 12), title, fill=INK, font=_font(20))
    if note:
        d.text((pad, 36), note, fill=MUTED, font=_font(12))
    for j, i in enumerate(idx):
        r, c = divmod(j, cols)
        x, y = pad + c * (tw + pad), head + r * (th + 26 + pad)
        img.paste(frames[i].resize((tw, th), Image.LANCZOS), (x, y))
        d.rectangle([x - 1, y - 1, x + tw, y + th], outline=(185, 181, 173))
        d.text((x, y + th + 5), f'{j + 1:02d}   t = {times[i]:.2f} s', fill=MUTED, font=_font(13))
    img.paste(tr, (0, head + rows * (th + 26 + pad)))
    return img, m


def svg_sheet(items, cols=5, cell=300, bgs=None, title='', out=None):
    """SVGs (label, svg, ground colour) on one sheet, through the browser (so blends and gradients render as on the
    page)."""
    cells = ''.join(f'<figure style="background:{bg}"><div>{svg}</div><figcaption>{lab}</figcaption></figure>'
                    for lab, svg, bg in items)
    html = f"""<!doctype html><meta charset="utf-8"><style>
body {{ margin: 0; background: rgb{SHEET}; font: 13px DejaVu Sans, sans-serif; color: rgb{MUTED}; padding: 14px }}
h1 {{ font-size: 20px; font-weight: 400; color: rgb{INK}; margin: 0 0 12px }}
main {{ display: grid; grid-template-columns: repeat({cols}, {cell}px); gap: 14px }}
figure {{ margin: 0; border-radius: 4px; overflow: hidden }}
figure div {{ padding: 14%; }} figure svg {{ display: block; width: 100%; height: auto }}
figcaption {{ padding: 6px 8px; background: rgb{SHEET} }}
</style><h1>{title}</h1><main>{cells}</main>"""
    tmp = tempfile.mkdtemp(prefix='sheet-')
    open(os.path.join(tmp, 's.html'), 'w').write(html)
    js = os.path.join(tmp, 's.js')
    open(js, 'w').write(f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: {cols * (cell + 14) + 14}, height: 400 }}, deviceScaleFactor: 1 }});
  await p.goto('file://{tmp}/s.html', {{ waitUntil: 'load' }});
  await p.screenshot({{ path: '{out}', fullPage: true }});
  await b.close();
}})();
""")
    r = subprocess.run(['node', js], capture_output=True, text=True)
    shutil.rmtree(tmp)
    if r.returncode:
        raise SystemExit(r.stderr[-3000:])
    return out


def size_sheet(items, sizes=(300, 64, 32, 16), title='', out=None):
    """Each SVG (label, svg, ground colour) at several sizes in a row, at one pixel to one pixel, so a critic sees what
    survives small."""
    rows = ''.join(f'<div class="row" style="background:{bg}"><span>{lab}</span>' + ''.join(
        f'<div class="cell"><div style="width:{px}px;height:{px}px">{svg}</div><i>{px}</i></div>' for px in sizes) + '</div>'
        for lab, svg, bg in items)
    html = f"""<!doctype html><meta charset="utf-8"><style>
body {{ margin: 0; background: rgb{SHEET}; font: 13px DejaVu Sans, sans-serif; color: rgb{MUTED}; padding: 14px }}
h1 {{ font-size: 20px; font-weight: 400; color: rgb{INK}; margin: 0 0 12px }}
.row {{ display: flex; align-items: flex-end; gap: 28px; padding: 16px 20px; margin-bottom: 10px; border-radius: 4px }}
.row span {{ width: 150px; align-self: center; background: rgb{SHEET}; padding: 4px 6px; border-radius: 3px }}
.cell {{ display: grid; justify-items: center; gap: 6px }} .cell i {{ font-style: normal; font-size: 11px; background: rgb{SHEET}; padding: 0 4px }}
.cell svg {{ display: block; width: 100%; height: 100% }}
</style><h1>{title}</h1>{rows}"""
    tmp = tempfile.mkdtemp(prefix='sizes-')
    open(os.path.join(tmp, 's.html'), 'w').write(html)
    js = os.path.join(tmp, 's.js')
    open(js, 'w').write(f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: {200 + sum(sizes) + 28 * len(sizes) + 60}, height: 300 }}, deviceScaleFactor: 1 }});
  await p.goto('file://{tmp}/s.html', {{ waitUntil: 'load' }});
  await p.screenshot({{ path: '{out}', fullPage: true }});
  await b.close();
}})();
""")
    r = subprocess.run(['node', js], capture_output=True, text=True)
    shutil.rmtree(tmp)
    if r.returncode:
        raise SystemExit(r.stderr[-3000:])
    return out


def marks_sheet(styles=('discs', 'acrylic', 'even'), out=None):
    items = []
    for st in styles:
        for t, g, f in E.RAILS:
            items.append((f'{st}: {t.lower()}', E.mark_svg(st, f(), ground=g), E.NIGHT if g == 'night' else E.PAPER))
    return svg_sheet(items, cols=len(E.RAILS), cell=260, title='EARF globe: each style in every rail', out=out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('what', choices=['ident', 'scene', 'marks', 'svgs', 'sizes', 'check'])
    ap.add_argument('name', nargs='*')
    ap.add_argument('--style', default='discs')
    ap.add_argument('--ground', default='paper')
    ap.add_argument('--opts', default='{}')
    ap.add_argument('--n', type=int, default=12)
    ap.add_argument('--picks', help='the frames\' times instead of even ones, comma separated (e.g. a coin\'s faces)')
    ap.add_argument('--t1', type=float)
    ap.add_argument('--cols', type=int, default=5)
    ap.add_argument('--bg', default=E.PAPER)
    ap.add_argument('--styles', nargs='*', default=['discs', 'acrylic', 'even'])
    ap.add_argument('--out')
    a = ap.parse_args()
    if a.what == 'check':
        print('\n'.join(check(*a.name)))
        return
    if a.what == 'marks':
        print(marks_sheet(a.styles, out=os.path.abspath(a.out or 'marks.png')))
        return
    if a.what in ('svgs', 'sizes'):                      # LABEL=FILE.svg, or LABEL=FILE.svg@#RRGGBB for its own ground
        items = []
        for x in a.name:
            lab, f = x.split('=', 1)
            f, bg = f.split('@') if '@' in f else (f, a.bg)
            items.append((lab, open(f).read(), bg))
        if a.what == 'sizes':
            print(size_sheet(items, out=os.path.abspath(a.out or 'sizes.png')))
        else:
            print(svg_sheet(items, cols=a.cols, out=os.path.abspath(a.out or 'svgs.png')))
        return
    if a.what == 'ident':
        kind = a.name[0]
        opts = dict(kind=kind, style=a.style, ground=a.ground, **json.loads(a.opts))
        frames, times, end = capture('ident', opts, t1=a.t1)
        title = f'Ident: {kind} - {a.style} on {a.ground}'
    else:
        opts = json.loads(a.opts)
        frames, times, end = capture(a.name[0], opts, t1=a.t1)
        title = f'Scene: {a.name[0]} {json.dumps(opts)}'
    picks = [float(x) for x in a.picks.split(',')] if a.picks else None
    img, m = board(frames, times, title, n=a.n, picks=picks, marks=capture.marks,
                   note=f'{len(frames)} frames at {FPS} fps; the scene ends at {end:.2f} s')
    out = os.path.abspath(a.out or f'story-{a.name[0]}.png')
    img.save(out)
    side = dict(title=title, fps=FPS, end=end, times=times, motion=m, marks=capture.marks, opts=opts)
    json.dump(side, open(os.path.splitext(out)[0] + '.json', 'w'))
    print(out, f'motion: peak {max(m):.4f}, longest still {metric(side, "longest_still", [0, end]):.2f} s, '
               f'settles at {metric(side, "settle", [0, end]):.2f} s')


if __name__ == '__main__':
    main()
