"""Stage a blind critic or a blind duel for round 48 (the method of critic/PROMPT-promo.md and critic/duel.py, with
this round's prompt). The critic sees a neutral file name, a one-line card, the measuring tool and the prompt's text:
nothing else.

    python3 stage.py critic IMAGE TAG "card line" STAGE_DIR
    python3 stage.py duel NEW OLD TAG STAGE_DIR          (random order; the order is saved beside it, not shown)
"""
import json, os, random, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
PROMPT = os.path.join(HERE, 'PROMPT-realism.md')
DUEL = os.path.join(ROOT, 'critic', 'ab', 'PROMPT-DUEL.txt')
CARD = ('Card: a belt-drive record player in through-tinted cast acrylic (the Smoke tint), to sell at about $6,500. '
        'This frame: {}. The record and the sleeve are props.\n')


def critic(img, tag, line, d):
    os.makedirs(d, exist_ok=True)
    shutil.copy(os.path.join(ROOT, 'critic', 'measure.py'), os.path.join(d, 'measure.py'))
    im = os.path.join(d, f'render-{tag}.png'); shutil.copy(img, im)
    card = os.path.join(d, f'card-{tag}.md'); open(card, 'w').write(CARD.format(line))
    work = os.path.join(d, f'work-{tag}'); os.makedirs(work, exist_ok=True)
    body = open(PROMPT).read().split('\n---\n', 1)[1].replace('TOOL', os.path.join(d, 'measure.py')).replace('SCRATCH', work)
    msg = os.path.join(d, f'message-{tag}.txt')
    open(msg, 'w').write(f'Image: {im}\nCard: {card}\nMeasuring tool: {os.path.join(d, "measure.py")}\nScratch directory: {work}\n\n{body}')
    print(msg)


def duel(new, old, tag, d):
    os.makedirs(d, exist_ok=True)
    shutil.copy(os.path.join(ROOT, 'critic', 'measure.py'), os.path.join(d, 'measure.py'))
    new_is_a = random.Random(tag).random() < 0.5
    a, b = (new, old) if new_is_a else (old, new)
    A, B = os.path.join(d, f'duel-{tag}-A.png'), os.path.join(d, f'duel-{tag}-B.png')
    shutil.copy(a, A); shutil.copy(b, B)
    work = os.path.join(d, f'work-duel-{tag}'); os.makedirs(work, exist_ok=True)
    json.dump({'new': os.path.relpath(new, ROOT), 'old': os.path.relpath(old, ROOT), 'new_is': 'A' if new_is_a else 'B'},
              open(os.path.join(d, f'duel-{tag}.order.json'), 'w'), indent=1)
    msg = open(DUEL).read().replace('AB_A', A).replace('AB_B', B).replace('TOOL', os.path.join(d, 'measure.py')).replace('SCRATCH', work)
    p = os.path.join(d, f'message-duel-{tag}.txt'); open(p, 'w').write(msg)
    print(p)


if __name__ == '__main__':
    if sys.argv[1] == 'critic':
        critic(*sys.argv[2:6])
    else:
        duel(*sys.argv[2:6])
