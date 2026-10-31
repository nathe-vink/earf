"""Stage a Planet EARF frame (round 44) for a blind critic (critic/PROMPT-interiors.md, step 1): the image under a
neutral name, its card, and the message for a fresh critic (the prompt's text between its rules, verbatim, and the paths).

    python3 spinoffs/barkhorn/planet/r43/r43_stage.py VIEW IMG TAG       # prints the message's path
"""
import os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
STAGE = os.environ.get('STAGE', '/tmp/claude-0/critic-stage')


def main():
    view, img, tag = sys.argv[1:4]
    os.makedirs(STAGE, exist_ok=True)
    dst = os.path.join(STAGE, f'render-{tag}.png')
    shutil.copy(img, dst)
    card = os.path.join(STAGE, f'card-{tag}.md')
    shot = os.path.splitext(img)[0] + '.shot.json'
    subprocess.run([sys.executable, os.path.join(HERE, 'r44_card.py'), view, card, '--shot', shot,
                    '--scale', os.environ.get('CARD_SCALE', '0.5')], check=True, stdout=subprocess.DEVNULL)
    prompt = open(os.path.join(ROOT, 'critic', 'PROMPT-interiors.md')).read().split('\n---\n')[1].strip()
    msg = (f"{prompt}\n\nThe image: {dst}\nThe card (read it only in stage 2): {card}\n"
           f"The measuring tool: python3 {os.path.join(ROOT, 'critic', 'measure.py')}\nScratch space: {STAGE}/scratch-{tag}\n")
    mp = os.path.join(STAGE, f'msg-{tag}.txt')
    open(mp, 'w').write(msg)
    print(mp)


if __name__ == '__main__':
    main()
