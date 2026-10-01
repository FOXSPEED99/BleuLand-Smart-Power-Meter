# Component selection — audit brief

**Purpose of this document:** hand it to a fresh reviewer (human or AI) and ask
them to independently re-check every component choice. It states the
requirements to judge against, every part and the reasoning behind it, the
calculations already done, and the places the selection is least certain.

**Nothing here is settled.** Challenge any of it. Where a choice has a reason
recorded, the reason is given so it can be attacked rather than guessed at.

---

## 1. What the product has to do

| Requirement | Value |
|---|---|
| Supply | single phase, 230 V, 50 Hz, grid mains only (no generator/inverter spec) |
| Service size | up to a **63 A** breaker |
| Measurement | whole-house, **non-invasive** — a split-core CT clamps around the live conductor, nothing is cut |
| Channels | **one** current channel, one voltage channel |
| Accuracy goal | as good as a single channel allows; a per-unit calibration constant is acceptable |
| Outputs | kWh to cloud over Wi-Fi, local buffering through internet outages, bill estimate from a user-entered price per kWh |
| Timekeeping | must survive mains loss so buffered readings keep correct timestamps |
| Mechanical | must hide **inside a domestic distribution board**; smallest practical size |
| Enclosure | 3D printed, Class II (no protective earth) |
| Insulation | reinforced, overvoltage **category III**, pollution degree 2 |
| Assembly | **hand assembly only** — soldering iron and hot-air station, no reflow oven, no hotplate |
| Volume | 1,000 units |
| Sourcing | local Syria/Lebanon first, then China (LCSC / JLCPCB / AliExpress). **Mouser and DigiKey are not realistic.** |
| Board | 75 × 75 mm, 2 layers, 44 components (23 SMD bottom / 21 through-hole top) |

Constraints that have shaped choices and should be understood before
challenging them:

- **An ESP32 development board on female headers**, not a bare chip or module —
  hand assembly, and the module carries its own PCB antenna.
- **A dedicated metering IC**, not ADC sampling in firmware.
- **PCB antenna only**, no external connector.
- **L and N are both available** at the install point, and **may be swapped** —
  which is common locally and is the reason the isolation exists.

---

## 2. Signal chain

```
house live cable ──(clamped, not cut)── split-core CT
  │
  └─ J1 ─ D4 SMAJ5.0CA ─ R16 0.68 Ω burden ─ R15/R17 1.5 kΩ ─> HLW8032 IP/IN
                                             C10 33 nF differential
                                             C11/C12 10 nF to AGND

mains L ─ P1 ─ F1 fuse ─ C5 0.1 µF X2 ─ R4 MOV 14D471K
   ├─ PS1 HLK-5M05 ─> 5 V ─ C3 470 µF, C4/C8 100 nF
   │                   ├─ FB1 ferrite ─> HLW8032 VDD (C6 100 nF, C7 10 µF)
   │                   ├─ DS1307 VCC
   │                   └─ ESP32 5 V pin ─> 3V3 ─ C1 10 µF, C2 100 nF
   │
   └─ R5/R8/R10/R13 4 × 47 kΩ ─> T1 ZMPT101B primary
                  T1 secondary ─ R14 300 Ω ─ D3 SMAJ5.0CA
                               ─ R12 1 kΩ, C9 33 nF ─> HLW8032 VP

HLW8032 TX ─ R11 1 kΩ / R6 2 kΩ divider (5 V → 3.3 V) ─> ESP32 IO16
DS1307 ─ R2/R3 4.7 kΩ pull-ups ─> ESP32 IO23 (SDA) / IO22 (SCL)
D1 green ─ R1 330 Ω ─> IO19        D2 blue ─ R9 330 Ω ─> IO18
R7 0 Ω: the single tie between ANALOG_GROUND and GND
```

---

## 3. Two problems found while compiling this — check these first

### 3.1 The DS1307 cannot read a 3.3 V I²C bus

`IC1` (DS1307) has its VCC on the **5 V** net. `R2`/`R3`, the SDA and SCL
pull-ups, go to the **3.3 V** rail.

The DS1307's input-high threshold is **VIH ≥ 0.7 × VCC**:

| DS1307 VCC | VIH min | Bus can reach | Margin |
|---|---|---|---|
| **5.0 V (as drawn)** | **3.50 V** | 3.30 V | **−0.20 V — out of spec** |
| 4.5 V | 3.15 V | 3.30 V | +0.15 V |
| 3.3 V | 2.31 V | 3.30 V | +0.99 V |

The bus physically cannot reach the threshold. It may appear to work on a
bench unit and fail over temperature or across a production batch, which is the
worst failure mode to ship.

Note the DS1307's own supply range is specified **4.5–5.5 V**, so simply moving
it to 3.3 V is also out of spec.

Candidate resolutions for the reviewer to weigh:
- **DS3231SN** instead: 2.3–5.5 V, so it runs at 3.3 V and the problem
  disappears. It is a TCXO, so it is far more accurate and needs **no external
  crystal** — which also removes `Y1` and its 12.5 pF requirement. Costs more.
  (Note: the *bare chip* only. The DS3231 "blue module" is already rejected
  because its charging circuit destroys a non-rechargeable CR2032.)
- A 2-MOSFET bidirectional level shifter on SDA and SCL. Adds parts.
- Run the DS1307 at 4.5 V from a dropper. Marginal, and ugly.

### 3.2 `D2`, the blue LED, will not light

Both LEDs are driven straight from an ESP32 GPIO at 3.3 V through 330 Ω.

| LED | Vf | Current at VOH ≈ 3.0–3.1 V |
|---|---|---|
| `D1` green, `R1` 330 Ω | 1.9–2.2 V | 2.4–3.6 mA — fine |
| `D2` **blue**, `R9` 330 Ω | **2.7–3.2 V** | **0 to 1.2 mA** |

A blue LED's forward voltage is at or above the GPIO's output voltage. At the
high end of the Vf distribution there is no forward bias at all. At the low end
you get under 1.2 mA, which behind a light pipe inside a closed panel will not
be visible.

Candidate resolutions:
- Change `D2` to **red, yellow or green** (Vf 1.8–2.2 V) and keep 330 Ω. Free.
- Keep blue, drive it from the **5 V** rail through a small NPN or MOSFET
  switched by the GPIO. Adds a transistor and a base resistor per LED.
- Keep blue on 3.3 V and drop `R9` to ~47 Ω. Works only at the low end of the
  Vf spread, so it is not a production answer.

---

## 4. Calculations already done — verify these rather than redo them

**Current channel.** `SCT-013-000`, 100 A : 50 mA, into a 0.68 Ω burden.
HLW8032 IP/IN range is ±30.9 mV RMS differential.

| Primary current | CT output | Across 0.68 Ω | % of range |
|---|---|---|---|
| 63 A (breaker rating) | 31.50 mA | 21.42 mV | 69 % |
| 90.9 A | 45.50 mA | 30.94 mV | 100 % — clipping |

So the burden is correctly sized: 69 % of range at full rated load, clipping
only above 91 A. The `SCT-013-000` is a current-output CT with no internal
burden, so an external burden is correct.

**Voltage channel.** 4 × 47 kΩ = 188 kΩ into the ZMPT101B primary (a 1:1
current transformer), secondary into `R14` = 300 Ω. HLW8032 VP range is
±495 mV RMS.

| Mains | Primary current | Across 300 Ω | % of range |
|---|---|---|---|
| 230 V | 1.223 mA | 367.0 mV | 74 % |
| 310 V | 1.649 mA | 494.7 mV | 100 % — clipping |

74 % at nominal, with headroom to 310 V. The ZMPT101B wants roughly 1 mA
primary, and 1.22 mA is in range. Dissipation per 47 kΩ resistor is **70 mW**,
so ¼ W is electrically sufficient and ½ W is margin.

**Mains current drawn by the whole board:** ~39 mA (HLK input 30 mA, `C5`
7.2 mA reactive, divider 1.2 mA). No load current crosses the board — the CT
clamps externally and `P1` has only two pins.

---

## 5. Full component list, with the reason for each choice

### Active and major parts

| Ref | Part | Package on board | Why this part | Source |
|---|---|---|---|---|
| `U1` | ESP32 DevKitC (ESP-WROOM-32) | 38-pin header, 2 × 19 | Wi-Fi + on-module PCB antenna; a dev board rather than a bare module because assembly is by hand | local / AliExpress |
| `U2` | **HLW8032** energy metering IC | SOIC-8 | dedicated 24-bit metering front end; one-way 4800-baud UART out; cheap and widely stocked. Pin 8 (RX) is a reserved port the datasheet says not to use, and is left open | LCSC `C128023` |
| `IC1` | **DS1307** RTC | **DIP-8** | keeps time through mains loss. Bare chip, never a module — both the DS3231 and DS1307 modules carry charging circuits that destroy a normal CR2032 | LCSC `C1520446` (SOIC-8 — see §6) |
| `T1` | **ZMPT101B** voltage transformer | 4-pin block | galvanic isolation on the voltage channel. **Bare transformer, not the blue op-amp board.** Retained rather than replaced by a resistor divider because the HLW8032 reference design ties GND to neutral — with L and N swapped, a divider would put the clamp cable and USB port at 230 V | AliExpress / local |
| `PS1` | **HLK-5M05** AC-DC module | 34 × 20 mm | isolated transformer type, not a capacitive dropper. This module *is* the isolation barrier for the low-voltage side | AliExpress / local |
| — | **SCT-013-000** split-core CT | external, cabled | 100 A : 50 mA current output, 13 mm aperture. Biggest single line item, roughly a third of the BOM | AliExpress / local |
| `Y1` | 32.768 kHz crystal | 3.2 × 8.3 mm vertical | **must be 12.5 pF** — the DS1307 has its load capacitors on-chip, so a 6 pF crystal runs the clock minutes/day slow | LCSC `C52082` (2 × 6 mm — see §6) |
| `BT1` | CR2032 holder + cell | through-hole | battery goes **directly** to the RTC battery pin — no diode, no resistor, no charging. 0.84 µA gives 8–10 years | local |

### Mains and safety

| Ref | Part | Why | Source |
|---|---|---|---|
| `P1` | **KF128-5.08-2P-AA** screw terminal | mains in. 5.08 mm pitch. A 2-pin screw terminal footprint is just two holes at the pitch, so brands are interchangeable — unlike an audio jack, which is why this won over a 3.5 mm socket | LCSC `C474952` |
| `J1` | **JST B2B-XH-AM** | clamp input. Deliberately a **different, physically incompatible** connector from `P1`, so mains cannot be screwed into the clamp terminal by mistake. This mechanical exclusion replaced an earlier fuse + surge-thyristor protection scheme | LCSC |
| `F1` | Fuse **250 mA slow-blow, 250 VAC**, 5 × 20 mm glass + clips | must be 250 VAC rated. Never an SMD fuse — most are 63 V parts that arc over instead of interrupting | local |
| `R4` | MOV **14D471K** (470 V, 14 mm) | surge clamp L–N. The one real high-current event on the board | local / LCSC |
| `C5` | **X2 safety capacitor, 100 nF, 275 VAC** | **fails open.** An ordinary ceramic with the same `104` marking fails **short**, across the mains. Never substitute | local / LCSC |
| `R5` `R8` `R10` `R13` | 47 kΩ 1 %, **metal film, through-hole axial**, ¼–½ W | must stay through-hole: full mains sits across the chain, a long body fails open, and a chip resistor can arc across itself under surge. **Never one 188 kΩ part instead of four** | LCSC `C410613`, or local (metal film = blue body, not carbon = beige) |
| `D3` `D4` | **SMAJ5.0CA** bidirectional TVS | `D3` on the ZMPT secondary, `D4` on the clamp input | LCSC / local |

### Measuring path — accuracy critical

| Ref | Value | Spec that matters | Why |
|---|---|---|---|
| `R16` | **0.68 Ω** burden | **≤100 ppm/°C**, ideally ≤50; ±1 % | **The most important part on the board.** Tolerance calibrates out via a per-unit constant; **temperature coefficient cannot**. Metal oxide at ±200–300 ppm/°C drifts 0.9–1.4 % over a 45 °C panel swing and **over-reports in summer**, when the AC load is highest. Power rating is irrelevant — it dissipates 0.0007 W |
| `R15` `R17` | 1.5 kΩ | ≤100 ppm/°C, **matched pair from one reel** | series into IP/IN. Their matching to each other matters more than their absolute value |
| `R14` | **300 Ω** | ordinary 1 % is fine | ZMPT secondary burden. Does not need low tempco because the reading depends on the **ratio** `R14 ÷ 188 kΩ` and both sides drift together. Raised from an earlier 150 Ω, which used only 37 % of the HLW8032's voltage range |
| `R12` | 1 kΩ | ordinary 1 % | series into VP with `C9` |
| `C10` | 33 nF | X7R | differential filter across IP/IN |
| `C11` `C12` | 10 nF | X7R | common-mode filter IP/IN to AGND |
| `C9` | 33 nF | X7R | VP filter |

All of these stay surface-mount — not because through-hole is less accurate,
but because the signal is ~20 mV next to a switching supply, and a
through-hole resistor's 10 mm legs are an antenna.

### Housekeeping

| Ref | Value | Role | Note |
|---|---|---|---|
| `R2` `R3` | 4.7 kΩ | I²C pull-ups | **must go to 3.3 V, never 5 V** — the ESP32 is not 5 V tolerant. See §3.1 |
| `R11` `R6` | 1 kΩ / 2 kΩ | divider on HLW8032 TX | shifts the 5 V UART output to 3.3 V for IO16 |
| `R1` `R9` | 330 Ω | LED series | see §3.2 |
| `R7` | 0 Ω link | the single ANALOG_GROUND ↔ GND tie | must sit at the star point; everything else keeps the two grounds separate |
| `C3` | 470 µF | HLK output bulk | 105 °C rated. 8 mm diameter — the tallest/widest part on the low-voltage side |
| `C4` `C8` | 100 nF | 5 V decoupling | |
| `C1` `C2` | 10 µF / 100 nF | 3.3 V decoupling | |
| `C6` `C7` | 100 nF / 10 µF | HLW8032 VDD decoupling, fed through `FB1` | |
| `FB1` | ferrite bead | isolates the metering chip's supply from ESP32 Wi-Fi current bursts | |

### Verified LCSC parts (all JLCPCB "Basic", UNI-ROYAL thick film, ±1 %, ±100 ppm/°C)

| Value | LCSC | Used for |
|---|---|---|
| 1 kΩ | `C17513` | `R11`, `R12` |
| 1.5 kΩ | `C4310` | `R15`, `R17` |
| 2 kΩ | `C17604` | `R6` |
| 4.7 kΩ | `C17673` | `R2`, `R3` |
| 150 Ω | `C17471` | (was `R14`, now 300 Ω — needs a new part number) |
| 0 Ω | `C17477` | `R7` |
| 47 kΩ THT | `C410613` | `R5` `R8` `R10` `R13` |
| 100 nF | `C49678` | |
| 10 µF | `C15850` | |
| 33 nF | `C1739` | |
| 10 nF | `C1710` | |
| 1 Ω / 2.2 Ω | `C25271` / `C17521` | `R16` fallback — 1 ∥ 2.2 = 0.6875 Ω, within 1 % of 0.68 Ω, both always in stock |

`R16` has three sourcing routes because no single catalogue number is certain:
a current-sense chip resistor (best), a through-hole metal film part (check its
tempco — often only ±250 ppm/°C at this value), or the two-resistor parallel
fallback. **Lay `R16` out as two 1206 pads in parallel** so any route drops in.

---

## 6. Known drift between the parts list and the current schematic/PCB

`hardware/parts-to-buy.md` predates several design changes. A reviewer should
treat the schematic and PCB as authoritative and reconcile these:

| Item | Parts list says | Board actually has |
|---|---|---|
| ESP32 board | "ESP32 Type-C, **30 pins**" | **38-pin** `MODULE_ESP32-DEVKITC-32` footprint (2 × 19) |
| Power module | **HLK-PM01** (3 W) | **HLK-5M05** (5 W), footprint `CONV_HLK-5M05` |
| `C3` | 470 µF **16 V** | schematic says 470 µF **10 V** |
| `IC1` package | DS1307**Z+**, SOIC-8 (`C1520446`) | **DIP-8** footprint `DIP794W47P254L991H457Q8` |
| `Y1` | 2 × 6 mm cylindrical (`C52082`) | **3.2 × 8.3 mm** footprint `XTAL_D3.2xL8.3_P2.00_Vertical` |
| Clamp connector | KF128-2.54-2P screw terminal (`C474920`) | **JST B2B-XH-AM** (`J1`) |
| Clamp protection | fuse #16a + SMP100LC-65 surge thyristor #16b | **both removed** — replaced by connector incompatibility |
| `R14` / `Rv5` | 150 Ω | **300 Ω** |
| LED resistors | 1 kΩ | **330 Ω** (`R1`, `R9`) |
| Passive package | 0805 throughout | **1206 and 2512** on the board |

The parts list also uses an older designator scheme. Mapping:

`Rb` → `R16` · `Rv1`–`Rv4` → `R5` `R8` `R10` `R13` · `Rv5` → `R14` ·
`Rf1` → `R12` · `Rf2`/`Rf3` → `R15`/`R17` · `Rls1`/`Rls2` → `R11`/`R6` ·
`R5`/`R6` (old) → `R2`/`R3`

---

## 7. Questions worth a second opinion

1. **§3.1 and §3.2** above — the two confirmed problems. What is the cleanest
   fix given hand assembly and local sourcing?
2. **CT aperture.** The `SCT-013-000` has a **13 mm** opening. A 63 A service
   is typically 16 mm² copper, around 8–9 mm outside diameter with insulation;
   25 mm² is closer to 11 mm. Is 13 mm enough margin for real Syrian
   installations, including where two conductors share a duct?
3. **CT accuracy class.** The `SCT-013-000` is a hobby-grade part with no
   stated accuracy or phase-error specification. At 69 % of the ADC range the
   electronics are fine, but the CT may dominate total error. Is there a better
   part at this price, and what phase error should the firmware correct for?
4. **One channel on a 63 A single-phase service** — is any of the installed
   base actually three-phase or split-phase, in which case one clamp measures
   only part of the load?
5. **`R16` tempco** — is ≤100 ppm/°C the right line to draw, and does the
   parallel 1 Ω ∥ 2.2 Ω fallback hold that spec in practice?
6. **`C5` at 100 nF X2** — 7.2 mA of continuous reactive current. Is a smaller
   X2 value sufficient for the filtering it is there to do?
7. **`F1` at 250 mA slow-blow** — the board draws ~39 mA steady with a
   capacitive-input inrush. Is 250 mA the right rating, and does it clear a
   fault fast enough to matter given the house breaker is 63 A?
8. **Lifetime of `C3`** — a 470 µF electrolytic inside a sealed, printed
   enclosure in a Syrian distribution board. 105 °C rated, but what is the
   expected service life at the real internal temperature, and should it be a
   polymer or a solid part instead?
9. **ESP32 dev board consistency.** These boards change silently between
   production runs. Is "buy all 1,050 from one batch" adequate risk control for
   a 1,000-unit product, or does this position need a module and a proper
   footprint eventually?

## 8. Already checked — do not spend time re-deriving

- Current and voltage channel scaling against the HLW8032's real datasheet
  ranges (§4).
- 47 kΩ chain dissipation: 70 mW each.
- Mains trace current: ~39 mA against a ~2 A track rating; no load current
  crosses the board.
- Surge heating: 1.6 kA for 8/20 µs raises a 1.5 mm 1 oz trace 93 °C
  adiabatically, 23 °C in 2 oz.
- `U2` pin 8 is a reserved port the datasheet says not to use, and is
  correctly left open.
- ESP32 pin assignment: IO23/IO22 for I²C and IO16 for the metering UART are
  all free of boot straps. IO12 in particular must never see a pull-up.
