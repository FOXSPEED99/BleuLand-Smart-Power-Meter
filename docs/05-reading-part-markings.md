# Reading resistor and capacitor markings

**Who this is for:** anyone ordering parts or checking a bag of components on the
assembly bench.

You will see the same 1 kΩ resistor written as `1001`, `102`, `01B`,
`0805W8F1001T5E` and `RC0805FR-071KL`. All five mean 1 kΩ. Here is why.

---

## The big idea: there are TWO different numbers

| | What it is | Where you see it | Example for 1 kΩ |
|---|---|---|---|
| **The marking** | 3 or 4 characters printed on the black body of the part | On the part itself | `1001` |
| **The part number** | The manufacturer's catalogue code | On the reel label, on LCSC, in your order | `0805W8F1001T5E` |

They are not the same thing, and they are not interchangeable. **You order by part
number. You check by marking.**

---

## 1. The 3-digit marking — used on ±5 % parts

**First two digits = the number. Third digit = how many zeros to add.**

| Marking | Working | Value |
|---|---|---|
| `102` | 10, then 2 zeros → 1000 | **1 kΩ** |
| `101` | 10, then 1 zero → 100 | **100 Ω** |
| `103` | 10, then 3 zeros → 10000 | **10 kΩ** |
| `151` | 15, then 1 zero → 150 | **150 Ω** |
| `472` | 47, then 2 zeros → 4700 | **4.7 kΩ** |
| `4R7` | R is the decimal point | **4.7 Ω** |
| `000` or `0` | — | **0 Ω link** |

## 2. The 4-digit marking — used on ±1 % parts

**First THREE digits = the number. Fourth digit = how many zeros to add.**

This is the system our board uses, because all our resistors are ±1 %.

| Marking | Working | Value |
|---|---|---|
| `1001` | 100, then 1 zero → 1000 | **1 kΩ** |
| `1000` | 100, then 0 zeros → 100 | **100 Ω** |
| `1002` | 100, then 2 zeros → 10000 | **10 kΩ** |
| `1500` | 150, then 0 zeros → 150 | **150 Ω** |
| `1501` | 150, then 1 zero → 1500 | **1.5 kΩ** |
| `2001` | 200, then 1 zero → 2000 | **2 kΩ** |
| `4701` | 470, then 1 zero → 4700 | **4.7 kΩ** |
| `1R00` | R is the decimal point | **1 Ω** |
| `2R20` | R is the decimal point | **2.2 Ω** |
| `R680` | R is the decimal point | **0.68 Ω** |

### ⚠️ The mistake everybody makes

> **`1000` is 100 Ω, NOT 1000 Ω.**

`1000` and `1001` sit next to each other in a parts drawer and are **ten times
apart**. If you fit `1000` where `1001` belongs, the board still works — it just
reads wrong, and you will spend a week looking for it.

**The rule:** count the characters first.
- **3 characters** → last one is the zero count, first two are the number.
- **4 characters** → last one is the zero count, first **three** are the number.

So `102` (3 chars) and `1001` (4 chars) are **the same 1 kΩ**. One is the 5 %
system, the other is the 1 % system.

## 3. The letter code (EIA-96) — you will NOT see this on our board

On very small parts (0402 and smaller) there is no room for 4 characters, so they
use 2 digits + 1 letter. The digits are an index into a lookup table, the letter
is the multiplier.

| Letter | Multiply by |
|---|---|
| A | × 1 |
| B | × 10 |
| C | × 100 |
| D | × 1000 |

A few of the table's digit codes: `01` = 100, `18` = 150, `30` = 200.

- `01B` = 100 × 10 = **1 kΩ**
- `18A` = 150 × 1 = **150 Ω**
- `01C` = 100 × 100 = **10 kΩ**

**Our board uses 0805 parts, which are large enough for the 4-digit code.** You
will not meet this system. If you ever do, use an online SMD resistor calculator
rather than memorising the table.

## 4. Some parts have no marking at all

Many 0603 and smaller resistors — and some 0805 — are printed with **nothing**.
A blank black rectangle.

**This is why the workshop rule below matters more than any of the tables above.**

---

## Decoding the part number

### UNI-ROYAL (what we are buying)

> `0805` `W8` `F` `1001` `T5E`

| Piece | Meaning |
|---|---|
| `0805` | Package size |
| `W8` | 1/8 W power rating (1206 parts say `W4` = 1/4 W) |
| `F` | ±1 % tolerance (`J` would be ±5 %) |
| `1001` | **The value — same 4-digit code as the marking** → 1 kΩ |
| `T5E` | Packaging code (tape and reel) |

So `0805W8F1001T5E` and a part stamped `1001` are the same thing. The value code
is sitting right there in the middle of the part number.

### YAGEO

> `RC` `0805` `F` `R-07` `1K` `L`

Yageo writes the value in **plain text** (`1K`) instead of the digit code. Same
resistor, different house style. `RC` = thick film chip, `F` = ±1 %, `L` =
lead-free.

### Every other manufacturer has its own style

Do not try to learn them all.

> **Golden rule for ordering: ignore the part number and read the LCSC page
> title.** It always spells out the real specification in plain language, e.g.
> *"125mW Thick Film Resistor 150V ±1% ±100ppm/℃ 1kΩ 0805"*. That line is the
> truth. The part number is just a code for it.

---

## What our board's resistors should look like

| Board label | Value | Marking you should see | LCSC part |
|---|---|---|---|
| Rf1, Rls1, R3, R4 | 1 kΩ | `1001` | C17513 |
| Rf2, Rf3 | 1.5 kΩ | `1501` | C4310 |
| Rls2 | 2 kΩ | `2001` | C17604 |
| R5, R6 | 4.7 kΩ | `4701` | C17673 |
| Rv5 | 150 Ω | `1500` | C17471 |
| R7 | 0 Ω link | `000` or `0` | C17477 |
| Rb | 0.68 Ω | `R680` | see parts list |
| Rb (parallel option) | 1 Ω + 2.2 Ω | `1R00` and `2R20` | C25271 + C17521 |

**Rv1–Rv4 (47 kΩ) are through-hole**, so they have colour bands, not digits. A
±1 % part has **five** bands:

> **yellow · violet · black · red · brown** = 4 · 7 · 0 · ×100 · ±1 % = **47 kΩ ±1 %**

⚠️ A ±5 % carbon film part has only **four** bands (yellow · violet · orange ·
gold). **Four bands means it is the wrong part** — see section 7b of the parts
list for why these must be metal film.

---

---

## Capacitor markings

Capacitors use **the same 3-digit system** as resistors — with one difference
that changes everything:

> **A resistor code is in ohms. A capacitor code is in PICOfarads.**

First two digits = the number, third digit = how many zeros, answer in pF.

| Marking | Working | Value | Also written |
|---|---|---|---|
| `103` | 10, 3 zeros → 10,000 pF | **10 nF** | 0.01 µF |
| `333` | 33, 3 zeros → 33,000 pF | **33 nF** | 0.033 µF |
| `104` | 10, 4 zeros → 100,000 pF | **100 nF** | 0.1 µF |
| `106` | 10, 6 zeros → 10,000,000 pF | **10 µF** | — |
| `473` | 47, 3 zeros → 47,000 pF | **47 nF** | 0.047 µF |
| `220` | 22, 0 zeros → 22 pF | **22 pF** | — |

A letter after the digits is the tolerance: `K` = ±10 %, `M` = ±20 %,
`J` = ±5 %. So `104K` is 100 nF ±10 %.

### ⚠️ The marking does NOT tell you the dielectric

This is the most important thing on this page. `104` on a good X7R capacitor and
`104` on a rubbish Y5V capacitor look **exactly the same**, and one of them loses
**over 80 % of its value** when the breaker panel gets hot.

You cannot see it, measure it on the bench at room temperature, or read it off
the body. **The only place it is written is the part number and the datasheet.**

> `CC0805` `K` `R` `X7R` `9BB` `104`
>
> Yageo puts it in the middle of the part number in plain text: **X7R**.

**So: buy capacitors by LCSC part number, never from an unlabelled bag.** For
this board the four numbers are **C49678**, **C15850**, **C1739**, **C1710**.
See section 8 of the parts list for which goes where and why.

### ⚠️ And the marking does NOT tell you the voltage rating

An X2 mains safety capacitor and an ordinary ceramic can both be marked `104`.
They are completely different components:

- The **X2** part is printed with **`X2`** and **`275VAC`** on its body, and
  fails **open**.
- The ordinary ceramic fails **short** — across live and neutral, that is a fire.

**Nothing goes across the mains unless the part itself says `X2` and `275VAC`.**

## The workshop rule

Markings are for **checking**, never for **identifying**.

1. **Never decant.** Keep every value on its own reel or in its own labelled bag.
   The moment loose 1 % resistors from two values get mixed, the only way to sort
   them is one at a time with a multimeter.
2. **Label the bag the second it is opened** — value, LCSC part number, date.
3. **Before each batch**, take one part from the reel and measure it. Thirty
   seconds; catches a mis-picked reel before it reaches 200 boards.
4. **When a board reads wrong**, check `Rb`, `Rf2`, `Rf3` and `Rv5` against the
   table above before suspecting anything else. A swapped resistor is far more
   likely than a bad chip.
