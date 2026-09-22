# 9. Schematic Netlist — Connection-by-Connection

Everything you need to draw the schematic in Altium Designer. **Every net, every
pin.** Work through §9.5 top to bottom and the schematic is complete.

---

## 9.1 Read this first

### Pins are named, not numbered — on purpose

Nets below reference pins by **signal name** (`VDD`, `EN`, `IO16`, `SDA`), not
by pin number. Altium symbols carry named pins, so this is how you will actually
wire it, and it protects you from a transcription error in a pin table.

### ⚠️ Three things you must confirm from datasheets before routing

| Item | What to confirm | Why |
|---|---|---|
| **U2 HLW8032 pinout** | Map `VDD`, `GND`, `I+`, `I−`, `V_IN`, `TX`, `PF` to real pin numbers from the **Hiliwei HLW8032 user manual Rev 1.5**, and identify the 8th pin (likely a reference or second ground). | It is an 8-pin part and I will not guess its pin order for you. |
| **T1 ZMPT101B primary vs secondary** | Which pin pair is the primary. | The part has 4 pins and the pairs look identical. Getting it backwards gives no signal. |
| **U2 current-channel common-mode range** | That a ground-referenced CT sits inside it. | The chip was designed for a shunt. See §9.6. |

### Domains

Two electrically separate regions. **Nothing crosses the barrier except PS1 and
T1**, which are built to cross it.

| Domain | Nets | Treat as |
|---|---|---|
| **MAINS** | `MAINS_L`, `MAINS_L_FUSED`, `MAINS_N`, `VDIV_A…D` | Live at all times |
| **SELV** | everything else | Safe to touch |

---

## 9.2 Component list for Altium

| Designator | Value | Footprint | Library note |
|---|---|---|---|
| J1 | Screw terminal 2P 5.08 mm | `TERM-2P-5.08` | **Make this** — check your actual part's drill and body |
| F1 + FH1 | Fuse 250 mA T 250 VAC | `FUSE-5x20-CLIPS` | **Make this** — two clips, 5 × 20 mm barrel between them |
| RV1 | MOV 14D471K | `MOV-14D` | **Make this** — 14 mm disc, ~7.5 mm lead pitch |
| C1 | X2 100 nF 275 VAC | `CAP-X2-BOX` | **Make this** — measure your part |
| PS1 | HLK-PM01 | `HLK-PM01` | **Make this** — 34 × 20 mm, 4 pins |
| Rv1–Rv4 | 47 kΩ ½ W MF | `AXIAL-0.4` | Standard axial |
| T1 | ZMPT101B | `ZMPT101B` | **Make this** — 4 pins |
| C2, C4 | 470 µF electrolytic | `CAP-RADIAL-D8` | Standard radial |
| U1 | AMS1117-3.3 | `SOT-223-4` | Altium standard |
| D1 | 1N4148W | `SOD-123` | Altium standard |
| U2 | HLW8032 | `SOIC127P600X175-8N` | SOP-8 standard |
| U3 | ESP32-WROOM-32E-N8 | `ESP32-WROOM-32E` | Espressif provides one; else make it |
| U4 | DS3231SN | `SOIC127P1032X265-16N` | SOIC-16 standard |
| D2, D3 | SMAJ5.0CA | `SMA` / `DO-214AC` | Altium standard |
| J2 | Screw terminal 2P 3.5 mm | `TERM-2P-3.5` | **Make this** |
| J3 | Header 1 × 6, 2.54 mm | `HDR1X6` | Altium standard |
| SW1 | Tact 6 × 6 mm THT | `SW-TACT-6x6` | **Make this** — see §9.5.9 warning |
| BT1 | CR2032 holder | `BATT-CR2032-THT` | **Make this** |
| LED1, LED2 | LED 0805 | `LED-0805` | Standard |
| All R, C | 0805 | `0805` | Standard |
| FB1 | Ferrite bead | `0805` | Standard |
| R7 | 0 Ω | `0805` | Or Altium `NetTie` — see §9.4 |
| U5 | W25Q64 — **DNP** | `SOIC127P600X175-8N` | Footprint only, do not fit |

---

## 9.3 Net classes

Create these in Altium before routing — the design rules in §9.7 hang off them.

| Class | Nets | Min width | Clearance to SELV |
|---|---|---|---|
| **MAINS** | `MAINS_L`, `MAINS_L_FUSED`, `MAINS_N`, `VDIV_A`, `VDIV_B`, `VDIV_C`, `VDIV_D` | 1.5 mm | **8 mm** |
| **ANALOG** | `V_SENSE`, `V_FILT`, `I_SENSE_P`, `I_FILT_P`, `I_FILT_N` | 0.3 mm | — |
| **POWER** | `+5V`, `+5V_A`, `+3V3` | 0.8 mm | — |
| **DIGITAL** | everything else | 0.25 mm | — |

---

## 9.4 Ground: two nets, one link

There are **two** ground nets, joined at exactly one point:

- **`GND`** — digital/power return. ESP32, LDO, RTC, LEDs, button, header.
- **`AGND`** — analog island. Metering IC, burden resistors, filters, the CT
  cold leg, the ZMPT secondary.
- **`R7` (0 Ω, 0805)** is the only connection between them. Place it **directly
  under the metering IC**.

This stops the ESP32's 500 mA Wi-Fi transmit bursts returning through the analog
ground, where they would appear as measurement noise on a 26 mV signal.

> In Altium you can use a `NetTie` component instead of a 0 Ω resistor. The
> NetTie is cleaner for DRC; the 0 Ω resistor is easier to understand and gives
> you a place to cut the link if you ever need to debug ground coupling. Either
> is fine — **just make sure it is a single, deliberate point.**

---

## 9.5 The complete netlist

### 9.5.1 Mains input — ⚡ LIVE

```
                    F1
  J1.1 ──────────●──▭▭▭──●──┬──────────┬──────────┬────────── PS1.AC-L
       MAINS_L            │  │          │          │
                          │ RV1        C1         Rv1.1
                          │  │          │          │
  J1.2 ──────────●────────┴──┴──────────┴──────────┼────────── PS1.AC-N
       MAINS_N                                     │
                                                   ↓ (voltage divider, 9.5.2)
```

| Net | Connections |
|---|---|
| `MAINS_L` | **J1.1**, **F1.1** |
| `MAINS_L_FUSED` | **F1.2**, **RV1.1**, **C1.1**, **PS1.AC-L**, **Rv1.1** |
| `MAINS_N` | **J1.2**, **RV1.2**, **C1.2**, **PS1.AC-N**, **T1.P2** |

**Wire it in this order:**
1. `J1.1` → `F1.1`. That is the whole `MAINS_L` net — nothing else touches it.
2. `F1.2` out to a junction. Everything else on the live side hangs off the
   **fused** side.
3. From that junction: `RV1.1`, `C1.1`, `PS1.AC-L`, and `Rv1.1` (divider input).
4. `J1.2` to a second junction: `RV1.2`, `C1.2`, `PS1.AC-N`, `T1.P2`.

> ⚠️ **RV1 and C1 must be on the FUSED side.** A MOV fails short at end of life.
> Upstream of the fuse that is an unprotected L-N short — a fire. Downstream it
> simply blows the fuse.

### 9.5.2 Voltage divider into the transformer — ⚡ LIVE

```
 MAINS_L_FUSED ──[Rv1]──[Rv2]──[Rv3]──[Rv4]── T1.P1
   (Rv1..Rv4 = 47k each, total 188k)          T1.P2 ── MAINS_N
```

| Net | Connections |
|---|---|
| `VDIV_A` | **Rv1.2**, **Rv2.1** |
| `VDIV_B` | **Rv2.2**, **Rv3.1** |
| `VDIV_C` | **Rv3.2**, **Rv4.1** |
| `VDIV_D` | **Rv4.2**, **T1.P1** |

Four resistors in series, nothing else on the intermediate nets. Reasons for
four rather than one are in [`docs/02-circuit.md`](02-circuit.md) §2.3.

**This is the last mains net.** Everything below is SELV.

### 9.5.3 Power rails

```
 PS1.+Vo ──●──┬────┬──────┬───────[FB1]──●── +5V_A ──┬────┬──── U2.VDD
    +5V     C2.+  C3.1  D1.K  U1.VIN              C7.1  C8.1
                                 │
                            U1 AMS1117-3.3
                                 │
 U1.VOUT + TAB ──●── +3V3 ──┬────┬────┬─────┬──── (see table)
                           C4.+ C5.1 C6.1  D1.A
```

| Net | Connections |
|---|---|
| `+5V` | **PS1.+Vo**, **C2.+**, **C3.1**, **D1.K** (cathode), **U1.VIN**, **FB1.1** |
| `+5V_A` | **FB1.2**, **C7.1**, **C8.1**, **U2.VDD** |
| `+3V3` | **U1.VOUT**, **U1.TAB**, **D1.A** (anode), **C4.+**, **C5.1**, **C6.1**, **U3.3V3**, **U4.VCC**, **C13.1**, **R1.1**, **R2.1**, **R5.1**, **R6.1**, **J3.1** |
| `GND` | **PS1.−Vo**, **C2.−**, **C3.2**, **U1.GND**, **C4.−**, **C5.2**, **C6.2**, **U3.GND** *(every GND pin and pad)*, **U4.GND**, **C13.2**, **C12.2**, **Rls2.2**, **SW1.2**, **LED1.K**, **LED2.K**, **BT1.−**, **J3.2**, **R7.1** |

**Notes:**
- **D1 orientation matters:** cathode (banded end) to `+5V`, anode to `+3V3`. It
  conducts only if a programmer back-feeds 3.3 V into an unpowered board.
- **AMS1117 in SOT-223: the tab is VOUT**, not ground. Tie it to `+3V3` and give
  it ≥200 mm² of copper.
- **FB1 splits the 5 V rail.** `+5V` feeds the LDO; `+5V_A` feeds only the
  metering IC. Nothing else may connect to `+5V_A`.

### 9.5.4 Voltage sense chain

```
 T1.S1 ──●──┬──────┬──────[Rf1 1k]──●── V_FILT ── U2.V_IN
 V_SENSE   Rv5.1  D3.1                │
           Rv6.1                    Cf1.1
              │      │                │
 T1.S2 ──────┴──────┴────────────────┴──── AGND
```

| Net | Connections |
|---|---|
| `V_SENSE` | **T1.S1**, **Rv5.1**, **Rv6.1** *(DNP)*, **D3.1**, **Rf1.1** |
| `V_FILT` | **Rf1.2**, **Cf1.1**, **U2.V_IN** |

`T1.S2`, `Rv5.2`, `Rv6.2`, `D3.2`, `Cf1.2` all go to **`AGND`**.

`Rv6` is an unpopulated footprint in parallel with `Rv5`, for trimming the
voltage range on prototypes without cutting traces.

### 9.5.5 Current sense chain

```
        J2.1 ──●──┬──────┬──────[Rf2 1.5k]──●── I_FILT_P ── U2.I+
   I_SENSE_P     Rb.1   D2.1                 │       │
                 Rb2.1                     Cf2.1   Cf3.1
                   │      │                  │       │
        J2.2 ──────┴──────┴──[Rf3 1.5k]──●───┴───────┼── I_FILT_N ── U2.I−
           (= AGND)                        │         │
                                         Cf2.2     Cf4.1
                                                     │
                                                    AGND
```

| Net | Connections |
|---|---|
| `I_SENSE_P` | **J2.1**, **Rb.1**, **Rb2.1** *(DNP)*, **D2.1**, **Rf2.1** |
| `I_FILT_P` | **Rf2.2**, **Cf2.1**, **Cf3.1**, **U2.I+** |
| `I_FILT_N` | **Rf3.2**, **Cf2.2**, **Cf4.1**, **U2.I−** |

`J2.2`, `Rb.2`, `Rb2.2`, `D2.2`, `Rf3.1`, `Cf3.2`, `Cf4.2` all go to **`AGND`**.

**Wire it in this order:**
1. `J2.1` → `Rb.1` → `D2.1`, all bunched tightly together.
2. `J2.2` → `Rb.2` → `D2.2` → `AGND`. **This is the CT's cold leg** — the
   single point that references the clamp to the board.
3. `Rb2` in parallel with `Rb` (unpopulated, for range trimming).
4. `I_SENSE_P` → `Rf2` → `I_FILT_P`.
5. `AGND` → `Rf3` → `I_FILT_N`. **Rf3 must be present even though it goes to
   ground** — it balances the impedance on both legs, which is what preserves
   common-mode rejection.
6. `Cf2` between `I_FILT_P` and `I_FILT_N` (differential).
7. `Cf3` from `I_FILT_P` to `AGND`; `Cf4` from `I_FILT_N` to `AGND`.

> ⚠️ **`Rf2` and `Rf3` must be identical.** They set the phase compensation
> ([§2.5.3](02-circuit.md)) *and* the common-mode rejection. When you tune the
> value on prototypes, **change both**.

### 9.5.6 Metering IC to MCU — the level shifter

```
 U2.TX ──[Rls1 1k]──●── HLW_TX_3V3 ── U3.IO16 (UART2 RX)
                    │
                 [Rls2 2k]
                    │
                   GND
```

| Net | Connections |
|---|---|
| `HLW_TX_5V` | **U2.TX**, **Rls1.1** |
| `HLW_TX_3V3` | **Rls1.2**, **Rls2.1**, **U3.IO16** |
| `HLW_PF` *(optional)* | **U2.PF**, **U3.IO4** |

`Rls2.2` → `GND`. `U2.GND` → **`AGND`** (not `GND` — see §9.4).

> ⚠️ **Never connect U2.TX directly to the ESP32.** The HLW8032 runs on 5 V and
> ESP32 GPIOs are not 5 V tolerant. `5 V × 2k/(1k+2k) = 3.33 V` ✓
>
> ⚠️ **IO16 is UART2, not UART0.** UART0 (`TXD0`/`RXD0`) is the programming port
> at J3. If the meter streams into it you can neither flash nor debug the board.

### 9.5.7 Real-time clock

| Net | Connections |
|---|---|
| `I2C_SDA` | **U4.SDA**, **R5.2**, **U3.IO21** |
| `I2C_SCL` | **U4.SCL**, **R6.2**, **U3.IO22** |
| `VBAT` | **U4.VBAT**, **BT1.+** |

`U4.VCC` and `C13.1` → `+3V3`. `U4.GND`, `C13.2`, `BT1.−` → `GND`.
`R5.1`, `R6.1` → `+3V3`.

Leave `U4.32kHz`, `U4.RST`, `U4.INT/SQW` and all `N.C.` pins **unconnected**.

> ⚠️ **Nothing else touches `VBAT`.** No diode, no resistor, no trickle charger.
> The CR2032 is non-rechargeable; the charging circuit on the common blue DS3231
> breakout boards would make it vent or rupture. The DS3231 switches over
> internally.

### 9.5.8 ESP32 boot and programming

```
 +3V3 ──[R1 10k]──●── EN ──┬── U3.EN
                           └── J3.5
                        [C12 1uF]
                           │
                          GND

 +3V3 ──[R2 10k]──●── IO0 ──┬── U3.IO0
                            ├── J3.6
                            └── SW1.1     SW1.2 ── GND
```

| Net | Connections |
|---|---|
| `EN` | **U3.EN**, **R1.2**, **C12.1**, **J3.5** |
| `IO0` | **U3.IO0**, **R2.2**, **SW1.1**, **J3.6** |
| `TXD0` | **U3.TXD0** *(IO1)*, **J3.3** |
| `RXD0` | **U3.RXD0** *(IO3)*, **J3.4** |

**J3 pinout, print it on the silkscreen:**

| Pin | Net |
|---|---|
| 1 | `+3V3` |
| 2 | `GND` |
| 3 | `TXD0` |
| 4 | `RXD0` |
| 5 | `EN` |
| 6 | `IO0` |

The auto-reset transistors live on your **programming jig**, not on the board —
saves 4 parts × 1,000 units. Jig circuit in
[`docs/04-calibration-and-test.md`](04-calibration-and-test.md) §4.6.

### 9.5.9 LEDs and button

```
 U3.IO25 ──[R3 1k]──▶|── GND      (LED1 green)
 U3.IO26 ──[R4 1k]──▶|── GND      (LED2 blue)
```

| Net | Connections |
|---|---|
| `LED1_DRV` | **U3.IO25**, **R3.1** |
| `LED1_A` | **R3.2**, **LED1.A** (anode) |
| `LED2_DRV` | **U3.IO26**, **R4.1** |
| `LED2_A` | **R4.2**, **LED2.A** (anode) |

`LED1.K`, `LED2.K` → `GND`.

> ⚠️ **6 × 6 mm tact switches have 4 pins, internally paired.** Pins 1–2 are
> shorted to each other, and 3–4 are shorted to each other. You must connect
> across the *switched* pair (1 and 3, or 2 and 4). Connecting 1 and 2 gives you
> a permanent short. Check your footprint's pin numbering against the part.

### 9.5.10 ESP32 pins — leave these alone

| Pin | Do |
|---|---|
| **IO12** | **Leave completely unconnected.** It selects flash voltage at boot; pulled high, the module fails to start. |
| **IO6–IO11** | **Never use.** Wired to the module's internal flash. |
| IO2, IO15 | Strapping pins. Leave unconnected. |
| IO34–IO39 | Input only — cannot drive an LED. |
| IO5, IO18, IO19, IO23 | Free (VSPI). Route to the U5 footprint if you want the optional flash. |
| IO17 | Free. UART2 TX — unused, the HLW8032 cannot receive. |

---

## 9.6 Confirm against datasheets before you route

| # | Check | Where |
|---|---|---|
| 1 | HLW8032 pin numbers for all 8 pins | Hiliwei user manual Rev 1.5 |
| 2 | HLW8032 **current-channel common-mode range** includes a ground-referenced CT | Same. The chip was designed for a shunt; this is the one architectural assumption in the design that a datasheet could overturn. |
| 3 | HLW8032 **full-scale input** (current and voltage, at the pin) | Same. Sets `Rb` and `Rv5` — see [§3.3](02-circuit.md). |
| 4 | HLW8032 recommended **source impedance** on the analog inputs | Same. `Rf2`/`Rf3` at 1.5 kΩ should be fine; confirm before going higher. |
| 5 | ZMPT101B primary vs secondary pin pair | ZMPT101B datasheet or part marking |
| 6 | HLK-PM01 pin order | Printed on the module body |
| 7 | Your tact switch's internal pin pairing | Part datasheet |

---

## 9.7 Altium design rules

| Rule | Value | Scope |
|---|---|---|
| **Clearance: MAINS ↔ SELV** | **8 mm** | Net class to net class |
| Clearance: MAINS ↔ MAINS | 3.5 mm | Within class |
| Clearance: everything else | 0.2 mm | Default |
| Width: MAINS | 1.5 mm min | MAINS class |
| Width: POWER | 0.8 mm | POWER class |
| Width: DIGITAL/ANALOG | 0.25 mm | Default |
| Mains copper ↔ board edge | 4 mm | Board outline |
| Mains copper ↔ mounting hole | 4 mm | Hole clearance |

**Also set up:**
- A **board cutout (routed slot) 2–3 mm wide** along the isolation barrier,
  passing under T1 and beside PS1. This makes the creepage path physically
  infinite there.
- **No polygon pour crosses the barrier.** Pour `GND`/`AGND` on the SELV side
  only; pour nothing on the mains side.
- **Antenna keep-out:** a no-copper region on both layers under and around the
  ESP32's antenna, extending ≥10 mm (15 mm is better). No vias, no pour, no
  silkscreen ink.

---

## 9.8 Checklist before you route

**Schematic**
- [ ] `GND` and `AGND` are separate nets, joined only by `R7`
- [ ] `U2.GND` goes to `AGND`, not `GND`
- [ ] Nothing but `FB1`, `C7`, `C8`, `U2.VDD` is on `+5V_A`
- [ ] `D1` cathode on `+5V`, anode on `+3V3`
- [ ] `U1` SOT-223 tab tied to `+3V3`
- [ ] `Rf2` and `Rf3` are the same value
- [ ] `Rls1` = 1 kΩ, `Rls2` = 2 kΩ, and the tap goes to **IO16**, not IO3
- [ ] `IO12` has nothing on it
- [ ] `VBAT` has exactly two connections: `U4.VBAT` and `BT1.+`
- [ ] `Rb2`, `Rv6`, `U5` are marked **DNP** / no-BOM
- [ ] Run **ERC**: no floating inputs, no nets with a single pin

**Layout**
- [ ] 8 mm clearance holds everywhere between mains and SELV
- [ ] Routed slot present on the barrier
- [ ] `Rb` is within a few millimetres of `J2`
- [ ] CT traces routed as a symmetrical differential pair, away from PS1 and the antenna
- [ ] `C4` (470 µF) within 10 mm of `U3.3V3`
- [ ] Antenna keep-out clear on both layers
- [ ] `R7` placed directly under `U2`
- [ ] Test points on `+3V3`, `+5V`, `GND`, `V_FILT`, `I_FILT_P`, `I_FILT_N`
- [ ] Silkscreen: `⚡ MAINS — DANGER`, dashed barrier line, `L`/`N` at J1, `CT` at J2, full J3 pinout

---

## 9.9 Suggested schematic sheet layout

One sheet is enough, arranged left to right in signal order:

```
 ┌────────────────┬────────────────┬────────────────┬────────────────┐
 │  A. MAINS IN   │  B. PSU        │  D. CURRENT    │  F. ESP32      │
 │  J1 F1 RV1 C1  │  PS1 C2 C3     │  J2 Rb D2      │  U3 R1 R2 C12  │
 │                │  U1 D1 C4-C6   │  Rf2 Rf3 Cf2-4 │  C4 SW1 J3     │
 ├────────────────┤                ├────────────────┤  LED1 LED2     │
 │  C. VOLTAGE    │                │  E. METERING   ├────────────────┤
 │  Rv1-Rv4 T1    │                │  U2 FB1 C7 C8  │  G. RTC        │
 │  Rv5 Rf1 Cf1   │                │  Rls1 Rls2 R7  │  U4 BT1 R5 R6  │
 │  D3            │                │                │  C13           │
 └────────────────┴────────────────┴────────────────┴────────────────┘
   ⚡ LIVE — draw a red box around blocks A and C and label it
```

Draw a **visible boundary on the schematic sheet** around the mains blocks with
a text note. Anyone who opens this file later should see the hazard in the first
two seconds.
