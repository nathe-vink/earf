"""The critic's card for round 44's views of the lantern (street, bar, lantern), in the format of rounds 37 to 43.

    python3 spinoffs/barkhorn/planet/r44/r44_card.py VIEW OUT.md --shot IMG.shot.json [--scale 0.5]
"""
import json, sys

FOR = {
    'street': 'the hero: the bar from the sidewalk at night, through the shopfront glass, as a passer-by sees it. The '
              'shop in front (oak shelves with EARF\'s Core lamps in their tints, a terrazzo window plinth, an oak table), '
              'the bar beyond, and at the end of the long room the lantern: a freestanding oak box, its slotted face lit '
              'by a band of amber acrylic fins under the ceiling. It has to stop someone walking past. ',
    'bar': 'the bar room from the shop table, looking down the counter to the lantern\'s face: the terrazzo-faced counter '
           'with its quartzite top and stools, the back bar\'s lit shelves of bottles, the leather banquette, and ahead '
           'the lantern\'s slotted oak baffle, its lit band under the ceiling and the small oak porch that is its sound '
           'lock. ',
    'lantern': 'inside the lantern, the listening room, from its back bench: the Tropos pair in Ember on terrazzo plinths, '
               'Mother EARF (a 1.25 m globe of six slotted tinted acrylic discs, its rims glowing) on her terrazzo plinth '
               'between them, her colored shadow on the end-grain floor, oak slat walls and lid, lounge chairs on a rug. '
               'Calm and dark: a room for listening. ',
}

CONTEXT = """**The project:** a design mockup of Planet EARF, a proposed listening bar in a typical San Francisco
storefront (7.6 m wide, 24.4 m deep, 4 m ceilings, flats above). Its architecture: the listening room is a freestanding
oak box (the lantern) on its own isolated floor at the end of the bar room, its face a slotted oak baffle, a band of lit
amber acrylic fins under the ceiling, a small oak porch as its sound lock. Lasting materials: honed terrazzo floors,
a quartzite bar top, oiled oak, blackened steel, lime plaster, end-grain oak inside the box. Its owner is EARF, which
makes tinted cast-acrylic loudspeakers (the Tropos pair), lamps (Core, Hemisphere) and a record player (Mantle). The
images are to show the owner, partners and investors the architecture, photographed as a design magazine would shoot a
new bar at night.

**Also answer, in stage 1 and in the verdict:** would a design magazine publish this as a specific, well-made place, or
is it a generic bar?"""

FIXED = """**Fixed (never change):** the architecture as drawn (the plan, the lantern's size and place, the porch, the
counter, the back bar, the banquette, the shop's shelves and table, the window plinth, the ceiling height), its
materials (terrazzo, quartzite, oak, blackened steel, lime plaster, end-grain oak, the acrylic band's place and fins),
and EARF's products as placed (one Tropos pair in Ember, Mother EARF on her plinth, the Cores and Hemispheres in tints)."""

MAY = """**What may change:** every light level and color (the band's glow, the lantern's foot line, the downlights,
the shelf and back-bar lines, the speakers' and Mother's spots, the trap's graze, the fills, the street), the camera,
the exposure and grade, haze, the materials' finish within their kind (the terrazzo's chip size and ground tone, the
oak's tone, the plaster's tone, the glass's reflection), small props (glasses, records), and the finish."""


def settings(sh, scale):
    cam = sh['camera']; R = sh['render']; Ls = sh['lights']
    room = next(p for p in sh['set']['props'] if p.get('fn') == 'house')

    def lamps(prefix):
        xs = [l for k, l in Ls.items() if k.startswith(prefix)]
        if not xs:
            return 'none'
        l = xs[0]
        if l['type'] == 'spot':
            return f"{len(xs)} x spot {l['power_w']} W, {l['cone_deg']} deg, {l['color']} K"
        return f"{len(xs)} x area {l.get('irradiance')} W/m2, {l['color']} K"
    return '\n'.join([
        f"- frame: {sh['size'][0]} x {sh['size'][1]} as delivered; this proof at scale {scale}",
        f"- camera: {cam['position']} m looking at {cam['target']}, lens {cam['lens_mm']} mm, f/{cam.get('fstop')}",
        f"- the lantern's band: emission {room.get('band_glow', 0.8)} behind cast Smoke acrylic fins (IOR 1.49); its foot "
        f"line {room.get('foot_glow', 9.0)}; the shelf and back-bar lines {room.get('shelf_led', 1.0)}",
        f"- the shop wall: {lamps('shop')}; the table: {lamps('table')}; the counter: {lamps('ctr')}; the banquette: {lamps('bq')}",
        f"- the baffle's graze: {lamps('baffle')}; the route: {lamps('route')}; the fill: {lamps('fill')}",
        f"- inside the lantern: the pair {lamps('stack')}; Mother EARF {lamps('mother')}; the trap {lamps('trap')}; "
        f"fill {lamps('infill')}",
        f"- haze {sh['haze']['density']} per meter; glass reflection {room.get('glass_gloss', 0.5)}",
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
