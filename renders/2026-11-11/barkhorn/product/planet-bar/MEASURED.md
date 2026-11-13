# Lamp colours against the lamps lane's finals (2026-11-11)

Median HSV of a patch at each lamp's centre (hue in degrees, saturation and value 0-1), against r32-lamps-final's
renders/2026-11-10/barkhorn/lamp-site/final/ measured the same way. Exposed as the lamps lane exposes them: AgX,
Punchy, white balance 4000 K; Core alone at EV -1 (its finals'), the wide at EV -1.5 (between Core -1 and Hemisphere -2).

| lamp | frame | ours (h, s, v) | finals (h, s, v) |
|---|---|---|---|
| Core Ember | core-bar-table | 4.9, 0.63, 0.92 (RGB 235 100 88) | 5.0, 0.64, 0.91 (RGB 232 98 86) |
| Hemisphere Acid | bar-backbar | 51.7, 0.19, 0.91 | 52.4, 0.19, 0.91 |
| Hemisphere Ember | bar-backbar | 5.0, 0.35, 1.00 | 5.1, 0.34, 1.00 |
| Hemisphere Dust | bar-backbar | 15.1, 0.31, 0.99 | 16.9, 0.30, 0.98 |
| Core Dust | bar-backbar | 21.9, 0.86, 0.68 | 17.1, 0.60, 0.86 |

All match but the Dust Core in the wide (half a stop under its own exposure: darker and more saturated). What fixed
Core: the lamps lane's own exposure for it (EV -1 and 4000 K, not -5) and its own LED colours (no 4000 K override for
Dust and Acid), with the room's declared light low enough that the ball's glow carries it.

## Round 3 (2026-11-11, after the coordinator's 20:47 notes)

Exposure EV -2.0 in the wide (was -1.5); core-bar-table keeps EV -1 and its room as approved.

| what | frame | measured |
|---|---|---|
| Core Ember centre (h, s, v) | core-bar-table | 5.0, 0.67, 0.90 (finals 5.0, 0.64, 0.91) |
| near Tropos, its lit cabinet face against the record wall | bar-backbar | top 0.70, side 0.26, wall 0.25: face 1.9x the wall (round 2's whole-speaker box 2.45x; now 0.7x, the cone near black pulling it down) |
| near Tropos woofer cone, mean | bar-backbar | 0.21 (grey-white before) |
| covered by nearer things | bar-backbar | near 1.8 % (Mantle's corner, below its foot), far 0.2 % |
| audit (reaudit.py) | both | hidden 0, equipment 0 |

Grey levels are the frame's 0-1 luminance on a 1200 px copy (cabinet top, cabinet side, cone, and a patch of the record wall
between the bays).

## Round 4 (2026-11-11/12, after the coordinator's 22:32 notes)

| what | frame | measured |
|---|---|---|
| Core Ember centre (h, s, v) | core-bar-table | 5.0, 0.67, 0.91 (finals 5.0, 0.64, 0.91) |
| near Tropos cabinet face against the wall; cone | bar-backbar | face 1.8x the wall; cone 0.20 |
| audit (reaudit.py) | both | hidden 0, equipment 0 |

The ball's pale rectangle was the house fill's reflection, a 3 m disc cut flat by the ceiling: in core-bar-table it
is a 1.6 m disc inside the room now (a round soft highlight, as on the lamps lane's own Core). The black square was
the book of matches, out of that frame. The near horn reads by a graduated warm card over its bay, seen only in
reflections (declared in the emitters file). Mantle's plinth is clear Ember acrylic in layers: a narrow low head from
past the frame's right edge passes through it.

## Full size and two test frames (2026-11-12, after the coordinator's 00:33 batch)

| frame | size, samples | file |
|---|---|---|
| bar-backbar | 3200 x 1800, 256 (adaptive 0.005) | 4.5 MB, lossless (the opaque alpha dropped) |
| core-bar-table | 3200 x 2133, 512 | 4.2 MB, lossless |
| bar-backbar-portrait | 2400 x 3000, 224 | 4.9 MB: lossless was 5.4 MB (zopfli), so the lowest bit of channel values under 24 is dropped (at most 1/255, deep shadows only) |
| bar-pendants (test) | 1920 x 1920, 256 | 2.7 MB, lossless |
| mantle-bar (test) | 1920 x 1280, 256 | 1.7 MB, lossless |

| what | frame | measured |
|---|---|---|
| Core Ember centre (h, s, v) | core-bar-table | 5.1, 0.59, 0.94 (finals 5.0, 0.64, 0.91; the patch takes in the soft highlight) |
| near Tropos, whole box against the wall; covered | bar-backbar | 0.79x the wall (the cone near black pulls the box down; round 4's face-only figure 1.8x); covered 1.8 % |
| audit (reaudit.py) | all five | hidden 0, equipment 0 |

Contact edges, checked in full-size crops: the Tropos feet on the bay floor (wide and portrait), the glasses on the
stone (wide, portrait, pendants), Mantle's plinth on the stone (wide, mantle-bar), the Core bases (wide, core-bar-table,
pendants). In the portrait the near Core is close and seen from above: the ball hides its narrower base, and the pink
under it is its reflection on the stone in front of the base.

## The coordinator's 07:22 batch (2026-11-12)

| frame | size, samples | file |
|---|---|---|
| bar-backbar-portrait | 2400 x 3000, 224 (adaptive 0.005) | 4.8 MB; rendered in two overlapping bands (rows 0-52 % and 48-100 %, `--crop`, 68 and 69 min) because the whole frame passes the 2-hour task limit; blended linearly over the 120-row overlap (the bands differ there by 0.7/255 on average: noise); the lowest bit of channel values under 24 dropped to stay under 5 MB |
| bar-pendants | 1920 x 1920, 256 | 2.8 MB; two bands as above (77-row overlap, 0.9/255), lossless |
| mantle-bar | 1920 x 1280, 256 | 1.6 MB, lossless |

- **bar-backbar-portrait:**
  - The Ember Core is no longer the blurred foreground shape. It stands beside Mantle (x 8.17, 0.22 behind the bar's
    front), whole and on its base, in focus at f/5.6.
  - The glasses in front stay soft.
- **bar-pendants:**
  - Five Hemispheres hang in a cluster at staggered heights (1.44 to 1.70 m), each whole in frame with its cap and cord.
  - Two Cores stand under them, with the drinks, the newspaper open flat, a sleeve face up, a linen napkin and the bowl
    of citrus.
  - The stone is unchanged (#1C1916, as the passed frames).
  - The Hemisphere's pools on the dark stone stay faint, because dark stone returns little. The light reads on what
    lies under it. (Corrected 2026-11-13: this said the lamp was an up-lighter. The lamps lane measured it: 73 % of its
    light goes down through the mouth.)
  - The Cores' bases: from this height the balls hide most of them, and the bases read as dark rims under the glow. A
    lower camera would show them; not re-rendered.
  - The flat props: a board at the bar top's own height was coplanar with the stone and rendered black. Each is now
    raised by its thickness. The passed bar-backbar keeps its old matchbook, a black sliver at the throw's edge (not
    re-rendered: the passed frames stand).
- **mantle-bar:**
  - An Ember Core stands just behind Mantle, right of centre and close. The posts read satin black and the bar top dark.
  - The camera is at 1.16 (42 mm, f/2.8). The sleeve is muted (#1C1B1A ground) and further off.
  - **Where the eye looks through the clear Ember plinth at the Core, the plinth reads Ember.** Elsewhere the deck
    reads as a dark form edged by the declared soft key (`mantle-key`, out of frame, high left).
  - So the deck is not wholly Ember: only the band in front of the Core is.
- **Audit (reaudit.py):** all five frames read hidden 0, equipment 0.
- **Contact edges, checked at full size:**
  - the portrait's Core on its base on the stone, and its glasses;
  - the pendants' glasses and props on the stone;
  - Mantle's posts and plinth on the bar top.

## The coordinator's 19:55 batch (2026-11-12)

| frame | size, samples | file |
|---|---|---|
| bar-pendants | 2400 x 2400, 256 | 4.2 MB; two bands (rows 0-52 % and 48-100 %), blended over the 96-row overlap (0.75/255 apart); no Core cable |
| mantle-bar-acid-test | 1920 x 1280, 256 | 1.7 MB: mantle-bar with Mantle in Acid (the Mantle lane's asset, its manifest asserted), nothing else changed |

Mantle's plinth, the median HSV of three patches (hue in degrees, saturation and value 0-1), Ember against Acid:

| patch | mantle-bar (Ember) | mantle-bar-acid-test (Acid) |
|---|---|---|
| deck top, right, under the pendant | 19, 0.47, 0.28 | 32, 0.53, 0.33 |
| deck top, left | 51, 1.00, 0.26 | 53, 0.99, 0.30 |
| deck front edge | 0, 1.00, 0.00 | 60, 1.00, 0.00 |

- **The aim is not met.** Acid reads olive on the top, not lemon, and the front edge stays black.
- **Why:** the only light on the deck is the Ember Hemisphere's, a deep red. Through Acid's yellow it comes out olive and
  dark.
- **The edge stays black** because the camera sees the front edge against the dark under the deck. No light enters it
  from behind or below.
- Audit (reaudit.py): hidden 0, equipment 0.

## The last Mantle test (the coordinator, 22:17)

mantle-bar-acid-test2 (1920 x 1280): as mantle-bar-acid-test, with the Hemisphere over Mantle in Acid too.

| patch | Acid, Ember pendant | Acid, Acid pendant | the aim |
|---|---|---|---|
| deck top, right, under the pendant | 32, 0.53, 0.33 | 32, 0.49, 0.33 | hue 50-60, s 0.40+, v 0.40+ |
| deck top, left | 53, 0.99, 0.30 | 54, 0.99, 0.30 | |
| deck front edge | v 0.00 | v 0.00 | (may stay dark) |

- **Not met; nothing moved.**
- **Corrected 2026-11-13:** this first said the Hemisphere was an up-lighter. It is not. The lamps lane measured 73 %
  of its light going down through the mouth: 348 lux at the centre of a table 0.5 m below.
- **The real reason, per the coordinator:** clear tinted acrylic over a dark bar has nothing light behind it. Light
  passes through the deck into the dark bar and comes back as little colour, whatever the lamp's tint.
- The lamps lane's asset is used unmodified here: its emitters are not changed, and `hemi_scale` is 1.0.
- **Per the coordinator's rule:** Mantle stays Ember in the bar, the portrait included. The Mantle frame is the Ember
  three-quarter at full size (2400 x 1600).

## The hero test (the coordinator, 23:48; 2026-11-13)

bar-hero (1600 x 900, 128 samples):
- **The camera:** from a stool at the bar's middle, eye 1.6 m, 26 mm, centred between the bays.
- **Mantle** is in Ember between the bays, under the passed pendants' cluster, which is raised 0.15.
- **Three Cores:** Acid and Ember at the left, Dust at the right.
- **The props:** the drinks, the newspaper, the citrus, a sleeve and the matchbook.
- **Raised boards:** every flat board on the bar is raised by its thickness. In the first full render the matchbook
  and a sleeve, coplanar with the stone, rendered black.

| lamp | h, s, v | the passed pendants |
|---|---|---|
| Hemisphere Ember (two) | 4.9, 0.38, 1.00 / 4.8, 0.37, 1.00 | 5.2, 0.41, 1.00 |
| Hemisphere Acid (two) | 51.9, 0.23, 0.88 / 51.8, 0.23, 0.88 | 52.9, 0.23, 0.87 |
| Hemisphere Dust | 15.3, 0.36, 0.97 | |
| Core Acid | 52.4, 0.68, 0.59 | |
| Core Ember | 8.4, 0.95, 0.74 | |
| Core Dust | 20.5, 0.85, 0.70 | |

**How it was measured:**
- The Hemispheres: the brightest fifth of each lit shade, just under its centre point (the point itself falls on the
  black cap).
- The Cores: a 12 px patch at each ball's centre.

**Checks:**
- Nothing stands in front of either speaker: Mantle and the Cores sit below the line from the eye to the speakers' feet.
- Audit (reaudit.py): hidden 0, equipment 0.

## The Mantle frame at full size (the coordinator, 22:17 and 23:48; 2026-11-13)

mantle-bar (2400 x 1600, from the same shot as the 1920 x 1280 frame): Mantle in Ember, the cleaned Tropos, no Core cable.

| lamp | h, s, v | the lamps lane's finals |
|---|---|---|
| Core Ember (in frame) | 5.1, 0.67, 0.90, no clipped channel | 5.0, 0.64, 0.91 |

- **How it was measured:** a 12 px patch at the ball's centre.
- **The Hemispheres:** all five are above the frame. They light the deck but are not seen, so they are not measured here.
- **Audit (reaudit.py):** hidden 0, equipment 0.
