"""EARF's ident, the brand animated as a film studio's is before the film (round 20, the owner: "I also would love the
brand to work like a movie studio animation before a movie starts, where the world and/or earf are animated somehow,
like a Spirograph type thing where a black dot rotates around several times to create a circle of circles, each
adopting a color as its mini circle is traced").

A black dot, the pen, starts at the centre and moves out to the top of the wheel. It draws each Cloud's circle in turn
from its outermost point, clockwise, the circle's colour sweeping in behind it, then glides along the rim to the next,
so the larger circle is drawn in the glides. Back at the centre it settles as the spindle's dot (in the six-round
version it first draws Fog's white disc and settles in it as Smoke's black). The wheel then moves aside and EARF is
drawn beside it, then its line. The geometry and colours are brand.py's wheel; the letters are marks.py's.

    python3 spinoffs/barkhorn/ident.py                      ->  brand/ident.html (a page that plays it)
    python3 spinoffs/barkhorn/ident.py --fragment PATH      ->  also the page as an Artifact's body (no html/head/body)
    python3 spinoffs/barkhorn/ident.py --video DIR          ->  also brand/ident-<eight|six>.mp4, 1280 x 720, 30 fps
                                                                (needs Playwright's Chromium and ffmpeg)
"""
import argparse, json, math, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import brand as B                                        # noqa: E402
import marks as M                                        # noqa: E402

OUT = os.path.join(HERE, 'brand')


def data():
    wheels = {}
    for name in B.WHEELS:
        cl, centre, dot = B.wheel(name)
        rec = lambda c: dict(name=c[0], colour=c[1], mode=c[2], cx=round(c[3], 5), cy=round(c[4], 5), r=round(c[5], 5),
                             a0=round(c[6], 5))
        wheels[name] = dict(circles=[rec(c) for c in cl], centre=rec(centre) if centre else None, dot=dot,
                            n=B.WHEELS[name]['n'], sw=round(B.WHEEL_SW / 225, 5))
    word = []
    for p in M.WORDMARK:
        if p[0] == 'rect':
            word.append(dict(pts=[[p[1], p[2]], [p[3], p[2]], [p[3], p[4]], [p[1], p[4]]]))
        elif p[0] == 'circle':
            word.append(dict(c=[p[1], p[2]], r=p[3]))
        else:
            word.append(dict(pts=[[round(x, 3), round(y, 3)] for x, y in p[1:]]))
    letters = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]             # E, A, R, F: which letter each shape belongs to
    assert len(letters) == len(word)
    clouds = [dict(num=num, name=name, colour=col) for key, line, num, name, col in M.SPEAKERS if line == 'Cloud']
    return dict(wheels=wheels, word=word, letters=letters, wordW=M.WORDMARK_W, wordSw=M.U * 0.8, clouds=clouds,
                paper=B.PAPER, ink=B.INK, frost=B.FROST)


PAGE = r"""<title>EARF Ident</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400..700&display=swap">
<style>
/* a screening room: the page dims round a paper screen where the ident plays; the brand's own paper, ink and faces */
:root {
  --page: #E9E5DE; --fg: #1C1A18; --muted: #5E5A53; --line: #CFC9BF; --screen: #F2EFEA; --screen-edge: #D9D3C9;
  --sans: 'Instrument Sans', Arial, sans-serif; --mono: 'IBM Plex Mono', 'Courier New', monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --page: #141311; --fg: #ECE8E1; --muted: #A39E95; --line: #34312C; --screen-edge: #2A2824; color-scheme: dark } }
:root[data-theme="dark"] { --page: #141311; --fg: #ECE8E1; --muted: #A39E95; --line: #34312C; --screen-edge: #2A2824;
  color-scheme: dark }
body { background: var(--page); color: var(--fg); font-family: var(--sans); font-size: 16px; line-height: 1.5;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 28px 48px }
main { max-width: 1080px; margin: 0 auto; display: grid; gap: 22px }
header { display: grid; gap: 6px }
.eyebrow { font-family: var(--mono); font-size: 13px; letter-spacing: 0.14em; text-transform: uppercase; color: var(--muted) }
h1 { margin: 0; font-size: clamp(30px, 5vw, 44px); line-height: 1.05; font-weight: 600; letter-spacing: -0.02em;
  text-wrap: balance }
header p { margin: 0; max-width: 62ch; color: var(--muted) }
.screen { position: relative; width: 100%; max-width: 100%; aspect-ratio: 16 / 9; background: var(--screen);
  border: 1px solid var(--screen-edge); border-radius: 4px; overflow: hidden }
.screen canvas { display: block; width: 100%; height: 100% }
.controls { display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between }
.seg { display: inline-flex; border: 1px solid var(--fg); border-radius: 999px; overflow: hidden }
.seg button, .play { font: 500 14px/1 var(--sans); color: var(--fg); background: transparent; border: 0; padding: 10px 16px;
  cursor: pointer }
.seg button[aria-pressed="true"] { background: var(--fg); color: var(--page) }
.play { border: 1px solid var(--fg); border-radius: 999px; display: inline-flex; gap: 8px; align-items: center }
.play svg { width: 12px; height: 12px; fill: currentColor }
button:focus-visible { outline: 2px solid var(--fg); outline-offset: 3px }
.legend { display: flex; flex-wrap: wrap; gap: 10px 22px; padding: 0; margin: 0; list-style: none }
.legend li { display: flex; gap: 8px; align-items: center; font-size: 14px }
.legend .sw { width: 16px; height: 16px; border-radius: 50%; border: 2px solid var(--fg); box-sizing: border-box; flex: none }
.legend .num { font-family: var(--mono); font-size: 12px; letter-spacing: 0.08em; color: var(--muted) }
.notes { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px 28px; border-top: 1px solid var(--line);
  padding-top: 18px }
.notes h2 { margin: 0 0 4px; font-family: var(--mono); font-size: 12px; font-weight: 500; letter-spacing: 0.14em;
  text-transform: uppercase; color: var(--muted) }
.notes p { margin: 0; font-size: 15px; min-width: 0 }
html.capture body { padding: 0 }
html.capture main > :not(.screen) { display: none }
html.capture main { max-width: none; gap: 0 }
html.capture .screen { border: 0; border-radius: 0; width: 100vw; height: 100vh; aspect-ratio: auto }
</style>

<main>
  <header>
    <div class="eyebrow">EARF</div>
    <h1>The ident</h1>
    <p>The globe drawn as the eight Clouds. A pen traces a ring of circles, each taking a speaker's colour as it closes,
      and the larger circle forms between them. Then the name.</p>
  </header>
  <div class="screen"><canvas id="stage" aria-label="EARF's ident: a black dot draws a ring of coloured circles, then the word EARF"></canvas></div>
  <div class="controls">
    <div class="seg" role="group" aria-label="Version">
      <button type="button" id="v-eight" aria-pressed="true">Eight circles</button>
      <button type="button" id="v-six" aria-pressed="false">Six circles</button>
    </div>
    <button type="button" class="play" id="play"><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 1l9 5-9 5z"/></svg>Play again</button>
  </div>
  <ul class="legend" id="legend"></ul>
  <section class="notes">
    <div><h2>The wheel</h2><p id="geo"></p></div>
    <div><h2>The colours</h2><p>Each circle is a Cloud's tint, and where two overlap the tints multiply, as two sheets of
      tinted acrylic do laid one on the other. Fog's white frosts what lies under it.</p></div>
    <div><h2>The pen</h2><p>It draws each circle from the point where it touches the rim, clockwise, then glides along the
      rim to the next. The glides draw the larger circle. It finishes at the centre, as a record's spindle.</p></div>
  </section>
</main>

<script>
const D = __DATA__;
const cv = document.getElementById('stage'), ctx = cv.getContext('2d');
const VW = 1920, VH = 1080;
let variant = 'eight', t0 = performance.now(), shown = 0, raf = 0;
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (location.hash === '#capture') document.documentElement.classList.add('capture');

const ease = x => x <= 0 ? 0 : x >= 1 ? 1 : (x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const sine = x => x <= 0 ? 0 : x >= 1 ? 1 : -(Math.cos(Math.PI * x) - 1) / 2;
const clamp01 = x => Math.max(0, Math.min(1, x));
const back = x => x <= 0 ? 0 : x >= 1 ? 1 : 1 + 2.70158 * Math.pow(x - 1, 3) + 1.70158 * Math.pow(x - 1, 2);   // overshoots a little
const lerp = (a, b, k) => a + (b - a) * k;

// the timeline: each step [kind, start, end, ...]; built once a version is chosen
function timeline(v) {
  const W = D.wheels[v], n = W.n, eight = v === 'eight';
  const dc = eight ? 0.5 : 0.62, dg = eight ? 0.2 : 0.25;
  const S = [];
  let t = 0.15;
  S.push(['appear', t, t + 0.4]); t += 0.4;
  S.push(['toRim', t, t + 0.4]); t += 0.4;
  for (let i = 0; i < n; i++) {
    S.push(['circle', t, t + dc, i]); t += dc;
    S.push(['glide', t, t + dg, i]); t += dg;
  }
  if (W.centre) {
    S.push(['toDisc', t, t + 0.3]); t += 0.3;
    S.push(['disc', t, t + 0.5]); t += 0.5;
    S.push(['toCentre', t, t + 0.22, 1]); t += 0.22;
  } else {
    S.push(['toCentre', t, t + 0.4, 0]); t += 0.4;
  }
  S.push(['settle', t, t + 0.32]); t += 0.32;
  const slide = t - 0.15;
  S.push(['slide', slide, slide + 0.9]);
  S.push(['word', slide + 0.7, slide + 2.06]);      // once the wheel has nearly moved aside
  S.push(['tag', slide + 1.9, slide + 2.6]);
  return { steps: S, end: slide + 2.9 };
}
let TL = timeline(variant);

function state(t) {
  const W = D.wheels[variant], n = W.n;
  const st = { fill: new Array(n).fill(0), rim: 0, disc: 0, pen: [0, 0], penR: 0, slide: 0, word: 0, tag: 0, dotGrow: 0 };
  const pen = 0.045;
  let penPos = [0, 0], penR = 0;
  for (const [k, a, b, i] of TL.steps) {
    const p = clamp01((t - a) / (b - a));
    if (t < a) continue;
    if (k === 'appear') { penR = pen * back(p); penPos = [0, 0]; }
    else if (k === 'toRim') { penPos = [0, lerp(0, -1, ease(p))]; }
    else if (k === 'circle') {
      const c = W.circles[i], e = sine(p), ang = c.a0 + e * 2 * Math.PI;
      st.fill[i] = e; penPos = [c.cx + c.r * Math.cos(ang), c.cy + c.r * Math.sin(ang)];
    }
    else if (k === 'glide') {
      const a0 = -Math.PI / 2 + 2 * Math.PI * i / n, ang = a0 + sine(p) * 2 * Math.PI / n;
      st.rim = (i + sine(p)) / n; penPos = [Math.cos(ang), Math.sin(ang)];
    }
    else if (k === 'toDisc') { const c = W.centre; penPos = [0, lerp(-1, c.cy - c.r, ease(p))]; }
    else if (k === 'disc') {
      const c = W.centre, e = sine(p), ang = c.a0 + e * 2 * Math.PI;
      st.disc = e; penPos = [c.cx + c.r * Math.cos(ang), c.cy + c.r * Math.sin(ang)];
    }
    else if (k === 'toCentre') { const y0 = i ? W.centre.cy - W.centre.r : -1; penPos = [0, lerp(y0, 0, ease(p))]; }
    else if (k === 'settle') { st.dotGrow = p; }
    else if (k === 'slide') { st.slide = ease(p); }
    else if (k === 'word') { st.word = (t - a) / (b - a); }
    else if (k === 'tag') { st.tag = ease(p); }
  }
  st.pen = penPos;
  // the dot: the pen, growing at the end into the centre's dot with a small overshoot
  const g = st.dotGrow, target = W.dot;
  st.penR = g > 0 ? lerp(pen, target, sine(Math.min(1, g * 1.25))) + Math.sin(Math.PI * g) * 0.01 : penR;
  return st;
}

function layout() {
  const s = 0.78, ww = 450 + 110 + D.wordW, x0 = (VW - ww * s) / 2;
  return { solo: { cx: VW / 2, cy: VH / 2, R: 330 }, lock: { cx: x0 + 225 * s, cy: VH / 2, R: 225 * s },
           word: { x: x0 + (450 + 110) * s, s, capTop: VH / 2 - (300 * s + 30 + 21) / 2 } };
}

function sector(c, e) {
  ctx.beginPath(); ctx.moveTo(c.cx, c.cy); ctx.arc(c.cx, c.cy, c.r, c.a0, c.a0 + e * 2 * Math.PI); ctx.closePath();
}

function drawWheel(st, W) {
  const sw = W.sw;
  ctx.save(); ctx.globalCompositeOperation = 'source-over';
  const fills = W.circles.map((c, i) => [c, st.fill[i]]);
  if (W.centre) fills.push([W.centre, st.disc]);
  for (const [c, e] of fills) {
    if (e <= 0) continue;
    ctx.globalCompositeOperation = c.mode === 'frost' ? 'source-over' : 'multiply';
    ctx.globalAlpha = c.mode === 'frost' ? D.frost : 0.82;
    ctx.fillStyle = c.colour; sector(c, e); ctx.fill();
  }
  ctx.restore();
  ctx.save(); ctx.strokeStyle = D.ink; ctx.lineWidth = sw; ctx.lineCap = 'round';
  for (const [c, e] of fills) {
    if (e <= 0) continue;
    ctx.beginPath(); ctx.arc(c.cx, c.cy, c.r, c.a0, c.a0 + e * 2 * Math.PI); ctx.stroke();
  }
  if (st.rim > 0) { ctx.beginPath(); ctx.arc(0, 0, 1, -Math.PI / 2, -Math.PI / 2 + st.rim * 2 * Math.PI); ctx.stroke(); }
  ctx.restore();
  if (st.penR > 0) { ctx.fillStyle = D.ink; ctx.beginPath(); ctx.arc(st.pen[0], st.pen[1], st.penR, 0, 2 * Math.PI); ctx.fill(); }
}

function primPath(p) {
  ctx.beginPath();
  if (p.c) { ctx.arc(p.c[0], p.c[1], p.r, -Math.PI / 2, 1.5 * Math.PI); return 2 * Math.PI * p.r; }
  let L = 0;
  p.pts.forEach((q, i) => { if (i) L += Math.hypot(q[0] - p.pts[i - 1][0], q[1] - p.pts[i - 1][1]); i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); });
  const a = p.pts[p.pts.length - 1], b = p.pts[0]; L += Math.hypot(a[0] - b[0], a[1] - b[1]); ctx.closePath();
  return L;
}

function drawWord(st, Ly) {
  if (st.word <= 0) return;
  ctx.save(); ctx.translate(Ly.word.x, Ly.word.capTop); ctx.scale(Ly.word.s, Ly.word.s);
  ctx.strokeStyle = D.ink; ctx.lineWidth = D.wordSw; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  D.word.forEach((p, i) => {
    const li = D.letters[i], q = sine(clamp01((st.word - li * 0.16) / 0.52));
    if (q <= 0) return;
    const L = primPath(p);
    ctx.setLineDash(q >= 1 ? [] : [L * q, L + 1]); ctx.stroke();
  });
  ctx.restore();
}

function drawTag(st, Ly) {
  if (st.tag <= 0) return;
  const text = 'NEATURE-INSPIRED LOUDSPEAKERS', size = 30, track = 0.12 * size;
  ctx.save(); ctx.globalAlpha = st.tag; ctx.fillStyle = D.ink;
  ctx.font = `500 ${size}px 'IBM Plex Mono', 'Courier New', monospace`; ctx.textBaseline = 'alphabetic';
  let x = Ly.word.x - 2, y = Ly.word.capTop + 300 * Ly.word.s + 30 + 21 + (1 - st.tag) * 10;
  for (const ch of text) { ctx.fillText(ch, x, y); x += ctx.measureText(ch).width + track; }
  ctx.restore();
}

function render(t) {
  shown = t;
  const W = D.wheels[variant], Ly = layout(), st = state(t);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.fillStyle = D.paper; ctx.fillRect(0, 0, cv.width, cv.height);
  const k = cv.width / VW; ctx.scale(k, k);
  const cx = lerp(Ly.solo.cx, Ly.lock.cx, st.slide), cy = lerp(Ly.solo.cy, Ly.lock.cy, st.slide), R = lerp(Ly.solo.R, Ly.lock.R, st.slide);
  ctx.save(); ctx.translate(cx, cy); ctx.scale(R, R); drawWheel(st, W); ctx.restore();
  drawWord(st, Ly); drawTag(st, Ly);
  ctx.restore();
}

function size() {
  const dpr = Math.min(2, window.devicePixelRatio || 1), w = cv.clientWidth || 960;
  cv.width = Math.round(w * dpr); cv.height = Math.round(w * dpr * VH / VW);
}

function loop(now) {
  const t = (now - t0) / 1000;
  render(Math.min(t, TL.end));
  if (t < TL.end) raf = requestAnimationFrame(loop);
}

function play() { cancelAnimationFrame(raf); t0 = performance.now(); raf = requestAnimationFrame(loop); }

function choose(v) {
  variant = v; TL = timeline(v);
  for (const id of ['eight', 'six']) document.getElementById('v-' + id).setAttribute('aria-pressed', String(id === v));
  geo(); reduce ? render(TL.end) : play();
}

function geo() {
  const W = D.wheels[variant], c = W.circles[0], R = Math.hypot(c.cx, c.cy);
  const f = x => x.toFixed(3).replace(/^0/, '');
  document.getElementById('geo').textContent = variant === 'eight'
    ? `Eight circles, each ${f(c.r)} of the wheel's radius, their centres on a ring at ${f(R)}, so each overlaps its two neighbours and touches the rim at one point. A dot at the centre, ${f(W.dot)} across the radius.`
    : `Six circles, each ${f(c.r)} of the wheel's radius, on a ring at ${f(R)}. Fog's white disc, ${f(W.centre.r)} across the radius, touches all six; Smoke's black dot sits in it.`;
}

document.getElementById('legend').innerHTML = D.clouds.map(c =>
  `<li><span class="sw" style="background:${c.colour}"></span><span class="num">${c.num}</span>${c.name}</li>`).join('');
document.getElementById('v-eight').addEventListener('click', () => choose('eight'));
document.getElementById('v-six').addEventListener('click', () => choose('six'));
document.getElementById('play').addEventListener('click', play);
window.addEventListener('resize', () => { size(); render(shown); });   // the frame last drawn, at the new size
window.__frame = (t, v) => { if (v && v !== variant) { variant = v; TL = timeline(v); } render(t); return TL.end; };

size(); geo();
(document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(() => {
  if (document.documentElement.classList.contains('capture')) { size(); render(0); return; }
  reduce ? render(TL.end) : play();
});
</script>
"""


def page():
    return PAGE.replace('__DATA__', json.dumps(data(), separators=(',', ':')))


def standalone():
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, '
            'initial-scale=1, viewport-fit=cover"></head><body>\n' + page() + '\n</body></html>\n')


FONTS = '/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/r8/fonts-dl/local.css'


def video(out_dir, variant, fps=30, w=1280, h=720):
    """The ident to an MP4: each frame drawn at its own time by the page's __frame, screenshot, then ffmpeg. The faces
    come from local copies (FONTS) where they exist, as this machine's browser cannot reach Google Fonts."""
    tmp = tempfile.mkdtemp(prefix='ident-')
    html = os.path.join(tmp, 'ident.html')
    doc = standalone()
    if os.path.exists(FONTS):
        doc = doc.replace('</head>', '<style>' + open(FONTS).read() + '</style></head>')
    open(html, 'w').write(doc)
    js = os.path.join(tmp, 'cap.js')
    open(js, 'w').write(f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch({{ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' }}).catch(async () => chromium.launch());
  const p = await b.newPage({{ viewport: {{ width: {w}, height: {h} }}, deviceScaleFactor: 1 }});
  await p.goto('file://{html}#capture', {{ waitUntil: 'networkidle' }});
  await p.evaluate(() => document.fonts.ready);
  const end = await p.evaluate(v => window.__frame(0, v), '{variant}');
  const n = Math.ceil((end + 0.6) * {fps});
  for (let i = 0; i < n; i++) {{
    await p.evaluate(([t, v]) => window.__frame(t, v), [i / {fps}, '{variant}']);
    await p.screenshot({{ path: '{tmp}/f' + String(i).padStart(4, '0') + '.png' }});
  }}
  await b.close(); console.log(n);
}})();
""")
    r = subprocess.run(['node', js], capture_output=True, text=True, cwd='/tmp/claude-0/-home-user-super-hot/f4a25b5c-7cd5-585d-b4f3-c7ba36b6c676/scratchpad/r8')
    if r.returncode:
        raise SystemExit(r.stderr[-2000:])
    mp4 = os.path.join(out_dir, f'ident-{variant}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(tmp, 'f%04d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', mp4], check=True)
    shutil.rmtree(tmp)
    return mp4


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--fragment'); ap.add_argument('--video', action='store_true')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'ident.html'), 'w').write(standalone())
    if a.fragment:
        open(a.fragment, 'w').write(page())
    print('brand/ident.html' + (f', {a.fragment}' if a.fragment else ''))
    if a.video:
        for v in B.WHEELS:
            print(os.path.relpath(video(OUT, v), HERE))


if __name__ == '__main__':
    main()
