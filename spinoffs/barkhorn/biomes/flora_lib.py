"""The world's plants and rocks, thinned once and kept as a library (assets/flora.blend, not committed).

    python3.11 spinoffs/barkhorn/biomes/flora_lib.py

Poly Haven's scans run to 7 M polygons (fir_tree_01); imported whole beside eight speakers they took the render past
the container's memory. Each model here is imported once, decimated where heavy, and saved as a collection
`flora.<id>` with its origin at its foot; world.py instances the collections.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'studio', 'engine'))
OUT = os.path.join(HERE, 'assets', 'flora.blend')
MODELS = {'fir_tree_01': 0.06, 'fern_02': 1.0, 'island_tree_01': 0.15, 'didelta_spinosa': 0.35,
          'namaqualand_boulder_02': 0.5, 'rock_07': 1.0, 'grass_medium_01': 1.0, 'dead_tree_trunk': 0.3}


def main():
    import bpy, assets
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for aid, ratio in MODELS.items():
        before = set(bpy.data.objects)
        root = assets.place(bpy, aid, res='1k')
        new = [o for o in bpy.data.objects if o not in before]
        col = bpy.data.collections.new(f'flora.{aid}'); bpy.context.scene.collection.children.link(col)
        dg = bpy.context.evaluated_depsgraph_get()
        for o in new:
            for c in list(o.users_collection):
                c.objects.unlink(o)
            col.objects.link(o)
            if o.type == 'MESH' and ratio < 1.0 and len(o.data.polygons) > 20000:
                md = o.modifiers.new('d', 'DECIMATE'); md.ratio = ratio
                dg.update()
                me = bpy.data.meshes.new_from_object(o.evaluated_get(dg))
                o.modifiers.clear(); old = o.data; o.data = me; bpy.data.meshes.remove(old)
        n = sum(len(o.data.polygons) for o in new if o.type == 'MESH')
        print(aid, n)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=OUT, compress=True)


if __name__ == '__main__':
    main()
