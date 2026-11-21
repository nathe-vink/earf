"""The house ground for the lamps (2026-11-20, the coordinator: Hemisphere and Core on the same light ground as the eight
Tropos fronts, off and on).

The recipe is the Tropos fronts' own (house-ground.json, copied verbatim from the speaker lane's shot): the warm white
sweep #F7F0E8 with its contact shading, the gradient sky at 0.15, every lamp of theirs with a light in it (key from
camera left at 40 degrees up, fill, kick, the big front softbox `horn`, and the four lamps linked to the sweep alone that
shape its tone), the camera, Khronos PBR Neutral, and their finish. A lamp is a fifth to a sixth of a speaker's size, so
the whole set is built at a scale s: every length (sweep, lamp positions, orbits, sizes, targets, camera) times s,
every irradiance unchanged (an area lamp's watts follow irradiance x pi x d^2, so at a fifth of the distance it puts
the same light on the subject). The camera's view of the set is then the Tropos frame's, and only the product differs.

Left out on purpose: the Tropos set's black flags and its white bounce card (cards for a speaker's gloss; out of frame,
and none is needed by a lamp), and the lamps at zero light (back, pool, edge, rim, paper, wall, wash, floor, through).

ON frames: every studio lamp and the sky divided by one declared factor DIM, the exposure raised by log2(DIM), so the
ground reads as in the OFF frame and the lamp's own light, at its real output, is what changed.
"""
import json, math, os, sys

from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, '..', '..', '..', '..', 'studio', 'engine')


def recipe():
    return json.load(open(os.path.join(HERE, 'house-ground.json')))


def _mul(v, s):
    return [x * s for x in v]


def build(bpy, s, dim=1.0, lift=0.0, studio=None):
    """The scaled set, sky and lamps. Returns (camera spec scaled, recipe).
    lift (m): the product hung that much higher (Hemisphere hung free, 2026-11-20); the product's lamps and the camera
    move up with it, the sweep and the lamps that light it alone stay. studio: a factor on every studio lamp and the sky
    apart from dim (the LIT frames: the studio taken down, the exposure set for the lamp); default 1/dim."""
    sys.path.insert(0, os.path.abspath(ENGINE))
    import sets as St, lights as Lt
    R = recipe()
    st = dict(R['set'])
    for k in ('width', 'front', 'depth', 'radius', 'height'):
        st[k] = st[k] * s
    ct = dict(st.get('contact') or {})
    for k in ('distance_m', 'core_distance_m'):
        if k in ct:
            ct[k] = ct[k] * s
    if os.environ.get('HOUSE_SWEEP_AO', '1') == '0':
        # (2026-11-21, the coordinator: LIT frames) the sweep's painted contact shadow off; in a dark studio it darkens
        # the lamp's own red pool next to the base; the path-traced shadow is the true one
        for k in ('strength', 'core_strength'):
            if k in ct:
                ct[k] = 0.0
    st['contact'] = ct
    st['flags'] = []; st['bounces'] = []
    sweep = St.sweep(bpy, st, {})[0]
    k_st = (1.0 / dim) if studio is None else studio
    sky = dict(R['sky']); sky['strength'] = sky['strength'] * k_st
    Lt.world(bpy, sky)
    centre = Vector(_mul(R['tropos_centre'], s))
    pcentre = centre + Vector((0, 0, lift))
    made = []
    # HOUSE_LIFT_RX (2026-11-20, the critics: a hot beam on the wall from a lamp just above the frame with the higher
    # hang): the lamps that light the sweep alone go up with the camera too, so the ground in frame is lit as in the
    # Tropos frame (and no sweep lamp sits just above the top edge)
    # (a list: only the lamps named, e.g. 'bg-left')
    rx_ = os.environ.get('HOUSE_LIFT_RX', '0')
    lift_rx = rx_ == '1'
    cen_rx = centre + Vector((0, 0, lift)) if lift_rx else centre
    solid = os.environ.get('HOUSE_SOLID', '1') == '1'
    for name, sp in R['lights'].items():
        if not (sp.get('irradiance', 0) > 0 or sp.get('power_w', 0) > 0):
            continue
        sp = json.loads(json.dumps(sp))
        if 'orbit' in sp:
            sp['orbit']['distance_m'] *= s
        for k in ('position', 'target'):
            if k in sp:
                sp[k] = _mul(sp[k], s)
                if not sp.get('receivers') or lift_rx or name in rx_.split(','):
                    sp[k][2] += lift
        sp['size_m'] = _mul(sp['size_m'], s)
        if 'power_w' in sp:
            sp['power_w'] *= s * s
        ob = Lt.area(bpy, 'house-' + name, sp, cen_rx if sp.get('receivers') else pcentre)
        ob.data.energy *= k_st
        if solid and not sp.get('receivers') and ob.data.specular_factor > 0:
            softbox(bpy, ob, s)
            if os.environ.get('HOUSE_LAMP_RAYVIS', '0') == '0':   # (the default since 2026-11-21: 1 the old double count)
                # (2026-11-21, the coordinator's audit, a test) specular_factor 0 may not hide the lamp from glossy and
                # transmission rays in Cycles; ray visibility does. The softbox's face then stands alone in reflections
                ob.visible_glossy = ob.visible_transmission = False
            if os.environ.get('HOUSE_SOFTBOX_SEEN', '1') == '0':
                # (2026-11-21, the coordinator: the LIT frames) the softboxes flagged off the lamp, as for a lamp that is
                # on: face and housing hidden from glossy and transmission rays (their outlines read as cracks in the
                # polished shell). The light on the set is unchanged; the room still reflects; the floor ring is untouched
                for nm_ in (ob.name + '-face', ob.name + '-housing'):
                    o_ = bpy.data.objects.get(nm_)
                    if o_ is not None:
                        o_.visible_glossy = o_.visible_transmission = False
                        print('SOFTBOX_UNSEEN', nm_)
        if sp.get('receivers'):
            # HOUSE_BG: the lamps that light the sweep alone, times one declared factor, so the paper behind a small
            # lamp reads as it does behind the speaker (whose own bounce lifts it); 1 is the recipe as it stands
            ob.data.energy *= float(os.environ.get('HOUSE_BG', '1'))
        if sp.get('receivers'):
            Lt.link_receivers(bpy, ob, [sweep])
        made.append(ob)
    if os.environ.get('HOUSE_WALL_LL'):
        # HOUSE_WALL_LL 'IRR' (2026-11-20, the pendant hung free: its lower frame is wall where the Tropos frame has
        # floor, 80 against 94 L*): a soft lamp lighting the sweep alone, low at the left, aimed at the wall behind and
        # below the shade, at IRR W/m2 (its size and place in full-scale metres, times s, lifted with the camera)
        wsp = {'type': 'area', 'size_m': [2.0 * s, 1.5 * s], 'position': [-3.0 * s, -0.8 * s, 1.2 * s + lift],
               'target': [-2.0 * s, 1.25 * s, 0.0], 'spread_deg': float(os.environ.get('HOUSE_WALL_LL_SPREAD', '180')), 'irradiance': float(os.environ['HOUSE_WALL_LL']),
               'color': '#FFF4E8', 'specular': 0.0, 'receivers': ['sweep']}
        wo = Lt.area(bpy, 'house-wall-ll', wsp, pcentre); wo.data.energy *= k_st * float(os.environ.get('HOUSE_BG', '1'))
        Lt.link_receivers(bpy, wo, [sweep]); made.append(wo)
    hf_ = os.environ.get('HOUSE_FLAGS', '0')     # '1' all of them, or names ('horn cutter')
    door_ = None
    if os.environ.get('HOUSE_DOOR'):
        door_ = barn_door(bpy, bpy.data.objects['house-key'], float(os.environ['HOUSE_DOOR']), s)
    if os.environ.get('HOUSE_KEYFLAG'):
        door_ = key_flag(bpy, bpy.data.objects['house-key'], [float(v) for v in os.environ['HOUSE_KEYFLAG'].split(',')], s)
    if hf_ != '0' or door_ is not None:
        # (2026-11-20, the critics: the Tropos ground darkens toward the bottom right, 84-87 at the bottom edge; the
        # lamps' stayed at 96) the Tropos set's flags that cast shadows, scaled: the card right of the product, the floor
        # card behind right, and the horn's cutter (whose shadow is that falloff). The back-edge card is the speaker's
        # own; the reflect-only cards cast nothing and are left out. Those over the floor stay on it; the others go up
        # with the product's lamps.
        fl = []
        for f in R['set']['flags']:
            if f.get('reflect_only') or f.get('name') == 'back-edge card':
                continue
            if hf_ != '1' and f.get('name') not in hf_.split(','):
                continue
            f = json.loads(json.dumps(f)); f['center_m'] = _mul(f['center_m'], s); f['size_m'] = _mul(f['size_m'], s)
            if f['center_m'][2] > 0.05 * s:
                f['center_m'][2] += lift
            fl.append(f)
            if f.get('name') == 'horn cutter' and os.environ.get('HOUSE_CUT2'):
                # HOUSE_CUT2 'LAMP,DX' (2026-11-20): a second cutter the same size, DX m (full scale) to the right, that
                # shades LAMP alone: the floor's front right off the fill, as the speaker's bulk shades it, its left kept
                l2_, dx_ = os.environ['HOUSE_CUT2'].split(',')
                f2 = json.loads(json.dumps(f)); f2['center_m'][0] += float(dx_) * s; f2['name'] = 'cutter2-' + l2_
                fl.append(f2)
        bo = []
        if os.environ.get('HOUSE_BOUNCE', '0') == '1':
            # the Tropos set's white bounce card right of the product, scaled (it lifts the floor at the left)
            for f in R['set'].get('bounces', []):
                f = json.loads(json.dumps(f)); f['center_m'] = _mul(f['center_m'], s); f['size_m'] = _mul(f['size_m'], s)
                f['center_m'][2] += lift; bo.append(f)
        if fl or bo:
            St.cards(bpy, {'flags': fl, 'bounces': bo})
        # Which lamps each cutter shades: the horn's cutter the lamps in HOUSE_CUT_SCOPE (default the horn alone, the
        # speaker lane's scope_flag), the second cutter its own lamp. HOUSE_CUT_FLOOR (default 1): a cutter shades the
        # FLOOR only, as the speaker's bulk did in the Tropos frame, never the product: each shaded lamp is split in two,
        # itself lighting everything but the sweep, and a copy of it lighting the sweep alone through its cutter (the
        # speaker lane's split_set_shadow, light linking); the cutters are then not seen in reflections either
        cuts = {}
        for i, f in enumerate(fl):
            if f.get('name') == 'horn cutter':
                cuts[f'flag{i}'] = os.environ.get('HOUSE_CUT_SCOPE', 'horn').split(',')
            elif f.get('name', '').startswith('cutter2-'):
                cuts[f'flag{i}'] = [f['name'][len('cutter2-'):]]
        if door_ is not None:
            cuts[door_.name] = ['key']
        lamps_ = [o for o in bpy.context.scene.objects if o.type == 'LIGHT' and o.name.startswith('house-')]
        floor_ = os.environ.get('HOUSE_CUT_FLOOR', '1') == '1'
        def excl(L_, obs):
            if not obs:                       # (an empty blocker collection would let nothing cast a shadow)
                return
            col_ = L_.light_linking.blocker_collection
            if col_ is None:
                col_ = bpy.data.collections.new(L_.name + '-blockers'); L_.light_linking.blocker_collection = col_
            for o_ in obs:
                if o_.name not in col_.objects:
                    col_.objects.link(o_)
            for o_, co_ in zip(col_.objects, col_.collection_objects):
                if o_ in obs:
                    co_.light_linking.link_state = 'EXCLUDE'
        cut_obs = [bpy.data.objects[n] for n in cuts]
        for L_ in lamps_:                     # no lamp is cut by a cutter unless named below
            excl(L_, cut_obs)
        if os.environ.get('HOUSE_FACE_UNCUT', '1') == '1':
            # (2026-11-21, the coordinator's audit) the softbox faces are emissive meshes: the cutters blocked the direct
            # (next-event) samples toward them but not the glossy and transmission hits, so their light on rough surfaces
            # differed between the two samplings. No cutter shadows a face; the cutters still shade the floor's lamps
            for fc_ in [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.name.startswith('house-') and o.name.endswith('-face')]:
                excl(fc_, cut_obs)
        for n, names in cuts.items():
            co_ = bpy.data.objects[n]
            if floor_:                        # shadow only: not in reflections, nor through glass, nor soaking bounce
                co_.visible_glossy = co_.visible_transmission = co_.visible_diffuse = co_.visible_volume_scatter = False
            for nm in names:
                L_ = bpy.data.objects.get('house-' + nm)
                if L_ is None:
                    continue
                if not floor_:
                    col_ = L_.light_linking.blocker_collection
                    col_.objects.unlink(co_)
                    continue
                cp = bpy.data.objects.get(L_.name + '-floor')
                if cp is None:
                    cp = L_.copy(); cp.data = L_.data.copy(); cp.name = L_.name + '-floor'
                    bpy.context.scene.collection.objects.link(cp)
                    cp.light_linking.blocker_collection = None
                    Lt.link_receivers(bpy, cp, [sweep])
                    rc_ = bpy.data.collections.new(L_.name + '-not-sweep'); rc_.objects.link(sweep)
                    L_.light_linking.receiver_collection = rc_
                    for c2_ in rc_.collection_objects:
                        c2_.light_linking.link_state = 'EXCLUDE'
                    # (a copy with no blocker collection was not shadowed by its own cutter once others had one:
                    # it always gets one, the sweep, which blocks nothing it lights, as its placeholder)
                    excl(cp, [o_ for o_ in cut_obs if o_ is not co_] or [sweep])
                else:                         # a lamp under two cutters: its copy now meets this one too
                    col_ = cp.light_linking.blocker_collection; col_.objects.unlink(co_)
    if os.environ.get('HOUSE_LAMP_K'):
        # HOUSE_LAMP_K 'wall_left:0.3,bg-left:0.5' (2026-11-21, tests for the Core LIT's left floor): any house lamp's
        # energy times K, by its name after 'house-'
        for it_ in os.environ['HOUSE_LAMP_K'].split(','):
            nm_, k_ = it_.rsplit(':', 1); L_ = bpy.data.objects.get('house-' + nm_)
            if L_ is not None and L_.type == 'LIGHT':
                L_.data.energy *= float(k_); print('LAMPK', L_.name, k_)
    if os.environ.get('HOUSE_FLOORCOPY_K'):
        # HOUSE_FLOORCOPY_K 'fill:0.5,horn:1' (2026-11-21, the critics on the Core LIT: its brightest ground was the floor
        # at the left, lit by the fill's sweep-only copy, brighter than the lamp's own pool): those copies' energy times K
        for it_ in os.environ['HOUSE_FLOORCOPY_K'].split(','):
            nm_, k_ = it_.split(':'); cp_ = bpy.data.objects.get('house-' + nm_ + '-floor')
            if cp_ is not None:
                cp_.data.energy *= float(k_); print('FLOORCOPY', cp_.name, k_)
    if os.environ.get('HOUSE_ROOM', '1') == '1':
        room(bpy, s)
    if os.environ.get('HOUSE_CARD'):
        for i_, c_ in enumerate(os.environ['HOUSE_CARD'].split(';')):      # several cards: 'X,Y,...;X,Y,...'
            card(bpy, [float(v) for v in c_.split(',')], lift, i_)
    if os.environ.get('HOUSE_DOME'):
        # HOUSE_DOME 'STRENGTH' (2026-11-21, a test of the base's fall-off with view angle): every studio lamp off and
        # the sky an even white of that strength, so the product sits in uniform light (the sweep still below it)
        for L_ in [o for o in bpy.context.scene.objects if o.type == 'LIGHT' and o.name.startswith('house-')]:
            L_.data.energy = 0.0
        w_ = bpy.context.scene.world; w_.use_nodes = True; nt_ = w_.node_tree; nt_.nodes.clear()
        bg_ = nt_.nodes.new('ShaderNodeBackground'); bg_.inputs['Color'].default_value = (1, 1, 1, 1)
        bg_.inputs['Strength'].default_value = float(os.environ['HOUSE_DOME'])
        ou_ = nt_.nodes.new('ShaderNodeOutputWorld'); nt_.links.new(bg_.outputs[0], ou_.inputs['Surface'])
    if os.environ.get('HOUSE_FLOORCARD'):
        floor_card(bpy, [float(v) for v in os.environ['HOUSE_FLOORCARD'].split(',')], lift)
    if os.environ.get('HOUSE_KEY_PRODUCT') == '1':
        # (2026-11-21, the Core LIT: the key off lit the floor out, and the base with it) the key lights everything but
        # the ground: the sweep and the floor ring excluded from its receivers, so it lights the lamp and its base alone.
        # Light linking, which a studio cannot do exactly (a flag or snoot only approximates a cut at the base's foot)
        K_ = bpy.data.objects.get('house-key')
        if K_ is not None:
            col_ = K_.light_linking.receiver_collection
            if col_ is None:
                col_ = bpy.data.collections.new('house-key-not-ground'); K_.light_linking.receiver_collection = col_
            for nm_ in ('sweep', 'house-floorcard'):
                o_ = bpy.data.objects.get(nm_)
                if o_ is not None and o_.name not in col_.objects:
                    col_.objects.link(o_)
            for o_, c_ in zip(col_.objects, col_.collection_objects):
                if o_.name in ('sweep', 'house-floorcard'):
                    c_.light_linking.link_state = 'EXCLUDE'
            print('KEY_PRODUCT', [(o_.name, c_.light_linking.link_state) for o_, c_ in zip(col_.objects, col_.collection_objects)])
    cam = json.loads(json.dumps(R['camera']))
    for k in ('position', 'target', 'focus'):
        cam[k] = _mul(cam[k], s); cam[k][2] += lift
    return cam, R, made


def softbox(bpy, ob, s):
    """A solid softbox for an area lamp's reflection (the coordinator, 2026-11-20: the bare area lamps read as flat
    rectangles with razor edges whose overlaps add). The lamp keeps lighting the scene but is no longer seen in
    reflections; in its place a face of the same size and mean radiance, brightest at its middle and falling to about a
    third at its edges (a diffuser's hot centre), in a black housing a little larger: seen only by glossy rays, casting
    no shadow, so a nearer box hides a farther one and the light on the set is unchanged."""
    L = ob.data; w, h = L.size, L.size_y
    rad = L.energy * L.specular_factor / (math.pi * w * h)            # an area lamp's radiance, P / (pi A)
    L.specular_factor = 0.0
    def plane(nm, ww, hh, dz):
        me = bpy.data.meshes.new(nm)
        me.from_pydata([(-ww / 2, -hh / 2, dz), (-ww / 2, hh / 2, dz), (ww / 2, hh / 2, dz), (ww / 2, -hh / 2, dz)], [], [(0, 1, 2, 3)])
        me.uv_layers.new(); o = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(o)
        o.parent = ob; o.matrix_parent_inverse.identity()
        o.visible_camera = o.visible_diffuse = o.visible_shadow = o.visible_volume_scatter = False
        o.visible_glossy = o.visible_transmission = True
        return o
    face = plane(ob.name + '-face', w, h, 0.0)
    m = bpy.data.materials.new(ob.name + '-face'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new('ShaderNodeEmission'); tc = nt.nodes.new('ShaderNodeTexCoord'); sep = nt.nodes.new('ShaderNodeSeparateXYZ')
    nt.links.new(tc.outputs['UV'], sep.inputs[0])
    def fall(ch):               # 1 - 0.65 (2u - 1)^2: 1 at the middle, 0.35 at the edge; its mean 0.783
        a = nt.nodes.new('ShaderNodeMath'); a.operation = 'MULTIPLY_ADD'; a.inputs[1].default_value = 2.0; a.inputs[2].default_value = -1.0
        nt.links.new(sep.outputs[ch], a.inputs[0])
        q = nt.nodes.new('ShaderNodeMath'); q.operation = 'POWER'; q.inputs[1].default_value = 2.0; nt.links.new(a.outputs[0], q.inputs[0])
        f = nt.nodes.new('ShaderNodeMath'); f.operation = 'MULTIPLY_ADD'; f.inputs[1].default_value = -0.65; f.inputs[2].default_value = 1.0
        nt.links.new(q.outputs[0], f.inputs[0]); return f
    fx, fy = fall('X'), fall('Y')
    pr = nt.nodes.new('ShaderNodeMath'); pr.operation = 'MULTIPLY'; nt.links.new(fx.outputs[0], pr.inputs[0]); nt.links.new(fy.outputs[0], pr.inputs[1])
    st = nt.nodes.new('ShaderNodeMath'); st.operation = 'MULTIPLY'; st.inputs[1].default_value = rad / (0.7833 ** 2)
    nt.links.new(pr.outputs[0], st.inputs[0]); nt.links.new(st.outputs[0], em.inputs['Strength'])
    em.inputs['Color'].default_value = (*L.color, 1)
    nt.links.new(em.outputs[0], nt.nodes.new('ShaderNodeOutputMaterial').inputs['Surface'])
    face.data.materials.append(m)
    hous = plane(ob.name + '-housing', w * 1.12, h * 1.12, 0.004 * s / 0.2)        # behind the face (a lamp faces -z)
    hm = bpy.data.materials.new('softbox-housing'); hm.use_nodes = True
    hb = hm.node_tree.nodes['Principled BSDF']; hb.inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1); hb.inputs['Roughness'].default_value = 0.6
    hous.data.materials.append(hm)


def key_flag(bpy, ob, rng, s):
    """A flag on the key (2026-11-20, the coordinator: the pendant's bottom corners darkened as the Tropos's): a black
    card at R m (full scale, times s) from the key, spanning bearings B0 to B1 (degrees from +y toward +x) and depression
    D0 to D1 (degrees below level). rng: [B0, B1, D0, D1, R]. Used as a cutter on the key's floor copy alone (the shade's
    own light and shadow untouched; not in reflections nor through glass)."""
    from mathutils import Vector
    b0, b1, d0, d1, r = rng; r *= s; K = ob.location.copy()
    def pt(b, d):
        b, d = math.radians(b), math.radians(d)
        return K + r * Vector((math.sin(b) * math.cos(d), math.cos(b) * math.cos(d), -math.sin(d)))
    c = [pt(b0, d0), pt(b1, d0), pt(b1, d1), pt(b0, d1)]
    me = bpy.data.meshes.new('house-key-flag'); me.from_pydata([tuple(v) for v in c], [], [(0, 1, 2, 3)])
    o = bpy.data.objects.new('house-key-flag', me); bpy.context.scene.collection.objects.link(o)
    o.visible_camera = os.environ.get('KF_CAM') == '1'; o.visible_shadow = True
    m = bpy.data.materials.new('house-key-flag'); m.use_nodes = True
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1)
    me.materials.append(m)
    return o


def barn_door(bpy, ob, phi, s):
    """A barn door on the key's right side (2026-11-20, the critics: the Tropos ground darkens toward the bottom right,
    84-87, where the lamps' stayed at 96; the key alone lights that corner, its light reaching the floor in front and to
    the right of the product, which the speaker's bulk takes from the Tropos frame). A black card, hinged at the
    softbox's right edge and swung to the plan bearing `phi` (degrees from +y toward +x): the key's rays bound right of
    that are cut, softly (the softbox is wide), and those to the product and its shadow, at about 40 degrees, pass.
    Unseen by the camera and in reflections; it casts shadow only."""
    from mathutils import Vector
    L = ob.data; K = ob.location.copy()               # (matrix_world is not updated until the depsgraph is)
    ax = ob.rotation_euler.to_matrix() @ Vector((0, 0, -1)); a = Vector((ax.x, ax.y, 0)).normalized()
    r = Vector((a.y, -a.x, 0))                                       # the softbox's right, level
    hng = K + r * (L.size / 2 * 1.05)
    u = Vector((math.sin(math.radians(phi)), math.cos(math.radians(phi)), 0))
    ld = 0.5 * s / 0.2; top = K.z + L.size_y; bot = K.z - 3.0 * ld
    c = [hng + Vector((0, 0, bot - K.z)), hng + u * ld + Vector((0, 0, bot - K.z)), hng + u * ld + Vector((0, 0, top - K.z)), hng + Vector((0, 0, top - K.z))]
    me = bpy.data.meshes.new('house-key-door'); me.from_pydata([tuple(v) for v in c], [], [(0, 1, 2, 3)])
    o = bpy.data.objects.new('house-key-door', me); bpy.context.scene.collection.objects.link(o)
    o.visible_camera = o.visible_glossy = o.visible_diffuse = o.visible_transmission = o.visible_volume_scatter = False
    o.visible_shadow = True
    m = bpy.data.materials.new('house-key-door'); m.use_nodes = True
    m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.01, 0.01, 0.01, 1)
    me.materials.append(m)
    return o


def card(bpy, p, lift=0.0, i=0):
    """HOUSE_CARD 'X,Y,Z,W,H,ALB[,TZ]' (2026-11-20, the critics: Core's base went near-black low on its flanks once the
    floor cutters took away the floor's bounce): a white bounce card, as a photographer sets one low beside the product.
    Its centre (X, Y, Z) in metres at the product's own scale (not the set's s), W x H, albedo ALB, turned to face the
    point (0, 0, TZ) (default 0.03 m, the base's middle). It reflects the studio's light like any card, but is not seen
    by the camera or in reflections, and casts no shadow: only the light it bounces reaches the set. It stays visible
    through glass, as the base's white liner sees it through the clear pour."""
    x, y, z, w, h, alb = p[:6]; tz = p[6] if len(p) > 6 else 0.03
    me = bpy.data.meshes.new(f'house-card{i}')
    me.from_pydata([(-w / 2, -h / 2, 0), (w / 2, -h / 2, 0), (w / 2, h / 2, 0), (-w / 2, h / 2, 0)], [], [(0, 1, 2, 3)])
    ob = bpy.data.objects.new(f'house-card{i}', me); bpy.context.scene.collection.objects.link(ob)
    ob.location = (x, y, z + lift)
    d = Vector((0, 0, tz + lift)) - Vector(ob.location)
    ob.rotation_euler = d.to_track_quat('Z', 'Y').to_euler()          # its face (+Z) toward the base
    m = bpy.data.materials.new('house-card'); m.use_nodes = True
    bs = m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value = (alb, alb, alb, 1.0); bs.inputs['Roughness'].default_value = 1.0
    bs.inputs['Specular IOR Level'].default_value = 0.0
    me.materials.append(m)
    ob.visible_camera = ob.visible_glossy = ob.visible_shadow = ob.visible_volume_scatter = False
    return ob


def floor_card(bpy, p, lift=0.0):
    """HOUSE_FLOORCARD 'RIN,ROUT,Z,ALB' (2026-11-20, the critics: the floor cutters darkened the floor round Core's base,
    and with it the base's flanks, which that floor's bounce had lit): the floor next to the base spared for the base
    alone. A flat white ring round the product, RIN to ROUT m from its axis, Z m above the floor, albedo ALB, lit by
    the studio's lamps without the cutters' shade (the cutters shade the sweep's lamps alone). The camera does not see
    it, nor do reflections; it casts no shadow. The floor in frame is unchanged; the base sees a lit floor about it."""
    rin, rout, z, alb = p[:4]; gl = len(p) > 4 and p[4] > 0; n = 96      # (a 5th value 1: seen in reflections too)
    vs = [(r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n), z + lift) for r in (rin, rout) for i in range(n)]
    fs = [(n + i, n + (i + 1) % n, (i + 1) % n, i) for i in range(n)]       # wound so its face (+Z) looks up
    me = bpy.data.meshes.new('house-floorcard'); me.from_pydata(vs, [], fs)
    ob = bpy.data.objects.new('house-floorcard', me); bpy.context.scene.collection.objects.link(ob)
    if alb < 0:
        # ALB -1 (2026-11-21, the coordinator's audit): the sweep's own material (its warm white, roughness and contact
        # darkening), so the base sees the floor as it is, not a brighter neutral card
        # (2026-11-21 03:23, the coordinator) its colour and roughness, NOT its contact term: that painted shadow treats
        # the tinted acrylic as opaque and stacks on the path-traced shadow the ring already receives
        sys.path.insert(0, os.path.abspath(ENGINE)); import materials as M_
        sp_ = recipe()['set']
        m = M_.make(bpy, 'house-floorcard', 'sweep', {'color': sp_.get('color', '#B9B5AE'), 'contact': 0.0, 'core': 0.0})
    else:
        m = bpy.data.materials.new('house-floorcard'); m.use_nodes = True
        bs = m.node_tree.nodes.get('Principled BSDF')
        bs.inputs['Base Color'].default_value = (alb, alb, alb, 1.0); bs.inputs['Roughness'].default_value = 1.0
        bs.inputs['Specular IOR Level'].default_value = 0.0
    # one-sided: its underside is clear, or the floor 1 mm below would see it in place of the room and change tone
    nt = m.node_tree; out = next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output)
    sh_ = out.inputs['Surface'].links[0].from_socket
    gm = nt.nodes.new('ShaderNodeNewGeometry'); tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(gm.outputs['Backfacing'], mx.inputs[0]); nt.links.new(sh_, mx.inputs[1]); nt.links.new(tr.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    me.materials.append(m)
    ob.visible_camera = ob.visible_glossy = ob.visible_shadow = ob.visible_volume_scatter = False
    ob.visible_glossy = gl
    # lit as the floor it stands for: the lamps that light the sweep alone light it too (not the cutters' floor copies:
    # the lamps they copy light it unshaded already)
    for L_ in [o for o in bpy.context.scene.objects if o.type == 'LIGHT' and not o.name.endswith('-floor')]:
        col_ = L_.light_linking.receiver_collection
        if col_ is None or 'sweep' not in [o.name for o in col_.objects]:
            continue
        st_ = dict(zip([o.name for o in col_.objects], [c.light_linking.link_state for c in col_.collection_objects]))
        if st_['sweep'] == 'INCLUDE' and ob.name not in col_.objects:
            col_.objects.link(ob)
            print('FLOORCARD lit by', L_.name)
    return ob


def room(bpy, s):
    """The studio's walls and ceiling, seen only in reflections (the coordinator, 2026-11-20: surfaces facing away from
    the lights read pure black; a satin black part in a white studio is charcoal). White walls left, right and behind the
    sweep's top, a white ceiling, a mid-grey wall behind the camera; lit by the studio's lamps, they light nothing on the
    set (glossy rays only, no shadow), so the ground is as measured. Full-size room 9 x 9 x 5 m, times s."""
    def wall(nm, verts, col):
        me = bpy.data.meshes.new(nm); me.from_pydata([tuple(c * s for c in v) for v in verts], [], [(0, 1, 2, 3)])
        o = bpy.data.objects.new(nm, me); bpy.context.scene.collection.objects.link(o)
        o.visible_camera = o.visible_diffuse = o.visible_shadow = o.visible_volume_scatter = False
        o.visible_glossy = True; o.visible_transmission = os.environ.get('HOUSE_ROOM_TRANS', '0') == '1'   # (1: also seen through glass, 2026-11-21 test)
        m = bpy.data.materials.new(nm); m.use_nodes = True; b = m.node_tree.nodes['Principled BSDF']
        b.inputs['Base Color'].default_value = (col, col, col * 0.97, 1); b.inputs['Roughness'].default_value = 1.0
        b.inputs['Specular IOR Level'].default_value = 0.0
        o.data.materials.append(m)
    X, Yf, Yb, Z = 4.5, -4.5, 4.5, 5.0
    if os.environ.get('HOUSE_ROOM_BIG', '1') == '1':   # (the default since 2026-11-21; 0 the old room)
        # (2026-11-21, the coordinator's audit, a test) the room round the whole sweep (18 m wide, its backdrop at 5.5 m):
        # the sides outside it, the back behind it, the ceiling above it, so a grazing reflection meets the backdrop
        X, Yf, Yb, Z = 9.5, -4.5, 6.0, 6.0
    wall('room-left', [(-X, Yf, 0), (-X, Yb, 0), (-X, Yb, Z), (-X, Yf, Z)], 0.8)
    wall('room-right', [(X, Yf, 0), (X, Yf, Z), (X, Yb, Z), (X, Yb, 0)], 0.8)
    wall('room-back', [(-X, Yb, 0), (X, Yb, 0), (X, Yb, Z), (-X, Yb, Z)], 0.8)
    wall('room-ceiling', [(-X, Yf, Z), (-X, Yb, Z), (X, Yb, Z), (X, Yf, Z)], 0.8)
    wall('room-front', [(-X, Yf, 0), (-X, Yf, Z), (X, Yf, Z), (X, Yf, 0)], 0.25)


def camera(bpy, sc, cam, W, H, lens=None, fstop_equiv=True, s=1.0):
    """The engine's level camera: horizontal sensor fit, looking level, the lens shifted so the target lands where a
    tilted camera would put it (verticals stay vertical). The depth of field as at full size (f-number / s)."""
    cd = bpy.data.cameras.new('cam'); ob = bpy.data.objects.new('cam', cd); sc.collection.objects.link(ob); sc.camera = ob
    cd.sensor_fit = 'HORIZONTAL'; cd.sensor_width = 36.0; cd.lens = lens or cam['lens_mm']; cd.clip_start = 0.005
    C = Vector(cam['position']); T = Vector(cam['target'])
    d = T - C; flat = Vector((d.x, d.y, 0))
    ob.rotation_euler = flat.to_track_quat('-Z', 'Y').to_euler()
    tilt = math.atan2(d.z, flat.length)
    cd.shift_y = math.tan(tilt) * cd.lens / cd.sensor_width * (1.0 if W >= H else W / H)
    ob.location = C
    cd.shift_x += cam.get('shift_x', 0.0); cd.shift_y += cam.get('shift_y', 0.0)
    if cam.get('fstop', 0) > 0:
        cd.dof.use_dof = True; cd.dof.aperture_fstop = cam['fstop'] / (s if fstop_equiv else 1.0)
        F = Vector(cam.get('focus', cam['target']))
        cd.dof.focus_distance = (F - C).dot((T - C).normalized())
    return ob
