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

---

# Spacing and isolation, measured in detail — 1 October 2026

Same file as Review 2. This pass measures the board outline, the holes, the
cross-layer overlap and the effect of solder fillets, which the earlier
numbers ignored.

## Clearance is a property of the assembled board, not the drawn one

Altium measures drawn copper. The standard applies after assembly. On a
hand-soldered through-hole pad the fillet grows roughly **0.4 mm radially**
past the pad edge, so any gap with a through-hole pad on both sides loses
about **0.8 mm** when you solder it.

No design rule check in any tool models this. You have to do it by hand.

| | drawn | soldered | reinforced needs |
|---|---|---|---|
| `F1` live pad ↔ `J1` unnetted pad | 5.62 mm | **4.82 mm** | 5.5 mm clearance |
| `F1` live pad ↔ `J1` `ANALOG_GROUND` pad | 6.34 mm | **5.54 mm** | 5.5 mm clearance |

`NetC5_1` is fused live. `J1` is the CT clamp connector — the wire the
installer handles. This is the worst gap on the board to get wrong, and as
built it fails.

### What each candidate fix actually buys

Simulated by translating `J1`'s pads and re-measuring:

| Change | New tightest mains → low voltage |
|---|---|
| Delete `J1`'s unnetted pad only | 6.34 drawn / **5.54 soldered** — 0.04 mm margin. Not enough. |
| Move `J1` 3 mm in −X | 6.71 drawn / 6.31 soldered |
| Move `J1` −3 mm **and redraw its two tracks** | 7.04 drawn / **6.64 soldered** |

The 6.71 mm in the middle row is an `ANALOG_GROUND` **track** at X 60.8 /
Y 95.7 that feeds `J1`. Dragging the connector without redrawing the trace
leaves that track where it is and gains almost nothing.

Afterwards the barrier's narrowest point is the ZMPT region — `T1`'s primary
pad against the `ANALOG_GROUND` and `NetC9_2` tracks at X 57 / Y 68 —
at 6.64 mm soldered against 5.5 mm required.

Alternative if `J1` is awkward: move `F1` 3 mm in +X. Its right clip lands at
X 90.25 and `P1`'s pad at X 91.71 is the same net, so nothing is violated.

## Mains to mains passes everywhere, fillets included

| drawn | soldered | ΔV across the gap | needs | margin |
|---|---|---|---|---|
| 2.48 | 1.68 | 114 V | 1.0 mm | +0.68 |
| 2.23 | 1.83 | 115 V | 1.0 mm | +0.83 |
| 3.43 | 2.63 | 230 V — `P1` L↔N | 1.5 mm | +1.13 |
| 3.18 | 3.18 | 230 V — `C5_1`↔`C5_2` | 1.5 mm | +1.68 |

Worst margin on the mains side is +0.68 mm. Nothing in the 47 kΩ block
needs to move.

The 3.43 mm at `P1` is set by the terminal block's 5.08 mm pitch, not by
anything you drew, and the block carries its own 300 V rating — so it is
covered by the component's approval. Two consequences: do not treat 3.4 mm
as a precedent for shrinking anything else, and inspect those two pins after
hand soldering, because that gap is the one place where a solder bridge is a
dead short across 230 V.

## Mains copper to board edge: 2.89 mm

Board outline is 75 × 75 mm, X 25.50–100.50, Y 25.50–100.50, with 2 mm
chamfered corners.

| distance to edge | net | what |
|---|---|---|
| 2.89 mm | `NetC5_2` | `P1` pad, X 96.8 / Y 95.7 |
| 2.96 mm | `NetC5_2` | track, X 96.8 / Y 93.4 |
| 3.35 mm | `NetC5_2` | `C5` pad, X 96.3 / Y 78.3 |
| 3.93 mm | `NetF1_1` | `P1` pad, X 91.7 / Y 95.7 |

Fine for the fab, which needs 0.3 mm. The point to absorb is that the whole
right-hand edge of the board — X 95–100 from Y 66 to Y 96 — is live.

- The enclosure wall is the insulation on that side, not your copper.
- No mounting screw, screw boss or cable entry on that edge.
- The board has to be held so it cannot slide into the wall.
- In a metal panel, that edge is 2.9 mm plus the wall thickness away from
  grounded steel.

## No mains copper overlaps low-voltage copper through the board

Checked every mains object against every low-voltage object on the opposite
layer: **zero overlap**, total area 0.00 mm². Correct as it stands, and it
means air and surface are the only insulation the numbers above have to
cover.

Protect this when you pour. A pour's default behaviour is to fill
everywhere, including under `T1`, under the HLK's AC half, and across the
barrier. Draw each pour's outline so it stops at the barrier rather than
letting the clearance rule carve it back — a clipped pour leaves slivers, a
pour drawn to the right shape does not.

## Mounting: two holes, diagonally opposite, 68 mm from the terminal block

Holes with no net: 2.2 mm at X 28.0 / Y 98.0 and X 97.5 / Y 28.0. That is
all of them.

`P1` sits at X 91.7–96.8 / Y 95.7 with no support within 68 mm. Torquing
4 mm² house wire into that terminal flexes the board, which cracks
through-hole joints and works the mains traces. Over 1,000 units it returns
as field failures that look random.

A screw hole there is not available — the corner is solid mains copper, and
the opposite free corner at X 28 / Y 28 is `U1` pin 1. Solve it in the
enclosure:

- Support boss under about X 93 / Y 93, directly beneath the terminal block.
  No screw, no hole, no clearance question: plastic against mains copper on
  the bottom layer is harmless inside a Class II box.
- Second boss at about X 45 / Y 30 for the opposite diagonal. **Not** at
  X 30 / Y 32 — that is inside the antenna zone, where plastic detunes the
  antenna as much as copper does.

## The rule set, in the order it has to be in

Altium applies the **first** matching rule. A MAINS ↔ All rule also matches
MAINS ↔ MAINS, which is what froze routing when the barrier rule sat on top.

| Priority | Name | Scope 1 | Scope 2 | Gap |
|---|---|---|---|---|
| 1 | `Full_Mains` | class `FULL_MAINS` | class `FULL_MAINS` | 3.0 mm |
| 2 | `Divider_Taps` | class `MAINS` | class `MAINS` | 1.5 mm |
| 3 | `Mains_to_World` | class `MAINS` | All | 6.5 mm |
| 4 | `Clearance` | All | All | 0.254 mm |

- `FULL_MAINS` = `NetF1_1`, `NetC5_1`, `NetC5_2` — the three nets actually at
  230 V.
- `MAINS` = those three plus `NetR5_1`, `NetR8_1`, `NetR10_1`, `NetR13_1`.

Anything rule 3 reports between 6.5 and 7.5 mm, inspect by hand: if both
sides are through-hole pads, add 0.8 mm before calling it passed.

## A slot will not fix the `J1` gap

Milling a slot through a barrier lengthens the **creepage** path — the
distance along the surface. **Clearance** is the straight line through air,
and a slot does not change it. The binding requirement here is clearance
(5.5 mm), not creepage (5.0 mm), so a slot buys nothing. Moving the
connector is the only fix.

Where a slot earns its keep is if the panel turns out dusty or humid enough
to push the design from pollution degree 2 to 3, when creepage becomes the
constraint. Cheaper insurance for that is conformal coating over the mains
zone, worth doing at 1,000 units for dust and condensation alone. It is not
a licence to shrink a gap — that needs a type test.

## Zone geometry

| | X | Y | copper area |
|---|---|---|---|
| mains | 59.7–97.6 | 65.5–96.6 | 266 mm² |
| low voltage | 26.3–97.7 | 27.0–99.6 | 602 mm² |

Board area 5,617 mm². The mains zone is a clean block in the top right; the
barrier is a straight line along X ≈ 59.7 and Y ≈ 65.5 everywhere except
where it jogs around `T1`, which is where its narrowest point is.

---

# Does the mains need top-layer tracks as well as bottom?

No. Bottom only. If you want more margin, buy it with 2 oz copper, not with a
second layer of tracks.

## What flows in the mains copper

All seven mains nets are 1.5 mm wide, all on the bottom layer, 167 mm of
track in total.

| Source | Current |
|---|---|
| HLK-5M05 input, 5 W out at ~72 % efficiency | 30.2 mA |
| `C5`, 0.1 µF X2 across L–N at 50 Hz | 7.2 mA |
| 47 kΩ divider chain, 188 kΩ total | 1.2 mA |
| `R4` MOV leakage | ~0.01 mA |
| worst case, simply added | **38.7 mA** |

A 1.5 mm track in 1 oz copper is 1.5 × 0.035 = **0.0525 mm²**, rated roughly
1.5–2 A for a 10 °C rise. That is **2.6 % utilisation**.

**No load current ever passes through this board.** The CT clamps around the
house cable externally and `P1` has exactly two pins — live-in and neutral —
with no pass-through. The 63 A figure describes the cable the clamp goes
around, not the copper. It never becomes a trace-width requirement.

DC resistance of the longest mains net, `NetC5_2` at 65.7 mm: 21.5 mΩ,
dropping 0.86 mV at 40 mA.

## The only event that stresses the copper

`R4` (14D471K) conducting a surge, along
`P1` → `F1` → `NetC5_1` → `R4` → `NetC5_2` → `P1`. For overvoltage category
III the design surge is the 4 kV / 2 Ω combination wave; with the MOV
clamping near 700 V that is about **1.6 kA for 8/20 µs**.

20 µs is adiabatic — all the I²R energy stays in the copper. The rise is
independent of track length, because resistance and heat capacity both scale
with length:

| Surge | 1 oz (35 µm) | 2 oz (70 µm) |
|---|---|---|
| 1.6 kA — cat III design level | **+93 °C** | +23 °C |
| 3 kA | +326 °C | +81 °C |
| 6 kA — the MOV's single-pulse rating | +1303 °C | +326 °C |

Temperature rise goes as **1/A²**: halve the copper area and the rise
quadruples. FR-4 resin starts degrading above roughly 250–300 °C.

## Why a parallel top track is the wrong fix

A parallel track doubles the area and cuts the rise 4×, the same as 2 oz
copper. The problem is the joint.

A 0.4 mm finished via with 25 µm plating has a barrel wall cross-section of
π × 0.4 × 0.025 = **0.0314 mm²** — 60 % of the 1.5 mm track, in a tube
surrounded by FR-4 with nowhere for heat to go. Same adiabatic sum on the
barrel:

| Surge | one via |
|---|---|
| 1.6 kA | **+259 °C** |
| 3 kA | +912 °C |

The via runs nearly three times hotter than the track it was meant to
reinforce. Matching the track would take three or four vias per transition,
and each one widens the mains copper where it sits — straight into the
6.5 mm barrier.

Beyond the thermal point, putting mains on two layers means:

- Every clearance check doubles. Today the barrier is a bottom-layer problem
  and the top layer carries mains **pads only**. That simplification is worth
  keeping.
- Top-layer mains tracks run between through-hole pads whose solder fillets
  are growing — the layer where the 0.8 mm goes.
- Exposed mains copper area doubles, the wrong direction for creepage and for
  dust or condensation bridging.

## Do this instead

**Order the board in 2 oz (70 µm) copper.** Same 4× surge improvement as
parallel copper, on every mains trace at once, with no layout work, no extra
vias and no effect on clearances.

It is safe for this board: 2 oz typically needs ≥0.2 mm minimum trace and
gap rather than 0.127 mm, and the narrowest track anywhere here is 0.6 mm
with a 0.254 mm default gap. `U2` is 1.27 mm pitch, far too coarse to care
about the extra etch taper.

Two related calls:

- **No pour on the mains side.** The only gain would be slight EMI shielding
  for the HLK, which is a certified module that filters its own input. The
  cost is a much longer barrier perimeter and far more mains copper for dust
  to bridge.
- **Keep the top layer empty inside the mains zone.** That emptiness is what
  makes the barrier a single-layer problem.

---

# The 39 silkscreen DRC errors — what to do with them

Measured from the same file. Counts here are silk-object-to-pad pairs, which
Altium groups more coarsely, so the totals differ from the error count in the
tool. The split is what matters.

## Ink actually on a pad opening: 4 spots, 2 components

| Component | Layer | Spots |
|---|---|---|
| `D1` | TopOverlay | 2 |
| `D2` | TopOverlay | 2 |

The LED outline circles cross their own pads. Nothing else on the board does.

## Merely closer than the rule, no ink on a pad: 138 spots, 34 components

| Gap | Components |
|---|---|
| 68 µm | `Y1` |
| 98 µm | `R12`, `R7`, `FB1` |
| 128 µm | `D1`, `D2` |
| 138 µm | `R5`, `R8`, `R10`, `R13` |
| 149 µm | `U2` |
| 155 µm | `C4` |
| **173 µm** | **27 components** — `C1`, `C2`, `C6`–`C12`, `R1`–`R17`, `D3`, `D4` |
| 199 µm | `IC1` |

Twenty-seven components sharing one figure to the micron is one library
convention, not 27 problems. The IPC-generated footprints place silk 6.8 mil
from the pad; Altium's default rule wants 10 mil.

## Solder mask slivers: zero

Every mask opening is clear of its neighbours. Pad **rotation** has to be
applied to get this right — the rotation is a double at offset 52 of the pad
record. Without it a 270°-rotated SOIC's pads appear to overlap and the check
reports six slivers on `U2` that do not exist.

## Two findings that are not silkscreen and are real

- **`J1`'s third pad has no annular ring at all**: 1.10 mm pad, 1.10 mm hole.
  The fab will flag it independently. Third reason to delete it, after "no
  net" and "closest low-voltage copper to the mains".
- **Both mounting holes are plated with floating copper**: 2.2 mm hole,
  2.5 mm pad, no net. Make them non-plated.

Annular rings everywhere else are fine — thinnest after `J1` are `IC1` and
`C3` at 175 µm, against a 100 µm floor.

## Why not fix the libraries

Silkscreen ink on a pad has exactly one failure mode: it stops solder
wetting. So the only question each error raises is whether ink will land on a
pad.

For the 138, it will not. The ink is 68–199 µm clear as drawn, fabs hold silk
registration to roughly ±100–150 µm, and JLCPCB and essentially every other
fab **automatically clip silkscreen that overlaps a mask opening** in CAM. The
worst realistic outcome is a slightly chopped outline, never a bad joint.

For the 4 on `D1`/`D2` it will, so the fab clips them and those LED outlines
come out with gaps. Cosmetic — but it is polarity marking on a
hand-assembled product, so fix it.

The cost of editing 34 footprints is not the half hour. It is forking 34
IPC-generated footprints away from their originals, after which every library
update, new board and BOM cross-check has to know about the fork. That is a
permanent tax to silence a cosmetic warning.

## What to do

1. Set `Silk To Solder Mask Clearance` to **0.05 mm** instead of 0.254 mm. The
   138 cosmetic spots go; the 4 real overlaps stay visible.
2. Fix `D1` and `D2` **on the PCB**, not in the library — nudge or shorten the
   two silk arcs that cross the pads.
3. Delete `J1`'s third pad.
4. Make both mounting holes non-plated.

## The real finding behind the 39 errors

None of the 39 was an unrouted net — but `C7`'s `ANALOG_GROUND` pad is
unrouted, proven by walking the copper. Altium's **batch** DRC has a per-rule
checkbox list and many rules ship unticked. Confirm these are ticked in
`Tools → Design Rule Check`:

- `Un-Routed Net` — would have caught `C7`
- `Clearance` — the mains barrier
- `Short Circuit`
- `Minimum Annular Ring` — would have caught `J1`
- `Hole To Hole Clearance`
- `Minimum Solder Mask Sliver`
- `Board Outline Clearance`

Read the rule names, not the error count. Thirty-nine errors in one cosmetic
rule is a single decision made once. One error in `Clearance` or
`Un-Routed Net` is a board that does not work, or one that hurts someone.
Run DRC at the end of every session — not for the silkscreen, but so the day
a `Clearance` error appears you see it that day.
