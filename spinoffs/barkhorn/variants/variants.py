"""Tropos design-pass proposals (2026-10-31, the owner: "nail design, make it realistic, make it cooler"): the new
parts, built apart from the Cloud (its build is at the container's memory limit) in the Cloud's own frame, so a shot
lays them on the current cabinet with the parts they replace hidden. The current design stays the baseline; nothing
here changes the Cloud's CAD.

    .venv-fab/bin/python studio/fabkit/build.py spinoffs/barkhorn/variants/variants.py --out spinoffs/barkhorn/variants/out

- **Strata** (variants/STRATA.md): the stepped laminated horn (horn_options.py's horn-plan-b) as the hero, and the
  cabinet answering it: the woofer set in a stepped caldera, three rings of stock 1/2 in sheet in place of the cloth
  disc and its dyed ring, so the horn's contour lines start at the woofer.
- **Topo** (variants/TOPO.md): the laminated horn whose 22 layers' outlines each walk a circle round Mount
  Tamalpais's East Peak at a set distance, the land's relief pushing the edge out (variants/topo/topo.py); the air
  path and the wall unchanged.
"""
import copy, dataclasses, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import cloud                                                         # noqa: E402
import horn_options                                                  # noqa: E402
import product                                                       # noqa: E402
from build123d import Align, Cylinder, Pos, Rot                      # noqa: E402

product.SOLIDS.setdefault('bronze', dict(title='Bronze bar (C93200 bearing bronze or C544), turned', density=8.8,
                                          usd_per_cm3=0.12))   # budget, 2026
P = copy.deepcopy(horn_options.P)
_topo = json.load(open(os.path.join(HERE, 'topo', 'outlines.json')))
P['horn']['cast']['formed']['laminated'].update(topo=[r['points'] for r in _topo['rings']], smooth=False, lamina=3.0,
                                                lip=20.0)   # Strata: the mouth's layer 20 outside the air path, an even lip
# Strata's posts (the critic: a visible mount): the four reviewed post positions kept, each a ø16 bronze rod with a
# turned collar on the top plate and one under the horn's pad, in place of the ø10 stainless tubes and their cups
POSTS = dict(at=[(97.0, 35.0, 929.6), (463.0, 35.0, 929.6), (240.0, 353.0, 998.7), (320.0, 353.0, 998.7)],
             d=16.0, foot=867.0, top_plate=880.0, base_collar=(28.0, 8.0), top_collar=(24.0, 6.0), into_pad=10.0)
# the caldera: rings of stock 1/2 in sheet stacked on the front panel's face round the woofer, the bores stepping out
# toward the room (a short terraced horn of the woofer's own); centre and face from the Cloud (x 280, z 478; face y 24)
CALDERA = dict(centre=(280.0, 478.0), face_y=24.0, layer=12.7, od=500.0, ids=(400.0, 427.0, 454.0))   # 13.5 radial steps: the horn's own at the mouth


def caldera(C):
    out = []
    for k, idia in enumerate(C['ids']):
        y1 = C['face_y'] - k * C['layer'] - 0.1; y0 = C['face_y'] - (k + 1) * C['layer'] + 0.1
        ring = Cylinder(C['od'] / 2, y1 - y0) - Cylinder(idia / 2, y1 - y0 + 2)
        out.append(Pos(C['centre'][0], (y0 + y1) / 2, C['centre'][1]) * Rot(90, 0, 0) * ring)
    return out


def posts(Q):
    out = []
    for x, y, top in Q['at']:
        rod = Pos(x, y, Q['foot']) * Cylinder(Q['d'] / 2, top - Q['foot'], align=(Align.CENTER, Align.CENTER, Align.MIN))
        bc = Pos(x, y, Q['top_plate'] + 0.1) * (Cylinder(Q['base_collar'][0] / 2, Q['base_collar'][1], align=(Align.CENTER, Align.CENTER, Align.MIN))
                                                 - Cylinder(Q['d'] / 2 + 0.2, Q['base_collar'][1] + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        pad = top - Q['into_pad']
        tc = Pos(x, y, pad - Q['top_collar'][1] - 0.1) * (Cylinder(Q['top_collar'][0] / 2, Q['top_collar'][1], align=(Align.CENTER, Align.CENTER, Align.MIN))
                                                           - Cylinder(Q['d'] / 2 + 0.2, Q['top_collar'][1] + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        out.append((rod, bc, tc))
    return out


def parts(P):
    wg = product.waveguide(P)
    fm = wg['formed']
    out = []
    if fm.get('laminated_topo'):
        from build123d import Compound
        out.append(product.Part('horn-topo', Compound(children=fm['laminated_topo']), product._lam_stock(P['horn']['cast']['formed'], fm['laminated_topo'], False),
                                finish='horn-lot', group='horn',
                                notes=['Topo (variants/TOPO.md): the laminated horn, 22 layers of stock 1/2 in and the boss, each '
                                       'layer\'s outline the air path plus the wall pushed out 8 to 45 mm by the elevation along a '
                                       'circle round Mount Tamalpais\'s East Peak (from 2.4 km at the mouth to 150 m at the throat); '
                                       'CNC-cut from the DXF of each layer, bonded and machined as horn-plan-b']))
    if fm.get('laminated_lines'):            # Topo Clear (the Mantle lane's idea): clear layers, a 3 mm tinted lamina each
        from build123d import Compound
        clear, lines = fm['laminated_lines']
        F = P['horn']['cast']['formed']
        out.append(product.Part('horn-topo-clear', Compound(children=clear), product._lam_stock(F, clear, False), finish='clear-cast',
                                group='horn', option='Topo Clear',
                                notes=['Topo Clear: the Topo horn\'s 22 layers in clear cast sheet (9.6 mm each, from 3/8 in faced), '
                                       'and the boss']))
        out.append(product.Part('horn-topo-lines', Compound(children=lines), product.Machined('stock-cast-sheet', 'cnc-mill', setup_usd=300.0),
                                finish='horn-lot', group='horn', option='Topo Clear',
                                notes=['Topo Clear: a 3 mm lamina of the horn\'s tint (stock 1/8 in sheet, e.g. 2423 or 2074) '
                                       'bonded on each clear layer\'s front face, cut to the same outline: the color reads as a '
                                       'contour line at every step\'s edge']))
    if fm.get('laminated'):                  # Strata's horn: the stepped laminated horn with its even front lip
        from build123d import Compound
        out.append(product.Part('horn-strata', Compound(children=fm['laminated']), product._lam_stock(P['horn']['cast']['formed'], fm['laminated'], False),
                                finish='horn-lot', group='horn',
                                notes=['Strata (variants/STRATA.md): the stepped laminated horn, 22 layers of stock 1/2 in and the '
                                       'boss, the mouth\'s layer 20 outside the air path (10 on the others), its front face and every '
                                       'layer\'s edge polished before bonding']))
    from build123d import Compound
    ps = posts(POSTS)
    out.append(product.Part('strata-posts', Compound(children=[r for r, _, _ in ps]), product.Machined('bronze', 'lathe', setup_usd=60.0),
                            finish='brass', group='horn',
                            notes=['Strata: four ø16 bronze rods (C93200 or C544), threaded M12 at the top into inserts in the horn\'s '
                                   'pads, at the four reviewed post positions. The engineering audit (2026-11-01): the front pair\'s feet are '
                                   'turned heads (14 across, 4 thick, on an 8 neck) hooked under keyhole sockets bonded through the top into '
                                   'the front panel\'s edge; the rear pair seated in sleeved sockets, the tie rod in rear post 3 at 2 N m; '
                                   'held at three points, the horn cannot lift (make/engineering-audit.md)']))
    out.append(product.Part('strata-collars', Compound(children=[c for _, b, t in ps for c in (b, t)]), product.Machined('bronze', 'lathe', setup_usd=40.0),
                            finish='brass', group='horn',
                            notes=['Strata: a turned bronze collar on the top plate at each post (ø28 x 8) and one under each pad '
                                   '(ø24 x 6), so the horn reads as mounted, not hovering']))
    for k, ring in enumerate(caldera(CALDERA)):
        out.append(product.Part(f'caldera-{k + 1}', ring, product.Machined('stock-cast-sheet', 'cnc-mill', stock=(CALDERA['od'] + 10, CALDERA['od'] + 10, CALDERA['layer']), setup_usd=60.0),
                                finish='bark', group='cabinet',
                                notes=[f'Strata (variants/STRATA.md): the woofer\'s caldera, ring {k + 1} of 3 from the panel: '
                                       f'Ø{CALDERA["od"]:g} outside, Ø{CALDERA["ids"][k]:g} bore, 1/2 in stock sheet in the '
                                       'cabinet\'s colour, faced, its bore and outside edges polished; bonded to the front panel '
                                       '(ring 1) and to each other with polymerising cement, before the woofer goes in']))
    return out


PRODUCT = dataclasses.replace(
    cloud.PRODUCT, name='barkhorn-variants', params=P, parts=parts, count=2,
    touching=[('horn-topo', 'horn-topo-clear'), ('horn-topo', 'horn-topo-lines')],      # alternatives in one place
    materials={**cloud.PRODUCT.materials,                # Topo Clear's body: water-clear cast sheet, a faint cool cast
               'clear-cast': {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': '#EEF2EF', 'radius': 0.05, 'roughness': 0.03}},
    kind='Tropos design-pass proposals: Strata\'s caldera and the Topo horn',
    notes=['Proposals beside the current design (variants/README.md); the Cloud\'s CAD is unchanged.'],
    origin=(280.0, 213.7, -12.0), drawing_prefix='BHV')
