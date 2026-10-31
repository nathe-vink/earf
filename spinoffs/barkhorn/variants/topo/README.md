# Topo: the place's data (2026-10-31)

`dem/tam-13-X-Y.png` are nine terrain tiles round Mount Tamalpais's East Peak (784 m), zoom 13, about 15 m a pixel.
They are Mapzen's terrarium encoding: elevation in metres = R × 256 + G + B / 256 − 32768. They come from the Terrain
Tiles open dataset on AWS (`s3.amazonaws.com/elevation-tiles-prod/terrarium/13/X/Y.png`), fetched with no login.

**Sources and attribution.** The dataset's attribution page (tilezen/joerd, `docs/attribution.md`) gives the
terms:
- **US data, USGS 3DEP (formerly NED):** public domain.
- **SRTM:** public domain (NASA and NGA, distributed by the USGS).

For US data the required line is: *"United States 3DEP (formerly NED) and global GMTED2010 and SRTM terrain data
courtesy of the U.S. Geological Survey."* When the hosted tiles are used, credit Mapzen as well.

Carry the line *"Terrain: 3DEP and SRTM data courtesy of the U.S. Geological Survey, via Mapzen Terrain Tiles (AWS
Open Data)"* wherever the Topo horn is shown or sold: on its page, in its manual, and on a small etched line under the
horn's boss.

**Files:**
- `topo.py` turns the tiles into each layer's outline (`outlines.json`) and lists the circles walked (`levels.csv`).
- `preview.png` draws all 22 outlines over the air path's wall, the solid line, and a band 45 mm outside it, the dotted
  line.
