"""The critic's card for round 43's Amsterdam views of Mother EARF at 2 m (quay, shadow, water), in the format of the
pop-up's card (`r43_card.py`).

    python3 spinoffs/barkhorn/planet/r43/r43_ams_card.py ams-VIEW OUT.md --shot IMG.shot.json [--scale 0.5]
"""
import json, sys

FOR = {
    'quay': 'image 1 of a light-festival entry: the work at night from eye level on the quay, as a visitor on the canal '
            'route first meets it: the globe on its plinth at the water\'s edge, its rims glowing in six colours, the '
            'canal and the gabled houses across the water behind it. ',
    'shadow': 'image 2 of the entry: the hard spot\'s coloured shadow, the globe drawn a second time in light on the '
              'quay\'s paving toward the water, seen from a little higher so the shadow and the globe read together. ',
    'water': 'the work from the water, as the festival\'s boat route sees it: low, across the canal, the globe on the '
             'quay with its reflection and the spot\'s beam. ',
}

CONTEXT = """**The project:** a design mockup for an entry to the Amsterdam Light Festival (Edition 16, on the canals,
25 November 2027 to 16 January 2028): Mother EARF, a light artwork by a San Francisco designer. It is a globe of six
slotted discs of tinted cast acrylic (three meridians in green, orange and violet; three parallels in red, blue and
yellow), its axis leaning 23.4 degrees, 2 m across, standing on a low blackened-steel plinth at a quay's edge. Light
enters each disc at its rim (an LED strip in a groove along the edge), so the rims glow in their colours and the faces
stay clear; one hard spot on a mast throws the globe's coloured shadow across the paving. The images go to a festival
jury, which judges whether the work is striking, feasible and right for the canals at night; they should read as
night photographs of the work in place.

**Also answer, in stage 1 and in the verdict:** would a jury see a specific, striking work in a real place, or a
generic render?"""

FIXED = """**Fixed (never change):** the globe's design: six flat slotted discs, their colours (green, orange, violet
meridians; red, blue, yellow parallels), the 23.4 degree tilt, 2 m across, 25 mm discs, rim-lit with clear faces; the
low round plinth; a site on a quay at the water's edge in Amsterdam at night."""

MAY = """**What may change:** every light level and colour (the rims' glow, the hard spot's power, aim and colour, the
street lamps, the lit windows across the canal, the far-quay fill, the sky's brightness), the camera, the exposure and
grade, haze, the materials' finish of the quay, water and houses (the paving, the stone kerb, the water's ripple and
gloss, the brick), and small props of the street (bollards, a bicycle, a bench, people far off)."""


def settings(sh, scale):
    canal = next(p for p in sh['set']['props'] if p.get('fn') == 'canal')
    g = next(p for p in sh['set']['props'] if p.get('fn') == 'globe')
    cam = sh['camera']; L = sh['lights']; hz = sh.get('haze') or {}
    hard = L.get('hard', {})
    return '\n'.join([
        f"- frame: {sh['size'][0]} x {sh['size'][1]} as delivered; this proof at scale {scale}",
        f"- camera: position {cam['position']} m (x along the quay, y across the canal: the quay at y < 0, the water from "
        f"0 to 18, the far houses beyond; z up from the paving, the water 1.1 m below it), level, at {cam['target']}, lens "
        f"{cam['lens_mm']} mm" + (f", f/{cam['fstop']} focused at {cam.get('focus')}" if cam.get('fstop') else ''),
        f"- the globe: {g.get('size')} m across at {g.get('at')}, discs {g.get('t')} m; the rims' glow (emission strength) "
        f"{g.get('rim')}; the plinth {g.get('base_h')} m high",
        f"- the hard spot: {hard.get('power_w')} W, cone {hard.get('cone_deg')} deg, {hard.get('color')} K, from "
        f"{hard.get('position')} at {hard.get('target')}",
        f"- the street lamps: 2 x point, {L.get('lamp-a', {}).get('power_w')} W, 2200 K; the far quay's fill "
        f"{L.get('far', {}).get('irradiance')} W/m2 at 2400 K",
        f"- the houses across: {canal.get('lit')} of the windows lit, their glow {canal.get('window_glow')}",
        f"- sky: a night gradient at strength {sh['sky'].get('strength')}; haze {hz.get('density', 0)} per metre",
        f"- render: {json.dumps(sh['render'])}"])


def main():
    view, out = sys.argv[1].replace('ams-', ''), sys.argv[2]
    sh = json.load(open(sys.argv[sys.argv.index('--shot') + 1]))
    scale = float(sys.argv[sys.argv.index('--scale') + 1]) if '--scale' in sys.argv else 0.5
    txt = (f"# Card: {sh['title']}\n\n**What the frame is for:** {FOR[view]}\n\n{CONTEXT}\n\n{FIXED}\n\n{MAY}\n\n"
           f"**Settings now:**\n\n{settings(sh, scale)}\n")
    open(out, 'w').write(txt)
    print(out)


if __name__ == '__main__':
    main()
