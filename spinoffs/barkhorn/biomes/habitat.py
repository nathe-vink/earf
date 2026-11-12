"""Any habitat shot rendered with the linked Tropos asset in place of the engine's model (r48-biomes, 2026-11-03).

    python3.11 spinoffs/barkhorn/biomes/habitat.py SHOT.json TINT --out OUT.png [--samples N] [--scale S]
        [--asset PATH] [--collection 'Tropos Strata {tint}'] [--light NAME=FACTOR ...] [--set KEY=JSON ...]

The owner, 2026-11-03: "All of the images need to be redone" with the latest speaker. The habitats were made through the
studio engine (studio/engine/render.py) with its built-in model; this renders the same shot with the speaker lane's
asset linked in its place, so the model swaps by relinking:
- the engine's own model is still built (the shot's lamps find their parts by name) but hidden from render;
- the asset's tint collection is linked and instanced at each product instance's place and turn;
- each lamp that lights only the product (`receivers`) gets the instance in its light linking.
SHOT is a shot JSON (elements/build.py writes them to studio/shots/barkhorn/element31/). `--set` overrides a shot key
by dotted path, e.g. --set camera.lens_mm=92.
"""
import argparse, json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ASSET = os.path.join(HERE, 'assets', 'hornA3', 'tropos-strata.blend')   # horn A: Strata's cabinet, caldera and bronze posts with the smooth formed horn, satin outside (r33-speaker-horn 0936e6d, the horn uncollapsed, its volumes closed); not in git


def set_path(d, path, value):
    keys = path.split('.')
    for k in keys[:-1]:
        d = d[int(k)] if isinstance(d, list) else d.setdefault(k, {})
    last = keys[-1]
    if isinstance(d, list):
        d[int(last)] = value
    else:
        d[last] = value


def scale_lights(sh, scales):
    for k, f in scales.items():
        if k not in sh.get('lights', {}):
            continue
        if f == 0:
            sh['lights'].pop(k)
            continue
        L = sh['lights'][k]
        for key in ('irradiance', 'power_w', 'energy'):
            if key in L:
                L[key] = L[key] * f


FRESNEL_ANGLE = [False]                 # --fresnel-angle: each face passes 1 - F(theta) (Schlick, n 1.49) of a shadow ray, not a flat sqrt(0.92)
SURFACE_GLASS = False                   # --surface-glass: the tint on the faces (not adopted: the speaker lane's volume is the line's material)
WELD = [True]                           # the asset's split vertices welded so its glass volumes close (--no-weld: off)
GLOSSY_FLAG = [False]                   # --glossy-flag: the flag and cards seen in reflections only (the earlier trick)
SPLIT = [None]                          # --split R G B: the tint's channel split, luminance held per part (the shared 9097 fix)
DOTS = [[]]                             # --dot D SIZE TX TY TZ: a grip's dot, SIZE m, D m out on the sun line from (TX, TY, TZ)
CARDS = [[]]                            # --card white|black W H Z SIDE_DEG: real cards round the speaker, pushed out of frame
MANIFEST = [None]                       # --manifest FILE: the approved build per tint (the speaker lane's), asserted
BERMS = [[]]                            # --berm LX LY RX RY H: sand banked against the base (the speaker's frame)
REFLECTORS = [[]]                       # --reflector W H AZ EL DIST TX TY TZ: a white board where a fill lamp stood
ROLL = [None]                           # --roll-edge FEATHER WANDER: the ground patch's far edge rolled down under the terrain
LAND = [True]                           # scattered tufts landed on the ground and checked against the camera (the coordinator, 2026-11-11)
MENISCUS = [0.0]                        # --meniscus R: a water meniscus round the cabinet's walls, radius R m
WET = [None]                            # --wet F L R SEED: rain beads on the front (F) and horn lip (L), R runnels
SCRIM = [None]                          # --scrim T W H D: a silk on the sun's line D m out, W x H m, passing T of the beam
PLANT_ALPHA = [()]                      # --plant-alpha ID...: wire these Poly Haven plants' own Alpha maps into their cards
CLEARING_AT = [(0.0, 0.0)]              # --canopy-clearing-at X Y: the gap's centre, world m (default over the speaker)
CLEARING = [None]                       # --canopy-clearing D: a treefall gap D m across over the speaker (world 0, 0)
CANOPY_OPEN = [None]                    # --canopy-open F: the canopy's gaps cut as real holes, F of it open (ruling 4)
REAL_SET = [False]                      # --real-set: every set object seen by every ray, casting shadows (ruling 4)
LED = [1.0]                             # --led F: the amp plate's power LED's emission scaled (1: the asset's)
SINK = [0.002]                          # --sink M: the feet bedded this far into the ground (ash, sand). The sets' crust and
                                        # ripples are displaced at render time, so the ray cast sees flat ground and can't seat
                                        # the feet in them: habitats.py beds them a full 12 mm, the cabinet on the ground
HORN = {'close': False, 'rough': None, 'shadows': True, 'as_cabinet': False}  # --horn-close: fill the horn shells' open seams; --horn-rough R: the satin's roughness (test only)
TT_SURFACE = 0.92                       # the two faces' reflection loss, as tints.py has it


def tt_factor(tt_from, tt_to, mm=20.0):
    """How much to scale an acrylic's absorption so `mm` of it passes tt_to instead of tt_from (fractions)."""
    return math.log(TT_SURFACE / tt_to) / math.log(TT_SURFACE / tt_from)


def feet(bpy_, col, r=0.016, h=0.012, inset=0.05):
    """Four rubber feet under the cabinet, where the speaker stands on its own (the stand-in until the speaker lane's
    final model: the owner, 2026-11-03, isn't convinced a base is needed)."""
    import bmesh
    from mathutils import Vector
    lo = [1e9, 1e9]; hi = [-1e9, -1e9]; zb = 1e9
    for o in col.all_objects:
        if o.type == 'MESH' and not o.name.split(' ')[-1].startswith('base-plinth') and o.name.split(' ')[-1] in ('bottom', 'left', 'right', 'front-panel', 'back'):
            for v in o.bound_box:
                w = o.matrix_world @ Vector(v)
                lo = [min(lo[0], w.x), min(lo[1], w.y)]; hi = [max(hi[0], w.x), max(hi[1], w.y)]; zb = min(zb, w.z)
    m = bpy_.data.materials.new('foot-rubber'); m.use_nodes = True
    bs = m.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1)
    bs.inputs['Roughness'].default_value = 0.8
    for x in (lo[0] + inset, hi[0] - inset):
        for y in (lo[1] + inset, hi[1] - inset):
            bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=r, radius2=r, depth=h)
            me = bpy_.data.meshes.new('foot'); bm.to_mesh(me); bm.free(); me.materials.append(m)
            # under the cabinet's own bottom (Strata's is at 12 mm, the feet's height, so they touch it)
            f = bpy_.data.objects.new('foot', me); f.location = (x, y, zb - h / 2); col.objects.link(f)
    print(f'feet: four, {2 * r * 1000:.0f} x {h * 1000:.0f} mm, under the cabinet bottom at z {zb:.4f}')


def uplight(bpy_, col, watts=40.0, color=(1.0, 0.9, 0.8)):
    """The night layer: light shining up through the speaker from inside its bottom (the site's uplit look), never
    down or out onto the floor. A small area lamp facing up, just above the bottom panel."""
    from mathutils import Vector
    zb, lo, hi = 0.0, [1e9, 1e9], [-1e9, -1e9]
    for o in col.all_objects:
        if o.type == 'MESH' and o.name.endswith(' bottom'):
            for v in o.bound_box:
                w = o.matrix_world @ Vector(v)
                zb = max(zb, w.z); lo = [min(lo[0], w.x), min(lo[1], w.y)]; hi = [max(hi[0], w.x), max(hi[1], w.y)]
    L = bpy_.data.lights.new('uplight', 'AREA'); L.shape = 'RECTANGLE'
    L.size = (hi[0] - lo[0]) * 0.6; L.size_y = (hi[1] - lo[1]) * 0.6; L.energy = watts; L.color = color
    o = bpy_.data.objects.new('uplight', L); o.location = ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, zb + 0.004)
    col.objects.link(o)                     # an area lamp shines along its -z: turned over, it faces up
    o.rotation_euler = (math.pi, 0, 0)



OVERHANG_DROP = 0.15   # a tuft's footprint may fall this much per metre of its radius (relief), no more
SETTLE_MODELS = ('rock_', 'moon_rock_', 'coast_rocks_', 'boulder_', 'searsia_', 'island_tree_')


def roll_edge(bpy_, feather, wander, below=0.06, seed=11.0):
    """The ground patch's far (+y) edge rolled over and down under the land beyond, as a brow, not a cut (the
    coordinator, 2026-11-12: Fog's lip read as a ruler-straight 10 cm step where the patch met the terrain). The edge
    wanders in by 0 .. 2 x `wander` metres along its length (noise); over the last `feather` metres before it the patch
    eases down (a rounded brow: slow at first) to `below` under the highest other ground beneath it; past it, it stays
    there, under. The patch is the ground mesh whose far edge is nearest the camera's view (the biggest by area at
    least 5 m across with no particle system), the land beyond every other big surface mesh."""
    from mathutils import Vector, noise
    from mathutils.bvhtree import BVHTree
    sc = bpy_.context.scene; dg = bpy_.context.evaluated_depsgraph_get()
    big = []
    for o in sc.objects:
        if o.type != 'MESH' or o.parent is not None or o.hide_render or o.name.startswith('grass_') or len(o.data.polygons) < 10000:
            continue
        if any(m.type == 'PARTICLE_SYSTEM' for m in o.modifiers):
            continue
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        dx = max(v.x for v in bb) - min(v.x for v in bb); dy = max(v.y for v in bb) - min(v.y for v in bb)
        if dx >= 5.0:
            big.append((dx * dy, o, max(v.y for v in bb)))
    if len(big) < 2:
        print('roll: no patch and land beyond'); return
    big.sort(key=lambda t: t[0])
    patch = big[0][1]                                                 # the smallest: the patch; the rest: the land
    land = []
    for _, o, _ in big[1:]:
        e = o.evaluated_get(dg); m = e.to_mesh(); mw = o.matrix_world
        land.append(BVHTree.FromPolygons([mw @ v.co for v in m.vertices], [q.vertices[:] for q in m.polygons])); e.to_mesh_clear()
    def under(x, y):
        zs = [h[0].z for h in (g.ray_cast(Vector((x, y, 100.0)), Vector((0, 0, -1))) for g in land) if h[0] is not None]
        return max(zs) if zs else None
    mw = patch.matrix_world; mi = mw.inverted(); me = patch.data
    ymax = max((mw @ v.co).y for v in me.vertices)
    n = 0; lo = 0.0
    for v in me.vertices:
        p = mw @ v.co
        edge = ymax - wander * (1.0 + 0.75 * noise.noise(Vector((p.x * 0.9, seed, 0.3))) + 0.25 * noise.noise(Vector((p.x * 3.1, seed, 1.7))))
        t = (p.y - (edge - feather)) / feather
        if t <= 0.0:
            continue
        z = under(p.x, p.y)
        if z is None:
            continue
        t = min(1.0, t); t = t * t * (3 - 2 * t) * t ** 0.5                  # eased: a rounded brow, then down
        q = Vector((p.x, p.y, p.z + (min(p.z, z - below) - p.z) * t))
        v.co = mi @ q; n += 1; lo = min(lo, q.z - p.z)
    me.update()
    print(f'roll: {patch.name} far edge (y {ymax:.2f}) rolled under the land over {feather} m, wandering in by up to '
          f'{2 * wander:.2f} m; {n} vertices moved, down to {lo:+.3f} m')


def land_scatter(bpy_, sink=0.01, edge=0.18, drop=0.04):
    """Every scattered tuft (Poly Haven grass_*, the kit's scatter stands them all at one flat z) stood on the real
    ground under it: the highest of the big surface meshes (the ground patch, the terrain) by a ray down, bedded `sink`.
    A tuft goes if no ground is under it, if the ground falls away by more than `drop` within `edge` of it (a brow or
    the patch's edge: it would hang over the void), or if its base is in frame but hidden from the camera behind the
    ground (its blades would show with no ground under them). The coordinator, 2026-11-11: Fog's tufts floated."""
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    import bpy_extras.object_utils as ou
    sc = bpy_.context.scene; dg = bpy_.context.evaluated_depsgraph_get()
    tufts = [o for o in sc.objects if o.parent is None and not o.hide_render and o.name.startswith('grass_')]
    G = []
    for o in sc.objects:
        if o.type != 'MESH' or o.parent is not None or o.hide_render or o.name.startswith('grass_') or len(o.data.polygons) < 10000:
            continue
        ms = [s_.material for s_ in o.material_slots if s_.material and s_.material.node_tree]
        if not any((n.type == 'OUTPUT_MATERIAL' and n.inputs['Surface'].is_linked) for m in ms for n in m.node_tree.nodes):
            continue
        bb = [o.matrix_world @ Vector(c) for c in o.bound_box]
        if max(v.x for v in bb) - min(v.x for v in bb) < 5.0:
            continue                                                  # a rock, not the ground
        e = o.evaluated_get(dg); m = e.to_mesh(); mw = o.matrix_world
        G.append((o.name, BVHTree.FromPolygons([mw @ v.co for v in m.vertices], [q.vertices[:] for q in m.polygons])))
        e.to_mesh_clear()

    def down(x, y):
        zs = [h[0].z for h in (g.ray_cast(Vector((x, y, 100.0)), Vector((0, 0, -1))) for _, g in G) if h[0] is not None]
        return max(zs) if zs else None
    def footprint(o):
        # 0.75 of the half-width of the tuft's blades (the outer blade tips are thin and lean)
        pts = [q.matrix_world @ Vector(c) for q in [o, *o.children_recursive] if q.type == 'MESH' for c in q.bound_box]
        if not pts:
            return 0.0
        return 0.75 * 0.5 * max(max(p_.x for p_ in pts) - min(p_.x for p_ in pts), max(p_.y for p_ in pts) - min(p_.y for p_ in pts))
    cam = sc.camera
    cp = cam.matrix_world.translation if cam else None
    gone = {'no ground': 0, 'edge': 0, 'overhang': 0, 'base hidden': 0}; moved = []
    for o in tufts:
        x, y = o.location.x, o.location.y
        z = down(x, y)
        if z is None:
            why = 'no ground'
        else:
            ring = [down(x + dx * edge, y + dy * edge) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7))]
            why = 'edge' if any(r is None or r < z - drop for r in ring) else None
            if why is None:
                # the blades' footprint, not only the root: a wide tuft near a brow hangs its blades over the void
                # (Fog's lip row, 2026-11-12: rooted 25 cm short of the brow, its blades reached 0.9 m out over the fog)
                r_ = footprint(o)
                if r_ > edge:
                    ring = [down(x + dx * r_, y + dy * r_) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7))]
                    why = 'overhang' if any(r is None or r < z - max(drop, OVERHANG_DROP * r_) for r in ring) else None
            if why is None and cam:
                b = Vector((x, y, z)); c = ou.world_to_camera_view(sc, cam, b)
                if -0.05 <= c.x <= 1.05 and -0.05 <= c.y <= 1.05 and c.z > 0:
                    d = b - cp; L = d.length; d.normalize()
                    if any((h[0] is not None and h[3] < L - 0.03) for h in (g.ray_cast(cp, d, L) for _, g in G)):
                        why = 'base hidden'
        if why:
            gone[why] += 1
            for q in [o, *o.children_recursive]:
                q.hide_render = True; q.hide_viewport = True
            continue
        moved.append(o.location.z - (z - sink)); o.location.z = z - sink
    # scanned rocks and shrubs set at a flat z (Acid's and Ember's lava blocks, Haze's far shrubs): a piece whose lowest
    # point is above the HIGHEST ground under its footprint is lowered onto it, bedded `sink`; never raised
    settled = []
    for o in sc.objects:
        if o.parent is not None or o.hide_render or not o.name.startswith(SETTLE_MODELS):
            continue
        obs = [q for q in [o, *o.children_recursive] if q.type == 'MESH' and not q.hide_render]
        if not obs:
            continue
        pts = [q.matrix_world @ Vector(c) for q in obs for c in q.bound_box]
        x0, x1 = min(p_.x for p_ in pts), max(p_.x for p_ in pts); y0, y1 = min(p_.y for p_ in pts), max(p_.y for p_ in pts)
        zs = [down(x0 + (x1 - x0) * i / 4, y0 + (y1 - y0) * j / 4) for i in range(5) for j in range(5)]
        zs = [z for z in zs if z is not None]
        if not zs:
            continue
        gap = min(p_.z for p_ in pts) - max(zs)
        if gap > 0.0:
            o.location.z -= gap + sink; settled.append(gap)
    if settled:
        print(f'land: {len(settled)} rocks/shrubs lowered onto the ground by up to {max(settled):.3f} m')
    if not tufts:
        return
    moved.sort()
    print(f'land: {len(tufts)} tufts on {[n for n, _ in G]}; removed {gone}; the rest moved by '
          f'{moved[0]:+.3f} .. {moved[-1]:+.3f} m (median {moved[len(moved) // 2]:+.3f})' if moved else f'land: removed {gone}')

def settle(bpy_, linked, sink=0.002):
    """Stand each speaker on the ground under it: a ray down through each of its feet (the asset's lowest points) onto
    the set, and the instance raised or lowered so the lowest foot touches the highest hit, sunk `sink` m."""
    from mathutils import Vector
    dg = bpy_.context.evaluated_depsgraph_get()
    sc = bpy_.context.scene
    for e in linked:
        col = e.instance_collection
        pts = []
        for o in col.all_objects:
            if o.type != 'MESH':
                continue
            for v in o.bound_box:
                w = o.matrix_world @ Vector(v)
                pts.append(w)
        if not pts:
            continue
        zmin = min(p.z for p in pts)
        feet_ = [p for p in pts if p.z < zmin + 0.01]
        xs = [p.x for p in feet_]; ys = [p.y for p in feet_]
        corners = [(min(xs), min(ys)), (min(xs), max(ys)), (max(xs), min(ys)), (max(xs), max(ys)), (sum(xs) / len(xs), sum(ys) / len(ys))]
        # the speaker itself, the hidden engine copy and the volumes out of the rays' way while they look for ground
        hide = [o for o in sc.objects if o.hide_render or o.get('volume') or o in linked]
        was = [(o, o.hide_viewport) for o in hide]
        for o in hide:
            o.hide_viewport = True
        dg = bpy_.context.evaluated_depsgraph_get(); dg.update()
        hits = []
        for cx, cy in corners:
            wp = e.matrix_world @ Vector((cx, cy, 0.0))
            ok, loc, nrm, idx, obj, mat = sc.ray_cast(dg, Vector((wp.x, wp.y, wp.z + 3.0)), Vector((0, 0, -1)), distance=6.0)
            if ok:
                hits.append(loc.z)
        for o, v in was:
            o.hide_viewport = v
        if hits:
            z_new = max(hits) - zmin - sink
            print(f'ground: {e.name} feet on the set at z {max(hits):.4f} (from {e.location.z:.4f} to {z_new:.4f}; hits {[round(h, 4) for h in hits]})')
            e.location.z = z_new


def black_flag(bpy_, linked, size):
    """A photographer's negative fill: a large black card behind and above the camera, out of frame, so the speaker's
    front faces mirror black instead of the bright sky. A real object (every ray type) since 2026-11-03 20:11;
    --glossy-flag keeps the earlier reflection-only card."""
    import bmesh
    from mathutils import Vector
    sc = bpy_.context.scene
    cam = sc.camera
    if not linked or cam is None:
        return
    t = linked[0].location
    c = cam.location
    d = (c - Vector((t.x, t.y, c.z))).normalized()
    pos = c + d * 1.2 + Vector((0, 0, 1.4))
    w, h = size
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    me = bpy_.data.meshes.new('black-flag'); bm.to_mesh(me); bm.free()
    m = bpy_.data.materials.new('black-flag'); m.use_nodes = True
    bs = m.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (0.0, 0.0, 0.0, 1)
    bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
    me.materials.append(m)
    f = bpy_.data.objects.new('black-flag', me); sc.collection.objects.link(f)
    f.location = pos; f.scale = (w, h, 1.0)
    f.rotation_euler = (Vector((t.x, t.y, t.z + 0.7)) - pos).to_track_quat('Z', 'Y').to_euler()
    if GLOSSY_FLAG[0]:
        # (until 2026-11-03 20:11) seen only in reflections: hidden from the camera, diffuse, shadow and transmission
        f.visible_camera = False; f.visible_diffuse = False; f.visible_shadow = False
        f.visible_transmission = False; f.visible_volume_scatter = False
    # otherwise real objects, every ray type, as a real set's flag and cards (the coordinator, 20:11): out of frame,
    # they block a little sky and cast shade like the real thing
    print(f'black flag: {w} x {h} m at {[round(v, 2) for v in pos]}')
    # and a card each side of the speaker, square to the camera's line, out of frame: the side walls mirror them, not
    # the sky, at the grazing angles where acrylic reflects most
    side = Vector((-d.y, d.x, 0.0))
    # real cards are seen by the camera, so each is pushed out sideways until no corner falls in the frame (Blender's own
    # projection, lens shift included; the first real-card Fog final had them in frame at the old fixed 1.8 m)
    from bpy_extras.object_utils import world_to_camera_view
    bpy_.context.view_layer.update()
    offs = []
    # a real card on the low sun's side stands between the sun and the set and throws a long shadow across the frame (the
    # Haze A/B: the field in front went dark), as no photographer would place one: that card is left out
    sun_dir = None
    for o in sc.objects:
        if o.type == 'LIGHT' and o.data.type == 'SUN' and not o.hide_render:
            z = o.matrix_world.to_3x3() @ Vector((0, 0, 1))          # toward the sun
            if z.z < 0.5 and not GLOSSY_FLAG[0]:
                sun_dir = Vector((z.x, z.y, 0.0)).normalized()
    for k, sgn in enumerate((1, -1)):
        if sun_dir is not None and (side * sgn).dot(sun_dir) > 0.2:
            offs.append('left out (sun side)')
            continue
        c_ = f.copy(); c_.data = me; sc.collection.objects.link(c_)
        c_.scale = (2.6, 2.4, 1.0)
        off = 1.8
        for _ in range(60):
            p_ = Vector((t.x, t.y, 0.9)) + side * sgn * off - d * 0.6
            c_.location = p_
            c_.rotation_euler = (Vector((t.x, t.y, 0.7)) - p_).to_track_quat('Z', 'Y').to_euler()
            bpy_.context.view_layer.update()
            corners = [c_.matrix_world @ Vector((x, y, 0.0)) for x in (-0.5, 0.5) for y in (-0.5, 0.5)]
            uv = [world_to_camera_view(sc, cam, q) for q in corners]
            xs = [q.x for q in uv]
            # the whole card beside the frame: left of its left edge, or right of its right edge (corners alone could
            # sit above and below a frame the card's middle crosses)
            inside = not (max(xs) < -0.02 or min(xs) > 1.02) and any(q.z > 0 for q in uv)
            if not inside or GLOSSY_FLAG[0]:
                break
            off += 0.2
        offs.append(round(off, 1))
    print(f'side cards: 2.6 x 2.4 m, out of frame at {offs} m each side')


def canopy_holes(bpy_, open_frac, spec, cell=0.3):
    """Ruling 4: the canopy's gaps as real holes in its geometry, not a transparency. The sheet is rebuilt as a grid of
    `cell` m squares; a fractal noise at the shot's gap size picks the open ones (exactly `open_frac` of them), and every
    cell inside one of the shot's explicit holes (placed so the sun reaches a spot) is cut too. The material is opaque."""
    import bmesh
    from mathutils import noise, Vector
    can = None
    for o in bpy_.context.scene.objects:
        if o.type == 'MESH' and max(o.dimensions[:2]) > 100 and o.location.z > 8 and o.data.materials and o.data.materials[0].node_tree \
                and any(n.type == 'BSDF_TRANSPARENT' for n in o.data.materials[0].node_tree.nodes):
            can = o
    if can is None or not spec:
        print('canopy holes: no canopy found'); return
    w, d = spec.get('size', [60.0, 60.0]); gap = spec.get('gap', 2.0)
    nx, ny = int(w / cell), int(d / cell)
    vals = []
    for j in range(ny):
        for i in range(nx):
            x = -w / 2 + (i + 0.5) * cell; y = -d / 2 + (j + 0.5) * cell
            vals.append(noise.fractal(Vector((x / gap, y / gap, 0.0)), 0.6, 2.0, 6))
    thr = sorted(vals)[int(len(vals) * (1.0 - open_frac))]
    holes = spec.get('holes', [])
    keep = spec.get('keep', [])   # canopy-local [x, y, r]: cells never cut (leaves left in a gap, a real shadow)
    # a treefall gap over the speaker: world (0, 0) is canopy-local (-px, -py); its rim broken by the shot's own gap
    # fractal (+-rim m), no soft edge (cells cut or kept)
    clr = None
    if CLEARING[0]:
        px, py = spec.get('position', [0.0, 0.0, 0.0])[:2]; cx, cy = CLEARING_AT[0]
        clr = (cx - px, cy - py, CLEARING[0] / 2, spec.get('clearing_rim', 1.5))
    bm = bmesh.new(); open_n = 0
    vs = [[bm.verts.new((-w / 2 + i * cell, -d / 2 + j * cell, 0.0)) for i in range(nx + 1)] for j in range(ny + 1)]
    for j in range(ny):
        for i in range(nx):
            x = -w / 2 + (i + 0.5) * cell; y = -d / 2 + (j + 0.5) * cell
            in_clr = clr and math.hypot(x - clr[0], y - clr[1]) <= clr[2] + clr[3] * noise.fractal(Vector((x / gap + 50.0, y / gap, 0.0)), 0.6, 2.0, 4)
            if any((x - kx) ** 2 + (y - ky) ** 2 <= kr * kr for kx, ky, kr in keep):
                bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i])); continue   # a leafy cluster left
            if in_clr or vals[j * nx + i] >= thr or any((x - hx) ** 2 + (y - hy) ** 2 <= hr * hr for hx, hy, hr in holes):
                open_n += 1; continue
            bm.faces.new((vs[j][i], vs[j][i + 1], vs[j + 1][i + 1], vs[j + 1][i]))
    me = bpy_.data.meshes.new(can.name + '-holed'); bm.to_mesh(me); bm.free()
    m = can.data.materials[0]; nt = m.node_tree
    mix = next(n for n in nt.nodes if n.type == 'MIX_SHADER')
    for l in list(mix.inputs['Fac'].links):
        nt.links.remove(l)
    mix.inputs['Fac'].default_value = 0.0                # all diffuse: opaque leaves, the light only through the holes
    me.materials.append(m); can.data = me
    print(f'canopy holes: {nx} x {ny} cells of {cell} m, {open_n / (nx * ny):.1%} open ({len(holes)} explicit holes cut)'
          + (f', a clearing {2 * clr[2]:.0f} m across at canopy-local ({clr[0]:.1f}, {clr[1]:.1f}), rim +-{clr[3]} m' if clr else ''))


def out_of_frame(pts):
    """True when a flat quad, its corners projected by world_to_camera_view, is wholly outside the frame: every corner
    behind the camera or past the same edge (a corner test alone passes a card wider than the view that crosses it)."""
    if all(p.z <= 0 for p in pts):
        return True
    # sideways only: when the set is built the camera's final framing (lens shift, resolution) is not yet applied, so
    # a vertical test lies (a strip under the lens tested out and rendered across the base, 2026-11-09)
    return all(p.x < 0 for p in pts) or all(p.x > 1 for p in pts)


def dots(bpy_, specs):
    """A grip's dot: a small black card on the sun's line D m from a target point, square to the beam, casting a sharp
    shadow on just that point (a woofer cone in full sun). Real: every ray type; out of frame is checked sideways."""
    import bmesh
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy_.context.scene; cam = sc.camera
    sun = next((o for o in sc.objects if o.type == 'LIGHT' and o.data.type == 'SUN' and not o.hide_render), None)
    if sun is None:
        return
    z = (sun.matrix_world.to_3x3() @ Vector((0, 0, 1))).normalized()
    for i, (d, size, tx, ty, tz) in enumerate(specs):
        bm = bmesh.new(); bmesh.ops.create_circle(bm, cap_ends=True, segments=24, radius=0.5)
        me = bpy_.data.meshes.new(f'dot-{i}'); bm.to_mesh(me); bm.free()
        m = bpy_.data.materials.new(f'dot-{i}'); m.use_nodes = True
        bs = m.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (0.02, 0.02, 0.02, 1)
        bs.inputs['Roughness'].default_value = 1.0; me.materials.append(m)
        f = bpy_.data.objects.new(f'dot-{i}', me); sc.collection.objects.link(f)
        f.location = Vector((tx, ty, tz)) + z * d; f.scale = (size, size, 1.0); f.rotation_euler = z.to_track_quat('Z', 'Y').to_euler()
        bpy_.context.view_layer.update()
        pts = [world_to_camera_view(sc, cam, f.matrix_world @ Vector(c)) for c in ((-.5, -.5, 0), (.5, -.5, 0), (.5, .5, 0), (-.5, .5, 0))]
        print(f'dot: {size} m, {d} m out on the sun line from {(tx, ty, tz)}, at {[round(c, 2) for c in f.location]}, out of frame: {out_of_frame(pts)}')


def cards(bpy_, linked, specs):
    """Real cards a grip would set: each W x H m, its centre Z m up, on the ground plan SIDE_DEG off the line from the
    speaker to the camera (0: between them, under the lens; +90: camera-right), square to the speaker's middle, pushed
    out along that bearing until it is out of frame. 'white' is a bounce (diffuse, albedo 0.85), 'warm' a gold-sand
    reflector (0.78, 0.62, 0.45), 'black' a negative (albedo 0.02). Every ray type, casting shadow."""
    import bmesh, math
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy_.context.scene; cam = sc.camera
    if cam is None or not linked:
        return
    t = linked[0].location; mid = Vector((t.x, t.y, t.z + 0.6))
    base = Vector((cam.location.x - t.x, cam.location.y - t.y, 0.0)).normalized()
    for i, (kind, w, h, z, side) in enumerate(specs):
        a = math.radians(side)
        dirn = Vector((base.x * math.cos(a) - base.y * math.sin(a), base.x * math.sin(a) + base.y * math.cos(a), 0.0))
        bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
        me = bpy_.data.meshes.new(f'card-{kind}-{i}'); bm.to_mesh(me); bm.free()
        m = bpy_.data.materials.new(f'card-{kind}-{i}'); m.use_nodes = True
        bs = m.node_tree.nodes['Principled BSDF']
        col = {'white': (0.85, 0.85, 0.85), 'black': (0.02, 0.02, 0.02), 'warm': (0.78, 0.62, 0.45)}[kind]   # warm: a gold-sand reflector
        bs.inputs['Base Color'].default_value = (*col, 1); bs.inputs['Roughness'].default_value = 1.0
        bs.inputs['Specular IOR Level'].default_value = 0.0
        me.materials.append(m)
        f = bpy_.data.objects.new(f'card-{kind}-{i}', me); sc.collection.objects.link(f); f.scale = (w, h, 1.0)
        for k in range(60):
            f.location = Vector((t.x, t.y, z)) + dirn * (0.8 + 0.2 * k)
            f.rotation_euler = (mid - f.location).to_track_quat('Z', 'Y').to_euler()
            bpy_.context.view_layer.update()
            pts = [world_to_camera_view(sc, cam, f.matrix_world @ Vector(c)) for c in ((-.5, -.5, 0), (.5, -.5, 0), (.5, .5, 0), (-.5, .5, 0))]
            if out_of_frame(pts):
                break
        else:
            print(f'card: {kind} could not be set out of frame on this bearing'); f.hide_render = True
        print(f'card: {kind} {w} x {h} m, centre {z} m up, {side} deg off the camera line, at {[round(c, 2) for c in f.location]}')


def scrim(bpy_, linked, spec):
    """A photographer's silk: a real cloth on the sun's line between the sun and the speaker, square to the beam,
    `t` of the direct light passing straight through (the open weave) and the rest scattered on through the cloth
    (translucent), so the speaker's direct sun drops by about log2(1/t) stops and the sky fill is unchanged. Every ray
    type, casting shadow; pushed out along the beam until no corner falls in the frame."""
    import bmesh
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    t, w, h, d = spec
    sc = bpy_.context.scene; cam = sc.camera
    sun = next((o for o in sc.objects if o.type == 'LIGHT' and o.data.type == 'SUN' and not o.hide_render), None)
    if sun is None or cam is None or not linked:
        print('scrim: no sun'); return
    z = (sun.matrix_world.to_3x3() @ Vector((0, 0, 1))).normalized()       # toward the sun
    c0 = Vector((linked[0].location.x, linked[0].location.y, linked[0].location.z + 0.7))
    bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
    me = bpy_.data.meshes.new('scrim'); bm.to_mesh(me); bm.free()
    m = bpy_.data.materials.new('scrim'); m.use_nodes = True; nt = m.node_tree
    for n in list(nt.nodes):
        if n.type != 'OUTPUT_MATERIAL': nt.nodes.remove(n)
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); tl = nt.nodes.new('ShaderNodeBsdfTranslucent')
    tl.inputs['Color'].default_value = (0.9, 0.9, 0.9, 1)
    mx = nt.nodes.new('ShaderNodeMixShader'); mx.inputs['Fac'].default_value = 1.0 - t
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(tl.outputs[0], mx.inputs[2])
    nt.links.new(mx.outputs[0], next(n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL').inputs['Surface'])
    me.materials.append(m)
    f = bpy_.data.objects.new('scrim', me); sc.collection.objects.link(f)
    f.scale = (w, h, 1.0); f.rotation_euler = z.to_track_quat('Z', 'Y').to_euler()
    for k in range(40):
        f.location = c0 + z * (d + 0.25 * k)
        bpy_.context.view_layer.update()
        pts = [world_to_camera_view(sc, cam, f.matrix_world @ Vector(v)) for v in ((-.5, -.5, 0), (.5, -.5, 0), (.5, .5, 0), (-.5, .5, 0))]
        if out_of_frame(pts):
            break
    else:
        print('scrim: could not be set out of frame'); f.hide_render = True
    print(f'scrim: {w} x {h} m passing {t} of the beam, {round((f.location - c0).length, 2)} m out on the sun line at {[round(v, 2) for v in f.location]}')


def wet(bpy_, linked, spec):
    """Rain on the speaker: water beads on the cabinet's front and on the horn's lip, and runnels down the front, each
    a low dome of clear water (IOR 1.33) sitting on the surface, seen by every ray type. spec: [front beads, lip beads,
    runnels, seed]. The surface is found by ray casts against the placed speaker (its rotation from the instance)."""
    import bmesh
    import random
    from mathutils import Vector, Matrix
    sc = bpy_.context.scene
    n_front, n_lip, n_run, seed = int(spec[0]), int(spec[1]), int(spec[2]), int(spec[3])
    # optional: the drops' radius range, mm (default 1.2-4.7 on the front), and the runnels' length range, m
    rlo, rhi = (spec[4] / 1000, spec[5] / 1000) if len(spec) > 5 else (0.0012, 0.0047)
    llo, lhi = (spec[6], spec[7]) if len(spec) > 7 else (0.12, 0.3)
    low = 1.6 if len(spec) <= 8 else spec[8]                    # >1: more drops low on the front
    rnd = random.Random(seed)
    dg = bpy_.context.evaluated_depsgraph_get()
    e = linked[0]
    R = e.matrix_world.to_3x3().normalized(); P = e.matrix_world.translation
    fwd = (R @ Vector((0, -1, 0))).normalized()                    # the speaker's front faces -y before its turn
    side = (R @ Vector((1, 0, 0))).normalized()

    def part(ob):
        return ob.name.split(' ')[-1].split('#')[0] if ob else ''   # welded parts are named 'front-panel#0'

    def hit(o, d, want):
        ok, loc, nrm, _i, ob, _m = sc.ray_cast(dg, o, d)
        if not ok or not want(part(ob)):
            return None
        if nrm.dot(d) > 0:
            nrm = -nrm
        return loc, nrm.normalized()
    bm = bmesh.new()

    def dome(loc, nrm, r, flat=0.38, stretch=1.0, down=None):
        """A drop on the surface: half an ellipsoid, r across (stretch along `down`), flat x r high, its rim 0.05 mm
        under the surface so no air shows under it."""
        g = bmesh.ops.create_uvsphere(bm, u_segments=12, v_segments=6, radius=1.0)
        vs = g['verts']
        kill = [v for v in vs if v.co.z < -1e-4]
        t = (down - nrm * down.dot(nrm)).normalized() if down is not None else nrm.orthogonal().normalized()
        b = nrm.cross(t)
        M = Matrix((t * r * stretch, b * r, nrm * r * flat)).transposed()
        for v in vs:
            v.co = loc + M @ v.co - nrm * 0.00005
        bmesh.ops.delete(bm, geom=kill, context='VERTS')
    def cap(loc, nrm, r, theta_deg=70.0, stretch=1.0, down=None):
        """A drop as water really sits on PMMA: a spherical cap meeting the surface at its contact angle (about 70 deg,
        height (1 - cos t) / sin t of its contact radius, about 0.7 r), r its contact radius (stretched along `down`),
        its rim 0.05 mm under the surface."""
        th = math.radians(theta_deg); R = 1.0 / math.sin(th)
        t = (down - nrm * down.dot(nrm)).normalized() if down is not None else nrm.orthogonal().normalized()
        b = nrm.cross(t)
        M = Matrix((t * r * stretch, b * r, nrm * r)).transposed()
        top = bm.verts.new(loc + M @ Vector((0, 0, R - R * math.cos(th))) - nrm * 0.00005)
        rings = []
        for k in range(1, 6):
            ph = th * k / 5
            rings.append([bm.verts.new(loc + M @ Vector((R * math.sin(ph) * math.cos(2 * math.pi * j / 14),
                                                        R * math.sin(ph) * math.sin(2 * math.pi * j / 14),
                                                        R * math.cos(ph) - R * math.cos(th))) - nrm * 0.00005)
                          for j in range(14)])
        for j in range(14):
            bm.faces.new((top, rings[0][j], rings[0][(j + 1) % 14]))
        for r0, r1 in zip(rings, rings[1:]):
            for j in range(14):
                bm.faces.new((r0[j], r1[j], r1[(j + 1) % 14], r0[(j + 1) % 14]))
    CAP = len(spec) > 9 and spec[9] > 0                           # spec[9]: the contact angle, deg (0: the old dome)
    front = lambda n: n in ('front-panel',)
    hornp = lambda n: n.startswith('horn') or 'waveguide' in n
    nf = nl = 0
    for _ in range(n_front * 20):
        if nf >= n_front:
            break
        # over the front, more drops low (the splash-back) and toward the edges
        u, v = rnd.uniform(-0.3, 0.3), rnd.uniform(0.02, 1.0) ** low * 1.0
        o = P + side * u + Vector((0, 0, 0.05 + v)) + fwd * 1.0
        h = hit(o, -fwd, front)
        if h is None:
            continue
        r = rlo + rnd.random() ** 3 * (rhi - rlo)                   # most near the small end, a few large
        if CAP:
            cap(h[0], h[1], r, spec[9], stretch=1.0 + rnd.uniform(0.0, 0.35), down=Vector((0, 0, -1)))
        else:
            dome(h[0], h[1], r, stretch=1.0 + rnd.uniform(0.0, 0.35), down=Vector((0, 0, -1)))
        nf += 1
    for _ in range(n_lip * 40):
        if nl >= n_lip:
            break
        # the horn's lip from above and in front: drops collect on its upper faces
        o = P + side * rnd.uniform(-0.32, 0.32) + fwd * rnd.uniform(-0.3, 0.35) + Vector((0, 0, 2.5))
        h = hit(o, Vector((0, 0, -1)), hornp)
        if h is None or h[1].z < 0.25:
            continue
        r = 0.001 + rnd.random() ** 3 * 0.003
        if CAP:
            cap(h[0], h[1], r, spec[9])
        else:
            dome(h[0], h[1], r, flat=0.45)
        nl += 1
    nr = 0
    for k in range(n_run * 30):
        if nr >= n_run:
            break
        # a runnel: from a drop high on the front straight down the face, a thin water line ending in a fat bead
        o = P + side * rnd.uniform(-0.22, 0.22) + Vector((0, 0, rnd.uniform(0.75, 1.0))) + fwd * 1.0
        h = hit(o, -fwd, front)
        if h is None:
            continue
        loc, nrm = h
        L = rnd.uniform(llo, lhi); step = 0.0012; w = rnd.uniform(0.0007, 0.001) * max(1.0, rlo / 0.0012) ** 0.5
        pts = []
        p = loc.copy(); wob = 0.0
        while (loc - p).length < L:
            pts.append((p.copy(), nrm))
            wob += rnd.uniform(-0.15, 0.15); wob *= 0.9
            dn = Vector((0, 0, -1)); dn = (dn - nrm * dn.dot(nrm)).normalized()
            tn = nrm.cross(dn)
            q = p + (dn + tn * wob * 0.15).normalized() * step
            h2 = hit(q + nrm * 0.01, -nrm, front)
            if h2 is None:
                break
            p, nrm = h2
        if len(pts) < 20:
            continue
        for i, (q, n) in enumerate(pts):
            dome(q, n, w * (1.0 + 0.25 * math.sin(i * 0.37)), flat=0.5, stretch=1.6, down=Vector((0, 0, -1)))
        if CAP:
            cap(pts[-1][0], pts[-1][1], rnd.uniform(0.0025, 0.0035) * max(1.0, rlo / 0.0025), spec[9], stretch=1.25, down=Vector((0, 0, -1)))
        else:
            dome(pts[-1][0], pts[-1][1], rnd.uniform(0.0025, 0.0035), flat=0.5, stretch=1.25, down=Vector((0, 0, -1)))
        nr += 1
    me = bpy_.data.meshes.new('wet'); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
    m = bpy_.data.materials.new('wet-water'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); gl = nt.nodes.new('ShaderNodeBsdfGlass')
    gl.inputs['IOR'].default_value = 1.333; gl.inputs['Roughness'].default_value = 0.0
    nt.links.new(gl.outputs[0], out.inputs['Surface']); me.materials.append(m)
    ob = bpy_.data.objects.new('wet', me); sc.collection.objects.link(ob)
    print(f'wet: {nf} beads on the front, {nl} on the horn, {nr} runnels ({len(me.polygons)} faces)')


def meniscus(bpy_, linked, r):
    """A water meniscus where the cabinet stands in the puddle: a thin tube of water, radius r, around the four walls
    at the water's own height (found by casting down beside each wall), half in the water, against the wall."""
    import bmesh
    from mathutils import Vector
    sc = bpy_.context.scene; dg = bpy_.context.evaluated_depsgraph_get()
    e = linked[0]; M = e.matrix_world
    pts = []
    for o in e.instance_collection.all_objects:
        if o.type == 'MESH' and o.name.split(' ')[-1].split('#')[0] in ('front-panel', 'back', 'left', 'right', 'bottom'):
            pts += [o.matrix_world @ Vector(c) for c in o.bound_box]
    if not pts:
        return
    lo = Vector([min(p[i] for p in pts) for i in range(3)]); hi = Vector([max(p[i] for p in pts) for i in range(3)])
    corners = [Vector((x, y, 0)) for x, y in ((lo.x, lo.y), (hi.x, lo.y), (hi.x, hi.y), (lo.x, hi.y))]
    out_dirs = [Vector((0, -1, 0)), Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((-1, 0, 0))]
    bm = bmesh.new(); made = 0
    for k in range(4):
        a, b = M @ corners[k], M @ corners[(k + 1) % 4]
        a.z = b.z = 0.0
        out = (M.to_3x3().normalized() @ out_dirs[k]).normalized()
        n = max(2, int((b - a).length / 0.004))
        ring = []
        for i in range(n + 1):
            q = a + (b - a) * (i / n) + out * (r * 0.6)
            # the first broad, flat surface down beside the wall: the water or the ground (past rain streaks, the horn)
            o_, zc = Vector((q.x, q.y, 2.0)), 0.0
            for _t in range(50):
                ok, loc, _n, _i, hob, _m = sc.ray_cast(dg, o_, Vector((0, 0, -1)))
                if not ok:
                    break
                if hob.dimensions.z < 1.0 and min(hob.dimensions.x, hob.dimensions.y) > 5.0:
                    zc = loc.z
                    break
                o_ = loc - Vector((0, 0, 1e-4))
            c = Vector((q.x, q.y, zc)); t = (b - a).normalized(); u = out.cross(t)
            ring.append([bm.verts.new(c + (out * math.cos(2 * math.pi * j / 8) + Vector((0, 0, 1)) * math.sin(2 * math.pi * j / 8)) * r)
                         for j in range(8)])
        for r0, r1 in zip(ring, ring[1:]):
            for j in range(8):
                bm.faces.new((r0[j], r0[(j + 1) % 8], r1[(j + 1) % 8], r1[j]))
        made += n
    me = bpy_.data.meshes.new('meniscus'); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
    m = bpy_.data.materials.new('meniscus-water'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o_ = nt.nodes.new('ShaderNodeOutputMaterial'); gl = nt.nodes.new('ShaderNodeBsdfGlass')
    gl.inputs['IOR'].default_value = 1.333; gl.inputs['Roughness'].default_value = 0.0
    nt.links.new(gl.outputs[0], o_.inputs['Surface']); me.materials.append(m)
    ob = bpy_.data.objects.new('meniscus', me); sc.collection.objects.link(ob)
    print(f'meniscus: r {r * 1000:.1f} mm, {made} segments around the cabinet')


def schlick_face(nt, tp, n):
    """A glass face's share of a shadow ray by its incidence: 1 - F, F = R0 + (1 - R0)(1 - |cos|)^5, R0 = ((n-1)/(n+1))^2.
    The same on entry and exit (|cos|): a shadow ray goes straight, so it leaves a parallel wall at the angle it came
    in, and the exit is never a total internal reflection as it would be for that angle measured inside."""
    r0 = ((n - 1) / (n + 1)) ** 2
    geo = nt.nodes.new('ShaderNodeNewGeometry')
    dot = nt.nodes.new('ShaderNodeVectorMath'); dot.operation = 'DOT_PRODUCT'
    nt.links.new(geo.outputs['Incoming'], dot.inputs[0]); nt.links.new(geo.outputs['True Normal'], dot.inputs[1])
    ab = nt.nodes.new('ShaderNodeMath'); ab.operation = 'ABSOLUTE'; nt.links.new(dot.outputs['Value'], ab.inputs[0])
    om = nt.nodes.new('ShaderNodeMath'); om.operation = 'SUBTRACT'; om.inputs[0].default_value = 1.0; om.use_clamp = True
    nt.links.new(ab.outputs[0], om.inputs[1])
    pw = nt.nodes.new('ShaderNodeMath'); pw.operation = 'POWER'; pw.inputs[1].default_value = 5.0
    nt.links.new(om.outputs[0], pw.inputs[0])
    # T = 1 - R0 - (1 - R0) x^5
    mu = nt.nodes.new('ShaderNodeMath'); mu.operation = 'MULTIPLY_ADD'
    nt.links.new(pw.outputs[0], mu.inputs[0]); mu.inputs[1].default_value = -(1 - r0); mu.inputs[2].default_value = 1 - r0
    nt.links.new(mu.outputs[0], tp.inputs['Color'])


def reflectors(bpy_, specs):
    """A grip's white reflector board where a fill lamp stood (the coordinator, 2026-11-09 23:48: the only emitters are
    the sun and the sky; a passive board out of frame is honest): W x H m, at the lamp's orbit (azimuth, lights' convention
    0 = -y, 90 = +x; elevation; distance) about its target, square to the target. Diffuse white (albedo 0.85), every ray
    type, casting shadow, lit only by the sun and sky. Its frame position is printed (the camera's own projection)."""
    import bmesh
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view
    sc = bpy_.context.scene; cam = sc.camera
    for i, (w, h, az, el, dist, tx, ty, tz) in enumerate(specs):
        bm = bmesh.new(); bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
        me = bpy_.data.meshes.new(f'reflector-{i}'); bm.to_mesh(me); bm.free()
        m = bpy_.data.materials.new(f'reflector-{i}'); m.use_nodes = True
        bs = m.node_tree.nodes['Principled BSDF']; bs.inputs['Base Color'].default_value = (0.85, 0.85, 0.85, 1)
        bs.inputs['Roughness'].default_value = 1.0; bs.inputs['Specular IOR Level'].default_value = 0.0
        me.materials.append(m)
        f = bpy_.data.objects.new(f'reflector-{i}', me); sc.collection.objects.link(f); f.scale = (w, h, 1.0)
        a, e = math.radians(az), math.radians(el)
        T = Vector((tx, ty, tz))
        f.location = T + Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e))) * dist
        f.rotation_euler = (T - f.location).to_track_quat('Z', 'Y').to_euler()
        bpy_.context.view_layer.update()
        pts = [world_to_camera_view(sc, cam, f.matrix_world @ Vector(c)) for c in ((-.5, -.5, 0), (.5, -.5, 0), (.5, .5, 0), (-.5, .5, 0))]
        print(f'reflector: {w} x {h} m at {[round(c, 2) for c in f.location]} (az {az}, el {el}, {dist} m), frame x '
              f'{[round(p.x, 2) for p in pts]}, out of frame sideways: {out_of_frame(pts)}')


def berms(bpy_, linked, specs):
    """Sand banked against the base (the coordinator, 2026-11-10 00:05: the sun got under the back-left of Dust's base
    through a ripple trough): a low mound in the ground's own material, centred LX LY in the speaker's frame (x right,
    y back, m), RX x RY across, H high at its crest (a cosine falloff), its foot 3 cm under the ground found below it.
    Every ray type, casting shadow."""
    import bmesh
    from mathutils import Vector
    sc = bpy_.context.scene; dg = bpy_.context.evaluated_depsgraph_get()
    M = linked[0].matrix_world
    own = {o.name for o in linked[0].instance_collection.all_objects} if linked[0].instance_collection else set()
    for i, (lx, ly, rx, ry, h) in enumerate(specs):
        c = M @ Vector((lx, ly, 0.0))
        # the ground under it: the first broad, flat object down from above (past the speaker's own parts)
        o_, zg, gob = Vector((c.x + rx * 1.3, c.y, 3.0)), None, None
        for _t in range(60):
            ok, loc, _n, _i, hob, _m = sc.ray_cast(dg, o_, Vector((0, 0, -1)))
            if not ok:
                break
            if hob.name not in own and _n.z > 0.5 and min(hob.dimensions.x, hob.dimensions.y) > 3.0:
                zg, gob = loc.z, hob
                break
            o_ = loc - Vector((0, 0, 1e-4))
        if gob is None:
            print('berm: no ground found'); continue
        bm = bmesh.new(); N = 24
        R = M.to_3x3().normalized()
        grid = []
        for a in range(N + 1):
            row = []
            for b in range(N + 1):
                u, v = -1 + 2 * a / N, -1 + 2 * b / N
                d = min(1.0, math.hypot(u, v))
                z = (h + 0.03) * 0.5 * (1 + math.cos(math.pi * d)) - 0.03
                row.append(bm.verts.new(Vector((c.x, c.y, zg)) + R @ Vector((u * rx, v * ry, 0.0)) + Vector((0, 0, z))))
            grid.append(row)
        for a in range(N):
            for b in range(N):
                bm.faces.new((grid[a][b], grid[a + 1][b], grid[a + 1][b + 1], grid[a][b + 1]))
        me = bpy_.data.meshes.new(f'berm-{i}'); bm.to_mesh(me); bm.free()
        for f in me.polygons:
            f.use_smooth = True
        for sl in gob.material_slots:
            if sl.material:
                me.materials.append(sl.material); break
        # in the ground's own object space, so a material that maps its texture by Object coordinates lines up across the
        # seam (the vertices were placed in world space: carried into the ground's frame)
        Gi = gob.matrix_world.inverted()
        for v in me.vertices:
            v.co = Gi @ v.co
        ob = bpy_.data.objects.new(f'berm-{i}', me); sc.collection.objects.link(ob); ob.matrix_world = gob.matrix_world.copy()
        if gob.data.uv_layers:
            # UV-mapped grounds: each berm vertex takes the ground's UV straight below it (a ray cast's face, nearest corner)
            uvl = me.uv_layers.new(name=gob.data.uv_layers.active.name)
            gm = gob.data; guv = gm.uv_layers.active.data
            for poly in me.polygons:
                for li in poly.loop_indices:
                    w = ob.matrix_world @ me.vertices[me.loops[li].vertex_index].co
                    ok, loc, _n, fi = gob.ray_cast(Gi @ Vector((w.x, w.y, 5.0)), Gi.to_3x3() @ Vector((0, 0, -1)))
                    if ok:
                        gp = gm.polygons[fi]
                        best = min(gp.loop_indices, key=lambda k: (gm.vertices[gm.loops[k].vertex_index].co - loc).length)
                        uvl.data[li].uv = guv[best].uv
        print(f'berm: {rx * 2:.2f} x {ry * 2:.2f} m, {h * 1000:.0f} mm high at {[round(x, 3) for x in c]} on {gob.name} (z {zg:.3f})')


def assert_approved(col, tint, manifest):
    """The speaker as the approved build (the coordinator, 2026-11-11: as rollout.py's site('front-off-tall', tint)):
    the prepared collection checked against the speaker lane's manifest (r33-speaker-horn 0f54ebee,
    tropos-strata.manifest.json): every part there with its materials, and every material's Principled values (base
    colour where it is a value, roughness, metallic, transmission, IOR, emission) and its volume's colour and density.
    The glass-shadow mix this builder adds sits in front of the Principled and leaves those values alone. Fails the render
    on any mismatch."""
    spec = manifest.get(tint)
    if spec is None:
        raise SystemExit(f'approved build: no manifest entry for {tint}')
    have = {}
    for o in col.all_objects:
        have[o.name.split(' ')[-1].split('#')[0]] = o
    bad = []
    keys = ('Base Color', 'Roughness', 'Metallic', 'Transmission Weight', 'IOR', 'Emission Strength')

    def check(m, mname, want):
        """One material against the manifest's entry for it (its name in this scene may carry a .00n suffix: the
        engine's hidden copy of the product already holds the plain names)."""
        if not m.node_tree:
            return
        b = next((n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        for k in keys:
            w = want.get(k)
            if w is None or b is None or b.inputs[k].is_linked:
                continue
            g = b.inputs[k].default_value
            g = list(g)[:3] if hasattr(g, '__len__') else [g]
            w = w if isinstance(w, list) else [w]
            if any(abs(x - y) > 1e-3 for x, y in zip(g, w)):
                bad.append(f'{mname} {k} {[round(x, 4) for x in g]} != {w}')
        if 'volume Density' in want:
            v = next((n for n in m.node_tree.nodes if n.type in ('VOLUME_ABSORPTION', 'PRINCIPLED_VOLUME') and n.outputs[0].is_linked), None)
            if v is None:
                bad.append(f'{mname} has no volume')
            else:
                gd = v.inputs['Density'].default_value; gc = list(v.inputs['Color'].default_value)[:3]
                if abs(gd - want['volume Density']) > 1e-3 * max(1.0, want['volume Density']) or \
                        any(abs(x - y) > 1e-3 for x, y in zip(gc, want.get('volume Color', gc))):
                    bad.append(f'{mname} volume {[round(x, 4) for x in gc]} x {gd:.3f} != {want.get("volume Color")} x {want["volume Density"]}')
    seen = set()
    for part, mnames in spec['parts'].items():
        o = have.get(part)
        if o is None:
            bad.append(f'part {part} missing'); continue
        slots = [sl.material for sl in getattr(o, 'material_slots', []) if sl.material]
        if len(slots) != len(mnames):
            bad.append(f'{part}: {len(slots)} materials, the manifest {len(mnames)}'); continue
        for m, mname in zip(slots, mnames):
            if (m.name, mname) in seen:
                continue
            seen.add((m.name, mname))
            if mname in spec['materials']:
                check(m, mname, spec['materials'][mname])
    if bad:
        raise SystemExit(f'approved build: {tint} FAILS ({len(bad)}): ' + '; '.join(bad[:12]))
    print(f'approved build: {tint} matches the manifest ({len(spec["parts"])} parts, {len(spec["materials"])} materials)')

def plant_alpha(bpy_, aids, res='1k'):
    """Some Poly Haven plant glTFs (grass_bermuda_01) carry no alpha at all: the cards render whole, their black,
    semi-glossy surround mirroring the sky as pale flecks (the Fog gate: "litter"). Wire the asset's own Alpha map
    (fetched once) into every material of that name, in the base colour's coordinates. The asset's own cut-out, as
    published, not a paint-over."""
    import assets as As
    for aid in aids:
        f = As.files(aid).get('Alpha', {})
        r = As._pick_res(f.keys(), res) if f else None
        e = (f[r].get('png') or f[r].get('jpg')) if r else None
        if not e:
            print('plant alpha: none published for', aid); continue
        path = os.path.join(As.CACHE, 'models', f'{aid}_{r}', 'textures', os.path.basename(e['url']))
        if not os.path.exists(path):
            As._get(e['url'], path)
        img = bpy_.data.images.load(path, check_existing=True); img.colorspace_settings.name = 'Non-Color'
        done = []
        for m in bpy_.data.materials:
            if not (m.name.split('.')[0] == aid and m.node_tree):
                continue
            nt = m.node_tree
            bs = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
            if bs is None or bs.inputs['Alpha'].is_linked:
                continue
            src = next((l.from_node for l in bs.inputs['Base Color'].links if l.from_node.type == 'TEX_IMAGE'), None)
            if src is None:
                continue
            a = nt.nodes.new('ShaderNodeTexImage'); a.image = img; a.interpolation = src.interpolation; a.extension = src.extension
            for i in src.inputs:
                for ll in i.links:
                    nt.links.new(ll.from_socket, a.inputs[i.name])
            nt.links.new(a.outputs['Color'], bs.inputs['Alpha']); done.append(m.name)
        print(f'plant alpha: {aid} {r} wired into {len(done)} materials')


def run(shot_path, collection, out, samples, scale, asset=ASSET, root=ROOT, extra=(), stand='feet', tt=None,
        up=0.0, glass_from=0.12, ground=True, flag=(8.0, 6.0), lining=None, glass_shadows=True):
    """Render a prepared shot file through `root`'s engine with the asset in. stand 'feet' leaves the stand-in plinth
    out and stands the speaker on four feet; 'plinth' keeps the asset as it is (linked). tt: the cabinet's and horn's
    transmission through 20 mm to render at, from `glass_from` (Smoke's 2074 is 0.12); up: the night uplight (W)."""
    os.chdir(root)
    sys.path.insert(0, os.path.join(root, 'studio', 'engine'))
    import bpy  # noqa: F401  (mathutils comes with it)
    import render, product as Pr, lights as Lt
    linked = []
    place0 = Pr.place
    editable = (stand == 'feet' or tt or up or lining or glass_shadows or HORN['close'] or HORN['as_cabinet'] or HORN['rough'] is not None
                or not HORN['shadows'] or LED[0] != 1.0 or SPLIT[0] or REAL_SET[0])   # else the asset as it is, linked

    def place(bpy_, pdef, templates, shot_, root_):
        objs, part_of = place0(bpy_, pdef, templates, shot_, root_)
        for o in objs:
            o.hide_render = True
        def prep(collection):
            """Load one tint's collection from the asset and prepare it (the feet, the weld, the glass and horn rules)."""
            with bpy_.data.libraries.load(asset, link=not editable) as (s_, d_):
                d_.collections = [collection]
            col = d_.collections[0]
            if col is None:
                raise SystemExit(f'{collection} is not in {asset}')
            if stand == 'feet':
                drop = []
                for o in list(col.all_objects):
                    if 'base-plinth' in o.name or 'base-uplight' in o.name:   # base A and its light: the base is open
                        col.objects.unlink(o); drop.append(o)
                feet(bpy_, col)
                print('stand: on four feet; left out', [o.name for o in drop])
            if tt:
                f = tt_factor(glass_from, tt)
                done = set()
                for o in col.all_objects:
                    for sl in getattr(o, 'material_slots', []):
                        m = sl.material
                        if not m or m.name in done or not m.name.split('@')[0] in ('bark', 'horn-lot') or not m.node_tree:
                            continue
                        done.add(m.name)
                        for n in m.node_tree.nodes:
                            if n.type in ('VOLUME_ABSORPTION', 'PRINCIPLED_VOLUME') and 'Density' in n.inputs:
                                n.inputs['Density'].default_value *= f
                print(f'glass: {glass_from:.0%} -> {tt:.0%} through 20 mm (absorption x {f:.3f}) on', sorted(done))
            if WELD[0]:
                # the asset's panels arrive from glTF with their vertices split at every seam, which leaves each glass
                # volume open (the speaker lane, 2026-11-03: welded, every panel closes, normals out); weld them
                import bmesh
                seen = set(); nw = 0
                for o in col.all_objects:
                    if o.type != 'MESH' or o.data.name in seen:
                        continue
                    seen.add(o.data.name)
                    bm = bmesh.new(); bm.from_mesh(o.data)
                    n0 = len(bm.verts)
                    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
                    if len(bm.verts) < n0:
                        nw += 1
                        bm.to_mesh(o.data)
                        flat = any(sl.material and sl.material.name.split('@')[0] == 'bark' for sl in o.material_slots)
                        o.data.polygons.foreach_set('use_smooth', [not flat] * len(o.data.polygons))
                    bm.free()
                print(f'weld: {nw} meshes welded')
            if HORN['close']:
                # the horn's shells (throat, waveguide, cap) stay open after the weld (seams 0.6-1.1 m long): a glass volume
                # with a gap leaks, rays inside stay "in the resin". Fill each hole so the volume closes
                import bmesh
                for o in col.all_objects:
                    if o.type == 'MESH' and any(k in o.name for k in ('horn-throat', 'waveguide')):
                        bm = bmesh.new(); bm.from_mesh(o.data)
                        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)
                        r = bmesh.ops.holes_fill(bm, edges=bm.edges, sides=0)
                        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
                        left = sum(1 for e in bm.edges if len(e.link_faces) == 1)
                        bm.to_mesh(o.data); bm.free()
                        print('horn close:', o.name, len(r['faces']), 'faces filled,', left, 'open edges left')
            if HORN['rough'] is not None:
                for m in {sl.material for o in col.all_objects for sl in getattr(o, 'material_slots', []) if sl.material}:
                    if m.name.split('@')[0] == 'horn-satin' and m.node_tree:
                        for n in m.node_tree.nodes:
                            if n.type == 'BSDF_PRINCIPLED':
                                n.inputs['Roughness'].default_value = HORN['rough']
                print('horn satin roughness ->', HORN['rough'])
            if HORN['as_cabinet']:
                # the horn as the cabinet's glass (the coordinator, 2026-11-10 01:37): the asset's horns carry their own, denser
                # volume absorption (Dust 9-51x the cabinet's per mm, Poison 3-5x); each horn material takes its cabinet's
                # Volume Absorption colour and density exactly (same IOR 1.49 already, no coat or sheen); its own wall
                # thickness then sets how much it tints
                allm = {sl.material for o in col.all_objects for sl in getattr(o, 'material_slots', []) if sl.material}
                def absn(m):
                    return next((n for n in m.node_tree.nodes if n.type == 'VOLUME_ABSORPTION' and n.outputs[0].is_linked), None) if m.node_tree else None
                bark = next((m for m in allm if m.name.split('@')[0] == 'bark' and absn(m)), None)
                if bark is not None:
                    vb = absn(bark); done = []
                    for m in allm:
                        if m.name.split('@')[0].startswith('horn-') and absn(m):
                            vh = absn(m)
                            vh.inputs['Color'].default_value = tuple(vb.inputs['Color'].default_value)
                            vh.inputs['Density'].default_value = vb.inputs['Density'].default_value
                            done.append(m.name)
                    print('horn as the cabinet glass (absorption from', bark.name + '):', sorted(done))
            if SPLIT[0]:
                # a tint's channel split changed in the speaker lane's shared model (9097, 732a8671): each acrylic part keeps
                # its luminous transmission through its own thickness (cabinet 20 mm, horn 12.7 mm), the absorption re-split
                import math as _m
                LUMW = (0.2126, 0.7152, 0.0722); sp = SPLIT[0]; mx = max(sp); done = {}
                for o in col.all_objects:
                    for sl in getattr(o, 'material_slots', []):
                        m = sl.material
                        base = m.name.split('@')[0] if m else ''
                        if not m or not m.node_tree or m.name in done or base not in ('bark', 'horn-formed', 'horn-satin', 'horn-lot'):
                            continue
                        absn = next((n for n in m.node_tree.nodes if n.type == 'VOLUME_ABSORPTION'), None)
                        if absn is None:
                            continue
                        t = 0.020 if base == 'bark' else 0.0127
                        c = absn.inputs['Color'].default_value; D = absn.inputs['Density'].default_value
                        L0 = sum(w * _m.exp(-(1 - c[i]) * D * t) for i, w in enumerate(LUMW))
                        lo, hi = 0.0, 5000.0
                        for _ in range(100):
                            k = (lo + hi) / 2
                            L = sum(w * _m.exp(-k * (sp[i] / mx) * t) for i, w in enumerate(LUMW))
                            lo, hi = (k, hi) if L > L0 else (lo, k)
                        absn.inputs['Color'].default_value = (*[1 - sp[i] / mx for i in range(3)], 1)
                        absn.inputs['Density'].default_value = k
                        done[m.name] = (round(L0, 4), round(k, 1))
                print('split', sp, '(luminance held):', done)
            if LED[0] != 1.0:
                for m in {sl.material for o in col.all_objects for sl in getattr(o, 'material_slots', []) if sl.material}:
                    if m.name.split('@')[0] == 'led-on' and m.node_tree:
                        for n in m.node_tree.nodes:
                            if n.type == 'EMISSION':
                                n.inputs['Strength'].default_value *= LED[0]
                print('led-on emission x', LED[0])
            if not HORN['shadows']:
                # the horn lit from the front (the coordinator, 2026-11-03, Ember): the asset's shadow rays pass the horn
                # untinted, so a lamp or bright sky behind a backlit satin horn makes it a lampshade, out-shining the
                # backdrop, the driver and posts as silhouettes. Direct light stops at the horn; its paths still refract
                done = set()
                for o in col.all_objects:
                    for sl in getattr(o, 'material_slots', []):
                        m = sl.material
                        if not m or not m.node_tree or not m.name.split('@')[0].startswith('horn-') or m.name in done:
                            continue
                        nt = m.node_tree
                        out = next((n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output), None)
                        bs = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                        if out is not None and bs is not None:
                            for l in list(out.inputs['Surface'].links):
                                nt.links.remove(l)
                            nt.links.new(bs.outputs[0], out.inputs['Surface'])
                            done.add(m.name)
                print('horn: direct light stops at it (no shadow transparency):', sorted(done))
            if glass_shadows:
                # light through the glass: Cycles renders without refractive caustics, so no lamp lights anything inside or
                # behind a clear wall and the inside reads black whatever the tint. Shadow rays pass each acrylic wall
                # tinted by what that wall transmits (its absorption over its thickness), the rest of the shading untouched
                done = {}
                for o in col.all_objects:
                    for sl in getattr(o, 'material_slots', []):
                        m = sl.material
                        base = m.name.split('@')[0] if m else ''
                        if not m or not m.node_tree or base not in ('bark', 'horn-formed', 'horn-satin', 'horn-lot') or m.name in done:
                            continue
                        if base.startswith('horn-') and not HORN['shadows']:
                            continue
                        nt = m.node_tree
                        out = next((n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output), None)
                        absn = next((n for n in nt.nodes if n.type == 'VOLUME_ABSORPTION'), None)
                        if out is None or absn is None or not out.inputs['Surface'].links:
                            continue
                        mm = 0.020 if base == 'bark' else 0.0127
                        c = absn.inputs['Color'].default_value; dens = absn.inputs['Density'].default_value
                        # a caustics stand-in: shadow rays pass the wall tinted by what it transmits, less its two faces'
                        # Fresnel loss (about 4 % each at IOR 1.49, x 0.92; without it clear glass cast no shadow at all)
                        tr = [0.92 * math.exp(-(1 - c[i]) * dens * mm) for i in range(3)]
                        if SURFACE_GLASS:
                            # the tint on the faces instead of in a volume: the asset's panels don't close the volume
                            # (rays inside the cabinet stay "in the glass" and the inside reads black whatever the
                            # tint); each face takes the square root of its wall's transmission, two faces a wall
                            for l in list(out.inputs['Volume'].links):
                                nt.links.remove(l)
                            bs = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
                            if bs is not None:
                                bs.inputs['Base Color'].default_value = (*[math.sqrt(x) for x in tr], 1)
                        src = out.inputs['Surface'].links[0].from_socket
                        lp = nt.nodes.new('ShaderNodeLightPath'); tp = nt.nodes.new('ShaderNodeBsdfTransparent')
                        # per FACE, not per wall: a shadow ray meets the transparency at each face it crosses (two a wall), and
                        # through the welded volume Cycles applies the absorption itself. So with the volume the faces carry only
                        # the Fresnel, sqrt(0.92) each; the tint comes once, from the volume (the slab test, 2026-11-09: tr at
                        # each face plus the volume passed tr^2 x volume, the tint three times). Without a volume (SURFACE_GLASS)
                        # each face carries sqrt of the whole wall's transmission
                        face = [math.sqrt(x) for x in tr] if SURFACE_GLASS else [math.sqrt(0.92)] * 3
                        tp.inputs['Color'].default_value = (*face, 1)
                        if FRESNEL_ANGLE[0] and not SURFACE_GLASS:
                            schlick_face(nt, tp, 1.49)
                        mx = nt.nodes.new('ShaderNodeMixShader')
                        nt.links.new(lp.outputs['Is Shadow Ray'], mx.inputs[0])
                        nt.links.new(src, mx.inputs[1]); nt.links.new(tp.outputs[0], mx.inputs[2])
                        nt.links.new(mx.outputs[0], out.inputs['Surface'])
                        done[m.name] = [round(x, 3) for x in tr]
                print('glass shadows:', done)
            if lining:
                # the lining's color (colors F: Smoke on black, the others white): the asset, appended, takes it
                h = lining.lstrip('#'); rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
                rgb = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
                done = set()
                for o in col.all_objects:
                    for sl in getattr(o, 'material_slots', []):
                        m = sl.material
                        if m and m.name.split('@')[0] == 'lining' and m.name not in done and m.node_tree:
                            done.add(m.name)
                            for n in m.node_tree.nodes:
                                if n.type == 'BSDF_PRINCIPLED':
                                    n.inputs['Base Color'].default_value = (*rgb, 1)
                print('lining:', lining, sorted(done))
            if up:
                uplight(bpy_, col, up)
            return col

        cols = {}
        for inst in shot_['product']['instances']:
            # an instance may name its own tint (the hero: eight colours in one scene); each tint's collection prepared once
            cname = f"Tropos Strata {inst['tint']}" if inst.get('tint') else collection
            if cname not in cols:
                cols[cname] = prep(cname)
                if MANIFEST[0] is not None:
                    assert_approved(cols[cname], cname.split(' ')[-1], MANIFEST[0])
            col = cols[cname]
            e = bpy_.data.objects.new(cname, None)
            e.instance_type = 'COLLECTION'; e.instance_collection = col
            e.location = inst.get('position', (0, 0, 0)); e.rotation_euler = (0, 0, math.radians(inst.get('rotate_z', 0)))
            bpy_.context.scene.collection.objects.link(e)
            linked.append(e)
        return objs, part_of
    Pr.place = place
    link0 = Lt.link_receivers

    def link_receivers(bpy_, light_ob, objects):
        link0(bpy_, light_ob, objects)
        col = light_ob.light_linking.receiver_collection
        for e in linked:
            if e.name not in col.objects:
                col.objects.link(e)
    Lt.link_receivers = link_receivers
    world0 = Lt.world

    def world(bpy_, sky, sun_spec=None):
        r = world0(bpy_, sky, sun_spec)
        if ground:
            settle(bpy_, linked, SINK[0])
        if flag:
            black_flag(bpy_, linked, flag)
        if REAL_SET[0]:
            # ruling 4 (the coordinator, 2026-11-03 23:47): every part of a set casts shadows, and is seen by every ray
            # type as the real thing would be (Poison's canopy was a shadow-only sheet, its mist shadowless); light
            # reaches the subject only through the set's real openings
            fixed = []
            for o in bpy_.context.scene.objects:
                if o.type != 'MESH' or o in linked or o.hide_render or o.name.startswith(('foot', 'black-flag')):
                    continue
                vis = ('visible_camera', 'visible_diffuse', 'visible_glossy', 'visible_transmission',
                       'visible_volume_scatter', 'visible_shadow')
                if not all(getattr(o, a) for a in vis):
                    if o.name.split('.')[0] in ('camera',) or o.get('engine_light'):
                        continue
                    for a in vis:
                        setattr(o, a, True)
                    fixed.append(o.name)
            print('real set: every ray type on for', fixed)
        if ROLL[0]:
            roll_edge(bpy_, *ROLL[0])
        if LAND[0]:
            land_scatter(bpy_)
        if CARDS[0]:
            cards(bpy_, linked, CARDS[0])
        if DOTS[0]:
            dots(bpy_, DOTS[0])
        if SCRIM[0]:
            scrim(bpy_, linked, SCRIM[0])
        if WET[0]:
            wet(bpy_, linked, WET[0])
        if REFLECTORS[0]:
            reflectors(bpy_, REFLECTORS[0])
        if BERMS[0]:
            berms(bpy_, linked, BERMS[0])
        if MENISCUS[0]:
            meniscus(bpy_, linked, MENISCUS[0])
        if PLANT_ALPHA[0]:
            plant_alpha(bpy_, PLANT_ALPHA[0])
        if CANOPY_OPEN[0] is not None:
            cs = next((q for q in json.load(open(shot_path))['set']['props'] if q.get('fn') == 'canopy'), None)
            canopy_holes(bpy_, CANOPY_OPEN[0], cs)
        return r
    Lt.world = world
    sys.argv = ['render.py', shot_path, '--out', os.path.abspath(out), '--samples', str(samples), '--scale', str(scale), *extra]
    render.main()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('shot'); ap.add_argument('tint')
    ap.add_argument('--out', required=True); ap.add_argument('--samples', type=int, default=64)
    ap.add_argument('--scale', type=float, default=1.0)
    ap.add_argument('--asset', default=ASSET)
    ap.add_argument('--collection', default='Tropos Strata {tint}')
    ap.add_argument('--light', action='append', default=[])
    ap.add_argument('--set', action='append', default=[], dest='sets')
    ap.add_argument('--stand', choices=['own', 'feet', 'plinth'], default='own')
    ap.add_argument('--tt', type=float, help="the glass's transmission through 20 mm to render at (e.g. 0.29)")
    ap.add_argument('--glass-from', type=float, default=0.12, help="the asset's own (Smoke 2074: 0.12)")
    ap.add_argument('--uplight', type=float, default=0.0, help='the night uplight, W (0: off, the day)')
    ap.add_argument('--no-ground', action='store_true', help="don't settle the speaker onto the set")
    ap.add_argument('--no-weld', action='store_true'); ap.add_argument('--surface-glass', action='store_true')
    ap.add_argument('--lining', help="the lining's color, hex (colors F: Smoke '#0B0B0B')")
    ap.add_argument('--glossy-flag', action='store_true', help='the flag and side cards in reflections only (before 20:11)')
    ap.add_argument('--split', type=float, nargs=3, help="the tint's channel split, R G B (luminance held per part)")
    ap.add_argument('--canopy-open', type=float, help="the canopy's gaps cut as real holes, this fraction open")
    ap.add_argument('--dot', type=float, nargs=5, action='append', default=[], metavar=('D', 'SIZE', 'TX', 'TY', 'TZ'),
                    help="a grip's dot: SIZE m, D m out on the sun line from the point TX TY TZ")
    ap.add_argument('--card', nargs=5, action='append', default=[], metavar=('KIND', 'W', 'H', 'Z', 'SIDE'),
                    help='a real card: white|black, W H (m), centre Z (m), SIDE_DEG off the speaker-camera line')
    ap.add_argument('--manifest', help="the approved build's per-tint manifest (JSON), asserted on every instance")
    ap.add_argument('--berm', type=float, nargs=5, action='append', default=[], metavar=('LX', 'LY', 'RX', 'RY', 'H'))
    ap.add_argument('--reflector', type=float, nargs=8, action='append', default=[], metavar=('W', 'H', 'AZ', 'EL', 'DIST', 'TX', 'TY', 'TZ'))
    ap.add_argument('--opaque-shadows', action='store_true', help='the glass blocks direct light (diagnostics only)')
    ap.add_argument('--crop', type=float, nargs=4, help='render a region only, fractions X0 Y0 X1 Y1 from the top left (tests)')
    ap.add_argument('--fresnel-angle', action='store_true', help="glass faces pass a shadow ray's 1 - F(theta) (Schlick, n 1.49)")
    ap.add_argument('--roll-edge', type=float, nargs=2, default=None, metavar=('FEATHER', 'WANDER'))
    ap.add_argument('--no-land', action='store_true', help='leave scattered tufts at the kit\'s flat z (old renders)')
    ap.add_argument('--meniscus', type=float, default=0.0, help='a water meniscus round the walls, radius m')
    ap.add_argument('--wet', type=float, nargs='+', help='rain on the speaker: front beads, lip beads, runnels, seed [r_min r_max mm [run_min run_max m [low]]]')
    ap.add_argument('--scrim', type=float, nargs=4, help='a silk on the sun line: T (beam passed) W H (m) D (m out)')
    ap.add_argument('--plant-alpha', nargs='+', default=[], help="Poly Haven plants whose own Alpha map is wired in (their glTF has none)")
    ap.add_argument('--canopy-clearing-at', type=float, nargs=2, default=(0.0, 0.0), help="the gap's centre, world X Y (m)")
    ap.add_argument('--canopy-clearing', type=float, help='with --canopy-open: a treefall gap this many m across over the speaker')
    ap.add_argument('--real-set', action='store_true', help='every set object seen by every ray, casting shadows')
    ap.add_argument('--led', type=float, default=1.0, help="scale the amp's power LED (the asset's strength is 6)")
    ap.add_argument('--sink', type=float, default=0.002, help='bed the feet this far into the ground, m')
    ap.add_argument('--horn-front', action='store_true', help='direct light stops at the horn (no lampshade from behind)')
    ap.add_argument('--horn-as-cabinet', action='store_true', help="the horn's absorption per mm = the cabinet's")
    ap.add_argument('--horn-close', action='store_true'); ap.add_argument('--horn-rough', type=float)
    ap.add_argument('--flag', type=float, nargs=2, default=(8.0, 6.0), help='the black flag behind the camera, m (0 0: none)')
    a = ap.parse_args()
    global SURFACE_GLASS
    WELD[0] = not a.no_weld; SURFACE_GLASS = a.surface_glass; FRESNEL_ANGLE[0] = a.fresnel_angle
    SINK[0] = a.sink; LED[0] = a.led; REAL_SET[0] = a.real_set; CANOPY_OPEN[0] = a.canopy_open; CLEARING[0] = a.canopy_clearing; CLEARING_AT[0] = tuple(a.canopy_clearing_at); PLANT_ALPHA[0] = tuple(a.plant_alpha); SCRIM[0] = a.scrim; WET[0] = a.wet; REFLECTORS[0] = [tuple(r) for r in a.reflector]; BERMS[0] = [tuple(b) for b in a.berm]; MANIFEST[0] = json.load(open(a.manifest)) if a.manifest else None; MENISCUS[0] = a.meniscus; LAND[0] = not a.no_land; ROLL[0] = tuple(a.roll_edge) if a.roll_edge else None; DOTS[0] = [tuple(d) for d in a.dot]; CARDS[0] = [(c[0], float(c[1]), float(c[2]), float(c[3]), float(c[4])) for c in a.card]; SPLIT[0] = a.split; GLOSSY_FLAG[0] = a.glossy_flag
    HORN['close'] = a.horn_close; HORN['rough'] = a.horn_rough; HORN['shadows'] = not a.horn_front; HORN['as_cabinet'] = a.horn_as_cabinet
    sh = json.load(open(a.shot))
    scale_lights(sh, {k: float(v) for k, v in (x.split('=', 1) for x in a.light)})
    for kv in a.sets:
        k, v = kv.split('=', 1)
        set_path(sh, k, json.loads(v))
    prepared = os.path.splitext(os.path.abspath(a.out))[0] + '.in.json'
    json.dump(sh, open(prepared, 'w'), indent=1)
    run(prepared, a.collection.format(tint=a.tint), a.out, a.samples, a.scale, os.path.abspath(a.asset), stand=a.stand,
        tt=a.tt, up=a.uplight, glass_from=a.glass_from, ground=not a.no_ground, flag=tuple(a.flag) if a.flag[0] > 0 else None,
        lining=a.lining, glass_shadows=not a.opaque_shadows, extra=(['--crop', *map(str, a.crop)] if a.crop else []))


if __name__ == '__main__':
    main()
