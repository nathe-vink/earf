# Mantle's drive and arm for the first one (round 43, 2026-10-31)

What to buy so the first Mantle plays. Prices are US listings seen on 2026-10-31. Anything seen only in a search
snippet is marked **[snippet]**. Nothing was bought or ordered.

## Corrections to the parts list

- **The Rega 24 V motor kit is $265, not $200.** Audio Advisor, in stock, ships in 1 to 3 days.
  - It is an AC synchronous motor, a hand-tuned board and a rigid mount.
  - https://www.audioadvisor.com/products/rega-24v-motor-upgrade-kit
- **The Neo PSU drives Rega's motor board, not the bare motor.** It sends 24 V AC, plus a 20 V DC line that switches
  a relay on the motor's board for 45 rpm. Keep the board inside the motor pod.
  - Rega lists the kit as "for Rega turntables only". People fit it to other Rega models; no fully DIY deck was found.
  - Forum threads: pinkfishmedia and diyaudio **[snippet]**.
- **Pro-Ject's "Speed Box S3" doesn't appear to exist.** The S and S2 are for 16 V AC motors, and the S2 is sold out
  at Pro-Ject USA **[snippet]**.

## Motor and speed control

| Option | Type | US price | Why |
|---|---|---|---|
| **Rega 24 V motor kit + Neo PSU MK2 (60 Hz)** | 24 V AC synchronous; DSP drive; 33/45; trim in 0.01 rpm steps | $265 + $445 = **$710** | A known low-vibration pair. The board goes in the pod. |
| Origin Live DC motor kit, "Advanced" | DC motor; off/33/45; continuous trimmers; strobe; a US adapter offered | £420 (Standard £320) + shipping | Made for fitting to any deck. Its wide trim forgives an imperfect pulley. https://www.originlive.com/hi-fi/turntable-upgrades-modification/turntable-motor-power-supply/ |
| Premotec 9904 111 31813 + VPI ADS | 110 V AC synchronous, 1.8 W; analog trim | $155 + about $1,265–1,400 **[snippet]** | Open market, but costly. |

**Pick for the first one: the Rega pair.** The fallback is Origin Live's Advanced, if Rega's board won't run outside a
Rega, or the Neo's listing can't be had (`certification.md`).

## Bearing

No new, off-the-shelf main bearing with a published spindle size and a US price was found:
- Rega's 17 mm hub and bearing are discontinued;
- Michell's Gyro bearing is discontinued;
- DIY HiFi Supply's inverted bearing (about $105 in an old post) is no longer listed;
- VPI's appear only used.

**So the bearing is turned to order, as designed, and it is the critical path.** Get it quoted with RFQ 04's shop
(RivCut turns stainless and brass). The emergency fallback is a used VPI HW-19 / Classic platter and bearing.

## Belt and pulley

- **The drawn belt (975 mm unstretched) is nearly the platter's own circumference** (π × 310 ≈ 974 mm). Driving the
  rim from a pod 100+ mm away needs a longer path. **Measure the path on the first plinth, then order the belt.**
- **The pulley:** Rega's is sized for Rega's sub-platter, so a 310 mm rim needs our own pulley. The Rega motor turns
  at 250 rpm at 60 Hz [check against the kit's sheet]. For 33.33 rpm on a 310 mm rim, the pulley is
  310 × 33.33 / 250 ≈ **41.3 mm**, plus about the belt's thickness; for 45 rpm, about 55.8 mm. Turn both on one
  stepped pulley, and fine-tune with the Neo's trim.
- **Belts:**
  - VPI BL001 (made for a 12 in rim), $30 at Upscale Audio **[snippet]**;
  - Origin Live cuts flat belts to length, price on request;
  - a round urethane O-ring belt cut and joined to the measured length (about $6–10) is the quick test belt.

## Tonearm

| Arm | Mount | US price |
|---|---|---|
| **Rega RB330** | Rega three-point; 236.5 effective, 222 mounting distance | **$675**, in stock (Audio Advisor; Upscale; Safe and Sound **[snippet]**) |
| Rega RB220 | Rega | $445 **[snippet]** |
| Pro-Ject EVO 9 CC | drilled board; 212 mounting distance | $949, backordered about 2 weeks |

Keep the **RB330**, as the plinth is drilled for it. Check the 236.5 / 222 figures against Rega's own drawing before
drilling.

## Cartridge

| Cartridge | US price | |
|---|---|---|
| Ortofon 2M Red | $109.99 | Upscale |
| **Ortofon 2M Blue** | **$219.99** | Upscale. The Red, Blue and Silver styli interchange **[snippet]**. |
| Ortofon 2M Black | $749.99 | Upscale |
| Audio-Technica VM540ML | $249–279 | **[snippet]** |
| Nagaoka MP-110 | $150–169 | **[snippet]** |

**Use a 2M Blue for the first build, and the 2M Black for the show unit.**

## The first one's drive and arm

| Item | Choice | Cost |
|---|---|---|
| Motor and control | Rega 24 V kit + Neo PSU MK2 | $710 |
| Bearing | turned to order, as designed | quote (RFQ 04) |
| Pulley | turned, stepped 41.3 / 55.8 | quote (RFQ 04) |
| Belt | an O-ring test belt, then a cut flat belt | about $30 |
| Tonearm | Rega RB330 | $675 |
| Cartridge | Ortofon 2M Blue | $220 |
| Phono stage | Pro-Ject Phono Box S2 | $269 (not re-checked) |
| **Total, bought** | | **about $1,904**; about $2,434 with the 2M Black |

**Lead-time risks:**
- the turned bearing and the pulley;
- whether Rega's board runs happily outside a Rega.

Order the Rega pair first and bench-run the motor on its board, before the plinth is cut.
