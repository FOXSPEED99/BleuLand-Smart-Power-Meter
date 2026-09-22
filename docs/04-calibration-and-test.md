# 4. Calibration, Test and Production Quality

You are hand-building 1,000+ units of a device that people will use to check
their electricity bill. The difference between a product and a pile of boards is
everything in this document.

---

## 4.1 Where the error actually comes from

Before designing a test process, know what you are fighting. Here is the error
budget for one unit:

| Error source | Typical size | Can you calibrate it out? |
|---|---|---|
| **CT amplitude accuracy** (`SCT-013` class) | ±1–3 % | Gain error yes, at one point. **Non-linearity, no.** |
| **CT phase error** | 0.5–3° | Yes — ATM90E26 phase-compensation register |
| Burden resistor tolerance | ±1 % | Yes |
| **Burden resistor temperature drift** | ±0.2 % over 40 °C (at 50 ppm/°C) | **No.** This is why the tempco spec matters. |
| ZMPT101B turns-ratio tolerance | ±1 % | Yes |
| ZMPT101B phase shift | 1–2° | Yes |
| Rv1–Rv4 combined tolerance | ±0.5 % | Yes |
| ATM90E26 itself | ±0.1 % | Not needed |
| **Realistic total after per-unit calibration** | **±1 % above 10 % of range** | |

Two conclusions fall straight out of this table:

1. **The clamp dominates.** A 0.1 %-class metering IC behind a ±3 % clamp gives
   you a ±3 % product. Spend your accuracy budget on the CT, not the IC.
2. **Per-unit calibration is not optional.** Without it you are stacking ±1 % CT,
   ±1 % burden, ±1 % transformer and ±0.5 % resistors — worst case around ±3.5 %
   before the customer even switches a light on.

---

## 4.2 Stage 1 — Bare-board inspection (before any power)

Do this on **every** unit. It takes about 90 seconds.

1. **Visual, under magnification.** Solder bridges, especially:
   - the ATM90E26's 0.65 mm pins,
   - the ESP32 module's castellated pads,
   - the DS3231's SOIC-16 pins.
2. **Polarity check.** C2, C4 (electrolytics), D1, D2, D3, both LEDs, U2, U3, U4.
   A reversed 470 µF electrolytic on a mains-powered board is a small explosion.
3. **Rail short test.** Multimeter in resistance mode:
   - 3V3 to GND — must **not** be a dead short. Expect a reading that climbs as
     the capacitors charge, settling above ~10 kΩ.
   - 5 V to GND — same.
4. **⭐ Isolation test — the single most important check.**
   Short J1's two pins together. Measure between that point and the SELV ground.
   - With a multimeter: must read open circuit (> 20 MΩ).
   - **Much better: with a 500 V insulation tester.** Must read > 20 MΩ at 500 V.
     A multimeter at 9 V will not find a contaminated or nearly-bridged barrier;
     500 V will.
   - **Any unit that fails this test does not get powered up. Ever.** Clean it,
     re-inspect, re-test, or scrap it.
5. **Barrier inspection.** Look along the routed isolation slot. No solder balls,
   no flux residue bridging it, no component lead bent across it.

> Record the result for every serial number. When a unit comes back from the
> field in two years, you want to know it passed.

---

## 4.3 Stage 2 — SELV bring-up (mains **not** connected)

This is where the isolated design pays for itself: you can do all of this safely
at a normal bench with a USB cable.

6. Power the board from the programming jig's 3.3 V. **Do not connect mains.**
7. Flash the firmware over J3. The jig handles the auto-reset (see §4.6).
8. Run the **firmware self-test**, which should check and print:

   | Check | Proves |
   |---|---|
   | Read ATM90E26 SysStatus + a known-value register | SPI wiring, IC alive, **crystal oscillating** |
   | Write then read back a scratch register | Bidirectional SPI |
   | DS3231 responds at I²C address 0x68, time is sane | RTC + pull-ups |
   | DS3231 "oscillator stopped" flag | Coin cell is fitted and good |
   | Mount the data partition, write and read a record | Flash partition |
   | Wi-Fi scan finds ≥ 1 access point | Radio + antenna |
   | Blink both LEDs | LEDs and their resistors |
   | Read the button | SW1 |

9. Print a single `PASS` / `FAIL: <which check>` line. Your technician needs one
   line, not a log.

---

## 4.4 Stage 3 — Mains-powered functional test

> **Bench safety.** Power the units under test through an **isolation
> transformer** and an **RCD/GFCI**. The board is isolated; your test setup and
> your hands are not. This is a hard rule for a workshop building 1,000 units.

10. Connect L and N. Confirm LED1 lights.
11. Measure the 5 V rail (expect 4.9–5.2 V) and the 3.3 V rail (3.25–3.35 V).
12. Read `Vrms` from the device and compare against a reference true-RMS
    multimeter on the same mains. Before calibration, expect within ±5 %. A
    reading that is wildly wrong, or zero, means a ZMPT101B or Rv5 problem.
13. Check that reported line frequency reads 49–51 Hz. If it reads 0 or garbage,
    the voltage channel is not seeing a clean sine wave.

---

## 4.5 Stage 4 — Calibration (the part that makes it a product)

Four things get calibrated per unit, in this order.

### (a) Voltage gain

1. Apply mains. Measure the true voltage with your reference DMM at the terminal
   block.
2. Read the device's `Vrms`.
3. ```
   Ugain_new = Ugain_current × (V_reference / V_device)
   ```
4. Write `Ugain`, re-read, confirm within ±0.3 %.

### (b) Current gain — and the trick that makes this practical

The obvious approach is to run a big known load and clamp the CT on its cable.
For a meaningful calibration you want 10–20 A, which means a 2–4 kW heater: hot,
slow, expensive to run, and awkward to do 1,000 times.

> **⭐ The 10-turn trick.** A current transformer measures *ampere-turns*. If you
> pass the load cable through the clamp's window **10 times** instead of once,
> the CT sees exactly 10× the current.
>
> So a **1 A** load (a 230 W lamp) presents itself as **10 A**. A 2 A load looks
> like 20 A. You calibrate at a realistic operating current using a small, cool,
> cheap, safe load.

Build a permanent calibration loop: a short length of flexible cable wound 10
turns through a fixed clamp position, terminated in a socket for your reference
load. Mark the turn count on the jig — an error here is a 10× calibration error.

1. Switch on the known load.
2. Measure true current with a reference clamp meter **on the single-turn part**
   of the cable.
3. Effective current at the CT = measured × 10.
4. ```
   Igain_new = Igain_current × (I_effective / I_device)
   ```
5. Verify linearity with a second point (e.g. 0.5 A → 5 A effective and 2 A →
   20 A effective). The two points should agree within 1 %. If they do not, the
   clamp is non-linear or something is clipping — go back to
   [circuit §3.3](02-circuit.md).

### (c) Phase compensation

With a **purely resistive** load (incandescent lamps or a heater — *not* an LED
lamp or a switch-mode supply, which are non-linear), the true power factor is
1.000.

1. Read the device's power factor.
2. Adjust the ATM90E26's phase-compensation register until PF ≥ 0.999.
3. Do this at the same current used for gain calibration.

This corrects the combined phase error of the CT and the ZMPT101B. Skipping it
costs you roughly 1.4 % error on a PF-0.8 motor load for every 1° of uncorrected
phase shift — and Syrian homes are full of motors.

### (d) No-load threshold — the one that protects your billing

With the CT connected but clamped around nothing, the device should report
**exactly zero**, not 0.8 W of noise.

> Why this matters more than it looks: 2 W of phantom reading × 24 h × 30 days =
> **1.4 kWh per month of consumption that does not exist**. Multiply by your
> price per kWh and you have a customer complaint every single month, on every
> single unit.

1. Record the reported power with no current.
2. Set a firmware start-up threshold slightly above the noise floor — typically
   **5 W**. Below it, report and accumulate exactly zero.
3. Document the threshold in your product specification: *"accurate above 50 W;
   loads below 5 W are not counted."* Honesty here prevents support tickets.

### (e) Store and back up the constants

- Write `Ugain`, `Igain`, the phase register and the no-load threshold to the
  ESP32's NVS, keyed to the module's MAC address.
- **Also upload them to your server.** If a board's flash is ever erased, or you
  replace a unit, you can re-provision it without repeating the calibration.
- ⚠️ **Checksum registers.** The ATM90E26 maintains checksum registers over its
  calibration register banks and raises an error flag if they do not match what
  you wrote. After writing calibration values you must recompute and write those
  checksums. Check the exact register names and the checksum algorithm in the
  datasheet before writing firmware — a unit that silently refuses to meter
  because of a checksum mismatch is a very confusing bug to find at unit 400.

---

## 4.6 The programming and test jig

Build one jig. It pays for itself in the first 50 boards.

### Auto-reset circuit (on the jig, **not** on the product)

This is the standard two-transistor circuit found on every ESP32 DevKit. It lets
`esptool` put the board into bootloader mode automatically, so nobody has to hold
a button 1,000 times.

```
                    Q1, Q2 = NPN  (S8050 / 2N3904 / MMBT3904)

   DTR ──┬────────────── Q1 emitter
         └──[10k]─────── Q2 base

   RTS ──┬────────────── Q2 emitter
         └──[10k]─────── Q1 base

   Q1 collector ─────────────► EN   (J3 pin 5)
   Q2 collector ─────────────► IO0  (J3 pin 6)
```

The cross-coupling is what makes it work: because each transistor's emitter is
tied to the *other* control line, EN and IO0 are only pulled low in the specific
DTR/RTS combinations `esptool` generates — so simply opening a serial monitor
never accidentally resets the board into bootloader mode.

The EN pull-up (R1) and delay capacitor (C12), and the IO0 pull-up (R2), are
already on the product board.

### Jig build

- A USB-serial adapter that exposes **both DTR and RTS** — CP2102 or CH340 are
  both fine. (A bare 4-pin FTDI cable with no RTS will not work.)
- **Pogo pins** aligned to J3's pads, so you never solder a header. Six
  spring-loaded pins in a 3D-printed or acrylic holder, with a lever clamp.
- A USB hub so one PC can drive 4–8 jig stations at once.
- A script that, in one keypress:
  1. flashes the firmware,
  2. runs the Stage-2 self-test,
  3. (on a mains-connected jig) runs the Stage-4 calibration,
  4. writes NVS and uploads the constants,
  5. prints `PASS` + the serial number, or `FAIL` + the reason.

One person with a 4-station jig can realistically process **40–60 boards per
hour** through flash + self-test.

---

## 4.7 Test equipment to buy

Roughly US$ 250 total. For a 1,000-unit run that is US$ 0.25 per unit — the
cheapest quality insurance you will ever buy.

| Equipment | Why you need it | Rough cost |
|---|---|---|
| **True-RMS multimeter** (e.g. UNI-T UT61E+, Aneng AN870) | Voltage reference for calibration. **Must be true-RMS** — an averaging meter is wrong on any distorted waveform. | US$ 50 |
| **True-RMS clamp meter** (e.g. UNI-T UT210E) | Current reference for calibration. | US$ 35 |
| **Reference energy meter** — a Class 1 DIN-rail kWh meter | The independent check on accumulated kWh. Class 0.5 if you can find one. | US$ 15–40 |
| **500 V insulation tester (megohmmeter)** | Stage-1 isolation test. A multimeter cannot do this job properly. | US$ 40 |
| **Isolation transformer, 300–500 VA** | Protects your technicians and your equipment during every mains-powered test. | US$ 40 |
| **Variac (autotransformer)** | Sweep 180–270 V to verify the voltage channel does not clip and the PSU holds up during brownouts. | US$ 60 |
| **RCD / GFCI for the bench** | Last-line protection for people. | US$ 10 |
| Inspection microscope or USB camera | Checking the SSOP-28 joints. Also listed in [tooling §7.3](07-assembly-and-tooling.md). | US$ 40 |

---

## 4.8 The golden-unit method

Calibrating every unit against lab-grade references is impractical. Instead:

1. Pick **three** boards from the first build. Calibrate them extremely
   carefully, at several load points, against your best references, ideally
   cross-checked against the customer's own utility meter over 24 hours.
2. These are your **golden units**. Label them, store them safely, and never
   sell them.
3. In production, run a golden unit alongside the batch on the same load. The
   unit under test is calibrated to agree with the golden unit.
4. Re-verify the golden units against your references every few months, and
   whenever you change CT supplier.

This is how real meter factories work. It transfers one careful, expensive
calibration to 1,000 cheap, fast ones.

---

## 4.9 Stage 5 — Soak test and acceptance

- Run each finished unit for **30–60 minutes** on a known constant load.
- Compare accumulated Wh against the expected value (or against the golden unit
  running on the same load).
- **Accept** if within ±2 %. **Reject** otherwise and investigate — do not just
  re-calibrate a unit that is out by 5 %, because something is actually wrong
  with it.
- Confirm the unit connects to Wi-Fi, reaches your server, and that its records
  arrive with correct timestamps.
- Pull the mains for 10 minutes, restore it, and confirm: the RTC kept time, the
  buffered records were uploaded, and no data gap appears on the server.

### Sampling checks (do these on 1 in 20 units)

- Low-load accuracy at ~100 W.
- Behaviour at 180 V and 270 V on the variac.
- Reverse the CT and confirm the firmware handles the sign correctly.

---

## 4.10 Traceability

Keep a simple record per unit — a spreadsheet is enough:

`serial · date · assembler · ESP32 MAC · isolation test result · self-test result
· Ugain · Igain · phase · no-load reading · soak error %`

When (not if) you get a batch of bad burden resistors or a bad reel of clamps,
this record is how you find out which 80 units are affected instead of recalling
all 1,000.
