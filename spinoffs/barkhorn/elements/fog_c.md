# Fog, concept C: San Francisco you can name (round 31b)

The owner, 2026-10-18: "For fog, what if it was set in a classic foggy SF setting, overlooking the golden gate and the
city from marin headlands, or with sutro and the wall of fog rolling over twin peaks in the background?"

`fog_c.py` (the shot), `studio/engine/kit_ext/fog_c_el.py` (the bridge, the far shore, the city, Sutro Tower, the
water, the fog). The headland is `fog_b_el.terrain`. Built with `python3 spinoffs/barkhorn/elements/build.py fog_c`.

## The set

- **Vantage.** A Marin headland about 110 m above the water, in the spirit of Battery Spencer and Conzelman Road.
  - Camera: 50 mm, 1.1 m up, 5.5 m from the speaker. The speaker is turned 25 degrees toward the low sun at the right.
- **The Golden Gate**, procedural and at real scale:
  - Towers 227 m above the water, each two stepped, fluted legs in five tiers, joined by four portal struts with
    ribbed Art Deco faces above the deck and one below it.
  - Main span 1280 m, side spans 343 m, roadway at 67 m.
  - Main cables on a parabola sagging 144 m, suspenders every 15.2 m, and a Warren-truss stiffening deck.
  - Concrete anchorages and approach piers. International Orange (#B8442C, with a slight patina).
  - The north tower stands about 900 m off on the right third; the south tower is about 2.1 km off.
  - Marin hills hide the north approach.
- **The city.**
  - About 4500 houses massed on its hills, and a downtown of 170 towers.
  - The Transamerica Pyramid (260 m) and Salesforce Tower (326 m).
  - Twin Peaks, with Sutro Tower (three legs, 298 m) on Mount Sutro.
- **The fog.** One volume:
  - a sea under the deck in the Gate;
  - a bank rising from the ocean side (beyond 1.1 km) that engulfs the deck round the towers, leaving their tops
    clear;
  - a wall rolling over Twin Peaks;
  - thin haze for the distance.
- **Light.** The same dawn sky as B (syferfontein 6d), its sun turned to 62 degrees right of the view, low and out of
  frame. One matched sun lamp.

## Proofs (0.3 scale, 24 spp, about 7 min each)

- **c1:** reads as the Golden Gate at once (sent to the coordinator as p0). The north approach and anchorage cut in
  behind the speaker, the near ground is bare, and the fog under the deck is a flat floor.
- **c2:** a full meadow, more billows. The coordinator's notes:
  - the tower sat right behind the speaker's edge and the deck line crossed the cabinet;
  - the fog should be a bank pouring through the Gate round the towers;
  - the clear acrylic read as a grey box.
- **c3:** the tower moved to the right third and the speaker left. But a hill high enough to hide the side span hid
  the city too, and the ocean bank rose as a wall right beside the camera.
- **c4:** the ocean bank now starts 1.3 km out and the hill is lower. The side span crossed the cabinet's top again.
- **c5, c6:** the hill set between the two heights and widened, so the side span runs behind it; a second hill hides
  the north approach. The bank engulfs the deck round the north tower, and the south tower's top stands out.

## Critic passes (critic/PROMPT-promo.md; fresh blind critic each pass, 0.5 scale, 128 spp)

| Pass | Score | Top changes | What I did |
|---|---|---|---|

## Stopped (2026-10-18)

The owner called off concept C before the first critic pass: "Forget the SF fog idea. If we can't make it look like a
real image of the real bridge or real sutro tower, it will look too obviously fake." The pass-1 render was stopped
and nothing was scored. Fog keeps concept B on the site. The proof (p0) is in
`renders/2026-10-18/barkhorn/proofs31/element-fog-c-p0.jpg`, and the rig is here for the record.
