"""barkhorn's comparison sheets: sets of frames, one speaker each under the same light and camera, rendered and set
in a grid with their names.

    python3 spinoffs/barkhorn/frames.py SET [--samples 64] [--all | --only NAME ...]

Sets:
- covers: each bark bare, as photographed, then with each front cover (round 2);
- front: the panel faced in bark under a solid colour cloth, two ways: the whole front's grille (the bark shows when it
  comes off) and a disc over the woofer alone (round 3);
- study: the waveguide's forms (P['horn']['form']), three-quarter and from the side; each form's render model is built
  first into out/study/ (`--build` to build them again after a change);
- experiments: material experiments (pressed recycled plastic, strata and terrazzo resin);
- proposal: where the study points: the pebble waveguide in strata resin (eucalyptus) and in terrazzo (birch), on the
  bark face with a cloth disc;
- horn (round 4): the photograph's horn, measured again, on four posts as photographed: its back as a shell round the
  driver or as a tub, from three sides, and beside the photograph from its own angle;
- resin (round 4): the cast resin's tints, close to;
- pressed (round 4): the cabinet faced in pressed recycled plastic sheet, and the sheets close to;
- pick (round 4): where round 4 points, both barks;
- horn5 (round 5): the horn running the cabinet's full depth, its back flush with the cabinet's, on a 2 in driver, from
  four sides;
- shells (round 5): the waveguide's resins, close to: clear, dark and clear, opaque, marbled and swirled;
- woodfree (round 5): the cabinet without wood, its panels pressed recycled plastic laid out in each bark's pattern;
- pick5 (round 5): where round 5 points, both barks;
- printed (round 6): the horn printed with its bark's pattern in translucent inks, close to and on the speaker;
- cabinets (round 6): the cabinet in other plastics, without wood: translucent acrylic, stone looks, marble and swirl;
- pick6 (round 6): the line, without wood, its two ports, from three-quarter and from the front;
- discs (round 7): the cloth disc in neutral colours on each cabinet, so the cabinet and the horn carry the colour;
- lookbook (rounds 7 to 10): the look book's speakers by line (Bark, Cloud, Crag), each on a sweep in its own colour,
  the cover on and off;
- room12 (round 12): the pair in a living room, for scale.

Each frame's shot goes to studio/shots/barkhorn/<set>/ (so any one can be re-rendered or tuned) and its image to
renders/<day>/barkhorn/<set>/, beside the grid <set>.png. Only frames not yet rendered are rendered, unless named with
--only or all are asked for with --all; the grid is set again every run.
"""
import argparse, copy, io, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(ROOT, 'studio', 'shots', 'barkhorn')
PRODUCT = 'studio/products/barkhorn.json'
STUDY = os.path.join(HERE, 'out', 'study')
DAY = {'covers': '2026-10-10', 'front': '2026-10-11', 'study': '2026-10-11', 'proposal': '2026-10-11',
       'experiments': '2026-10-11', 'horn10': '2026-10-13', 'lookbook2': '2026-10-13', 'room12': '2026-10-13'}   # where each set's renders live (a set first made that day; the rest 2026-10-12)

FRONT_CAM = {'position': [-0.78, -2.6, 1.0], 'target': [0.0, 0.0, 0.64], 'lens_mm': 66, 'level': True}
THREE_Q = {'position': [1.45, -2.7, 1.45], 'target': [0.0, 0.08, 0.66], 'lens_mm': 60, 'level': True}
RIGHT_Q = {'position': [1.25, -2.55, 1.2], 'target': [0.0, 0.05, 0.66], 'lens_mm': 60, 'level': True}
SIDE = {'position': [3.2, 0.12, 0.8], 'target': [0.0, 0.12, 0.66], 'lens_mm': 70, 'level': True}
# from behind: the speaker turned round and brought 1.2 m forward of the wall (the room's lamps follow it), seen from
# behind and above
BEHIND = {'position': [-1.0, -3.2, 1.45], 'target': [0.0, -1.2, 0.72], 'lens_mm': 55, 'level': True}
TURNED = dict(position=[0.0, -1.2, 0], rotate_z=180, shift=-1.2)


def F(name, bark, label, options=(), materials=None, product=PRODUCT, camera=None, lights=None, at=None, size=None, stage=None,
      hide=(), sky=None, pair=None, sun=None, render=None):
    """One frame. `stage`: a set of its own in place of the room (a sweep), with its `sky`; `hide`: parts left out (the
    cloth disc); `pair`: several speakers, each {position, rotate_z}, in place of the one at `at`; `sun`: the shot's sun;
    `render`: settings over the shot's (white balance, exposure)."""
    return dict(name=name, bark=bark, label=label, options=list(options), materials=materials or {}, product=product,
                camera=camera, lights=lights or {}, at=at, size=size, stage=stage, hide=list(hide), sky=sky, pair=pair, sun=sun,
                render=render)


def form_product(form):
    return os.path.relpath(os.path.join(STUDY, f'barkhorn-{form}.json'), ROOT)


FORMS = [('shell', 'shell (round 2)'), ('lens', 'lens'), ('slab', 'slab'), ('pebble', 'pebble: slab rim, lens back'),
         ('round', 'round')]
# each study model: the product with these parameters changed (dotted paths into P), built into out/study/
MODELS = {f: {'horn.form': f} for f, _ in FORMS}
MODELS.update({'cast': {'horn.form': 'cast', 'horn.cast.back': 'shell'}, 'cast-tub': {'horn.form': 'cast', 'horn.cast.back': 'tub'}})
# round 4's light: a soft lamp close behind the horn, so its resin glows as the photograph's does with the room behind it
GLOW = {'glow': {'type': 'area', 'size_m': [0.7, 0.32], 'position': [0.0, 0.66, 1.12], 'target': [0.0, 0.0, 1.1],
                 'irradiance': 1.6, 'color': '#FFF1DC', 'specular': 0}}      # it lights the resin, leaves no highlight
HORN_Q = {'position': [1.3, -2.45, 1.5], 'target': [0.0, 0.1, 0.8], 'lens_mm': 58, 'level': True}
HORN_SIDE = {'position': [2.9, -0.55, 1.3], 'target': [0.0, 0.16, 0.86], 'lens_mm': 62, 'level': True}
HORN_BEHIND = {'position': [-1.15, -3.1, 1.75], 'target': [0.0, -1.2, 0.9], 'lens_mm': 55, 'level': True}
# the photograph's own angle on its left speaker: from the room's middle, a little right of it, the camera low
PHOTO = {'position': [0.75, -2.9, 0.98], 'target': [0.0, 0.0, 0.78], 'lens_mm': 50, 'level': True}
CLOSE = {'position': [0.55, -1.75, 1.18], 'target': [0.0, 0.1, 1.09], 'lens_mm': 70, 'level': True}
CORNER = {'position': [0.78, -0.86, 0.8], 'target': [0.22, -0.16, 0.56], 'lens_mm': 60, 'level': True}
PRESSED = 'studio/products/barkhorn-pressed.json'      # pressed.py's build
# round 5: the glow lamp hidden from rays through clear resin (it would show through it as a bright patch)
GLOW5 = {'glow': {**GLOW['glow'], 'transmission': False}}
# looking into the horn from in front and a little above, at the throat
THROAT = {'position': [0.18, -1.15, 1.22], 'target': [0.0, 0.25, 1.1], 'lens_mm': 60, 'level': True}
# round 7, the owner: "I'm not sure I like the rust disc anymore. I think more neutral colors, depending on the cabinet,
# will help the cabinet and horn pop more." Warm neutrals, dark to light; on eucalyptus the middle one is the bark's
# own grey layer
DISCS_BIRCH = [('charcoal', 'charcoal (round 6\'s)', '#2E2C2A'), ('graphite', 'graphite', '#4B4844'), ('stone', 'stone', '#8E8981'),
               ('oat', 'oat', '#CFC8BA')]
DISCS_EUCALYPTUS = [('charcoal', 'charcoal', '#2E2C2A'), ('graphite', 'graphite', '#4B4844'), ('bark-grey', 'the bark\'s grey', '#7C776F'),
                    ('oat', 'oat', '#CFC8BA')]
# the look book (round 7, the owner: "a little look book that I can share out. For each cabinet, I want a version with the
# driver cover on and off. Each page should be designed to accent the speaker being showcased"): each speaker on a seamless
# sweep in a colour drawn from it, from three-quarter, with its cloth disc on and off. The studio's ambient is a neutral
# grey (the default sky's blue tints an open sweep)
LOOK = {'position': [1.2, -2.5, 1.0], 'target': [0.0, 0.05, 0.52], 'lens_mm': 68, 'level': True}
STUDIO = {'kind': 'gradient', 'zenith': '#C4C2BE', 'horizon': '#CFCDC8', 'ground': '#5A5650', 'strength': 0.7}
# the look book's speakers by line (round 8, the owner: "bark is more of a product style/line. Y2K another. Crag
# another, which would include marble and such"): Bark (the barks, each horn wearing its bark's pattern cast in, drawn
# as round 6's printed horns, which show the same artwork; the autumn birch's horn golden yellow), Cloud (translucent
# acrylic, named poison, smoke and fog; round 10, the owner: "the theme is Cloud") and Crag (stone patterns in plastic
# and resin; round 10's
# turquoise in place of the rhodochrosite and the travertine). Round 8 also: "Remove Phoenix, red vein, cherry. Only do
# the autumn birch for the birch option."
LOOKS = [('Bark', 'eucalyptus', 'eucalyptus-printed', 'eucalyptus', '#B7C3B4'),
         ('Bark', 'autumn', 'birch-autumn-pressed', 'autumn birch', '#BDB5A9'),
         ('Bark', 'manzanita', 'manzanita-pressed', 'manzanita', '#D8C69E'),
         ('Bark', 'striped', 'snakebark-white-pressed', 'striped maple', '#4F5B3A'),
         ('Cloud', 'green', 'eucalyptus-y2k-green', 'poison', '#D9E4D3'),
         ('Cloud', 'smoke', 'birch-y2k-smoke', 'smoke', '#C9C5D3'),
         ('Cloud', 'ice', 'birch-y2k-ice', 'fog', '#CFDCE4'),
         ('Crag', 'cobalt', 'birch-marbled-cobalt', 'cobalt marble', '#2F4FA8'),
         ('Crag', 'malachite', 'crag-malachite', 'malachite', '#E3DACA'),
         ('Crag', 'lapis', 'crag-lapis', 'lapis lazuli', '#C9A35E'),
         ('Crag', 'turquoise', 'crag-turquoise', 'turquoise', '#B8694C')]


# round 10, the owner: "add some back or side shots of the horn": one speaker of each line turned on its own sweep, the
# horn from the side (its mouth to the right) and from behind (the pod round the driver), framed on the horn
HORN10 = {'position': [1.2, -2.5, 1.25], 'target': [0.0, 0.05, 1.06], 'lens_mm': 95, 'level': True}
# round 11 (the critic of the look book: "Renders that are sharp at the size they are shown"): the look frames again at
# twice the size the look book shows them, the strip of the frame a page shows (546 x 1100 of the 840 x 1100 frame)
# rendered alone at 1080 x 2160, the lens longer by 840 / 546 so the framing holds
LOOK2 = {**LOOK, 'lens_mm': round(68 * 840 / 545.9, 1)}
HORN10_KEYS = ('autumn', 'green', 'turquoise')


# round 12 (the critic of the look book: "an image that gives scale"; the owner: "Do 1-3"): the pair in a living room,
# things whose size everyone knows round them: a low sideboard (52 high) with a record player and a record on it, an
# armchair beside the left one at the same depth (so the two compare directly), a floor lamp, a print, the window's
# light from the left. The speakers 44 cm out from the wall, 2.6 m apart, toed in 8 degrees; the room 6.2 x 6.4 x 2.8 m,
# its back wall at y = 0.85
ROOM12_CAM = {'position': [1.0, -5.1, 1.3], 'target': [-0.25, 0.2, 0.8], 'lens_mm': 35, 'level': True}
ROOM12_PAIR = [{'position': [-1.3, 0.2, 0], 'rotate_z': 8}, {'position': [1.3, 0.2, 0], 'rotate_z': -8}]
ROOM12_SET = {
    'kind': 'room', 'size': [6.2, 6.4, 2.8], 'center': [0.0, -2.35],
    'floor': {'plank_w': 0.18, 'plank_l': 1.8, 'base': '#B08A62', 'dark': '#97734F', 'light': '#C29C72', 'plank_contrast': 0.6},
    'wall': {'color': '#E9E4DA'}, 'ceiling': '#F3F0EA', 'skirting': {'h': 0.1, 'color': '#E2DCD0'},
    'windows': [{'wall': 'left', 'along': 1.75, 'sill': 0.45, 'size': [1.7, 2.0], 'mullions': [1, 2]}],
    'props': [
        {'kind': 'rug', 'position': [-0.2, -1.0], 'size': [2.6, 1.7], 'color': '#5A4E42', 'sheen': 0.15},
        {'kind': 'sideboard', 'position': [0.0, 0.58], 'size': [1.5, 0.42, 0.52], 'color': '#6B4A33', 'wood': 'veneer',
         'grain': 0.25, 'label': '#C9A227'},
        {'kind': 'books', 'position': [0.16, 0.6], 'z': 0.52, 'colors': ['#3C4A5A', '#B9A27A', '#7A2E2A'], 'seed': 4},
        {'kind': 'vase', 'position': [0.52, 0.58], 'z': 0.52, 'height': 0.3, 'branches': 5, 'seed': 3},
        {'kind': 'frame', 'position': [0.0, 0.85], 'z': 1.55, 'size': [0.72, 0.92], 'artwork': {
            'bands': [['#D9CDB6', 0.34], ['#6F7F66', 0.4], ['#8C8273', 0.26]], 'ground': '#E4DCCD', 'seed': 12}},
        {'kind': 'lamp', 'position': [-2.65, 0.45], 'height': 1.6},
        {'kind': 'armchair', 'position': [-2.3, -0.35], 'rotate_z': 45, 'color': '#8A7A66', 'wood': '#6E4B30'},
        {'kind': 'vase', 'position': [2.15, 0.5], 'height': 0.55, 'branches': 7, 'seed': 9, 'color': '#CFC6B6'},
        {'kind': 'curtain', 'position': [-3.04, 0.42], 'size': [0.8, 2.75], 'rotate_z': 90},
    ]}
ROOM12_SKY = {'kind': 'gradient', 'strength': 3.0, 'zenith': '#9FB8DA', 'horizon': '#E7EDF2', 'ground': '#857F73'}
# each speaker wears its own pattern (materials.object_space): laid in the world, the right one stood on the grey strips
# of the eucalyptus; read in its own space it wears its look book page's face, as the left one does
# the white point on the daylight (the base shot's 5600 K left the sky's light blue on the cabinets' greys)
ROOM12_RENDER = {'white_balance_k': 6300, 'white_balance_tint': 8.0, 'exposure': 0.2}
# a low afternoon sun through the window, its patch on the floor in front of the chair
ROOM12_SUN = {'aim': {'at': [-1.9, -1.4, 0.0], 'window': 0, 'through': [0.5, 0.55]}, 'irradiance': 6.0, 'angle_deg': 1.0,
              'color': '#FFF0DC'}
ROOM12_LIGHTS = {
    'key': {'off': True}, 'fill': {'off': True}, 'wash': {'off': True},
    # the room behind the camera: a soft, low front light, as a ceiling and a wall would bounce it
    'room': {'type': 'area', 'size_m': [3.2, 1.4], 'position': [0.4, -4.3, 2.3], 'target': [-0.2, 0.4, 0.9],
             'irradiance': 0.45, 'color': '#FFF4E6'},
    # the window's daylight, helped: a lamp in its opening, the sky's colour
    'window': {'type': 'area', 'size_m': [1.6, 1.9], 'position': [-2.95, -0.7, 1.45], 'target': [0.0, -0.2, 0.9],
               'irradiance': 2.4, 'color': '#F2F5FF'},
    # the speakers' own light (the owner: "the speakers look more grey than they should"): the window rakes across their
    # fronts, so a soft warm lamp behind the camera lights them alone (light linking), as a photographer's bounce would
    'speakers': {'type': 'area', 'size_m': [3.0, 2.0], 'position': [1.2, -5.4, 2.1], 'target': [0.0, 0.2, 0.75],
                 'irradiance': 1.4, 'color': '#FFF1DE',
                 'receivers': ['left', 'right', 'top', 'front-panel', 'cloth-disc', 'woofer-ring', 'waveguide', 'waveguide-cap',
                               'port-left', 'port-right']},
    # each horn lit from behind, as the look frames' glow, so its resin reads
    **{f'glow{k}': {'type': 'area', 'size_m': [0.7, 0.32], 'position': [x, 0.72, 1.12], 'target': [x, 0.0, 1.1],
                    'irradiance': 1.4, 'color': '#FFF1DC', 'specular': 0, 'transmission': False}
       for k, x in (('L', -1.27), ('R', 1.27))},
}

def sweep(color):
    return {'kind': 'sweep', 'color': color, 'width': 6.0, 'front': 5.0, 'depth': 1.5, 'radius': 1.2, 'height': 4.0}


SHELLS = {'birch': [('birch', 'smoked: clear resin tinted dark (the proposal)'), ('birch-clear', 'clear, a little warm'),
                    ('birch-black', 'black, opaque'), ('birch-marble', 'marbled black and white'),
                    ('birch-swirl', 'smoke swirled through clear')],
          'eucalyptus': [('eucalyptus', 'bottle green: clear, tinted dark (the proposal)'), ('eucalyptus-clear', 'clear, gum-leaf green'),
                         ('eucalyptus-green', 'deep green, opaque'), ('eucalyptus-marble', 'marbled in the bark\'s colours'),
                         ('eucalyptus-swirl', 'green swirled through amber')]}
SETS = {
    'covers': dict(title='barkhorn: front covers (options)', camera=FRONT_CAM, rows={
        'birch': [F('birch-bare', 'birch', 'bare, as photographed'), F('birch-cloth', 'birch', 'cloth grille', ['cloth']),
                  F('birch-lenticel-grille', 'birch', 'lenticel grille', ['lenticel-grille']),
                  F('birch-bark-face', 'birch', 'bark face', ['bark-face']), F('birch-cork-face', 'birch', 'cork face', ['cork-face'])],
        'eucalyptus': [F('eucalyptus-bare', 'eucalyptus', 'bare, as photographed'),
                       F('eucalyptus-cloth', 'eucalyptus', 'cloth grille', ['cloth']),
                       F('eucalyptus-strip-grille', 'eucalyptus', 'strip grille', ['strip-grille']),
                       F('eucalyptus-bark-face', 'eucalyptus', 'bark face', ['bark-face']),
                       F('eucalyptus-cork-face', 'eucalyptus', 'cork face', ['cork-face'])]}),
    'front': dict(title='barkhorn: the bark face under a solid colour cloth', camera=FRONT_CAM, rows={
        'birch': [F('birch-grille-charcoal', 'birch', 'grille, charcoal', ['bark-face', 'cloth'], {'cloth': {'color': '#2E2C2A'}}),
                  F('birch-disc-charcoal', 'birch', 'disc, charcoal', ['bark-face', 'cloth-disc'], {'disc': {'color': '#2E2C2A'}}),
                  F('birch-disc-apricot', 'birch', 'disc, apricot', ['bark-face', 'cloth-disc'], {'disc': {'color': '#C98F64'}}),
                  F('birch-disc-oxblood', 'birch', 'disc, oxblood', ['bark-face', 'cloth-disc'], {'disc': {'color': '#6B2B26'}})],
        'eucalyptus': [F('eucalyptus-grille-forest', 'eucalyptus', 'grille, forest green', ['bark-face', 'cloth'],
                         {'cloth': {'color': '#3F4F3A'}}),
                       F('eucalyptus-disc-rust', 'eucalyptus', 'disc, rust', ['bark-face', 'cloth-disc'], {'disc': {'color': '#9A4526'}}),
                       F('eucalyptus-disc-leaf', 'eucalyptus', 'disc, leaf green', ['bark-face', 'cloth-disc'], {'disc': {'color': '#5E6E4F'}}),
                       F('eucalyptus-disc-cream', 'eucalyptus', 'disc, cream', ['bark-face', 'cloth-disc'], {'disc': {'color': '#E4D9BF'}})]}),
    'study': dict(title='barkhorn: waveguide study (eucalyptus, bark face, rust disc)', rows={
        'three-quarter': [F(f'{f}-3q', 'eucalyptus', label, ['bark-face', 'cloth-disc'], product=form_product(f), camera=THREE_Q)
                          for f, label in FORMS],
        'side': [F(f'{f}-side', 'eucalyptus', label, ['bark-face', 'cloth-disc'], product=form_product(f), camera=SIDE)
                 for f, label in FORMS],
        'behind': [F(f'{f}-behind', 'eucalyptus', label, ['bark-face', 'cloth-disc'], product=form_product(f), camera=BEHIND,
                     at=TURNED) for f, label in FORMS]}),
    'proposal': dict(title='barkhorn: where the study points (round 3)', camera=RIGHT_Q, rows={
        'the proposal': [F('pebble-strata-eucalyptus', 'eucalyptus-strata', 'eucalyptus: pebble in strata resin, rust disc',
                           ['bark-face', 'cloth-disc'], product=form_product('pebble')),
                         F('pebble-terrazzo-birch', 'birch-terrazzo', 'birch: pebble in terrazzo resin, charcoal disc',
                           ['bark-face', 'cloth-disc'], product=form_product('pebble'))]}),
    'horn': dict(title='barkhorn: the photograph\'s horn on four posts', rows={
        'three-quarter': [F('shell-3q', 'eucalyptus', 'back: shell round the driver', product=form_product('cast'), camera=HORN_Q, lights=GLOW),
                          F('tub-3q', 'eucalyptus', 'back: tub', product=form_product('cast-tub'), camera=HORN_Q, lights=GLOW)],
        'side': [F('shell-side', 'eucalyptus', 'shell: posts 55 and 148 showing', product=form_product('cast'), camera=HORN_SIDE, lights=GLOW),
                 F('tub-side', 'eucalyptus', 'tub: posts 33 and 42 showing', product=form_product('cast-tub'), camera=HORN_SIDE, lights=GLOW)],
        'behind': [F('shell-behind', 'eucalyptus', 'shell, from behind', product=form_product('cast'), camera=HORN_BEHIND, at=TURNED, lights=GLOW),
                   F('tub-behind', 'eucalyptus', 'tub, from behind', product=form_product('cast-tub'), camera=HORN_BEHIND, at=TURNED, lights=GLOW)]}),
    'resin': dict(title='barkhorn: the cast resin, close to', camera=CLOSE, rows={
        'birch': [F('birch-milk', 'birch', 'milk, honey where thick (birch\'s)', product=form_product('cast'), lights=GLOW, size=[900, 640]),
                  F('birch-amber', 'birch', 'amber, as the eucalyptus\'s', product=form_product('cast'), lights=GLOW, size=[900, 640],
                    materials={'horn': {'color': '#EFE5D0', 'deep': '#D6A04E', 'cloud': 0.6}}),
                  F('birch-clear', 'birch', 'clearer milk, little amber', product=form_product('cast'), lights=GLOW, size=[900, 640],
                    materials={'horn': {'color': '#F4F2EC', 'deep': '#E6D3AE', 'radius': 0.03}})],
        'eucalyptus': [F('eucalyptus-amber', 'eucalyptus', 'amber: cream clouded with honey (the photograph\'s)', product=form_product('cast'),
                         lights=GLOW, size=[900, 640]),
                       F('eucalyptus-kino', 'eucalyptus', 'kino: the gum\'s red-brown resin', product=form_product('cast'), lights=GLOW, size=[900, 640],
                         materials={'horn': {'color': '#EEE3D3', 'deep': '#B4602F', 'cloud': 0.3}}),
                       F('eucalyptus-leaf', 'eucalyptus', 'leaf: deep gum-leaf green', product=form_product('cast'), lights=GLOW, size=[900, 640],
                         materials={'horn': {'color': '#E3E8D8', 'deep': '#4F6E35', 'cloud': 0.3}}),
                       F('eucalyptus-smoke', 'eucalyptus', 'smoke: the grey bark\'s', product=form_product('cast'), lights=GLOW, size=[900, 640],
                         materials={'horn': {'color': '#E6E4DD', 'deep': '#6E6A60', 'cloud': 0.3}})]}),
    'pressed': dict(title='barkhorn: faced in pressed recycled plastic', camera=RIGHT_Q, rows={
        'the speakers': [F('pressed-eucalyptus', 'eucalyptus-pressed', 'eucalyptus: strips of olive, ochre, rust and grey', product=PRESSED, lights=GLOW),
                         F('pressed-birch', 'birch-pressed', 'birch: black dashes in milk', product=PRESSED, lights=GLOW)],
        'close to': [F('pressed-eucalyptus-corner', 'eucalyptus-pressed', 'strips, pressed-in bits, an edge strip in front', product=PRESSED,
                       camera=CORNER, lights=GLOW),
                     F('pressed-birch-corner', 'birch-pressed', 'milk flakes, black dashes', product=PRESSED, camera=CORNER, lights=GLOW)]}),
    'pick': dict(title='barkhorn: where round 4 points', camera=RIGHT_Q, rows={
        'the pair': [F('pick-birch', 'birch', 'birch: milk resin, charcoal disc', lights=GLOW),
                     F('pick-eucalyptus', 'eucalyptus', 'eucalyptus: amber resin, rust disc', lights=GLOW)],
        'as photographed': [F('pick-photo-birch', 'birch', 'birch, from the photograph\'s angle', camera=PHOTO, lights=GLOW),
                            F('pick-photo-eucalyptus', 'eucalyptus', 'eucalyptus, from the photograph\'s angle', camera=PHOTO, lights=GLOW)]}),
    'horn5': dict(title='barkhorn: the horn the cabinet\'s full depth, on a 2 in driver', rows={
        bark: [F(f'{bark}-3q', bark, 'three-quarter', camera=HORN_Q, lights=GLOW5),
               F(f'{bark}-side', bark, 'side: its back flush with the cabinet\'s', camera=HORN_SIDE, lights=GLOW5),
               F(f'{bark}-behind', bark, 'from behind: the pod and its cap', camera=HORN_BEHIND, at=TURNED, lights=GLOW5),
               F(f'{bark}-throat', throat, label, camera=THROAT, lights=GLOW5, size=[900, 640])]
        for bark, throat, label in (('birch', 'birch-clear', 'into the 2 in throat (clear resin shows it)'),
                                    ('eucalyptus', 'eucalyptus-green', 'into the 2 in throat (opaque green)'))}),
    'shells': dict(title='barkhorn: the waveguide\'s resin, close to', camera=CLOSE, rows={
        bark: [F(f'shell-{fl}', fl, label, lights=GLOW5, size=[900, 640]) for fl, label in frames] for bark, frames in SHELLS.items()}),
    'woodfree': dict(title='barkhorn without wood: pressed recycled plastic in the bark\'s pattern', camera=RIGHT_Q, rows={
        'the speakers': [F('woodfree-eucalyptus', 'eucalyptus-pressed', 'eucalyptus: the bark\'s strips, pressed', product=PRESSED, lights=GLOW5),
                         F('woodfree-birch', 'birch-pressed', 'birch: the bark\'s lenticels, pressed', product=PRESSED, lights=GLOW5)],
        'close to': [F('woodfree-eucalyptus-corner', 'eucalyptus-pressed', 'a corner: each panel its own sheet', product=PRESSED,
                       camera=CORNER, lights=GLOW5),
                     F('woodfree-birch-corner', 'birch-pressed', 'a corner, birch', product=PRESSED, camera=CORNER, lights=GLOW5),
                     F('woodfree-strips-corner', 'eucalyptus-strips', 'round 4\'s strips, to compare', product=PRESSED, camera=CORNER,
                       lights=GLOW5)]}),
    'pick5': dict(title='barkhorn: where round 5 points', camera=RIGHT_Q, rows={
        'the pair': [F('pick5-birch', 'birch', 'birch: smoked resin, charcoal disc', lights=GLOW5),
                     F('pick5-eucalyptus', 'eucalyptus', 'eucalyptus: bottle-green resin, rust disc', lights=GLOW5)],
        'as photographed': [F('pick5-photo-birch', 'birch', 'birch, from the photograph\'s angle', camera=PHOTO, lights=GLOW5),
                            F('pick5-photo-eucalyptus', 'eucalyptus', 'eucalyptus, from the photograph\'s angle', camera=PHOTO, lights=GLOW5)]}),
    'printed': dict(title='barkhorn: the horn printed with its bark, in translucent inks', rows={
        'birch': [F('printed-birch', 'birch-printed', 'lenticels printed on clear', product=PRESSED, camera=CLOSE, lights=GLOW5, size=[900, 640]),
                  F('printed-birch-smoke', 'birch-printed-smoke', 'on a light smoke', product=PRESSED, camera=CLOSE, lights=GLOW5,
                    size=[900, 640]),
                  F('printed-birch-speaker', 'birch-printed', 'the speaker', product=PRESSED, camera=RIGHT_Q, lights=GLOW5)],
        'eucalyptus': [F('printed-eucalyptus', 'eucalyptus-printed', 'strips printed on clear', product=PRESSED, camera=CLOSE, lights=GLOW5,
                         size=[900, 640]),
                       F('printed-eucalyptus-green', 'eucalyptus-printed-green', 'on a light green', product=PRESSED, camera=CLOSE,
                         lights=GLOW5, size=[900, 640]),
                       F('printed-eucalyptus-speaker', 'eucalyptus-printed', 'the speaker', product=PRESSED, camera=RIGHT_Q, lights=GLOW5)]}),
    'cabinets': dict(title='barkhorn without wood: the cabinet in other plastics', camera=RIGHT_Q, rows={
        'translucent, as late-90s electronics (cast acrylic)': [
            F('cab-y2k-smoke', 'birch-y2k-smoke', 'smoked acrylic, smoked horn', product=PRESSED, lights=GLOW5),
            F('cab-y2k-green', 'eucalyptus-y2k-green', 'green acrylic, bottle-green horn', product=PRESSED, lights=GLOW5),
            F('cab-y2k-ice', 'birch-y2k-ice', 'frosted ice, clear horn', product=PRESSED, lights=GLOW5)],
        'stone': [F('cab-terrazzo', 'birch-stone-terrazzo', 'terrazzo', product=PRESSED, lights=GLOW5),
                  F('cab-marble', 'birch-stone-marble', 'cultured marble', product=PRESSED, lights=GLOW5),
                  F('cab-onyx', 'eucalyptus-stone-onyx', 'green onyx, translucent', product=PRESSED, lights=GLOW5)],
        'marble and swirl, horn and cabinet alike': [
            F('cab-marbled-birch', 'birch-marbled', 'marbled black and white', product=PRESSED, lights=GLOW5),
            F('cab-marbled-eucalyptus', 'eucalyptus-marbled', 'marbled in the bark\'s colours', product=PRESSED, lights=GLOW5),
            F('cab-swirled-birch', 'birch-swirled', 'smoke swirled through clear', product=PRESSED, lights=GLOW5),
            F('cab-swirled-eucalyptus', 'eucalyptus-swirled', 'green swirled through amber', product=PRESSED, lights=GLOW5)]}),
    'pick6': dict(title='barkhorn: the line, without wood', rows={
        'the pair': [F('pick6-birch', 'birch-pressed', 'birch: smoked resin, oat disc', product=PRESSED, camera=RIGHT_Q, lights=GLOW5),
                     F('pick6-eucalyptus', 'eucalyptus-pressed', 'eucalyptus: bottle-green resin, graphite disc', product=PRESSED,
                       camera=RIGHT_Q, lights=GLOW5)],
        'from the front: a port in each corner': [
            F('pick6-front-birch', 'birch-pressed', 'birch', product=PRESSED, camera=FRONT_CAM, lights=GLOW5),
            F('pick6-front-eucalyptus', 'eucalyptus-pressed', 'eucalyptus', product=PRESSED, camera=FRONT_CAM, lights=GLOW5)]}),
    'discs': dict(title='barkhorn: the disc in neutral colours', camera=RIGHT_Q, rows={
        bark: [F(f'disc-{bark}-{name}', f'{bark}-pressed', label, product=PRESSED, lights=GLOW5, materials={'disc': {'color': hx}})
               for name, label, hx in options]
        for bark, options in (('birch', DISCS_BIRCH), ('eucalyptus', DISCS_EUCALYPTUS))}),
    'lookbook': dict(title='barkhorn: the look book', camera=LOOK, rows={
        f'{line}: {label}': [F(f'look-{key}-on', flav, 'cover on', product=PRESSED, lights=GLOW5, size=[840, 1100], stage=sweep(c),
                               sky=STUDIO),
                             F(f'look-{key}-off', flav, 'cover off', product=PRESSED, lights=GLOW5, size=[840, 1100], stage=sweep(c),
                               sky=STUDIO, hide=['cloth-disc'])]
        for line, key, flav, label, c in LOOKS}),
    'lookbook2': dict(title='EARF: the look book at twice the size', camera=LOOK2, rows={
        f'{line}: {label}': [F(f'look-{key}-on', flav, 'cover on', product=PRESSED, lights=GLOW5, size=[1080, 2160], stage=sweep(c),
                               sky=STUDIO),
                             F(f'look-{key}-off', flav, 'cover off', product=PRESSED, lights=GLOW5, size=[1080, 2160], stage=sweep(c),
                               sky=STUDIO, hide=['cloth-disc'])]
        for line, key, flav, label, c in LOOKS}),
    'horn10': dict(title='EARF: the horn from the side and from behind', camera=HORN10, rows={
        f'{line}: {label}': [F(f'horn-{key}-side', flav, 'from the side', product=PRESSED, lights=GLOW5, size=[1200, 900],
                               stage=sweep(c), sky=STUDIO, at={'rotate_z': 115}),
                             F(f'horn-{key}-back', flav, 'from behind', product=PRESSED, lights=GLOW5, size=[1200, 900],
                               stage=sweep(c), sky=STUDIO, at={'rotate_z': 155})]
        for line, key, flav, label, c in LOOKS if key in HORN10_KEYS}),
    'room12': dict(title='EARF: the pair in a room', camera=ROOM12_CAM, rows={
        'room': [F('room-eucalyptus', 'eucalyptus-printed', 'eucalyptus, in a room', product=PRESSED, lights=ROOM12_LIGHTS,
                   size=[2880, 1620], stage=ROOM12_SET, sky=ROOM12_SKY, pair=ROOM12_PAIR, sun=ROOM12_SUN,
                   render=ROOM12_RENDER, materials={'bark': {'space': 'object'}, 'horn': {'space': 'object'}})]}),
    'experiments': dict(title='barkhorn: material experiments', camera=RIGHT_Q, rows={
        'cabinet': [F('pressed-eucalyptus', 'eucalyptus-pressed', 'pressed recycled plastic, eucalyptus', ['bark-face', 'cloth-disc']),
                    F('pressed-birch', 'birch-pressed', 'pressed recycled plastic, birch', ['bark-face', 'cloth-disc'])],
        'waveguide': [F('strata-eucalyptus', 'eucalyptus-strata', 'strata resin waveguide', ['bark-face', 'cloth-disc']),
                      F('terrazzo-birch', 'birch-terrazzo', 'terrazzo resin waveguide', ['bark-face', 'cloth-disc'])]}),
}


def shot_for(frame, set_camera):
    bark = frame['bark'].split('-')[0]
    s = copy.deepcopy(json.load(open(os.path.join(SHOTS, f'{bark}.json'))))
    at = frame['at'] or {}
    inst = {'position': at.get('position', [0, 0, 0]), 'rotate_z': at.get('rotate_z', 0), 'flavour': frame['bark']}
    for L in s['lights'].values():          # the lamps follow a speaker brought forward
        for k in ('target', 'position'):
            if k in L:
                L[k] = [L[k][0], L[k][1] + at.get('shift', 0.0), L[k][2]]
    if frame['options']:
        inst['options'] = frame['options']
    if frame.get('hide'):
        inst['hide'] = frame['hide']
    insts = [inst]
    if frame.get('pair'):
        insts = [{**{k: v for k, v in inst.items() if k not in ('position', 'rotate_z')}, **q} for q in frame['pair']]
    s['product'] = {'def': frame['product'], 'flavour': frame['bark'], 'instances': insts}
    s['camera'] = copy.deepcopy(frame['camera'] or set_camera)
    s['size'] = frame['size'] or [760, 1000]
    s['title'] = f"barkhorn, {frame['label']}"
    if frame['materials']:
        s.setdefault('materials', {}).update(frame['materials'])
    s['lights'].update(copy.deepcopy(frame['lights']))
    if frame.get('stage'):
        s['set'] = copy.deepcopy(frame['stage'])
    if frame.get('sky'):
        s['sky'] = copy.deepcopy(frame['sky'])
    if frame.get('sun'):
        s['sun'] = copy.deepcopy(frame['sun'])
    if frame.get('render'):
        s['render'].update(frame['render'])
    return s


def build_models(names):
    """Each named study model (MODELS: the product with some parameters changed) built into out/study/: its render
    model and engine file."""
    venv = os.path.join(ROOT, '.venv-fab', 'bin', 'python')
    code = f'''
import copy, dataclasses, os, sys
sys.path.insert(0, {os.path.join(ROOT, 'studio', 'fabkit')!r})
import build, render
P0 = build.load_product({os.path.join(HERE, 'product.py')!r})
os.makedirs({STUDY!r}, exist_ok=True)
for name, changes in {[(n, MODELS[n]) for n in names]!r}:
    params = copy.deepcopy(P0.params)
    for path, v in changes.items():
        d = params
        *head, last = path.split('.')
        for k in head:
            d = d[k]
        d[last] = v
    prod = dataclasses.replace(P0, name='barkhorn-' + name, params=params)
    parts = [p for p in prod.parts(params) if p.solid is not None]
    glb, pf = render.write(prod, parts, {STUDY!r}, engine_file=os.path.join({STUDY!r}, 'barkhorn-' + name + '.json'), proof=False)
    print('built', name, os.path.relpath(glb, {ROOT!r}), flush=True)
'''
    subprocess.run([venv, '-c', code], check=True, cwd=ROOT)


def font(size, bold=False):
    from fontTools.ttLib import TTFont
    from PIL import ImageFont
    tt = TTFont(os.path.join(ROOT, 'render', 'fonts', 'Archivo-Bold.woff' if bold else 'Archivo-Regular.woff'))
    tt.flavor = None
    buf = io.BytesIO(); tt.save(buf); buf.seek(0)
    return ImageFont.truetype(buf, size)


def grid(title, cells, out, cell_w=480):
    """cells: {row: [(png, label), ...]} -> one image, each row under its name, each frame's name under it; each frame
    `cell_w` wide."""
    from PIL import Image, ImageDraw
    rows = list(cells)
    w0, h0 = Image.open(cells[rows[0]][0][0]).size
    w, h = cell_w, round(cell_w * h0 / w0)
    pad, lab, head, rowhead = 20, 40, 64, 40
    ncol = max(len(v) for v in cells.values())
    W = pad + ncol * (w + pad)
    H = head + len(rows) * (rowhead + h + lab) + pad
    sheet = Image.new('RGB', (W, H), (246, 244, 239))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 20), title, font=font(28, True), fill=(30, 28, 26))
    for r, row in enumerate(rows):
        y = head + r * (rowhead + h + lab)
        d.text((pad, y + 4), row, font=font(24, True), fill=(30, 28, 26))
        y += rowhead
        for c, (png, label) in enumerate(cells[row]):
            x = pad + c * (w + pad)
            im = Image.open(png).convert('RGB')
            k = min(w / im.width, h / im.height)             # a frame of another shape fits inside the cell, centred
            fw, fh = round(im.width * k), round(im.height * k)
            sheet.paste(im.resize((fw, fh), Image.LANCZOS), (x + (w - fw) // 2, y + (h - fh) // 2))
            d.text((x, y + h + 8), label, font=font(20), fill=(60, 56, 52))
    sheet.save(out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('set', choices=list(SETS))
    ap.add_argument('--samples', type=int, default=64)
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--day', default='2026-10-12')
    ap.add_argument('--only', nargs='*', default=[], help='frame names to render again (e.g. birch-disc-charcoal)')
    ap.add_argument('--all', action='store_true', help='render every frame again')
    ap.add_argument('--build', action='store_true', help='build the set\'s study models again')
    a = ap.parse_args()
    S = SETS[a.set]
    need = sorted({os.path.basename(fr['product'])[len('barkhorn-'):-len('.json')] for frames in S['rows'].values() for fr in frames
                   if fr['product'].startswith(os.path.relpath(STUDY, ROOT))})
    todo = [n for n in need if a.build or not os.path.exists(os.path.join(STUDY, f'barkhorn-{n}.json'))
            or not os.path.exists(os.path.join(STUDY, 'render', f'barkhorn-{n}.glb'))]
    if todo:
        build_models(todo)
    sd = os.path.join(SHOTS, a.set); os.makedirs(sd, exist_ok=True)
    rd = os.path.join(ROOT, 'renders', DAY.get(a.set, a.day), 'barkhorn')
    od = os.path.join(rd, a.set); os.makedirs(od, exist_ok=True)
    cells = {}
    for row, frames in S['rows'].items():
        cells[row] = []
        for fr in frames:
            path = os.path.join(sd, f"{fr['name']}.json")
            json.dump(shot_for(fr, S.get('camera')), open(path, 'w'), indent=1)
            png = os.path.join(od, f"{fr['name']}.png")
            if a.all or fr['name'] in a.only or not os.path.exists(png):
                print('render', fr['name'], flush=True)
                subprocess.run([sys.executable, os.path.join(ROOT, 'studio', 'engine', 'render.py'), path, '--out', png,
                                '--samples', str(a.samples), '--scale', str(a.scale)], check=True, cwd=ROOT,
                               stdout=subprocess.DEVNULL)
            cells[row].append((png, fr['label']))
    print(grid(S['title'], cells, os.path.join(rd, f'{a.set}.png')))


if __name__ == '__main__':
    main()
