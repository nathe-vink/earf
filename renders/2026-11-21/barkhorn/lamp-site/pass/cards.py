"""Group E (2026-11-22): the share cards, 1200 x 630, one per lamp and tint, composed from the pass frames with no
render: the OFF frame on the left, the LIT frame on the right, each scaled to 600 wide (750 tall) and cut to 630 around
the lamp. No words on the card (its copy is the owner's). Writes cards/<lamp>-<tint>.jpg for every tint whose two
frames are in. Run with any Python that has PIL:  python3 renders/2026-11-21/barkhorn/lamp-site/pass/cards.py"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TINTS = [('red', 'ember'), ('orange', 'dust'), ('amber', 'acid'), ('green', 'poison'),
         ('blue', 'ice'), ('violet', 'haze'), ('ice', 'fog'), ('black', 'smoke')]
TOP = {'hemisphere': 90, 'core': 100}        # the cut's top in the 600-wide frame: the shade, or the ball and base, centred
os.makedirs(os.path.join(HERE, 'cards'), exist_ok=True)
for k, name in TINTS:
    for lamp, top in TOP.items():
        pair = [os.path.join(HERE, k, f'{lamp}-{k}-{s}.png') for s in ('off', 'lit')]
        if not all(os.path.exists(p) for p in pair):
            print('skip', lamp, name, '(frames not in)'); continue
        card = Image.new('RGB', (1200, 630))
        for i, p in enumerate(pair):
            im = Image.open(p).convert('RGB').resize((600, 750), Image.LANCZOS)
            card.paste(im.crop((0, top, 600, top + 630)), (600 * i, 0))
        out = os.path.join(HERE, 'cards', f'{lamp}-{name}.jpg')
        card.save(out, quality=88, optimize=True, progressive=True)
        print(out, os.path.getsize(out) // 1024, 'KB')
