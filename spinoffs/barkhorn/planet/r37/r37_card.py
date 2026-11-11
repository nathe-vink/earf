"""The critic's card for a Planet EARF frame, round 37 (critic/PROMPT-interiors.md): what the frame is for, the
project, what is fixed, what may change, and the shot's settings as rendered (read from the image's IMG.shot.json).

    python3 spinoffs/barkhorn/planet/r37/r37_card.py VIEW OUT.md [--shot IMG.shot.json] [--scale 0.3]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import r37_shots as S                                                # noqa: E402

CONFIG = {'smoke': 'Smoke (everything smoked: the house configuration)', 'ember': 'Ember (everything red)',
          'ice': 'Ice (everything pale blue)',
          'mixed': 'Mixed (the bar pair Ice under Dust Domes, the R3s Fog; the listening pair Ember with Acid Orbs)'}
FOR = {
    'bar': 'the back bar, the room\'s showroom wall, seen square across the counter from a banquette table: two of EARF\'s '
           'speakers standing on the floor in timber-lined, felt-lined niches either side of the DJ station (as Ginza '
           'Music Bar\'s Tannoys sit in theirs), facing the counter, their horns at a seated drinker\'s ear; between '
           'them the decks with a pair of EARF\'s own record players (R3 Float) and a rotary mixer, a frosted disc in a '
           'floor-to-ceiling record wall; blackened-steel doors under a zinc worktop; the zinc-topped racetrack counter '
           'with a fluted dark-oak front, a brass foot rail and counter chairs (blackened steel, espresso leather, a low '
           'curved back) in front; EARF\'s Dome pendants low over the zinc. Configuration: {config}.',
    'listening': 'the listening zone: a room within the room, raised 200 mm, in deep warm neutrals (espresso velvet tub '
                 'chairs, dark carpet, limewashed walls), all seats facing the altar: EARF\'s listening pair on solid oak '
                 'plinths in a niche lined in the shell\'s Douglas fir boards, toed in to the best seat, felt behind, a light '
                 'plinth glowing under each; small hexagonal oak tables with an EARF Orb lamp on each; the shell around '
                 'it: fir beams overhead, concrete, blackened steel. Configuration: {config}.',
    'street': 'the shopfront at night, from the kerb: the blackened-steel shopfront, the name etched into the glass, a '
              'frosted lightbox with the fogged silhouette of a woman dancing, and the room behind the glass: the zinc '
              'counter under its Dome pendants, the record wall, and at the far end EARF\'s pair on its altar. '
              'Configuration: {config}.',
    'sink': 'a detail: the washbasin in an alcove of the shell\'s Douglas fir boards, a slab of cast acrylic 160 mm '
            'thick in Smoke (EARF\'s smoked tint, polished), floating off the wall, unlit from within: it reads as '
            'smoked glass, by reflection and by its polished arrises; a soft bowl 120 mm deep with a 30 mm radius at '
            'its rim and a steel waste; a brushed-steel spout and a separate lever, each on its own escutcheon. Its '
            'light is the room\'s: a narrow warm downlight into the bowl, a hidden strip under the front edge, a wash '
            'down the boards. No internal glow (a design decision: a lit tinted block reads as a lit Corian box).',
}

CONTEXT = """**The project:** a design mockup of Planet EARF, a proposed listening bar in San Francisco: a narrow, deep
ground-floor storefront (6.1 x 17 m, 3.4 m to the ceiling, about 30 seats). Its owner is EARF, which makes tinted
cast-acrylic horn loudspeakers (the Atmosphere line, about $20,000 a pair). The owner wants a designed, specific place,
not a catalogue bar, in the line of Ginza Music Bar, Jazz Spot Bokunen, Space Talk, Equal Parts and A Bar with Shapes
for a Name: board-formed concrete, Douglas fir beams and blackened steel as the shell; the speakers as an altar; a
sculpted counter; furniture with a pedigree; acrylic kept for the special things (the speakers, the
lamps, the sink, the screens); dark, with pools of light. The bar is also EARF's showroom: the room is kept neutral and warm, and the colour comes
from the products alone, which swap between configurations (speakers, lamp covers, record players) while the room
stays the same. The images are to sell the room to the owner, photographed
as an interiors magazine would shoot a new bar at night.

**Also answer, in stage 1 and in the verdict:** would a design magazine publish this as a specific place, or is it a
generic bar?"""

FIXED = """**Fixed (never change):** EARF's products (their shape, colour and parts): the Atmosphere speakers (1293 mm tall,
tinted cast-acrylic cabinets with white batts inside, a resin horn; cover off; four of them: a pair in the back bar's
niches, a pair on the altar), EARF's bar lamps (the Dome pendant and the Orb table lamp: tinted acrylic with a frosted
liner set within it) and its record player (R3 Float: a tinted slab on clear posts over a lit base), each in the
configuration's tint. The room's design as proposed: its layout and dimensions, its materials, the screens and what
they show, the counter, the back bar and record wall, the banquette, the seats, the zone, the niches, the altar, the
sink and the shopfront."""

MAY = """**What may change:** the light levels and colours of every source (the Domes and their downlights, the Orbs,
the disc behind the DJ station, the record wall's spots, the altar's spots, the lamps on the speakers, the screens'
brightness, the lit niche, the sink's glow, candles, the street lamps), the camera, the exposure and grade (including the
view transform), the materials' finish (the concrete's tone and sheen, the oak's stain, the zinc's and steel's patina,
the floor's polish, how rough the frosted acrylic is), small props (glasses, a coat, records, menus), haze, and the
finish."""


SHOT_VIEW = ['']


def settings(sh, scale):
    v = {**next(p for p in sh['set']['props'] if p.get('module') == 'planet_r37'), 'config': S.VIEWS.get(SHOT_VIEW[0], {}).get('settings', {}).get('config', 'smoke')}
    dm = next((p for p in sh['set']['props'] if p.get('fn') == 'dome'), {})
    ob = next((p for p in sh['set']['props'] if p.get('fn') == 'orb'), {})
    cam = sh['camera']; R = sh['render']; Ls = sh['lights']

    def lamps(prefix):
        xs = [l for k, l in Ls.items() if k.startswith(prefix)]
        if not xs:
            return 'none'
        l = xs[0]
        what = f"{l['irradiance']} W/m2 at the target" if 'irradiance' in l else f"{l.get('power_w')} W"
        col = l.get('color'); col = f", {col} K" if isinstance(col, (int, float)) else ''
        return f"{len(xs)} x {l['type']}, {what}{col}" + (f", cone {l['cone_deg']} deg" if 'cone_deg' in l else '')
    hz = sh.get('haze') or {}
    return '\n'.join([
        f"- frame: {sh['size'][0]} x {sh['size'][1]} as delivered; this proof at scale {scale}",
        f"- camera: position {cam['position']} m (x 0 at the shopfront's glass to 17 at the back wall, y 0 at the "
        f"right-hand wall to {S.RP.W} at the left-hand wall where the counter runs, z up), level, at {cam['target']}, "
        f"lens {cam['lens_mm']} mm on 36 mm" + (f", f/{cam['fstop']} focused at {cam.get('focus')}" if cam.get('fstop') else ''),
        f"- configuration: {CONFIG.get(v.get('config', 'smoke'))}",
        f"- EARF's lamps (the lamp hidden; the frosted liner glows by itself): each Dome {dm.get('lamp_w', v.get('dome_w'))} W, "
        f"its liner's glow {dm.get('shade_glow', v.get('dome_glow'))}; each Orb {ob.get('lamp_w', v.get('sphere_w'))} W, glow "
        f"{ob.get('shade_glow', v.get('sphere_glow'))}",
        f"- the room's glowing surfaces (emission strengths): the screens' images {v.get('screen_glow')}, the disc behind "
        f"the DJ station {v.get('disc_glow')} in {v.get('disc_col')} (with a {v.get('disc_lamp')} W area lamp), the "
        f"lit niche's strip {v.get('niche_strip')}, the nameplate {v.get('name_glow')}, the sink's under-glow "
        f"{v.get('sink_glow')}, candle flames {v.get('flame')}, the window's etched name {v.get('etch_glow')}",
        f"- lamps: the Domes' downlights {lamps('pend')}; the record wall {lamps('rw')}; the altar {lamps('altar')}; on "
        f"each Ember speaker {lamps('spk')}; the sink {lamps('sink')}; candles {lamps('candle')}; street lamps "
        f"{lamps('street')}",
        f"- haze in the room's air: density {hz.get('density', 0)} per metre (0 = none)",
        "- props: rocks glasses and a half-drunk coupe, a record out of its sleeve, a coat over a counter chair, record "
        "sleeves on the panels' ledges, bottles in the lit niche, candles on the counter",
        f"- render: {json.dumps(R)}"])


def main():
    view = sys.argv[1]; out = sys.argv[2]
    img_shot = sys.argv[sys.argv.index('--shot') + 1] if '--shot' in sys.argv else None
    scale = float(sys.argv[sys.argv.index('--scale') + 1]) if '--scale' in sys.argv else 0.3
    sh = json.load(open(img_shot)) if img_shot else S.S.shot(view)
    key = view; SHOT_VIEW[0] = view
    cfg = S.VIEWS[view]['settings'].get('config', 'smoke')
    txt = (f"# Card: Planet EARF, {S.VIEWS[view]['title']}\n\n**What the frame is for:** "
           f"{FOR[key.split('-')[0]].format(config=CONFIG[cfg])}\n\n{CONTEXT}\n\n{FIXED}\n\n{MAY}\n\n"
           f"**Settings now:**\n\n{settings(sh, scale)}\n")
    open(out, 'w').write(txt)
    print(out)


if __name__ == '__main__':
    main()
