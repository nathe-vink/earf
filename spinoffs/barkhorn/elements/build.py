"""Write the in-their-element shots (round 31b) to studio/shots/barkhorn/element31/: <name>.json and
<name>-portrait.json for each set module named (ember, dust, ... or ember_b for a second concept), or for every module
present if none is named.

    python3 spinoffs/barkhorn/elements/build.py [NAME ...]
    python3 studio/engine/render.py studio/shots/barkhorn/element31/NAME.json --out OUT.png [--samples N --scale S]
"""
import importlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C                                        # noqa: E402

SKIP = {'common', 'build'}


def main():
    names = sys.argv[1:] or sorted(f[:-3] for f in os.listdir(HERE) if f.endswith('.py') and f[:-3] not in SKIP)
    os.makedirs(C.OUT, exist_ok=True)
    for n in names:
        m = importlib.import_module(n)
        for suffix, fn in (('', 'shot'), ('-portrait', 'portrait')):
            if hasattr(m, fn):
                path = os.path.join(C.OUT, f'{n}{suffix}.json')
                json.dump(getattr(m, fn)(), open(path, 'w'), indent=1)
                print(os.path.relpath(path, C.ROOT))


if __name__ == '__main__':
    main()
