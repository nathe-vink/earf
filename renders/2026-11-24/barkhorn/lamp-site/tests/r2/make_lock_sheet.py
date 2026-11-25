"""The owner's lock sheet (2026-11-24): top A's level frame four ways and the view from below, labelled. Built from
owner-lock.sh's frames with the CAD venv's Python."""
import os, matplotlib
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data', 'fonts', 'ttf')
FB = ImageFont.truetype(os.path.join(FD, 'DejaVuSans-Bold.ttf'), 28); F = ImageFont.truetype(os.path.join(FD, 'DejaVuSans.ttf'), 22)
FR = [('lock9-1-hidden', '1. With the lock, as drawn', 'the knob at the back, behind the crown'),
      ('lock9-2-profile', '2. With the lock, the lamp turned 79 deg', 'the knob in profile: Ø21, 29 out'),
      ('lock9-3-back', '3. With the lock, the lamp turned 169 deg', 'the knob toward the camera'),
      ('lock9-4-none', '4. No lock, from 2\'s angle', 'the J-slot and a detent; the cables at 0/180'),
      ('lock9-5-below', '5. From 30 deg below, the knob\'s side', '0.75 m off, 100 mm lens, an even dome')]
ims = [Image.open(os.path.join(HERE, f + '.png')).convert('RGB') for f, _, _ in FR]
W = 700; ims = [im.resize((W, int(im.size[1] * W / im.size[0])), Image.LANCZOS) for im in ims]
H = max(im.size[1] for im in ims); G = 16; TH = 90
S = Image.new('RGB', (5 * W + 4 * G, TH + H + 200), (255, 255, 255)); d = ImageDraw.Draw(S)
for i, ((f, t, s), im) in enumerate(zip(FR, ims)):
    x = i * (W + G); d.text((x + 6, 8), t, font=FB, fill=(0, 0, 0)); d.text((x + 6, 48), s, font=F, fill=(50, 50, 50)); S.paste(im, (x, TH))
y = TH + H + 14
for l in ('Hemisphere top A, Ember, off. Frames 1 to 4: one camera, light and exposure (1.6 m off, 200 mm lens); the lamp turned about its axis.',
          'The lock (Ganter GN 617, about $18, one per shade) stops the shade being lifted, turned or lowered until its knob is pulled. Without it the',
          'shade still needs a lift, a turn and a lower against its own weight, and a ball detent clicks it home, as today\'s top and B have.',
          'The knob is matte black polyamide on a blackened steel body (as drawn). It can be seen from about two-thirds of the directions round',
          'the lamp; from the rest the crown hides it. With the lock, A\'s cables run on the lock\'s line (105/285 deg); without it, at 0/180.'):
    d.text((8, y), l, font=F, fill=(60, 60, 60)); y += 34
out = os.path.join(HERE, 'lock-sheet-v9.jpg'); S.save(out, quality=88); print(out, S.size, os.path.getsize(out))
