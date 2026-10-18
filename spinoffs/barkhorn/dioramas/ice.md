# Ice: a cabin beyond the frozen pond, in glass, wool and balsa (round 31)

The owner, verbatim (relayed by the coordinator during the round):

- "Ice could have a snow covered wood cabin in the back, or maybe the speaker is in the abominable snowman's cave home."
- "It's important to stay on the theme of earth and placing the speakers in their respective atmospheres, though the
  yeti and witch ideas are fun, subtle nods."

"Keeps its cool." The final has the ice-blue speaker (`cloud-blue`, cover off) on a frozen pond lit from beneath, in a
snowy clearing at night. A balsa log cabin stands soft in the distance, with cotton snow on its roof and a warm window.
Felt pines stand behind it, with wool hills beyond. The yeti is only a nod: a trail of big snowy footprints crosses the
ice past the speaker toward the cabin. The first concept, the natural ice grotto, is kept as a landscape alternate with
the same footprints (`ICE_WORLD=grotto`, `ice-grotto.json`). Set: `ice.py`, with `WORLD` choosing. Its own kit pieces:
`studio/engine/kit_ext/ice.py`.

## The final, and why the cabin

Both directions came out well (k06 against g01). The cabin is the owner's own picture. It is also more plainly an earth
setting, a place in the snow rather than a set of crystals. Its warm window gives the cold frame one accent and a
story, and the footprints lead the eye from the speaker to the door. The grotto is cooler and more abstract. It is the
better object study, but the cabin is the better campaign image.

- **Materials.** These were the cabin world's materials:
  - balsa logs, interlocked, with plank gables;
  - a thick cotton snow blanket on the roof;
  - a card window frame and chimney;
  - three-tier felt pines with cotton caps;
  - a felt snow blanket over the clearing;
  - wool hills;
  - the rimed glass pond with cotton banks;
  - paper snowflakes on threads.
- **The icon.** The cabin's front eave carries the icon's three icicles (the middle longest) among smaller ones. The
  grotto alternate keeps the icon as a silver-bar mobile.
- **Light.** The pond's under-glow is the one idea, as in the grotto. The window is the warm counterpoint, with a
  point lamp on the snow in front of it.
- **The nod.** The earmuffed snowman I had made way for the yeti's footprints, to keep one joke per surface.

## Rounds after the direction changed

12. w-cabin against w-grotto (first proofs). The cabin was cut by the frame's left edge, and the trees were too near
    and too big. The snowfield's mounds left a hard ellipse edge and a navy gap where the bed showed through.
13. k02 and k03: the pond became a rectangle of rimed glass. The snow is four felt boards round it, their seams under
    cotton banks. The cabin moved to the upper left, inside the frame, and the pines moved back and got smaller.
14. k04 and k05: the speaker's feet were cut by the frame's bottom, so the target came nearer and lower (0.1, 0.3,
    0.88). The footprints grew to 0.46 m.
15. k06 (mid): the footprints' toes floated off the sole, so the toes moved in, a little thinner than the sole so that
    no face lies on another. The eave icicles grew, and the left snowflake moved off the cabin's corner.
16. Portrait kq01 and kq02: at 70 mm the speaker was a quarter of the frame. At 90 mm, aimed left, the cabin sits upper
    left, the speaker lower right and the footprints lead in from below.

---

The first concept, the grotto, follows as it was written before the direction changed.

# The alternate: a frozen grotto, in glass and wool

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
