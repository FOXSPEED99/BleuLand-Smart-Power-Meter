# 1. Architecture and Rationale

This document explains *what* the design is and, more importantly, *why*. Every
significant choice is written as a decision with the alternatives that were
rejected, so you can re-open any of them later with full context.

---

## 1.1 The constraints we are designing against

From your brief and the follow-up answers:

| Constraint | Consequence for the design |
|---|---|
| Non-invasive — house current must not pass through the board | Current is sensed with a split-core clamp (CT). No shunt, no relay, no load terminals. |
| One channel only | Single current input. No multi-channel front end. |
| As small as possible, hidden in the breaker board | Two-layer board ~50 × 45 mm; magnetics chosen for small footprint. |
| "Accurate as best as possible" | True power measurement (voltage **and** current), dedicated metering IC, per-unit calibration. |
| Grid mains only, 230 V / 50 Hz | No need for wide-frequency tracking or inverter-waveform handling. Simplifies the front end. |
| 63 A maximum main breaker | CT and burden sized for ~78 A full scale (24 % headroom). |
| Cloud + on-board buffering | Needs non-volatile storage and a real-time clock that survives power cuts. |
| Dedicated metering IC | Rules out MCU-ADC sampling. |
| PCB antenna, plastic 3D-printed enclosure | ESP32 module with integrated antenna; strict antenna keep-out in layout. |
| Buy locally first, import from China otherwise | BOM built from parts that exist in Middle-East markets, with LCSC part numbers as the import fallback. |
| Hand assembly, soldering iron only, no hidden pads | No QFN, no BGA, no leadless parts. Minimum pitch 0.65 mm. Reflow-compatible footprints so you can switch to stencil + hotplate later. |
| L and N both available at the install point | We can power from L-N and measure true voltage from the same pair. |

---

## 1.2 Decision 1 — Measure **real power**, not just current

### The choice
Sense both mains **voltage** and **current**, and compute real power
`P = (1/T)·∫ v(t)·i(t) dt`. The alternative was to sense only current and
multiply by an assumed 230 V.

### Why

Two independent errors make the current-only approach unusable for billing:

**a) Power factor.** Real power is `P = V · I · cos φ`. A house full of motors —
fridge, freezer, washing machine, water pump, air conditioner — runs at a power
factor around 0.7–0.85. Current-only monitoring reports apparent power (VA), not
watts, so it would over-report the bill by **15–40 %**. The customer's utility
meter charges for watt-hours. If your app and their bill disagree by 30 %, your
product is worthless to them.

**b) Voltage variation.** Syrian distribution voltage is not a stable 230 V. If
the real voltage is 200 V and you assume 230 V, you are **15 % wrong** before you
even start. Power scales with voltage, so this error goes straight into the kWh
total.

Measuring voltage costs one small transformer and four resistors. It is the
single highest-value decision in this design.

### Bonus
Once you measure voltage you get, for free: real-time mains voltage (a feature
customers in Syria genuinely care about), power factor, and sag/brownout
detection. All of these become app features at zero extra hardware cost.

*(The HLW8032 reports voltage, current, active power, apparent power and power
factor. It does not report line frequency — the ATM90E26 did. Since you are
grid-only at a stable 50 Hz, this costs you a nice-to-have diagnostic rather
than a feature. Confirm against the datasheet before promising it in the app.)*

---

## 1.3 Decision 2 — Fully **isolated** low-voltage section

### The choice
An isolated AC-DC power module (transformer-based) **and** an isolated voltage
sensor (a voltage transformer), so that the entire ESP32 / metering-IC section
sits at safe, touchable SELV potential — not at mains potential.

The rejected alternative is the way almost every cheap Tuya/Sonoff-class device
does it: tie the board ground to mains neutral, sense voltage with a plain
resistor divider, and power the board from a non-isolated capacitive dropper or
a non-isolated buck. That is smaller and about US$ 2 cheaper per unit.

### Why isolation is worth US$ 2 to you specifically

1. **You are hand-building 1,000+ units and testing them yourselves.** On a
   non-isolated board, connecting a USB-serial adapter to a mains-powered unit
   puts mains voltage on your laptop's USB ground. That kills laptops and, much
   worse, people. With an isolated design, your technician can plug in a USB-TTL
   adapter on a live, running unit with no risk. Over 1,000 units, that is
   hundreds of safe debug and calibration operations instead of hundreds of
   dangerous ones.

2. **Earthing in many Syrian homes is poor or absent, and L/N are frequently
   swapped in the distribution board.** A neutral-referenced board is only "near
   earth potential" if the installation is correct. If L and N are reversed —
   very common — the entire board floats at 230 V. With isolation, a wiring
   mistake is harmless.

3. **The CT lead is a 1-metre wire hanging inside the panel.** On an isolated
   board, that lead can never become live. On a non-isolated board, the burden
   resistor is referenced to a board ground that may be at mains potential.

4. **Liability.** You are a company selling a product that a homeowner or a local
   electrician will install inside their own panel. Isolation is the difference
   between a defensible product and an unacceptable one.

### What it costs
Two magnetic components instead of none: the **HLK-PM01** AC-DC module
(34 × 20 × 15 mm, ~US$ 1.80) and the **ZMPT101B** voltage transformer
(~20 × 20 mm, ~US$ 0.90). Board grows by roughly 15 mm in one dimension. Both
parts are through-hole, which is *easier* to hand-solder, not harder.

> **This is the decision I would most defend.** If you later decide the extra
> US$ 2.70 and 15 mm are unacceptable, the change is contained: swap HLK-PM01 for
> a non-isolated buck, replace the ZMPT101B with a resistor divider, tie ground
> to N, and re-do the layout without the isolation slot. But then you must build
> a bench isolation transformer into your production test process, without
> exception.

---

## 1.4 Decision 3 — **HLW8032** for v1, ATM90E26 held for v2

This decision was reopened after the first draft, and the reversal is
deliberate. The reasoning is worth keeping because it is a good example of
letting a real constraint beat a spec sheet.

### The shortlist

Your "no hidden pads" rule eliminates most modern metering ICs immediately.

| Candidate | Package | Pitch | Verdict |
|---|---|---|---|
| **HLW8032** | **SOP-8** | **1.27 mm** | **CHOSEN for v1.** 8 pins at twice the pitch of anything else on the list — genuinely easy by hand. ~US$ 0.27 with ~32,000 in stock. Internal 3.579 MHz oscillator, so no crystal. Runs on 5 V, UART broadcast only. |
| ATM90E26-YU-R | SSOP-28 | 0.65 mm | **Held for v2.** Technically the best fit: 0.1 % class, 5000:1 dynamic range, **phase-compensation register**, current-channel PGA, English datasheet. But ~230 pieces in stock against a 1,000-unit need, and 28 fine-pitch pins. See [§8](08-v2-upgrade-path.md). |
| BL0942 | TSSOP-14 / SSOP-10 | 0.65 mm | Rejected for v1. Fewer pins than the ATM90E26 but **the same pitch** — it does not solve the soldering constraint, only halves the exposure. Worth revisiting for v2 if it turns out to have a phase register. |
| BL0940 | TSSOP-14 | 0.65 mm | Same objection as BL0942. |
| CS5490 | SOIC-16 | 1.27 mm | Nice package, but ~US$ 4.75 and out of stock. Rejected on price and supply. |
| ADE7953 | LFCSP-28 | — | **Rejected outright.** Leadless with an exposed thermal pad — exactly the part type you asked us to avoid. Unbuildable with your equipment. |
| ADE7753 | SSOP-20 | 0.65 mm | Viable but older, pricier, thinner supply. |
| ESP32 internal ADC | — | — | Rejected. Noisy, non-linear, temperature-sensitive; 1 % from it is a research project, not a product. |

### Why the easier chip won

The ATM90E26 is the better chip. It is not the better *decision* for a first
production run, for four reasons:

1. **Supply.** ~230 pieces in stock against a 1,000-unit need was the single
   biggest risk in the original design. The HLW8032 has ~32,000. That risk
   simply disappears.
2. **Assembly yield.** 28 pins at 0.65 mm, hand-soldered 1,000 times by several
   people of varying skill, was the most likely defect on the board. 8 pins at
   1.27 mm is not a risk at all.
3. **The accuracy gap is small, and smaller than the error you already have.**
   Modelled over a realistic household day (see [§4.1](04-calibration-and-test.md)):

   | | kWh/day on a true 25.10 | Error |
   |---|---|---|
   | ATM90E26 | 25.15 | +0.19 % |
   | HLW8032, no phase fix | 25.45 | +1.40 % |
   | **HLW8032 + phase-trimmed filter** | **25.22** | **+0.48 %** |

   Meanwhile the **unit-to-unit spread caused by the clamp is ±1.6 %** — larger
   than the entire gap between the chips, and identical for both because they
   share the same front end.
4. **Cost.** US$ 0.27 against US$ 1.32, and the crystal and its two load
   capacitors come off the board too. About US$ 1.15 per unit, US$ 1,150 across
   the run.

### What you are actually giving up

Be honest about this in your product spec — it is not nothing:

| | ATM90E26 | HLW8032 |
|---|---|---|
| Dynamic range | 5000 : 1 | **400 : 1** |
| Smallest reliable load | 4 W | **45 W** |
| Phase correction | register, per unit | fixed capacitor, per batch |
| Calibration | into the chip | ESP32 firmware only |
| Datasheet | English | **largely Chinese** |
| Interface | SPI, bidirectional | UART, **transmit only** |

**The dynamic range is the real cost, not the phase error.** A house spends most
of the night between 200 and 400 W, which is close to the HLW8032's floor. Your
marketing must say **"accurate above 50 W"** and mean it.

### The phase problem, and the capacitor that solves it

A current transformer shifts the current waveform by roughly 1.5° relative to
the true current — at 50 Hz that is **83 microseconds**. Because real power is
`V × I × cos(φ)`, this costs almost nothing on resistive loads (you are at the
flat top of the cosine curve) and about 2 % on a PF-0.8 motor load (you are on
the steep part).

The ATM90E26 cancels it with a register. The HLW8032 has no registers at all —
it only broadcasts. So we cancel it in hardware instead, by making the
current-channel anti-alias capacitor larger than the voltage channel's, which
makes the current signal lag by exactly enough to compensate. **One capacitor,
`Rf2`/`Rf3`, typically 1.5 kΩ.** Details and the tuning procedure are in
[`docs/02-circuit.md`](02-circuit.md) §2.5.3.

### The v1 → v2 strategy

v1 ships with the HLW8032 and is hand-assembled. If the product succeeds, v2
moves to machine assembly, at which point "easy to solder" stops being a
constraint and the ATM90E26 becomes available again at no assembly cost.

To keep that door open, four things must be true from **day one** — all of them
free, all of them painful to retrofit:

- **Log raw `V`, `I` and `P` to your server, not just kWh.** Then a v1 and a v2
  unit on the same house can be compared directly.
- **Carry a `hardware_revision` field in the database from the first record.**
- **Keep calibration constants in NVS, never hard-coded.**
- **Keep the CT, burden and voltage front end architecturally the same**, so
  calibration procedure and installer training transfer unchanged.

---

## 1.5 Decision 4 — **ESP32-WROOM-32E** as MCU + radio

### Why this module
- **Castellated edge pads** — the easiest surface-mount part on the whole board
  to hand-solder, and it reflows perfectly if you move to a hotplate.
- Integrated, certified PCB antenna — matches your choice of a plastic enclosure.
- Hardware AES/SHA acceleration, so **TLS to your cloud is fast and does not
  starve RAM**. This is the reason not to use an ESP8266.
- Flash is large enough for OTA plus a long offline buffer (see §1.6).
- Universally available, including in Middle-East markets, and cheap (~US$ 2.20).

### The one clever detail: `WROOM-32E` vs `WROOM-32UE`
These two modules are **pin- and footprint-identical**. The `-UE` variant
replaces the PCB antenna with a u.FL connector for an external antenna.

You told us the enclosure is plastic and the router is close, so the standard
`-32E` is right. But **lay the board out once and you get both options for
free**: if you later find a customer whose *distribution board* is metal (the
plastic inner box does not help there), you fit a `-32UE` plus a US$ 0.80 pigtail
antenna on that unit only. No PCB revision, no second design. Reserve the antenna
keep-out area either way.

---

## 1.6 Decision 5 — Buffering and timekeeping

You chose "cloud + on-board buffering", which needs two things the naive design
forgets: **somewhere to put the data** and **a trustworthy clock**.

### Storage: use the ESP32's own flash, not an extra chip

| | |
|---|---|
| Record size | ~16 bytes (timestamp, Vrms, Irms, P, energy delta, flags) |
| Rate | 1 record / minute |
| Daily volume | 23 KB |
| Partition | ~4 MB of an **8 MB** module, after reserving two OTA app partitions |
| Retention | **~6 months offline** before the oldest data is overwritten |

**Why 8 MB and not 4 MB.** Over-the-air updates are mandatory for 1,000 units
sealed inside people's breaker panels, and OTA needs *two* application partitions
so a failed update can roll back. On a 4 MB module that leaves only ~0.95 MB for
data — still a respectable 41 days of buffer, but no headroom as the firmware
grows. The 8 MB part costs about US$ 0.30 more and removes the constraint
permanently. See [risks §6.11](06-risks-and-decisions.md).

Flash wear is a non-issue either way: a 4 MB ring buffer is ~1,000 sectors of
4 KB, each erased roughly once every 6 months, so 100,000 erase cycles is longer
than the universe will plausibly care about. No external flash chip is needed.
That removes a part, a footprint and a failure mode.

An optional `W25Q64` SOIC-8 footprint is included but **not populated** — fit it
only if you later want 15-second resolution kept for a year.

### Clock: a real RTC, not just NTP

The failure case that matters is: *mains returns after a cut, but the internet
does not.* The device is now measuring, but has no idea what time it is, so every
buffered record is untrustworthy — and untrustworthy timestamps mean you cannot
bill from them.

A **DS3231** (I²C, ±2 ppm TCXO, CR2032 backup, ~US$ 1.50, SOIC-16 and easy to
solder) makes time survive any outage. It costs about 1 % of the BOM and removes
an entire class of data-integrity bugs.

- Firmware rule: RTC is the source of truth; NTP corrects it whenever the
  internet is available; every buffered record carries a "time was RTC-only"
  flag so your server can weight it.

---

## 1.7 Decision 6 — Current sensing details

- **Sensor:** split-core CT, 100 A : 50 mA (2000:1 turns), e.g. YHDC
  `SCT-013-000`, 13 mm window. This is the single most widely available clamp in
  the world and clones are everywhere.
- **Why the 100 A / 50 mA "current output" version and not the 60 A / 1 V
  "voltage output" version:** the voltage-output versions have the burden
  resistor moulded inside, which is safer but locks you to their range and their
  resistor's tolerance and temperature coefficient. With the current-output
  version, **your** burden resistor sets the range — so you can pick a precise,
  low-drift resistor, and you can change the measurement range later by changing
  one component instead of the whole clamp.
- **Range:** sized so that ~78 A is full scale. Your breaker is 63 A, so you have
  24 % headroom for motor inrush and for the customer who upgrades their main.
- **Safety:** the burden resistor is permanently soldered on the board, so the CT
  is never open-circuit while connected. A bidirectional TVS across the input
  clamps the spike if the lead is ever pulled while the clamp is on a live cable.

---

## 1.8 What Phase 1 deliberately leaves out

| Not included | Why | Where it belongs |
|---|---|---|
| Relay / load disconnect | Your brief says non-invasive monitoring; a relay would put house current through the product | Never, for this product |
| Second CT channel | You asked for one channel | A future "Pro" variant |
| Local display | Adds cost, size and an enclosure window; the app is the UI | Optional future variant |
| Bidirectional / solar export | You answered "grid mains only" | Firmware-only change later — the hardware already supports it (see §6.7) |
| CE / EMC certification | Out of scope for Phase 1 | Before export sales |
| The mobile / web app | Explicitly out of scope | Phase 2 |

---

## 1.9 What this hardware makes possible for the Phase 2 app

Without any hardware change, the board can report, per minute:

`timestamp · Vrms · Irms · active power (W) · apparent power (VA) · power factor
· cumulative energy (Wh) · signal quality flags · hardware_revision`

That is enough for: live consumption, daily/weekly/monthly kWh, bill estimation
at a user-entered price per kWh, voltage-quality history and brownout alerts,
"which day was most expensive", and anomaly detection.

Two rules for the Phase 2 backend, both of which are much cheaper to honour now
than to retrofit:

1. **Bill from the accumulated energy counter, not from the sum of power
   samples.** The counter cannot lose energy during a network stall; a sum of
   samples can.
2. **Store `hardware_revision` on every record, and store raw `V`, `I`, `P`
   alongside the kWh.** When the v2 board arrives you will want to put an old
   and a new unit on the same house and compare them directly. Adding this field
   after 500 units are deployed is miserable; adding it now is free.
