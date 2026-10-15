"""The globe as an object (round 22): earth.py's six rings as six discs of the Clouds' tinted cast acrylic, slotted
together into a desk globe on a steel ring, its axis leaning 23.4 degrees as the mark's does; rendered as the speakers
are, so the Discs mark can be seen as the thing it suggests.

    .venv-fab/bin/python spinoffs/barkhorn/globe_object.py     ->  out-globe/render/earf-globe.glb,
                                                                   studio/products/earf-globe.json and the shot
                                                                   studio/shots/barkhorn/globe22/globe.json
    python3 studio/engine/render.py studio/shots/barkhorn/globe22/globe.json

- Six discs 8 mm thick, 240 across: the three meridians (Poison, Ice, Haze) whole circles through the poles, 60 apart,
  and the three parallels (Flare at 40 N, Dust at the equator, Acid at 40 S) at the sphere's own radius there, so every
  edge lies on one sphere. Where two discs cross, the later is slotted round the earlier (0.3 clear), as they would be
  cut and cemented: Ice's meridian, the one facing the camera, whole; the others slotted round it in turn.
- Each disc polished cast acrylic in its Cloud's cabinet tint (the cabinets' `deep`, which is the colour after 25 mm;
  here after 14), so a face is a clear tint and an edge, seen along 240 mm of it, glows deep. (The horns' deeper tints,
  tried first, stacked to mud where four discs overlap.)
- The stand a brushed steel ring, 92 across and 20 high; the globe rests in it.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
LEAN, ELEV, LAT = 23.44, 22.0, 40.0                      # earth.py's (which needs shapely, not in the fab venv)
R, T, GAP = 120.0, 8.0, 0.3
TINTS = {'flare': '#F2A29C', 'dust': '#F2B184', 'acid': '#F2D06B', 'poison': '#B2C9A2', 'ice': '#B5D9EE', 'haze': '#BEADD8'}
RING = dict(r_out=46.0, r_in=38.0, h=20.0)


def discs():
    """The six discs in the globe's frame (its axis z, the camera along -y), each slotted round those before it."""
    from build123d import Cylinder, Rot, Pos
    full = []
    for name, lam in (('ice', 90.0), ('poison', 30.0), ('haze', 150.0)):
        full.append((name, Rot(Z=lam - 90) * Rot(X=90) * Cylinder(R, T), Rot(Z=lam - 90) * Rot(X=90) * Cylinder(R + 1, T + 2 * GAP)))
    for name, phi in (('dust', 0.0), ('flare', LAT), ('acid', -LAT)):
        r, z = R * math.cos(math.radians(phi)), R * math.sin(math.radians(phi))
        full.append((name, Pos(0, 0, z) * Cylinder(r, T), Pos(0, 0, z) * Cylinder(r + 1, T + 2 * GAP)))
    out = []
    for i, (name, solid, _) in enumerate(full):
        for _, _, slab in full[:i]:
            solid = solid - slab
        out.append((name, solid))
    return out


def build(out=os.path.join(HERE, 'out-globe')):
    from build123d import Cylinder, Pos, Rot
    from model import Part, Product, Machined
    import render
    lift = RING['h'] + math.sqrt(R * R - RING['r_in'] ** 2)          # the globe's centre, resting in the ring
    parts = [Part(f'disc-{n}', Pos(0, 0, lift) * Rot(Y=LEAN) * s, Machined('cast-acrylic', 'cnc-mill'), finish=f'acrylic-{n}')
             for n, s in discs()]
    ring = Pos(0, 0, RING['h'] / 2) * (Cylinder(RING['r_out'], RING['h']) - Cylinder(RING['r_in'], RING['h'] + 2))
    parts.append(Part('stand', ring, Machined('stainless', 'cnc-mill'), finish='steel'))
    mats = {f'acrylic-{n}': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': c, 'radius': 0.014, 'roughness': 0.03}
            for n, c in TINTS.items()}
    mats['steel'] = {'preset': 'metal', 'color': '#C9C9C6', 'roughness': 0.32}
    product = Product('earf-globe', 'EARF globe', 'The globe in six tinted cast acrylics', params={}, parts=lambda p: parts,
                      count=1, materials=mats)
    glb, pf = render.write(product, parts, out, proof=False)
    return glb, pf, lift


def shot(lift):
    """The globe from 22 degrees up, as the mark is drawn, on a paper sweep, lit as the look book's speakers are."""
    c = [0.0, 0.0, lift / 1000]
    el, dist = math.radians(ELEV), 1.55
    s = {'product': {'def': 'studio/products/earf-globe.json', 'flavour': 'default',
                     'instances': [{'position': [0, 0, 0], 'rotate_z': 0, 'flavour': 'default'}]},
         'set': {'kind': 'sweep', 'color': '#F1EFEA', 'width': 4.0, 'front': 3.0, 'depth': 1.2, 'radius': 0.8, 'height': 3.0},
         'lights': {
             'key': {'type': 'area', 'size_m': [1.6, 1.2], 'orbit': {'azimuth_deg': -40, 'elevation_deg': 45, 'distance_m': 2.2},
                     'target': c, 'irradiance': 2.6, 'color': '#FFF3E1'},
             'fill': {'type': 'area', 'size_m': [2.0, 1.6], 'orbit': {'azimuth_deg': 35, 'elevation_deg': 15, 'distance_m': 2.4},
                      'target': c, 'irradiance': 0.8, 'color': '#FFF7EA'},
             'back': {'type': 'area', 'size_m': [1.2, 0.8], 'orbit': {'azimuth_deg': 170, 'elevation_deg': 35, 'distance_m': 1.8},
                      'target': c, 'irradiance': 1.6, 'color': '#FFF7EA'}},
         'render': {'samples': 160, 'adaptive': 0.02, 'denoise': True, 'clamp': 8, 'bounces': 16, 'view': 'Khronos PBR Neutral',
                    'exposure': 0.0, 'white_balance_k': 5600, 'white_balance_tint': 3.0},
         'title': 'EARF globe, six tinted acrylics', 'size': [1400, 1400],
         'camera': {'position': [0.0, -dist * math.cos(el), c[2] + dist * math.sin(el)], 'target': [0.0, 0.0, c[2] - 0.012],
                    'lens_mm': 105.0, 'level': False},
         'sky': {'kind': 'gradient', 'zenith': '#C4C2BE', 'horizon': '#CFCDC8', 'ground': '#5A5650', 'strength': 0.7}}
    d = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'globe22'); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'globe.json'); json.dump(s, open(p, 'w'), indent=1)
    return p


if __name__ == '__main__':
    glb, pf, lift = build()
    print(os.path.relpath(glb, ROOT), os.path.relpath(pf, ROOT), os.path.relpath(shot(lift), ROOT))
