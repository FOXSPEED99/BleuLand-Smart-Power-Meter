# The Complete Wiring Guide

**Every single connection in this device, written so anyone can follow it.**

Each connection names the **real part** and the **real leg** you are connecting.
Work through it section by section and the circuit will be complete and correct.

---

# ⚠️ READ THIS BEFORE ANYTHING ELSE

This device connects directly to **230 V mains electricity, which can kill you.**

- **Never** work on the board while it is connected to mains.
- **Never** touch the mains section while power is on.
- Always test with the power off first.
- When you must power it up, use an **isolation transformer** and an **RCD /
  earth-leakage breaker** on your bench.
- The parts in **Sections A, B and C** are dangerous. Treat them as live at all
  times, even when you think the power is off.

There is a **safety barrier** running across the middle of this board. On one
side everything sits at mains voltage. On the other side everything is safe to
touch. **Nothing may cross that barrier** except the two components designed to
cross it: the HLK-PM01 power module and the ZMPT101B transformer.

---

# 1. What this circuit does

A clamp goes around the main electricity cable of the house. It never touches
the wire inside — it measures the magnetic field around it. That is how we
measure current without cutting anything.

Separately we tap the live and neutral wires for two jobs: to power the device,
and to measure the real mains voltage.

The measuring chip combines current and voltage into real power in watts. The
ESP32 board reads that, saves it, and sends it over WiFi.

```
   House main cable  ══════╪══════
                        ╭──┴──╮
                        │clamp│════╗
                        ╰─────╯    ║
                                   ▼
  Live  ──┬──[fuse]──────────────► HLW8032 ──► ESP32 ──► WiFi
          │                        chip        board
  Neutral ┴──────────────────────►
```

---

# 2. Part name key — what each label means

Every part has a **label** printed on the board (`R3`, `C2`, and so on). This
table tells you what to actually buy and what its legs are called.

## Mains side — DANGEROUS

| Label | The real part | Its legs are called |
|---|---|---|
| `J1` | **2-way screw terminal, 5.08 mm** (KF301-2P or similar) | Two screw holes. Mark them **LIVE** and **NEUTRAL** on the silkscreen |
| `F1` | **Glass fuse, 5 × 20 mm, 250 mA slow-blow, 250 VAC** | Two metal end caps — **no polarity** |
| `FH1` | **Two PCB fuse clips** | One clip holds each end of the fuse |
| `RV1` | **Varistor 14D471K** — the blue disc | Two wire legs — **no polarity** |
| `C1` | **X2 safety capacitor, 100 nF 275 VAC** — the yellow or blue box | Two wire legs — **no polarity** |
| `PS1` | **HLK-PM01** power module | **Printed on the module itself:** `AC-L`, `AC-N`, `+Vo`, `-Vo` |
| `Rv1` `Rv2` `Rv3` `Rv4` | **47 kΩ, 1 %, ½ W metal film resistors** (through-hole) | Two wire legs each — **no polarity** |
| `T1` | **ZMPT101B** voltage transformer — small black block, 4 pins | **Primary pair** (input side) and **secondary pair** (output side). ⚠️ Identify which pair is which from the datasheet or by measuring resistance — they look identical |

## Safe side

| Label | The real part | Its legs are called |
|---|---|---|
| `C2` | **Electrolytic capacitor, 470 µF 16 V, 105 °C** | **+ (positive)** — the longer leg. **− (negative)** — marked with a stripe on the can |
| `C3` `C6` `C8` | **Ceramic capacitor, 100 nF, 0805** | Two ends — **no polarity** |
| `C5` `C7` | **Ceramic capacitor, 10 µF, 0805** | Two ends — **no polarity** |
| `Cf1` `Cf2` | **Ceramic capacitor, 33 nF, 0805** | Two ends — **no polarity** |
| `Cf3` `Cf4` | **Ceramic capacitor, 10 nF, 0805** | Two ends — **no polarity** |
| `FB1` | **Ferrite bead, 600 Ω @ 100 MHz, 0805** | Two ends — **no polarity** |
| `U2` | **HLW8032** metering chip, SOP-8 (8 legs) | `VDD` (power), `GND` (ground), `V1P` (voltage in), `I1P` and `I1N` (current in), `TX` (data out), `PF` (energy pulse). ⚠️ **Get the leg numbers from the HLW8032 datasheet** — do not guess them |
| `J2` | **2-way screw terminal, 3.5 mm** | Two screw holes, for the clamp's two wires |
| `CT1` | **Current clamp, SCT-013-000**, 100 A : 50 mA | Two wires coming out of its cable. **Not soldered** — they screw into `J2` |
| `Rb` | **0.68 Ω, 1 %, ≤50 ppm/°C precision resistor** | Two ends — **no polarity** |
| `Rv5` | **150 Ω, 1 %, ≤50 ppm/°C precision resistor** | Two ends — **no polarity** |
| `Rf1` `Rls1` `R3` `R4` | **1 kΩ, 1 %, 0805 resistors** | Two ends — **no polarity** |
| `Rf2` `Rf3` | **1.5 kΩ, 1 %, 0805 resistors** (matched pair) | Two ends — **no polarity** |
| `Rls2` | **2 kΩ, 1 %, 0805 resistor** | Two ends — **no polarity** |
| `R7` | **0 Ω link, 0805** | Two ends — **no polarity** |
| `D2` `D3` | **TVS diode SMAJ5.0CA** | Two ends — **bidirectional, so no polarity** |
| `U4` | **DS1307Z+** clock chip, SOIC-8 (8 legs) | `VCC` (power), `GND` (ground), `X1` and `X2` (crystal), `VBAT` (battery), `SDA` and `SCL` (data lines), `SQW/OUT` (unused). ⚠️ **Get the leg numbers from the DS1307 datasheet** |
| `Y1` | **Crystal, 32.768 kHz, 12.5 pF**, cylindrical 2 × 6 mm | Two wire legs — **no polarity** |
| `BT1` | **CR2032 battery holder**, through-hole | **+ (positive)** — the metal cup the battery sits in. **− (negative)** — the small tab that touches the battery's underside |
| `B1` | **CR2032 battery, 3 V** | Not soldered — it clips into `BT1`. Printed side (`+`) faces up |
| `R5` `R6` | **4.7 kΩ, 1 %, 0805 resistors** | Two ends — **no polarity** |
| `C13` | **Ceramic capacitor, 100 nF, 0805** | Two ends — **no polarity** |
| `MCU1` | **ESP32 development board** ("ESP32 Type-C", 30 pins) | **Printed on the board itself:** `VIN`, `GND`, `3V3`, `D16`, `D21`, `D22`, `D25`, `D26` |
| `J4` `J5` | **1 × 15 female header strips** | 15 holes each — the ESP32 board plugs in |
| `LED1` | **Green LED, 0805** | **Anode (+)** and **cathode (−)**. ⚠️ The cathode marking differs between makers — test one with a battery and a resistor before soldering a hundred |
| `LED2` | **Blue LED, 0805** | Same as above |

---

# 3. How to read the connection lists

Each line says: run a wire (or a copper track) **from** one place **to** another.

When several parts connect to the same place they form a **junction** — like
several wires twisted together. Everything listed at one junction is
electrically the same point.

---

# 4. The two ground zones — read this, it matters

Ground is the return path all electricity flows back through. This board has
**two separate ground zones** that meet at exactly one point.

| Zone | Name used in this guide | What connects to it |
|---|---|---|
| Noisy | **`GROUND`** | ESP32 board, LEDs, power supply |
| Quiet | **`ANALOG GROUND`** | Measuring chip, the clamp, all filter parts |

**Why:** the ESP32 gulps half an amp in short bursts when it transmits WiFi. The
measuring chip is reading signals of a few thousandths of a volt. If they share
a ground path, those bursts show up as noise in your measurements.

**The rule:** keep them separate everywhere, and join them at **one single
point** — the 0 Ω link `R7`, placed right beside the measuring chip.

```
   ┌─────────────────┐            ┌──────────────────┐
   │     GROUND      │──[ R7 ]────│  ANALOG GROUND   │
   │ (ESP32, LEDs,   │   0 ohm    │ (measuring chip, │
   │  power supply)  │  ONE POINT │  clamp, filters) │
   └─────────────────┘            └──────────────────┘
```

---

# SECTION A — Mains input ⚠️ DANGEROUS

```
                   F1 (fuse)
  J1 LIVE ──────────▭▭▭──────┬──────────┬──────────┬───── PS1 "AC-L"
                             │          │          │
                            RV1        C1        Rv1
                             │          │          (to Section C)
  J1 NEUTRAL ────────────────┴──────────┴──────────┴───── PS1 "AC-N"
                                                   │
                                                   └───── T1 primary
```

| # | From | To |
|---|---|---|
| **A1** | **Screw terminal** `J1` — **LIVE** screw | **Fuse clip** `FH1` — first clip |
| **A2** | **Fuse clip** `FH1` — second clip | **Junction "LIVE-FUSED"** |
| **A3** | Junction LIVE-FUSED | **Varistor** `RV1` — either leg |
| **A4** | Junction LIVE-FUSED | **X2 capacitor** `C1` — either leg |
| **A5** | Junction LIVE-FUSED | **HLK-PM01** `PS1` — the pin marked **`AC-L`** |
| **A6** | Junction LIVE-FUSED | **Resistor** `Rv1` — either end *(carries on into Section C)* |
| **A7** | **Screw terminal** `J1` — **NEUTRAL** screw | **Junction "NEUTRAL"** |
| **A8** | Junction NEUTRAL | **Varistor** `RV1` — its other leg |
| **A9** | Junction NEUTRAL | **X2 capacitor** `C1` — its other leg |
| **A10** | Junction NEUTRAL | **HLK-PM01** `PS1` — the pin marked **`AC-N`** |
| **A11** | Junction NEUTRAL | **ZMPT101B** `T1` — one leg of the **primary** pair |

*(The fuse `F1` itself is not soldered — it clips into `FH1` so it can be
replaced. `RV1`, `C1` and the resistors have no polarity, so either leg works.)*

### ⚠️ Critical rules for this section

1. **`RV1` and `C1` must be AFTER the fuse, never before it.** A varistor fails
   as a short circuit at the end of its life. After the fuse, that just blows the
   fuse. Before the fuse, it is a direct short across the mains — a fire.
2. **The fuse must be 250 VAC rated and slow-blow (marked `T`).** A 63 V SMD fuse
   cannot interrupt a mains fault and will explode.
3. **`C1` must be class X2.** X2 capacitors fail open-circuit by design. A normal
   ceramic capacitor here is a fire hazard.
4. Nothing in this section may come within **8 mm** of anything on the safe side.

---

# SECTION B — Power supply

The **HLK-PM01** module `PS1` takes 230 V in and gives 5 V out. It has a
transformer inside, and that is what makes everything after it safe to touch.

```
  PS1 "+Vo" ──┬──────┬────────┬────────────────► MCU1 "VIN"
              │      │        │
             C2 +   C3      FB1 ──┬────┬──────► U2 "VDD"
              │      │            │    │
  PS1 "-Vo" ──┴──────┴─ GROUND   C7   C8 ──► ANALOG GROUND
```

| # | From | To |
|---|---|---|
| **B1** | **HLK-PM01** `PS1` — the pin marked **`+Vo`** | **Junction "5 VOLTS"** |
| **B2** | Junction 5 VOLTS | **Electrolytic capacitor** `C2` — the **+ (positive)** leg |
| **B3** | Junction 5 VOLTS | **Ceramic capacitor** `C3` — either end |
| **B4** | Junction 5 VOLTS | **Ferrite bead** `FB1` — either end |
| **B5** | Junction 5 VOLTS | **ESP32 board** `MCU1` — the pin marked **`VIN`** |
| **B6** | **HLK-PM01** `PS1` — the pin marked **`-Vo`** | **`GROUND`** |
| **B7** | **Electrolytic capacitor** `C2` — the **− (negative)** leg, the striped side | **`GROUND`** |
| **B8** | **Ceramic capacitor** `C3` — its other end | **`GROUND`** |

> ⚠️ **`C2` is an electrolytic capacitor and it has a direction.** The negative
> leg is the shorter one, and the can has a stripe printed down the negative
> side. Fitted backwards it will burst.

### Clean 5 volts for the measuring chip

The ferrite bead `FB1` splits the 5 V supply into two branches. The measuring
chip gets its own filtered branch so WiFi noise cannot reach it.

| # | From | To |
|---|---|---|
| **B9** | **Ferrite bead** `FB1` — its other end | **Junction "5 VOLTS CLEAN"** |
| **B10** | Junction 5 VOLTS CLEAN | **Ceramic capacitor** `C7` (10 µF) — either end |
| **B11** | Junction 5 VOLTS CLEAN | **Ceramic capacitor** `C8` (100 nF) — either end |
| **B12** | Junction 5 VOLTS CLEAN | **HLW8032** `U2` — the leg marked **`VDD`** |
| **B13** | **Ceramic capacitor** `C7` — its other end | **`ANALOG GROUND`** |
| **B14** | **Ceramic capacitor** `C8` — its other end | **`ANALOG GROUND`** |

> ⚠️ **Nothing else may connect to "5 VOLTS CLEAN"** — only those four things. If
> you hang anything else off it, the filter stops working.

### The 3.3 volt supply

The ESP32 board makes its own 3.3 V internally and shares it on a pin. We use it
only to keep the analog filtering stable.

| # | From | To |
|---|---|---|
| **B15** | **ESP32 board** `MCU1` — the pin marked **`3V3`** | **Junction "3.3 VOLTS"** |
| **B16** | Junction 3.3 VOLTS | **Ceramic capacitor** `C5` (10 µF) — either end |
| **B17** | Junction 3.3 VOLTS | **Ceramic capacitor** `C6` (100 nF) — either end |
| **B18** | **Ceramic capacitor** `C5` — its other end | **`GROUND`** |
| **B19** | **Ceramic capacitor** `C6` — its other end | **`GROUND`** |

---

# SECTION C — Measuring the mains voltage ⚠️ HALF DANGEROUS

Four resistors reduce the mains to a tiny current. That current goes through the
small transformer `T1`, which passes the signal across the safety barrier with
**no electrical connection at all**.

```
 LIVE-FUSED ──[Rv1]──[Rv2]──[Rv3]──[Rv4]──► T1 primary
                                            T1 primary ──► NEUTRAL

      ═══════════════ SAFETY BARRIER ═══════════════

 T1 secondary ──┬──────┬───────[Rf1]───┬──► U2 "V1P"
                │      │               │
              Rv5     D3             Cf1
                │      │               │
 T1 secondary ──┴──────┴───────────────┴──► ANALOG GROUND
```

| # | From | To |
|---|---|---|
| **C1** | **Resistor** `Rv1` — its other end | **Resistor** `Rv2` — either end |
| **C2** | **Resistor** `Rv2` — its other end | **Resistor** `Rv3` — either end |
| **C3** | **Resistor** `Rv3` — its other end | **Resistor** `Rv4` — either end |
| **C4** | **Resistor** `Rv4` — its other end | **ZMPT101B** `T1` — the other leg of the **primary** pair |
| **C5** | **ZMPT101B** `T1` — one leg of the **secondary** pair | **Junction "VOLTAGE SIGNAL"** |
| **C6** | Junction VOLTAGE SIGNAL | **Precision resistor** `Rv5` (150 Ω) — either end |
| **C7** | Junction VOLTAGE SIGNAL | **TVS diode** `D3` — either end |
| **C8** | Junction VOLTAGE SIGNAL | **Resistor** `Rf1` (1 kΩ) — either end |
| **C9** | **ZMPT101B** `T1` — the other leg of the **secondary** pair | **`ANALOG GROUND`** |
| **C10** | **Precision resistor** `Rv5` — its other end | **`ANALOG GROUND`** |
| **C11** | **TVS diode** `D3` — its other end | **`ANALOG GROUND`** |
| **C12** | **Resistor** `Rf1` — its other end | **Junction "VOLTAGE FILTERED"** |
| **C13** | Junction VOLTAGE FILTERED | **Ceramic capacitor** `Cf1` (33 nF) — either end |
| **C14** | Junction VOLTAGE FILTERED | **HLW8032** `U2` — the leg marked **`V1P`** *(voltage input)* |
| **C15** | **Ceramic capacitor** `Cf1` — its other end | **`ANALOG GROUND`** |

### Why four resistors and not one

All three reasons are safety:

1. A single resistor across 230 V is at its voltage limit and will arc over
   during a surge. Four share the stress — about 58 V each.
2. If one fails, it fails open and the chain safely disconnects.
3. The heat spreads across four parts instead of one hot spot next to mains
   tracks.

**Never substitute one resistor for the four.**

> ⚠️ **Buy the bare ZMPT101B transformer** — a small black rectangular part with
> four pins. Do **not** buy the popular blue circuit board with an op-amp and a
> blue potentiometer on it. That one is built for hobby projects and drifts over
> time.

> ⚠️ **The ZMPT101B's four pins look identical.** Two are the primary (input),
> two are the secondary (output). Identify them from the datasheet or by
> measuring resistance with a multimeter before you commit the PCB layout.

---

# SECTION D — Measuring the current

The clamp produces a tiny current in proportion to the house current. The
precision resistor `Rb` turns that into a voltage the chip can read.

```
  J2 screw 1 ──┬──────┬──────[Rf2]───┬──────┬──► U2 "I1P"
               │      │              │      │
              Rb     D2            Cf2    Cf3
               │      │              │      │
  J2 screw 2 ──┴──────┴──[Rf3]───────┴──────┼──► U2 "I1N"
        │                  ▲               Cf4
        └─ ANALOG GROUND ──┘                │
                                     ANALOG GROUND
```

The clamp `CT1` is **not soldered to the board** — its two wires screw into `J2`.
It has no polarity for wiring purposes, but if the power reads negative once
installed, the clamp is facing the wrong way around the cable.

| # | From | To |
|---|---|---|
| **D1** | **Clamp terminal** `J2` — first screw *(clamp wire 1)* | **Junction "CLAMP SIGNAL"** |
| **D2** | Junction CLAMP SIGNAL | **Precision resistor** `Rb` (0.68 Ω) — either end |
| **D3** | Junction CLAMP SIGNAL | **TVS diode** `D2` — either end |
| **D4** | Junction CLAMP SIGNAL | **Resistor** `Rf2` (1.5 kΩ) — either end |
| **D5** | **Clamp terminal** `J2` — second screw *(clamp wire 2)* | **`ANALOG GROUND`** |
| **D6** | **Precision resistor** `Rb` — its other end | **`ANALOG GROUND`** |
| **D7** | **TVS diode** `D2` — its other end | **`ANALOG GROUND`** |
| **D8** | **Resistor** `Rf2` — its other end | **Junction "CURRENT +"** |
| **D9** | Junction CURRENT + | **Ceramic capacitor** `Cf2` (33 nF) — either end |
| **D10** | Junction CURRENT + | **Ceramic capacitor** `Cf3` (10 nF) — either end |
| **D11** | Junction CURRENT + | **HLW8032** `U2` — the leg marked **`I1P`** *(current positive)* |
| **D12** | **`ANALOG GROUND`** | **Resistor** `Rf3` (1.5 kΩ) — either end |
| **D13** | **Resistor** `Rf3` — its other end | **Junction "CURRENT −"** |
| **D14** | Junction CURRENT − | **Ceramic capacitor** `Cf2` — its other end |
| **D15** | Junction CURRENT − | **Ceramic capacitor** `Cf4` (10 nF) — either end |
| **D16** | Junction CURRENT − | **HLW8032** `U2` — the leg marked **`I1N`** *(current negative)* |
| **D17** | **Ceramic capacitor** `Cf3` — its other end | **`ANALOG GROUND`** |
| **D18** | **Ceramic capacitor** `Cf4` — its other end | **`ANALOG GROUND`** |

### Things that matter here

**`Rf3` looks pointless but is essential.** It runs from ground into the chip's
negative input, and it must be **exactly the same value as `Rf2`**. The chip
compares its two inputs against each other. If the two paths have different
resistance, noise picked up by the clamp cable no longer cancels out.

**`Rf2` and `Rf3` also correct the clamp's timing error.** A clamp shifts the
current signal very slightly in time, which makes power readings wrong on motor
loads. Making these two larger than `Rf1` compensates for it. Start at 1.5 kΩ and
fine-tune during calibration — **always change both together.**

**`Rb` is the most accuracy-critical part on the board.** Every amp you ever
measure is defined by this one resistor's value:
- 1 % tolerance or better
- 50 ppm/°C or better temperature stability
- **Never wirewound** — its inductance adds timing error
- Starting value 0.68 Ω, but **must be confirmed on prototypes**

### ⚠️ Clamp safety rule for the installation manual

A current clamp left open-circuit on a live cable develops dangerous voltage.
`Rb` is permanently soldered to the board, so while the clamp is plugged in it is
always safe. But:

> **Always open and remove the clamp from the cable BEFORE disconnecting its
> wires from the device.**

---

# SECTION E — The measuring chip to the ESP32

The measuring chip runs on 5 V and sends its data on a single wire. The ESP32
only tolerates 3.3 V on its inputs, so two resistors divide the signal down.

```
  U2 "TX" ──[Rls1 1k]──┬──► MCU1 "D16"
                       │
                   [Rls2 2k]
                       │
                     GROUND
```

| # | From | To |
|---|---|---|
| **E1** | **HLW8032** `U2` — the leg marked **`TX`** *(data out)* | **Resistor** `Rls1` (1 kΩ) — either end |
| **E2** | **Resistor** `Rls1` — its other end | **Junction "DATA 3.3 V"** |
| **E3** | Junction DATA 3.3 V | **Resistor** `Rls2` (2 kΩ) — either end |
| **E4** | Junction DATA 3.3 V | **ESP32 board** `MCU1` — the pin marked **`D16`** |
| **E5** | **Resistor** `Rls2` — its other end | **`GROUND`** |
| **E6** | **HLW8032** `U2` — the leg marked **`GND`** | **`ANALOG GROUND`** |
| **E7** | **0 Ω link** `R7` — either end | **`GROUND`** |
| **E8** | **0 Ω link** `R7` — its other end | **`ANALOG GROUND`** |

The maths: 5 V × 2k ÷ (1k + 2k) = **3.33 V** — exactly what the ESP32 wants.

> ⚠️ **Never connect `U2` `TX` straight to the ESP32.** ESP32 pins are not 5 V
> tolerant. It may appear to work for a while and then fail — which is worse than
> failing immediately.

> ⚠️ **Use `D16`, not `RX0`.** `RX0` is the pin the USB programming uses. If the
> measuring chip is sending data into it you will not be able to upload code or
> read debug messages.

> ⚠️ **`U2` `GND` goes to ANALOG GROUND**, not to `GROUND`. This is the whole
> point of Section 4.

The chip's `PF` leg *(energy pulse output)* is **not connected** — the data we
need already comes over `TX`.

---

# SECTION F — The ESP32 board

The board plugs into two 15-hole female header strips, `J4` and `J5`. Orient it
so that:
- the **antenna end hangs over the edge** of your board, and
- the **USB-C socket faces the enclosure wall**, so a cable can be plugged in.

```
  antenna →│████ ESP32 board ████│← USB-C faces the wall
           └─╥─────────────────╥─┘
        J4 ──╨─────────────────╨── J5
      ┌─────────────────────────────────┐
      │        your PCB                 │
      └─────────────────────────────────┘
```

Only **9 of the 30 pins** are used. The rest are simply not connected.

| # | ESP32 pin *(as printed on the board)* | Connect to | Why |
|---|---|---|---|
| **F1** | **`VIN`** | Junction 5 VOLTS | Power in from the HLK-PM01 |
| **F2** | **`GND`** *(either one)* | `GROUND` | Return path |
| **F3** | **`GND`** *(the other one)* | `GROUND` | Second ground, for stability |
| **F4** | **`3V3`** | Junction 3.3 VOLTS | Feeds the analog filtering |
| **F5** | **`D16`** | Junction DATA 3.3 V | Reads the measuring chip |
| **F6** | **`D21`** | Junction CLOCK DATA | Talks to the clock chip |
| **F7** | **`D22`** | Junction CLOCK SIGNAL | Talks to the clock chip |
| **F8** | **`D25`** | **Resistor** `R3` — either end | Drives the green light |
| **F9** | **`D26`** | **Resistor** `R4` — either end | Drives the blue light |

**Leave completely unconnected:** `D2`, `D4`, `D5`, `D12`, `D13`, `D14`, `D15`,
`D17`, `D18`, `D19`, `D23`, `D27`, `D32`, `D33`, `D34`, `D35`, `VP`, `VN`, `EN`,
`RX0`, `TX0`.

### What we get for free from this board

| Already on the ESP32 board | So we do not need |
|---|---|
| USB-C socket + USB-to-serial chip | A programming header and a programming jig |
| Auto-reset circuit | Two transistors and two resistors |
| 3.3 V regulator | A regulator, a protection diode and its capacitors |
| BOOT button | A separate factory-reset button |
| RESET button | — |

**Use the board's own BOOT button as the factory-reset button** — the firmware
can read it. Drill a small hole in the enclosure above it.

---

# SECTION G — The indicator lights

```
  MCU1 "D25" ──[R3 1k]──►|── GROUND     (LED1, green)
  MCU1 "D26" ──[R4 1k]──►|── GROUND     (LED2, blue)
                          ▲
                 the arrow points from + to −
```

| # | From | To |
|---|---|---|
| **G1** | **ESP32 board** `MCU1` — pin **`D25`** | **Resistor** `R3` (1 kΩ) — either end |
| **G2** | **Resistor** `R3` — its other end | **Green LED** `LED1` — the **anode (+)** |
| **G3** | **Green LED** `LED1` — the **cathode (−)** | **`GROUND`** |
| **G4** | **ESP32 board** `MCU1` — pin **`D26`** | **Resistor** `R4` (1 kΩ) — either end |
| **G5** | **Resistor** `R4` — its other end | **Blue LED** `LED2` — the **anode (+)** |
| **G6** | **Blue LED** `LED2` — the **cathode (−)** | **`GROUND`** |

> ⚠️ **LEDs only work one way round.** On small surface-mount LEDs the cathode is
> usually marked with a green line, a dot or a notch — but **the marking is not
> standard between manufacturers.** Test one with a coin cell and a 1 kΩ resistor
> before you solder a hundred of them.

---

# SECTION H — The clock chip

`U4` is a **DS1307Z+**. Its only job is to keep the time running while the device
is switched off, so that readings stored during an internet outage still get
correct timestamps.

```
   5 VOLTS ──┬──────────── U4 "VCC"          Y1 (crystal)
             │                                ┌───────┐
            C13                    U4 "X1" ───┤ 32.768│
             │                     U4 "X2" ───┤  kHz  │
   GROUND ───┴──────────── U4 "GND"           └───────┘

   3.3 VOLTS ──[R5 4.7k]──┬── U4 "SDA" ── MCU1 "D21"
   3.3 VOLTS ──[R6 4.7k]──┴── U4 "SCL" ── MCU1 "D22"

   U4 "VBAT" ──────────── BT1 "+"   (battery)
                          BT1 "−" ── GROUND
```

| # | From | To |
|---|---|---|
| **H1** | **DS1307** `U4` — the leg marked **`VCC`** | **Junction "5 VOLTS"** |
| **H2** | **DS1307** `U4` — the leg marked **`GND`** | **`GROUND`** |
| **H3** | **DS1307** `U4` — the leg marked **`X1`** | **Crystal** `Y1` — either leg |
| **H4** | **DS1307** `U4` — the leg marked **`X2`** | **Crystal** `Y1` — its other leg |
| **H5** | **DS1307** `U4` — the leg marked **`VBAT`** | **Battery holder** `BT1` — the **+ (positive)** terminal |
| **H6** | **Battery holder** `BT1` — the **− (negative)** terminal | **`GROUND`** |
| **H7** | **DS1307** `U4` — the leg marked **`SDA`** | **Junction "CLOCK DATA"** |
| **H8** | Junction CLOCK DATA | **Resistor** `R5` (4.7 kΩ) — either end |
| **H9** | Junction CLOCK DATA | **ESP32 board** `MCU1` — the pin marked **`D21`** |
| **H10** | **DS1307** `U4` — the leg marked **`SCL`** | **Junction "CLOCK SIGNAL"** |
| **H11** | Junction CLOCK SIGNAL | **Resistor** `R6` (4.7 kΩ) — either end |
| **H12** | Junction CLOCK SIGNAL | **ESP32 board** `MCU1` — the pin marked **`D22`** |
| **H13** | **Resistor** `R5` — its other end | **Junction "3.3 VOLTS"** |
| **H14** | **Resistor** `R6` — its other end | **Junction "3.3 VOLTS"** |
| **H15** | **Ceramic capacitor** `C13` (100 nF) — either end | **Junction "5 VOLTS"** |
| **H16** | **Ceramic capacitor** `C13` — its other end | **`GROUND`** |

The chip's `SQW/OUT` leg is **not connected** — we don't use it.

## ⚠️ Four rules for this section

### 1. The chip runs on 5 V, but the pull-ups go to 3.3 V

This is the single most important thing on this page.

The DS1307 needs **4.5–5.5 V** to work, so `VCC` goes to the 5 V rail. But
**ESP32 pins are not 5 V tolerant.**

The trick is that the DS1307's data lines are **open-drain** — they can only pull
a line *down*, never push it up. So whatever voltage you pull the lines up to is
the highest voltage the bus ever reaches. Pull them up to **3.3 V** and the bus
never exceeds 3.3 V, no matter that the chip runs on 5 V.

And in the other direction: the DS1307 treats anything above **2.2 V** as a logic
high, so the ESP32's 3.3 V signals drive it comfortably.

> **`R5` and `R6` must go to the 3.3 VOLTS junction. Never to 5 VOLTS.** Getting
> this wrong puts 5 V onto the ESP32's pins. It may appear to work for a while
> and then fail — which is worse than failing immediately. This is exactly what
> destroys ESP32s on cheap DS1307 modules, where the pull-ups go to whatever
> powers the module.

### 2. The battery connects directly — nothing else on that wire

`VBAT` connects to the battery holder's positive terminal and **to nothing
else.** No diode. No resistor. No charging circuit.

The DS1307 switches to the battery internally, all by itself, when mains goes
away. That is what the `VBAT` leg is for.

> **This is why we use the bare chip and not a module.** The "Tiny RTC" DS1307
> module puts a resistor divider on this pin (because it ships with a 3.6 V
> rechargeable cell) — the DS1307 datasheet is explicit that the battery must
> connect with **0 Ω** in series. And the DS3231 "blue module" has a trickle
> charger that will cook a non-rechargeable CR2032. Both are broken by design
> for our purposes.

**A CR2032 here lasts 8–10 years** — the chip draws 0.84 µA in timekeeping mode,
and in this device the battery is only used while mains is off.

### 3. The crystal must be 12.5 pF, and needs no capacitors

The DS1307's load capacitors are **inside the chip**. You connect the crystal
straight to `X1` and `X2` and **add nothing else** — no capacitors, no resistors.

But the crystal must be the matching type: **32.768 kHz with 12.5 pF load
capacitance.** A 6 pF crystal (which the DS1302 uses) would make the clock run
minutes per day slow.

### 4. Layout: keep the crystal close and quiet

Place `Y1` **within 5 mm** of the `X1`/`X2` legs, with a ground pour around it,
and route nothing underneath on either layer. A 32.768 kHz oscillator is a
low-energy circuit and it picks up noise easily.

## Why we bothered

The ESP32 counts seconds since it powered on, so if it never loses power it can
work out the time of every stored reading once the internet returns. But when
mains cuts, that counter resets and it has no way to know how long it was off.

The DS1307 is a little watch with its own battery that **keeps ticking while
everything else is dead.** On boot, the ESP32 asks it what time it is and gets
the right answer straight away — internet or not.

Accuracy comes entirely from the crystal, roughly **±3 seconds per day**, and the
ESP32 resets it from the internet whenever it can. That is far more than enough:
its job is to bridge days, not years.

---

# 5. Complete connection list — quick reference

Every junction in the design, and everything attached to it.

| Junction | Everything connected to it |
|---|---|
| **LIVE (raw)** ⚠️ | `J1` LIVE screw, `FH1` first fuse clip |
| **LIVE-FUSED** ⚠️ | `FH1` second fuse clip, `RV1`, `C1`, `PS1` `AC-L`, `Rv1` |
| **NEUTRAL** ⚠️ | `J1` NEUTRAL screw, `RV1`, `C1`, `PS1` `AC-N`, `T1` primary |
| **DIVIDER A** ⚠️ | `Rv1`, `Rv2` |
| **DIVIDER B** ⚠️ | `Rv2`, `Rv3` |
| **DIVIDER C** ⚠️ | `Rv3`, `Rv4` |
| **DIVIDER D** ⚠️ | `Rv4`, `T1` primary |
| **5 VOLTS** | `PS1` `+Vo`, `C2` **+**, `C3`, `FB1`, `MCU1` `VIN`, `U4` `VCC`, `C13` |
| **5 VOLTS CLEAN** | `FB1`, `C7`, `C8`, `U2` `VDD` |
| **3.3 VOLTS** | `MCU1` `3V3`, `C5`, `C6`, `R5`, `R6` |
| **GROUND** | `PS1` `-Vo`, `C2` **−**, `C3`, `C5`, `C6`, `MCU1` `GND` ×2, `LED1` −, `LED2` −, `Rls2`, `R7`, `U4` `GND`, `C13`, `BT1` **−** |
| **ANALOG GROUND** | `U2` `GND`, `C7`, `C8`, `T1` secondary, `Rv5`, `D3`, `Cf1`, `J2` second screw, `Rb`, `D2`, `Rf3`, `Cf3`, `Cf4`, `R7` |
| **VOLTAGE SIGNAL** | `T1` secondary, `Rv5`, `D3`, `Rf1` |
| **VOLTAGE FILTERED** | `Rf1`, `Cf1`, `U2` `V1P` |
| **CLAMP SIGNAL** | `J2` first screw, `Rb`, `D2`, `Rf2` |
| **CURRENT +** | `Rf2`, `Cf2`, `Cf3`, `U2` `I1P` |
| **CURRENT −** | `Rf3`, `Cf2`, `Cf4`, `U2` `I1N` |
| **DATA 5 V** | `U2` `TX`, `Rls1` |
| **DATA 3.3 V** | `Rls1`, `Rls2`, `MCU1` `D16` |
| **CLOCK DATA** | `U4` `SDA`, `R5`, `MCU1` `D21` |
| **CLOCK SIGNAL** | `U4` `SCL`, `R6`, `MCU1` `D22` |
| **BATTERY** | `U4` `VBAT`, `BT1` **+** |
| **CRYSTAL A** | `U4` `X1`, `Y1` one leg |
| **CRYSTAL B** | `U4` `X2`, `Y1` other leg |
| **GREEN LIGHT** | `MCU1` `D25` → `R3` → `LED1` **+** |
| **BLUE LIGHT** | `MCU1` `D26` → `R4` → `LED2` **+** |

**26 junctions. That is the entire circuit.**

---

# 6. Check this before you power anything on

## With a multimeter, power completely off

- [ ] Between `GROUND` and 5 VOLTS — **not** a short circuit
- [ ] Between `GROUND` and 3.3 VOLTS — **not** a short circuit
- [ ] `GROUND` and `ANALOG GROUND` connect **only** through `R7` — lift one end
      of `R7` and confirm they become separate
- [ ] Between the mains terminal `J1` (both screws shorted together) and
      `GROUND` — **completely open, above 20 MΩ.** This is the most important
      test on the board. **If it fails, do not power it up. Ever.**
- [ ] The four resistors `Rv1`–`Rv4` measure about **188 kΩ** end to end

## By eye

- [ ] `C2` electrolytic is the right way round (stripe = negative)
- [ ] `LED1` and `LED2` are the right way round
- [ ] `D2` and `D3` are fitted (no direction, but they must be there)
- [ ] `U2` and `U4` leg 1 match the markings on the board
- [ ] `BT1` battery holder is the right way round (+ cup, − tab)
- [ ] **`R5` and `R6` go to 3.3 VOLTS, not to 5 VOLTS** — trace them with a meter
- [ ] **Nothing but `BT1` **+** touches `U4` `VBAT`** — no diode, no resistor
- [ ] No solder bridges anywhere, especially on `U2` and `U4`
- [ ] **The safety slot across the board is clean** — no solder, no flux, no bent
      component lead crossing it
- [ ] Nothing on the mains side comes within 8 mm of the safe side

## First power-up

- [ ] Use an isolation transformer and an RCD
- [ ] `PS1` `+Vo` measures **4.9 – 5.2 V**
- [ ] `MCU1` `3V3` measures **3.25 – 3.35 V**
- [ ] The green light comes on
- [ ] The device appears on USB when you plug a cable in
- [ ] The clock chip answers, and reports a sensible time after you set it

---

# 7. Three values to confirm on the first prototypes

These are starting points, not final answers. Build five boards, test, then lock
them in before ordering 1,000.

| Part | Start with | What it controls | How to confirm |
|---|---|---|---|
| `Rb` | **0.68 Ω** | The current range | Feed a known current; check the reading is correct and does not flatten off at high load |
| `Rv5` | **150 Ω** | The voltage range | Vary mains from 180 V to 270 V; the reading must stay proportional |
| `Rf2` `Rf3` | **1.5 kΩ** | The clamp's timing correction | With a pure heater load, adjust until power factor reads 1.000 |

Buy a range of values for these three (listed in the shopping list) so you can
try them without re-ordering. About half a day of work, and it protects the
entire production run.
