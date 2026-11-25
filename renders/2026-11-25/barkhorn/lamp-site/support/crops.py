"""Before (live, final/) and after (this folder) at the site's size (1600 px wide), whole and cropped where the sweep
found the faults. Writes before-after-cluster.jpg and before-after-inuse.jpg here. Python 3 with Pillow."""
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
LIVE = os.path.join(HERE, '..', '..', '..', '..', '2026-11-10', 'barkhorn', 'lamp-site', 'final')
try:
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
except OSError:
    F = ImageFont.load_default()
def site(p):
    im = Image.open(p).convert('RGB'); return im.resize((1600, round(im.size[1] * 1600 / im.size[0])), Image.LANCZOS)
for name, crop in (('hemisphere-cluster', (0, 0, 1600, 520)), ('hemisphere-ember-inuse', (700, 330, 1500, 800))):
    b, a = site(os.path.join(LIVE, name + '.png')), site(os.path.join(HERE, name + '.png'))
    cb, ca = b.crop(crop), a.crop(crop)
    W = 1600 * 2 + 30; H = 60 + b.size[1] + 60 + cb.size[1] * (1600 // cb.size[0] if cb.size[0] < 1600 else 1)
    k = 1600 / cb.size[0]; cb = cb.resize((1600, round(cb.size[1] * k)), Image.LANCZOS); ca = ca.resize(cb.size, Image.LANCZOS)
    S = Image.new('RGB', (W, 60 + b.size[1] + 70 + cb.size[1]), (255, 255, 255)); d = ImageDraw.Draw(S)
    d.text((10, 14), 'BEFORE (live, at 1600 px)', font=F, fill=(0, 0, 0)); d.text((1630 + 10, 14), 'AFTER (at 1600 px)', font=F, fill=(0, 0, 0))
    S.paste(b, (0, 60)); S.paste(a, (1630, 60))
    y = 60 + b.size[1] + 10
    d.text((10, y + 10), f'the crop {crop} of the 1600 px frame, enlarged {k:.1f}x', font=F, fill=(0, 0, 0))
    S.paste(cb, (0, y + 60)); S.paste(ca, (1630, y + 60))
    out = os.path.join(HERE, f'before-after-{name.replace("hemisphere-", "")}.jpg'); S.save(out, quality=86); print(out, S.size, os.path.getsize(out))
