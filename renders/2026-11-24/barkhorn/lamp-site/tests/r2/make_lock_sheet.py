"""The owner's lock sheet (2026-11-24; V10, 2026-11-25: frame 4's cables kept where frame 2's are, a 45 deg frame, the
text as the v9 check asked): top A's level frame five ways and the view from below, labelled. Built from owner-lock.sh's
frames with the CAD venv's Python. Writes lock-sheet-v10.jpg. V11-19 (2026-11-25): the text as the V10 check asked, laid out 3 x 2."""
import os, matplotlib
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
FB = ImageFont.truetype(os.path.join(FD, 'DejaVuSans-Bold.ttf'), 28); F = ImageFont.truetype(os.path.join(FD, 'DejaVuSans.ttf'), 22)
FR = [('lock9-1-hidden', '1. Lock, the knob facing away', 'behind the crown'),
      ('lock9-2-profile', '2. Lock, the lamp turned 79 deg', 'the knob in profile: Ø21, 29 out'),
      ('lock10-6-45', '3. Lock, the lamp turned 124 deg', 'the knob 45 deg off the camera'),
      ('lock9-3-back', '4. Lock, the lamp turned 169 deg', 'the knob toward the camera'),
      ('lock10-4-none', '5. No lock', 'the cables hang where they do in 2'),
      ('lock9-5-below', '6. 30 deg below, the knob\'s side', '0.75 m off, 100 mm lens, an even dome')]
ims = [Image.open(os.path.join(HERE, f + '.png')).convert('RGB') for f, _, _ in FR]
W = 800; ims = [im.resize((W, int(im.size[1] * W / im.size[0])), Image.LANCZOS) for im in ims]
H = max(im.size[1] for im in ims); G = 16; TH = 90
TXT = ('Hemisphere top A, Ember, off. Frames 1 to 5: one camera, light and exposure (1.6 m off, 200 mm lens), the lamp turned about its axis.',
       'Only top A can take the lock (Ganter GN 617, one per shade; price to quote). It keeps the shade from being lifted, turned or lowered until its knob is pulled.',
       'In a swap the knob is held out through the lift, the turn and the lower, while it turns with the shade; we have not yet shown that one person can do that',
       'while steadying the top. Ganter\'s GN 617.1, which has a rest position that holds the knob out by itself, is the alternative.',
       'The lock does not help a shade let go before it dropped: it engages only once the shade has dropped home. Without the lock the shade still needs a lift,',
       'a turn and a lower against its own weight, and a ball detent clicks it home.',
       'The knob always points along the cables\' line, one of the two opposite ways, set by the ceiling box. At eye level it shows from about five-sixths of the way',
       'round: clear of the top from about two-thirds, face-on against it from about a sixth (frame 4); only within about 25 deg of directly behind does the top hide it',
       '(frame 1). Matte black polyamide knob on a blackened steel body (as drawn).')
S = Image.new('RGB', (3 * W + 2 * G, 2 * (TH + H) + 30 + 34 * len(TXT) + 20), (255, 255, 255)); d = ImageDraw.Draw(S)
for i, ((f, t, s_), im) in enumerate(zip(FR, ims)):
    x = (i % 3) * (W + G); y0 = (i // 3) * (TH + H)
    d.text((x + 6, y0 + 8), t, font=FB, fill=(0, 0, 0)); d.text((x + 6, y0 + 48), s_, font=F, fill=(50, 50, 50)); S.paste(im, (x, y0 + TH))
y = 2 * (TH + H) + 20
for l in TXT:
    d.text((8, y), l, font=F, fill=(60, 60, 60)); y += 34
out = os.path.join(HERE, 'lock-sheet-v10.jpg'); S.save(out, quality=88); print(out, S.size, os.path.getsize(out))
