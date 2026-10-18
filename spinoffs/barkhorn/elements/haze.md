# Haze, concept A: a lavender field at dusk (round 31b)

Set: `haze.py`, pieces in `studio/engine/kit_ext/haze_el.py`. Shots: `studio/shots/barkhorn/element31/haze.json`,
`haze-portrait.json`. Critic replies: `haze-critic/`.

The owner, verbatim (BRIEF.md): "the diorama looks cheap, like a bad video game. I was hoping for more texture in a lot
of these. The speakers are too stark in contrast to the setting too. Tilt shift may have been a bad direction. Lighting
in general in a lot of them is off. ... Maybe don't think about them so much like dioramas, and think more about placing
them in there element, so to speak."

## The concept

The Valensole plateau in early July, minutes before sunset. Rows of lavender run from the lens toward low, rounded hills
that recede in haze; the sun, an orange disc, is sinking into the haze over them. The speaker stands in the path between
two rows on the field's soil, turned 18 degrees, the low sun behind it. An 85 mm lens from 9.5 m at eye level stacks
the rows, the hills and the sun behind the speaker.

References (2026-10-18, WebSearch): Valensole guides agree on late June to July and sunset, with the sun going down
behind the field, and on using the rows' lines for depth
([Jabi Sanz](https://blog.skylum.com/best-photography-spots-in-valensole-by-jabi-sanz/),
[Mickey Shannon, "Valensole Lavender Sunset"](https://www.mickeyshannon.com/photo/valensole-lavender-sunset/),
[Fstoppers, "A purple world"](https://fstoppers.com/media/940829),
[Location Scout](https://locationscout.net/france/1415-lavender-field-in-valensole)). The plateau's lone trees are its
landmarks, so one stands out in the field.

## How it is built

- **Lavender** (`haze_el.field`): no scanned lavender exists on Poly Haven, so each bush is modelled: about 220 leafy
  grey-green shoots with pairs of narrow leaves, under a dome of 140 bare flower stems that arch outward, each ending in
  a spike of 6 to 8 whorls of closed florets (the lowest whorls spaced apart, as on the real spike). Six near variants
  and three lighter far ones; the rows are linked copies (Cycles instances them), each turned, sized and leant at
  random, with colour varying per bush and per floret. A bush takes about 37 s to build, so the bushes are cached as a
  .blend in `studio/assets/cache/haze_el/` (a build then takes 18 s instead of 225 s).
- **Ground**: Poly Haven `farm_soil` at 4k, displaced, under the near rows; beyond 160 m, a far-field material of rows
  as stripes (bloom, leaf, soil) broken by noise.
- **Hills**: three ranges (0.6, 1.7 and 4.2 km), layered-noise height fields laid with `aerial_grass_rock`, tinted.
- **Trees**: Poly Haven `island_tree_01`, a lone oak at 240 m; a line of `island_tree_01..03` at 800 m.
- **Sky and sun**: Poly Haven `the_sky_is_on_fire` (4k), turned so its glow is behind the speaker's left shoulder; the
  sky's sun is behind cloud, so a sun disc (`haze_el.sun`, 20 km off, 0.55 degrees across) sinks into the haze where
  the glow is, and the sun lamp shines from the same place.
- **Haze**: a scattering volume over the plateau, kept low so the sky above the horizon keeps its colour.

## Engine changes (own commits)

- `assets.hdri_sun` reported a sky's sun 180 degrees from where Cycles draws it (bcd5aa4). Cycles looks a map up at
  u = 0.5 - atan2(y, x) / 2 pi.
- `camera.clip_end`: the far clip as a knob, 300 m by default as before (e8a9d4e). The hills are kilometres off.

## Proofs before the critic (0.3 scale)

1. Rows from the left: the speaker read as standing behind a row. Moved the camera into the path.
2. `the_sky_is_on_fire` turned by hdri_sun showed the city: the 180-degree bug, fixed.
3. No hills: the far clip. Hills added, then made low and rounded (the first were alpine).
4. An 85 mm lens from 9.5 m, to compress the rows, the hills and the sun behind the speaker.
5. The sky's sun hides behind cloud: added a disc in the haze. Haze at 0.001 per metre made a flat grey wall; at
   0.00025 the ranges layered.

## Critic passes (proofs at 0.5 scale, 128 samples)

| Pass | Score | Top changes | What I did |
|---|---|---|---|
| h1 | 5.5 (iterate; 7.5 if fixed) | backlight that rims and shadows; a sun that clips and glows; light through the acrylic; the horn's black throat; haze to melt the hills; finer soil; a pale bush; the tree's tangent with the horn | Sun 22, angle 0.6; disc brighter and orange; a light on the sun's axis behind the speaker and two grazing glows at its sides (diffuse only: the first mirrored as a white patch); a reflection card for the horn; farm_soil 4k; the reflector linked to the speaker (it was blowing out the nearest bush); the tree moved 52 m right. Moving the sun to 197 degrees, as asked, put it and the sky's glow out of frame: kept at 188. A taller, denser haze washed the sky to beige: kept low (45 m, 0.0004). |
| h2 | 6.0 (iterate; 7.8 if fixed) | the acrylic as a dark box; the horizon crossing the horn's joint; no warm rim from the sun, a white disc; beige haze; a pale sky; smooth soil; the tree cut by the edge; the horn's studio-bright reflection | Camera down to 0.7 m (the horn now stands against the sky); the light behind the speaker larger and stronger; the sun lamp to 4.5 degrees (over the rows; the disc stays in the sky's glow at 3.4); haze thinner, violet, 80 m tall; sky 0.55, contrast 0.25; clods, pebbles and clippings on the path (`haze_el.litter`), displacement 35 mm; the tree 30 m right; the card dimmer. After merging main (the shared white balance dropped) the frame went salmon: set 5600 K / tint 3 again. A strong sun lamp scattering forward in the haze veiled everything: sun 15, anisotropy 0.3. |
| h3 | 6.0 (iterate; 7.8 if fixed) | two suns (the sky's glow at the right edge, my disc on the left); the cabinet murky; the horn's black throat; a dull disc; no contact; the horizon tangent to the cabinet's top; a dark foreground; the far field ending in a band | The sky's glow is where its sun is, about 20 degrees right of hdri_sun's brightest patch (a cloud): disc and lamp moved there (176, just right of the speaker), sky turned to -165. Back light 9 at 18 degrees, reflector 2.2 then 1.2 (at 2.2, and the card at 0.8, the speaker went white: card 0.35); disc 60; feet 15 mm (no caustics: Cycles' caustics through the lined cabinet would be noise for little); camera 0.45 m then 0.55 m (at 0.45 the hills hid behind the rows); exposure +0.25, vignette 0.1; rows to 400 m, haze 0.0003. |
| h4 | 6.0 (iterate; 7.6 if fixed) | the horn pod blown milky; the front near black; no depth past the speaker at 0.55 m; salmon sky; a clipped sun; uniform clods | **Three passes at 6.0: per the protocol the concept, not the settings, is the problem.** Every pass found the same root: with the sun itself behind the speaker, its face is in shadow and it reads only with lamps that look like its own (a blown pod, a muddy front, two suns). Changed the light: the moment just after sunset. Sky `kiara_9_dusk` (a real dusk, the afterglow low behind the speaker, a range of hazy mountains in the photograph itself), the sun gone (a faint last light, irradiance 2), my hills and sun disc removed, exposure -1.3, a lilac bounce card for the face and a weak afterglow behind. Lavender muted to a dusk violet (#62558E). |
| h5 | 5.5 (iterate; 7.5 if fixed) | the sky blown white; the body crushed dark; the horn far brighter than the body; instanced-looking lavender, too blue; a seam at the far field; weak contact; foreground too sharp | Sky down to 0.26 with exposure back to 0 (the lights on the speaker now count against the sky, not under it); the bounce card larger and stronger (4.5); the afterglow card lower and further (elevation 2, 4 m); white balance 5000 K / 6; haze 0.0005; feet 25 mm; f/2.8; lavender redder and more varied in size (0.75-1.25), lean (7 degrees) and spacing (0.6-1.0 m). |
| h6 | 5.5 (iterate; 7.5 if fixed) | the sky still near white; navy lavender; a hard seam where the field meets the haze; the speaker lit by studio cards (head clips); weak contact; repeated clods; the lone tree beside the head | Sky 0.12 with exposure +0.35; white balance 5600 K / 10; lavender redder (#7A5FB0); the bounce card softer and higher (2.0, elevation 25, 4 x 3 m); the haze from 25 m, 0.0009, 40 m tall; clods halved; the lone tree removed. |
| h7 | 6.0 (iterate; 7.6 if fixed) | the horn a clipped lightbox; no violet on the soil; a black path; a flat cream upper sky; studio lines on the edges; bloom on the horn; the tree line repeats; a seam at the far field | The afterglow card 0.6 and 4 x 2 m; a faint violet pool on the path in front of the feet (a lamp lighting only the set, unseen in the acrylic); the soil tinted drier; the bounce card 8 x 4 m at 5 m, 1.2; bloom 0.12 over 0.92; sky 0.10; haze from 12 m at 0.0012; 14 trees at 800 m in three models, sized 0.6-1.5. No graduated filter: the engine's finish has none. |
| h8 | 5.5 (iterate; 7.5 if fixed) | the cabinet crushed into the lavender's value; the horn pink against a navy body; a hard step at the far field; no colour on the path; the lower half crushed | Not applied: the stopping rule. |

## Stopping, and the duel

Eight blind passes held between 5.5 and 6.0 across both lights: the sunset (h1 to h4: 5.5, 6.0, 6.0, 6.0) and the
afterglow (h5 to h8: 5.5, 5.5, 6.0, 5.5). By the coordinator's rule of 2026-10-18 (after a concept change, stop when
the passes stop gaining), I stopped. The two 6.0 rigs met in a blind duel (`critic/ab/PROMPT-DUEL.txt`, fresh judge,
frames unnamed): **the sunset (pass 4's rig) won, 6.0 to 5.0.** The judge liked its warm backlit sky with a visible sun,
the lavender stems against the sky from the low camera, and the warm graze on the soil; it liked the afterglow's
clearer horn but found its ground crushed and its blue dusk underexposed. The finals are rendered from the sunset rig
(`haze.py` as at pass 4; the afterglow rig is kept in the history, commit 12d8dcc).

## Honestly: where it stands, and what holds it back

A blind critic scores this frame about 6: it reads as a real place (the lavender, the soil and the sky hold up), but
not yet as a photograph a luxury house would run. What holds it back, by the critics' agreement:

- **The speaker's light.** With the sun behind, its face is in shade, and every light I add to model it (the bounce,
  the back light, the grazing glows) reads as a studio card: the horn pod blows to milky pink and the cabinet goes muddy,
  or the reverse. The horn's dark throat (the waveguide seen through the acrylic) reads as a blob in every pass. A real
  photographer would scrim the sun and bounce it from a big reflector; the engine's lamps can't make a reflector's
  falloff look like one, and refractive caustics through the lined cabinet would be noise.
- **No violet on the ground.** The acrylic's colour cast onto the soil never reads at this distance.
- **The far field.** The modelled rows meet the haze in a visible step; a denser haze flattens the sky.
- **The lavender.** Modelled (no scanned lavender exists), it reads as plants but slightly regular and blue.

What I'd try next: a sky with the sun itself in frame and a few degrees higher (so the front gets real skylight), a
photographed lavender scan if one can be had under CC0, a speaker-sized silk scrim between the sun and the speaker, and
the camera turned 20 degrees so the sun rims one side rather than sitting behind.
