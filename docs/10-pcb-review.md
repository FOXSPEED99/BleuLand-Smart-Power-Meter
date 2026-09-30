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
