#!/usr/bin/env python3
"""Stage a site-set frame of Tropos in its final design (Strata on the lit plinth) for a fresh, blind critic under
critic/PROMPT-promo.md, as studio31's frames were judged: the image under a neutral name, a card (what the frame is
for, what is fixed, the shot's settings now), the measuring tool, and the message to hand the critic verbatim.

    python3 spinoffs/barkhorn/critic/stage_site.py IMAGE.png --frame side --tint ice --tag s1 [--stage DIR]

The gate (the coordinator, 2026-11-01): framing and light only. The speaker's materials (its tints, the lining behind
its walls) are fixed in the card while the owner decides them; a note that would change them is not a fix.
"""
import argparse, json, os, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

PURPOSE = {
    'front-off-tall': 'the product page\'s card and the phone gallery: the whole speaker, front three-quarter, a 4:5 '
                      'portrait shown about 1000 px wide',
    'front-off-wide': 'the product page\'s gallery stage at 3:2, shown about 1800 px wide: the whole speaker, front '
                      'three-quarter, with room round it',
    'hero-light': 'the product page\'s hero on a light ground, 16:9, shown up to 2400 px wide with a heading set beside '
                  'the speaker: the whole speaker, front three-quarter, calm and bright',
    'side': 'the product page\'s side view, a 4:5 portrait: the whole speaker from its right side, a little of the front '
            'showing, so the horn\'s stepped profile, its posts and the plinth\'s steps read',
    'back': 'the product page\'s back view, a 4:5 portrait shown 880 px wide: the whole back, the amplifier\'s plate and '
            'the etched EARF mark readable, the horn above',
}

PRODUCT = """EARF's Tropos loudspeaker, in its final design, sold at about $20,000 a pair: a cabinet of 20 mm tinted cast
acrylic (TINT), clear enough to see into, lined inside with polyester batts in dark voile sleeves between its ribs; a
woofer in a stepped ring of the same acrylic (the caldera); above it, on four bronze posts, a horn built from laminated
layers of the same tinted acrylic, stepped like terraces (Strata); the whole standing on a stepped plinth of three
frames of the same tinted acrylic with a warm LED strip under the bottom step, so it glows faintly on the floor. Cover off."""

FIXED = ["The speaker: its shape, its parts, its proportions.",
         "Its materials as they are: the cabinet's and horn's tint, the lining's colour behind the walls, the plinth's "
         "glow. (They are being decided by the owner separately; in this round a note on them is not a fix.)",
         "The whole speaker in frame, never cropped: horn, cabinet and plinth.",
         "The horn's shape (set by acoustic simulation): never change it for a picture."]


def prompt_text():
    t = (ROOT / 'critic' / 'PROMPT-promo.md').read_text()
    a = t.index('\n---\n') + 5; b = t.index('\n---\n', a)
    return t[a:b].strip()


def settings(sh):
    L = [f'- frame: {sh["size"][0]} x {sh["size"][1]} px as delivered (the proof may be half size)',
         f'- camera (`camera`): {json.dumps(sh["camera"])} (metres, z up; the speaker faces -y unless turned)']
    for blk in sh['products'][:1]:
        for i in blk['instances']:
            L.append(f'- the speaker (`products.0.instances.0`): ' + json.dumps({k: i[k] for k in ('position', 'rotate_z') if k in i}))
    for k in ('set', 'sky', 'finish'):
        if k in sh:
            L.append(f'- `{k}`: {json.dumps(sh[k])}')
    L.append(f'- `render`: {json.dumps(sh["render"])}')
    for n, l in (sh.get('lights') or {}).items():
        if not (isinstance(l, dict) and l.get('off')):
            L.append(f'- `lights.{n}`: {json.dumps(l)}')
    if sh.get('materials'):
        L.append(f'- `materials` (the set\'s, and `led.glow`, the plinth light\'s strength): {json.dumps(sh["materials"])}')
    return L


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('image'); ap.add_argument('--frame', required=True); ap.add_argument('--tint', required=True)
    ap.add_argument('--tag', required=True); ap.add_argument('--shot', help='the shot file (default the image\'s .shot.json)')
    ap.add_argument('--stage', default=os.environ.get('CLAUDE_SCRATCH', '/tmp') + '/critic-stage')
    a = ap.parse_args()
    d = Path(a.stage); d.mkdir(parents=True, exist_ok=True)
    src = Path(a.image)
    img = d / f'render-{a.tag}{src.suffix}'
    shutil.copy(src, img)
    shot = Path(a.shot) if a.shot else src.with_suffix('.shot.json')
    sh = json.loads(shot.read_text())
    tint = {'ice': 'a clear mid blue', 'dust': 'orange', 'acid': 'a fluorescent yellow', 'fog': 'clear, untinted',
            'ember': 'red', 'poison': 'a deep green', 'haze': 'violet', 'smoke': 'a near-black gray'}[a.tint]
    L = [f'# Card: Tropos, {a.frame}, {a.tint.capitalize()}', '', '## The product', '',
         ' '.join(PRODUCT.replace('TINT', tint).split()), '', '## What this frame is for', '', PURPOSE[a.frame] + '.', '',
         '## Fixed', ''] + [f'- {f}' for f in FIXED]
    L += ['', '## What may change', '', 'The light (every lamp: its position, size, strength, colour), the camera (position, '
          'target, lens, shift), the exposure and white balance, the set\'s surfaces, and how the speaker is turned or '
          'placed. Lengths are metres; z up. The view transform is Khronos PBR Neutral.', '',
          '## The shot\'s current settings', ''] + settings(sh)
    (d / f'card-{a.tag}.md').write_text('\n'.join(L) + '\n')
    tool = d / 'measure.py'
    shutil.copy(ROOT / 'critic' / 'measure.py', tool)
    work = d / f'work-{a.tag}'; work.mkdir(exist_ok=True)
    text = prompt_text().replace('TOOL', str(tool)).replace('IMAGE', str(img)).replace('SCRATCH', str(work))
    msg = (f'Image: {img}\nCard (read only in stage 2): {d / f"card-{a.tag}.md"}\nMeasuring tool: {tool} (run it with python3)\n'
           f'Scratch directory for your crops and grids: {work}\n\n{text}\n')
    (d / f'message-{a.tag}.txt').write_text(msg)
    print(d / f'message-{a.tag}.txt')


if __name__ == '__main__':
    main()
