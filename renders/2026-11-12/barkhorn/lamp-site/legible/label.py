"""Five labels on the cutaway (2026-11-12), plain words, thin leader lines from the projected anchors that lamp_site.py
prints (ANCHOR name x y, in the 2000 x 2000 frame). Usage: label.py raw.png render.log out.png [phone]
'phone' (2026-11-13, the coordinator: on a phone the site shows it about 360 px wide): 1200 x 1200 from the same render,
the labels about twice the size relative to the picture, on two lines, in the free corners above and below the lamp,
the leaders heavier."""
import re, subprocess, sys
raw, log, out = sys.argv[1:4]
PHONE = len(sys.argv) > 4 and sys.argv[4] == 'phone'
A = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in re.finditer(r'ANCHOR (\w+) (-?\d+) (-?\d+)', open(log).read())}
FONT = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
# (anchor, text, the text's top-left, the leader's end at the text)
LABELS = [
    ('leds', 'LEDs on a ring, facing up', (1270, 1330), (1262, 1352)),
    ('carrier', 'black center', (330, 1330), (640, 1352)),
    ('diffuser', 'white diffuser', (150, 560), (452, 582)),
    ('shade', 'clear shell, tinted outside', (1300, 560), (1292, 582)),
    ('down', 'warm white light, down', (760, 1760), (1000, 1745)),
]
if PHONE:
    k = 0.6; A = {n: (round(x * k), round(y * k)) for n, (x, y) in A.items()}
    # (anchor, lines, the first line's top-left, the leader's end)
    PL = [('diffuser', ['white', 'diffuser'], (40, 40), (190, 176)),
          ('shade', ['clear shell,', 'tinted outside'], (780, 40), (905, 176)),
          ('carrier', ['black center'], (40, 905), (230, 895)),
          ('leds', ['LEDs on a ring,', 'facing up'], (790, 905), (900, 895)),
          ('down', ['warm white', 'light, down'], (555, 1062), (665, 1052))]
    a = ['convert', raw, '-resize', '1200x1200', '-stroke', '#E8E6E1', '-strokewidth', '4', '-fill', 'none']
    for key, lines, tl, end in PL:
        ax, ay = A[key]
        if key == 'down':
            a += ['-draw', f'line {ax},{ay - 50} {ax},{end[1] - 34}', '-fill', '#E8E6E1',
                  '-draw', f'polygon {ax - 15},{end[1] - 58} {ax + 15},{end[1] - 58} {ax},{end[1] - 24}', '-fill', 'none']
        else:
            a += ['-draw', f'line {ax},{ay} {end[0]},{end[1]}', '-draw', f'circle {ax},{ay} {ax + 8},{ay}']
    a += ['-stroke', 'none', '-fill', '#F2F0EB', '-font', FONT, '-pointsize', '50']
    for key, lines, tl, end in PL:
        for i, ln in enumerate(lines):
            a += ['-annotate', f'+{tl[0]}+{tl[1] + 50 + i * 60}', ln]
    a += ['-depth', '8', '-type', 'TrueColor', 'PNG24:' + out]
    subprocess.run(a, check=True); print('labelled (phone)', out); sys.exit(0)
args = ['convert', raw, '-stroke', '#E8E6E1', '-strokewidth', '2.5', '-fill', 'none']
for key, text, tl, end in LABELS:
    ax, ay = A[key]
    if key == 'down':      # straight down from just under the mouth, with an arrowhead
        args += ['-draw', f'line {ax},{ay - 60} {ax},{end[1] - 30}',
                 '-fill', '#E8E6E1', '-draw', f'polygon {ax - 12},{end[1] - 52} {ax + 12},{end[1] - 52} {ax},{end[1] - 26}', '-fill', 'none']
    else:
        args += ['-draw', f'line {ax},{ay} {end[0]},{end[1]}', '-draw', f'circle {ax},{ay} {ax + 6},{ay}']
args += ['-stroke', 'none', '-fill', '#F2F0EB', '-font', FONT, '-pointsize', '44']
for key, text, tl, end in LABELS:
    args += ['-annotate', f'+{tl[0]}+{tl[1] + 44}', text]
args += ['-depth', '8', '-type', 'TrueColor', 'PNG24:' + out]
subprocess.run(args, check=True)
print('labelled', out, {k: A[k] for k, *_ in LABELS})
