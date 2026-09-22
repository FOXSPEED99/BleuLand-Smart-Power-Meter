# 7. Hand Assembly, and Whether to Buy a Stencil + Hotplate

You asked directly: *"If you think buying a hotplate + stencil is worth it for
our volume, tell us what to buy and explain the process simply."*

**Short answer: yes, buy them.** The numbers are in §7.3. But first, the board is
designed so you never *have* to — everything on it can be built with a soldering
iron alone.

---

## 7.1 The board is iron-only by design

Every choice here was made against your constraint:

| Part | Package | Why it is iron-friendly |
|---|---|---|
| **HLW8032** | **SOP-8, 1.27 mm pitch** | 8 pins at twice the spacing of a typical metering IC. This is why it was chosen for v1 — see [`docs/01-architecture.md`](01-architecture.md) §1.4. |
| ESP32 module | Castellated edge pads | The *easiest* part to hand-solder — the pads are half-holes on the module edge, so you touch the iron to the outside and the solder wicks in. |
| DS3231 | SOIC-16, 1.27 mm | Comfortable. |
| AMS1117 | SOT-223 | Large tab, very forgiving. |
| Passives | 0805 | Deliberately not 0603 or 0402. 0805 is the sweet spot: small enough to be compact, large enough to place with ordinary tweezers and see without a microscope. |
| TVS diodes | DO-214AC | Large. |
| Everything on the mains side | Through-hole | Easier, and better for voltage rating and creepage. |

**Nothing on this board has a hidden pad, a thermal pad underneath, or a leadless
package.** No QFN, no DFN, no BGA — and since the v1 chip change, **no fine
pitch either**. The tightest spacing anywhere on the board is now 1.27 mm,
shared by the metering IC, the RTC and the ESP32's castellated pads. You can
build all 1,000 with an iron, comfortably.

---

## 7.2 Iron-only technique notes

### There is no longer a hard part

The v1 design has no 0.65 mm pitch anywhere. Nothing on it needs drag soldering,
a microscope, or special technique. The three ICs — HLW8032 (SOP-8), DS3231
(SOIC-16) and the ESP32 module (castellated) — are all straightforward
pin-by-pin work with a fine tip and flux.

If you later move to v2 with the ATM90E26, that changes: SSOP-28 at 0.65 mm does
need drag soldering. The technique is written up in
[`docs/08-v2-upgrade-path.md`](08-v2-upgrade-path.md) §8.5, so it is there when
you need it.

### General
- Leaded solder (Sn63Pb37, 0.5 mm) is significantly easier than lead-free:
  it melts at 183 °C instead of 217 °C and wets far better. Since you are not
  exporting to the EU, use it.
- Flux pen or gel flux is not optional — budget for it as a consumable.
- Solder the **low parts first**, tall parts last, so the board sits flat.
- Clean flux residue with IPA at the end. See the warning in §7.6.

### Realistic timing (practiced assembler)

| Step | Time |
|---|---|
| 33 SMD placements by iron | 11–13 min |
| 18 THT placements | 5–6 min |
| Inspection | 2 min |
| **Total per board** | **~18–21 min** |
| **× 1,000 units** | **~300–350 hours ≈ 40 working days for one person** |

---

## 7.3 Should you buy a stencil and hotplate? The arithmetic

### Time

| | Iron only | Stencil + hotplate |
|---|---|---|
| Paste printing | — | 30 s |
| SMD placement | 11–13 min (place **and** solder each part) | ~5 min (place only, paste holds them) |
| Reflow | — | 4 min, **batched** — ~1 min/board if you do 4 at a time |
| THT by hand | 5–6 min | 5–6 min |
| Inspection | 2–3 min | 2 min |
| **Per board** | **~22 min** | **~14 min** |
| **× 1,000** | **~370 hours** | **~235 hours** |

**You save roughly 135 hours** — about 17 working days of one person's labour.

### The bigger reason: consistency

Time saved is the smaller benefit. The real one is that **reflow makes every
joint identical**. Hand-soldering ~120 SMD joints × 1,000 boards is 120,000
opportunities for a cold joint, a bridge, or a tombstoned resistor. Reflow
removes almost all of them in one step.

Expect first-pass yield to go from roughly **90–95 % (iron)** to **97–99 %
(reflow)**. At 1,000 units that is 50–80 fewer boards to diagnose and rework —
and rework on a board you have already built is far more expensive than building
it right.

### Verdict
**Buy the stencil and hotplate.** Total tooling is US$ 120–200, against 135 hours
saved and a meaningful yield improvement. It pays back within the first ~150
boards.

---

## 7.4 What to buy

| Item | What to look for | Rough cost |
|---|---|---|
| **Stainless steel stencil** | Frameless, **0.12 mm** thick, laser-cut, matched to your board's paste layer. Order it from the same house as your PCB (JLCPCB, PCBWay) — they generate it from your Gerbers. **Order two**; they bend and wear. | US$ 8–15 each |
| **Reflow hotplate** | **200 × 200 mm minimum** heating area, **PID temperature control** (not a simple thermostat), 600–1000 W, flat aluminium surface, digital setpoint with thermocouple feedback. A programmable profile is a bonus, not a requirement. Avoid the tiny 30 × 30 mm "mini" hotplates — your board is 50 × 45 mm and you want to do several at once. | US$ 60–120 |
| **Solder paste** | **Sn63Pb37 (leaded)**, T4 particle size, in a **jar** (not a syringe — syringes are for rework, jars are for stencil printing). 100 g covers roughly 300–500 boards of this size. Keep it refrigerated; let it reach room temperature before opening or it will absorb condensation. | US$ 15 / 100 g |
| **Squeegee** | A metal squeegee blade, or honestly an old metal scraper or a stiff plastic card. | US$ 0–10 |
| **Fine ESD tweezers** | Buy 3–4 pairs, straight and bent tips. They wear out and get magnetised. | US$ 15 |
| **Flux** | Gel flux in a syringe for rework, and a no-clean flux pen. Consumable — buy plenty. | US$ 10 |
| **Inspection microscope** | A USB microscope at 1080p is plenty for v1's 1.27 mm parts. You would want a stereo microscope for the v2 ATM90E26. | US$ 40–150 |
| **IPA + brushes** | For cleaning flux. Essential — see §7.6. | US$ 10 |
| **Solder wick** | Bridge removal. | US$ 5 |
| **Stencil jig** (optional) | A frame that holds the board and aligns the stencil repeatably. You can improvise one from scrap PCBs, but for 1,000 boards a proper jig is worth it. | US$ 20–40 |

You already own a hot-air station. Keep using it for **rework only** — hot air is
poor at assembly (it blows small parts around) and excellent at removing a
misplaced IC.

### ⭐ Panelise your PCBs

Order the boards **panelised** — for example a 2 × 2 array of four boards joined
by mouse-bite tabs or a V-groove. JLCPCB and PCBWay both do this from a single
order.

Then you print paste on four boards in one squeegee pass, reflow four at a time,
and snap them apart afterwards. This roughly **quarters** your paste-printing and
reflow time, and it makes the stencil alignment far easier because the panel is
bigger and easier to hold.

---

## 7.5 The reflow process, simply

**Step 1 — Support the board.** Tape scrap PCBs of the *same thickness* around
your board (or panel) so the stencil rests flat. Any tilt smears the paste.

**Step 2 — Align the stencil.** Line up the apertures with the pads. Use the
fiducial marks from [layout §5.8](05-layout-and-enclosure.md). Tape one edge of
the stencil down so it hinges — that way you can lift and re-check without losing
alignment.

**Step 3 — Print.** Put a line of paste along one edge. Hold the squeegee at
about 45° and make **one firm, steady pass**. One pass. Going back and forth
pushes paste under the stencil and bridges everything.

**Step 4 — Lift the stencil straight up.** Vertically, not tilted. Check the
result: every pad should carry a clean brick of paste. If it is smeared, wipe the
board clean with IPA and start again — it takes two minutes, and it is much
cheaper than reworking bridges.

**Step 5 — Place the parts.** With tweezers, set each SMD part onto its paste.
The paste is tacky and holds them. Perfect alignment is not required — surface
tension pulls parts into place during reflow. Work in a sensible order: ICs
first while you have clear access, then passives.

**Step 6 — Reflow.** On the hotplate, for **leaded Sn63Pb37 paste**:

```
  °C
 220 ┤                          ╭──╮          ← peak 200–215 °C, 30–45 s
 200 ┤                       ╭──╯  ╰╮
 180 ┤                    ╭──╯      ╰╮
 160 ┤        ╭───────────╯          ╰╮
 150 ┤    ╭───╯  SOAK 60–90 s         ╰╮
 100 ┤ ╭──╯                            ╰──╮   ← remove and cool
  25 ┼─╯                                  ╰──
     └──────────────────────────────────────── time
       ramp      soak         reflow    cool
```

- Ramp to **150 °C** and hold for **60–90 seconds** (the "soak" — this activates
  the flux and evens out the temperature across the board).
- Then raise to **200–215 °C**. Watch the paste: it will visibly change from dull
  grey to **bright shiny liquid metal**. That moment is called the flash.
- Once everything has flashed, wait about 10 more seconds, then slide the board
  off onto a cool surface.
- **Do not overheat.** More time above melting does not improve the joints; it
  damages parts and grows brittle intermetallics.

*(For lead-free SAC305: soak at 150–180 °C, peak 235–245 °C. Harder, hotter, and
unnecessary for you.)*

**Step 7 — Inspect** every board under magnification before going further,
especially the HLW8032 and the ESP32 pads.

**Step 8 — Hand-solder the through-hole parts** (§7.6).

---

## 7.6 Assembly order for the finished board

1. **Paste, place, reflow all top-side SMD** (34 parts).
2. **Inspect** under magnification. Fix bridges now, while access is clear.
3. **Hand-solder the SELV through-hole parts:** Y1, C2, C4, J2, J3, SW1, BT1.
4. **Hand-solder the mains through-hole parts last:** Rv1–Rv4, T1, PS1, J1, fuse
   clips, RV1, C1. These are the tallest parts and the ones you least want to
   work around.
5. **⚠️ Clean the flux — especially across the isolation barrier.**
   Scrub with IPA and a stiff brush, then dry thoroughly. This is not cosmetic:
   **flux residue is hygroscopic and becomes conductive in humid air.** A film of
   residue bridging your isolation slot quietly destroys the creepage distance
   you designed so carefully, and the failure will not show up until the first
   humid summer in a coastal panel. Clean the barrier region on every single
   unit, and inspect it.
6. **Insert the CR2032** cell.
7. Run the test sequence in
   [calibration §4.2](04-calibration-and-test.md) — starting with the isolation
   test, before the board ever sees mains.

### Parts that must **never** go through reflow

| Part | Why |
|---|---|
| PS1 (HLK-PM01) | Encapsulated module, through-hole, not reflow-rated |
| T1 (ZMPT101B) | Wound component, plastic bobbin |
| C2, C4 (electrolytics) | Will vent or degrade |
| BT1 (CR2032 holder) | Plastic body deforms |
| J1, J2 (screw terminals) | Plastic bodies melt |
| SW1 (tact switch) | Plastic actuator deforms |
| J3 (header) | Plastic spacer deforms |
| B1 (CR2032 cell) | **Never** heat a lithium cell |

---

## 7.7 Consumables to stock for a 1,000-unit run

| Item | Quantity |
|---|---|
| Solder paste (Sn63Pb37, jar) | 300 g |
| Solder wire, 0.5 mm leaded | 500 g |
| Gel flux syringes | 5–10 |
| Flux pens | 5 |
| IPA | 5 L |
| Solder wick | 5 rolls |
| Iron tips (chisel + fine) | 10 — they wear out faster than you expect |
| Cleaning brushes | 10 |
| **Spare components** | **5 % of every line item; 10 % of the ICs** |

That last row matters. Parts get lost, tombstoned, overheated or soldered in
backwards. Ordering 1,000 of a part for a 1,000-unit run guarantees you will stop
the line at unit 970.
