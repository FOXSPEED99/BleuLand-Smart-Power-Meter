# What to Buy — Complete Shopping List

**35 things to order. About US$ 14,500 for 1,000 devices.**

Spreadsheet version: [`parts-to-buy.csv`](parts-to-buy.csv)

| | |
|---|---|
| Different items to order | **35** |
| Parts on one finished device | **51** (48 soldered + battery + clamp + PCB) |
| Total pieces to order | **~54,000** |
| Cost of the whole order | **≈ US$ 14,500** |
| **Cost per finished device** | **≈ US$ 13.87** |

> Prices are Chinese wholesale estimates for budgeting. Buy locally in Syria or
> Lebanon wherever you can — treat these as the ceiling.

---

## Why "order this many" is more than 1,000

| Part type | Extra | Why |
|---|---|---|
| Chips, modules, connectors | **+5 %** | Expensive and slow to replace mid-run |
| Small resistors and capacitors | **+5–10 %** | They get lost, flicked off the bench, tombstoned |
| Fuse, diodes, crystal | **+10 %** | Cheap, and you never want to stop the line |
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
| 3 | **HLW8032** metering chip, SOP-8 | 1 | **1,050** | LCSC [`C128023`](https://www.lcsc.com/product-detail/C128023.html) |
| 4 | **Current clamp**, 100 A : 50 mA, 13 mm opening (`SCT-013-000`) | 1 | **1,030** | AliExpress / local |
| 5 | **ZMPT101B** voltage transformer | 1 | **1,050** | AliExpress / local |

⚠️ For #5, buy the **bare transformer** — a small black block with four pins. Not
the blue circuit board with an op-amp and a potentiometer on it.

⚠️ #4 is your **biggest single cost, about a third of the bill**. Buy samples
from three suppliers and compare before committing.

## 3. Timekeeping

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 6 | **DS1307Z+** clock chip, SOIC-8 | 1 | **1,050** | LCSC [`C1520446`](https://www.lcsc.com/product-detail/C1520446.html) |
| 7 | **Crystal, 32.768 kHz, 12.5 pF**, cylindrical 2 × 6 mm | 1 | **1,100** | LCSC [`C52082`](https://www.lcsc.com/product-detail/C52082.html) |
| 8 | CR2032 battery holder, through-hole | 1 | **1,050** | Local |
| 9 | CR2032 battery, 3 V | 1 | **1,020** | Local |

**What this does:** keeps the time running when mains is off, so readings stored
during an internet outage still get correct timestamps.

⚠️ **Buy the bare chip, never a module.** Both the DS3231 "blue module" and the
DS1307 "Tiny RTC" module have charging circuits that destroy a normal CR2032 —
and the Tiny RTC ships with a rechargeable cell that dies in about two years.

⚠️ **The crystal must be 12.5 pF.** The DS1307 has its load capacitors *inside*,
so you add no extra capacitors — but the crystal must match. A 6 pF crystal here
makes the clock run minutes-per-day slow.

⚠️ **The battery connects directly to the chip's battery pin and nothing else.**
No diode, no resistor, no charging circuit. At 0.84 µA it lasts **8–10 years**.

## 4. Power

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 10 | **HLK-PM01** — 230 VAC to 5 V, **isolated** | 1 | **1,050** | AliExpress / local |
| 11 | Electrolytic capacitor 470 µF 16 V, **105 °C** | 1 | **1,050** | Local |

⚠️ #10 must be the **isolated transformer type**, not a capacitive dropper. This
part is what makes the whole low-voltage side safe to touch.

## 5. Safety parts — buy these from a reputable source

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 12 | **Fuse 250 mA slow-blow, 250 VAC**, 5 × 20 mm glass | 1 | **1,100** | Local |
| 13 | Fuse clips for 5 × 20 mm | 2 | **2,100** | Local |
| 14 | **MOV surge protector 14D471K** (470 V, 14 mm disc) | 1 | **1,050** | Local / LCSC |
| 15 | **X2 safety capacitor, 100 nF, 275 VAC** | 1 | **1,050** | Local / LCSC |
| 16 | TVS diode **SMAJ5.0CA** (bidirectional) | 2 | **2,100** | LCSC / local |

⚠️ **Do not let a shop substitute "the same value" from an unmarked bin for items
12, 14 and 15.** A counterfeit X2 capacitor or MOV is a fire risk, not a
performance issue. The fuse must be **250 VAC** rated and **slow-blow** — never
an SMD fuse, most are only rated 63 V.

## 6. Connectors

| # | Item | Per device | **Order** | Where |
|---|---|---|---|---|
| 17 | Screw terminal, 2-pin, **5.08 mm** (mains) | 1 | **1,050** | Local |
| 18 | Screw terminal, 2-pin, **3.5 mm** (clamp) | 1 | **1,050** | Local |

The two sizes are different **on purpose** — it makes it impossible to wire mains
into the clamp input by mistake.

## 7. Resistors

| # | Value | Per device | **Order** | Board labels |
|---|---|---|---|---|
| 19 | **47 kΩ, 1 %, ½ W metal film, through-hole** | 4 | **4,200** | Rv1 Rv2 Rv3 Rv4 |
| 20 | **0.68 Ω, 1 %, ≤50 ppm/°C, thin film** | 1 | **1,100** | Rb |
| 21 | **150 Ω, 1 %, ≤50 ppm/°C, thin film** | 1 | **1,100** | Rv5 |
| 22 | **1.5 kΩ, 1 %** | 2 | **2,200** | Rf2, Rf3 |
| 23 | 1 kΩ, 1 % | 4 | **4,200** | Rf1, Rls1, R3, R4 |
| 24 | 2 kΩ, 1 % | 1 | **1,100** | Rls2 |
| 25 | **4.7 kΩ, 1 %** | 2 | **2,100** | R5, R6 |
| 26 | 0 Ω jumper | 1 | **1,100** | R7 |

⚠️ **#20 is the most accuracy-critical part on the whole board.** It must be 1 %
and ≤50 ppm/°C. **Never wirewound** — its inductance introduces timing error.

⚠️ **#19 must be through-hole**, not surface-mount. Small SMD resistors are not
rated for the voltage across them here.

⚠️ **#25 must connect to 3.3 V, never to 5 V.** The clock chip runs on 5 V but
the ESP32 is not 5 V tolerant. These two resistors are what keep the bus at
3.3 V and protect the ESP32.

## 8. Capacitors

| # | Value | Per device | **Order** | Board labels |
|---|---|---|---|---|
| 27 | 100 nF X7R 50 V, 0805 | 4 | **4,200** | C3, C6, C8, C13 |
| 28 | 10 µF X7R 16 V, 0805 | 2 | **2,100** | C5, C7 |
| 29 | 33 nF X7R 50 V, 0805 | 2 | **2,100** | Cf1, Cf2 |
| 30 | 10 nF X7R 50 V, 0805 | 2 | **2,100** | Cf3, Cf4 |

⚠️ Buy **all the filter capacitors (#29, #30) from one batch**. Their consistency
matters more than their exact value, because the timing correction is tuned
around whatever they actually are.

## 9. Everything else

| # | Item | Per device | **Order** |
|---|---|---|---|
| 31 | LED green, 0805 | 1 | **1,100** |
| 32 | LED blue, 0805 | 1 | **1,100** |
| 33 | Ferrite bead 600 Ω @ 100 MHz, 0805 | 1 | **1,100** |
| 34 | **Bare PCB**, 2-layer, 1.6 mm, ~60 × 55 mm | 1 | **1,030** |
| 35 | Solder stencil, 0.12 mm stainless | — | **2** |

---

## Where the money goes

| Item | Share of the bill |
|---|---|
| **Current clamp** | **~32 %** |
| **ESP32 board** | **~25 %** |
| HLK-PM01 power supply | ~13 % |
| DS1307 clock chip | ~7 % |
| ZMPT101B transformer | ~7 % |
| Everything else (30 items) | ~16 % |

**Five items are 84 % of the cost.** If you need to cut, that is where to look —
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
4. **Safety parts (#12–#16) from a reputable supplier**, even at higher cost.
5. **Test a sample batch** of the three most-counterfeited items: the **ESP32
   boards**, the **DS1307 chips** and the **current clamps**. For the clock, run
   three samples for a week and measure the drift — a fake will lose minutes,
   a real one a few seconds.
6. **One batch per item.** If a supplier would mix stock from different
   shipments, ask for a single batch — especially the ESP32 boards.
