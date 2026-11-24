# Convergence (24 Nov): Dust's right side and base, 96 spp (adaptive 0.01, as the fronts) against 768 spp (adaptive 0.001), both clamp 0, OIDN

Crop x 0.44-0.80, y 0.36-0.944 of the 1000 x 1250 front (360 x 730 px). Regions from the front's mask. Sheet: sheet-conv.png (96, 768, |diff| x5).

| region | px | L* 96 | L* 768 | dL* | C* 96 | C* 768 | |dL*| p95 |
|---|---|---|---|---|---|---|---|
| right side | 74481 | 45.1 | 44.9 | -0.25 | 55.9 | 55.6 | 3.8 |
| front panel | 37097 | 55.7 | 55.6 | -0.06 | 58.8 | 58.7 | 4.1 |
| base | 3179 | 29.3 | 29.4 | +0.05 | 29.2 | 28.5 | 6.0 |
| ports | 5857 | 50.1 | 50.0 | -0.12 | 59.3 | 59.1 | 6.0 |
| paper (floor) | 95800 | 92.9 | 92.9 | -0.00 | 6.3 | 6.3 | 0.5 |
| whole crop | 262800 | 61.8 | 61.7 | -0.09 | 33.0 | 32.9 | 3.5 |
No dark or smooth bias at 96 spp: every region's mean is within 0.25 L* and C* within 0.7 of 768 spp. The differences are local, at edges and refracted detail (95th percentile 4-6 L* on the product, 0.5 on the paper): the denoiser's reconstruction of fine caustic edges, not a shift in level.
