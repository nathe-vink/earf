# The globe's turn on a transparent ground (2026-11-10)

120 straight-alpha RGBA PNG frames, 512 x 512, f0000 to f0119: half a turn, 1.5 degrees a frame, a seamless loop at
30 fps (4 s). f0000 is the still mark's pose (spin 0). The A3 colors (brandbook/review/2026-11-10-globe/
A3-translucent-matched-colors.hues.json) in the approved look: the key's reflection at 0.4, the fill out of
reflections, the plain grey room; no ground plane, a transparent film (film_transparent_glass on).

    python3.11 globe_real.py --spin-frames DIR --frames 120 --px 512 --transparent --hues-file .../A3-translucent-matched-colors.hues.json

Checked: no near-white pixel (all channels >= 245) in any frame; the brightest 0.1 % moves at most 3 levels between frames.
