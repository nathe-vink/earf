"""Median sRGB of the tinted body, away from highlights: Hemisphere's lower flanks, Core's lower ball."""
import sys, statistics
from PIL import Image
BOX = {'h': [(215, 560, 330, 620), (490, 560, 600, 620)], 'c': [(270, 520, 530, 600)]}
def med(path, kind):
    im = Image.open(path).convert('RGB'); px = []
    for b in BOX[kind]:
        px += list(im.crop(b).getdata())
    return tuple(int(statistics.median(p[i] for p in px)) for i in range(3))
if __name__ == '__main__':
    for p in sys.argv[1:]:
        k = 'h' if '/h-' in p else 'c'; print(p.rsplit('/', 1)[1], med(p, k))
