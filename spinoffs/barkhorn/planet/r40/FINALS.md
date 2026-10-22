# Planet EARF round 40: results

The brief (the coordinator, from the owner's answers of 2026-10-22: "Mother EARF: A and B" and "Bar pictures: blurred
figures allowed"): the three heroes again, aiming for 7, with blurred people and the critics' named tells taken out;
Mother EARF stays over a banquette table. Same protocol as round 39. Verbatim JSON and the table are in `critic/`.

**The target was not reached, and no frame reached 6 on both critics, so no full-size final was rendered this round.**

| frame | p1 | p2 | p3 | duels against round 39's best (p1 / p2 / p3) | kept |
|---|---|---|---|---|---|
| door with Mother EARF | 6.0 / 5.5 | 4.5 / 5.5 | 5.0 / 5.0 | 0–2 / 0–2 / 0–2 | round 39's finals/door-mother.png |
| bar | 5.0 / 5.0 | 4.5 / 4.5 | 4.5 / 4.5 | 2–0 / 0–2 / 0–2 | round 40's proofs/bar.png (p1) |
| listening | 5.5 / 5.0 | 4.5 / 4.5 | 5.0 / 4.0 | 2–0 / 0–2 / 0–2 | round 40's proofs/listening.png (p1) |

Renders are in `renders/2026-10-22/barkhorn/planet40/`: proofs (p1), proofs-p2 and proofs-p3, all at 1200 × 800. Read
tests on every pass called every frame a render.

## What held it back

The people. They are built in `kit40.figures`: skinned skeletons in cloth, each body, arm pair and head moving its own
way during the shutter so Cycles draws real motion blur. No CC0 scanned humans are reachable without a login, so they
could not be swapped for scans. Every critic and every duel judge named them first:

- **Blurred hard (p1, a full shutter, 10–30 cm of travel):** "translucent double copies", "composited ghosts". But
  p1 still won both the bar and listening duels against round 39's empty rooms, the only round 40 frames to do so.
- **Held still (p2, a half shutter, 2–4 cm):** "faceless mannequins with ball heads". Worse everywhere.
- **Dark and few (p3):** "grey clay". Still worse than p1.

What would reach 7, by the critics' own estimates (6.5 to 7.5 "if fixed"):

1. **Real people.** Scanned or properly modelled figures with clothes, hair and hands, supplied by the owner. A CC0
   pack, or a licensed one the owner holds, dropped into `kit40.figures` in place of the skeletons. The motion-blur
   rig and the poses can stay.
2. **The altar pair as the hero from the door.** At 28 mm from the door it is about 5 % of the frame. The light alone
   cannot carry it; the critics keep asking for a tighter lens or another frame.
3. **Mother EARF's edges.** Smoke acrylic at night reads as a black cage unless its polished edges catch light. It
   needs its own edge light from the camera side (proposed, not built: a second narrow spot).
4. **The zinc.** It still reads as a pale slab under the Domes. It needs a scanned patina with ring marks.

## What round 40 did fix

The critics stopped naming these:

- the hard stool-shadow fan from the street lamps (the street lamps are off in the interiors, the counter strip down);
- the fir as one texture (`kit40.boards`: every board its own stretch of the scan and its own tone);
- the colour noise (`photo.py`: chroma noise reduction before the lens step).
