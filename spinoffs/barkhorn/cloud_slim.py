"""The Cloud with the throat ring slimmed (cloud.THROAT_SLIM), an alternative not yet adopted: its render model only, to
studio/products/barkhorn-cloud-slimthroat.json (the GLB in out-cloud-slim/render, not in git), so a shot can set it
beside the default.

    .venv-fab/bin/python spinoffs/barkhorn/cloud_slim.py
"""
import copy, dataclasses, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(ROOT, 'studio', 'fabkit'))
import cloud                                                         # noqa: E402

P = copy.deepcopy(cloud.P)
P['horn']['cast']['formed'].update(cloud.THROAT_SLIM)
PRODUCT = dataclasses.replace(cloud.PRODUCT, name='barkhorn-cloud-slimthroat', params=P)

if __name__ == '__main__':
    import render                                                    # noqa: E402
    parts = [p for p in PRODUCT.parts(PRODUCT.params) if p.solid is not None]
    print(render.write(PRODUCT, parts, os.path.join(HERE, 'out-cloud-slim'), proof=False))
