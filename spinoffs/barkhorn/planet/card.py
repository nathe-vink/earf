"""The critic's card for a Planet EARF frame (critic/PROMPT-promo.md, step 1): what the frame is for, what is fixed,
what may change, and the shot's settings as they are.

    python3 spinoffs/barkhorn/planet/card.py VIEW OUT.md [--scale 0.5]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import shots as S                                                   # noqa: E402

FOR = {
    'door': 'the whole room at night, seen from just inside the plain front door: the first look at the bar.',
    'bar': 'the bar front lit, at eye level: the 8.4 m spectrum of eight back-lit acrylic panels, the bar\'s signature.',
    'listening': 'the listening corner: one of the Ice pair that stand either side of the record wall, the lounge\'s low chairs before it, the record wall beyond.',
    'backbar': 'the back-bar seen from across the room: the Fog pair of speakers in their lit niches, rising above the '
               'bar among edge-lit acrylic shelves of bottles, the bar front below.',
    'records': 'the record wall and the DJ desk set into it, with Cumulus (EARF\'s acrylic record player) on the desk.',
    'street': 'the street at night: the corner storefront from across the street, the room glowing through its one long '
              'window, a plain door with one small neon sign.',
    'clock': 'the colour clock: the same view at one of four hours, the ceiling\'s colour the only change.',
}

CONTEXT = """**The project:** a design mockup of Planet EARF, a proposed acrylic listening bar in San Francisco (Hayes Valley,
a 30 x 60 ft concrete storefront, 14 ft to the slab), for its owner: EARF, which makes tinted cast-acrylic horn
loudspeakers (the Atmosphere line, eight colours: Ember red, Dust orange, Acid yellow, Poison green, Ice blue, Haze violet,
Fog clear-white, Smoke black; about $20,000 a pair), a record player (Cumulus) and a lamp (Bell). The images are to sell
the idea of the room to the owner and, later, its guests: a calm, kissa-style listening bar at night, lit by its own
acrylic, photographed as an interiors magazine would shoot a new bar."""

FIXED = """**Fixed (never change):** EARF's products (their shape, colour and parts): the Atmosphere speakers (1293 mm tall, tinted
cast acrylic cabinets with white batts inside, a resin horn; cover off), Bell (pendants over the bar, lamps on the booth
tables) and Cumulus. The room's design as proposed: the layout and every dimension, the bar's eight panels in spectrum
order with the honed dark stone top, the edge-lit shelves, the Haze slats, the record wall, the screens, the back-lit
ceiling membrane and the colour of each speaker."""

MAY = """**What may change:** the light levels and colours of every source (the membrane, the panels' glow, shelves, niches,
slats, spots, Bell, the street lamps), the camera, the exposure and grade, the materials of the surfaces (floor, walls,
upholstery, wood, the street), small props (glasses, a menu, a coat), people (none now), haze in the air, and the finish."""


def settings(sh, view, scale):
    """The frame's settings as rendered: read from the image's own resolved shot (IMG.shot.json)."""
    v = next(p for p in sh['set']['props'] if p.get('module') == 'planet_room')
    cam = sh['camera']; R = sh['render']; Ls = sh['lights']
    def lamps(prefix):
        xs = [l for k, l in Ls.items() if k.startswith(prefix) and not l.get('off')]
        if not xs:
            return 'none'
        l = xs[0]
        what = f"{l['irradiance']} W/m2 at the target" if 'irradiance' in l else f"{l.get('power_w')} W"
        return f"{len(xs)} x {l['type']}, {what}" + (f", cone {l['cone_deg']} deg" if 'cone_deg' in l else '')
    def bells(prefix):
        xs = [l for k, l in Ls.items() if k.startswith(prefix)]
        return f"{round(sum(l['power_w'] for l in xs[:3]), 1)} W each" if xs else 'none'
    hz = sh.get('haze') or {}
    out = [f"- frame: {sh['size'][0]} x {sh['size'][1]} as delivered; this proof at scale {scale}",
           f"- camera: position {cam['position']} m (the room runs x 0 at the door to 18.29 at the record wall, y 0 at "
           f"the street window to 9.14 at the back-bar, z up), level, at {cam['target']}, lens {cam['lens_mm']} mm on 36 mm"
           + (f", f/{cam['fstop']} focused at {cam.get('focus')}" if cam.get('fstop') else ''),
           f"- the room's sources (emission strengths; Cycles units): membrane {v.get('membrane')} (clock '{v.get('clock')}'), "
           f"bar panels {v.get('panel_glow')} (graded from {v.get('panel_foot', 1.0)} of that at the foot to all of it at the top), "
           f"shelves {v.get('shelf_glow')}, back-bar back panel {v.get('backpanel_glow')}, Fog niches {v.get('niche_glow')}, "
           f"slats {v.get('slat_glow')} with their LED {v.get('slat_led')}, DJ recess {v.get('dj_glow')}, street neon {v.get('neon')}",
           f"- lamps: on each corner speaker {lamps('spk')}; the wash behind each pair {lamps('wash')}; on each Fog speaker "
           f"{lamps('fog')}; bar-top pinholes {lamps('bar')}; the DJ desk {lamps('dj')}; the record wall {lamps('rec')}; "
           f"Bell pendants {bells('pend')}; booth Bells {bells('booth')}; lounge Bells {bells('side')}; street lamps {lamps('street')}",
           f"- haze in the room's air: density {hz.get('density', 0)} per metre (0 = none), anisotropy {hz.get('anisotropy', 0)}",
           "- props on the bar and booth tables: rocks glasses with a pour and ice, coupes, folded menus",
           f"- render: {json.dumps(R)}"]
    return '\n'.join(out)


def main():
    view = sys.argv[1]; out = sys.argv[2]
    img_shot = sys.argv[sys.argv.index('--shot') + 1] if '--shot' in sys.argv else None
    scale = float(sys.argv[sys.argv.index('--scale') + 1]) if '--scale' in sys.argv else 0.5
    sh = json.load(open(img_shot)) if img_shot else S.shot(view)
    key = 'clock' if view.startswith('clock') else view
    txt = (f"# Card: Planet EARF, {S.VIEWS[view]['title']}\n\n**What the frame is for:** {FOR[key]}\n\n{CONTEXT}\n\n"
           f"{FIXED}\n\n{MAY}\n\n**Settings now:**\n\n{settings(sh, view, scale)}\n")
    open(out, 'w').write(txt)
    print(out)


if __name__ == '__main__':
    main()
