"""Two light colours from one render (the owner, 2026-11-10: "in a bar setting I want amber/yellow lighting ... render
with both"): the rig's LIGHTGROUPS pass file (an uncompressed 32-bit multilayer EXR with Combined_lamp, the lamp's own
LEDs, and Combined_studio, everything else) recoloured and viewed at ONE camera balance, 4000 K:
  -warm   the LEDs as drawn (2700 K; 3000 K on Ice and Haze)
  -amber  the same LEDs at 2200 K, the same lumens
Cycles renders each RGB channel linearly, so scaling the lamp pass channel by channel is the same as re-rendering
with the LEDs' colour changed (the emitters' energy is set per lumen at the colour's luminance, so the lumens hold).

    python3.11 launch/lightcolor.py PASSES.exr OUT_BASE EV DRAWN_K [LOOK]
"""
import sys, os, struct
import numpy as np
a = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
src, base, ev, drawn = a[0], a[1], float(a[2]), int(a[3]); look = a[4] if len(a) > 4 else 'AgX - Punchy'
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def read_exr(path):
    """An uncompressed scanline EXR, single- or multi-part (Blender 5 writes a multilayer file as one part a pass)."""
    d = open(path, 'rb').read(); p = 8; multi = bool(struct.unpack('<i', d[4:8])[0] & 0x1000); parts = []
    while True:
        hdr = {}
        while d[p] != 0:
            e = d.index(b'\0', p); name = d[p:e].decode(); p = e + 1
            e = d.index(b'\0', p); typ = d[p:e].decode(); p = e + 1
            n = struct.unpack('<i', d[p:p + 4])[0]; p += 4; hdr[name] = d[p:p + n]; p += n
        p += 1; parts.append(hdr)
        if not multi or d[p] == 0:
            p += 1 if multi else 0
            break
    out = {}
    tables = []
    for hdr in parts:
        assert hdr['compression'][0] == 0, 'uncompressed only'
        x0, y0, x1, y1 = struct.unpack('<4i', hdr['dataWindow']); W, H = x1 - x0 + 1, y1 - y0 + 1
        n = struct.unpack('<i', hdr['chunkCount'])[0] if 'chunkCount' in hdr else H
        tables.append(struct.unpack(f'<{n}Q', d[p:p + 8 * n])); p += 8 * n
    for pi, (hdr, offs) in enumerate(zip(parts, tables)):
        chl, q, raw = [], 0, hdr['channels']
        while raw[q] != 0:
            e = raw.index(b'\0', q); nm = raw[q:e].decode(); q = e + 1
            pt = struct.unpack('<i', raw[q:q + 4])[0]; q += 16; chl.append((nm, pt))
        x0, y0, x1, y1 = struct.unpack('<4i', hdr['dataWindow']); W, H = x1 - x0 + 1, y1 - y0 + 1
        for nm, _ in chl:
            out[nm] = np.zeros((H, W), np.float32)
        for o in offs:
            q = o + (4 if multi else 0)
            y = struct.unpack('<i', d[q:q + 4])[0] - y0; q += 8
            for nm, pt in chl:
                sz = 4 if pt == 2 else 2
                out[nm][y] = np.frombuffer(d[q:q + W * sz], np.float32 if pt == 2 else np.float16).astype(np.float32); q += W * sz
    return out, W, H


ch, W, H = read_exr(src)
def rgb(p):
    return np.stack([ch[f'ViewLayer.{p}.{c}'] for c in 'RGB'], -1)
lamp, studio, comb = rgb('Combined_lamp'), rgb('Combined_studio'), rgb('Combined')
err = float(np.abs(lamp + studio - comb).mean() / max(comb.mean(), 1e-9))
import lamp_pictures as LP
def unit(T):
    c = np.array(LP.blackbody(T)); return c / (0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])
k = unit(2200) / unit(drawn)
import bpy
sc = bpy.context.scene; vs = sc.view_settings
vs.view_transform = 'AgX'; vs.look = look; vs.exposure = ev
vs.use_white_balance = True; vs.white_balance_temperature = 4000.0; vs.white_balance_tint = 0.0
f = sc.render.image_settings; f.file_format = 'PNG'; f.color_mode = 'RGB'; f.color_depth = '8'
for tag, img_ in (('warm', studio + lamp), ('amber', studio + lamp * k)):
    im = bpy.data.images.new(tag, W, H, alpha=True, float_buffer=True)
    px = np.concatenate([img_[::-1].astype(np.float32), np.ones((H, W, 1), np.float32)], -1).ravel()
    im.pixels.foreach_set(px)
    im.save_render(f'{base}-{tag}.png', scene=sc)
    print('LIGHTCOLOR', f'{base}-{tag}.png')
print('LIGHTCOLOR check: |lamp + studio - combined| / combined =', round(err, 5), '; amber k =', [round(v, 3) for v in k])
