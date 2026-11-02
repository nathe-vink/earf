# The horn, deep: the sheen and the cone (2026-11-02, evening)

The owner, on the study (README 741149d5, the time fixed in 9ccabeff): "The darker option in those examples looks better I think, except like to smooth one also, granted it looks flattened and not coned. But they have a metallic sheen to them which looks cheap and bad."

So the horns stay deep: today's depth per tint (Ice #369BCA, Ember the stock 2423 1/2 in, #E02B3A). The matched-luminance direction is dropped. Every frame uses the site's front-off-tall shot in colors F at 0.6 scale and 96 samples, with a 2x mouth crop from the same frame. `sheet-deep.png` shows, left to right, Ice a studio, a satin, c studio, c satin; then Ember the same four, then c's side in Ember. The mouths sit below in the same order.

## What makes the sheen

These are proxies on Ice at today's depth (the scratch tools `make.py` and `sheen.py` are copied here).

| test | a (stepped) | c (smooth) |
|---|---|---|
| reflection cards off (`scrim`, `sheen`, `topline`, `sidesheen`) | no visible change | no visible change |
| + the horn and fill lights' specular off, the rim light off | little change | **large**: the rim (260 W on the formed horn) lit the shell from behind, so it glowed flat; without it the walls shade down to the throat and it reads as a cone |
| + dark, warm reflection-only flags round the camera | no visible change | no visible change |
| + larger, softer key and horn light | little change | little change |
| satin outside (horn-lot roughness 0.25) | **large**: the step edges turn from chrome lines into soft frosted bands | **large**: the shell reads as a satin cone; the pod and the pads behind it fade |

So the stepped horn's sheen is **not the studio**. It comes from the horn itself: 22 polished layer edges, each a small mirror, and the light reflected inside the stack, which comes back out at the edges as silver lines. A real polished-edge stack would do the same. On the smooth horn, the flat look was the rim light, a studio choice, and its "face" was the pod and the two pads seen through clear polished walls.

The studio fix for every frame here is the cards off, the horn and fill specular off, the rim off, and the dark flags. It stays within the set's family: the same key, fill, sweep and backdrop. The finish fix is that plus a satin horn.

**One limit of the model:** a part takes one material, so "satin" here roughens the whole horn, the air path too. The product as proposed keeps the air path polished, which would show slightly more depth and gloss inside the mouth than these frames do.

## The frames

Each row gives the horn against the cabinet (median luminance), the hue difference and the share of saturated pixels in the horn's mouth.

| frame | horn / cabinet Y | hue diff | saturated | the sheen | the X |
|---|---|---|---|---|---|
| ice-a-studio | 0.042 / 0.581 | +4 | 84 % | still silver step lines and a bright diagonal streak top right: the studio barely moves it | clear X |
| ice-a-satin | 0.095 / 0.581 | -2 | 89 % | gone: the steps read as soft frosted bands, the colour rich | much weaker: a soft diagonal on the right faces only |
| ice-c-studio | 0.339 / 0.582 | -14 | 95 % | low; one soft streak top right | none |
| ice-c-satin | 0.376 / 0.582 | -13 | 86 % | none; a satin cone, the walls falling to the throat | none |
| ember-a-studio | 0.070 / 0.371 | -1 | 95 % | silver step lines and the diagonal streak remain | clear X |
| ember-a-satin | 0.140 / 0.371 | -3 | 78 % | gone: soft red bands | much weaker |
| ember-c-studio | 0.199 / 0.372 | -5 | 90 % | low; the pod and the two pads show through as a face | none |
| ember-c-satin | 0.226 / 0.372 | -5 | 69 % | none; reads as a cone, the pod a soft shadow at the throat | none |
| ember-c-side-studio | (side view) | | | low | none; the flare reads plainly as a horn from the side |

**Ice's smooth horn reads teal.** It sits 13 to 14 degrees from the cabinet: today's Ice horn tint (#369BCA) was matched for the thick stepped stack, and through the formed horn's thin shell it reads more cyan. A formed Ice horn would want its own chip, a few degrees bluer. It is not rendered here.

**Middle-depth references in Ice** (committed earlier, one folder up):
- `ice-a-stock.png`: a on stock 2069 1/2 in, 0.45 of the cabinet, hue +1, 65 % saturated. Stock sheet alone gives a its middle depth.
- `ice-c-mid.png`: c at 5.3 times the stock dye, 0.54 of the cabinet, hue +10.

## The finish, as a product change for the owner

- **a, stepped, with satin risers:** each layer's edge bead-blasted or sanded to about 400 grit before bonding, in place of today's edge polish. The front faces and the air path stay polished. Cost: about the same as today, or a little less, since the blast replaces a polish step. It also takes most of the X away.
- **c, smooth, with a satin outside and a polished air path:** the formed shell bead-blasted outside with the air path masked. Cost: about $60 to $120 a horn for the masking and the blast. It also hides the pod and the pads (the "face"). The reverse, a satin air path, would keep the outside glossy and so keep the flat look: not recommended.
- **What did not help:** a darker pod, cap and throat piece (black stock cast sheet), and bronze pads (`ice-e-mid`, `ember-e-mid`, `ice-f-mid`, `ember-f-mid`, one folder up). Seen through the tinted shell, the pads still read as two dark tubes. They are structural, so only a satin shell honestly hides them.

## Round 2: c-satin with its colour fixed (2026-11-02, late)

The coordinator's second blind round (wf_4a38dc3d-256) put a-satin first (6.8). c-satin came second (5.8), held back only by colour: turquoise in Ice, coral in Ember, and a little milky. This round fixes the formed horn's chip and finish, with the lighting unchanged.

Each row gives the horn against the cabinet (median luminance), the hue difference and the share of saturated pixels in the mouth:

| frame | horn deep | horn / cabinet Y | hue diff | saturated |
|---|---|---|---|---|
| ice-c-satin2 | **#0A52B8** | 0.148 / 0.582 = 0.25 | +2 | 90 % |
| ember-c-satin2 | **#C50206** | 0.161 / 0.372 = 0.43 | 0 | 88 % |
| ice-a-satin (round 1, for comparison) | #369BCA | 0.095 / 0.581 = 0.16 | -2 | 89 % |
| ember-a-satin (round 1) | #E02B3A | 0.140 / 0.371 = 0.38 | -3 | 78 % |

- **The chips in sheet terms** (the formed horn is 10 mm sheet):
  - Ice #0A52B8 is a **deep custom blue batch**, about 10 % TT through 10 mm (stock 2069 3/8 in is about 64 %). It carries a little more green than a straight concentration of the dye: darker chips drifted violet (#033EB8 +8, #0021A2 +16), so Ice lands at 0.25 of its cabinet, a little lighter than a-satin's 0.16, to keep the hue.
  - Ember #C50206 is about 11 % TT through 10 mm, roughly 1.5 to 2 times stock 2423's dye: **a custom batch** (or a deeper stock red, if TruCast makes one; not checked).
- **The finest satin that hides the pod and the pads** is roughness 0.25, a **fine glass-bead blast, about a 400 to 600 grit finish**, on the outside, with the air path masked and left polished. On Ember proxies, 0.08 shows the pod and the pads plainly, 0.2 still shows the pads faintly, and 0.3 hides everything but begins to read milky.
- **a-satin's pale wedge on the right wall is not a light.** Halving the horn light, moving it to the left, and a dark reflection-only card back left all left it unchanged. It is the white backdrop seen through the horn's right wall, where the light crosses the least acrylic. The only studio fix would be a darker backdrop, which would break the set, so a-satin is unchanged and both options are lit alike.
- **c's side view in Ember** (`ember-c-side-satin2.png`), satin, deep: the flare reads plainly as a horn.
- The sheen on both: gone. The X on c: none; on a-satin: much weaker.
