"""Brighten a shot's light sources by group, not its grade (the lead, 2026-10-19, on the review set: "Brighten the
light sources, not the grade"). Groups are light-name prefixes; `glow:NAME` scales a room setting (an emissive glow).

    python3 spinoffs/barkhorn/planet/loft/lift_shot.py IN.json OUT.json pend=3 tlamp=3 glow:shelf_glow=1.5 ...
"""
import json, re, sys


def lift(s, factors):
    for k, l in s['lights'].items():
        g = re.match(r'[a-zA-Z-]+?(?=\d|$)', k).group(0).rstrip('-')
        for key, f in factors.items():
            if not key.startswith('glow:') and g == key:
                for q in ('power_w', 'irradiance'):
                    if q in l:
                        l[q] = round(l[q] * f, 3)
    for p in s['set']['props']:
        if 'module' in p:
            for key, f in factors.items():
                if key.startswith('glow:'):
                    n = key[5:]
                    if n in p:
                        p[n] = round(p[n] * f, 4)
    return s


if __name__ == '__main__':
    fac = {a.split('=')[0]: float(a.split('=')[1]) for a in sys.argv[3:]}
    s = lift(json.load(open(sys.argv[1])), fac)
    json.dump(s, open(sys.argv[2], 'w'), indent=1)
    print(sys.argv[2], fac)
