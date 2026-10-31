"""Refresh the flavours in the Cloud's engine file (studio/products/barkhorn-cloud.json) from product.VARIANTS, without
the Cloud's 16-minute build, which is at the container's memory limit. The flavours are the only thing it changes; the
build writes the same list (studio/fabkit/render.py), so a full build after this changes nothing more in that field.

    .venv-fab/bin/python spinoffs/barkhorn/flavours.py

Used for the stock colours (stock_colours.json), which are flavours only: no part changes with them.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import cloud                                                         # noqa: E402

path = os.path.join(ROOT, 'studio', 'products', 'barkhorn-cloud.json')
eng = json.load(open(path))
before = set(eng['flavours'])
eng['flavours'] = cloud.PRODUCT.variants or {'default': {}}
json.dump(eng, open(path, 'w'), indent=1)
print(f'{os.path.relpath(path, ROOT)}: {len(eng["flavours"])} flavours, new: {sorted(set(eng["flavours"]) - before)}')
