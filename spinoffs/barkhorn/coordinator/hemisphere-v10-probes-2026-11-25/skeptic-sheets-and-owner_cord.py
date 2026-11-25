# Measure the cord's centre and the cables' columns per row in each lock frame (dark thin vertical structures).
import sys, math
import numpy as np
from PIL import Image
D = sys.argv[1]
FR = ['lock9-1-hidden', 'lock9-2-profile', 'lock10-6-45', 'lock9-3-back', 'lock10-4-none', 'lock9-4-none']
for f in FR:
    a = np.asarray(Image.open(f'{D}/{f}.png').convert('L')).astype(float)
    bg = np.median(a[:, :60])
    out = []
    for r in (20, 60, 100, 150, 200, 250, 300, 350, 400, 420):
        row = a[r]
        dark = row < 60        # the cord is near black; the cables are grey/light
        xs = np.nonzero(dark)[0]
        # group runs
        runs = []
        if len(xs):
            s = xs[0]; p = xs[0]
            for x in xs[1:]:
                if x != p + 1:
                    runs.append((s, p)); s = x
                p = x
            runs.append((s, p))
        # cables: mid-grey thin lines, darker than bg by >12 but >60
        mid = (row < bg - 12) & (row >= 60)
        ms = np.nonzero(mid)[0]
        mruns = []
        if len(ms):
            s = ms[0]; p = ms[0]
            for x in ms[1:]:
                if x != p + 1:
                    mruns.append((s, p)); s = x
                p = x
            mruns.append((s, p))
        out.append((r, runs, mruns))
    print(f)
    cs = []
    for r, runs, mruns in out:
        big = [ru for ru in runs if ru[1] - ru[0] >= 3]
        c = [(ru[0] + ru[1]) / 2 for ru in big]
        cs.append((r, c))
        print(f'  row {r:4d} cord runs {big}  grey runs {[m for m in mruns if m[1]-m[0] < 12][:6]}')
    # lean from row 60 to row 400 using the first big run
    try:
        c60 = [c for r, c in cs if r == 60][0][0]; c400 = [c for r, c in cs if r == 400][0][0]
        print(f'  cord centre row60 {c60} row400 {c400}: lean {math.degrees(math.atan2(c60 - c400, 340)):+.2f} deg')
    except Exception as e:
        print('  lean n/a', e)
