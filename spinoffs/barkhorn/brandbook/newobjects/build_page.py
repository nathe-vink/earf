"""The private artifact "EARF New Objects": page/index.html from six.py's data, with the renders and drawings as files
beside it (page/img/). Run: python3 build_page.py"""
import html, os, re, shutil
from PIL import Image
import six

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'page'); IMG = os.path.join(OUT, 'img')
os.makedirs(IMG, exist_ok=True)

def md(t):
    t = html.escape(t)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)

CAP = {
 'moho': 'Render. Moho on Mantle\'s platter, at true size against a 12-inch record: Dust, Acid and Ice under a Clear top, the brass core seen through them. Lighter custom pours of Dust, Acid and Ice (est.), as is Mantle\'s Dust plinth here; in stock sheet the puck reads darker.',
 'lithos': 'Render. Lithos in a room corner, books for scale: the filament shows only at the clear guides, which glow warm between the eight bands, buffed clear and satin in turn at Core Sample\'s 12.7 mm pitch. The colored bands are lighter custom pours (est.); in stock sheet the deep ones read near-black.',
 'ionos': 'Render. Ionos in a lighter custom pour of Ice (est.), its near-clear middle layer unlit; the top disc turns to tune, 24 detents read against the lit index at the front. The electronics tray shows through the bottom layers, as it would.',
 'cairn': 'Render. Cairn in Fog with one layer of Dust, stock sheet; faces as cast, sides flame-polished. Window light from behind throws the Dust forward.',
 'bedrock': 'Render. Bedrock in stock Dust (2422), the inch-thick end-plates stepped, three steel rails; low daylight from behind throws the amber onto the floor.',
 'relief': 'Render. Relief in Fog, lit by its own bar along the top edge: the green deepens with each of the twelve layers, like a sea chart in glass.',
 'meridian': 'Render. Meridian at ten past two: the Acid hour disc and the Ice minute disc cross, and where they overlap the light is green.',
}
TINT_OF = {'meridian': 'poison', 'moho': 'dust', 'lithos': 'smoke', 'ionos': 'ice', 'cairn': 'fog', 'bedrock': 'dust', 'relief': 'fog'}

def images():
    for o in six.OBJECTS:
        k = o['key']
        src = os.path.join(HERE, 'renders', f'{k}.png')
        im = Image.open(src).convert('RGB'); im.thumbnail((1600, 1600)); im.save(os.path.join(IMG, f'{k}.jpg'), quality=86)
        d = Image.open(os.path.join(HERE, 'drawings', f'{k}.png')).convert('RGB'); d.thumbnail((1500, 1500)); d.save(os.path.join(IMG, f'{k}-drawing.jpg'), quality=86)

def page():
    rows = []
    for o in six.OBJECTS:
        t = sum(f() for _, f in o['bom'])
        rows.append(f'<tr><th scope="row"><a href="#{o["key"]}">{o["name"]}</a></th><td>{html.escape(o["what"])}</td>'
                    f'<td class="num">${o["price"]:,}</td><td class="num">${t:,.0f}</td><td class="num">{(o["price"]-t)/o["price"]:.0%}</td></tr>')
    secs = []
    for i, o in enumerate(six.OBJECTS):
        k = o['key']; t = sum(f() for _, f in o['bom'])
        portrait = k == 'lithos'
        dims = ''.join(f'<div class="kv"><dt>{html.escape(a)}</dt><dd>{html.escape(b)}</dd></div>' for a, b in o['dims'])
        bom = ''.join(f'<tr><td>{html.escape(a)}</td><td class="num">${f():,.0f}</td></tr>' for a, f in o['bom'])
        secs.append(f'''
<section class="obj{' portrait' if portrait else ''}" id="{k}">
  <figure class="hero"><img src="img/{k}.jpg" alt="{html.escape(CAP[k])}" width="{1067 if portrait else 1600}" height="{1600 if portrait else 1067}" loading="lazy"><figcaption>{html.escape(CAP[k])}</figcaption></figure>
  <div class="text">
    <p class="eyebrow"><span class="chip" style="--c: var(--t-{TINT_OF[k]})"></span>{html.escape(o["what"])}</p>
    <h2>{o["name"]}</h2>
    <p class="tag">{html.escape(o["tag"])}</p>
    <p class="concept">{md(o["concept"])}</p>
    <dl class="dims">{dims}</dl>
    <p class="proc"><span class="eyebrow">Materials and process</span>{html.escape(o["process"])}</p>
    <div class="price"><div><span class="eyebrow">Price (est.)</span><b>${o["price"]:,}</b></div><div><span class="eyebrow">Landed at 100 (est.)</span><b>${t:,.0f}</b></div><div><span class="eyebrow">Margin</span><b>{(o["price"]-t)/o["price"]:.0%}</b></div></div>
    <p class="role">{html.escape(o["role"])}</p>
    <details><summary>The bill of materials</summary><div class="scroll"><table class="bom"><tbody>{bom}<tr class="total"><td>Landed</td><td class="num">${t:,.0f}</td></tr></tbody></table></div></details>
  </div>
  <figure class="drawing"><img src="img/{k}-drawing.jpg" alt="Dimensioned drawing of {o['name']}" width="1400" height="900" loading="lazy"><figcaption>Drawing, mm, first angle. Proposal, 31 October 2026.</figcaption></figure>
</section>''')
    tints = ''.join(f'<li><span class="chip" style="--c: var(--t-{n})"></span><b>{n.title()}</b><span>{code}</span><span class="num">{lt:.1%}</span></li>'
                    for n, (code, lt, hx) in __import__('render_objects_tints').TINTS.items())
    return f'''<title>EARF New Objects</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400..700&display=swap">
<style>
/* Layout: a catalogue of six objects, each a full-width render with its text and its drawing; paper by day, night by night. */
:root {{
  --page: #F4F1EC; --paper: #ECE8E1; --ink: #1C1A18; --muted: #5E5A53; --rule: #D6D0C6; --accent: #C92118;
  --t-ember: #C92118; --t-dust: #E06718; --t-acid: #E2AA15; --t-poison: #367424; --t-ice: #2584BE; --t-haze: #5B3197; --t-fog: #D5DFE0; --t-smoke: #57545F;
  --display: 'Instrument Sans', 'Helvetica Neue', Arial, sans-serif; --mono: 'IBM Plex Mono', ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --page: #100F12; --paper: #1A181C; --ink: #EDE7DD; --muted: #A79F93; --rule: #2E2B27; --accent: #E2554C; color-scheme: dark }} }}
:root[data-theme="dark"] {{ --page: #100F12; --paper: #1A181C; --ink: #EDE7DD; --muted: #A79F93; --rule: #2E2B27; --accent: #E2554C; color-scheme: dark }}
* {{ box-sizing: border-box }}
body {{ background: var(--page); color: var(--ink); font-family: var(--display); font-size: 17px; line-height: 1.55; -webkit-font-smoothing: antialiased }}
.wrap {{ max-width: 1240px; margin: 0 auto; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)) }}
header {{ padding-block: 56px 28px }}
.eyebrow {{ font-family: var(--mono); font-size: 12px; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); display: flex; align-items: center; gap: 8px; margin: 0 0 8px }}
h1 {{ font-size: clamp(44px, 8vw, 96px); line-height: .95; letter-spacing: -.035em; font-weight: 600; margin: 0 0 20px; text-wrap: balance }}
.lede {{ font-size: clamp(18px, 2.1vw, 22px); line-height: 1.45; max-width: 60ch; margin: 0 }}
.band {{ display: flex; height: 6px; margin-top: 32px }} .band i {{ flex: 1 }}
.summary {{ padding-block: 28px 8px }}
.scroll {{ overflow-x: auto }}
table {{ border-collapse: collapse; width: 100%; font-size: 15px }}
th, td {{ text-align: left; padding: 10px 12px 10px 0; border-bottom: 1px solid var(--rule); vertical-align: top }}
thead th {{ font-family: var(--mono); font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); font-weight: 500; border-bottom: 1px solid var(--ink) }}
th a {{ color: var(--ink); font-weight: 600; text-decoration: none; border-bottom: 1px solid var(--rule) }} th a:hover, th a:focus-visible {{ border-color: var(--accent) }}
.num {{ font-variant-numeric: tabular-nums; text-align: right; font-family: var(--mono); font-size: 14px }}
.note {{ font-size: 14px; color: var(--muted); max-width: 70ch }}
.obj {{ display: grid; grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr); gap: 28px 40px; padding-block: 64px; border-top: 1px solid var(--rule); align-items: start }}
.obj .hero {{ grid-column: 1 / -1; margin: 0 }}
.obj.portrait .hero {{ grid-column: 1; grid-row: 1 / span 2 }}
.obj.portrait .text {{ grid-column: 2 }}
.obj.portrait .drawing {{ grid-column: 2 }}
figure img {{ display: block; width: 100%; height: auto; max-width: 100%; background: var(--paper) }}
figcaption {{ font-family: var(--mono); font-size: 11.5px; letter-spacing: .04em; color: var(--muted); margin-top: 8px }}
.text {{ min-width: 0 }}
h2 {{ font-size: clamp(40px, 5.5vw, 64px); line-height: 1; letter-spacing: -.03em; font-weight: 600; margin: 0 }}
.tag {{ font-style: italic; color: var(--muted); margin: 6px 0 16px }}
.concept {{ margin: 0 0 18px; max-width: 62ch }}
.chip {{ width: 12px; height: 12px; border-radius: 50%; background: var(--c); display: inline-block; box-shadow: inset 0 0 0 1px rgba(0,0,0,.15) }}
.dims {{ display: grid; gap: 0; margin: 0 0 18px; border-top: 1px solid var(--rule) }}
.kv {{ display: grid; grid-template-columns: 9.5em minmax(0, 1fr); gap: 12px; padding: 7px 0; border-bottom: 1px solid var(--rule); font-size: 15px }}
.kv dt {{ font-family: var(--mono); font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); padding-top: 2px }}
.kv dd {{ margin: 0 }}
.proc {{ font-size: 15px; margin: 0 0 18px; max-width: 62ch }} .proc .eyebrow {{ display: block }}
.price {{ display: flex; flex-wrap: wrap; gap: 28px; margin: 0 0 14px }}
.price b {{ display: block; font-size: 28px; letter-spacing: -.02em; font-variant-numeric: tabular-nums }}
.role {{ font-size: 15px; color: var(--muted); margin: 0 0 14px; max-width: 62ch }}
details {{ border-top: 1px solid var(--rule); padding-top: 10px }}
summary {{ cursor: pointer; font-family: var(--mono); font-size: 12px; letter-spacing: .1em; text-transform: uppercase }}
summary:focus-visible, a:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 3px }}
.bom td {{ font-size: 14px }} .bom .total td {{ font-weight: 600; border-bottom: 0 }}
.drawing {{ margin: 0; min-width: 0 }}
.method {{ border-top: 1px solid var(--rule); padding-block: 56px 72px; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 40px }}
.method h3 {{ font-size: 26px; letter-spacing: -.02em; margin: 0 0 12px }}
.tints {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 0; border-top: 1px solid var(--rule) }}
.tints li {{ display: grid; grid-template-columns: 16px 6em minmax(0, 1fr) 4.5em; gap: 10px; align-items: center; padding: 7px 0; border-bottom: 1px solid var(--rule); font-size: 15px }}
.tints li span:nth-child(3) {{ font-family: var(--mono); font-size: 13px; color: var(--muted) }}
footer {{ padding-block: 24px 48px; font-family: var(--mono); font-size: 12px; color: var(--muted); border-top: 1px solid var(--rule) }}
@media (max-width: 820px) {{
  .obj, .obj.portrait, .method {{ grid-template-columns: minmax(0, 1fr) }}
  .obj.portrait .hero, .obj.portrait .text, .obj.portrait .drawing {{ grid-column: 1; grid-row: auto }}
  .kv {{ grid-template-columns: 7.5em minmax(0, 1fr) }}
}}
</style>
<div class="wrap">
<header>
  <p class="eyebrow">EARF · proposals for the owner · 31 October 2026</p>
  <h1>New objects</h1>
  <p class="lede">Six new things in the line's tinted cast acrylic, chosen from twenty-nine, and a seventh as a wildcard. Each is built by laminating stock sheet, so its layers show at every cut edge, and each treats light as part of the material. None touches Tropos, Hemisphere, Core, Mantle or the bar. Every picture is a render; every price and cost is an estimate.</p>
  <div class="band"><i style="background:var(--t-ember)"></i><i style="background:var(--t-dust)"></i><i style="background:var(--t-acid)"></i><i style="background:var(--t-poison)"></i><i style="background:var(--t-ice)"></i><i style="background:var(--t-haze)"></i><i style="background:var(--t-fog)"></i><i style="background:var(--t-smoke)"></i></div>
</header>
<section class="summary" aria-label="The six at a glance">
  <div class="scroll"><table><thead><tr><th>Object</th><th>What</th><th class="num">Price</th><th class="num">Landed at 100</th><th class="num">Margin</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
  <p class="note">From the cheapest way into the tints to a statement lamp: Moho and Cairn are gifts and Kickstarter add-ons; Bedrock and Relief sell to bars, hotels and studios; Ionos sits below Tropos's price; Lithos is a numbered edition. Costs at a run of 100 from published sheet prices and a $100-an-hour shop rate; prices at about 2.2 to 2.4 times landed.</p>
</section>
{''.join(secs)}
<section class="method">
  <div>
    <h3>How the tints are rendered</h3>
    <p>Each tint is a volume that absorbs light by the Beer–Lambert law, calibrated so that 3.2 mm of it passes the light that AC Plastics' TruCast stock publishes for the nearest code, in the tint's own hue, with about 8% lost at the two faces. Index 1.49; polished faces clear, sawn faces satin; bonded layers show as faint, countable joint lines, as a laminate does; caustics on. That is why the deep tints read deep: 2423 Red passes 14% through 3.2 mm, so a thick Ember part is nearly black except where light runs through an edge. So thick parts here are in the light stock tints (Dust, Fog) or in lighter custom pours, captioned as such, and Lithos lights its clear layers rather than its colors.</p>
    <p class="note">Prior art set the rules: thin countable layers with bond lines, no polished monoliths, no ombré, no neon, nothing embedded, and names clear of Strata, Skyline, Totem and Voie. The long list, the prior art, the costing and the scene files are in the repository under spinoffs/barkhorn/brandbook/newobjects/.</p>
  </div>
  <div>
    <p class="eyebrow">Stock code and published transmission at 3.2 mm</p>
    <ul class="tints">{tints}</ul>
    <p class="note">TruCast figures from the stock-color research (31 October 2026); Acid's is an estimate, since TruCast doesn't publish 2208.</p>
  </div>
</section>
<footer>EARF · New objects · drafts for the owner, nothing ordered or tested · renders are renders</footer>
</div>
'''

if __name__ == '__main__':
    images()
    open(os.path.join(OUT, 'index.html'), 'w').write(page())
    print('built', OUT)
