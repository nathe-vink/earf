# Acid: acid rain, in glass and resin (round 31)

*A yellow with opinions.*

## The concept

A plump wool cloud, the cream of a lemon's pith, hangs over the speaker and rains on it. The rain is the stop-motion
trick: each drop is the Acid icon's drop (a ball and the cone tangent to it, `icons.tongue`) cast in lemon resin with the
icon's two bubbles inside it as air, hung on a fine thread. Below, a wet chartreuse varnish with domed pools of lemon
resin, ripple rings on them where drops have landed, beads of acid standing on the ground and a few glass bubbles. The
speaker stands in its own pool.

- **Light, one idea:** a low sun behind the rain (a round area lamp, 15 degrees up, opposite the camera). It comes
  through the drops, the pools and the speaker's golden acrylic, and its glare on the wet ground sits behind the speaker
  as a halo, which separates it from the distance. A soft high light from the front keeps the cloud and the speaker's
  face from going dark.
- **Palette:** chartreuse ground (lifted into olive, `#3E4A0C`), lemon resin, the cloud's pale lemon; the speaker's
  gold is the warmest thing in the frame.
- **Craft vocabulary:** resin and glass (drops, pools, ripples, beads, bubbles), wool for the cloud, paper for the one
  joke. No felt, no fabric, no paper landscape: those are the other sets'.
- **The joke:** a paper cocktail umbrella, lemon and white, stuck in a pool of acid. The sour, served.

## The earth setting

The owner, through the coordinator: stay on the theme of earth, each speaker in its own atmosphere; story elements are
subtle nods, not the subject. This set is a place: acid rain falling on a wet plain with rolling hills behind it,
under its cloud. The umbrella is the one nod, small and to one side.

## Concepts (why this one)

The first proofs tried three grounds under the same rain: a pale lime paper sweep (p1: flat, a hard sweep line, the
speaker dull), a bright wet lime floor (p2 to p4: dreamy but washed out, the middle a glare), and a deep chartreuse
varnish (p5 on). The deep ground won: the lemon drops, pools and the gold acrylic glow against it, and it is the
"slightly toxic" half of "candy-like, slightly toxic".

## Proof rounds

| Proof | What changed | Why |
|---|---|---|
| p1 | first set: a sweep, flat resin pools, small drops | it read as acid rain at once; speaker dull, pools brown, sweep line, cloud cropped |
| p2 | stage with a 60 m varnish floor, gumdrop resin hills far back, stronger backlight, sun only | dreamier; a white rectangle on the floor |
| p3 | more and bigger drops (0.11 to 0.19 m), fill moved to a high front light | the rectangle stayed: it was the sun shining through a gap between the hills |
| p4 | sun moved in front of the hills | gone, but the middle washed out |
| p5 | ground deepened to chartreuse `#6F8A14`, cloud creamier | colours now glow |
| p6, p7 | sun lowered, then a round (DISK) lamp opposite the camera | its glare on the wet floor became a halo behind the speaker instead of a hard rectangle beside it |
| m1 | mid proof, glare tamed (lamp specular 0.35), front light up | pools read as flat paper, rings as drawn lines, cloud heavy |
| p8 to p12 | pools as luminous resin, rings softer; the umbrella (a kit piece of striped paper gores), turned until it reads | the joke reads at a glance |
| m2 | mid proof | pools too flat, two pools merging into one blob, empty foreground |
| p13 to p15 | domed pools (surface tension), ripples raised onto the dome, the speaker's pool smaller and separate | liquid, not stickers |
| c1, c2 | crops on the speaker, with and without depth of field | the horn's rim was soft from the depth of field, not refraction |
| m3 | focus moved up and back (0, -0.08, 0.9), miniature 12 to 10, lens 58 to 64 | horn rim and back corners crisp; speaker 41 % of the height |
| p16, p17 | glass beads on the ground (read as grit), then lemon resin beads | the ground reads wet |
| m4 | cloud lower and smaller (headroom), halo up (specular 0.6), beads thinned | the landscape signed off |
| pp1 to pp4 | portrait: lens 48 to 94 from the same place, target raised | speaker 35 % of the 4:5 frame, cloud and umbrella kept |

## Final settings

- Landscape `acid.json`: 2400 x 1600, 256 samples, camera 24 degrees down, 18 to the speaker's left, 7.2 m, 64 mm,
  f/2.8 at miniature 10, focus (0, -0.08, 0.9); kit_scale 11.
- Portrait `acid-portrait.json`: 1600 x 2000, the same set and light, 94 mm from the same place, target (-0.42, 0.1, 1.1).
- Lights: sun (DISK 2.4 m, 22 W/m^2 at the speaker, `#FFE070`, specular 0.6), front (64 degrees up, 4.0), rim (125 degrees round, 3.0).
- Finish: bloom 0.3, vibrance 0.16, lift 0.04 in `#3E4A0C`, vignette 0.25.
- Render times: see below.

## Environment note

The container's default Python is now 3.13 and `bpy` 5.0.1 has no wheel for it, so `studio/setup.sh` failed at the
bpy step. bpy 5.0.1 installed on `python3.11` (`python3.11 -m pip install bpy==5.0.1 "numpy<2"`) and every render here
ran as `python3.11 studio/engine/render.py ...`. Nothing in the repo was changed for it.

## What I'd still improve

- The ground is one flat colour of varnish; a faint pour texture (resin levelling waves) would make it richer.
- The cloud is a good wool puff but a plain one; a few loose wisps of fibre at its edges would sell the wool.
- The drops' air bubbles are barely visible at this size; larger bubbles in the nearest drops would carry the icon.
