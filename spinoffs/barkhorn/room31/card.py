"""The critic's card for a room 31 frame (critic/PROMPT-promo.md, step 1): what the frame is for, what is fixed, what
may change, and the shot's settings as they are.

    python3 spinoffs/barkhorn/room31/card.py SHOT.json OUT.md [--scale 0.5]
"""
import json, sys

FIXED = """**Fixed (never change):** the speaker, EARF's Cloud loudspeaker in the colour Poison: its shape, its colour, its parts.
It is a 1293 mm tall horn loudspeaker, a cabinet of 20 mm tinted cast acrylic lined inside with white polyester batts
in voile sleeves between its ribs (light through the cabinet shows them), its woofer under a cloth cover, under a horn
in tinted cast resin; sold at about $20,000 a pair. Its reference colour: white light after 25 mm of its acrylic is
#B2C9A2; the horn's deep tint #4C6A36; the cover cloth #6F7F66; the cover's disc #2E4A2C. The pair stays a pair (the two
the same), cover on. Each speaker's mains lead runs visibly to a wall socket (the owner asked for it); it may be re-routed,
never removed. The record player on the credenza is EARF's own (Cumulus, clear acrylic): it may move, not change."""

FOR = """**What the frame is for:** the home page's room band at earf.world (shown 1800 px wide at 16:9) and the look book's
room page: the image that says "this is what they look like in a home". A heading ("A pair of Poison.") is set over the
wall. The brief: a real living room photographed as a design magazine or a luxury house would shoot it; late-afternoon
sun through tall windows, crossing the room and passing through both cabinets; materials photographed, at real scale;
few props, all real; camera at about eye level, squared to the back wall, verticals straight, each speaker about half the
frame's height."""

MAY = """**What may change:** everything about the set, the light, the camera and the finish (the room, its surfaces and props,
the sun and every lamp, the lens, the exposure and grade). The speakers may be moved or turned."""


def settings(sh, scale):
    st = sh['set']; cam = sh['camera']; R = sh['render']
    lines = []
    lines.append(f"- frame: {sh['size'][0]} x {sh['size'][1]} as delivered; this proof at scale {scale} "
                 f"({int(sh['size'][0] * scale)} x {int(sh['size'][1] * scale)})")
    lines.append(f"- camera: position {cam['position']} m (z up; the speakers' fronts face -y), aimed level (shift lens, "
                 f"verticals straight) at {cam['target']}, lens {cam['lens_mm']} mm on 36 mm, f/{cam.get('fstop')}, "
                 f"focus {cam.get('focus')}")
    pr = sh['products'][0]
    lines.append(f"- speakers: at {[i['position'] for i in pr['instances']]} m, toe-in {[i['rotate_z'] for i in pr['instances']]} deg")
    w, d, h = st['size']
    lines.append(f"- room: {w} x {d} m, {h} m high, centre {st['center']}; back wall face y {st['center'][1] + d / 2:.2f}, "
                 f"left wall face x {st['center'][0] - w / 2:.2f} (glazed)")
    for i, wi in enumerate(st['windows']):
        lines.append(f"- window {i}: {wi['wall']} wall, along {wi['along']} m from its centre, sill {wi['sill']} m, "
                     f"size {wi['size']} m, mullions {wi['mullions']}, frame {wi.get('frame')}")
    s = sh['sun']
    lines.append(f"- sun: azimuth {s['azimuth_deg']} deg (0 = from the camera side, -90 = from the left), elevation "
                 f"{s['elevation_deg']} deg, irradiance {s['irradiance']} W/m2, size {s.get('angle_deg')} deg, colour {s['color']}")
    lines.append(f"- sky (light through the glazing): {sh['sky']}")
    for k, L in sh['lights'].items():
        if not L.get('off'):
            lines.append(f"- lamp `{k}`: {L}")
    for i, p in enumerate(st['props']):
        q = {k: v for k, v in p.items() if k not in ('kind', 'path', 'points')}
        if p.get('kind') == 'cable':
            q = {'cable': 'mains lead, speaker to wall socket', 'd': p['d']}
        lines.append(f"- prop {i}: {json.dumps(q)}")
    lines.append(f"- render: {R}")
    return '\n'.join(lines)


def main():
    sh = json.load(open(sys.argv[1])); out = sys.argv[2]
    scale = float(sys.argv[sys.argv.index('--scale') + 1]) if '--scale' in sys.argv else 0.5
    txt = f"# Card: a pair of Poison at home\n\n{FOR}\n\n{FIXED}\n\n{MAY}\n\n**Settings now:**\n\n{settings(sh, scale)}\n"
    open(out, 'w').write(txt)
    print(out)


if __name__ == '__main__':
    main()
