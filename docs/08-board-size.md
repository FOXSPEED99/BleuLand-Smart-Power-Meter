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

## Choosing a smaller ESP32 board

The dev board is the biggest single item, so it is the right thing to attack.
Three candidates:

| Board | Size | Area | vs DevKitC | USB on board | Antenna |
|---|---|---|---|---|---|
| **ESP32-DevKitC-32E** (current) | 54.4 × 27.9 | 1 518 mm² | — | ✅ | PCB trace |
| **ESP32-CAM** (AI-Thinker) | 40.5 × 27 | 1 094 mm² | −28 % | ❌ **none** | PCB trace |
| ⭐ **D1 Mini ESP32** | ≈ 34 × 26 | **≈ 884 mm²** | **−42 %** | ✅ | PCB trace |

### Why not the ESP32-CAM

The antenna reasoning is right — it carries a real **ESP32-WROOM-style module
with a PCB trace antenna**, which is exactly the property that disqualified the
SuperMini boards. But three things rule it out:

**1. It has no USB-to-serial chip.** Programming means an external adapter, a
jumper from IO0 to ground, a power cycle, the upload, removing the jumper, and
another power cycle. Call it 60–90 seconds of handling per unit — **17 to 25
hours across 1 000 boards**, with a much higher chance of getting it wrong.
Keeping programming to a plugged-in USB cable was the reason for choosing a dev
board in the first place.

**2. The microSD socket is on the underside.** That kills the single biggest
saving on this page. The board saves 424 mm² of outline but blocks roughly
700 mm² of under-board space — **a net loss**.

**3. Its free pins are a minefield.** Most of its GPIO is spoken for by the
camera and the SD card. What is left is mostly strapping pins: **IO12 must be
low at boot** or the flash voltage comes up wrong, **IO0** selects boot mode,
**IO15** must be low for a silent boot, **IO16** is the PSRAM chip select, and
**IO4 drives the onboard white flash LED**. We need five clean pins — SDA, SCL,
the meter chip's serial line and two LEDs — and finding five without a trap is
uncomfortable.

On top of that, you pay for a camera socket, an FPC connector, an SD slot, PSRAM
and a flash LED, fit all of it, and use none of it.

### ⭐ Use a D1 Mini ESP32 instead

Same ESP32-WROOM module and **the same PCB trace antenna**, but:

- **USB and a serial chip on board** — programming stays a plugged-in cable
- **Smaller than the ESP32-CAM**, ≈ 884 mm² against 1 094
- **Flat underside** — the under-board space stays usable
- **I²C is already on GPIO21 and GPIO22** — the same pins the schematic uses, so
  the DS1307 wiring does not change at all
- Around **US$ 3–4**, cheaper than either of the others

**Saving against the DevKitC: ≈ 634 mm² of parts ≈ 1 270 mm² of board.** That is
larger than every item in the reduction table except the under-board trick.

> With this board the target becomes **≈ 5 900 mm², about 77 × 77 mm.**

⚠️ **"D1 Mini ESP32" is a form factor, not a part number.** Several vendors build
it with small differences — the same trap as the audio socket. **Pick one
supplier, buy five, measure them, and confirm the underside is flat** before the
outline is fixed.

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
