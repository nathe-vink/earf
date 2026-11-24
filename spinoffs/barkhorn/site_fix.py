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
  const show = (k, quiet) => { want = k; const t = T[k];
    line.innerHTML = `<b>${t.name}.</b> <span>${t.line}</span>`;
    tiles.forEach(a => { const f = a.dataset.p, im = a.querySelector('img'), s = t.pics[f];
      a.href = `#${R[f]}-${t.slug}`; im.alt = `${N[f]} in ${t.name}`;
      const n = warm[s] || (warm[s] = new Image()); if (!n.src) n.src = s;
      const swap = () => { if (want === k) im.src = s; };
      if (n.complete && n.naturalWidth) swap(); else if (n.decode) n.decode().then(swap, swap); else n.addEventListener('load', swap, { once: true }); });
    if (!quiet && typeof setTint === 'function') setTint(k); };
  box.querySelectorAll('.tint input').forEach(r => {
    r.addEventListener('change', () => r.checked && show(r.value));
    r.closest('label').addEventListener('pointerenter', () => Object.values(T[r.value].pics).forEach(s => { if (!warm[s]) { warm[s] = new Image(); warm[s].src = s; } }), { passive: true });
  });
  // one tint for the visit: the row starts in it (else Ember), and after Back it follows that tint, not a chip the browser restored
  const sync = () => { let k = null; try { k = sessionStorage.getItem('earf-tint'); } catch (e) {} const has = !!T[k]; if (!has) k = 'red';
    box.querySelectorAll('.tint input').forEach(r => { r.checked = r.value === k; }); show(k, !has); };
  sync(); addEventListener('pageshow', sync); addEventListener('hashchange', () => { if (location.hash === '' || location.hash === '#top' || location.hash === '#family' || location.hash === '#colors') sync(); });
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
@media (min-aspect-ratio: 1/1) and (max-width: 960px) and (min-height: 641px) {
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


# ------------------------------------------------------------------------------------------------------------------
# Build 1B: the sets (items 11 to 15)

# the products in each bar picture, with the tint shown (planet-bar/<frame>.centres.json, r33-speaker-horn): the names
# row under it, its only caption
BAR_NAMES = {
    'tropos-bar.webp': [('speaker', 'amber'), ('hemisphere', 'red'), ('hemisphere', 'amber'), ('hemisphere', 'orange'),
                        ('core', 'red'), ('core', 'amber'), ('core', 'orange'), ('mantle', 'red')],      # every product and tint in the frame (bar-backbar.centres.json; hues measured 15:10)          # bar-backbar
    'bar-pendants.webp': [('hemisphere', 'red'), ('hemisphere', 'amber'), ('hemisphere', 'orange'), ('core', 'red'), ('core', 'orange')],     # every product and tint in the frame (bar-pendants.centres.json; the coordinator 15:06)
    'core-bar-table.webp': [('core', 'red')],
    'mantle-bar.webp': [('speaker', 'amber'), ('core', 'red'), ('mantle', 'red')],
}
PNAME = {'speaker': 'Tropos', 'hemisphere': 'Hemisphere', 'core': 'Core', 'mantle': 'Mantle'}
CNAME = dict(zip(KEYS, ['Ember', 'Dust', 'Acid', 'Poison', 'Ice', 'Haze', 'Fog', 'Smoke']))
# one list of views per product, the same order in every tint, the product alone first
VORDER = {'speaker': ['off', 'horn-back', 'amp', 'turn', 'bar', 'habitat'],
          'dome': ['hero', 'below', 'off', 'cap', 'rim', 'table', 'bar', 'cluster'],     # its own two first (the coordinator 13:56)
          'orb': ['hero', 'bar'], 'turntable': ['studio', 'cover', 'bar']}
# Tropos's particulars and its page's facts as one list, one wording (the fuller where they differed)
TROPOS_SPEC = [
    ("Acrylic", "${c.tint}"),
    ("Cabinet", "Cast acrylic, 20 mm, tinted through; lined in white"),
    ("Lining", "Polyester batts in white voile, 100 mm at the top and the bottom"),
    ("Horn", "Thermoformed cast acrylic, 10 mm, in the cabinet&rsquo;s color; polished inside and out, on four black posts"),
    ("Woofer", "FaitalPRO 15PR400, 15-inch, with two ports in the front&rsquo;s lower corners"),
    ("Horn driver", "B&amp;C DE1085TN, 2-inch compression driver"),
    ("Amplifier", "Hypex FusionAmp FA123 built in: the woofer on two bridged channels, up to 125 W into its 8 &Omega;; the horn on its own; crossed at 1 kHz in its DSP"),
    ("Bass", "To about 51 Hz at &minus;3 dB, before the room adds its own; the ports tuned to 38 Hz"),
    ("Loudness", "Up to about 115 dB at 1 m, each"),
    ("Inputs", "XLR (and a link out), RCA, AES, S/PDIF coaxial and optical; USB to set it up"),
    ("Size", "1295 high, 560 wide (the horn flush with the cabinet), 442 deep overall, 420 at the cabinet (mm)"),
    ("Weight", "About 75 kg (165 lb) each"),
    ("Care", "${D.care}"),
]


def _row_cuts(path):
    """The eight lamps' bounds across a row picture, as the edges between neighbors in percent: [0, ..., 100]."""
    from PIL import Image
    import numpy as np
    a = np.asarray(Image.open(path).convert('RGB')).astype(int); h, w = a.shape[:2]
    bg = np.median(np.concatenate([a[:10, :10].reshape(-1, 3), a[:10, -10:].reshape(-1, 3)]), 0)
    col = (np.abs(a - bg).max(2) > 40)[int(h * 0.2):int(h * 0.95)].sum(0) > 6
    runs, x = [], 0
    while x < w:
        if col[x]:
            s = x
            while x < w and col[x]:
                x += 1
            if x - s > 15:
                runs.append((s + x) / 2)
        x += 1
    assert len(runs) == 8, ('_row_cuts: not eight', path, len(runs))
    mids = [(runs[i] + runs[i + 1]) / 2 / w * 100 for i in range(7)]
    return [0] + [round(m, 2) for m in mids] + [100]


def names_row(pic):
    """"Tropos in Acid · Hemisphere in Ember · ...": each name a link to that product in that tint."""
    return ' &middot; '.join(f'<a href="#{r}-{NAMES[k]}">{PNAME[r]} in {CNAME[k]}</a>' for r, k in BAR_NAMES[pic])


def finish_1b(web):
    """/tropos forwards to Tropos in Ember (its eight cards are the product page's row of eight now)."""
    vj = os.path.join(web.SITE, 'vercel.json')
    v = json.load(open(vj))
    if not any(r['source'] == '/tropos' for r in v.get('redirects', [])):
        v.setdefault('redirects', []).append({'source': '/tropos', 'destination': '/tropos/ember', 'permanent': True})
    json.dump(v, open(vj, 'w'), indent=2)


def fix_1b(p, web):
    i, j, D = _data(p)
    C = {c['k']: c for c in D['clouds']}
    # --- 11. one set of views per product: a picture that exists in one tint is shown in all eight, marked
    def share(views_of, key, frm):
        src = views_of(frm).get(key)
        assert src, ('fix_1b: no view to share', key, frm)
        for k in KEYS:
            v = views_of(k)
            if key not in v:
                v[key] = dict(src, shown=frm)
    speaker = lambda k: C[k]['views']
    dome = lambda k: D['lamps']['dome']['colours'][k]['views']
    orb = lambda k: D['lamps']['orb']['colours'][k]['views']
    tt = lambda k: D['tt']['colours'][k]['views']
    share(speaker, 'bar', 'amber')
    for key in ('off', 'cap', 'rim', 'table', 'bar'):
        share(dome, key, 'red')
    bar_table = dict(orb('red')['bar'])
    assert 'core-bar-table' in bar_table['src'], ('fix_1b: Core in Ember at the bar', bar_table['src'])
    for k in KEYS:                                   # Core at the bar is the close view, in Ember, on every tint
        orb(k)['bar'] = dict(bar_table, **({} if k == 'red' else {'shown': 'red'}))
    share(tt, 'bar', 'red')
    for views_of, drop in ((dome, ('row', 'unlit')), (orb, ('row', 'day', 'unlit'))):
        for k in KEYS:
            for d in drop:
                views_of(k).pop(d, None)
    p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
    p.sub("const tintWord = c =>",
          "// one list of views per product, the same order in every tint (fix list 2026-11-20, 11)\n"
          f"const VORDER = {json.dumps(VORDER)};\n"
          "const reorder = (list, keys) => list.splice(0, list.length, ...keys.map(k => list.find(x => x[0] === k)).filter(Boolean));\n"
          "reorder(SPEAKER_VIEWS, VORDER.speaker); reorder(LAMP_VIEWS.dome, VORDER.dome); reorder(LAMP_VIEWS.orb, VORDER.orb); reorder(TT_VIEWS, VORDER.turntable);\n"
          "const tintWord = c =>")

    # --- 12. the rows of eight leave the stage: at full width under the gallery, each product in a row a link to its tint
    rows = {}
    for prod, files in (('dome', [('hemisphere-row.webp', 'Eight Hemispheres, one in each color')]),
                        ('orb', [('core-row.webp', 'Eight Core lamps, lit, one in each color'), ('core-row-day.webp', 'Eight Core lamps by day, one in each color')])):
        rows[prod] = []
        for f, alt in files:
            from PIL import Image
            path = os.path.join(web.SITE, 'img', 'rc', f); w, h = Image.open(path).size
            rows[prod].append({'src': f'img/rc/{f}', 'w': w, 'h': h, 'alt': alt, 'cuts': _row_cuts(path)})
    rows['speaker'] = 'fronts'
    p.sub("    <section class=\"lights\" id=\"p-lights\"", "    <section class=\"rows\" id=\"p-rows\" aria-label=\"In each color\" hidden></section>\n    <section class=\"lights\" id=\"p-lights\"")
    p.sub("  setTint(k);",
          "  setTint(k); renderRows(P, c);\n"
          "  { const e = document.getElementById('p-para'), t = PARA[P.id] || ''; e.innerHTML = t; e.hidden = !t; }")
    p.sub("// \"Copy link\": the product's own page",
          f"const ROWS = {json.dumps(rows, separators=(',', ':'))};\n"
          "function renderRows(P, c) {        // the row of eight under the gallery: each product in it a link to its own tint\n"
          "  const box = document.getElementById('p-rows'), R = ROWS[P.id], nm = o => o.name.toLowerCase(), cur = o => o.k === c.k ? ' aria-current=\"true\"' : '';\n"
          "  box.hidden = !R; if (!R) { box.replaceChildren(); return; }\n"
          "  box.innerHTML = R === 'fronts'\n"
          "    ? '<div class=\"fronts\">' + D.clouds.map(o => `<a href=\"#speaker-${nm(o)}\"${cur(o)}><img src=\"img/rc/${o.k}-tall.webp\" width=\"1000\" height=\"1250\" loading=\"lazy\" alt=\"Tropos in ${o.name}\"></a>`).join('') + '</div>'\n"
          "    : R.map(r => `<figure class=\"row8\"><img src=\"${r.src}\" width=\"${r.w}\" height=\"${r.h}\" loading=\"lazy\" alt=\"${r.alt}\">` + D.clouds.map((o, i) =>\n"
          "        `<a href=\"#${P.route}-${nm(o)}\" style=\"left:${r.cuts[i]}%;width:${(r.cuts[i + 1] - r.cuts[i]).toFixed(2)}%\" aria-label=\"${P.name(c)} in ${o.name}\"${cur(o)}></a>`).join('') + '</figure>').join('');\n"
          "}\n"
          "// \"Copy link\": the product's own page")
    # a paragraph from a folded page, under the product's sentence (15): Mantle's from /mantle, Core's "Cordless." from /lighting
    para = {'turntable': 'Its tinted plinth floats 40&nbsp;mm over a smoked base on four black posts. The motor is fixed under the plinth, and the phono stage is built in.',
            'orb': 'About five hours a charge at full brightness, longer dimmed. Set it back on its dock and it charges in two to three hours. When the cells tire, you change the cells, not the lamp.'}
    p.sub('<p class="line" id="p-line"></p>', '<p class="line" id="p-line"></p>\n        <p class="para" id="p-para" hidden></p>')
    p.sub("const ROWS = ", f"const PARA = {json.dumps(para)};\nconst ROWS = ")

    # --- 13. the turning view: "360" on its thumbnail, "Drag to turn" until it is dragged, the arrow keys turn it
    p.sub("  stage.replaceChildren(pic);",
          "  stage.replaceChildren(pic);\n"
          "  if (v === 'turn' && !turnTried) { stage.appendChild(el('span', { class: 'hint', 'aria-hidden': 'true' }, 'Drag to turn'));\n"
          "    pic.addEventListener('pointerdown', () => { turnTried = true; const t = stage.querySelector('.hint'); if (t) t.remove(); }, { once: true }); }")
    p.sub("const keys = (e, focus) => {\n",
          "let turnTried = false;\n"
          "const turnStep = d => { const pic = stage.querySelector('.spin'); if (!pic) return; cancelAnimationFrame(autoTurn); turnTried = true;\n"
          "  const t = stage.querySelector('.hint'); if (t) t.remove(); turnFrame = ((turnFrame + d) % N + N) % N; pic.style.backgroundPosition = frameAt(turnFrame); };\n"
          "const keys = (e, focus) => {\n"
          "  if (!focus && view === 'turn' && (e.key === 'ArrowRight' || e.key === 'ArrowLeft')) { e.preventDefault(); turnStep(e.key === 'ArrowRight' ? -1 : 1); return; }\n")

    # --- 14. under every bar picture its names row, the picture's only caption
    p.sub("      e = document.getElementById('cap'); e.textContent = t; e.hidden = !t; }",
          "      e = document.getElementById('cap'); e.textContent = t; e.hidden = !t;\n"
          "    const nr = NAMEROWS[(s.src || '').split('/').pop()]; if (nr) { e.innerHTML = nr; e.hidden = false; } }")
    p.sub("const ROWS = ", "const NAMEROWS = " + json.dumps({k: names_row(k) for k in BAR_NAMES}, separators=(',', ':')) + ";\nconst ROWS = ")

    # --- 15. the in-between pages folded: /tropos and /mantle into their product pages; /lighting rebuilt
    p.sub("  { const c = /^colou?r-([a-z]+)$/.exec(h);",
          "  if (LINE_OF[h] === 'speakers' || LINE_OF[h] === 'turntable') {     // /tropos and /mantle are their product pages now\n"
          "    h = LINE_OF[h] === 'speakers' ? 'speaker-ember' : 'mantle-ember'; history.replaceState(null, '', '#' + h); }\n"
          "  { const c = /^colou?r-([a-z]+)$/.exec(h);")
    spec = '[' + ', '.join(f"['{a}', `{b}`]" for a, b in TROPOS_SPEC) + ']'
    p.rest, nf = re.subn(r"facts: c => \[\['Acrylic', c\.tint\].*?\['Care', D\.care\]\],", lambda m: f"facts: c => {spec},", p.rest, count=1, flags=re.S)
    assert nf == 1, 'fix_1b: Tropos facts'
    # /lighting: the title in sight, one room picture with its names row, two equal tiles, then the rows, each lamp a link
    dots = lambda r: '<ul class="dots-row" aria-label="Colors">' + ''.join(
        f'<li><a href="#{r}-{NAMES[k]}" aria-label="{CNAME[k]}" title="{CNAME[k]}"><span class="coin-dot" style="--i:{C[k]["coin"]}"></span></a></li>' for k in KEYS) + '</ul>'
    def lt_tile(r, name, kind):
        return (f'<article class="lt-tile"><p class="ft-kind">{kind}</p><h2>{name}</h2>{dots(r)}'
                f'<a class="cta-btn cta-solid" href="#{r}-ember" data-carry="{r}">See {name}</a></article>')
    def row_fig(r, name, files):
        out = ''
        for f, alt in files:
            path = os.path.join(web.SITE, 'img', 'rc', f)
            from PIL import Image
            w, h = Image.open(path).size; cuts = _row_cuts(path)
            out += (f'<figure class="row8"><img src="img/rc/{f}" width="{w}" height="{h}" loading="lazy" alt="{alt}">' +
                    ''.join(f'<a href="#{r}-{NAMES[k]}" style="left:{cuts[n]}%;width:{cuts[n + 1] - cuts[n]:.2f}%" aria-label="{name} in {CNAME[k]}"></a>' for n, k in enumerate(KEYS)) +
                    '</figure>')
        return out
    from PIL import Image
    room_w, room_h = Image.open(os.path.join(web.SITE, 'img', 'rc', 'bar-pendants.webp')).size
    lighting = ('  <div class="lineview" data-line="lighting">\n'
                '    <div class="wrap"><p class="crumbs"><a href="#top">Home</a> / Lighting</p><h1 class="lt-title">Lighting</h1></div>\n'
                '  <section class="band lamps" id="lamps"><div class="wrap">\n'
                f'    <div class="lt-grid"><figure class="lt-room"><img src="img/rc/bar-pendants.webp" width="{room_w}" height="{room_h}" alt="Five Hemispheres over a bar in Acid, Ember and Dust, two Cores on the counter, a wall of records behind">'
                f'<figcaption class="names">{names_row("bar-pendants.webp")}</figcaption></figure>\n'
                '    <div class="lt-tiles">' + lt_tile('hemisphere', 'Hemisphere', 'Pendant') + lt_tile('core', 'Core', 'Table lamp') + '</div></div>\n'
                '    <div class="lt-rows">' + row_fig('hemisphere', 'Hemisphere', [('hemisphere-row.webp', 'Eight Hemispheres, one in each color')]) +
                row_fig('core', 'Core', [('core-row.webp', 'Eight Core lamps, lit, one in each color')]) + '</div>\n'
                '  </div></section>\n  </div>\n')
    m = re.search(r'  <div class="lineview" data-line="lighting">.*?(?=  <div class="lineview" data-line="turntable">)', p.rest, re.S)
    assert m, 'fix_1b: /lighting'
    p.rest = p.rest[:m.start()] + lighting + p.rest[m.end():]
    # the crumbs: Home / Lighting / Hemisphere in Ember; Tropos and Mantle have no page between, so Home / Tropos in Ember
    p.sub('<p class="crumbs"><a href="#top">Home</a> / <a id="p-line-link" href="#speakers">Speakers</a> / <span id="p-crumb"></span></p>',
          '<p class="crumbs"><a href="#top">Home</a> / <span id="p-line-wrap"><a id="p-line-link" href="#lighting">Lighting</a> / </span><span id="p-crumb"></span></p>')
    p.sub("document.getElementById('p-crumb').textContent = P.title(c);",
          "document.getElementById('p-crumb').textContent = P.title(c); document.getElementById('p-line-wrap').hidden = P.line !== 'lighting';")
    p.css("""
/* fix list 2026-11-20, build 1B */
.para { margin: 12px 0 0; max-width: 46ch; line-height: 1.5 }
.rows { margin: clamp(32px, 4vw, 56px) 0 0; display: grid; gap: 16px }
.fronts { display: grid; grid-template-columns: repeat(8, minmax(0, 1fr)); gap: 8px }
.fronts a { display: block; border-radius: 4px; overflow: hidden; outline-offset: 3px }
.fronts img { display: block; width: 100%; height: auto }
.fronts a[aria-current] { box-shadow: 0 0 0 2px var(--ink) }
.row8 { position: relative; margin: 0 }
.row8 img { display: block; width: 100%; height: auto; border-radius: 4px }
.row8 a { position: absolute; top: 0; bottom: 0; border-radius: 4px }
.row8 a:hover, .row8 a:focus-visible { box-shadow: inset 0 0 0 2px rgb(255 255 255 / .7); outline: none }
.row8 a[aria-current] { box-shadow: inset 0 0 0 2px rgb(255 255 255 / .9) }
@media (max-width: 760px) { .fronts { grid-template-columns: repeat(4, minmax(0, 1fr)) } }
.gallery .nav { display: grid !important }
.thumb.turn { position: relative } .thumb.turn::after { content: '360'; position: absolute; right: 4px; bottom: 4px; padding: 1px 5px; border-radius: 999px;
  background: rgb(255 255 255 / .88); color: #1C1A18; font: 600 11px/1.3 system-ui, sans-serif }
.stage .hint { position: absolute; left: 50%; bottom: 14px; transform: translateX(-50%); padding: 6px 12px; border-radius: 999px; background: rgb(255 255 255 / .9);
  color: #1C1A18; font-size: 14px; pointer-events: none }
.cap a { color: inherit }
/* /lighting: the title in sight, the room and the two lamps on the first screen */
.lt-title { margin: 8px 0 0; font-size: clamp(34px, 4.6vw, 64px); line-height: 1.02; letter-spacing: -0.035em }
#lamps.band { padding-top: 24px }
.lt-grid { display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 24px; align-items: start }
.lt-room { margin: 0 } .lt-room img { display: block; width: 100%; height: auto; max-height: calc(100vh - 240px); object-fit: cover; border-radius: 4px }
.lt-room .names, .names { margin-top: 10px; font-size: 14px; line-height: 1.6; color: var(--muted) } .names a { color: inherit }
.lt-tiles { display: grid; gap: 16px }
.lt-tile { padding: 22px 22px 24px; border-radius: 4px; background: #EAE6E0 } .lt-tile h2 { margin: 4px 0 12px; font-size: clamp(26px, 2.4vw, 36px); letter-spacing: -0.03em }
.lt-tile .dots-row { margin: 0 0 16px }
.lt-rows { display: grid; gap: 16px; margin-top: clamp(32px, 4vw, 56px) }
@media (max-width: 860px) { .lt-grid { grid-template-columns: minmax(0, 1fr) } .lt-room img { max-height: none } }
""")


# ---------------------------------------------------------------------------------------------------------------------
# Build 2: the product page (items 16 to 19)
KELVIN = {'red': 2200, 'green': 2700, 'ice': 2700, 'violet': 3000, 'orange': 4000, 'amber': 4000, 'blue': 4000, 'black': 4000}
ASK = {'speaker': 'Ask about a pair', 'dome': 'Ask about Hemisphere', 'orb': 'Ask about Core', 'turntable': 'Ask about Mantle'}
MAIL = 'hello@earf.world'
# Specifications: four or five plain headings, one fact to a row. {a|b}: a, or b on Fog. {lm} {K}: this color's own.
SPEC = {      # inches first, millimeters in brackets; pounds first; feet first for a cable (the coordinator 15:42, C3 1-3)
    'speaker': [
        ('Materials', [('Acrylic', '{tint}'), ('Cabinet', 'Cast acrylic, 0.8 in (20 mm), {tinted through|clear}'),
                       ('Lining', 'Polyester batts in white voile, 3.9 in (100 mm) at the top and the bottom'),
                       ('Horn', 'Thermoformed cast acrylic, 0.4 in (10 mm), in the cabinet&rsquo;s color; polished inside and out, on four black posts')]),
        ('Drivers and amplifier', [('Woofer', 'FaitalPRO 15PR400, 15-inch, with two ports in the front&rsquo;s lower corners'),
                                   ('Horn driver', 'B&amp;C DE1085TN, 2-inch compression driver'),
                                   ('Amplifier', 'Hypex FusionAmp FA123 built in: the woofer on two bridged channels, up to 125 W into its 8 &Omega;; the horn on its own; crossed at 1 kHz in its DSP')]),
        ('Sound and connections', [('Bass', 'To about 51 Hz at &minus;3 dB, before the room adds its own; the ports tuned to 38 Hz'),
                   ('Loudness', 'Up to about 115 dB at 3.3 ft (1 m), each'),
                   ('Inputs', 'XLR (and a link out), RCA, AES, S/PDIF coaxial and optical; USB to set it up'),
                   ('Power', '100&ndash;120 V / 200&ndash;240 V, 50/60 Hz, 350 W max'),
                   ('With a pair', 'Two power cords and a 16 ft (5 m) link cable between the speakers')]),
        ('Size and weight', [('Size', '51 in (1295 mm) tall, 22 in (560 mm) wide, the horn flush with the cabinet; 17.4 in (442 mm) deep overall, 16.5 in (420 mm) at the cabinet'),
                             ('Weight', 'About 165 lb (75 kg) each')]),
        ('Care', [('Care', '{care}')]),
    ],
    'dome': [
        ('Materials', [('Shade', 'Cast acrylic in three layers: its color on the outside, over a clear shell and an opal diffuser within'),
                       ('Cap', 'Satin black anodized aluminum, with a quarter-turn catch')]),
        ('Light', [('Output', 'About {lm} lm out of the shade in this color'), ('On the table', 'About 340 lux at 20 in (0.5 m) below, in every color'),
                   ('CRI', '90'), ('Color temperature', '{K} K')]),
        ('Electrical', [('Power', 'About 7 W at 120 V'), ('Dimming', 'Phase-cut (leading or trailing edge) or 0&ndash;10 V')]),
        ('Size and hanging', [('Size', '7.9 in (200 mm) across; 5.0 in (126 mm) from the rim to the top of the cap; the shade 3.9 in (100 mm) deep'),
                              ('Weight', 'About 3.5 lb (1.6 kg) hanging; the canopy about 0.9 lb (0.4 kg)'),
                              ('Cord', '10 ft (3 m), black, cloth-braided, cut to the drop at install'),
                              ('Drop', '23.6 in (600 mm) as standard: 30.6 in (776 mm) from the ceiling to the rim'),
                              ('Canopy', 'Satin black anodized aluminum, 5.9 in across, 2.0 in deep (150 x 50 mm)')]),
        ('Shades and care', [('Shades', 'In all eight colors, sold separately'),
                             ('Care', 'A quarter turn takes the shade off to wash: water and a drop of mild soap, then dry. No glass cleaner, alcohol or solvents: they craze acrylic.')]),
    ],
    'orb': [
        ('Materials', [('Ball', '{Tinted|Clear} cast acrylic, with an opal diffuser centered inside it'), ('Base', 'Its own color, satin')]),
        ('Light', [('Use', 'A glow, not a reading light'), ('Output', 'About {lm} lm out of the ball in this color'),
                   ('Color temperature', '{K} K'), ('Control', 'Touch the top of the base: tap to switch, hold to dim')]),
        ('Power', [('Runtime', 'About five hours a charge at full brightness, longer dimmed'),
                   ('Charging', 'Two to three hours on its dock'),
                   ('Cells', 'Three LiFePO4 18650, 14.4 Wh, replaceable, behind a hatch under the base')]),
        ('Size and weight', [('Size', '6.3 in (160 mm) ball, 7.4 in (187 mm) tall, the base 5.9 in (150 mm) across'), ('Weight', 'About 3.1 lb (1.4 kg) with its cells')]),
        ('In the box', [('Contents', 'The lamp, its dock, a 6.6 ft (2 m) braided USB-C cable and a 20 W USB-C adapter')]),
        ('Balls, rating and care', [('Balls', 'In all eight colors, sold separately. Each comes off by hand.'),
                                    ('Rating', 'Designed to meet IP44, for terraces and spilled drinks'), ('Cleaning', '{care}')]),
    ],
    'turntable': [
        ('Materials', [('Plinth', '{Cast acrylic in its color|Clear cast acrylic}, about 1 in (25 mm), raised 1.6 in (40 mm) over the base; its top face polished, the underside and the edges satin with a fine polished bevel'),
                       ('Posts', 'Four solid posts, 1.2 in (30 mm) across, satin black'), ('Hardware', 'Satin black throughout; the RCA sockets&rsquo; contacts are gold'),
                       ('Base', 'Smoked cast acrylic, 0.5 in (12.7 mm), set in 1.4 in (35 mm) all around'),
                       ('Platter', 'Cast acrylic, 11.8 in (300 mm) across, 0.8 in (21 mm) thick, in three layers'),
                       ('Cover', 'Included: a lift-off dust cover in the deck&rsquo;s own {tint|color}: 0.1 in (3 mm) cast acrylic, 17.6 x 14.1 x 3.9 in (448 x 358 x 100 mm), about 2.4 lb (1.1 kg). It rests on four small bumpers and lifts straight off; no hinges.')]),
        ('Playing', [('Drive', 'Belt, from Rega&rsquo;s 24 V motor, fixed beneath the plinth'), ('Speeds', '33 and 45 rpm, by a button on the Neo PSU'),
                     ('Arm', 'Rega RB330'), ('Cartridge', 'Ortofon 2M Black, fitted'),
                     ('Phono stage', 'Built in, for moving-magnet cartridges'),
                     ('Outputs', 'RCA line outputs and a ground post; a switch picks the built-in phono stage or bypass'),
                     ('Power', 'Two supplies at the wall: Rega&rsquo;s Neo PSU drives the motor; the phono stage runs on its own 18 V adapter.')]),
        ('Size and weight', [('Size', '17.7 in (450 mm) wide, 14.2 in (360 mm) deep, 6.3 in (161 mm) high to the top of the arm; 7.7 in (196 mm) with the cover on'),
                             ('Weight', 'About 25.6 lb (11.6 kg); about 28 lb (12.7 kg) with the cover')]),
        ('Care', [('Care', '{care}')]),
    ],
}
PARA2 = {'turntable': 'Its {tinted|clear} plinth is raised 40&nbsp;mm on four black posts over a smoked base. The motor is fixed under the plinth, and the phono stage is built in.',
         'orb': 'About five hours a charge at full brightness, longer dimmed. Set it back on its dock and it charges in two to three hours. When the cells tire, you change the cells, not the lamp.'}
LINK_IC = ('<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M8.5 11.5a3.5 3.5 0 0 0 5 0l2.5-2.5a3.5 3.5 0 0 0-5-5l-1 1M11.5 8.5a3.5 3.5 0 0 0-5 0L4 11a3.5 3.5 0 0 0 5 5l1-1" '
           'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>')


_SIDES = {}


def _sides(path):
    """The picture's left and right edge colors (medians of a 6 px strip), for the stage's sides."""
    if path not in _SIDES:
        from PIL import Image
        import numpy as np
        a = np.asarray(Image.open(path).convert('RGB')).astype(int)
        hx = lambda v: '#%02x%02x%02x' % tuple(int(x) for x in v)
        h = a.shape[0]
        col = lambda strip: ''.join(hx(np.median(strip[int(h * n / 10):int(h * (n + 1) / 10)].reshape(-1, 3), 0))[1:] for n in range(10))
        _SIDES[path] = col(a[:, :4]) + col(a[:, -4:])
    return _SIDES[path]


def fix_2(p, web):
    i, j, D = _data(p)
    # every picture without a ground of its own gets its sides' colors: the stage is wider than a tall picture
    views = [v for c in D['clouds'] for v in c['views'].values()]
    views += [v for L in D['lamps'].values() for t in L['colours'].values() for v in (t.get('views') or {}).values()]
    views += [v for t in D['tt']['colours'].values() for v in (t.get('views') or {}).values()]
    gr = {}
    for v in views:
        if isinstance(v, dict) and v.get('src') and not v.get('bg') and v['src'].endswith(('.webp', '.jpg', '.png')):
            f = os.path.join(web.SITE, v['src'])
            if os.path.exists(f):
                pass                                     # no sampled sides any more (the coordinator 12:27)
    for prod, groups in SPEC.items():           # every fact the pages hold, once (none added)
        for _, rows in groups:
            for _, v in rows:
                assert '{care}' in v or v, prod
    care = D['care']
    # --- 17. beside the pictures: kind and status, name, color dots with the chosen name, the one sentence, the ask
    m = re.search(r'<aside class="buy" aria-label="This product">.*?</aside>', p.rest, re.S)
    assert m, 'fix_2: the aside'
    ask = f'<a class="cta-btn cta-solid p-ask" href="mailto:{MAIL}">Ask</a>'
    aside = ('<aside class="buy" aria-label="This product">\n'
             '        <p class="num"><span id="p-num"></span></p>\n'
             '        <h1 class="named"><span id="p-name"></span><span class="pic" id="p-icon"></span></h1>\n'
             '        <ul class="swatches" id="swatches" aria-label="Color"></ul>\n'
             '        <p class="pick">Color: <b id="p-pick"></b><span class="pick-ic" id="p-pick-ic"></span></p>\n'
             '        <p class="line" id="p-line"></p>\n'
             '        <p class="para" id="p-para" hidden></p>\n'
             '        <p class="price">Price on request. <span id="p-unit"></span></p>\n'
             f'        <div class="acts">{ask.replace("p-ask", "p-ask", 1).replace("<a ", "<a id=\"p-enquire\" ", 1)}'
             f'<button type="button" class="ic-btn" id="p-share" aria-label="Copy link" title="Copy link">{LINK_IC}</button></div>\n'
             f'        <p class="addr2"><span>{MAIL}</span> <button type="button" class="btn sm" id="p-copy">Copy address</button></p>\n'
             '        <p class="share-note" id="p-share-note" aria-live="polite"></p>\n'
             '      </aside>')
    p.rest = p.rest[:m.start()] + aside + p.rest[m.end():]
    # the facts under the gallery as "Specifications", with the figures' caveat
    p.sub('      <section class="gallery" aria-label="Pictures">', '      <div class="pcol">\n      <section class="gallery" aria-label="Pictures">')
    p.sub('        <p class="render-note">Pictures are renders. Nothing is built yet.</p>\n      </section>',
          '        <p class="render-note">Pictures are renders. Nothing is built yet.</p>\n      </section>\n'
          '      <section class="spec2" id="p-spec" aria-labelledby="p-spec-h"><h2 id="p-spec-h">Specifications</h2><div id="p-spec-body"></div>'
          '<p class="figs">All figures come from the design; none is measured yet.</p></section>\n      </div>')
    # --- 18/19. at the foot: the ask again, the other three products in this tint; on a phone the ask in a bar
    p.sub('    <p class="more-line" id="p-more"></p>',
          f'    <div class="foot-ask">{ask}</div>\n'
          '    <section class="others" id="p-others" aria-label="The family"></section>\n'
          f'    <div class="ask-bar">{ask}</div>')
    p.sub("  document.getElementById('p-enquire').textContent = P.ask;\n", "")
    p.sub("  document.getElementById('facts').innerHTML = P.facts(c).map(([a, b]) => `<dt>${a}</dt><dd>${b}</dd>`).join('');\n",
          "  renderSpec(P, c); renderAsk(P, c);\n")
    p.sub("  document.getElementById('p-more').innerHTML = (MORE[P.id] || '').replace(/#(speaker|hemisphere|core|mantle)-[a-z]+/g, (x, r) => `#${r}-${c.name.toLowerCase()}`);\n",
          "  renderOthers(P, c);\n")
    p.sub("{ const e = document.getElementById('p-para'), t = PARA[P.id] || ''; e.innerHTML = t; e.hidden = !t; }",
          "{ const e = document.getElementById('p-para'), t = fillSpec(PARA[P.id] || '', c); e.innerHTML = t; e.hidden = !t; }")
    pi = p.rest.index('const PARA = '); pj = p.rest.index('\n', pi)
    p.rest = p.rest[:pi] + f'const PARA = {json.dumps(PARA2)};' + p.rest[pj:]
    # the other three, from the family's tiles
    from PIL import Image
    pic = lambda f, k: f'img/rc/{k}-tall.webp' if f == 'tropos' else f'img/rc/tile-{f}-{NAMES[k]}.webp'
    src0 = {'tropos': 'img/rc/red-tall.webp', 'mantle': 'img/rc/mantle-ember.webp', 'hemisphere': 'img/rc/home-hemisphere-ember.webp', 'core': 'img/rc/home-core-ember.webp'}
    others = []
    for f, name, route, kind in TILES:
        for k in KEYS:
            assert os.path.exists(os.path.join(web.SITE, pic(f, k))), ('fix_2: no tile', pic(f, k))
        w, h = Image.open(os.path.join(web.SITE, pic(f, 'red'))).size
        others.append({'route': route, 'name': name, 'kind': kind, 'w': w, 'h': h, 'ground': _ground(os.path.join(web.SITE, src0[f])),
                       'pics': {k: pic(f, k) for k in KEYS}})
    lm = {pid: D['lamps'][pid].get('lm') for pid in D['lamps']}
    p.sub("// \"Copy link\": the product's own page",
          f"const SPEC = {json.dumps(SPEC, separators=(',', ':'))}, LM = {json.dumps(lm)}, KELVIN = {json.dumps(KELVIN)}, CARE = {json.dumps(care)};\n"
          f"const GR = {json.dumps(gr, separators=(',', ':'))};\n"
          "const grOf = s => { const h = s && GR[s.src]; if (!h) return ''; const c = h.match(/.{6}/g).map(x => '#' + x), st = cs => cs.map((x, i) => `${x} ${5 + 10 * i}%`).join(', ');\n"
          "  return `linear-gradient(${st(c.slice(0, 10))}) left / 51% 100% no-repeat, linear-gradient(${st(c.slice(10))}) right / 51% 100% no-repeat`; };\n"
          f"const ASK = {json.dumps(ASK)}, MAIL = '{MAIL}', OTHERS = {json.dumps(others, separators=(',', ':'))}, ARROW = {json.dumps(ARROW)};\n"
          "const fillSpec = (t, c) => t.replace(/\\{([^{}|]*)\\|([^{}]*)\\}/g, (x, a, b) => c.k === 'ice' ? b : a).replace('{tint}', c.tint)\n"
          "  .replace('{lm}', (LM[P.id] || {})[c.k]).replace('{K}', KELVIN[c.k]).replace('{care}', CARE);\n"
          "function renderSpec(P, c) {        // Specifications: plain headings, one fact to a row (fix list 2026-11-20, 17)\n"
          "  document.getElementById('p-spec-body').innerHTML = (SPEC[P.id] || []).map(([h, rows]) => `<h3>${h}</h3>` + (rows.length === 1\n"
          "    ? `<p class=\"spec1\">${fillSpec(rows[0][1], c)}</p>` : '<dl class=\"facts\">' + rows.map(([a, b]) => `<dt>${a}</dt><dd>${fillSpec(b, c)}</dd>`).join('') + '</dl>')).join(''); }\n"
          "function renderAsk(P, c) {         // the ask: a letter, its subject the product in its color (18)\n"
          "  const t = P.title(c), href = `mailto:${MAIL}?subject=${encodeURIComponent(t)}&body=${encodeURIComponent(`${t}. Quantity: \\nCountry: `)}`;\n"
          "  document.querySelectorAll('#pdp .p-ask').forEach(a => { a.textContent = ASK[P.id] || 'Ask'; a.href = href; }); }\n"
          "function renderOthers(P, c) {      // the other three in the tint now chosen, each a link to it (19)\n"
          "  const nm = c.name.toLowerCase();\n"
          "  document.getElementById('p-others').innerHTML = '<div class=\"ftiles ftiles3\">' + OTHERS.filter(o => o.route !== P.route).map(o =>\n"
          "    `<a class=\"ftile\" href=\"#${o.route}-${nm}\"><span class=\"ft-pic\" style=\"background:${o.ground}\"><img src=\"${o.pics[c.k]}\" width=\"${o.w}\" height=\"${o.h}\" loading=\"lazy\" alt=\"${o.name} in ${c.name}\"></span>`\n"
          "    + `<span class=\"ft-body\"><span class=\"ft-kind\">${o.kind}</span><h3 class=\"ft-name\">${o.name}</h3><span class=\"ft-btn\">See ${o.name} ${ARROW}</span></span></a>`).join('') + '</div>'; }\n"
          "{ const bar = document.querySelector('#pdp .ask-bar'), seen = new Set();      // the phone's bar steps away while an ask is on screen\n"
          "  const io = new IntersectionObserver(es => { es.forEach(e => e.isIntersecting ? seen.add(e.target) : seen.delete(e.target)); bar.classList.toggle('off', seen.size > 0); });\n"
          "  document.querySelectorAll('#p-enquire, #pdp .foot-ask .p-ask').forEach(a => io.observe(a)); }\n"
          "document.getElementById('p-copy').addEventListener('click', () => {\n"
          "  const note = document.getElementById('p-share-note'), say = t => { note.textContent = t; setTimeout(() => { note.textContent = ''; }, 2400); };\n"
          "  try { navigator.clipboard.writeText(MAIL).then(() => say('Address copied.'), () => say(MAIL)); } catch (e) { say(MAIL); } });\n"
          "// \"Copy link\": the product's own page")

    # --- 16. the gallery
    # the stage in the picture's own shape (the phone's tall cut on a phone), capped in height
    p.sub("  stage.style.background = P.id === 'speaker' ? ground(v) : 'transparent'; if (P.id === 'turntable') stage.style.setProperty('aspect-ratio', '3 / 2', 'important'); else stage.style.removeProperty('aspect-ratio');",
          "  stage.parentElement.parentElement.style.setProperty('--sar', (phone.matches && s.tall && (v === 'habitat' || s.fill) ? s.tall.w / s.tall.h : s.w / s.h).toFixed(4));\n"
          "  stage.style.background = 'transparent';      // the picture whole on the page's paper, no sampled ground (the coordinator 12:27)")
    p.sub("new ResizeObserver(() => { if (cur) stage.style.background = ground(view); }).observe(stage);",
          "new ResizeObserver(() => { if (cur) stage.style.background = 'transparent'; }).observe(stage);")
    p.sub("thumbs.addEventListener('keydown', e => keys(e, true));",
          "thumbs.addEventListener('keydown', e => keys(e, true));\n"
          "// the arrow keys turn the pictures without a first click (16)\n"
          "addEventListener('keydown', e => { if (pdp.hidden || e.defaultPrevented || e.altKey || e.metaKey || e.ctrlKey || e.shiftKey) return;\n"
          "  if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;\n"
          "  if (e.target.closest && e.target.closest('input, textarea, select, [contenteditable], #thumbs, #stage')) return;\n"
          "  keys(e, false); });\n"
          "// a color click keeps the view and adds no step to Back: the address is replaced, not added to\n"
          "addEventListener('click', e => { const a = e.target.closest && e.target.closest('#swatches a');\n"
          "  if (!a || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;\n"
          "  e.preventDefault(); e.stopPropagation(); const h = a.getAttribute('href'); if (h === location.hash) return;\n"
          "  WANT = view; history.replaceState(null, '', location.pathname + h); dispatchEvent(new HashChangeEvent('hashchange')); }, true);\n"
          "// a click on the picture opens its full file (a drag or a swipe does not)\n"
          "let downAt = null;\n"
          "stage.addEventListener('pointerdown', e => { downAt = [e.clientX, e.clientY]; });\n"
          "stage.addEventListener('click', e => { if (view === 'turn' || view === 'spin' || !downAt || Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) > 8) return;\n"
          "  const s = src(BY[cur], view); if (s && s.src) window.open(s.src, '_blank', 'noopener'); });")

    # the same words everywhere the page still holds them (the old /mantle view, the data behind the facts)
    for a, b in (('it floats 40 mm over the base', 'raised 40 mm on four posts over the base'),
                 ('Its tinted plinth floats 40&nbsp;mm over a smoked base on four black posts', 'Its tinted plinth is raised 40&nbsp;mm on four black posts over a smoked base'),
                 ('"Mains"', '"Power"'), ('"Fitting"', '"Cap"'), ('sold singly', 'sold separately'), ('a 600 mm drop as standard', 'a standard 600 mm drop')):
        assert a in p.rest, ('fix_2: words', a)
        p.rest = p.rest.replace(a, b)
    m = re.search(r"const MORE = \{.*?\n\};\n", p.rest, re.S)
    assert m, 'fix_2: MORE'
    p.rest = p.rest[:m.start()] + p.rest[m.end():]

    # --- 18. /contact: a page of its own, no opening
    p.sub("    page = 'home'; showMain('home'); document.title = h === 'contact' ? 'Contact · EARF' : TITLE0; heroIn();",
          "    const oc = h === 'contact'; page = oc ? 'contact' : 'home'; showMain('home'); home.classList.toggle('only-contact', oc);\n"
          "    document.title = oc ? 'Contact · EARF' : TITLE0; if (!oc) heroIn();")
    p.sub("    if (target && h !== 'top') target.scrollIntoView();", "    if (oc) scrollTo(0, 0); else if (target && h !== 'top') target.scrollIntoView();")

    p.css("""
/* fix list 2026-11-20, build 2: the product page */
:root { --cap: max(300px, calc(100svh - 270px)) }
.pdp { grid-template-columns: minmax(0, 2fr) minmax(280px, 1fr) !important; gap: clamp(28px, 3.4vw, 56px) !important }
.pcol { display: grid; gap: clamp(40px, 5vw, 72px); min-width: 0; align-content: start }
/* the stage spans the column; its height the picture's at that width, capped so the thumbnails stay on the first screen;
   a picture narrower than that sits in it whole, on its own ground carried to the sides */
.gallery { container-type: inline-size }
.stage { aspect-ratio: auto !important; width: 100%; height: min(var(--cap), calc(100cqw / var(--sar, 0.8))) }
.stage .fit, .stage .fill img { cursor: zoom-in }
.stage .fill { width: 100%; height: 100% } .stage .fill img { object-fit: contain !important }
.stage .spin, .stage .spinner { cursor: grab }
.thumbs { display: flex !important; flex-wrap: wrap; gap: 8px; overflow: visible !important; margin: 0 !important; padding: 0 !important }
.thumb { width: 64px !important; height: 64px !important; flex: none; aspect-ratio: 1 }
.cap { min-height: 1.6em }
.buy { gap: 16px }
.buy .pick { margin: -4px 0 0 }
.buy .price { margin: 0 }
.acts { align-items: center }
.ic-btn { width: 44px; height: 44px; border-radius: 50%; border: 1px solid var(--rule); background: transparent; color: var(--ink); display: grid; place-items: center; cursor: pointer; padding: 0 }
.ic-btn svg { width: 20px; height: 20px }
.ic-btn:hover { border-color: var(--ink) }
.addr2 { margin: 0; display: flex; flex-wrap: wrap; align-items: center; gap: 10px; font-size: 15px; color: var(--muted) }
.addr2 span { user-select: all; color: var(--ink) }
.btn.sm { min-height: 36px; padding: 0 14px; font-size: 14px }
.share-note:empty { display: none }
.spec2 h2 { margin: 0 0 8px; font-size: clamp(26px, 2.4vw, 36px); letter-spacing: -0.03em }
.spec2 h3 { margin: 28px 0 8px; font-size: 13px; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); font-weight: 600 }
.spec2 .facts { grid-template-columns: 160px minmax(0, 1fr); border-top: 1px solid var(--ink) }
.spec2 .spec1 { margin: 0; padding: 10px 0; border-top: 1px solid var(--ink); font-family: var(--spec-mono); font-size: 15px }
.spec2 .figs { margin: 20px 0 0; font-size: 14px; color: var(--muted) }
.foot-ask { padding-block: clamp(40px, 5vw, 64px) 24px }
.others { padding-bottom: 72px }
.ftiles3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px }
.ask-bar { display: none }
#copy { display: inline-flex } #copy-note { display: block }
#home.only-contact > :not(#contact) { display: none !important }
#home.only-contact #contact { min-height: calc(100svh - var(--header, 64px) - 160px); padding-top: clamp(48px, 8vw, 120px) }
@media (max-width: 860px) {
  .pdp { grid-template-columns: minmax(0, 1fr) !important }
  .pcol { display: contents } .pcol > .spec2 { order: 3 }
  :root { --cap: calc(100svh - 200px) }
  .spec2 .facts { grid-template-columns: minmax(0, 1fr) }
}
@media (max-width: 700px) {
  .ftiles3 { grid-template-columns: minmax(0, 1fr) }
  .ftiles3 > .ftile { display: flex !important; flex-direction: row !important; gap: 14px; align-items: center }
  .thumb { width: 52px !important; height: 52px !important }
  .ftiles3 .ft-pic { width: 40%; flex: none }
  .ftiles3 .ft-body { padding: 0 }
  .ask-bar { display: flex; position: fixed; left: 0; right: 0; bottom: 0; z-index: 40; padding: 10px 16px calc(10px + env(safe-area-inset-bottom));
    background: var(--page); border-top: 1px solid var(--rule) }
  .ask-bar .cta-btn { flex: 1; justify-content: center }
  body:has(#pdp:not([hidden])) { padding-bottom: 72px }
  .ask-bar { transition: transform .2s ease } .ask-bar.off { transform: translateY(110%); visibility: hidden }
}
@media (orientation: landscape) and (max-height: 520px) { :root { --cap: 80svh } }
""")


# ---------------------------------------------------------------------------------------------------------------------
# Build 3: addresses, phone, files (items 20 to 22)
ROUTES3 = [('hemisphere', 'Hemisphere'), ('core', 'Core'), ('mantle', 'Mantle')]
# each place's speaker, measured on its master (fractions of width and height): center x, height, center y
PLACE_BOX = {'red': (.50, .42, .58), 'orange': (.46, .35, .505), 'amber': (.51, .41, .495), 'green': (.46, .43, .545),
             'blue': (.635, .42, .55), 'violet': (.625, .41, .575), 'ice': (.505, .42, .66), 'black': (.505, .34, .53)}
PLACE_SPEAKER = 0.56      # the speaker's height in every tile, as a share of the tile's
PLACE_CY = 0.56           # and its center's height


def _grain_save(im, path, q=90, sigma=2.0, seed=7):
    """Fine monochrome grain before encoding, so a near-black ground holds its gradient instead of a few flat blocks."""
    import numpy as np
    from PIL import Image
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    n = np.random.default_rng(seed).normal(0, sigma, a.shape[:2])[..., None]
    Image.fromarray(np.clip(a + n, 0, 255).round().astype(np.uint8)).save(path, 'WEBP', quality=q, method=6)


def fix_3(p, web):
    import site_v2
    from PIL import Image
    i, j, D = _data(p)
    # --- 20. real paths for the lamps and Mantle: the clean map knows them (the pages are written in finish_3); last
    # build's pages and cards go first, so the deploy check sees none of their old names
    import glob, shutil
    for r, _ in ROUTES3:
        if os.path.isdir(os.path.join(web.SITE, r)):
            shutil.rmtree(os.path.join(web.SITE, r))
        for f in glob.glob(os.path.join(web.IMG, 'rc', f'og-{r}-*.jpg')) + glob.glob(os.path.join(web.IMG, 'rc', f'card-{r}-*.jpg')):
            os.remove(f)
    a = p.rest.index('(() => { const P = ') + len('(() => { const P = ')
    b = p.rest.index(', R = Object', a)
    P = json.loads(p.rest[a:b])
    for r, _ in ROUTES3:
        for k in KEYS:
            P[f'{r}-{NAMES[k]}'] = f'/{r}/{NAMES[k]}'
    p.rest = p.rest[:a] + json.dumps(P) + p.rest[b:]
    # "Copy link" copies the address in the bar
    p.sub("const url = location.hash ? `${location.origin}/s/${location.hash.slice(1)}` : location.href, note",
          "const url = location.href, note")
    # an unknown fragment: the not-found view
    p.sub('<main id="pdp" hidden>',
          '<main id="nf" hidden tabindex="-1"><div class="wrap nf"><h1>Nothing here.</h1><nav class="nf-links" aria-label="Pages">'
          '<a href="#speaker-ember" data-carry="speaker">Tropos</a><a href="#lighting">Lighting</a><a href="#mantle-ember" data-carry="mantle">Mantle</a>'
          '<a href="#contact">Contact</a></nav></div></main>\n\n<main id="pdp" hidden>')
    p.sub("MAINS = { home, line: lineMain, color: colourMain, pdp };", "MAINS = { home, line: lineMain, color: colourMain, pdp, nf: document.getElementById('nf') };")
    p.sub("    const oc = h === 'contact'; page = oc",
          "    if (h && h !== 'top' && h !== 'contact' && !document.getElementById(h)) {      // an address the site does not have\n"
          "      page = 'nf'; showMain('nf'); home.classList.remove('only-contact'); document.title = 'Nothing here · EARF'; scrollTo(0, 0); navAt(null); last = page; return; }\n"
          "    const oc = h === 'contact'; page = oc")
    # pages that skip the opening keep the header's still globe (the 339 kB sheet is not fetched)
    p.sub("const own = !G.layers && !document.documentElement.classList.contains('intro');",
          "const own = false;      // no opening: the still globe, not the 339 kB sheet (fix list 2026-11-20, 20)")

    # --- 21. phone and input
    p.sub("const menuOpen = o => { navEl.classList.toggle('open', o); menuBtn.setAttribute('aria-expanded', String(o)); };",
          "const menuOpen = o => { navEl.classList.toggle('open', o); menuBtn.setAttribute('aria-expanded', String(o)); menuBtn.textContent = o ? 'Close' : 'Menu'; };\n"
          "document.addEventListener('pointerdown', e => { if (navEl.classList.contains('open') && !navEl.contains(e.target)) menuOpen(false); });\n"
          "addEventListener('scroll', () => { if (navEl.classList.contains('open')) menuOpen(false); }, { passive: true });\n"
          "// the skip link: to whichever page is showing, without touching the address\n"
          "addEventListener('click', e => { const a = e.target.closest && e.target.closest('a.skip'); if (!a) return; e.preventDefault(); e.stopPropagation();\n"
          "  const m = [...document.querySelectorAll('main')].find(x => !x.hidden); if (m) { m.setAttribute('tabindex', '-1'); m.focus(); } }, true);")
    _sub_any(p, '<header class="top">', '<a class="skip" href="#top">Skip to content</a>\n<header class="top">')
    _sub_any(p, 'html.cursor, html.cursor * { cursor: none !important }', '')
    # /lighting: the dots with their names
    p.rest, n = re.subn(r'(<li><a href="#(?:hemisphere|core)-[a-z]+" aria-label="(\w+)" title="\2"><span class="coin-dot" style="[^"]*"></span>)(</a></li>)',
                        r'\1<span class="dn">\2</span>\3', p.rest)
    assert n == 16, ('fix_3: /lighting dots', n)

    # --- 22. files from the masters
    LF = os.path.join(web.ROOT, site_v2.LAMP_FINAL)
    lamp = [(f'hemisphere-{n}-direct', f'hemisphere-{n}', 1200) for n in NAMES.values()]
    lamp += [(f'hemisphere-{n}-under', f'hemisphere-{n}-under', 1200) for n in NAMES.values()]
    lamp += [(f'core-{n}', f'core-{n}', 1200) for n in NAMES.values()]
    lamp += [(f'hemisphere-ember-{d}', f'hemisphere-ember-{d}', 1200) for d in ('off', 'cap', 'rim')]
    lamp += [('hemisphere-cluster', 'hemisphere-cluster', 1600), ('hemisphere-row', 'hemisphere-row', 2000), ('core-row', 'core-row', 2000)]
    for src, dst, w in lamp:
        im = Image.open(LF.format(f=src)).convert('RGB')
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        out = os.path.join(web.IMG, 'rc', dst + '.webp')
        assert os.path.exists(out), ('fix_3: no lamp file', out)
        assert Image.open(out).size == im.size, ('fix_3: size', dst, Image.open(out).size, im.size)
        _grain_save(im, out)
    # Horn, behind: the master's whole frame, 1200 x 900
    for c in D['clouds']:
        v = c['views'].get('horn-back')
        if not v:
            continue
        name = NAMES[c['k']]
        im = Image.open(os.path.join(web.ROOT, site_v2.HORN_BACK_SRC.format(name=name))).convert('RGB')
        assert im.width >= 1040, ('fix_3: horn-back master', im.size)
        im.save(os.path.join(web.IMG, 'rc', f'{c["k"]}-horn-back.webp'), 'WEBP', quality=86, method=6)
        v['w'], v['h'] = im.size
    i, j, _ = _data(p)                                 # the page has moved since D was read
    p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
    # the eight place tiles stay the whole approved pictures (the coordinator took the re-cut back, 13:56)

    p.css("""
/* fix list 2026-11-20, build 3: phone and input */
.skip { position: absolute; left: 12px; top: -60px; z-index: 100; padding: 10px 16px; border-radius: 999px; background: var(--ink); color: var(--page); text-decoration: none }
.skip:focus { top: 12px }
.swatches { gap: 0 4px !important } .swatches a { width: 44px !important; height: 44px !important; padding: 3px; box-sizing: border-box }
.swatches a[aria-current="true"] { outline-offset: 0 !important }
@media (max-width: 700px) { .swatches { gap: 0 !important } }
.lt-tile .dots-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(92px, 1fr)); gap: 2px 8px }
.lt-tile .dots-row a { width: auto; height: auto; min-height: 44px; display: flex; align-items: center; gap: 8px; border-radius: 22px; color: var(--ink); text-decoration: none; font-size: 14px }
.lt-tile .dots-row .coin-dot { width: 30px; height: 30px; flex: none }
.crumbs a { display: inline-flex; align-items: center; min-height: 44px }
a.cta-btn, .ft-btn { min-height: 44px }
.names a { display: inline-block; padding-block: 10px }
.cur-dot { display: none !important }
.cur-ring.on { background: none !important }
#nf .nf { padding-block: 18vh 24vh } #nf h1 { margin: 0 0 24px; font-size: clamp(40px, 6vw, 72px); letter-spacing: -0.03em }
.nf-links { display: flex; flex-wrap: wrap; gap: 8px 24px } .nf-links a { color: var(--ink); min-height: 44px; display: inline-flex; align-items: center }
""")


def _og_card(src, dst, paper=False):
    """A 1200 x 630 link card from a product picture: the picture whole at the card's height, its edges carried out to the sides."""
    from PIL import Image, ImageFilter
    im = Image.open(src).convert('RGB')
    im = im.resize((round(im.width * 630 / im.height), 630), Image.LANCZOS)
    if im.width > 1200:
        x = (im.width - 1200) // 2
        im = im.crop((x, 0, x + 1200, 630))
    can = Image.new('RGB', (1200, 630), (244, 241, 236))      # the page's paper, as the Tropos cards
    side = (1200 - im.width) // 2
    if side > 0 and not paper:
        can.paste(im.crop((0, 0, 6, 630)).resize((side + 2, 630), Image.BILINEAR).filter(ImageFilter.GaussianBlur(10)), (0, 0))
        can.paste(im.crop((im.width - 6, 0, im.width, 630)).resize((1200 - side - im.width + 2, 630), Image.BILINEAR).filter(ImageFilter.GaussianBlur(10)), (side + im.width - 2, 0))
    can.paste(im, (side, 0))
    can.save(dst, 'JPEG', quality=86)


def finish_3(web):
    """The 24 lamp and Mantle addresses, each with its own title, description and card; /mantle forwards to Mantle in Ember."""
    import html
    pic = {'hemisphere': 'img/rc/hemisphere-{n}.webp', 'core': 'img/rc/core-{n}.webp', 'mantle': 'img/rc/mantle-{n}-house.webp'}
    idx = open(os.path.join(web.SITE, 'index.html')).read()
    e = lambda x: html.escape(x, quote=True)
    for r, name in ROUTES3:
        for k in KEYS:
            n = NAMES[k]; h = f'{r}-{n}'
            card = f'img/rc/card-{r}-{n}.jpg'      # not og-mantle-*: that name is held by the deploy check
            _og_card(os.path.join(web.SITE, pic[r].format(n=n)), os.path.join(web.SITE, card), paper=(r == 'mantle'))
            alt = f'{name} in {CNAME[k]}'
            sf = os.path.join(web.SITE, 's', h + '.html')
            s = open(sf).read()
            s = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*(")', r'\g<1>' + web.URL + '/' + card + r'\2', s)
            s = re.sub(r'(<meta property="og:image:alt" content=")[^"]*(")', r'\g<1>' + alt + r'\2', s)
            s = re.sub(r'("image":")[^"]*(")', r'\g<1>' + web.URL + '/' + card + r'\2', s)
            open(sf, 'w').write(s)
            title = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1))
            desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
            url = f'{web.URL}/{r}/{n}'
            page = idx.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n'
                               f'<script>if (!location.hash) history.replaceState(null, "", location.pathname + "#{h}")</script>', 1)
            page = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', page, count=1)
            page = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', page, count=1)
            page = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{e(title)}">', page, count=1)
            page = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{e(desc)}">', page, count=1)
            page = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">\n<link rel="canonical" href="{url}">', page, count=1)
            page = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{web.URL}/{card}">\n'
                          f'<meta property="og:image:alt" content="{e(alt)}">', page, count=1)
            page = page.replace('<meta name="twitter:card" content="summary_large_image">', '<meta name="twitter:card" content="summary_large_image">\n'
                                f'<meta name="twitter:title" content="{e(title)}">\n<meta name="twitter:description" content="{e(desc)}">\n'
                                f'<meta name="twitter:image" content="{web.URL}/{card}">', 1)
            assert 'noindex' in page and f'#{h}' in page
            os.makedirs(os.path.join(web.SITE, r), exist_ok=True)
            open(os.path.join(web.SITE, r, n + '.html'), 'w').write(page)
    vj = os.path.join(web.SITE, 'vercel.json')
    v = json.load(open(vj))
    if not any(x['source'] == '/mantle' for x in v.get('redirects', [])):
        v.setdefault('redirects', []).append({'source': '/mantle', 'destination': '/mantle/ember', 'permanent': True})
    json.dump(v, open(vj, 'w'), indent=2)


# ---------------------------------------------------------------------------------------------------------------------
# The critics' list on Build 1B (the coordinator, 20 Nov 12:56)
def _split_row(src, w, h, alt, cuts, href, label, current=''):
    """A row of eight as two halves of four: side by side on a desktop (the picture whole), stacked on a phone."""
    out = []
    for half in (0, 1):
        links = ''
        for n in range(half * 4, half * 4 + 4):
            left = max(0.0, (cuts[n] - 50 * half) * 2); right = min(100.0, (cuts[n + 1] - 50 * half) * 2)
            links += f'<a href="{href[n]}" style="left:{left:.2f}%;width:{right - left:.2f}%" aria-label="{label[n]}"{current[n] if current else ""}></a>'
        img = (f'<img src="{src}" width="{w}" height="{h}" loading="lazy" alt="{alt}">' if half == 0 else
               f'<img src="{src}" width="{w}" height="{h}" loading="lazy" alt="" aria-hidden="true">')
        out.append(f'<div class="half h{half}">{img}{links}</div>')
    return '<figure class="row8 split">' + ''.join(out) + '</figure>'


def fix_4(p, web):
    from PIL import Image
    i, j, D = _data(p)
    C = {c['k']: c for c in D['clouds']}
    # --- 1. Copy link: the product and tint only; the address drops "/out" once the visitor leaves that view
    p.sub("// \"Copy link\": the product's own page",
          "function productPath() { return (P.route === 'speaker' ? '/tropos/' : `/${P.route}/`) + BY[cur].name.toLowerCase(); }\n"
          "// \"Copy link\": the product's own page")
    p.sub("const url = location.href, note", "const url = location.origin + productPath(), note")
    p.sub("  const c = BY[cur], list = shown(c), i = list.indexOf(v); view = v;\n",
          "  const c = BY[cur], list = shown(c), i = list.indexOf(v); view = v;\n"
          "  { const o = /^#[a-z]+-[a-z]+\\/([a-z-]+)$/.exec(location.hash); if (o && v !== (VIEWKEY[o[1]] || o[1])) history.replaceState(null, '', productPath()); }\n")
    # --- 2. a view with a names row carries no "Shown in" pill; the pill's line ends with its period
    p.sub("  if (s.shown) stage.appendChild(el('span', { class: 'tag' }, `Shown in ${BY[s.shown].name}`));",
          "  if (s.shown && !NAMEROWS[(s.src || '').split('/').pop()]) stage.appendChild(el('span', { class: 'tag' }, `Shown in ${BY[s.shown].name}.`));")
    # --- 3. the two moved paragraphs go: their page says it already
    a = p.rest.index('const PARA = '); b = p.rest.index('\n', a)
    p.rest = p.rest[:a] + 'const PARA = {};' + p.rest[b:]
    # --- 5. Core at the bar: one picture, one alt, on all eight
    p.sub("['bar', 'At the bar', c => c.k === 'red' ? 'Core in Ember on a bar table, a wall of records behind.' : 'Two Cores on a bar counter in Ember and Dust, five Hemispheres over them.'],",
          "['bar', 'At the bar', () => 'Core in Ember on a bar table, a wall of records behind.'],")
    # --- 6. the names row directly under its picture, its height kept
    p.sub('        <div class="thumbs" id="thumbs" role="tablist" aria-label="Pictures"></div>\n        <p class="cap" id="cap" aria-live="polite"></p>',
          '        <p class="cap" id="cap" aria-live="polite"></p>\n        <div class="thumbs" id="thumbs" role="tablist" aria-label="Pictures"></div>')
    # --- 9. the rows of eight as two rows of four on a phone (the product pages' and /lighting's)
    a = p.rest.index('function renderRows(P, c) {'); b = p.rest.index('\n}\n', a) + 3
    p.rest = p.rest[:a] + (
        "function renderRows(P, c) {        // the row of eight under the gallery: each product in it a link to its own tint; two rows of four on a phone\n"
        "  const box = document.getElementById('p-rows'), R = ROWS[P.id], nm = o => o.name.toLowerCase(), cur = o => o.k === c.k ? ' aria-current=\"true\"' : '';\n"
        "  box.hidden = !R; if (!R) { box.replaceChildren(); return; }\n"
        "  box.innerHTML = R === 'fronts'\n"
        "    ? '<div class=\"fronts\">' + D.clouds.map(o => `<a href=\"#speaker-${nm(o)}\"${cur(o)}><img src=\"img/rc/${o.k}-tall.webp\" width=\"1000\" height=\"1250\" loading=\"lazy\" alt=\"Tropos in ${o.name}\"></a>`).join('') + '</div>'\n"
        "    : R.map(r => '<figure class=\"row8 split\">' + [0, 1].map(hf => `<div class=\"half h${hf}\"><img src=\"${r.src}\" width=\"${r.w}\" height=\"${r.h}\" loading=\"lazy\" ` + (hf ? 'alt=\"\" aria-hidden=\"true\">' : `alt=\"${r.alt}\">`)\n"
        "        + D.clouds.slice(hf * 4, hf * 4 + 4).map((o, n) => { const k = hf * 4 + n, L = Math.max(0, (r.cuts[k] - 50 * hf) * 2), Rr = Math.min(100, (r.cuts[k + 1] - 50 * hf) * 2);\n"
        "          return `<a href=\"#${P.route}-${nm(o)}\" style=\"left:${L.toFixed(2)}%;width:${(Rr - L).toFixed(2)}%\" aria-label=\"${P.name(c)} in ${o.name}\"${cur(o)}></a>`; }).join('') + '</div>').join('') + '</figure>').join('');\n"
        "}\n"
        "// 11. a tint chosen in a row: its page from the top, so the gallery and the facts change in sight\n"
        "document.getElementById('p-rows').addEventListener('click', e => { if (e.target.closest('a')) setTimeout(() => scrollTo(0, 0), 0); });\n") + p.rest[b:]
    def lt_rows():
        out = ''
        for r, name, f, alt in (('hemisphere', 'Hemisphere', 'hemisphere-row.webp', 'Eight Hemispheres, one in each color'),
                                ('core', 'Core', 'core-row.webp', 'Eight Core lamps, lit, one in each color')):
            path = os.path.join(web.SITE, 'img', 'rc', f); w, h = Image.open(path).size
            out += _split_row(f'img/rc/{f}', w, h, alt, _row_cuts(path), [f'#{r}-{NAMES[k]}' for k in KEYS], [f'{name} in {CNAME[k]}' for k in KEYS])
        return out
    p.rest, n = re.subn(r'<div class="lt-rows">.*?</div>\n', lambda m: '<div class="lt-rows">' + lt_rows() + '</div>\n', p.rest, count=1, flags=re.S)
    assert n == 1, 'fix_4: /lighting rows'
    # --- 8. /lighting: each tile its lamp's picture, changing with the dots; the room sized so its names row is in sight
    def tile(m):
        kind, name = m.group(2), m.group(3); f = name.lower(); r = f
        src = f'img/rc/tile-{f}-ember.webp'; w, h = Image.open(os.path.join(web.SITE, src)).size
        return (f'<article class="lt-tile" data-p="{f}" data-name="{name}"><a class="lt-pic" href="#{r}-ember" data-carry="{r}" tabindex="-1" aria-hidden="true">'
                f'<img src="{src}" width="{w}" height="{h}" alt=""></a><div class="lt-body">{m.group(1)}</div></article>')
    p.rest, n = re.subn(r'<article class="lt-tile">(<p class="ft-kind">([\w ]+)</p><h2>(\w+)</h2>.*?)</article>', tile, p.rest, flags=re.S)
    assert n == 2, ('fix_4: /lighting tiles', n)
    js = """<script>(function () {      // /lighting's tiles: each its lamp in the tint chosen, and in the tint of a dot under the pointer or the focus
  const S = %s, tiles = document.querySelectorAll('.lt-tile[data-p]');
  const show = (t, slug) => { const im = t.querySelector('.lt-pic img'), s = `img/rc/tile-${t.dataset.p}-${slug}.webp`; if (!im.getAttribute('src').endsWith(s)) im.src = s; };
  const chosen = () => { let k = null; try { k = sessionStorage.getItem('earf-tint'); } catch (e) {} return S[k] || 'ember'; };
  const sync = () => tiles.forEach(t => show(t, chosen()));
  tiles.forEach(t => { t.querySelectorAll('.dots-row a').forEach(a => { const slug = a.getAttribute('href').split('-').pop();
    a.addEventListener('pointerenter', () => show(t, slug)); a.addEventListener('focus', () => show(t, slug)); });
    t.querySelector('.dots-row').addEventListener('pointerleave', () => show(t, chosen())); });
  addEventListener('hashchange', () => setTimeout(sync, 0)); sync();
})()</script>""" % json.dumps(NAMES)
    at = p.rest.index('</body>') if '</body>' in p.rest else len(p.rest)
    p.rest = p.rest[:at] + js + '\n' + p.rest[at:]
    # --- 12. /#mantle (and #hemisphere, #core) open the product in the tint chosen; the not-found view names the header's kinds
    p.sub("  if (LINE_OF[h] === 'speakers' || LINE_OF[h] === 'turntable') {",
          "  { const b = /^(hemisphere|core|mantle)$/.exec(h); if (b) { h = `${b[1]}-${BY[TINT].name.toLowerCase()}`; history.replaceState(null, '', '#' + h); } }\n"
          "  if (LINE_OF[h] === 'speakers' || LINE_OF[h] === 'turntable') {")
    p.sub('<a href="#speaker-ember" data-carry="speaker">Tropos</a><a href="#lighting">Lighting</a><a href="#mantle-ember" data-carry="mantle">Mantle</a>',
          '<a href="#speaker-ember" data-carry="speaker">Speakers</a><a href="#lighting">Lighting</a><a href="#mantle-ember" data-carry="mantle">Turntable</a>')
    p.css("""
/* the critics' list on 1B (the coordinator, 20 Nov 12:56) */
:root { --cap: max(300px, calc(100svh - 300px)) }
.cap { margin: 8px 0 0; min-height: 1.6em; font-size: 14px; line-height: 1.6; color: var(--muted) }
.cap a { white-space: nowrap }
@media (max-width: 700px) { .cap { min-height: 4.8em } }
/* one stage height per page at every size, the tall 4:5 picture's: each picture whole inside it; the arrows, counter and thumbnails never move */
.stage { height: min(var(--cap), calc(100cqw * 1.25)) !important }
/* the arrows at the picture's foot, beside the counter, off the product */
.gallery .nav { top: auto !important; bottom: 10px; translate: none !important; width: 36px !important; height: 36px !important }
.gallery .nav.next { right: 10px !important; left: auto !important }
.gallery .nav.prev { right: 52px !important; left: auto !important }
.gallery .count { right: 96px !important; bottom: 15px !important }
.stage .hint { text-transform: none !important; letter-spacing: 0 !important; font: 500 14px/1.2 var(--sans) !important }
.thumb.turn::after { font: 600 11px/1.3 var(--sans) !important }
/* rows of eight in two halves: whole on a desktop, two rows of four on a phone */
.row8.split { display: grid; grid-template-columns: 1fr 1fr; gap: 0 }
.row8.split .half { position: relative; overflow: hidden }
.row8.split .half img { width: 200%; max-width: none; height: auto; display: block; border-radius: 0 }
.row8.split .h1 img { margin-left: -100% }
@media (max-width: 700px) { .row8.split { grid-template-columns: minmax(0, 1fr); gap: 8px } }
/* /lighting: the tiles with their lamps; the room whole and its names row on the first screen */
.lt-tile { display: grid; grid-template-columns: minmax(0, 38%) minmax(0, 1fr); gap: 18px; align-items: start }
.lt-pic { display: block; border-radius: 4px; overflow: hidden } .lt-pic img { display: block; width: 100%; height: auto }
.lt-room img { width: auto !important; max-width: 100%; max-height: max(260px, calc(100svh - 330px)) !important; object-fit: contain !important }
@media (max-width: 860px) {
  .lt-tiles { order: -1 } .lt-grid { display: flex; flex-direction: column }
  .lt-tile { grid-template-columns: minmax(0, 30%) minmax(0, 1fr); gap: 12px; padding: 14px }
  .lt-tile h2 { margin: 2px 0 6px } .lt-tile .dots-row { margin-bottom: 8px }
  .lt-tile .dots-row { grid-template-columns: repeat(2, minmax(0, 1fr)) }
}
""")


def finish_4(web):
    """The 404 page: the header's names for its links, each in the tint chosen in this visit; an /s/ address with more after the
    product lands on the product."""
    f = os.path.join(web.SITE, '404.html'); s = open(f).read()
    for a, b in (('<a href="/tropos">Tropos</a>', '<a href="/tropos">Speakers</a>'), ('<a href="/mantle">Mantle</a>', '<a href="/mantle">Turntable</a>')):
        assert s.count(a) == 1, ('finish_4: 404', a); s = s.replace(a, b)
    s = s.replace('</body>', '<script>try { const n = %s[sessionStorage.getItem("earf-tint")]; if (n) { document.querySelector(\'a[href="/tropos"]\').href = "/tropos/" + n;'
                  ' document.querySelector(\'a[href="/mantle"]\').href = "/mantle/" + n; } } catch (e) {}</script></body>' % json.dumps(NAMES), 1)
    open(f, 'w').write(s)
    vj = os.path.join(web.SITE, 'vercel.json')
    v = json.load(open(vj))
    if not any(x['source'] == '/s/:page/(.+)' for x in v.get('redirects', [])):
        v.setdefault('redirects', []).append({'source': '/s/:page/(.+)', 'destination': '/s/:page', 'permanent': False})
    json.dump(v, open(vj, 'w'), indent=2)


# ---------------------------------------------------------------------------------------------------------------------
# The coordinator, 20 Nov 12:59 and 13:05: the eight Mantle pictures on the Tropos ground, and the words critic's leftovers
MANTLE_HOUSE = 'renders/2026-11-20/barkhorn/mantle-r48/mantle-house-{n}.png'     # r48-mantle-design 06228224, passed 12:59
MANTLE_HOUSE_COVER = 'renders/2026-11-20/barkhorn/mantle-r48/mantle-house-{n}-cover.png'     # r48-mantle-design b839428b, passed 14:36


def fix_5(p, web):
    from PIL import Image
    i, j, D = _data(p)
    # --- the Mantle alone on the Tropos ground: picture 1 of its gallery ("In the studio"), the spot-lit one second
    for k in KEYS:
        n = NAMES[k]
        im = Image.open(os.path.join(web.ROOT, MANTLE_HOUSE.format(n=n))).convert('RGB')
        assert im.size == (1600, 2000), ('fix_5: Mantle picture', n, im.size)
        big = im.resize((1200, 1500), Image.LANCZOS); big.save(os.path.join(web.IMG, 'rc', f'mantle-{n}-house.webp'), 'WEBP', quality=86, method=6)
        im.resize((336, 420), Image.LANCZOS).save(os.path.join(web.IMG, 'rc', f'mantle-{n}-house-th.webp'), 'WEBP', quality=82)
        im.resize((800, 1000), Image.LANCZOS).save(os.path.join(web.IMG, 'rc', f'tile-mantle-{n}.webp'), 'WEBP', quality=86, method=6)   # the tiles: the whole frame
        D['tt']['colours'][k]['views']['house'] = {'src': f'img/rc/mantle-{n}-house.webp', 'w': 1200, 'h': 1500, 'th': f'img/rc/mantle-{n}-house-th.webp'}
        # its cover on, same camera (r48-mantle-design b839428b, passed 14:36): replaces the gray-ground "With its cover"
        cv = Image.open(os.path.join(web.ROOT, MANTLE_HOUSE_COVER.format(n=n))).convert('RGB')
        assert cv.size == (1600, 2000), ('fix_5: Mantle cover picture', n, cv.size)
        cv.resize((1200, 1500), Image.LANCZOS).save(os.path.join(web.IMG, 'rc', f'mantle-{n}-house-cover.webp'), 'WEBP', quality=86, method=6)
        cv.resize((336, 420), Image.LANCZOS).save(os.path.join(web.IMG, 'rc', f'mantle-{n}-house-cover-th.webp'), 'WEBP', quality=82)
        D['tt']['colours'][k]['views']['cover'] = {'src': f'img/rc/mantle-{n}-house-cover.webp', 'w': 1200, 'h': 1500, 'th': f'img/rc/mantle-{n}-house-cover-th.webp'}
    # the lamp tiles from the real 4:5 pictures (the coordinator 13:56, B1): the masters at 800 x 1000, grain as the gallery, nothing added
    import site_v2
    for f, src in (('hemisphere', 'hemisphere-{n}-direct'), ('core', 'core-{n}')):
        for k in KEYS:
            n = NAMES[k]
            im = Image.open(os.path.join(web.ROOT, site_v2.LAMP_FINAL.format(f=src.format(n=n)))).convert('RGB')
            assert abs(im.width / im.height - 0.8) < 1e-3, ('fix_5: lamp tile not 4:5', f, n, im.size)
            _grain_save(im.resize((800, 1000), Image.LANCZOS), os.path.join(web.IMG, 'rc', f'tile-{f}-{n}.webp'))
    # the dead lines out of the page data: the lamps' old lines become their pages' sentences
    D['lamps']['dome']['line'] = 'A pendant in cast acrylic. The shade comes off with a quarter turn.'
    D['lamps']['orb']['line'] = 'A table lamp in cast acrylic. Cordless. About five hours a charge.'
    # the Core's height, weight and touch surface (r32-lamps-final 7fa9e68a FACTS.md; the coordinator 15:42): the old figures out of the page data too
    fx = {'Size': '160 mm ball, 187 mm tall, base 150 mm across', 'Weight': 'About 1.4 kg with its cells', 'Control': 'Touch the top of the base: tap to switch, hold to dim'}
    D['lamps']['orb']['facts'] = [[a, fx.get(a, b)] for a, b in D['lamps']['orb']['facts']]
    i, j, _ = _data(p)
    p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
    p.sub('"turntable": ["studio", "cover", "bar"]', '"turntable": ["house", "cover", "studio", "bar"]')     # cover off, then on, then under a spot
    p.sub("const TT_VIEWS = [['studio', 'In the studio', c => `${D.tt.name} in ${c.name}.`],",
          "const TT_VIEWS = [['house', 'In the studio', c => `${D.tt.name} in ${c.name}.`], ['studio', 'Under a spot', c => `${D.tt.name} in ${c.name}, under a spot.`],")
    p.sub('turntable: {"studio": "",', 'turntable: {"house": "", "studio": "",')
    # the Mantle tile on the same light card as the Tropos tile (home row and the foot's family row)
    p.sub('<a class="ftile ft-mantle" href="#mantle-ember" data-p="mantle"><span class="ft-pic" style="background:#74706C">',
          '<a class="ftile ft-mantle" href="#mantle-ember" data-p="mantle"><span class="ft-pic" style="background:#E9E5DC">')
    p.rest, n = re.subn(r'("route":"mantle","name":"Mantle","kind":"Turntable","w":\d+,"h":\d+,"ground":")#[0-9A-Fa-f]{6}', r'\g<1>#E9E5DC', p.rest)
    assert n == 1, ('fix_5: the foot row\'s Mantle ground', n)
    # --- words: How it lights, by removal alone; the old /tropos view's numbers and figures
    p.sub("Twenty-four LEDs, all facing away from you, so there&rsquo;s no bright point to look into.",
          "Twenty-four LEDs face away from you, so there&rsquo;s no bright point to look into.")
    p.rest, n = re.subn(r'<p class="num">Tropos 0\d</p>', '', p.rest)
    assert n == 8, ('fix_5: Tropos 0N', n)
    S_ = r'(?:\s|&nbsp;|\u00a0)'
    for a, b in ((r'About 73' + S_ + r'kg; about 64' + S_ + r'kg with the horn lifted off \(modeled\)', 'About 75&nbsp;kg (165&nbsp;lb) each'),
                 (r'428(' + S_ + r')mm overall', r'442\1mm overall')):
        n = len(re.findall(a, p.head)) + len(re.findall(a, p.rest))
        assert n, ('fix_5: figure', a)
        p.head = re.sub(a, b, p.head); p.rest = re.sub(a, b, p.rest)
    # --- the sentence under the name wraps without a lone word; "See Hemisphere" on one line at every width
    p.css("""
/* the coordinator 13:05 */
.buy .line { text-wrap: pretty }
.ft-btn { white-space: nowrap }
@media (max-width: 380px) { .ft-btn { padding: 0 12px; gap: 6px } .ft-btn .arr { display: none } }
@media (min-width: 761px) and (max-width: 860px) { .ft-btn { padding: 0 12px; font-size: 14px } }
""")


def finish_5(web):
    """One kind word for Tropos ("horn speaker"); the /s/ pages' structured data says what their description says; the
    retired /s/color pages carry their Tropos's title, words and card; /lighting made to order; /hemisphere and /core forward."""
    import glob, html as H
    for f in glob.glob(os.path.join(web.SITE, '**', '*.html'), recursive=True):
        s = open(f).read(); t = s.replace('horn loudspeaker', 'horn speaker').replace('Horn loudspeaker', 'Horn speaker')
        if f.endswith('lighting.html'):
            t = t.replace('in the eight colors. In development."', 'in the eight colors. In development. Made to order."')
        if t != s:
            open(f, 'w').write(t)
    for f in glob.glob(os.path.join(web.SITE, 's', '*.html')):
        s = open(f).read()
        m = re.search(r'<meta name="description" content="([^"]*)"', s)
        if m:
            desc = json.dumps(H.unescape(m.group(1)))[1:-1]
            s = re.sub(r'("@type":"Product".*?"description":")(?:[^"\\]|\\.)*(")', lambda x: x.group(1) + desc + x.group(2), s, count=1, flags=re.S)
            open(f, 'w').write(s)
    for k in KEYS:
        n = NAMES[k]; sp = os.path.join(web.SITE, 's', f'speaker-{n}.html'); cp = os.path.join(web.SITE, 's', f'color-{n}.html')
        if os.path.exists(sp) and os.path.exists(cp):
            open(cp, 'w').write(open(sp).read())          # it forwards to that Tropos: its title, words and card
    vj = os.path.join(web.SITE, 'vercel.json')
    v = json.load(open(vj))
    for src, dst in (('/hemisphere', '/hemisphere/ember'), ('/core', '/core/ember')):
        if not any(x['source'] == src for x in v.get('redirects', [])):
            v.setdefault('redirects', []).append({'source': src, 'destination': dst, 'permanent': True})
    json.dump(v, open(vj, 'w'), indent=2)


# ---------------------------------------------------------------------------------------------------------------------
# The clicks critic on 1A (the coordinator, 20 Nov 13:24)
def fix_6(p, web):
    # --- 3. a header item pressed on its own page adds no step to Back and goes to the top
    p.sub("const navAt = which =>",
          "addEventListener('click', e => { const a = e.target.closest && e.target.closest('header a[href^=\"#\"], footer a[href^=\"#\"]');\n"
          "  if (!a || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;\n"
          "  const h = a.getAttribute('href').slice(1), here = last === 'home' ? (h === 'top' || h === '') : last === 'line-lighting' ? h === 'lighting' : last === h;\n"
          "  if (!here) return; e.preventDefault(); e.stopPropagation(); if (typeof menuOpen === 'function') menuOpen(false); scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); }, true);\n"
          "const navAt = which =>")
    p.css("""
/* the hero in a short wide window (a phone held sideways, 960 x 600): the line and buttons stay over the picture on the first
   screen, and the Hemisphere dot, which would lie on them, steps aside */
@media (min-aspect-ratio: 1/1) and (max-width: 960px) and (max-height: 640px) { .hs-hero .hs-pt[href^="#hemisphere"] { display: none } }
/* from 961 to 1060 px the name "Tropos in Acid" would touch "See the colors" just above it: it opens a little lower */
@media (min-width: 961px) and (max-width: 1060px) { .hs-hero .hs-pt.hs-w[href^="#speaker"] .hs-label { translate: 0 14px } }
""")


# ---------------------------------------------------------------------------------------------------------------------
# The last critic pass, push C (the coordinator, 20 Nov 13:56)
SIZEL = {'speaker': '51 in (1295 mm) tall', 'dome': '7.9 in (200 mm) across', 'orb': '7.4 in (187 mm) tall', 'turntable': '17.7 in (450 mm) wide'}


def fix_7(p, web):
    from PIL import Image
    # C2: Left and Right always step through the pictures; the horn turns by keys only while the picture itself has focus
    p.sub("  if (!focus && view === 'turn' && (e.key === 'ArrowRight' || e.key === 'ArrowLeft')) {",
          "  if (!focus && view === 'turn' && document.activeElement === stage && (e.key === 'ArrowRight' || e.key === 'ArrowLeft')) {")
    # C6: Enter on the picture does what a click does; a dot chosen with the keys keeps the focus
    p.sub("stage.addEventListener('keydown', e => keys(e, false));",
          "stage.addEventListener('keydown', e => keys(e, false));\n"
          "stage.addEventListener('keydown', e => { if (e.key !== 'Enter' || view === 'turn' || view === 'spin') return; const s = src(BY[cur], view); if (s && s.src) { e.preventDefault(); window.open(s.src, '_blank', 'noopener'); } });")
    p.sub("  WANT = view; history.replaceState(null, '', location.pathname + h); dispatchEvent(new HashChangeEvent('hashchange')); }, true);",
          "  WANT = view; history.replaceState(null, '', location.pathname + h); dispatchEvent(new HashChangeEvent('hashchange'));\n"
          "  const f = document.querySelector(`#swatches a[href=\"${h}\"]`); if (f) f.focus({ preventScroll: true }); }, true);")
    # C8: one size line under the sentence, inches first
    p.sub('<p class="line" id="p-line"></p>', '<p class="line" id="p-line"></p>\n        <p class="sizel" id="p-size"></p>')
    p.sub("function renderSpec(P, c) {", f"const SIZEL = {json.dumps(SIZEL)};\nfunction renderSpec(P, c) {{ document.getElementById('p-size').textContent = SIZEL[P.id] || '';")
    # C7: the home's family row says what the gallery says
    p.rest, n = re.subn(r'(<section class="band mk" id="family">.*?<div class="mk-wide ftiles">.*?</a></div>)(</section>)',
                        r'\1<div class="wrap"><p class="render-note">Pictures are renders. Nothing is built yet.</p></div>\2', p.rest, count=1, flags=re.S)
    assert n == 1, 'fix_7: the family note'
    # C9: lazy where it was lost; the place tiles at the slot's size
    p.sub('<figure class="lt-room"><img src="img/rc/bar-pendants.webp"', '<figure class="lt-room"><img loading="lazy" src="img/rc/bar-pendants.webp"')
    p.rest, n = re.subn(r'(<a class="lt-pic"[^>]*><img )', r'\1loading="lazy" ', p.rest)
    assert n == 2, ('fix_7: lt-pic lazy', n)
    for k in KEYS:
        big = os.path.join(web.IMG, 'rc', f'{k}-habitat.webp')
        im = Image.open(big); assert im.size == (1200, 1500), ('fix_7: habitat', k, im.size)
        im.convert('RGB').resize((600, 750), Image.LANCZOS).save(os.path.join(web.IMG, 'rc', f'{k}-habitat-600.webp'), 'WEBP', quality=86, method=6)
        p.rest, n = re.subn(r'(<a class="place" href="#speaker-%s/out"><img src="img/rc/%s-habitat\.webp" width="1200" height="1500")' % (NAMES[k], k),
                            r'\1 srcset="img/rc/%s-habitat-600.webp 600w, img/rc/%s-habitat.webp 1200w" sizes="(max-width: 700px) 76vw, 25vw"' % (k, k), p.rest)
        assert n == 1, ('fix_7: place srcset', k, n)
    p.css("""
/* the last critic pass, push C (the coordinator, 13:56) */
.sizel { margin: -8px 0 0; font-size: 15px; color: var(--muted) }
.sizel:empty { display: none }
.share-note { min-height: 1.5em; margin: 0 } .share-note:empty { display: block !important }
/* C6: focus is its own ring, outside the chosen one, and shows on the chosen dot too */
.swatches a:focus { outline: none } .swatches a:focus-visible { box-shadow: 0 0 0 4px var(--page), 0 0 0 6px #1A5FD0 }
.swatches a[aria-current="true"]:focus-visible { box-shadow: 0 0 0 4px var(--page), 0 0 0 6px #1A5FD0 }
/* C14: the dots four and four where one line does not fit beside the picture */
@media (min-width: 861px) and (max-width: 1260px) { .swatches { display: grid !important; grid-template-columns: repeat(4, 44px); gap: 4px 8px !important } }
/* C12: the chips four and four where one line does not fit */
@media (min-width: 480px) and (max-width: 1000px) { #family .tint-pick { display: grid !important; grid-template-columns: repeat(4, max-content); justify-content: start } }
/* C11: on an upright tablet the hero's picture is capped so its line and buttons show */
@media (max-aspect-ratio: 1/1) and (min-width: 560px) { .hs-hero .hero-photo { width: min(100%, calc((100svh - 330px) * 0.8)); margin-inline: auto } }
/* C10: /lighting, the room and two compact tiles filling the row, both whole on the first screen */
@media (min-width: 861px) {
  .lt-grid { grid-template-columns: auto minmax(0, 1fr) !important; gap: 24px }
  .lt-tile { grid-template-columns: minmax(0, 18%) minmax(0, 1fr); padding: 16px 18px; gap: 18px }
  .lt-body { display: grid; grid-template-columns: minmax(0, 1fr) auto; column-gap: 16px; align-items: center }
  .lt-body .ft-kind { grid-column: 1 / -1; margin: 0 } .lt-body h2 { margin: 0 } .lt-body .cta-btn { grid-column: 2; grid-row: 2 }
  .lt-body .dots-row { grid-column: 1 / -1; margin: 8px 0 0 !important; grid-template-columns: repeat(auto-fill, minmax(96px, 1fr)) }
}
@media (max-width: 700px) {
  /* C3: one row of thumbnails that scrolls sideways */
  .thumbs { flex-wrap: nowrap !important; overflow-x: auto !important; scrollbar-width: none }
  /* C4: less air above the picture, so the name is on the first screen */
  .pdp { padding-top: 0 !important } #pdp .crumbs { margin: 0 } .cap { min-height: 3.2em }
  .stage { height: min(var(--cap), calc(100cqw * 1.1)) !important }
  /* C14: the arrows 44 px */
  .gallery .nav { width: 44px !important; height: 44px !important } .gallery .nav.prev { right: 62px !important } .gallery .count { right: 114px !important; bottom: 19px !important }
}
/* C14: a phone held sideways, the picture beside the words */
@media (orientation: landscape) and (max-height: 520px) and (max-width: 960px) {
  .pdp { grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr) !important; gap: 20px !important }
  .pcol > .spec2 { grid-column: 1 / -1 }
  .buy { position: static !important }
}
/* push C2 (the coordinator, 15:06) */
/* C2-1: a full-bleed picture (Tropos "Out") stands whole in the stage like every other: its own proportions, inside the box */
.stage .fill { display: contents !important }
.stage .fill img { width: min(100cqw, calc(100cqh * var(--sar, 0.8))) !important; height: auto !important; aspect-ratio: var(--sar, 0.8);
  object-fit: contain !important; max-width: 100%; max-height: 100% }
/* C2-2: the names row is one line, scrolling sideways inside its own box; its height is kept under every picture */
.cap { height: 1.6em !important; min-height: 0 !important; line-height: 1.6 !important; white-space: nowrap; overflow-x: auto; overflow-y: hidden;
  scrollbar-width: none; overscroll-behavior-x: contain }
.cap::-webkit-scrollbar { display: none }
.cap[hidden] { display: block !important; visibility: hidden }
.lt-room .names { white-space: nowrap; overflow-x: auto; overflow-y: hidden; scrollbar-width: none; line-height: 1.6 }
.lt-room .names::-webkit-scrollbar { display: none }
.names a, .cap a { padding-block: 0 !important; display: inline !important }
/* C2-3: the chosen thumbnail's whole frame inside the sideways row */
@media (max-width: 700px) { .thumbs { padding: 5px !important; margin: -5px -5px 0 !important; scroll-padding-inline: 5px } }
/* C2-4: on an upright tablet the capped hero picture is centered, and the headline and its line align with it */
@media (max-aspect-ratio: 1/1) and (min-width: 560px) {
  .hs-hero .hero-pic > .hero-photo { margin-left: auto !important; margin-right: auto !important; align-self: center }
  .hs-hero .hero-title .wrap, .hs-hero .hero-more .wrap { width: min(100%, calc((100svh - 330px) * 0.8)); max-width: none !important;
    margin-left: auto !important; margin-right: auto !important; padding-left: 0 !important; padding-right: 0 !important; box-sizing: border-box }
}
""")


# ---------------------------------------------------------------------------------------------------------------------
# Prepared on r47 while push C is under the critics (the coordinator, 20 Nov 14:33)
DIMS = {'speaker': ('tropos', 'Tropos, front and side, with its height, width and depth in inches and millimeters'),
        'turntable': ('mantle', 'Mantle from above and from the front, with its cover off and on, with its sizes in inches and millimeters'),
        'dome': ('hemisphere', 'Hemisphere from the side, hung from its canopy, with its sizes and its drop in inches and millimeters'),
        'orb': ('core', 'Core from the front, with its ball, its base and its height in inches and millimeters')}


def fix_8(p, web):
    """The dimension drawings with Specifications: a picture the visitor can enlarge (the drawing's own SVG opens on a click)."""
    from PIL import Image
    import shutil
    dims = {}
    for pid, (f, alt) in DIMS.items():
        src = os.path.join(web.ROOT, 'spinoffs', 'barkhorn', 'dims-site', f'{f}-dims')
        im = Image.open(src + '.png').convert('L')
        im.save(os.path.join(web.IMG, 'rc', f'dims-{f}.webp'), 'WEBP', lossless=True, method=6)
        shutil.copy(src + '.svg', os.path.join(web.IMG, 'rc', f'dims-{f}.svg'))
        dims[pid] = {'src': f'img/rc/dims-{f}.webp', 'svg': f'img/rc/dims-{f}.svg', 'w': im.width, 'h': im.height, 'alt': alt}
    p.sub('<h2 id="p-spec-h">Specifications</h2>',
          '<h2 id="p-spec-h">Specifications</h2><figure class="dims" id="p-dims" hidden><a target="_blank" rel="noopener"><img loading="lazy" alt=""></a></figure>')
    p.sub("function renderSpec(P, c) {",
          f"const DIMS = {json.dumps(dims)};\n"
          "function renderDims(P) { const f = document.getElementById('p-dims'), d = DIMS[P.id]; f.hidden = !d; if (!d) return;\n"
          "  const a = f.querySelector('a'), i = f.querySelector('img'); a.href = d.svg; a.setAttribute('aria-label', d.alt + ' (opens the drawing)');\n"
          "  if (i.getAttribute('src') !== d.src) { i.src = d.src; i.width = d.w; i.height = d.h; i.alt = d.alt; } }\n"
          "function renderSpec(P, c) { renderDims(P);")
    p.css("""
.dims { margin: 4px 0 24px } .dims a { display: inline-block; max-width: 100%; cursor: zoom-in }
.dims img { display: block; width: auto; max-width: 100%; height: auto; max-height: min(78svh, 720px); background: #fff; border-radius: 4px }
""")


# the lamps on the light ground: one switch, the owner's (off: the tiles and picture 1 show the lamp off; on: lit)
LAMP_LEAD = 'off'
LAMP_HOUSE = 'renders/2026-11-20/barkhorn/lamp-site/house/{f}-{n}-{state}.png'     # r32-lamps-final, from 2026-11-20
HOUSE_LABEL = {'off': 'Off', 'on': 'Lit'}


def fix_9(p, web):
    """Per lamp: when all eight tints have their off and lit pictures on the light ground, the tile (home row, the foot's
    family row, /lighting) is the LAMP_LEAD one and the gallery opens on the pair, LAMP_LEAD first. A lamp with any tint
    missing keeps today's files everywhere: a row never mixes grounds within one product."""
    from PIL import Image
    i, j, D = _data(p)
    ready = []
    for pid, f in (('dome', 'hemisphere'), ('orb', 'core')):
        paths = {(k, st): os.path.join(web.ROOT, LAMP_HOUSE.format(f=f, n=NAMES[k], state=st)) for k in KEYS for st in ('off', 'on')}
        if not all(os.path.exists(x) for x in paths.values()):
            continue
        ready.append(pid)
        other = 'on' if LAMP_LEAD == 'off' else 'off'
        for k in KEYS:
            n = NAMES[k]; views = D['lamps'][pid]['colours'][k]['views']
            for st in ('off', 'on'):
                im = Image.open(paths[(k, st)]).convert('RGB')
                assert abs(im.width / im.height - 0.8) < 1e-3, ('fix_9: not 4:5', f, n, st, im.size)
                im.resize((1200, 1500), Image.LANCZOS).save(os.path.join(web.IMG, 'rc', f'{f}-{n}-house-{st}.webp'), 'WEBP', quality=86, method=6)
                im.resize((336, 420), Image.LANCZOS).save(os.path.join(web.IMG, 'rc', f'{f}-{n}-house-{st}-th.webp'), 'WEBP', quality=82)
                views[f'house-{st}'] = {'src': f'img/rc/{f}-{n}-house-{st}.webp', 'w': 1200, 'h': 1500, 'th': f'img/rc/{f}-{n}-house-{st}-th.webp'}
                if st == LAMP_LEAD:
                    im.resize((800, 1000), Image.LANCZOS).save(os.path.join(web.IMG, 'rc', f'tile-{f}-{n}.webp'), 'WEBP', quality=86, method=6)
        name = D['lamps'][pid]['name']
        # the pair first in the gallery, the lead one first; their labels; the dark-room pictures say where they are
        a = p.rest.index(f'const LAMP_VIEWS = {{'); b = p.rest.index(f'{pid}: [', a) + len(f'{pid}: [')
        p.rest = (p.rest[:b] + f"['house-{LAMP_LEAD}', '{HOUSE_LABEL[LAMP_LEAD]}', c => `{name} in ${{c.name}}, {'switched off' if LAMP_LEAD == 'off' else 'lit'}.`], "
                  f"['house-{other}', '{HOUSE_LABEL[other]}', c => `{name} in ${{c.name}}, {'lit' if other == 'on' else 'switched off'}.`], " + p.rest[b:])
        for old, new in (("['hero', 'Lit',", "['hero', 'In the dark',"), ("['off', 'Off',", "['off', 'Off, in the dark',")):
            c_ = p.rest.find(old, b, p.rest.index('],', b) if False else len(p.rest))
            e_ = p.rest.find(']],', b)          # the end of this lamp's list
            if 0 <= c_ < e_:
                p.rest = p.rest[:c_] + new + p.rest[c_ + len(old):]
        vo = re.search(r'"%s": \[([^\]]*)\]' % pid, p.rest[p.rest.index('const VORDER = '):])
        at = p.rest.index('const VORDER = ') + vo.start(1)
        p.rest = p.rest[:at] + f'"house-{LAMP_LEAD}", "house-{other}", ' + p.rest[at:]
        cap_at = p.rest.index('const CAPS = '); k_at = p.rest.index(f'{pid}: {{', cap_at) + len(f'{pid}: {{')
        p.rest = p.rest[:k_at] + '"house-off": "", "house-on": "", ' + p.rest[k_at:]
        # the tiles stand on the Tropos tile's light card
        fam = re.search(r'(<a class="ftile ft-%s"[^>]*><span class="ft-pic" style="background:)#[0-9A-Fa-f]{6}' % f, p.rest)
        assert fam, ('fix_9: family tile', f)
        p.rest = p.rest[:fam.start()] + fam.group(1) + '#E9E5DC' + p.rest[fam.end():]
        p.rest, n_ = re.subn(r'("route":"%s","name":"%s","kind":"[^"]+","w":\d+,"h":\d+,"ground":")#[0-9A-Fa-f]{6}' % (f, name), r'\g<1>#E9E5DC', p.rest)
        assert n_ == 1, ('fix_9: the foot row', f, n_)
    if ready:
        i, j, _ = _data(p)
        p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
    print('fix_9: lamps on the light ground:', ready or 'none yet (a tint missing)')


# ---------------------------------------------------------------------------------------------------------------------
# Push C3: the critics' smaller items on push C (the coordinator, 20 Nov 15:42); items 1-3 are in SPEC above
def fix_10(p, web):
    # 6. "Shown in Ember." beside the picture, in the line under it, never across its edge
    p.sub("  if (s.shown && !NAMEROWS[(s.src || '').split('/').pop()]) stage.appendChild(el('span', { class: 'tag' }, `Shown in ${BY[s.shown].name}.`));\n", "")
    p.sub("    const nr = NAMEROWS[(s.src || '').split('/').pop()]; if (nr) { e.innerHTML = nr; e.hidden = false; } }",
          "    const nr = NAMEROWS[(s.src || '').split('/').pop()]; if (nr) { e.innerHTML = nr; e.hidden = false; }\n"
          "    else if (s.shown && !e.textContent) { e.textContent = `Shown in ${BY[s.shown].name}.`; e.hidden = false; } }")
    # 13. the arrows and the counter at the picture's own foot (an upright picture is narrower than the stage)
    p.sub("  document.getElementById('g-count').textContent",
          "  pin();\n  document.getElementById('g-count').textContent")
    p.sub("function go(d, focus) {",
          "function pin() { const st = stage.getBoundingClientRect(), pw = Math.min(st.width, st.height * 0.8);   // the 4:5 picture's foot: one place for every picture\n"
          "  stage.parentElement.style.setProperty('--pin', Math.max(0, (st.width - pw) / 2).toFixed(1) + 'px'); }\n"
          "new ResizeObserver(() => { if (cur) pin(); }).observe(stage);\n"
          "function go(d, focus) {")
    # 7. the canonical address follows the color
    p.sub("setTint(k); renderRows(P, c);",
          "setTint(k); renderRows(P, c);\n"
          "  { let l = document.querySelector('link[rel=\"canonical\"]'); if (!l) { l = document.createElement('link'); l.rel = 'canonical'; document.head.appendChild(l); }\n"
          "    l.href = 'https://www.earf.world' + productPath(); }")
    # 4. Space chooses a dot as Enter does, without scrolling the page
    p.sub("thumbs.addEventListener('keydown', e => keys(e, true));",
          "thumbs.addEventListener('keydown', e => keys(e, true));\n"
          "document.addEventListener('keydown', e => { if (e.key !== ' ' && e.key !== 'Spacebar') return; const a = e.target.closest && e.target.closest('#swatches a'); if (!a) return; e.preventDefault(); a.click(); });")
    # 11. a place tile leaves a clean address (/tropos/<tint>) with its view kept; Copy link from there opens the same picture
    p.sub("  { const v = /^([a-z]+-[a-z]+)\\/([a-z-]+)$/.exec(h); if (v) { h = v[1]; WANT = VIEWKEY[v[2]] || v[2]; } }",
          "  { const v = /^([a-z]+-[a-z]+)\\/([a-z-]+)$/.exec(h); if (v) { h = v[1]; WANT = VIEWKEY[v[2]] || v[2];\n"
          "      const r = /^(speaker|hemisphere|core|mantle)-([a-z]+)$/.exec(h); if (r) history.replaceState(null, '', (r[1] === 'speaker' ? '/tropos/' : `/${r[1]}/`) + r[2]); } }\n"
          "  { const q = new URLSearchParams(location.search).get('view'); if (q && !WANT) { WANT = VIEWKEY[q] || q; } }")
    p.sub("const url = location.origin + productPath(), note", "const url = location.origin + productPath() + (view === 'habitat' ? '?view=out' : ''), note")
    # 8. the home's Write to us: room kept for its note, which says what beside the ask says
    p.sub("const done = () => { note.textContent = 'Copied.'; };", "const done = () => { note.textContent = 'Address copied.'; };")
    p.sub('<div class="wrap"><p class="render-note">Pictures are renders. Nothing is built yet.</p></div>',
          '<div class="mk-wide"><p class="render-note">Pictures are renders. Nothing is built yet.</p></div>')
    # 12. a phone's first load: no opening film (its four frame sheets are about 1 MB); the hidden block's icons lazy
    _sub_any(p, "if (location.pathname.replace(/index\\.html$/, '') !== '/' || location.hash || seen",
             "if (location.pathname.replace(/index\\.html$/, '') !== '/' || location.hash || seen || matchMedia('(max-width: 700px)').matches")
    p.rest, n = re.subn(r'<img class="ic only-light " (?![^>]*loading=)', '<img class="ic only-light " loading="lazy" ', p.rest)
    assert n >= 1, ('fix_10: icons', n)
    p.css("""
/* push C3 (the coordinator, 15:42) */
/* 4: the dots one row where it fits, else four and four; focus outside the chosen ring, both shown, apart from the neighbors */
.buy { container-type: inline-size }
.swatches { display: flex !important; flex-wrap: wrap; gap: 8px !important }
@container (max-width: 407px) { .swatches { display: grid !important; grid-template-columns: repeat(4, 44px); gap: 6px 10px !important } }
.swatches a:focus:not(:focus-visible) { outline: none }
.swatches a:focus { outline: none }
.swatches a[aria-current="true"], .swatches a[aria-current="true"]:focus { outline: 2px solid var(--ink) !important; outline-offset: 0 !important }
.swatches a:focus-visible { box-shadow: 0 0 0 3px var(--page), 0 0 0 5px #1A5FD0 !important }
/* 5: a short phone keeps the name above the ask bar */
/* 8: the renders line under the family row from the row's own edge; the Write to us note keeps its room */
#family .render-note { margin: 12px 0 0 }
#copy-note { display: block !important; min-height: 1.5em }
/* 10: /lighting, the eight named dots four and four at every width, each name under its dot; the names row no wider than its picture */
.lt-tile .dots-row, .lt-body .dots-row { display: grid !important; grid-template-columns: repeat(4, minmax(0, 1fr)) !important; gap: 4px 6px !important }
.lt-tile .dots-row a { flex-direction: column; justify-content: center; gap: 2px !important; min-height: 52px; font-size: 12px; border-radius: 8px }
.lt-tile .dots-row .coin-dot { width: 28px !important; height: 28px !important }
@media (max-width: 860px) { .lt-room .names { width: 0; min-width: 100% } }
@media (min-width: 861px) { .lt-room .names { overflow: visible !important; width: auto } .lt-room { min-width: 0 } }
/* 13: one counter width; the arrows and counter at the picture's own foot; the breadcrumb's focus clear of the slash */
.gallery .count { min-width: 52px; text-align: center; box-sizing: border-box; font-variant-numeric: tabular-nums }
.gallery .nav.next { right: calc(var(--pin, 0px) + 10px) !important }
.gallery .nav.prev { right: calc(var(--pin, 0px) + 54px) !important }
.gallery .count { right: calc(var(--pin, 0px) + 98px) !important }
@media (max-width: 700px) {
  .gallery .nav.prev { right: calc(var(--pin, 0px) + 62px) !important } .gallery .count { right: calc(var(--pin, 0px) + 114px) !important }
}
.crumbs a { margin-inline: 3px } .crumbs a:first-child { margin-left: 0 } .crumbs a:focus-visible { outline-offset: 1px }
/* 9: the hero's line and both buttons on the first screen of a phone too; in a short wide window the buttons side by side, clear of the pendants */
@media (max-aspect-ratio: 1/1) and (max-width: 559px) {
  .hs-hero .hero-pic > .hero-photo { width: min(100%, calc((100svh - 290px) * 0.8)); margin-left: auto !important; margin-right: auto !important; align-self: center }
}
@media (min-aspect-ratio: 1/1) and (max-width: 960px) and (max-height: 640px) {
  .hs-hero .hero-more { left: 0 !important; right: 0 !important; margin-inline: auto !important; width: min(92vw, 640px) !important; max-width: none !important }
  .hs-hero .hero-more .wrap { width: auto !important; max-width: none !important; text-align: center }
  .hs-hero .hero-sub { max-width: none !important; margin-bottom: 10px !important }
  .hs-hero .hero-cta { flex-wrap: nowrap !important; justify-content: center; gap: 10px }
}
""")


def finish_10(web):
    """The static pages keep a ?view on their way to their own fragment (a place tile's copied link opens its picture)."""
    import glob
    for f in glob.glob(os.path.join(web.SITE, '**', '*.html'), recursive=True):
        s = open(f).read()
        t = s.replace('history.replaceState(null, "", location.pathname + "#', 'history.replaceState(null, "", location.pathname + location.search + "#')
        if t != s:
            open(f, 'w').write(t)


# ---------------------------------------------------------------------------------------------------------------------
# Push C4: the critics' faults on C3 (the coordinator, 20 Nov 18:43); the rows are in SPEC above
def fix_11(p, web):
    # 1. the arrows and the counter in a strip under the stage, at its right edge, on the names row's line: never on a picture
    p.sub("  pin();\n  document.getElementById('g-count').textContent", "  document.getElementById('g-count').textContent")
    # 5. every figure on one line with its unit
    p.sub("const fillSpec = (t, c) => t.replace(",
          "const keepUnits = t => t.replace(/(\\d) (in|mm|lb|kg|ft|m|W|V|Wh|K|lm|lux|dB|Hz|kHz|rpm)\\b/g, '$1\\u00a0$2').replace(/\\b(in|mm|lb|kg|ft|m) \\(/g, '$1\\u00a0(')\n"
          "  .replace(/(\\d) x (\\d)/g, '$1\\u00a0x\\u00a0$2');\n"
          "const fillSpec = (t, c) => keepUnits(t).replace(")
    # 15, 16: the first frame sheet fetched once; a phone held sideways is a phone (no opening film)
    _sub_any(p, "{ const l = document.createElement('link'); l.rel = 'preload'; l.as = 'image'; l.href = 'img/globe-frames-0.webp'; document.head.appendChild(l); }", "")
    _sub_any(p, "|| matchMedia('(max-width: 700px)').matches", "|| matchMedia('(max-width: 700px), (max-height: 500px)').matches")
    p.css("""
/* push C4 (the coordinator, 18:43) */
/* 1: the strip under the stage: the names row at the left, the counter and the arrows at the right; one place for every picture */
.gallery .frame { padding-bottom: 44px }
.gallery .cap { margin-top: -44px !important; height: 44px !important; line-height: 44px !important; padding-right: 160px; position: relative; z-index: 1 }
.gallery .nav { top: auto !important; bottom: 0 !important; translate: none !important; width: 40px !important; height: 40px !important;
  background: transparent !important; color: var(--ink) !important; box-shadow: inset 0 0 0 1px var(--rule) !important; z-index: 2 }
.gallery .nav:hover { box-shadow: inset 0 0 0 1.5px var(--ink) !important }
.gallery .nav.next { right: 0 !important; left: auto !important }
.gallery .nav.prev { right: 48px !important; left: auto !important }
.gallery .count { bottom: 10px !important; right: 96px !important; background: transparent !important; color: var(--muted) !important; z-index: 2 }
@media (max-width: 700px) {
  .gallery .nav { width: 44px !important; height: 44px !important } .gallery .nav.prev { right: 52px !important } .gallery .count { right: 100px !important; bottom: 11px !important }
  .gallery .cap { padding-right: 156px }
  .pdp { row-gap: 14px !important } #pdp .gallery { gap: 8px !important } #pdp .render-note { margin: 0 !important }
}
:root { --cap: max(300px, calc(100svh - 322px)) }
@media (max-width: 860px) { :root { --cap: calc(100svh - 222px) } }
/* 5: a visible gap between a label and its value */
.spec2 .facts { column-gap: 16px } .spec2 .facts dt { overflow-wrap: anywhere; padding-right: 6px }
/* 6: a focused dot never under the ask bar */
@media (max-width: 700px) { html { scroll-padding-bottom: 84px } }
/* 17: the home chips: four to a row, or three, never one alone */
@media (max-width: 479px) and (min-width: 400px) { #family .tint-pick { display: grid !important; grid-template-columns: repeat(4, max-content); gap: 8px } }
@media (max-width: 399px) { #family .tint-pick { display: grid !important; grid-template-columns: repeat(3, max-content); gap: 8px } }
/* 18, 19: the Copy address note one height, empty or filled; its focus box for the keyboard only */
#copy-note { display: block !important; height: 22px !important; min-height: 0 !important; line-height: 22px !important; overflow: hidden }
#copy:focus:not(:focus-visible), .btn:focus:not(:focus-visible), .ic-btn:focus:not(:focus-visible) { outline: none !important; box-shadow: none }
""")


# ---------------------------------------------------------------------------------------------------------------------
# Push C5: two of the owner's decisions (24 Nov, "go with the research and critics"; the coordinator 03:58)
MOOD = ['The last light of the fire.', 'A long, dry afternoon.', 'A yellow with an edge.', 'Bottle green. Keep out of reach.',
        'Glacier blue, and in no hurry.', 'Dusk, kept indoors.', 'Water-clear. Almost not there.', 'Smoked glass, for after dark.']
HERO_NAMES = [('speaker', 'acid', 'Tropos in Acid'), ('hemisphere', 'ember', 'Hemisphere in Ember'), ('core', 'ember', 'Core in Ember'), ('mantle', 'ember', 'Mantle in Ember')]


def fix_12(p, web):
    # (10) the hero: no dots; one names row inside its bottom edge, each name a link to that product in that tint
    p.rest, n = re.subn(r'<a class="hs-pt[^"]*" href="#[a-z]+-[a-z]+" style="[^"]*"><span class="hs-dot" aria-hidden="true"></span><span class="hs-label">[^<]*</span></a>', '', p.rest)
    assert n == 8, ('fix_12: hero dots', n)
    names = '<nav class="hero-names" aria-label="In the picture">' + ' <span aria-hidden="true">&middot;</span> '.join(
        f'<a href="#{r}-{t}">{label}</a>' for r, t, label in HERO_NAMES) + '</nav>'
    p.sub('</script></div>\n      <script>if (document.documentElement.dataset.home) heroIn()</script>',
          '</script>' + names + '</div>\n      <script>if (document.documentElement.dataset.home) heroIn()</script>')
    # (11) the eight mood lines out, everywhere; the plain facts beside them stay
    for line in MOOD:
        esc = json.dumps(line)[1:-1]
        for where in ('head', 'rest'):
            s = getattr(p, where)
            s = s.replace(f'"line":"{esc}"', '"line":""').replace(f'"line": "{esc}"', '"line": ""').replace(f'<p class="line">{line}</p>', '')
            setattr(p, where, s)
    # the switcher's line would say only the color's name: it goes, with what filled it
    p.rest, n = re.subn(r'<p class="tint-line" aria-live="polite"><b>[^<]*</b> <span>[^<]*</span></p>', '', p.rest)
    assert n == 1, ('fix_12: the switcher line', n)
    p.rest, n = re.subn(r'line\.innerHTML = `<b>\$\{t\.name\}\.</b> <span>\$\{t\.line\}</span>`;', '', p.rest)
    assert n == 2, ('fix_12: the line scripts', n)
    p.sub('<div class="wrap mk-head"><h2>Each color is a place.</h2></div>', '')
    for line in MOOD:
        assert line not in p.head and line not in p.rest, ('fix_12: a mood line left', line)
    p.css("""
/* C5 (10): the hero's names row, inside its bottom edge, on a dark veil so it reads on the picture */
.hs-hero .hero-photo { position: relative }
.hero-names { position: absolute; left: 0; right: 0; bottom: 0; z-index: 3; padding: 44px 16px 14px; text-align: center; color: #F4F1EC;
  font: 500 15px/1.5 var(--sans); background: linear-gradient(rgb(0 0 0 / 0), rgb(0 0 0 / .62) 55%); text-shadow: 0 1px 2px rgb(0 0 0 / .6) }
.hero-names a { color: #F4F1EC; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 3px; display: inline-block; padding-block: 8px }
.hero-names a:hover { color: #fff; text-decoration-thickness: 2px }
.hero-names a:focus-visible { outline: 2px solid #F4F1EC; outline-offset: 2px }
.hero-names span { margin-inline: 6px; opacity: .8 }
@media (max-width: 560px) { .hero-names { font-size: 14px; padding: 36px 10px 8px } .hero-names span { margin-inline: 3px } }
""")


def finish_12(web):
    """No mood line in any built file (the pages, the previews, their descriptions and structured data)."""
    import glob
    for f in glob.glob(os.path.join(web.SITE, '**', '*.html'), recursive=True) + [os.path.join(web.SITE, 'vercel.json')]:
        s = open(f).read()
        t = s.replace('<h2>Eight colors, the full spectrum.</h2>', '<h2>Eight colors</h2>').replace('Eight colors, the full spectrum.', 'Eight colors.').replace('eight colors, the full spectrum.', 'eight colors.')     # set late (rc_finish's SPECTRUM)
        if t != s:
            open(f, 'w').write(t); s = t
        assert 'the full spectrum' not in s and 'Each color is a place' not in s, ('finish_12: a retired heading in', f)
        t = s
        for line in MOOD:                       # removed, not rewritten: the plain facts after it stay ("Acid: translucent golden yellow ...")
            for form in (line, json.dumps(line)[1:-1]):
                t = t.replace(form + ' ', '').replace(form, '')
        if t != s:
            open(f, 'w').write(t); s = t
        for line in MOOD:
            assert line not in s and json.dumps(line)[1:-1] not in s, ('finish_12: a mood line in', f, line)


# --- C5 (the coordinator 24 Nov 04:05, the owner: "9 just 'Make first contact'"): every product page's Ask
# button reads the one label, the second button and the phone bar too; the price line beside it goes.
# The address line with Copy address stays under it; the header's Contact and the home's Write to us stay.
ASK_LABEL = 'Make first contact'
def finish_13(web):
    import glob
    old_ask = {'Ask about a pair', 'Ask about Hemisphere', 'Ask about Core', 'Ask about Mantle', 'Ask about it'}
    n_pages = 0
    for f in glob.glob(os.path.join(web.SITE, '**', '*.html'), recursive=True):
        t = open(f, encoding='utf-8').read()
        if 'p-ask' not in t:
            assert not any(a in t for a in old_ask), ('finish_13: an Ask label outside a product page', f)
            continue
        n_pages += 1
        o = t
        for a in old_ask:
            t = t.replace(f'"{a}"', f'"{ASK_LABEL}"').replace(f"'{a}'", f"'{ASK_LABEL}'")
        t = t.replace("a.textContent = ASK[P.id] || 'Ask';", f"a.textContent = ASK[P.id] || '{ASK_LABEL}';")
        k = t.count('p-ask" href="mailto:hello@earf.world">Ask</a>')
        assert k == 3, ('finish_13: the three Ask buttons', f, k)
        t = t.replace('p-ask" href="mailto:hello@earf.world">Ask</a>', f'p-ask" href="mailto:hello@earf.world">{ASK_LABEL}</a>')
        for old in ('        <p class="price">Price on request. <span id="p-unit"></span></p>\n',
                    "  document.getElementById('p-unit').innerHTML = P.unit;\n"):
            assert t.count(old) == 1, ('finish_13', f, old)
            t = t.replace(old, '')
        assert not any(a in t for a in old_ask) and 'Price on request' not in t and 'p-unit' not in t, ('finish_13: left', f)
        open(f, 'w', encoding='utf-8').write(t)
    assert n_pages >= 32, ('finish_13: product pages', n_pages)
