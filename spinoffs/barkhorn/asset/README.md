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

## The approved build (`tropos-strata.blend`, since 2026-11-11)

`tropos-strata.blend` is now built from the site's own frames: each tint exactly as `rollout.py` builds the site's tall
front (`shots.site('front-off-tall', tint)` with `TROPOS_BASE=A`, `TROPOS_HORN=polished`): base A on its swivel feet
(`feet-base`, `feet-stem`), the line's tints and linings (Smoke the neutral grey, 50 % through 20 mm, its lining
#18181B), the polished horn (0.05), the black rods, no plinth and no light. The collections keep their names (Tropos
Strata Ember ... Smoke). `tropos-strata.manifest.json` lists, per tint, its parts and each material's key values
(base colour, roughness, transmission, IOR, the volume's colour and density, the lining's colour), so a scene that
links it can assert itself against the approved build as `shots._approved` does.

    python3.11 spinoffs/barkhorn/asset/make_blend.py --design site --name 'Tropos Strata' \
        --out spinoffs/barkhorn/asset/tropos-strata.blend --manifest spinoffs/barkhorn/asset/tropos-strata.manifest.json

The sections below describe the file as it was before (Strata on the lit plinth); `--design strata` still builds that.

## Strata, the leading proposal (`tropos-strata.blend`, until 2026-11-11)

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

Since 2026-11-01 both files carry **stock TruCast sheet's tints**, the owner's choice ("I like the darker colors").
- Each cabinet is in its code, with its TT held at 20 mm. Smoke is 2074 Dark Gray.
- Each horn is in its cabinet's code at 12.7 mm, except Dust, Acid and Ice. Their horns keep the site's deep horn, a
  heavier batch, by the owner's "Deep, like the site".
- The calibration is `tints.py` / `tints-trucast.json`, applied to the line's eight flavors in `product.py`. Every
  rebuild carries it, so `--tints trucast` now gives the same files.
- `TINTS.md` has the decisions, the earlier comparison with the site's lighter tints, and one doubt: Haze's 2287 is
  listed as translucent, not transparent.

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

## Horn A (2026-11-03): `tropos-strata.blend` rebuilt

The owner's pick on 2026-11-03 ("Horn: A, smooth", its outside polished since 15:14) is now the default. `tropos-strata.blend` carries the
smooth formed horn (the waveguide in satin, the throat, pod, cap, pads and saddle formed) on Strata's bronze posts, with
the caldera, on base A (the plinth) with its uplight (option `Plinth uplight`; the base question is open, see
`variants/BASES.md`). The collections keep the plain names, **Tropos Strata Ember** through **Smoke**. `--horn stepped`
builds the stepped horn as "Tropos Strata Stepped <tint>".

**The horn is never collapsed any more.** Horn A is clear acrylic with an absorbing volume. A collapsed mesh can open it,
so light would leak out of the horn. The biomes lane asked whether the acrylic volumes close, and the rebuilt file was checked:
- every clear panel (front, back, sides, top, bottom, both braces) closes once its glTF split vertices are welded: no
  open edges, a positive volume, so the normals face out;
- the waveguide, pod and cap close the same way. The throat has 222 edges shared by three faces but no open edge, so it
  is watertight;
- the clear material's shadow rays cross its surface and still absorb in the volume.

So the file is 42 MB, not 23. The plates' print, the screws and the lining's voile webs are still collapsed.

## Horn A's outside: satin or polished (a feasibility note, 2026-11-03)

> **Decided: polished** (the owner, 2026-11-03 15:14: "Can we do satin on the horn interior and polish on the exterior,
> or does that add build complexity? If so just go polished"). A satin inside would need the outside masked and an even
> blast into the narrowing throat, a step on every horn. So the horn is polished outside and in. `FORMED_HORN_SATIN` in
> `product.py` is 0.05; the material keeps its name, `horn-satin`.
>
> **The inside, plainly:** it is the face that touches the plug, so it takes the plug's finish. It comes off glossy only
> if the plug is. The risk register already asks for the plug sealed, sanded to 600 and polished, and wiped before every
> shot (F3). On the prototype's tooling-board plug, expect a slightly duller, faintly textured inside, with any dust or vent
> marks printed into it. On the production aluminium tool, polished, expect a good gloss. No extra step on the horn
> itself, but the plug's polish is now a look item, not only an acoustic one. Buffing the inside afterwards is possible
> only near the mouth, never into the throat or near the joint. The forming trial should judge the inside's gloss under a
> raking light against a limit sample.

**Why this matters.** The owner misses "the old renderings of the horn where the thicker parts of the acrylic got darker, almost giving it a glassy feel".
- The biomes lane's proxies show where that depth comes from: a polished outside. With the satin outside, the horn glows evenly, and thick and thin look the same. Closing the mesh changes nothing (63.2 against 63.4 mean luminance).
- Polished (roughness 0.05), it is about 2.5 times darker. The throat reads deep, and the posts show through.
- Satin is the owner's own spec ("Horn: A, smooth, satin outside", 2026-11-03 03:00), so this is the owner's question. The manufacturing answer, plainly:

**Which face touches the tool.**
- The horn is pressure-formed from 10 mm cell-cast acrylic over a **male plug** (`make/horn-risks.md`). The plug touches the **inside**, the air face.
- The **outside is the free side**: it touches only air at about 4 bar. So the outside comes off the press with the cast sheet's own gloss. A polished outside is the formed part as it is; satin is the extra step (a bead blast).

**What would show on a gloss outside.**
- Dust that lands on the free side before or during forming prints as small pits or specks. Gloss shows them; satin hides them. The press needs the clean room the risk register already asks for (F3).
- Slight ripple or orange peel from uneven heating, mostly at the mouth's corners, which form last. Gloss shows it under a raking light.
- Webbing (F2) is a reject either way.
- Mark-off from the plug's vents and texture (F3) is on the inside and doesn't change.
- Handling scuffs after forming: trimming, annealing and assembly need a protective film or soft cradles.

**Polishing a formed part.**
- **Flame polishing** isn't used on a large formed face. It stresses cast acrylic and risks crazing near the cemented joints (A1); it's for edges only, away from the cement.
- A gloss outside is kept as formed and touched up locally by hand buffing, a few minutes of compound on a soft wheel, about **$10-20 a horn**. A full hand buff of the whole shell, if the free side comes off hazy, is about 0.5-1 h, **$30-60 a horn**.
- The bead blast for satin is about **$15-30 a horn** plus masking. Gloss, kept as formed, costs about the same as satin or less, but its reject rate for specks and ripples is higher. The forming trial (`make/forming-trial.md`) should judge the free side as well as the corners.

**Why satin was chosen.** It was the owner's look ("smooth, satin outside"). It also hides the free side's specks and ripples, fingerprints and fine scratches. That second reason is real, but it's a by-product: satin was not chosen to hide defects.

**In use.**
- **Gloss** shows fingerprints and fine swirl scratches. Both polish out with plastic polish, as on any acrylic speaker.
- **Satin** hides fingerprints, but oil can leave darker patches, and a scratch shows as a shiny line that can't be buffed out without re-blasting the panel.

**Tooling.** No change. The plug shapes the inside either way: $6,925 for the prototype plug and base, $14,465 for the production aluminium tool.

**What it changes in the light.** On a gloss outside, the volume's absorption reads: thick parts (the throat, the pod) darker, the mouth's thin lip lighter, and the posts and the woofer's top visible through it. On satin the surface scatters first, and the horn glows evenly in its colour. The frame pair is in `renders/2026-11-03/barkhorn/base-question/gate2/`: `A-ice.png` (satin) and `A-ice-polished.png`.

## The polished horn's see-through: build proposals for the owner (2026-11-03)

The polished close-up (`renders/2026-11-03/barkhorn/horn-closeup/horn-A-polished.png`) passed the coordinator's gate 2 SHOW, 1 HOLD: honest, premium, the best the horn has looked as a material. It reads busy through the polish in three places. **These are proposals only.** Nothing in the model changes while the roll-out renders from 5295e58f, and a change comes after, with the owner's yes.

| what reads busy | the critics' proposal | already true in the model? |
|---|---|---|
| The pod's outline breaks into petal-like lobes and nested rings, "a dark glass knot", bulging past the right rim from that angle. | One simple round pod, centred on and flush to the throat, in matte black or dark bronze, with a crisp front edge or a thin bronze ring. A matte-black sleeve over the driver's body. Generous corner radii where the flare meets the throat. | **The pod is already one simple round pod**, 200 mm across (`pod_r` 100, 130 deep), centred on the throat. But it is **clear, in the horn's own tinted acrylic** (`horn-formed`). The lobes and rings are refraction: the driver's dark body, seen through the flare's corner fillets and then through the clear pod wall. A matte black or dark-bronze pod (or a black sleeve on the driver inside a clear pod) would show as one dark round shape, and the outline would calm. The flare's corner radii at the throat are the formed shell's; making them more generous changes the plug, a tooling item. |
| The driver's ringed throat part reads as a bright silver "lens". | Finish it dark or bronze. | Not yet. The driver's exit and band are bright metal (`driver-bright`), as the bought driver comes. A dark or bronze exit means a painted or anodised part, or a dark ring between the driver and the throat. |
| The rear posts read dark blue through Ice, not bronze. | One clean diameter into the pod, matching bronze ferrules at both ends, behind the flatter middle of the horn's bottom wall, away from the tight curve by the right rim. | **Mostly true already.** The posts are ø16 bronze, one diameter into the horn's pads, with turned bronze collars at both ends (`strata-collars`). The rear pair stand near the middle (x 240 and 320 of 560), behind the flatter part of the bottom wall. They read blue because they are seen through 10 mm of Ice acrylic: that is the material, not the parts. Bronze only reads as bronze where it is outside the horn. |

**For future close-ups:** use deep focus. That frame was at f/8, and the right rear post's top fell out of focus as a smudge. f/16, or focus between the throat and the posts, holds both.
