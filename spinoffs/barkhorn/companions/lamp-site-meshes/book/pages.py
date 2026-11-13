"""The open book's two pages for the in-use picture (2026-11-13): text written for this repo (no third-party text),
typeset in DejaVu Serif on cream stock, a running head and a folio. Writes page-L.jpg and page-R.jpg beside this file."""
import os, random
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
TEXT = {
 'L': ("The evening came on slowly over the water, and the lamps along the quay were lit one by one, each throwing a "
       "small round of yellow onto the stones. Nobody hurried. The boats knocked gently against the pilings, and somewhere "
       "above the harbor a window opened and a voice called a name that nobody answered. She sat at the long table with "
       "the book open in front of her and did not read it. The light from the lamp fell on the page and on her hands and "
       "on the rim of the cup, and beyond it the room went soft and gray, the chairs and the shelves and the far wall only "
       "shapes now, kept at a distance. It was the hour she liked best, when the day had stopped asking for anything and "
       "the night had not yet begun. She turned the page without looking down. Outside, the tide was turning too, the "
       "water drawing back from the steps a little at a time, leaving them dark and shining.", 112),
 'R': ("In the morning there would be letters to answer and the long road into town, the bakery and the post office and "
       "the slow conversation at the counter about the weather, which was always about to change. But that was the "
       "morning. Now there was only this: the warm circle on the table, the grain of the old wood running out of the light "
       "and into the dark, the cup gone cool beside the book. She had bought the table from a farmhouse up the valley, "
       "years ago, and it still carried the marks of every meal eaten at it, every knife and every elbow. She liked to "
       "think of the people who had sat where she was sitting, in the same light at the same hour, talking or not "
       "talking. The lamp hummed very faintly, or perhaps that was the house settling. She reached for the cup, found it "
       "empty, and left it where it was.", 113)}
W, H, M = 1500, 2200, 170
f = ImageFont.truetype(FONT, 40); fs = ImageFont.truetype(FONT, 32)
random.seed(3)
for side, (text, folio) in TEXT.items():
    im = Image.new('RGB', (W, H), (243, 238, 227)); d = ImageDraw.Draw(im)
    for _ in range(40000):   # the stock's faint tooth
        x, y = random.randrange(W), random.randrange(H); v = random.randint(-6, 4)
        r, g, b = im.getpixel((x, y)); im.putpixel((x, y), (r + v, g + v, b + v))
    d.text((W / 2, 120), 'THE QUIET HOUR', font=fs, fill=(80, 74, 66), anchor='mm')
    other = TEXT['R' if side == 'L' else 'L'][0]
    words, lines, cur = (text + ' ' + other + ' ' + text).split(), [], ''   # run on until the page is full
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) > W - 2 * M:
            lines.append(cur); cur = w
        else:
            cur = t
    lines.append(cur)
    lines = lines[:int((H - 420) / 58)]
    y = 240
    for i, ln in enumerate(lines):
        ws = ln.split()
        if len(ws) > 1:   # justified
            gap = (W - 2 * M - sum(d.textlength(w, font=f) for w in ws)) / (len(ws) - 1); x = M
            for w in ws:
                d.text((x, y), w, font=f, fill=(38, 35, 31)); x += d.textlength(w, font=f) + gap
        else:
            d.text((M, y), ln, font=f, fill=(38, 35, 31))
        y += 58
    d.text((W / 2, H - 110), str(folio), font=fs, fill=(80, 74, 66), anchor='mm')
    im.save(os.path.join(HERE, f'page-{side}.jpg'), quality=88)
print('pages written')
