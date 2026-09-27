# Making the board fit

**Problem:** the first layout lands at roughly **100 × 100 mm**. That is not a
mistake in the layout — it is what these parts actually add up to.

---

## Where the area actually goes

| Part | Footprint | mm² | Share |
|---|---|---|---|
| **ESP32-DevKitC-32E** | 54.4 × 27.9 | **1518** | **32 %** |
| **HLK-5M05** power supply | 38 × 23 | **874** | 18 % |
| **ZMPT101B** transformer | 32 × 20 | **640** | 13 % |
| **Two 5 × 20 mm fuse holders** | 25 × 10 each | **500** | 10 % |
| **CR2032 holder** | 24 × 20 | **480** | 10 % |
| MOV, X2 cap, 470 µF | — | 326 | 7 % |
| Terminal blocks | — | 115 | 2 % |
| DS1307 in **DIP-8** | 10 × 8 | 80 | 2 % |
| Crystal, LEDs, ferrite | — | 69 | 1 % |
| **All 16 resistors + 9 capacitors + both chips + TVS** | — | **349** | **7 %** |
| **Total parts** | | **≈ 4 790** | |

A hand-routed 2-layer board with an 8 mm mains barrier runs at roughly **50 %
utilisation**, so 4 790 mm² of parts → **≈ 9 600 mm² of board ≈ 98 × 98 mm.**

**The estimate of 100 × 100 is correct.** Nothing was done wrong.

### Two things this table settles

**1. Every resistor and capacitor on the board is 7 % of the area.** Arguing
about 1206 versus 0805 moves the board by about 3 mm on a side. It is not where
the problem is.

**2. Deleting the ESP32 board entirely would still leave 68 %.** Going to a bare
module saves about 1 000 mm² and then gives some of it back for a USB-serial
chip, an auto-reset circuit and a regulator. **Correct instinct — it is not the
answer on its own.**

---

## ⭐ The change that beats all the others: build underneath the ESP32

The dev board sits on female headers about **8.5 mm above the PCB**. Everything
in that 349 mm² row above is **under 2.5 mm tall**:

| Part | Height |
|---|---|
| 1206 resistors and capacitors | 0.7 mm |
| HLW8032, DS1307 (in SOIC) | 1.75 mm |
| TVS and surge thyristor, SMB | 2.3 mm |

**All of it fits in the gap under the dev board.** That area is already spent —
the module occupies it whether you use it or not.

⚠️ **One rule:** nothing under there can ever need a soldering iron again once
the dev board is fitted. Solder and test everything underneath **first**, then
fit the headers.

---

## The full reduction plan

| Change | Board saved | Cost |
|---|---|---|
| ⭐ **Small parts under the ESP32 board** | **≈ 700 mm²** | Layout care only |
| **HLK-5M05 → HLK-PM01** (3 W is plenty — the board draws ~150 mA) | ≈ 390 mm² | None |
| **F2 → SMD fuse**, 250 VAC rated, mounted under the ESP32 | ≈ 500 mm² | Not hand-replaceable |
| **F1 → bare fuse clips** instead of a moulded holder | ≈ 300 mm² | Slightly fiddlier |
| **DS1307 DIP-8 → SOIC-8** | ≈ 100 mm² | Solders like the HLW8032 |
| **MOV 14D471K → 10D471K** | ≈ 100 mm² | Lower surge rating, still adequate |
| **CR2032 → CR1220 holder** | ≈ 300 mm² | **5.4 years** of life instead of 8–10 |
| **Total** | **≈ 2 390 mm²** | |

> **9 600 − 2 390 ≈ 7 200 mm² → about 85 × 85 mm.**

If the CR1220 is unacceptable, put the **CR2032 holder on the bottom of the
board** instead and keep the full 8–10 years. Nothing else needs the underside.

---

## The target is wrong, not the board

**Stop aiming at "as small as possible". Aim at two specific numbers.**

### 1. Stay at or under 100 × 100 mm

That is the **standard PCB price tier**. Every fabricator prices 2-layer boards
up to 100 × 100 mm at the cheapest rate, and going even slightly over moves you
into a higher band. **100 × 100 is a sweet spot, not a failure.**

### 2. Fit a standard DIN-rail modular enclosure

These are the plastic boxes that clip onto the rail in a breaker panel, sold by
module width — **6, 8, 9, 10 and 12 modules** (Kradex ZD series and equivalents,
stocked everywhere). They are built to take exactly this class of board.

**Four reasons this beats a 3D-printed box:**

1. **They are flame-retardant.** PLA and PETG are not — this is
   [risk 1.9](04-risks-and-v2.md) in the risk list, and the enclosure removes it.
2. **It clips onto the DIN rail** instead of sitting loose in the panel next to
   live busbars.
3. **It looks like a real product**, which matters when an electrician decides
   whether to install it.
4. **It fixes the target.** No more "as small as possible" — a specific box means
   a specific board outline, and the layout is done when it fits.

⚠️ **Buy the enclosure first, measure its PCB slots, and draw the board outline
from that measurement.** Do not design the board and then hunt for a box.

---

## Order of work

1. **Buy two or three candidate DIN enclosures.** Measure the internal PCB size.
2. Set the board outline to that, not to a guess.
3. Place the **mains section** — terminal blocks, fuse, MOV, X2, power supply,
   ZMPT — in one corner behind the 8 mm barrier. That block cannot shrink and
   cannot move, so place it first.
4. Place the **ESP32 board** next.
5. Put **everything small underneath it.**
6. Whatever is left over goes around the edges.

If it still does not fit after all of that, the honest next step is **two stacked
boards** — a mains board and a logic board on headers. It doubles the bare-PCB
cost (about US$ 1 per device) and roughly halves the footprint. That is what
commercial meters in this class actually do.
