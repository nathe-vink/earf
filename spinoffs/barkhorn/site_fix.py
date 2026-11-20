"""The fix list of 2026-11-20 (the research and critic pass), applied after site_v2's release-candidate steps.

Build 1A: the home, the names, the lines (items 1 to 10). fix_1a(p, web) runs on the page as the last step of
site_v2.apply(); finish_1a(web) runs over the built files after site_v2.rc_finish().
The owner's copy rule stands throughout: remove, do not rewrite; no line beside a picture says what it shows.
"""
import json
import os
import re

KEYS = ['red', 'orange', 'amber', 'green', 'blue', 'violet', 'ice', 'black']
NAMES = dict(zip(KEYS, ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke']))
# the products in the order of the header's kinds: speakers, lighting, turntable
TILES = [('tropos', 'Tropos', 'speaker', 'Horn speaker'), ('hemisphere', 'Hemisphere', 'hemisphere', 'Pendant'),
         ('core', 'Core', 'core', 'Table lamp'), ('mantle', 'Mantle', 'mantle', 'Turntable')]
ARROW = ('<svg class="arr" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10h11M11 5l5 5-5 5" fill="none" stroke="currentColor" '
         'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def tint_word(c):
    """The color's material in a sentence: "translucent red"; Fog is "clear" (the coordinator 2026-11-20)."""
    return 'clear' if c['k'] == 'ice' else c['tint'].lower()


def _data(p):
    i = p.rest.index('const D = ') + len('const D = ')
    j = p.rest.index(', BY = Object', i)
    return i, j, json.loads(p.rest[i:j])


def _sub_any(p, old, new):
    """p.sub in whichever half of the page holds the text (once)."""
    for where in ('head', 'rest'):
        if getattr(p, where).count(old) == 1:
            p.sub(old, new, where=where)
            return
    raise AssertionError(('site_fix: not found once', old[:90]))


def _ground(path):
    """The median color of a picture's top and bottom edges (their middle half: the corners can be vignetted), as
    #RRGGBB: the tile's ground above and below a picture wider than 4:5."""
    from PIL import Image
    import numpy as np
    a = np.asarray(Image.open(path).convert('RGB')).astype(int)
    h, w = a.shape[:2]; s = 6; x0, x1 = w // 4, 3 * w // 4
    g = np.median(np.concatenate([a[:s, x0:x1].reshape(-1, 3), a[-s:, x0:x1].reshape(-1, 3)]), 0)
    return '#%02X%02X%02X' % tuple(int(v) for v in g)


def _tile_4x5(src_path, out_path, width=800):
    """A picture wider than 4:5 set into a 4:5 tile: its own top and bottom rows stretched into the bands above and below
    and softened, so the ground runs on without a seam."""
    from PIL import Image, ImageFilter
    im = Image.open(src_path).convert('RGB')
    h = round(im.height * width / im.width); im = im.resize((width, h), Image.LANCZOS)
    H = round(width * 5 / 4); top = (H - h) // 2; bot = H - h - top
    can = Image.new('RGB', (width, H))
    can.paste(im, (0, top))
    if top > 0:
        band = im.crop((0, 0, width, 3)).resize((width, top), Image.BILINEAR).filter(ImageFilter.GaussianBlur(6))
        can.paste(band, (0, 0))
    if bot > 0:
        band = im.crop((0, h - 3, width, h)).resize((width, bot), Image.BILINEAR).filter(ImageFilter.GaussianBlur(6))
        can.paste(band, (0, top + h))
    can.save(out_path, 'WEBP', quality=82, method=6)


def fix_1a(p, web):
    i, j, D = _data(p)
    C = {c['k']: c for c in D['clouds']}
    src = lambda f, k: {'tropos': f'img/rc/{k}-tall.webp', 'mantle': f'img/rc/mantle-{NAMES[k]}.webp',
                        'hemisphere': f'img/rc/home-hemisphere-{NAMES[k]}.webp', 'core': f'img/rc/home-core-{NAMES[k]}.webp'}[f]
    img = lambda f, k: src(f, k) if f == 'tropos' else f'img/rc/tile-{f}-{NAMES[k]}.webp'
    for k in KEYS:                                 # every tile 4:5: Tropos's tall front as it is, the others set in
        for f, *_ in TILES:
            assert os.path.exists(os.path.join(web.SITE, src(f, k))), ('fix_1a: no picture', src(f, k))
            if f != 'tropos':
                _tile_4x5(os.path.join(web.SITE, src(f, k)), os.path.join(web.SITE, img(f, k)))

    # --- 1. the home: "The family." with the eight chips, then the four products as four equal tiles; starts in Ember
    from PIL import Image
    grounds = {f: _ground(os.path.join(web.SITE, src(f, 'red'))) for f, *_ in TILES}
    def tile(f, name, route, kind):
        src = img(f, 'red'); w, h = Image.open(os.path.join(web.SITE, src)).size
        return (f'<a class="ftile ft-{f}" href="#{route}-ember" data-p="{f}"><span class="ft-pic" style="background:{grounds[f]}">'
                f'<img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{name} in Ember"></span>'
                f'<span class="ft-body"><span class="ft-kind">{kind}</span><h3 class="ft-name">{name}</h3>'
                f'<span class="ft-btn">See {name} {ARROW}</span></span></a>')
    chips = ''.join(f'<label class="tint"><input type="radio" name="tint" value="{k}"{" checked" if k == "red" else ""}>'
                    f'<span class="coin-dot" style="--i:{C[k]["coin"]}"></span><span class="tn">{C[k]["name"]}</span></label>' for k in KEYS)
    family = ('<section class="band mk" id="family"><i class="anchor" id="colors"></i><div class="wrap mk-head"><h2>The family.</h2></div>'
              '<div class="wrap"><fieldset class="tint-pick"><legend class="sr">Choose a color</legend>' + chips + '</fieldset>'
              f'<p class="tint-line" aria-live="polite"><b>{C["red"]["name"]}.</b> <span>{C["red"]["line"]}</span></p></div>'
              '<div class="mk-wide ftiles">' + ''.join(tile(*t) for t in TILES) + '</div></section>')
    p.section('colors-band')                       # the second, unnamed set of four goes with it
    m = re.search(r'<section class="band mk" id="family">.*?</section>', p.rest, re.S)
    assert m, 'fix_1a: the family'
    p.rest = p.rest[:m.start()] + family + p.rest[m.end():]
    data = {k: {'name': C[k]['name'], 'line': C[k]['line'], 'slug': NAMES[k], 'pics': {f: img(f, k) for f, *_ in TILES}} for k in KEYS}
    routes = {f: r for f, n, r, _ in TILES}
    names = {f: n for f, n, *_ in TILES}
    js = """<script>(function () {      // the family's chips: every link and alt at once, each picture as soon as it has loaded
  const T = %s, R = %s, N = %s, box = document.getElementById('family'); if (!box) return;
  const line = box.querySelector('.tint-line'), tiles = box.querySelectorAll('.ftile'), warm = {};
  let want = 'red';
  const show = k => { want = k; const t = T[k];
    line.innerHTML = `<b>${t.name}.</b> <span>${t.line}</span>`;
    tiles.forEach(a => { const f = a.dataset.p, im = a.querySelector('img'), s = t.pics[f];
      a.href = `#${R[f]}-${t.slug}`; im.alt = `${N[f]} in ${t.name}`;
      const n = warm[s] || (warm[s] = new Image()); if (!n.src) n.src = s;
      const swap = () => { if (want === k) im.src = s; };
      if (n.complete && n.naturalWidth) swap(); else if (n.decode) n.decode().then(swap, swap); else n.addEventListener('load', swap, { once: true }); });
    if (typeof setTint === 'function') setTint(k); };
  box.querySelectorAll('.tint input').forEach(r => {
    r.addEventListener('change', () => r.checked && show(r.value));
    r.closest('label').addEventListener('pointerenter', () => Object.values(T[r.value].pics).forEach(s => { if (!warm[s]) { warm[s] = new Image(); warm[s].src = s; } }), { passive: true });
  });
})()</script>""" % (json.dumps(data, separators=(',', ':')), json.dumps(routes), json.dumps(names))
    at = p.rest.index('</body>') if '</body>' in p.rest else len(p.rest)
    p.rest = p.rest[:at] + js + '\n' + p.rest[at:]
    p.css("""
/* the family: four equal tiles for 4:5 pictures, two by two on a phone (fix list 2026-11-20, 1) */
.ftiles { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 16px }
.ftile { display: flex; flex-direction: column; color: var(--ink); text-decoration: none; min-width: 0 }
.ftile:focus-visible { outline: 3px solid var(--ink); outline-offset: 3px }
.ft-pic { display: block; aspect-ratio: 4 / 5; border-radius: 4px; overflow: hidden }
.ft-pic img { display: block; width: 100%; height: 100%; object-fit: cover }
.ft-body { display: grid; gap: 4px; padding: 14px 2px 0; justify-items: start }
.ft-kind { font-size: 12px; letter-spacing: .14em; text-transform: uppercase; color: var(--muted) }
.ft-name { margin: 0; font-size: clamp(22px, 2vw, 30px); line-height: 1.05; letter-spacing: -0.03em }
.ft-btn { display: inline-flex; align-items: center; gap: 8px; margin-top: 8px; min-height: 44px; padding: 0 16px; border-radius: 999px;
  border: 2px solid currentColor; font-weight: 600; font-size: 15px; transition: background-color .2s ease, color .2s ease }
.ft-btn .arr { width: 18px; height: 18px }
.ftile:hover .ft-btn, .ftile:focus-visible .ft-btn { background: var(--ink); color: #F4F1EC; border-color: var(--ink) }
@media (max-width: 760px) { .ftiles { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px 10px } .ft-btn { padding: 0 12px; font-size: 14px } }
""")

    # --- 2. the hero: Meet Tropos opens Tropos in Acid; the line; the dots after the buttons in tab order; a shown name is a link
    p.sub('<p class="hero-sub">Horn speakers, lamps and a turntable, cast in tinted acrylic.</p>',
          '<p class="hero-sub">Horn speakers, lamps and a turntable in tinted cast acrylic.</p>')
    p.sub('<a class="cta-btn cta-solid" href="#speakers">Meet Tropos</a>', '<a class="cta-btn cta-solid" href="#speaker-acid">Meet Tropos</a>')
    m = re.search(r'<div class="hero-more">.*?</p></div></div>', p.rest, re.S)
    assert m, 'fix_1a: the hero buttons'
    more = m.group(0); p.rest = p.rest[:m.start()] + p.rest[m.end():]
    p.sub('<div class="hero-photo hs">', more + '<div class="hero-photo hs">')
    p.css("""
/* the hero: the buttons ahead of the dots in the page's order; on a tall screen they still sit under the picture */
@media (max-aspect-ratio: 1/1) { .hs-hero .hero-pic { display: flex !important; flex-direction: column }
  .hs-hero .hero-title { order: 1 } .hs-hero .hero-photo { order: 2 } .hs-hero .hero-more { order: 3 } }
/* between a phone and a wide screen (up to 960 px) the line and the buttons stand under the picture, clear of its dots */
@media (min-aspect-ratio: 1/1) and (max-width: 960px) {
  .hs-hero .hero-pic { display: flex !important; flex-direction: column } .hs-hero .hero-photo { order: 1 } .hs-hero .hero-more { order: 2 }
  .hs-hero .hero-more { position: static !important; left: auto !important; right: auto !important; top: auto !important; text-align: left; padding-top: 20px }
  .hs-hero .hero-more .wrap { margin-inline: auto !important; padding-inline: 16px !important; max-width: 1240px !important }
  .hs-hero .hero-sub { color: #1C1A18; margin: 0 0 16px; max-width: none; font-size: 17px }
  .hs-hero .hero-cta { justify-content: flex-start }
  .hs-hero .cta-solid { background: #1C1A18; color: #F4F1EC; border-color: #1C1A18 } .hs-hero .cta-solid:hover { background: #000 }
  .hs-hero .cta-line { background: transparent; color: #1C1A18; border-color: #1C1A18 } .hs-hero .cta-line:hover { background: rgb(28 26 24 / .06) }
  .hs-hero .cta-btn:focus-visible { outline-color: #1C1A18 } }
/* a name shown by a first tap is itself the link */
.hs-pt.open .hs-label { pointer-events: auto }
""")

    # --- 3. the header by kind; Speakers and Turntable open their product in the tint chosen in this visit, else Ember
    p.sub('<li><a href="#speakers" data-nav="speakers">Tropos</a></li><li><a href="#lighting" data-nav="lighting">Lighting</a></li>\n'
          '    <li><a href="#turntable" data-nav="turntable">Mantle</a></li>',
          '<li><a href="#speaker-ember" data-nav="speakers" data-carry="speaker">Speakers</a></li><li><a href="#lighting" data-nav="lighting">Lighting</a></li>\n'
          '    <li><a href="#mantle-ember" data-nav="turntable" data-carry="mantle">Turntable</a></li>')

    # --- 4. the tint carried: every link from one product to another keeps the tint now chosen
    for a, b in (('<a class="more" href="#hemisphere-ember">See Hemisphere</a>', '<a class="more" href="#hemisphere-ember" data-carry="hemisphere">See Hemisphere</a>'),
                 ('<a class="more" href="#core-ember">See Core</a>', '<a class="more" href="#core-ember" data-carry="core">See Core</a>'),
                 ('<a class="more" href="#mantle-ember">See Mantle</a>', '<a class="more" href="#mantle-ember" data-carry="mantle">See Mantle</a>'),
                 ('<figure class="mantle-pic page"><a href="#mantle-ember">', '<figure class="mantle-pic page"><a href="#mantle-ember" data-carry="mantle">')):
        p.sub(a, b)
    p.sub('function route() {',
          "// the tint chosen in this visit (a product's page or the family's chips): carried by every link marked data-carry\n"
          "let TINT = (() => { try { return sessionStorage.getItem('earf-tint'); } catch (e) { return null; } })(), WANT = null;\n"
          "if (!BY[TINT]) TINT = 'red';\n"
          "const carry = () => document.querySelectorAll('a[data-carry]').forEach(a => { a.href = `#${a.dataset.carry}-${BY[TINT].name.toLowerCase()}`; });\n"
          "const setTint = k => { if (!BY[k]) return; TINT = k; try { sessionStorage.setItem('earf-tint', k); } catch (e) {} carry(); };\n"
          "carry();\n"
          "const VIEWKEY = { out: 'habitat' };      // #speaker-ember/out: the product, opened on that view\n"
          "function route() {")
    p.sub("function route() {\n  let h = location.hash.slice(1);",
          "function route() {\n  let h = location.hash.slice(1);\n"
          "  { const v = /^([a-z]+-[a-z]+)\\/([a-z-]+)$/.exec(h); if (v) { h = v[1]; WANT = VIEWKEY[v[2]] || v[2]; } }\n"
          "  { const c = /^colou?r-([a-z]+)$/.exec(h); if (c && keyOf(c[1])) { h = `speaker-${c[1]}`; history.replaceState(null, '', '#' + h); } }   // the color pages are retired: their Tropos")
    p.sub("document.getElementById('p-more').innerHTML = MORE[P.id] || '';",
          "document.getElementById('p-more').innerHTML = (MORE[P.id] || '').replace(/#(speaker|hemisphere|core|mantle)-[a-z]+/g, (x, r) => `#${r}-${c.name.toLowerCase()}`);\n  setTint(k);")

    # --- 5. the places: each opens its Tropos on the place picture clicked
    n = len(re.findall(r'<a class="place" href="#speaker-([a-z]+)">', p.rest))
    assert n >= 7, ('fix_1a: the places', n)
    p.rest = re.sub(r'<a class="place" href="#speaker-([a-z]+)">', r'<a class="place" href="#speaker-\1/out">', p.rest)
    p.sub("if (n) showView(shown(c)[0]);", "if (n) showView(WANT && shown(c).includes(WANT) ? WANT : shown(c)[0]); WANT = null;")

    # --- 7. every product page in one pattern: kind and status, the name, "Color: Ember", one sentence and one fact
    p.sub("const PRODUCTS = [", "const tintWord = c => c.k === 'ice' ? 'clear' : c.tint.toLowerCase();\nconst PRODUCTS = [")
    p.sub("kind: 'Horn loudspeaker', name: c => c.name,\n    num: c => `Tropos ${c.num}`, copy: c => c.line,",
          "kind: 'Horn loudspeaker', name: () => 'Tropos',\n    num: () => 'Horn speaker', copy: c => `A powered horn loudspeaker in ${tintWord(c)} cast acrylic. Sold in pairs.`,")
    p.sub("num: () => `Lighting &middot; ${L.kind}`, copy: () => L.line,",
          "num: () => L.kind, copy: c => (id === 'dome' ? `A pendant in ${tintWord(c)} cast acrylic. The shade comes off with a quarter turn.`\n"
          "      : `A table lamp in ${tintWord(c)} cast acrylic. Cordless. About five hours a charge.`),")
    p.sub("num: () => 'Mantle', copy: () => D.tt.line,", "num: () => 'Turntable', copy: c => `A turntable in ${tintWord(c)} cast acrylic.`,")
    p.sub("document.getElementById('p-crumb').textContent = P.id === 'speaker' || P.id === 'turntable' ? c.name : P.title(c);",
          "document.getElementById('p-crumb').textContent = P.title(c);")
    p.sub("document.getElementById('p-icon').innerHTML = P.id === 'speaker' ? icons(c) : '';",
          "document.getElementById('p-icon').innerHTML = '';")
    p.sub("document.getElementById('p-pick-ic').innerHTML = P.id === 'speaker' ? '' : icons(c);",
          "document.getElementById('p-pick-ic').innerHTML = icons(c);")

    # --- 8. the lines that restate a picture, or say more than its facts: removed
    caps = re.search(r'const CAPS = (\{.*?\});   // the captions the owner kept', p.rest)
    assert caps, 'fix_1a: CAPS'
    t = caps.group(1)
    for a, b in (('"horn-back": "Its compression driver, on four black posts."', '"horn-back": ""'),
                 ('"below": "The opal diffuser inside the shade."', '"below": ""'),
                 ('"table": "Half a meter over an oak table."', '"table": ""'),
                 ('"cap": "Satin black anodized aluminum."', '"cap": ""'),
                 ('"rim": "The opal diffuser within the rim."', '"rim": ""'),
                 ('speaker: {', 'speaker: {"off": "", ')):          # the front kept its alt as its caption: now none
        assert t.count(a) == 1, ('fix_1a: CAPS', a)
        t = t.replace(a, b)
    p.rest = p.rest[:caps.start(1)] + t + p.rest[caps.end(1):]
    for gone in ('The 15-inch woofer, the two ports', 'Its compression driver, on four black posts', 'The opal diffuser inside the shade',
                 'Half a meter over an oak table', 'Satin black anodized aluminum."', 'The opal diffuser within the rim'):
        assert gone not in re.search(r'const CAPS = \{.*?\};', p.rest).group(0), ('fix_1a: a caption stayed', gone)
    # "How it lights": only what its labeled picture does not show
    p.rest, nw = re.subn(r'(<section class="lights" id="p-lights".*?<p>)(.*?)(</p>)',
                         lambda m: m.group(1) + 'Twenty-four LEDs, all facing away from you, so there&rsquo;s no bright point to look into.' + m.group(3),
                         p.rest, count=1, flags=re.S)
    assert nw == 1, 'fix_1a: How it lights'
    p.sub(' each with a white opal diffuser inside its color, so the color glows and the source never shows.',
          ' each with a white opal diffuser inside its color.')
    p.sub(' The lining shows through the walls, so we dressed it in white voile.', ' The lining shows through the walls.')
    # the lines under the lamps' names on /lighting, as on their pages
    p.sub('<p class="line">A ball of tinted acrylic sitting low in a satin base of its own color. No cord: it goes where the conversation is.</p>', '')
    p.sub('<p class="line">Hung low over a table. A quarter turn takes its shade off, and another puts a new color on.</p>',
          '<p class="line">Hung low over a table. A quarter turn takes its shade off.</p>')
    # one line's height stays under the stage when there is no caption, so nothing below moves
    p.css("#cap { min-height: 1.45em } #cap[hidden] { display: block !important; visibility: hidden }\n")

    # --- 9. one voice on status: Made to order; renders said once under the pictures; one caveat on the figures
    p.rest = p.rest.replace("unit: 'Each is made to order.'", "unit: 'Made to order.'")
    p.sub('<p class="cap" id="cap" aria-live="polite"></p>',
          '<p class="cap" id="cap" aria-live="polite"></p>\n        <p class="render-note">Pictures are renders. Nothing is built yet.</p>')
    p.sub('<dl class="facts" id="facts"></dl>', '<dl class="facts" id="facts"></dl>\n        <p class="figs">All figures come from the design; none is measured yet.</p>')
    p.sub('Pictures are renders until the first pair is built.', 'Pictures are renders; nothing is built yet.')
    i, j, D = _data(p)
    for L in list(D['lamps'].values()) + [D['tt']]:
        L['facts'] = [f for f in L['facts'] if f[0] != 'Figures']
    p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
    p.css(".render-note, .figs { margin: 8px 0 0; color: var(--muted); font-size: 13px; line-height: 1.4 }\n")

    # --- 10. the opening plays only on / with no fragment, once a visit
    m = re.search(r"  if \(/\^#\(speaker\|dome\|orb\|turntable\|colou\?r\)-.*?\.test\(location\.hash\)\n"
                  r"      \|\| matchMedia\('\(prefers-reduced-motion: reduce\)'\)\.matches\) return;\n  d\.classList\.add\('intro'\);", p.head + p.rest, re.S)
    assert m, 'fix_1a: the opening'
    _sub_any(p, m.group(0),
             "  let seen = false; try { seen = !!sessionStorage.getItem('earf-opened'); } catch (e) {}\n"
             "  if (location.pathname.replace(/index\\.html$/, '') !== '/' || location.hash || seen\n"
             "      || matchMedia('(prefers-reduced-motion: reduce)').matches) return;\n"
             "  try { sessionStorage.setItem('earf-opened', '1'); } catch (e) {}\n  d.classList.add('intro');")


def finish_1a(web):
    """Over the built files: the link previews in one voice (the product's sentence; "In development. Made to order."),
    and the retired color pages forwarded to their Tropos."""
    import glob
    clouds = {'Ember': 'translucent red', 'Dust': 'translucent orange', 'Acid': 'translucent golden yellow', 'Poison': 'translucent bottle green',
              'Ice': 'translucent ice blue', 'Haze': 'translucent violet', 'Fog': 'clear', 'Smoke': 'smoked gray'}
    for f in glob.glob(os.path.join(web.SITE, '**', '*.html'), recursive=True):
        t = open(f).read()
        u = re.sub(r'content="[^"]*? Tropos 0\d, a powered horn loudspeaker in ([^"]+?) cast acrylic\. In development, not yet for sale\."',
                   lambda m: 'content="A powered horn loudspeaker in %s cast acrylic. In development. Made to order."' % ('clear' if m.group(1) == 'water-clear' else m.group(1)), t)
        u = re.sub(r'content="Hung low over a table\. A quarter turn takes its shade off, and another puts a new color on\. Pendant in (\w+)\. In development, not yet for sale\."',
                   lambda m: 'content="A pendant in %s cast acrylic. In development. Made to order."' % clouds[m.group(1)], u)
        u = re.sub(r'content="A ball of tinted acrylic sitting low in a satin base of its own color\. No cord: it goes where the conversation is\. Table lamp in (\w+)\. In development, not yet for sale\."',
                   lambda m: 'content="A table lamp in %s cast acrylic. In development. Made to order."' % clouds[m.group(1)], u)
        u = re.sub(r'content="Mantle in (\w+), a turntable in cast acrylic\. In development, not yet for sale\."',
                   lambda m: 'content="A turntable in %s cast acrylic. In development. Made to order."' % clouds[m.group(1)], u)
        u = (u.replace('In development at EARF, not yet for sale.', 'In development at EARF. Made to order.')
              .replace('In development, not yet for sale.', 'In development. Made to order.')
              .replace('In development, not yet for sale', 'In development. Made to order'))
        if u != t:
            open(f, 'w').write(u)
    vj = os.path.join(web.SITE, 'vercel.json')
    v = json.load(open(vj))
    if not any(r['source'] == '/colors/:name' for r in v.get('redirects', [])):
        v.setdefault('redirects', []).append({'source': '/colors/:name', 'destination': '/tropos/:name', 'permanent': True})
    json.dump(v, open(vj, 'w'), indent=2)
