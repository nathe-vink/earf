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
DEFAULTS = dict(colourway='neutral', chair_leather=R.CHAIR_LEATHER, banq_col=R.BANQ_COL, sink_deep=R.SINK_DEEP,
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
    # the card: a small folded tent card by the right deck, its face to the customers
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


def room(bpy, name, p, kit):
    K.R = R                                                           # round 36's builders on round 37's plan
    p = {**DEFAULTS, **p}
    objs = K.room(bpy, name, p, kit)
    niches(bpy, kit, p, objs)
    ledges(bpy, kit, p, objs)
    altar_plinths(bpy, kit, p, objs)
    ginza(bpy, kit, p, objs)
    return objs
