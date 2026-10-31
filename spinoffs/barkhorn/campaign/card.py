"""The critic's card for a Tropos campaign still (critic/PROMPT-promo.md, step 1): what the frame is for, what is fixed,
what may change, and the shot's settings as they are. The room's settings are listed as room31's card lists them.

    python3 spinoffs/barkhorn/campaign/card.py NAME SHOT.json OUT.md [--scale 0.5]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'room31'))
import card as room_card                                             # noqa: E402

COLOURS = {
    'Poison': ('#B2C9A2', '#4C6A36', '#2E4A2C'),
    'Ember': ('#F2A29C', '#C8262B', '#7A1A1C'),
}

FIXED = """**Fixed (never change):** the speaker, EARF's Tropos loudspeaker in the colour {col}: its shape, its colour, its
parts. It is a 1293 mm tall horn loudspeaker: a cabinet of 20 mm tinted cast acrylic, lined inside with white polyester
batts in voile sleeves between its ribs (light through the cabinet shows them), its woofer under a cover, and above it a
horn pressure-formed from a deeper-tinted lot of the same cast acrylic, on four posts. Sold at about $20,000 a pair. Its
reference colour: white light after 25 mm of the cabinet's acrylic is {cab}; after 10 mm of the horn's, {horn}; the
cover's disc {disc}."""

MAY = """**What may change:** everything about the set, the light, the camera and the finish (surfaces and props, the sun
and every lamp, the lens, the exposure and grade). The speaker may be moved or turned."""

FOR = {
    'room': ('Poison', """**What the frame is for:** the home page's room band and the deck's "at home" page: a pair in
a real living room at golden hour, shown 1800 px wide at 16:9, a heading set over the wall. Late sun through tall
windows crossing the room and passing through both cabinets; few props, all real; camera at eye level, squared to the
back wall, verticals straight. Each speaker's mains lead runs to a wall socket (kept on purpose)."""),
    'night': ('Ember', """**What the frame is for:** the night image for the deck and the press: speakers on a wall
of a building at night, each lit from below so the light passes up through its tinted acrylic and glows. A wide
banner (12:5); room for a line of type in the dark sky. One speaker leads in Ember; the others show the range."""),
    'inside': ('Ember', """**What the frame is for:** the "see into it" story: light passing through the cabinet shows
how it is made: the ribs, the batts in their sleeves, the woofer's basket, the horn above. A 4:5 portrait for the press
kit and social; the inside should read at a glance."""),
    'corner': ('Ember', """**What the frame is for:** the craft macro: a polished edge of the 20 mm acrylic and a
cemented joint, so close the polish and the clarity of the joint are the subject; the horn above, out of focus. A
square for the press kit and the deck's "how it's made" page."""),
    'above': ('Ember', """**What the frame is for:** the horn from above: a high view over the front corner, so the
horn's mouth, its flare and the light through its deep tint are the subject, with the cabinet below. A 3:2 still life
on a bright studio set for the deck and the press."""),
}


def generic(sh, scale):
    lines = [f"- frame: {sh['size'][0]} x {sh['size'][1]} as delivered; this proof at scale {scale} "
             f"({int(sh['size'][0] * scale)} x {int(sh['size'][1] * scale)})"]
    lines.append(f"- camera: {json.dumps(sh['camera'])} (metres, z up; the speaker faces -y)")
    pr = sh.get('product') or sh['products'][0]
    for i in pr['instances']:
        lines.append(f"- speaker: {json.dumps({k: v for k, v in i.items() if k in ('position', 'rotate_z', 'flavour')})}")
    for k in ('set', 'sky', 'haze', 'materials', 'finish'):
        if k in sh:
            lines.append(f"- {k}: {json.dumps(sh[k])}")
    for k, L in sh.get('lights', {}).items():
        if not (isinstance(L, dict) and L.get('off')):
            lines.append(f"- lamp `{k}`: {json.dumps(L)}")
    lines.append(f"- render: {json.dumps(sh['render'])}")
    return '\n'.join(lines)


def main():
    name, shot, out = sys.argv[1:4]
    scale = float(sys.argv[sys.argv.index('--scale') + 1]) if '--scale' in sys.argv else 0.5
    sh = json.load(open(shot))
    col, for_ = FOR[name]
    cab, horn, disc = COLOURS[col]
    sets = room_card.settings(sh, scale) if name == 'room' else generic(sh, scale)
    txt = (f"# Card: Tropos, {name}\n\n{for_}\n\n{FIXED.format(col=col, cab=cab, horn=horn, disc=disc)}\n\n{MAY}\n\n"
           f"**Settings now:**\n\n{sets}\n")
    open(out, 'w').write(txt)
    print(out)


if __name__ == '__main__':
    main()
