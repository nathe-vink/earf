"""Horn against box for one or more frames: OKLab hue and luminance (stops) of the horn and the upper box, and hot-pink glint pixels."""
import sys, math, numpy as np; from PIL import Image
def lin(c): c = c / 255; return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
def oklab(rgb):
    r, g, b = rgb
    l = 0.4122214708*r + 0.5363325363*g + 0.0514459929*b; m = 0.2119034982*r + 0.6806995451*g + 0.1073969566*b; s = 0.0883024619*r + 0.2817188376*g + 0.6299787005*b
    l, m, s = [x ** (1/3) for x in (l, m, s)]
    L = 0.2104542553*l + 0.7936177850*m - 0.0040720468*s; a = 1.9779984951*l - 2.4285922050*m + 0.4505937099*s; bb = 0.0259040371*l + 0.7827717662*m - 0.8086757660*s
    return L, math.hypot(a, bb), math.degrees(math.atan2(bb, a)) % 360
for p in sys.argv[1:]:
    a = np.asarray(Image.open(p).convert('RGB')).astype(float); k = a.shape[1] / 1200
    def reg(x0, y0, x1, y1): return lin(a[int(y0*k):int(y1*k), int(x0*k):int(x1*k)]).reshape(-1, 3).mean(0)
    horn = reg(640, 560, 860, 680); box = reg(640, 750, 860, 850)
    Y = lambda v: v @ [0.2126, 0.7152, 0.0722]
    _, ch, hh = oklab(horn); _, cb, hb = oklab(box)
    pink = ((a[..., 0] > 230) & (a[..., 1] > 120) & (a[..., 1] < 200) & (a[..., 2] > 180)).sum()
    print(f'{p.split("/")[-1]:34s} horn hue {hh:5.1f} | box hue {hb:5.1f} | dH {hh-hb:+5.1f} | horn vs box {math.log2(Y(horn)/Y(box)):+.2f} stops | box Y {Y(box):.4f} | pink px {pink}')
