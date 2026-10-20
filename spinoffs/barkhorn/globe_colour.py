"""Round 33c: the multicolour acrylic globe made real (the owner, 2026-10-20: "Is it possible to actually build the paper
and black globes as well? Those could be cool with light cast on them. Maybe not." and then: "For the globe I meant use
the dark and light mode version of the globe. The multicolor acrylic globe.").

The site's globe (site/img/globe-turn-poster.webp by day, globe-turn-night-poster.webp by night) as an object: six
discs slotted together, the three meridians whole circles through the poles (Poison facing us, Dust and Haze either
side) and the three parallels (Ember at 40 N, Ice at the equator, Acid at 40 S), each slotted round those before it
(globe_mono.discs), leaning 23.4 degrees, resting in a black base. Each disc is cast acrylic in its speaker's tint,
polished: by day light passes through and the discs throw their colours across the table in coloured shadow. By night
each disc's edge glows its colour, the site's neon: in the product, fluorescent cast acrylic lit by a ring of 395 nm
UV-A LEDs in the base (the README says what holds up and what doesn't), modelled here as a band of light inside each
rim and a faint UV ring.

A 300 mm desk or bar piece (R 150, 8 mm sheet) is modelled; the 1 m back-bar piece is the same drawing at 3.33x in
25 mm sheet (the kit piece scales it; the fab files are written for both).

    .venv-fab/bin/python spinoffs/barkhorn/globe_colour.py                 the model, the cut files, the shots
    python3.11 spinoffs/barkhorn/globe_colour.py --render [names] [--scale S] [--samples N]
    python3 spinoffs/barkhorn/globe_colour.py --sheet proof|finals
"""
import json, math, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'companions'))
OUT = os.path.join(HERE, 'out-globe-colour')
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'globe-colour')
RENDERS = os.path.join(ROOT, 'renders', '2026-10-20', 'barkhorn', 'globe-colour')
DEF = os.path.join(OUT, 'earf-globe-colour.json')

LEAN, LAT = 23.44, 40.0
R, T = 150.0, 8.0                       # the desk globe: 300 across in 8 mm sheet (the mark's slab, 0.05 of the radius)
GAP = 0.15                              # each slot's clearance a side, on the sheet's measured thickness
RIM = 0.6                               # night: the glow band's depth inside each rim
CHIPS_X = 2000.0                        # the chips' row, 2 m off to the right
BASE = dict(d=110.0, h=22.0, seat_r=34.0, ring=(24.0, 31.0))   # black anodised aluminium; the globe sits on a seat ring
# the discs (globe_mono's names), their speakers and the mark's places: the meridian facing us green, the larger side
# meridian orange and the smaller violet; red north, blue the equator, yellow south (earth.RING)
DISCS = {'m90': 'Poison', 'm150': 'Dust', 'm30': 'Haze', 'equator': 'Ice', 'north': 'Ember', 'south': 'Acid'}
SWATCH = {'Ember': '#D2382F', 'Dust': '#E5732A', 'Acid': '#E9B320', 'Poison': '#4F7F3A', 'Ice': '#4A90C8',
          'Haze': '#6C4BA3'}            # earth._C
GLOW = {'Ember': '#FF4A3A', 'Dust': '#FF8A3A', 'Acid': '#FFC93A', 'Poison': '#6BD45A', 'Ice': '#4FB8FF',
        'Haze': '#9A6BFF'}              # companions/common.GLOW
GROUNDS = {'paper': '#F2EFEA', 'night': '#121114'}


def _lighter(swatch, t, turn=0.0):
    """The swatch `t` of the way to white in OKLab with its hue held (a thinner path through Beer's law, each channel
    to its own root, turned Ember and Ice 10 to 12 degrees off their swatches)."""
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    def srgb(v):
        v = max(0.0, min(1.0, v))
        return 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
    r, g, b = (lin(int(swatch[i:i + 2], 16)) for i in (1, 3, 5))
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s_ = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s_
    A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s_
    B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s_
    L, A, B = L + (1 - L) * t, A * (1 - t * 0.6), B * (1 - t * 0.6)     # lighter, a little less chroma, the hue held
    if turn:                                                            # and turned against the warm room's drift
        c, s2 = math.cos(math.radians(turn)), math.sin(math.radians(turn))
        A, B = A * c - B * s2, A * s2 + B * c
    l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3
    m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3
    s_ = (L - 0.0894841775 * A - 1.2914855480 * B) ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s_, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s_,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s_)
    return '#' + ''.join(f'{round(srgb(c) * 255):02X}' for c in rgb)


def _deep(swatch, k=1.0):
    """The sheet's `deep` (after its thickness): the swatch lightened (1 - k of the way to white, the hue held), so the
    disc over paper lands on that colour."""
    import coin as C
    name = next(n for n, c in SWATCH.items() if c == swatch)
    return C.tint_deep(_lighter(swatch, 1.0 - k, HUE_TURN.get(name, 0.0)), passes=2.0)


# each disc's tint: light through the 8 mm sheet to the paper and back lands on the swatch (coin.tint_deep); lighter
# where discs cross (a sheet seen through three others went mud in round 28's study), tuned by the hue check
# each target's hue turned (OKLab degrees) against what the warm paper and light did to it, measured on the chips
# (Ember and Dust 10 low, Poison 11 high, at 0.7)
HUE_TURN = {'Ember': 11.0, 'Dust': 11.0, 'Acid': 3.0, 'Poison': -12.0, 'Ice': 2.0, 'Haze': 6.0}
TINT_K = {'Ember': 0.7, 'Dust': 0.7, 'Acid': 0.7, 'Poison': 0.7, 'Ice': 0.7, 'Haze': 0.7}
# the finals' fluorescent sheet: denser, more saturated (the lead: the day tile read paler than the site's light mode)
FLUO_K = 1.0


def materials():
    m = {}
    for name in SWATCH:
        k = name.lower()
        m[f'disc-{k}'] = {'preset': 'clear_resin', 'color': '#FFFFFF', 'deep': _deep(SWATCH[name], TINT_K[name]),
                          'radius': T / 1000, 'roughness': 0.03}
        m[f'rim-{k}'] = {'preset': 'emit', 'color': GLOW[name], 'strength': 0.0}
        m[f'face-{k}'] = {'preset': 'emit', 'color': GLOW[name], 'strength': 0.0}
    m['base'] = {'preset': 'black_oxide', 'color': '#1E1E1F'}
    m['uv'] = {'preset': 'emit', 'color': '#7A52FF', 'strength': 0.0}
    m['seat'] = {'preset': 'rubber', 'color': '#161616'}
    return m


def full_discs(r=R, t=T, gap=GAP):
    """The six discs whole, with their slot cutters, in the globe's frame (axis z, the camera along -y)."""
    from build123d import Cylinder, Rot, Pos
    out = []
    for name, lam in (('m90', 90.0), ('m30', 30.0), ('m150', 150.0)):
        rot = Rot(Z=lam - 90) * Rot(X=90)
        out.append((name, rot, 0.0, r))
    for name, phi in (('equator', 0.0), ('north', LAT), ('south', -LAT)):
        out.append((name, None, r * math.sin(math.radians(phi)), r * math.cos(math.radians(phi))))
    shapes = []
    for name, rot, z, rr in out:
        def place(s, rot=rot, z=z):
            return rot * s if rot is not None else Pos(0, 0, z) * s
        disc = place(Cylinder(rr, t))
        cutter = place(Cylinder(rr + 1, t + 2 * gap))
        rim = place(Cylinder(rr - 0.05, t - 1.0) - Cylinder(rr - RIM, t))
        face = place(Cylinder(rr - RIM - 0.3, 0.2))          # night: the face's own faint glow, at its mid-plane
        shapes.append((name, disc, cutter, rim, face))
    return shapes


def discs(r=R, t=T, gap=GAP):
    """[(name, disc, rim)] each slotted round those before it (the meridian facing us whole)."""
    sh = full_discs(r, t, gap)
    out = []
    for i, (name, disc, cutter, rim, face) in enumerate(sh):
        for _, _, c, _, _ in sh[:i]:
            disc = disc - c
            rim = rim - c
            face = face - c
        out.append((name, disc, rim, face))
    return out


def lift():
    b = BASE
    return b['h'] + math.sqrt(R * R - b['seat_r'] ** 2)


def parts():
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
    from build123d import Pos, Rot, Sphere
    from kit import Part, Machined, Bought, Sheet, cyl
    z = lift()
    M = lambda s: Pos(0, 0, z) * Rot(Y=LEAN) * s
    ps = []
    for name, disc, rim, face in discs():
        k = DISCS[name].lower()
        ps.append(Part(f'disc-{name}', M(disc), Machined('cast-acrylic', 'cnc-mill'), finish=f'disc-{k}', group='globe',
                       notes=[f'{DISCS[name]}: fluorescent (or the speaker\'s) cast acrylic, 8 mm, laser-cut, the slots '
                              'kerf-compensated to the measured sheet, every edge diamond-polished']))
        ps.append(Part(f'rim-{name}', M(rim), Bought('globe-glow'), finish=f'rim-{k}', render=True, inside=True))
        ps.append(Part(f'face-{name}', M(face), Bought('globe-glow'), finish=f'face-{k}', render=True, inside=True))
    b = BASE
    cup = Pos(0, 0, z) * Sphere(R + 0.3)
    base = cyl('z', (0, 0), b['d'], 0, b['h']) - cup - cyl('z', (0, 0), 2 * b['ring'][1] + 1, b['h'] - 8, b['h'] + 1)
    ring = cyl('z', (0, 0), 2 * b['ring'][1], b['h'] - 8, b['h'] - 6.5) - cyl('z', (0, 0), 2 * b['ring'][0], b['h'] - 9, b['h'] - 6)
    ps += [Part('base', base, Machined('aluminium', 'lathe'), finish='base', group='base',
                notes=['aluminium, black anodised: the globe sits on its seat ring; inside, the UV ring, the board, the '
                       'USB-C socket at the back and a touch dimmer under the rim']),
           Part('uv', ring, Bought('globe-uv-ring'), finish='uv', group='base', inside=True)]
    # the hue check's chips: a 60 mm square of each sheet, far off to the side (hidden in the globe's shots)
    from kit import box
    for i, name in enumerate(SWATCH):
        x0 = CHIPS_X + i * 80.0
        ps.append(Part(f'chip-{name.lower()}', box(x0, -30, 0.02, x0 + 60, 30, T + 0.02), Bought('globe-chip'),
                       finish=f'disc-{name.lower()}', option='chips'))
    return ps


def build():
    sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
    import kit as K
    import render as fk_render
    ps = parts()
    # fluorescent sheet gathers daylight through its faces and gives it out at its cut edges, so by day the edges glow
    # too, less (clear tinted sheet's edges, seen along 300 mm of tint, render black)
    flav = {'day': {'materials': {f'rim-{n.lower()}': {'strength': 0.8} for n in SWATCH}}, 'night': {'materials': {**{f'rim-{n.lower()}': {'strength': 2.5} for n in SWATCH},
                                               **{f'face-{n.lower()}': {'strength': 0.12} for n in SWATCH},
                                               'uv': {'strength': 2.0}}}}
    prod = K.Product('earf-globe-colour', 'EARF globe, in colour', 'the site\'s globe in six acrylics', params={},
                     parts=lambda P: ps, count=1, materials=materials(), variants=flav,
                     origin=(0, 0, 1e-6))    # (all zero, the kit centres the model on its parts, chips and all)
    fk_render.write(prod, ps, OUT, engine_file=DEF, proof=False)
    return ps


# --- the cut files: each disc flat, its slots, for both sizes ---------------------------------------------------------
def cut_files(out=os.path.join(OUT, 'cut')):
    """Each disc as a flat outline (its slots cut, kerf-compensated: the slot is the measured sheet plus 2 x GAP, the
    laser's kerf taken off the outline by the shop's own offset), SVG and DXF in mm, for the 300 desk globe in 8 mm and
    the 1 m bar globe in 25 mm. Read off the CAD: each disc's face, in its own plane."""
    import ezdxf
    from build123d import Plane
    os.makedirs(out, exist_ok=True)
    made = []
    for tag, r, t, gap in (('300', R, T, GAP), ('1000', 500.0, 25.0, 0.4)):
        sh = discs(r, t, gap)
        full = full_discs(r, t, gap)
        for (name, disc, _, _) in sh:
            # the disc's plane: a section through its middle, turned flat
            faces = _flat(name, disc, r)
            doc = ezdxf.new('R2010', setup=True); doc.units = ezdxf.units.MM
            msp = doc.modelspace(); doc.layers.add('CUT')
            svg = []
            for ring in faces:
                msp.add_lwpolyline(ring, close=True, dxfattribs={'layer': 'CUT'})
                svg.append('M' + 'L'.join(f'{x:.2f},{-y:.2f}' for x, y in ring) + 'Z')
            fn = os.path.join(out, f'globe-{tag}-{name}-{DISCS[name].lower()}')
            doc.saveas(fn + '.dxf')
            w = 2 * r + 20
            open(fn + '.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{w}mm" '
                                         f'viewBox="{-w / 2} {-w / 2} {w} {w}"><path d="{" ".join(svg)}" fill="none" '
                                         f'stroke="#F00" stroke-width="0.2" fill-rule="evenodd"/></svg>\n')
            made += [fn + '.dxf', fn + '.svg']
    return made


def _flat(name, disc, r):
    """The disc's outline in its own plane (u, v), as point rings: a section at its mid-plane, turned flat."""
    from build123d import Plane, Vector, section, Rot, Pos
    if name.startswith('m'):
        lam = {'m90': 90.0, 'm30': 30.0, 'm150': 150.0}[name]
        flat = Rot(X=-90) * Rot(Z=-(lam - 90)) * disc        # back to the x-y plane
    else:
        z = {'equator': 0.0, 'north': r * math.sin(math.radians(LAT)), 'south': -r * math.sin(math.radians(LAT))}[name]
        flat = Pos(0, 0, -z) * disc
    sec = flat.intersect(Pos(0, 0, 0) * _slab(r))
    rings = []
    for f in sec.faces():
        for w in f.wires():
            pts = [(round(v.X, 3), round(v.Y, 3)) for v in w.positions([i / 240 for i in range(241)])]
            rings.append(pts)
    return rings


def _slab(r):
    from build123d import Box
    return Box(4 * r, 4 * r, 0.01)


# --- the shots -------------------------------------------------------------------------------------------------------
def product(mode):
    # by day the faces' glow discs are off: an unlit emitter inside the sheet renders black
    return {'def': os.path.relpath(DEF, ROOT), 'flavour': mode, 'instances': [{'position': [0, 0, 0], 'rotate_z': 0}],
            **({'hide': ['face-*']} if mode == 'day' else {})}


def cam(size, lens=85.0, dist=1.75, elev=22.0, tx=0.0):
    zc = lift() / 1000
    e = math.radians(elev)
    return {'position': [tx, -dist * math.cos(e), zc + dist * math.sin(e)], 'target': [tx, 0.0, zc - 0.01],
            'lens_mm': lens, 'level': False}


def day(size=(900, 900), samples=160, final=False):
    s = _day(size, samples, final)
    if final:
        # the fluorescent sheet, denser: the faces carry the site's colour face-on
        s['materials'] = {f'disc-{n.lower()}': {'deep': _deep(SWATCH[n], FLUO_K)} for n in SWATCH}
        # soft light from behind the camera through the discs (not a rake on every slot's edge)
        s['lights']['front'] = {'type': 'area', 'size_m': [1.6, 1.2], 'orbit': {'azimuth_deg': 10, 'elevation_deg': 35,
                                'distance_m': 2.5}, 'target': [0, 0, lift() / 1000], 'irradiance': 1.0, 'color': '#FFF7EA',
                                'camera': False}
    return s


def _day(size=(900, 900), samples=160, final=False):
    """Light mode: on paper in the pale studio, a hard sun low from the left behind, the discs' colours thrown across
    the paper in coloured shadow."""
    zc = lift() / 1000
    c = cam(size, lens=105.0 if final else 105.0, dist=1.75, elev=24.0)
    if final:       # the globe about 60 % of the frame's height, its shadows running off to the right
        c.update(lens_mm=95.0, target=[0.09, 0.03, zc - 0.035])
    return {'title': 'The EARF globe in colour, by day', 'size': list(size), 'product': product('day'), 'camera': c,
            'set': {'kind': 'sweep', 'color': '#EEEAE3', 'width': 8.0, 'front': 4.0, 'depth': 2.0, 'radius': 1.2, 'height': 4.0},
            'sky': {'kind': 'gradient', 'zenith': '#D8D4CE', 'horizon': '#DEDAD4', 'ground': '#6A665F', 'strength': 1.0},
            'sun': {'azimuth_deg': 295.0, 'elevation_deg': 30.0, 'irradiance': 5.0, 'angle_deg': 2.5 if final else 0.6,
                    'color': '#FFF2DE'},
            'lights': {'fill': {'type': 'area', 'size_m': [2.0, 1.6], 'orbit': {'azimuth_deg': -30, 'elevation_deg': 20, 'distance_m': 3.0},
                                'target': [0, 0, zc], 'irradiance': 0.5, 'color': '#FFF7EA', 'camera': False}},
            'render': {'samples': samples, 'adaptive': 0.01, 'denoise': True, 'clamp': 10, 'bounces': 24,
                       'transmission_bounces': 24, 'view': 'Khronos PBR Neutral', 'exposure': 0.0, 'white_balance_k': 5400}}


def night(size=(900, 900), samples=160, final=False):
    """Dark mode: on black, each edge glowing its colour (the fluorescent sheet under the base's UV ring), a little of
    their colour cast on the surface."""
    zc = lift() / 1000
    c = cam(size, lens=95.0 if final else 105.0, dist=1.75, elev=22.0)
    return {'title': 'The EARF globe in colour, by night', 'size': list(size), 'product': product('night'), 'camera': c,
            'set': {'kind': 'sweep', 'color': '#121114', 'width': 8.0, 'front': 4.0, 'depth': 2.0, 'radius': 1.2, 'height': 4.0},
            'sky': {'kind': 'gradient', 'zenith': '#0A0A0C', 'horizon': '#0E0E10', 'ground': '#050505', 'strength': 0.05},
            'lights': {'key': {'type': 'area', 'size_m': [1.2, 0.8], 'orbit': {'azimuth_deg': -40, 'elevation_deg': 40, 'distance_m': 2.5},
                               'target': [0, 0, zc], 'irradiance': 0.06, 'color': '#C8D0FF', 'camera': False}},
            'render': {'samples': samples, 'adaptive': 0.01, 'denoise': True, 'clamp': 12, 'bounces': 24,
                       'transmission_bounces': 24, 'view': 'Khronos PBR Neutral', 'exposure': 0.0, 'white_balance_k': 6000}}


def chips():
    """The hue check: the six sheets as chips on paper from above, in the day shot's light."""
    s = day((1400, 300), 64)
    s['product'] = {**product('day'), 'options': ['chips'],
                    'instances': [{'position': [-CHIPS_X / 1000 - 0.23, 0, 0], 'rotate_z': 0}]}
    s['camera'] = {'position': [0.0, -0.05, 1.3], 'target': [0.0, 0.0, 0.0], 'lens_mm': 85, 'level': False}
    s.pop('sun')
    s['lights']['top'] = {'type': 'area', 'size_m': [2.0, 2.0], 'position': [0, -0.3, 2.0], 'target': [0, 0, 0],
                          'irradiance': 3.0, 'color': '#FFF7EA', 'camera': False}
    return s


FRAMES = {'chips': chips, 'proof-day': lambda: day(), 'proof-night': lambda: night(),
          'final-day': lambda: day((1600, 1067), 384, True), 'final-night': lambda: night((1600, 1067), 384, True)}


def write_shots():
    os.makedirs(SHOTS, exist_ok=True)
    for n, f in FRAMES.items():
        json.dump(f(), open(os.path.join(SHOTS, n + '.json'), 'w'), indent=1)


def render_(names, scale, samples):
    os.makedirs(RENDERS, exist_ok=True)
    for n in names:
        cmd = [sys.executable, os.path.join(ROOT, 'studio', 'engine', 'render.py'), os.path.join(SHOTS, n + '.json'),
               '--out', os.path.join(RENDERS, n + '.png'), '--scale', str(scale)] + (['--samples', str(samples)] if samples else [])
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-2000:], r.stderr[-2000:]); raise SystemExit(n)
        print(n, flush=True)


def sheet(kind):
    site = os.path.join(HERE, 'site', 'img')
    R_ = lambda n: os.path.join(RENDERS, n + '.png')
    if kind == 'proof':
        tmp = [os.path.join(RENDERS, f'_site-{k}.png') for k in ('day', 'night')]
        for src, dst in zip(('globe-turn-poster.webp', 'globe-turn-night-poster.webp'), tmp):
            subprocess.run(['convert', os.path.join(site, src), dst], check=True)
        tiles = (f"-label 'The site, light mode' {tmp[0]} -label 'Made real: by day (Ember to Haze acrylic, a hard sun)' "
                 f"{R_('proof-day')} -label 'The site, dark mode' {tmp[1]} -label 'Made real: by night (fluorescent edges, "
                 f"UV-A ring)' {R_('proof-night')}")
        out = os.path.join(RENDERS, 'sheet-proof.png')
        subprocess.run(f"montage {tiles} -tile 2x2 -geometry 560x560+4+4 -pointsize 15 -background '#F2F0EC' -depth 8 {out}",
                       shell=True, check=True)
        for t in tmp:
            os.remove(t)
    else:
        out = os.path.join(RENDERS, 'sheet-finals.png')
        subprocess.run(f"montage -label 'By day' {R_('final-day')} -label 'By night' {R_('final-night')} -tile 2x1 "
                       f"-geometry 800x533+4+4 -pointsize 15 -background '#F2F0EC' -depth 8 {out}", shell=True, check=True)
    print(out)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--sheet' in a:
        sheet(a[a.index('--sheet') + 1])
    elif '--render' in a:
        write_shots()
        scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 1.0
        samples = int(a[a.index('--samples') + 1]) if '--samples' in a else None
        render_([x for x in a if x in FRAMES] or ['proof-day', 'proof-night'], scale, samples)
    elif '--cut' in a:
        print(len(cut_files()))
    else:
        build()
        write_shots()
        print('built', lift())
