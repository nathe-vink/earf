# Tropos campaign stills (2026-10-31)

These are the campaign pictures for the site, the deck and the press, from rigs that passed their critics in round 31,
now with the model as it stands: the round-36 formed horn in its deep lot. Shots are built by
`spinoffs/barkhorn/campaign/shots.py`, and the critic's cards by `campaign/card.py`. The critic prompt is
`critic/PROMPT-promo.md`, blind and in a fresh context, at most three rounds a shot.

Most of the day went to the horn decision instead (`../horn-choice/`, `spinoffs/barkhorn/make/`). The coordinator
reordered the work: the stock colours, the laminated horn, the schedule and the quote requests first. The campaign
stills are therefore not finished.

| shot | state |
|---|---|
| room (a pair at home at golden hour, Poison) | **final: `tropos-room-golden-hour.png`** (2400 x 1350), round 3's look, blind 7.0; look 2 scored 6.5 and was dropped |
| above (the horn from above, Ember) | proofs `above-p1`, `above-p2`; p2 crops the cabinet at the bottom; no critic yet |
| night, inside, corner | not proofed on the new horn yet |

## The room: critic log

| round | image | score | the critic's top changes | what was done |
|---|---|---|---|---|
| 1 | `proofs/room-p1-post.png` | 6.5 | front fill too strong (the covers wash out, the interiors look self-lit); the floor bounce lamp; exposure and sun lower; camera left so the window explains the light; the vase lit flat; a rug for the foreground | c1 to c4, c6, c7 applied (`critic/room-r1.json`) |
| 2 | `proofs/room-p2-post.png` | 6.0 | the horn's grey shadow centre-wall (sun up to 17°); the north fill halved; the rug a cool slab; the sheer clipping at the left; the right speaker crowding the edge; a softer sun | c1 to c7 applied; no other rug texture is in the local CC0 cache, so the same one is tinted (`critic/room-r2.json`) |
| 3 | `proofs/room-p3-post.png` | **7.0** | the rug still a pale neutral slab (its tint does not take: lum 180); the left cabinet in the dim side of the sun (sun azimuth −60, elevation 15); the sheer a white bar; the feet's contact; lift the shaded upper wall for the heading; the vase's green glaze; the right floor corner | **not applied**: three rounds is the protocol's limit for this look (`critic/room-r3.json`, score if fixed 8.1) |

**Look 2** (the coordinator: finish it as a new look). Round 3's changes were applied: the sun into the left cabinet,
the rug darker and warmer, the sheer, the floor's coat, the fills, the vase. One fresh critic scored it **6.5**
(`critic/room-look2-r1.json`):
- the left speaker fell into the shadow of the pier between the windows;
- the rug still read cool grey.

As the coordinator set out, a proof under 7 means round 3's look is the final. The final is rendered at 2400 x 1350,
160 samples, finished with `room31/post.py`, from the shot `room-final` (`shots.py`, `room(critic_round=3)`).

**The rug.** Its tint does reach the shader: Blender's socket lookup takes the enabled colour sockets (checked), and the
COLOR blend sets its hue. It reads cool because:
- the scan is pale;
- the room's cool north fill lands on it;
- PBR Neutral desaturates near-white.

A different texture (a darker wool or jute) is the fix, and none is in the local CC0 cache.

**For a later session:**
- a darker wool or jute rug texture;
- the sun moved so the pier's shadow misses the left cabinet;
- then a fresh look.

The night, inside and corner shots and the top view wait for another session.
