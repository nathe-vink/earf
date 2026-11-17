# Smoke f, a dispersed trail (2026-11-17): references and the A/B proof

The owner, 17 Nov: "The smoke trail still doesn't look dispersed enough. Use reference shots of stuff burning in the
atmosphere or something, and account for time having passed since impact."

## References (links only; no photos copied)

- Chelyabinsk 2013, the train minutes on: a wide, sunlit band, kinked where its upper part met different winds; satellite views show high winds pulling it apart. <https://www.planetary.org/space-images/chelyabinsk-meteorite-trail>, <https://cimss.ssec.wisc.edu/satellite-blog/archives/12356>, <https://www.space.com/19802-russian-meteor-blast-photos.html>
- Persistent trains: last minutes to over an hour; wind shear with height bends them into corkscrews, loops, right angles and bright knots. <https://arxiv.org/html/2407.18344v1>, <https://www.nasa.gov/blogs/watch-the-skies/2018/12/20/fireball-leaves-persistent-train-over-western-skies>, <https://cires1.colorado.edu/science/groups/chu/pubs/documents/2002JGR_Drummond_MeteorGloworm.pdf>
- Rocket trails at twilight: upper winds twist them into knots within minutes; sunlit from below the horizon. <https://apod.nasa.gov/apod/ap240312.html>, <https://en.wikipedia.org/wiki/Twilight_phenomenon>

In common: much wider than the body that made them, widest and most sheared high up; kinks where the wind changes
with height; densest in knots and fading to nothing at the edges, the sky through most of it; lit warm on the
sun's side at low sun. (A zigzag itself was not confirmed by a source found here.)

## What the scene allows

Only the last ~10 m of the main trail above the crash is in frame (t 0 to 0.009 of its 975 m; it leaves the top at
x ~2200). So the kinks and spread have to happen in that stretch, and the trail lies at 10-20 m from the camera,
inside the depth of the column (which spans about 4 to 16 m).

## A and B (trail props 11 and 12; settings in the commands under the scratch run, summarized)

- A: radius 0.4 m at the crash (2.4x w1), widening to 2x by the frame top; optical depth through the core ~0.4
  (w1 ~1.4); edge [1.2, 0] with gamma 2; warp 0.3 one octave; puffs 0.8 at scale 0.3, puff_detail 1, soft;
  shear kinks +-0.3 to 0.85 m every ~2 m of height, growing upward, plus a 0.8 m downwind drift; low end fades
  over 4 m.
- B: radius 0.65 m (3.8x), depth ~0.3, kinks x1.7, drift 1.3 m, puffs 1.1, low end over 5 m.

## Result

Neither reads as a trail. Wherever the see-through trail lies behind the column's thin outer smoke, that smoke's
fine lumpy texture (bright lit lumps over the darker trail) shows as a curdled speckle. The w1 trail hid it by being
opaque; its "scalloped edge" was most likely the same texture at the trail's border. Changing the trail's own lumps
(puff_detail 6 to 1) did not change the speckle, so it is the column's, not the trail's.
