# 2. Circuit Design

Block-by-block, with the arithmetic behind every value. Reference designators
used here match [`docs/03-bom.md`](03-bom.md) and
[`hardware/bom.csv`](../hardware/bom.csv).

**Convention:** everything in sections 2.1–2.3 is on the **mains side** of the
isolation barrier and must be treated as live at all times. Everything from
section 2.4 onward is **SELV** and safe.

---

## 2.1 Block A — Mains input and protection

```
  L ──── J1.1 ──── F1 ──┬──────────── to PS1 (AC-L)
                        │
                       RV1 (MOV)     C1 (X2, 100nF)
                        │              │
  N ──── J1.2 ──────────┴──────────────┴──── to PS1 (AC-N)
                        │
                        └──── to Rv1..Rv4 → T1 primary (voltage sense)
```

| Ref | Value | Role |
|---|---|---|
| J1 | 2-pin screw terminal, 5.08 mm pitch, 300 V / 10 A | Mains L and N entry. 5.08 mm (not 3.5 mm) because it must accept 1.5 mm² house wire and hold 300 V between poles. |
| F1 | 250 mA, **time-lag (T)**, 250 VAC, 5 × 20 mm glass + PCB clips | The fire-safety part. If anything downstream fails short, this opens before the house wiring heats up. |
| RV1 | MOV, 14 mm disc, 470 V varistor voltage (`14D471K` / `S14K275`) | Clamps lightning-induced and switching surges to a level the PSU survives. |
| C1 | 100 nF X2 safety capacitor, 275 VAC | Suppresses fast differential-mode noise, both incoming and outgoing. |

### Why these values

**Fuse = 250 mA, time-lag.** The whole board draws at most 3 W from the mains,
which is about 13 mA at 230 V. But the HLK-PM01's input capacitor draws a large,
brief inrush spike at switch-on — a fast-blow fuse would nuisance-trip. 250 mA
time-lag is ~19× the running current (so it never trips in service) while still
being far below the current that would damage 1.5 mm² wiring.

**MOV must be *after* the fuse.** This is a safety rule, not a preference. MOVs
fail short at end of life. If the MOV is upstream of the fuse, a failed MOV is a
direct L-N short with no protection — a fire. Downstream of the fuse, a failed
MOV simply blows the fuse and the unit goes dark.

**Varistor voltage 470 V for 230 V mains.** The MOV must not conduct on normal
mains peaks. 230 V RMS peaks at 325 V, and a 10 % high line (253 V) peaks at
358 V. A 470 V device sits safely above that while still clamping real surges.
Do not fit a 275 V or 390 V MOV here — it will cook itself on normal mains.

**X2, not X1 or Y or a general-purpose capacitor.** X-class capacitors are
designed to fail *open*, not short, when connected line-to-line. A normal 100 nF
ceramic in this position is a fire hazard. This part number matters.

### Optional (not in the base BOM)
A common-mode choke in the L/N path would improve conducted-emissions behaviour.
Leave a **footprint** for it, unpopulated. You will want it if you ever pursue CE
marking; you do not need it to make the product work.

---

## 2.2 Block B — Isolated power supply

```
  AC-L ──┐                        ┌──── +5V ──┬──[D1]──┐
         │   ┌──────────────┐     │           │        │
         ├───┤  PS1         ├─────┘          C2       U1 AMS1117-3.3
         │   │  HLK-PM01    │              470µF     ┌────┴────┐
  AC-N ──┴───┤  230VAC→5V   ├─────┐          │       │ IN  OUT ├──┬── +3V3
             │  3 W isolated│     │          │       │   GND   │  │
             └──────────────┘     └──── GND ─┴───────┴────┬────┘ C4 470µF
                                                          │      C5 10µF
                                                         GND     C6 100nF
```

| Ref | Value | Role |
|---|---|---|
| PS1 | HLK-PM01, 100–264 VAC → 5 V / 0.6 A / 3 W, **isolated** | The isolation barrier for power. Through-hole, 34 × 20 × 15 mm. |
| C2 | 470 µF / 16 V electrolytic | Bulk reservoir on 5 V; absorbs the ESP32's Wi-Fi transmit bursts before they reach the PSU. |
| D1 | 1N4148 (or SS14) cathode→5 V, anode→3V3 | Protects the LDO if a programmer back-feeds 3.3 V into an unpowered board. |
| U1 | AMS1117-3.3, SOT-223 | 5 V → 3.3 V linear regulator. |
| C4 | 470 µF / 10 V electrolytic | Bulk on 3.3 V, placed **within 10 mm of the ESP32's 3V3 pin**. |
| C5 | 10 µF / 16 V X7R 0805 | Mid-frequency decoupling. |
| C6 | 100 nF X7R 0805 | High-frequency decoupling. |

### Power budget

| Consumer | Typical | Peak |
|---|---|---|
| ESP32 (Wi-Fi connected, idle) | 80 mA | 500 mA for < 2 ms during TX |
| ATM90E26 | 4 mA | 4 mA |
| DS3231 | 0.2 mA | 0.2 mA |
| 2 × status LED | 4 mA | 4 mA |
| **Total at 3.3 V** | **~90 mA** | ~510 mA burst |

- HLK-PM01 supplies 600 mA at 5 V (3 W). Average draw is ~90 mA → **6.7× margin**.
- LDO dissipation: `(5 − 3.3) × 0.09 = 0.15 W` average. SOT-223 with ~200 mm² of
  copper pour handles this at a modest temperature rise. Peaks of 0.85 W last
  under 2 ms and are absorbed thermally.
- The 470 µF on 3.3 V is what makes the Wi-Fi bursts invisible to the LDO. Do not
  reduce it — brown-out resets during Wi-Fi TX are the classic ESP32 field
  failure, and they are always a missing bulk capacitor.

### Alternative if you want to drop the LDO
`HLK-PM03` outputs 3.3 V directly, saving U1 and one capacitor. The cost is
switching ripple landing directly on the analog rail of the metering IC. If you
take this route, the ferrite-bead filter in §2.5 becomes mandatory rather than
recommended, and you should verify measurement noise on a prototype before
committing.

---

## 2.3 Block C — Isolated mains voltage sensing

```
                Rv1   Rv2   Rv3   Rv4        T1: ZMPT101B
  AC-L ────────[47k]─[47k]─[47k]─[47k]────┬──╮│╭──┬──── (secondary) ──┐
                                          │  ││││  │                  │
                                          ╰──╯│╰──╯              Rv5 [330R]
                                     (primary)│                       │
  AC-N ───────────────────────────────────────┘                    ┌──┴──┐
                                                                   │     │
          ║ ISOLATION BARRIER ║              Rf1 [1k]              D3   AGND
                                     VP ◄────[1k]──┬───────────────┤ (TVS
                                                   │               │  SMAJ5.0CA)
                                     VN ◄─── AGND  Cf1 [33nF]      │
                                                   │               │
                                                  AGND            AGND
```

| Ref | Value | Role |
|---|---|---|
| Rv1–Rv4 | 4 × 47 kΩ, 1 %, **1/2 W metal film, through-hole** | Convert mains voltage into a small, safe current for the transformer primary. |
| T1 | ZMPT101B voltage transformer (1000 : 1000 turns, 2 mA : 2 mA) | The isolation barrier for the voltage signal. |
| Rv5 | 330 Ω, 1 %, ≤ 50 ppm/°C | **Secondary burden** — converts the transformer's output current back to a voltage. *Value to confirm — see §3.3.* |
| Rf1 | 1 kΩ, 1 % | Anti-alias filter resistor. |
| Cf1 | 33 nF, NP0/C0G | Anti-alias filter capacitor. |
| D3 | SMAJ5.0CA bidirectional TVS | Clamps transients coupled through the transformer. |

### The arithmetic

The ZMPT101B is a **current-type** transformer: you feed a small current into the
primary and the same current comes out of the secondary, isolated.

```
Primary resistance  R = Rv1 + Rv2 + Rv3 + Rv4 = 4 × 47 kΩ = 188 kΩ

Primary current at nominal 230 V :  I = 230 / 188 000 = 1.22 mA RMS
Primary current at 250 V (high)  :  I = 1.33 mA RMS
Primary current at 300 V (surge) :  I = 1.60 mA RMS   ← still under the 2 mA rating ✓

Total dissipation : P = I² · R = (1.22 mA)² × 188 kΩ = 0.28 W
Per resistor      : 0.28 / 4 = 0.07 W   ← 1/2 W parts run at 14 % of rating ✓
```

### Why four resistors in series instead of one

Three separate reasons, all of which matter:

1. **Voltage rating.** A standard 1/4 W or 1/2 W resistor is rated for about
   200–250 V *working voltage*, regardless of its power rating. One 188 kΩ
   resistor across 230 V mains is operating at its limit, and a surge will arc
   across it. Four in series share the stress: ~58 V each at nominal, and the
   string survives an 800 V transient.
2. **Failure mode.** If a resistor fails, it fails open, and the string opens —
   which is the safe outcome. There is no single-point failure that shorts mains
   into the transformer.
3. **Heat.** 0.28 W in one small part is a hot spot next to mains tracks.
   Spread over four, nothing gets warm.

Use **through-hole metal film** here rather than SMD. It is easier to hand-solder,
it has a much better voltage rating than a 1206 chip resistor, it lifts the body
off the board surface (extra creepage), and it is available in every electronics
shop in Damascus and Beirut.

### Sizing the secondary burden Rv5

Because primary current = secondary current, the secondary sees the same
1.22 mA at 230 V. `Rv5` turns that into the voltage the metering IC reads:

```
V_sense = I_secondary × Rv5
```

We want the *maximum* expected mains voltage (take 300 V as the design ceiling)
to land at roughly 80–85 % of the metering IC's full-scale input, leaving
headroom so surges clip the TVS rather than the ADC.

| If ATM90E26 full scale is… | Target at 300 V | Required Rv5 | Reading at 230 V |
|---|---|---|---|
| ~600 mV RMS | 500 mV | **330 Ω** | 402 mV |
| ~120 mV RMS | 100 mV | **62 Ω** | 83 mV |

**Recommended starting value: 330 Ω**, with a second parallel footprint (`Rv6`,
not populated) so you can trim downward on the prototypes without cutting traces.
See §3.3 — this is one of the two values you must confirm on hardware.

### Important: buy the bare ZMPT101B transformer, not the "ZMPT101B module"

AliExpress sells a popular blue breakout board also called "ZMPT101B" that
carries an LM358 op-amp and a blue trimmer potentiometer. **Do not buy that.**
It is designed to feed an Arduino's single-ended ADC, it adds op-amp offset
drift, and the trimmer is a long-term reliability problem (they drift and go
noisy). You want the bare transformer only — a small black rectangular part with
four pins.

---

## 2.4 Block D — Current sensing (CT input)

```
                              J2 (3.5mm screw terminal, SELV)
   ╭─────────╮  1 m lead      ┌──────┐
   │   CT    │════════════════│ S1   ├──┬──────[Rf2 1k]───► I1P
   │ clamp   │                │      │  │                    │
   │ 100A:   │                │      │ Rb (10R)    Cf2 [33nF]│
   │  50mA   │                │      │  │  D2        │       │
   ╰─────────╯                │ S2   ├──┴──┴─────[Rf3 1k]───► I1N
                              └──────┘     │              │
                                          AGND           AGND
```

| Ref | Value | Role |
|---|---|---|
| CT1 | Split-core CT, 100 A : 50 mA (2000:1), 13 mm window — `SCT-013-000` | Non-invasive current sensing. **External to the PCB.** |
| J2 | 2-pin screw terminal, 3.5 mm pitch | CT connection. Deliberately a *different size* from J1 so mains can never be wired here by mistake. |
| Rb | 10 Ω, 1 %, **≤ 50 ppm/°C**, 0.25 W | **Burden resistor** — converts CT secondary current to voltage. *Value to confirm — see §3.3.* |
| Rb2 | (parallel footprint, not populated) | Range trimming during prototype bring-up. |
| D2 | SMAJ5.0CA bidirectional TVS | Clamps the open-circuit spike and ESD on the CT leads. |
| Rf2, Rf3 | 1 kΩ, 1 %, **matched pair** | Anti-alias / current-limit into the differential input. |
| Cf2 | 33 nF NP0 (differential) | Anti-alias. |
| Cf3, Cf4 | 10 nF NP0 (each leg to AGND) | Common-mode filtering. |

### The arithmetic

```
CT ratio            : 2000 : 1   (100 A primary → 50 mA secondary)
Design full scale   : 78 A primary  (63 A breaker + 24 % headroom)
Secondary at 78 A   : 78 / 2000 = 39 mA RMS

Burden voltage      : V = 39 mA × 10 Ω = 390 mV RMS
Burden dissipation  : P = (39 mA)² × 10 Ω = 15 mW      ← nothing ✓
Sensitivity         : 10 Ω / 2000 = 5 mV per amp
```

### Why the burden resistor is the most important passive on the board

Everything about your current accuracy flows through this one part:

- **Its tolerance is your gain error.** A 5 % resistor gives you a 5 % current
  error before calibration. You calibrate that out per unit — but only at the
  temperature you calibrated at.
- **Its temperature coefficient is your drift, and you cannot calibrate it out.**
  A cheap 100 ppm/°C resistor drifting over a 40 °C swing inside a breaker panel
  gives 0.4 % error. A 50 ppm/°C part halves that; 25 ppm/°C quarters it.
  **Specify ≤ 50 ppm/°C and do not let a supplier substitute it.**
- Use a 1 % metal-film or thin-film part. Do not use a wirewound resistor here —
  its inductance introduces phase error that varies with frequency.

### Deliberately choosing the burden on the *low* side

Note that 10 Ω is a conservative choice. Here is the reasoning, and it is worth
understanding because it applies to every ADC front end you will ever design:

> **Clipping is unrecoverable. Gain is a register write.**

If the burden is too large and a 60 A load clips the ADC, the reading is silently
wrong and no firmware can fix it — you must unsolder 1,000 resistors. If the
burden is too small, the signal is smaller than ideal, and you simply raise the
ATM90E26's PGA from 1× to 4× in firmware and get the resolution back.

So: size for no clipping at the worst case, and keep the PGA in your pocket.

> ⚠️ One caveat: with `Rb = 10 Ω`, PGA **must stay at 1×** for whole-house use.
> PGA 4× would clip at about 19 A. The PGA is a recovery option only if you
> discover the real full scale is much larger than assumed.

### CT safety

An open-circuited current transformer sitting on a live conductor develops
dangerous voltages across its terminals. Two protections:

1. **The burden resistor is permanently soldered to the board.** While the CT is
   plugged in, it is never open. This is why the burden lives on the PCB and not
   inside the clamp.
2. **D2 clamps the transient** if someone pulls the lead out while the clamp is
   still on a live cable.

**Installation rule for your manual, in bold:** *always open and remove the clamp
from the cable before disconnecting its wires from the device.*

---

## 2.5 Block E — Metering IC (ATM90E26)

```
                        ┌──────────────────────┐
     3V3 ──[FB1]──┬─────┤ AVDD                 │
                  │     │                 CS   ├──► ESP32 IO5
                C7 10µF │                 SCK  ├──► ESP32 IO18
                C8 100nF│                 MOSI ├──► ESP32 IO23
                  │     │                 MISO ├──◄ ESP32 IO19
                AGND    │                      │
     3V3 ──────────┬────┤ DVDD            IRQ  ├──► ESP32 IO4  (optional)
                 C9 100nF                 ZX   ├──► ESP32 IO16 (optional)
                   │    │                      │
                 DGND   │ USEL ── GND (= SPI)  │
                        │                      │
      V sense ─────────►│ VP              OSCI ├──┬── Y1 8.192 MHz ──┬── OSCO
      AGND ────────────►│ VN                   │ C10 27pF        C11 27pF
      CT + ────────────►│ I1P                  │  │                  │
      CT − ────────────►│ I1N                  │ AGND               AGND
                        └──────────────────────┘
```

| Ref | Value | Role |
|---|---|---|
| U2 | ATM90E26-YU-R, SSOP-28 | The measurement engine. |
| Y1 | 8.192 MHz crystal, 18 pF load (HC-49S through-hole, or 3225 SMD) | Timebase for all metering. **Must be 8.192 MHz** — the IC's internal constants depend on it. |
| C10, C11 | 27 pF, NP0/C0G | Crystal load capacitors. |
| FB1 | Ferrite bead, 600 Ω @ 100 MHz, 0805 | Isolates the analog supply from digital/Wi-Fi switching noise. |
| C7 | 10 µF X7R | Analog supply bulk. |
| C8, C9 | 100 nF X7R | Analog and digital supply decoupling. |

### Crystal load capacitor calculation

```
C_load(crystal) = 18 pF     C_stray(PCB+pins) ≈ 5 pF

C10 = C11 = 2 × C_load − 2 × C_stray = 2(18) − 2(5) = 26 pF  →  use 27 pF (E24)
```

Place the crystal **within 5 mm of pins 22/23**, with a grounded copper guard
ring around it and no signals routed underneath.

### Interface selection
Tie **USEL (pin 12) to GND** to select SPI. SPI is preferred over the UART option
because it is faster, has no baud-rate calibration issues, and shares cleanly
with the optional W25Q64 flash footprint.

### Follow the datasheet reference circuit exactly
The ATM90E26 has specific requirements for its internal voltage reference and
supply decoupling. When you draw the schematic, put the datasheet's typical
application circuit next to it and match it pin for pin. Metering ICs are much
less forgiving of "close enough" decoupling than a typical MCU — a missing
reference capacitor shows up as slow gain drift, which is exactly the kind of
bug you will not find until 500 units are in the field.

---

## 2.6 Block F — ESP32 module

| Ref | Value | Role |
|---|---|---|
| U3 | ESP32-WROOM-32E-N8 (8 MB) | MCU, Wi-Fi, TLS, buffering, cloud client. |
| R1 | 10 kΩ | EN pull-up. |
| C12 | 1 µF | EN reset delay — **required** for reliable power-on boot. |
| R2 | 10 kΩ | IO0 pull-up (normal boot). |
| SW1 | Tact switch 6 × 6 mm, IO0 → GND | Boot-mode entry during flashing; factory reset in firmware. |
| LED1 / R3 | Green LED 0805 / 1 kΩ, on IO25 | Power + heartbeat. |
| LED2 / R4 | Blue LED 0805 / 1 kΩ, on IO26 | Wi-Fi / cloud status. |
| J3 | 1 × 6 header, 2.54 mm | Programming and debug. |

### Pin assignment

| ESP32 pin | Net | Note |
|---|---|---|
| IO5 | ATM90E26 CS | Default VSPI CS |
| IO18 | ATM90E26 SCK | |
| IO19 | ATM90E26 MISO | |
| IO23 | ATM90E26 MOSI | |
| IO4 | ATM90E26 IRQ | Optional |
| IO16 | ATM90E26 ZX (zero cross) | Optional, useful for diagnostics |
| IO21 | DS3231 SDA | |
| IO22 | DS3231 SCL | |
| IO25 | LED1 (green) | |
| IO26 | LED2 (blue) | |
| IO0 | SW1 + R2 | Strapping pin — boot select |
| TXD0 / RXD0 | J3 | Programming UART |

**Strapping-pin rules — get these wrong and boards fail to boot intermittently:**
- **IO12 must not be pulled high at reset** (it selects flash voltage). Leave it
  completely unconnected.
- IO2 and IO15 are also strapping pins. Leave them unconnected, or if you must
  use them, verify the boot state.
- IO6–IO11 are connected to the module's internal flash. **Never use them.**
- IO34–IO39 are input-only. Do not drive LEDs from them.

### Programming header, and a production cost saving

```
J3:  1 → 3V3     2 → GND     3 → TXD0     4 → RXD0     5 → EN     6 → IO0
```

The usual ESP32 auto-reset circuit (two transistors and two resistors driven by
the adapter's DTR/RTS lines) is **deliberately left off the board** and built into
your programming jig instead.

- Saves 4 components × 1,000 units = 4,000 parts you never have to place.
- Saves 4 solder joints per board of technician time.
- The jig gets built once.

See [`docs/04-calibration-and-test.md`](04-calibration-and-test.md) §4.6 for the
jig circuit.

---

## 2.7 Block G — Real-time clock

| Ref | Value | Role |
|---|---|---|
| U4 | DS3231SN, SOIC-16 | ±2 ppm temperature-compensated RTC. |
| BT1 | CR2032 holder, through-hole | Backup cell holder. |
| B1 | CR2032 lithium cell | ~8 years of backup timekeeping. |
| R5, R6 | 4.7 kΩ | I²C pull-ups to 3.3 V. |
| C13 | 100 nF | Decoupling. |

> ⚠️ **Do not copy the charging circuit from the common blue DS3231 breakout
> boards.** Those modules include a diode + resistor trickle charger intended for
> a rechargeable LIR2032. If you fit a non-rechargeable **CR2032** and leave that
> charger in place, you are charging a primary lithium cell — it will vent, leak
> or rupture. Connect the CR2032 **directly** to the DS3231's VBAT pin and
> nothing else. The DS3231 handles power switchover internally.

---

## 2.8 Block H — Optional extra storage (not populated)

| Ref | Value | Role |
|---|---|---|
| U5 | W25Q64, SOIC-8 — **DNP** | Optional 8 MB log flash on the same SPI bus, with its own CS on IO15. |

Include the footprint; leave it empty. The ESP32's internal flash already gives
~6 months of one-minute records on an 8 MB module (see [`docs/01-architecture.md`](01-architecture.md)
§1.6). Populate U5 only if you later decide to keep 15-second resolution for a
full year.

---

## 3. Component values that must be confirmed on hardware

### 3.3 The two "VERIFY ON PROTOTYPE" values

| Ref | Starting value | What it sets | Confirm by |
|---|---|---|---|
| **Rb** | **10 Ω** | Current full scale (~78 A) | Drive a known current and check for clipping |
| **Rv5** | **330 Ω** | Voltage full scale (~300 V) | Sweep mains with a variac and check for clipping |

**Why this is flagged rather than fixed.** Both values depend on the ATM90E26's
full-scale differential input range at PGA = 1×. Published reference designs
using the same `SCT-013-000` clamp use a **12 Ω** burden, which implies a
full-scale range in the hundreds of millivolts — consistent with the 10 Ω
starting value above. However, I could not retrieve the exact figure from the
Microchip datasheet to state it as fact, and this number is too important to
guess at 1,000-unit scale.

**What to do — half a day of work that de-risks the whole run:**

1. Open the ATM90E26 datasheet and find the analog-input full-scale
   specification for the voltage and current channels at gain 1×.
2. Recompute `Rb` and `Rv5` from the formulas in §2.3 and §2.4.
3. Build **5 prototypes**. Fit `Rb` and `Rv5` in the primary footprints and leave
   the parallel trim footprints (`Rb2`, `Rv6`) empty.
4. Using the 10-turn calibration trick from
   [`docs/04-calibration-and-test.md`](04-calibration-and-test.md) §4.5, present
   the equivalent of **70 A** to the CT and confirm the reported current is
   linear and not clipping (check that doubling the load doubles the reading).
5. With a variac, sweep mains from 180 V to 270 V and confirm the voltage reading
   stays linear across the range.
6. **Lock both values** and order the 1,000-unit quantity.

Both trim footprints stay on the production board anyway — they cost nothing and
they let you build a 100 A variant later by changing one resistor.
