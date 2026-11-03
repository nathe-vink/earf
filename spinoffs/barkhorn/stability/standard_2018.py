"""Tropos with horn A against IEC 62368-1:2018/2023's stability tests for MS3 floor-standing equipment (the coordinator's
research of 2026-11-03, wf_a73d7898-d30; stability/standard-2018.md), on the cabinet's own four feet, and on a slim
light plate (a separately sold stand, 8.10).

    python3.11 spinoffs/barkhorn/stability/standard_2018.py     ->  standard_2018.json beside this file, and a table

The mass and centre of mass come from the render models as in com.py (the Cloud with its formed horn, the default since
2026-11-03, and the variants' bronze posts and caldera; no plinth). Tipping is geometric: about each edge of the
support rectangle, the speaker tips at the angle whose tangent is the centre of mass's arm over its height.
"""
import json, math, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import com                                                               # noqa: E402

G = 9.81
# the cabinet's own feet (com.py): centres, and the pads' outer edges; x -left +right, y -front +back, metres
FEET = {'feet centres': (-0.23, 0.23, -0.1887, 0.1813), 'pad edges': (-0.25, 0.25, -0.2087, 0.2013)}
CAB = dict(x=(-0.28, 0.28), y=(-0.2137, 0.2063))        # the cabinet's outline in the asset's frame
# the slim light plate (stability/standard-2018.md, the coordinator's item 3): the cabinet's footprint, its feet 20 in
# from its corners; `h` its height to the cabinet's feet, `kg` its mass, its centre of mass `zc` up
PLATE = dict(h=0.050, kg=5.6, zc=0.020, feet=(-0.26, 0.26, -0.1937, 0.1863), pads=(-0.28, 0.28, -0.2137, 0.2063))


def tilt(C, box):
    x0, x1, y0, y1 = box
    arms = {'forward': C[1] - y0, 'back': y1 - C[1], 'left': C[0] - x0, 'right': x1 - C[0]}
    return {k: dict(arm_mm=round(a * 1000), tips_at_deg=round(math.degrees(math.atan2(a, C[2])), 1)) for k, a in arms.items()}


def force(M, C, box, h, F):
    """A horizontal force F (N) at height h, each way: restoring over overturning about the far edge."""
    x0, x1, y0, y1 = box
    arms = {'forward': C[1] - y0, 'back': y1 - C[1], 'left': C[0] - x0, 'right': x1 - C[0]}
    return {k: dict(restoring_Nm=round(M * G * a, 1), overturning_Nm=round(F * h, 1), ratio=round(M * G * a / (F * h), 2))
            for k, a in arms.items()}


def main():
    hide_c = ['cloth-disc', 'post-*', 'post-sleeves', 'post-sockets', 'woofer-ring']          # horn A: the formed horn shown
    P = {**com.parts('studio/products/barkhorn-cloud.json', hide_c)[0],
         **com.parts('studio/products/barkhorn-variants.json', ['horn-topo*', 'horn-strata', 'base-*'])[0]}
    M = sum(p['mass'] for p in P.values())
    C = [sum(p['mass'] * p['c'][i] for p in P.values()) / M for i in range(3)]
    top = max(p['zmax'] for p in P.values())
    # the horn's overhang past the cabinet (from its vertices' y and x)
    boxes = json.load(open(com.ROOT / 'spinoffs/barkhorn/out-cloud/render/barkhorn-cloud.json'))['parts']   # mm, the Cloud's frame
    hb = [boxes[n] for n in ('waveguide', 'horn-throat', 'horn-pod', 'waveguide-cap') if n in boxes]
    ov = dict(front_mm=round(max(0.0, -min(b[1] for b in hb))), back_mm=round(max(0.0, max(b[4] for b in hb) - 420.0)),
              sides_mm=round(max(0.0, -min(b[0] for b in hb), max(b[3] for b in hb) - 560.0)))
    res = dict(mass_kg=round(M, 1), com_m=[round(x, 4) for x in C], top_m=round(top, 4), horn_overhang=ov)
    # 8.6.2.2 (a) / 8.6.3: a 10 degree tilt; 8.6.5's alternative (if it applied): 15 degrees
    res['tilt'] = {k: tilt(C, b) for k, b in FEET.items()}
    # 8.6.2.2 (c): 13 % of the weight horizontally (at most 100 N), at the most unfavourable point at or below 1.5 m
    h = min(top, 1.5)
    F = min(0.13 * M * G, 100.0)
    res['push_13pct'] = dict(F_N=round(F, 1), at_m=round(h, 3), feet=force(M, C, FEET['feet centres'], h, F))
    # the old reading for comparison: 20 % (at most 250 N) at the top
    F20 = min(0.2 * M * G, 250.0)
    res['push_20pct_old'] = dict(F_N=round(F20, 1), at_m=round(top, 3), feet=force(M, C, FEET['feet centres'], top, F20))
    # 8.6.2.3: 800 N down on any surface at least 125 x 200 below 1 m: the cabinet's top (its height below)
    ztop = max(p['zmax'] for n, p in P.items() if n == 'top')
    load = {}
    x0, x1, y0, y1 = FEET['feet centres']
    for k, (edge, foot) in {'front': (CAB['y'][0], y0), 'back': (CAB['y'][1], y1), 'left': (CAB['x'][0], x0), 'right': (CAB['x'][1], x1)}.items():
        over = abs(edge - foot)                   # how far the top's edge reaches past the feet's line
        arm = abs((C[1] if k in ('front', 'back') else C[0]) - foot)
        load[k] = dict(edge_past_feet_mm=round(over * 1000), overturning_Nm=round(800 * over, 1),
                       restoring_Nm=round(M * G * arm, 1), ratio=round(M * G * arm / (800 * over), 1) if over > 0 else None)
    res['load_800N'] = dict(surface='the cabinet top, 560 x 420', height_m=round(ztop, 3), applies=ztop < 1.0, edges=load)
    # a 5 degree tilt back: the centre of mass's arm toward the back feet as the speaker leans back 5 degrees
    a5 = math.radians(5)
    yb = FEET['feet centres'][3]
    arm_after = (yb - C[1]) * math.cos(a5) - C[2] * math.sin(a5)
    res['lean_back_5deg'] = dict(arm_mm_before=round((yb - C[1]) * 1000), arm_mm_after=round(arm_after * 1000),
                                 tips_back_at_deg=res['tilt']['feet centres']['back']['tips_at_deg'])
    # on the plate: the speaker raised by its height, the plate's own mass low
    Mp = M + PLATE['kg']
    Cp = [(M * C[0]) / Mp, (M * C[1]) / Mp, (M * (C[2] + PLATE['h']) + PLATE['kg'] * PLATE['zc']) / Mp]
    res['on_plate'] = dict(mass_kg=round(Mp, 1), com_m=[round(x, 4) for x in Cp],
                           tilt={'plate feet centres': tilt(Cp, PLATE['feet']), 'plate edges': tilt(Cp, PLATE['pads'])})
    json.dump(res, open(Path(__file__).with_name('standard_2018.json'), 'w'), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
