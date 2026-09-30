# Schematic review — `Energy-Meter.SchDoc`

**Reviewed:** 27 September 2026, before PCB layout starts.
**Method:** the netlist was rebuilt from the schematic geometry — 45 components,
146 pins, 66 wires, 62 nets — and every net compared against
[`02-connections.md`](02-connections.md).

---

## Verdict

**The circuit is right.** Every block is wired exactly as specified, including
all three of the things the documentation calls out as easy to get wrong. The
problems below are about **parts and packages**, not about the design.

**Do not start PCB layout until the three 🔴 items are fixed** — two of them
would waste the whole board order.

---

## ✅ Verified correct

| Check | Result |
|---|---|
| Mains in → fuse → live | `P1.1 → F1 → C5, PS1.AC1, MOV, 47 k chain` ✓ |
| **MOV downstream of the fuse** | ✓ |
| Four 47 kΩ in series | `R5 → R8 → R10 → R13 → T1.1` ✓ |
| ZMPT secondary → 150 Ω + TVS + 1 kΩ | ✓ |
| Voltage channel → `U2.VP` with 33 nF | ✓ |
| Clamp → fuse → burden → filters | ✓ **exactly as specified** |
| Current channel symmetry | Both 1.5 kΩ present, `R15`→`IP`, `R17`→`IN` from AGND ✓ |
| 33 nF across `IP`–`IN`, 10 nF each to AGND | ✓ |
| **I²C pull-ups to 3V3, not 5 V** | `R2, R3 → U1.J2_1 (3V3)` ✓ **the critical one** |
| **Battery straight to VBAT, no divider** | `BT1.POS → IC1.3` ✓ |
| Crystal on X1/X2, no load caps | ✓ correct for DS1307 |
| Single-point ground link | `R7: AGND ↔ GND` ✓ |
| Ferrite isolating the meter chip supply | `FB1 → C6, C7 → U2.VDD` ✓ |
| 5 V → 3.3 V level shift on TX | `U2.TX → 1 k → node → 2 k → GND`, node → IO16 ✓ |
| ESP32 pins used | 3V3, EXT_5V, GND, IO16, IO21, IO22, IO25, IO26 — **matches the docs exactly** ✓ |
| Decoupling | 4 × 100 nF, 2 × 10 µF, 470 µF — matches the parts list ✓ |

**Nothing is miswired.** That is the hard part and it is done.

---

## 🔴 Must fix before laying out the board

### 1. `P1` and `P2` are the same part — the safety interlock is gone

Both terminal blocks are **TE 282837-2**, a 5.08 mm 2-position block. That means
**a mains wire fits the clamp terminal**, which is the exact accident
[`06-clamp-input-protection.md`](06-clamp-input-protection.md) exists to prevent.

**Fix:** `P2` (clamp) becomes a **2.54 mm** block — **KF128-2.54-2P**, LCSC
C474920. Keep `P1` at 5.08 mm — **KF128-5.08-2P-AA**, LCSC C474952.

This also saves money: TE blocks are roughly US$ 1–2 each against US$ 0.10 for
the KF128 — about **US$ 2,000–4,000 across 1,000 units** for 2 connectors.

### 2. The footprints are 2512 and 1206, but the whole parts list is 0805

Fifteen of the sixteen resistors use **2512** footprints
(`FP-AC2512`, `FP-CRCW2512`, `FP-RMCF2512`). Every part number in
[`parts-to-buy.md`](../hardware/parts-to-buy.md) — C17513, C4310, C17604,
C17673, C17471, C17477 — is **0805**.

**An 0805 part cannot bridge a 2512 pad pair.** The gap is about 4 mm; the part
is 2 mm long. If you order the parts list against this board, **nothing fits.**

It also costs size: 2512 instead of 0805 on fifteen resistors is about
**322 mm² of extra board** — roughly **10 % of a 60 × 55 mm board**, on a
product whose main requirement is fitting inside a breaker panel.

**Fix:** change the resistor footprints to **0805**, and the capacitors from
1206 to **0805**.

**One deliberate exception: keep `R16` (0.68 Ω) as `FP-CSRN2512`.** That is a
Stackpole current-sense part, and it is a **better** choice than the 1206 in the
parts list — low temperature coefficient is exactly what that position needs.
Update the parts list to match the board here, not the other way round.

### 3. The surge thyristor is missing

There is no **SMP100LC-65** (LCSC C2649282) on the clamp input. Without it the
burden resistor is the only thing across the terminals, and mains on those
screws puts hundreds of joules into the board.

**Fix:** add it between `CLAMP+` (the `F2.1 / R16.2 / D4.2 / R15.1` node) and
**ANALOG_GROUND**. It is a two-terminal SMB part — same shape as `D3`/`D4`.

---

## 🟠 Should fix

### 4. The 47 kΩ mains resistors are surface-mount

`R5`, `R8`, `R10`, `R13` sit across mains and use `FP-AC2512` — generic thick
film. Section 7b of the parts list calls for **through-hole metal film**: a long
body, and a failure mode that goes **open** rather than arcing across the part.

This is a deliberate decision in the documentation, so changing it is your call
— but change it knowingly, not by accident.

### 5. Two of the three ESP32 ground pins are unconnected

`J3_1` is connected. **`J2_14` and `J3_7` are not.** The 5 V feed enters on
`J2_19`, so the supply return currently has to cross the module to reach the one
ground pin on the other header.

**Fix:** connect all three. Costs nothing, and gives the return current a short
path.

### 6. `U2.8` (HLW8032 `RX`) is left floating

`U2.7` (`PF`) floating is fine — it is an optional output. **`RX` is an input**,
and a floating CMOS input can sit mid-rail, draw current and pick up noise.

**Fix:** check the HLW8032 datasheet for the recommended idle state and tie it
through a resistor. At minimum, put an unpopulated resistor footprint to 5 V and
one to GND so it can be set later without a respin.

### 7. `C4` is a through-hole ceramic on a decoupling position

`C4` is `AR215C104K4R` on a 5.08 mm radial footprint, while `C2`, `C6` and `C8`
are SMD. Section 8 of the parts list explains why decoupling capacitors must be
surface-mount: leads are inductance, and that is the one thing decoupling exists
to remove.

**Fix:** make `C4` 0805, the same as the other three.

---

## 🟡 Worth doing, not blocking

| # | Item | Note |
|---|---|---|
| 8 | `C3` is 470 µF **10 V** | Parts list says **16 V**. 10 V on a 5 V rail works, but 16 V was chosen for lifetime derating |
| 9 | `PS1` is **HLK-5M05**, parts list says **HLK-PM01** | 5 W instead of 3 W — more headroom, slightly larger. Fine, but update the parts list so the BOM matches |
| 10 | Two 5 × 20 mm fuse holders | `F1` and `F2` both use holder 4628. Field-replaceable is nice, but two of them eat real board area. Consider a small SMD fuse for `F2` (250 VAC rated) |
| 11 | Only two net labels in the whole sheet | `ANALOG_GROUND` and `GND`. Everything else is bare wire. Adding labels for **5V, 3V3, CLAMP+, IP, IN, VP** costs minutes and makes layout and future review far easier |
| 12 | No power port symbols | Same point as above |

---

## Fix order

1. `P2` → 2.54 mm terminal block ← **safety**
2. All resistor and capacitor footprints → 0805 (keep `R16` at 2512) ← **or nothing fits**
3. Add the SMP100LC-65 surge thyristor
4. `R5`, `R8`, `R10`, `R13` → through-hole, or record the decision to keep SMD
5. Connect `J2_14` and `J3_7` to GND
6. Resolve `U2.8` (RX)
7. `C4` → 0805
8. Add net labels
9. Re-run **Update PCB from Schematic** — then start layout

**Items 1–3 are the ones that cost money if missed.**

---

# Review 2 — 30 September 2026

Netlist rebuilt from the updated schematic: **44 components, 59 nets.** All 44
are placed on the PCB.

## ✅ Fixed since review 1

| # | Was | Now |
|---|---|---|
| **1** | Both terminal blocks the same part | **Clamp is a JST-XH (`B2B-XH-A`)** — see below |
| **4** | 47 kΩ mains resistors surface-mount | **Through-hole axial** `AXIAL_L9.0-D3.2_P12.70` ✓ |
| **5** | Two of three ESP32 grounds unconnected | **All three connected** — pins 14, 32, 38 ✓ |

## ✅ The new pin assignment is clean

| Signal | Pin | |
|---|---|---|
| SCL | IO22 | ✓ safe |
| SDA | IO23 | ✓ safe |
| Metering chip serial | IO16 | ✓ safe |
| Green LED | IO19 | ✓ safe |
| Blue LED | IO18 | ✓ safe |

**No strapping pins, no input-only pins.** IO12 avoided. Nothing here can stop a
board booting.

## ⭐ The JST-XH is a better fix than the one I recommended

I suggested a 2.54 mm terminal block to make a mains wire physically not fit.
**A JST-XH does that job harder:** the contact is crimped inside a polarised,
latching housing, and there is no opening a stripped mains conductor can be
pushed into at all.

### So removing the clamp fuse (`F2`) is now defensible

`F2` and the surge thyristor existed for **one accident: mains wired into the
clamp input.** With a crimped JST housing that accident is not merely
discouraged, it is **not possible**.

**Recorded as a deliberate decision, not an omission.** The mechanical exclusion
replaced the electrical protection, and mechanical exclusion is the stronger of
the two.

**`D4` (SMAJ5.0CA) still covers the remaining real risk** — static and surge
coupling onto a 1–2 m clamp cable running inside a panel full of switching.
That one must stay.

### ⚠️ But it adds an assembly step that needs costing

The clamp's moulded plug is cut off, and the two wires now need **crimped JST-XH
contacts in a housing** instead of going under a screw.

| | |
|---|---|
| Crimp contacts (×2) + housing | ~US$ 0.05 per unit |
| Crimp tool | ~US$ 25, once |
| Time | ~30 s per unit → **~9 hours over 1 000 units** |

A proper crimp is **more reliable than a screw terminal** long-term — it is
gas-tight and cannot loosen. But budget the tool and the hours, and **buy a real
ratcheting crimper**, not pliers; a bad crimp is an intermittent connection that
will not show up until the device is in a wall.

💡 **Cheaper alternative:** buy pre-made JST-XH pigtails and solder them to the
clamp wires with heatshrink. No crimp tool, no crimp skill, and probably faster.

## 🔴 Blocking — do these before the next PCB update

### 1. Two components are unannotated: `J?` and `U?`

The clamp connector and the ESP32 module both still have **`?`** designators.

Altium cannot run a clean engineering change order or produce a correct bill of
materials with unannotated parts, and the PCB will not track them properly.

**Run Annotate. Thirty seconds, and it is blocking everything downstream.**

### 2. Nine resistors are still on 2512 footprints

The package decision was **1206**. Still on 2512:

> `R1`, `R2`, `R3`, `R6`, `R7`, `R9`, `R11`, `R15`, `R17`

Already correct: `R12` and `R14` (1206), `R5`/`R8`/`R10`/`R13` (through-hole),
and **`R16` stays 2512 on purpose** — the Stackpole current-sense part.

Leaving these mixed means the board and the parts list still describe different
products.

## 🟠 Still open from review 1

| # | Item |
|---|---|
| **6** | **`U2.8` (HLW8032 `RX`) is still floating.** `PF` on pin 7 floating is fine — it is an output. `RX` is an input; give it a pull resistor, or at least an unpopulated footprint to 5 V and to ground |
| **7** | **`C4` is still through-hole** (`CAPRR508W50L508T318H762`) while `C2`, `C6`, `C8` are 1206. It is a decoupling capacitor — leads are inductance |

## Order of work

1. **Annotate** — clears `J?` and `U?`
2. **Nine resistors → 1206**
3. `C4` → 1206
4. Resolve `U2.8`
5. Update PCB from schematic, then carry on with layout
