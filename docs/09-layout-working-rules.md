# Working rules for the PCB layout

**Why this file exists:** there are a thousand valid solutions for every
placement, so nothing ever feels finished. That is not a skill problem. It is a
**missing stopping rule**. These are the stopping rules.

---

## 1. The real problem: nothing is frozen

Every part can still move, so every change opens new options, forever.

**Fix: freeze in tiers, write the tier down, and never reopen a tier above the
one you are working on.**

| Tier | What | Frozen when |
|---|---|---|
| **1** | **Board outline** | The enclosure is measured |
| **2** | **Connector positions** | Decided by where the wires enter the box — *not* by what routes nicely |
| **3** | **The mains block** — terminal, fuse, MOV, X2, power supply, ZMPT | Tier 2 is frozen |
| **4** | **The ESP32 module** — antenna end overhanging the board edge | Tier 3 is frozen |
| **5** | Everything else | — |

Keep a plain text file next to the project:

```
FROZEN
  outline      75 x 75      2026-09-28
  P1 P2        top edge     2026-09-28
  mains block  left third   ...
```

**Once tiers 1–4 are frozen, most of the thousand options become illegal.** The
remaining parts mostly have one sensible home each.

---

## 2. Stop shrinking. 75 mm is finished.

85 → 75 mm is a **23 % area reduction**. Good. Now stop.

**The enclosure is the constraint, not the board.** If 75 × 75 fits the box, the
next millimetre is worth **exactly nothing** — it does not lower the PCB price
(anything under 100 × 100 is the same tier), it does not help the customer, and
it costs hours.

> **Measure the enclosure today. If 75 fits, freeze the outline and never open
> that question again.**

That one act removes a large share of the daily churn.

---

## 3. The test for "should I change this?"

Right now the test is *"might this be better?"* — which is always yes, forever.

**Replace it with: "does this fix a written rule violation?"** If no, do not
touch it.

The rules are already written, in this repo:

- 8 mm clearance across the mains barrier, with a routed slot
- Analog ground and digital ground joined **only** at `R7`
- Decoupling capacitors within a few mm of the pin they serve
- The `I1P` / `I1N` pair short and symmetric
- Clamp input away from the power supply

**Keep a violations list. Fix them one at a time. Stop when it is empty.**
That turns an infinite aesthetic problem into a finite checklist.

---

## 4. Route in order of consequence, not convenience

Most people route whatever the ratsnest highlights. **Route the signals that can
ruin the product first, while you still have complete freedom.**

| Order | Net | Why first |
|---|---|---|
| **1** | **`I1P` / `I1N`** — burden → filters → chip | A **20 mV** signal. This is the product |
| **2** | `VP` — the voltage channel | Same reason, larger signal |
| **3** | Mains | Thick tracks and clearances dictate their own path |
| **4** | 5 V, 3.3 V, grounds | Wide and forgiving |
| **5** | I²C and the meter serial line | Slow and lazy. They can snake anywhere |

### The one routing detail that actually changes the reading

**`I1P` and `I1N` must be routed as a matched pair:** same layer, side by side,
same length, ground on both sides, and **no other track crossing between them**.

The chip measures the *difference* between them. Anything that reaches one and
not the other becomes a measurement error. This is the single track pair on the
board where care shows up in the product.

Route it first, route it short, and do not let later work push it around.

---

## 5. Placement is an assembly problem, not a density problem

You are hand-building a thousand of these. Placement should minimise **mistakes
per board**, not millimetres.

- **All SMD parts in the same orientation.** Every resistor horizontal, or every
  one vertical. When a person places the 400th board, uniform orientation halves
  the error rate.
- **Group parts by value.** All the 1.5 kΩ near each other, all the 100 nF near
  each other. Fewer reel swaps, fewer wrong picks.
- **Leave at least 0.5 mm between SMD parts** — an iron tip needs to get in.
- **Never put a tall part where it blocks access to a short one.**
- ⚠️ **Everything that lives under the ESP32 module must be one contiguous
  block**, because it all gets soldered and tested *before* the module goes on.
  Scattered under-module parts mean a broken assembly sequence.

---

## 6. Save a numbered copy every single day

`v01-2026-09-26.PcbDoc`, `v02-2026-09-27.PcbDoc`, …

Two reasons, and the second one matters more:

1. You can go back when a "better" idea turns out worse.
2. **You can see that you are moving.** A single file that keeps mutating gives
   no sense of progress, which is most of the feeling of being lost.

---

## 7. If a decision takes more than a few minutes, it does not matter

If two placements were meaningfully different, one would be obviously better
within seconds. **The decisions that matter are obvious, because each has a rule
attached to it.**

Everything else: pick one, move on, never revisit.

---

## 8. Print it at 1:1 and put the real parts on the paper

Before ordering anything. Print the top layer at **exactly 1:1**, lay the actual
components on it, and look.

This catches, in five minutes, what no design rule check ever will:

- Parts that physically collide
- A connector facing the wrong way for the cable
- Somewhere an iron tip cannot physically reach
- Whether the fuse can actually be changed with the board in the box
- Whether the terminal screws can be reached with a screwdriver

---

## 9. What "done" means — decide it now, not later

**Order the boards when all of these are true:**

- [ ] Design rule check passes clean
- [ ] Every net routed, no unrouted connections
- [ ] Mains barrier ≥ 8 mm, slot routed
- [ ] `I1P` / `I1N` routed as a symmetric pair
- [ ] Analog and digital ground meet only at `R7`
- [ ] Board fits the measured enclosure
- [ ] The 1:1 paper check passed
- [ ] The fix list in [`07-schematic-review.md`](07-schematic-review.md) is closed

**Not "when it feels perfect."** That day does not arrive.

---

## 10. The thing worth remembering

**The prototype's job is to answer questions, not to be the product.**

Ten boards exist to confirm three resistor values and prove the circuit works.
The documentation already says `Rb`, `Rv5` and `Rf2`/`Rf3` must be measured on
real hardware — which means **there is going to be a second revision no matter
how good this one is.**

> A 75 mm board with ordinary routing that arrives **next week** teaches you more
> than a 70 mm masterpiece that arrives in **three weeks**.

Version 1 does not need to be good. It needs to be **finished, safe, and
testable**. Make it those three things and send it.
