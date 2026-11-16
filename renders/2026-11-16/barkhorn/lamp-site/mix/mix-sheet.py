"""THE MIX (2026-11-16): each tint moves the lamp that keeps its lit color rich. Assembled from the A2 (match3), Step A
(match2) and corrected (corr) scratch cells; three Hemisphere lit cells added (Smoke 0.3x and 1.2x, Fog: mixcells.sh)."""
import statistics, json
from PIL import Image, ImageDraw, ImageFont
S = '/tmp/claude-0/-home-user-earf/e73bd455-48f8-5f69-9a3b-fa1e22e4e1e9/scratchpad/'
OUT = '/home/user/earf/renders/2026-11-16/barkhorn/lamp-site/mix/'
# key, name, which lamp moves, its loading today > mix, lumens Hemisphere today/mix, Core today/mix
T = [('red', 'Ember', 'H', '1 > 1.8', (334.1, 307.3), (44.7, 44.7)),
     ('orange', 'Dust', 'C', '3 > 1.6', (353.4, 353.4), (51.1, 62.2)),
     ('amber', 'Acid', 'H', '3 > 5', (419.4, 379.8), (63.2, 63.2)),
     ('green', 'Poison', 'C', '1 > 0.6', (282.1, 282.1), (29.8, 38.1)),
     ('blue', 'Ice', 'H', '3 > 6', (307.5, 269.8), (38.9, 38.9)),
     ('violet', 'Haze', 'H', '1 > 1.8', (280.7, 258.2), (33.0, 33.0)),
     ('ice', 'Fog', '-', 'left', (521.4, 521.4), (95.1, 95.1)),
     ('black', 'Smoke', 'HC', 'H 0.3 > 1.2, C 0.3 > 0.6', (377.6, None), (52.7, 35.1))]
def cells(k, mv):
    ho = [S + 'corr/h-%s.png' % k]; co = [S + 'corr/c-%s.png' % k]
    hl = [S + 'match3/t-%s.png' % k]; cl = [S + 'match2/t-%s.png' % k]
    ho.append(S + ('match3/v-%s.png' % k if 'H' in mv and k != 'black' else 'corr/h-black1.2.png' if k == 'black' else 'corr/h-%s.png' % k))
    co.append(S + ('match2/v-%s.png' % k if 'C' in mv and k != 'black' else 'corr/c-black0.6.png' if k == 'black' else 'corr/c-%s.png' % k))
    hl.append(S + ('match3/l-%s.png' % k if 'H' in mv else 'match3/t-%s.png' % k))
    cl.append(S + ('match2/l-%s.png' % k if 'C' in mv else 'match2/t-%s.png' % k))
    return [('H', 'off', ho), ('C', 'off', co), ('H', 'lit', hl), ('C', 'lit', cl)]
BOX = {('H', 'off'): [(215, 560, 330, 620), (490, 560, 600, 620)], ('C', 'off'): [(270, 520, 530, 600)],
       ('H', 'lit'): [(80, 330, 232, 370)], ('C', 'lit'): [(96, 340, 216, 440)]}
CROP = {'off': (150, 330, 650, 880), 'lit': (0, 170, 312, 590)}
def med(p, key):
    im = Image.open(p).convert('RGB'); px = []
    for b in BOX[key]: px += list(im.crop(b).get_flattened_data() if hasattr(im, 'get_flattened_data') else im.crop(b).getdata())
    return tuple(int(statistics.median(q[i] for q in px)) for i in range(3))
def gap(a, b): return max(abs(x - y) for x, y in zip(a, b))
hs = open(S + 'smoke-photometry.txt').read() if __import__('os').path.exists(S + 'smoke-photometry.txt') else ''
import re
m = re.search(r'dome-black total lm ([\d.]+)', hs)
HS_NEW = float(m.group(1)) if m else 260.0
W, HW, HO, HL, top, lab, line = 420, 210, 231, 284, 70, 150, 34
F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 15)
FS = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 19)
rowh = [HO + line, HO + line, HL + line, HL + line]
H = top + sum(rowh) + 150
im = Image.new('RGB', (lab + W * len(T), H), '#1c1c1c'); d = ImageDraw.Draw(im)
ACC = '#f0c040'; data = {}
for j, (k, n, mv, ld, hlm, clm) in enumerate(T):
    x = lab + j * W
    d.text((x + 10, 8), n, fill='white', font=FB)
    who = {'H': 'Hemisphere denser', 'C': 'Core lighter', 'HC': 'Smoke: the approved pair', '-': 'left as built'}[mv]
    d.text((x + 10, 34), '%s  %s' % (who, ld if mv not in '-' else ''), fill=ACC if mv != '-' else '#bbb', font=FS)
    y = top; rec = {}
    for (lamp, st, ps), rh in zip(cells(k, mv), rowh):
        hh = HO if st == 'off' else HL
        for i, p in enumerate(ps):
            c = Image.open(p).convert('RGB').crop(CROP[st]).resize((HW, hh))
            im.paste(c, (x + i * HW, y))
            v = med(p, (lamp, st)); rec[(lamp, st, i)] = v
            changed = i == 1 and lamp in mv
            d.text((x + i * HW + 8, y + hh + 4), ('%d,%d,%d' % v) + ('  MIX' if changed else ''), fill=ACC if changed else '#ccc', font=FS)
            if changed: d.rectangle((x + i * HW + 1, y + 1, x + (i + 1) * HW - 2, y + hh - 2), outline=ACC, width=3)
        y += rh
    if k == 'black': hlm = (377.6, HS_NEW)
    g0 = gap(rec[('H', 'off', 0)], rec[('C', 'off', 0)]); g1 = gap(rec[('H', 'off', 1)], rec[('C', 'off', 1)])
    data[n] = dict(gap=(g0, g1), H_lm=hlm, C_lm=clm, cells={'%s %s %s' % (a, b, 'mix' if c else 'today'): v for (a, b, c), v in rec.items()})
    d.multiline_text((x + 10, y + 8), 'off gap %d > %d\nHemisphere %.0f > %.0f lm\nCore %.1f > %.1f lm' % (g0, g1, hlm[0], hlm[1], clm[0], clm[1]), fill='white', font=F, spacing=6)
y = top
for s, rh in zip(['Hemisphere off\ntoday | mix', 'Core off\ntoday | mix', 'Hemisphere lit\ntoday | mix', 'Core lit\ntoday | mix'], rowh):
    d.multiline_text((10, y + 20), s, fill='white', font=F); y += rh
d.text((10, H - 30), 'Off: the one off rig, 128 spp. Lit: the rows\' rig and exposure, 256 spp. Corrected method (lamp_site.py since 9a6a2913). '
       'Dye: x the stock pour, as the loading table. The changed lamp outlined. Fog left.', fill='#bbb', font=FS)
im.save(OUT + 'mix-sheet.png', optimize=True)
json.dump(data, open(OUT + 'mix-numbers.json', 'w'), indent=1)
for n, v in data.items(): print(n, v['gap'], v['H_lm'], v['C_lm'], {a: b for a, b in v['cells'].items()})
