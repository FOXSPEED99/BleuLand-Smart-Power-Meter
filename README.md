# BleuLand Smart Power Meter

A small device that clamps onto the main electricity cable of a house, measures
how much power the home is using, and sends it to a phone app — so the owner can
watch their consumption live and estimate their bill.

Built for **230 V / 50 Hz single-phase homes in Syria**, designed to be
hand-assembled in batches of 1,000+.

---

## The strategy

We are building this in **two versions**, on purpose.

### Version 1 — get it into customers' hands

Every decision in v1 favours **things we can buy locally and build by hand
today** over things that are technically better but slow us down.

- **ESP32 development board**, not a bare module — it plugs into headers, it
  programs over a USB cable, and it is sold in Damascus.
- **HLW8032 metering chip** — an easy 8-pin chip instead of a 28-pin one, costs
  US$ 0.27, and there are tens of thousands in stock.
- Everything else hand-solderable with an ordinary soldering iron.

**Accuracy: ±2–3 % above 200 W.** Honest, adequate for a bill estimate, and
comparable to what commercial clamp meters actually deliver.

### Version 2 — once v1 sells

When the product proves itself and we move to **machine-assembled boards**, the
constraints that shaped v1 disappear. Then we upgrade:

- The **ATM90E26** metering chip — better accuracy, proper phase correction, and
  a much better low-power floor (4 W instead of 45 W).
- A soldered **ESP32 module** instead of a development board — smaller, cheaper,
  fully under our control.

**Four rules in v1 keep that door open.** See [the v2 plan](docs/04-risks-and-v2.md).

---

## Where the project is now

**The design is complete and ready to draw as a PCB.**

Three component values are marked "confirm on prototypes". Build five boards,
test them, lock the values in, then order for the full run. About half a day of
work that protects the entire production run.

---

## What is in this repository

| File | What it is |
|---|---|
| [`docs/01-how-it-works.md`](docs/01-how-it-works.md) | How the device works, and why each major choice was made |
| **[`docs/02-connections.md`](docs/02-connections.md)** | **The complete wiring guide — every connection, in plain language** |
| [`docs/03-build-test-calibrate.md`](docs/03-build-test-calibrate.md) | Assembly, testing and calibration for production |
| [`docs/04-risks-and-v2.md`](docs/04-risks-and-v2.md) | Risks, honest limitations, and the version 2 plan |
| [`docs/05-reading-part-markings.md`](docs/05-reading-part-markings.md) | How to read the codes printed on resistors and capacitors, and what each of ours should say |
| **[`hardware/parts-to-buy.md`](hardware/parts-to-buy.md)** | **The shopping list — what to buy and how many** |
| [`hardware/parts-to-buy.csv`](hardware/parts-to-buy.csv) | The same list as a spreadsheet |

---

## The design in one picture

```
                      ┌──────── SAFETY BARRIER ────────┐
                      │                                │
  House main cable    │                                │
     ══════╪══════    │                                │
        ╭───┴───╮     │                                │
        │ CLAMP │═════╪═══► burden ──┐                 │
        ╰───────╯     │              │                 │
                      │              ▼                 │
  LIVE ──[fuse]──┬────┼──► ZMPT ──► HLW8032 ──UART──► ESP32 ──► WiFi
                 │    │    (volts)   (measures)  5→3.3V  BOARD
  NEUTRAL ───────┼────┼──► ZMPT ──►     │                 │
                 │    │                 │              DS1307
                 └────┼──► HLK-PM01 ──► 5 V             (clock)
                      │    (isolated)
      ⚡ MAINS ⚡      │         SAFE TO TOUCH
                      └────────────────────────────────┘
```

**The house current never enters the product.** The clamp measures the magnetic
field around the cable. Everything on the right of the barrier is safe to touch,
safe to probe, and safe to plug a USB cable into while the device is running.

---

## Key numbers

| | |
|---|---|
| Supply | 230 V ± 20 %, 50 Hz, single phase |
| Measuring range | **50 W up to ~14 kW** (63 A main breaker) |
| Accuracy | **±2–3 % above 200 W** |
| Reports | Volts, amps, watts, power factor, kWh — every minute |
| Offline storage | Keeps ~40 days of readings if the internet drops |
| Board | 2-layer, ~60 × 55 mm |
| Parts | **51 per device, 35 different items to order** |
| Cost | **≈ US$ 13.87 per device** at 1,000 units |
| Assembly | Hand-solderable throughout — no fine-pitch parts |

---

## What to do next

1. **Buy 3 ESP32 boards** from the local shop. Measure them with callipers and
   confirm the pin order — build the PCB footprint from a real board, not from a
   picture on the internet.
2. **Ask the shop whether they can supply 1,050 from one batch**, and what the
   lead time and bulk price are. This is the single most important sourcing
   question in the project.
3. **Draw the PCB**, following [`docs/02-connections.md`](docs/02-connections.md).
4. **Order 10 prototype sets** plus the resistor sweep values listed in the
   shopping list.
5. **Build five boards**, confirm `Rb`, `Rv5` and `Rf2`/`Rf3`, and lock them.
6. **Then order for the full run.**

---

## ⚠️ Safety

This device connects to 230 V mains, which can kill. Never work on the board
while it is connected to mains. Always use an isolation transformer and an
earth-leakage breaker on the test bench. The full safety rules are at the top of
[`docs/02-connections.md`](docs/02-connections.md) — read them before building
anything.
