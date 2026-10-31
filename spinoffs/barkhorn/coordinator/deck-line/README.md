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
