# Building, Testing and Calibrating

How to turn bare boards and a box of parts into 1,000 working devices.

---

# Part 1 — Assembly

## 1.1 What you need

| Tool | Notes |
|---|---|
| Soldering iron, 330–350 °C | Chisel tip, 1.6–2.4 mm |
| Leaded solder, 0.5 mm | Sn63Pb37. Melts at 183 °C and flows far better than lead-free |
| Flux (gel or pen) | **Not optional.** It is what makes soldering work |
| Fine tweezers | Buy 3–4 pairs |
| Isopropyl alcohol + brush | For cleaning at the end |
| Solder wick | For fixing bridges |
| Magnifier or USB microscope | For inspection |
| Hot-air station | You already have one — for rework only |

## 1.2 Should you buy a stencil and hotplate?

**Yes.** At 1,000 units the numbers are clear:

| | By hand | Stencil + hotplate |
|---|---|---|
| Surface-mount parts | 13–15 min | ~5 min (place only) |
| Reflow | — | ~1 min per board, done in batches |
| Through-hole by hand | 6 min | 6 min |
| **Per board** | **~21 min** | **~13 min** |
| **× 1,000** | **~350 hours** | **~215 hours** |

You save around **135 hours** — but the bigger win is **consistency**. Reflow
makes every joint identical. Expect first-pass yield to go from ~93 % by hand to
~98 % with reflow.

**What to buy:** a frameless 0.12 mm stainless stencil ordered with your PCB
(~US$ 12 each, buy two), and a 200 × 200 mm PID-controlled hotplate
(~US$ 60–120). Plus Sn63Pb37 solder paste in a jar, kept in the fridge.

⭐ **Order your PCBs panelised 2 × 2** — then you paste and reflow four boards at
a time.

## 1.3 The reflow process, simply

1. **Support the board.** Tape scrap PCBs of the same thickness around it so the
   stencil lies flat.
2. **Align the stencil** over the pads. Tape one edge so it hinges.
3. **Print.** Line of paste at one edge, squeegee at 45°, **one firm pass**.
   Going back and forth pushes paste underneath and bridges everything.
4. **Lift the stencil straight up.** Check every pad has a clean brick of paste.
   If it smeared, wipe with alcohol and start again — two minutes, versus an
   hour of rework.
5. **Place the parts** with tweezers. The paste holds them. Perfect alignment is
   not needed — surface tension pulls them straight during reflow.
6. **Reflow** on the hotplate:
   - Ramp to **150 °C**, hold **60–90 seconds** (this activates the flux and
     evens out the heat).
   - Raise to **200–215 °C**. Watch the paste turn from dull grey to **shiny
     liquid metal** — that moment is called the flash.
   - Wait ~10 more seconds, then slide the board off to cool.
   - **Do not overheat.** More time above melting does not improve joints; it
     damages parts.
7. **Inspect** under magnification.

## 1.4 Assembly order

1. **Paste, place and reflow all surface-mount parts** (29 of them).
2. **Inspect.** Fix any bridges now while access is clear.
3. **Hand-solder the safe-side through-hole parts:** `C2`, `Y1`, `BT1`, `J2`, `J4`, `J5`.
4. **Hand-solder the mains parts last:** `Rv1`–`Rv4`, `T1`, `PS1`, `J1`, the fuse
   clips, `RV1`, `C1`. These are the tallest parts and the ones you least want
   to work around.
5. **⚠️ Clean the flux, especially across the safety slot.** Scrub with alcohol
   and a stiff brush, then dry completely.

   > **This is not cosmetic.** Flux residue absorbs moisture and becomes
   > conductive in humid air. A film of it bridging the safety slot quietly
   > destroys the isolation you designed so carefully — and it will not show up
   > until the first humid coastal summer. Clean every board, inspect every
   > board.

6. **Fit the CR2032 battery**, printed side up.
7. **Plug in the ESP32 board.**

## 1.5 Parts that must never go through reflow

| Part | Why |
|---|---|
| `PS1` HLK-PM01 | Sealed module, not reflow-rated |
| `T1` ZMPT101B | Wound component with a plastic bobbin |
| `C2` electrolytic | Will vent or degrade |
| `J1`, `J2` terminals | Plastic melts |
| `J4`, `J5` headers | Plastic deforms |
| `BT1` battery holder | Plastic deforms |
| `Y1` crystal | Through-hole, and a heat-sensitive tuning-fork part |
| `B1` battery | **Never heat a lithium cell** |
| `MCU1` ESP32 board | Obviously — it plugs in at the end |

---

# Part 2 — Testing

## 2.1 Where the error actually comes from

Know what you are fighting before designing a test process.

| Source | Typical | Can you fix it? |
|---|---|---|
| **The clamp itself** | ±1–3 % | Gain, yes — at one point. Non-linearity, no |
| **Clamp timing error** | 0.5–3° | Yes — `Rf2`/`Rf3`, once per batch |
| `Rb` tolerance | ±1 % | Yes, by calibration |
| **`Rb` temperature drift** | ±0.2 % | **No.** This is why 50 ppm/°C matters |
| Transformer `T1` | ±1 % | Yes |
| The measuring chip | ±0.5 % | No, it is what it is |
| **Realistic total after calibration** | **±2–3 % above 200 W** | |

**Two conclusions:**

1. **The clamp dominates.** A better chip behind a ±3 % clamp still gives a ±3 %
   product. Spend your accuracy budget on the clamp.
2. **Per-unit calibration is not optional.** Without it you are stacking every
   tolerance in that table.

## 2.2 Stage 1 — Before any power (every board, ~90 seconds)

1. **Look at it** under magnification: solder bridges, especially on `U2` and
   `U2`.
2. **Check polarity:** `C2`, `LED1`, `LED2`, `BT1`, `U2` leg 1, `U4` leg 1.
3. **Rail test:** 5 V to `GROUND` must not be a short. 3.3 V to `GROUND` must not
   be a short.
4. **⭐ Isolation test — the most important test on the board.**
   Short both pins of `J1` together. Measure between that and `GROUND`.
   - With a multimeter: must read open, above 20 MΩ.
   - **Much better: with a 500 V insulation tester** (~US$ 40). A multimeter at
     9 V will not find a nearly-bridged barrier; 500 V will.
   - **A board that fails this never gets powered up. Ever.** Clean it,
     re-inspect, re-test, or scrap it.
5. **Inspect the safety slot.** No solder balls, no flux film, no bent lead
   crossing it.

**Record the result against the serial number.** When a unit comes back from the
field in two years, you want to know it passed.

## 2.3 Stage 2 — USB only, no mains

This is where the isolated design pays for itself: you can do all of this safely
at a normal bench.

1. Plug a USB cable into the ESP32 board. **Do not connect mains.**
2. Upload the firmware.
3. Run the **self-test**, which should check and print:

| Check | Proves |
|---|---|
| A valid 24-byte packet arrives from `U2` within 1 second | Measuring chip alive, level shifter correct, wiring good |
| Its checksum is valid | Clean signal path |
| The clock chip `U4` answers on the data bus | `U4`, `Y1`, `R5`, `R6` correct |
| The clock reports a sane time and its "oscillator stopped" flag is clear | Crystal running, battery fitted and good |
| The device reaches an NTP server and sets the clock chip | Internet path works end to end |
| Storage area mounts, a test record writes and reads back | Flash partition |
| WiFi scan finds at least one network | Radio and antenna |
| Both lights blink | `LED1`, `LED2`, `R3`, `R4` |

4. Print **one line**: `PASS`, or `FAIL: <which check>`. Your technician needs
   one line, not a log.

## 2.4 Stage 3 — Powered from mains

> ⚠️ **Power the board through an isolation transformer and an RCD.** The board
> is isolated; your bench and your hands are not. This is a hard rule.

1. Connect live and neutral. The green light should come on.
2. Measure the 5 V rail (expect 4.9–5.2 V) and the ESP32's 3.3 V pin
   (3.25–3.35 V).
3. Compare the reported voltage against a true-RMS multimeter on the same
   supply. Before calibration, expect within ±5 %. Wildly wrong or zero means a
   `T1` or `Rv5` problem.

---

# Part 3 — Calibration

Everything here is a **firmware constant stored in the ESP32**, not a setting in
the measuring chip. The HLW8032 cannot be written to — it only broadcasts.

> **Consequence:** a board with erased flash is an **uncalibrated** board. Always
> back the constants up to your server.

## 3.1 Voltage

1. Apply mains. Measure the true voltage with a reference meter at `J1`.
2. Read the raw voltage value from the chip's packet.
3. `k_voltage = true voltage ÷ raw value`
4. Save `k_voltage`. Confirm the reported voltage is now within ±0.3 %.

## 3.2 Current — and the trick that makes this practical

The obvious approach needs 10–20 A of load, which means a 2–4 kW heater: hot,
slow, expensive to run and awkward to do a thousand times.

> ### ⭐ The 10-turn trick
>
> A current clamp measures **ampere-turns**. Pass the load cable through the
> clamp's opening **10 times** instead of once, and the clamp sees exactly **10×
> the current**.
>
> So a **1 A** load — a single 230 W lamp — looks like **10 A**. You calibrate at
> a realistic current using a small, cool, cheap, safe load.

Build a permanent calibration loop: a short flexible cable wound 10 turns
through a fixed clamp, ending in a socket. **Mark the turn count on the jig** —
a mistake here is a 10× calibration error.

1. Switch on the known load.
2. Measure true current with a clamp meter **on the single-turn part** of the
   cable.
3. Effective current = measured × 10.
4. `k_current = effective current ÷ raw value`
5. **Check linearity with a second point** (e.g. 0.5 A → 5 A, then 2 A → 20 A).
   The two must agree within 1 %. If they do not, something is clipping — go
   back to the burden resistor.

Derive the power constant from a known power reading too, rather than assuming
it equals `k_voltage × k_current`.

## 3.3 Timing correction — tuning `Rf2` / `Rf3`

Done **once for the product**, on the prototypes — not per unit. It is a
hardware value, so it must be fixed before the production run.

1. Connect a **purely resistive** load — incandescent lamps or a heater. **Not**
   LED lamps, not anything with a switch-mode supply.
2. From the chip's readings, compute `power factor = watts ÷ (volts × amps)`.
   With a pure heater, the true answer is exactly **1.000**.
3. If it reads above or below 1.000, the clamp's timing error is uncorrected.
4. Try `Rf2` = `Rf3` in sequence: **820 Ω, 1.2 kΩ, 1.5 kΩ, 1.8 kΩ, 2.2 kΩ** until
   power factor reads 1.000 within ±0.001.
5. **Lock that value for the whole run** and write it down.

⚠️ **Always change both resistors together.** They must stay a matched pair or
the measuring chip loses its noise rejection.

⚠️ **This is tuned to one clamp model.** If you change clamp supplier — or your
supplier changes their core — re-run this and re-qualify. Put that in your
purchasing rules, because a silent clamp substitution would shift every unit's
accuracy with no other visible symptom.

## 3.4 Zero — the one that protects your billing

With the clamp connected but clamped around nothing, the device must report
**exactly zero**, not 0.8 W of noise.

> **Why this matters more than it looks:** 2 W of phantom reading × 24 hours ×
> 30 days = **1.4 kWh per month of consumption that does not exist** — on every
> unit, every month, forever.

1. Record the reading with no current.
2. Set a firmware threshold slightly above the noise — typically **5 W**. Below
   it, report and accumulate exactly zero.
3. **Write it in your product specification:** *"accurate above 50 W; loads below
   5 W are not counted."* Honesty here prevents support tickets.

## 3.5 Save the constants

- Store `k_voltage`, `k_current`, `k_power` and the zero threshold in the ESP32,
  keyed to its WiFi MAC address.
- **Also upload them to your server.** If a board's memory is ever erased, or you
  replace a unit, you can restore it without repeating the calibration.

## 3.6 ⚠️ Always check the packet checksum

At 4,800 baud inside an electrically noisy distribution panel you **will**
receive corrupted data. A corrupted power value that slips into your energy
total silently poisons the customer's monthly bill, and you will never find it
afterwards.

**Throw away any packet whose checksum fails and wait for the next one.** A fresh
one arrives every 50 milliseconds, so dropping bad packets costs nothing.

---

# Part 4 — Production quality

## 4.1 The golden unit method

Calibrating every board against lab-grade references is impractical. Instead:

1. Pick **three boards** from the first build. Calibrate them very carefully at
   several load points, ideally cross-checked against a real utility meter over
   24 hours.
2. These are your **golden units**. Label them, store them safely, **never sell
   them**.
3. In production, run a golden unit alongside the batch on the same load. The
   board under test is calibrated to agree with the golden unit.
4. Re-verify the golden units every few months, and **whenever you change clamp
   supplier**.

This is how real meter factories work. It transfers one careful, expensive
calibration onto a thousand fast, cheap ones.

## 4.2 Soak test

- Run each finished unit for **30–60 minutes** on a known constant load.
- Compare accumulated kWh against expected, or against the golden unit.
- **Accept** within ±2 %. **Reject** otherwise — and investigate rather than
  simply re-calibrating, because something is actually wrong.
- Confirm the unit connects to WiFi and reaches your server with correct
  timestamps.
- **Pull the mains for 10 minutes**, restore it, and confirm: the clock kept
  time, the stored readings uploaded, no gap appears on the server.

## 4.3 Sample checks — 1 board in 20

- Accuracy at a low load, around 100 W.
- Behaviour at 180 V and 270 V.
- Reverse the clamp and confirm the firmware handles the sign correctly.

## 4.4 Test equipment to buy

About **US$ 250** total — US$ 0.25 per unit across the run. The cheapest quality
insurance available.

| Equipment | Why | ~Cost |
|---|---|---|
| **True-RMS multimeter** | Voltage reference. **Must be true-RMS** — an averaging meter is wrong on any distorted waveform | $50 |
| **True-RMS clamp meter** | Current reference | $35 |
| **Reference energy meter** (Class 1 DIN-rail kWh meter) | Independent check on accumulated kWh | $15–40 |
| **500 V insulation tester** | The Stage 1 isolation test. A multimeter cannot do this properly | $40 |
| **Isolation transformer, 300–500 VA** | Protects your people and equipment on every mains test | $40 |
| **Variac** | Sweep 180–270 V to check behaviour at the extremes | $60 |
| **RCD for the bench** | Last-line protection for people | $10 |
| Inspection microscope | Joint inspection | $40 |

## 4.5 Keep records

A spreadsheet is enough. Per unit:

`serial · date · who built it · ESP32 MAC · isolation test · self-test ·
k_voltage · k_current · zero reading · soak error %`

When — not if — you get a bad batch of burden resistors or clamps, this record
is how you find out **which 80 units** are affected instead of recalling all
1,000.

## 4.6 Consumables for a 1,000-unit run

| Item | Quantity |
|---|---|
| Solder paste (Sn63Pb37, jar) | 300 g |
| Solder wire, 0.5 mm leaded | 500 g |
| Gel flux syringes | 5–10 |
| Flux pens | 5 |
| Isopropyl alcohol | 5 L |
| Solder wick | 5 rolls |
| Iron tips | 10 — they wear out faster than you expect |
| Cleaning brushes | 10 |
