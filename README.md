# BleuLand Smart Power Meter — Phase 1 (Electronics / PCB Design)

Non-invasive, single-channel, whole-house Wi-Fi energy monitor for 230 V / 50 Hz
single-phase homes. Designed for hand assembly in batches of 1,000+ units.

---

## What this repository contains

Phase 1 is a **paper design**: a complete, buildable circuit specification with a
costed bill of materials, a production test plan and layout rules. There is no
schematic capture file yet — the next step is to draw this in KiCad.

| Document | What it covers |
|---|---|
| [`docs/01-architecture.md`](docs/01-architecture.md) | The architecture and *why* each major decision was made |
| [`docs/02-circuit.md`](docs/02-circuit.md) | Block-by-block circuit design with all component values and the maths behind them |
| [`docs/03-bom.md`](docs/03-bom.md) | Full bill of materials: quantity per unit, role, alternatives |
| [`hardware/bom.csv`](hardware/bom.csv) | The same BOM as a spreadsheet-ready CSV |
| [`docs/04-calibration-and-test.md`](docs/04-calibration-and-test.md) | Production test, calibration, jigs and the equipment to buy |
| [`docs/05-layout-and-enclosure.md`](docs/05-layout-and-enclosure.md) | PCB layout rules, isolation/creepage, antenna, enclosure |
| [`docs/06-risks-and-decisions.md`](docs/06-risks-and-decisions.md) | Risks, limitations and decisions you should be aware of |
| [`docs/07-assembly-and-tooling.md`](docs/07-assembly-and-tooling.md) | Hand assembly order, and whether to buy a stencil + hotplate |

---

## The design in one paragraph

A split-core current clamp (CT) goes around the house's main live conductor, so
no house current ever enters the product. The board taps L and N for two
purposes: to power itself through an **isolated** AC-DC module, and to measure
mains voltage through a small **voltage transformer**. Because both the current
signal and the voltage signal arrive through magnetics, the entire electronics
section is galvanically isolated from the mains — it is safe to touch, safe to
probe and safe to plug a USB-serial adapter into while the unit is running. A
dedicated energy-metering IC (ATM90E26) does the real maths — RMS voltage, RMS
current, real power, power factor, frequency and accumulated energy — and an
ESP32 module reads it over SPI, timestamps it from a battery-backed RTC, buffers
readings in its own flash when the internet is down, and pushes them to your
server over Wi-Fi.

```
                     ┌─────────── ISOLATION BARRIER ───────────┐
                     │                                         │
 House main cable    │                                         │
   ══════╪══════     │                                         │
      ╭──┴──╮        │                                         │
      │ CT  │────────┼──► burden R ──► ┌──────────┐            │
      ╰─────╯        │                 │          │            │
                     │                 │ ATM90E26 │──SPI──► ┌──────────┐
   L ───[F]──┬───────┼──► ZMPT101B ──► │ metering │         │  ESP32   │──► Wi-Fi
             │       │    (V sense)    │    IC    │         │ WROOM-32E│
   N ────────┼───────┼──► ZMPT101B ──► └──────────┘         └────┬─────┘
             │       │                                           │ I2C
             └───────┼──► HLK-PM01 ──► 5 V ──► 3.3 V ──► rails   │
                     │    (isolated PSU)                    ┌────┴─────┐
                     │                                      │ DS3231   │
        MAINS SIDE   │              SELV (SAFE) SIDE        │   RTC    │
                     └──────────────────────────────────────└──────────┘
```

## Headline numbers

| | |
|---|---|
| Supply | 230 V ± 20 %, 50 Hz, single phase, L + N |
| Measurement range | 0 – ~78 A (sized for a 63 A main breaker with headroom) |
| Target accuracy | ±1 % of reading above 200 W, ±2 % from 50 – 200 W |
| Board size | ~50 × 45 mm, 2-layer FR4 |
| Parts per unit | 53 placements (34 SMD, 19 through-hole) + coin cell + 1 external CT |
| Estimated unit cost @1,000 | ~US$ 14.6 including the clamp, ~US$ 10.1 without |

## Status

Phase 1 design complete and ready for schematic capture. Two component values
(`R_BURDEN` and `R_VSENSE`) are marked **VERIFY ON PROTOTYPE** — see
[`docs/02-circuit.md`](docs/02-circuit.md) §3.3. Build 5 prototypes and lock
these before committing to a 1,000-unit component order.
