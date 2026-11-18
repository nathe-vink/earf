# Smoke f meteor shower proof 2 (2026-11-18, the owner: "one more try"): exec'd in the q203 session on the no-trail
# build. Three long meteors in the right-hand sky, on lines through the radiant of the fallen one's path (w1's trail
# direction), self-luminous, dimmed and reddened by the air at their elevation; two slender far smoke columns on the
# right at 5.5 and 8 km, dark smoke (smoke_el.trail as a leaning, top-sheared column) with the air between in their
# own shader (density x T, colour toward the horizon sky by 1 - T), and a small fire glow at each foot, dimmed the
# same way. No air box: the sky stays exactly the no-trail sky.
import bpy, bmesh, math, os, json, sys
from mathutils import Vector
os.chdir('/home/user/earf')
sys.path.insert(0, '/home/user/earf/studio/engine/kit_ext')
import importlib, smoke_el; importlib.reload(smoke_el)
sc = bpy.context.scene; cam = sc.camera
cam.data.clip_end = 1.0e6
C = Vector(cam.location)
W = 2400; F = cam.data.lens / cam.data.sensor_width * W; CX = 1200.0; CY = 1500.0 + cam.data.shift_y * W
R_E = 6371000.0
LOG = []
U = Vector((212.8, 889.7, 328.4)).normalized()      # back up the fallen meteor's path, toward the radiant
OUT = '/tmp/claude-0/-home-user-earf/57ed16bf-b821-5fb9-96e8-d26782970682/scratchpad/f36/shower.json'

def ray(px, py):
    return Vector(((px - CX) / F, 1.0, (CY - py) / F)).normalized()

def proj(P):
    d = P - C
    return CX + F * d.x / d.y, CY - F * d.z / d.y

def at_height(px, py, h):
    r = ray(px, py); a = (r.x ** 2 + r.y ** 2) / (2 * R_E); b = r.z
    s = (-b + math.sqrt(b * b + 4 * a * (h - C.z))) / (2 * a)
    return C + r * s, s

def lin(hexs):
    h = hexs.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]

def air_meteor(P):
    d = (P - C); el = math.atan2(d.z, math.hypot(d.x, d.y))
    am = 1.0 / (math.sin(el) + 0.15 * (math.degrees(el) + 3.885) ** -1.253)
    return [math.exp(-k * am) for k in (0.07, 0.10, 0.17)], math.degrees(el), am

def emis(name, rgb_head, rgb_tail, strength, gamma=None, s_tail=None):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    e = N('ShaderNodeEmission'); o = N('ShaderNodeOutputMaterial'); L(e.outputs[0], o.inputs['Surface'])
    if gamma is None:
        e.inputs['Color'].default_value = (*rgb_head, 1.0); e.inputs['Strength'].default_value = strength; return m
    tc = N('ShaderNodeTexCoord'); sep = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sep.inputs[0]); g = sep.outputs['Z']
    pw = N('ShaderNodeMath'); pw.operation = 'POWER'; L(g, pw.inputs[0]); pw.inputs[1].default_value = gamma
    inv = N('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0; L(pw.outputs[0], inv.inputs[1])
    st = N('ShaderNodeMath'); st.operation = 'MULTIPLY'; L(inv.outputs[0], st.inputs[0]); st.inputs[1].default_value = s_tail
    mix = N('ShaderNodeMix'); mix.data_type = 'RGBA'; L(g, mix.inputs['Factor'])
    mix.inputs[6].default_value = (*rgb_head, 1.0); mix.inputs[7].default_value = (*rgb_tail, 1.0)
    L(mix.outputs[2], e.inputs['Color']); L(st.outputs[0], e.inputs['Strength'])
    return m

def meteor(name, px, py, h, tail_px, s_head, s_tail, head_px_r, tail_px_r, gamma=1.0):
    P, s = at_height(px, py, h)
    lo, hi = 100.0, 400000.0
    for _ in range(60):
        mid = (lo + hi) / 2; x1, y1 = proj(P + U * mid)
        if math.hypot(x1 - px, y1 - py) < tail_px: lo = mid
        else: hi = mid
    Lt = lo; mpp = s / F                                   # metres per pixel at the head
    T, el, am = air_meteor(P)
    head = [a * t for a, t in zip(lin('#FFF8F0'), T)]; tail = [a * t for a, t in zip(lin('#FF9A50'), T)]
    mt = emis(name + '-tail', head, tail, 0, gamma, s_tail); mh = emis(name + '-head', head, head, s_head)
    bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=10, radius1=tail_px_r * mpp, radius2=0.0, depth=Lt)
    me = bpy.data.meshes.new(name + '-tail'); bm.to_mesh(me); bm.free(); me.materials.append(mt)
    ob = bpy.data.objects.new(name + '-tail', me); sc.collection.objects.link(ob)
    ob.location = P + U * (Lt / 2); ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = U.to_track_quat('Z', 'Y')
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=2, radius=head_px_r * mpp)
    me = bpy.data.meshes.new(name + '-head'); bm.to_mesh(me); bm.free(); me.materials.append(mh)
    ob = bpy.data.objects.new(name + '-head', me); sc.collection.objects.link(ob); ob.location = P
    x1, y1 = proj(P + U * Lt); P2 = P + U * Lt
    LOG.append(dict(name=name, head_px=[px, py], tail_end_px=[round(x1), round(y1)], head_km=round(h / 1000, 1),
                    tail_top_km=round((P2.z + ((P2 - C).length) ** 2 / (2 * R_E)) / 1000, 1), dist_km=round(s / 1000),
                    elev_deg=round(el, 1), T_rgb=[round(t, 2) for t in T], tail_km=round(Lt / 1000), s_head=s_head, s_tail=s_tail))

# (A) the meteors: one long and brightest, one lesser, one breaking into three (ATV-1-like: parallel pieces, own tails)
meteor('met1', 2140, 1150, 30000, 690, 400.0, 26.0, 6, 3.2)        # a fireball: down to 30 km, like Chelyabinsk's
meteor('met2', 2075, 600, 50000, 440, 160.0, 11.0, 4, 2.4)
for k, (dx, dy, f) in enumerate(((0, 0, 1.0), (-14, -30, 0.7), (12, -58, 0.5))):
    meteor(f'met3-{k}', 2325 + dx, 1050 + dy, 45000, 400 * (1.0 if k == 0 else 0.7), 160.0 * f, 10.0 * f, 4, 2.2)

# (B) the far columns: dark smoke, leaning with the main plume's wind (toward -x), the top sheared over; air in the shader
SKY = '#ABA7B4'          # the no-trail sky just above the horizon on the right (sRGB of the raw frame)
def column(name, px, dist, height, r0, r1, lean, shear_top, seed):
    r = ray(px, CY); x = r.x / r.y * dist
    E = Vector((x, dist, -2.0)); S = Vector((x + lean, dist, height))
    p = dict(end=list(E), start=list(S), radius=[r0, r1], grow=1.0, thin=0.6, density=round(10.0 / (2 * r0), 4),
             color='#2C2926', anisotropy=0.4, fade=0.25, seed=seed, warp=[0.25, 0.6], warp_detail=1.0,
             puff=[0.45, 0.7], puff_detail=3.0, puff_soft=0.3, edge=[1.15, 0.0], edge_gamma=1.4,
             shear=[[0.0, 0, 0], [0.45, 0, 0], [0.75, 0, -0.3 * shear_top], [1.0, 0, -shear_top]],
             air=dict(beta=1.0e-4, H=8000.0, cam=list(C), sky=SKY), step=0.5)
    obs = smoke_el.trail(bpy, name, p, kit)
    # the fire at its foot: a low glowing mound no wider than the column, dimmed by the same air (R, G, B a little apart)
    T = [math.exp(-1.0e-4 * k * dist) for k in (0.8, 1.0, 1.3)]
    gl = emis(name + '-glow', [a * t for a, t in zip(lin('#FF8A3A'), T)], None, 6.0)
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=3, radius=1.0)
    me = bpy.data.meshes.new(name + '-glow'); bm.to_mesh(me); bm.free(); me.materials.append(gl)
    ob = bpy.data.objects.new(name + '-glow', me); sc.collection.objects.link(ob)
    ob.location = Vector((x, dist, -0.4 * r0)); ob.scale = (0.7 * r0, 0.7 * r0, 0.45 * r0)
    LOG.append(dict(name=name, px_base=px, dist_km=dist / 1000, height_m=height, px_tall=round(F * height / dist),
                    px_wide_base=round(F * 2 * r0 / dist), px_wide_top=round(F * 2 * r1 / dist), lean_m=lean,
                    shear_top_m=shear_top, T_air=[round(t, 2) for t in T], boxes=len(obs)))
column('farA', 2265, 5500.0, 450.0, 22.0, 100.0, -40.0, 60.0, 4)
column('farB', 2360, 8000.0, 380.0, 18.0, 85.0, -30.0, 50.0, 7)
json.dump(LOG, open(OUT, 'w'), indent=1)
print('SHOWER', json.dumps(LOG))
