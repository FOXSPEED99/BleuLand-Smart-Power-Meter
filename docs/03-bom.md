# 3. Bill of Materials

**Per unit.** 34 SMD placements + 19 through-hole placements + 1 coin cell,
plus 1 external current clamp.

A spreadsheet-ready version is at [`hardware/bom.csv`](../hardware/bom.csv).

> **On part numbers:** LCSC codes are given **only where they have been
> verified**. Where a cell says "search LCSC", that is deliberate — I would
> rather you look it up than order 1,000 of the wrong thing because I quoted a
> code from memory. Always cross-check package and pitch on the product page
> before ordering.

---

## 3.1 Mains side (all through-hole)

| Ref | Qty | Part | Package | Role in the circuit | Alternatives |
|---|---|---|---|---|---|
| **J1** | 1 | Screw terminal, 2-pin, 5.08 mm, 300 V / 10 A | THT | Mains L and N entry. Wide pitch so it accepts 1.5 mm² house wire and holds 300 V between poles. | KF128-5.08, KF301-5.08, Phoenix MKDS equivalents. Any 5.0/5.08 mm 2-way block. |
| **F1** | 1 | Fuse, 250 mA, **time-lag (T)**, **250 VAC**, 5 × 20 mm glass | THT | Fire protection. Opens before house wiring can heat up if anything downstream shorts. | Radial TR5/TE5 250 mA 250 V (smaller, no clips needed). **Never** substitute an SMD fuse — most are rated 63 V only. |
| **FH1** | 2 | PCB fuse clips for 5 × 20 mm | THT | Holds F1, allows field replacement. | Omit if using a radial fuse. |
| **RV1** | 1 | MOV, 14 mm, 470 V varistor voltage — `14D471K` | THT | Clamps surges. Fitted **after** the fuse so a failed MOV blows the fuse instead of starting a fire. | `7D471K` (smaller, lower energy), `S14K275`, `TVR14471`. Do **not** use a 275 V or 390 V part — it will conduct on normal mains peaks. |
| **C1** | 1 | **X2 safety capacitor**, 100 nF, 275 VAC | THT | Differential-mode EMI suppression across L-N. | Any X2-class 100 nF / 275 VAC. **Class matters:** X2 fails open. A general-purpose ceramic here is a fire hazard. |
| **PS1** | 1 | **HLK-PM01** — 100–264 VAC → 5 V / 0.6 A / 3 W, **isolated** | THT module, 34 × 20 × 15 mm | Isolated power supply. This part *is* the isolation barrier for power. | `HLK-PM03` (3.3 V out, drop U1), `HLK-5M05` (5 W), `TSP-05`, `IRM-03-5`. Must be the **isolated transformer** type — not a capacitive dropper. |
| **Rv1–Rv4** | 4 | 47 kΩ, 1 %, **1/2 W metal film** | THT axial | Set the ZMPT101B primary current (1.22 mA at 230 V). Four in series for voltage rating, safe open-failure and heat spreading. | 4 × 51 kΩ, or 5 × 39 kΩ. Keep the total at 180–200 kΩ. **Do not** replace with one resistor. |
| **T1** | 1 | **ZMPT101B** voltage transformer, 1000:1000, 2 mA : 2 mA | THT | Isolation barrier for the voltage signal. | Small PCB mains transformer 230 V : 6 V, 0.35 VA (bulkier, more phase shift). ⚠️ Buy the **bare transformer**, not the blue LM358 breakout module. |

---

## 3.2 Power conversion (SELV side)

| Ref | Qty | Part | Package | Role | Alternatives |
|---|---|---|---|---|---|
| **C2** | 1 | 470 µF / 16 V electrolytic, 105 °C | THT radial | 5 V bulk reservoir; absorbs Wi-Fi transmit bursts. | 330–1000 µF. Use a 105 °C part — it lives in a hot panel. |
| **U1** | 1 | AMS1117-3.3 | SOT-223 | 5 V → 3.3 V linear regulator. | LM1117-3.3, AP1117-33, RT9013 (SOT-23, lower current), SPX1117-3.3. |
| **D1** | 1 | 1N4148W | SOD-123 | Protects U1 if a programmer back-feeds 3.3 V into an unpowered board. | SS14, BAT54, 1N4007 (THT). |
| **C4** | 1 | 470 µF / 10 V electrolytic, 105 °C | THT radial | 3.3 V bulk. **Place within 10 mm of the ESP32's 3V3 pin.** Do not reduce — this is what prevents brown-out resets during Wi-Fi TX. | 470–1000 µF, low ESR preferred. |
| **C5** | 1 | 10 µF / 16 V X7R | 0805 | Mid-frequency decoupling on 3.3 V. | 4.7–22 µF X5R/X7R. |
| **C6** | 1 | 100 nF X7R | 0805 | High-frequency decoupling on 3.3 V. | Any 100 nF X7R. |

---

## 3.3 Measurement front end

| Ref | Qty | Part | Package | Role | Alternatives |
|---|---|---|---|---|---|
| **U2** | 1 | **ATM90E26-YU-R** — single-phase metering IC | **SSOP-28, 0.65 mm** | The measurement engine: Vrms, Irms, real/reactive/apparent power, PF, frequency, energy accumulation, phase compensation. | LCSC **C616398** (reel) / **C145595** (`-YU-B`). ⚠️ **Stock is thin — see [risks §6.1](06-risks-and-decisions.md).** Plan B: `BL0940` (TSSOP-14, LCSC C691894) or `HLW8032` (SOP-8, LCSC C128023) — both need a different footprint, so decide before the PCB order. |
| **Y1** | 1 | Crystal, **8.192 MHz**, 18 pF load | HC-49S THT (or 3225 SMD) | Metering timebase. The frequency is not negotiable — the IC's energy constants assume it. | HC-49S through-hole is easier to hand-solder and more available locally. SMD 3225 if you move to reflow. |
| **C10, C11** | 2 | 27 pF, **NP0/C0G**, 50 V | 0805 | Crystal load caps: `2 × 18 − 2 × 5 = 26 pF → 27 pF`. | 22–33 pF NP0. Must be NP0/C0G — X7R drifts and pulls the oscillator. |
| **FB1** | 1 | Ferrite bead, 600 Ω @ 100 MHz | 0805 | Keeps Wi-Fi and digital switching noise out of the analog supply. | 120–1000 Ω @ 100 MHz, ≥ 200 mA rating. |
| **C7** | 1 | 10 µF X7R | 0805 | Analog supply bulk (AVDD). | 4.7–22 µF. |
| **C8, C9** | 2 | 100 nF X7R | 0805 | AVDD / DVDD decoupling. Place hard against the pins. | — |
| **Rb** | 1 | **10 Ω, 1 %, ≤ 50 ppm/°C**, 0.25 W metal/thin film | 0805 or 1206 | **Burden resistor.** Converts CT secondary current to voltage. The single most accuracy-critical passive on the board. ⚠️ *Value to confirm on prototype — see [circuit §3.3](02-circuit.md).* | 12 Ω is the published reference value with this clamp. **Never** substitute a wirewound part (inductance causes phase error) or a >50 ppm/°C part (uncalibratable drift). |
| **Rb2** | 0 | (parallel trim footprint) | 0805 | Empty. Lets you trim the current range without cutting traces, and lets you build a 100 A variant later. | — |
| **Rv5** | 1 | **330 Ω, 1 %, ≤ 50 ppm/°C** | 0805 | Secondary burden for T1 — sets voltage full scale (~300 V). ⚠️ *Value to confirm on prototype.* | 62 Ω if the IC's full scale turns out to be ~120 mV. See [circuit §2.3](02-circuit.md). |
| **Rv6** | 0 | (parallel trim footprint) | 0805 | Empty. Voltage-range trimming. | — |
| **Rf1, Rf2, Rf3** | 3 | 1 kΩ, 1 % | 0805 | Anti-alias / input current limiting. **Rf2 and Rf3 must be a matched pair** — mismatch degrades common-mode rejection on the current channel. | 470 Ω–2.2 kΩ, adjust Cf to keep the corner near 5 kHz. |
| **Cf1, Cf2** | 2 | 33 nF, NP0/C0G | 0805 | Anti-alias filter, corner ≈ 4.8 kHz. | 22–47 nF NP0. |
| **Cf3, Cf4** | 2 | 10 nF, NP0/C0G | 0805 | Common-mode filtering on the CT legs. | — |
| **D2, D3** | 2 | SMAJ5.0CA — bidirectional TVS, 5 V | DO-214AC | Clamps the CT open-circuit spike, ESD and transformer-coupled transients. | P6KE6.8CA, SMBJ5.0CA, or two 3.9 V zeners back-to-back. **Must be bidirectional** — the signal is AC. |
| **J2** | 1 | Screw terminal, 2-pin, **3.5 mm** | THT | CT clamp connection. Deliberately a different pitch from J1 so mains can never be wired here by mistake. | 3.81 mm block, or a PJ-320 3.5 mm jack if you want plug-in clamps. |
| **CT1** | 1 | **Split-core CT, 100 A : 50 mA (2000:1), 13 mm window** — `SCT-013-000` | External | Non-invasive current sensing. Clamps around the house main live conductor. | Any 2000:1 split-core 100 A clamp (many clones). `SCT-013-060` (60 A : 1 V, internal burden) is safer but caps out below your 63 A breaker and needs a different input network. **This is your biggest single cost — source it carefully.** |

---

## 3.4 MCU, storage and user interface

| Ref | Qty | Part | Package | Role | Alternatives |
|---|---|---|---|---|---|
| **U3** | 1 | **ESP32-WROOM-32E-N8** (8 MB flash) | Castellated module, 18 × 25.5 mm | MCU, Wi-Fi, TLS to cloud, flash buffering, RTC management. Hardware AES/SHA makes TLS fast. **8 MB, not 4 MB** — OTA needs two app partitions, which leaves only ~0.95 MB for buffering on a 4 MB part. See [risks §6.11](06-risks-and-decisions.md). | **`ESP32-WROOM-32UE` is footprint-identical** with a u.FL connector — fit it plus a pigtail antenna for metal-panel installs, no PCB change. Also: `ESP32-WROOM-32D`, `ESP32-C3-WROOM-02` (cheaper, native USB, different pinout). **Avoid ESP8266** — TLS is too slow and RAM-tight. |
| **R1** | 1 | 10 kΩ | 0805 | EN pull-up. | — |
| **C12** | 1 | 1 µF X7R | 0805 | EN reset delay. **Required** for reliable power-on boot. | 0.1–4.7 µF. |
| **R2** | 1 | 10 kΩ | 0805 | IO0 pull-up (normal boot). | — |
| **SW1** | 1 | Tact switch, 6 × 6 mm, THT | THT | Boot-mode entry during flashing; factory reset / Wi-Fi reconfig in firmware. | 4.5 × 4.5 mm SMD, or 6 × 6 with a tall actuator to reach the enclosure wall. |
| **LED1** | 1 | LED, green | 0805 | Power / heartbeat. | 3 mm THT if you prefer a light pipe. |
| **LED2** | 1 | LED, blue | 0805 | Wi-Fi / cloud status. | Any second colour. |
| **R3, R4** | 2 | 1 kΩ | 0805 | LED current limit (~2 mA each — plenty through a diffuser). | 470 Ω–2.2 kΩ to taste. |
| **U4** | 1 | **DS3231SN** — ±2 ppm TCXO RTC, I²C | SOIC-16 | Keeps time through power cuts so buffered records have trustworthy timestamps. | `DS3231M` (SOIC-8, ±5 ppm, cheaper, no crystal), `PCF8563T` (SOP-8, cheapest, needs a 32.768 kHz crystal, ±30 ppm). |
| **BT1** | 1 | CR2032 holder, THT | THT | Backup cell holder. | Any CR2032 PCB holder. |
| **B1** | 1 | CR2032 lithium cell | — | ~8 years of backup timekeeping. | ⚠️ **Non-rechargeable.** Connect straight to VBAT — no trickle-charge circuit. See [circuit §2.7](02-circuit.md). |
| **R5, R6** | 2 | 4.7 kΩ | 0805 | I²C pull-ups. | 2.2–10 kΩ. |
| **C13** | 1 | 100 nF X7R | 0805 | DS3231 decoupling. | — |
| **J3** | 1 | Header, 1 × 6, 2.54 mm | THT | Programming and debug: `3V3 · GND · TXD0 · RXD0 · EN · IO0`. | Or leave as bare pads for a pogo-pin jig — cheaper and faster in production. |
| **U5** | **0** | W25Q64 — 8 MB SPI flash | SOIC-8 | **Not populated.** Footprint only, for a future high-resolution logging variant. | Populate only if you need 15-second data kept for a year. |

---

## 3.5 Bare board

| Item | Spec |
|---|---|
| Layers | 2 |
| Size | ~50 × 45 mm |
| Thickness | 1.6 mm |
| Copper | 1 oz (35 µm) |
| Surface finish | **ENIG recommended** (flat pads make the SSOP-28 far easier to hand-solder). HASL is acceptable and cheaper. |
| Special | **Routed slot** along the isolation barrier — see [layout §5.2](05-layout-and-enclosure.md) |
| Silkscreen | Mains area clearly marked, dashed isolation line, polarity marks on every polarised part |

---

## 3.6 Indicative cost per unit at 1,000 pieces

Chinese distributor pricing, for budgeting only. Local Syrian/Lebanese prices
will differ — treat this as the import-fallback ceiling.

| Item | Unit cost (USD) |
|---|---|
| ESP32-WROOM-32E-N8 | 2.50 |
| ATM90E26-YU-R | 1.32 |
| HLK-PM01 | 1.80 |
| DS3231SN | 1.50 |
| ZMPT101B | 0.90 |
| Terminals J1 + J2 | 0.30 |
| Fuse + clips + MOV + X2 cap | 0.35 |
| 2 × TVS | 0.12 |
| CR2032 + holder | 0.20 |
| Crystal | 0.10 |
| AMS1117 + diode | 0.08 |
| Rv1–Rv4 metal film | 0.08 |
| ~25 × 0805 passives | 0.25 |
| 2 × electrolytic | 0.10 |
| Switch, LEDs, header | 0.15 |
| Ferrite bead | 0.02 |
| PCB (2-layer, qty 1,000) | 0.35 |
| **Subtotal — board only** | **≈ 10.10** |
| **CT clamp (`SCT-013-000`)** | **4.50** (generic clone ≈ 2.50) |
| **Total per unit** | **≈ 14.60** (≈ 12.60 with a clone clamp) |

**Note where the money is.** The clamp alone is ~31 % of the bill of materials —
more than the ESP32 and the metering IC combined. If you need to cut cost, that
is the place to negotiate, and if you need to *improve accuracy*, that is also
the place to spend. See [risks §6.3](06-risks-and-decisions.md).

Not included: enclosure, wiring, packaging, labour, the ~US$ 250 of test
equipment in [§4.7](04-calibration-and-test.md), and stencil/hotplate tooling in
[§7.3](07-assembly-and-tooling.md).
