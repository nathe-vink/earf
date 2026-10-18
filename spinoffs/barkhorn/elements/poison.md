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
| 4 | 5.0 | iterate | (A2's first) The ground three times brighter than the speaker (112 vs 40); the acrylic not glowing; no mist or shafts; the log's moss a slab and its end a pink disc; the fly agaric the most saturated thing; the horn crushed | Sky down to 0.45. The sun from the front-left (it lights the lining through the acrylic, so the cabinet glows) through a near-closed canopy with one gap over the speaker and three over the bank. A second card for the horn. Light mist from 3 m back. The log turned across behind, its ends hidden. One small fly agaric at the fern edge. Camera 75 mm at 6.4 m, azimuth +18°, 0.8 m high. Feet sunk 22 mm. |
| 5 | 5.5 | iterate | The floor a flat printed texture brighter than the speaker; no contact occlusion; the log a straight-topped hedge; no shafts; the horn crushed; the trunk a flat wall | Ground albedo ×0.68 and roughness ×0.85 (a `darken` piece). 3D litter within 3.5 m strewn by geometry nodes: bark crumbs, twigs, moss in patches, dense moss banked round the plinth. Found and fixed a `strew` bug where avoid/within were in the object's frame, not the world's. The log turned to recede to the right, its near end under a fern. Sky 0.3, mist 0.06 isotropic from 2.5 m. Canopy gaps on the agarics and a sliver on the trunk. Two agarics lower right, darker and waxier. |
| 6 | 5.0 | iterate | No shafts (the mist a flat wall); no depth behind; the trunk flat with a seam; the horn crushed; moss in rows; the log a black slab; toy agarics in front; the bank grey | The canopy was 70 m across, so a sun from behind at 45° came in under its edge and lit the mist evenly. It is now 220 m, with 1.2 m gaps 5 % open, so shafts show. Sun at azimuth −100°, elevation 42°, irradiance 32, the pool on the speaker's face. Seven trunks 11–34 m back in the mist (density 0.05, anisotropy 0.65). Bark at 1.4 m a tile displaced 9 cm. The log removed. Agarics moved right, into the ferns. Bank tinted green. Reflector at the camera's left, warm bounce above. |
| 7 | 6.0 | iterate | The sun pool on the dirt, not the speaker; the horn crushed; shafts weak; flat fill and a softbox strip on the front; stamped moss mat; no log or agarics visible; the left trunk too big | Sun to −95°, elevation 50°: a sun-only render showed the left ferns shading the front at 38°. Pool 1.9 m across on the speaker. Reflector down to 1.2, warm bounce off, card 0.5, and a kicker behind-left for the horn. Mist 0.08. Five more trunks behind. The near trunk 1.5 m back. A mossy log 3–6 m behind at the right. Agarics on clear duff front-right. Moss thinned into irregular clumps. |
| 8 | 5.8 | iterate | The horn a chrome blob (a white panel and a black void); the body dark (23); no shafts; the trunk a flat wall; the right edge lost; agarics hidden; a stick in front; centred | The pass-8 reflector and kicker mirrored in the horn as softboxes. The reflector is now diffuse only (3.0) and a dim scrim is seen only in reflections, so the horn shows mist, not a lamp. A warm rim behind-right. Sun −110°, elevation 45°. Shafts 7–12 m back at the left, and a sliver on the near trunk, now 6.4 m back with bark displaced 15 cm. Mist 0.13. Agarics on clear duff 0.7 m front-right, and no twigs in a 0.75 m zone in front. Camera azimuth +12° with shift_x −0.12, so the speaker sits right of centre with room for type at the left. |
| 9 | 5.5 | iterate | The horn crushed against dark ferns (11.8); the sun pool's hot spot on the agarics (118), not the speaker; a flat trunk; toy agarics; the right side panel black; dark overall | Stopped here, per the coordinator's rule: two passes in a row after the concept change gained under 0.5 (6.0 → 5.8 → 5.5). |
