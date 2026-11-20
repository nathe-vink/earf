"""The LIT frames' balance from one render (2026-11-20, the critics: both glows clipped in red, the two lamps unmatched):
the rig's LIGHTGROUPS pass file (Combined_lamp, the LEDs' own light; Combined_studio, everything else, rendered at
HOUSE_STUDIO=1) recombined as lamp + K x studio and viewed as the house frames are (Khronos PBR Neutral, the Tropos
white balance, exposure E), for each K,E given. Cycles is linear in each light, so this is the same as re-rendering
with the studio at K and the exposure at E. Writes OUT_BASE-K-E.png (raw; the house finish is applied by the caller).

    python3.11 launch/lit_balance.py PASSES.exr OUT_BASE K,E [K,E ...]
"""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0]] + (sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
src, base = sys.argv[1], sys.argv[2]
_lc = open(os.path.join(HERE, 'lightcolor.py')).read()
exec(_lc[_lc.index('def read_exr'):_lc.index('ch, W, H = read_exr(src)')])
ch, W, H = read_exr(src)
rgb = lambda p: np.stack([ch[f'ViewLayer.{p}.{c}'] for c in 'RGB'], -1)
lamp, studio = rgb('Combined_lamp'), rgb('Combined_studio')
hr = json.load(open(os.path.join(HERE, 'house-ground.json')))['render']
import bpy
sc = bpy.context.scene; vs = sc.view_settings
vs.view_transform = hr['view']; vs.look = 'None'
vs.use_white_balance = True; vs.white_balance_temperature = hr['white_balance_k']; vs.white_balance_tint = hr['white_balance_tint']
f = sc.render.image_settings; f.file_format = 'PNG'; f.color_mode = 'RGB'; f.color_depth = '8'
for ke in sys.argv[3:]:
    k, e = (float(v) for v in ke.split(','))
    vs.exposure = hr['exposure'] + e
    img_ = lamp + k * studio
    im = bpy.data.images.new('b', W, H, alpha=True, float_buffer=True)
    im.pixels.foreach_set(np.concatenate([img_[::-1].astype(np.float32), np.ones((H, W, 1), np.float32)], -1).ravel())
    out = f'{base}-{k:g}-{e:g}.png'; im.save_render(out, scene=sc); bpy.data.images.remove(im)
    print('LITBAL', out)
