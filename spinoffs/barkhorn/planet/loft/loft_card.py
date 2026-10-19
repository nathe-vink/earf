"""The critic's card for a Planet EARF frame, round 34 (critic/PROMPT-promo.md, step 1): what the frame is for, what
is fixed, what may change, and the shot's settings as rendered (read from the image's IMG.shot.json).

    python3 spinoffs/barkhorn/planet/loft/loft_card.py VIEW OUT.md [--shot IMG.shot.json] [--scale 0.35]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import loft_shots as S                                               # noqa: E402

FOR = {
    'bar': 'the bar, down the room from the window table: the fir-topped concrete bar and the steel back-bar with its '
           'clear acrylic shelves on the left, the banquette and its two frosted screens (pressed hands, a shell in fog) '
           'on the right, frosted acrylic pendants under fir beams, and at the far end, through a smoked acrylic '
           'partition, one of the Ember pair glowing in the listening room.',
    'listening': 'the listening room at the back: one of the Ember pair beside the record wall, board-formed concrete '
                 'behind it, fir beams overhead, leather chairs turned toward it.',
    'street': 'the shopfront window at night, from the kerb: the blackened-steel shopfront, the name frosted into the glass, '
              'a frosted acrylic lightbox showing the fogged silhouette of a woman dancing, the warm room behind the glass '
              'and, through a clear pane, one of the Ember pair glowing at the far end.',
}

CONTEXT = """**The project:** a design mockup of Planet EARF, a proposed listening bar in San Francisco: a narrow, deep
ground-floor storefront (6.1 x 17 m, 3.4 m to the ceiling, about 30 seats). Its owner is EARF, which makes tinted
cast-acrylic horn loudspeakers (the Atmosphere line, about $20,000 a pair). The owner wants board-formed concrete,
Douglas fir beams and blackened steel, a lot of acrylic used tastefully (thick, clear, frosted or smoked; never cheap),
screens behind large frosted acrylic panels showing slow, suggestive images (hands pressed against fogged glass, a
dancer's fogged silhouette, Arrival-like forms), and a dim but readable, cozy room. The speakers are its only colour.
The images are to sell the room to the owner, photographed as an interiors magazine would shoot a new bar at night."""

FIXED = """**Fixed (never change):** EARF's products (their shape, colour and parts): the Atmosphere speakers (1293 mm tall,
tinted cast-acrylic cabinets with white batts inside, a resin horn; cover off; an Ember (red) pair in the listening
room, a Fog (water-clear) pair in the back-bar's niches), Bell (the table lamps) and Cumulus (a small stand-in). The
room's design as proposed: its layout and dimensions, its materials (concrete, fir, blackened steel, neutral acrylic),
the screens and what they show, the bar, back-bar, banquette, listening room, record wall and shopfront."""

MAY = """**What may change:** the light levels and colours of every source (pendants, the shelves' lit edges, the niches'
frosted backs, the screens' brightness, the bar top's lit inlay, the sconce, Bell, candles, the record wall's light, the
lamps and pinholes on the speakers, the street lamps), the camera, the exposure and grade (including the view
transform), the materials' finish (the concrete's tone and sheen, the stain of the fir, the steel's patina, the floor's
polish, how rough the frosted acrylic is), small props (glasses, bottles, books, menus, a coat), haze, and the finish."""


def settings(sh, scale):
    v = next(p for p in sh['set']['props'] if p.get('module') == 'planet_loft')
    cam = sh['camera']; R = sh['render']; Ls = sh['lights']

    def lamps(prefix):
        xs = [l for k, l in Ls.items() if k.startswith(prefix) and not l.get('off')]
        if not xs:
            return 'none'
        l = xs[0]
        what = f"{l['irradiance']} W/m2 at the target" if 'irradiance' in l else f"{l.get('power_w')} W"
        col = l.get('color'); col = f", {col} K" if isinstance(col, (int, float)) else ''
        return f"{len(xs)} x {l['type']}, {what}{col}" + (f", cone {l['cone_deg']} deg" if 'cone_deg' in l else '')

    def bells(prefix):
        xs = [l for k, l in Ls.items() if k.startswith(prefix)]
        return f"{len(xs) // 3} lamps, {round(sum(l['power_w'] for l in xs[:3]), 1)} W each" if xs else 'none'
    hz = sh.get('haze') or {}
    out = [f"- frame: {sh['size'][0]} x {sh['size'][1]} as delivered; this proof at scale {scale}",
           f"- camera: position {cam['position']} m (x 0 at the shopfront's glass to 17 at the back wall, y 0 at the "
           f"right-hand wall to {S.LP.W} at the left-hand wall where the bar runs, z up), level, at {cam['target']}, lens "
           f"{cam['lens_mm']} mm on 36 mm" + (f", f/{cam['fstop']} focused at {cam.get('focus')}" if cam.get('fstop') else ''),
           f"- the room's glowing surfaces (emission strengths; Cycles units): the screens' images {v.get('screen_glow')}, "
           f"the shelves' lit edges {v.get('shelf_glow')}, the niches' frosted backs {v.get('niche_glow')}, the pendants' "
           f"frosted tubes {v.get('pendant_glow')} and lamps {v.get('pendant_lamp')}, the bar top's inlay {v.get('inlay_glow')}, "
           f"the sconce's frosted shade {v.get('shade_glow')}, candle flames {v.get('flame')}, record-wall strip "
           f"{v.get('record_glow')}, the window's frosted name {v.get('etch_glow')}",
           f"- lamps: sconces {lamps('sconce')}; pendants {lamps('pend')}; on each Ember speaker {lamps('spk')}; in each "
           f"niche {lamps('niche')}; the record wall {lamps('rec')}; candles {lamps('candle')}; Bell {bells('bell')}; "
           f"street lamps {lamps('street')}",
           f"- haze in the room's air: density {hz.get('density', 0)} per metre (0 = none)",
           "- props: rocks glasses and coupes, folded menus, candles in amber votives, bottles on the back-bar, books",
           f"- render: {json.dumps(R)}"]
    return '\n'.join(out)


def main():
    view = sys.argv[1]; out = sys.argv[2]
    img_shot = sys.argv[sys.argv.index('--shot') + 1] if '--shot' in sys.argv else None
    scale = float(sys.argv[sys.argv.index('--scale') + 1]) if '--scale' in sys.argv else 0.3
    sh = json.load(open(img_shot)) if img_shot else S.shot(view)
    txt = (f"# Card: Planet EARF, {S.VIEWS[view]['title']}\n\n**What the frame is for:** {FOR[view]}\n\n{CONTEXT}\n\n"
           f"{FIXED}\n\n{MAY}\n\n**Settings now:**\n\n{settings(sh, scale)}\n")
    open(out, 'w').write(txt)
    print(out)


if __name__ == '__main__':
    main()
