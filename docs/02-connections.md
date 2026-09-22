# The Complete Wiring Guide

**Every single connection in this device, explained so anyone can follow it.**

You do not need to be an electronics engineer to use this document. Work through
it section by section, connect what each line says, and the circuit will be
complete and correct.

---

# ⚠️ READ THIS BEFORE ANYTHING ELSE

This device connects directly to **230 V mains electricity, which can kill you.**

- **Never** work on the board while it is connected to mains.
- **Never** touch the mains section while power is on.
- Always test with the power off first.
- When you must power it up, use an **isolation transformer** and an **RCD /
  earth-leakage breaker** on your bench.
- The parts in **Section A, B and C** are dangerous. Treat them as live at all
  times, even when you think the power is off.

There is a **safety barrier** running across the middle of this board. On one
side, everything is at mains voltage. On the other side, everything is safe to
touch. **Nothing may cross that barrier** except the two components designed to
cross it: the power supply module and the voltage transformer.

---

# 1. What this circuit does

A clamp goes around the main electricity cable of the house. The clamp never
touches the wire inside — it measures the magnetic field around it. That is how
we measure current without cutting anything.

Separately, we tap the live and neutral wires to do two jobs:
1. Power the device.
2. Measure the actual mains voltage.

The measuring chip combines current and voltage to calculate real power in
watts. The ESP32 board reads that number, stamps it with the time, saves it, and
sends it over WiFi.

```
   House main cable  ══════╪══════
                        ╭──┴──╮
                        │clamp│════╗
                        ╰─────╯    ║
                                   ▼
  Live  ──┬──[fuse]──────────────► MEASURING ──► ESP32 ──► WiFi
          │                        CHIP           BOARD
  Neutral ┴──────────────────────►
```

---

# 2. The parts and what each one does

Every part has a **label** (like `R5` or `C2`). These labels appear on the
circuit board silkscreen, in the parts list, and throughout this document.

## Mains side — DANGEROUS

| Label | Part | Job |
|---|---|---|
| `J1` | Screw terminal, 2 holes, wide | Where the live and neutral wires come in |
| `F1` | Fuse, 250 mA slow-blow | Cuts the power if something fails. Fire protection |
| `FH1` | Two fuse clips | Hold the fuse |
| `RV1` | Blue disc (MOV) | Absorbs lightning and switching spikes |
| `C1` | Yellow/blue box capacitor (X2) | Filters electrical noise |
| `PS1` | HLK-PM01 module | Converts 230 V to safe 5 V. **This is part of the safety barrier** |
| `Rv1` `Rv2` `Rv3` `Rv4` | Four 47k resistors | Reduce the mains voltage to a tiny safe current |
| `T1` | ZMPT101B transformer | Passes the voltage signal across the safety barrier |

## Safe side

| Label | Part | Job |
|---|---|---|
| `C2` | Big capacitor, 470 µF | Stores energy for WiFi transmission bursts |
| `C3` | 100 nF | Cleans up the 5 V supply |
| `U2` | HLW8032 chip (8 legs) | **The measuring chip.** Calculates volts, amps, watts |
| `FB1` | Ferrite bead | Blocks WiFi noise from reaching the measuring chip |
| `C7` `C8` | 10 µF and 100 nF | Clean power for the measuring chip |
| `J2` | Screw terminal, 2 holes, narrow | Where the clamp plugs in |
| `Rb` | 0.68 Ω precision resistor | Converts the clamp's current into a voltage |
| `D2` `D3` | TVS diodes | Protect against voltage spikes |
| `Rf2` `Rf3` | Two 1.5k resistors | Filter + correct the clamp's timing error |
| `Cf2` `Cf3` `Cf4` | 33 nF and two 10 nF | Filter the current signal |
| `Rv5` | 150 Ω precision resistor | Sets the voltage measuring range |
| `Rf1` `Cf1` | 1k and 33 nF | Filter the voltage signal |
| `Rls1` `Rls2` | 1k and 2k | Step the chip's 5 V signal down to 3.3 V |
| `R7` | 0 Ω link | Joins the two ground areas at one point |
| `MCU1` | ESP32 board | The brain. WiFi, storage, cloud |
| `J4` `J5` | Two 15-hole female headers | The ESP32 board plugs into these |
| `C5` `C6` | 10 µF and 100 nF | Clean the 3.3 V supply |
| `U4` | DS3231 chip (16 legs) | Keeps the time during power cuts |
| `BT1` `B1` | Battery holder + CR2032 | Powers the clock when mains is off |
| `R5` `R6` | Two 4.7k resistors | Needed for the clock's communication |
| `C13` | 100 nF | Clean power for the clock |
| `LED1` `LED2` | Green and blue lights | Show power and WiFi status |
| `R3` `R4` | Two 1k resistors | Limit the current through the lights |

---

# 3. How to read the connection lists

Each connection is written like this:

> **Connect `A` pin 1 → `B` pin 2**

Meaning: run a wire (or a copper track on the PCB) from pin 1 of part A to pin 2
of part B.

When several things connect to the same place, they form a **junction** — like
several wires twisted together. All the parts listed at one junction are
electrically the same point.

**Resistors and capacitors have no direction.** Pin 1 and pin 2 are
interchangeable. **Diodes, LEDs, electrolytic capacitors, chips and modules DO
have a direction** — those are marked clearly below.

---

# 4. The two ground zones — read this, it matters

Ground is the "return path" that all electricity flows back through. This board
has **two separate ground zones** that meet at exactly one point.

| Zone | Name | What connects to it |
|---|---|---|
| **Noisy** | `GROUND` | ESP32 board, clock chip, LEDs, power supply |
| **Quiet** | `ANALOG GROUND` | Measuring chip, the clamp, all filter parts |

**Why:** the ESP32 gulps half an amp in short bursts when it transmits WiFi. The
measuring chip is reading signals of a few thousandths of a volt. If they share
the same ground path, the WiFi bursts show up as noise in your measurements.

**The rule:** keep them separate everywhere, and join them at **one single
point** — through `R7`, placed right next to the measuring chip `U2`.

```
   ┌─────────────────┐          ┌──────────────────┐
   │     GROUND      │──[R7]────│  ANALOG GROUND   │
   │ (ESP32, clock,  │  0 ohm   │ (measuring chip, │
   │  LEDs, supply)  │  ONE     │  clamp, filters) │
   └─────────────────┘  POINT   └──────────────────┘
```

Throughout this document, **`GROUND`** and **`ANALOG GROUND`** are written in
full so you never confuse them.

---

# SECTION A — Mains input ⚠️ DANGEROUS

```
              F1 (fuse)
  J1 pin 1 ────▭▭▭────┬──────────┬──────────┬────── PS1 "AC" pin 1
   (LIVE)             │          │          │
                     RV1        C1       Rv1 pin 1
                      │          │          (to Section C)
  J1 pin 2 ───────────┴──────────┴─────────────────  PS1 "AC" pin 2
   (NEUTRAL)                     │
                                 └────────────────── T1 primary pin 2
```

| # | Connect | To |
|---|---|---|
| A1 | `J1` pin 1 *(live in)* | `F1` pin 1 |
| A2 | `F1` pin 2 | **Junction "LIVE-FUSED"** |
| A3 | Junction LIVE-FUSED | `RV1` pin 1 |
| A4 | Junction LIVE-FUSED | `C1` pin 1 |
| A5 | Junction LIVE-FUSED | `PS1` AC input pin 1 |
| A6 | Junction LIVE-FUSED | `Rv1` pin 1 *(Section C)* |
| A7 | `J1` pin 2 *(neutral in)* | **Junction "NEUTRAL"** |
| A8 | Junction NEUTRAL | `RV1` pin 2 |
| A9 | Junction NEUTRAL | `C1` pin 2 |
| A10 | Junction NEUTRAL | `PS1` AC input pin 2 |
| A11 | Junction NEUTRAL | `T1` primary pin 2 *(Section C)* |

### ⚠️ Critical rules for this section

1. **`RV1` and `C1` must be AFTER the fuse, never before it.** A surge protector
   fails as a short circuit at the end of its life. After the fuse, that just
   blows the fuse. Before the fuse, it is a direct short across the mains — a
   fire.
2. **`F1` must be 250 VAC rated and slow-blow.** A 63 V SMD fuse will not
   interrupt a mains fault and will explode.
3. **`C1` must be class X2.** X2 capacitors are designed to fail open-circuit. A
   normal ceramic capacitor in this position is a fire hazard.
4. Nothing in this section may come within **8 mm** of anything on the safe side.

---

# SECTION B — Power supply

`PS1` (HLK-PM01) takes 230 V in and gives 5 V out. It contains a transformer
inside, which is what makes everything after it safe to touch.

```
  PS1 "+" ──┬──────┬────────┬──────────────► MCU1 "VIN"
            │      │        │
           C2 +   C3     FB1 pin 1
            │      │        │
            │      │        └──► FB1 pin 2 ──┬────┬──► U2 supply pin
            │      │                         │    │
  PS1 "−" ──┴──────┴─────────────────────── GROUND  C7  C8 ──► ANALOG GROUND
```

| # | Connect | To |
|---|---|---|
| B1 | `PS1` output **+** *(5 V)* | **Junction "5 VOLTS"** |
| B2 | Junction 5 VOLTS | `C2` **positive** leg |
| B3 | Junction 5 VOLTS | `C3` pin 1 |
| B4 | Junction 5 VOLTS | `FB1` pin 1 |
| B5 | Junction 5 VOLTS | `MCU1` pin marked **`VIN`** |
| B6 | `PS1` output **−** | **`GROUND`** |
| B7 | `C2` **negative** leg | `GROUND` |
| B8 | `C3` pin 2 | `GROUND` |

### Clean 5 volts for the measuring chip

`FB1` splits the 5 V supply into two. The measuring chip gets its own filtered
branch so WiFi noise cannot reach it.

| # | Connect | To |
|---|---|---|
| B9 | `FB1` pin 2 | **Junction "5 VOLTS CLEAN"** |
| B10 | Junction 5 VOLTS CLEAN | `C7` pin 1 |
| B11 | Junction 5 VOLTS CLEAN | `C8` pin 1 |
| B12 | Junction 5 VOLTS CLEAN | `U2` supply pin *(VDD)* |
| B13 | `C7` pin 2 | **`ANALOG GROUND`** |
| B14 | `C8` pin 2 | **`ANALOG GROUND`** |

> ⚠️ **Nothing else may connect to "5 VOLTS CLEAN".** Only those four things. If
> you hang anything else off it, the filter stops working.

### The 3.3 volt supply

The ESP32 board makes its own 3.3 V and shares it on a pin. We use it to power
the clock chip only.

| # | Connect | To |
|---|---|---|
| B15 | `MCU1` pin marked **`3V3`** | **Junction "3.3 VOLTS"** |
| B16 | Junction 3.3 VOLTS | `C5` pin 1 |
| B17 | Junction 3.3 VOLTS | `C6` pin 1 |
| B18 | `C5` pin 2 | `GROUND` |
| B19 | `C6` pin 2 | `GROUND` |

> ⚠️ **`C2` is an electrolytic capacitor — it has a positive and a negative
> leg.** The negative leg is marked with a stripe and is usually the shorter
> lead. Fitting it backwards will make it burst.

---

# SECTION C — Measuring the mains voltage ⚠️ HALF DANGEROUS

Four resistors reduce the mains to a tiny current. That current goes through a
small transformer `T1`, which passes the signal across the safety barrier
without any electrical connection.

```
 LIVE-FUSED ──[Rv1]──[Rv2]──[Rv3]──[Rv4]──► T1 primary pin 1
                                             T1 primary pin 2 ──► NEUTRAL

        ═══════════ SAFETY BARRIER ═══════════

 T1 secondary pin 1 ──┬─────┬──────[Rf1]──┬──► U2 voltage pin
                      │     │             │
                    Rv5    D3           Cf1
                      │     │             │
 T1 secondary pin 2 ──┴─────┴─────────────┴──► ANALOG GROUND
```

| # | Connect | To |
|---|---|---|
| C1 | `Rv1` pin 2 | `Rv2` pin 1 |
| C2 | `Rv2` pin 2 | `Rv3` pin 1 |
| C3 | `Rv3` pin 2 | `Rv4` pin 1 |
| C4 | `Rv4` pin 2 | `T1` primary pin 1 |
| — | *(`Rv1` pin 1 → LIVE-FUSED and `T1` primary pin 2 → NEUTRAL were done in Section A)* | |
| C5 | `T1` secondary pin 1 | **Junction "VOLTAGE SIGNAL"** |
| C6 | Junction VOLTAGE SIGNAL | `Rv5` pin 1 |
| C7 | Junction VOLTAGE SIGNAL | `D3` pin 1 |
| C8 | Junction VOLTAGE SIGNAL | `Rf1` pin 1 |
| C9 | `T1` secondary pin 2 | `ANALOG GROUND` |
| C10 | `Rv5` pin 2 | `ANALOG GROUND` |
| C11 | `D3` pin 2 | `ANALOG GROUND` |
| C12 | `Rf1` pin 2 | **Junction "VOLTAGE FILTERED"** |
| C13 | Junction VOLTAGE FILTERED | `Cf1` pin 1 |
| C14 | Junction VOLTAGE FILTERED | `U2` voltage input pin |
| C15 | `Cf1` pin 2 | `ANALOG GROUND` |

### Why four resistors instead of one

Three reasons, all of them safety:
1. A single resistor across 230 V is operating at its voltage limit and will arc
   over during a surge. Four share the stress — about 58 V each.
2. If one fails, it fails open and the chain safely disconnects.
3. The heat spreads across four parts instead of one hot spot next to mains
   tracks.

**Never substitute one resistor for the four.**

> **Buy the bare `ZMPT101B` transformer** — a small black rectangular part with
> four pins. Do **not** buy the popular blue circuit board with an op-amp and a
> blue potentiometer on it. That version is for hobby projects and will drift
> over time.

---

# SECTION D — Measuring the current

The clamp produces a tiny current proportional to the house current. `Rb` turns
that into a voltage the chip can read.

```
  J2 pin 1 ──┬──────┬──────[Rf2 1.5k]──┬──────┬──► U2 current+ pin
  (clamp)    │      │                  │      │
            Rb     D2                Cf2    Cf3
             │      │                  │      │
  J2 pin 2 ──┴──────┴──[Rf3 1.5k]──────┴──────┼──► U2 current− pin
       │                    ▲                Cf4
       └── ANALOG GROUND ───┘                 │
                                        ANALOG GROUND
```

The clamp itself (`CT1`) is **not soldered to the board** — its two wires screw
into the terminal `J2`. The clamp has no polarity for measurement purposes, but
if the power reads negative once installed, the clamp is facing the wrong way
around the cable.

| # | Connect | To |
|---|---|---|
| D1 | `J2` pin 1 *(`CT1` clamp wire 1)* | **Junction "CLAMP SIGNAL"** |
| D2 | Junction CLAMP SIGNAL | `Rb` pin 1 |
| D3 | Junction CLAMP SIGNAL | `D2` pin 1 |
| D4 | Junction CLAMP SIGNAL | `Rf2` pin 1 |
| D5 | `J2` pin 2 *(clamp wire 2)* | `ANALOG GROUND` |
| D6 | `Rb` pin 2 | `ANALOG GROUND` |
| D7 | `D2` pin 2 | `ANALOG GROUND` |
| D8 | `Rf2` pin 2 | **Junction "CURRENT +"** |
| D9 | Junction CURRENT + | `Cf2` pin 1 |
| D10 | Junction CURRENT + | `Cf3` pin 1 |
| D11 | Junction CURRENT + | `U2` current **+** pin |
| D12 | `ANALOG GROUND` | `Rf3` pin 1 |
| D13 | `Rf3` pin 2 | **Junction "CURRENT −"** |
| D14 | Junction CURRENT − | `Cf2` pin 2 |
| D15 | Junction CURRENT − | `Cf4` pin 1 |
| D16 | Junction CURRENT − | `U2` current **−** pin |
| D17 | `Cf3` pin 2 | `ANALOG GROUND` |
| D18 | `Cf4` pin 2 | `ANALOG GROUND` |

### Things that matter here

**`Rf3` looks pointless but is essential.** It goes from ground to the chip's
negative input, and it must be the *same value* as `Rf2`. The chip compares its
two inputs; if the two paths have different resistance, noise picked up by the
clamp cable no longer cancels out.

**`Rf2` and `Rf3` also correct the clamp's timing error.** A clamp shifts the
current signal slightly in time, which makes power readings wrong on motor
loads. Making these two resistors larger than `Rf1` compensates for that. Start
at 1.5 kΩ and fine-tune during calibration. **Always change both together.**

**`Rb` is the most accuracy-critical part on the board.** Every amp you measure
passes through this one resistor's value.
- 1 % tolerance or better
- 50 ppm/°C or better temperature stability
- **Never wirewound** — its inductance adds timing error
- The starting value is 0.68 Ω but **must be confirmed on prototypes**

### ⚠️ Clamp safety rule for the installation manual

A current clamp left open-circuit on a live cable develops dangerous voltage.
`Rb` is permanently soldered to the board, so while the clamp is plugged in it is
always safe. But:

> **Always open and remove the clamp from the cable BEFORE disconnecting its
> wires from the device.**

---

# SECTION E — The measuring chip to the ESP32

The measuring chip runs on 5 V and sends data on one wire. The ESP32 only
tolerates 3.3 V on its inputs, so two resistors divide the signal down.

```
  U2 "TX" ──[Rls1 1k]──┬──► MCU1 pin "D16"
                       │
                   [Rls2 2k]
                       │
                     GROUND
```

| # | Connect | To |
|---|---|---|
| E1 | `U2` TX pin *(data out)* | `Rls1` pin 1 |
| E2 | `Rls1` pin 2 | **Junction "DATA 3.3 V"** |
| E3 | Junction DATA 3.3 V | `Rls2` pin 1 |
| E4 | Junction DATA 3.3 V | `MCU1` pin marked **`D16`** |
| E5 | `Rls2` pin 2 | `GROUND` |
| E6 | `U2` ground pin | **`ANALOG GROUND`** |
| E7 | `R7` pin 1 | `GROUND` |
| E8 | `R7` pin 2 | `ANALOG GROUND` |

The maths: 5 V × 2k ÷ (1k + 2k) = **3.33 V** — exactly what the ESP32 wants.

> ⚠️ **Do not connect `U2` TX straight to the ESP32.** ESP32 pins are not 5 V
> tolerant. It may appear to work for a while and then fail — which is worse
> than failing immediately.

> ⚠️ **Use `D16`, not `RX0`.** `RX0` is the pin the USB programming uses. If the
> measuring chip is sending data into it, you will not be able to upload code or
> read debug messages.

> ⚠️ **`U2` ground goes to ANALOG GROUND**, not to GROUND. This is the whole
> point of Section 4.

---

# SECTION F — The ESP32 board

The board plugs into two 15-hole female headers, `J4` and `J5`. Orient it so
that:
- the **antenna end hangs over the edge** of your board, and
- the **USB socket faces the enclosure wall**, so a cable can be plugged in.

```
  antenna →│████ ESP32 board ████│ ← USB faces the wall
           └─╥─────────────────╥─┘
        J4 ──╨─────────────────╨── J5
      ┌─────────────────────────────────┐
      │        your PCB                 │
      └─────────────────────────────────┘
```

Only **8 of the 30 pins** are used. The rest are simply not connected.

| # | ESP32 pin | Connect to | Purpose |
|---|---|---|---|
| F1 | `VIN` | Junction 5 VOLTS | Power in from `PS1` |
| F2 | `GND` *(either one)* | `GROUND` | Return path |
| F3 | `GND` *(the other one)* | `GROUND` | Second ground for stability |
| F4 | `3V3` | Junction 3.3 VOLTS | Powers the clock chip |
| F5 | `D16` | Junction DATA 3.3 V | Reads the measuring chip |
| F6 | `D21` | Junction CLOCK DATA | Talks to the clock chip |
| F7 | `D22` | Junction CLOCK SIGNAL | Talks to the clock chip |
| F8 | `D25` | `R3` pin 1 | Drives the green light |
| F9 | `D26` | `R4` pin 1 | Drives the blue light |

**Leave completely unconnected:** `D2`, `D4`, `D5`, `D12`, `D13`, `D14`, `D15`,
`D17`, `D18`, `D19`, `D23`, `D27`, `D32`, `D33`, `D34`, `D35`, `VP`, `VN`, `EN`,
`RX0`, `TX0`.

### What we get for free from this board

The ESP32 board already contains parts we would otherwise have to fit:

| Already on the board | So we do not need |
|---|---|
| USB socket + USB-to-serial chip | A programming header and a programming jig |
| Auto-reset circuit | Two transistors and two resistors |
| 3.3 V regulator | A regulator, a protection diode and its capacitors |
| BOOT button | A separate factory-reset button |
| RESET button | — |

**Use the board's own BOOT button as the factory-reset button** — the firmware
can read it. Drill a small hole in the enclosure above it.

---

# SECTION G — The clock chip

`U4` keeps the time when the power goes out, so that saved readings have correct
timestamps.

| # | Connect | To |
|---|---|---|
| G1 | `U4` `VCC` pin | Junction 3.3 VOLTS |
| G2 | `U4` `GND` pin | `GROUND` |
| G3 | `U4` `SDA` pin | **Junction "CLOCK DATA"** |
| G4 | Junction CLOCK DATA | `R5` pin 2 |
| G5 | Junction CLOCK DATA | `MCU1` pin `D21` |
| G6 | `U4` `SCL` pin | **Junction "CLOCK SIGNAL"** |
| G7 | Junction CLOCK SIGNAL | `R6` pin 2 |
| G8 | Junction CLOCK SIGNAL | `MCU1` pin `D22` |
| G9 | `R5` pin 1 | Junction 3.3 VOLTS |
| G10 | `R6` pin 1 | Junction 3.3 VOLTS |
| G11 | `U4` `VBAT` pin | `BT1` **positive** terminal |
| G12 | `BT1` **negative** terminal | `GROUND` |
| G13 | `C13` pin 1 | Junction 3.3 VOLTS |
| G14 | `C13` pin 2 | `GROUND` |

Leave every other pin of `U4` unconnected.

> ⚠️ **Nothing else may touch `VBAT`.** No diode, no resistor, no charging
> circuit. Many DS3231 breakout boards you see online include a charging circuit
> for a rechargeable battery. A CR2032 is **not rechargeable** — charging it will
> make it leak, vent or burst. Just the battery holder, nothing else.

---

# SECTION H — The indicator lights

```
  MCU1 "D25" ──[R3 1k]──►|── GROUND     (LED1, green)
  MCU1 "D26" ──[R4 1k]──►|── GROUND     (LED2, blue)
                          ▲
                    the arrow points
                    from + to −
```

| # | Connect | To |
|---|---|---|
| H1 | `MCU1` pin `D25` | `R3` pin 1 |
| H2 | `R3` pin 2 | `LED1` **positive (anode)** |
| H3 | `LED1` **negative (cathode)** | `GROUND` |
| H4 | `MCU1` pin `D26` | `R4` pin 1 |
| H5 | `R4` pin 2 | `LED2` **positive (anode)** |
| H6 | `LED2` **negative (cathode)** | `GROUND` |

> **LEDs only work one way round.** On small surface-mount LEDs the negative
> side is usually marked with a green line, a dot or a notch. Check your
> specific part — the marking is not standard across manufacturers. Test one
> with a battery and a resistor before soldering a hundred.

---

# 5. Complete connection list — quick reference

Every junction in the design and everything attached to it.

| Junction name | Everything connected to it |
|---|---|
| **LIVE (raw)** ⚠️ | `J1` pin 1, `F1` pin 1 |
| **LIVE-FUSED** ⚠️ | `F1` pin 2, `RV1` pin 1, `C1` pin 1, `PS1` AC 1, `Rv1` pin 1 |
| **NEUTRAL** ⚠️ | `J1` pin 2, `RV1` pin 2, `C1` pin 2, `PS1` AC 2, `T1` primary 2 |
| **DIVIDER A** ⚠️ | `Rv1` pin 2, `Rv2` pin 1 |
| **DIVIDER B** ⚠️ | `Rv2` pin 2, `Rv3` pin 1 |
| **DIVIDER C** ⚠️ | `Rv3` pin 2, `Rv4` pin 1 |
| **DIVIDER D** ⚠️ | `Rv4` pin 2, `T1` primary 1 |
| **5 VOLTS** | `PS1` +, `C2` +, `C3` pin 1, `FB1` pin 1, `MCU1` VIN |
| **5 VOLTS CLEAN** | `FB1` pin 2, `C7` pin 1, `C8` pin 1, `U2` VDD |
| **3.3 VOLTS** | `MCU1` 3V3, `C5` pin 1, `C6` pin 1, `U4` VCC, `C13` pin 1, `R5` pin 1, `R6` pin 1 |
| **GROUND** | `PS1` −, `C2` −, `C3` pin 2, `C5` pin 2, `C6` pin 2, `MCU1` GND ×2, `U4` GND, `C13` pin 2, `BT1` −, `LED1` −, `LED2` −, `Rls2` pin 2, `R7` pin 1 |
| **ANALOG GROUND** | `U2` GND, `C7` pin 2, `C8` pin 2, `T1` secondary 2, `Rv5` pin 2, `D3` pin 2, `Cf1` pin 2, `J2` pin 2, `Rb` pin 2, `D2` pin 2, `Rf3` pin 1, `Cf3` pin 2, `Cf4` pin 2, `R7` pin 2 |
| **VOLTAGE SIGNAL** | `T1` secondary 1, `Rv5` pin 1, `D3` pin 1, `Rf1` pin 1 |
| **VOLTAGE FILTERED** | `Rf1` pin 2, `Cf1` pin 1, `U2` voltage in |
| **CLAMP SIGNAL** | `J2` pin 1, `Rb` pin 1, `D2` pin 1, `Rf2` pin 1 |
| **CURRENT +** | `Rf2` pin 2, `Cf2` pin 1, `Cf3` pin 1, `U2` current + |
| **CURRENT −** | `Rf3` pin 2, `Cf2` pin 2, `Cf4` pin 1, `U2` current − |
| **DATA 5 V** | `U2` TX, `Rls1` pin 1 |
| **DATA 3.3 V** | `Rls1` pin 2, `Rls2` pin 1, `MCU1` D16 |
| **CLOCK DATA** | `U4` SDA, `R5` pin 2, `MCU1` D21 |
| **CLOCK SIGNAL** | `U4` SCL, `R6` pin 2, `MCU1` D22 |
| **BATTERY** | `U4` VBAT, `BT1` + |
| **GREEN LIGHT** | `MCU1` D25 → `R3` → `LED1` + |
| **BLUE LIGHT** | `MCU1` D26 → `R4` → `LED2` + |

**24 junctions. That is the entire circuit.**

---

# 6. Check this before you power anything on

## With a multimeter, power completely off

- [ ] Between `GROUND` and 5 VOLTS — **not** a short circuit
- [ ] Between `GROUND` and 3.3 VOLTS — **not** a short circuit
- [ ] `GROUND` and `ANALOG GROUND` connect **only** through `R7` — lift one end
      of `R7` and confirm they become separate
- [ ] Between the mains terminal `J1` (both pins shorted together) and `GROUND`
      — **completely open, above 20 MΩ.** This is the most important test on the
      board. **If it fails, do not power it up. Ever.**
- [ ] The four resistors `Rv1`–`Rv4` measure about **188 kΩ** end to end

## By eye

- [ ] `C2` electrolytic is the right way round (stripe = negative)
- [ ] `LED1` and `LED2` are the right way round
- [ ] `D2` and `D3` are fitted (they have no direction, but must be present)
- [ ] `U2` and `U4` pin 1 matches the board marking
- [ ] No solder bridges anywhere, especially on `U2` and `U4`
- [ ] **The safety slot across the board is clean** — no solder, no flux, no bent
      component lead crossing it
- [ ] Nothing on the mains side comes within 8 mm of the safe side

## First power-up

- [ ] Use an isolation transformer and an RCD
- [ ] `PS1` output measures **4.9 – 5.2 V**
- [ ] `MCU1` `3V3` pin measures **3.25 – 3.35 V**
- [ ] The green light comes on
- [ ] The device appears on USB when you plug a cable in

---

# 7. Things that must be confirmed on the first prototypes

Three values are starting points, not final answers. Build five boards, test,
then lock them in before ordering 1,000.

| Part | Start with | What it controls | How to confirm |
|---|---|---|---|
| `Rb` | **0.68 Ω** | The current range | Feed a known current; check the reading is correct and does not flatten off at high load |
| `Rv5` | **150 Ω** | The voltage range | Vary mains from 180 V to 270 V; the reading must stay proportional |
| `Rf2` `Rf3` | **1.5 kΩ** | The clamp's timing correction | With a pure heater load, adjust until power factor reads 1.000 |

Buy a range of values for these three (see the parts list) so you can try them
without re-ordering. This is about half a day of work and it protects the entire
production run.
