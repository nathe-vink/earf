# Smoke f meteor shower proof (the owner's idea, 2026-11-17): exec'd inside the q202 session on the no-trail build.
# Adds (A) meteors burning up 60-110 km high, 150-600 km away, each a self-luminous head and a tapering tail, all
# moving parallel to the fallen meteor's path (w1's trail direction), dimmed and reddened by the air along their line
# of sight; (B) two far crash sites (the same plume cache, its fire and heat glow its own light) at about 2 and 5.5 km;
# (C) the air between 420 m and 6 km (the scene's haze box stops at 420 m), as a thin volume of the haze's colour.
import bpy, bmesh, math, os, json, sys
from mathutils import Vector
os.chdir('/home/user/earf')
sys.path.insert(0, '/home/user/earf/studio/engine/kit_ext')
import plume as PL
sc = bpy.context.scene; cam = sc.camera
cam.data.clip_end = 1.0e6
C = Vector(cam.location)                         # (0, -6.3, 0.55), level, looking +y
W = 2400; F = cam.data.lens / cam.data.sensor_width * W; CX = 1200.0; CY = 1500.0 + cam.data.shift_y * W
R_E = 6371000.0
LOG = []

def ray(px, py):
    return Vector(((px - CX) / F, 1.0, (CY - py) / F)).normalized()

def proj(P):
    d = P - C
    return CX + F * d.x / d.y, CY - F * d.z / d.y

def at_height(px, py, h):
    """The point on the pixel's ray that lies h m above the curved ground."""
    r = ray(px, py); a = (r.x ** 2 + r.y ** 2) / (2 * R_E); b = r.z
    s = (-b + math.sqrt(b * b + 4 * a * (h - C.z))) / (2 * a)      # height above the curved ground: C.z + b s + a s^2
    return C + r * s, s

U = Vector((212.8, 889.7, 328.4)).normalized()  # w1's trail: from the crash back up its path (toward the radiant)

def emis_mat(name, head_rgb, tail_rgb, s_head, s_tail, gamma):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear(); N = nt.nodes.new; L = nt.links.new
    tc = N('ShaderNodeTexCoord'); sep = N('ShaderNodeSeparateXYZ'); L(tc.outputs['Generated'], sep.inputs[0])
    g = sep.outputs['Z']                                        # 0 at the head, 1 at the tail's end
    pw = N('ShaderNodeMath'); pw.operation = 'POWER'; L(g, pw.inputs[0]); pw.inputs[1].default_value = gamma
    inv = N('ShaderNodeMath'); inv.operation = 'SUBTRACT'; inv.inputs[0].default_value = 1.0; L(pw.outputs[0], inv.inputs[1])
    st = N('ShaderNodeMath'); st.operation = 'MULTIPLY'; L(inv.outputs[0], st.inputs[0]); st.inputs[1].default_value = s_tail
    mix = N('ShaderNodeMix'); mix.data_type = 'RGBA'; L(g, mix.inputs['Factor'])
    mix.inputs[6].default_value = (*head_rgb, 1.0); mix.inputs[7].default_value = (*tail_rgb, 1.0)
    e = N('ShaderNodeEmission'); L(mix.outputs[2], e.inputs['Color']); L(st.outputs[0], e.inputs['Strength'])
    o = N('ShaderNodeOutputMaterial'); L(e.outputs[0], o.inputs['Surface'])
    mh = bpy.data.materials.new(name + '-head'); mh.use_nodes = True; t2 = mh.node_tree; t2.nodes.clear()
    e2 = t2.nodes.new('ShaderNodeEmission'); e2.inputs['Color'].default_value = (*head_rgb, 1.0); e2.inputs['Strength'].default_value = s_head
    o2 = t2.nodes.new('ShaderNodeOutputMaterial'); t2.links.new(e2.outputs[0], o2.inputs['Surface'])
    return m, mh

def lin(hexs):
    h = hexs.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]

def airT(P):
    """Transmittance of the air between the camera and P (exponential atmosphere, airmass from the elevation),
    per channel: dusk extinction 0.10 / 0.17 / 0.30 (R, G, B) per airmass."""
    d = (P - C); el = math.atan2(d.z, math.hypot(d.x, d.y))
    am = 1.0 / (math.sin(el) + 0.15 * (math.degrees(el) + 3.885) ** -1.253)   # Kasten-Young
    return [math.exp(-k * am) for k in (0.10, 0.17, 0.30)], math.degrees(el), am

def meteor(name, px, py, h, tail_px, s_head, s_tail, r_head, r_tail, pieces=((0.0, 0.0, 1.0),)):
    P0, s = at_height(px, py, h)
    # tail length in metres for the wanted length on screen
    lo, hi = 100.0, 200000.0
    for _ in range(50):
        mid = (lo + hi) / 2; x1, y1 = proj(P0 + U * mid)
        if math.hypot(x1 - px, y1 - py) < tail_px: lo = mid
        else: hi = mid
    Lt = lo
    T, el, am = airT(P0)
    head = [a * t for a, t in zip(lin('#FFF6E6'), T)]; tail = [a * t for a, t in zip(lin('#FF9050'), T)]
    for k, (back, side, share) in enumerate(pieces):
        side_v = U.cross(Vector((0, 0, 1))).normalized()
        P = P0 + U * back + side_v * side
        Lk = Lt * (0.55 if k else 1.0)
        m, mh = emis_mat(f'{name}-{k}', head, tail, s_head * share, s_tail * share, 0.6)
        bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=r_tail * share ** 0.5, radius2=0.0, depth=Lk)
        me = bpy.data.meshes.new(f'{name}-{k}-tail'); bm.to_mesh(me); bm.free(); me.materials.append(m)
        ob = bpy.data.objects.new(f'{name}-{k}-tail', me); sc.collection.objects.link(ob)
        # cone along local +z from -L/2 (radius1, the head) to +L/2 (the tail's end); generated z 0 at the head
        ob.location = P + U * (Lk / 2); ob.rotation_mode = 'QUATERNION'; ob.rotation_quaternion = U.to_track_quat('Z', 'Y')
        bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=2, radius=r_head * share ** 0.5)
        me = bpy.data.meshes.new(f'{name}-{k}-head'); bm.to_mesh(me); bm.free(); me.materials.append(mh)
        ob = bpy.data.objects.new(f'{name}-{k}-head', me); sc.collection.objects.link(ob); ob.location = P
    x1, y1 = proj(P0 + U * Lt)
    LOG.append(dict(name=name, head_px=[px, py], tail_end_px=[round(x1), round(y1)], height_km=h / 1000, dist_km=round(s / 1000, 1),
                    elev_deg=round(el, 2), airmass=round(am, 2), T_rgb=[round(t, 3) for t in T], tail_km=round(Lt / 1000, 1),
                    px_per_km=round(F / (s / 1000) / 1000 * 1000, 1), pieces=len(pieces), s_head=s_head))

# (A) the meteors: unequal, unevenly placed, all in the sky clear of the column
meteor('met1', 2075, 1010, 72000, 310, 60.0, 9.0, 260, 160)                                   # the bright one
meteor('met2', 2290, 430, 95000, 150, 22.0, 4.0, 180, 110)
meteor('met3', 2175, 705, 84000, 95, 26.0, 5.0, 200, 120, pieces=((0, 0, 1.0), (1700, 450, 0.7), (3400, -300, 0.45)))  # breaking up
meteor('met4', 2375, 1215, 66000, 70, 9.0, 2.0, 140, 90)
meteor('met5', 165, 1440, 78000, 120, 40.0, 7.0, 240, 150)                                    # low on the left: reddened

# (B) two far crash sites: the plume cache (its own fire and heat glow), on the ground plane, same wind and lean
shot = json.load(open('/home/user/earf/studio/shots/barkhorn/element31/smoke_f-portrait.json')); P8 = shot['set']['props'][8]
def site(name, px, dist, scale, density, strength):
    r = ray(px, CY + 2); y = dist; x = r.x / r.y * y
    p = {**P8, 'position': [x, y, 0.0], 'scale': scale, 'density': density, 'strength': strength, 'box_fade': 0.2}
    obs = PL.plume(bpy, name, p, kit)
    LOG.append(dict(name=name, px=px, dist_km=dist / 1000, pos=[round(x), round(y)], scale=scale,
                    height_m=round(160 * 0.05 * scale), px_tall=round(F * 160 * 0.05 * scale / y), density=density))
site('far1-kit', 2215, 2000.0, 1.75 * 5.0, 8.5 * 0.35, 820.0)         # younger, nearer: 70 m tall
site('far2-kit', 235, 5500.0, 1.75 * 12.0, 8.5 * 0.12, 820.0)         # older, wider, thinner: 168 m tall

# (C) the air beyond the haze box: 420 m to 6 km, up to 300 m, visibility about 25 km (beta 1.6e-4 / m)
bm = bmesh.new(); g = bmesh.ops.create_cube(bm, size=1.0)
for v in g['verts']:
    v.co = Vector(((v.co.x + 0.5) * 6000 - 3000, (v.co.y + 0.5) * 5580 + 420, (v.co.z + 0.5) * 301 - 1))
me = bpy.data.meshes.new('air-far'); bm.to_mesh(me); bm.free()
m = bpy.data.materials.new('air-far'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
vv = nt.nodes.new('ShaderNodeVolumePrincipled'); vv.inputs['Density'].default_value = 1.6e-4
vv.inputs['Color'].default_value = (*lin('#E8DCD0'), 1.0); vv.inputs['Anisotropy'].default_value = 0.5
oo = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(vv.outputs['Volume'], oo.inputs['Volume'])
me.materials.append(m); ob = bpy.data.objects.new('air-far', me); sc.collection.objects.link(ob)
LOG.append(dict(name='air-far', box=[-3000, 420, -1, 3000, 6000, 300], beta=1.6e-4))
json.dump(LOG, open('/tmp/claude-0/-home-user-earf/57ed16bf-b821-5fb9-96e8-d26782970682/scratchpad/f33/shower.json', 'w'), indent=1)
print('SHOWER', json.dumps(LOG))
