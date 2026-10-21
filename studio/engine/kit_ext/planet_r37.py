"""Planet EARF, round 37: the bar as a showroom (spinoffs/barkhorn/planet/r37/README.md). Round 36's room
(planet_r36.py) on round 37's plan (r37_plan.py): the room neutral and warm so any configuration works, the bar pair
in two timber-lined, felt-lined niches in the back bar either side of the decks, EARF's record players at the decks,
the sink in Smoke glowing amber.

    {"kind": "kit", "shape": "ext", "module": "planet_r37", "fn": "room", ...round 36's keys...}

Round 36's builders read their plan module as `R`; this swaps it for round 37's (which imports round 36's and changes
only what the brief changes), runs round 36's room, then adds the niches.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'spinoffs', 'barkhorn', 'planet', 'r37'))
sys.path.insert(0, HERE)
import planet_r36 as K                                               # noqa: E402
import r37_plan as R                                                 # noqa: E402

LK = K.LK
DEFAULTS = dict(altar_lining='fir', colourway='neutral', chair_leather=R.CHAIR_LEATHER, banq_col=R.BANQ_COL, sink_deep=R.SINK_DEEP,
                sink_glow_col=R.SINK_GLOW, decks='earf', disc_col='#FFD2A0')


def niches(bpy, kit, p, objs):
    """Each a box of dark oak (cheeks, head, floor board, back) lined in charcoal felt, open to the counter; a hidden
    warm strip in the head grazes down the cabinet; the felt stops 150 above the horn."""
    N = R.SPK_NICHE
    oak = K.Mesh('spk-niche-oak'); felt = K.Mesh('spk-niche-felt'); strip = K.Mesh('spk-niche-strip')
    for xc in R.SPK_NICHES:
        x0, x1, yf, yb, z0, z1 = R.niche_box(xc)
        t, f = N['wall'], N['felt']
        oak.box(x0, yf + 0.004, z0, x0 + t, yb, z1)                  # the cheeks
        oak.box(x1 - t, yf + 0.004, z0, x1, yb, z1)
        oak.box(x0 + t, yf + 0.004, z1 - t, x1 - t, yb, z1)          # the head
        oak.box(x0 + t, yf, z0, x1 - t, yb, z0 + 0.02)               # the floor board
        oak.box(x0 + t, yb - t, z0 + 0.02, x1 - t, yb, z1 - t)       # the back
        fw = 0.045                                                    # a proud face frame: two stiles and a head
        oak.box(x0 - 0.012, yf - 0.012, z0, x0 + fw, yf + 0.004, z1 + 0.012)
        oak.box(x1 - fw, yf - 0.012, z0, x1 + 0.012, yf + 0.004, z1 + 0.012)
        oak.box(x0 + fw, yf - 0.012, z1 - fw, x1 - fw, yf + 0.004, z1 + 0.012)
        # the felt: a hair inside the oak (coplanar faces render black)
        felt.box(x0 + t + 0.001, yb - t - f, z0 + 0.021, x1 - t - 0.001, yb - t - 0.001, z1 - t - 0.001)
        felt.box(x0 + t + 0.001, yf + 0.02, z0 + 0.021, x0 + t + f, yb - t - f, z1 - t - 0.001)
        felt.box(x1 - t - f, yf + 0.02, z0 + 0.021, x1 - t - 0.001, yb - t - f, z1 - t - 0.001)
        felt.box(x0 + t + f, yf + 0.02, z1 - t - f, x1 - t - f, yb - t - f, z1 - t - 0.001)
        strip.box(x0 + t + f + 0.03, yf + 0.04, z1 - t - f - 0.012, x1 - t - f - 0.03, yf + 0.06, z1 - t - f - 0.004)
    objs.append(oak.object(bpy, K.dark_oak(bpy, vertical=True, name='oak-spk-niche'), bevel=0.003))
    objs.append(felt.object(bpy, kit.material(bpy, 'felt', p.get('niche_felt', '#1C1B1A'))))
    lamp = strip.object(bpy, K.emitter(bpy, 'spk-niche-strip', '#FF9A50', p.get('spk_niche_strip', 2.0)))
    lamp.visible_camera = False; lamp.visible_glossy = False; objs.append(lamp)


def ledges(bpy, kit, p, objs):
    """The ledge under each niche: a solid oak block on the back bar's worktop, its top at counter height, faced to the
    floor of the niche; a sloped oak wedge under each cabinet, its top the cabinet's tilted base."""
    import math
    from mathutils import Matrix, Vector
    oak = K.Mesh('spk-ledges')
    B = R.BACKBAR36
    for xc in R.SPK_NICHES:
        x0, x1, yf, yb, z0, z1 = R.niche_box(xc)
        oak.box(x0 - 0.012, yf - 0.012, B['low'], x1 + 0.012, yb, z0)
    objs.append(oak.object(bpy, K.dark_oak(bpy, name='oak-spk-ledge'), bevel=0.003))
    # the light plinth (the owner: "Lights under the speakers could be cool too"): the wedge under each cabinet in
    # frosted acrylic lit from within, so light rises into the tinted cabinet's base; its glow `plinth` (0 = an unlit
    # frosted wedge), its colour the configuration's (warm amber in Smoke, red in Ember, blue in Ice)
    oak = K.Mesh('spk-light-plinths')
    zf = R.SPK_LEDGE['top'] + R.SPK_NICHE['floor'] + 0.001
    hw, hd = R.CLOUD_HALF['w'] - 0.01, R.CLOUD_HALF['d'] - 0.01
    for role, x, y, z, rot, tilt in R.bar_speakers():
        M = (Matrix.Translation(Vector((x, y, z))) @ Matrix.Rotation(math.radians(rot), 4, 'Z')
             @ Matrix.Rotation(math.radians(tilt), 4, 'X'))
        top = [M @ Vector((sx * hw, sy * hd, -0.001)) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        bot = [Vector((v.x, v.y, zf)) for v in top]
        bm = oak.bm
        vt = [bm.verts.new(v) for v in top]; vb = [bm.verts.new(v) for v in bot]
        bm.faces.new(vt); bm.faces.new(list(reversed(vb)))
        for i in range(4):
            j = (i + 1) % 4
            bm.faces.new([vb[i], vb[j], vt[j], vt[i]])
    col = p.get('plinth_bar_col', '#FFB060')
    w = oak.object(bpy, LK.acrylic(bpy, 'frosted', 'plinth-bar-' + col, glow=p.get('plinth_bar', p.get('plinth', 0.0)), glow_col=col), bevel=0.002)
    w.visible_shadow = False; objs.append(w)


def altar_plinths(bpy, kit, p, objs):
    """The listening pair's plinths get the same: a frosted acrylic top, lit from within, 30 deep, standing 2 proud of
    the oak on every side."""
    import math
    S = R.PAIR36; z0 = R.ZONE['z'] + S['plinth'] - 0.030
    top = K.Mesh('altar-light-tops')
    for role, colour, x, y, z, rot in R.speakers():
        K._obox(top.bm, x, y, z0, S['plinth_d'] + 0.004, S['plinth_w'] + 0.004, 0.0295, math.radians(rot + 90))
    col = p.get('plinth_listen_col', '#FFB060')
    t = top.object(bpy, LK.acrylic(bpy, 'frosted', 'plinth-listen-' + col, glow=p.get('plinth_listen', p.get('plinth', 0.0)), glow_col=col), bevel=0.002)
    t.visible_shadow = False; objs.append(t)


def ginza(bpy, kit, p, objs):
    """Details from the owner's photo of Ginza Music Bar: a warm strip under the counter's top edge lighting its front;
    a single sconce with a glass chimney on the record wall; a small card by the decks, "Sorry, no requests"."""
    import math
    C = R.COUNTER
    zt = C['top_z'] - C['top_t']
    st = K.Mesh('counter-strip')
    st.box(C['x0'] + 0.45, C['y0'] - C['over'] + 0.006, zt - 0.008, C['x1'] - 0.45, C['y0'] - C['over'] + 0.018, zt - 0.002)
    lamp = st.object(bpy, K.emitter(bpy, 'counter-strip', '#FFB870', p.get('counter_strip', 3.0)))
    lamp.visible_camera = False; lamp.visible_glossy = False; objs.append(lamp)
    # the sconce: a brass back plate and arm, a clear glass chimney round a small warm bulb
    sx, sz = p.get('sconce_x', 4.30), p.get('sconce_z', 2.42)
    yw = R.W - 0.02 - R.RECORD_WALL['depth'] - 0.004
    br = K.Mesh('sconce-brass')
    K._cyl(br.bm, sx, yw - 0.006, sz, 0.05, 0.012, seg=32, axis='y')
    K.LK._rod(br.bm, (sx, yw - 0.01, sz), (sx, yw - 0.16, sz), 0.007, 0.007, seg=12)
    K._cyl(br.bm, sx, yw - 0.16, sz - 0.09, 0.035, 0.012, seg=32)            # the cup the chimney stands in
    K.LK._rod(br.bm, (sx, yw - 0.16, sz), (sx, yw - 0.16, sz - 0.078), 0.006, 0.006, seg=10)
    objs.append(br.object(bpy, K.brass(bpy), smooth=True))
    gl = K.Mesh('sconce-glass')
    K._lathe(gl.bm, [(0.032, 0.0), (0.034, 0.0), (0.040, 0.06), (0.036, 0.16), (0.033, 0.16), (0.037, 0.06), (0.030, 0.0)],
             seg=48, z0=sz - 0.078, cx=sx, cy=yw - 0.16)
    g = gl.object(bpy, K.principled(bpy, 'chimney-glass', '#FFFFFF', rough=0.02, trans=1.0, ior=1.5), smooth=True)
    g.visible_shadow = False; objs.append(g)
    bu = K.Mesh('sconce-bulb'); K._cyl(bu.bm, sx, yw - 0.16, sz - 0.02, 0.012, 0.03, seg=24)
    objs.append(bu.object(bpy, K.emitter(bpy, 'sconce-filament', '#FFB060', p.get('sconce_glow', 6.0)), smooth=True))
    K._lamp(bpy, 'sconce-lamp', (sx, yw - 0.16, sz + 0.0), p.get('sconce_w', 6.0), 2300)
    # the card: a small folded tent card by the right deck, its face to the customers. Out since 2026-10-20 (the owner's
    # EARFcoin: a coin per guest, exchanged for a song request; round 38 puts a request column here): `card` to show it
    if p.get('card', False):
        cx, cy, cz = R.DJ['x'] + 0.80, C['y1'] - 0.30, C['top_z']
        a = math.radians(14)
        card = K.Mesh('no-requests-card')
        hgt, w = 0.075, 0.105
        for sgn in (-1, 1):
            y0 = cy + sgn * hgt * math.sin(a)
            bm = card.bm
            q = [bm.verts.new((cx - w / 2, y0, cz)), bm.verts.new((cx + w / 2, y0, cz)),
                 bm.verts.new((cx + w / 2, cy, cz + hgt * math.cos(a))), bm.verts.new((cx - w / 2, cy, cz + hgt * math.cos(a)))]
            bm.faces.new(q if sgn < 0 else list(reversed(q)))
        c = card.object(bpy, K.principled(bpy, 'card-stock', '#E9E2D2', rough=0.8))
        c.modifiers.new('thick', 'SOLIDIFY').thickness = 0.0008
        objs.append(c)
        try:
            cu = bpy.data.curves.new('no-requests', 'FONT'); cu.body = p.get('card_text', 'Sorry, no requests')
            cu.size = 0.0085; cu.align_x = 'CENTER'; cu.align_y = 'CENTER'
            ob = bpy.data.objects.new('no-requests', cu); bpy.context.scene.collection.objects.link(ob)
            ob.data.materials.append(K.principled(bpy, 'card-ink', '#1E1A16', rough=0.7))
            zc = cz + hgt * math.cos(a) / 2; yc = cy - hgt * math.sin(a) / 2 - 0.0012
            ob.location = (cx, yc, zc); ob.rotation_euler = (math.radians(90) - a, 0, 0)
            objs.append(ob)
        except Exception as e:
            print('card: no text', e)



# --- the sink in Smoke, as smoked glass (the lead, 2026-10-20: drop the glow; a hidden lamp in a tinted block reads as
# a lit Corian box at any level) ---------------------------------------------------------------------------------------
def _bowl_cutter(bpy, cx, cy, top, bx, by, D, f, seg=96, n=24):
    """A soft basin: an elliptical bowl `D` deep, its wall eased into the top by a radius `f` at the rim; a closed mesh
    for the boolean."""
    import bmesh, math
    from mathutils import Vector
    prof = []                                          # (radial offset from the ellipse, z below the top)
    for k in range(n + 1):                             # the bowl: a half-ellipsoid D - f deep under the fillet
        b = math.pi / 2 * (n - k) / n
        prof.append((math.cos(b), -f - (D - f) * math.sin(b), 'bowl'))
    for k in range(1, n // 2 + 1):                     # the fillet: from vertical at depth f to the top at offset f
        a = math.pi / 2 * k / (n // 2)
        prof.append((1.0, -f + f * math.sin(a), f - f * math.cos(a)))
    prof.append((1.0, 0.02, f + 0.01))
    me = bpy.data.meshes.new('sink37-cut'); bm = bmesh.new(); rings = []
    for s_, z, d in prof:
        ring = []
        for j in range(seg):
            t = 2 * math.pi * j / seg
            if d == 'bowl':
                x, y = bx * s_ * math.cos(t), by * s_ * math.sin(t)
            else:
                x, y = (bx + d) * math.cos(t), (by + d) * math.sin(t)
            ring.append(bm.verts.new(Vector((cx + x, cy + y, top + z))))
        rings.append(ring)
    bot = bm.verts.new(Vector((cx, cy, top - D)))
    for j in range(seg):
        bm.faces.new((bot, rings[0][(j + 1) % seg], rings[0][j]))   # rings[0] is the bottom (s = cos(pi/2) = 0)
    for a, b in zip(rings, rings[1:]):
        for j in range(seg):
            bm.faces.new((a[j], a[(j + 1) % seg], b[(j + 1) % seg], b[j]))
    bm.faces.new(rings[-1])
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    for fc in bm.faces:
        fc.smooth = True
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new('sink37-cut', me); bpy.context.scene.collection.objects.link(ob)
    return ob


def sink(bpy, kit, p, objs):
    """The alcove in the shell's fir, boards running up; a floating slab in the Cloud's Smoke (cast acrylic, polished),
    read by what it reflects and by its arrises; a soft bowl 120 deep with a 30 radius at the rim and a steel waste; a
    brushed-steel spout and a separate lever, each on its own escutcheon. Its light is the room's: a narrow warm
    downlight into the bowl, a hidden strip under the slab's front edge, a wash down the boards."""
    import math
    A = R.ALCOVE; S = R.SINK37
    bk = K.Mesh('alcove-back'); bk.box(A['x0'], 0.001, 0.0, A['x1'], 0.003, A['z1'])
    objs.append(bk.object(bpy, K.principled(bpy, 'alcove-shadow', '#0A0806', rough=0.9)))
    boards = [K.Mesh(f'alcove-fir-{k}') for k in range(3)]; x = A['x0']; k = 0
    while x < A['x1'] - 0.01:
        boards[(k * 2) % 3].box(x + 0.002, 0.004, 0.0, min(x + 0.136, A['x1']), A['depth'], A['z1'])
        x += 0.14; k += 1
    for k, (m, tint) in enumerate(zip(boards, ('#5A3C26', '#4E3420', '#64442C'))):
        objs.append(m.object(bpy, LK.fir(bpy, vertical=True, tint=tint, mix=0.45), bevel=0.003))
    hd = K.Mesh('alcove-head'); hd.box(A['x0'] - 0.02, 0.0, A['z1'], A['x1'] + 0.02, A['depth'] + 0.04, A['z1'] + 0.05)
    objs.append(hd.object(bpy, K.dark_oak(bpy, name='oak-alcove-head'), bevel=0.004))
    y0 = A['depth'] + S['gap']; z0 = S['top'] - S['t']; cy = y0 + S['d'] / 2
    blk = K.Mesh('sink-block'); blk.box(S['x'] - S['w'] / 2, y0, z0, S['x'] + S['w'] / 2, y0 + S['d'], S['top'])
    smoke = K.resin(bpy, p.get('sink_deep', '#8A888E'), 'sink-smoke', radius=p.get('sink_radius', 0.025),
                    rough=p.get('sink_rough', 0.02))
    ob = blk.object(bpy, smoke)
    cut = _bowl_cutter(bpy, S['x'], cy, S['top'], S['bx'], S['by'], S['D'], S['fillet'])
    mod = ob.modifiers.new('basin', 'BOOLEAN'); mod.operation = 'DIFFERENCE'; mod.object = cut; mod.solver = 'EXACT'
    bev = ob.modifiers.new('arris', 'BEVEL'); bev.width = 0.004; bev.segments = 3; bev.limit_method = 'ANGLE'
    bev.angle_limit = 1.2
    cut.hide_render = True; cut.hide_viewport = True
    objs.append(ob)
    # the waste: a brushed-steel ring and grid a hair above the bowl's floor, a dark throat under it
    zb = S['top'] - S['D']
    ws = K.Mesh('sink-waste'); K._cyl(ws.bm, S['x'], cy, zb + 0.0015, 0.021, 0.002, seg=48)
    objs.append(ws.object(bpy, K.brushed_steel(bpy), smooth=True))
    th = K.Mesh('sink-waste-throat'); K._cyl(th.bm, S['x'], cy, zb + 0.0036, 0.014, 0.0004, seg=32)
    objs.append(th.object(bpy, K.principled(bpy, 'waste-throat', '#050505', rough=0.6)))
    # the spout and the lever, each on an escutcheon on the boards' face (round 36's plate sat inside the boards)
    fy = A['depth']; zs = S['top'] + 0.22; xl = S['x'] + 0.13
    sp = K.Mesh('sink-spout')
    K._cyl(sp.bm, S['x'], zs, fy, 0.035, 0.008, seg=48, axis='y')                    # the escutcheon, 70
    LK._rod(sp.bm, (S['x'], fy + 0.006, zs), (S['x'], fy + 0.20, zs), 0.011, 0.011, seg=24)
    LK._rod(sp.bm, (S['x'], fy + 0.195, zs + 0.004), (S['x'], fy + 0.215, zs - 0.05), 0.011, 0.010, seg=24)
    K._cyl(sp.bm, xl, zs, fy, 0.024, 0.007, seg=40, axis='y')                         # the lever's, 48
    LK._rod(sp.bm, (xl, fy + 0.005, zs), (xl, fy + 0.045, zs), 0.012, 0.012, seg=24)
    LK._rod(sp.bm, (xl, fy + 0.04, zs), (xl, fy + 0.04, zs + 0.075), 0.0045, 0.0035, seg=12)  # the lever, up
    objs.append(sp.object(bpy, K.brushed_steel(bpy), smooth=True))
    # the light: a strip hidden under the slab's front edge washing the boards and floor beneath (warm white)
    if p.get('sink_strip', 0) > 0:
        K._area(bpy, 'sink-strip', (S['x'], y0 + S['d'] - 0.03, z0 - 0.004), (0, 0, 0), (S['w'] - 0.06, 0.012),
                p['sink_strip'], kelvin=3000)
    # round 38 prep (the lead: let its thickness read, the front not crushed): a hidden panel under the slab facing up
    # into its bottom face, so light crosses the cast to the polished front and arrises
    if p.get('sink_under', 0) > 0:
        import math
        K._area(bpy, 'sink-under', (S['x'], y0 + S['d'] / 2, z0 - 0.006), (math.pi, 0, 0), (S['w'] - 0.04, S['d'] - 0.04),
                p['sink_under'], kelvin=3000)
    # and a soft warm panel facing the slab from the room side, seen in its polished front (a photographer's softbox:
    # the front face of a smoked block reads only by what it mirrors)
    if p.get('sink_fill', 0) > 0:
        import math
        f = K._area(bpy, 'sink-fill', (S['x'], 1.45, z0 + S['t'] / 2), (math.radians(90), 0, 0), (0.9, 0.35),
                    p['sink_fill'], kelvin=2900)
        f.visible_glossy = True
    # round 38 prep (the lead: rake a narrow line along the polished arrises): a long thin strip above and in front of
    # the slab, aimed at its top front arris, seen in the bevel as a bright line
    if p.get('sink_rake', 0) > 0:
        import math
        yf = y0 + S['d']; zr = S['top'] + 0.30; yr = yf + 0.22
        a = math.atan2(zr - S['top'], yr - yf)
        r = K._area(bpy, 'sink-rake', (S['x'], yr, zr), (math.radians(90) - a + math.radians(90), 0, 0),
                    (S['w'] + 0.10, 0.012), p['sink_rake'], kelvin=3200)
        r.visible_glossy = True
    # round 38b (the lead: the bowl's floor lifted by a room reflection, not crushed black): a soft warm panel over the
    # front of the slab facing down, seen in the polished bowl and top
    if p.get('sink_top_fill', 0) > 0:
        tf = K._area(bpy, 'sink-top-fill', (S['x'], y0 + S['d'] + 0.25, S['top'] + 0.75), (math.radians(-35), 0, 0),
                     (0.7, 0.3), p['sink_top_fill'], kelvin=3000)
        tf.visible_glossy = True
    # and a wash down the boards from the alcove's head, so the slab has something to reflect
    if p.get('sink_wash', 0) > 0:
        import math
        K._area(bpy, 'sink-wash', ((A['x0'] + A['x1']) / 2, A['depth'] + 0.10, A['z1'] - 0.03),
                (math.radians(-25), 0, 0), (A['x1'] - A['x0'] - 0.1, 0.03), p['sink_wash'], kelvin=2900)



# --- round 38 prep: signs of life in the listening zone (the lead, 2026-10-20) -----------------------------------------
def _tilted_box(bm, cx, cy, z0, w, d, h, heading, lean):
    """A box w (along `heading`) by d by h standing at (cx, cy, z0), leaning back by `lean` radians about its base's
    long edge (a sleeve against a plinth)."""
    from mathutils import Matrix, Vector
    import bmesh
    g = bmesh.ops.create_cube(bm, size=1.0)
    M = (Matrix.Translation((cx, cy, z0)) @ Matrix.Rotation(heading, 4, 'Z') @ Matrix.Rotation(-lean, 4, 'X')
         @ Matrix.Translation((0, -d / 2, h / 2)) @ Matrix.Diagonal((w, d, h, 1)))
    bmesh.ops.transform(bm, matrix=M, verts=g['verts'])


def zone_life(bpy, kit, p, objs):
    """A sleeve leaning on the left plinth, its record on the table by the near chair; a coat over the near chair's back;
    a rocks glass and a coupe by the Orb on the near tables."""
    import math
    Z = R.ZONE; z0 = Z['z']; P = R.PAIR36; T = R.TUB
    sl = K.Mesh('zone-sleeves')
    (role, c, sx, sy, sz, rot) = R.speakers()[0]
    _tilted_box(sl.bm, sx - P['plinth_d'] / 2 - 0.10, sy + 0.12, z0, 0.314, 0.004, 0.314, math.radians(90) - 0.0, math.radians(14))
    tx, ty = R.TUB_TABLES[0]                          # the zone's middle table
    K._obox(sl.bm, tx - 0.04, ty + 0.06, z0 + R.TUB_TABLE['h'] + 0.0005, 0.314, 0.314, 0.003, math.radians(-20))
    objs.append(sl.object(bpy, K.principled(bpy, 'sleeve-zone', '#C9B79A', rough=0.6)))
    vr = K.Mesh('zone-record'); K._cyl(vr.bm, tx - 0.04, ty + 0.06, z0 + R.TUB_TABLE['h'] + 0.0035, 0.15, 0.0018, seg=64)
    objs.append(vr.object(bpy, K.principled(bpy, 'vinyl', '#0B0B0C', rough=0.25), smooth=True))
    # a coat over the back of the near chair (the one nearest the camera's side of the zone)
    cx, cy = R.TUBS[0]
    ax, ay = P['x'], R.YC
    face = math.atan2(ay - cy, ax - cx); bx, by = cx - math.cos(face) * (T['r'] - 0.05), cy - math.sin(face) * (T['r'] - 0.05)
    co = K.Mesh('zone-coat'); top = z0 + T['h']
    K._obox(co.bm, bx - math.cos(face) * 0.07, by - math.sin(face) * 0.07, top - 0.50, 0.03, 0.46, 0.51, face)
    K._obox(co.bm, bx, by, top - 0.005, 0.16, 0.46, 0.035, face)
    objs.append(co.object(bpy, LK.wool(bpy, '#8A6A48', 'wool-coat-zone'), bevel=0.015, seg=3))



# --- round 38 prep: a host stand inside the door for the bowl of EARFcoins (the owner: "Each guest gets one") --------
def host_stand(bpy, kit, p, objs):
    """A blackened-steel post on a plate, a dark-oak top: where the bowl of coins waits inside the door."""
    H = R.HOST
    st = K.Mesh('host-steel')
    K._cyl(st.bm, H['x'], H['y'], 0.0, 0.16, 0.012, seg=48)
    K._cyl(st.bm, H['x'], H['y'], 0.012, 0.03, H['top'] - 0.04 - 0.012, seg=24)
    objs.append(st.object(bpy, K.blackened_steel(bpy), smooth=True))
    tp = K.Mesh('host-top'); tp.box(H['x'] - H['w'] / 2, H['y'] - H['d'] / 2, H['top'] - 0.04, H['x'] + H['w'] / 2,
                                    H['y'] + H['d'] / 2, H['top'])
    objs.append(tp.object(bpy, K.dark_oak(bpy, name='oak-host'), bevel=0.004))



# --- the Orbs wired in the bar (the owner, 2026-10-20; the kit's own cable, round 32f, runs 420 mm straight back from
# the base, off a small table): a thin black fabric cable from the back of each base to a grommet in its table and down
# through it to the floor. The kit piece's own cable is off (`cable: false`), the Orb still plugged in
_CABLE_M = {}


def _cable(bpy, name, T, c):
    """A plug-in Orb, wired (the owner, 2026-10-20: USB-C, a battery cartridge optional; in a bar it is wired): a thin
    black fabric cable from the back of the base across the table top to a grommet, and down through it to the floor."""
    import bmesh
    from mathutils import Matrix, Vector
    r = c.get('radius', 0.0022); back = c.get('back', 0.075); run = c.get('run', 0.10); floor = c['floor']
    z0 = T.translation.z
    p0 = T @ Vector((0.0, back, r)); p1 = T @ Vector((0.0, back + run, r))
    pts = [p0, p1, Vector((p1.x, p1.y, z0 - 0.02)), Vector((p1.x, p1.y, floor + r))]
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    for a, b in zip(pts, pts[1:]):
        d = b - a; L = d.length
        if L < 1e-4:
            continue
        g = bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=r, radius2=r, depth=L)
        q = d.normalized().to_track_quat('Z', 'Y').to_matrix().to_4x4()
        bmesh.ops.transform(bm, matrix=Matrix.Translation((a + b) / 2) @ q, verts=g['verts'])
    # the grommet: a black anodised ring flush in the table top
    g = bmesh.ops.create_cone(bm, cap_ends=False, segments=24, radius1=0.009, radius2=0.009, depth=0.003)
    bmesh.ops.transform(bm, matrix=Matrix.Translation((p1.x, p1.y, z0 + 0.0008)), verts=g['verts'])
    bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    key = 'orb-cable-fabric'
    if key not in _CABLE_M:
        _CABLE_M[key] = K.MT.make(bpy, key, 'rubber', {'color': '#121212', 'roughness': 0.85, 'sheen': 0.5})
    ob.data.materials.append(_CABLE_M[key])
    return [ob]



def orb_cables(bpy, kit, p, objs):
    from mathutils import Matrix
    for i, s in enumerate(p.get('orb_cables', [])):
        T = Matrix.Translation(s['position'])
        objs += _cable(bpy, f'orb-cable#{i}', T, {'radius': 0.0022, 'back': 0.075, 'run': 0.10, 'floor': s['floor']})


# --- round 38b (the critics, all frames: the fir, the fluted oak repeat): each loose part of a board or flute object
# takes one of a few copies of its scanned material, the copies' grain shifted and turned, dealt at random
def _vary(bpy, mat, k):
    import math
    name = f'{mat.name}~v{k}'
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    m = mat.copy(); m.name = name
    for n in m.node_tree.nodes:
        if n.type == 'MAPPING':
            loc = n.inputs['Location'].default_value
            n.inputs['Location'].default_value = (loc[0] + 0.37 * k, loc[1] + 0.61 * k, loc[2] + 0.53 * k)
            r = n.inputs['Rotation'].default_value
            n.inputs['Rotation'].default_value = (r[0], r[1], r[2] + math.radians(180 * (k % 2)))
    return m


def decorrelate(bpy, ob, n=5, seed=38):
    """Deal the object's loose parts (its boards, its flutes) across `n` shifted copies of its material."""
    import bmesh, random
    if not ob.data.materials:
        return
    base = ob.data.materials[0]
    for k in range(1, n):
        ob.data.materials.append(_vary(bpy, base, k))
    bm = bmesh.new(); bm.from_mesh(ob.data); bm.faces.ensure_lookup_table()
    rnd = random.Random(seed); seen = set()
    for f in bm.faces:
        if f.index in seen:
            continue
        stack = [f]; part = []
        while stack:
            g = stack.pop()
            if g.index in seen:
                continue
            seen.add(g.index); part.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen:
                        stack.append(h)
        k = rnd.randrange(n)
        for g in part:
            g.material_index = k
    bm.to_mesh(ob.data); bm.free()



# --- round 38b: a sign of life where each camera looks (the lead, from the critics) ----------------------------------
def extra_life(bpy, kit, p, objs):
    """Glasses, an open record sleeve, a wet ring on the zinc, a soap on a steel dish: whatever the view's settings list."""
    import math
    G = p.get('life_glasses', []); SL = p.get('life_sleeves', []); RG = p.get('life_rings', []); SO = p.get('life_soap')
    if G:
        glass = K.principled(bpy, 'tumbler-glass', '#FFFFFF', rough=0.01, trans=1.0, ior=1.5)
        pour = K.principled(bpy, 'pour-r36', '#B5601A', rough=0.0, trans=1.0, ior=1.36)
        rocks = [(0, 0), (0.041, 0), (0.0425, 0.09), (0.0385, 0.09), (0.037, 0.016), (0, 0.016)]
        gl = K.Mesh('life38-glasses'); lq = K.Mesh('life38-pours')
        for x, y, z, fill in G:
            K._lathe(gl.bm, rocks, seg=40, z0=z + 0.0002, cx=x, cy=y)
            K._cyl(lq.bm, x, y, z + 0.0167, 0.0366, fill, seg=40)
        objs.append(gl.object(bpy, glass, smooth=True)); objs.append(lq.object(bpy, pour, smooth=True))
    for k, (x, y, z, a) in enumerate(SL):
        sl = K.Mesh(f'life38-sleeve{k}'); K._obox(sl.bm, x, y, z + 0.0006, 0.314, 0.314, 0.003, math.radians(a))
        objs.append(sl.object(bpy, K.principled(bpy, 'sleeve-life38', '#B9A98C', rough=0.6)))
        vr = K.Mesh(f'life38-record{k}'); K._cyl(vr.bm, x + 0.06 * math.cos(math.radians(a)), y + 0.06 * math.sin(math.radians(a)),
                                                  z + 0.0040, 0.15, 0.0018, seg=64)
        objs.append(vr.object(bpy, K.principled(bpy, 'vinyl', '#0B0B0C', rough=0.25), smooth=True))
    if RG:
        rg = K.Mesh('life38-rings')
        for x, y, z in RG:                              # a thin wet ring a glass left, not a disc
            K._lathe(rg.bm, [(0.034, 0.0), (0.038, 0.0), (0.038, 0.0003), (0.034, 0.0003)], seg=48, z0=z + 0.0001, cx=x, cy=y)
        objs.append(rg.object(bpy, K.principled(bpy, 'wet-ring', '#3A3A3A', rough=0.08), smooth=True))
    if SO:
        x, y, z = SO
        d = K.Mesh('life38-soapdish'); K._cyl(d.bm, x, y, z + 0.0003, 0.045, 0.006, seg=40)
        objs.append(d.object(bpy, K.blackened_steel(bpy), smooth=True))
        so = K.Mesh('life38-soap'); K._obox(so.bm, x, y, z + 0.0065, 0.07, 0.045, 0.022, math.radians(12))
        objs.append(so.object(bpy, K.principled(bpy, 'soap-stone', '#CFC6B4', rough=0.7), bevel=0.008, seg=3))


def room(bpy, name, p, kit):
    K.R = R                                                           # round 36's builders on round 37's plan
    K.sink = sink                                                     # the sink as smoked glass (the lead, 2026-10-20)
    p = {**DEFAULTS, **p}
    LK.STEEL_MIX = p.get('steel_mix', 0.55)
    objs = K.room(bpy, name, p, kit)
    niches(bpy, kit, p, objs)
    ledges(bpy, kit, p, objs)
    altar_plinths(bpy, kit, p, objs)
    ginza(bpy, kit, p, objs)
    if p.get('zone_life'):
        zone_life(bpy, kit, p, objs)
    if p.get('host_stand'):
        host_stand(bpy, kit, p, objs)
    orb_cables(bpy, kit, p, objs)
    extra_life(bpy, kit, p, objs)
    if p.get('decorrelate'):
        for ob in objs:
            if any(ob.name.startswith(t) for t in ('counter-flutes', 'alcove-fir', 'altar-fir', 'records-shelving')):
                decorrelate(bpy, ob)
    return objs
