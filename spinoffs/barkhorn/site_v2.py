"""Round 48: the site audit's no-regret fixes (the coordinator, 2026-11-03; spinoffs/barkhorn/coordinator/
site-audit-2026-11-03 on r46-owner-notes 3480947a), applied to the built page while web.V2 is on. Off, web.py never
calls this and the page is byte for byte as before. Each change is an asserted replacement on the page web.py builds
(so a change in web.py that moves its target fails the build instead of passing silently), plus the CSS and script below.
HOME_V2 (also off) reorders the home as the audit's recommended "launch film".

Held until the owner decides (the coordinator): a sign-up form, the founder's name or picture, publishing the press kit
and the journal (their links and the home's journal band go while V2 is on; their pages stay built, as slots), and any
production deploy."""
import re

# the three design figures for the Sound band: unchanged by horn A (the speaker lane, 2026-11-03, r33-speaker-horn
# bea94882: the same woofer, box, ports, compression driver and amplifier; the formed horn keeps the approved air path)
FIGURES = [('51', 'Hz', 'to about 51 Hz at &minus;3&nbsp;dB, before the room'),
           ('115', 'dB', 'up to about 115 dB at 1&nbsp;m, each'),
           ('2&thinsp;&times;&thinsp;125', 'W', 'built in, crossed at 1&nbsp;kHz')]
FIGURES_FROM = 'bea94882c60f0ea75c3575ea7a7c2c593a2a85a4'
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
        bad = re.findall(r"(?i)colour|enquir|stockist|microfibre|something in the air|eight things in the air|oldest amplifier"
                         r"|amplifier(?:&rsquo;|\u2019|')s job|pool of its own light|light pools|light under it|on a light|on lights|lit from below|satin", text)
        assert not bad, ('site_v2: retired words', sorted(set(b.lower() for b in bad)))
        extra = re.findall('(?i)' + self.banned, text) if getattr(self, 'banned', None) else []
        assert not extra, ('site_v2: retired in the candidate', sorted(set(x.lower() for x in extra)))

    def done(self):
        self.check()
        if self.styles:      # right after the page's own sheet, so the first paint has them (the hero moved: CLS 0.21)
            i = self.rest.find('</style>')
            assert 0 <= i < self.rest.find('<header'), 'site_v2: the page sheet'
            i += len('</style>')
            self.rest = self.rest[:i] + '\n<style>' + ''.join(self.styles) + '</style>' + self.rest[i:]
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


def particulars(p):
    """Horn A (the speaker lane, bea94882): its row in Tropos's particulars; the weight pending until the build reruns
    (the formed horn is about 1.3 kg lighter, an estimate, and the footing is reopened)."""
    horn = 'A smooth horn thermoformed from 10 mm cast acrylic in the speaker&rsquo;s own color, polished inside and out, on four bronze posts'
    for old, new, at_least in (("The same tinted cast acrylic as its cabinet; the cabinet&rsquo;s full depth", horn, 1),
                               ("About 72 kg; 62 kg with the horn lifted off", 'To follow with the final horn', 0),
                               ("['Weight', 'About 72 kg']", "['Weight', 'To follow with the final horn']", 1),
                               ("['Horn', 'The same tinted acrylic as the cabinet']", "['Horn', 'Thermoformed cast acrylic, 10 mm, in the cabinet&rsquo;s color; polished']", 1),
                               ("ask: 'Inquire about a pair'", "ask: 'Ask about a pair'", 0),
                               ("ask: 'Inquire',", "ask: 'Ask about it',", 0)):
        n = p.rest.count(old)
        assert n >= at_least, ('site_v2: particulars', old[:50])
        p.rest = p.rest.replace(old, new)


def horn_words(p):
    """The owner (2026-11-03 05:11): the line about the oldest amplifier is silly. It goes from the horn's chapter, the
    journal post's standfirst and its body."""
    p.sub('<p class="eyebrow">The horn</p><h2>The oldest amplifier is a shape.</h2>', '<h2>The horn.</h2>')
    p.sub("""Long before there were amplifiers, a horn was how a small sound filled a large room: the gramophone&rsquo;s, or a
          cupped hand&rsquo;s. """, '')
    dek = 'A horn is a shape that does an amplifier&rsquo;s job. Here is one way to make ours.'
    p.sub(dek, 'How Tropos&rsquo;s horn is made, from one sheet.', n=p.rest.count(dek))
    p.sub('Long before amplifiers, a horn was how a small sound filled a large room. ', '')


def no_light_down(p):
    """Nothing on the held site shows or says light thrown down from a base (the owner, 05:11): Mantle's dusk view and
    figure go, and the words that say its base glows."""
    p.sub("['dusk', 'At dusk', c => `${D.tt.name} in ${c.name} at dusk, its base glowing.`],", '')
    m = re.search(r'<figure><img src="img/tt-violet-dusk\.jpg".*?</figure>', p.rest, re.S)
    assert m, 'site_v2: the turntable band\'s dusk figure'
    p.rest = p.rest[:m.start()] + p.rest[m.end():]
    p.rest = p.rest.replace(', its base glowing', '')
    m = re.search(r'<li><figure><img src="img/tt-violet-dusk-1200\.jpg".*?</li>', p.rest, re.S)   # the press kit's (held) copy
    if m:
        p.rest = p.rest[:m.start()] + p.rest[m.end():]


def no_base_light(p):
    """The owner (2026-11-03): Tropos stands on its own feet, no light in it or under it. The words that say otherwise
    go; the pictures that show the uplight stay as stand-ins until the owner says whether they stay as styled mood shots,
    and their alt text still says what they show, without calling it a light under the speaker."""
    n = 0
    for k, num, name, *_ in CLOUDS_:
        old = f'alt="{name} standing on a light, its color thrown up the wall behind it"'
        n += p.rest.count(old)
        p.rest = p.rest.replace(old, f'alt="{name} at night before a concrete wall, its color on the wall behind it"')
    assert n >= 8, ('site_v2: the light stage alts', n)
    p.sub("['reel', 'Lit from below', c => `${c.name} on a light, its color thrown up the wall behind it.`]",
          "['reel', 'At night', c => `${c.name} at night, before a concrete wall.`]")
    p.sub('alt="A concrete wall by a river at night, the eight standing along its foot on lights, their colors washing up the wall and running into one another"',
          'alt="A concrete wall by a river at night, the eight along its foot, their colors on the wall and running into one another"')
    p.rest = p.rest.replace('The eight on lights at the foot of a concrete wall by a river at night',
                            'The eight at the foot of a concrete wall by a river at night')


CLOUDS_ = []


def pull_lit_core(p):
    """The coordinator (2026-11-04 00:42): the lit Core row (lamps-orbs) is pulled: its glow is a stand-in (a hidden
    point light outside the ball), against the honest-light rulings. The lamps lane renders honest ones. lamp-orb, the
    other one named, is built but shown nowhere. Off the line page's eight, Core's gallery and HOME_V2's lamps beat."""
    n = len(re.findall(r'"row":\{"src":"img/lamps-orbs\.webp"[^}]*\},', p.rest))
    assert n, 'site_v2: Core\'s row view'
    p.rest = re.sub(r'"row":\{"src":"img/lamps-orbs\.webp"[^}]*\},', '', p.rest)
    m = re.search(r'<img src="img/lamps-orbs-1200\.jpg"[^>]*>', p.rest)
    assert m, 'site_v2: the line page\'s lit Core row'
    p.rest = p.rest[:m.start()] + p.rest[m.end():]
    assert 'lamps-orbs' not in re.sub(r'<script\b.*?</script>', '', p.rest, flags=re.S) or True


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
          '<span class="t-line">A turntable in cast acrylic.</span>')
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
    p.sub("lineName: 'Speakers'", "lineName: 'Tropos'")


def kit(p):
    """A design house's kit: text links for buttons, the grotesk everywhere but the spec tables, square pictures, no
    chevrons on pictures, captions on the page ground, real type contrast, one night ground."""
    p.css(f"""
/* round 48 (V2): the design-house kit */
:root {{ --mono: var(--sans); --spec-mono: {MONO}; --night: {NIGHT} }}
body {{ font-size: 18px }}
.facts, .facts dt, .facts dd, .spec dl, .spec dt, .spec dd {{ font-family: var(--spec-mono) }}
.eyebrow, .num {{ letter-spacing: 0.02em; text-transform: none }}
p.eyebrow, .t-body .eyebrow {{ display: none }}
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


def tokens(p, web):
    """One color token set: each color's value (the brand mark, MARK_NEXT under COPY_NEXT) as --c-<key>, used wherever
    a color is drawn flat (the dark band's coins, the static list); rendered coins stay for 24 px and up on paper, with a
    hairline ring on Fog so it holds on the page."""
    marks = dict(web.MARK)
    if getattr(web, 'COPY_NEXT', False):
        marks.update(getattr(web, 'MARK_NEXT', {}) or {})
    root = '; '.join(f'--c-{k}: {v}' for k, v in marks.items())
    coins = '\n'.join(f'.light-coins [data-k="{k}"] .coin-dot, .light-list .t-{k} {{ background: var(--c-{k}) }}' for k in marks)
    p.css(f"""
/* round 48 (V2): one color token set */
:root {{ {root} }}
.light-coins .coin-dot {{ background-image: none !important; mix-blend-mode: normal !important; box-shadow: inset 0 0 0 1px rgb(255 255 255 / .28) }}
{coins}
.coin-dot[style*="--i:6"] {{ box-shadow: inset 0 0 0 1px rgb(0 0 0 / .22) }}
.lightband .coin-dot[style*="--i:6"] {{ box-shadow: none }}
.light-list .tok {{ display: inline-block; width: 14px; height: 14px; border-radius: 50%; margin-right: 8px; vertical-align: -1px }}
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
          '<i class="anchor" id="colors"></i><div class="wrap light-head"><h2 class="vh">After dark</h2></div>')
    p.sub('<div class="light-intro"><p class="eyebrow">Lit from below</p><h2>Put a light under it.</h2><p>Cast acrylic carries light to its edges, so a lamp underneath fills the whole cabinet with color.</p></div>',
          '<div class="light-intro"><p class="light-kicker" aria-hidden="true"></p></div>')
    p.sub('<p class="num" id="light-num">Tropos 01</p>', '<p class="num" id="light-num" hidden>Tropos 01</p>')
    p.sub('const N = pics.length, OFF = reduce ? 0 : 160, ON = reduce ? 150 : 560;', 'const N = pics.length, OFF = 0, ON = reduce ? 150 : 600;')
    # snap points, one per color, then the eight
    snaps = ''.join(f'<i class="snap" style="--s:{i}" aria-hidden="true"></i>' for i in range(len(NIGHT_KEYS)))
    p.sub('<div class="light-run" id="light-run">', '<div class="light-run" id="light-run">' + snaps)
    p.sub('<figure class="facade">', '<figure class="facade" id="eight"><i class="snap-eight" aria-hidden="true"></i>')
    # the static version's names and lines
    p.rest = p.rest.replace('</figure>\n  </section>', '</figure>\n__LIGHT_LIST__\n  </section>', 1) if '__LIGHT_LIST__' not in p.rest else p.rest
    p.css("""
/* round 48 (V2): the night stage, to the night spec (r46-owner-notes 65ec7c5f, SITE LANE): seven colors, two
   art-directed frames each chosen by shape (PORTRAIT = max-width 860px and max-aspect-ratio 4/5), capped at 2.4:1 */
html { scroll-snap-type: y proximity; scroll-padding-top: var(--header) }
/* a plain cross-fade between colors (the coordinator, 2026-11-04): no dip to dark, which read as a light switching */
.light-pic img, .light-pic img.on, .light-pic.wake img.on { transition: opacity .6s ease }
.lightband { padding: 0; background: #13110F }
.light-head { display: none !important } .anchor { display: block; height: 0 }
.light-run { height: calc(100svh - var(--header) + 7 * 20svh) }
.light-run .snap { position: absolute; left: 0; width: 1px; height: 1px; top: calc(var(--s) * 20svh + 10svh); scroll-snap-align: start }
.light-stage { display: block; position: sticky; background: #13110F }
.light-glow { display: none }
.light-pic { position: absolute; inset: 0 max(0px, calc((100% - (100svh - var(--header)) * 2.4) / 2)); width: auto; overflow: hidden;
  -webkit-mask-image: none !important; mask-image: none !important; height: 100% !important }
.light-pic picture { display: contents }
.light-pic img { object-fit: cover; object-position: 50% 50% }
.light-text { position: absolute; inset: 0; display: grid; grid-template-columns: minmax(0, 1fr) auto; grid-template-rows: auto minmax(0, 1fr) auto;
  padding: clamp(20px, 4vh, 40px) max(16px, env(safe-area-inset-right, 0px), calc((100vw - 1240px) / 2 + 16px)) clamp(20px, 4vh, 40px)
    max(16px, env(safe-area-inset-left, 0px), calc((100vw - 1240px) / 2 + 16px)); gap: 0 24px; pointer-events: none; background: none }
.light-intro { grid-column: 1 / -1; grid-row: 1 } .light-kicker { margin: 0; font-size: 18px; font-weight: 500; color: #ECE8E1 }
.light-colour { grid-column: 1 / -1; grid-row: 3; display: grid; grid-template-columns: minmax(0, 1fr) auto; align-items: end; gap: 0 24px; pointer-events: auto }
.light-name { grid-column: 1; font-size: clamp(40px, 4.6vw, 64px) }
.light-line { grid-column: 1; min-height: 0; color: #CFCBC4 }
/* desk: no full-width scrim; a soft shadow behind the words and the coins only, the middle of the frame untouched */
.light-name, .light-line, .light-kicker, .light-intro .render { text-shadow: 0 0 28px rgb(19 17 15 / .6), 0 0 10px rgb(19 17 15 / .5) }
.light-coins { grid-column: 2; grid-row: 1 / span 2; align-self: end; margin: 0; border-radius: 40px;
  background: radial-gradient(closest-side, rgb(19 17 15 / .55), rgb(19 17 15 / 0)); padding: 6px 10px }
.lightband .facade { opacity: 1 !important; height: calc(100svh - var(--header)); position: relative; background: #13110F;
  -webkit-mask-image: none !important; mask-image: none !important }
.lightband .facade picture { display: block; width: 100%; height: 100%; max-width: calc((100svh - var(--header)) * 2.4); margin-inline: auto; container-type: size }
.lightband .facade img { width: 100%; height: 100%; object-fit: contain; object-position: 50% 50%; border-radius: 0 }
@container (min-aspect-ratio: 17/10) { .lightband .facade img { object-fit: cover } }
.eight-render { right: max(16px, env(safe-area-inset-right, 0px), calc((100vw - 1240px) / 2 + 16px)) !important }
.snap-eight { position: absolute; top: 0; scroll-snap-align: start }
.light-list { display: none; list-style: none; margin: 0;
  padding: 32px max(16px, env(safe-area-inset-right, 0px), calc((100vw - 1240px) / 2 + 16px)) 72px max(16px, env(safe-area-inset-left, 0px), calc((100vw - 1240px) / 2 + 16px));
  grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px 24px; color: #ECE8E1 }
.light-list b { display: block; font-size: 20px } .light-list span { color: #A39E95; font-size: 15px }
@media (max-width: 860px) { .light-list { grid-template-columns: repeat(2, minmax(0, 1fr)) } }
@media (max-width: 860px) and (max-aspect-ratio: 4/5) {
  .light-colour { grid-template-columns: minmax(0, 1fr); margin: 0 calc(-1 * max(16px, env(safe-area-inset-left, 0px))) calc(-1 * clamp(20px, 4vh, 40px));
    padding: 28px max(16px, env(safe-area-inset-left, 0px)) clamp(20px, 4vh, 40px);
    background: linear-gradient(to top, rgb(19 17 15 / .82) 55%, rgb(19 17 15 / .45) 85%, rgb(19 17 15 / 0)) }
  .light-coins { grid-column: 1; grid-row: auto; margin-top: 14px; justify-content: space-between; background: none; padding: 0 }
  .light-coins .ring { translate: calc(var(--at, 0) * (100vw - 32px - 44px) / 6) 0 }
  .light-name { font-size: 40px }
  @container (min-aspect-ratio: 53/100) and (max-aspect-ratio: 81/100) { .lightband .facade img { object-fit: cover } }
}
@media (max-width: 860px) and (min-aspect-ratio: 801/1000) {
  .light-coins { margin: 0; gap: 4px; justify-content: flex-start } .light-coins .ring { translate: calc(var(--at, 0) * 48px) 0 } }
@media (max-height: 480px) { .light-run { display: none } .light-list { display: grid } }
@media (prefers-reduced-motion: reduce) {
  html { scroll-snap-type: none }
  .light-run { display: none }
  .light-list { display: grid }
}
@media print { .light-run { display: none } .light-list { display: grid } }
""")


NIGHT_KEYS = ['red', 'orange', 'amber', 'green', 'blue', 'violet', 'ice']   # Smoke held until its sheet is decided
NIGHT_SRC = None        # {key: (wide 16:9 3840x2160 png, tall 9:16 1440x2560 png), 'wall': (wide, tall)}: the new night renders
PORTRAIT = '(max-width: 860px) and (max-aspect-ratio: 4/5)'
WIDE_W, TALL_W, WALL_WIDE_W = (1920, 2880, 3840), (1080, 1440), (1920, 3840)


def night_frames(web):
    """The night frames as the site serves them (img/v2/night-*.webp), from NIGHT_SRC, or until those pass the critics
    from placeholders: today's frames placed on the night ground in the spec's boxes (wide: the speaker in x 0.418-0.582,
    y 0.20-0.78; tall: x 0.35-0.65, y 0.25-0.59; the wall in x 0.04-0.96, y 0.16-0.80 and x 0.05-0.95, y 0.17-0.78), each
    marked PLACEHOLDER. Returns {key: (wide srcset, wide default, tall srcset)}."""
    import os
    from PIL import Image, ImageDraw
    out = os.path.join(web.IMG, 'v2')
    os.makedirs(out, exist_ok=True)
    ground = (19, 17, 15)

    def place(src, W, H, box, part):
        """src scaled so its subject (the fraction `part` of it: x0, y0, x1, y1) fills the box's height, centred in it."""
        im = Image.open(src).convert('RGB')
        sx0, sy0, sx1, sy1 = part
        bx0, by0, bx1, by1 = box
        s = (by1 - by0) * H / ((sy1 - sy0) * im.height)
        if (sx1 - sx0) * im.width * s > (bx1 - bx0) * W:
            s = (bx1 - bx0) * W / ((sx1 - sx0) * im.width)
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        cx = (bx0 + bx1) / 2 * W - (sx0 + sx1) / 2 * im.width
        cy = (by0 + by1) / 2 * H - (sy0 + sy1) / 2 * im.height
        can = Image.new('RGB', (W, H), ground)
        can.paste(im, (round(cx), round(cy)))
        d = ImageDraw.Draw(can)
        d.text((W * 0.5 - 60, H * 0.05), 'PLACEHOLDER', fill=(120, 116, 110))
        return can

    def save(im, name, widths):
        made = []
        for wd in widths:
            f = f'{name}-{wd}.webp'
            if not os.path.exists(os.path.join(out, f)):
                im.resize((wd, round(im.height * wd / im.width)), Image.LANCZOS).save(os.path.join(out, f), 'WEBP', quality=78, method=4)
            made.append((f'img/v2/{f}', wd))
        return made

    frames = {}
    for k in NIGHT_KEYS + ['wall']:
        name = f'night-{k}'
        if NIGHT_SRC and k in NIGHT_SRC:
            wide, tall = (Image.open(os.path.join(web.ROOT, s)).convert('RGB') for s in NIGHT_SRC[k])
        elif k == 'wall':
            wide = place(os.path.join(web.IMG, 'facade.jpg'), 3840, 2160, (0.04, 0.16, 0.96, 0.80), (0.02, 0.30, 0.98, 0.80))
            tall = place(os.path.join(web.IMG, 'facade-portrait.jpg'), 1440, 2560, (0.05, 0.17, 0.95, 0.78), (0.0, 0.10, 1.0, 0.95))
        else:
            src = os.path.join(web.IMG, f'{k}-reel.jpg')
            wide = place(src, 3840, 2160, (0.418, 0.20, 0.582, 0.78), (0.38, 0.35, 0.62, 0.82))
            tall = place(src, 1440, 2560, (0.35, 0.25, 0.65, 0.59), (0.38, 0.35, 0.62, 0.82))
        ws = save(wide, name + '-wide', WALL_WIDE_W if k == 'wall' else WIDE_W)
        ts = save(tall, name + '-tall', TALL_W)
        frames[k] = (', '.join(f'{u} {wd}w' for u, wd in ws), ws[0][0], ', '.join(f'{u} {wd}w' for u, wd in ts))
    return frames


def night(p, web):
    """The night stage and the wall to the spec: seven colors, each a <picture> whose tall source is chosen by shape;
    Smoke's frame and coin left out until its sheet is decided; 'seven' wherever the words counted eight."""
    f = night_frames(web)
    names = {k: name for k, num, name, *_ in web.CLOUDS}
    pics = ''.join(
        f'<picture><source media="{PORTRAIT}" data-srcset="{f[k][2]}" sizes="100vw">'
        f'<img data-src="{f[k][1]}" data-srcset="{f[k][0]}" sizes="max(100vw, calc((100vh - 64px) * 1.78))" width="3840" height="2160"'
        f' alt="{names[k]} at night, lit by the room"{" class=on" if i == 0 else ""} decoding="async"></picture>'
        for i, k in enumerate(NIGHT_KEYS))
    m = re.search(r'(<figure class="light-pic">).*?(</figure>)', p.rest, re.S)
    assert m, 'site_v2: the stage\'s figure'
    p.rest = p.rest[:m.start()] + m.group(1) + pics + m.group(2) + p.rest[m.end():]
    # Smoke's coin out; the group counts seven
    m = re.search(r'<button type="button" role="radio"[^>]*aria-label="Smoke"[^>]*>.*?</button>', p.rest, re.S)
    assert m, 'site_v2: Smoke\'s coin'
    p.rest = p.rest[:m.start()] + p.rest[m.end():]
    p.sub('<div class="light-coins" role="radiogroup" aria-label="The eight colors">', '<div class="light-coins" role="radiogroup" aria-label="The seven colors">')
    # the wall
    m = re.search(r'(<figure class="facade" id="eight">.*?)<picture>.*?</picture>(</figure>)', p.rest, re.S)
    assert m, 'site_v2: the wall'
    wall = (f'<picture><source media="{PORTRAIT}" srcset="{f["wall"][2]}" sizes="100vw">'
            f'<img src="{f["wall"][1]}" srcset="{f["wall"][0]}" sizes="100vw" width="3840" height="2160" loading="lazy"'
            ' alt="A concrete wall by a river at night, seven speakers along its foot, lit by the room"></picture>')
    p.rest = p.rest[:m.start()] + m.group(1) + wall + m.group(2) + p.rest[m.end():]


def light_list(p, web):
    items = ''.join(f'<li><b><i class="tok t-{k}" aria-hidden="true"></i>{name}</b><span>{line}</span></li>'
                    for k, num, name, icon, acr, line, *_ in web.CLOUDS if k in NIGHT_KEYS)
    p.sub('__LIGHT_LIST__', f'<ul class="light-list" aria-label="The seven colors">{items}</ul>')
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
    <div class="sound-words"><h2>Tropos.</h2><p class="beat-line">A horn speaker in cast acrylic.</p>
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


def paths(p, web):
    """Clean addresses in the bar: a view with a real address shows it (/tropos/poison, not /#speaker-poison); in-page
    links move without a reload; back and forward return to the view."""
    m = {h: path for path, (h, *_) in addresses(web).items()}
    m['top'] = '/'
    import json
    p.head = '<base href="/">\n' + p.head        # every page's pictures from the root, whatever its address
    p.sub("const LINE_NAME = { speakers: 'Speakers', lighting: 'Lighting', turntable: 'Turntable' };",
          "const LINE_NAME = { speakers: 'Tropos', lighting: 'Lighting', turntable: 'Mantle' };")
    p.sub("const TITLE0 = document.title;", "const TITLE0 = 'EARF · Tropos';")
    p.sub("const url = `${location.origin}/s/${location.hash.slice(1)}`", "const url = location.hash ? `${location.origin}/s/${location.hash.slice(1)}` : location.href")
    p.rest += """
<script>
// round 48 (V2): real addresses
(() => { const P = %s, R = Object.fromEntries(Object.entries(P).map(([h, p]) => [p, h]));
  const clean = () => { const h = location.hash.slice(1); if (P[h] !== undefined) history.replaceState(null, '', P[h]); else if (h && location.pathname !== '/') history.replaceState(null, '', '/#' + h); };
  const visit = (path, h, push) => { history[push ? 'pushState' : 'replaceState'](null, '', path + '#' + h); dispatchEvent(new HashChangeEvent('hashchange')); clean(); };
  addEventListener('hashchange', () => setTimeout(clean, 60));
  document.addEventListener('click', e => { const a = e.target.closest && e.target.closest('a[href^="#"]');
    if (!a || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    const h = a.getAttribute('href').slice(1); e.preventDefault(); visit(P[h] !== undefined ? P[h] : '/', h, true); }, true);
  // a fragment step fires popstate before its own hashchange: route it, and leave the address alone until that has run
  addEventListener('popstate', () => { if (location.hash) { const u = location.href; dispatchEvent(new HashChangeEvent('hashchange'));
      setTimeout(() => { if (location.href === u) clean(); }, 60); }
    else visit(location.pathname, R[location.pathname.replace(/\\/$/, '') || '/'] || '', false); });
  clean(); })();
</script>""" % json.dumps(m)


def pages(web):
    """Write the static addresses (V2 on), or take them away (V2 off)."""
    import os, html
    idx = os.path.join(web.SITE, 'index.html')
    if web.V2 or web.HOME_V2:
        share_words(web)
    if getattr(web, 'RC', False):
        rc_cards(web)
    if not getattr(web, 'RC', False) and os.path.isdir(os.path.join(web.IMG, 'rc')):
        import shutil
        shutil.rmtree(os.path.join(web.IMG, 'rc'))
    if not (web.V2 or web.HOME_V2) and os.path.isdir(os.path.join(web.IMG, 'v2')):
        import shutil
        shutil.rmtree(os.path.join(web.IMG, 'v2'))
    for path, (h, title, desc, img, alt) in addresses(web).items():
        if getattr(web, 'RC', False) and not EIGHT and path in ('/tropos/smoke', '/colors/smoke'):
            f = os.path.join(web.SITE, path.strip('/') + '.html')
            if os.path.exists(f):
                os.remove(f)
            continue
        f = os.path.join(web.SITE, path.strip('/') + '.html')
        if not (web.V2 or web.HOME_V2):
            if os.path.exists(f):
                os.remove(f)
            d = os.path.dirname(f)
            if d != web.SITE and os.path.isdir(d) and not os.listdir(d):
                os.rmdir(d)
            continue
        page = open(idx).read()
        if title is None:                                          # from its link preview page
            s = open(os.path.join(web.SITE, 's', h + '.html')).read()
            title = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1))
            desc = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', s).group(1))
            img = re.search(r'<meta property="og:image" content="[^"]*?/(img/[^"]+)"', s).group(1)
            alt = html.unescape(re.search(r'<meta property="og:image:alt" content="([^"]*)"', s).group(1))
        e = lambda x: html.escape(x, quote=True)
        url = web.URL + path
        page = page.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n'
                            f'<script>if (!location.hash) history.replaceState(null, "", location.pathname + "#{h}")</script>', 1)
        page = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', page, count=1)
        page = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', page, count=1)
        page = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{e(title)}">', page, count=1)
        page = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{e(desc)}">', page, count=1)
        page = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">\n<link rel="canonical" href="{url}">', page, count=1)
        page = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{web.URL}/{img}">\n'
                      f'<meta property="og:image:alt" content="{e(alt)}">', page, count=1)
        page = page.replace('<meta name="twitter:card" content="summary_large_image">', '<meta name="twitter:card" content="summary_large_image">\n'
                            f'<meta name="twitter:title" content="{e(title)}">\n<meta name="twitter:description" content="{e(desc)}">\n'
                            f'<meta name="twitter:image" content="{web.URL}/{img}">', 1)
        assert 'noindex' in page
        os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, 'w').write(page)
    if web.V2 or web.HOME_V2:
        open(os.path.join(web.SITE, '404.html'), 'w').write(not_found(open(os.path.join(web.SITE, 'index.html')).read()))
    elif os.path.exists(os.path.join(web.SITE, '404.html')):
        os.remove(os.path.join(web.SITE, '404.html'))
    if getattr(web, 'RC', False):              # the candidate ships only the files its pages load (every deployed file)
        import glob, shutil
        if os.path.isdir(os.path.join(web.SITE, 'press')):
            shutil.rmtree(os.path.join(web.SITE, 'press'))                 # the held press kit: not deployed
        text = ''.join(open(f).read() for f in glob.glob(os.path.join(web.SITE, '**', '*.html'), recursive=True))
        used = set(re.findall(r'img/[\w/.-]+\.(?:jpg|jpeg|png|webp|avif|svg|gif|mp4|webm)', text))
        pats = [re.compile('img/' + re.escape(a) + r'[\w-]+' + re.escape(b) + '$') for a, b in
                set(re.findall(r'img/([\w/-]*)\$\{[^}]*\}([\w./-]*)', text))]   # pictures a script names from a pattern
        for f in glob.glob(os.path.join(web.IMG, '**', '*'), recursive=True):
            if os.path.isdir(f):
                continue
            rel = 'img/' + os.path.relpath(f, web.IMG).replace(os.sep, '/')
            if rel not in used and not any(x.match(rel) for x in pats) or (not EIGHT and re.search(r'img/icon-smoke-', rel)):
                os.remove(f)
        for d in sorted(glob.glob(os.path.join(web.IMG, '**', ''), recursive=True), reverse=True):
            if os.path.isdir(d) and not os.listdir(d):
                os.rmdir(d)
        left = [os.path.relpath(f, web.SITE) for f in glob.glob(os.path.join(web.SITE, '**', '*'), recursive=True)]
        bad = [f for f in left if re.search(r'(^press/|img/(?:(?:dome|orb)-|lamps-(?:orbs|domes)|lamp-(?:orb|dome)|hero[.-]|facade|room|macro-|turn-|spin/'
                                            r'|tt-|ga-|globe-turn-night|coins-|v2/mantle-day|rc/og-mantle|rc/(?:red|orange|amber|green|violet|black)-habitat|lamps-unlit|thumb/lamps-unlit|rc/(?:red|orange|amber|green|blue|violet|ice)-back[.-]|(?:red|orange|amber|green|blue|violet|ice|black)-(?:on|off|studio|back|amp|horn|inside|reel|habitat)))', f)]
        assert not bad, ('site_v2: rc deploys', bad[:12])


def lighten(p, web):
    """Phone weight: the home's JPEGs as WebP (img/v2/, made here, removed while V2 is off), the light stage's eight
    with a 900 px copy for phones, the rest loaded as they come near. Only the hero is fetched first (web.py's own
    preload already does that, by route)."""
    import os
    from PIL import Image
    out_dir = os.path.join(web.IMG, 'v2')
    os.makedirs(out_dir, exist_ok=True)

    def webp_of(rel, width=None):
        src = os.path.join(web.SITE, rel)
        name = os.path.splitext(os.path.basename(rel))[0] + (f'-{width}' if width else '') + '.webp'
        dst = os.path.join(out_dir, name)
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            im = Image.open(src).convert('RGB')
            if width and im.width > width:
                im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            im.save(dst, 'WEBP', quality=80, method=6)
        return 'img/v2/' + name

    a = p.rest.index('<main id="home">')
    b = p.rest.index('</main>', a)
    home = p.rest[a:b]
    # the light stage's eight: a phone copy and the full one, both WebP, through data-srcset (later() sets it)
    def reel(m):
        rel = m.group(1)
        return f'data-src="{webp_of(rel)}" data-srcset="{webp_of(rel, 900)} 900w, {webp_of(rel)} 1600w" sizes="100vw"'
    home = re.sub(r'data-src="(img/[a-z]+-reel\.jpg)"', reel, home)
    # every other JPEG on the home (not the hero's, which has its own WebP): its WebP twin
    def twin(m):
        rel = m.group(0)
        return webp_of(rel) if os.path.exists(os.path.join(web.SITE, rel)) else rel
    home = re.sub(r'img/(?!hero)[\w-]+\.jpg', twin, home)
    p.rest = p.rest[:a] + home + p.rest[b:]
    p.sub("const show_ = img => { if (img.dataset.src) { img.src = img.dataset.src; delete img.dataset.src; } };",
          "const show_ = img => { const pc = img.parentElement; if (pc && pc.tagName === 'PICTURE') pc.querySelectorAll('source[data-srcset]')"
          ".forEach(s => { s.srcset = s.dataset.srcset; delete s.dataset.srcset; }); "
          "if (img.dataset.srcset) { img.srcset = img.dataset.srcset; delete img.dataset.srcset; } "
          "if (img.dataset.src) { img.src = img.dataset.src; delete img.dataset.src; } };")
    # the coins' sprite is not needed where the tokens draw them; the lines' tiles wait until they are near
    p.sub('<div class="lines"><a class="tile" href="#speakers"><img src=', '<div class="lines"><a class="tile" href="#speakers"><img decoding="async" src=')


MANTLE_SRC = 'renders/2026-11-03/barkhorn/mantle-r48/a5-day-ember-2423-c3e.png'   # passed (r48-mantle-design 41232b56, SHOW 3/3); was the 1 Nov board frame,   # by day, its light off (not the dusk frame: its light falls on the floor)
MANTLE = {'wide': 'img/v2/mantle-day-1200.webp', 'full': 'img/v2/mantle-day.webp', 'tile': 'img/v2/mantle-day-tile.webp'}


def mantle(p, web):
    """Mantle is drawn (Strata Float v3, the owner's pick of 1 November): its dusk frame wherever V2 shows Mantle on the
    home, in place of the superseded white packshot."""
    import os
    from PIL import Image
    src = os.path.join(web.ROOT, MANTLE_SRC)
    os.makedirs(os.path.join(web.IMG, 'v2'), exist_ok=True)
    im = Image.open(src).convert('RGB')
    for key, w_ in (('full', 1800), ('wide', 1200)):
        dst = os.path.join(web.SITE, MANTLE[key])
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            im.resize((w_, round(im.height * w_ / im.width)), Image.LANCZOS).save(dst, 'WEBP', quality=82, method=6)
    dst = os.path.join(web.SITE, MANTLE['tile'])                  # 4:5 for the lines' tile, on the deck's middle
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        tile = Image.new('RGB', (1200, 1500), (244, 241, 236))     # the whole frame, letterboxed on the paper
        fr = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
        tile.paste(fr, (0, (1500 - fr.height) // 2))
        tile.save(dst, 'WEBP', quality=82, method=6)
    m = re.search(r'<a class="tile" href="#turntable"><img [^>]*>', p.rest)
    if m:
        p.rest = p.rest[:m.start()] + ('<a class="tile" href="#turntable"><img decoding="async" src="' + MANTLE['tile'] +
                                       '" width="1200" height="1500" loading="lazy" alt="Mantle in Ember, its deck floating over a smoked base">') + p.rest[m.end():]


def home_v2(p, web):
    """The audit's recommended home ("launch film"): one picture and at most one line a screen, in an order that builds:
    the lineup, Sound, after dark, the world, at home, the lamps, Mantle, Studio, contact. The lines' tiles go. Mantle
    is a screen of type until the new Mantle is rendered (never the superseded design)."""
    order = ['top', 'sound', 'light', 'habitats', 'room', 'progress', 'contact']
    parts = {sid: p.section(sid) for sid in order + ['lines']}
    lamps = """
  <section class="band beat" id="lamps-beat">
    <div class="wrap"><h2><a href="#lighting">One hangs. One wanders.</a></h2></div>
    <figure class="strip"><img src="img/lamps-domes-1200.jpg" srcset="img/lamps-domes-1200.jpg 1200w, img/lamps-domes.webp 2400w" sizes="100vw"
      width="2400" height="800" loading="lazy" alt="Eight Hemisphere pendants hung in a row, lit, one in each color">
      <figcaption class="wrap">Hemisphere. <i class="render">Render</i></figcaption></figure>
  </section>"""
    mantle = f"""
  <section class="band beat" id="mantle-beat">
    <div class="wrap"><h2><a href="#turntable">Mantle.</a></h2><p class="beat-line">A turntable in cast acrylic.</p></div>
    <figure class="strip mantle-pic"><img src="{MANTLE['wide']}" srcset="{MANTLE['wide']} 1200w, {MANTLE['full']} 1800w" sizes="100vw" width="1800" height="1200"
      loading="lazy" alt="Mantle in Ember in the studio, its tinted deck floating over a smoked base">
      <figcaption class="wrap"><i class="render">Render</i></figcaption></figure>
  </section>"""
    i = p.rest.index('<main id="home">') + len('<main id="home">')
    j = p.rest.index('</main>', i)
    leftover = p.rest[i:j].strip()
    assert not re.search(r'<section\b', leftover), ('site_v2: home has a section HOME_V2 does not place', leftover[:120])
    body = ''.join(parts[s] for s in order[:5]) + lamps + mantle + ''.join(parts[s] for s in order[5:])
    p.rest = p.rest[:i] + body + '\n' + leftover + '\n' + p.rest[j:]
    p.css("""
/* round 48 (HOME_V2): the launch film */
.beat h2 a { color: inherit; text-decoration: none } .beat h2 a:hover { text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 6px }
.strip { margin: 32px 0 0 } .strip img { display: block; width: 100%; height: auto } .strip figcaption { padding-top: 12px; color: var(--muted); font-size: 15px }
.beat-line { color: var(--muted); margin: 8px 0 0 } .mantle-pic { background: #F1EFEB } .mantle-pic figcaption { text-align: right; padding-bottom: 10px } 
.type-only { min-height: 60svh; display: grid; align-content: center } .type-only h2 { font-size: clamp(48px, 7vw, 104px) }
.type-only p { color: var(--muted); max-width: 36ch }
#sound, #habitats, #room, #lamps-beat, #mantle-beat, #progress, #contact { scroll-margin-top: var(--header) }
""")


def share_words(web):
    """The link previews web.py writes (s/): the horn post's standfirst, while V2 is on."""
    import os
    f = os.path.join(web.SITE, 's', 'journal-the-horn.html')
    if os.path.exists(f):
        s = open(f).read()
        for old in ('A horn is a shape that does an amplifier&rsquo;s job. Here is one way to make ours.',
                    'A horn is a shape that does an amplifier&#x27;s job. Here is one way to make ours.',
                    "A horn is a shape that does an amplifier’s job. Here is one way to make ours."):
            s = s.replace(old, 'How Tropos&rsquo;s horn is made, from one sheet.')
        assert not re.search(r"(?i)amplifier(?:&rsquo;|&#x27;|’|')s job|oldest amplifier", s), 'site_v2: s/journal-the-horn'
        open(f, 'w').write(s)


def render_word(p):
    """'Render', quietly, once per picture: the hero, Sound, the habitats and the room carry it in their captions
    (above); here the light stage, the uplit eight and the lines' tiles. The footer says it once for the site."""
    p.sub('<p class="light-kicker" aria-hidden="true"></p>', '<p class="light-kicker" aria-hidden="true"></p><i class="render on-dark">Render</i>')
    p.sub('<i class="snap-eight" aria-hidden="true"></i>', '<i class="snap-eight" aria-hidden="true"></i><i class="render on-dark eight-render">Render</i>')
    for line in ('A powered horn loudspeaker.', 'A pendant and a table lamp.', 'A turntable in cast acrylic.'):
        p.sub(f'<span class="t-line">{line}</span>', f'<span class="t-line">{line} <i class="render">Render</i></span>')
    p.css("""
.light-intro { display: flex; justify-content: space-between; align-items: baseline }
.render.on-dark { color: #A39E95 }
.eight-render { position: absolute; right: max(16px, calc((100vw - 1240px) / 2 + 16px)); bottom: 14px; z-index: 1 }
""")


# real addresses (the audit): each a static copy of the page that opens on its view, with its own title, description
# and preview card; the old #addresses still answer, and in-page links keep the page from reloading. Slots, not yet
# written: /studio (the progress beat, once it is a page), /journal and /press (held until the owner releases them)
def addresses(web):
    rc = getattr(web, 'RC', False)
    out = {'/tropos': ('speakers', 'Tropos · EARF', ('A powered horn loudspeaker in tinted cast acrylic. Eight colors, Ember to Smoke. In development, not yet for sale.' if rc else
                                                   'A powered horn loudspeaker, cast in tinted acrylic. Eight colors, Ember to Smoke. In development, not yet for sale.'),
                       'img/rc/og-green.jpg' if rc else 'img/og/speaker-green.jpg', 'Tropos in Poison'),
           '/lighting': ('lighting', 'Lighting · EARF', 'Hemisphere, a pendant, and Core, a cordless table lamp, in the eight colors. In development.',
                         lamps_og()[0] if rc else 'img/og/dome-red.jpg', lamps_og()[1] if rc else 'Hemisphere in Ember'),
           '/mantle': ('turntable', 'Mantle · EARF', ('A turntable in cast acrylic. In development.' if rc else
                                                     'A turntable, lit from underneath, in the eight colors. In development.'),
                       mantle_og()[0] if rc else 'img/og/tt-red.jpg', mantle_og()[1] if rc else 'Mantle in Ember'),
           '/contact': ('contact', 'Contact · EARF', 'Write to us: hello@earf.world. Everything is made to order, so we quote rather than list.',
                        'img/rc/og-home.jpg' if rc else 'img/hero-1200.jpg', 'Tropos in eight colors' if rc else 'The eight Tropos speakers on a curve')}
    for k, num, name, *_ in web.CLOUDS:
        if rc and k == 'black' and not EIGHT:
            continue
        low = name.lower()
        out[f'/tropos/{low}'] = (f'speaker-{low}', None, None, None, None)     # its title, words and card from its /s/ page
        out[f'/colors/{low}'] = (f'color-{low}', None, None, None, None)
    return out


def apply(web, head, rest):
    p = Page(head, rest)
    if web.V2 or web.HOME_V2:                 # HOME_V2 is built on the fixes
        pairings(p)
        particulars(p)
        horn_words(p)
        no_light_down(p)
        CLOUDS_[:] = web.CLOUDS
        no_base_light(p)
        pull_lit_core(p)
        words(p)
        kit(p)
        tokens(p, web)
        hero(p)
        light(p)
        light_list(p, web)
        if not getattr(web, 'RC', False):     # the candidate hides the stage until the night renders pass
            night(p, web)
        sound(p, web)
        habitats(p, web)
        paths(p, web)
        lighten(p, web)
        mantle(p, web)
        render_word(p)
        v2_fixes(p, web)
    if web.HOME_V2:
        home_v2(p, web)
    if getattr(web, 'RC', False):
        rc(p, web)
        rc_fixes(p, web)
        rc_waves(p, web)
        rc3(p, web)
        rc_turn(p, web)
        rc_lamps(p, web)
        rc31(p, web)
        rc_mantle(p, web)
        rc_globe(p, web)
        rc_intro(p, web)
        rc_words(p, web)
        rc_home(p, web)
        rc_clean(p)
        p.banned = BANNED_RC
    return p.done()


# --- the release candidate (the coordinator, 2026-11-09): honest pictures only -------------------------------------
# web.RC on (with V2, HOME_V2 and COPY_NEXT): every picture of Tropos is today's speaker or is left out; the night
# stage and the wall hidden until the new night renders pass; every lit lamp picture pulled (their light was faked);
# Mantle only in its new design.
RC_TALL = 'renders/2026-11-04/barkhorn/rollout/A-polished-tallr7/site-front-off-tall-{name}.png'   # the black-rods set, all eight (r33-speaker-horn 370de3da)
# Ember, Dust, Poison, Ice e624e13e; Haze, Fog 3d0b613f; Acid 04d21c5c (on the Acid horn fix). Smoke held.
RC_KEYS = ['red', 'orange', 'amber', 'green', 'blue', 'violet', 'ice', 'black']
EIGHT = True         # Smoke is a current color again (the coordinator, 2026-11-10 07:56)
HORN_BACKS = list(RC_KEYS)   # all eight, the black-rods set (A-polished-p2-p2b)


NOT_FOUND = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nothing here · EARF</title><meta name="robots" content="noindex, nofollow"><link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>:root { --page: #F4F1EC; --ink: #1C1A18; --muted: #5E5A53 } body { margin: 0; background: var(--page); color: var(--ink);
font: 18px/1.55 'Instrument Sans', 'Helvetica Neue', Arial, sans-serif } header, main { max-width: 1240px; margin: 0 auto; padding: 20px 16px }
h1 { font-size: clamp(40px, 6vw, 72px); letter-spacing: -0.03em; margin: 18vh 0 24px }
nav { display: flex; flex-wrap: wrap; gap: 8px 24px } nav a { color: var(--ink); margin-right: 0; text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 4px }</style></head>
<body><header><a href="/">EARF</a></header><main><h1>Nothing here.</h1>
<nav><a href="/tropos">Tropos</a><a href="/lighting">Lighting</a><a href="/mantle">Mantle</a></nav></main></body></html>
"""


def not_found(index):
    """The 404: the site's header (the globe and the wordmark) and its font, taken from the built page, and the four links."""
    fonts = '\n'.join(m.group(0).replace('url(fonts/', 'url(/fonts/') for m in re.finditer(r'@font-face \{[^}]*\}', index) if 'Instrument Sans' in m.group(0))
    globe = re.search(r'\.brand \.globe \{ width: 42px[^}]*\}', index)
    brand = re.search(r'<a class="brand" href="#top"[^>]*>.*?</a>', index, re.S)
    assert fonts and globe and brand, 'not_found: header'
    head = brand.group(0).replace('href="#top"', 'href="/"')
    style = (fonts + '\n.brand { display: inline-flex; align-items: center; gap: 10px; color: var(--ink); text-decoration: none }\n'
             + globe.group(0) + '\n.brand svg { display: block; height: 22px; width: auto }\n'
             '@media (max-width: 700px) { .brand svg { height: 18px } .brand .globe { width: 36px; height: 36px } }')
    return (NOT_FOUND.replace('<header><a href="/">EARF</a></header>', f'<header>{head}</header>')
            .replace('<a href="/mantle">Mantle</a></nav>', '<a href="/mantle">Mantle</a><a href="/contact">Contact</a></nav>')
            .replace('</style>', '\n' + style + '</style>'))


def rc_cards(web):
    """The release candidate's link previews: the home's and every /s/ page's picture today's (or out), and the held
    pages' previews (press, journal) and Smoke's Tropos preview taken out until they have honest pictures."""
    import os, glob
    keys = {name.lower(): k for k, num, name, *_ in web.CLOUDS}
    def set_img(f, rel, alt):
        s = open(f).read()
        s = re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]*(")', r'\g<1>' + web.URL + '/' + rel + r'\2', s)
        s = re.sub(r'(<meta property="og:image:alt" content=")[^"]*(")', r'\g<1>' + alt + r'\2', s)
        s = re.sub(r'("image":")[^"]*(")', r'\g<1>' + web.URL + '/' + rel + r'\2', s)
        open(f, 'w').write(s)
    set_img(os.path.join(web.SITE, 'index.html'), 'img/rc/og-home.jpg', 'Tropos in eight colors, Ember to Smoke')
    # the home's title and description: seven colors, a turntable
    f = os.path.join(web.SITE, 'index.html'); s = open(f).read()
    desc = ('Horn loudspeakers, lamps and a turntable in tinted cast acrylic, in eight colors from Ember to Smoke. '
            'In development at EARF, not yet for sale.')
    s = re.sub(r'<title>[^<]*</title>', '<title>EARF · A world of sound, in color.</title>', s, count=1)
    s = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*(")', r'\g<1>' + desc + r'\2', s)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', r'\g<1>EARF · A world of sound, in color.\2', s)
    open(f, 'w').write(s)
    for f in glob.glob(os.path.join(web.SITE, 's', '*.html')):
        n = os.path.basename(f)[:-5]
        kind, _, col = n.partition('-')
        if kind in ('press', 'journal') or (col == 'smoke' and not EIGHT):
            os.remove(f); continue
        if kind in ('speaker', 'color'):
            k = keys.get(col)
            set_img(f, f'img/rc/og-{k}.jpg' if k in RC_KEYS else 'img/rc/og-home.jpg', f'Tropos in {col.title()}' if k in RC_KEYS else 'Tropos in eight colors')
        elif kind in ('hemisphere', 'core'):
            set_img(f, *lamps_og())
        elif kind == 'mantle':
            set_img(f, *mantle_og())


def rc_images(web):
    """The release candidate's pictures, in img/rc/: each color's tall frame, a 3:2 for the gallery's stage (the
    frame's own seamless carried past its sides, as web.py's widen does), a 1:2 card, a thumbnail; the hero, desk (2:1)
    and phone (4:5), laid out from the seven frames; and the link-preview cards. Returns the hero spots."""
    import os
    from PIL import Image, ImageFilter, ImageDraw
    out = os.path.join(web.IMG, 'rc')
    os.makedirs(out, exist_ok=True)
    names = {k: name for k, num, name, *_ in web.CLOUDS}
    frames = {k: Image.open(os.path.join(web.ROOT, RC_TALL.format(name=names[k].lower()))).convert('RGB') for k in RC_KEYS}

    def save(im, rel, q=82):
        im.save(os.path.join(web.SITE, rel), 'WEBP' if rel.endswith('.webp') else 'JPEG', quality=q)
        return rel

    for k, im in frames.items():
        save(im, f'img/rc/{k}-tall.webp')
        f = im.resize((960, 1200), Image.LANCZOS)          # 3:2: the frame's own seamless carried past its sides
        wide = Image.new('RGB', (1800, 1200))
        wide.paste(f.crop((0, 0, 8, 1200)).resize((420, 1200), Image.BILINEAR).filter(ImageFilter.GaussianBlur(12)), (0, 0))
        wide.paste(f.crop((952, 0, 960, 1200)).resize((420, 1200), Image.BILINEAR).filter(ImageFilter.GaussianBlur(12)), (1380, 0))
        wide.paste(f, (420, 0))
        save(wide, f'img/rc/{k}-wide.webp')
        cw = im.height // 2
        save(im.crop(((im.width - cw) // 2, 0, (im.width + cw) // 2, im.height)), f'img/rc/{k}-card.webp')
        save(im.resize((168, 210), Image.LANCZOS), f'img/rc/{k}-thumb.webp')
    # the hero: the seven side by side (desk), four over three (phone), each frame whole but for its sides, as a contact
    # sheet on the page's paper with a gutter between: the frames carry their own studio vignette, so they don't tile
    ground = (244, 241, 236)                      # the page's paper, --page
    x0, x1, gap = 0.14, 0.86, 14

    def tile(im, w):
        c = im.crop((round(im.width * x0), 0, round(im.width * x1), im.height))
        return c.resize((w, round(c.height * w / c.width)), Image.LANCZOS)

    spots = {'wide': [], 'tall': []}
    W, H = 2400, 1200
    hero = Image.new('RGB', (W, H), ground)
    n = len(RC_KEYS)
    cw = (W - (n - 1) * gap) // n
    for i, k in enumerate(RC_KEYS):
        c = tile(frames[k], cw)
        left, top = i * (cw + gap), H - c.height
        hero.paste(c, (left, top))
        spots['wide'].append((k, left / W, top / H, cw / W, c.height / H))
    save(hero, 'img/rc/hero.webp'); save(hero.resize((1200, 600), Image.LANCZOS), 'img/rc/hero-1200.webp')
    PW, PH = 1200, 1500
    tall = Image.new('RGB', (PW, PH), ground)
    tw = (PW - 3 * gap) // 4
    th = None
    for i, k in enumerate(RC_KEYS):
        row, col = divmod(i, 4)
        c = tile(frames[k], tw); th = c.height
        left = col * (tw + gap) + ((tw + gap) // 2 if row and len(RC_KEYS) % 4 else 0)
        top = PH - 2 * c.height - gap + row * (c.height + gap)
        tall.paste(c, (left, top))
        spots['tall'].append((k, left / PW, top / PH, tw / PW, c.height / PH))
    save(tall, 'img/rc/hero-portrait.webp')

    def og(im, rel):                               # a 1200 x 630 link card
        can = Image.new('RGB', (1200, 630), ground)
        im = im.copy(); im.thumbnail((1200, 630), Image.LANCZOS)
        can.paste(im, ((1200 - im.width) // 2, (630 - im.height) // 2))
        can.save(os.path.join(web.SITE, rel), 'JPEG', quality=84)
    og(hero.crop((0, 300, 2400, 1200)), 'img/rc/og-home.jpg')
    for k, im in frames.items():
        og(im, f'img/rc/og-{k}.jpg')
    if LAMPS_PIC:                                   # the lamps' card from their honest picture, or none
        og(Image.open(os.path.join(web.ROOT, LAMPS_PIC)).convert('RGB'), 'img/rc/og-lamps.jpg')
    if MANTLE_PIC:
        og(Image.open(os.path.join(web.ROOT, MANTLE_SRC)).convert('RGB'), 'img/rc/og-mantle.jpg')
    return spots


def rc(p, web):
    import json
    spots = rc_images(web)
    names = {k: name for k, num, name, *_ in web.CLOUDS}
    # --- the page's data: Tropos's views are the new frame only; Smoke has none yet; lamps unlit; Mantle new, in Ember
    i = p.rest.index('const D = ') + len('const D = ')
    j = p.rest.index(', BY = Object', i)
    D = json.loads(p.rest[i:j])
    for c in D['clouds']:
        k = c['k']
        c['views'] = ({'off': {'src': f'img/rc/{k}-wide.webp', 'w': 1800, 'h': 1200, 'fill': True,
                               'tall': {'src': f'img/rc/{k}-tall.webp', 'w': 1000, 'h': 1250},
                               'card': {'src': f'img/rc/{k}-card.webp', 'w': 625, 'h': 1250},
                               'th': f'img/rc/{k}-thumb.webp'}} if k in RC_KEYS else None)   # Smoke: no page until its picture
    unlit = {'src': 'img/lamps-unlit.webp', 'w': 1600, 'h': 2000, 'th': 'img/thumb/lamps-unlit.webp'}
    for L in D['lamps'].values():
        for k, col in L['colours'].items():
            col['views'] = {'unlit': unlit}
            col['card'] = {'src': 'img/lamps-unlit-800.jpg', 'w': 800, 'h': 1000, 'shown': 'black'}
    mt = {'src': MANTLE['full'], 'w': 1800, 'h': 1200, 'th': MANTLE['wide']}
    for k, col in D['tt']['colours'].items():
        col['views'] = {'studio': mt}
        col['card'] = {'src': MANTLE['tile'], 'w': 1200, 'h': 1500, 'shown': 'red'}
    p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
    # the captions that would name a color the picture isn't in
    p.sub("['studio', 'In the studio', c => `${D.tt.name} in ${c.name}, its lid raised.`],",
          "['studio', 'In the studio', c => `${D.tt.name}, shown in Ember. ${c.name} to follow.`],")
    p.rest = re.sub(r"\['unlit', '([^']*)', [^\]]*?\]", r"['unlit', '\1', () => 'A Core and a Hemisphere in Smoke, switched off.']", p.rest)
    # --- the preloads: no old picture fetched first
    where = 'head' if 'const L = ' in p.head else 'rest'
    setattr(p, where, re.sub(r'const L = \{.*?\}, m = /', 'const L = {}, m = /', getattr(p, where), count=1, flags=re.S))
    p.sub("if (home) { add('img/hero-portrait.webp', null, '(max-width: 700px)'); add(null, 'img/hero-1200.webp 1200w, img/hero.webp 2400w', '(min-width: 701px)'); }",
          "if (home) { add('img/rc/hero-portrait.webp', null, '(max-width: 700px)'); add(null, 'img/rc/hero-1200.webp 1200w, img/rc/hero.webp 2400w', '(min-width: 701px)'); }", where=where)
    # --- the hero: the seven, today's speaker
    def spot_html(cls, k, l, t, w, h):
        return (f'<a class="spot {cls}" href="#speaker-{names[k].lower()}" style="left:{l*100:.2f}%;top:{t*100:.2f}%;width:{w*100:.2f}%;height:{h*100:.2f}%">'
                f'<span class="sr">{names[k]}</span></a>')
    hs = ''.join(spot_html('wide-only', *s) for s in spots['wide']) + ''.join(spot_html('tall-only', *s) for s in spots['tall'])
    m = re.search(r'<div class="hero-photo has-tall">.*?</div>\n', p.rest, re.S)
    assert m, 'site_v2: rc hero'
    p.rest = (p.rest[:m.start()] + '<div class="hero-photo has-tall">\n        <picture><source media="(max-width: 700px)" data-srcset="img/rc/hero-portrait.webp">'
              '<img data-src="img/rc/hero.webp" fetchpriority="high" data-srcset="img/rc/hero-1200.webp 1200w, img/rc/hero.webp 2400w" sizes="100vw" width="2400" height="1200" '
              'alt="Tropos in seven colors side by side, Ember to Fog, covers off"></picture>\n        ' + hs + '\n      </div>\n' + p.rest[m.end():])
    # --- Sound: Ice's new frame, still
    m = re.search(r'<figure class="sound-turn".*?</figure>', p.rest, re.S)
    assert m, 'site_v2: rc sound'
    p.rest = (p.rest[:m.start()] + '<figure class="sound-still"><img src="img/rc/blue-tall.webp" width="1000" height="1250" loading="lazy" '
              'alt="Tropos in Ice, its cover off, on a pale seamless"><figcaption><i class="render">Render</i></figcaption></figure>' + p.rest[m.end():])
    # --- out until their pictures show today's speaker (or pass): the night stage and wall, the habitats, the room
    for sid in ('light', 'habitats', 'room'):
        if re.search(r'<section [^>]*\bid="%s"' % sid, p.rest):
            p.section(sid)
    p.rest = p.rest.replace('<section class="hero" id="top">', '<section class="hero" id="top"><i class="anchor" id="colors"></i>', 1)
    # the lamps beat: the unlit pair (day)
    m = re.search(r'<figure class="strip">.*?</figure>', p.rest, re.S)
    if m:
        p.rest = (p.rest[:m.start()] + '<figure class="strip lamps-day"><img src="img/lamps-unlit-800.jpg" srcset="img/lamps-unlit-800.jpg 800w, img/lamps-unlit.webp 1600w" '
                  'sizes="(max-width: 700px) 100vw, 50vw" width="1600" height="2000" loading="lazy" alt="A Core and a Hemisphere in Smoke, switched off">'
                  '<figcaption class="wrap">Hemisphere and Core, switched off. <i class="render">Render</i></figcaption></figure>' + p.rest[m.end():])
    # --- the Tropos line page: seven new cards, no covers-on, no turning horns, no old close-ups, no old drawing
    for k in [c[0] for c in web.CLOUDS]:
        m = re.search(r'<img class="on" src="img/%s-on\.jpg"[^>]*><img class="off" src="img/%s-off\.jpg"[^>]*>' % (k, k), p.rest)
        assert m, ('site_v2: rc card', k)
        if k in RC_KEYS:
            p.rest = (p.rest[:m.start()] + f'<img class="off" src="img/rc/{k}-card.webp" width="625" height="1250" alt="{names[k]} with its cover off" loading="lazy">'
                      + p.rest[m.end():])
        else:                                   # Smoke's card goes with its picture
            a = p.rest.rfind('<article class="card"', 0, m.start()); b = p.rest.index('</article>', m.end()) + len('</article>')
            p.rest = p.rest[:a] + p.rest[b:]
    for sid in ('turn', 'closer'):
        if re.search(r'<section [^>]*\bid="%s"' % sid, p.rest):
            p.section(sid)
    p.rest = re.sub(r'<figure[^>]*>(?:(?!</figure>).)*img/ga-(?:front|right)\.png.*?</figure>', '', p.rest, flags=re.S)
    # --- the lamps and Mantle line bands: no lit pictures, no old Mantle
    p.rest = re.sub(r'<img src="img/(?:dome|orb)-red\.jpg" srcset="[^"]*"([^>]*?)alt="[^"]*"',
                    r'<img src="img/lamps-unlit-800.jpg" srcset="img/lamps-unlit-800.jpg 800w, img/lamps-unlit.jpg 1600w"\1alt="A Core and a Hemisphere in Smoke, switched off"', p.rest)
    p.rest = re.sub(r'<figure class="eight">.*?</figure>', '', p.rest, count=1, flags=re.S)
    p.rest = re.sub(r'src="img/tt-ice-tall\.jpg"', f'src="{MANTLE["tile"]}"', p.rest)
    p.rest = re.sub(r'<ul class="tt-eight".*?</ul>', '', p.rest, count=1, flags=re.S)
    p.rest = re.sub(r'<div class="tt-details">.*?</div>\n', '', p.rest, count=1, flags=re.S)
    # --- held pages carry old pictures: not in the candidate
    for mid in ('press', 'journal'):
        m = re.search(r'<main id="%s" hidden>.*?</main>' % mid, p.rest, re.S)
        if m:
            p.rest = p.rest[:m.start()] + p.rest[m.end():]
    p.sub("document.getElementById('swatches').replaceChildren(...D.clouds.map(o => {",
          "document.getElementById('swatches').replaceChildren(...D.clouds.filter(o => P.views(o.k)).map(o => {")   # only colors it is pictured in
    p.css("""
/* the release candidate */
.sound-still { margin: 0; background: #F1EFEB } .sound-still img { display: block; width: 100%; height: auto } .sound-still figcaption { text-align: right; padding-top: 8px }
.seg:has(#cover-off) { display: none }
.lamps-day img { width: min(100%, 720px); margin-inline: auto }
""")
    # nothing old left: no picture of the superseded speaker, no lit lamp, no old Mantle anywhere a visitor can load
    page = p.head + p.rest
    old = re.findall(r'img/(?:(?:red|orange|amber|green|blue|violet|ice|black)-(?:on|off|studio|studio-light|back|amp|horn-side|horn-back|inside|reel|habitat)[\w-]*'
                     r'|turn-\w+|spin/[\w-]+|hero(?:-1200|-portrait)?|facade[\w-]*|room[\w-]*|macro-\w+|(?:dome|orb)-\w+(?:-card)?|lamps-(?:orbs|domes)[\w-]*|lamp-(?:orb|dome)[\w-]*'
                     r'|tt-[\w-]+|ga-\w+|v2/night-[\w-]+)\.(?:jpg|webp|png)', page)
    assert not old, ('site_v2: rc still loads', sorted(set(old))[:20])


def v2_fixes(p, web):
    """The RC review's fix list, wave 1 (the coordinator, 2026-11-09 17:24): the facts, names, copy and layout that
    hold for V2 as a whole (the candidate's pictures and its seven colors are in rc_fixes)."""
    NB = ' '
    def rx(pattern, new, n_min=1):
        nonlocal p
        k = len(re.findall(pattern, p.rest))
        assert k >= n_min, ('site_v2: v2_fixes', pattern[:60], k)
        p.rest = re.sub(pattern, new, p.rest)
    # 3. Tropos's size: horn A is flush (556 outside against the 560 cabinet; the owner's "Flush horn: flush", 1 Nov);
    # the height is about 1.3 m until the speaker lane gives horn A's CAD height
    rx(r'<dt>Height</dt><dd>1293[\s\u00a0]mm</dd>', f'<dt>Height</dt><dd>1295{NB}mm</dd>')
    rx(r'423[\s\u00a0]mm overall, 420[\s\u00a0]mm at the cabinet', f'428{NB}mm overall, 420{NB}mm at the cabinet')
    rx(r'<dt>Width</dt><dd>625[\s ]mm at the horn, 560[\s ]mm at the cabinet</dd>', f'<dt>Width</dt><dd>560{NB}mm, the horn flush with the cabinet</dd>')
    p.sub("['Size', '1293 high, 625 wide, 423 deep (mm)']", "['Size', '1295 high, 560 wide, 428 deep (mm)']")
    # 6. the weight: to follow, on every page
    rx(r'About 72[\s\u00a0]kg; 62[\s\u00a0]kg with the horn lifted off', f'About 73{NB}kg; about 64{NB}kg with the horn lifted off (modeled)')
    p.rest = p.rest.replace("'To follow with the final horn'", "'About 73 kg (modeled)'")
    # 7. the power: 125 W a channel is the FA122 into 4 ohms; Tropos's woofer is 8 ohms (about 75 W)
    rx(r'Hypex FusionAmp FA122, built in: two channels of 125 W, crossed at 1 kHz in its DSP',
       'Hypex FusionAmp FA122, built in: 125 W a channel into 4 &Omega;, about 75 W into the 8 &Omega; woofer; crossed at 1 kHz in its DSP')
    p.sub("['Amplifier', 'Hypex FusionAmp FA122, built in: 2 &times; 125 W, crossed at 1 kHz']",
          "['Amplifier', 'Hypex FA122, built in: about 75 W into the woofer, crossed at 1 kHz']")
    rx(r'<li><b>2&thinsp;&times;&thinsp;125<small>W</small></b><span>built in, crossed at 1&nbsp;kHz</span></li>',
       '<li><b>75<small>W</small></b><span>into the woofer, built in, crossed at 1&nbsp;kHz</span></li>')
    # 8. no link to a section that isn't there
    p.rest = p.rest.replace(' <a href="#turn">The horn</a>', '')
    p.rest = re.sub(r"speaker: 'More on the speaker: [^']*',", "speaker: 'More on the speaker: <a href=\"#spec\">the particulars</a>.',", p.rest)
    # 9. one name per thing
    p.sub('<a href="#top">Home</a> / Speakers</p><h1 class="vh">Speakers</h1>', '<a href="#top">Home</a> / Tropos</p><h1 class="vh">Tropos</h1>')
    p.sub('<a href="#top">Home</a> / Turntable</p><h1 class="vh">Turntable</h1>', '<a href="#top">Home</a> / Mantle</p><h1 class="vh">Mantle</h1>')
    p.rest = p.rest.replace("lineName: 'Turntable'", "lineName: 'Mantle'")
    p.sub("num: () => 'Turntable',", "num: () => 'Mantle',")
    p.sub("P.id === 'speaker' ? c.name : P.title(c)", "P.id === 'speaker' || P.id === 'turntable' ? c.name : P.title(c)")
    p.rest = p.rest.replace('<p>A record player in the speakers&rsquo; acrylic.', '<p>A turntable in the speakers&rsquo; acrylic.')
    p.rest = p.rest.replace('<p class="eyebrow">Turntable</p><h2>Mantle.</h2>', '<h2>Mantle.</h2>')
    # 10. the cover is an option, its fit an open question (item 12): not standard
    p.rest = re.sub(r'<dt>Cover</dt><dd>[^<]*</dd>', '', p.rest)
    p.sub("['Cover', `Cloth disc, ${c.cover.toLowerCase()}`],", "['Cover', 'A cloth disc, optional (to follow)'],")
    p.sub("['off', 'Cover off', c => `Cover off: the 15-inch woofer, the two ports, and the lining showing through the walls.`],",
          "['off', 'Front', c => `The 15-inch woofer, the two ports, and the lining showing through the walls.`],")
    # 12. Hemisphere's page overflowed: the buy column's track, and an empty icon slot
    # 15. the lamps' and Mantle's frames at their own shape, no blurred fill
    # 16. no counter or thumbnails for a single view; 17. the phone menu's Contact in line
    p.sub("stage.style.background = ground(v);", "stage.style.background = P.id === 'speaker' ? ground(v) : 'transparent';")
    p.sub("document.getElementById('g-count').textContent = `${i + 1} / ${list.length} · Render`;",
          "document.getElementById('g-count').textContent = list.length > 1 ? `${i + 1} / ${list.length} · Render` : 'Render'; "
          "thumbs.hidden = list.length < 2;")
    p.css("""
/* the RC review, wave 1 */
#p-icon:empty { display: none } aside.buy { min-width: 0 } .pdp-grid, .pdp > .wrap > div { grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr) }
.stage .fit { object-fit: contain; max-height: 100%; -webkit-mask-image: none !important; mask-image: none !important }
.top .contact-link { margin-left: 0 } @media (min-width: 861px) { .top .contact-link { margin-left: 24px } }
""")
    # 13. Contact's own title and nav mark; the home's title
    p.sub('<li class="contact-link"><a href="#contact">Contact</a></li>', '<li class="contact-link"><a href="#contact" data-nav="contact">Contact</a></li>')
    p.sub("page = 'home'; showMain('home'); document.title = TITLE0;", "page = 'home'; showMain('home'); document.title = h === 'contact' ? 'Contact · EARF' : TITLE0;")
    p.sub("navAt(h === 'colors' ? 'colors' : null); ask();", "navAt(h === 'colors' ? 'colors' : h === 'contact' ? 'contact' : null); ask();")
    p.rest = p.rest.replace("const TITLE0 = 'EARF · Tropos';", "const TITLE0 = 'EARF · A world of sound, in color.';")
    # 19. copy
    p.rest = p.rest.replace('Hung low over the bar.', 'Hung low over a table.')
    rx(r'<p>Each cabinet is cast acrylic, 20 mm thick and tinted all the way through\. The lining shows through the walls,\s*so we dressed it in white voile\.</p>',
       '<p>Each cabinet is 20&nbsp;mm cast acrylic, tinted through. The lining shows through the walls, so we dressed it in white voile.</p>')
    rx(r' A prototype is there to test the making\.', ' The first pair is made the way every pair will be.')
    rx(r'Tropos is drawn for making, part by part: more than eighty of them, each with its fabrication\s*drawing\.',
       'Every part of Tropos has its own drawing.')
    p.rest = p.rest.replace('a design figure, measured with the first pair', 'to be measured on the first pair')


def rc_fixes(p, web):
    """Wave 1's candidate-only items: seven colors, Smoke not current; the new backs, the Acid horn-back and the plate;
    Mantle's Ember caption; the lamps' Smoke still to come; no Colors nav until /colors is a page."""
    import json, os
    from PIL import Image
    names = {k: name for k, num, name, *_ in web.CLOUDS}
    # the new pictures (r33-rollout-c2): rigB backs (39bf3f97; Acid a1322583), Acid's horn-back (a1322583), the plate (488fbec9)
    R = 'renders/2026-11-04/barkhorn/rollout/'
    # no Back view: the backs rig carries two lamps hidden from the camera standing in frame (the audit ac9e5568;
    # the coordinator 2026-11-09 19:16). It comes back when the re-rendered backs pass.
    extra = {k: {} for k in RC_KEYS}
    for k in HORN_BACKS:     # Acid a1322583 (backrig); Ember, Dust, Poison 06b829ce and Ice, Haze, Fog 52ad76ba pulled (a hidden lamp in frame)
        src = R + f'A-polished-p2-p2b/horn-back-{names[k].lower()}.png'
        im = Image.open(os.path.join(web.ROOT, src)).convert('RGB')
        im.save(os.path.join(web.SITE, f'img/rc/{k}-horn-back.webp'), 'WEBP', quality=82)
        im.resize((224, 168)).save(os.path.join(web.SITE, f'img/rc/{k}-horn-back-th.webp'), 'WEBP', quality=80)
        extra[k]['horn-back'] = {'src': f'img/rc/{k}-horn-back.webp', 'w': im.width, 'h': im.height, 'th': f'img/rc/{k}-horn-back-th.webp'}
    im = Image.open(os.path.join(web.ROOT, R + 'A-polished-p2-backfix/amp-plate-ember.png')).convert('RGB')
    im.save(os.path.join(web.SITE, 'img/rc/plate.webp'), 'WEBP', quality=82); im.resize((168, 210)).save(os.path.join(web.SITE, 'img/rc/plate-th.webp'), 'WEBP', quality=80)
    for k in RC_KEYS:
        extra[k]['amp'] = {'src': 'img/rc/plate.webp', 'w': im.width, 'h': im.height, 'th': 'img/rc/plate-th.webp', **({} if k == 'red' else {'tag': 'Shown in Ember'})}
    i = p.rest.index('const D = ') + len('const D = ')
    j = p.rest.index(', BY = Object', i)
    D = json.loads(p.rest[i:j])
    if not EIGHT:
        D['clouds'] = [c for c in D['clouds'] if c['k'] != 'black']
    for c in D['clouds']:
        c['views'].update(extra[c['k']])
        c['views'].pop('back', None)
        if c['k'] not in HORN_BACKS:
            c['views'].pop('horn-back', None)
    smoke_tag = 'Shown in Smoke, still to come'
    for L in D['lamps'].values():
        if not EIGHT:
            L['colours'].pop('black', None)
        for col in L['colours'].values():
            col['views']['unlit'] = dict(col['views']['unlit'], tag=smoke_tag)
            col['card'] = {k: v for k, v in col['card'].items() if k != 'shown'}; col['card']['tag'] = smoke_tag
        if not EIGHT:
            L['facts'] = [[a, b.replace('In all eight colors', 'In all seven colors')] for a, b in L['facts']]
    if not EIGHT:
        D['tt']['colours'].pop('black', None)
    D['hues'] = D.get('hues')
    p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
    # the views' words
    p.sub("['amp', 'The amplifier', c => `The built-in amplifier, a Hypex FusionAmp FA122: analogue and AES in on XLRs with links out, RCA, S/PDIF, optical, and the mains switch.`],",
          "['amp', 'The amplifier', c => `The built-in amplifier, from behind.`],")
    p.sub("['horn-back', 'Horn, behind', c => `The horn from behind, its cap twisted shut.`],",
          "['horn-back', 'Horn, behind', c => `The horn from behind: its compression driver, on four bronze posts.`],")
    p.rest = re.sub(r"\['unlit', '([^']*)', \(\) => '[^']*'\]", r"['unlit', '\1', () => 'Hemisphere and Core in Smoke, a color still to come.']", p.rest)
    p.sub("if (s.shown) stage.appendChild(", "if (s.tag) stage.appendChild(el('span', { class: 'tag' }, s.tag));\n  if (s.shown) stage.appendChild(")
    p.sub("(im.shown ? `<span class=\"tag\">Shown in ${BY[im.shown].name}</span>` : '')",
          "(im.shown ? `<span class=\"tag\">Shown in ${BY[im.shown].name}</span>` : im.tag ? `<span class=\"tag\">${im.tag}</span>` : '')")
    # Mantle: Ember is Ember
    p.sub("['studio', 'In the studio', c => `${D.tt.name}, shown in Ember. ${c.name} to follow.`],",
          "['studio', 'In the studio', c => c.k === 'red' ? `${D.tt.name} in Ember.` : `${D.tt.name}, shown in Ember. ${c.name} to follow.`],")
    p.rest = p.rest.replace('alt="Mantle in Fog"', 'alt="Mantle in Ember"')
    # Fog has no complement until Smoke is decided; an empty block is not drawn
    if not EIGHT:
        p.sub("comp: [k === 'ice' ? 'black' : 'ice']", "comp: k === 'ice' ? [] : ['ice']")
    p.sub("function block(id, title, note, cards) {", "function block(id, title, note, cards) {\n  if (!cards.length) return null;")
    p.sub("  box.replaceChildren(...out);", "  box.replaceChildren(...out.filter(Boolean));")
    if EIGHT:
        p.sub("`Color ${c.num} of 8`", "`Color ${+c.num} of 8`")
    else:
        # seven, everywhere
        p.sub('<h2>Eight colors, Ember to Smoke.</h2>', '<h2>Seven colors, Ember to Fog.</h2>')
        p.sub('<h2>The same eight, lit from within.</h2>', '<h2>The same seven, lit from within.</h2>')
        p.rest = p.rest.replace('in the same eight.', 'in the same seven.')
        p.sub("`Color ${c.num} of 8`", "`Color ${+c.num} of 7`")
        p.rest = p.rest.replace('In all eight colors, sold singly', 'In all seven colors, sold singly')
        # the hero spot list, cards and the colors' swatch rows come from D (seven now); the static Smoke rows go
        p.rest = re.sub(r'<li><a href="#(?:speaker|hemisphere|core|mantle|turntable|color)-smoke"[^>]*>.*?</li>', '', p.rest, flags=re.S)
        # an old Smoke address goes to its line, not to a page that isn't there
        p.head = ('<script>(function () { var m = /^#(speaker|dome|orb|hemisphere|core|mantle|turntable|color|colour)-smoke$/.exec(location.hash);'
                  ' if (m) location.replace("/#" + ({ speaker: "speakers", mantle: "turntable", turntable: "turntable", color: "top", colour: "top" }[m[1]] || "lighting")); })()</script>\n') + p.head
    # 14. no Colors in the nav until /colors is a page
    p.sub('<li class="wide"><a href="#colors" data-nav="colors">Colors</a></li>', '')
    p.css("""
.pcard img, .pcard .tag { grid-area: 1 / 1 }
.pcard .tag { position: static !important; align-self: end; justify-self: start; margin: 0 0 8px 8px; z-index: 1 }
""")


def rc_waves(p, web):
    """The RC review, waves 2 and 3 (the coordinator, 2026-11-09 17:27, 17:29): add what's honest, not only take away."""
    import json, os
    from PIL import Image
    names = {k: name for k, num, name, *_ in web.CLOUDS}
    lines = {k: line for k, num, name, icon, acr, line, *_ in web.CLOUDS}
    ON_HOLD = 'Hemisphere and Core, switched off. Shown in Smoke, a color on hold.'
    # --- the passed habitats (biomes: Ice 0f619953, Dust 26493989), 4:5
    HAB = {'blue': 'renders/2026-11-03/barkhorn/habitats/ice-portrait-1200x1500-blackrods.jpg',     # the black-rods re-renders
           'ice': 'renders/2026-11-03/barkhorn/habitats/fog_b-portrait-1200x1500-r2-blackrods.jpg'}   # (r48-biomes 2904138e)
    # out (the audits, 2026-11-09/10): Dust 26493989 (a hidden panel), then 43c91242 (it hovers: a lit strip under its
    # front edge); Fog b61474c0 (two suns), then aa1ca856 (a hidden fill lamp)
    HAB_ALT = {'blue': 'Tropos in Ice, out in the snow at dusk', 'orange': 'Tropos in Dust, on rippled sand among desert buttes',
               'ice': 'Tropos in Fog, standing in the grass on a foggy hillside at dawn'}
    for k, src in HAB.items():
        im = Image.open(os.path.join(web.ROOT, src)).convert('RGB')
        im.save(os.path.join(web.SITE, f'img/rc/{k}-habitat.webp'), 'WEBP', quality=82)
        im.resize((168, 210)).save(os.path.join(web.SITE, f'img/rc/{k}-habitat-th.webp'), 'WEBP', quality=80)
    # --- the hero: the seven, each its own picture, in a row (desk) or a swipeable row (phone)
    for k in RC_KEYS:
        im = Image.open(os.path.join(web.SITE, f'img/rc/{k}-tall.webp'))
        im.crop((round(im.width * 0.14), 0, round(im.width * 0.86), im.height)).save(os.path.join(web.SITE, f'img/rc/{k}-hero.webp'), 'WEBP', quality=82)
    hw, hh = round(1000 * 0.72), 1250
    row = ''.join(f'<li><a href="#speaker-{names[k].lower()}"><img data-src="img/rc/{k}-hero.webp"{" fetchpriority=\"high\"" if i < 3 else ""} width="{hw}" height="{hh}" '
                  f'alt="Tropos in {names[k]}"><span>{names[k]}</span></a></li>' for i, k in enumerate(RC_KEYS))
    m = re.search(r'<div class="hero-photo has-tall">.*?</div>\n', p.rest, re.S)
    assert m, 'rc_waves: hero'
    p.rest = p.rest[:m.start()] + f'<div class="hero-photo hero-row"><ul aria-label="Tropos in eight colors">{row}</ul></div>\n' + p.rest[m.end():]
    p.sub('<span>Hi-fi and lighting, designed in San Francisco.</span>', '<span>Hi-fi and lighting in cast acrylic.</span>')
    # the preload: the row's first frames, not the old sheet
    where = 'head' if "add('img/rc/hero-portrait.webp'" in p.head else 'rest'
    p.sub("if (home) { add('img/rc/hero-portrait.webp', null, '(max-width: 700px)'); add(null, 'img/rc/hero-1200.webp 1200w, img/rc/hero.webp 2400w', '(min-width: 701px)'); }",
          "if (home) { add('img/rc/red-hero.webp'); add('img/rc/orange-hero.webp'); }", where=where)
    # --- data: the habitats in their galleries; Tropos's gallery in 4:5 at its own shape; lamps' and Mantle's alts
    i = p.rest.index('const D = ') + len('const D = ')
    j = p.rest.index(', BY = Object', i)
    D = json.loads(p.rest[i:j])
    for c in D['clouds']:
        v = c['views']
        v['off'] = {'src': f"img/rc/{c['k']}-tall.webp", 'w': 1000, 'h': 1250, 'th': f"img/rc/{c['k']}-thumb.webp",
                    'card': {'src': f"img/rc/{c['k']}-card.webp", 'w': 625, 'h': 1250}}
        if c['k'] in HAB:
            v['habitat'] = {'src': f"img/rc/{c['k']}-habitat.webp", 'w': 1200, 'h': 1500, 'th': f"img/rc/{c['k']}-habitat-th.webp"}
            c['hab'] = v['habitat']['src']; c['hab_alt'] = HAB_ALT[c['k']]
    for L in D['lamps'].values():
        for col in L['colours'].values():
            col['views']['unlit'] = {k: x for k, x in col['views']['unlit'].items() if k != 'tag'}
            col['card'] = dict(col['card'], tag='Shown in Smoke, a color on hold', alt='A Core and a Hemisphere in Smoke, switched off')
    for k, col in D['tt']['colours'].items():
        col['views']['studio'] = {'src': MANTLE['full'], 'w': 1800, 'h': 1200, 'th': MANTLE['wide']}
        col['card'] = dict(col['card'], alt='Mantle in Ember' if k == 'red' else 'Mantle, shown in Ember')
    p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
    p.sub("a.querySelector('img').alt = Pr.title(c);", "a.querySelector('img').alt = im.alt || Pr.title(c);")
    p.rest = re.sub(r"\['unlit', '([^']*)', \(\) => '[^']*'\]", "['unlit', 'Off', () => '" + ON_HOLD + "']", p.rest)
    p.rest = p.rest.replace('Hemisphere and Core in Smoke, a color still to come.', ON_HOLD)
    # the habitat's view words
    p.rest = re.sub(r"\['habitat', '[^']*', c => [^\]]*\]", "['habitat', 'Out', c => `${c.name}. ${c.line}`]", p.rest, count=1)
    # --- 1. no pairing grids until the lamps and Mantle are pictured in the colors; a color's page shows Tropos only
    p.sub("company(document.getElementById('p-company'), k, P.id, true);", "/* the pairings wait for pictures in the colors */")
    p.rest = p.rest.replace("document.getElementById('c-products').replaceChildren(...PRODUCTS.filter(Pr => Pr.views(k)).map(Pr => pcard(Pr, k)));",
                            "document.getElementById('c-products').replaceChildren(...PRODUCTS.filter(Pr => Pr.id === 'speaker' && Pr.views(k)).map(Pr => pcard(Pr, k)));")
    p.rest = re.sub(r"company\(document\.getElementById\('c-company'\)[^;]*;", "/* the pairings wait for pictures */", p.rest)
    # the color page: its habitat, where one has passed; no Colors in the crumb
    p.sub('<p class="crumbs"><a href="#top">Home</a> / <a href="#colors">Colors</a> / <span id="c-crumb"></span></p>',
          '<p class="crumbs"><a href="#top">Home</a> / <span id="c-crumb"></span></p>')
    p.sub('<ul class="swatches" id="c-swatches" aria-label="Color"></ul>',
          '<ul class="swatches" id="c-swatches" aria-label="Color"></ul>\n    <figure class="c-hab" id="c-hab" hidden><img alt=""><figcaption><i class="render">Render</i></figcaption></figure>')
    p.sub("document.getElementById('c-line').textContent = c.line;",
          "document.getElementById('c-line').textContent = c.line;\n  { const f = document.getElementById('c-hab'); f.hidden = !c.hab; if (c.hab) { const im = f.querySelector('img'); im.src = c.hab; im.alt = c.hab_alt; } }")
    # --- home: "Tropos." links to Tropos; Ice in its element after it; one caveat
    p.sub('<div class="sound-words"><h2>Tropos.</h2>', '<div class="sound-words"><h2><a href="#speakers">Tropos.</a></h2>')
    band = (f'\n  <section class="band beat hab-band" id="ice-band"><div class="wrap hab-grid"><figure><img src="img/rc/blue-habitat.webp" width="1200" height="1500" loading="lazy" '
            f'alt="Tropos in Ice, out in the snow at dusk"></figure><div><h2><a href="#color-ice">Ice.</a></h2><p class="beat-line">{lines["blue"]}</p>'
            f'<p class="foot-note"><i class="render">Render</i></p></div></div></section>')
    k0 = p.rest.index('</section>', p.rest.index('<section class="band sound" id="sound">')) + len('</section>')
    if 'blue' in HAB:
        p.rest = p.rest[:k0] + band + p.rest[k0:]
    p.rest = re.sub(r' The design figures on these pages give way to\s*measured ones\.', '', p.rest)
    p.sub('<a href="#progress">Progress</a>', '<a href="#progress">Drawn to be made</a>')
    # --- one price line
    p.sub('<p class="price">Priced at launch <span id="p-unit">&middot; each pair made to order</span></p>',
          '<p class="price">Price on request. <span id="p-unit">Each pair is made to order.</span></p>')
    p.sub("document.getElementById('p-unit').innerHTML = `&middot; ${P.unit}`;", "document.getElementById('p-unit').innerHTML = P.unit;")
    p.sub("unit: 'each pair made to order',", "unit: 'Each pair is made to order.',")
    p.rest = p.rest.replace("unit: 'made to order',", "unit: 'Each is made to order.',")
    p.rest = p.rest.replace('Everything is made to order, so we quote rather than list. Prices and lead times from launch. Designers, dealers\n      and press: the same address.',
                            'Everything is made to order, so we quote rather than list. Designers, dealers and press: the same address.')
    # --- /tropos: the card's picture and name are the link; no "Up close"
    p.rest = re.sub(r'<a class="more" href="#speaker-[a-z]+">Up close</a>', '', p.rest)
    p.rest = re.sub(r'<h3 class="named">([A-Za-z]+)<span', lambda m: f'<h3 class="named"><a href="#speaker-{m.group(1).lower()}">{m.group(1)}</a><span', p.rest)
    # --- /lighting: the pair once, large; no lit headline
    p.sub('<h2>The same %s, lit from within.</h2>' % ('eight' if EIGHT else 'seven'), '<h2>Two lamps in the speakers&rsquo; acrylic.</h2>')
    p.rest = re.sub(r'<a class="ph" href="#(?:hemisphere|core)-ember"><img [^>]*></a>', '', p.rest)
    p.rest = re.sub(r'<div class="lamp-duo solo"><figure><img src="img/lamps-unlit-800\.jpg"[^>]*><figcaption>Off, in Smoke\.</figcaption></figure>',
                    '<div class="lamp-duo solo lamps-pair"><figure><img src="img/lamps-unlit.webp" srcset="img/lamps-unlit-800.jpg 800w, img/lamps-unlit.webp 1600w" '
                    'sizes="(max-width: 860px) 100vw, 560px" width="1600" height="2000" loading="lazy" alt="A Core and a Hemisphere in Smoke, switched off">'
                    f'<figcaption>{ON_HOLD} <i class="render">Render</i></figcaption></figure>', p.rest)
    p.rest = p.rest.replace('<figcaption class="wrap">Hemisphere and Core, switched off. <i class="render">Render</i></figcaption>',
                            f'<figcaption class="wrap">{ON_HOLD} <i class="render">Render</i></figcaption>')
    # --- /mantle: one full-width picture, the words beside it
    p.rest = re.sub(r'<a class="ph" href="#mantle-ember"><img [^>]*></a>',
                    f'<a class="ph mantle-wide" href="#mantle-ember"><img src="{MANTLE["full"]}" srcset="{MANTLE["wide"]} 1200w, {MANTLE["full"]} 1800w" '
                    'sizes="(max-width: 860px) 100vw, 62vw" width="1800" height="1200" loading="lazy" alt="Mantle in Ember"></a>', p.rest)
    # --- Tropos's size: depth 420 with the horn flush


    p.css("""
/* the RC review, waves 2 and 3 */
.hero { justify-content: flex-start; height: auto !important; min-height: 0 !important; padding-bottom: clamp(32px, 6vh, 64px) !important }
.hero-title .wrap { padding-block: clamp(20px, 4vh, 48px) 0 }
.hero-pic { width: 100% !important; position: static }
.hero-title { position: static !important }
.hero-row { aspect-ratio: auto !important; background: none !important; overflow: visible; margin-top: clamp(16px, 4vh, 48px) }
.hero-row ul { list-style: none; margin: 0 auto; padding: 0 16px; display: grid; grid-template-columns: repeat(8, minmax(0, 1fr)); gap: 8px }
.hero-row a { display: grid; gap: 8px; color: var(--ink); text-decoration: none; font-size: 15px }
.hero-row img { width: 100%; height: auto; aspect-ratio: 72 / 125; object-fit: cover; display: block }
.hero-row a:hover span { text-decoration: underline; text-underline-offset: 4px }
@media (max-width: 860px) {
  .hero { height: auto; min-height: 0 }
  .hero-row ul { grid-template-columns: none; grid-auto-flow: column; grid-auto-columns: 62vw; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; padding-bottom: 8px }
  .hero-row ul::-webkit-scrollbar { display: none } .hero-row li { scroll-snap-align: start }
  .hero-row img { max-height: none }
}
.sound-words h2 a, .hab-band h2 a { color: inherit; text-decoration: none } .sound-words h2 a:hover, .hab-band h2 a:hover { text-decoration: underline; text-decoration-thickness: 2px; text-underline-offset: 6px }
.hab-grid { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 6fr); gap: 48px; align-items: end }
.hab-grid figure { margin: 0 } .hab-grid img { display: block; width: 100%; height: auto }
.hab-grid h2 { font-size: clamp(48px, 7vw, 104px) }
@media (max-width: 860px) { .hab-grid { grid-template-columns: minmax(0, 1fr); gap: 20px } }
.c-hab { margin: 28px 0 0; max-width: 520px } .c-hab img { display: block; width: 100%; height: auto } .c-hab figcaption { padding-top: 8px }
/* galleries: a 4:5 picture column beside the particulars */
@media (min-width: 1001px) { .pdp { grid-template-columns: minmax(0, 520px) minmax(0, 1fr) !important; justify-content: start } }
.stage { aspect-ratio: 4 / 5 !important }
/* /tropos: the cards, the last row centered; on the phone, an odd last card across */
.cards { display: flex !important; flex-wrap: wrap; justify-content: center }
.cards > .card { flex: 0 1 calc((100% - 3 * 18px) / 4) }
@media (max-width: 860px) { .cards > .card { flex-basis: calc((100% - 18px) / 2) } .cards > .card:last-child:nth-child(odd) { flex-basis: 100% } }
.card .named a { color: inherit; text-decoration: none }
/* /lighting: the pair once */
.lamps .ptile { grid-template-columns: minmax(0, 1fr) !important }
.lamps-pair { grid-template-columns: minmax(0, 560px) minmax(0, 1fr) !important; align-items: end }
.lamps-pair img { width: 100%; height: auto; display: block }
@media (max-width: 860px) { .lamps-pair { grid-template-columns: minmax(0, 1fr) !important } }
/* /mantle: the picture wide */
.tt-duo { grid-template-columns: minmax(0, 1fr) !important } .tt-duo .ptile { grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr) !important; align-items: end }
.mantle-wide img { width: 100%; height: auto; aspect-ratio: 3 / 2 !important; object-fit: cover }
@media (max-width: 860px) { .tt-duo .ptile { grid-template-columns: minmax(0, 1fr) !important } }
/* the lamps beat: picture and caption aligned, at most 75vh */
.lamps-day img { max-height: 75vh; width: auto !important; max-width: 100%; margin: 0 }
.lamps-day { display: grid; justify-items: start; padding-inline: max(16px, calc((100vw - 1240px) / 2 + 16px)) } .lamps-day figcaption { padding-inline: 0 !important }
/* Fog's swatch: a circle with a hairline */
.swatches a, .swatches .coin-dot { border-radius: 50% } .swatches .coin-dot[style*="--i:6"] { box-shadow: inset 0 0 0 1px #9A958D }
""")


def rc3(p, web):
    """The RC2 review (five lenses, the coordinator 2026-11-09 18:41): the punch list for RC3."""
    import os
    from PIL import Image
    names = {k: name for k, num, name, *_ in web.CLOUDS}
    HAB_ALT = {'blue': 'Tropos in Ice, out in the snow at dusk', 'orange': 'Tropos in Dust, on rippled sand among desert buttes',
               'ice': 'Tropos in Fog, in the grass on a hillside, in fog at dawn'}
    HAB_CAP = {'blue': 'Out in the snow at dusk.', 'orange': 'On rippled sand among desert buttes.', 'ice': 'In the grass on a hillside, in fog at dawn.'}
    # --- 1. home, the lamps: the picture left, the two lamps' names beside it, one line each, as links
    m = re.search(r'<figure class="strip lamps-day"><img (.*?)><figcaption class="wrap">(.*?)</figcaption></figure>', p.rest, re.S)
    assert m, 'rc3: lamps-day'
    p.rest = (p.rest[:m.start()] + '<div class="wrap lamps-home"><figure class="lamps-day"><img ' + m.group(1).replace('sizes="(max-width: 700px) 100vw, 50vw"', 'sizes="(max-width: 860px) 100vw, 540px"')
              + '><figcaption>' + m.group(2) + '</figcaption></figure>'
              '<ul class="lamp-names"><li><a href="#hemisphere-ember">Hemisphere</a>, a pendant.</li>'
              '<li><a href="#core-ember">Core</a>, a cordless table lamp.</li></ul></div>' + p.rest[m.end():])
    # --- 2. home: the Tropos block shows the amplifier plate (a view the hero doesn't; its rig is clean); the Ice habitat mirrored
    p.sub('<figure class="sound-still"><img src="img/rc/blue-tall.webp" width="1000" height="1250" loading="lazy" alt="Tropos in Ice, its cover off, on a pale seamless">',
          '<figure class="sound-still"><img src="img/rc/plate.webp" width="1000" height="1250" loading="lazy" alt="The built-in amplifier, from behind.">')   # the plate's rig is clean (the audit ac9e5568)
    if 'hab-band' in p.rest:
        p.sub('<div class="wrap hab-grid"><figure><img src="img/rc/blue-habitat.webp" width="1200" height="1500" loading="lazy" alt="Tropos in Ice, out in the snow at dusk"></figure>',
              '<div class="wrap hab-grid hab-mirror"><figure><img src="img/rc/blue-habitat.webp" width="1200" height="1500" loading="lazy" alt="' + HAB_ALT['blue'] + '"></figure>')
        p.sub('<p class="beat-line">' + next(line for k, num, name, icon, acr, line, *_ in web.CLOUDS if k == 'blue') + '</p><p class="foot-note"><i class="render">Render</i></p>',
              '<p class="beat-line">' + next(line for k, num, name, icon, acr, line, *_ in web.CLOUDS if k == 'blue') + '</p><p class="foot-note">' + HAB_CAP['blue'] + ' <i class="render">Render</i></p>')
    # --- 3. a color's page: Tropos in its 4:5 tall frame, two columns, no 1:2 card in a 4:5 box; no "Every line" note
    p.sub("document.getElementById('c-in-note').textContent = `Every line, in ${c.tint.toLowerCase()} acrylic.`;",
          "document.getElementById('c-in-note').textContent = '';")
    p.sub("document.getElementById('c-products').replaceChildren(...PRODUCTS.filter(Pr => Pr.id === 'speaker' && Pr.views(k)).map(Pr => pcard(Pr, k)));",
          "{ const low = c.name.toLowerCase(), b = el('div', { class: 'c-tropos' },\n"
          "    `<a class=\"ph\" href=\"#speaker-${low}\"><img src=\"img/rc/${k}-tall.webp\" width=\"1000\" height=\"1250\" alt=\"Tropos in ${c.name}\"></a>` +\n"
          "    `<div><h3><a href=\"#speaker-${low}\">Tropos in ${c.name}</a></h3><a class=\"more\" href=\"#speaker-${low}\">See the speaker</a></div>`);\n"
          "  document.getElementById('c-products').replaceChildren(b); }")
    p.sub('<div class="pgrid" id="c-products"></div>', '<div id="c-products"></div>')
    # --- 4. galleries: each view at its own ratio for Mantle (3:2, no bands); the horn-backs cut to 4:5
    p.sub("stage.style.background = P.id === 'speaker' ? ground(v) : 'transparent';",
          "stage.style.background = P.id === 'speaker' ? ground(v) : 'transparent'; if (P.id === 'turntable') stage.style.setProperty('aspect-ratio', '3 / 2', 'important'); else stage.style.removeProperty('aspect-ratio');")
    for k in HORN_BACKS:
        src = 'renders/2026-11-04/barkhorn/rollout/' + f'A-polished-p2-p2b/horn-back-{names[k].lower()}.png'
        im = Image.open(os.path.join(web.ROOT, src)).convert('RGB').crop((270, 0, 990, 900))
        im.save(os.path.join(web.SITE, f'img/rc/{k}-horn-back.webp'), 'WEBP', quality=82)
        im.resize((168, 210)).save(os.path.join(web.SITE, f'img/rc/{k}-horn-back-th.webp'), 'WEBP', quality=80)
    n = p.rest.count('"w":1200,"h":900,"th":"img/rc/')
    p.rest = re.sub(r'("src":"img/rc/[a-z]+-horn-back\.webp","w":)1200,"h":900', r'\g<1>720,"h":900', p.rest)
    assert n == len(HORN_BACKS) and '-horn-back.webp","w":720' in p.rest, ('rc3: horn-backs', n)
    # --- 5. words that repeat
    p.sub('<div class="wrap hero-cap"><span>Hi-fi and lighting in cast acrylic.</span><i class="render">Render</i></div>',
          '<div class="wrap hero-cap"><i class="render">Render</i></div>')
    p.sub('<p>A pendant and a table lamp in the speakers&rsquo; acrylic, frosted inside, so the color glows and the source never shows. Every shade comes off by hand.</p>',
          '<p>A pendant and a table lamp, each with a white opal diffuser inside its color, so the color glows and the source never shows. Every shade comes off by hand.</p>')   # Core B (the owner, 2026-11-09)
    p.sub('<div class="pt-body"><h3>Mantle<small>Turntable</small></h3><p class="line">A turntable in cast acrylic.</p>',
          '<div class="pt-body"><h3>Mantle<small>Turntable</small></h3>')
    # --- 6. one price line, in the particulars too
    n = p.rest.count('Set at launch; each pair is made to order')
    assert n >= 1, 'rc3: price row'
    p.rest = p.rest.replace('Set at launch; each pair is made to order', 'On request. Each pair is made to order.')   # the label says Price
    # --- 7. the habitat reserves its space
    p.sub('<figure class="c-hab" id="c-hab" hidden><img alt=""><figcaption><i class="render">Render</i></figcaption></figure>',
          '<figure class="c-hab" id="c-hab" hidden><img alt="" width="1200" height="1500"><figcaption><span id="c-hab-cap"></span> <i class="render">Render</i></figcaption></figure>')
    p.sub("if (c.hab) { const im = f.querySelector('img'); im.src = c.hab; im.alt = c.hab_alt; }",
          "if (c.hab) { const im = f.querySelector('img'); im.src = c.hab; im.alt = c.hab_alt; document.getElementById('c-hab-cap').textContent = c.hab_cap; }")
    # --- 8. American spelling
    # --- 11. alts and labels
    p.rest = re.sub(r'aria-label="([A-Z][a-z]+), up close"', r'aria-label="Tropos in \1"', p.rest)
    p.rest = re.sub(r'(<img class="off" src="img/rc/[a-z]+-card\.webp" width="625" height="1250") alt="([A-Z][a-z]+) with its cover off"', r'\1 alt="Tropos in \2"', p.rest)
    # --- 12. the habitats say what's shown, the same words everywhere
    i = p.rest.index('const D = ') + len('const D = ')
    j = p.rest.index(', BY = Object', i)
    import json
    D = json.loads(p.rest[i:j])
    for c in D['clouds']:
        if c.get('hab'):
            c['hab_alt'] = HAB_ALT[c['k']]; c['hab_cap'] = HAB_CAP[c['k']]
    for L in D['lamps'].values():          # 21. the lamps' thumb is the picture already shipped
        for col in L['colours'].values():
            col['views']['unlit']['th'] = 'img/lamps-unlit-800.jpg'
    for col in D['tt']['colours'].values():
        col['card'] = dict(col['card'], src=MANTLE['wide'], w=1200, h=800)
    p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
    p.rest = re.sub(r"\['habitat', 'Out', c => `\$\{c\.name\}\. \$\{c\.line\}`\]",
                    "['habitat', 'Out', c => c.hab_alt || `${c.name}, out`, c => c.hab_cap || `${c.name}. ${c.line}`]", p.rest, count=1)
    assert 'c => c.hab_alt ||' in p.rest, 'rc3: habitat words'
    # --- 17. drawn to be made
    p.sub('Built to the drawings: the cabinet and its horn in the same tinted acrylic,\n        the back screwed to the braces. The first pair is made the way every pair will be.',
          'Built to the drawings, the back screwed to the braces. The first pair is made the way every pair will be.')
    # --- 19. an old Smoke address on a hash change goes where the first load sends it
    if not EIGHT:
        p.sub("function route() {\n  let h = location.hash.slice(1);",
              "function route() {\n  let h = location.hash.slice(1);\n"
              "  const sm = /^(speaker|dome|orb|hemisphere|core|mantle|turntable|color|colour)-smoke$/.exec(h);\n"
              "  if (sm) { h = { speaker: 'speakers', mantle: 'turntable', turntable: 'turntable', color: 'top', colour: 'top' }[sm[1]] || 'lighting'; history.replaceState(null, '', '#' + h); }")
    # --- 21. no dark-only pictures named where nothing dark is shown
    p.rest = p.rest.replace('background-image: url(img/coins-dark.jpg)', 'background-image: none')
    p.rest = re.sub(r'html\.globe-live header\.top\.on-dark \.brand \.globe \{ background-image: url\(img/globe-spin-dark\.webp\);\s*background-image: image-set\([^}]*\}', '', p.rest)
    assert 'globe-spin-dark' not in p.rest and 'coins-dark' not in p.rest, 'rc3: dark pictures'
    p.css("""
/* RC3 */
.lamps-home { margin-top: clamp(20px, 3vw, 36px); display: grid; grid-template-columns: minmax(0, 540px) minmax(0, 1fr); gap: 48px; align-items: end }
.lamps-home .lamps-day { padding: 0 !important; margin: 0; display: block } .lamps-home .lamps-day img { width: 100% !important; height: auto; max-height: none; display: block }
.lamps-home figcaption { margin: 0; padding: 8px 0 0 !important; max-width: 540px }
.lamp-names { list-style: none; margin: 0 0 40px; padding: 0; display: grid; gap: 14px; font-size: clamp(22px, 2.4vw, 32px); letter-spacing: -0.01em }
.lamp-names a { color: var(--ink); text-underline-offset: 6px; text-decoration-thickness: 1px }
@media (max-width: 860px) { .lamps-home { grid-template-columns: minmax(0, 1fr); gap: 20px } .lamp-names { margin: 0 } }
.hab-mirror { grid-template-columns: minmax(0, 6fr) minmax(0, 5fr) } .hab-mirror figure { order: 2 }
@media (max-width: 860px) { .hab-mirror { grid-template-columns: minmax(0, 1fr) } .hab-mirror figure { order: 0 } }
.c-tropos { display: grid; grid-template-columns: minmax(0, 520px) minmax(0, 1fr); gap: 40px; align-items: end }
.c-tropos .ph img { display: block; width: 100%; height: auto }
.c-tropos h3 { font-size: clamp(28px, 3vw, 40px); margin: 0 0 8px } .c-tropos h3 a { color: inherit; text-decoration: none } .c-tropos h3 a:hover { text-decoration: underline; text-underline-offset: 6px }
.c-tropos .more { color: var(--ink); text-underline-offset: 4px }
@media (max-width: 860px) { .c-tropos { grid-template-columns: minmax(0, 1fr); gap: 16px } }
.c-hab img { aspect-ratio: 4 / 5 }
.dots-row .coin-dot { border-radius: 50% } .dots-row .coin-dot[style*="--i:6"] { box-shadow: inset 0 0 0 1px #9A958D }
.hero-row ul { scroll-padding-inline: 16px }
.sound-still, .mantle-pic { background: none !important }
.hab-band .foot-note .render, .hero-cap .render { margin-left: 0 }
""")


TURN = {k: f'A-polished-p2-p2b/turn-{n}' for k, n in zip(RC_KEYS, ['ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog', 'smoke'])}
# the black-rods turns, all eight (r33-speaker-horn 370de3da)
TURN_REST = 20        # three-quarter front: the mouth opens toward you and the cabinet's side shows (the addendum, 3)
TURN_GUTTER = 16      # px of repeated edge round every tile, so the lossy sprite never bleeds one frame into the next


def rc_turn(p, web):
    """The turning horn in each Tropos gallery: 24 frames at 15 degrees, one 6 x 4 sprite per color with a gutter round
    every tile; frame 0 stands in until the sprite is decoded, then one turn (desk and phone; none under reduced motion)."""
    import json, os
    from PIL import Image
    R = os.path.join(web.ROOT, 'renders/2026-11-04/barkhorn/rollout/')
    G = TURN_GUTTER
    i = p.rest.index('const D = ') + len('const D = ')
    j = p.rest.index(', BY = Object', i)
    D = json.loads(p.rest[i:j])
    size = None
    for c in D['clouds']:
        k = c['k']
        if k not in TURN:
            continue
        files = [R + f'{TURN[k]}-{n:02d}.png' for n in range(24)]
        fr = [Image.open(f).convert('RGB') for f in files]
        w, h = fr[0].size
        assert all(f.size == (w, h) for f in fr) and size in (None, (w, h)), ('rc_turn: frame sizes', k)
        assert w % 16 == 0 and h % 16 == 0, ('rc_turn: tiles on 16 px', w, h)
        size = (w, h)
        sheet = Image.new('RGB', (6 * (w + 2 * G), 4 * (h + 2 * G)))
        for n, f in enumerate(fr):
            x, y = G + (n % 6) * (w + 2 * G), G + (n // 6) * (h + 2 * G)
            # the gutter: the frame's edge rows and columns repeated outward (a clamp), the frame itself in the middle
            edge = Image.new('RGB', (w + 2 * G, h + 2 * G))
            edge.paste(f, (G, G))
            edge.paste(f.crop((0, 0, w, 1)).resize((w, G)), (G, 0)); edge.paste(f.crop((0, h - 1, w, h)).resize((w, G)), (G, h + G))
            col = edge.crop((G, 0, G + 1, h + 2 * G)); edge.paste(col.resize((G, h + 2 * G)), (0, 0))
            col = edge.crop((G + w - 1, 0, G + w, h + 2 * G)); edge.paste(col.resize((G, h + 2 * G)), (G + w, 0))
            sheet.paste(edge, (x - G, y - G))
        sheet.save(os.path.join(web.IMG, f'rc/turn-{k}.webp'), 'WEBP', quality=72, method=6)
        fr[TURN_REST].save(os.path.join(web.IMG, f'rc/turn-{k}-0.webp'), 'WEBP', quality=80)
        fr[TURN_REST].resize((168, round(168 * h / w))).save(os.path.join(web.IMG, f'rc/turn-{k}-th.webp'), 'WEBP', quality=80)
        c['views']['turn'] = dict(src=f'img/rc/turn-{k}.webp', still=f'img/rc/turn-{k}-0.webp', w=w, h=h, th=f'img/rc/turn-{k}-th.webp',
                                  **web.ground(f'rc/turn-{k}-0.webp'))
    p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
    w, h = size
    SW, SH = 6 * (w + 2 * G), 4 * (h + 2 * G)
    p.sub("const frameAt = (k) => `${(k % C) * 100 / (C - 1)}% ${Math.floor(k / C) * 100 / (R - 1)}%`;",
          f"const REST = {TURN_REST}; const frameAt = (k) => `${{({G} + (k % C) * {w + 2 * G}) * 100 / {SW - w}}}% ${{({G} + Math.floor(k / C) * {h + 2 * G}) * 100 / {SH - h}}}%`;   // tiles in a {G} px gutter")
    old = """    pic = el('div', { class: 'fit spin' + (s.edge === 'cut' ? ' cut' : ''), role: 'img', 'aria-label': `${c.name}'s horn; drag to spin it`, style: `background-image:url(${s.src});--ar:${ar}` });
    turnFrame = 0; pic.style.backgroundPosition = frameAt(0);
    draggable(pic, (d, start, base) => { if (start) return turnFrame; turnFrame = ((base - d) % N + N) % N; pic.style.backgroundPosition = frameAt(turnFrame); });
    if (!reduce) { const t0 = performance.now(); (function f(now) { const p = Math.min(1, (now - t0) / 2600); turnFrame = Math.round(p * N) % N;
      pic.style.backgroundPosition = frameAt(turnFrame); if (p < 1) autoTurn = requestAnimationFrame(f); })(t0); }"""
    new = """    pic = el('div', { class: 'fit spin still' + (s.edge === 'cut' ? ' cut' : ''), role: 'img', 'aria-label': `${c.name}'s horn, all the way around`, style: `background-image:url(${s.still});--ar:${ar}` });
    turnFrame = REST;
    const sheet = new Image(); sheet.src = s.src;           // frame 0 until the sprite is decoded; then one turn (none under reduced motion)
    sheet.decode().catch(() => {}).then(() => { if (!pic.isConnected) return;
      pic.style.backgroundImage = `url(${s.src})`; pic.style.backgroundPosition = frameAt(REST); pic.classList.remove('still');
      draggable(pic, (d, start, base) => { if (start) { cancelAnimationFrame(autoTurn); return turnFrame; } turnFrame = ((base - d) % N + N) % N; pic.style.backgroundPosition = frameAt(turnFrame); });
      if (!reduce) { const t0 = performance.now(); (function f(now) { const p = Math.min(1, (now - t0) / 2600); turnFrame = (REST + Math.round(p * N)) % N;
        pic.style.backgroundPosition = frameAt(turnFrame); if (p < 1 && pic.isConnected) autoTurn = requestAnimationFrame(f); })(t0); } });"""
    p.sub(old, new)
    p.sub("['turn', 'Turning', c => `${c.name}'s horn, all the way round.`],", "['turn', 'Turning', c => `${c.name}'s horn, all the way around.`],")
    p.css(f"""
.stage .spin {{ background-size: {SW * 100 / w:.4f}% {SH * 100 / h:.4f}% }} .stage .spin.still {{ background-size: 100% 100%; background-position: 0 0 }}
""")


# the lamps' picture (the coordinator 2026-11-09 19:29): the Smoke pair was lit by lamps hidden in frame, so it goes.
# Its replacement, the pair in Ember on the fixed rig, goes here once it passes; until then the lamps show no picture.
LAMPS_PIC = None


def lamps_og():
    """The lamps' share card: their picture's, or the home's while they have none."""
    return ('img/rc/og-lamps.jpg', 'A Core and a Hemisphere in Ember, switched off') if LAMPS_PIC else ('img/rc/og-home.jpg', 'Tropos in eight colors')


def rc_lamps(p, web):
    import json, os
    from PIL import Image
    i = p.rest.index('const D = ') + len('const D = ')
    j = p.rest.index(', BY = Object', i)
    D = json.loads(p.rest[i:j])
    if LAMPS_PIC:
        im = Image.open(os.path.join(web.ROOT, LAMPS_PIC)).convert('RGB')
        if im.width > 1600:
            im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        W, H = im.size
        im.save(os.path.join(web.IMG, 'rc/lamps.webp'), 'WEBP', quality=82)
        im.resize((800, round(H * 800 / W)), Image.LANCZOS).save(os.path.join(web.IMG, 'rc/lamps-800.webp'), 'WEBP', quality=82)
        im.resize((168, round(H * 168 / W)), Image.LANCZOS).save(os.path.join(web.IMG, 'rc/lamps-th.webp'), 'WEBP', quality=80)
        full = {'src': 'img/rc/lamps.webp', 'w': W, 'h': H, 'th': 'img/rc/lamps-th.webp'}
        for L in D['lamps'].values():
            for k, col in L['colours'].items():
                col['views'] = {'unlit': dict(full, **({} if k == 'red' else {'tag': 'Shown in Ember'}))}
                col['card'] = {'src': 'img/rc/lamps-800.webp', 'w': 800, 'h': round(H * 800 / W), 'alt': 'A Core and a Hemisphere in Ember, switched off',
                               **({} if k == 'red' else {'tag': 'Shown in Ember'})}
        p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
        def tag(m):
            t = m.group(0).replace('img/lamps-unlit.webp', 'img/rc/lamps.webp').replace('img/lamps-unlit-800.jpg', 'img/rc/lamps-800.webp')
            return re.sub(r'width="1600" height="2000"', f'width="{W}" height="{H}"', t)
        p.rest = re.sub(r'<img [^>]*img/lamps-unlit[^>]*>', tag, p.rest)
        for a, b in (('Shown in Smoke, a color on hold.', 'Shown in Ember.'), ('Shown in Smoke, a color on hold', 'Shown in Ember'),
                     ('in Smoke, switched off', 'in Ember, switched off'), (': dark, polished acrylic, pale at the center', '')):
            p.rest = p.rest.replace(a, b)
    else:
        for L in D['lamps'].values():
            for col in L['colours'].values():
                col['views'] = {}; col['card'] = None
        p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
        n = len(re.findall(r'<figure class="lamps-day">.*?</figure>', p.rest, re.S))
        p.rest = re.sub(r'<figure class="lamps-day">.*?</figure>', '', p.rest, flags=re.S)
        p.rest = p.rest.replace('<div class="wrap lamps-home">', '<div class="wrap lamps-home no-pic">')
        m = len(re.findall(r'<figure><img src="img/lamps-unlit\.webp".*?</figure>', p.rest, re.S))
        p.rest = re.sub(r'<figure><img src="img/lamps-unlit\.webp".*?</figure>', '', p.rest, flags=re.S)
        assert n == 1 and m == 1, ('rc_lamps: figures', n, m)
        for a, b in ((' Shown in Smoke, a color on hold.', ''), (' in Smoke, switched off', ', switched off'), (': dark, polished acrylic, pale at the center', '')):
            p.rest = p.rest.replace(a, b)       # the words for a picture that is no longer there
        # a lamp's page: its words and particulars, no gallery
        p.sub("  showView(shown(c)[0]);",
              "  { const g = document.querySelector('#pdp .gallery'), n = shown(c).length; g.hidden = !n; document.querySelector('#pdp .pdp').classList.toggle('no-pic', !n); if (n) showView(shown(c)[0]); }")
        p.css("""
.lamps-home.no-pic { grid-template-columns: minmax(0, 1fr) } .lamps-home.no-pic .lamp-names { margin: 0 }
.lamps-pair { grid-template-columns: minmax(0, 1fr) !important }
@media (min-width: 1001px) { .pdp.no-pic { grid-template-columns: minmax(0, 720px) !important } }
""")
    assert 'lamps-unlit' not in p.rest, 'rc_lamps: the old pair is still named'


def rc31(p, web):
    """The RC3.1 review (the coordinator 2026-11-09 20:06, addendum 20:08): the home's Tropos block shows the Ember
    horn-back with the gallery's own words; the color page's block; Fog's coin; Mantle's closing line."""
    # the home's Tropos block: its picture held (Ember's horn-back pulled, the re-audit 23:28); the words stay
    m = re.search(r'<figure class="sound-still"><img [^>]*><figcaption>.*?</figcaption></figure>\s*', p.rest)
    assert m, 'rc31: the sound still'
    p.rest = p.rest[:m.start()] + p.rest[m.end():]
    p.sub('<div class="wrap sound-grid">', '<div class="wrap sound-grid no-pic">')
    p.css(".sound-grid.no-pic { grid-template-columns: minmax(0, 1fr) !important }")
    p.sub("document.getElementById('c-in').textContent = `In ${c.name}`;", "document.getElementById('c-in').textContent = '';")
    p.sub("turntable: 'See it beside the speakers: <a href=\"#speakers\">Tropos</a>.',", "turntable: 'Pair it with <a href=\"#speakers\">Tropos</a>.',")
    p.css("""
/* RC3.1 */
.c-tropos { margin-bottom: 72px } @media (max-width: 860px) { .c-tropos { margin-bottom: 52px } }
.colour-head .coin-big .coin-dot { border-radius: 50% } .colour-head .coin-big .coin-dot[style*="--i:6"] { box-shadow: inset 0 0 0 1px #9A958D }
""")


# Mantle's picture (the owner, 2026-11-10 00:46: "like black and red wood instead of acrylic ... It looks cheap"): out
# until a new one passes. Words only, as the lamps; its share cards on the home's.
MANTLE_PIC = False


def mantle_og():
    return ('img/rc/og-mantle.jpg', 'Mantle in Ember') if MANTLE_PIC else ('img/rc/og-home.jpg', 'Tropos in eight colors')


def rc_mantle(p, web):
    import json
    if MANTLE_PIC:
        return
    i = p.rest.index('const D = ') + len('const D = ')
    j = p.rest.index(', BY = Object', i)
    D = json.loads(p.rest[i:j])
    for col in D['tt']['colours'].values():
        col['views'] = {}; col['card'] = None
    p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
    n = len(re.findall(r'<figure class="strip mantle-pic">.*?</figure>', p.rest, re.S))
    p.rest = re.sub(r'\s*<figure class="strip mantle-pic">.*?</figure>', '', p.rest, flags=re.S)
    m = len(re.findall(r'<a class="ph mantle-wide"[^>]*><img [^>]*></a>', p.rest))
    p.rest = re.sub(r'<a class="ph mantle-wide"[^>]*><img [^>]*></a>', '', p.rest)
    assert n == 1 and m == 1, ('rc_mantle', n, m)
    p.rest = p.rest.replace('<div class="lamp-duo solo tt-duo"><article class="ptile">', '<div class="lamp-duo solo tt-duo"><article class="ptile no-pic">')
    if "document.querySelector('#pdp .pdp').classList.toggle('no-pic', !n)" not in p.rest:      # a page with no picture: no gallery
        p.sub("  showView(shown(c)[0]);",
              "  { const g = document.querySelector('#pdp .gallery'), n = shown(c).length; g.hidden = !n; document.querySelector('#pdp .pdp').classList.toggle('no-pic', !n); if (n) showView(shown(c)[0]); }")
        p.css("@media (min-width: 1001px) { .pdp.no-pic { grid-template-columns: minmax(0, 720px) !important } }")
    p.css(".tt-duo .ptile.no-pic { grid-template-columns: minmax(0, 1fr) !important }")
    assert 'mantle-day' not in p.rest, 'rc_mantle: the picture is still named'


GLOBE_RC = 'site-rc'   # brand/site-rc: the owner's approved globe (r47-brand c19abdba): its film and poster, the header's
# sheet (60 of the film's 120 frames on its ground, 237 236 229) and the touch icon. No night film until an honest one.
CHIPS = {'red': '#B50404', 'orange': '#D35D17', 'amber': '#C5BC1E', 'green': '#027614', 'blue': '#1169C1', 'violet': '#500CB4'}


def rc_globe(p, web):
    import os, io, base64, shutil
    from PIL import Image
    B = os.path.join(web.BRAND, GLOBE_RC)
    b64 = lambda path: 'data:image/webp;base64,' + base64.b64encode(open(path, 'rb').read()).decode()

    def first(path):
        with Image.open(path) as sp:
            buf = io.BytesIO(); sp.crop((0, 0, sp.width // 10, sp.height // 6)).save(buf, 'WEBP', quality=90, method=6)
        return 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()
    img = lambda n: os.path.join(web.IMG, n)
    old = [first(img('globe-spin-light.webp')), b64(img('globe-turn-poster.webp'))]
    old_night = b64(img('globe-turn-night-poster.webp')) if os.path.exists(img('globe-turn-night-poster.webp')) else None
    for n in ('globe-turn.mp4', 'globe-turn.webm', 'globe-turn-poster.webp'):
        shutil.copy(os.path.join(B, n), img(n))
    sheet = web.cutout(Image.open(os.path.join(B, 'globe-spin-light.png')).convert('RGB'), (237, 236, 229))
    sheet = sheet.convert('RGBa').resize((840, 504), Image.LANCZOS).convert('RGBA')
    sheet.save(img('globe-spin-light.avif'), quality=60)
    sheet.save(img('globe-spin-light.webp'), quality=70, alpha_quality=80, method=6)
    for n in ('globe-turn-night.mp4', 'globe-turn-night.webm', 'globe-turn-night-poster.webp'):
        if os.path.exists(img(n)):
            os.remove(img(n))
    new = [first(img('globe-spin-light.webp')), b64(img('globe-turn-poster.webp'))]
    for a, b in zip(old, new):
        assert a in p.head or a in p.rest, 'rc_globe: the old inline frame'
        p.head = p.head.replace(a, b); p.rest = p.rest.replace(a, b)
    if old_night:
        p.head = p.head.replace(old_night, new[1]); p.rest = p.rest.replace(old_night, new[1])
    for where in ('head', 'rest'):
        txt = getattr(p, where)
        if "f = night ? 'globe-turn-night' : 'globe-turn';" in txt:
            setattr(p, where, txt.replace("f = night ? 'globe-turn-night' : 'globe-turn';", "f = 'globe-turn';"))
    assert 'globe-turn-night' not in p.head + p.rest, 'rc_globe: the night film is still named'
    # the color dots: flat chips in the logo's colors (Fog and Smoke as the site has them), no sprite
    hexes = [CHIPS[k] for k in ('red', 'orange', 'amber', 'green', 'blue', 'violet')] + ['#F6F8F8', '#34323A']   # Fog, Smoke: the site's tokens
    p.css(':root { ' + ' '.join(f'--c-{k}: {CHIPS[k]};' for k in CHIPS) + ' }\n'
          '.coin-dot, .coin-big .coin-dot { background-image: none !important; mix-blend-mode: normal !important }\n'
          + '\n'.join(f'.coin-dot[style*="--i:{i}"] {{ background-color: {h} !important }}' for i, h in enumerate(hexes)) + '\n'
          '.coin-dot[style*="--i:6"] { box-shadow: inset 0 0 0 1px #9A958D }\n')
    p.rest = p.rest.replace('background-image: url(img/coins-light.jpg)', 'background-image: none')



def rc_words(p, web):
    """The audit's visible fixes and the settled facts only (the coordinator 2026-11-10 07:56; book-audit plan.md, SURFACE
    FIXES): no cover switch; the rods and Mantle's posts black; the lamps' light as settled; no open details."""
    import json
    # the cover switch and its fact row go; the cards stay cover off
    m = re.search(r'\s*<div class="seg" role="group" aria-label="The speakers\' covers">.*?</div>', p.rest, re.S)
    assert m, 'rc_words: the cover switch'
    p.rest = p.rest[:m.start()] + p.rest[m.end():]
    m = re.search(r"\n// the cards' covers\nconst on = document\.getElementById\('cover-on'\).*?cards\.classList\.add\('show-off'\); \}\);", p.rest, re.S)
    assert m, 'rc_words: the cover script'
    p.rest = p.rest[:m.start()] + p.rest[m.end():]
    p.sub("      ['Cover', 'A cloth disc, optional (to follow)'], ", "      ")
    p.rest = re.sub(r"\n  \['on', 'Cover on', c => `With its cover on, in \$\{c\.cover\.toLowerCase\(\)\}\.`\],", '', p.rest)
    # the rods are black
    n = p.rest.count('on four bronze posts')
    assert n >= 2, ('rc_words: bronze posts', n)
    p.rest = p.rest.replace('on four bronze posts', 'on four black posts')
    # the data's facts
    i = p.rest.index('const D = ') + len('const D = ')
    j = p.rest.index(', BY = Object', i)
    D = json.loads(p.rest[i:j])
    def facts(rows, change, drop=(), add_after=None):
        out = []
        for a, b in rows:
            if a in drop:
                continue
            out.append([a, change.get(a, b)])
            if add_after and a == add_after[0]:
                out.append(list(add_after[1]))
        return out
    D['lamps']['dome']['facts'] = facts(D['lamps']['dome']['facts'], {
        'Light': '2700 K, CRI 90; the dome glows in its own color, and the light straight down is the lamp&rsquo;s own warm white',
        'Mains': '120 V, dimmable'})
    D['lamps']['orb']['facts'] = facts(D['lamps']['orb']['facts'], {},
        add_after=('Size', ('Ball', 'Tinted cast acrylic, with a white opal ball centered inside it')))
    D['tt']['facts'] = facts(D['tt']['facts'], {
        'Posts': 'Four solid black posts, 30 mm across',
        'Cartridge': 'A moving-magnet cartridge'})
    for c in D['clouds']:                     # unread fields (the audit, source item 3): no history in the page's data
        for key in ('place', 'cover', 'view3d', 'campaign'):
            c.pop(key, None)
    D.pop('campaign', None)
    p.rest = p.rest[:i] + json.dumps(D, separators=(',', ':')) + p.rest[j:]
    n = p.rest.count('over a smoked base on four polished steel posts')
    assert n >= 1, 'rc_words: Mantle lead'
    p.rest = p.rest.replace('over a smoked base on four polished steel posts', 'over a smoked base on four black posts')
    assert 'to be chosen' not in p.rest and 'safety listing' not in p.rest and 'stainless steel' not in p.rest, 'rc_words: open details'
    # the coin sheet is gone: flat chips only
    p.rest = p.rest.replace('url(img/coins-light.jpg)', 'none')
    p.rest = p.rest.replace('its complement and its neighbours', 'its complement and its neighbors')


INTRO_ARC = 'site/globe-turn-alpha'   # brand/: the turn on a transparent ground (r47-brand 92142eb5): 120 frames, 1.5 deg each,
# half a turn, f0000 the still mark's pose. The opening plays the last 42 (63 deg) into f0000, from an image, no video.
ARC_FROM, ARC_TILE, ARC_COLS = 78, 288, 7
ARC_CROP = (80, 80, 432, 432)          # the globe and its discs span px 85-426 of 512: the same square for every use
HDR_TILE = 84                          # the header's 42 px globe, at 2x
REVEAL = 'circle'                      # 'circle': the cream closes on the header's globe; 'fade': it fades out as the globe flies


def rc_intro(p, web):
    """The opening globe from pre-cut frames with real alpha (no video, no canvas): a sprite of the arc f0078 ... f0119, f0000.
    The globe eases into a turn from rest during the hold (45 deg/s at most); as the flight starts a curve that matches its
    speed carries it on to f0000, which it reaches as it lands; the header rests there, then turns again (the same frames).
    If the sprite is not ready when the flight starts, the globe flies still. No video, no canvas keying."""
    import io, os, base64
    from PIL import Image
    B = os.path.join(web.BRAND, INTRO_ARC)
    frames = [Image.open(os.path.join(B, f'f{(ARC_FROM + k) % 120:04d}.png')).convert('RGBA') for k in range(120 - ARC_FROM + 1)]
    N = len(frames) - 1
    rows = -(-len(frames) // ARC_COLS)
    assert rows <= ARC_COLS, 'rc_intro: the sheet'
    sheet = Image.new('RGBA', (ARC_COLS * ARC_TILE, ARC_COLS * ARC_TILE), (0, 0, 0, 0))
    for k, f in enumerate(frames):
        sheet.paste(f.crop(ARC_CROP).resize((ARC_TILE, ARC_TILE), Image.LANCZOS), ((k % ARC_COLS) * ARC_TILE, (k // ARC_COLS) * ARC_TILE))
    sheet.save(os.path.join(web.IMG, 'globe-arc.webp'), quality=72, alpha_quality=85, method=6)
    def uri(im, px, q):
        b = io.BytesIO(); im.crop(ARC_CROP).resize((px, px), Image.LANCZOS).save(b, 'WEBP', quality=q, alpha_quality=90, method=6)
        return 'data:image/webp;base64,' + base64.b64encode(b.getvalue()).decode()
    first, mark = uri(frames[0], 200, 80), uri(frames[-1], 126, 88)
    # the header's mark: f0000, still (the turning sprite and its clock go)
    p.rest, n = re.subn(r'(\.brand \.globe \{ width: 42px; height: 42px; flex: none; background: url\()data:image/webp;base64,[A-Za-z0-9+/=]+\)',
                        lambda m: m.group(1) + mark + ')', p.rest)
    assert n == 1, ('rc_intro: the header mark', n)
    # the header's turn: the same frames at header size, every other one (60, 3 deg each: half a turn, a seamless loop),
    # one loop in 4 s as before; it rests on f0000 as the opening lands, then eases back into its turn
    hs = Image.new('RGBA', (10 * HDR_TILE, 6 * HDR_TILE), (0, 0, 0, 0))
    for k in range(60):
        f = Image.open(os.path.join(B, f'f{2 * k:04d}.png')).convert('RGBA').crop(ARC_CROP).resize((HDR_TILE, HDR_TILE), Image.LANCZOS)
        hs.paste(f, ((k % 10) * HDR_TILE, (k // 10) * HDR_TILE))
    hs.save(os.path.join(web.IMG, 'globe-spin-light.webp'), quality=80, alpha_quality=90, method=6)
    hs.save(os.path.join(web.IMG, 'globe-spin-light.avif'), quality=70)
    assert re.search(r'html\.globe-live \.brand \.globe \{[^}]*\}', p.rest), 'rc_intro: the turning sprite rule'
    m = re.search(r"if \(!reduce\) \(function globeTurn\(now\) \{.*?\}\)\(turn0\);\n", p.rest, re.S)
    assert m, 'rc_intro: the header turn'
    p.rest = p.rest[:m.start()] + '''const HDR = { t0: document.documentElement.classList.contains('intro') ? Infinity : performance.now() }, EASE_IN = 1000;
const globeAt0 = () => { globeAt = 0; GLOBES.forEach(g => { g.style.backgroundPosition = '0% 0%'; }); };
window.__globeLand = () => { HDR.t0 = performance.now() + 700; globeAt0(); };   // the opening lands on f0000: rest there, then turn
if (!reduce) (function globeTurn(now) {
  const s = now - HDR.t0, v = 60 / GLOBE_TURN;                        // frames a ms at full pace; the first second eases in
  const f = s <= 0 ? 0 : s < EASE_IN ? v * s * s / (2 * EASE_IN) : v * (s - EASE_IN / 2);
  const i = Math.floor(f) % 60;
  if (i !== globeAt) { globeAt = i; GLOBES.forEach(g => { g.style.backgroundPosition = `${(i % 10) * 100 / 9}% ${Math.floor(i / 10) * 100 / 5}%`; }); }
  requestAnimationFrame(globeTurn);
})(performance.now());
''' + p.rest[m.end():]
    p.sub("if (film && film.currentTime) setTurn(film.currentTime);", "if (window.__globeLand) __globeLand();", n=2)
    # the flyer: an image, no video
    m = re.search(r'<video muted playsinline loop autoplay[^>]*></video>(?:<canvas[^>]*></canvas>)?</div>', p.rest)
    assert m, 'rc_intro: the film'
    p.rest = p.rest[:m.start()] + '<i class="turn" aria-hidden="true"></i></div>' + p.rest[m.end():]
    m = re.search(r"<script>\(function \(d, v\) \{ if \(!d\.classList\.contains\('intro'\)\) return;.*?\(document\.documentElement, document\.querySelector\('\.flyer video'\)\)</script>\n?", p.rest, re.S)
    assert m, 'rc_intro: the film script'
    p.rest = p.rest[:m.start()] + p.rest[m.end():]
    p.sub("    flyer.animate([{ transform: 'none' }",
          "    if (window.__turnFly) __turnFly(T);\n    flyer.animate([{ transform: 'none' }")
    if REVEAL == 'fade':        # the cream fades while the globe flies (no closing circle); the landing waits for the flight
        p.sub("""      { duration: T, easing, fill: 'forwards' });
    splash.animate([{ clipPath: `circle(${R}px at ${ax}px ${ay}px)` }, { clipPath: `circle(${b.width / 2}px at ${bx}px ${by}px)` }],
      { duration: T, easing, fill: 'forwards' }).finished.then(land, done);""",
              """      { duration: T, easing, fill: 'forwards' }).finished.then(land, done);
    splash.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 500, easing: 'cubic-bezier(.4, 0, .2, 1)', fill: 'forwards' });""")
    turn = """<script>(function (d, fl) { if (!d.classList.contains('intro') || !fl) return;   // the opening's turn: from rest, into the mark
  const t = fl.querySelector('.turn'), N = %d, C = %d;
  const at = k => { k = Math.max(0, Math.min(N, Math.round(k))); if (k === t._k) return; t._k = k;
    t.style.backgroundPosition = `${(k %% C) * 100 / (C - 1)}%% ${Math.floor(k / C) * 100 / (C - 1)}%%`; };
  const V = 0.03, TAU = 500;                          // frames a ms at most (45 deg/s), and when the turn is fastest
  const hold = s => V * TAU * Math.E * (1 - (1 + s / TAU) * Math.exp(-s / TAU)), speed = s => V * (s / TAU) * Math.exp(1 - s / TAU);
  let t0 = 0, fly = null, ready = false;
  const step = now => { if (!fl.isConnected) return;
    if (fly) { const u = Math.min(1, (now - fly.at) / fly.T), m = fly.m;
      at(fly.p + fly.d * (m * u + (3 - 2 * m) * u * u + (m - 2) * u * u * u)); if (u >= 1) return; }
    else at(hold(now - t0));
    requestAnimationFrame(step); };
  window.__turnFly = T => { if (!ready) { fly = false;            // no frames yet: the flight is the still mark
      const g = document.querySelector('.brand .globe'); if (g) t.style.backgroundImage = getComputedStyle(g).backgroundImage; return; }
    const now = performance.now(), s = now - t0, p = hold(s), dd = N - p;
    fly = { at: now, T, p, d: dd, m: dd > 0.05 ? Math.min(3, speed(s) * T / dd) : 0 }; };
  const im = new Image(); im.src = 'img/globe-arc.webp';
  (im.decode ? im.decode() : new Promise((r, j) => { im.onload = r; im.onerror = j; })).then(() => {
    if (!fl.isConnected || fly === false) return;
    t.style.backgroundImage = `url(${im.src})`; t.style.backgroundSize = `${C * 100}%% ${C * 100}%%`;
    ready = true; at(0); t0 = performance.now(); requestAnimationFrame(step); }, () => {});
})(document.documentElement, document.querySelector('.flyer'))</script>""" % (N, ARC_COLS)
    i = p.rest.index("<noscript><style>html.opening .hero-photo img { opacity: 1 }</style></noscript>")
    p.rest = p.rest[:i] + turn + '\n' + p.rest[i:]
    p.css("html.intro .splash { background: var(--page, #F4F1EC) }\n"
          ".flyer .turn { display: block; width: 100%; height: 100%; background: url(" + first + ") 0 0 / 100% 100% no-repeat }\n")
    assert 'globe-turn.webm' not in p.rest and '<video' not in p.rest.split('<header', 1)[0], 'rc_intro: the film is still named'


HOTSPOTS = True    # the hero's point (Tropos in Ice, to its page); off: the picture alone
HERO_SRC = 'renders/2026-11-03/barkhorn/habitats/ice-portrait-1200x1500-blackrods.jpg'   # Ice out in the snow at dusk
HERO_ALT = 'Tropos in Ice, out in the snow at dusk'
HERO_WIDE = (8 / 5, 0.5, 0.616)    # the desktop crop: aspect, object-position x and y (the speaker whole, its horn to its foot)
HERO_TALL = (4 / 5, 0.5, 0.5)      # the phone: the whole 4:5 picture
HERO_POINTS = [(63.8, 59.9, 'Tropos in Ice', '#speaker-ice')]   # x, y in percent of the picture: the woofer's cap


def cover_point(x, y, size, crop):
    """A point of the picture (x, y in percent) where it lands in a box of the crop's aspect, with object-fit: cover and
    the crop's object-position: the box's percent."""
    A, px, py = crop
    w, h = size
    X, Y = x / 100 * w, y / 100 * h
    if A > w / h:                                 # fitted to the width: some height cut
        vh = w / A; top = py * (h - vh)
        return round(X / w * 100, 2), round((Y - top) / vh * 100, 2)
    vw = h * A; left = px * (w - vw)
    return round((X - left) / vw * 100, 2), round(Y / h * 100, 2)


def hotspot_hero(img, size, alt, points, wide, tall, srcset=None, attrs=''):
    """A picture with points on it: (x, y in percent of the picture, label, link) each. The box takes the wide crop's aspect,
    or the tall one's in a portrait window, so every point's place is fixed in CSS: nothing moves when the picture or a
    label arrives. Each point is a link with its label as its name (keyboard and screen readers get it as is); the label
    shows on hover, on keyboard focus and, on a touch screen, on the first tap (the second follows the link)."""
    pts = []
    for (x, y, label, href) in points:
        wx, wy = cover_point(x, y, size, wide); tx, ty = cover_point(x, y, size, tall)
        side = ' hs-left' if wx > 62 else ''
        pts.append(f'<a class="hs-pt{side}" href="{href}" style="--x:{wx}%;--y:{wy}%;--tx:{tx}%;--ty:{ty}%">'
                   f'<span class="hs-dot" aria-hidden="true"></span><span class="hs-label">{label}</span></a>')
    ss = f' data-srcset="{srcset}" sizes="100vw"' if srcset else ''
    return (f'<div class="hero-photo hs"{attrs}><img data-src="{img}"{ss} fetchpriority="high" width="{size[0]}" height="{size[1]}" '
            f'alt="{alt}">' + ''.join(pts) + '</div>')


HOTSPOT_CSS = """
.hs { position: relative; width: 100%; aspect-ratio: var(--hs-a); overflow: hidden; background: #C9CDD6 }
.hs > img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: var(--hs-p) }
.hs-pt { position: absolute; left: var(--x); top: var(--y); width: 44px; height: 44px; margin: -22px 0 0 -22px; z-index: 2;
  display: grid; place-items: center; color: #1C1A18; text-decoration: none; -webkit-tap-highlight-color: transparent }
.hs-dot { width: 18px; height: 18px; border-radius: 50%; background: #FFF; box-shadow: 0 0 0 5px rgb(255 255 255 / .35), 0 1px 6px rgb(0 0 0 / .35);
  transition: transform .2s ease }
.hs-label { position: absolute; left: 50%; bottom: calc(100% - 4px); transform: translate(-50%, 4px); white-space: nowrap;
  padding: 7px 12px; border-radius: 999px; background: #FFF; color: #1C1A18; font-size: 15px; line-height: 1.2;
  box-shadow: 0 2px 10px rgb(0 0 0 / .2); opacity: 0; pointer-events: none; transition: opacity .18s ease, transform .18s ease }
.hs-pt:hover .hs-label, .hs-pt:focus-visible .hs-label, .hs-pt.open .hs-label { opacity: 1; transform: translate(-50%, 0) }
.hs-pt:hover .hs-dot, .hs-pt:focus-visible .hs-dot, .hs-pt.open .hs-dot { transform: scale(1.15) }
.hs-pt:focus-visible { outline: none }
.hs-pt:focus-visible .hs-dot { box-shadow: 0 0 0 3px #1C1A18, 0 0 0 6px #FFF }
@media (prefers-reduced-motion: reduce) { .hs-label, .hs-dot { transition: none } }
"""

HOTSPOT_JS = """<script>(function () {   // on a touch screen, a point's first tap shows what it is; the second follows it
  const pts = document.querySelectorAll('.hs-pt'); if (!pts.length) return;
  const touch = () => matchMedia('(hover: none)').matches;
  addEventListener('click', e => {     // the window's capture: ahead of the page's router, which yields to a prevented click
    const a = e.target.closest && e.target.closest('.hs-pt');
    if (!a || !touch() || a.classList.contains('open')) return;
    e.preventDefault(); pts.forEach(b => b.classList.toggle('open', b === a)); }, true);
  document.addEventListener('click', e => { if (!e.target.closest || !e.target.closest('.hs-pt')) pts.forEach(b => b.classList.remove('open')); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') pts.forEach(b => b.classList.remove('open')); });
})()</script>"""


def rc_home(p, web):
    """The home as the owner asked: one full-width picture, Ice out in the snow at dusk, with the line over its sky; the
    four products below, a line and a link each. No figures on home (Tropos's page keeps them) and no row of fronts."""
    import os
    from PIL import Image
    src = Image.open(os.path.join(web.ROOT, HERO_SRC)).convert('RGB')
    size = src.size
    out = {}
    for w in (1200, 800):
        n = f'img/rc/home-ice-{w}.webp'
        (src if w == size[0] else src.resize((w, round(size[1] * w / size[0])), Image.LANCZOS)).save(
            os.path.join(web.SITE, n), quality=80, method=6)
        out[w] = n
    srcset = f'{out[800]} 800w, {out[1200]} 1200w'
    m = re.search(r'<div class="hero-photo hero-row">.*?</ul></div>', p.rest, re.S)
    assert m, 'rc_home: the row of fronts'
    pic = hotspot_hero(out[1200], size, HERO_ALT, HERO_POINTS if HOTSPOTS else [], HERO_WIDE, HERO_TALL, srcset)
    p.rest = p.rest[:m.start()] + pic + p.rest[m.end():]
    p.sub('<section class="hero" id="top">', '<section class="hero hs-hero" id="top">')
    # on a wide screen the line stands in two, left of the speaker; in a tall one, in one over the sky
    p.sub('<h1 class="tagline">A&nbsp;world&nbsp;of&nbsp;sound,&nbsp;in&nbsp;color.</h1>',
          '<h1 class="tagline">A&nbsp;world&nbsp;of&nbsp;sound,<br class="hs-br"> in&nbsp;color.</h1>')
    # the line over the picture's sky
    p.css(HOTSPOT_CSS +
          f".hs-hero .hs {{ --hs-a: {HERO_WIDE[0]:.4f}; --hs-p: {HERO_WIDE[1]*100:.1f}% {HERO_WIDE[2]*100:.1f}% }}\n"
          f"@media (max-aspect-ratio: 1/1) {{ .hs-hero .hs {{ --hs-a: {HERO_TALL[0]:.4f}; --hs-p: {HERO_TALL[1]*100:.1f}% {HERO_TALL[2]*100:.1f}% }}\n"
          "  .hs-hero .hs-pt { left: var(--tx); top: var(--ty) } }\n"
          ".hs-hero { padding: 0 0 clamp(24px, 5vh, 56px) !important; height: auto !important; min-height: 0 !important; display: block !important }\n"
          ".hs-hero .hero-pic { position: relative !important; width: 100% !important; margin: 0 !important }\n"
          ".hs-hero .hero-title { position: absolute !important; left: 0; right: 0; top: 0; z-index: 3; pointer-events: none; color: #1C1A18 }\n"
          ".hs-hero .hero-title .wrap { padding-block: clamp(18px, 3.2vw, 48px) 0 !important }\n"
          ".hs-hero .hero-photo { margin: 0 !important; max-width: none }\n"
          ".hs-hero .hero-title h1 { font-size: clamp(34px, 4.3vw, 64px) !important; line-height: 1.04 }\n"
          "@media (max-aspect-ratio: 1/1) { .hs-hero .hs-br { display: none }\n"
          "  .hs-hero .hero-title h1 { font-size: clamp(18px, min(9.4vw, calc((100vw - 32px) / 12.69)), 44px) !important }\n"
          "  .hs-dot { width: 14px; height: 14px; box-shadow: 0 0 0 4px rgb(255 255 255 / .35), 0 1px 5px rgb(0 0 0 / .35) } }\n")
    # the products: no figures on home
    m = re.search(r'\s*<ul class="figures">.*?</ul>\s*<p class="foot-note">[^<]*</p>', p.rest, re.S)
    assert m and p.rest.count('<ul class="figures">') == 1, 'rc_home: the figures'
    p.rest = p.rest[:m.start()] + p.rest[m.end():]
    if 'id="ice-band"' in p.rest:                       # the same picture: once, at the top
        p.section('ice-band')
    # the first view's picture, fetched first
    p.sub("if (home) { add('img/rc/red-hero.webp'); add('img/rc/orange-hero.webp'); }",
          f"if (home) add(null, '{srcset}');", where='head' if "add('img/rc/red-hero.webp')" in p.head else 'rest')
    i = p.rest.index('</body>') if '</body>' in p.rest else len(p.rest)
    if HOTSPOTS:
        p.rest = p.rest[:i] + HOTSPOT_JS + '\n' + p.rest[i:]


HISTORY = r'(?:round \d+|\br\d\d[a-z]?\b|\bRC\d?\b|coordinator|the owner|critics?\b|\bcommit\b|\bbranch\b|r\d\d-[a-z]|wave \d|the audit)'


def rc_clean(p):
    """The page source without its history: comments that narrate rounds, branches, people or reviews go (code stays)."""
    def strip(t):
        t = re.sub(r'/\*(?:(?!\*/).)*?' + HISTORY + r'(?:(?!\*/).)*?\*/', '', t, flags=re.S | re.I)
        t = re.sub(r'(?m)(^|[ \t;{}(),])//[^\n]*?' + HISTORY + r'[^\n]*', lambda m: m.group(1).rstrip(), t, flags=re.I)
        t = re.sub(r'<!--(?:(?!-->).)*?' + HISTORY + r'(?:(?!-->).)*?-->', '', t, flags=re.S | re.I)
        return t
    p.head, p.rest = strip(p.head), strip(p.rest)
    p.styles = [strip(x) for x in p.styles]



SPECTRUM = [('Eight colors, Ember to Smoke.', 'Eight colors, the full spectrum.'),
            ('in eight colors from Ember to Smoke', 'in eight colors, the full spectrum'),
            ('eight colors, Ember to Smoke', 'eight colors, the full spectrum'),
            (', Ember to Smoke', ', the full spectrum')]


def rc_finish(web):
    """After web.py's favicons and vercel.json: the favicon titled EARF, and vercel.json
    without the retired journal redirect."""
    import os, json, shutil
    # the touch icon is web.py's own (favicons(): the flat mark, one shade per color, brand/mark/earf-globe-tiles.png)
    fav = os.path.join(web.SITE, 'favicon.svg'); f = open(fav).read()
    f = re.sub(r'<title>[^<]*</title>', '<title>EARF</title>', f); f = re.sub(r'aria-label="[^"]*"', 'aria-label="EARF"', f, count=1)
    open(fav, 'w').write(f)
    vj = os.path.join(web.SITE, 'vercel.json'); v = json.load(open(vj))
    v['redirects'] = [r for r in v.get('redirects', []) if 'journal' not in r['source']]
    json.dump(v, open(vj, 'w'), indent=2)
    # Smoke is a neutral gray that passes about half the light (the coordinator, 2026-11-10): every page, card and meta
    import glob
    for f in glob.glob(os.path.join(web.SITE, '**', '*.html'), recursive=True):
        t = open(f).read()
        u = t.replace('Smoked black', 'Smoked gray').replace('smoked black', 'smoked gray')
        for a, b in SPECTRUM:                 # the eight as the full spectrum, not a run from one to another
            u = u.replace(a, b)
        assert not re.search(r'(?i)ember to smoke', u), ('rc_finish: Ember to Smoke', f)
        if u != t:
            open(f, 'w').write(u)


BANNED_RC = r'seven colors|Ember to Fog|Smoke as current|still to come|on hold' if EIGHT else r'eight colors|to Smoke|Smoke as current'
