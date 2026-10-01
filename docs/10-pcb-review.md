# PCB review — `Energy-Meter.PcbDoc`, 30 September 2026

Geometry extracted directly from the file: **board 75.0 × 75.0 mm, 317 copper
tracks (268 bottom, 49 top), 6 vias, 0 copper pours, 44 components placed
(21 top, 23 bottom).**

> ⚠️ **Caveat on the numbers below:** the clearances are measured
> **track-to-track only**. Pad geometry could not be parsed, so where a pad is
> involved the real clearance may be **worse**, never better. Treat every figure
> as an upper bound.

---

# 🔴 Two safety violations — fix these before anything else

## 1. Live-to-neutral clearance is **1.33 mm**

| | |
|---|---|
| Measured | **1.33 mm** |
| Required at 230 V, overvoltage category III | **~3.0 mm** |
| Worst pair | `NetC5_2` (neutral) ↔ **`NetF1_1`** (live, **before the fuse**) |

**The worst possible pair.** `NetF1_1` is on the **unfused** side of the circuit —
it comes straight from the mains terminal. A flashover there is not current
limited by anything on this board; it is limited only by the house breaker,
which takes about 10 ms to notice.

## 2. Mains-to-low-voltage clearance is **3.95 mm**

| | |
|---|---|
| Measured | **3.95 mm** |
| Required | **8.0 mm** |
| Worst pair | `NetR10_1` (a node in the 47 kΩ chain) ↔ `ANALOG_GROUND` |

**This is the isolation barrier**, and it is breached by more than half. That
barrier is the only thing keeping mains potential away from the side of the
board a person can touch — the clamp cable, the low-voltage circuitry, the
module.

---

# 🔴 Why the design rule check did not catch either of them

**The file contains exactly one clearance rule:**

> `All ↔ All — 10 mil (0.254 mm)`

That is the Altium factory default. **There are no net classes and no mains
clearance rule at all.**

So the board passes its own DRC while breaching the barrier by 4 mm — because
1.33 mm comfortably clears a 0.254 mm requirement.

> ⭐ **Do not hunt these by hand. Configure the rules and let the DRC find them.**

### Set this up first — about thirty minutes

**Create a net class `MAINS`** containing every mains-referenced net:

> `NetF1_1`, `NetC5_1`, `NetC5_2`, `NetR5_1`, `NetR8_1`, `NetR10_1`, `NetR13_1`

**Then three clearance rules, in this priority order:**

| Priority | Scope 1 | Scope 2 | Gap |
|---|---|---|---|
| **1** | `InNetClass('MAINS')` | `All` | **8 mm** |
| **2** | `InNetClass('MAINS')` | `InNetClass('MAINS')` | **3 mm** |
| 3 | `All` | `All` | 0.2 mm |

Run the DRC after that and it will list every violation, including the ones
involving pads that this review could not see.

---

# 🔴 There is no copper pour anywhere

**Zero polygons in the file.** Both grounds are routed as 0.6 mm traces:

| Net | Total trace length | Layers |
|---|---|---|
| `GND` | **191 mm** | 47 bottom, 9 top |
| `ANALOG_GROUND` | **109 mm** | 45 bottom, 5 top |

A **191 mm-long, 0.6 mm-wide** return path on a board that carries 500 mA WiFi
bursts and measures a **20 mV** signal. Every ground rule in
[`09-layout-working-rules.md`](09-layout-working-rules.md) is still outstanding.

# 🔴 Only 6 vias, and the top layer is nearly empty

**268 tracks on the bottom against 49 on the top.** This is effectively a
single-sided board with a two-layer stack-up paid for.

**The top layer is free, empty, and is exactly where the ground pour belongs** —
it is the return path for everything routed underneath it.

---

# 🟠 The analog pair is not routed as a pair

| Net | Length | Layer |
|---|---|---|
| `NetC10_1` (`I1P`) | **25.3 mm** | bottom |
| `NetC10_2` (`I1N`) | **18.5 mm** | bottom |
| **Difference** | **6.8 mm — a 27 % mismatch** | |

Both on the bottom, which is right. But a 27 % length difference means they are
**not running together**.

### Why this matters — and it is not propagation delay

At 50 Hz, 6.8 mm of copper is nothing in time. **The point is common-mode
rejection.**

The chip measures the **difference** between those two nets. If they run side by
side, noise from the switching supply and the WiFi burst couples into **both**
equally and subtracts to zero. If they take different paths, **whatever reaches
one and not the other stops being noise and becomes signal.**

**Fix:** route them side by side, same layer, parallel for their whole length,
equal length, with ground on both sides and nothing crossing between them.

---

# ✅ What is already right

- **Board is 75.0 × 75.0 mm** — matches the target, inside the price tier
- **Mains tracks are 1.5 mm, signal tracks 0.6 mm** — good discipline, and the
  mains width is well above what 150 mA needs
- **21 components on top, 23 on the bottom** — the surface-mount-to-bottom plan
  is actually done
- **12 board cutouts / keepout regions** are present
- **Every net has copper on it** — nothing is completely unrouted

---

# Do them in this order

**The order matters — several of these invalidate each other if done backwards.**

1. **Set up the net class and the three clearance rules.** Thirty minutes, and
   it turns the rest of this list into a DRC report you can work from.
2. **Fix the two clearance violations.** Expect this to force the mains section
   to move, and possibly to grow the board. **Do it before pouring.**
3. **Pour the grounds** — `GND` and `ANALOG_GROUND`, both layers, top layer as
   solid as possible, joined only at `R7`.
4. **Add stitching vias**, every 5–10 mm, especially around the analog block.
5. **Re-route `I1P` and `I1N` as a matched pair.**
6. **Re-run the DRC** and confirm it is clean against the new rules.

⚠️ **Step 2 before step 3.** Pouring first and then moving the mains section
means pouring twice.

---

# Review 2 — 1 October 2026

Measured on the file uploaded 1 October, 11:30. Board still **75 × 75 mm**,
copper extent 69.8 × 70.7 mm, 335 copper tracks (276 bottom / 59 top),
6 vias, 143 pads, 44 components (23 bottom, 21 top).

This pass measured **pads, vias and tracks together**, not just tracks. Pads
are the biggest copper on the mains nets, so the earlier track-only numbers
were optimistic.

## ✅ The isolation barrier now passes

| Measurement | Review 1 | Now | Required |
|---|---|---|---|
| Mains → low voltage (nets) | 3.95 mm | **6.34 mm** | 5.5 mm clearance / 5.0 mm creepage |
| Mains → low voltage (incl. J1's unnetted pad) | — | 5.62 mm | as above |
| Live ↔ neutral (`NetC5_1` ↔ `NetC5_2`) | 1.33 mm | **3.18 mm** | 1.5 mm cat II / 3.0 mm cat III |

`T1` is the reason. Its primary pins (`NetC5_2`, `NetR13_1`) now both sit on
the Y 71.20 row and its secondary pins (`NetD3_1`, `ANALOG_GROUND`) both on
the Y 61.20 row — 8.49 mm pad to pad. In Review 1 the primary and secondary
rows were tangled, which is where the 3.95 mm came from.

## ✅ Mains-to-mains is fine — the required gap scales with the voltage across it

A 1.5 mm or 3.0 mm blanket rule is wrong, because clearance is a function of
the voltage **between the two points**, not of the fact that both are on the
mains side. The 47 kΩ chain divides it down:

| Net | Volts vs neutral |
|---|---|
| `NetF1_1`, `NetC5_1` | 230 |
| `NetR5_1` | 172.5 |
| `NetR8_1` | 115 |
| `NetR10_1` | 57.5 |
| `NetR13_1` | ≈0 |

The tightest gap on the board is 2.23 mm, between `NetC5_1` and `NetR8_1` —
115 V apart, which needs about 1.0 mm. Every mains pair has positive margin.
**Nothing in the 47 kΩ block needs to move.**

## ✅ Copper under the HLK-PM01 is correctly segregated

| Zone | What is routed there |
|---|---|
| AC half, X 78–98 / Y 55–72 | mains only (`NetC5_1`, `NetC5_2`) |
| DC half, X 78–98 / Y 36–55 | low voltage only (`NetC3_P`, `GND`) |

## 🔴 1. `C7`'s ground pad is not connected to anything

A connectivity check — every pad of every net, walked through tracks, vias
and overlapping pads — comes back clean for 27 of 28 nets. `ANALOG_GROUND`
comes back as **two islands**:

```
island A: T1 J1 C9 R14 D3 C6 U2 C12 D4 R16 R7 C11 R17
island B: C7
```

`C7` is the 10 µF bulk cap on the HLW8032's VDD rail (`C6` 100 nF in
parallel with it, both fed through `FB1`). Its ground pin at X 49.72 /
Y 59.10 is floating, so the only decoupling the metering chip actually has
is `C6`.

Fix: one 0.6 mm track from X 49.72 / Y 59.10 to `C6`'s ground pad at
X 52.51 / Y 59.24. 2.8 mm.

## 🔴 2. `J1`'s third pad sits 5.62 mm from the fuse

`J1` is a 2-circuit XH. Pads 1 and 2 are at X 54.15 and X 56.65 — 2.5 mm
pitch, correct. There is a **third pad at X 58.25 / Y 98.25 with no net**,
off the pitch, so it is a footprint artifact rather than a pin. It is the
closest low-voltage copper to the mains: 5.62 mm from `F1`'s live pad at
X 64.75 / Y 95.25.

5.62 mm still clears the 5.5 mm reinforced minimum, but by 0.12 mm — less
than the fab tolerance plus the solder fillet that will grow on a
through-hole pad.

Fix, do both:
1. Delete that pad from the footprint.
2. Move `J1` 3 mm in −X. `R16`'s pad at X 47.50 / Y 98.00 is the nearest
   obstacle, so there is room.

Minimum afterwards: 6.58 mm.

## 🔴 3. There is copper under the ESP32 antenna

Which end of `U1` the antenna is on is settled by the pin map, not by
eyeballing the module: pin 1 (3V3) is at X 27.73 / Y 27.80 and pin 38
(GND3) at X 27.73 / Y 53.20, while pin 19 (5 V, next to the USB socket) is
at X 73.45. On a DevKitC, 3V3 and that GND are the two antenna-end pins.
**So the antenna is at the X 27.73 end**, sitting over roughly X 26–33,
Y 27.8–53.2. The board edge is at X 25.5, so almost none of it overhangs.

Copper inside X 25.5–31:

| Layer | Net | Area |
|---|---|---|
| Top | `GND` | 3.55 mm² |
| Bottom | `NetC1_1` (3V3) | 4.00 mm² |
| Bottom | `NetIC1_5` (SDA) | 3.30 mm² |

Fix:
1. Keepout over X 25.5–34, Y 26–55, all layers.
2. Route pins 1, 37 and 38 straight inward (+X) out of that band. Nothing
   may run laterally across it.
3. Cut the FR-4 out between the two header rows — a slot from about
   X 25.5 to X 33, Y 31 to Y 50, leaving 2 mm rails under each pad row. The
   dielectric detunes the antenna as much as the copper does.

## 🟠 4. Still no copper pour

`Polygons6` and `Fills6` are both **0 bytes**. `GND` is 190 mm of 0.6 mm
trace, `ANALOG_GROUND` is 114 mm. Unchanged from Review 1, and now the
largest remaining electrical weakness. Two pours, both layers, joined only
at `R7`.

## 🟠 5. `C4` is a through-hole film-cap footprint

`C4` is a 100 nF on the 5 V rail, sitting on `CAPRR508W50L508T318H762` —
a 5.08 mm radial box. Change it to 1206 so it solders in the same pass as
the other 1206s and frees ~30 mm² of top side.

## 🟢 6. The I1P/I1N length mismatch does not matter

24.1 mm vs 19.7 mm. At 50 Hz, 4.4 mm of 0.6 mm trace is nothing — about
4 mΩ and 4 nH. Do not spend layout effort on it. What matters is that the
two run side by side as a pair so that interference arrives on both
equally, and they do.

## Correction to the board-size advice

Earlier in this project I worked out that a 6.5 mm barrier would force the
board to about 100 × 100 mm and recommended splitting it into two stacked
boards. **That was wrong.** I added the mains-zone and low-voltage-zone
areas as if they could not interleave; they can, and the barrier is a line
between them rather than a border of empty board. The barrier is met at
75 × 75 mm.

One board. 75 × 75 mm. The two-board split and the panel-depth question
that went with it are both closed.

## Do them in this order

1. Connect `C7`'s ground pad. One track, 2.8 mm.
2. Delete `J1`'s unnetted pad and move `J1` 3 mm in −X.
3. Clear the antenna band, then slot the FR-4.
4. Change `C4` to 1206.
5. Pour `GND` and `ANALOG_GROUND`, both layers, single tie at `R7`.
6. Stitch vias along the pour boundary.
