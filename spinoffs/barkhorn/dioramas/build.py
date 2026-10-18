"""Writes each diorama's frames: studio/shots/barkhorn/diorama31/<colour>.json (landscape) and <colour>-portrait.json.

    python3 spinoffs/barkhorn/dioramas/build.py              every colour with a module here
    python3 spinoffs/barkhorn/dioramas/build.py ember fog     those only
"""
import importlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C                                         # noqa: E402


def main(names):
    os.makedirs(C.OUT, exist_ok=True)
    for name in names or [n for n in C.COLOURS if os.path.exists(os.path.join(HERE, f'{n}.py'))]:
        mod = importlib.import_module(name)
        frames = {'': mod.shot()}
        if hasattr(mod, 'portrait'):
            frames['-portrait'] = mod.portrait()
        for suffix, sh in frames.items():
            f = os.path.join(C.OUT, f'{name}{suffix}.json')
            json.dump(sh, open(f, 'w'), indent=1)
            print(os.path.relpath(f, C.ROOT))


if __name__ == '__main__':
    main(sys.argv[1:])
