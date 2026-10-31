"""The critic's card for round 43's pop-up views (shop, window, listening): what the frame is for, the context, what is
fixed and what may change, and every setting as rendered, in the format of rounds 37 to 42.

    python3 spinoffs/barkhorn/planet/r43/r43_card.py VIEW OUT.md --shot IMG.shot.json [--scale 0.5]
"""
import json, sys

FOR = {
    'shop': 'the hero of the pop-up: its shop at night, seen from the bar end toward the street. Blackened-steel and oak '
            'shelving on both walls with EARF\'s Core table lamps in their tints, Mantle record players and records, a '
            'price card at each piece; a long walnut table with two Cores, a Mantle and a bowl of EARFcoins; Hemisphere '
            'pendants hung low in tints; and in the window, against the street, the Tropos pair in Ember on its low black '
            'plinth, facing out. ',
    'window': 'the pop-up from the sidewalk at night, as a passer-by sees it: one big pane of shopfront glass, a Tropos '
              'pair in Ember on a low black plinth in the window facing the street, the shop lit behind them (the shelves '
              'on both walls, the Hemispheres, the table, the bar), the felt drapes at the back. It has to stop someone '
              'walking past. ',
    'listening': 'the pop-up\'s listening room, behind the felt: a room of charcoal felt drapes on a ceiling track, a wool '
                 'rug, ten oak chairs in two rows facing the Tropos pair in Ember on oak plinths either side, toed in to '
                 'the middle seat; the decks on a table by the drape. Quiet is the rule here. ',
}

CONTEXT = """**The project:** a design mockup of the Planet EARF pop-up, the first step toward a proposed listening bar in
San Francisco: a vacant downtown storefront (7.6 x 15.2 m, 4 m to a dark painted ceiling, 36 people at most) taken for
eight weeks to two months. Nothing is built in: everything is brought in and leaves with the licence. Its owner is EARF,
which makes tinted cast-acrylic horn loudspeakers (the Tropos line, about $19,000 a pair), lamps (the Hemisphere pendant,
the Core table lamp) and a record player (Mantle). The pop-up is a shop that plays records: everything in it is for
sale, a licensed partner pours drinks on catered nights, and the listening room behind the felt holds sessions on the
hour. Simple surfaces (plaster walls, sealed concrete floor, steel, oak, felt) so the products carry the colour. The
images are to show the owner, partners and investors what the debut room will look like, photographed as a design
magazine would shoot a new shop at night.

**Also answer, in stage 1 and in the verdict:** would a design magazine publish this as a specific place, or is it a
generic shop?"""

FIXED = """**Fixed (never change):** EARF's products (their shape, colour and parts): the Tropos speakers (1293 mm tall,
tinted cast-acrylic cabinets with white batts inside, a resin horn), the Hemisphere pendant and the Core table lamp
(tinted acrylic with a frosted liner within), the Mantle record player, the EARFcoins, each in its tint as placed (the
shop shows the line in its tints, as a shop does). Only one Tropos pair exists, in Ember: it stands in the window and is
moved to the listening room's plinths for sessions, so a frame shows it in one place or the other, never two pairs. The plan (drawing A-401): the room's
size, the zones front to back (window, shop, bar, listening room, back of house), where the shelves, table, bar, ledges,
drapes, chairs and plinths stand, and their materials."""

MAY = """**What may change:** the light levels and colours of every source (the track spots on the shelves, the window
pair's spots, the table and bar spots, the listening pair's spots, the wash on the back felt, the room's soft fill, the
Hemispheres and Cores, the shelf LEDs, the street lamp), the camera, the exposure and grade, the materials' finish (the
plaster's tone, the floor's tone and sheen, the felt's colour within charcoal, the oak's stain), small props (records,
cards, glasses), haze, and the finish."""


def settings(sh, scale):
    room = next(p for p in sh['set']['props'] if p.get('fn') == 'popup')
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
        f"- camera: position {cam['position']} m (x 0 at the shopfront's glass to 15.2 at the back wall, y 0 at the "
        f"right-hand wall to 7.6 at the left-hand wall, z up), level, at {cam['target']}, lens {cam['lens_mm']} mm on 36 mm"
        + (f", f/{cam['fstop']} focused at {cam.get('focus')}" if cam.get('fstop') else ''),
        f"- EARF's lamps (the lamp hidden; the frosted liner glows by itself): each Hemisphere {dm.get('lamp_w')} W, its "
        f"liner's glow {dm.get('shade_glow')}; each Core {ob.get('lamp_w')} W, glow {ob.get('shade_glow')} (some shown unlit)",
        f"- the shelves' LED strips (emission strength, hidden from the camera): {room.get('led', 3.0)}",
        f"- track spots: the right wall's shelves {lamps('tr')}; the left wall {lamps('tl')}; the window pair {lamps('win')}; "
        f"the table {lamps('table')}; the bar {lamps('bar')}; the listening pair {lamps('stack')}; the seats {lamps('seats')}",
        f"- soft light: the back felt's wash {lamps('drape')}; the room's fill {lamps('fill')}; the street lamp outside "
        f"{lamps('street')}",
        f"- outside: the building opposite with {room.get('windows_lit', 0.35)} of its windows lit; the pavement "
        f"{room.get('pavement', '#45423E')}",
        f"- materials: the plaster {room.get('plaster', '#BDB4A6')}, the ceiling {room.get('ceiling', '#1E1D1C')}, the felt "
        f"{room.get('felt', '#1F1E1D')}, the floor a sealed concrete scan tinted {room.get('floor_tint', '#6A645D')}",
        f"- haze in the room's air: density {hz.get('density', 0)} per metre (0 = none)",
        f"- render: {json.dumps(R)}"])


def main():
    view, out = sys.argv[1], sys.argv[2]
    sh = json.load(open(sys.argv[sys.argv.index('--shot') + 1]))
    scale = float(sys.argv[sys.argv.index('--scale') + 1]) if '--scale' in sys.argv else 0.5
    txt = (f"# Card: {sh['title']}\n\n**What the frame is for:** {FOR[view]}\n\n{CONTEXT}\n\n{FIXED}\n\n{MAY}\n\n"
           f"**Settings now:**\n\n{settings(sh, scale)}\n")
    open(out, 'w').write(txt)
    print(out)


if __name__ == '__main__':
    main()
