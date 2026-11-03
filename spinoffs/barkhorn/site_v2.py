"""Round 48: the site audit's no-regret fixes (the coordinator, 2026-11-03; spinoffs/barkhorn/coordinator/
site-audit-2026-11-03 on r46-owner-notes 3480947a), applied to the built page while web.V2 is on. Off, web.py never
calls this and the page is byte for byte as before. Each change is an asserted replacement on the page web.py builds
(so a change in web.py that moves its target fails the build instead of passing silently), plus the CSS and script below.
HOME_V2 (also off) reorders the home as the audit's recommended "launch film".

Held until the owner decides (the coordinator): a sign-up form, the founder's name or picture, publishing the press kit
and the journal (their links and the home's journal band go while V2 is on; their pages stay built, as slots), and any
production deploy."""
import re

# the three design figures for the Sound band: today's particulars until the speaker lane sends horn A's
# (asked 2026-11-03; FIGURES_FROM names the commit they came from once they arrive)
FIGURES = [('51', 'Hz', 'to about 51 Hz at &minus;3&nbsp;dB, before the room'),
           ('115', 'dB', 'up to about 115 dB at 1&nbsp;m, each'),
           ('2&thinsp;&times;&thinsp;125', 'W', 'built in, crossed at 1&nbsp;kHz')]
FIGURES_FROM = None
SOUND_KEY = 'blue'          # the turning view's color (Ice): today's front-arc frames, until the new set
HELD_HABITATS = ('red', 'orange')   # Ember's lava and the Dust mesa read as CG (the audit); the biomes lane is rebuilding them
NIGHT = '#13110F'           # the night ground, warmed to the paper's hue (was #0B0C10)
MONO = "'IBM Plex Mono', 'Courier New', monospace"


class Page:
    def __init__(self, head, rest):
        self.head, self.rest, self.styles = head, rest, []

    def sub(self, old, new, n=1, where='rest'):
        s = getattr(self, where)
        assert s.count(old) == n, ('site_v2: expected', n, 'got', s.count(old), old[:90])
        setattr(self, where, s.replace(old, new))

    def css(self, text):
        self.styles.append(text)      # after the page's own styles (some of which sit in its body), so these win

    def check(self):
        """The house words: the build fails on British spellings and the retired lines in anything a visitor reads
        (scripts' code aside: the router still answers the old #colour addresses)."""
        page = re.sub(r'<script\b.*?</script>|<style\b.*?</style>', ' ', self.head + self.rest, flags=re.S)
        said = re.findall(r'\b(?:alt|title|content|aria-label)="([^"]*)"', page)    # words in attributes a visitor meets
        text = re.sub(r'<[^>]+>', ' ', page) + ' '.join(said)
        bad = re.findall(r'(?i)colour|enquir|stockist|microfibre|something in the air|eight things in the air', text)
        assert not bad, ('site_v2: retired words', sorted(set(b.lower() for b in bad)))

    def done(self):
        self.check()
        if self.styles:
            self.rest += '\n<style>' + ''.join(self.styles) + '</style>'
        return self.head, self.rest

    def section(self, sid):
        """The home's <section ... id="sid"> ... </section>, cut out of the page and returned."""
        m = re.search(r'\n?[ \t]*<section [^>]*\bid="%s"[^>]*>' % re.escape(sid), self.rest)
        assert m, ('site_v2: no section', sid)
        depth, i = 0, m.start()
        for t in re.finditer(r'<(/?)section\b', self.rest[m.start():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = m.start() + t.end() + len('>')
                break
        out = self.rest[m.start():end]
        self.rest = self.rest[:m.start()] + self.rest[end:]
        return out


def pairings(p):
    """The owner's rule: on a product page, recommend only the other lines, never a speaker for a speaker (nor a lamp
    for a lamp). Monochromatic first (the same color in the other lines), then the complement, then the neighbors.
    The color pages keep the whole range."""
    p.sub("function picks(cols, pid, k, max = 4) {\n  const order = [...PRODUCTS.filter(x => x.id === pid), ...PRODUCTS.filter(x => x.id !== pid)], out = [];",
          "function picks(cols, pid, k, max = 4, others = false) {\n"
          "  const line = (PRODUCTS.find(x => x.id === pid) || {}).line;\n"
          "  const order = others ? PRODUCTS.filter(x => x.line !== line) : [...PRODUCTS.filter(x => x.id === pid), ...PRODUCTS.filter(x => x.id !== pid)], out = [];")
    p.sub("""      : `${names(r.comp)}, opposite on the color wheel. ${pair}`, picks(r.comp, pid, k)),""",
          """      : `${names(r.comp)}, opposite on the color wheel. ${pair}`, picks(r.comp, pid, k, 4, mono)),""")
    p.sub("""      : `${names(r.ana)}, either side of it on the wheel.`, picks(r.ana, pid, k))];
  if (mono) out.push(block(`${box.id}-mono`, 'Monochromatic', `${c.name} in the other lines.`, picks([k], pid, k)));""",
          """      : `${names(r.ana)}, either side of it on the wheel.`, picks(r.ana, pid, k, 4, mono))];
  if (mono) out.unshift(block(`${box.id}-mono`, 'Monochromatic', `${c.name} in the other lines.`, picks([k], pid, k, 4, true)));""")


def words(p):
    """Every line says one thing, once: the explainers, eyebrows and 'See the ...' links go; one name per thing
    (Tropos, Lighting, Mantle; a turntable, never a record player); Contact for Inquire."""
    # the header and footer
    p.sub('<li><a href="#speakers" data-nav="speakers">Speakers</a></li>', '<li><a href="#speakers" data-nav="speakers">Tropos</a></li>')
    p.sub('<li><a href="#turntable" data-nav="turntable">Turntable</a></li>', '<li><a href="#turntable" data-nav="turntable">Mantle</a></li>')
    p.sub('    <li><a href="#journal" data-nav="journal">Journal</a></li>\n', '')
    p.sub('    <li><a href="#contact">Inquire</a></li>', '    <li class="contact-link"><a href="#contact">Contact</a></li>')
    p.sub('<a href="#journal">Journal</a><a href="#press">Press</a><a href="#contact">Inquiries</a>', '<a href="#contact">Contact</a>')
    p.sub('<p>EARF &middot; San Francisco &middot; In development, not yet for sale &middot; The pictures are renders &middot; &copy; 2026</p>',
          '<p class="foot-line">Designed in San Francisco. Pictures are renders until the first pair is built. &copy; 2026 EARF</p>')
    # the lines' tiles: the name is the link, one line each
    p.sub('<span class="t-line">A powered horn loudspeaker in eight colors of cast acrylic.</span><span class="t-go">See the speakers</span>',
          '<span class="t-line">A powered horn loudspeaker.</span>')
    p.sub('<span class="t-line">A pendant and a table lamp in the speakers&rsquo; acrylic, frosted within.</span><span class="t-go">See the lighting</span>',
          '<span class="t-line">A pendant and a table lamp.</span>')
    p.sub('<span class="t-line">A record player in the same eight colors, lit from underneath.</span><span class="t-go">See the record player</span>',
          '<span class="t-line">A turntable, lit from underneath.</span>')
    p.sub('<div class="head"><div><p class="eyebrow">The lines</p><h2>One acrylic, three ways to use it.</h2></div></div>',
          '<h2 class="vh">The lines</h2>')
    # the speaker line: the brand lane's line for the eight
    p.sub('<p class="eyebrow">Tropos</p><h2>Eight things in the air.</h2>', '<h2>Eight colors, Ember to Smoke.</h2>')
    # the habitats, the room, progress
    p.sub('<p class="eyebrow">In their element</p><h2>Each color, where it began.</h2>', '<h2>Each color, where it began.</h2>')
    p.sub('<p class="eyebrow">At home</p><h2>A pair in Poison.</h2>', '<h2>A pair in Poison.</h2>')
    p.sub('<figcaption class="wrap"><span>At golden hour, by a tall window.</span><span>Each stands 1293&nbsp;mm tall, 560&nbsp;mm wide at the cabinet.</span></figcaption>',
          '<figcaption class="wrap"><span>A room can be one color or three. <i class="render">Render</i></span><span>51&nbsp;in (1293&nbsp;mm) tall</span></figcaption>')
    p.sub('<p class="eyebrow">Progress</p><h2>Drawn to be made.</h2>', '<h2>Drawn to be made.</h2>')
    # the close: no pill, the address a plain link
    p.sub('''    <p class="eyebrow">Inquiries</p>
    <h2>Write to us.</h2>
    <p>Everything is made to order, so we quote rather than list. From launch, write here for prices and lead times.
      Trade and stockists: the same address.</p>
    <div class="addr"><code id="addr">hello@earf.world</code>''', '''    <h2>Write to us.</h2>
    <p>Everything is made to order, so we quote rather than list. Prices and lead times from launch. Designers, dealers
      and press: the same address.</p>
    <div class="addr"><a class="mail" href="mailto:hello@earf.world"><span id="addr">hello@earf.world</span></a>''')
    # the product page
    p.sub('<a class="btn solid" id="p-enquire" href="#contact">Inquire about a pair</a>', '<a class="btn solid" id="p-enquire" href="#contact">Ask about a pair</a>')
    # the palette shows once on the home: in the light stage (its coins, then the eight); 'By color' goes
    p.section('colors')
    # the journal and the press kit are held: their home band goes (their pages stay built, unlinked)
    p.section('from-journal')
    # the turntable is a turntable
    p.sub("kind: D.tt.kind,", "kind: 'Turntable',")


def kit(p):
    """A design house's kit: text links for buttons, the grotesk everywhere but the spec tables, square pictures, no
    chevrons on pictures, captions on the page ground, real type contrast, one night ground."""
    p.css(f"""
/* round 48 (V2): the design-house kit */
:root {{ --mono: var(--sans); --spec-mono: {MONO}; --night: {NIGHT} }}
body {{ font-size: 18px }}
.facts, .facts dt, .facts dd, .spec dl, .spec dt, .spec dd {{ font-family: var(--spec-mono) }}
.eyebrow, .num {{ letter-spacing: 0.02em; text-transform: none }}
p.eyebrow {{ display: none }}
.btn, .btn.solid {{ background: none !important; border: 0 !important; border-radius: 0 !important; padding: 0 !important; min-height: 44px;
  color: var(--ink) !important; font: 500 18px/1.3 var(--sans); text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 4px }}
.btn:hover {{ text-decoration-thickness: 2px }}
#copy, #copy-note {{ display: none }}
.addr .mail {{ color: var(--ink); font-size: clamp(22px, 2.4vw, 30px); text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 6px }}
main img, main picture, main figure, .tile, .pcard, .stage, .photo, .card, .thumb, .thumb img {{ border-radius: 0 !important }}
.tile, .pcard, .card {{ background: none !important; box-shadow: none !important }}
.hab-frame .nav, .gallery .nav {{ display: none !important }}
.habitats, .habitats.v2 {{ -webkit-mask-image: none !important; mask-image: none !important }}
.lightband, .debut-top {{ background: var(--night) !important }}
h1, .hero-title h1 {{ font-weight: 600; letter-spacing: -0.035em }}
h2 {{ font-weight: 600; letter-spacing: -0.025em }}
figcaption, .cap, .t-line {{ font-size: 15px }}
.render {{ font-style: normal; color: var(--muted); font-size: 13px; letter-spacing: 0.02em; margin-left: 6px }}
.foot-line {{ font-family: var(--sans) !important; text-transform: none !important; letter-spacing: 0 !important; font-size: 14px !important }}
.top .contact-link {{ margin-left: 24px }}
.menu {{ border: 0 !important; border-radius: 0 !important; padding: 10px 0 !important; font: 500 16px/1 var(--sans) !important;
  text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 4px }}
""")


def hero(p):
    """One frame, the height of the screen: the tagline in the picture's quiet upper third, the speakers each a link
    (the hotspots), one small line and 'Render' beneath. No pills, no legend, no explainer."""
    i = p.rest.index('<div class="wrap hero-foot">')
    j = p.rest.index('</ul></div>', i) + len('</ul></div>')
    p.rest = (p.rest[:i] + '<div class="wrap hero-cap"><span>Hi-fi and lighting, designed in San Francisco.</span>'
              '<i class="render">Render</i></div>' + p.rest[j:])
    p.sub('<p class="eyebrow">EARF &middot; Tropos</p><h1', '<h1')
    p.css("""
/* round 48 (V2): the hero, one frame */
.hero { height: calc(100svh - var(--header)); min-height: 520px; padding: 0; display: flex; flex-direction: column; justify-content: center; overflow: hidden }
.hero-pic { flex: none; width: min(100%, calc((100svh - var(--header) - 56px) * 2)); margin-inline: auto }
.hero-title .wrap { padding-block: clamp(20px, 5vh, 64px) 0 }
.hero-cap { width: 100%; display: flex; justify-content: space-between; gap: 16px; padding-block: 14px 0; color: var(--muted); font-size: 14px }
.hero-cap .render { margin: 0 }
@media (max-width: 860px) {
  .hero-pic { width: min(100%, calc((100svh - var(--header) - 56px) * 0.8)) }
  .hero-title { position: absolute; color: var(--ink) }
  .hero-title .wrap { padding-block: 22px 0 }
}
""")


def light(p):
    """The light stage: one frame the height of the screen, the uplit photograph full-bleed with the color's name and
    line over it at lower left and the coins at lower right; scroll snaps to each color (8 x 20svh), the lamp goes off
    and the next comes on, and the run ends on the uplit eight at full height. Without script, under reduced motion and
    in print: the uplit eight, with the eight names and lines beneath."""
    # the explainer and the number go; the section's line stays, small, at the top of the frame
    p.sub('<div class="wrap light-head"><p class="eyebrow">Lit from below</p><h2>Put a light under it.</h2><p>Cast acrylic carries light to its edges, so a lamp underneath fills the whole cabinet with color.</p></div>',
          '<i class="anchor" id="colors"></i><div class="wrap light-head"><h2 class="vh">Put a light under it.</h2></div>')
    p.sub('<div class="light-intro"><p class="eyebrow">Lit from below</p><h2>Put a light under it.</h2><p>Cast acrylic carries light to its edges, so a lamp underneath fills the whole cabinet with color.</p></div>',
          '<div class="light-intro"><p class="light-kicker" aria-hidden="true">Put a light under it.</p></div>')
    p.sub('<p class="num" id="light-num">Tropos 01</p>', '<p class="num" id="light-num" hidden>Tropos 01</p>')
    # snap points, one per color, then the eight
    snaps = ''.join(f'<i class="snap" style="--s:{i}" aria-hidden="true"></i>' for i in range(8))
    p.sub('<div class="light-run" id="light-run">', '<div class="light-run" id="light-run">' + snaps)
    p.sub('<figure class="facade">', '<figure class="facade" id="eight"><i class="snap-eight" aria-hidden="true"></i>')
    # the static version's names and lines
    p.rest = p.rest.replace('</figure>\n  </section>', '</figure>\n__LIGHT_LIST__\n  </section>', 1) if '__LIGHT_LIST__' not in p.rest else p.rest
    p.css("""
/* round 48 (V2): the light stage, one frame */
html { scroll-snap-type: y proximity; scroll-padding-top: var(--header) }
.lightband { padding: 0 }
.light-head { display: none !important } .anchor { display: block; height: 0 }
.light-run { height: calc(100svh - var(--header) + 8 * 20svh) }
.light-run .snap { position: absolute; left: 0; width: 1px; height: 1px; top: calc(var(--s) * 20svh + 10svh); scroll-snap-align: start }
.light-stage { display: block; position: sticky }
.light-glow { display: none }
.light-pic { position: absolute; inset: 0; -webkit-mask-image: none !important; mask-image: none !important; height: 100% !important }
.light-pic img { object-fit: cover; object-position: 50% 62% }
.light-text { position: absolute; inset: 0; display: grid; grid-template-columns: minmax(0, 1fr) auto; grid-template-rows: auto minmax(0, 1fr) auto;
  padding: clamp(20px, 4vh, 40px) max(16px, calc((100vw - 1240px) / 2 + 16px)); gap: 0 24px; pointer-events: none;
  background: linear-gradient(to top, rgb(19 17 15 / .55), transparent 34%) }
.light-intro { grid-column: 1 / -1; grid-row: 1 } .light-kicker { margin: 0; font-size: 18px; font-weight: 500; color: #ECE8E1 }
.light-colour { grid-column: 1 / -1; grid-row: 3; display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: end; gap: 0 24px; pointer-events: auto }
.light-name { grid-column: 1; font-size: clamp(40px, 4.6vw, 64px) }
.light-line { grid-column: 1; min-height: 0; color: #CFCBC4 }
.light-coins { grid-column: 2; grid-row: 1 / span 2; align-self: end; margin: 0 }
.lightband .facade { opacity: 1 !important; height: calc(100svh - var(--header)); position: relative; -webkit-mask-image: none !important; mask-image: none !important }
.lightband .facade picture { display: block; width: 100%; height: 100% }
.lightband .facade img { width: 100%; height: 100%; object-fit: contain; border-radius: 0 }
.snap-eight { position: absolute; top: 0; scroll-snap-align: start }
.light-list { display: none; list-style: none; margin: 0; padding: 32px max(16px, calc((100vw - 1240px) / 2 + 16px)) 72px;
  grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px 24px; color: #ECE8E1 }
.light-list b { display: block; font-size: 20px } .light-list span { color: #A39E95; font-size: 15px }
@media (max-width: 860px) {
  .light-colour { grid-template-columns: minmax(0, 1fr) }
  .light-coins { grid-column: 1; grid-row: auto; margin-top: 14px; justify-content: space-between }
  .light-name { font-size: 40px }
  .light-pic img { object-position: 50% 60% }
  .light-list { grid-template-columns: repeat(2, minmax(0, 1fr)) }
  .light-text { background: linear-gradient(to top, rgb(19 17 15 / .8), rgb(19 17 15 / .35) 30%, transparent 46%) }
  .lightband .facade img { object-fit: cover }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-snap-type: none }
  .light-run { display: none }
  .light-list { display: grid }
}
@media print { .light-run { display: none } .light-list { display: grid } }
""")


def light_list(p, web):
    items = ''.join(f'<li><b>{name}</b><span>{line}</span></li>' for k, num, name, icon, acr, line, *_ in web.CLOUDS)
    p.sub('__LIGHT_LIST__', f'<ul class="light-list" aria-label="The eight colors">{items}</ul>')
    p.rest += '\n<noscript><style>.light-run { display: none } .light-list { display: grid !important }</style></noscript>'


def sound(p, web):
    """Sound, straight after the hero: Tropos turning slowly on the studio's seamless (today's front-arc frames), the
    line, three design figures, footnoted as design figures and linked to the horn's chapter."""
    k = SOUND_KEY
    frames = [f'img/spin/{k}-{i:02d}.webp' for i in range(9)]
    figs = ''.join(f'<li><b>{n}<small>{u}</small></b><span>{t}</span></li>' for n, u, t in FIGURES)
    html = f'''
  <section class="band sound" id="sound"><div class="wrap sound-grid">
    <figure class="sound-turn" data-frames='{",".join(frames)}'><img src="{frames[2]}" width="600" height="746" loading="lazy"
      alt="Tropos in Ice, turning slowly on a pale seamless"><figcaption><i class="render">Render</i></figcaption></figure>
    <div class="sound-words"><h2>The oldest amplifier is a shape.</h2>
      <ul class="figures">{figs}</ul>
      <p class="foot-note">Design figures; measured ones follow with the first pair. <a href="#turn">The horn</a></p></div>
  </div></section>
'''
    i = p.rest.index('</section>', p.rest.index('<section class="hero" id="top">')) + len('</section>')
    p.rest = p.rest[:i] + html + p.rest[i:]
    p.css("""
/* round 48 (V2): Sound */
.sound-grid { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: 48px; align-items: center }
.sound-turn { margin: 0; background: #F1EFEB } .sound-turn img { display: block; width: 100%; height: auto }
.sound-turn figcaption { text-align: right; padding-top: 8px }
.sound-words h2 { font-size: clamp(34px, 4.2vw, 60px); max-width: 14ch }
.figures { list-style: none; margin: 40px 0 0; padding: 0; display: grid; gap: 24px }
.figures b { display: block; font-size: clamp(40px, 4.6vw, 64px); font-weight: 600; letter-spacing: -0.03em; line-height: 1 }
.figures small { font-size: .45em; font-weight: 500; margin-left: 6px; letter-spacing: 0 }
.figures span { color: var(--muted); font-size: 16px }
.foot-note { margin: 28px 0 0; color: var(--muted); font-size: 14px } .foot-note a { color: var(--ink) }
@media (max-width: 860px) { .sound-grid { grid-template-columns: minmax(0, 1fr); gap: 28px } }
""")
    p.rest += """
<script>
// round 48 (V2): Sound turns slowly while in view (a ping-pong through the front arc), still under reduced motion
(() => { const f = document.querySelector('.sound-turn'); if (!f || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const src = f.dataset.frames.split(','), img = f.querySelector('img'); let i = 2, d = 1, t = 0;
  src.forEach(s => { const x = new Image(); x.decoding = 'async'; f._pre = (f._pre || []).concat(x); x.dataset.s = s; });
  const step = () => { i += d; if (i >= src.length - 1 || i <= 0) d = -d; img.src = src[i]; };
  new IntersectionObserver(es => es.forEach(e => { clearInterval(t);
    if (e.isIntersecting) { f._pre.forEach(x => { if (!x.src) x.src = x.dataset.s; }); t = setInterval(step, 420); } }), { threshold: 0.4 }).observe(f); })();
</script>"""


def habitats(p, web):
    """The habitats without carousel chrome: each captioned with its line and a quiet count, native swipe; any frame
    that still reads as CG held back until the biomes lane's rebuild."""
    for k in HELD_HABITATS:
        m = re.search(r'<li><a href="#speaker-[a-z]+"><picture><source media="\(max-width: 700px\)" srcset="img/%s-habitat-portrait\.jpg">.*?</li>' % k, p.rest)
        assert m, ('site_v2: habitat', k)
        p.rest = p.rest[:m.start()] + p.rest[m.end():]
    shown = [c for c in web.CLOUDS if c[0] not in HELD_HABITATS]
    for n, (k, num, name, icon, acr, line, *_) in enumerate(shown, 1):
        p.sub(f'<span><b>{name}</b></span></a></li>', f'<span><b>{name}.</b> {line} <i class="render">{n}&thinsp;/&thinsp;{len(shown)} &middot; Render</i></span></a></li>')
    p.sub('<ul class="habitats" id="hab"', '<ul class="habitats v2" id="hab"')


def render_word(p):
    """'Render', quietly, once per picture where a caption carries it; the room's caption has it (words()); the
    footer says it once for the site."""
    pass


def apply(web, head, rest):
    p = Page(head, rest)
    if web.V2:
        pairings(p)
        words(p)
        kit(p)
        hero(p)
        light(p)
        light_list(p, web)
        sound(p, web)
        habitats(p, web)
    return p.done()
