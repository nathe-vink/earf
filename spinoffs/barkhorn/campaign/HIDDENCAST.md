# Hiddencast: every object the camera cannot see, by rig (2026-11-09)

The coordinator's rule (18:37): no object in frame hidden from the camera, but a practical's bulb inside its own fitting.
`hiddencast.py` lists each shot's hidden objects (flags and bounces without `camera`, reflect-only cards, panel lamps
without `camera`, area lamps) with the share of the frame each covers by ray-cast (`shots.card_coverage`), and counts as
a violation any lit one that covers more than 0 %. Lamps at 0 are left out (they emit nothing and have no surface).

Generated from the rollout's own shot files at this commit (A, polished, Smoke held), c2's rigB back (15626b64), and
the re-lit close-ups (1bdbf2fc). `shots.realize_hidden` now runs in the four site frames (tall, wide, hero-light, side)
and the arc: every hidden flag or bounce becomes real (seen by the camera and in reflections, casting shadows), and one
in frame, or a lit lamp in frame, slides out along the line from the speaker or its target, grown to hold its angle
(an irradiance holds; watts gain the square); one that cannot leave the studio goes.

| rig | shots | hidden objects (max) | shots clean | in frame and hidden (worst coverage) |
|---|---|---|---|---|
| deck-cover | 1 | 11 | 0/1 | area lamp face 100.0 %; area lamp cyc 77.1 %; area lamp strip 14.6 %; area lamp smoke 1.0 % |
| deck-hero | 1 | 28 | 0/1 | area lamp horn 58.7 %; area lamp edge 3.0 % |
| deck-home-portrait | 1 | 3 | 0/1 | area lamp bounce 100.0 % |
| deck-home | 1 | 3 | 0/1 | area lamp bounce 95.0 %; area lamp north 39.4 % |
| deck-row | 1 | 9 | 0/1 | area lamp back-top 18.7 %; panel front-strip 4.2 % |
| site-back-<k> | 7 | 11 | 0/7 | area lamp horn-rim 8.6 %; area lamp wash 5.0 % |
| site-front-off-tall-<k> | 7 | 27 | 7/7 | - |
| site-front-off-wide-<k> | 7 | 24 | 7/7 | - |
| site-hero-light-<k> | 7 | 8 | 7/7 | - |
| site-side-<k> | 7 | 25 | 7/7 | - |
| amp-plate-<k> | 1 | 5 | 1/1 | - |
| back-mark-<k> | 1 | 11 | 0/1 | area lamp fill 2.8 % |
| coin-<k> | 1 | 1 | 1/1 | - |
| coins-eight | 1 | 1 | 1/1 | - |
| horn-back-<k> | 7 | 5 | 7/7 | - |
| inside-<k> | 1 | 5 | 1/1 | - |
| joinery-<k> | 1 | 9 | 0/1 | hidden flag 3.1 % |
| macro-amp-<k> | 1 | 9 | 1/1 | - |
| macro-corner-<k> | 1 | 9 | 1/1 | - |
| macro-grip-<k> | 1 | 9 | 1/1 | - |
| macro-horn-<k> | 1 | 10 | 1/1 | - |
| spin-<k> | 63 | 8 | 63/63 | - |
| studio-dark-<k> | 1 | 10 | 0/1 | panel horn-front 54.9 %; area lamp glow 35.9 %; panel horn-back 2.1 %; panel strip-right 0.4 % |
| turn-<k> | 168 | 3 | 168/168 | - |
| site-back (rigB, c2 15626b64) | 1 | 11 | 0/1 | area lamp horn-rim 8.6 %; area lamp wash 5.0 % |
| horn-A-front-polished | 1 | 27 | 1/1 | - |
| horn-A-front-satin-outside | 1 | 27 | 1/1 | - |
| horn-A-side-polished | 1 | 25 | 0/1 | panel sidesheen 32.3 %; lamp-rig flag flag_right 4.8 %; area lamp edge 3.8 % |
| horn-A-side-satin-outside | 1 | 25 | 0/1 | panel sidesheen 32.3 %; lamp-rig flag flag_right 4.8 %; area lamp edge 3.8 % |

**Passed or rendered pictures that carried a violation** (before this commit), for re-gating:
- The seven talls: the `horn` area lamp between the camera and the horn, 71.2 % of the frame.
- The wides (c4 rc1 80aa5bb3): key 11.3 %, horn 5.5 %, pool 4.7 %, scrim panel 4.3 %, fill 1.3 %, paper 1.5 %,
  bg-left 0.5 %, kick 0.1 %.
- The sides (b00945ab): horn 10.2 %, pool 0.7 %.
- The hero-lights (c3 2318a4cc, c2 7d599d6a): a white bounce 58.9 % between the camera and the speaker, a flag 11.8 %,
  the ring-card panel 3.0 %.
- The arc proofs (34b40201): flags 11.7 % and 1.6 %, ring-card 0.3 %, bg-left 0.2 %.
- Not fixed here (their rigs live elsewhere or wait on the coordinator): the backs (rigB, c2), the deck's five frames,
  the side close-ups, studio-dark-ember, back-mark-fog, joinery-ember.
- Clean: the turns, the horn-backs, the amp plate, inside, the four macros, the coins, the front close-ups.
