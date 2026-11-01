# Four pieces, named for the Earth: the deck's room (2026-10-31 to 11-01)

The owner, on the deck's four-pieces slide: "Would be cooler to show all 4 products in a room together with the labels
and descriptions next to each product in the image, so the point of them going together comes across more. Sleeker,
like a nice furniture magazine." Then, on round 7's slide: "Not lines and dots to things. Everything spaced far enough
out against a neutral enough background that text next to each object is enough. Also should it have a version with
the lights on?"

## The deliverables

**The deck uses the Strata pair** (the owner, 2026-11-01: Tropos starts with the stepped Strata design). The frames
are `four-pieces-strata-{day,dusk}-3840.jpg`, `four-pieces-strata-{day,dusk}-1920.png` and
`four-pieces-strata-{day,dusk}.anchors.json`. They come from the rebuilt asset `tropos-strata.blend` (r33-speaker-horn
c77460f0, where the top bay's lining box is whole again), with the same camera, lights and zones. Only Tropos's zone moves,
by 1-3 px. They carry the last measured pass:
- day: the sun softened so the rug no longer clips; the window as the key light; the skirting a step below the wall;
- dusk: a wall-wash and an uplight even the wall; soft cards on the two speakers; 3100 K.

The files below, without "strata", are the first finals (the round-36 Tropos). The coordinator built the line slide on
them; they are kept as a record.

| file | what |
|---|---|
| `four-pieces-day-3840.jpg`, `four-pieces-day-1920.png` | golden hour, no text |
| `four-pieces-dusk-3840.jpg`, `four-pieces-dusk-1920.png` | lights on, no text; same camera and layout |
| `four-pieces-day.anchors.json`, `four-pieces-dusk.anchors.json` | at 1920 x 1080: each product's box, its label zone (380 x 130), the zone's side and tone, its luminance spread and median sRGB; the header zone (900 x 160); an even patch for the corner note |

All four pieces in Poison. Tropos is the asset `tropos.blend` (r33-speaker-horn 8e44484e), cover off and checked at
render time. Mantle is the floating-plinth build (r32-turntable-final 8f465244), its dust lid off. Hemisphere and Core
come from the lamps' kit piece (r32-lamps-final, round 41's designs), and Core is cordless (`cable: false`,
`cartridge: "in"`). All are at true size.

## How it is made

- `spinoffs/barkhorn/four-pieces/fetch.sh` checks out the other lanes' inputs, uncommitted.
- `four_pieces_v3.py` writes the shots.
- `layout.py` projects each piece through the engine's camera and places the label zones before anything renders.
- `render_fp.py` renders through `studio/engine/render.py` and links Tropos from the asset.
- `room31/post.py` gives the lens finish.
- `finalize.py` writes the frames and anchors.json.

The room is the speaker team's golden-hour room (6770c713), widened to 8.4 m, with its windows out of frame at the left.

## Rounds

| round | what | blind score |
|---|---|---|
| 1 | six proofs: morning, golden hour, blue hour x all Poison, Ice + Dust (two critics) | golden 6.0 / 6.0, morning 5.0 / 5.0, blue hour 4.5 / 4.0; Ice + Dust broke the family |
| 2 | the reading nook by the window, a three-quarter camera | proofs only |
| 3 | no rug | 6 (8 if fixed) |
| 4 / 5 | the critic's fixes; the sun turned so Hemisphere's shadow falls on a speaker (a ray cast found the "caster-less" ellipse was the pendant's) | 6 (7.5); lost both blind duels to the 7.0 golden room, 6 to 7 |
| 6 | re-laid for the owner's ruling: frontal, the lamps forward, zones solved | day 5, dusk 4 |
| 7 | closer (Tropos 430 px tall), shorter credenza, cognac chair, a rug, the furniture whole | day 5, dusk 5 (7 if fixed) |
| finals | round 7's fixes; day's wall warm off-white for dark ink (the coordinator), Hemisphere's zone off the pendant's glow | day 5, dusk 5 (7 if fixed): the gate is not met, and three rounds is the limit for this look; as a slide "mostly yes" (day) and "structurally it does the job" (dusk) |
| Strata | the launch speaker, with the measured fixes from the finals' critics; judged on measurements, no critic round (the coordinator) | day zones sRGB #CFC9BA-#E2D9CA (dark ink); dusk zones luminance 66-113, spread 13-37 (light ink) |

Critic notes are in `critic/`. Proofs are in `proofs/`.

## Known limits

- **Colored shadows.** Tropos's acrylic passes shadow rays through its volume absorber, so its shadows are tinted, but the
  drivers and lining inside darken them. Path-traced caustics from a 1-degree sun through flat sheets do not resolve
  at these sample counts (tested at 256 samples). The green light on the floor at a speaker's foot is real; there are
  no bright caustic patterns.
- **The critics' lived-in layer.** LP sleeves, a throw and books are not in the local CC0 cache. The plant would sit in
  Core's zone.
- **The off-axis camera** that two critics asked for would need every zone re-solved. It is left for a later pass.
