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

## Strata, the leading proposal (`tropos-strata.blend`)

`tropos-strata.blend` is the Strata proposal (`variants/STRATA.md`) in the same eight tints, the same frame and the
same layout. Its collections are named **Tropos Strata Ember** through **Tropos Strata Smoke**, tagged `Strata` and
`proposal`, and their description says it is a proposal, not the design on sale.

It holds:
- the Cloud's cabinet, with the formed horn, its throat, the stainless posts, the cloth disc and the dyed woofer ring
  left out;
- the stepped laminated horn (`horn-strata`: 22 layers of 1/2 in and the boss, the mouth's layer an even 20 mm lip);
- the four ø16 bronze posts and their collars;
- the caldera, three rings round the woofer.

There is no cover collection: the woofer sits in the caldera, and the cloth disc does not fit it as drawn.

It is 23 MB. Unused meshes are dropped before saving: the templates, and the parts a design hides.
`link_example.py -- strata OUT.png` links four tints and renders `link_example_strata.png`.

    python3.11 spinoffs/barkhorn/asset/make_blend.py --design strata --out spinoffs/barkhorn/asset/tropos-strata.blend

It needs the proposals' render model too, `spinoffs/barkhorn/variants/out/render/barkhorn-variants.glb`. That model is
written by `variants/render_model.py` and is not in git.

## Tints

Both files carry the site's tints, the look of every picture so far. `make_blend.py --tints trucast` builds either
design in stock TruCast sheet instead (`tints.py`, `tints-trucast.json`). That build is reconciled with r48-biomes'
`tints.json`; `TINTS.md` has the comparison and the open question for the owner, how deep the horn goes. A trucast build
is not committed: rebuild it in about 30 s.

## Fixed 2026-11-01: the top batt's wedge

Collapsing the lining meshes broke the top batt, a 48-face box, into a pale wedge. The four-pieces room showed it. A
mesh under 2,000 faces is now never collapsed (`MIN_FACES`), and both files are rebuilt. See
`renders/2026-11-01/barkhorn/top-batt/NOTES.md`.

## Strata's two horns (the owner, 2026-11-01)

"I love the stepping in the loudspeaker but not sure about the horn. Would like to keep both options for the horn but
happy to start with the stepped version." So Strata is the design, and the stepped horn is its lead version.
`tropos-strata.blend` carries the stepped horn.

The smooth formed horn is an option on the same cabinet, caldera and bronze posts:

    python3.11 spinoffs/barkhorn/asset/make_blend.py --design strata --horn smooth --out …/tropos-strata-smooth.blend

The collections are then "Tropos Strata Smooth <tint>". `link_example_strata_smooth.png` shows four. That file is not
committed: it rebuilds in about 30 s.
