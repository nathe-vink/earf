"""Photographic assets from Poly Haven (polyhaven.com, all CC0), fetched on demand and cached: environment maps, PBR
texture sets and scanned models, for sets that put a product on location (round 31b: the owner wanted the speakers "in
their element", with real texture and real light, not dioramas).

    python3 studio/engine/assets.py search hdris|textures|models WORD...   ids whose name, tags or categories match
    python3 studio/engine/assets.py info ID                                  its kind, categories, tags, size, files
    python3 studio/engine/assets.py get ID [--res 2k]                        fetch it into the cache, print the paths
    python3 studio/engine/assets.py sun HDRI_ID [ROTATION_DEG]               where its sun is, as a sun lamp's settings

From a shot (no code needed):
    "sky": {"kind": "hdri", "polyhaven": "kloofendal_48d_partly_cloudy_puresky", "res": "4k", "rotation_deg": 120}
    kit pieces (studio/engine/kit.py): {"shape": "ground", "texture": "aerial_rocks_02", ...},
        {"shape": "asset", "model": "boulder_01", ...}, {"shape": "scatter_assets", "models": [...], ...}, and
        "material": "pbr" with "texture": ID on any other shape.

From a kit_ext module (`kit` is passed in; `import assets` works there too):
    assets.hdri(ID, '4k')                    -> the .hdr's path
    assets.texture(ID, '2k')                 -> {'diff': path, 'nor_gl': path, 'rough': path, 'disp': path, ...}
    assets.model(ID, '2k')                   -> the .gltf's path (its textures and buffer beside it)
    assets.pbr(bpy, ID, res, scale=None, displace=0.0, tint=None, ...) -> a Cycles material
    assets.place(bpy, ID, res, location, rotation_deg, scale)          -> the imported model's root object
    assets.ground(bpy, name, ID, size, ...)  -> a subdivided patch of ground, displaced by its own height map

Scale: a texture is laid at its real size (Poly Haven gives each set's dimensions in millimetres) unless `scale` (metres
a tile) says otherwise; models arrive in metres. The cache is studio/assets/cache/, kept out of git: it is large and a
fresh clone fetches what its shots name again. Poly Haven asks callers to send a User-Agent; requests without one get
403.
"""
import json, math, os, random, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, '..', 'assets', 'cache')
API = 'https://api.polyhaven.com'
UA = {'User-Agent': 'earf-studio-engine/1.0 (product renders; github.com/nathe-vink/earf)'}
KINDS = ('hdris', 'textures', 'models')
# texture maps by the names Poly Haven gives them, mapped to the short keys this module uses; formats in preference order
MAPS = {'diff': ('Diffuse', ('jpg', 'png')), 'nor_gl': ('nor_gl', ('jpg', 'png')), 'rough': ('Rough', ('jpg', 'png')),
        'disp': ('Displacement', ('png', 'jpg')), 'ao': ('AO', ('jpg', 'png')), 'arm': ('arm', ('jpg', 'png')),
        'alpha': ('Alpha', ('png', 'jpg')), 'trans': ('Translucent', ('jpg', 'png'))}


def _get(url, path=None, tries=4):
    """GET url (to `path` if given, else return the bytes), retrying a dropped connection with backoff."""
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                data = r.read()
            if path:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                tmp = path + '.part'
                open(tmp, 'wb').write(data); os.replace(tmp, path)
                return path
            return data
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 ** (i + 1))


def _json(url, cache_name, max_age=86400):
    p = os.path.join(CACHE, '_api', cache_name)
    if os.path.exists(p) and time.time() - os.path.getmtime(p) < max_age:
        return json.load(open(p))
    d = json.loads(_get(url))
    os.makedirs(os.path.dirname(p), exist_ok=True); json.dump(d, open(p, 'w'))
    return d


def index(kind):
    """{id: info} for every asset of a kind ('hdris', 'textures', 'models')."""
    return _json(f'{API}/assets?t={kind}', f'index-{kind}.json')


def info(aid):
    return _json(f'{API}/info/{aid}', f'info-{aid}.json')


def files(aid):
    return _json(f'{API}/files/{aid}', f'files-{aid}.json')


def search(kind, *words):
    """Ids of `kind` whose id, name, tags or categories contain every word."""
    out = []
    for k, v in index(kind).items():
        text = ' '.join([k, v.get('name', '')] + v.get('tags', []) + v.get('categories', [])).lower()
        if all(w.lower() in text for w in words):
            out.append(k)
    return sorted(out)


def _pick_res(avail, res):
    """The resolution asked for if offered, else the nearest below it, else the smallest above."""
    order = sorted(avail, key=lambda r: int(r.rstrip('k')))
    want = int(res.rstrip('k'))
    below = [r for r in order if int(r.rstrip('k')) <= want]
    return below[-1] if below else order[0]


def hdri(aid, res='4k', fmt='hdr'):
    """An environment map's path (fetched once): .hdr by default (.exr if asked)."""
    f = files(aid)['hdri']
    r = _pick_res(f.keys(), res)
    entry = f[r].get(fmt) or f[r].get('exr') or f[r].get('hdr')
    path = os.path.join(CACHE, 'hdris', os.path.basename(entry['url']))
    return path if os.path.exists(path) else _get(entry['url'], path)


def texture(aid, res='2k', maps=('diff', 'nor_gl', 'rough', 'disp', 'ao', 'alpha', 'trans')):
    """A texture set's maps that exist, {key: path}, each fetched once."""
    f = files(aid)
    out = {}
    for key in maps:
        name, fmts = MAPS[key]
        if name not in f:
            continue
        r = _pick_res(f[name].keys(), res)
        fmt = next((x for x in fmts if x in f[name][r]), None)
        if not fmt:
            continue
        url = f[name][r][fmt]['url']
        path = os.path.join(CACHE, 'textures', aid, os.path.basename(url))
        out[key] = path if os.path.exists(path) else _get(url, path)
    return out


def model(aid, res='2k'):
    """A scanned model's .gltf path, with its buffer and textures beside it (each fetched once)."""
    f = files(aid)['gltf']
    r = _pick_res(f.keys(), res)
    g = f[r]['gltf']
    root = os.path.join(CACHE, 'models', f'{aid}_{r}')
    path = os.path.join(root, os.path.basename(g['url']))
    for rel, e in g.get('include', {}).items():
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            _get(e['url'], p)
    return path if os.path.exists(path) else _get(g['url'], path)


def ambientcg(aid, res='2K'):
    """An ambientCG (ambientcg.com, CC0) material's maps, {key: path}, from its zip (fetched and unpacked once): the
    second library, for what Poly Haven lacks (lava with its emission map, for one). Keys as texture()'s, plus
    'emit'. Search: https://ambientcg.com/api/v2/full_json?type=Material&q=WORD"""
    import zipfile
    root = os.path.join(CACHE, 'ambientcg', f'{aid}_{res}')
    if not os.path.isdir(root) or not os.listdir(root):
        z = os.path.join(CACHE, 'ambientcg', f'{aid}_{res}-JPG.zip')
        if not os.path.exists(z):
            _get(f'https://ambientcg.com/get?file={aid}_{res}-JPG.zip', z)
        with zipfile.ZipFile(z) as f:
            f.extractall(root)
    keys = {'_Color': 'diff', '_NormalGL': 'nor_gl', '_Roughness': 'rough', '_Displacement': 'disp',
            '_AmbientOcclusion': 'ao', '_Opacity': 'alpha', '_Emission': 'emit'}
    out = {}
    for f in sorted(os.listdir(root)):
        for tag, key in keys.items():
            if tag in f and f.lower().endswith(('.jpg', '.png')):
                out[key] = os.path.join(root, f)
    return out


def size_m(aid):
    """A texture set's real size in metres (width, height), from Poly Haven's dimensions (mm), or None."""
    d = info(aid).get('dimensions')
    return (d[0] / 1000.0, d[1] / 1000.0) if d else None


def read_hdr(path):
    """A Radiance .hdr as a float32 array (rows top to bottom, linear RGB): enough of the format for Poly Haven's
    files (new-style run-length scanlines), so a sky can be measured without Blender."""
    import numpy as np
    data = open(path, 'rb').read()
    i = data.index(b'\n\n') + 2
    j = data.index(b'\n', i)
    dims = data[i:j].split()
    H, W = int(dims[1]), int(dims[3])
    pos = j + 1
    out = np.zeros((H, W, 4), np.uint8)
    for y in range(H):
        if data[pos] != 2 or data[pos + 1] != 2:
            raise ValueError('old-style RLE not supported')
        pos += 4
        for c in range(4):
            x = 0
            row = out[y, :, c]
            while x < W:
                n = data[pos]; pos += 1
                if n > 128:
                    n -= 128; row[x:x + n] = data[pos]; pos += 1
                else:
                    row[x:x + n] = np.frombuffer(data, np.uint8, n, pos); pos += n
                x += n
    e = out[..., 3].astype(np.int32)
    f = np.where(e > 0, np.ldexp(1.0, e - 136), 0.0).astype(np.float32)
    return out[..., :3].astype(np.float32) * f[..., None]


def hdri_sun(aid, rotation_deg=0.0, res='1k'):
    """Where an environment's sun is, in the engine's terms, so a sun lamp can match it: the brightest patch of the
    map, turned as `sky.rotation_deg` turns it. Returns {azimuth_deg (the compass direction it shines from, 0 from
    the product's front, +90 from +x), elevation_deg, color (sRGB hex of its light), peak (its brightness against the
    sky's median, a guide to how hard its shadows are)}."""
    import numpy as np
    img = read_hdr(hdri(aid, res))
    H, W, _ = img.shape
    lum = img @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    k = max(1, int(lum.size * 0.0005))                                # the brightest 0.05 % of the map
    idx = np.argpartition(lum.ravel(), -k)[-k:]
    w = lum.ravel()[idx]
    rows, cols = np.unravel_index(idx, lum.shape)
    u = (np.average(cols, weights=w) + 0.5) / W
    v = 1.0 - (np.average(rows, weights=w) + 0.5) / H
    # Cycles' equirectangular lookup: u = 0.5 - atan2(y, x) / 2 pi (u 0.5 looks along +x, 0.25 along +y), v from elevation
    phi, theta = (u - 0.5) * 2 * math.pi, (v - 0.5) * math.pi
    d = (math.cos(phi) * math.cos(theta), -math.sin(phi) * math.cos(theta), math.sin(theta))
    r = math.radians(-rotation_deg)                                   # the map is looked up through Rz(rotation)
    x, y = d[0] * math.cos(r) - d[1] * math.sin(r), d[0] * math.sin(r) + d[1] * math.cos(r)
    col = (img.reshape(-1, 3)[idx] * w[:, None]).sum(0); col = col / max(col.max(), 1e-9)
    srgb = [1.055 * c ** (1 / 2.4) - 0.055 if c > 0.0031308 else 12.92 * c for c in col]
    return {'azimuth_deg': round(math.degrees(math.atan2(x, -y)), 1), 'elevation_deg': round(math.degrees(math.asin(d[2])), 1),
            'color': '#%02X%02X%02X' % tuple(int(max(0, min(1, c)) * 255) for c in srgb),
            'peak': round(float(lum.ravel()[idx].mean() / max(np.median(lum), 1e-9)), 1)}


# --- in Blender -------------------------------------------------------------------------------------------------
def _img(bpy, nt, path, colour, x, y):
    n = nt.nodes.new('ShaderNodeTexImage'); n.location = (x, y)
    n.image = bpy.data.images.load(os.path.abspath(path), check_existing=True)
    if not colour:
        n.image.colorspace_settings.name = 'Non-Color'
    return n


def pbr(bpy, aid, res='2k', scale=None, displace=0.0, tint=None, tint_mix=0.0, rough_mul=1.0, bump=1.0,
        coords='object', name=None, translucency=0.0, emit=0.0, value=1.0):
    """A Cycles material from a Poly Haven texture set (or an ambientCG one, its id prefixed 'acg:', e.g. 'acg:Lava004',
    whose emission map glows at `emit`), laid at its real size (`scale` metres a tile overrides it).
    `displace` (metres) lifts the surface by its height map where the mesh is dense enough (Cycles displacement, bump
    beyond); `tint` (hex) blended in by `tint_mix` shifts its colour toward a set's palette (its hue and saturation
    only: a dark tint leaves a light texture light), and `value` scales its brightness; `coords` 'object' (box
    projection in object space, for ground and rock without UVs) or 'uv'."""
    acg = aid.startswith('acg:')
    maps = ambientcg(aid[4:], res.upper()) if acg else texture(aid, res)
    sx = sy = scale if scale else None
    if not sx:
        s = (None if acg else size_m(aid)) or (2.0, 2.0)
        sx, sy = s
    m = bpy.data.materials.new(name or f'pbr-{aid}')
    m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    out = nt.nodes.new('ShaderNodeOutputMaterial'); out.location = (900, 0)
    bs = nt.nodes.new('ShaderNodeBsdfPrincipled'); bs.location = (600, 0)
    nt.links.new(bs.outputs['BSDF'], out.inputs['Surface'])
    tc = nt.nodes.new('ShaderNodeTexCoord'); tc.location = (-900, 0)
    mp = nt.nodes.new('ShaderNodeMapping'); mp.location = (-700, 0)
    mp.inputs['Scale'].default_value = (1.0 / sx, 1.0 / sy, 1.0 / sx)
    nt.links.new(tc.outputs['UV' if coords == 'uv' else 'Object'], mp.inputs['Vector'])
    vec = mp.outputs['Vector']
    proj = 'BOX' if coords == 'object' else 'FLAT'

    def tex(key, colour, y):
        n = _img(bpy, nt, maps[key], colour, -400, y); n.projection = proj; n.projection_blend = 0.25
        nt.links.new(vec, n.inputs['Vector']); return n
    if 'diff' in maps:
        d = tex('diff', True, 300)
        col = d.outputs['Color']
        if 'ao' in maps:
            ao = tex('ao', False, 520); mul = nt.nodes.new('ShaderNodeMix'); mul.data_type = 'RGBA'; mul.blend_type = 'MULTIPLY'
            mul.inputs['Factor'].default_value = 0.6; mul.location = (100, 400)
            nt.links.new(col, mul.inputs['A']); nt.links.new(ao.outputs['Color'], mul.inputs['B']); col = mul.outputs['Result']
        if tint and tint_mix > 0:
            mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'COLOR'; mx.location = (300, 400)
            h = tint.lstrip('#'); c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
            c = [((v + 0.055) / 1.055) ** 2.4 if v > 0.04045 else v / 12.92 for v in c]
            mx.inputs['Factor'].default_value = tint_mix; mx.inputs['B'].default_value = (*c, 1.0)
            nt.links.new(col, mx.inputs['A']); col = mx.outputs['Result']
        if value != 1.0:
            vm = nt.nodes.new('ShaderNodeMix'); vm.data_type = 'RGBA'; vm.blend_type = 'MULTIPLY'; vm.location = (380, 400)
            vm.inputs['Factor'].default_value = 1.0; vm.inputs['B'].default_value = (value, value, value, 1.0)
            nt.links.new(col, vm.inputs['A']); col = vm.outputs['Result']
        nt.links.new(col, bs.inputs['Base Color'])
    if 'rough' in maps:
        r = tex('rough', False, 0)
        if rough_mul != 1.0:
            mm = nt.nodes.new('ShaderNodeMath'); mm.operation = 'MULTIPLY'; mm.inputs[1].default_value = rough_mul; mm.location = (200, 0)
            nt.links.new(r.outputs['Color'], mm.inputs[0]); nt.links.new(mm.outputs['Value'], bs.inputs['Roughness'])
        else:
            nt.links.new(r.outputs['Color'], bs.inputs['Roughness'])
    if 'nor_gl' in maps:
        n = tex('nor_gl', False, -300); nm = nt.nodes.new('ShaderNodeNormalMap'); nm.location = (200, -300)
        nm.inputs['Strength'].default_value = bump
        nt.links.new(n.outputs['Color'], nm.inputs['Color']); nt.links.new(nm.outputs['Normal'], bs.inputs['Normal'])
    if 'alpha' in maps:
        a = tex('alpha', False, -600); nt.links.new(a.outputs['Color'], bs.inputs['Alpha'])
    if translucency > 0:
        bs.inputs['Subsurface Weight'].default_value = translucency
    if 'emit' in maps and emit > 0:                                 # lava and the like glow by their own map
        e = tex('emit', True, -1000)
        nt.links.new(e.outputs['Color'], bs.inputs['Emission Color']); bs.inputs['Emission Strength'].default_value = emit
    if 'disp' in maps and displace > 0:
        dn = tex('disp', False, -800); dp = nt.nodes.new('ShaderNodeDisplacement'); dp.location = (600, -500)
        dp.inputs['Scale'].default_value = displace; dp.inputs['Midlevel'].default_value = 0.5
        nt.links.new(dn.outputs['Color'], dp.inputs['Height']); nt.links.new(dp.outputs['Displacement'], out.inputs['Displacement'])
        m.displacement_method = 'BOTH'                                  # true displacement where dense, bump beyond
    return m


def _alpha_maps(bpy, aid, res, objs):
    """Poly Haven's glTFs for plants cut their leaves out with an alpha mask but point the base colour at a JPG, which
    has no alpha, so the leaf cards render solid. Where a material takes its alpha from a JPG's alpha, wire in the
    asset's own Alpha map instead (fetched once)."""
    mats = {m for o in objs if o.type == 'MESH' for m in o.data.materials if m and m.use_nodes}
    fix = []
    for m in mats:
        for l in m.node_tree.links:
            n = l.from_node
            if (l.from_socket.name == 'Alpha' and n.type == 'TEX_IMAGE' and n.image
                    and n.image.filepath.lower().endswith(('.jpg', '.jpeg'))):
                fix.append((m, l))
    if not fix:
        return
    f = files(aid).get('Alpha', {})
    r = _pick_res(f.keys(), res) if f else None
    e = f[r].get('png') or f[r].get('jpg') if r else None
    if not e:
        return
    path = os.path.join(CACHE, 'models', f'{aid}_{r}', 'textures', os.path.basename(e['url']))
    if not os.path.exists(path):
        _get(e['url'], path)
    img = bpy.data.images.load(path, check_existing=True); img.colorspace_settings.name = 'Non-Color'
    for m, l in fix:
        nt = m.node_tree; src = l.from_node; to = l.to_socket
        a = nt.nodes.new('ShaderNodeTexImage'); a.image = img; a.location = (src.location.x, src.location.y - 300)
        a.interpolation = src.interpolation; a.extension = src.extension
        for i in src.inputs:                                 # the same coordinates as the colour it pairs with
            for ll in i.links:
                nt.links.new(ll.from_socket, a.inputs[i.name])
        nt.links.remove(l); nt.links.new(a.outputs['Color'], to)


def place(bpy, aid, res='2k', location=(0, 0, 0), rotation_deg=(0, 0, 0), scale=1.0, name=None):
    """Import a scanned model (fetched once) under one empty, placed and turned (degrees) and scaled; return the empty.
    The model's own materials come with it."""
    path = model(aid, res)
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    _alpha_maps(bpy, aid, res, new)
    root = bpy.data.objects.new(name or aid, None); bpy.context.scene.collection.objects.link(root)
    for o in new:
        if o.parent is None:
            o.parent = root
    root.location = location
    root.rotation_euler = [math.radians(a) for a in rotation_deg]
    root.scale = (scale,) * 3 if isinstance(scale, (int, float)) else scale
    return root


def instance(bpy, root, location, rotation_deg=(0, 0, 0), scale=1.0, name=None):
    """Another copy of a placed model sharing its meshes (cheap), placed, turned and scaled."""
    def dup(o, parent):
        c = o.copy(); bpy.context.scene.collection.objects.link(c); c.parent = parent
        for ch in o.children:
            dup(ch, c)
        return c
    r = dup(root, None)
    if name:
        r.name = name
    r.location = location
    r.rotation_euler = [math.radians(a) for a in rotation_deg]
    r.scale = (scale,) * 3 if isinstance(scale, (int, float)) else scale
    return r


def scatter(bpy, ids, res='2k', count=20, area=(-3, -3, 3, 3), avoid=(), scale=(0.8, 1.2), z=0.0, seed=1,
            spin=True, tilt_deg=0.0):
    """`count` copies of the models in `ids` scattered over `area` (x0, y0, x1, y1), none inside an `avoid` circle
    (x, y, r), each turned and sized at random; the first of each model is imported, the rest share its meshes."""
    rnd = random.Random(seed)
    roots = {i: place(bpy, i, res, location=(0, 0, -1000)) for i in ids}
    made, tries = [], 0
    while len(made) < count and tries < count * 50:
        tries += 1
        x, y = rnd.uniform(area[0], area[2]), rnd.uniform(area[1], area[3])
        if any((x - ax) ** 2 + (y - ay) ** 2 < ar ** 2 for ax, ay, ar in avoid):
            continue
        rot = (rnd.uniform(-tilt_deg, tilt_deg), rnd.uniform(-tilt_deg, tilt_deg), rnd.uniform(0, 360) if spin else 0)
        made.append(instance(bpy, roots[rnd.choice(ids)], (x, y, z), rot, rnd.uniform(*scale)))
    for r in roots.values():                                          # the originals stay out of sight
        r.hide_render = True
        for o in r.children_recursive:
            o.hide_render = True
    return made


def ground(bpy, name, aid, size=(8.0, 8.0), res='2k', centre=(0.0, 0.0, 0.0), cells=None, displace=0.03,
           tint=None, tint_mix=0.0, scale=None, rough_mul=1.0, bump=1.0, relief=None, flat=(0.0, 0.0, 0.9),
           dents=None, furrows=None):
    """A patch of ground `size` metres, dense enough to take its texture's height map (`displace` metres) as true
    displacement, laid with that texture at its real size. `relief` (metres, optional) adds broad undulation by noise
    so the ground does not read as a floor; it fades to nothing within `flat` (x, y, r: a world point and a radius,
    the product's footprint by default) so what stands there stands on level ground; `cells` sets the mesh's density
    (default about 1.5 cm). Smoke E12's impact, both optional and in world metres: `dents`, craters [x, y, r, depth,
    rim, rim width] (a bowl `depth` deep at its centre, its lip raised `rim` round radius r), and `furrows`, trenches
    [x0, y0, x1, y1, half-width, depth at the start, depth at the end, rim] (a groove ploughed from the first point to
    the second, its spoil heaped along both banks)."""
    import bmesh
    w, d = size
    nx = cells or max(2, int(w / 0.015)); ny = max(2, int(nx * d / w))
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=nx, y_segments=ny, size=0.5)
    for v in bm.verts:
        v.co.x *= w; v.co.y *= d
    if relief:
        from mathutils import noise, Vector
        fx, fy, fr = (flat[0] - centre[0], flat[1] - centre[1], flat[2]) if flat else (0.0, 0.0, 0.0)
        for v in bm.verts:
            t = 1.0
            if fr > 0:
                q = min(1.0, max(0.0, (math.hypot(v.co.x - fx, v.co.y - fy) - fr) / fr))
                t = q * q * (3 - 2 * q)                               # level under the product, rising to full by 2r
            v.co.z += t * relief * noise.noise(Vector((v.co.x * 0.35, v.co.y * 0.35, 0.7)))
    if dents or furrows:
        from mathutils import noise as nz, Vector as V
        for v in bm.verts:
            x, y = v.co.x + centre[0], v.co.y + centre[1]
            dz = 0.0
            for cx, cy, r, depth, rim, rw in dents or []:
                d = math.hypot(x - cx, y - cy)
                if d > r + 4 * rw:
                    continue
                jag = 1.0 + 0.12 * nz.noise(V((x * 6.0, y * 6.0, 3.1)))      # no crater is round
                q = d / (r * jag)
                if q < 1.0:
                    dz -= depth * (1.0 - q * q)
                dz += rim * math.exp(-((d - r * jag) / rw) ** 2) * (1.0 + 0.5 * nz.noise(V((x * 9.0, y * 9.0, 5.3))))
            for x0, y0, x1, y1, hw, d0, d1, rim in furrows or []:
                ax, ay = x1 - x0, y1 - y0; L2 = ax * ax + ay * ay
                t = max(0.0, min(1.0, ((x - x0) * ax + (y - y0) * ay) / L2))
                px, py = x0 + ax * t, y0 + ay * t
                d = math.hypot(x - px, y - py)
                w = hw * (0.5 + 0.5 * t) * (1.0 + 0.15 * nz.noise(V((x * 5.0, y * 5.0, 7.7))))   # wider as it bit deeper
                if d > 3 * w:
                    continue
                q = d / w
                depth = d0 + (d1 - d0) * t
                if q < 1.0:
                    dz -= depth * (1.0 - q * q)
                dz += rim * (0.3 + 0.7 * t) * math.exp(-((q - 1.15) / 0.45) ** 2)
            v.co.z += dz
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    for f in me.polygons:
        f.use_smooth = True
    me.materials.append(pbr(bpy, aid, res, scale=scale, displace=displace, tint=tint, tint_mix=tint_mix,
                            rough_mul=rough_mul, bump=bump, name=f'{name}-mat'))
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = centre
    return ob


def main():
    a = sys.argv[1:]
    if a and a[0] == 'sun':                                           # where a sky's sun is: sun ID [ROTATION]
        print(json.dumps(hdri_sun(a[1], float(a[2]) if len(a) > 2 else 0.0))); return
    if not a or a[0] not in ('search', 'info', 'get'):
        print(__doc__); return
    if a[0] == 'search':
        for i in search(a[1], *a[2:]):
            v = index(a[1])[i]
            print(f'{i:44s} {", ".join(v.get("categories", []))[:60]}')
    elif a[0] == 'info':
        v = info(a[1]); f = files(a[1])
        print(json.dumps({k: v.get(k) for k in ('name', 'type', 'categories', 'tags', 'dimensions', 'evs_cap')}, indent=1))
        print('files:', {k: sorted(x.keys()) if isinstance(x, dict) else x for k, x in f.items() if k in ('hdri', 'gltf', 'Diffuse')})
    else:
        res = a[a.index('--res') + 1] if '--res' in a else '2k'
        kind = info(a[1]).get('type')                                 # Poly Haven: 0 an HDRI, 1 a texture, 2 a model
        if kind == 0:
            print(hdri(a[1], res))
        elif kind == 2:
            print(model(a[1], res))
        else:
            for k, p in texture(a[1], res).items():
                print(k, p)


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:                                           # piped into head
        pass
