"""The press kit's one-page fact sheets as US Letter PDFs: press/out/earf-<name>.pdf, and all of them together in
press/out/earf-press-kit.pdf. The facts are the sheets' in this folder (from web.py and the logs); the pictures the
site's. Set in the site's own type through headless Chromium.

    python3 make_sheets.py
"""
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, '..', 'site', 'img')
# Core is cordless (owner, 2026-10-31): its pictures come from the Brand Book's copy of the lamps lane's cordless set,
# since the site's still show the cord.
BOOK = os.path.join(HERE, '..', 'brandbook', 'book', 'img')
FROM_BOOK = {'lamp-orb.jpg', 'lamps-orbs.jpg', 'lamps-unlit.jpg', 'room.jpg'}
# Only pictures that passed the critics (2026-11-09): the seven tall fronts, in the Book's img. A sheet whose picture
# has not passed gets a labelled gap.
SEVEN = [f'honest-front-{t}.jpg' for t in ('ember', 'dust', 'acid', 'poison', 'ice', 'haze', 'fog')]
OUT = os.path.join(HERE, 'out')
MARK = os.path.join(HERE, '..', 'brand', 'mark', 'earf-wordmark-black.svg')
STANDING = ('In development and not yet for sale. Every picture is a render until the first are built. Figures are '
            'design figures; measured ones follow with the first pair. Prices are set at launch.')

SHEETS = [
    ('company', 'EARF', 'The company', 'Hi-fi and light, cast in tinted acrylic, in seven colors, Ember to Fog.',
     SEVEN,
     'EARF is a San Francisco maker of hi-fi and lighting in tinted cast acrylic. Every product comes '
     'in the same seven colors, from Ember to Fog, so a room can be one color or three. Each is named for a layer of '
     'the Earth. A wall of tinted acrylic 20 mm thick shows what is inside it.',
     [('Where', 'San Francisco, California'), ('Site', 'earf.world'), ('Inquiries', 'hello@earf.world; trade and stockists the same'),
      ('Products', 'Tropos, a powered horn loudspeaker · Hemisphere, a pendant · Core, a table lamp · Mantle, a record player'),
      ('Colors', '01 Ember · 02 Dust · 03 Acid · 04 Poison · 05 Ice · 06 Haze · 07 Fog (an eighth, Smoke, held)'),
      ('Sells', 'Made to order; prices set at launch'),
      ('Where it stands', 'Tropos is drawn for making, part by part: more than eighty parts, each with its fabrication drawing. '
       'The horn and the bass were worked out by simulation before any acrylic was cut. Next, the first pair, built as '
       'production will build it; then measured, by ear and by microphone. The lamps and Mantle follow the same way'),
      ('Founder', '[FOUNDER]')]),
    ('tropos', 'Tropos', 'Powered horn loudspeaker', 'Seven colors, Ember to Fog.', 'honest-front-ember.jpg',
     'Each cabinet is tinted cast acrylic, 20 mm thick. The horn is one sheet of 10 mm acrylic in the cabinet’s own color, '
     'formed over a plug and polished, its driver in a pod whose cap twists off by hand. Above 1 kHz the horn carries the music; below, a 15-inch '
     'woofer takes it, each on its own channel of the amplifier inside. The lining shows through the walls, so it is '
     'dressed in white voile. The name: the troposphere, the air we live in, from the Greek tropos, a turn.',
     [('Height', '1293 mm'), ('Width', '560 mm, the cabinet, with the horn flush'), ('Depth', '423 mm overall, 420 mm at the cabinet'),
      ('Weight', '72.6 kg on its own feet'), ('Woofer', 'FaitalPRO 15PR400, 15-inch, two ports in the front’s lower corners'),
      ('Horn driver', 'B&C DE1085TN, 2-inch compression driver'), ('Amplifier', 'Hypex FusionAmp FA122, built in: two channels of 125 W, crossed at 1 kHz in its DSP'),
      ('Bass', 'To about 51 Hz at −3 dB, before the room adds its own; ports tuned to 38 Hz'), ('Loudness', 'Up to about 115 dB at 1 m, each'),
      ('Inputs', 'XLR (and a link out), RCA, AES, S/PDIF coaxial and optical; USB to set it up'),
      ('Lining', 'Polyester batts in white voile'), ('Colors', 'All seven; the cover cloth matched to each')]),
    ('hemisphere', 'Hemisphere', 'Pendant lamp', 'A quarter turn takes its shade off, and another puts a new color on.',
     None,
     'A pendant in the speakers’ acrylic, frosted within, so the color glows and the source never shows. Hung low over '
     'the bar. The shade comes off by hand to wash or to change color. The name: half a globe, hung mouth down.',
     [('Size', '200 mm across'), ('Shade', 'Cast acrylic in three layers, tinted, with a frosted layer between'),
      ('Light', 'A 575-lumen LED, 2700 K, CRI 90, shielded inside the hub'), ('Fitting', 'Black anodized aluminum, with a quarter-turn catch'),
      ('Hanging', 'A 600 mm drop as standard, cut to length; a black acrylic canopy 150 mm across'),
      ('Mains', '120 V, dimmable; listing to UL 1598 to follow'), ('Shades', 'In all seven colors, sold singly')]),
    ('core', 'Core', 'Table lamp', 'Goes where the conversation is.', None,
     'A ball of tinted acrylic sitting low in a black acrylic base. Cordless, it goes where the '
     'conversation is. When the cells tire, you change the cells, not the lamp. The name: the glowing center.',
     [('Size', '160 mm ball, 180 mm tall'), ('Weight', 'About 1.5 kg'), ('Light', '2200 to 2700 K, warmer as it dims'),
      ('Control', 'Touch the black ring: tap to switch, hold to dim'),
      ('Power', 'Cordless: about five hours a charge on three standard LiFePO4 cells you can replace yourself; two to three hours to charge'),
      ('Rating', 'Designed to meet IP44, for terraces and spilled drinks'), ('Shades', 'In all seven colors, sold singly')]),
    ('mantle', 'Mantle', 'Record player', 'A turntable in cast acrylic.', None,
     'A turntable in cast acrylic. The plinth floats 40 mm over its base. The motor stands apart in a pod of its own, on '
     'soft feet, so its hum stays out of the plinth, and the phono stage is built in. The lid’s hinges sit on brass '
     'inserts, so no screw cuts the acrylic. The name: the layer that moves beneath the crust.',
     [('Plinth', 'Tinted cast acrylic, 25 mm; it floats 40 mm over the base'), ('Base', 'Cast acrylic'),
      ('Drive', 'Belt, its motor in a heavy pod of its own'), ('Speeds', '33 and 45, by a button'), ('Arm', 'Rega RB330'),
      ('Cartridge', 'Ortofon 2M Black'), ('Phono stage', 'Built in, for moving-magnet cartridges, with a line out and a bypass'),
      ('Cover', 'Tinted acrylic, hinged'), ('Size', '470 wide, 380 deep, 194 high with the lid down (mm)'), ('Weight', 'About 15.5 kg')]),
]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Instrument+Sans:wght@400..700&display=block');
@page { size: Letter; margin: 0 }
* { box-sizing: border-box }
body { margin: 0; font-family: 'Instrument Sans', Arial, sans-serif; color: #1C1A18; -webkit-print-color-adjust: exact; print-color-adjust: exact }
.page { width: 8.5in; height: 11in; padding: 0.55in 0.6in; display: flex; flex-direction: column; gap: 16px; page-break-after: always; background: #F4F1EC; position: relative }
.top { display: flex; justify-content: space-between; align-items: center }
.top img { height: 18px }
.k { font-family: 'IBM Plex Mono', monospace; font-size: 8.5pt; letter-spacing: .12em; text-transform: uppercase; color: #5E5A53 }
h1 { margin: 6px 0 0; font-size: 46pt; line-height: .95; letter-spacing: -.035em; font-weight: 600 }
.line { font-size: 15pt; letter-spacing: -.01em; margin: 0 }
.pic { height: 3.4in; border-radius: 3px; overflow: hidden; background: #F8F7F5 }
.pic img { width: 100%; height: 100%; object-fit: cover; object-position: 50% 42% }
.pic.fit { background: #E4E0D9 }
.pic.fit img { object-fit: contain }
.pic.row { display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px; background: none; align-items: center }
.pic.row img { height: auto; aspect-ratio: 4/5; border-radius: 2px }
.pic.gap { display: grid; place-content: center; text-align: center; gap: 6px; border: 1px dashed #5E5A53; background: #ECE8E1; font-size: 13px; color: #5E5A53 }
.pic.gap b { color: #1C1A18; font-size: 15px }
.body { font-size: 10.5pt; line-height: 1.5; margin: 0; max-width: 6.6in }
dl { margin: 0; display: grid; grid-template-columns: 1.35in 1fr; gap: 0; font-size: 9.5pt; line-height: 1.4; border-top: 1px solid #D6D0C6 }
dt, dd { padding: 5px 0; border-bottom: 1px solid #D6D0C6; margin: 0 }
dt { font-family: 'IBM Plex Mono', monospace; font-size: 7.5pt; letter-spacing: .1em; text-transform: uppercase; color: #5E5A53; padding-top: 7px }
.foot { margin-top: auto; display: flex; justify-content: space-between; gap: 24px; font-family: 'IBM Plex Mono', monospace; font-size: 7pt; letter-spacing: .06em; color: #5E5A53; line-height: 1.5; text-transform: uppercase }
.strip { position: absolute; left: 0; right: 0; bottom: 0; height: 6px; display: flex }
.strip i { flex: 1 }
"""
TINTS = ['#920000', '#E06718', '#E2AA15', '#1C5B02', '#2584BE', '#44147B', '#D5DFE0']   # seven; Smoke held (the owner's call)


def page(key, name, kind, line, pic, body, rows):
    esc = lambda s: s.replace('&', '&amp;').replace('<', '&lt;')
    dl = ''.join(f'<dt>{esc(k)}</dt><dd>{esc(v)}</dd>' for k, v in rows)
    strip = ''.join(f'<i style="background:{c}"></i>' for c in TINTS)
    src = lambda f: f'file://{os.path.join(BOOK if f in FROM_BOOK or f.startswith("honest-") else IMG, f)}'
    if isinstance(pic, list):
        pic_html = '<div class="pic row">' + ''.join(f'<img src="{src(f)}" alt="">' for f in pic) + '</div>'
        credit = 'Pictures: the seven, each its own studio render.'
    elif pic:
        pic_html = f'<div class="pic{" fit" if key in ("tropos",) else ""}"><img src="{src(pic)}" alt=""></div>'
        credit = 'Picture: a render.'
    else:
        pic_html = f'<div class="pic gap"><span>PENDING</span><b>{esc(name)}: a new render</b><span>It goes here when it passes the critics.</span></div>'
        credit = ''
    return (f'<section class="page"><div class="top"><img src="file://{MARK}" alt="EARF"><span class="k">Press · fact sheet · not for release</span></div>'
            f'<div><span class="k">{esc(kind)}</span><h1>{esc(name)}</h1></div><p class="line">{esc(line)}</p>'
            f'{pic_html}<p class="body">{esc(body)}</p><dl>{dl}</dl>'
            f'<div class="foot"><span>{STANDING} {credit}</span><span>earf.world<br>hello@earf.world</span></div>'
            f'<div class="strip">{strip}</div></section>')


def main():
    os.makedirs(OUT, exist_ok=True)
    pages = [(s[0], page(*s)) for s in SHEETS]
    jobs = []
    for key, html in pages + [('press-kit', ''.join(h for _, h in pages))]:
        path = os.path.join(OUT, f'earf-{key}.html')
        open(path, 'w').write(f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>{html}')
        jobs.append((path, os.path.join(OUT, f'earf-{key}.pdf')))
    js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();for(const [h,p] of "
          + json.dumps(jobs) + "){const pg=await b.newPage();await pg.goto('file://'+h,{waitUntil:'networkidle'});"
          "await pg.evaluate(()=>document.fonts.ready);await pg.pdf({path:p,format:'Letter',printBackground:true});"
          "await pg.close();console.log('wrote',p)}await b.close()})();")
    subprocess.run(['node', '-e', js], check=True)
    for h, _ in jobs:
        os.remove(h)


if __name__ == '__main__':
    main()
