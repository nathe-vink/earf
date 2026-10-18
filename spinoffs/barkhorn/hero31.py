"""The hero, remade for the campaign (round 31, r31-hero): the eight Clouds on a gentle arc on pale paper, lit from
behind and low so each tinted cabinet throws its own colour onto the floor in front of it.

site30/hero.json (the template, kept as it is) scored 5.5 with the blind promotional critic
(critic/rounds/2026-10-18/promo-hero-r1.json). This module writes its successor from one table of settings, so every
pass of the critic is a change to `P` and a render, and the site's link boxes come from the same arc and camera.

    python3 spinoffs/barkhorn/hero31.py build [--portrait] [--set key=value ...]   writes studio/shots/barkhorn/hero31/
    python3 spinoffs/barkhorn/hero31.py spots [--portrait] [--report IMG.report.json]
                                                                 the eight link boxes, % of the frame (projected, or
                                                                 read off a rendered frame)
    python3 spinoffs/barkhorn/hero31.py card --tag h9                              the critic's card, current settings

Notes and the critic's passes: hero31.md.
"""
import argparse, copy, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'studio', 'shots', 'barkhorn', 'hero31')

# spectrum order: Ember, Dust, Acid, Poison, Ice, Haze, Fog, Smoke
FLAVOURS = ['cloud-red', 'cloud-orange', 'cloud-amber', 'eucalyptus-y2k-green', 'cloud-blue', 'cloud-violet',
            'birch-fog-clear', 'cloud-black']
W_M, H_M = 0.56, 1.33
CABINET = ['left', 'right', 'top', 'bottom', 'front-panel', 'back', 'brace*', 'rib-*', 'land-*']          # a Cloud's width and its height to the horn's top (README: 1293 cabinet and feet)

P = {
    # the arc: centres `pitch` apart along x, the middle `sag` metres farther from the camera than the ends; each copy
    # turned to face the lens, then `toe` degrees more toward the middle (0: every baffle square to the camera)
    'pitch': 0.72, 'sag': 0.5, 'toe': 0.0, 'stagger': 0.7, 'x0': -0.05, 'turns': [3.0, -4.0, -2.0, 5.0, -3.0, 2.0, -5.0, 4.0],
    # the camera: distance in front of the ends, height, lens; it looks level (verticals stay vertical), the frame
    # placed by `aim_z` (the height it centres on) and `shift_y`
    'cam_dist': 13.5, 'cam_h': 2.2, 'lens': 70.0, 'aim_z': 0.8, 'shift_y': -0.03, 'fstop': 4.0, 'focus_y': 0.0,
    # the key: a small hard source behind the middle of the arc, low, aimed through the line at the floor in front
    'key_y': 14.0, 'key_z': 9.5, 'key_size': 0.8, 'key_w': 0.0, 'key_irr': 5.5, 'key_color': 5200, 'key_spread': 100,
    # or the key as a sun from behind the wall (the sweep casts no shadow): W/m2 (0: the disc above), elevation, size
    'sun': 32.0, 'sun_el': 30.0, 'sun_angle': 1.5,
    # cutters behind the row (only the sun meets them), each opening its speaker's shape seen from the sun, `cut_in`
    # metres inside its edges; false off
    'cutters': False, 'cut_in': 0.006,
    # side strips lighting the cabinets' edges (light-linked to the cabinets), W/m2; 0 off
    'sides': 14.0, 'sides_r': 20.0,
    # the cyc: a ground row on the floor behind the line, washing the sweep's wall evenly
    'cyc_irr': 21.0, 'cyc_z': 2.0, 'cyc_color': 5200,
    # the top: a silk over the floor behind the line, so the floor between the line and the cove is paper, not a band
    'top_irr': 4.0, 'top_y': 7.0,
    # the over: a silk high over the floor in front of the line, lifting the shadows as a white ceiling would
    'over_irr': 3.0, 'over_y': -5.0,
    # the front fill: a large soft source over the camera
    'fill_irr': 3.5, 'fill_color': 5200, 'fill_size': [8.0, 2.0], 'fill_z': 2.0, 'fill_spec': 0.0,
    # the faces: a fill for the speakers alone (light-linked to the cabinet, lining and rings), 0 off
    'face_irr': 5.5, 'face_z': 2.6, 'edge': 6.0, 'smoke_kick': 80.0, 'smoke_at': [4.0, 0.5, 2.0],
    # the cones: a strip softbox above the camera light-linked to the cones, surrounds and caps (matte paper, so it
    # models them rather than glinting), W/m2; 0 off
    'strip': 70.0, 'strip_z': 2.6,
    # the paper
    'paper': '#EEECE7', 'tooth': 2.2, 'tooth_mm': 0.9, 'mottle': 0.06, 'contact': 0.6,
    'sky': 0.15, 'hdri': 'studio_small_03_1k', 'hdri_rot': 0.0, 'depth': 12.0,
    # the render
    'exposure': -2.5, 'wb': 5250, 'tint': 3.0, 'samples': 256, 'transmission_bounces': 16,
    'white_in': 228, 'white_out': 230, 'peak': 246, 'contrast': 0.18, 'clarity': 0.10, 'sharpen': 0.45, 'vibrance': 0.4,
}


def arc(p):
    """[(x, y, rotate_z)] for the eight, left to right (or nearest first, on a diagonal)."""
    n = len(FLAVOURS)
    if p.get('diag'):                   # a straight line receding from (x0, y0) by (dx, dy) a step, each facing the lens
        x0, y0, dx, dy = p['diag']
        pts = [(x0 + i * dx, y0 + i * dy) for i in range(n)]
        return [(x, y, math.degrees(math.atan2(-x, y + p['cam_dist'])) + p['toe']) for x, y in pts]
    half = p['pitch'] * (n - 1) / 2
    cam_y = -p['cam_dist']
    out = []
    for i in range(n):
        x = (i - (n - 1) / 2) * p['pitch']
        y = p['sag'] * (1 - (x / half) ** 2) + (p['stagger'] if i % 2 else 0.0)   # every other one a step back
        if i % 2:                       # the back rank spread by its extra distance, so each lands in its gap in the frame
            x *= (y - cam_y) / (p['sag'] * (1 - (x / half) ** 2) - cam_y)
        x += p['x0']
        rz = math.degrees(math.atan2(-x, y - cam_y)) + (p['toe'] * (1 if x < 0 else -1) if x else 0)
        rz += p['turns'][i] if p.get('turns') else 0.0    # each set down by hand: a few degrees off true
        out.append((x, y, rz))
    return out


def cutters(p, a):
    """Black cutters behind the row that only the sun's shadow rays meet (`see_through`), so the sun reaches the floor
    in front only through the acrylic: the floor round the throws lies in the even light of the silks, the cabinets'
    grey shadows sink into it, and the colour that passes is all that reads (a photographer's cutters).

    One upright plane at the foot of the cove, down to the floor (the sun's rays are parallel, so an opening projected
    along them works at any distance); each speaker's opening is its cabinet's and its
    horn's boxes projected along the sun onto it (`cut_in` metres inside them, so no white light slips past an edge). The plane is
    cut into pieces round the openings: a full-height piece between neighbours, the shoulders beside the cabinet under
    the wider horn, a piece over each horn and one under each foot (the floor between the plane and the speaker). Only the strip of floor behind the plane, at the cove, is sunlit (its rays
    cross no cutter), so the line where the sun stops is the cove's own."""
    e = math.radians(p['sun_el'])
    v = (0.0, 0.0, 1.0)                                  # an upright plane just behind the back rank, facing the sun's way
    n_ = (0.0, 1.0, 0.0)
    C = (0.0, p['depth'] - 3.4, 0.0)                     # at the foot of the cove: the floor in front of it all in shade
    S = lambda P: P[2] + (C[1] - P[1]) * math.tan(e)     # where the sun's ray through a point crosses the plane
    k = p['cut_in']
    ops = []
    for x, y, rz in a:
        t = math.radians(rz)
        def box(x0, x1, y0, y1, z0, z1):
            us, ss = [], []
            for bx in (x0, x1):
                for by in (y0, y1):
                    for bz in (z0, z1):
                        wx, wy = x + bx * math.cos(t) - by * math.sin(t), y + bx * math.sin(t) + by * math.cos(t)
                        us.append(wx); ss.append(S((wx, wy, bz)))
            return [min(us) + k, max(us) - k, min(ss), max(ss) - k]
        cab = box(-0.28, 0.28, -0.214, 0.209, 0.0, 0.892)
        horn = box(-0.313, 0.313, -0.214, 0.206, 0.931, 1.293)
        ops.append((cab, horn))
    out = {}
    def piece(name, u0, u1, s0, s1):
        if u1 - u0 < 0.002 or s1 - s0 < 0.002:
            return
        u, sc = (u0 + u1) / 2, (s0 + s1) / 2
        P = (C[0] + u, C[1] + sc * v[1], C[2] + sc * v[2])
        out[name] = {'type': 'flag', 'size_m': [round(u1 - u0, 4), round(s1 - s0, 4)],
                     'position': [round(c, 4) for c in P], 'target': [round(P[j] + n_[j], 4) for j in range(3)],
                     'lights': ['sun'], 'see_through': True}
    lo_s, hi_s = 0.0, 9.0                                # down to the floor, so its foot hides behind the back rank
    for i, (cab, horn) in enumerate(ops):
        l = min(cab[0], horn[0]); r = max(cab[1], horn[1])
        prev_r = max(ops[i - 1][0][1], ops[i - 1][1][1]) if i else l - 9.0
        piece(f'cut{i}gap', prev_r - 0.01, l + 0.01, lo_s, hi_s)          # between this speaker and the last
        piece(f'cut{i}top', l, r, horn[3], hi_s)                          # over the horn
        piece(f'cut{i}foot', l, r, lo_s, cab[2] + 0.01)                   # under the foot: the floor behind it
        if horn[0] < cab[0]:
            piece(f'cut{i}sl', horn[0], cab[0] + 0.005, lo_s, horn[2] + 0.005)   # beside the cabinet, under the horn
        if horn[1] > cab[1]:
            piece(f'cut{i}sr', cab[1] - 0.005, horn[1], lo_s, horn[2] + 0.005)
        piece(f'cut{i}mid', l, r, cab[3], horn[2] + 0.01) if cab[3] < horn[2] else None   # the gap between cabinet and horn
    last = ops[-1]
    piece('cutend', max(last[0][1], last[1][1]) - 0.01, max(last[0][1], last[1][1]) + 9.0, lo_s, hi_s)
    return out


def camera(p):
    return {'position': [0.0, -p['cam_dist'], p['cam_h']], 'target': [0.0, 0.0, p['aim_z']], 'lens_mm': p['lens'],
            'level': True, **({'shift_y': p['shift_y']} if p['shift_y'] else {}),
            **({'fstop': p['fstop'], 'focus': [0.0, p['focus_y'], 0.7]} if p.get('fstop') else {})}


def shot(p, portrait=False):
    a = arc(p)
    inst = [{'flavour': f, 'position': [round(x, 4), round(y, 4), 0.0], 'rotate_z': round(rz, 3), 'hide': ['cloth-disc']}
            for f, (x, y, rz) in zip(FLAVOURS, a)]
    lights = {} if p['sun'] else {
        'key': {'type': 'area', 'shape': 'DISK' if not p['key_w'] else 'RECTANGLE',
                'size_m': [p['key_size'], p['key_size']] if not p['key_w'] else [p['key_w'], p['key_size']],
                'position': [0.0, p['key_y'], p['key_z']], 'target': [0.0, -2.0, 0.0],
                'irradiance': p['key_irr'], 'color': p['key_color'], 'spread_deg': p['key_spread'], 'transmission': False}}
    lights.update({
        'cyc': {'type': 'area', 'size_m': [30.0, 5.0], 'position': [0.0, p['depth'] - 7.0, p['cyc_z']], 'target': [0.0, p['depth'], p['cyc_z']],
                'irradiance': p['cyc_irr'], 'color': p['cyc_color'], 'spread_deg': 120, 'transmission': False},
        'top': {'type': 'area', 'size_m': [24.0, 6.0], 'position': [0.0, p['top_y'], 8.0], 'target': [0.0, p['top_y'] + 0.5, 0.0],
                'irradiance': p['top_irr'], 'color': p['cyc_color'], 'spread_deg': 90, 'transmission': False},
        'over': {'type': 'area', 'size_m': [16.0, 8.0], 'position': [0.0, p['over_y'], 8.0], 'target': [0.0, p['over_y'], 0.0],
                 'irradiance': p['over_irr'], 'color': p['cyc_color'], 'spread_deg': 90, 'transmission': False},
        'fill': {'type': 'area', 'size_m': p['fill_size'], 'position': [0.0, -p['cam_dist'] - 3.0, p['fill_z']],
                 'target': [0.0, 0.0, 0.7], 'irradiance': p['fill_irr'], 'color': p['fill_color'],
                 'specular': p['fill_spec']},
    })
    if p['sides']:                      # two tall strips either side, lighting the cabinets' edges and corners
        for nm, sx, irr in (('side_l', -1, p['sides']), ('side_r', 1, p['sides_r'] or p['sides'])):
            lights[nm] = {'type': 'area', 'size_m': [0.6, 3.0], 'position': [sx * 6.0, -3.0, 1.4] if sx < 0 else [7.0, -1.0, 1.6],
                          'target': [0.0, 0.0, 0.7],
                          'irradiance': irr, 'color': p['fill_color'], 'receivers': CABINET}
    if p['cutters'] and p['sun']:
        lights.update(cutters(p, a))
    if p['face_irr']:
        lights['face'] = {'type': 'area', 'size_m': [4.0, 2.0], 'position': [0.0, -p['cam_dist'] + 1.0, p['face_z']],
                          'target': [0.0, 0.0, 0.7], 'irradiance': p['face_irr'], 'color': p['fill_color'],
                          'receivers': CABINET + ['lining-*', 'woofer-ring'],
                          'specular': 0}
    if p['edge']:                       # a narrow strip high in front that the cabinets' top front edges and faces mirror
        lights['edge'] = {'type': 'area', 'size_m': [4.0, 0.6], 'position': [0.0, -p['cam_dist'] + 4.0, 3.2],
                          'target': [0.0, 0.0, 0.9], 'irradiance': p['edge'], 'color': p['fill_color'], 'receivers': CABINET}
    if p['smoke_kick']:                 # edge light on the smoked cabinet alone (the last copy)
        lights['smoke'] = {'type': 'area', 'size_m': [0.6, 2.5], 'position': p['smoke_at'], 'target': list(a[-1][:2]) + [0.8],
                           'irradiance': p['smoke_kick'], 'color': p['fill_color'],
                           'receivers': [f'{c}#{len(a) - 1}' for c in CABINET] + [f'waveguide#{len(a) - 1}']}
    if p['strip']:
        lights['strip'] = {'type': 'area', 'size_m': [9.0, 0.5], 'position': [0.0, -4.0, p['strip_z']],
                           'target': [0.0, 0.0, 0.62], 'irradiance': p['strip'], 'color': p['fill_color'],
                           'receivers': ['woofer-cone', 'woofer-surround', 'woofer-cap', 'hf-motor', 'hf-frame', 'hf-adaptor',
                                         'hf-plug']}
    sh = {
        **({'sun': {'azimuth_deg': 180, 'elevation_deg': p['sun_el'], 'irradiance': p['sun'], 'angle_deg': p['sun_angle'],
                    'color': p['key_color']}} if p['sun'] else {}),
        'product': {'def': 'studio/products/barkhorn-cloud.json', 'flavour': FLAVOURS[0], 'instances': inst},
        'set': {'kind': 'sweep', 'color': p['paper'], 'width': 34.0, 'front': 16.0, 'depth': p['depth'], 'radius': 3.0,
                'height': 16.0, 'cast_shadow': not p['sun'], 'contact': {'strength': p['contact'], 'distance_m': 0.08, 'core_strength': 0.4,
                                           'core_distance_m': 0.012}},
        'materials': {'sweep': {'tooth': p['tooth'], 'tooth_mm': p['tooth_mm'], 'mottle': p['mottle'], 'roughness': 0.9}},
        'lights': lights,
        'render': {'samples': p['samples'], 'adaptive': 0.01, 'denoise': True, 'clamp': 10, 'bounces': 24,
                   'transmission_bounces': p['transmission_bounces'], 'transparent_bounces': 64,
                   'view': 'Khronos PBR Neutral', 'exposure': p['exposure'], 'white_balance_k': p['wb'],
                   'white_balance_tint': p['tint']},
        'finish': {'enabled': True, 'white_in': p['white_in'], 'white_out': p['white_out'], 'peak': p['peak'], 'contrast': p['contrast'],
                   'clarity': p['clarity'], 'sharpen': p['sharpen'], 'sharpen_px': 0.7,
                   **({'dream': {'saturation': p['vibrance']}} if p['vibrance'] else {})},
        'title': 'EARF: the eight Clouds (hero31)',
        'size': [1600, 2000] if portrait else [2560, 1280],
        'camera': camera(p),
        'sky': ({'kind': 'hdri', 'file': p['hdri'], 'rotation_deg': p['hdri_rot'], 'strength': p['sky']} if p['hdri'] else
                {'kind': 'gradient', 'zenith': '#E9E8E5', 'horizon': '#ECEBE8', 'ground': '#8C8A86', 'strength': p['sky']}),
    }
    return sh


def spots(p, size=(2560, 1280), sensor=36.0):
    """The eight link boxes (% of the frame), as web.hero_spots() gives them: each Cloud's sides at its middle height,
    its top and its foot, projected through the engine's level camera (looking level, the frame placed by lens shift).
    The copies face the lens, so their width is W_M as seen."""
    W, H = size
    C, T = camera(p)['position'], camera(p)['target']
    lens = p['lens']
    k = lens / sensor * W                           # render.py fits the sensor to the frame's width
    # level camera: the target's height lands at the frame's centre (shift = its tilt), plus any extra shift
    dist_t = T[1] - C[1]
    out = []
    for x, y, _ in arc(p):
        d = y - C[1]
        def P(px, pz):
            u = (px - C[0]) / d * k + W / 2
            v = H / 2 - ((pz - C[2]) / d - (T[2] - C[2]) / dist_t) * k + p['shift_y'] * max(W, H)
            return u, v
        (l, _), (r, _), (_, top), (_, foot) = P(x - W_M / 2, 0.6), P(x + W_M / 2, 0.6), P(x, H_M), P(x, -0.02)
        out.append(dict(l=round(l / W * 100, 2), w=round((r - l) / W * 100, 2), t=round(top / H * 100, 2),
                        h=round((foot - top) / H * 100, 2)))
    return out


CARD = """# Card: {tag}

What it is for: the home page's hero image, full width at the top of the brand's site at 2:1 (shown 2400 and 1200
wide): the whole range at once. The eight colours of one loudspeaker stand on a gentle arc in spectrum order (red,
orange, golden yellow, green, blue, violet, water-clear, smoked black), covers off so each woofer shows in its coloured
ring, on pale paper, lit from behind and low so each tinted acrylic cabinet throws its colour onto the floor in front
of it. The picture is about colour and light passing through acrylic. The site's title ("Weather for the living
room.", one line, about 4 % of the frame's height, with a small eyebrow above it) sits over the top-left of the
frame, in the top fifth, and each speaker in the picture is a link.

Fixed (never yours to change): the speakers themselves, their shape, colours and parts. Each is a 1293 mm tall, 560 mm
wide horn loudspeaker: a cabinet of 20 mm tinted cast acrylic, lined inside with white polyester batts between its
ribs, under a horn of tinted resin, sold at about $20,000 a pair. The batts are opaque, so the floor behind a cabinet's
lining is in its shadow; the coloured light reaches the floor through the clear parts and the horn.

May change: the set (paper colour and grain, floor, what surrounds them), the light (direction, size, number, colour,
which surfaces a lamp lights), the camera (height, distance, lens, framing), the arrangement (spacing, arc, turn of
each speaker) and the finish (exposure, white point, contrast). The frame is {w} x {h}; this proof is at half size.

Current settings (metres; the speakers' feet at z = 0, the line's middle at the origin, the camera toward -y):
- arrangement: centres {pitch} m apart across, on an arc whose middle is {sag} m farther from the camera than its ends,
  every other speaker (orange, green, violet, smoke) {stagger} m farther back, so the eight stand in two staggered
  ranks; each turned to face the lens, then {toe} deg more toward the middle, then a few degrees off true as if set
  down by hand ({turns}).
- camera: at (0, -{cam_dist}, {cam_h}), {lens} mm lens on a 36 mm sensor, looking level (verticals vertical), the frame
  centred on height {aim_z} m by lens shift, extra shift {shift_y} frame heights; f/{fstop}, focused 0.7 m up at
  y = {focus_y} (between the ranks).
{keyline}
- cyc: a 30 x 5 m softbox facing the wall from 7 m in front of it, centred {cyc_z} m up, washing the wall and the cove, {cyc_irr} W/m2, {cyc_color} K.
- top: a 24 x 6 m silk at height 8 m over y = {top_y}, aimed down, {top_irr} W/m2 (the floor behind the line and the cove).
- over: a 16 x 8 m silk at height 8 m over y = {over_y} (the floor in front of the line), aimed down, {over_irr} W/m2.
- fill: an {fill_size} m softbox at (0, -{fill_y}, {fill_z}) behind the camera, aimed at the line, {fill_irr} W/m2, in
  reflections at a share of {fill_spec}.
- face: a 4 x 2 m softbox at (0, -{face_y}, {face_z}) light-linked to the cabinets, linings and rings only, no reflection,
  {face_irr} W/m2.
- strip: a 9 x 0.5 m strip at (0, -4, {strip_z}) light-linked to the woofer cones, surrounds and caps and the horn's
  compression driver, {strip} W/m2.
{cutline}- sides: two 0.6 x 3 m strips at (-6, -3, 1.4) and (7, -1, 1.6) aimed at the line, light-linked to the cabinets'
  acrylic, in reflections, {sides} W/m2 (left) and {sides_r} W/m2 (right).
- edge: a 4 x 0.6 m strip at (0, -{edge_y}, 3.2) light-linked to the cabinets' acrylic, in reflections (their top
  front edges and faces mirror it), {edge} W/m2.
- smoke: a 0.6 x 2.5 m strip at {smoke_at} light-linked to the smoked speaker's acrylic and horn only, {smoke_kick} W/m2.
{skyline}
- set: a paper sweep 34 m wide, its wall {depth} m behind the line, a 3 m cove.
- paper: {paper}, roughness 0.9, tooth {tooth} at {tooth_mm} mm, colour mottle {mottle}; a contact shadow {contact}.
- render: Cycles, {samples} samples, denoised, 24 bounces ({transmission_bounces} through clear parts), view Khronos PBR
  Neutral, exposure {exposure} EV, white balance {wb} K, tint {tint} (10 neutral, lower greener).
- finish: white point {white_in} -> {white_out} with a soft shoulder to {peak}, contrast {contrast}, clarity {clarity},
  sharpen {sharpen}, vibrance {vibrance}.
"""


def card(p, tag, size=(2560, 1280)):
    keyline = (f"- key: a sun from straight behind the line (the paper casts no shadow, so it reaches the floor), elevation "
               f"{p['sun_el']} deg, {p['sun']} W/m2, {p['sun_angle']} deg across, {p['key_color']} K; it is the only light that "
               f"throws the colour." if p['sun'] else
               f"- key: a {p['key_size']} m disc softbox at (0, {p['key_y']}, {p['key_z']}) behind the line, aimed at (0, -2, 0), "
               f"{p['key_irr']} W/m2 at its target, {p['key_color']} K, beam spread {p['key_spread']} deg; it is the only light "
               f"that throws the colour.")
    return CARD.format(tag=tag, w=size[0], h=size[1], fill_y=p['cam_dist'] + 3.0, face_y=p['cam_dist'] - 1.0, keyline=keyline, skyline=(f"- sky: a photographed small studio with softboxes (Poly Haven {p['hdri']}, CC0), turned {p['hdri_rot']} deg, strength {p['sky']}: seen only in reflections and as soft ambient." if p['hdri'] else f"- sky: a pale grey dome, strength {p['sky']}."), edge_y=p['cam_dist'] - 4.0,
                       cutline=('- cutters: black cutters behind the row that only the key meets (bounce light and the sky pass them), one '
                                'upright plane down to the floor at the foot of the cove, with an opening for each speaker the shape of its cabinet and horn seen from '
                                'the sun, so the key reaches the floor in front only through the acrylic; the floor round the throws '
                                'is lit by the silks alone.\n') if p['cutters'] else '',
                       **{k: v for k, v in p.items()})


def spots_from_report(report):
    """The eight link boxes read off a rendered frame's report (each copy's parts' boxes in the frame, the horn
    included), in the form web.hero_spots() gives: left, width, top, height as % of the frame. Exact where spots() is
    a projection of the arc (they agree within about 1 %)."""
    r = json.load(open(report))
    W, H = r['size']
    boxes = {}
    for k, v in r['parts_2d'].items():
        if '#' not in k or not v.get('box_px'):
            continue
        i, b = int(k.split('#')[1]), v['box_px']
        B = boxes.setdefault(i, [1e9, 1e9, -1e9, -1e9])
        B[:] = [min(B[0], b[0]), min(B[1], b[1]), max(B[2], b[2]), max(B[3], b[3])]
    return [dict(l=round(x0 / W * 100, 2), w=round((x1 - x0) / W * 100, 2), t=round(y0 / H * 100, 2),
                 h=round((y1 - y0) / H * 100, 2)) for x0, y0, x1, y1 in (boxes[i] for i in sorted(boxes))]


def parse_sets(sets, over=None):
    p = {**copy.deepcopy(P), **(over or {})}
    for kv in sets or []:
        k, v = kv.split('=', 1)
        p[k] = json.loads(v) if v[:1] in '[{0123456789-.tfn' else v
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('what', choices=['build', 'spots', 'card'])
    ap.add_argument('--report', help='spots: read the boxes off this rendered frame\'s report instead')
    ap.add_argument('--tag', default='h')
    ap.add_argument('--portrait', action='store_true')
    ap.add_argument('--set', action='append')
    ap.add_argument('--name')
    a = ap.parse_args()
    p = parse_sets(a.set, PORTRAIT if a.portrait else None)
    if a.what == 'build':
        os.makedirs(OUT, exist_ok=True)
        f = os.path.join(OUT, (a.name or ('hero-portrait' if a.portrait else 'hero')) + '.json')
        json.dump(shot(p, a.portrait), open(f, 'w'), indent=1)
        print(os.path.relpath(f, ROOT))
    elif a.what == 'card':
        print(card(p, a.tag, (1600, 2000) if a.portrait else (2560, 1280)))
    elif a.report:
        print(json.dumps(spots_from_report(a.report), indent=1))
    else:
        print(json.dumps(spots(p, (1600, 2000) if a.portrait else (2560, 1280)), indent=1))


# the phone frame (1600 x 2000; on a phone the title sits above the picture, not over it): the same two ranks drawn
# closer together (the back rank half hidden behind the front), from nearer and higher, so each speaker is as big
# as a narrow frame allows and the throws fan down the lower half
PORTRAIT = {'pitch': 0.5, 'stagger': 0.9, 'x0': 0.0, 'sag': 0.3, 'cam_dist': 7.0, 'cam_h': 2.8, 'lens': 50.0, 'aim_z': -0.25,
            'shift_y': 0.0, 'cyc_z': 3.0, 'cyc_irr': 24.0, 'top_irr': 6.0, 'face_irr': 9.0, 'face_z': 3.2, 'smoke_kick': 75.0,
            'over_irr': 3.5, 'over_y': -3.0, 'vibrance': 0.55, 'contrast': 0.22, 'sun_el': 26.0, 'sun_angle': 1.0}

if __name__ == '__main__':
    main()
