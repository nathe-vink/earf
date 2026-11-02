# Deck "line" slide builder (coordinator)

The owner asked for the four pieces in one room, "with the labels and descriptions next to each product in the image…
Sleeker, like a nice furniture magazine." The room picture comes from the four-pieces lane (r48-four-pieces); this
builds the deck section around it.

- `line_build.py spec.json outdir` writes `slide.html` (the deck section, image `/_blob/<id>`) and `preview.html`
  (local image and fonts), and prints a contrast report. Each text block's ink is picked from the picture under it:
  dark ink (#1C1A18) on light ground, light (#F4F1EC) on dark; anything under 4.5:1 is flagged.
- `shoot.js preview.html out.png` renders the preview at 1920x1080 with Playwright (fonts: Instrument Sans and
  IBM Plex Mono from Google Fonts, saved locally next to the builder as `fonts/local.css`).
- `spec-example.json` is the first layout on a stand-in (it had pin lines to each product).
- **Owner ruling (6a93885f): no leader lines or dots.** The room is re-laid so each piece has an even, neutral label
  zone beside it, and a label next to each object is enough. The builder draws no leaders unless a spec sets
  `style.leaders`; labels are placed in the four-pieces lane's label zones (anchors.json). Two versions: golden hour
  and lights on.

Copy (American English; no starting color; Tropos cover off; Core cordless):
Tropos, Speaker, "A powered horn loudspeaker." / Hemisphere, Pendant, "A shade that swaps in a quarter turn." /
Core, Table lamp, "Cordless, about five hours a charge." / Mantle, Record player, "Floats on its own light." /
foot: "A render. Shown in Poison, one of eight colors."

## Effective contrast with the halo (2026-11-01)
`line_build.py`'s worst-case figure ignores the halo, so a dark frame can report under 4.5:1 while it reads well. To measure what is
actually rendered: `node shoot_pair.js out/preview.html A.png B.png` (B is the same frame with the text transparent and its shadows kept),
then `python3 eff_contrast.py spec.json A.png B.png`, which compares each block's glyph cores against the halo-darkened ground under them.
The final dusk frame (specs/spec-final-dusk.json: all labels light, halo `0 0 16px rgba(20,16,14,0.7), 0 1px 3px rgba(20,16,14,0.55)`)
measures 7.0 to 13.3:1 on the labels and 4.7:1 on the corner note.

The stock-tint dusk frame (specs/spec-final2092-dusk.json, the four-pieces lane's final-2092 dusk, 416eb5e6, near-black Tropos
cabinets with deep green horns): same zones, inks and halo; 7.0 to 13.3:1 on the labels and 4.7:1 on the corner note. Deck v46.

The Strata Float day frame (specs/spec-final2092sf-day.json, the four-pieces lane's final-2092-sf day, 11a1d8bf; slide kept as
specs/line-day-sf.html, image /_blob/1506c4659a39015266edad449a224397): dark ink, no halo; 7.7 to 12.2:1 on the labels. The corner note
sits on the rug's mid tone, where the builder's muted ink measured 3.9:1, so a spec can now set `foot.color` (here #1C1A18: 5.5:1).
Kept as the alternative; the deck shows the lights-on room.

**Current (deck v49):** the Strata Float dusk frame (specs/spec-final2092sf-dusk.json; the four-pieces lane's final-2092-sf dusk,
02877dad; slide kept as specs/line-dusk-sf.html, image /_blob/43138711dfedd8f3150f6dddaa84a527): Strata Float v3 and Hemisphere v3,
Mantle's label 10 px lower with its zone; 7.0 to 13.3:1 on the labels, 4.7:1 on the corner note. Day alternative: line-day-sf.html.

**Current (deck v54):** the colors F dusk frame (specs/spec-final2092sf-f-dusk.json; four-pieces cebd67c8, Tropos from the speaker
lane's F build 2bf9b217; image /_blob/4ea7f045fc25019c094415bb41e7b366): Tropos as lit green glass over the white lining; Mantle and
the lamps still stock Poison (their match is being checked). Same zones and inks; 7.0 to 13.4:1 on the labels, 4.7:1 corner note.
