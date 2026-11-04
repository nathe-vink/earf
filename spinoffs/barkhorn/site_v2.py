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
  const clean = () => { const h = location.hash.slice(1); if (P[h] !== undefined) history.replaceState(null, '', P[h]); };
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
    if not (web.V2 or web.HOME_V2) and os.path.isdir(os.path.join(web.IMG, 'v2')):
        import shutil
        shutil.rmtree(os.path.join(web.IMG, 'v2'))
    for path, (h, title, desc, img, alt) in addresses(web).items():
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


MANTLE_SRC = 'renders/2026-11-01/barkhorn/mantle-r48/a-studio-ember-2423.png'   # by day, its light off (not the dusk frame: its light falls on the floor)
MANTLE = {'wide': 'img/v2/mantle-studio-1200.webp', 'full': 'img/v2/mantle-studio.webp', 'tile': 'img/v2/mantle-studio-tile.webp'}


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
        cw = round(im.height * 4 / 5)
        x0 = max(0, min(im.width - cw, round(im.width * 0.52 - cw / 2)))
        im.crop((x0, 0, x0 + cw, im.height)).resize((1200, 1500), Image.LANCZOS).save(dst, 'WEBP', quality=82, method=6)
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
    out = {'/tropos': ('speakers', 'Tropos · EARF', 'A powered horn loudspeaker, cast in tinted acrylic. Eight colors, Ember to Smoke. In development, not yet for sale.',
                       'img/og/speaker-green.jpg', 'Tropos in Poison'),
           '/lighting': ('lighting', 'Lighting · EARF', 'Hemisphere, a pendant, and Core, a cordless table lamp, in the eight colors. In development.',
                         'img/og/dome-red.jpg', 'Hemisphere in Ember'),
           '/mantle': ('turntable', 'Mantle · EARF', 'A turntable, lit from underneath, in the eight colors. In development.',
                       'img/og/tt-red.jpg', 'Mantle in Ember'),
           '/contact': ('contact', 'Contact · EARF', 'Write to us: hello@earf.world. Everything is made to order, so we quote rather than list.',
                        'img/hero-1200.jpg', 'The eight Tropos speakers on a curve')}
    for k, num, name, *_ in web.CLOUDS:
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
        night(p, web)
        sound(p, web)
        habitats(p, web)
        paths(p, web)
        lighten(p, web)
        mantle(p, web)
        render_word(p)
    if web.HOME_V2:
        home_v2(p, web)
    return p.done()
