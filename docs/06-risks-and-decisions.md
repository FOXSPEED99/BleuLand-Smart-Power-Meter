# 6. Risks, Limitations and Decisions You Should Be Aware Of

Ordered roughly by how likely they are to actually cause you a problem.

---

## 6.1 🔴 The ATM90E26 supply is thin — act on this before you order PCBs

**The risk.** At the time of writing, LCSC listed roughly **200–230 pieces of
`ATM90E26-YU-R` at about US$ 1.32**. You need 1,000. That is a single order away
from stopping your production line, and this part has no drop-in replacement —
nothing else on the market shares its SSOP-28 pinout.

**What to do, in order:**

1. **Check live stock before you commit to a PCB layout.** Not after.
2. **Buy the full 1,000 (plus 5 % spares) up front**, across multiple
   distributors if necessary — LCSC, Arrow, and Chinese brokers all list it.
   At US$ 1.32 that is about US$ 1,400. Committing that early is far cheaper than
   a stalled line and idle assemblers.
3. Order `ATM90E26-YU-B` (LCSC **C145595**) as well as `-YU-R` — same die, same
   SSOP-28 package, different packing (tube vs reel). Treat them as
   interchangeable, but **verify the package on the product page** before paying.
4. **Decide your Plan B now, not later.** If you cannot secure 1,000 pieces,
   switch to `BL0940` (TSSOP-14, LCSC **C691894**, ~US$ 0.36, thousands in stock)
   or `HLW8032` (SOP-8, LCSC **C128023**, ~US$ 0.27, ~32,000 in stock). Both are
   hand-solderable. Both cost you some accuracy, some documentation quality
   (largely Chinese datasheets), and finer phase-calibration control.
   **Critically: they need a different footprint**, so this decision must be made
   *before* the PCB is finalised.
5. If you want maximum insurance, draw **two board variants** from the same
   schematic — one with the ATM90E26 footprint, one with the BL0940 footprint —
   and order a small quantity of each. Bare PCBs are the cheapest thing in this
   project.

---

## 6.2 🔴 Two component values are not yet confirmed

`Rb` (CT burden, starting value 10 Ω) and `Rv5` (voltage burden, starting value
330 Ω) both depend on the ATM90E26's full-scale analog input range, which I could
not confirm from the datasheet with enough certainty to fix at 1,000-unit scale.

Published reference designs using the same `SCT-013-000` clamp use a **12 Ω**
burden, which is consistent with the starting values above — but "consistent
with" is not "verified".

**Do not order 1,000 of either resistor until you have built 5 prototypes and run
the verification in [circuit §3.3](02-circuit.md).** The parallel trim footprints
(`Rb2`, `Rv6`) exist precisely so this costs you half a day rather than a
respin.

---

## 6.3 🟠 The current clamp sets your accuracy, not the metering IC

A `SCT-013-000`-class clamp is roughly **±1–2 % above 10 % of its range and
±3 % or worse below that**. Putting a 0.1 %-class metering IC behind it does not
make the system 0.1 % accurate — it makes it clamp-accurate.

**Implications:**
- If a customer disputes their reading, the clamp is almost always the cause.
- If you want to improve accuracy, **spend the money on a better CT**, not a
  better IC. A 0.5 %-class clamp costs more but moves the whole product.
- The clamp is also ~31 % of your BOM cost. It deserves the most supplier
  attention of anything in the design: buy samples from three suppliers, measure
  their actual turns ratio and linearity against each other, and then commit.
- **Re-verify your golden units whenever you change clamp supplier or batch.**

---

## 6.4 🟠 Low-load accuracy, and phantom consumption

With the CT sized for ~78 A full scale, a 50 W standby load draws about 0.22 A —
**0.28 % of full scale**. It is measurable, but noisy.

- Specify your product honestly: **accurate above ~50 W**.
- Implement the no-load threshold from
  [calibration §4.5(d)](04-calibration-and-test.md). Without it, a couple of
  watts of noise accumulates into **~1.4 kWh of phantom consumption per month**,
  on every unit, forever.
- This is an unavoidable consequence of whole-house monitoring with one clamp,
  not a flaw in this design. Every competitor product has the same limit.

---

## 6.5 🟠 Single-phase only — you need a pre-sale check

This device measures **one phase**. If a customer's home has a three-phase
supply — common in larger villas and in buildings with lifts or large pumps — it
will under-report by up to **3×**, and the customer will conclude your product is
broken.

**Add a question to your sales/install process:** *"How many live wires enter
your main breaker — one or three?"* Three-phase homes need a different product
(three clamps and a three-channel front end), which is a natural "Pro" variant
later.

---

## 6.6 🟠 The clamp must go after any changeover switch

You told us grid mains only, and the design reflects that. But installation
reality is broader: many Syrian homes have a changeover between the grid, a
neighbourhood generator subscription, or an inverter/UPS.

**If the clamp is placed on the incoming grid cable only, everything the house
consumes from any other source is invisible.** The install rule is: *clamp the
conductor that feeds the house, downstream of any changeover* — not the one that
comes from the street.

Put this in the installer manual with a diagram. It is the single most common way
these devices get installed wrong.

> Note also: the design measures true power from L-N voltage and L current, so it
> would still read correctly on generator or inverter power, **except** that a
> cheap inverter's non-sinusoidal output would introduce error the design is not
> tuned for. If you later want to sell into homes running on inverters, revisit
> this — the hardware can do it; the calibration approach would need widening.

---

## 6.7 🟡 CT direction, and leaving the door open for solar

If the clamp is fitted backwards, real power reads **negative**.

- Handle it at commissioning: if the device sees sustained negative power, either
  auto-correct and record that it did, or prompt the installer.
- **Do not simply take the absolute value in firmware and forget about it.** Log
  the raw sign. The day you want to support solar export — which is coming fast
  in Syria — the sign *is* the export measurement, and the hardware already
  supports it. Throwing the sign away in firmware would mean re-visiting every
  installed unit.

---

## 6.8 🟡 3D-printed enclosures are not flame-retardant

Covered in detail in [layout §5.9](05-layout-and-enclosure.md). Short version:
**never PLA**; PETG or ABS as a minimum; move to an off-the-shelf UL94 V-0
electrical box for volume production. This is a liability question for a company
selling mains-connected hardware, not just an engineering preference.

---

## 6.9 🟡 Counterfeit and out-of-spec parts from open-market sourcing

Buying locally and from AliExpress means you will eventually receive fake or
remarked parts. The three most commonly counterfeited items in this BOM:

| Part | What goes wrong | Incoming check |
|---|---|---|
| **DS3231** | Very commonly remarked lower-grade parts with no real TCXO. Drifts minutes per month instead of seconds per year. | Read the DS3231's internal temperature register — a fake often returns a fixed or implausible value. Then leave 3 samples running for a week and measure the drift. |
| **ESP32 modules** | Relabelled 4 MB parts sold as 8 MB; refurbished modules. | `esptool.py flash_id` on every unit reports the real flash size. Make this part of your Stage-2 self-test. |
| **CT clamps** | Wildly variable turns ratio between batches; cores that do not close properly. | Measure the turns ratio on 5 pieces per batch with a known current. Reject the batch if they disagree by more than 2 %. |

Also: **X2 capacitors and MOVs are safety parts**. A counterfeit X2 cap is a fire
risk, not a performance issue. Buy these from a reputable source even if it costs
more, and do not let a local shop substitute "the same value" from an unmarked
bin.

---

## 6.10 🟡 Wi-Fi inside a metal distribution board

You chose the PCB antenna with a plastic enclosure and a nearby router, which is
reasonable. The residual risk is that a *metal* distribution board acts as a
Faraday cage — the plastic inner box does not help with that.

**Mitigation, at zero BOM cost:** `ESP32-WROOM-32UE` is **footprint-identical**
to the `-32E` and carries a u.FL connector. Lay the board out once; on any
install that needs it, fit a `-32UE` plus a US$ 0.80 pigtail antenna. No PCB
revision, no second design, no decision needed today.

---

## 6.11 🟡 Flash size vs OTA updates — decide this before ordering modules

You will need **over-the-air firmware updates**. With 1,000 units installed
inside people's breaker panels, physically re-flashing them is not an option.

OTA requires **two application partitions** so a failed update can roll back. On
a 4 MB module that changes the storage arithmetic:

| Module | App partitions | Left for data | Offline buffer @ 1 record/min |
|---|---|---|---|
| `ESP32-WROOM-32E-**N4**` (4 MB) | 2 × ~1.5 MB | ~0.95 MB | **~41 days** |
| `ESP32-WROOM-32E-**N8**` (8 MB) | 2 × ~1.9 MB | ~4 MB | **~6 months** |

**Recommendation: specify the N8 (8 MB) variant.** It costs roughly US$ 0.30 more
and buys you comfortable headroom for both the buffer and a firmware image that
will grow (TLS + MQTT + a Wi-Fi config web portal add up fast). The N4 is
acceptable and 41 days of buffer is genuinely enough for grid-only use — but the
N8 removes a constraint you would otherwise fight for years.

Whichever you choose, **plan the partition table before the first production
flash.** Changing partition layout later means every field unit needs a full
re-flash, which is exactly what OTA was supposed to prevent.

---

## 6.12 🟡 Security

The device stores Wi-Fi credentials and a cloud token, and its programming header
is physically accessible to anyone who opens the box.

Minimum sensible practice for Phase 2:
- **Per-device credentials.** Never ship a shared secret across 1,000 units — one
  extracted token must not compromise the fleet.
- **TLS to your server**, with certificate validation actually enabled. (The
  ESP32's hardware crypto is why this design does not use an ESP8266.)
- No default password on any local configuration interface.
- Consider ESP32 **flash encryption and secure boot** if the cloud token is
  valuable. This has real operational costs — a bricked unit cannot be recovered
  — so decide deliberately rather than by default.
- Provisioning: use a proper Wi-Fi provisioning flow (SoftAP portal or BLE), not
  hard-coded credentials.

---

## 6.13 🟡 Hand-assembly consistency across 1,000 units

Thirty-four SMD placements by hand, 1,000 times, by several people, is where
defects come from — not from the circuit.

- The ATM90E26's 0.65 mm pitch is the hardest joint on the board. Drag-soldering
  with good flux is reliable, but it needs practice and magnified inspection.
- Expect a first-pass yield around 90–95 % by hand. Budget rework time and
  spare parts accordingly (order 5 % spares of every part, 10 % of the ICs).
- This is the strongest argument for the stencil + hotplate route in
  [tooling §7](07-assembly-and-tooling.md): it does not just save time, it makes
  the joints *consistent*, which is what actually determines your yield.

---

## 6.14 🟢 No EMC or safety certification

This design is not EMC-tested or safety-certified. It includes the basics that
make certification *possible* later (fuse, MOV, X2 capacitor, proper isolation
and creepage), and a footprint for a common-mode choke, but no testing has been
done.

For domestic sales in Syria this may be acceptable today. For export — or if a
serious customer or insurer asks — you would need CE marking, which means
conducted/radiated emissions testing and a safety assessment. Budget for it
before you plan any export.

---

## 6.15 🟢 Limitations inherent to the concept

These are not flaws to fix; they are properties of whole-house clamp monitoring
that your marketing should be honest about:

- It measures **total** consumption. It cannot tell you which appliance is
  running, only that something is.
- It is an **estimate of the bill**, not the bill. The utility's own meter is the
  legal instrument. Your app should say so, in the app — "estimated" in small
  grey text is a real customer-trust feature.
- Accuracy below ~50 W is limited (§6.4).
- One clamp, one phase (§6.5).

---

## 6.16 Open decisions for you

| # | Decision | My recommendation | Deadline |
|---|---|---|---|
| 1 | ATM90E26 vs BL0940 fallback | ATM90E26 if you can secure 1,000 pieces; decide now | **Before PCB layout** |
| 2 | 4 MB vs 8 MB ESP32 module | **8 MB (N8)** | Before ordering modules |
| 3 | Final `Rb` and `Rv5` values | Verify on 5 prototypes | Before the 1,000-unit component order |
| 4 | 3D-printed vs off-the-shelf enclosure | Printed (PETG/ABS) for pilot, V-0 box for volume | Before pilot batch ships |
| 5 | Buy a stencil + hotplate? | **Yes** — see [§7.3](07-assembly-and-tooling.md) | Before volume assembly |
| 6 | Cloud backend and data model | Out of scope here; the board is agnostic | Phase 2 |
| 7 | Board variant with BL0940 footprint as insurance | Worth the ~US$ 50 for a small PCB order | With decision 1 |
