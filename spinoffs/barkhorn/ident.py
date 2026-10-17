"""EARF's ident, the brand played as a film studio's plays before the film (round 20).

The owner: "I also would love the brand to work like a movie studio animation before a movie starts, where the world
and/or earf are animated somehow, like a Spirograph type thing where a black dot rotates around several times to
create a circle of circles, each adopting a color as its mini circle is traced". Of the first version, a ring of
circles round a hub with the rim drawn between them: "It's too much like a film reel and the acceleration changes too
much as it draws. It should be on fluid motion, and it shouldn't have to create a stroke outside of each circle. I'm
open to more ideas here as well."

So the wheel is brand.py's, eight circles through one centre with no rim and no hub, and it comes on one of two ways:

- pen: a dot draws each circle at one steady speed, from its outermost point clockwise, the circle's tint sweeping in
  behind it. At that point the circle runs along the wheel's edge, so between circles the pen swings along the edge to
  the next one, drawing nothing; it never stops or turns a corner. It speeds up once, at the start, and slows once,
  lifting as it comes back to the top.
- bloom: the eight circles start stacked as one, grown from a dot, and part in one turn, spiralling out to their
  places. Stacked, the tints multiply to nearly black, as eight sheets of the acrylic would; as light they add to white.

and on one of two grounds, paper (the tints multiply where circles overlap) or light (the speakers' colours add towards
white, Smoke's black shades). Then the wheel moves aside and EARF is drawn beside it, then its line.

    python3 spinoffs/barkhorn/ident.py                    ->  brand/ident.html (a page that plays it)
    python3 spinoffs/barkhorn/ident.py --fragment PATH    ->  also the page as an Artifact's body (no html/head/body)
    python3 spinoffs/barkhorn/ident.py --video            ->  also brand/ident-<pen|bloom>-<paper|light>.mp4, 1280 x 720,
                                                              30 fps (needs Playwright's Chromium and ffmpeg)
    python3 spinoffs/barkhorn/ident.py --video --fonts CSS    the faces from a local @font-face sheet, where the browser
                                                              cannot reach Google Fonts
"""
import argparse, json, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import brand as B                                        # noqa: E402
import marks as M                                        # noqa: E402

OUT = os.path.join(HERE, 'brand')
MOTIONS, GROUNDS = ('pen', 'bloom'), ('paper', 'light')


def data():
    r5 = lambda x: round(x, 5)
    circles = [dict(name=c['name'], colour=c['colour'], tint=c['tint'], mode=c['mode'], cx=r5(c['cx']), cy=r5(c['cy']),
                    r=r5(c['r']), a0=r5(c['a0'])) for c in B.wheel()]
    word = []
    for p in M.WORDMARK:
        if p[0] == 'rect':
            word.append(dict(pts=[[p[1], p[2]], [p[3], p[2]], [p[3], p[4]], [p[1], p[4]]]))
        elif p[0] == 'circle':
            word.append(dict(c=[p[1], p[2]], r=p[3]))
        elif p[0] == 'ring':                                     # round 29: the R's bowl, its hole outlined too
            word.append(dict(c=[p[1], p[2]], r=p[3], ri=p[4]))
        else:
            word.append(dict(pts=[[round(x, 3), round(y, 3)] for x, y in p[1:]]))
    letters = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3]             # E, A, R, F: which letter each shape belongs to
    assert len(letters) == len(word)
    clouds = [dict(num=num, name=name, colour=col) for key, line, num, name, col in M.SPEAKERS if line == 'Cloud']
    return dict(circles=circles, sw=B.WHEEL_SW, word=word, letters=letters, wordW=M.WORDMARK_W, wordSw=M.U * 0.8,
                clouds=clouds, paper=B.PAPER, ink=B.INK, dark=B.DARK, frost=B.FROST)


PAGE = r"""<title>EARF Ident</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400..700&display=swap">
<style>
/* a screening room: the page dims round the screen where the ident plays; the brand's own paper, ink and faces */
:root {
  --page: #E9E5DE; --fg: #1C1A18; --muted: #5E5A53; --line: #CFC9BF; --screen: #F2EFEA; --screen-edge: #D9D3C9;
  --sans: 'Instrument Sans', Arial, sans-serif; --mono: 'IBM Plex Mono', 'Courier New', monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --page: #141311; --fg: #ECE8E1; --muted: #A39E95; --line: #34312C; --screen-edge: #2A2824; color-scheme: dark } }
:root[data-theme="dark"] { --page: #141311; --fg: #ECE8E1; --muted: #A39E95; --line: #34312C; --screen-edge: #2A2824;
  color-scheme: dark }
body { margin: 0; background: var(--page); color: var(--fg); font-family: var(--sans); font-size: 16px; line-height: 1.5;
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
.sets { display: flex; flex-wrap: wrap; gap: 12px }
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
    <p>The globe drawn as the eight Clouds: eight circles through one centre, each in its speaker's acrylic tint. Then
      the name. Choose how the wheel comes on, and on what ground.</p>
  </header>
  <div class="screen"><canvas id="stage" aria-label="EARF's ident: eight coloured circles through one centre form a wheel, then the word EARF is drawn beside it"></canvas></div>
  <div class="controls">
    <div class="sets">
      <div class="seg" role="group" aria-label="Motion">
        <button type="button" id="m-pen" aria-pressed="true">Pen</button>
        <button type="button" id="m-bloom" aria-pressed="false">Bloom</button>
      </div>
      <div class="seg" role="group" aria-label="Ground">
        <button type="button" id="g-paper" aria-pressed="true">Paper</button>
        <button type="button" id="g-light" aria-pressed="false">Light</button>
      </div>
    </div>
    <button type="button" class="play" id="play"><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2 1l9 5-9 5z"/></svg>Play again</button>
  </div>
  <ul class="legend" id="legend"></ul>
  <section class="notes">
    <div><h2>Pen</h2><p>A dot draws each circle at one steady speed, from where the circle meets the wheel's edge, and the
      circle's tint sweeps in behind it. Between circles it swings along that edge to the next, drawing nothing, so it
      never stops or turns a corner.</p></div>
    <div><h2>Bloom</h2><p>The eight circles start stacked as one, grown from a dot, and part in one turn. Stacked, the
      tints multiply to nearly black, as eight sheets of the acrylic would. As light, they add to white.</p></div>
    <div><h2>Paper and light</h2><p>On paper, the tints multiply where circles overlap, and Fog's white frosts what lies
      under it. As light, the colours add towards white, and Smoke's black shades.</p></div>
  </section>
</main>

<script>
const D = __DATA__;
const cv = document.getElementById('stage'), ctx = cv.getContext('2d');
const VW = 1920, VH = 1080, TAU = 2 * Math.PI, N = D.circles.length, PEN = 0.045, TWIST = Math.PI / 2;
let motion = 'pen', ground = 'paper', TL = null, t0 = performance.now(), shown = 0, raf = 0;
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (location.hash === '#capture') document.documentElement.classList.add('capture');

const clamp01 = x => Math.max(0, Math.min(1, x));
const sine = x => x <= 0 ? 0 : x >= 1 ? 1 : (1 - Math.cos(Math.PI * x)) / 2;      // eases in and out
const out = x => x <= 0 ? 0 : x >= 1 ? 1 : Math.sin(Math.PI * x / 2);             // eases out
const lerp = (a, b, k) => a + (b - a) * k;
const span = (t, w) => clamp01((t - w[0]) / (w[1] - w[0]));

// the share of a path covered at x, the share of its time: one steady speed throughout, reached and left by sine
// ramps of a of the time each, so whatever follows it speeds up once and slows once
function cruise(x, a = 0.05) {
  if (x <= 0) return 0;
  if (x >= 1) return 1;
  const v = 1 / (1 - a), ramp = u => v * (u / 2 - a / (2 * Math.PI) * Math.sin(Math.PI * u / a));
  return x < a ? ramp(x) : x > 1 - a ? 1 - ramp(1 - x) : v * (x - a / 2);
}

// the pen's path: each circle from its outermost point, clockwise, then a glide along the wheel's edge (radius 1) to
// the next circle's. A circle is tangent to the edge where it touches it, so the path never turns a corner. The glides
// draw nothing; the last brings the pen back to the top, where it started
const PATH = [];
D.circles.forEach((c, i) => {
  PATH.push({ kind: 'circle', i, len: TAU * c.r });
  PATH.push({ kind: 'glide', a0: c.a0, len: TAU / N, last: i === N - 1 });
});
const LEN = PATH.reduce((s, p) => s + p.len, 0);

// when each part plays, in seconds
function timeline(m) {
  const T = { appear: [0.15, 0.55] };
  let t;
  if (m === 'pen') { T.draw = [0.3, 6.9]; t = 6.9; }
  else { T.grow = [0.15, 1.35]; T.part = [0.95, 3.75]; t = 3.75; }       // the parting starts before the growing ends
  T.slide = [t - 0.05, t + 0.9];
  T.word = [t + 0.55, t + 2.0];
  T.tag = [t + 1.8, t + 2.5];
  T.end = t + 2.9;
  return T;
}

function state(t) {
  const st = { circles: D.circles.map(c => ({ ...c, e: 0, k: 1 })), pen: null, penR: 0,
               slide: sine(span(t, TL.slide)), word: span(t, TL.word), tag: out(span(t, TL.tag)) };
  if (motion === 'pen') {
    let s = cruise(span(t, TL.draw)) * LEN, lift = 1;
    for (const p of PATH) {
      const q = Math.min(1, s / p.len);
      if (p.kind === 'circle') {
        const c = st.circles[p.i], a = c.a0 + q * TAU;
        c.e = q; st.pen = [c.cx + c.r * Math.cos(a), c.cy + c.r * Math.sin(a)];
      } else {
        const a = p.a0 + q * p.len;                        // on the edge, radius 1, the angle is the length
        st.pen = [Math.cos(a), Math.sin(a)];
        if (p.last) lift = 1 - sine(q);
      }
      if (s <= p.len) break;
      s -= p.len;
    }
    st.penR = PEN * out(span(t, TL.appear)) * lift;
  } else {
    const r = 0.5 * sine(span(t, TL.grow)), p = sine(span(t, TL.part));
    for (const c of st.circles) {
      const d = Math.hypot(c.cx, c.cy) * p, a = c.a0 - (1 - p) * TWIST;  // out from the centre, turning as they go
      c.cx = d * Math.cos(a); c.cy = d * Math.sin(a); c.r = r; c.e = r > 0 ? 1 : 0; c.k = p;
    }
  }
  return st;
}

function layout() {
  const s = 0.78, ww = 450 + 110 + D.wordW, x0 = (VW - ww * s) / 2;
  return { solo: { cx: VW / 2, cy: VH / 2, R: 330 }, lock: { cx: x0 + 225 * s, cy: VH / 2, R: 225 * s },
           word: { x: x0 + (450 + 110) * s, s, capTop: VH / 2 - (300 * s + 30 + 21) / 2 } };
}

// a circle's fill on its ground. On paper each tint multiplies what is under it and Fog's white frosts it; as light
// each colour screens towards white and Smoke's black shades. k brings Fog's frost and Smoke's shade in as the bloom's
// circles part, so stacked they are the tints alone: nearly black on paper, white as light
function paint(c, k) {
  const light = ground === 'light';
  if (light && c.mode === 'shade') { ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 0.55 * k; ctx.fillStyle = '#000'; }
  else if (light) {
    ctx.globalCompositeOperation = 'screen'; ctx.globalAlpha = c.mode === 'frost' ? 0.55 : 0.8;
    ctx.fillStyle = c.mode === 'frost' ? '#FFF' : c.colour;
  }
  else if (c.mode === 'frost') { ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = D.frost * k; ctx.fillStyle = '#FFF'; }
  else { ctx.globalCompositeOperation = 'multiply'; ctx.globalAlpha = 1; ctx.fillStyle = c.tint; }
}

function shape(c) {                 // the circle so far: a sector from its centre, swept from its outermost point
  ctx.beginPath();
  if (c.e >= 1) { ctx.arc(c.cx, c.cy, c.r, 0, TAU); return; }
  ctx.moveTo(c.cx, c.cy); ctx.arc(c.cx, c.cy, c.r, c.a0, c.a0 + c.e * TAU); ctx.closePath();
}

function drawWheel(st) {
  const light = ground === 'light', live = st.circles.filter(c => c.e > 0 && c.r > 0);
  ctx.save();
  for (const c of live) { paint(c, c.k); shape(c); ctx.fill(); }
  ctx.restore();
  ctx.save();
  ctx.strokeStyle = light ? D.paper : D.ink; ctx.globalAlpha = light ? 0.85 : 1; ctx.lineWidth = D.sw; ctx.lineCap = 'round';
  for (const c of live) {
    ctx.beginPath();
    c.e >= 1 ? ctx.arc(c.cx, c.cy, c.r, 0, TAU) : ctx.arc(c.cx, c.cy, c.r, c.a0, c.a0 + c.e * TAU);
    ctx.stroke();
  }
  ctx.restore();
  if (st.pen && st.penR > 0) {
    ctx.fillStyle = light ? D.paper : D.ink; ctx.beginPath(); ctx.arc(st.pen[0], st.pen[1], st.penR, 0, TAU); ctx.fill();
  }
}

function outline(p) {               // a letter's shape as a path; returns its length
  ctx.beginPath();
  if (p.c) {
    ctx.arc(p.c[0], p.c[1], p.r, -Math.PI / 2, 1.5 * Math.PI);
    if (!p.ri) return TAU * p.r;
    ctx.moveTo(p.c[0], p.c[1] - p.ri); ctx.arc(p.c[0], p.c[1], p.ri, -Math.PI / 2, 1.5 * Math.PI);
    return TAU * (p.r + p.ri);
  }
  let L = 0;
  p.pts.forEach((q, i) => { if (i) L += Math.hypot(q[0] - p.pts[i - 1][0], q[1] - p.pts[i - 1][1]); i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); });
  const a = p.pts[p.pts.length - 1], b = p.pts[0]; L += Math.hypot(a[0] - b[0], a[1] - b[1]); ctx.closePath();
  return L;
}

function drawWord(st, Ly) {
  if (st.word <= 0) return;
  ctx.save(); ctx.translate(Ly.word.x, Ly.word.capTop); ctx.scale(Ly.word.s, Ly.word.s);
  ctx.strokeStyle = ground === 'light' ? D.paper : D.ink; ctx.lineWidth = D.wordSw; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  D.word.forEach((p, i) => {
    const q = cruise(clamp01((st.word - D.letters[i] * 0.16) / 0.52), 0.25);   // each letter in turn, at a steady pace
    if (q <= 0) return;
    const L = outline(p);
    ctx.setLineDash(q >= 1 ? [] : [L * q, L + 1]); ctx.stroke();
  });
  ctx.restore();
}

function drawTag(st, Ly) {
  if (st.tag <= 0) return;
  const text = 'NEATURE-INSPIRED LOUDSPEAKERS', size = 30, track = 0.12 * size;
  ctx.save(); ctx.globalAlpha = st.tag; ctx.fillStyle = ground === 'light' ? D.paper : D.ink;
  ctx.font = `500 ${size}px 'IBM Plex Mono', 'Courier New', monospace`; ctx.textBaseline = 'alphabetic';
  let x = Ly.word.x - 2, y = Ly.word.capTop + 300 * Ly.word.s + 30 + 21 + (1 - st.tag) * 10;
  for (const ch of text) { ctx.fillText(ch, x, y); x += ctx.measureText(ch).width + track; }
  ctx.restore();
}

function render(t) {
  shown = t;
  const Ly = layout(), st = state(t);
  ctx.save(); ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.globalCompositeOperation = 'source-over'; ctx.globalAlpha = 1;
  ctx.fillStyle = ground === 'light' ? D.dark : D.paper; ctx.fillRect(0, 0, cv.width, cv.height);
  const k = cv.width / VW; ctx.scale(k, k);
  const cx = lerp(Ly.solo.cx, Ly.lock.cx, st.slide), cy = lerp(Ly.solo.cy, Ly.lock.cy, st.slide), R = lerp(Ly.solo.R, Ly.lock.R, st.slide);
  ctx.save(); ctx.translate(cx, cy); ctx.scale(R, R); drawWheel(st); ctx.restore();
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

function set(m, g) {
  motion = m; ground = g; TL = timeline(m);
  for (const id of ['pen', 'bloom']) document.getElementById('m-' + id).setAttribute('aria-pressed', String(id === m));
  for (const id of ['paper', 'light']) document.getElementById('g-' + id).setAttribute('aria-pressed', String(id === g));
}

function choose(m, g) { set(m, g); reduce ? render(TL.end) : play(); }

document.getElementById('legend').innerHTML = D.clouds.map(c =>
  `<li><span class="sw" style="background:${c.colour}"></span><span class="num">${c.num}</span>${c.name}</li>`).join('');
for (const m of ['pen', 'bloom']) document.getElementById('m-' + m).addEventListener('click', () => choose(m, ground));
for (const g of ['paper', 'light']) document.getElementById('g-' + g).addEventListener('click', () => choose(motion, g));
document.getElementById('play').addEventListener('click', play);
window.addEventListener('resize', () => { size(); render(shown); });   // the frame last drawn, at the new size
window.__frame = (t, m, g) => { set(m || motion, g || ground); render(t); return TL.end; };

set(motion, ground); size();
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


def video(out_dir, motion, ground, fonts=None, fps=30, w=1280, h=720):
    """The ident to an MP4: each frame drawn at its own time by the page's __frame, screenshot, then ffmpeg. `fonts`, a
    local @font-face sheet, stands in for Google Fonts where the browser cannot reach them."""
    tmp = tempfile.mkdtemp(prefix='ident-')
    html = os.path.join(tmp, 'ident.html')
    doc = standalone()
    if fonts:
        doc = doc.replace('</head>', '<style>' + open(fonts).read() + '</style></head>')
    open(html, 'w').write(doc)
    js = os.path.join(tmp, 'cap.js')
    open(js, 'w').write(f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch();
  const p = await b.newPage({{ viewport: {{ width: {w}, height: {h} }}, deviceScaleFactor: 1 }});
  await p.goto('file://{html}#capture', {{ waitUntil: 'networkidle' }});
  await p.evaluate(() => document.fonts.ready);
  const end = await p.evaluate(([m, g]) => window.__frame(0, m, g), ['{motion}', '{ground}']);
  const n = Math.ceil((end + 0.6) * {fps});
  for (let i = 0; i < n; i++) {{
    await p.evaluate(([t, m, g]) => window.__frame(t, m, g), [i / {fps}, '{motion}', '{ground}']);
    await p.screenshot({{ path: '{tmp}/f' + String(i).padStart(4, '0') + '.png' }});
  }}
  await b.close(); console.log(n);
}})();
""")
    r = subprocess.run(['node', js], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-2000:])
    mp4 = os.path.join(out_dir, f'ident-{motion}-{ground}.mp4')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(fps), '-i', os.path.join(tmp, 'f%04d.png'),
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', mp4], check=True)
    shutil.rmtree(tmp)
    return mp4


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--fragment', help='also write the page as an Artifact body to this path')
    ap.add_argument('--video', action='store_true', help='also write an MP4 of each motion on each ground')
    ap.add_argument('--fonts', help='a local @font-face sheet for the videos, where Google Fonts cannot be reached')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, 'ident.html'), 'w').write(standalone())
    if a.fragment:
        open(a.fragment, 'w').write(page())
    print('brand/ident.html' + (f', {a.fragment}' if a.fragment else ''))
    if a.video:
        for m in MOTIONS:
            for g in GROUNDS:
                print(os.path.relpath(video(OUT, m, g, a.fonts), HERE))


if __name__ == '__main__':
    main()
