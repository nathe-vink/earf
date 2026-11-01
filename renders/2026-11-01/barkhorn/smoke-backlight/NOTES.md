# Smoke in backlight (2026-11-01)

**The complaint:** in the biomes lane's meteor-fire frame (r48-biomes 46e2366), Smoke read milky pale gray. The owner:
"doesn't look like smoke at all".

**The material is not the cause.**
- The asset's acrylic is the engine's own `clear_resin`: a pure absorbing volume (Beer's law), with no scattering, no
  subsurface and no emission. A linked asset carries the same node tree.

**What causes it:**
1. **The white voile batts inside.** Lit by the fire through the back and side walls, they fill every bay with a pale
   glow, and the tinted wall in front reads as frosted.
2. **Smoke's tint was light:** about 30 % through 20 mm (`#8A888E` after 25 mm), a pale gray glass when lit from
   behind.

**The test:** `smoke-backlit-white-black-deep.png`, from `smoke_backlit.py`. The asset is appended, with a warm area
light behind it as the fire. Left to right:
- as it was: milky;
- black sleeves: much darker, but a light amber smoke;
- black sleeves and Smoke deepened 1.86 times: dark, glassy, smoked.

**The fix:**
- **Black voile sleeves, every tint** (the owner's working default, 2026-11-01).
- **Smoke's cabinet deepened to about 12 % through 20 mm** (`#4F4D54` after 25 mm, in `product.py`'s `cloud-black`).
  That is the published TT of stock TruCast 2074 Dark Gray (11.7 %), which the stock pair already uses for the horn.
  So a 2074 cabinet would match it, if 2074 is available at 3/4 in.

The site's other Smoke pictures (rendered with the old tint) will read lighter than the rebuilt asset until they are
rendered again.
