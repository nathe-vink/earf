"""The critic's card for a Planet EARF frame, round 33 (critic/PROMPT-promo.md, step 1): what the frame is for, what
is fixed, what may change, and the shot's settings as rendered (read from the image's IMG.shot.json).

    python3 spinoffs/barkhorn/planet/den/den_card.py VIEW OUT.md [--shot IMG.shot.json] [--scale 0.35]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import den_shots as S                                               # noqa: E402

FOR = {
    'street': 'the shopfront at night from across the street: one narrow storefront in an ordinary San Francisco '
              'building, the room glowing warm behind café curtains, a recessed door, the transom lit, the name in gold '
              'leaf on the glass.',
    'bar': 'the bar: a reeded walnut bar under three brass pendants, the back-bar\'s lit shelves of bottles with a Fog '
           'speaker standing among them, the listening room glimpsed at the far end.',
    'listening': 'the listening room at the back: one of the Ember pair beside the record wall, old brick behind it, '
                 'leather chairs turned toward it, a sconce and a lamp making pools of warm light.',
    'door': 'the whole room from just inside the door: the bar down the left, the banquette down the right, the '
            'listening room at the end.',
}

CONTEXT = """**The project:** a design mockup of Planet EARF, a proposed listening bar in San Francisco: a narrow, deep
ground-floor storefront (about 7 x 17 m, 3.4 m to the ceiling, about 30 seats). Its owner is EARF, which makes tinted
cast-acrylic horn loudspeakers (the Atmosphere line; about $20,000 a pair), a record player (Cumulus) and a lamp (Bell).
The images are to sell the room to the owner and, later, its guests: a cozy, warm, lived-in listening bar at night,
lit in pools by its own lamps, photographed as an interiors magazine would shoot a new bar. The speakers are the
room's only colour."""

FIXED = """**Fixed (never change):** EARF's products (their shape, colour and parts): the Atmosphere speakers (1293 mm tall,
tinted cast acrylic cabinets with white batts inside, a resin horn; cover off; an Ember (red) pair in the listening
room, a Fog (clear) pair in the back-bar's niches), Bell (the table lamps), and Cumulus (a small stand-in on the
console). The room's design as proposed: its layout and dimensions, the walnut bar and back-bar, the banquette, the
listening room, the record wall and the shopfront."""

MAY = """**What may change:** the light levels and colours of every source (sconces, pendants, shelf strips, niches,
Bell, candles, the record wall's light, the lamps on the speakers, the street lamps), the camera, the exposure and
grade, the materials and colours of the surfaces (floor, plaster, brick, leather, velvet, wood stain, the street),
small props (glasses, bottles, books, menus, a coat), people (none now), haze in the air, and the finish."""


def settings(sh, scale):
    v = next(p for p in sh['set']['props'] if p.get('module') == 'planet_den')
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
           f"right-hand wall to 7 at the left-hand wall where the bar runs, z up), level, at {cam['target']}, lens "
           f"{cam['lens_mm']} mm on 36 mm" + (f", f/{cam['fstop']} focused at {cam.get('focus')}" if cam.get('fstop') else ''),
           f"- the room's glowing surfaces (emission strengths; Cycles units): back-bar shelf strips {v.get('shelf_glow')}, "
           f"sconce shades {v.get('shade_glow')}, pendants' insides {v.get('pendant_glow')}, niche backs {v.get('niche_glow')}, "
           f"candle flames {v.get('flame')}, record-wall strip {v.get('record_glow')}, the gold leaf {v.get('gold_glow', 0.25)}",
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
    scale = float(sys.argv[sys.argv.index('--scale') + 1]) if '--scale' in sys.argv else 0.35
    sh = json.load(open(img_shot)) if img_shot else S.shot(view)
    txt = (f"# Card: Planet EARF, {S.VIEWS[view]['title']}\n\n**What the frame is for:** {FOR[view]}\n\n{CONTEXT}\n\n"
           f"{FIXED}\n\n{MAY}\n\n**Settings now:**\n\n{settings(sh, scale)}\n")
    open(out, 'w').write(txt)
    print(out)


if __name__ == '__main__':
    main()
