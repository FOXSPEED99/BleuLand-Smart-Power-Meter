# 8. The v2 Upgrade Path — ATM90E26

This document preserves the design that v1 stepped away from, so that moving to
v2 is a planned upgrade rather than a fresh start.

**Read [`docs/01-architecture.md`](01-architecture.md) §1.4 first** — it explains
why v1 uses the HLW8032 instead.

---

## 8.1 When to trigger v2

Any one of these is a good enough reason. None of them is urgent today.

| Trigger | Why it points at v2 |
|---|---|
| **You move to machine assembly** (JLCPCB PCBA or similar) | The only real objection to the ATM90E26 was hand-soldering 28 pins at 0.65 mm. Machine placement makes that objection vanish, at no assembly cost. |
| **Night-time accuracy becomes a customer complaint** | The HLW8032's ~400:1 dynamic range puts the floor at ~45 W. The ATM90E26's 5000:1 puts it at ~4 W. This is the biggest single improvement v2 offers. |
| **You want per-unit phase calibration** | v1 compensates CT phase in hardware, fixed per batch. v2 can calibrate it per unit, per load level, in a register. |
| **You add solar / bidirectional measurement** | Sign handling and reactive power are cleaner on a register-programmable front end. |
| **You need a Pro / three-phase variant** | The ATM90E32 shares the family's architecture and register model, so the firmware work carries over. |

---

## 8.2 What actually changes

| | v1 (HLW8032) | v2 (ATM90E26) |
|---|---|---|
| Package | SOP-8, 1.27 mm | SSOP-28, 0.65 mm |
| Supply | 5 V | 3.3 V |
| Interface | UART, transmit only, 4800 baud | **SPI**, bidirectional |
| Crystal | none (internal 3.579 MHz) | **8.192 MHz + 2 × 27 pF** |
| Level shifter | Rls1/Rls2 required | **not needed** (3.3 V native) |
| Current-channel PGA | none | **1 / 4 / 8 / 16 / 24×** |
| Phase correction | `Rf2`/`Rf3` filter trim, fixed per batch | **register**, per unit |
| Dynamic range | ~400 : 1 (≈45 W floor) | **5000 : 1 (≈4 W floor)** |
| Calibration | firmware constants in NVS | registers written into the chip |
| Cost | ~US$ 0.27 | ~US$ 1.32 |
| Stock (at time of writing) | ~32,000 | **~230 ⚠️** |
| Daily energy error (modelled) | +0.48 % | **+0.19 %** |

**Net BOM change:** +US$ 1.15 per unit, +1 part.

### Component deltas

**Remove:** `Rls1`, `Rls2` (level shifter — no longer needed).

**Add:**

| Ref | Value | Package | Role |
|---|---|---|---|
| Y1 | Crystal, **8.192 MHz**, 18 pF load | HC-49S THT or 3225 SMD | Metering timebase. Frequency is not negotiable — the IC's energy constants assume it. |
| C10, C11 | 27 pF, **NP0/C0G** | 0805 | Crystal load caps: `2 × 18 − 2 × 5 = 26 pF → 27 pF`. Must be NP0 — X7R drifts and pulls the oscillator. |
| C9 | 100 nF X7R | 0805 | Second supply decoupling (the ATM90E26 has separate AVDD and DVDD pins). |

**Change:**

| Ref | v1 | v2 | Why |
|---|---|---|---|
| U2 | HLW8032, SOP-8 | **ATM90E26-YU-R**, SSOP-28 (LCSC C616398 / C145595) | The metering IC |
| Rb | 0.68 Ω | **~10 Ω** (verify) | ATM90E26's full scale is an order of magnitude higher |
| Rv5 | 150 Ω | **~330 Ω** (verify) | Same reason |
| Rf2, Rf3 | 1.5 kΩ | **1 kΩ** | Phase is corrected in a register now, so the filter goes back to plain anti-aliasing |
| C7, C8, FB1 | on the 5 V rail | on the **3.3 V** rail | ATM90E26 runs at 3.3 V |

### Pin assignment

| ESP32 pin | v2 net |
|---|---|
| IO5 | ATM90E26 CS (VSPI) |
| IO18 | SCK |
| IO19 | MISO |
| IO23 | MOSI |
| IO4 | IRQ (optional) |
| IO16 | ZX zero-cross (optional diagnostics) |

These are the pins v1 deliberately leaves free. **Route them to the metering
footprint area in the v1 layout even though v1 does not use them** — it costs
nothing and makes the v2 board a smaller change.

Tie **USEL (pin 12) to GND** to select SPI over UART.

---

## 8.3 What stays exactly the same

This is the important part, and it is why v2 is cheap:

- The **CT clamp, terminal block and install procedure** — unchanged.
- The **ZMPT101B voltage sensing chain** and `Rv1–Rv4` — unchanged.
- The **isolated PSU** (HLK-PM01 + AMS1117) — unchanged.
- The **ESP32 module, RTC, LEDs, button, programming header** — unchanged.
- The **isolation barrier, creepage rules and enclosure** — unchanged.
- The **10-turn calibration trick, golden-unit method and test jig** — unchanged.
- Your **server, data model and app** — unchanged, *provided* you followed the
  four v1 rules in [`docs/01-architecture.md`](01-architecture.md) §1.4
  (raw V/I/P logged, `hardware_revision` field, constants in NVS, same front
  end).

Realistically, v2 is a **partial re-layout of one corner of the board** plus a
firmware driver swap. Not a new product.

---

## 8.4 Calibration differences

v1 calibration produces firmware constants; v2 writes registers into the chip.

| | v1 | v2 |
|---|---|---|
| Voltage | `k_voltage` in NVS | `Ugain` register |
| Current | `k_current` in NVS | `Igain` register |
| Phase | `Rf2`/`Rf3` filter trim, fixed per batch | phase-compensation register, per unit |
| Survives a flash wipe? | **No** — constants live in NVS | Partially — registers live in the chip |

Two v2-specific gotchas:

- ⚠️ **Checksum registers.** The ATM90E26 maintains checksums over its
  calibration register banks and raises an error flag on a mismatch. After
  writing calibration values you must recompute and write those checksums.
  Confirm the exact register names and algorithm in the datasheet — a unit that
  silently refuses to meter because of a checksum mismatch is a miserable bug to
  find at unit 400.
- The full-scale analog input range must be confirmed from the datasheet before
  fixing `Rb` and `Rv5`, exactly as in v1. Published reference designs using the
  `SCT-013-000` clamp use a **12 Ω** burden, which implies a full scale in the
  hundreds of millivolts — consistent with the ~10 Ω starting value, but that is
  inference, not a quoted spec.

---

## 8.5 Drag-soldering SSOP-28 (the technique v1 does not need)

If you hand-build v2 prototypes, this is the one joint that needs real
technique. Reflow with a stencil handles it far better — see
[`docs/07-assembly-and-tooling.md`](07-assembly-and-tooling.md) §7.3.

1. Tack **one corner pin**. Check alignment under magnification against the
   footprint. Re-melt and nudge until every pin sits centred on its pad.
2. Tack the **opposite corner**. Check again. This is the last cheap chance to
   fix alignment.
3. **Flood the pins with flux** — gel or liquid no-clean, generously. Flux is
   what makes drag soldering work, not solder and not iron temperature.
4. Use a chisel or knife tip at ~320 °C (leaded) with a small amount of solder,
   and drag slowly along the row. Surface tension pulls solder onto the pads and
   off the gaps.
5. Bridges will happen. Add flux and drag again, or lift the excess with wick.
6. Inspect **every pin** under magnification.

Counterintuitively, **reflow makes fine pitch easier, not harder** — molten
paste self-centres each lead on its pad. If you have the stencil and hotplate,
SSOP-28 is a non-event.

---

## 8.6 Alternatives worth re-checking before you commit to v2

Do not assume the v1 analysis still holds. Two things to re-check:

1. **ATM90E26 stock.** It was ~230 pieces at ~US$ 1.32. Re-check before
   committing to a layout — that number was the main reason v1 went elsewhere.
2. **Does BL0942 have a phase-compensation register?** This was never resolved
   during the v1 work because every datasheet mirror was blocked. If it does,
   BL0942 may beat the ATM90E26 for your purposes: TSSOP-14 instead of SSOP-28,
   no crystal, cheaper, much better stock, and 0.1 % claimed accuracy over
   4000:1. **Open the datasheet, find the register map, search for a phase or
   angle register.** Ten minutes, potentially a better v2.
