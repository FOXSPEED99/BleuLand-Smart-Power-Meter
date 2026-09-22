# Purchase List — What to Actually Buy

**This is the shopping list.** Unlike [`bom.csv`](bom.csv), which lists every
reference designator separately, this file **aggregates identical parts** so
each line is one thing you order.

- **40 distinct line items** for the whole product.
- **53 placements per board** (35 SMD + 18 through-hole), plus a coin cell, the
  CT clamp and the bare PCB.
- Machine-readable version: [`purchase-list.csv`](purchase-list.csv)

> Prices are China qty-1000 estimates for budgeting only. Buy locally in Syria
> or Lebanon first where you can — treat these as the import-fallback ceiling.

---

## How the quantities work

| Column | Meaning |
|---|---|
| **Qty per unit** | How many go on one board |
| **Qty for 1000** | Straight multiplication |
| **Order qty** | What to actually buy, **including spares** |

**Spares policy built into the numbers:**

| Part type | Spare margin | Why |
|---|---|---|
| ICs, modules, connectors, magnetics | **+5 %** | Expensive, hard to replace mid-run |
| Small passives (0805) | **+5–10 %** | They get lost, tombstoned, flicked off the bench |
| Safety parts (fuse, diodes) | **+10 %** | Cheap, and you never want to stop the line |
| CT clamp, PCB, coin cell | **+2–3 %** | Bulky or expensive; less prone to loss |

> **Order 1,000 of a part for a 1,000-unit run and you will stop the line at
> unit 970.** This is the single most common first-production mistake.

---

## 1. Active parts and modules

| # | Item | Spec | Package | Refs | /unit | Order | Notes |
|---|---|---|---|---|---|---|---|
| 1 | **HLW8032** metering IC | 5 V, UART | SOP-8 | U2 | 1 | **1,050** | LCSC `C128023`. Internal oscillator — no crystal. |
| 2 | **ESP32-WROOM-32E-N8** | **8 MB** flash | Castellated | U3 | 1 | **1,050** | 8 MB, not 4 MB — OTA needs two app partitions. Verify real size with `esptool flash_id`. |
| 3 | **DS3231SN** RTC | ±2 ppm TCXO, I²C | SOIC-16 | U4 | 1 | **1,050** | Commonly counterfeited — see [risks §6.9](../docs/06-risks-and-decisions.md). Alt: DS3231M SOIC-8. |
| 4 | **HLK-PM01** | 100–264 VAC → 5 V 0.6 A **isolated** | THT module | PS1 | 1 | **1,050** | Must be the isolated transformer type. Alt: HLK-PM03 / HLK-5M05 / IRM-03-5. |
| 5 | **AMS1117-3.3** | 3.3 V LDO | SOT-223 | U1 | 1 | **1,050** | Alt: LM1117-3.3 / AP1117-33 / SPX1117-3.3. |

## 2. Sensing

| # | Item | Spec | Refs | /unit | Order | Notes |
|---|---|---|---|---|---|---|
| 6 | **ZMPT101B** voltage transformer | 1000:1000, 2 mA : 2 mA | T1 | 1 | **1,050** | ⚠️ Buy the **bare transformer**, not the blue LM358 breakout module. |
| 7 | **Split-core CT clamp** | 100 A : 50 mA (2000:1), 13 mm window, `SCT-013-000` | CT1 | 1 | **1,030** | ⚠️ **Biggest single cost (~33 % of BOM).** Buy samples from three suppliers and measure the turns ratio before committing. |

## 3. Connectors

| # | Item | Spec | Refs | /unit | Order | Notes |
|---|---|---|---|---|---|---|
| 8 | Screw terminal 2-pin **5.08 mm** | 300 V / 10 A | J1 | 1 | **1,050** | Mains L/N. KF128-5.08 or KF301-5.08. |
| 9 | Screw terminal 2-pin **3.5 mm** | SELV | J2 | 1 | **1,050** | CT input. Different pitch from J1 **on purpose** — mains can never be wired here by mistake. |
| 10 | Pin header 1 × 6, 2.54 mm | Male straight | J3 | 1 | **1,050** | Programming port. Can be bare pads if you use a pogo-pin jig. |

## 4. Safety and protection

| # | Item | Spec | Refs | /unit | Order | Notes |
|---|---|---|---|---|---|---|
| 11 | Fuse **250 mA time-lag** | **250 VAC**, 5 × 20 mm glass | F1 | 1 | **1,100** | ⚠️ Must be 250 VAC and **time-lag (T)**. **Never** an SMD fuse — most are 63 V rated. |
| 12 | Fuse clips for 5 × 20 mm | PCB mount | FH1 | **2** | **2,100** | Omit if you use a radial TR5 fuse instead. |
| 13 | MOV varistor **14D471K** | 470 V varistor voltage | RV1 | 1 | **1,050** | Alt: 7D471K / S14K275. ⚠️ Do **not** fit a 275 V or 390 V part — it will cook on normal mains peaks. |
| 14 | **X2 safety capacitor** | 100 nF, 275 VAC | C1 | 1 | **1,050** | ⚠️ **Class X2 mandatory** — it fails open. A general-purpose ceramic here is a fire hazard. |
| 15 | TVS **SMAJ5.0CA** | 5 V **bidirectional** | D2, D3 | **2** | **2,100** | Must be bidirectional — the signal is AC. Alt: P6KE6.8CA / SMBJ5.0CA. |
| 16 | Diode **1N4148W** | Small signal | D1 | 1 | **1,100** | LDO reverse-feed protection. Alt: SS14 / BAT54 / 1N4007 THT. |

## 5. Resistors

| # | Value | Package | Refs | /unit | Order | Notes |
|---|---|---|---|---|---|---|
| 17 | **47 kΩ 1 % ½ W metal film** | **THT axial** | Rv1–Rv4 | **4** | **4,200** | ZMPT primary string. Through-hole for voltage rating and creepage. ⚠️ **Never** replace with one resistor. |
| 18 | 1 kΩ 1 % | 0805 | Rls1, Rf1, R3, R4 | **4** | **4,200** | General purpose. |
| 19 | **1.5 kΩ 1 %** | 0805 | Rf2, Rf3 | **2** | **2,200** | ⚠️ **Phase compensation — matched pair.** Buy 820 Ω / 1.2 k / 1.8 k / 2.2 k as well for prototype tuning. |
| 20 | 2 kΩ 1 % | 0805 | Rls2 | 1 | **1,100** | Level shifter shunt leg. |
| 21 | 10 kΩ 1 % | 0805 | R1, R2 | **2** | **2,100** | EN and IO0 pull-ups. |
| 22 | 4.7 kΩ 1 % | 0805 | R5, R6 | **2** | **2,100** | I²C pull-ups. |
| 23 | 0 Ω jumper | 0805 | R7 | 1 | **1,100** | AGND ↔ GND star link. |
| 24 | **0.68 Ω 1 % ≤50 ppm/°C thin film** | 0805/1206 | Rb | 1 | **1,100** | ⚠️ **CT burden — the most accuracy-critical passive on the board.** Value must be confirmed on prototypes. **No wirewound. No >50 ppm/°C.** |
| 25 | **150 Ω 1 % ≤50 ppm/°C thin film** | 0805 | Rv5 | 1 | **1,100** | ⚠️ ZMPT burden. Value must be confirmed on prototypes. |

## 6. Capacitors

| # | Value | Package | Refs | /unit | Order | Notes |
|---|---|---|---|---|---|---|
| 26 | 100 nF X7R 50 V | 0805 | C3, C6, C8, C13 | **4** | **4,200** | Decoupling. |
| 27 | 10 µF X7R 16 V | 0805 | C5, C7 | **2** | **2,100** | Bulk decoupling. |
| 28 | 1 µF X7R | 0805 | C12 | 1 | **1,100** | EN reset delay — **required** for reliable boot. |
| 29 | 33 nF X7R 50 V | 0805 | Cf1, Cf2 | **2** | **2,100** | Anti-alias. ⚠️ **Buy all filter caps from one reel** — consistency matters more than absolute value. |
| 30 | 10 nF X7R 50 V | 0805 | Cf3, Cf4 | **2** | **2,100** | Common-mode filter. Same reel. |
| 31 | 470 µF 16 V 105 °C electrolytic | Radial THT | C2 | 1 | **1,050** | 5 V bulk. **105 °C part** — it lives in a hot panel. |
| 32 | 470 µF 10 V 105 °C electrolytic | Radial THT | C4 | 1 | **1,050** | 3.3 V bulk. ⚠️ **Must sit within 10 mm of the ESP32's 3V3 pin.** |

## 7. Everything else

| # | Item | Spec | Refs | /unit | Order | Notes |
|---|---|---|---|---|---|---|
| 33 | Ferrite bead | 600 Ω @ 100 MHz, ≥200 mA | FB1 | 1 | **1,100** | Keeps Wi-Fi noise off the metering IC supply. |
| 34 | Tact switch 6 × 6 mm | THT | SW1 | 1 | **1,050** | Needs a tall actuator to reach the enclosure wall. |
| 35 | LED green | 0805 | LED1 | 1 | **1,100** | Power / heartbeat. |
| 36 | LED blue | 0805 | LED2 | 1 | **1,100** | Wi-Fi / cloud status. |
| 37 | CR2032 holder | THT | BT1 | 1 | **1,050** | |
| 38 | CR2032 lithium cell | 3 V | B1 | 1 | **1,020** | ⚠️ **Non-rechargeable.** Straight to VBAT, no trickle charger. |
| 39 | **Bare PCB** | 2-layer, 1.6 mm, 1 oz, HASL | — | 1 | **1,030** | Routed isolation slot required. **Order panelised 2 × 2** if using a stencil. |
| 40 | SMT stencil | Frameless, 0.12 mm stainless | — | — | **2** | Order with the PCB. Buy two — they bend and wear. |

---

## Budget

| | USD |
|---|---|
| **Everything above, for a 1,000-unit run** | **≈ 13,950** |
| Cost per finished unit (parts only, no spares) | **≈ 13.35** |
| Effective per unit including spares and stencil | **≈ 13.95** |

Not included: enclosures, wiring, packaging, labour, the ~US$ 250 of test
equipment in [calibration §4.7](../docs/04-calibration-and-test.md), and the
hotplate in [tooling §7.4](../docs/07-assembly-and-tooling.md).

### Where the money goes

| Item | Share of BOM |
|---|---|
| **CT clamp** | **~33 %** |
| ESP32 module | ~19 % |
| HLK-PM01 | ~13 % |
| DS3231 RTC | ~11 % |
| ZMPT101B | ~7 % |
| Everything else combined | ~17 % |

Five line items are 83 % of the cost. If you need to cut, that is where to look
— and the clamp alone is worth negotiating hard on.

---

## Prototype shopping list (buy this FIRST)

**Do not order the 1,000-unit quantities yet.** Three values must be confirmed
on hardware first — see [`docs/02-circuit.md`](../docs/02-circuit.md) §3.3.

Buy **10 of everything above**, plus these sweep values so you can find the
right ones without re-ordering:

| For | Buy these values (10 each, 0805 1 %) |
|---|---|
| **Rb** — CT burden | 0.47 Ω, 0.51 Ω, 0.56 Ω, 0.62 Ω, **0.68 Ω**, 0.75 Ω, 0.82 Ω, 1.0 Ω |
| **Rv5** — ZMPT burden | 62 Ω, 100 Ω, **150 Ω**, 220 Ω, 330 Ω, 470 Ω |
| **Rf2 / Rf3** — phase trim | 430 Ω, 820 Ω, 1.2 kΩ, **1.5 kΩ**, 1.8 kΩ, 2.2 kΩ, 2.7 kΩ (buy **20** of each — they go in pairs) |

That is perhaps US$ 15 of resistors and it is the difference between locking the
design in half a day and discovering the problem at unit 300.

---

## Ordering strategy

1. **Prototype batch first.** 10 boards plus the sweep resistors above. Lock
   `Rb`, `Rv5` and `Rf2`/`Rf3`.
2. **Then commit to the run.** Buy the full 1,050 of every line item in one go —
   especially the ICs. Stock levels are a snapshot, not a promise.
3. **Buy safety parts (#11–#16) from a reputable source**, even if it costs
   more. A counterfeit X2 capacitor or MOV is a fire risk, not a performance
   issue. Do not let a local shop substitute "the same value" from an unmarked
   bin.
4. **Incoming inspection** on the three commonly-faked items — DS3231, ESP32
   modules and CT clamps. Procedures in
   [risks §6.9](../docs/06-risks-and-decisions.md).
5. **Keep one reel per filter capacitor value** for the whole run. If you change
   capacitor supplier mid-run, re-verify the phase trim.
