# What to Buy — Complete Shopping List

**30 things to order. About US$ 13,200 for 1,000 devices.**

Spreadsheet version: [`parts-to-buy.csv`](parts-to-buy.csv)

| | |
|---|---|
| Different items to order | **30** |
| Parts on one finished device | **44** (42 on the board + clamp + PCB) |
| Total pieces to order | **~46,700** |
| Cost of the whole order | **≈ US$ 13,190** |
| **Cost per finished device** | **≈ US$ 12.62** |

> Prices are Chinese wholesale estimates for budgeting. Buy locally in Syria or
> Lebanon wherever you can — treat these as the ceiling.

---

## Why "order this many" is more than 1,000

| Part type | Extra | Why |
|---|---|---|
| Chips, modules, connectors | **+5 %** | Expensive and slow to replace mid-run |
| Small resistors and capacitors | **+5–10 %** | They get lost, flicked off the bench, tombstoned |
| Fuse, diodes | **+10 %** | Cheap, and you never want to stop the line |
| Clamp, PCB | **+2–3 %** | Bulky or expensive, less easily lost |

> **Order 1,000 of something for a 1,000-unit run and you will stop the line at
> unit 970.** This is the most common first-production mistake there is.

---

## 1. The brain

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 1 | **ESP32 development board** — "ESP32 Type-C", 30 pins, with the metal-shielded ESP-WROOM-32 module and a CH340C chip | 1 | **1,050** | Local (eng-elec.com) or AliExpress |
| 2 | Female header strip, 1 × 15, 2.54 mm | 2 | **2,100** | Local / LCSC |

**Check every board has:** the silver metal module (not a bare black chip), 15
pins per side, two buttons, USB-C. Buy all 1,050 **from one batch** — these
boards change between production runs.

## 2. Measuring

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 3 | **HLW8032** metering chip, SOP-8 | 1 | **1,050** | LCSC `C128023` |
| 4 | **Current clamp**, 100 A : 50 mA, 13 mm opening (`SCT-013-000`) | 1 | **1,030** | AliExpress / local |
| 5 | **ZMPT101B** voltage transformer | 1 | **1,050** | AliExpress / local |

⚠️ For #5, buy the **bare transformer** — a small black block with four pins. Not
the blue circuit board with an op-amp and a potentiometer on it.

⚠️ #4 is your **biggest single cost, about a third of the bill**. Buy samples
from three suppliers and compare before committing.

## 3. Power

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 6 | **HLK-PM01** — 230 VAC to 5 V, **isolated** | 1 | **1,050** | AliExpress / local |
| 7 | Electrolytic capacitor 470 µF 16 V, **105 °C** | 1 | **1,050** | Local |

⚠️ #6 must be the **isolated transformer type**, not a capacitive dropper. This
part is what makes the whole low-voltage side safe to touch.

## 4. Safety parts — buy these from a reputable source

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 8 | **Fuse 250 mA slow-blow, 250 VAC**, 5 × 20 mm glass | 1 | **1,100** | Local |
| 9 | Fuse clips for 5 × 20 mm | 2 | **2,100** | Local |
| 10 | **MOV surge protector 14D471K** (470 V, 14 mm disc) | 1 | **1,050** | Local / LCSC |
| 11 | **X2 safety capacitor, 100 nF, 275 VAC** | 1 | **1,050** | Local / LCSC |
| 12 | TVS diode **SMAJ5.0CA** (bidirectional) | 2 | **2,100** | LCSC / local |

⚠️ **Do not let a shop substitute "the same value" from an unmarked bin for items
8, 10 and 11.** A counterfeit X2 capacitor or MOV is a fire risk, not a
performance issue. The fuse must be **250 VAC** rated and **slow-blow** — never
an SMD fuse, most are only rated 63 V.

## 5. Connectors

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 13 | Screw terminal, 2-pin, **5.08 mm** (mains) | 1 | **1,050** | Local |
| 14 | Screw terminal, 2-pin, **3.5 mm** (clamp) | 1 | **1,050** | Local |

The two sizes are different **on purpose** — it makes it impossible to wire mains
into the clamp input by mistake.

## 6. Resistors

| # | Value | Per device | **Order** | Board labels |
|---|---|---|---|---|
| 15 | **47 kΩ, 1 %, ½ W metal film, through-hole** | 4 | **4,200** | Rv1 Rv2 Rv3 Rv4 |
| 16 | **0.68 Ω, 1 %, ≤50 ppm/°C, thin film** | 1 | **1,100** | Rb |
| 17 | **150 Ω, 1 %, ≤50 ppm/°C, thin film** | 1 | **1,100** | Rv5 |
| 18 | **1.5 kΩ, 1 %** | 2 | **2,200** | Rf2, Rf3 |
| 19 | 1 kΩ, 1 % | 4 | **4,200** | Rf1, Rls1, R3, R4 |
| 20 | 2 kΩ, 1 % | 1 | **1,100** | Rls2 |
| 21 | 0 Ω jumper | 1 | **1,100** | R7 |

⚠️ **#16 is the most accuracy-critical part on the whole board.** It must be 1 %
and ≤50 ppm/°C. **Never wirewound** — its inductance introduces timing error. Do
not let anyone substitute a cheap 5 % part.

⚠️ **#15 must be through-hole**, not surface-mount. Small SMD resistors are not
rated for the voltage across them here.

## 7. Capacitors

| # | Value | Per device | **Order** | Board labels |
|---|---|---|---|---|
| 22 | 100 nF X7R 50 V, 0805 | 3 | **3,200** | C3, C6, C8 |
| 23 | 10 µF X7R 16 V, 0805 | 2 | **2,100** | C5, C7 |
| 24 | 33 nF X7R 50 V, 0805 | 2 | **2,100** | Cf1, Cf2 |
| 25 | 10 nF X7R 50 V, 0805 | 2 | **2,100** | Cf3, Cf4 |

⚠️ Buy **all the filter capacitors (#24, #25) from one batch**. Their consistency
matters more than their exact value, because the timing correction is tuned
around whatever they actually are.

## 8. Everything else

| # | Item | Per device | **Order** |
|---|---|---|---|
| 26 | LED green, 0805 | 1 | **1,100** |
| 27 | LED blue, 0805 | 1 | **1,100** |
| 28 | Ferrite bead 600 Ω @ 100 MHz, 0805 | 1 | **1,100** |
| 29 | **Bare PCB**, 2-layer, 1.6 mm, ~60 × 55 mm | 1 | **1,030** |
| 30 | Solder stencil, 0.12 mm stainless | — | **2** |

---

## ❌ What is deliberately NOT on this list

**No clock chip.** An earlier version of this design had a DS3231 real-time
clock, a battery, a holder and three small parts — about **US$ 1.70 per device,
US$ 1,700 across the run.**

It was over-specified. The ESP32 counts seconds since it powered on and stores
that with every reading; the moment it reaches the internet it works backwards
and timestamps everything exactly. A clock chip only helps if the device
power-cycles **twice** without reaching the internet in between — and even then
the **kWh total, which is what the bill depends on, is never affected.**

**Leave the footprints on the PCB unpopulated.** If the daily graph ever turns
out to matter to customers, fit a `PCF8563T` (~US$ 0.38) plus a crystal and a
coin cell on a later batch — no PCB redesign needed. Full explanation in
[the wiring guide, Section H](../docs/02-connections.md).

---

## Where the money goes

| Item | Share of the bill |
|---|---|
| **Current clamp** | **~36 %** |
| **ESP32 board** | **~28 %** |
| HLK-PM01 power supply | ~14 % |
| ZMPT101B transformer | ~7 % |
| Everything else (26 items) | ~15 % |

**Four items are 85 % of the cost.** If you need to cut, that is where to look —
and the clamp is worth negotiating hardest on.

---

## ⭐ Buy this FIRST — the prototype batch

**Do not order the 1,000-unit quantities yet.** Three component values must be
confirmed on real hardware first.

Buy **10 of everything above**, plus these extra values so you can find the right
ones without re-ordering:

| For | Buy 10 each of these (0805, 1 %) |
|---|---|
| **`Rb`** (clamp range) | 0.47 Ω, 0.51 Ω, 0.56 Ω, 0.62 Ω, **0.68 Ω**, 0.75 Ω, 0.82 Ω, 1.0 Ω |
| **`Rv5`** (voltage range) | 62 Ω, 100 Ω, **150 Ω**, 220 Ω, 330 Ω, 470 Ω |
| **`Rf2`/`Rf3`** (timing) | 820 Ω, 1.2 kΩ, **1.5 kΩ**, 1.8 kΩ, 2.2 kΩ — buy **20** of each, they go in pairs |

About **US$ 15 of resistors.** It is the difference between locking the design in
half a day and finding the problem at unit 300.

---

## Ordering plan

1. **Prototype batch first** — 10 sets plus the sweep resistors above.
2. **Confirm `Rb`, `Rv5` and `Rf2`/`Rf3`** on five working boards.
3. **Then order everything**, the full quantity, in one go. Stock levels are a
   snapshot, not a promise.
4. **Safety parts (#8–#12) from a reputable supplier**, even at higher cost.
5. **Test a sample batch** of the two most-counterfeited items: the ESP32 boards
   and the current clamps.
6. **One batch per item.** If a supplier would mix stock from different
   shipments, ask for a single batch — especially the ESP32 boards.
