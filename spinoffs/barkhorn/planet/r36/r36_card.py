"""The critic's card for a Planet EARF frame, round 36 (critic/PROMPT-interiors.md): what the frame is for, the
project, what is fixed, what may change, and the shot's settings as rendered (read from the image's IMG.shot.json).

    python3 spinoffs/barkhorn/planet/r36/r36_card.py VIEW OUT.md [--shot IMG.shot.json] [--scale 0.3]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import r36_shots as S                                                # noqa: E402

ZONE = {'green': 'deep bottle green', 'oxblood': 'oxblood'}
FOR = {
    'bar': 'the bar, down the room\'s axis to the altar: a racetrack counter (a 70 mm zinc top with a rounded edge over a '
           'fluted dark-oak front, a brass foot rail, turntables and a rotary mixer built in) with counter chairs (dark '
           'oak, a low curved back, upholstered seats) on the left, behind it a quiet back bar of blackened-steel doors '
           'under a floor-to-ceiling record wall with a frosted disc behind the DJ station; a built-in curved oak '
           'banquette with small round tables on the right under frosted screens set in the concrete (pressed hands, a '
           'shell in fog); smoked-acrylic Dome pendants hung low over the zinc; and at the far end, through the smoked '
           'partition, the Ember pair on its altar.',
    'listening': 'the listening zone: a room within the room, raised 200 mm, in one saturated colour ({zone}: velvet tub '
                 'chairs, wool carpet, limewashed walls), all seats facing the altar: the Ember pair on solid oak plinths in '
                 'a niche lined in end-grain blocks, toed in to the best seat, felt behind; small hexagonal oak tables with '
                 'a squat smoked-acrylic Orb lamp on each.',
    'street': 'the shopfront at night, from the kerb: the blackened-steel shopfront, the name etched into the glass, a '
              'frosted lightbox with the fogged silhouette of a woman dancing, and the room behind the glass: the zinc '
              'counter under its Dome pendants, the record wall, and at the far end the Ember pair on its altar.',
    'sink': 'a detail: the washbasin in an alcove of dark timber boards between the banquette and the listening zone, a '
            'floating trough cast in Ember (red) acrylic, its basin soft and rounded into its top, lit from below so it '
            'glows through its thickness, a brushed-steel spout from the wall.',
}

CONTEXT = """**The project:** a design mockup of Planet EARF, a proposed listening bar in San Francisco: a narrow, deep
ground-floor storefront (6.1 x 17 m, 3.4 m to the ceiling, about 30 seats). Its owner is EARF, which makes tinted
cast-acrylic horn loudspeakers (the Atmosphere line, about $20,000 a pair). The owner wants a designed, specific place,
not a catalogue bar, in the line of Ginza Music Bar, Jazz Spot Bokunen, Space Talk, Equal Parts and A Bar with Shapes
for a Name: board-formed concrete, Douglas fir beams and blackened steel as the shell; the speakers as an altar; one
saturated zone; a sculpted counter; furniture with a pedigree; acrylic kept for the special things (the speakers, the
lamps, the sink, the screens); dark, with pools of light. The images are to sell the room to the owner, photographed
as an interiors magazine would shoot a new bar at night.

**Also answer, in stage 1 and in the verdict:** would a design magazine publish this as a specific place, or is it a
generic bar?"""

FIXED = """**Fixed (never change):** EARF's products (their shape, colour and parts): the Atmosphere speakers (1293 mm tall,
tinted cast-acrylic cabinets with white batts inside, a resin horn; cover off; the Ember (red) pair on the altar), and
EARF's bar lamps (the Dome pendant, its covers swapped by hand, and the Orb, a squat crystal-ball table lamp in a
low cup: tinted acrylic with a frosted liner set within it, smoked here). The room's design as proposed: its layout and dimensions, its materials, the screens and what
they show, the counter, the back bar and record wall, the banquette, the seats, the zone and its colour, the altar, the
sink and the shopfront."""

MAY = """**What may change:** the light levels and colours of every source (the Domes and their downlights, the Spheres,
the disc behind the DJ station, the record wall's spots, the altar's spots, the lamps on the speakers, the screens'
brightness, the lit niche, the sink's glow, candles, the street lamps), the camera, the exposure and grade (including the
view transform), the materials' finish (the concrete's tone and sheen, the oak's stain, the zinc's and steel's patina,
the floor's polish, how rough the frosted acrylic is), small props (glasses, a coat, records, menus), haze, and the
finish."""


def settings(sh, scale):
    v = next(p for p in sh['set']['props'] if p.get('module') == 'planet_r36')
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
        f"- the zone's colour: {ZONE.get(v.get('colourway', 'green'))}",
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
    key = 'listening' if view.startswith('listening') else view
    v = next(p for p in sh['set']['props'] if p.get('module') == 'planet_r36')
    txt = (f"# Card: Planet EARF, {S.VIEWS[view]['title']}\n\n**What the frame is for:** "
           f"{FOR[key].format(zone=ZONE.get(v.get('colourway', 'green')))}\n\n{CONTEXT}\n\n{FIXED}\n\n{MAY}\n\n"
           f"**Settings now:**\n\n{settings(sh, scale)}\n")
    open(out, 'w').write(txt)
    print(out)


if __name__ == '__main__':
    main()
