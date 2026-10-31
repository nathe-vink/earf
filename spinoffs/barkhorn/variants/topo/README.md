# Topo: the place's data (2026-10-31)

`dem/tam-13-X-Y.png` are nine terrain tiles round Mount Tamalpais's East Peak (784 m), zoom 13, about 15 m a pixel.
They are Mapzen's terrarium encoding: elevation in metres = R × 256 + G + B / 256 − 32768. They come from the Terrain
Tiles open dataset on AWS (`s3.amazonaws.com/elevation-tiles-prod/terrarium/13/X/Y.png`), fetched with no login.

**Sources and attribution** (the dataset's terms): the tiles combine public elevation data, including USGS 3DEP (NED)
and SRTM. Credit "Terrain Tiles: Mapzen and the AWS Open Data programme; USGS 3DEP; SRTM" wherever the Topo horn is
shown or sold. The attribution terms should be confirmed before a product carries the place.

**Files:**
- `topo.py` turns the tiles into each layer's outline (`outlines.json`) and lists the circles walked (`levels.csv`).
- `preview.png` draws all 22 outlines over the air path's wall, the solid line, and a band 45 mm outside it, the dotted
  line.
