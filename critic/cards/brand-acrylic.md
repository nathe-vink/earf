# Card: the EARF globe in acrylic (round 25, after critic round 3)

## What it is for

EARF makes horn loudspeakers whose cabinets come in tinted cast acrylic. Its mark is a 3D globe: three parallels and
three meridians, the axis leaning 23.4 degrees, tipped 22 degrees toward the viewer. In colour each ring is a flat disc,
flush, no strokes (the "discs" style): the equator blue, the meridian facing the viewer green, north red, south yellow, the
side meridians orange and violet. The globe is its six discs alone, with no fill completing the circle (its outline is
the discs' own).
The acrylic style is the same discs as tinted acrylic sheets. Sheet 1 shows each style in every rail (black only,
white only, one colour, multicolour on paper and on ink); sheet 2 shows the acrylic moving (the globe spinning on its
axis, on ink); sheet 3 shows the discs and the acrylic large, side by side.

## The owner's requirements, in their own words (fixed)

- "I liked the acrylic idea if it looked more like actual acrylic where the crossing primary colors created secondary
  colors." (round 24)
- "The acrylic is meant to be a transparent version of the discs but it looks very different." and "Push it further."
  (round 25)
- "For the discs, I want them to not have strokes, so they are flush. The strokes should be the non-color versions."
  (round 24b, of the discs style)
- The logo "has to work in white only, black only, single color, multicolor and animated." (round 21)
- "For acrylic I was expecting each disc to have a little thickness to it." and "for both discs and acrylic there's
  this artificial green completing the circle shape that isn't one of the discs." (round 25, after round 3)

## Fixed

The globe's geometry and the six colours; the discs and lines styles.

## How the acrylic is made, and its parameters

After round 3: where a disc is, the ground takes nothing; where none is, the ground shows (no ball is filled). The
meridian facing the viewer, green, is the backing, as the discs have it. Wherever coloured discs lie in front of the green, they share all of
what shows, nearest first: the nearest keeps `face`, the next `face` of the rest, and the farthest what is left (at
0.5 a crossing of two is the same colour whichever is in front, as filters are). Where no coloured disc lies in
front, the green keeps `green` and the back halves behind it share the rest, as ghosts. The sheets are stacked, not
mixed like paint, in OKLab: a and b the share-weighted mean, so opposed tints cancel toward a smoky grey; the
lightness the darkest sheet's, lowered by `dark` for each sheet beyond the first and by `smoke` times (1 - R), where R
is the mean's chroma over the mean chroma (1 for one hue, near 0 for opposites). So every crossing is darker than
each of its sheets, and one sheet shows its own flat colour, as in the discs. Behind the green the back halves count
as one sheet (a ghost is at most one step deeper). Paper and ink match inside the rim. In the SVGs each region is one
flat colour (regions within OKLab 0.012 of each other merged); on screen it is drawn per pixel on the graphics card by
the same rule (supersampled 4 times); without WebGL the flush discs are drawn instead.

- `face` 0.5 (round 1: 0.45 paper, 0.55 ink; round 2: 0.72 paper, 0.80 ink; round 3: 0.72)
- `green` 0.8 (round 3: 0.9)
- `dark` 0.04 (from round 3)
- `smoke` 0.10 (new after round 3)
- `thick` 0.05 (after round 3, the owner's note): each disc a slab this thick (of the radius); where its side faces
  the viewer it shows as a crescent along one edge, in a deeper tone of its tint (`side` 0.10 off the lightness,
  `sideC` 0.15 more chroma), stacked with the sheets it is seen through like any sheet
- `edge` 0 (round 1: each disc's edge in full colour, 0.045 of the radius; read as strokes). A thin glint, 0.012 of
  the radius, is the owner's option.
- In one colour (black only, white only, a speaker's own) the acrylic is the lines (strokes at 0.075 of the radius)

You may propose additions (kind "new"), with exact values.
