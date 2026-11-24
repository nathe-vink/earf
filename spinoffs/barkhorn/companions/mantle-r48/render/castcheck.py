"""The cast check for a saved Mantle scene (the coordinator's rule, from the lamps lane's lamp_site.py AUDIT block):
every mesh and every lamp hidden from the camera must cover 0.0 % of the frame (hiddencast_bpy, copied from
r32-lamps-final), and every mesh's and lamp's ray visibilities (RAYVIS) and every light- or shadow-linking collection
(LINK) are printed. With --mask PNG, Blender's own camera renders the hidden objects as a mask too (CASTCHECK).

    python3.11 render/castcheck.py SCENE.blend [--mask MASK.png]
"""
import os, sys
import bpy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hiddencast_bpy import hiddencast, report, mask_check

blend = sys.argv[1]
bpy.ops.wm.open_mainfile(filepath=blend)
sc = bpy.context.scene
frame = os.path.splitext(os.path.basename(blend))[0]
print(report(frame, hiddencast(sc)))
links = 0
for o_ in sc.objects:
    if o_.type in ('MESH', 'LIGHT'):
        print('RAYVIS', o_.type, o_.name, ' '.join(f'{k}={int(getattr(o_, "visible_" + k))}' for k in
              ('camera', 'diffuse', 'glossy', 'transmission', 'volume_scatter', 'shadow')))
    for kind_ in ('receiver_collection', 'blocker_collection'):
        c_ = getattr(o_.light_linking, kind_, None) if hasattr(o_, 'light_linking') else None
        if c_ is not None:
            links += 1
            print('LINK', o_.name, kind_.split('_')[0], [(m_.name, cm_.light_linking.link_state) for m_, cm_ in zip(c_.objects, c_.collection_objects)])
if not links:
    print('LINK none: no light- or shadow-linking collection in the scene')
if '--mask' in sys.argv:
    print('CASTCHECK', frame, {k: round(v * 100, 2) for k, v in mask_check(sc, sys.argv[sys.argv.index('--mask') + 1]).items()})
