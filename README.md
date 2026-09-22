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
| **[`hardware/purchase-list.md`](hardware/purchase-list.md)** | **What to buy** — identical parts aggregated into 40 order lines, with spares |
| [`hardware/purchase-list.csv`](hardware/purchase-list.csv) | The same purchase list as CSV |
| **[`docs/09-netlist.md`](docs/09-netlist.md)** | **Every net, every pin** — for schematic entry in Altium |
| [`tools/accuracy_model.py`](tools/accuracy_model.py) | Runnable model behind the accuracy numbers — edit it with your own load profile |
| [`docs/04-calibration-and-test.md`](docs/04-calibration-and-test.md) | Production test, calibration, jigs and the equipment to buy |
| [`docs/05-layout-and-enclosure.md`](docs/05-layout-and-enclosure.md) | PCB layout rules, isolation/creepage, antenna, enclosure |
| [`docs/06-risks-and-decisions.md`](docs/06-risks-and-decisions.md) | Risks, limitations and decisions you should be aware of |
| [`docs/07-assembly-and-tooling.md`](docs/07-assembly-and-tooling.md) | Hand assembly order, and whether to buy a stencil + hotplate |
| [`docs/08-v2-upgrade-path.md`](docs/08-v2-upgrade-path.md) | The ATM90E26 design held in reserve for v2 |

---

## The design in one paragraph

A split-core current clamp (CT) goes around the house's main live conductor, so
no house current ever enters the product. The board taps L and N for two
purposes: to power itself through an **isolated** AC-DC module, and to measure
mains voltage through a small **voltage transformer**. Because both the current
signal and the voltage signal arrive through magnetics, the entire electronics
section is galvanically isolated from the mains — it is safe to touch, safe to
probe and safe to plug a USB-serial adapter into while the unit is running. A
dedicated energy-metering IC (**HLW8032**) does the real maths — RMS voltage,
RMS current, real power, power factor and accumulated energy — and an ESP32
module reads its UART stream, timestamps it from a battery-backed RTC, buffers
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
                     │                 │ HLW8032  │─UART──► ┌──────────┐
   L ───[F]──┬───────┼──► ZMPT101B ──► │ metering │  4800   │  ESP32   │──► Wi-Fi
             │       │    (V sense)    │    IC    │  baud   │ WROOM-32E│
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
| Target accuracy | **±2–3 % of reading above 200 W.** Hard floor at ~50 W — see [risks §6.4](docs/06-risks-and-decisions.md) |
| Board size | ~50 × 45 mm, 2-layer FR4 |
| Parts per unit | 53 placements (35 SMD, 18 through-hole) + coin cell + 1 external CT |
| Estimated unit cost @1,000 | ~US$ 13.5 including the clamp, ~US$ 9.0 without |

## Status

**v1 baseline: HLW8032.** Chosen deliberately over the more accurate ATM90E26
because it is hand-solderable at 1.27 mm pitch, has ~32,000 pieces in stock
against the ATM90E26's ~230, and costs US$ 1.05 less. It gives up about 0.3 % of
daily accuracy and a much worse low-load floor. Full reasoning in
[`docs/01-architecture.md`](docs/01-architecture.md) §1.4; the ATM90E26 design is
preserved for v2 in [`docs/08-v2-upgrade-path.md`](docs/08-v2-upgrade-path.md).

Design complete and ready for schematic capture. Three component values (`Rb`,
`Rv5`, `Rf2`/`Rf3`) are marked **VERIFY ON PROTOTYPE** — see
[`docs/02-circuit.md`](docs/02-circuit.md) §3.3. Build 5 prototypes and lock
these before committing to a 1,000-unit component order.
