# Ice: a frozen grotto, in glass and wool (round 31)

"Keeps its cool." The ice-blue speaker (`cloud-blue`, cover off) stands on a frozen lake in a grotto of cast-glass
shards, the lake lit from beneath. Set: `ice.py`. Its own kit pieces: `studio/engine/kit_ext/ice.py`.

## The concept

- **Materials.** Glass and wool, nothing else of note:
  - cast-glass shards (convex-hull crystals, flat facets, clear and frosted) for the grotto's wall;
  - a cast-glass lake, clear in places and frosted in drifts of rime, with a faint swell and fine scratches;
  - glass icicles;
  - cotton-wool drifts and wool heaps;
  - folded-and-cut paper snowflakes on threads;
  - a felt snowman;
  - one silver accent (the foil bar of the icon, the snowman's earmuff band).
- **The icon.** Three glass icicles touching under a silver bar, the middle one longest, the proportions of
  `icons.ice()`. It hangs on two threads as a mobile, right of the speaker, in the focus band. It is the "icicles
  hanging from above", made as a model-maker would hang them.
- **One light idea.** The cold glow from under the ice. It is a radial emitter under the glass lake, brightest behind
  and under the speaker, falling smoothly to navy at the walls. Everything else serves it:
  - a soft cold skylight from the front left;
  - a lamp low behind the speaker, light-linked to the speaker alone, shining through its acrylic so its edges glow;
  - silver rims from behind, on the speaker only;
  - a moonlight and a back light on the set only, for white snow tops;
  - a low blue wash behind the shards.
- **Palette.** Ice blue to navy, with white snow. The shadows are lifted toward `#14304F`. The only warm note is the
  snowman's carrot, a few pixels.
- **The joke.** A felt snowman in earmuffs stands beside a loudspeaker.
- **Camera.** 24° down from the speaker's front left (azimuth -30, the speaker turned -10 so its side shows its depth
  and its edges catch the glow). 60 mm at 7 m, f/3.5 at miniature 11, focus through the speaker's front.

## Concepts, and why this one

These were quick proofs at 0.3 scale and 24 samples, kept in the scratchpad.

- **A, the wide grotto** (p01): a wall of tall glass columns, a long flat lake, banks of puffs. It read at once as
  ice, but it was empty, the drifts were plastic balls, and the icicles were off the top of the frame.
- **B, a ledge across the back** (p02, p03): a long frosted ledge with rows of icicles in threes. The straight bar read
  as a pipe across the frame, and the cotton caps on the icicle groups went black.
- **C, the icon as a mobile** (p03 on): one group of three on a silver bar, hung on threads like the snowflakes. It is
  the icon itself, made as craft, and it keeps the frame's top clean. Picked.

## Rounds

1. p01: concept A. The drifts were spheres in a row, so I wrote `drift` (cotton heaped in 3D, squashed balls). The glow
   spheres behind the wall were visible as blobs, so they went.
2. p02 and p03: ledge against mobile. The mobile won. The drifts read as cotton now. Building them with bmesh's create
   ops took the scene build from 12 s to 430 s (the ops slow down as the mesh grows), so `drift` copies one unit ball
   instead: 9 s again.
3. p04: the shards became a rugged cluster (varied sizes, leaning, smaller ones in front). A lamp behind the speaker
   lights its acrylic through. The horn's top blew out, so that lamp went lower.
4. p05: a three-quarter view (azimuth -30, turn -10), so the cabinet shows its depth and its glowing edges. Bigger
   snowflakes, and the bar became silver foil. A hard bright bar showed on the lake beside the speaker.
5. p06 to p08: the bar was the through-lamp lighting the lake. Light-linking that lamp to the speaker's parts cured it
   (`specular: 0` had not). The wall light came down and the pool came up. The mobile moved into the focus band.
6. p09: elevation 18° to 24°, for more lake and a stronger toy look. Making the lake glossier showed the glow discs'
   hard edges (a stage spot), so I wrote `pool`: a radial emitter with a smooth falloff.
7. p10 and p11: the figure-of-eight skate trail meant to be the joke read as a dropped thread. It went, and the
   earmuffed snowman replaced it. The behind-left rim was mirrored in the lake, so it was linked to the speaker too.
8. p12 and p13 (mid): the snowman moved to the speaker's left at the same depth, and soft foreground drifts frame the
   bottom. The small drift touching the speaker's right side moved clear of its silhouette.
9. c14 (full-res crop): the speaker is crisp to its far edges, the horn's rim and the back corners at f/3.5 (f/2.8
   was a hair soft at the horn). The snowman read as smooth plastic, so his felt grain went up to 2.5. The lake read as
   a polished floor, so I wrote `lake`: cast glass with patches of rime, a swell and scratches.
10. p16 (mid): a moonlight on the set alone gives the snow white tops without flattening the speaker.
11. Portrait q01 to q08: `portrait_of`'s key is `lens_mm`. At 80 mm, aimed a little right and up, the snowman and the
    icon both stay in the tall frame. A crystal's top blew out: the rim lamp stood next to it. That rim is now linked
    to the speaker, and a separate set-only back light lights the snow.

## Finals

See the end of this file.
