"""Stage a critic round for an edition frame: the image under a neutral name, its card, and the message (the text of
critic/PROMPT.md between its rules, verbatim, plus the paths). Usage: python3 stage.py IMAGE CARD TAG STAGEDIR"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
img, card, tag, d = sys.argv[1:5]
d = Path(d); d.mkdir(parents=True, exist_ok=True)
shutil.copy(img, d / f'render-{tag}.png')
shutil.copy(card, d / f'card-{tag}.md')
t = (ROOT / 'critic' / 'PROMPT.md').read_text()
a = t.index('\n---\n') + 5; b = t.index('\n---\n', a)
msg = (t[a:b].strip() + f"\n\nIMAGE: {d}/render-{tag}.png\nCARD: {d}/card-{tag}.md\nTOOL: {ROOT}/critic/measure.py\n"
       f"SCRATCH: {d}/scratch-{tag}\n\nReply with the JSON only, and also write it to {d}/reply-{tag}.json.")
(d / f'message-{tag}.txt').write_text(msg)
print(d / f'message-{tag}.txt')
