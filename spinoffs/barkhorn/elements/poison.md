# Poison, concept A: a redwood rainforest (round 31b)

*Green, and not the healthy kind.*

## The direction

- **The owner, verbatim:**
  - "Poison could be more of a witch's garden … Or a mossy, ferny redwood forest with a fallen log and poisonous mushrooms. It's important to stay on the theme of earth and placing the speakers in their respective atmospheres."
  - "The poison one should be in a more lush fern and redwood rainforest."
  - On round 31's dioramas: "looks cheap, like a bad video game … Maybe don't think about them so much like dioramas, and think more about placing them in there element."
  - "Continue to do critic passes until you feel it's in a good enough place for promotional images for a $20K product."
- **The coordinator's brief for Poison A:** a real, lush redwood and fern rainforest. Towering fibrous trunks rise out of frame, with layers of ferns, moss over a fallen log, and a few poisonous toadstools at most. Light comes down in shafts through mist, and the green acrylic catches the shafts and stands clear of the green around it. The camera stays at eye level.

## References

Prairie Creek, Jedediah Smith and Del Norte Coast Redwoods State Parks, and Fern Canyon:

- sword fern and redwood sorrel under the redwoods, and mossy nurse logs;
- deeply furrowed cinnamon-red bark;
- thin cloud or lifting fog for soft light, with one morning shaft through mist (the Ossagon Trail photographs).

## Concept proofs

- **A:** a 45 mm lens at 4.6 m, the speaker centred among ferns with trunks behind.
- **B:** 55 mm from the speaker's right, the speaker on the right third and backlit.

**Chosen: A.** B put the speaker at about 80 % of the frame's height and cut its feet, while A gave the forest room to read as a place. A's camera has since moved to 65 mm at 6.2 m (pass 1).

## The set

- **Sky:** Poly Haven `misty_pines`, a misty pine forest, which reads as the distant forest behind the fog.
- **Trunks:** modelled redwoods (`kit_ext/poison_el.redwood`), buttressed and fluted, in Poly Haven `metasequoia_bark` (the dawn redwood) tinted toward the coast redwood's cinnamon.
- **Ferns:** Poly Haven `fern_02` scans, each placed singly (`plants`).
- **Ground:** Poly Haven `forest_leaves_02`.
- **The log:** modelled (`mossy_log`), with ambientCG `TreeEnd005` for its cut end and ambientCG `Moss004` over its back, carrying Poly Haven `moss_01` sprigs strewn by geometry nodes (`strew`).
- **Fly agarics:** modelled (`toadstool`).
- **Mist:** a scattering volume (`mist`) behind the speaker only.
- **Shafts:** a canopy sheet unseen by the camera (`canopy`), its gaps placed so a shaft lands on the cabinet.

## Engine changes

`studio/engine/assets.py` (47a08ef, on main as 9e9ac89): Poly Haven's plant glTFs mask their leaves with a JPG's alpha, which doesn't exist, so the leaves rendered as solid cards. Their own Alpha map is now wired in.

## Concept A2 (from pass 4)

Concept A1 was a deep misty grove built entirely from modelled trunks. Three passes scored 5.5, 5.5 and 4.5: the mist turned the modelled trunks into grey flats, which read as CG at once. A2 keeps the rainforest but lets a photograph carry the distance. Poly Haven's `mossy_forest`, a lush mossy rainforest, sits out of focus behind (rotation 180°). A modelled bank of moss and ferns rises 4–9 m back to hide the seam with it. In front stand one redwood with truly displaced bark at the left, the mossy log, the ferns, the duff and two fly agarics. It is lit by the sky's own sun (`sun_from_sky`) and a reflector. The A1 set stays in `poison.py` as `shot_misty()`.

## Critic passes (blind, a fresh subagent each, critic/PROMPT-promo.md)

| Pass | Score | Verdict | Main changes asked | What I did |
|---|---|---|---|---|
| 1 | 5.5 | iterate | the sun through the acrylic; the horn crushed black; the log a flat hedge; toy agarics; heavy left ferns; no separation from the trunk; 65 mm f/2.8; more contrast | Sun to azimuth −150°, elevation 28°, with a canopy gap on the cabinet. A big reflector at the camera's right for the horn. The log turned end-on, moss on top only. Two agarics. Thinner left ferns and a near frond at the right. The central trunk 1.5 m back. Camera 65 mm f/2.8 at 6.2 m, 0.85 m high. Finish contrast 0.10, clarity 0.08, vignette 0.22. Then my own fixes: mist down to 0.055 (it greyed the trunks), white balance 5300 K, redwood tint, a trunk that blocked the sun moved, more ferns behind. |
| 2 | 5.5 | iterate | The cabinet still in shade (lum 41) and the same value as the trunk behind; bark smooth; flat decal twigs; clone ferns; the log's end a clean disc | A sun-only render showed the backlight lit only the left panel: the lining stops it reaching the front. So the sun moved to front-left (azimuth −68°), the speaker turned −20° toward it, and the camera moved to +10°. The trunk behind moved aside, 11 trunks added in layers, mist 40 m deep and lit by more sky. All four fern plants with tilts. Bark at 0.8 m with bump 2.4. |
| 3 | 4.5 | iterate | Mist erases the trunks into grey flats (the strongest CG tell); bark without relief; moss edge stepped; toy agarics; no glow through the acrylic | Three passes with no gain, so per the brief the concept changes (below). |

