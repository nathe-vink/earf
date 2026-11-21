# The horn 360 on the house ground: the proof (2026-11-20)

Ember, frames 0, 6, 12 and 18 of the 24-frame turn, 1200 x 1080, made by `spinoffs/barkhorn/campaign/horn_turn.py`.

- **What each frame is:** the Ember front's own shot file
  (`renders/2026-11-04/barkhorn/rollout/A-polished-tallr7/site-front-off-tall-ember.shot.json`: its sweep, every lamp,
  its sky, render settings and finish block) with only two things put in from the 10 Nov turn (370de3da,
  `A-polished-p2-p2b/turn-ember-NN`): its camera (125 mm on the horn) and the speaker's turn (115 degrees + 15 a frame).
- **Time:** 10, 11, 10 and 12 minutes a frame (96 samples).
- **Audit:** hidden 0, equipment 0 on all four, from the masks and from `reaudit.py`.
- **The ground:**
  - the four corners read 93.3 (top left), 93.4 (top right), 90.5 (bottom left) and 94.8 (bottom right);
  - they move by 0.4 L* at most from frame to frame;
  - the Ember front's ground reads 92.6 to 93.4 away from its darker top left (78.5);
  - the turn's camera frames the horn and the cabinet's top, so no floor, shadow or reflection is in frame.
- **Size:** at full size the driver's dome rings and screws are a touch crisper at 1200 than at 960 x 864. The site's
  667 x 600 slot asks 1334 px on a 2x screen, so 1200 comes closer.

## The Ember turn, all 24 frames (2026-11-21)

`turn-ember-00` to `turn-ember-23`, 1200 x 1080, 96 samples, made as above. `contact-ember-24.png` shows them in
order, six to a row, frame 0 at the top left. (`contact-sheet.png` is the four-frame proof.)

- **Time:** 10 to 13 minutes a frame.
- **Audit:** hidden 0, equipment 0 on all 24 (each frame's `.equipment.txt`).
- **The ground** (L*, the 60 x 54 px corner boxes):
  - The top corners read 93.3 and 93.4 to 93.5 in every frame. They never move more than 0.06 L* from one frame to the next.
  - The bottom right reads 94.6 to 94.9.
  - The bottom left reads 90.5 to 90.6, except in frames 4, 5, 8, 9, 10, 15, 16, 17, 20 and 21. In those frames the
    cabinet's corner reaches into the box as the speaker turns, not the ground.
- **The loop:** frame 23 runs into frame 0 at the same 15-degree step as every other pair.
