# Hiddencast: the lamps lane's pictures (2026-11-09)

**The rule** (the coordinator, 19:13): no light, card or panel may stand in frame hidden from the camera. The one
exception is a practical's bulb inside its own opal or frosted fitting. A hidden object outside the frame is fine.

**How it is measured:** a 96 x 96 grid of rays through the frame, lens shift included, padded 3 % past each edge (the
speaker lane's `shots.card_coverage`, r33-speaker-horn ac9e5568). Each ray is tested against each hidden object's whole
shape, occlusion ignored. The share in the tables is the share of those rays that hit it.
- `hiddencast_bpy.py` for the bpy-direct rigs (`lamp_site.py`, `lamp_pictures.py`). It runs in their audit modes
  (`AUDIT=1`, `CARD_AUDIT=1`) and covers meshes with camera visibility off and every lamp with camera visibility off.
- `shotcast.py` for the studio-engine shot files (the cordless set, lamps-unlit). It covers area, panel, point and spot
  lamps without `camera`, and flags and bounces.

## lamps-unlit (on the site and in the Brand Book)

`renders/2026-10-31/barkhorn/lamps-cordless/p4-lamps-unlit.png`, shot `studio/shots/barkhorn/lamps-cordless/p4-lamps-unlit.json`.

| Object | Kind | Where | In frame | What changed |
|---|---|---|---|---|
| bounce | area lamp, 0.8 x 0.5 | (0, -0.60, 0.30), between the lens and the orb | **100.0 %** | slid back along the line from its target to (-0.03, -1.38, 0.56), x2.3 (1.84 x 1.15), irradiance held: 0.0 % |
| back | area lamp, 0.6 x 1.2 | (0.35, 1.0, 1.1) | **9.9 %** | removed: along its line it reaches the sweep's back before it leaves the frame |
| thru_orb | area lamp, 0.16 x 0.16 | inside/behind the orb, facing the lens | **6.7 %** | removed: it was the orb's "pale core", a fake that cannot leave the frame |
| thru_dome | area lamp, 0.30 x 0.18 | behind the dome, facing the lens | **8.0 %** | removed, for the same reason |
| key, fill | area lamps | orbits at 2.6 and 3.0 m | 0.0 % | none |
| bgwash | area lamp, 6 x 4 | overhead | 0.0 % | its specular 0 removed (ruling 1): now seen in reflections |
| edges | area lamp, specular only | right, out of frame | 0.0 % | none (ruling 1's exception: a specular-only lamp, dimmed as a whole) |

**Result:** 0 hidden objects in frame. The new frame is `renders/2026-11-09/barkhorn/lamp-site/lamps-unlit.png`, from
`lamps_cordless.py --unlit-real` (shot `lamps-unlit-real.json`).

**Two visible differences:**
- **The orb's lower half reads black, not pale.** The "pale core" was the hidden thru_orb lamp. The site's caption says
  "a pale core" (web.py: 'dark, polished acrylic with a pale core'). Copy unchanged; the owner or coordinator decides.
- **A bright ring at Core's foot.** This is the contact dock's ring, drawn into the CAD on 2026-11-01 (ef23b82d), after
  the old frame was made. It shows with or without the wash's reflections (checked both ways).

## The cordless lit set (still in site-img until the honest site set replaces it)

| Shot | Hidden | In frame |
|---|---|---|
| p4-lamp-orb-&lt;each of 8&gt;, core-dock-ember | 6 | `pool+0.00` point lamp (r 0.06, a coloured pool at the base's front, transmission off) 17.7 %; `ball` point lamp 3.5 % |
| p4-lamps-orbs | 12 | `bases` area lamp 9.9 %; eight `pool` point lamps 0.7 % each |

- **ball** is a bulb inside its own frosted ball: ruling 3's exception.
- **The pools are faked light.** These are the pictures the honest site set (`lamp_site.py`) replaces. They are not
  re-rendered here.

## The round-2 site rig (`lamp_site.py`), from the start

| Frame | Hidden | In frame |
|---|---|---|
| dome-&lt;colour&gt; | key, fill (out); cob-&lt;colour&gt; (practical, 0.0 %) | 0 |
| orb-&lt;colour&gt; | key, fill (out) | 0 |
| lamps-domes, lamps-domes-7 | key, fill (out); 8 or 7 COBs (practical, 0.0 %) | 0 |
| lamps-orbs, lamps-orbs-7 | key, fill (out) | 0 |

No meshes are hidden from the camera. Every mesh casts shadows.

## The night and day pairs (`lamp_pictures.py`, the finals awaiting the gate)

| Frame | In frame before | What changed |
|---|---|---|
| core-ice-night-frost, core-ice-night-nested | 0 (fill, dusk-left out) | none |
| core-ice-day, core-ice-day-nested | 0 (window-sky out) | none |
| hemi-ice-day | 0 (window-sky out) | none |
| hemi-ice-night | **dusk-back 22.4 %**, **kicker 4.1 %** | dusk-back is the dusk sky behind the back wall's opening, seen through it: now visible to the camera, a lit sky behind the sheer. The kicker cannot leave the frame under the 600 mm drop's ceiling: removed. Now 0 in frame. |

The committed hemi-ice-night final (2fb64db3) carries both. It needs a re-render before it passes.
