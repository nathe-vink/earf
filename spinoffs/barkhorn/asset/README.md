# Tropos as a Blender asset (2026-10-31)

`tropos.blend` holds the current Tropos (the Cloud as built on r33-speaker-horn: the round-36 formed horn) in all eight
tints. It is one collection per tint, each marked as an asset: **Tropos Ember, Dust, Acid, Poison, Ice, Haze, Fog,
Smoke**.

**The frame:**
- metres, z up;
- the front faces −y;
- the feet stand on z = 0;
- the speaker is centred on x.

**The cover is off by default** (the owner, 2026-10-31: every Tropos picture shows the woofer). Each tint's cloth
disc sits in a child collection, `Tropos <tint> cover`, which is hidden in render and viewport. To fit it:

```python
c = bpy.data.collections['Tropos Smoke cover']; c.hide_render = c.hide_viewport = False
```

This works on a linked library collection only through a library override; otherwise append the collection.

**The materials** are the render engine's own (Cycles; the acrylic is a volume absorber, so a speaker casts its tint's
shadow). The file opens with Ember shown and the other seven excluded from the view layer.

**Using it.** Link or append a collection, then instance it. `link_example.py` does this for four tints and renders
`link_example.png`:

```python
with bpy.data.libraries.load('…/tropos.blend', link=True, assets_only=True) as (src, dst):
    dst.collections = ['Tropos Smoke']
e = bpy.data.objects.new('Tropos', None); e.instance_type = 'COLLECTION'
e.instance_collection = bpy.data.collections['Tropos Smoke']; bpy.context.scene.collection.objects.link(e)
```

Or add the folder as an asset library in Blender's preferences and drag a tint in from the Asset Browser.

**Weight.** The file is 30 MB, and has no `.blend1` backup beside it. It is made for a speaker seen across a room or a landscape:
- the plates' printed text and the screws' threads are collapsed;
- the horn's dense tessellation and the lining's voile webs are collapsed;
- see `LIGHTER` in `make_blend.py`.

For close-ups, render through the studio engine (`studio/engine/render.py`), or rebuild the file with `--full`, which
is about 73 MB and not for git.

**Rebuilding.** Rebuild only when the design changes, since each rebuild adds 30 MB to the history:

    python3.11 spinoffs/barkhorn/asset/make_blend.py [--out …] [--full]

It needs the Cloud's render model, `spinoffs/barkhorn/out-cloud/render/barkhorn-cloud.glb`, which the Cloud's fabkit
build writes. The model is not in git. A proposal's variant gets its own file beside this one.
