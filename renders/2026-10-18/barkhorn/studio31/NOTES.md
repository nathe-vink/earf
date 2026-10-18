# studio31: the launch-page set, critic passes

Prompt: `critic/PROMPT-promo.md` (critic v2 for campaign images), a fresh blind subagent each pass, given only the
image, a card (the frame's purpose, the fixed product, the shot's settings) and `critic/measure.py`. Replies in
`critic/`.

| pass | frame | size | score | top changes | what I did |
|---|---|---|---|---|---|
| h1 | hero-dark-ember | 2560 full | 5.5 | reflection too long; edges untraced; horn crushed; glow blue-grey; seam trough | strips re-aimed where the faces mirror (by `--probe`), glow larger and warm, cove radius 3.4, key 1.9, fill 0.6, a second sheen |
| h2 | hero-dark-ember | 1280 proof | 5.0 | right face flooded white by the strip; sheen clips the front's top; horn black; reflection a smear; too big in frame | strip-right 0.08 m at 113, left 30; sheen 2.2; a panel through the horn from behind; strip-top forward; the floor's reflectance 0.06 (new `sweep.specular`); 60 mm, more room above |
| h3 | hero-dark-ember | 1280 proof | 5.5 | too small now; horn reads as chrome; right edge black; magenta cast; floor a void | three passes within half a point, so the concept moved: the glow became a backlight (0.8 m, 650 W) that the acrylic glows against, a charcoal floor (#1A1A1A, rough 0.3, specular 0.035), closer (6.6 m), tint 0; strips 24/34, sheen 1.2, horn backlight 16 |
| h4 | hero-dark-ember | 1280 proof | 5.5 | horn washed pink; front salmon; glow a spotlight ellipse; horizon cut; cyan wall | sheen 0.45 (top band only), key 1.4 at -55, glow 380 W 75 deg aimed lower, cove radius 5, floor specular 0.06, strip-top over the horn, 6000 K, fill 0.85; the horn's pink traced (lamp by lamp) to its backlight panel: 16 -> 4 |
| h5 | hero-dark-ember | 1280 proof | 5.0 | horn mouth a black void; clipped flank; right face brown; floor smear, no contact; glow an edged disc; sharpen fringe | a bigger sheen and a card in front of the horn for its mouth to mirror, strip-top 18, key 1.1, fill 1.4, strip-right 44, a crisp faint floor (rough 0.08, specular 0.04, core contact 0.7), glow 1.4 m 260 W 110 deg, floor #242424, sharpen 0.12 |
| l1 | hero-light-ember | 1280 proof | 5.5 | seamless too dark and green; no contact; right face maroon; horn blob; soft edges; internals busy (out of scope) | held for the dark hero's rig to settle |
| h6 | hero-dark-ember | 1280 proof | 5.0 | horn chrome; front and side equal; right edge dark; floor a full mirror; glow a horizon band; olive cast | horn card large and faint (whole-horn ramp), horn backlight 10, key 1.6 / fill 0.55, strip-right at 98 and 50, strip-left 16, floor rough 0.2 spec 0.025, glow 2 m higher and neutral, 5800 K tint 4 |
| h7 | hero-dark-ember | 1280 proof | 5.0 | horn face pink-white, throat black; front salmon; blue-grey glow; right edge soft; floor smear; horizon band | horn card 0.2, sheen 0.8 (ramp to 0.6), glow warm-neutral lower and wider, tint 0, floor rough 0.12 spec 0.03, strip-top forward; tried strip-right at 105 (floods the face again, as in h2) and the horn backlight at 22 (pinks the horn again, as in h4), so kept 98 and 8 |

Seven passes on the dark hero scored 5.5, 5.0, 5.5, 5.5, 5.0, 5.0, 5.0 (the light hero 5.5): a plateau, and the passes
contradict each other on the floor (a faint smear vs a crisp mirror), the size, the strips' aim and key against fill.
What every pass names and none can fix with light is the product: the horn's mirror gloss and its dark throat, and the
internals seen through clear sides, listed as out of scope each time. The finals are rendered from h7's settings.

## Round 31c: concepts, by duel

The coordinator called the plateau and asked for two classic ways of shooting coloured clear acrylic, cover on, from
the look book's three-quarter direction: bright field on white (the iMac G3, the Cube) and dark field on black. Blind
duels (`critic/ab/PROMPT-DUEL.txt`, random order, 1280 proofs, Ember), replies in `critic/duels/`:

| duel | A | B | scores | verdict |
|---|---|---|---|---|
| 1 | bright field, cover on | h7 | 4.0 / 6.0 | h7 |
| 2 | h7 | dark field, cover on | 5.0 / 2.5 | h7 |
| 3 | h7 | bright field, cover off | 4.8 / 5.6 | bright field |

**For the record: both cover-on duels read the cover's flat cloth disc as "a placeholder"** (duel 1: "a flat,
unshaded red disc with no cone, surround or dust cap"; duel 2, the black cloth: "a hole or missing part"). The
catalogue's cover-on views face the same reader.

Bright field with the cover off is the studio set from here (the coordinator: the eight heroes, the lineup and the
macros all from its rig, named hero-light-<colour>); hero-dark-ember.png stays as the record of the h7 rig.

| pass | frame | size | score | top changes | what I did |
|---|---|---|---|---|---|
| b1 | concept-bright-ember | 1280 proof | 5.5 | mint cast; a flag's grey wedge on the left; no coloured light thrown; front face matte; woofer a hole; small; light contact | 5600 K tint 5; left flag moved in, background lamps 4 m wide; a graduated front strip; a lamp high behind; a bounce card facing the woofer; 70 mm; softer, longer contact |
| b2 | concept-bright-ember | 1280 proof | 5.5 | cabinet brick-red, not glowing; right face milky (mirrors the sweep); thin contact; cool white; driver blob | background lamp aimed through the cabinet's line of sight, 2.8; back lamp 5 at 175/38; right flag where the right face mirrors; contact 0.8 over 0.45 m; camera down to 0.75 m; white balance by measure (5100 K turned it blue, 6600 K yellow; 6100 K tint 4 gives 250/250/244) |
| b3 | concept-bright-ember | 1280 proof | 5.5 | a grey line on the sweep (flag 2 reached below the floor); cabinet dense brick-red; hairline contact; no coloured spill; woofer flat | flag lifted; background lamps 3.0/4.2; a soft bank behind (1.2 x 1.6 m, 15 deg up, 6.0); contact 1.0 over 0.6 m with a 25 mm core; scrim smaller and behind the horn's top; key specular 1, front strip higher; 5750 K tint 2. Not done: a fake coloured spill lamp (the engine has no caustics; a lamp coloured per flavour would be a cheat a retoucher would not need) |
| b4 | concept-bright-ember | 1280 proof | 5.5 | the sweep's end showed (24 m wide); background lamps fill the floor, no cast shadow; cabinet dull; green white; horn pink | sweep 44 x 20 m, cove radius 5; background lamps behind the speaker's plane, aimed low at the wall; key 3.2, 1.6 m, 38 deg; back bank 10 at 8 deg; white balance measured (tint 7 at 5900 K: 249/248/246) |
| b5 | concept-bright-ember | 1280 proof | 5.5 | the right flag blacked out the whole side, then a milky band; contact thin; front maroon; no key shadow; top-left smudge; denoise soft | right flag a 0.3 m strip on the rear edge; contact 0.8 over 0.7 m, core 8 cm; back bank 14 at 5 deg; key 4.0, 1.2 m; background lamps 3.6 each; sweep 52 m; left flag matte (no dark lobes in the horn); finals at 128 samples, adaptive 0.01 |

Five passes on bright field held at 5.5, as seven on the dark rig held at 5.0 to 5.5. Every pass's top items turned out
to be real set bugs (a flag's shadow, the sweep's end, a flag reaching below the floor, a flag filling a face), each
fixed; the score did not move, and every pass names the same out-of-scope items: the busy internals seen through the
clear sides, the horn's black driver, the horn's colour against the cabinet's. That is these judges' ceiling for this
product as it stands, not the light's. The finals are rendered from b5's rig.

Finals: the first five heroes showed a grey wedge in the top-left corner, the left flag's shadow on the cove (gone with the flag off, the left edge still traced by the sweep's own falloff); the flag is off and those five and Haze are rendered again after the rest.
| n1 | lineup (final, 2880) | full | **6.0** | the front bounce card cast a grey band and a cool grey foreground; no contact; a horizon line; the black horn crushed; no coloured light on the floor; tight margins | bounce cards reflection-only (no shadow) plus a high one for the horns' shoulders; cove radius 9, background lamps aimed at its foot; the back bank high behind and aimed through the cabinets onto the floor in front (each throws a pool of its own colour); 58 mm; floor roughness 0.32 for a faint reflection. Rendered again |
| b6 | hero-light-ember (rig 1769c6a: the colour thrown on the floor) | 1280 proof | **6.0** | contact weak; right edge soft; lower bays milky; the white flat with no depth; a clipped edge line | the first move off 5.5 in twelve passes; the finals render from this rig (helpers h1-h3 restarted on it); its changes are left for a next round, not to restart the finals a third time |
| f1 | hero-light-ember **final** (2560, rig 1769c6a, helper h1) | full | **6.5** | no contact core under the feet; the coloured pool streaky, fanning left; right face salmon, its edge soft; top-left corner greyer; horn throat | next round: contact core 0.75 at 4 cm, strength 0.6; back lamp at 52 deg, 16, 1.4 m (a compact pool); right flag wider; front strip ramp to 0.7, bounce off the right face; bg-left aimed higher |

Duel 4: f1's changes proofed (contact core, a compact pool at 52 deg, wider right flag, softer scrim) against the f1
final downscaled to the same size: **the final won, 6.5 to 5.5**. The judge preferred its saturated red spill on the
floor and the horn's crisp specular streaks; the proof's softer light read milky and pink. The finals keep rig 1769c6a.

## Passes on the finals (bright field, rig 1769c6a)

| pass | frame | score | top items |
|---|---|---|---|
| n2 | lineup (final, with n1's changes) | **6.5** | contact still faint; floor flat 248; grey patches in both bottom corners (the bounce card's reflection ends); black unit's edges weak; cabinets milky |
| m | macro-horn-acid | 5.5 | an overview, not a detail (cabinet strip, lip at the edge, cap edge-on); the bell's top dissolves into the white; flat mouth; a flag's square glint |
| m | macro-woofer-ice | 5.0 | ring and cone flat, no specular sweep; framed off-centre with a violet edge stripe and a clipped sliver |
| m | macro-grip-poison | 5.0 | the slot a dark hole (nothing behind it); the top face blown into the white; horn and posts cropped at the top |
| m | macro-corner-ember | 5.5 | no single subject (the horn's underside crowds it); the polished edge grey, no line; right face dead |
| m | macro-amp-dust (h3, rig 1769c6a) | 5.5 | the plate lit flat like a card; the edge glows at red clip; an empty block below; dim beside a white hero. Proofed its light changes (raking key, dimmer back lamp, +0.35 EV, a strip on the bevel) and a tighter frame: each turned the orange a murky brown, so the final stands as rendered |
| m2 | macro-horn-acid, reframed (cap and lip toward the camera) | 5.0 | the top 40 % empty; the lip a dark line; the plinth cut. Duel 5 against the first horn macro: **reframed wins, 5.0 to 4.5**; recentred on the horn (target lower, 125 mm) and rendered again |
| duel 6 | macro-corner-ember: reframed (horn out, 280 mm) vs first (h3) | | **first wins, 5.0 to 4.0**: the reframe cut the horn to a sliver and lost the shell's refraction, the most photographic surface; the first stands, and its shot is restored |
| m2 | macro-woofer-ice, reframed (h5) | 4.5 | duel 7 against the first: **first wins, 5.5 to 4.5** (it sits the driver inside the enclosure's frame with margin; the reframe crowds the ring to the left edge). The first stands, its shot restored |
| m2 | macro-grip-poison, reframed (h5) | 3.5 | a neon bloom on the right edge from the lamp behind the slot; the slot still a black hole; two empty panels below. Duel 8 against the first decides |
| duel 8 | macro-grip-poison: first vs reframed (h5) | | **first wins, 5.5 to 3.5**: the reframe's lamp through the slot bloomed the right edge to neon and left the slot black; the first stands, its shot restored |

So of the macro reframes only the horn's held (duel 5); the woofer, grip and corner keep their first finals. The
module's MACRO_FIX now carries only the horn's change, and every final's shot.json matches its shot file.
