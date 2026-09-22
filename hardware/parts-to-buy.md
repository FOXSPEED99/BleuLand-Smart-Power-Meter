# What to Buy — Complete Shopping List

**34 things to order. About US$ 15,000 for 1,000 devices.**

Spreadsheet version: [`parts-to-buy.csv`](parts-to-buy.csv)

| | |
|---|---|
| Different items to order | **34** |
| Parts on one finished device | **50** (47 on the board + battery + clamp + PCB) |
| Total pieces to order | **~52,900** |
| Cost of the whole order | **≈ US$ 14,980** |
| Cost per finished device | **≈ US$ 14.33** |

> Prices are Chinese wholesale estimates for budgeting. Buy locally in Syria or
> Lebanon wherever you can — treat these as the ceiling.

---

## Why "order this many" is more than 1,000

| Part type | Extra | Why |
|---|---|---|
| Chips, modules, connectors | **+5 %** | Expensive and slow to replace mid-run |
| Small resistors and capacitors | **+5–10 %** | They get lost, flicked off the bench, tombstoned |
| Fuse, diodes | **+10 %** | Cheap, and you never want to stop the line |
| Clamp, PCB, battery | **+2–3 %** | Bulky or expensive, less easily lost |

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
the blue circuit board with an op-amp and a potentiometer.

⚠️ #4 is your **biggest single cost, about a third of the bill**. Buy samples
from three suppliers and compare before committing.

## 3. Timekeeping

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 6 | **DS3231SN** real-time clock, SOIC-16 | 1 | **1,050** | LCSC / local |
| 7 | CR2032 battery holder, through-hole | 1 | **1,050** | Local |
| 8 | CR2032 battery, 3 V | 1 | **1,020** | Local |

⚠️ The DS3231 is heavily counterfeited. Test a sample batch before buying 1,050.

## 4. Power

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 9 | **HLK-PM01** — 230 VAC to 5 V, **isolated** | 1 | **1,050** | AliExpress / local |
| 10 | Electrolytic capacitor 470 µF 16 V, **105 °C** | 1 | **1,050** | Local |

⚠️ #9 must be the **isolated transformer type**, not a capacitive dropper. This
part is what makes the whole low-voltage side safe to touch.

## 5. Safety parts — buy these from a reputable source

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 11 | **Fuse 250 mA slow-blow, 250 VAC**, 5 × 20 mm glass | 1 | **1,100** | Local |
| 12 | Fuse clips for 5 × 20 mm | 2 | **2,100** | Local |
| 13 | **MOV surge protector 14D471K** (470 V, 14 mm disc) | 1 | **1,050** | Local / LCSC |
| 14 | **X2 safety capacitor, 100 nF, 275 VAC** | 1 | **1,050** | Local / LCSC |
| 15 | TVS diode **SMAJ5.0CA** (bidirectional) | 2 | **2,100** | LCSC / local |

⚠️ **Do not let a shop substitute "the same value" from an unmarked bin for
items 11, 13 and 14.** A counterfeit X2 capacitor or MOV is a fire risk, not a
performance issue. The fuse must be **250 VAC** rated and **slow-blow** — never
an SMD fuse, most are only rated 63 V.

## 6. Connectors

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 16 | Screw terminal, 2-pin, **5.08 mm** (mains) | 1 | **1,050** | Local |
| 17 | Screw terminal, 2-pin, **3.5 mm** (clamp) | 1 | **1,050** | Local |

The two sizes are different **on purpose** — it makes it impossible to wire mains
into the clamp input by mistake.

## 7. Resistors

| # | Value | Per device | **Order** | Board labels |
|---|---|---|---|---|
| 18 | **47 kΩ, 1 %, ½ W metal film, through-hole** | 4 | **4,200** | Rv1 Rv2 Rv3 Rv4 |
| 19 | **0.68 Ω, 1 %, ≤50 ppm/°C, thin film** | 1 | **1,100** | Rb |
| 20 | **150 Ω, 1 %, ≤50 ppm/°C, thin film** | 1 | **1,100** | Rv5 |
| 21 | **1.5 kΩ, 1 %** | 2 | **2,200** | Rf2, Rf3 |
| 22 | 1 kΩ, 1 % | 4 | **4,200** | Rf1, Rls1, R3, R4 |
| 23 | 2 kΩ, 1 % | 1 | **1,100** | Rls2 |
| 24 | 4.7 kΩ, 1 % | 2 | **2,100** | R5, R6 |
| 25 | 0 Ω jumper | 1 | **1,100** | R7 |

⚠️ **#19 is the most accuracy-critical part on the whole board.** It must be 1 %
and ≤50 ppm/°C. **Never wirewound** — its inductance introduces timing error.
Do not let anyone substitute a cheap 5 % part.

⚠️ **#18 must be through-hole**, not surface-mount. Small SMD resistors are not
rated for the voltage across them here.

## 8. Capacitors

| # | Value | Per device | **Order** | Board labels |
|---|---|---|---|---|
| 26 | 100 nF X7R 50 V, 0805 | 4 | **4,200** | C3, C6, C8, C13 |
| 27 | 10 µF X7R 16 V, 0805 | 2 | **2,100** | C5, C7 |
| 28 | 33 nF X7R 50 V, 0805 | 2 | **2,100** | Cf1, Cf2 |
| 29 | 10 nF X7R 50 V, 0805 | 2 | **2,100** | Cf3, Cf4 |

⚠️ Buy **all the filter capacitors (#28, #29) from one batch**. Their consistency
matters more than their exact value, because the timing correction is tuned
around whatever they actually are.

## 9. Everything else

| # | Item | Per device | **Order** |
|---|---|---|---|
| 30 | LED green, 0805 | 1 | **1,100** |
| 31 | LED blue, 0805 | 1 | **1,100** |
| 32 | Ferrite bead 600 Ω @ 100 MHz, 0805 | 1 | **1,100** |
| 33 | **Bare PCB**, 2-layer, 1.6 mm, ~60 × 55 mm | 1 | **1,030** |
| 34 | Solder stencil, 0.12 mm stainless | — | **2** |

---

## Where the money goes

| Item | Share of the bill |
|---|---|
| **Current clamp** | **~31 %** |
| **ESP32 board** | **~25 %** |
| HLK-PM01 power supply | ~13 % |
| DS3231 clock | ~11 % |
| ZMPT101B transformer | ~6 % |
| Everything else (29 items) | ~14 % |

Five items are **86 %** of the cost. If you need to cut, that is where to look —
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
4. **Safety parts (#11–#15) from a reputable supplier**, even at higher cost.
5. **Test a sample batch** of the three most-counterfeited items: the ESP32
   boards, the DS3231 clocks and the current clamps.
6. **One batch per item.** If a supplier would mix stock from different
   shipments, ask for a single batch — especially the ESP32 boards.
