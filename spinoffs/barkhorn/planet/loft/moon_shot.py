"""Re-make an earlier loft shot with EARF Moon in place of the placeholder lamps (the lead, 2026-10-19): the plain table
lamps and their bulbs out, a smoked Moon table lamp at each of their spots, a Moon pendant at each downlight over the
bar in place of the frosted tubes. Everything else, the camera and the light, stays as the shot had it.

    python3 spinoffs/barkhorn/planet/loft/moon_shot.py IN.shot.json OUT.json TABLE_W PENDANT_W [GLOW]
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loft_plan as LP                                              # noqa: E402


def moon(s, table_w, pendant_w, glow=0.6, flavour='smoked'):
    room = next(p for p in s['set']['props'] if p.get('module') == 'planet_loft')
    spots = room.get('table_lamps') or []
    room['table_lamps'] = []; room['moon_pendants'] = True
    s['lights'] = {k: l for k, l in s['lights'].items() if not k.startswith('tlamp')}
    y = round(LP.BAR_FRONT + 0.18, 4)
    s['set']['props'] += [
        {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'table', 'spots': spots, 'flavour': flavour,
         'lamp_w': table_w, 'lamp_k': 2700, 'shade_glow': glow},
        {'kind': 'kit', 'shape': 'ext', 'module': 'earf_moon', 'fn': 'pendant', 'flavour': flavour,
         'spots': [[x, y, LP.PENDANT_RIM] for x in LP.PENDANTS], 'ceiling': LP.CEIL, 'lamp_w': pendant_w,
         'lamp_k': 2700, 'shade_glow': glow}]
    return s


if __name__ == '__main__':
    a = sys.argv
    s = moon(json.load(open(a[1])), float(a[3]), float(a[4]), float(a[5]) if len(a) > 5 else 0.6)
    json.dump(s, open(a[2], 'w'), indent=1)
    print(a[2], len(s['lights']), 'lights')
