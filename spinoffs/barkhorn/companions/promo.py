"""Round 31b's promotional critic passes on the companions (critic/PROMPT-promo.md): stage an image for a fresh, blind
critic with a short card and the measuring tool, and keep the passes' log.

    python3 spinoffs/barkhorn/companions/promo.py stage IMAGE.png TAG --shot SHOT.json --kind turntable|lamp [--purpose ...]
        -> SCRATCH/critic-stage/render-TAG.png, card-TAG.md, measure.py, message-TAG.txt (give the message to the critic)

The card says what the frame is for, what is fixed (the product: its shape, colour and parts) and what may change
(the set, the light, the camera, the finish), with the shot's current settings, as the prompt asks. Nothing else about
the product, the brief or this conversation goes to the critic.
"""
import argparse, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
STAGE = os.path.join(os.environ.get('CLAUDE_SCRATCH', '/tmp'), 'critic-stage')

FIXED = {
    'turntable': ('a belt-drive record player, 483 x 373 mm, its plinth two cemented sheets of tinted cast acrylic cut as '
                  'three fused circles (the platter\'s, the arm\'s, the motor\'s), the motor standing apart in its own '
                  'acrylic pod in a hole in the plinth, a 25 mm tinted acrylic platter, a black Rega tonearm and black '
                  'cartridge, brass bearing; sold at about $5,000. Beside it, as context, a 1293 mm tall horn loudspeaker in '
                  'the same tinted acrylic (sold at about $20,000 a pair).'),
    'lamp': ('a table lamp 480 mm tall, its shade a horn\'s flare 432 mm across formed in tinted cast acrylic and hung mouth '
             'down, lit from an opal sleeve at its throat (warm white LED, about 600 lm), on a clear acrylic stem and a foot '
             'of two tinted acrylic discs; sold at about $1,500. Beside it, as context, a 1293 mm tall horn loudspeaker in '
             'the same tinted acrylic (sold at about $20,000 a pair).'),
    # round 32: Moon, the bar lamps
    'moon': ('a pair of bar lamps in one tinted cast acrylic. A cordless table lamp 277 mm tall: a frosted acrylic dome '
             '150 across over a solid tinted acrylic column 40 across, a brass hub and finial, on a blackened-steel foot '
             '120 across; lit from inside the dome, the LED never seen. A pendant: a frosted acrylic dome 200 across under '
             'a 20 mm tinted acrylic disc 220 across, a brass hub and canopy, a black cord. Sold to bars and restaurants '
             'at about $450 (the table lamp) and $750 (the pendant).'),
}
PURPOSE = {
    'turntable': 'The record player\'s campaign hero: the record player is the subject, in a real living room, with the '
                 'loudspeaker in its colour as context. It will run as a full page and as the hero of its homepage.',
    'lamp': 'The lamp\'s campaign hero: the lamp, switched on, is the subject; its light through the coloured shade carries '
            'the room at dusk, the loudspeaker in its colour as context. It will run as a full page and as the hero of its '
            'homepage.',
    'moon': 'The bar lamps\' hero for the trade: both lamps lit, in a dim bar at about 2700 K (board-formed concrete, a '
            'fir table), so a bar owner sees the light they make and the quality of the acrylic and the metal. It will run '
            'as the line sheet\'s and the website\'s lead image.',
}


def prompt_text():
    t = open(os.path.join(ROOT, 'critic', 'PROMPT-promo.md')).read()
    a = t.index('\n---\n') + 5
    b = t.index('\n---\n', a)
    return t[a:b].strip()


def settings(shot):
    """The shot's settings, short: camera, sun and sky, lamps, the set's pieces, exposure."""
    s = json.load(open(shot))
    L = ['| setting | value |', '|---|---|']
    def row(k, v):
        L.append(f'| `{k}` | {json.dumps(v)} |')
    for k in ('position', 'target', 'lens_mm', 'fstop', 'focus'):
        if k in s.get('camera', {}):
            row(f'camera.{k}', s['camera'][k])
    for k, v in (s.get('sun') or {}).items():
        row(f'sun.{k}', v)
    for k, v in (s.get('sky') or {}).items():
        row(f'sky.{k}', v)
    for n, l in (s.get('lights') or {}).items():
        row(f'lights.{n}', l)
    st = s.get('set', {})
    for k in ('kind', 'size', 'center', 'floor', 'wall', 'windows', 'color'):
        if k in st:
            row(f'set.{k}', st[k])
    for i, p in enumerate(st.get('props', [])):
        row(f'set.props.{i}', p)
    for k, v in (s.get('materials') or {}).items():
        row(f'materials.{k}', v)
    for b, blk in enumerate(s.get('products') or ([s['product']] if s.get('product') else [])):
        row(f'products.{b}.instances.0.position', blk['instances'][0]['position'])
    for k in ('exposure', 'white_balance_k', 'samples'):
        if k in s.get('render', {}):
            row(f'render.{k}', s['render'][k])
    return L


def stage(a):
    os.makedirs(STAGE, exist_ok=True)
    img = os.path.join(STAGE, f'render-{a.tag}.png')
    shutil.copy(a.image, img)
    card = os.path.join(STAGE, f'card-{a.tag}.md')
    L = ['# Card', '', '## What this frame is for', '', a.purpose or PURPOSE[a.kind], '',
         '## Fixed (never prescribe a change to these)', '', 'The product: ' + FIXED[a.kind] + ' Their shape, size, '
         'colour, materials and parts are fixed' + ('.' if a.kind == 'moon' else ', and so is which loudspeaker stands '
         'beside it. Every piece in the frame shares one colour by design.'), '',
         '## May change', '', 'Everything about the set (the room, its walls, floor, window, furniture and props, any '
         'Poly Haven CC0 texture, model or sky), the light (sun, sky, lamps, the lamp\'s own output), the camera (place, '
         'lens, aperture, focus) and the finish (exposure, white balance). Where the products stand may change.', '',
         '## The shot\'s current settings (metres, degrees, watts; the frame\'s world: z up, the camera\'s side is -y)', '']
    L += settings(a.shot)
    open(card, 'w').write('\n'.join(L) + '\n')
    tool = os.path.join(STAGE, 'measure.py')
    shutil.copy(os.path.join(ROOT, 'critic', 'measure.py'), tool)
    work = os.path.join(STAGE, f'work-{a.tag}')
    os.makedirs(work, exist_ok=True)
    text = prompt_text().replace('TOOL', tool).replace('IMAGE', img).replace('SCRATCH', work)
    msg = (f'Image: {img}\nCard (read only in stage 2): {card}\nMeasuring tool: {tool} (run it with python3)\n'
           f'Scratch directory: {work}\n\n{text}\n')
    path = os.path.join(STAGE, f'message-{a.tag}.txt')
    open(path, 'w').write(msg)
    print(path)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest='cmd', required=True)
    s = sp.add_parser('stage'); s.add_argument('image'); s.add_argument('tag'); s.add_argument('--shot', required=True)
    s.add_argument('--kind', required=True, choices=list(FIXED)); s.add_argument('--purpose')
    a = ap.parse_args()
    stage(a)
