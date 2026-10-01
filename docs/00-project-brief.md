# BleuLand Smart Power Meter — project brief

A standalone handoff. Everything needed to pick the project up cold.

---

## What it is

A single-phase (230 V / 50 Hz) **non-invasive whole-house energy monitor**.

A split-core current transformer clamps around the incoming live conductor —
nothing is cut or rewired. An **HLW8032** metering IC reads current across a
0.68 Ω burden resistor and voltage from a **ZMPT101B** transformer fed through
a 4 × 47 kΩ divider, then reports over a 4800-baud serial link to an
**ESP32 DevKitC**, which uploads to the cloud over Wi-Fi, buffers readings
locally, and multiplies kWh by a user-entered price per kWh to estimate the
bill. A **DS1307** with a CR2032 keeps time through outages. An
**HLK-5M05** powers everything from the same mains.

Designed to hide inside a domestic distribution board. 75 × 75 mm two-layer
PCB, hand-assembled with soldering iron and hot-air station, 1,000-unit
production run, built in Syria.

## Signal chain

```
house live cable ──(clamped, not cut)── split-core CT
                                          │
          J1 (JST B2B-XH) ── D4 SMAJ5.0CA ─┤
                                          │
                      R16 0.68 Ω burden ──┴── R15/R17 1.5 kΩ ──> HLW8032 IP/IN
                                                C10 33 nF diff, C11/C12 10 nF

mains L ── P1 ── F1 fuse ── C5 0.1 µF X2 ── R4 MOV 14D471K
                   │
                   ├── PS1 HLK-5M05 ──> 5 V ── C3 470 µF, C4/C8 100 nF
                   │                         ├── FB1 ──> HLW8032 VDD (C6 100 nF, C7 10 µF)
                   │                         ├── DS1307 VCC
                   │                         └── ESP32 5 V pin ──> 3V3 ── C1 10 µF, C2 100 nF
                   │
                   └── R5/R8/R10/R13 4 × 47 kΩ ──> T1 ZMPT101B primary
                                   T1 secondary ── R14 300 Ω ── D3 SMAJ5.0CA
                                                 ── R12 1 kΩ, C9 33 nF ──> HLW8032 VP

HLW8032 TX ── R11 1 kΩ / R6 2 kΩ divider (5 V → 3.3 V) ──> ESP32 IO16
DS1307 ── R2/R3 4.7 kΩ pull-ups ──> ESP32 IO23 (SDA) / IO22 (SCL)
D1 green ── R1 330 Ω ──> IO19      D2 blue ── R9 330 Ω ──> IO18
R7 0 Ω: the single tie between ANALOG_GROUND and GND
```

44 components: 23 SMD on the bottom layer, 21 through-hole on top.

---

## Frozen decisions — do not re-open these

| Decision | Why |
|---|---|
| **One board, 75 × 75 mm** (2 mm chamfered corners) | an earlier conclusion that the isolation barrier forced ~100 × 100 mm and a two-board stack was wrong; the barrier is met at 75 × 75 |
| **Mains on the bottom layer only**, 1.5 mm wide | 39 mA steady state against a ~2 A track rating; see "mains copper" below |
| **No mains-side copper pour** | only gain would be slight HLK shielding; cost is a longer barrier perimeter and more mains copper for dust to bridge |
| **Keep the ZMPT101B** — do not replace it with a resistor divider alone | the HLW8032 reference design ties GND to neutral; with L and N swapped (common locally) the clamp cable and USB port would sit at 230 V |
| **`U2` pin 8 (HLW8032 RX) stays unconnected** | the datasheet calls it a reserved port not to be used, and Fig. 4 leaves it open |
| **1206 for passives**, 2512 where already used | hand-solderable; 0805 rejected as too small |
| **ESP32 DevKitC module on female headers**, not a bare chip or module | hand assembly, and the module carries its own PCB antenna |
| **Terminal blocks, not 3.5 mm jacks** | mains = KF128-5.08-2P; clamp = JST B2B-XH (`J1`) |
| **`R14` = 300 Ω** | scales the ZMPT secondary to use the HLW8032's ±495 mV voltage range instead of 37 % of it |
| **No fuse + surge thyristor on the clamp input** | mechanical exclusion (a connector mains cannot fit into) is the stronger fix; `D4` still covers surge |
| **DS1307 on IO23 / IO22**, HLW8032 TX on IO16 | all free of boot straps; IO12 in particular must never see a pull-up |
| **Overvoltage category III, pollution degree 2** | the unit lives inside a distribution board |
| **2 oz (70 µm) copper** | quadruples surge margin with no layout change |

## Insulation targets

Reinforced, cat III, PD2: **≥ 5.5 mm clearance / 5.0 mm creepage** between the
mains side and everything else. Design target **6.5 mm** for margin.

Mains-to-mains requirements scale with the voltage *across each gap*, not with
"both are mains". The 47 kΩ chain divides it: `NetF1_1`/`NetC5_1` 230 V,
`NetR5_1` 172.5 V, `NetR8_1` 115 V, `NetR10_1` 57.5 V, `NetR13_1` ≈ 0 V,
`NetC5_2` neutral.

**Clearance applies to the assembled board.** A hand-soldered through-hole pad
grows a fillet ~0.4 mm radially, so any gap with a through-hole pad on both
sides loses ~0.8 mm. No DRC in any tool models this.

---

## Where the board stands (measured, not estimated)

| Measurement | Value | Verdict |
|---|---|---|
| Mains → low voltage, drawn | 6.34 mm (5.62 mm counting `J1`'s stray pad) | fails once soldered |
| same, after fillets | **4.82 mm** vs 5.5 mm needed | **the one real failure** |
| Live ↔ neutral | 3.18 mm | passes cat III |
| Tightest mains ↔ mains | 2.23 mm at 115 V ΔV (needs ~1.0 mm) | passes, +0.68 mm worst margin |
| Mains copper → board edge | 2.89 mm | fine for fab; the whole right edge is live |
| Mains over low-voltage copper on the other layer | **0 mm²** | correct, protect this |
| Solder mask slivers | **0** | clean |
| Net connectivity | 27 of 28 nets fully routed | `C7` is not |
| Copper pours | **none** (`Polygons6` 0 bytes) | biggest electrical gap |
| Vias | 6 | follows from no pours |
| Mains current | ~39 mA of a ~2 A rating (2.6 %) | no load current ever crosses this board |
| 1.6 kA surge, 1 oz | +93 °C adiabatic | survivable; 2 oz gives +23 °C |

`T1` is correctly oriented: primary pins on the Y 71.20 row, secondary on
Y 61.20, 8.49 mm apart. Copper under the HLK is correctly segregated —
mains only under its AC half, low voltage only under its DC half.

---

## The remaining work, in order

### 1. Clearance rules — do this first
The file contains exactly **one** clearance rule: `All / All` at 10 mil. The
barrier is being checked by nothing. Create four rules, in this priority order
(Altium applies the first match, and MAINS↔All also matches MAINS↔MAINS):

| Pri | Name | Scope 1 | Scope 2 | Gap |
|---|---|---|---|---|
| 1 | `Full_Mains` | class `FULL_MAINS` | class `FULL_MAINS` | 3.0 mm |
| 2 | `Divider_Taps` | class `MAINS` | class `MAINS` | 1.5 mm |
| 3 | `Mains_to_World` | class `MAINS` | All | 6.5 mm |
| 4 | `Clearance` | All | All | 0.254 mm |

`FULL_MAINS` = `NetF1_1`, `NetC5_1`, `NetC5_2`.
`MAINS` = those three plus `NetR5_1`, `NetR8_1`, `NetR10_1`, `NetR13_1`.

Anything rule 3 reports between 6.5 and 7.5 mm: check by hand, add 0.8 mm if
both sides are through-hole pads.

### 2. Connect `C7`
Its `ANALOG_GROUND` pad at X 49.72 / Y 59.10 is floating, so the HLW8032's
only decoupling is `C6`'s 100 nF. One 0.6 mm track, 2.8 mm, to `C6`'s ground
pad at X 52.51 / Y 59.24.

### 3. Fix the barrier at `J1`
- Delete `J1`'s third pad at X 58.25 / Y 98.25 — no net, off the 2.5 mm XH
  pitch, and a 1.10 mm hole in a 1.10 mm pad (100 %, so it also fails the
  `HoleSize` rule's 80 % maximum).
- Move `J1` **3 mm in −X** and redraw both its tracks with it. Moving the part
  without the tracks gains almost nothing.
- Result: 7.04 mm drawn / 6.64 mm soldered. The new limit becomes the ZMPT
  region at X 57 / Y 68.

Alternative: move `F1` 3 mm in +X instead; its right clip lands at X 90.25 and
`P1`'s pad at X 91.71 is the same net.

### 4. Clear the ESP32 antenna
The antenna end is proven by pin map: `U1` pin 1 (3V3) at X 27.73 / Y 27.80
and pin 38 (GND) at X 27.73 / Y 53.20 are the antenna-end pins; pin 19 (5 V,
beside the USB socket) is at X 73.45. The antenna sits over roughly
X 26–33, Y 27.8–53.2, and the board edge is only at X 25.5.

Currently inside X 25.5–31: 3.55 mm² top `GND`, 4.00 mm² bottom 3V3,
3.30 mm² bottom SDA.

- Keepout X 25.5–34, Y 26–55, all layers.
- Route pins 1, 37, 38 straight inward (+X). Nothing runs laterally.
- Slot the FR-4 out: X 25.5–33, Y 31–50, leaving 2 mm rails under each pad
  row. The dielectric detunes the antenna as much as copper does.

### 5. Ground pours
Two pours, `GND` and `ANALOG_GROUND`, both layers, joined only at `R7`.
**Draw each outline so it stops at the barrier** — do not rely on the
clearance rule to carve it back, which leaves slivers. Thermal relief spokes
on through-hole ground pads, for hand soldering.

Before placing stitching vias, change `RoutingVias` from its current 0.711 mm
hole / 1.27 mm pad to **0.3 mm hole / 0.6 mm pad**.

### 6. Smaller items
- `C4` is a 100 nF on a 5.08 mm through-hole film-cap footprint
  (`CAPRR508W50L508T318H762`). Change to 1206.
- Both mounting holes (2.2 mm, at X 28.0 / Y 98.0 and X 97.5 / Y 28.0) are
  plated with a 2.5 mm pad on no net. Make them **non-plated**.
- Set `SilkToSolderMaskClearance` to **0.05 mm** instead of 0.254 mm. That
  clears ~138 cosmetic warnings and leaves the 4 real ones — silk arcs on `D1`
  and `D2` that cross their own pads. Fix those two **on the PCB**, not in the
  library; do not fork 34 IPC footprints over a 173 µm library convention.
- Ignore the I1P/I1N length mismatch (24.1 vs 19.7 mm). At 50 Hz that is
  ~4 mΩ and 4 nH. They already run as a pair.

### 7. Enclosure
`P1` sits at X 91.7–96.8 / Y 95.7 with **no mounting support within 68 mm**.
Torquing house wire into that terminal will flex the board and crack joints.
A screw hole there is impossible — solid mains copper — and the opposite free
corner is `U1` pin 1. So:
- Printed support boss under ~X 93 / Y 93, directly beneath the terminal block.
- Second boss at ~X 45 / Y 30. **Not** X 30 / Y 32 — inside the antenna zone.
- The right-hand board edge is live: no screw, boss or cable entry there, and
  the board must be held captive so it cannot slide into the wall.

### 8. Order
2 oz (70 µm) copper. Safe here: 2 oz wants ≥0.2 mm trace and gap; the
narrowest track is 0.6 mm and the default gap 0.254 mm. `U2` is 1.27 mm pitch.

---

## Not started yet

- **Firmware.** Read the HLW8032 at 4800 baud, accumulate kWh, apply the
  user's price per kWh, upload to cloud, buffer locally through outages, read
  the DS1307.
- **Enclosure CAD.** 3D printed. Needs the free depth in the target breaker
  panel measured — still unknown.
- **Calibration procedure.** A per-unit `k_current` constant cancels resistor
  **tolerance**. It cannot cancel **temperature coefficient** — which is why
  `R16` must be a low-tempco part. Metal oxide at ±200–300 ppm/°C drifts
  0.9–1.4 % over a 45 °C panel swing, and over-reports in summer when the air
  conditioning load is highest.

## Working habits that paid off

- Run DRC at the end of every session and **read the rule names, not the error
  count**. 39 errors in one cosmetic rule is one decision; one error in
  `Clearance` or `Un-Routed Net` is a board that does not work.
- Subtract 0.8 mm from any gap where both sides are through-hole pads.
- Clearance between two points scales with the voltage between *those two
  points*.
- A milled slot raises creepage but **not** clearance, so it cannot fix a
  clearance-limited gap.
