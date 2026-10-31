"""Fetch the photographed CC0 texture sets the new-object scenes use into studio/assets/cache/ (gitignored; a fresh
clone runs this once). Sources and licenses: TEXTURES.md. Uses the studio engine's Poly Haven fetcher.
    python3 fetch_textures.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'studio', 'engine'))
import assets
SETS = ['oak_wood_planks', 'beige_wall_001', 'marble_01', 'book_pattern']
for aid in SETS:
    maps = assets.texture(aid, '2k')
    print(aid, len(maps), 'maps')
