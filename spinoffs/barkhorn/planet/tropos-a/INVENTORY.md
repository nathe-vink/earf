# Bar and Planet EARF pictures that show the old Tropos (2026-11-03)

The owner set Tropos on 2026-11-03: base A (its own feet, no plinth, no light) and horn A polished. Every Planet EARF picture made before that shows the earlier cabinet with its stepped horn. Many also stand it on a plinth, and from round 37 most light it from below. This list is for the coordinator; nothing here has been changed yet. `bar-listening.jpg`'s replacement is in `renders/2026-11-03/barkhorn/planet-tropos-a/`.

**Legend:**
- **lit plinth:** a frosted, glowing plinth or wedge, plus the lamps aimed up under the cabinet (`plinthl*`, `plinthb*`).
- **back kick:** a speaker-only lamp behind each cabinet at low height (`spkb*`).
- **plinth:** an unlit pedestal.
- **stepped horn:** the old waveguide.

## In use outside the archive

| Picture | Where it is used | Source on r33-planet-world | Shows |
|---|---|---|---|
| `bar-listening.jpg` | Brand book (r47-brand): `book/img`, `assets`, the Sessions mockup (`scenes/idea-sessions.html`) and launch grid post 6 (Sun 31 Jan) | `renders/2026-10-20/barkhorn/planet38/finals-best/listening-smoke.png` | lit plinth, back kick, stepped horn. **Replaced by this job.** |
| `bar-door.jpg` | Brand book (r47-brand): `book/img` and `assets` | `renders/2026-10-22/barkhorn/planet41/finals/door-mother-colour-p3-1200.jpg` | lit plinth, back kick, stepped horn |
| `bar-street.jpg` | Brand book (r47-brand), `make_book.py` | `renders/2026-10-22/barkhorn/planet39/finals/street-1200.jpg` | lit plinth, back kick, stepped horn |
| `bar-decks.jpg` | Brand book (r47-brand): `book/img` and `assets` | `renders/2026-10-20/barkhorn/planet38/finals-best/coins-decks.png` | lit plinth, back kick, stepped horn |
| `bar-smoke.jpg` | Brand book (r47-brand) `assets` (the Sessions mockup's copies) | `renders/2026-10-20/barkhorn/planet38/finals-best/bar-smoke.png` | lit plinth, back kick, stepped horn |
| `door-hero.jpg` | House Book (the hero) | `renders/2026-10-22/barkhorn/planet41/finals/door-mother-colour-p3.png` | lit plinth, back kick, stepped horn |
| `r42-counter.jpg`, `r42-night.jpg`, `r42-shop.jpg` | House Book (round 42, the 2,800 sq ft house) | `renders/2026-10-31/barkhorn/planet42/finals/{counter,night,shop}.png` | lit plinth, back kick, stepped horn |
| `r43-listening.jpg`, `r43-shop.jpg`, `r43-window.jpg` | House Book (round 43, the pop-up) | `renders/2026-10-31/barkhorn/planet43/proofs/listening-p3.png`, `shop-p2.png`, `window-p2.png` (matched by image) | plinth (unlit, 0.26–0.40 m), stepped horn |
| `r44-street.jpg`, `r44-bar.jpg`, `r44-lantern.jpg` | House Book v11 (round 44, the lantern) | `renders/2026-10-31/barkhorn/planet44/finals/{street-p4,bar-p4,lantern-p3}.png` | plinth (terrazzo, unlit, 0.40 m), stepped horn, cover off |

## The archive (finals and owner reviews, not linked from the books today)

| Folder | Pictures | Shows |
|---|---|---|
| `renders/2026-10-18/barkhorn/planet32/` | backbar, bar, clock-{last,late,opening,sunset}, listening, records, street | plinth (unlit), stepped horn |
| `renders/2026-10-19/barkhorn/planet34/owner/` | bar-p12, listening-p11, street-p13 | plinth, back kick, stepped horn |
| `renders/2026-10-20/barkhorn/planet37/finals/` | bar- and listening- in ember, ice, mixed, smoke; sink; street | lit plinth, back kick, stepped horn |
| `renders/2026-10-20/barkhorn/planet38/finals/`, `finals-b/`, `finals-best/` | bar-smoke, coins-decks, coins-door, listening-smoke, sink, street (and planet38-smoke, the sheet) | lit plinth, back kick, stepped horn |
| `renders/2026-10-22/barkhorn/planet39/finals/` | door, door-mother, street-final (and street-1200/2400) | lit plinth, back kick, stepped horn |
| `renders/2026-10-22/barkhorn/planet41/finals/` | door-mother-colour-p3 | lit plinth, back kick, stepped horn |
| `renders/2026-10-31/barkhorn/planet44/look2/finals/` | street-p4, bar-p4 (pair not in frame), porch-p4, lantern-p3 | plinth (terrazzo, unlit, 0.40 m), stepped horn, cover off |

Rounds 33, 36 and 40 kept only proofs. These show the same arrangement as the round that followed each of them.

## Method

Every `*.shot.json` under `renders/2026-1*/barkhorn/planet*/` (proofs and reviews left out) whose products name `barkhorn-cloud`. For each, the script read:
- its lamps under or behind the cabinet;
- the room's plinth glow;
- the cabinets' heights.

The uses come from:
- the brand book's `make_book.py` and its pages on origin/r47-brand (8001f777);
- the House Book's image folder.
