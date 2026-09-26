# Wiring Guide

Every connection in the device, written as plain instructions.

Work through the eight blocks in order. Each one tells you what it does, shows a
picture, and lists the connections as simple sentences.

---

## ⚠️ Safety — read once, then remember it

1. This device connects to **230 V mains. It can kill you.**
2. **Never** work on the board while mains is connected.
3. Test everything with the power **off** first.
4. When you must power it up, use an **isolation transformer** and an
   **earth-leakage breaker (RCD)** on your bench.
5. Blocks 1 and 3 are at mains voltage. Treat them as live at all times.

There is a **safety barrier** across the middle of the board. Mains on one side,
safe on the other. Only two parts are allowed to cross it: the **power module**
and the **voltage transformer**. Both are built for it.

---

## What the device does

A clamp goes around the house's main electricity cable and measures the magnetic
field around it — it never touches the wire inside. Separately we tap live and
neutral to power the device and to measure the real mains voltage.

The metering chip combines current and voltage into watts. The ESP32 board reads
that, saves it, and sends it over WiFi.

```
   house main cable ══════╪══════
                       ╭──┴──╮
                       │clamp│═══╗
                       ╰─────╯   ║
                                 ▼
  live ──[fuse]───────────► metering ──► ESP32 ──► WiFi
                             chip        board
  neutral ──────────────►
```

---

## The parts

| What it is | Buy | How many |
|---|---|---|
| Mains terminal block | 2-way screw terminal, 5.08 mm | 1 |
| Fuse + clips | 250 mA slow-blow, 250 V, 5 × 20 mm glass | 1 + 2 clips |
| Varistor | 14D471K, blue disc | 1 |
| X2 capacitor | 100 nF, 275 VAC, safety class X2 | 1 |
| Power module | HLK-PM01, 230 V → 5 V isolated | 1 |
| Divider resistors | 47 kΩ, 1 %, ½ W, through-hole | 4 |
| Voltage transformer | ZMPT101B, bare part | 1 |
| Bulk capacitor | 470 µF, 16 V, 105 °C | 1 |
| Metering chip | HLW8032, 8 legs | 1 |
| Ferrite bead | 600 Ω at 100 MHz | 1 |
| Clamp socket | 3.5 mm stereo socket, PCB mount | 1 |
| Current clamp | SCT-013-000, 100 A : 50 mA | 1 (external) |
| Burden resistor | 0.68 Ω, 1 %, 50 ppm | 1 |
| Voltage range resistor | 150 Ω, 1 %, 50 ppm | 1 |
| Voltage filter resistor | 1 kΩ | 1 |
| Current filter resistors | 1.5 kΩ, matched pair | 2 |
| Filter capacitors | 33 nF | 2 |
| Small filter capacitors | 10 nF | 2 |
| Protection diodes | SMAJ5.0CA, bidirectional | 2 |
| Divider resistors (signal) | 1 kΩ and 2 kΩ | 1 each |
| Ground link | 0 Ω jumper | 1 |
| ESP32 board | ESP32 Type-C, 30 pins | 1 |
| Header sockets | 1 × 15 female | 2 |
| Clock chip | DS1307Z+, 8 legs | 1 |
| Crystal | 32.768 kHz, **12.5 pF**, cylindrical | 1 |
| Battery holder + battery | CR2032 | 1 each |
| Pull-up resistors | 4.7 kΩ | 2 |
| LED resistors | 1 kΩ | 2 |
| LEDs | green and blue | 1 each |
| Decoupling capacitors | 100 nF | 4 |
| Decoupling capacitors | 10 µF | 2 |

---

## The two grounds

The board has **two separate ground areas** that meet at exactly one point.

| | Used by |
|---|---|
| **GROUND** | ESP32 board, clock chip, LEDs, power module |
| **ANALOG GROUND** | Metering chip, the clamp, all the filter parts |

The ESP32 gulps half an amp in bursts when it transmits WiFi. The metering chip
reads signals of a few thousandths of a volt. Sharing a ground path would put
those bursts straight into your measurements.

**They are joined by the 0 Ω jumper, and nowhere else.** Put it right beside the
metering chip.

```
    GROUND ─────[ 0 Ω jumper ]───── ANALOG GROUND
                  ONE POINT
```

---

# Block 1 — Mains input ⚠️

Brings mains in, protects the circuit, and feeds the power module.

```
              fuse
  LIVE ───────▭▭▭────┬─────────┬─────────┬──── power module "AC-L"
                     │         │         │
                 varistor   X2 cap   to Block 3
                     │         │
  NEUTRAL ───────────┴─────────┴──────────────  power module "AC-N"
                                         │
                                         └──── to Block 3
```

**Connections**

1. **Live** comes into one screw of the **mains terminal block**.
2. From that screw, go to **one end of the fuse**.
3. The **other end of the fuse** is your **fused live** point. Connect four
   things to it: the **varistor**, the **X2 capacitor**, the power module's
   **AC-L** pin, and the **first 47 kΩ resistor** (which carries on into Block 3).
4. **Neutral** comes into the other screw of the terminal block. That screw is
   your **neutral** point. Connect four things to it: the **varistor's other
   leg**, the **X2 capacitor's other leg**, the power module's **AC-N** pin, and
   **one input pin of the voltage transformer** (Block 3).

The fuse is not soldered — it clips into the two fuse clips so it can be
replaced. The varistor and X2 capacitor have no polarity; either leg works.

---

# Block 2 — Power supply

The power module turns 230 V into an isolated 5 V. Everything after it is safe
to touch.

```
  "+Vo" ──┬────────┬──────┬──────────────► ESP32 "VIN"
          │        │      │                clock chip "VCC"
       470 µF   100 nF  ferrite ──┬──┬──► metering chip "VDD"
          │        │              │  │
  "-Vo" ──┴────────┴─ GROUND    10 µF 100 nF ─► ANALOG GROUND
```

**Connections — the 5 V rail**

1. The power module's **+Vo** pin is your **5 V rail**. Connect five things to
   it: the **470 µF capacitor's positive leg**, a **100 nF capacitor**, the
   **ferrite bead**, the ESP32 board's **VIN** pin, and the clock chip's **VCC**
   pin (Block 7).
2. The power module's **−Vo** pin goes to **GROUND**.
3. The **470 µF capacitor's negative leg** goes to **GROUND**.
4. That **100 nF capacitor's other end** goes to **GROUND**.

The 470 µF capacitor has a direction — the negative leg is the shorter one, and
the can has a stripe down that side.

**Connections — the clean 5 V for the metering chip**

The ferrite bead splits the supply so WiFi noise cannot reach the metering chip.

5. The **ferrite bead's other end** is your **clean 5 V** point. Connect three
   things: a **10 µF capacitor**, a **100 nF capacitor**, and the metering
   chip's **VDD** pin.
6. Both of those capacitors' other ends go to **ANALOG GROUND**.

**Nothing else may touch the clean 5 V point.** Only those three things.

**Connections — the 3.3 V rail**

The ESP32 board makes its own 3.3 V and shares it on a pin.

7. The ESP32's **3V3** pin is your **3.3 V rail**. Connect four things: a
   **10 µF capacitor**, a **100 nF capacitor**, and both **4.7 kΩ pull-up
   resistors** (Block 7).
8. Both of those capacitors' other ends go to **GROUND**.

---

# Block 3 — Measuring the mains voltage ⚠️

Four resistors shrink the mains to a tiny current. The transformer passes that
across the safety barrier with no electrical connection at all.

```
 fused live ─[47k]─[47k]─[47k]─[47k]─► transformer in 1
                                       transformer in 2 ─► neutral

        ═════════ SAFETY BARRIER ═════════

 transformer out 1 ─┬──────┬─────[1 kΩ]──┬─► metering chip "V1P"
                    │      │             │
                 150 Ω   diode        33 nF
                    │      │             │
 transformer out 2 ─┴──────┴─────────────┴─► ANALOG GROUND
```

**Connections**

1. Chain the **four 47 kΩ resistors end to end**, in series. The first one
   connects to **fused live** (from Block 1).
2. The **last 47 kΩ resistor** connects to **one input pin of the transformer**.
3. The transformer's **other input pin** goes to **neutral** (from Block 1).
4. One of the transformer's **output pins** is your **voltage signal** point.
   Connect three things: the **150 Ω resistor**, a **protection diode**, and the
   **1 kΩ voltage filter resistor**.
5. The transformer's **other output pin** goes to **ANALOG GROUND**.
6. The **150 Ω resistor's other end** goes to **ANALOG GROUND**.
7. The **diode's other end** goes to **ANALOG GROUND**.
8. The **1 kΩ resistor's other end** is your **filtered voltage** point. Connect
   two things: a **33 nF capacitor**, and the metering chip's **V1P** pin.
9. That **33 nF capacitor's other end** goes to **ANALOG GROUND**.

The protection diode is bidirectional, so it has no polarity.

**Why four resistors and not one:** a single resistor across 230 V is at its
voltage limit and will arc over during a surge. Four share it — about 58 V each.
If one fails it fails open, which is the safe outcome. And the heat spreads over
four parts instead of one hot spot. **Never replace them with a single resistor.**

---

# Block 4 — Measuring the current

The clamp makes a tiny current. The burden resistor turns it into a voltage.

```
   jack TIP ────┬──────┬───[1.5k]──┬──────┬─► metering chip "I1P"
                │      │           │      │
            0.68 Ω   diode       33 nF  10 nF
                │      │           │      │
 jack SLEEVE ───┴──────┴──[1.5k]───┴──────┼─► metering chip "I1N"
       │                    ▲            10 nF
   jack RING                │              │
       │                    │              │
       └─ ANALOG GROUND ────┘       ANALOG GROUND
```

**The clamp plugs in — it is not soldered and not screwed.** The SCT-013-000
arrives with a **3.5 mm stereo plug already moulded onto its cable**, so the
board carries a matching **3.5 mm stereo socket**. The installer pushes the plug
in and the job is done.

### Why the socket has three contacts when the clamp has two wires

A 3.5 mm stereo socket has three contacts, named after the parts of the plug
they touch:

| Contact | Name | What the clamp uses it for |
|---|---|---|
| **TIP** | the very end of the plug | **One end of the clamp winding** |
| **RING** | the middle band | **Nothing — the clamp leaves it unconnected** |
| **SLEEVE** | the long barrel nearest the cable | **The other end of the clamp winding** |

So the clamp really does only use two of them. The third exists because the
plug is a standard audio plug.

**We connect RING to ANALOG GROUND anyway**, for three reasons:

1. The socket then also accepts a **two-contact (mono) plug**, in case a
   different clamp is ever used.
2. While a plug is being pushed in, its tip slides across the RING contact.
   With RING grounded, that momentarily **shorts** the clamp — and **a shorted
   clamp is the safe state.** (It is an *open* clamp that is dangerous.)
3. A floating metal contact sitting right beside the signal contact picks up
   noise. Grounded, it shields instead.

This is harmless once the plug is fully home, because the plug's own ring band
is not connected to anything inside the clamp.

**Connections**

1. The socket's **TIP** contact is your **clamp signal** point.
   Connect three things: the **0.68 Ω burden resistor**, a **protection diode**,
   and the **first 1.5 kΩ filter resistor**.
2. The socket's **SLEEVE** contact goes to **ANALOG GROUND**.
3. The socket's **RING** contact goes to **ANALOG GROUND** as well.
4. The **burden resistor's other end** goes to **ANALOG GROUND**.
5. The **diode's other end** goes to **ANALOG GROUND**.
6. The **first 1.5 kΩ resistor's other end** is your **current +** point.
   Connect three things: a **33 nF capacitor**, a **10 nF capacitor**, and the
   metering chip's **I1P** pin.
7. Separately, connect **ANALOG GROUND** to the **second 1.5 kΩ resistor**.
8. That resistor's **other end** is your **current −** point. Connect three
   things: the **33 nF capacitor's other end** (the same one from step 6), the
   **second 10 nF capacitor**, and the metering chip's **I1N** pin.
9. Both **10 nF capacitors' other ends** go to **ANALOG GROUND**.

**The second 1.5 kΩ resistor looks pointless but is essential.** It runs from
ground into the chip's negative input. The chip compares its two inputs against
each other — if the two paths have different resistance, noise picked up by the
clamp cable stops cancelling out. **Both resistors must be the same value.**

**They also correct the clamp's timing error.** A clamp shifts the current signal
slightly in time, which makes readings wrong on motor loads. Making these two
bigger than the 1 kΩ voltage filter resistor compensates. 1.5 kΩ is the starting
point — you tune it during calibration, and you always change both together.

### Three things to get right about the socket

**1. It must sit on the low-voltage side of the barrier.** The socket, its hole
in the case, and everything it touches belong on the safe side of the 8 mm gap.
Never route a clamp track across the barrier.

**2. Give the cable a strain relief in the plastic case.** This is the one real
weakness of a plug compared to a screw terminal: a screw terminal cannot fall
out, a plug can vibrate loose over years in a panel. Mould a slot or clamp into
the 3D-printed case that grips the **cable**, so the socket never takes the
pull. Design the hole about 0.5 mm oversize — 3D prints are not precise enough
to trust a tight fit.

**3. The footprint must match the socket you actually buy.** Every 3.5 mm socket
has a different pin arrangement. Download the footprint from the product page of
the exact part number you are ordering — do not reuse a footprint from another
manufacturer's socket because "it is also 3.5 mm". See section 6 of the parts
list.

### Is it safe that the clamp can be unplugged while the power is on?

**Yes — and this is designed for, not a lucky accident.**

Normally, disconnecting a current transformer while current flows through the
cable it is clamped around is dangerous: the winding tries to push current into
an open circuit and the voltage climbs. The **SCT-013-000 has a transient
voltage suppressor built inside it** for exactly this reason (older units used
two 22 V zener diodes). The voltage on the plug is clamped to a safe level.

**Good practice anyway:** unclip the clamp from the cable before pulling the
plug out.

### Optional: let the device know the clamp is missing

Most 3.5 mm sockets include a **switch contact** — a spare pin that is connected
when no plug is inserted and disconnects when one is. Wire it to a spare ESP32
pin with a pull-up and the firmware can tell the difference between
**"0 watts"** and **"nobody plugged the clamp in"**.

Cost: one spare pin and one resistor. **Worth it** — it turns a silent
installation mistake into a message on the app.

---

# Block 5 — Metering chip to ESP32

The metering chip runs on 5 V and sends data on one wire. The ESP32 only accepts
3.3 V, so two resistors divide it down.

```
  metering chip "TX" ──[1 kΩ]──┬──► ESP32 "D16"
                               │
                            [2 kΩ]
                               │
                            GROUND
```

**Connections**

1. The metering chip's **TX** pin connects to the **1 kΩ divider resistor**.
2. That resistor's **other end** connects to two things: the **2 kΩ divider
   resistor**, and the ESP32's **D16** pin.
3. The **2 kΩ resistor's other end** goes to **GROUND**.
4. The metering chip's **GND** pin goes to **ANALOG GROUND** — not to GROUND.
5. Connect the **0 Ω jumper** between **GROUND** and **ANALOG GROUND**. This is
   the only place the two grounds meet.

The chip's **PF** pin is not connected — we don't use it.

The maths: 5 V × 2k ÷ (1k + 2k) = **3.33 V**, exactly what the ESP32 wants.

---

# Block 6 — The ESP32 board

The board plugs into two 15-hole female header strips. Orient it so the
**antenna end hangs over the edge** of your board, and the **USB socket faces the
enclosure wall**.

```
  antenna →│████ ESP32 board ████│← USB faces the wall
           └─╥─────────────────╥─┘
             ╨  header sockets ╨
      ┌────────────────────────────────┐
      │           your PCB             │
      └────────────────────────────────┘
```

**Only 9 of the 30 pins are used.**

| ESP32 pin | Goes to |
|---|---|
| **VIN** | the 5 V rail |
| **GND** (either) | GROUND |
| **GND** (the other) | GROUND |
| **3V3** | the 3.3 V rail |
| **D16** | the signal divider (Block 5) |
| **D21** | the clock chip's data line (Block 7) |
| **D22** | the clock chip's clock line (Block 7) |
| **D25** | the green LED's resistor (Block 8) |
| **D26** | the blue LED's resistor (Block 8) |

**Leave every other pin unconnected.**

The board already has a USB socket, a USB-to-serial chip, an auto-reset circuit,
a 3.3 V regulator and two buttons — so we don't fit any of those ourselves.
**Use its BOOT button as the factory-reset button**; the firmware can read it.
Put a small hole in the enclosure above it.

---

# Block 7 — The clock chip

Keeps time running while the device is switched off, so readings stored during an
internet outage still get correct timestamps.

```
  5 V rail ──┬──────── clock "VCC"       crystal
             │                         ┌─────────┐
          100 nF          clock "X1" ──┤ 32.768  │
             │            clock "X2" ──┤   kHz   │
  GROUND ────┴──────── clock "GND"     └─────────┘

  3.3 V ──[4.7k]──┬── clock "SDA" ── ESP32 "D21"
  3.3 V ──[4.7k]──┴── clock "SCL" ── ESP32 "D22"

  clock "VBAT" ──── battery holder "+"
                    battery holder "−" ── GROUND
```

**Connections**

1. The clock chip's **VCC** pin goes to the **5 V rail**.
2. The clock chip's **GND** pin goes to **GROUND**.
3. The clock chip's **X1** pin goes to **one leg of the crystal**.
4. The clock chip's **X2** pin goes to the **crystal's other leg**.
5. The clock chip's **VBAT** pin goes to the **battery holder's positive
   terminal** — and to nothing else.
6. The **battery holder's negative terminal** goes to **GROUND**.
7. The clock chip's **SDA** pin connects to two things: a **4.7 kΩ pull-up
   resistor**, and the ESP32's **D21** pin.
8. The clock chip's **SCL** pin connects to two things: the **other 4.7 kΩ
   pull-up resistor**, and the ESP32's **D22** pin.
9. Both **pull-up resistors' other ends** go to the **3.3 V rail**.
10. Connect a **100 nF capacitor** between the **5 V rail** and **GROUND**, close
    to the chip.

The chip's **SQW** pin is not connected.

**The crystal must be the 12.5 pF type, and needs no capacitors** — the clock
chip has them inside. Place the crystal within 5 mm of the chip.

---

# Block 8 — The indicator lights

```
  ESP32 "D25" ──[1 kΩ]──▶|── GROUND    green LED
  ESP32 "D26" ──[1 kΩ]──▶|── GROUND    blue LED
```

**Connections**

1. The ESP32's **D25** pin goes to a **1 kΩ resistor**.
2. That resistor's other end goes to the **green LED's positive side (anode)**.
3. The **green LED's negative side (cathode)** goes to **GROUND**.
4. The ESP32's **D26** pin goes to the **other 1 kΩ resistor**.
5. That resistor's other end goes to the **blue LED's positive side**.
6. The **blue LED's negative side** goes to **GROUND**.

---

# Before you power anything on

**With a multimeter, power completely off**

- [ ] 5 V rail to GROUND — **not** a short circuit
- [ ] 3.3 V rail to GROUND — **not** a short circuit
- [ ] The two grounds connect **only** through the 0 Ω jumper. Lift one end of
      it and confirm they separate
- [ ] ⭐ **Short both screws of the mains terminal block together and measure to
      GROUND. It must read completely open, above 20 MΩ.** If it does not, do
      not power the board up. Ever
- [ ] The four 47 kΩ resistors measure about **188 kΩ** end to end
- [ ] Trace the two 4.7 kΩ pull-ups — they must reach the **3.3 V rail**, not 5 V

**By eye**

- [ ] The 470 µF capacitor is the right way round (stripe = negative)
- [ ] Both LEDs are the right way round
- [ ] The battery holder is the right way round
- [ ] Leg 1 of both chips matches the board marking
- [ ] No solder bridges, especially on the two chips
- [ ] The safety slot across the board is clean — no solder, no flux, no bent
      component lead crossing it
- [ ] Nothing on the mains side comes within 8 mm of the safe side

**First power-up** — use an isolation transformer and an RCD

- [ ] The power module puts out **4.9 – 5.2 V**
- [ ] The ESP32's 3V3 pin reads **3.25 – 3.35 V**
- [ ] The green LED comes on
- [ ] The device appears on USB when you plug a cable in
- [ ] The clock chip answers and reports a sensible time once you set it

---

# Things that will bite you

Every mistake worth warning about, in one place.

### Mains side

**The varistor and X2 capacitor must be AFTER the fuse.** A varistor fails as a
short circuit at the end of its life. After the fuse, it just blows the fuse.
Before it, it is a direct short across mains — a fire.

**The fuse must be 250 VAC rated and slow-blow.** A 63 V surface-mount fuse
cannot interrupt a mains fault and will explode.

**The capacitor across mains must be class X2.** X2 parts fail open by design.
An ordinary ceramic capacitor there is a fire hazard.

**Keep 8 mm between the mains side and the safe side**, everywhere.

### The clock chip

**Its pull-up resistors go to 3.3 V, never 5 V.** The chip runs on 5 V, but its
data lines are open-drain — they only pull *down*, never push up. So whatever
you pull them up to is the highest voltage the bus ever reaches. Pull to 3.3 V
and the ESP32 is safe. Pull to 5 V and you damage it, possibly not immediately,
which is worse.

**The battery wire has nothing else on it.** No diode, no resistor, no charging
circuit. The chip switches to the battery by itself. This is why we use the bare
chip instead of a ready-made module — the common modules put a resistor divider
or a charging circuit on that pin, and both are wrong.

**The crystal must be 12.5 pF.** A 6 pF crystal makes the clock run minutes per
day slow.

### The metering chip

**Never connect its TX pin straight to the ESP32.** It outputs 5 V. Use the two
divider resistors.

**Use D16, not RX0.** RX0 is the USB programming pin. If the metering chip is
sending data into it, you cannot upload code or read debug messages.

**Its GND pin goes to ANALOG GROUND**, not GROUND.

### The current clamp

**Always open and remove the clamp from the cable BEFORE disconnecting its wires
from the device.** A clamp left open-circuit on a live cable develops dangerous
voltage across its terminals.

**The burden resistor must be 1 %, 50 ppm/°C, and never wirewound.** Every amp
you measure is defined by this one resistor's value. Wirewound parts add timing
error.

### General

**LEDs only work one way round**, and the cathode marking is not standard between
manufacturers. Test one with a coin cell and a resistor before soldering a
hundred.

**Clean the flux off, especially across the safety slot.** Flux residue absorbs
moisture and becomes conductive in humid air — it quietly destroys the isolation
you built in, and you will not find out until the first humid summer.

---

# Three values to confirm on the first prototypes

These are starting points, not final answers. Build five boards, test, then lock
them in before ordering 1,000.

| Part | Start with | What it sets | How to confirm |
|---|---|---|---|
| **Burden resistor** | 0.68 Ω | The current range | Feed a known current; the reading must be correct and must not flatten off at high load |
| **Voltage range resistor** | 150 Ω | The voltage range | Vary mains from 180 V to 270 V; the reading must stay proportional |
| **The two 1.5 kΩ resistors** | 1.5 kΩ | The clamp's timing correction | With a pure heater load, adjust until power factor reads 1.000 |

Buy a range of values for these three — the shopping list says which — so you can
try them without re-ordering. Half a day of work that protects the whole run.

---

# Appendix — labels for the board silkscreen

When you draw the PCB you will want short labels printed next to each part. These
are the ones used in the shopping list.

| Label | Part |
|---|---|
| J1 / J2 | Mains terminal block / clamp socket |
| F1 | Fuse (FH1 = its two clips) |
| RV1 | Varistor |
| C1 | X2 capacitor |
| PS1 | Power module |
| Rv1, Rv2, Rv3, Rv4 | The four 47 kΩ resistors |
| T1 | Voltage transformer |
| Rv5 | 150 Ω voltage range resistor |
| Rf1 | 1 kΩ voltage filter resistor |
| Cf1 | 33 nF voltage filter capacitor |
| D3 | Voltage protection diode |
| CT1 | The current clamp (external — not on the board) |
| Rb | 0.68 Ω burden resistor |
| Rf2 / Rf3 | The two 1.5 kΩ current filter resistors |
| Cf2 | 33 nF current filter capacitor |
| Cf3 / Cf4 | The two 10 nF capacitors |
| D2 | Clamp protection diode |
| U2 | Metering chip |
| FB1 | Ferrite bead |
| Rls1 / Rls2 | 1 kΩ and 2 kΩ signal divider |
| R7 | 0 Ω ground jumper |
| MCU1 | ESP32 board (J4, J5 = its header sockets) |
| U4 | Clock chip |
| Y1 | Crystal |
| BT1 / B1 | Battery holder / battery |
| R5 / R6 | The two 4.7 kΩ pull-ups |
| C13 | Clock decoupling capacitor |
| LED1 / LED2 | Green / blue LED |
| R3 / R4 | The two LED resistors |
| C2 | 470 µF bulk capacitor |
| C3 / C6 / C8 | 100 nF decoupling capacitors |
| C5 / C7 | 10 µF decoupling capacitors |
