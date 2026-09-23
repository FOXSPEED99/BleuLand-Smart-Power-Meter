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

The resistors on this board do **three completely different jobs**, and each job
has a different rule. Buy the wrong *type* and the board still works — it just
reads the wrong number, and you will never find out why.

### 7a. The measuring resistors — accuracy critical

These five sit in the measuring path. Whatever they do, the reading does.

| # | Value | **Type you must buy** | Per device | **Order** | Board labels |
|---|---|---|---|---|---|
| 20 | **0.68 Ω** | **Current-sense chip resistor, 1 %, ≤100 ppm/°C** (≤50 ppm better), 1206 or 0805 | 1 | **1,100** | Rb |
| 21 | **150 Ω** | 1 %, ordinary 0805 — see the note below | 1 | **1,100** | Rv5 |
| 22 | **1.5 kΩ** | 1 %, ≤100 ppm/°C, 0805, **both from the same reel** | 2 | **2,200** | Rf2, Rf3 |
| 23a | 1 kΩ | 1 %, ≤100 ppm/°C, 0805 | 1 | **1,100** | Rf1 |

**Keep all five surface-mount.** Not because through-hole is less accurate — it
isn't — but because these carry a signal of about **20 millivolts**, next to a
switching power supply. A through-hole resistor has 10 mm legs; every extra
millimetre of leg is an antenna picking up switching noise straight into the
measuring chip.

**`Rb` (0.68 Ω) is the single most important part on the board.** See the
explanation below before you buy it.

**`Rf2` and `Rf3` must be a matched pair.** Buy them on one reel, fit them from
the same reel. Their *exact* value matters less than the fact that they are the
same as each other.

**`Rv5` does not need a special low-drift part**, even though it is in the
measuring path. The voltage reading depends on the **ratio** `Rv5 ÷ (the four
47 kΩ)`, not on `Rv5` alone. Both sides drift upward together when the panel
warms, so most of the drift cancels in the division. An ordinary 1 % chip
resistor is fine here. `Rb` has no partner to cancel against — which is exactly
why it is the one part that needs the good specification.

### 7b. The mains resistors — safety critical

| # | Value | **Type you must buy** | Per device | **Order** | Board labels |
|---|---|---|---|---|---|
| 19 | **47 kΩ** | 1 %, **½ W metal film, through-hole axial** | 4 | **4,200** | Rv1 Rv2 Rv3 Rv4 |

⚠️ **These four must stay through-hole.** Full mains sits across the chain. A
through-hole resistor has a long body and fails **open** — it goes quiet. A tiny
chip resistor can arc across its own body under a lightning surge. Never replace
the four with one 188 kΩ resistor.

### 7c. The housekeeping resistors — nothing critical

| # | Value | Type | Per device | **Order** | Board labels |
|---|---|---|---|---|---|
| 23b | 1 kΩ | Anything, 1 % or 5 % | 3 | **3,100** | Rls1, R3, R4 |
| 24 | 2 kΩ | Anything, 1 % or 5 % | 1 | **1,100** | Rls2 |
| 25 | **4.7 kΩ** | Anything, 1 % or 5 % | 2 | **2,100** | R5, R6 |
| 26 | 0 Ω jumper | 0805 link, or a short piece of wire | 1 | **1,100** | R7 |

These carry LED current and digital signals. **Through-hole ½ W is completely
fine here.** So is 5 %. Use whatever the local shop has.

⚠️ **#25 must connect to 3.3 V, never to 5 V.** The clock chip runs on 5 V but
the ESP32 is not 5 V tolerant. These two resistors are what keep the bus at
3.3 V and protect the ESP32.

---

### About the 0.68 Ω — what actually matters

**The power rating does not matter. At all.**

At the biggest load this device will ever see, the clamp pushes about **31
milliamps** through this resistor. The heat it makes is:

> 0.031 A × 0.031 A × 0.68 Ω ≈ **0.0007 watts**

A 2 W resistor is about **three thousand times** bigger than it needs to be. Any
resistor made, down to the smallest chip, has enough power rating. **Stop looking
at the wattage.**

**What matters is how much the resistor changes when it gets warm.**

This is called the **temperature coefficient**, written in **ppm/°C**. It says
how many parts-per-million the resistance moves for every degree.

A breaker box in Syria goes from maybe 10 °C on a winter night to 55 °C on a
summer afternoon — the box is closed, and the power supply inside warms it. Call
it a **45 °C swing**:

| Resistor type | Typical ppm/°C | Error over 45 °C |
|---|---|---|
| Carbon film (beige body, 5 %) | 250 – 500 | **1.1 % – 2.3 %** |
| **Metal oxide film (grey body, 5 %)** | 200 – 300 | **0.9 % – 1.4 %** |
| Ordinary chip resistor, 1 % | 100 | 0.45 % |
| Metal film axial, 1 % | 50 – 100 | 0.2 % – 0.45 % |
| **Current-sense chip resistor** | 50 – 75 | **0.2 % – 0.3 %** |

**Now the important part — why this is different from tolerance.**

A **5 % tolerance** sounds terrible and is actually harmless. It is a *fixed*
error. You measure each board once during calibration, work out its correction
factor, and store it. After that the 5 % is gone forever.

A **temperature coefficient cannot be calibrated out.** It is not a fixed error —
it moves during the day, every day, for the life of the product. Calibrate at
25 °C and the board is right at 25 °C and wrong everywhere else.

And it fails in the worst possible direction: resistance goes **up** with
temperature → the chip sees **more** millivolts → the device reports **more**
power. So a metal-oxide resistor would over-report by about 1 % **in summer,
exactly when the air conditioning is running and the bill is highest and the
customer is looking hardest.**

**So: the grey 2 W resistor in the photo is the wrong part** — not because it is
too big, but because it is metal oxide film. Buy one of these instead:

1. **Best — a current-sense chip resistor.** On LCSC, filter
   *Resistors → Current Sense Resistors* for **0.68 Ω, ±1 %, ≤100 ppm/°C**, in
   **1206** (easier to solder than 0805, and still no hidden pads). Stackpole
   CSR/CSRN and Yageo PE series are both this class.
2. **Backup, if you cannot get 0.68 Ω** — put **two 1.3 Ω or two 1.5 Ω metal
   film resistors in parallel** (that gives 0.65 Ω or 0.75 Ω). Above 1 Ω,
   ordinary 1 % / 50 ppm metal film is available everywhere, including as a
   through-hole axial. Two parts instead of one, but the specification is easy
   to find.

⚠️ **Never wirewound** for this position, whatever its tolerance says. A
wirewound resistor is a coil — it adds a small timing shift to the current
signal, which is exactly the thing the whole design is fighting.

---

### "Can I just use through-hole ½ W for everything?"

**Short answer: for the housekeeping ones (7c), yes. For the measuring ones
(7a), no. For the mains ones (7b), you must.**

Three things people get wrong here:

**1. Through-hole is not less accurate.** An ordinary blue 1 % metal film axial
is **50–100 ppm/°C**, which is as good as or better than a generic 1 % chip
resistor. Going through-hole is not an accuracy downgrade — *provided you buy
metal film (blue body) and not carbon film (beige body)*. Carbon film is
250–500 ppm/°C and only comes in 5 %.

**2. The real cost is board area.** A ½ W axial resistor lying flat needs about
**30 mm²** of board. An 0805 chip needs about **4.5 mm²** — seven times less. The
board is roughly 60 × 55 mm. Moving ten resistors to through-hole eats about
**10 % of the whole board**. You asked for the smallest board that can hide in a
breaker panel; this is where it goes.

**3. The real cost is assembly time.** If you ever buy the stencil and hotplate,
chip resistors cost **zero** assembly time — they go on with the paste and come
out soldered. Through-hole parts must still be hand-soldered afterwards, two
joints each. Ten extra through-hole resistors is roughly **55 hours across 1,000
units**. With an iron only, the two are about the same speed.

**Summary of what to buy:**

| Position | Buy |
|---|---|
| Rb (0.68 Ω) | **Current-sense chip, 1206, 1 %, ≤100 ppm/°C** |
| Rv5 (150 Ω) | 0805 thin film, 1 %, ≤50 ppm/°C |
| Rf1, Rf2, Rf3 | 0805, 1 %, one reel each value |
| Rv1–Rv4 (47 kΩ) | **Through-hole metal film, ½ W, 1 %** |
| Rls1, Rls2, R3, R4, R5, R6, R7 | Anything you have — through-hole ½ W is fine |

### 7d. Exact parts to order — click and buy

Every part below is a **JLCPCB "Basic" part**: LCSC keeps them in stock in
millions, they are the cheapest grade, and they never go end-of-life. All are
UNI-ROYAL (Uniroyal Elec) thick film, ±1 %, ±100 ppm/°C, 1/8 W, 0805.

| Board label | Value | LCSC part | Buy link | **Order** | ~Price each |
|---|---|---|---|---|---|
| Rf1, Rls1, R3, R4 | 1 kΩ | **C17513** | [lcsc.com/product-detail/C17513.html](https://www.lcsc.com/product-detail/C17513.html) | **4,200** | $0.0027 |
| Rf2, Rf3 | 1.5 kΩ | **C4310** | [lcsc.com/product-detail/C4310.html](https://www.lcsc.com/product-detail/C4310.html) | **2,200** | $0.0038 |
| Rls2 | 2 kΩ | **C17604** | [lcsc.com/product-detail/C17604.html](https://www.lcsc.com/product-detail/C17604.html) | **1,100** | $0.0028 |
| R5, R6 | 4.7 kΩ | **C17673** | [lcsc.com/product-detail/C17673.html](https://www.lcsc.com/product-detail/C17673.html) | **2,100** | $0.0027 |
| Rv5 | 150 Ω | **C17471** | [lcsc.com/product-detail/C17471.html](https://www.lcsc.com/product-detail/C17471.html) | **1,100** | $0.0028 |
| R7 | 0 Ω link | **C17477** | [lcsc.com/product-detail/C17477.html](https://www.lcsc.com/product-detail/C17477.html) | **1,100** | $0.0029 |

**That is about US$ 35 for all the ordinary resistors in 1,000 devices.**

Two positions are not on that list, because they are the two that cannot be a
generic chip resistor:

#### Rv1–Rv4 — the 47 kΩ mains chain

Buy **through-hole metal film, 1 %, 47 kΩ**, ½ W preferred. Each one only has to
dissipate 0.07 W, so ¼ W is electrically fine too — ½ W just gives a longer body
and more surge margin.

- **LCSC, ¼ W:** TyoHM `RN 1/4W 47K F T/B A1` — **C410613**, ±1 %, **±50 ppm/°C**,
  D2.4 × L6.5 mm →
  [lcsc.com/product-detail/C410613.html](https://www.lcsc.com/product-detail/C410613.html)
- **LCSC, ½ W:** the same TyoHM RN series in `RN1/2WS…` form. Browse
  [Through Hole Resistors → Metal Film](https://www.lcsc.com/category/1203.html)
  and filter for 47 kΩ, ±1 %.

⚠️ **LCSC stock on through-hole resistors is thin — often only a few thousand
pieces.** You need 4,200. This is the one resistor to **buy locally in
Syria/Lebanon**: 47 kΩ ½ W metal film is a commodity everywhere. Just make sure
it is **metal film (blue body)** and **not carbon film (beige body)**.

#### Rb — the 0.68 Ω burden resistor

This is the part with no single obvious catalogue number, so you have three
routes. Decide after the prototype sweep tells you the real value.

**Route 1 — one current-sense chip resistor (best, do this if you can).**
Open LCSC's
[Current Sense Resistors category](https://www.lcsc.com/category/1336.html)
and filter: **Resistance 0.68 Ω · Tolerance ±1 % · Package 1206 · TCR ≤100 ppm/°C**.
Confirm the stock covers 1,100 pieces before you commit. Look for Yageo PE / RL,
Stackpole CSR / CSRN, Ever Ohms, or UNI-ROYAL low-ohm series.

**Route 2 — through-hole metal film.** LCSC lists
`MF1/4W-0.68Ω±1% T` from CCO (Chian Chia Elec) as **C119261** →
[lcsc.com/product-detail/C119261.html](https://www.lcsc.com/product-detail/C119261.html).
**Check its temperature coefficient on the page before buying** — metal film at
this low a value is sometimes only ±250 ppm/°C, which is not good enough.

**Route 3 — two ordinary chip resistors in parallel (guaranteed available).**

> **1 Ω ∥ 2.2 Ω = 0.6875 Ω** — that is **within 1 % of 0.68 Ω**.

| Part | Value | LCSC | Buy link | **Order** |
|---|---|---|---|---|
| Rb-a | 1 Ω 0805 1 % | **C25271** | [C25271](https://www.lcsc.com/product-detail/C25271.html) | **1,100** |
| Rb-b | 2.2 Ω 0805 1 % | **C17521** | [C17521](https://www.lcsc.com/product-detail/C17521.html) | **1,100** |

Both are Basic parts and always in stock. Two footprints instead of one, both
±100 ppm/°C, and the current divides between them automatically because 2 Ω is
enormous compared to any track resistance. **If Route 1 has no stock, build the
PCB with two pads side by side so either route drops in.**

> **Design tip:** lay out `Rb` as **two 1206 pads in parallel** from the start.
> Fit one current-sense resistor across one pair, or two ordinary resistors
> across both. That single decision removes the sourcing risk permanently.

#### Prototype sweep parts

For finding the right values on the first 10 boards, tolerance and temperature
coefficient **do not matter** — you are only hunting the value. Buy the cheap
ordinary parts:

| For | Values | LCSC parts |
|---|---|---|
| `Rf2`/`Rf3` timing | 820 Ω / 1.2 kΩ / **1.5 kΩ** / 1.8 kΩ / 2.2 kΩ | C17837 · C17379 · C4310 · C17398 · C17520 |
| `Rv5` voltage range | 62 Ω … 470 Ω | search LCSC 0805 1 % by value |
| `Rb` clamp range | 0.47 Ω … 1.0 Ω | 1 Ω is **C25271**; for the sub-ohm values buy a cheap assorted SMD low-ohm kit from AliExpress |

Buy **20 of each** sweep value. The whole sweep is under US$ 15.

#### Before you place a 4,200-piece order

LCSC part numbers are stable, but **stock and price are not**. On each product
page check: the **value and tolerance in the title match**, the **stock covers
your quantity**, and the **price break** — most of these drop sharply at 1,000+
pieces. Order the whole quantity in one go; a second reel from a different batch
is a different batch.

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

| For | Buy 10 each of these, 1 % |
|---|---|
| **`Rb`** (clamp range) | 0.47 Ω, 0.51 Ω, 0.56 Ω, 0.62 Ω, **0.68 Ω**, 0.75 Ω, 0.82 Ω, 1.0 Ω — **current-sense type**, 1206 |
| **`Rv5`** (voltage range) | 62 Ω, 100 Ω, **150 Ω**, 220 Ω, 330 Ω, 470 Ω |
| **`Rf2`/`Rf3`** (timing) | 820 Ω, 1.2 kΩ, **1.5 kΩ**, 1.8 kΩ, 2.2 kΩ — buy **20** of each, they go in pairs |

About **US$ 15 of resistors.** It is the difference between locking the design in
half a day and finding the problem at unit 300.

For the sweep only, tolerance and tempco do not matter — you are finding the
right *value*. Once the value is fixed, buy the production parts to the
specification in section 7.

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
