# 5. PCB Layout and Enclosure

The schematic decides whether the circuit *can* work. The layout decides whether
it *does* work, and whether it is safe. On a mains-connected measurement product,
layout is not cosmetic.

---

## 5.1 Board specification

| Parameter | Value | Why |
|---|---|---|
| Layers | 2 | Sufficient. A 4-layer board would give a better ground plane but triples the PCB cost at 1,000 pieces. |
| Size | ~50 × 45 mm | Driven by the HLK-PM01 (34 × 20 mm) and the ESP32 module (18 × 25.5 mm). |
| Thickness | 1.6 mm | Standard, rigid enough for screw terminals. |
| Copper | 1 oz (35 µm) | Currents are tiny; this is about mechanical robustness. |
| Surface finish | **ENIG preferred**, HASL acceptable | ENIG gives dead-flat pads, which makes drag-soldering the 0.65 mm SSOP-28 noticeably easier. Worth the small premium when you will do it 1,000 times. |
| Solder mask | Any colour; **white silkscreen must be legible** | Assemblers will read it 1,000 times. |
| Special | **Routed slot** on the isolation barrier | See §5.2. |

---

## 5.2 The isolation barrier — the most important part of the layout

Draw a single straight line across the board. Mains on one side, SELV on the
other. Nothing crosses it except the three components that are *designed* to
cross it: **PS1** (HLK-PM01), **T1** (ZMPT101B), and nothing else.

```
 ┌──────────────────────────────────────────────────────────┐
 │  MAINS SIDE                  ║                           │
 │  ┌────┐ ┌──┐                 ║      ┌──────────────┐     │
 │  │ J1 │ │F1│  RV1  C1        ║      │   ATM90E26   │  Y1 │
 │  │L  N│ └──┘                 ║      └──────────────┘     │
 │  └────┘                      ║                           │
 │                  ┌─────────┐ ║  ┌──────┐   ┌──────────┐  │
 │  Rv1 Rv2 Rv3 Rv4 │ PS1     │ ║  │DS3231│   │          │  │
 │  ▬▬  ▬▬  ▬▬  ▬▬  │ HLK-PM01│ ║  │      │   │  ESP32   │  │
 │                  │         │ ║  └──────┘   │ WROOM-32E│  │
 │        ┌──────┐  │         │ ║             │          │  │
 │        │  T1  │  └─────────┘ ║  ┌────┐     │          │  │
 │        │ZMPT  │              ║  │ J2 │     │  ┌────┐  │  │
 │        └──────┘              ║  │CT  │     │  │ANT │  │  │
 │                              ║  └────┘     └──┤    ├──┘  │
 │  ◄── SLOT ROUTED THROUGH ──► ║   J3  SW1      └────┘     │
 │      BOARD ALONG THIS LINE   ║             KEEP-OUT ▲    │
 └──────────────────────────────────────────────────────────┘
                                                    board edge
```

### Spacing rules — treat these as minimums, not targets

| Between | Minimum | Recommended |
|---|---|---|
| Mains (L or N) and SELV copper | 6.4 mm creepage | **8 mm** |
| L and N tracks | 2.5 mm | 3.5 mm |
| Mains copper and a mounting hole / board edge | 3 mm | 4 mm |

**Creepage vs clearance.** *Clearance* is the distance through air; *creepage* is
the distance along the surface of the board. Creepage is the one that kills you,
because dust, humidity and condensation inside a breaker panel let current track
along a surface at a voltage that would never arc through air. A Syrian
distribution board in a humid coastal summer is exactly the environment these
rules exist for.

### Cut a slot

Route a **2–3 mm wide slot** completely through the board along the barrier line,
passing under T1 and alongside PS1. This:

- makes the creepage path physically infinite at the slot (there is no surface to
  track along),
- gives you a visible, unmistakable line that an assembler cannot accidentally
  bridge with solder,
- costs nothing at the PCB house (it is just a routed cut-out).

Leave short bridges of board material where PS1 and T1 need mechanical support.

### Barrier rules

- **No copper pour of any kind crosses the barrier.** Two separate, isolated
  ground regions: `MAINS_N` and `GND` (SELV). They must never connect — not by a
  track, not by a via, not by a stitching pour, not by a "just in case" 0 Ω link.
- No silkscreen text crosses it. Print a dashed line and the word **MAINS** with
  a ⚡ symbol on the hazardous side.
- No mounting hole in the barrier region.
- Keep the mains area as small as you can — less live copper is less risk.

---

## 5.3 Grounding on the SELV side

The metering front end resolves signals of a few hundred microvolts while an
ESP32 30 mm away slams 500 mA on and off at 2.4 GHz. Ground layout is what keeps
those two facts compatible.

- **Solid ground pour on both layers** across the whole SELV region, stitched
  with vias every ~10 mm.
- Define an **AGND region** under and around the ATM90E26's analog pins, the
  burden resistor, the anti-alias filters and the crystal.
- Connect AGND to the main digital GND at **exactly one point**, a short wide
  link placed directly under the ATM90E26. This stops ESP32 return currents from
  flowing across the analog ground and appearing as measurement noise.
- Never route a digital signal (especially SPI clock or anything going to the
  ESP32) across the AGND region.

## 5.4 Analog front-end layout

- **Burden resistor `Rb` as close as physically possible to J2**, with short,
  symmetrical tracks. Route the two CT legs as a **tight differential pair** —
  same length, same width, running side by side the whole way. Any asymmetry
  turns common-mode noise into a measurement error.
- `Rf2`/`Rf3` and `Cf3`/`Cf4` must be laid out symmetrically too. Matched
  components on mismatched tracks are still mismatched.
- Keep the CT tracks **away from PS1** (switching noise) and **away from the
  ESP32 antenna**.
- **Crystal Y1 within 5 mm of pins 22/23**, with C10/C11 right beside it, a
  grounded guard ring around the whole oscillator, and **no tracks underneath on
  either layer**.
- Decoupling caps C8/C9 hard against their supply pins — under 2 mm of track.
- The ferrite bead FB1 goes in the AVDD feed, with C7 on the analog side of it.

## 5.5 Power layout

- C4 (470 µF) **within 10 mm of the ESP32's 3V3 pin**, with a wide, short track.
  This single capacitor is the difference between a reliable product and
  intermittent brown-out reboots during Wi-Fi transmission.
- Give U1 (AMS1117, SOT-223) a copper pour of at least 200 mm² on its tab pad,
  stitched to the bottom layer with several vias.
- Keep the 5 V and 3.3 V return paths short and wide.

## 5.6 Antenna keep-out — non-negotiable

You chose the module's integrated PCB antenna, so the layout must respect it:

- The module's antenna end **must overhang the edge of your PCB**, or at minimum
  sit over a region with **no copper on any layer** — no ground pour, no tracks,
  no via stitching, no silkscreen ink.
- Keep-out extends **at least 10 mm** beyond the antenna in the board plane, and
  15 mm is better.
- Place the antenna end pointing **out of the distribution panel**, away from
  metal, and away from the mains wiring.
- No mounting screws, metal standoffs or the CR2032 cell within 15 mm of it.

> Reserve this area even though it looks like wasted board space. It is the
> difference between a device that connects on the first try and a support call
> you cannot diagnose remotely.

## 5.7 Test points and silkscreen

Add exposed 1.5 mm pads, clearly labelled, for: `3V3`, `5V`, `GND`, `VP`, `I1P`,
`I1N`. Your technicians will thank you 1,000 times.

Silkscreen that actually matters in production:

- `⚡ MAINS — DANGER` on the hazardous side, plus the dashed barrier line.
- `L` and `N` at J1; `CT` at J2.
- Pin 1 of every IC, and a clear `+` on both electrolytics and the coin cell.
- The full pinout printed next to J3: `3V3 GND TX RX EN IO0`.
- A serial-number box, and the board revision and date.

## 5.8 Assembly-friendly layout details

Small things that add up over 1,000 boards:

- Orient all polarised parts the **same way** where you can. An assembler
  scanning a panel spots one rotated capacitor instantly if the other nine point
  the same direction.
- Keep at least 1 mm between SMD parts so a soldering iron tip can reach.
- Do not tuck small passives under or right against the ESP32 module or the
  terminal blocks — hand-rework becomes impossible.
- Put all SMD parts on the **top side only**. A single-sided-SMD board can be
  stencil-printed and reflowed in one pass (see [tooling §7](07-assembly-and-tooling.md)).
- Add 2 × 1 mm optical fiducials diagonally opposite if you plan to use a
  stencil — they make alignment fast and repeatable.

---

## 5.9 Enclosure

### ⚠️ Read this before 3D-printing production enclosures

You said the enclosure will be 3D printed in plastic. That is fine for
prototypes, but for a product sold to homeowners there is a real safety issue
worth understanding:

**The enclosure around a mains-connected device is a fire-safety component.** Its
job is to contain a fault — if a component overheats or arcs inside, the box must
not become fuel. Commercial electrical enclosures are made of **UL94 V-0**
flame-retardant plastic, meaning they self-extinguish within 10 seconds and do
not drip flaming material.

Standard 3D-printing filaments are **not** flame-retardant:

| Material | Softening point | Flammability | Verdict for production |
|---|---|---|---|
| **PLA** | ~60 °C | Burns readily, drips | **Do not use.** A breaker panel in a Syrian summer can exceed 60 °C on its own. The box will deform and sag around live parts. |
| **PETG** | ~80 °C | Burns, self-extinguishes poorly | Acceptable for prototypes and pilot units. Minimum for anything leaving your workshop. |
| **ABS / ASA** | ~100 °C | Burns, but better dimensional stability | Better. Still not V-0. |
| **Flame-retardant filament** (V-0 rated PC or ABS) | 100 °C+ | Self-extinguishing | Good, but expensive and harder to print. |
| **Off-the-shelf V-0 ABS/PC electrical box** | 100 °C+ | Self-extinguishing | **Best.** Cheap in quantity, already certified, already looks like a product. |

**My recommendation, and this is your call to make:** 3D-print for prototypes and
your first pilot batch, then move to a standard off-the-shelf flame-retardant
enclosure for volume. A generic DIN-rail modular box or a small ABS junction box
costs about the same as the filament and print time, looks more professional, and
removes a liability you do not want as a new company. If you do continue with
printing, **use PETG or ABS at minimum and never PLA**, print solid walls at
least 2.5 mm thick, and keep at least 3 mm of air between any live copper and the
inside wall.

### Dimensions and features

| Feature | Spec |
|---|---|
| Internal volume | ~55 × 50 × 28 mm (board 50 × 45 mm + clearance) |
| Wall thickness | 2.5 mm minimum, 3 mm preferred |
| Board mounting | 4 × M3 brass inserts or screw bosses; board raised ≥ 4 mm off the floor |
| Mains cable entry | Grommet or gland with **strain relief** — a pulled wire must never reach the terminal screws |
| CT lead entry | Separate opening on the opposite face from the mains entry |
| Button | 3.5 mm hole over SW1, or a moulded flexible membrane |
| LEDs | 3 mm clear windows or light pipes |
| Antenna | Leave the region over the module's antenna **free of any insert, screw or metal**; orient this face outward |
| Ventilation | **None.** The board dissipates well under 1 W. A sealed box keeps dust and insects out of the isolation barrier — which is exactly what protects your creepage. |

### Labelling

Print or label on the outside: brand and model, `230 V~ 50 Hz`, max measured
current, your contact details, a serial number, and a warning that installation
must be done by a qualified electrician with the main supply switched off.

---

## 5.10 Installation notes (for your installer manual)

1. **Switch off the main breaker before opening the panel.**
2. Connect L and N to J1 from a protected point — ideally a spare MCB, not
   directly to the incoming busbar.
3. Clamp the CT around the **main incoming live conductor only** — one single
   conductor, never both L and N together (the fields would cancel and you would
   read zero).
4. Clamp it **after** any changeover switch, so that whatever the house actually
   consumes passes through it.
5. Observe the arrow / polarity mark on the clamp. If power reads negative, the
   clamp is reversed.
6. Close the clamp until it clicks. A gap in the core causes a large, consistent
   under-reading — and this is the most common installation fault in the field.
7. Keep the CT lead away from the mains bundle where you can, to reduce
   pickup.
8. Position the device so its antenna end faces out of the panel.
