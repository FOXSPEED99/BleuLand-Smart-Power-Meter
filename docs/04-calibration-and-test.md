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
| **CT phase error** | 0.5–3° | Yes — but in **hardware**, via the `Cf2` capacitor (§4.5c). Fixed per batch, not per unit. |
| Burden resistor tolerance | ±1 % | Yes |
| **Burden resistor temperature drift** | ±0.2 % over 40 °C (at 50 ppm/°C) | **No.** This is why the tempco spec matters. |
| ZMPT101B turns-ratio tolerance | ±1 % | Yes |
| ZMPT101B phase shift | 1–2° | Yes |
| Rv1–Rv4 combined tolerance | ±0.5 % | Yes |
| HLW8032 metering core | ±0.5 % above 10 % of range, **±3 % below 2 %** | No — this is the chip's dynamic-range limit |
| **Realistic total after per-unit calibration** | **±2–3 % above 200 W; unreliable below ~50 W** | |

Two conclusions fall straight out of this table:

1. **The clamp dominates.** A better metering IC behind a ±3 % clamp still gives
   you a ±3 % product. Spend your accuracy budget on the CT, not the IC. This is
   exactly why the cheaper, easier-to-solder HLW8032 was the right call for v1 —
   see [`docs/01-architecture.md`](01-architecture.md) §1.4.
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
   | A valid 24-byte HLW8032 packet arrives on UART2 within 1 s | Metering IC alive, level shifter correct, UART wiring |
   | Its **checksum validates** | Clean signal path, no noise corruption |
   | Reported Vrms is 0 (no mains yet) but the packet is well-formed | Voltage channel wired, not shorted |
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

> **Everything here is a firmware constant, not a chip register.** The HLW8032
> cannot be written to — it only broadcasts. So calibration means computing a
> scale factor in the ESP32 and storing it in NVS. This is simpler than register
> calibration, but it means a board with a wiped flash is an *uncalibrated*
> board. Back the constants up to your server (§4.5e).

### (a) Voltage scale factor

1. Apply mains. Measure the true voltage with your reference DMM at the terminal
   block.
2. Read the raw voltage value from the HLW8032 packet.
3. ```
   k_voltage = V_reference / V_raw
   ```
4. Store `k_voltage` in NVS. Re-read and confirm the reported voltage is within
   ±0.3 % of the reference.

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
   k_current = I_effective / I_raw
   ```
   Store `k_current` in NVS. Derive the power scale factor the same way from a
   known power reading rather than assuming `k_power = k_voltage × k_current` —
   the chip's power path has its own scaling.
5. Verify linearity with a second point (e.g. 0.5 A → 5 A effective and 2 A →
   20 A effective). The two points should agree within 1 %. If they do not, the
   clamp is non-linear or something is clipping — go back to
   [circuit §3.3](02-circuit.md).

### (c) Phase compensation — tuning the `Cf2` capacitor

This is done **once for the product**, on the prototypes, not per unit. It is a
hardware value, so you must fix it before the production run.

With a **purely resistive** load (incandescent lamps or a heater — *not* LED
lamps or anything with a switch-mode supply, which are non-linear), the true
power factor is exactly 1.000.

1. Put the resistive load on, at roughly the same current used for gain
   calibration.
2. From the HLW8032 packet compute `PF = P / (V × I)`.
3. If it reads above or below 1.000, the CT's phase error is uncorrected.
4. Try `Cf2` values in sequence — 68 nF, 82 nF, 100 nF, 120 nF, 150 nF — until
   PF reads 1.000 (within ±0.001).
5. **Lock that value for the whole production run** and record it.

Skipping this costs roughly 1.4 % on the daily energy total, and about 2 % on a
PF-0.8 motor load — and Syrian homes are full of motors. One capacitor recovers
almost all of it. The theory is in [`docs/02-circuit.md`](02-circuit.md) §2.5.3.

> ⚠️ **This is tuned to one CT model.** If you change clamp supplier or the
> supplier changes their core, re-run this procedure and re-qualify. Write that
> into your purchasing rules, because a silent CT substitution would shift every
> unit's accuracy with no other visible symptom.

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
- ⚠️ **Validate the HLW8032's packet checksum on every frame, without
  exception.** At 4800 baud inside an electrically noisy distribution panel you
  *will* receive corrupted frames. A corrupted power value that passes into your
  energy accumulator silently poisons the customer's monthly total, and you will
  never find it afterwards. Discard bad frames and wait — a fresh one arrives
  roughly every 50 ms, so dropping them costs nothing.
- ⚠️ **A wiped flash means an uncalibrated board.** Unlike register-based
  calibration, nothing is stored in the metering chip. Treat the server-side
  backup of `k_voltage`, `k_current`, `k_power` and the no-load threshold as
  mandatory, not optional.

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
| Inspection microscope or USB camera | General joint inspection. Less critical for v1 than it was with the ATM90E26, but still the fastest way to catch a bridge. Also in [tooling §7.4](07-assembly-and-tooling.md). | US$ 40 |

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
