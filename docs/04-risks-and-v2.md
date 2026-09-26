# Risks, Honest Limitations, and the Version 2 Plan

---

# Part 1 — Things that could go wrong

Ordered by how likely they are to actually cause a problem.

## 1.1 🔴 Three component values are not final yet

`Rb` (0.68 Ω), `Rv5` (150 Ω) and `Rf2`/`Rf3` (1.5 kΩ) are **starting points**,
not answers.

`Rb` and `Rv5` depend on the HLW8032's exact input range, which its datasheet
describes in terms of a shunt resistor rather than as a pin voltage. The starting
values are *worked out* from the published shunt configurations — sound
reasoning, but it is inference, not a quoted specification. `Rf2`/`Rf3` depend on
your specific clamp's timing error, which cannot be known in advance at all.

**This matters more than it would with a fancier chip.** Some metering chips have
an adjustable gain stage you can use to rescue a burden resistor that turned out
wrong. **The HLW8032 does not.** What the burden gives it is what it gets:

- Burden too large → a 60 A load flattens off, silently and unfixably.
- Burden too small → every reading is noisier and the low-load floor gets worse.

> **Do not order 1,000 of any of the three until you have built five prototypes
> and confirmed them.** Half a day of work. The shopping list includes the
> sweep values to make it easy.

## 1.2 🟠 The clamp sets your accuracy, not the chip

A `SCT-013`-class clamp is roughly **±1–2 % above 10 % of its range, ±3 % or
worse below**. Putting a better measuring chip behind it would not make the
product better — it would still be clamp-accurate.

- If a customer disputes a reading, the clamp is almost always the reason.
- **If you want better accuracy, spend the money on a better clamp**, not a
  better chip.
- It is also ~31 % of your bill of materials, so it deserves more supplier
  attention than anything else: buy samples from three suppliers, measure their
  actual ratio and linearity, then commit.

## 1.3 🟠 Nothing below ~50 W is reliable

The HLW8032 has a measuring range of roughly **400:1**. With the clamp sized for
78 A, the smallest load it reads reliably is about **45 W**.

A house spends most of the night between 200 and 400 W — only 5–9× above that
floor — so night-time readings will be the noisiest part of your data.

- **Say "accurate above 50 W" in your product specification** and mean it. Do not
  let marketing round it down.
- Implement the zero threshold from the calibration guide. Without it, a couple
  of watts of noise accumulates into **~1.4 kWh of imaginary consumption per
  month**, on every unit, forever.
- If night-time accuracy ever becomes a real customer complaint, that is a
  concrete, measurable reason to move to v2.

## 1.4 🟠 Single-phase only — ask before you sell

This device measures **one phase**. A home with a three-phase supply — common in
larger villas and buildings with lifts or big pumps — would be **under-reported
by up to 3×**, and the customer would conclude the product is broken.

**Add one question to your sales process:** *"How many live wires come into your
main breaker — one or three?"* Three-phase homes need a different product with
three clamps. That is a natural "Pro" version later.

## 1.5 🟠 The clamp must go in the right place

This is the most common way these devices get installed wrong.

Many Syrian homes have a changeover switch between the grid, a neighbourhood
generator and sometimes an inverter. **If the clamp is put on the incoming grid
cable only, everything the house uses from any other source is invisible.**

**The rule: clamp the conductor that feeds the house, after any changeover
switch** — not the one coming from the street. Put this in the installer manual,
with a diagram.

> The device measures real power from live-neutral voltage and live current, so
> it would still read correctly on generator power. A cheap inverter's
> non-sinusoidal output would introduce error the design is not tuned for — worth
> revisiting if you ever sell into homes running on inverters.

## 1.6 🟡 Clamp direction, and leaving room for solar

Fit the clamp backwards and the power reads **negative**.

Handle it at commissioning: if the device sees sustained negative power, either
correct it automatically and record that it did, or prompt the installer.

> **Do not simply take the absolute value in firmware and forget about it.** Log
> the raw sign. When you want to support solar export — which is coming fast in
> Syria — **the sign is the export measurement**, and this hardware already
> supports it. Throwing it away would mean revisiting every installed unit.

## 1.7 🟡 Development boards vary between batches

This is the real cost of using an off-the-shelf board instead of a soldered
module. Board makers change the regulator, the USB chip, sometimes the pin order
— without telling anyone.

**Four rules that neutralise most of it:**

1. **Buy all 1,050 from one supplier, in one order, from one batch.**
2. **Build the PCB footprint from a board you physically have**, measured with
   callipers — not from a pinout diagram found online.
3. **Keep three boards from that batch sealed as reference samples.** When unit
   700 behaves oddly, compare it against a known-good one.
4. **Test a sample** before committing: `esptool flash_id` reports the real chip
   and flash size, which catches remarked parts.

## 1.8 🟡 Counterfeit parts

Buying from open markets means you will eventually receive fakes. The three most
commonly faked items here:

| Part | What goes wrong | How to check |
|---|---|---|
| **ESP32 boards** | Remarked flash size, refurbished modules | `esptool flash_id` reports the truth. Make it part of your self-test |
| **DS1307 clock** | Remarked or clone parts that drift badly | Run three samples for a week against a reference. A genuine one loses a few seconds; a fake loses minutes |
| **Current clamps** | Wildly variable ratio between batches; cores that do not close properly | Measure the ratio on 5 pieces per batch with a known current. Reject the batch if they disagree by more than 2 % |

⚠️ **The X2 capacitor and the MOV are safety parts.** A counterfeit there is a
fire risk, not a performance issue. Buy them from a reputable source even at
higher cost, and never let a shop substitute "the same value" from an unmarked
bin.

## 1.9 🟡 3D-printed enclosures are not flame-retardant

The enclosure around a mains-connected device is a **fire-safety component**. Its
job is to contain a fault. Commercial electrical boxes are made of UL94 V-0
self-extinguishing plastic. Common filaments are not.

| Material | Softens at | Verdict |
|---|---|---|
| **PLA** | ~60 °C | **Do not use.** A breaker panel in a Syrian summer reaches that on its own. The box will sag around live parts |
| **PETG** | ~80 °C | Minimum acceptable — prototypes and pilot units |
| **ABS / ASA** | ~100 °C | Better. Still not V-0 |
| **Off-the-shelf V-0 electrical box** | 100 °C+ | **Best.** Cheap in quantity, already certified, looks like a product |

**Recommendation:** 3D-print for prototypes and your first pilot batch, then move
to a standard flame-retardant enclosure for volume. If you do keep printing, use
**PETG or ABS, never PLA**, with walls at least 2.5 mm thick and 3 mm of air
between any live copper and the inside wall.

## 1.10 🟡 WiFi inside a metal panel

A plastic enclosure is fine, but if the **distribution board itself** is metal,
it acts as a shield and the plastic inner box does not help.

Mitigation: mount the device just outside the metal panel, or route the clamp
lead out to a device sitting beside it.

## 1.11 🟡 Security

The device holds a customer's WiFi password and a cloud token, and its USB port
is physically reachable.

Minimum sensible practice:
- **Per-device credentials.** Never ship one shared secret across 1,000 units —
  one extracted token must not compromise the fleet.
- **Encrypted connection to your server**, with certificate checking actually
  enabled.
- No default password on any local configuration screen.
- Use a proper WiFi setup flow, not hard-coded credentials.

## 1.12 🟢 No certification

This design is not EMC-tested or safety-certified. It includes the basics that
make certification possible later — fuse, surge protector, X2 capacitor, proper
isolation and spacing — but no testing has been done.

For domestic sales in Syria this may be acceptable today. For export, or if a
serious customer or insurer asks, you would need CE marking. Budget for it before
planning any export.

## 1.13 🟢 Limits that come with the concept itself

Not flaws to fix — properties of whole-house clamp monitoring that your marketing
should be honest about:

- It measures **total** consumption. It cannot tell you which appliance is
  running, only that something is.
- It is an **estimate of the bill**, not the bill. The utility's own meter is the
  legal instrument. **Your app should say so** — "estimated" in small grey text
  is a real customer-trust feature.
- Accuracy below ~50 W is limited.
- One clamp, one phase.

---

# Part 2 — The Version 2 plan

## 2.1 When to start v2

Any one of these is reason enough. None is urgent today.

| Trigger | Why it points to v2 |
|---|---|
| **You move to machine-assembled boards** | The only reason for the development board was hand assembly. Machine placement removes that reason entirely |
| **Night-time accuracy becomes a real complaint** | The biggest single improvement v2 offers: a 4 W floor instead of 45 W |
| **You want per-unit timing correction** | v1 corrects it in hardware, fixed per batch. v2 can correct it per unit, in software |
| **You add solar export measurement** | Cleaner on a chip you can configure |
| **You need a three-phase version** | The upgrade chip's bigger sibling shares the same programming model |

## 2.2 What changes

| | v1 (today) | v2 |
|---|---|---|
| Measuring chip | HLW8032, 8 pins | **ATM90E26**, 28 pins |
| Accuracy | ±2–3 % | **±1–2 %** |
| Smallest reliable load | 45 W | **4 W** |
| Timing correction | Resistor value, per batch | **Register, per unit** |
| Calibration | Firmware constants | Written into the chip |
| Brain | ESP32 development board | **Soldered ESP32 module** |
| Assembly | By hand | Machine |
| Chip cost | $0.27 | $1.32 |
| Clamp connection | Screw terminal — plug cut off | **3.5 mm socket — plug in** |

**Net cost change: roughly +US$ 2 per device** — and the board gets smaller.

### The clamp socket, deferred from v1

The SCT-013-000 arrives with a **3.5 mm stereo plug already moulded on**, so v1
throws that away: every unit needs the plug cut off and two wires stripped,
inside a panel, and a faulty clamp can never simply be unplugged.

**It was not a cost problem** — a generic socket is about US$ 0.07, roughly what
the screw terminal costs. It was a **footprint risk**. A 2-pin screw terminal is
two holes at a fixed pitch and every manufacturer's is identical; every 3.5 mm
socket has a different pin layout, and picking the wrong one means a thousand
unusable bare boards with no warning from the design rule check.

**To bring it into v2, do this first, in this order:**

1. Pick **one** socket part number that has a real datasheet with a dimensioned
   drawing — not a marketplace listing from a reseller brand.
2. Buy 20 and confirm the pins sit where the drawing says.
3. With a clamp plugged in, measure between every pair of pins. **Two read a few
   tens of ohms — that is the winding.** The third reads open: that is the ring
   contact, and the clamp does not use it. Tie it to analog ground.
4. Build the footprint from that drawing, and keep the part number pinned in the
   bill of materials.

Do all four before routing, and the socket is a straight upgrade.

## 2.3 What stays exactly the same

This is why v2 is cheap rather than a fresh start:

- The **clamp, the terminals and the installation procedure** — unchanged.
- The **voltage sensing chain** (`T1`, `Rv1`–`Rv4`, `Rv5`) — unchanged.
- The **isolated power supply** — unchanged.
- The **clock, lights and enclosure** — unchanged.
- The **safety barrier and spacing rules** — unchanged.
- The **10-turn calibration trick, golden units and test procedure** —
  unchanged.
- **Your server, your data model and your app** — unchanged, *provided* you
  follow the four rules below.

Realistically, v2 is a **partial redraw of one corner of the board** plus a
firmware driver swap. Not a new product.

## 2.4 ⭐ Four rules in v1 that keep v2 cheap

All free now. All painful to retrofit.

1. **Log raw volts, amps and watts to your server — not only kWh.** Then you can
   put a v1 and a v2 unit on the same house and compare them directly.
2. **Put a `hardware_version` field on every record, from the very first one.**
   Adding it after 500 units are deployed is miserable.
3. **Keep calibration constants in the ESP32's memory, never hard-coded** in the
   firmware.
4. **Keep the clamp, the burden resistor and the voltage chain the same across
   versions**, so your calibration procedure and installer training carry over
   unchanged.

## 2.5 Two things to re-check before committing to v2

Do not assume today's analysis still holds:

1. **ATM90E26 stock.** At the time of writing there were only ~230 pieces
   available against a 1,000-unit need — that was the original reason v1 went a
   different way. Check before committing to a layout.
2. **Whether the BL0942 chip has a timing-correction register.** This was never
   resolved. If it does, it may beat the ATM90E26 for our purposes: fewer pins,
   no crystal, cheaper, far better stock. Ten minutes with the datasheet,
   potentially a better v2.

---

# Part 3 — Decisions already settled (do not re-open these)

## 3.1 The clock chip — why DS1307 and not the others

This one was investigated at length. The conclusion is recorded here so nobody
starts again from scratch in six months.

**The question:** the ESP32 can work out timestamps by itself as long as it never
loses power. When mains cuts *during* an internet outage, its counter resets. One
power cut is recoverable; two or more before the internet returns is not. In
Syrian homes that is common enough to matter.

**What was evaluated:**

| Option | Why it was rejected |
|---|---|
| **No clock chip at all** | Works for the common case (mains on, internet off) but leaves the daily graph hours out of place after repeated power cuts |
| DS3231 "blue module" | Has a trickle charger that destroys a non-rechargeable CR2032 |
| DS1307 "Tiny RTC" module | Ships with a rechargeable LIR2032 that dies in ~2 years; puts a **resistor divider on the battery pin**, which the DS1307 datasheet forbids; pull-ups go to whatever powers it |
| **DS1302** chip | Needs a **6 pF** crystal. Essentially every cheap 32.768 kHz crystal is 12.5 pF — could not source the right one |
| **MCP7940N** chip | Needs **external load capacitors** → 9 parts instead of 7 |
| **PCF8563** chip | **No battery pin** — needs two Schottky diodes to switch supplies → 9 parts |
| **DS3231M / MZ** | Assumed cheaper than the DS3231SN. It is not — $2.02 to $6.55 against ~$1.50 |
| DS3231SN chip | Excellent, 6 parts, no crystal — but ~$0.46/device more than the DS1307 |

**Chosen: the bare DS1307Z+ chip.** 7 parts, ~$1.25/device, internal load
capacitors so the crystal connects directly, and a proper battery pin with
automatic switchover.

**The three things that make it work:**

1. **Pull-ups to 3.3 V, never 5 V.** The chip runs on 5 V but its data lines are
   open-drain, so the pull-up voltage sets the bus voltage. This is what protects
   the ESP32 — and it is exactly what cheap modules get wrong.
2. **Crystal must be 12.5 pF**, with no external capacitors (they are inside the
   chip).
3. **Battery straight to the battery pin, nothing else on that wire.**

**What was accepted:** ±3 seconds/day of drift, against the DS3231's ±2 ppm. It
does not matter — the internet resets the clock every time it connects. The
chip's job is to bridge days, not years.

---

# Part 4 — Decisions still open

| # | Decision | Recommendation | When |
|---|---|---|---|
| 1 | Can the local shop supply 1,050 ESP32 boards from one batch? | **Ask this week.** It is the most important sourcing question in the project | Before ordering |
| 2 | Final `Rb`, `Rv5`, `Rf2`/`Rf3` values | Confirm on five prototypes | Before the full order |
| 3 | 3D-printed vs off-the-shelf enclosure | Printed (PETG/ABS) for the pilot, V-0 box for volume | Before the pilot ships |
| 4 | Buy a stencil and hotplate? | **Yes** — saves ~135 hours and improves yield | Before volume assembly |
| 5 | Cloud backend and data model | Out of scope here; the board is agnostic | Phase 2 |
| 6 | When to start v2 | When machine assembly is on the table, or night-time accuracy becomes a complaint | After v1 ships |
