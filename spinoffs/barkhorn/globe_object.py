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

Round 23 (the owner: "Could try one where the even lines look like acrylic tubes"): `--tubes` builds the six rings as
tubes of tinted cast acrylic instead, 12.6 mm across with 1.6 mm walls (the mark's tube, earth.py W_TUBE, on a globe
240 across), each in its ring's colour (the mark's own hues, not the cabinets' tints), slotted round one another as the
discs are, and renders them floating over a paper sweep from the mark's own view, as a reference for earth.py's tubes:

    .venv-fab/bin/python spinoffs/barkhorn/globe_object.py --tubes  ->  out-globe/render/earf-globe-tubes.glb,
                                                                      studio/products/earf-globe-tubes.json and the shot
                                                                      studio/shots/barkhorn/globe23/tubes.json
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
LEAN, ELEV, LAT = 23.44, 16.0, 40.0                      # earth.py's (which needs shapely, not in the fab venv; tip 16 since 27f)
R, T, GAP = 120.0, 8.0, 0.3
TINTS = {'flare': '#F2A29C', 'dust': '#F2B184', 'acid': '#F2D06B', 'poison': '#B2C9A2', 'ice': '#B5D9EE', 'haze': '#BEADD8'}
RING = dict(r_out=46.0, r_in=38.0, h=20.0)
HUES = {'flare': '#D2382F', 'dust': '#E5732A', 'acid': '#E9B320', 'poison': '#4F7F3A', 'ice': '#4A90C8', 'haze': '#6C4BA3'}   # marks.py's
TUBE_R, TUBE_WALL = 6.3, 1.6                             # round 23's tubes: earth.py's W_TUBE (0.105 of the radius) on R


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


def tubes():
    """The six rings as hollow tubes in the globe's frame (its axis z, the camera along -y), centred on the origin, each
    slotted round those before it (the meridian facing the camera whole)."""
    from build123d import Torus, Rot, Pos
    ring = lambda major: Torus(major, TUBE_R) - Torus(major, TUBE_R - TUBE_WALL)
    full = [(name, Rot(Z=lam - 90) * Rot(X=90) * ring(R), Rot(Z=lam - 90) * Rot(X=90) * Torus(R, TUBE_R + GAP))
            for name, lam in (('ice', 90.0), ('poison', 30.0), ('haze', 150.0))]
    for name, phi in (('dust', 0.0), ('flare', LAT), ('acid', -LAT)):
        r, z = R * math.cos(math.radians(phi)), R * math.sin(math.radians(phi))
        full.append((name, Pos(0, 0, z) * ring(r), Pos(0, 0, z) * Torus(r, TUBE_R + GAP)))
    out = []
    for i, (name, solid, _) in enumerate(full):
        for _, _, sleeve in full[:i]:
            solid = solid - sleeve
        out.append((name, solid))
    return out


def build_tubes(out=os.path.join(HERE, 'out-globe')):
    """The tubes' render model, the globe leaning as the mark's; returns its files and the centre's height over the
    model's lowest point."""
    from build123d import Rot
    from model import Part, Product, Machined
    import render
    parts = [Part(f'tube-{n}', Rot(Y=LEAN) * s, Machined('cast-acrylic', 'bent'), finish=f'tube-{n}') for n, s in tubes()]
    low = min(p.solid.bounding_box().min.Z for p in parts)
    mats = {f'tube-{n}': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': c, 'radius': 0.005, 'roughness': 0.02}
            for n, c in HUES.items()}
    product = Product('earf-globe-tubes', 'EARF globe in tubes', 'The globe as six tinted acrylic tubes', params={},
                      parts=lambda p: parts, count=1, materials=mats)
    glb, pf = render.write(product, parts, out, proof=False)
    return glb, pf, -low


def shot_tubes(centre, float_mm=45.0):
    """The tubes from the mark's view (22 degrees up, a long lens, nearly flat), floating over a paper sweep."""
    z = (float_mm + centre) / 1000
    c = [0.0, 0.0, z]
    el, dist = math.radians(ELEV), 2.0
    s = {'product': {'def': 'studio/products/earf-globe-tubes.json', 'flavour': 'default',
                     'instances': [{'position': [0, 0, float_mm / 1000], 'rotate_z': 0, 'flavour': 'default'}]},
         'set': {'kind': 'sweep', 'color': '#F1EFEA', 'width': 4.0, 'front': 3.0, 'depth': 1.2, 'radius': 0.8, 'height': 3.0},
         'lights': {
             'key': {'type': 'area', 'size_m': [1.6, 1.2], 'orbit': {'azimuth_deg': -40, 'elevation_deg': 45, 'distance_m': 2.2},
                     'target': c, 'irradiance': 2.6, 'color': '#FFF3E1'},
             'fill': {'type': 'area', 'size_m': [2.0, 1.6], 'orbit': {'azimuth_deg': 35, 'elevation_deg': 15, 'distance_m': 2.4},
                      'target': c, 'irradiance': 0.8, 'color': '#FFF7EA'},
             'back': {'type': 'area', 'size_m': [1.2, 0.8], 'orbit': {'azimuth_deg': 170, 'elevation_deg': 35, 'distance_m': 1.8},
                      'target': c, 'irradiance': 1.6, 'color': '#FFF7EA'}},
         'render': {'samples': 96, 'adaptive': 0.02, 'denoise': True, 'clamp': 8, 'bounces': 16, 'view': 'Khronos PBR Neutral',
                    'exposure': 0.0, 'white_balance_k': 5600, 'white_balance_tint': 3.0},
         'title': 'EARF globe, six tinted acrylic tubes', 'size': [1200, 1200],
         'camera': {'position': [0.0, -dist * math.cos(el), z + dist * math.sin(el)], 'target': [0.0, 0.0, z - 0.008],
                    'lens_mm': 200.0, 'level': False},
         'sky': {'kind': 'gradient', 'zenith': '#C4C2BE', 'horizon': '#CFCDC8', 'ground': '#5A5650', 'strength': 0.7}}
    d = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'globe23'); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, 'tubes.json'); json.dump(s, open(p, 'w'), indent=1)
    return p


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
    if '--tubes' in sys.argv:
        glb, pf, centre = build_tubes()
        print(os.path.relpath(glb, ROOT), os.path.relpath(pf, ROOT), os.path.relpath(shot_tubes(centre), ROOT))
    else:
        glb, pf, lift = build()
        print(os.path.relpath(glb, ROOT), os.path.relpath(pf, ROOT), os.path.relpath(shot(lift), ROOT))
