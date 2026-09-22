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
| HLW8032 (on the 5 V rail) | 3 mA | 3 mA |
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

| If the HLW8032's voltage full scale is… | Target at 300 V | Required Rv5 | Reading at 230 V |
|---|---|---|---|
| ~600 mV RMS | 500 mV | **330 Ω** | 402 mV |
| ~300 mV RMS | 250 mV | **150 Ω** | 183 mV |
| ~120 mV RMS | 100 mV | **62 Ω** | 83 mV |

**Recommended starting value: 150 Ω**, with a second parallel footprint (`Rv6`,
not populated) so you can trim on the prototypes without cutting traces.
See §3.3 — this is one of the values you must confirm on hardware.

> ⚠️ **The HLW8032's datasheet assumes a resistor divider straight from mains,
> not a transformer.** Its stated input range (85–280 VAC) refers to the mains
> voltage behind the divider it specifies, not to the signal at its pin. You must
> find the **actual pin-level full-scale voltage** in the datasheet and size
> `Rv5` from that. Do not copy a divider ratio from a shunt-based reference
> design — your signal arrives through the ZMPT101B instead, and the numbers do
> not carry over.

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
| Rb | **0.68 Ω**, 1 %, **≤ 50 ppm/°C**, 0.25 W | **Burden resistor** — converts CT secondary current to voltage. *Value to confirm — see §3.3.* |
| Rb2 | (parallel footprint, not populated) | Range trimming during prototype bring-up. |
| D2 | SMAJ5.0CA bidirectional TVS | Clamps the open-circuit spike and ESD on the CT leads. |
| Rf2, Rf3 | **1.5 kΩ**, 1 %, **matched pair** | Anti-alias, current-limit, **and CT phase compensation** — see §2.5.3. Larger than Rf1 on purpose. ⚠️ *Tune on prototype.* |
| Cf2 | 33 nF X7R (differential) | Anti-alias. Same part as Cf1 — the phase trim lives in Rf2/Rf3, not here. |
| Cf3, Cf4 | 10 nF X7R (each leg to AGND) | Common-mode filtering. **Note these add 5 nF to the differential path** — accounted for in §2.5.3. |

### The arithmetic

```
CT ratio            : 2000 : 1   (100 A primary → 50 mA secondary)
Design full scale   : 78 A primary  (63 A breaker + 24 % headroom)
Secondary at 78 A   : 78 / 2000 = 39 mA RMS

Burden voltage      : V = 39 mA × 0.68 Ω = 26.5 mV RMS
Burden dissipation  : P = (39 mA)² × 0.68 Ω = 1 mW     ← nothing ✓
Sensitivity         : 0.68 Ω / 2000 = 0.34 mV per amp
```

**Why the burden is so much smaller than you might expect.** The HLW8032's
current channel was designed for a 1 mΩ shunt carrying 20 A — that is 20 mV. Its
full-scale input is therefore only about **20–30 mV RMS**, an order of magnitude
below the ATM90E26's. The burden must be sized to match:

| If the chip's full scale is | Required Rb |
|---|---|
| 20 mV RMS | 0.51 Ω |
| **25 mV RMS** | **0.64 Ω** |
| 30 mV RMS | 0.77 Ω |

`0.68 Ω` is the nearest E24 value to the middle of that range. **Confirm the real
figure from the datasheet before ordering 1,000 of them — see §3.3.**

One genuine silver lining: a lower burden loads the CT less, which *reduces* its
phase error and improves its linearity. Some of what you lose in signal level you
get back in sensor behaviour.

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

### Getting this value right matters more than it did before

With the ATM90E26 there was a safety net: if the burden turned out too small, you
raised the chip's programmable gain in firmware and recovered the resolution.

**The HLW8032 has no programmable gain.** What the burden resistor gives the chip
is what the chip gets. That makes `Rb` a one-shot decision:

- **Too large** → a 60 A load clips the ADC. The reading is silently wrong and no
  firmware can fix it. You would unsolder 1,000 resistors.
- **Too small** → every reading is noisier and the low-load floor gets worse, and
  again no firmware can fix it.

The signal levels here are genuinely small. At the 250 W night standby of a
typical home (1.45 A), the burden produces about **0.5 mV**. That is still
comfortably above the chip's ~50 µV floor, but it means the CT input layout in
[`docs/05-layout-and-enclosure.md`](05-layout-and-enclosure.md) §5.4 —
short, tight, symmetrical differential traces on a clean analog ground — is no
longer a nicety. It is load-bearing.

> **Build 5 prototypes and sweep this value before committing.** The parallel
> trim footprint `Rb2` exists exactly for that.

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

## 2.5 Block E — Metering IC (HLW8032)

> **v1 baseline.** The ATM90E26 design this replaced is preserved in
> [`docs/08-v2-upgrade-path.md`](08-v2-upgrade-path.md). Read that before
> starting v2.

```
                        ┌──────────────────────┐
     5V ──────────┬─────┤ VDD (5 V)            │
                  │     │                      │      Rls1 1k
                C7 10uF │                 TX   ├────[1k]──┬──► ESP32 IO16 (RX2)
                C8 100nF│  (4800 baud, 8N1,    │          │
                  │     │   transmit only)     │        Rls2 2k
                AGND    │                      │          │
                        │                 PF   ├──►       │
      V sense ─────────►│ V channel   (energy  │  (opt)  AGND
      CT + ────────────►│ I channel    pulse)  │
      CT - ────────────►│                      │
                        │   internal 3.579 MHz │
                        │   NO CRYSTAL NEEDED  │
                        └──────────────────────┘
```

| Ref | Value | Role |
|---|---|---|
| U2 | **HLW8032, SOP-8 (1.27 mm pitch)** | The measurement engine. |
| C7 | 10 uF X7R, 0805 | 5 V supply bulk for the analog section. |
| C8 | 100 nF X7R, 0805 | Supply decoupling, hard against the pin. |
| Rls1 | 1 kOhm, 0805 | Level shifter, series element. |
| Rls2 | 2 kOhm, 0805 | Level shifter, shunt element. |

### Why this chip (and what it costs you)

Chosen for **v1** because at 1.27 mm pitch and 8 pins it is trivially
hand-solderable, it has ~32,000 pieces in stock at ~US$ 0.27 (versus ~230 pieces
of the ATM90E26), and it needs no external crystal. See
[`docs/01-architecture.md`](01-architecture.md) §1.4 for the full reasoning.

What you give up, stated plainly:

| | ATM90E26 | **HLW8032** |
|---|---|---|
| Dynamic range | 5000 : 1 | **~400 : 1** |
| Smallest reliable load (78 A full scale) | 4 W | **45 W** |
| Phase compensation | register | **none — fixed in hardware, see §2.5.3** |
| Calibration | written into the chip | **all in ESP32 firmware** |
| Datasheet | English | **largely Chinese** |

The dynamic range is the one that actually bites. Your product spec must say
**"accurate above 50 W"**, and that is now a hard floor rather than a comfortable
margin.

### 2.5.1 It only talks — it never listens

The HLW8032 has no configuration. It continuously broadcasts a **24-byte packet
at 4800 baud, 8N1**, containing voltage, current, power, a power-factor/energy
pulse counter and a checksum. There is no way to write anything to it.

Consequences for the design:

- **All calibration happens in ESP32 firmware**, as scaling constants stored in
  NVS. See [`docs/04-calibration-and-test.md`](04-calibration-and-test.md).
- **Always validate the checksum** before using a packet. At 4800 baud in an
  electrically noisy panel you will get corrupted frames, and a corrupted power
  value silently poisons the customer's energy total. Discard and wait for the
  next packet — one arrives roughly every 50 ms, so dropping bad frames costs
  nothing.
- Only one wire is needed: the chip's TX to an ESP32 RX pin.

### 2.5.2 The 5 V level shifter (do not skip this)

The HLW8032 runs on **5 V**, so its TX pin idles at 5 V. **ESP32 GPIOs are not
5 V tolerant.** Connecting them directly will damage the ESP32, possibly not
immediately, which is worse.

A two-resistor divider is all that is required:

```
HLW8032 TX ──[Rls1 1k]──┬──► ESP32 RX
                        │
                    [Rls2 2k]
                        │
                       GND

  V_esp = 5 V x 2k / (1k + 2k) = 3.33 V   ✓
```

No level shifting is needed in the other direction, because there is no other
direction.

### 2.5.3 Hardware phase compensation (replaces the ATM90E26's phase register)

A current transformer shifts the current waveform in time by roughly 1.5 degrees
relative to the true current. At 50 Hz, **1 degree is 55.6 microseconds**. The
ATM90E26 cancelled this with a register. The HLW8032 has no register, so we
cancel it with the **anti-alias filter that is already on the board**.

#### The two channels are not symmetrical

The voltage channel is **single-ended**: `Rf1` in series, `Cf1` to AGND.

```
tau_V = Rf1 x Cf1 = 1 kOhm x 33 nF = 33 us   ->  lag = 0.594 deg
```

The current channel is **differential**: `Rf2` and `Rf3` in series on each leg,
`Cf2` across the pair, `Cf3`/`Cf4` from each leg to AGND. In differential mode
the series resistance is `Rf2 + Rf3`, and `Cf3`/`Cf4` sit in series with each
other, adding `Cf3 / 2` to the differential capacitance:

```
R_eff = Rf2 + Rf3
C_eff = Cf2 + Cf3/2 = 33 nF + 5 nF = 38 nF
tau_I = R_eff x C_eff
```

> **This asymmetry is easy to miss and it matters.** With `Rf2 = Rf3 = 1 kOhm`
> the current channel already lags 1.368 deg against the voltage channel's
> 0.594 deg — so **+0.774 deg of compensation is built in before you tune
> anything.**

#### Tune with the resistor, not the capacitor

To compensate a CT phase lead of `d` degrees, make the current channel lag by
`0.594 + d` degrees and solve for `Rf2 = Rf3`:

| CT phase error | Needed lag | Exact Rf2/Rf3 | **Use (E24)** | Residual | Current-channel corner |
|---|---|---|---|---|---|
| 0.0 deg | 0.59 | 434 Ω | **430 Ω** | +0.01 deg | 4,870 Hz |
| 0.5 deg | 1.09 | 800 Ω | **820 Ω** | −0.03 deg | 2,554 Hz |
| 1.0 deg | 1.59 | 1,165 Ω | **1.2 kΩ** | −0.05 deg | 1,745 Hz |
| **1.5 deg (typical)** | **2.09** | **1,531 Ω** | **1.5 kΩ** | **+0.04 deg** | 1,396 Hz |
| 2.0 deg | 2.59 | 1,897 Ω | **1.8 kΩ** | +0.13 deg | 1,163 Hz |
| 2.5 deg | 3.09 | 2,264 Ω | **2.2 kΩ** | +0.09 deg | 952 Hz |
| 3.0 deg | 3.59 | 2,631 Ω | **2.7 kΩ** | −0.09 deg | 776 Hz |

**Start at 1.5 kΩ** and tune on the prototypes — procedure in
[`docs/04-calibration-and-test.md`](04-calibration-and-test.md) §4.5(c).

#### Why the resistor and not the capacitor

1. **A 120 nF C0G/NP0 capacitor does not exist in 0805.** C0G tops out around
   10–22 nF in that package; 120 nF C0G needs a 1210 and is rare and expensive.
   An earlier revision of this document specified one. It was not a buildable
   part.
2. **Resistors are far more stable than ceramics.** A 1 % thin-film resistor at
   100 ppm/°C holds the phase angle over temperature. An X7R capacitor is ±10 %
   with a large temperature coefficient, which would move the compensation by
   ±0.2–0.3 degrees in service.
3. **Resistors exist in every E24 value**, so you can hit the target closely.
4. **Tuning means swapping one value.** `Rf2` and `Rf3` stay a matched pair —
   change both together, always.

Because you tune empirically on real hardware, the capacitors' absolute
tolerance barely matters: whatever `Cf2` actually is, the resistor value you land
on absorbs it. **What matters is consistency** — buy `Cf1`–`Cf4` from one reel
for the production run, and re-verify if you change capacitor supplier.

#### Caveats

- The larger resistors drop the current-channel anti-alias corner to ~1.4 kHz
  (from 4.9 kHz). Fine for 50 Hz energy; it softens harmonics above the 28th.
- **Do not go much above ~2.2 kΩ** without checking the HLW8032's recommended
  source impedance. Its switched-capacitor ADC inputs draw small charging
  pulses, and too high a series resistance causes settling errors. If your CT
  needs more than ~2.5 degrees of correction, raise `Cf2` to 47 nF instead and
  re-solve, keeping the resistors low.
- This is a **fixed** correction tuned to one CT model. **Change clamp supplier,
  re-tune and re-qualify.** Write that into your purchasing rules.

### 2.5.4 Pinout — read it off the datasheet, do not guess

The HLW8032 is an 8-pin device carrying: 5 V supply, ground, the differential
current-channel inputs, the voltage-channel input, the UART TX output, and an
energy pulse output. **Map these to actual pin numbers from the Hiliwei
HLW8032 user manual (Rev 1.5) when you draw the schematic** — the pin order is
not something to take from any secondary source, including this document.

Follow the datasheet's typical application circuit for supply decoupling and
input filtering exactly. Metering ICs are far less forgiving of approximate
decoupling than an MCU, and the failure mode is slow gain drift that you will
not find until hundreds of units are in the field.

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
| **IO16 (UART2 RX)** | **HLW8032 TX**, via the 1k/2k divider | **The only metering connection.** See the warning below. |
| IO17 (UART2 TX) | *unused* | The HLW8032 cannot receive. Leave free. |
| IO4 | HLW8032 PF (energy pulse) | Optional — a cross-check on the UART energy counter |
| IO5, IO18, IO19, IO23 | *free* (VSPI) | No longer needed for metering. Reserved for the optional W25Q64 footprint. |
| IO21 | DS3231 SDA | |
| IO22 | DS3231 SCL | |
| IO25 | LED1 (green) | |
| IO26 | LED2 (blue) | |
| IO0 | SW1 + R2 | Strapping pin — boot select |
| TXD0 / RXD0 | J3 | Programming UART |

> ⚠️ **Use UART2 (IO16/IO17) for the meter, never UART0.** UART0 is the
> programming and debug port at J3. If the HLW8032 is streaming 24-byte packets
> into it every 50 ms, you cannot flash the board and you cannot read a debug
> log. This costs nothing to get right now and is painful to discover later.

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
| **Rb** | **0.68 Ω** | Current full scale (~78 A) | Drive a known current and check for clipping |
| **Rv5** | **150 Ω** | Voltage full scale (~300 V) | Sweep mains with a variac and check for clipping |
| **Rf2, Rf3** | **1.5 kΩ** (matched pair) | CT phase compensation | Resistive load; tune until PF reads 1.000 (§4.5c) |

**Why these are flagged rather than fixed.** `Rb` and `Rv5` depend on the
HLW8032's full-scale analog input range, which its datasheet expresses in terms
of a shunt resistor and a mains divider rather than as a pin-level voltage. The
starting values above are derived from the published shunt configurations
(1 mΩ at 20 A → ~20 mV; 3 mΩ at 10 A → ~30 mV), which is sound reasoning but is
*inference*, not a quoted specification. At 1,000-unit scale that is not good
enough. `Rf2`/`Rf3` depend on your specific CT's phase error, which varies by
supplier and cannot be known in advance at all.

**What to do — half a day of work that de-risks the whole run:**

1. Open the **Hiliwei HLW8032 user manual (Rev 1.5)** and find the analog-input
   full-scale figures for the current and voltage channels, expressed at the pin.
   Translate the relevant pages if needed — this is the one part of the Chinese
   datasheet you cannot skip.
2. Recompute `Rb` and `Rv5` from the formulas in §2.3 and §2.4.
3. Build **5 prototypes**. Fit `Rb`, `Rv5` and `Rf2`/`Rf3` at their starting
   values and leave the parallel trim footprints (`Rb2`, `Rv6`) empty.
4. Using the 10-turn calibration trick from
   [`docs/04-calibration-and-test.md`](04-calibration-and-test.md) §4.5, present
   the equivalent of **70 A** to the CT and confirm the reported current is
   linear and not clipping (check that doubling the load doubles the reading).
5. Check the **other end** too: confirm a ~200 W load still reads sensibly. The
   HLW8032's ~400:1 dynamic range makes the low end the real risk, not the top.
6. With a variac, sweep mains from 180 V to 270 V and confirm the voltage reading
   stays linear across the range.
7. Tune `Rf2`/`Rf3` on a resistive load until the computed power factor reads
   1.000 (§4.5c), then fix that value for the run. **Change both together — they
   must stay matched.**
8. **Lock all three values** and order the 1,000-unit quantity.

The trim footprints stay on the production board anyway — they cost nothing and
they let you build a 100 A variant later by changing one resistor.
