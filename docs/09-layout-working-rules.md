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

---

# All SMD on the bottom layer

A good decision — it is how mixed through-hole and surface-mount boards are
really built, and it means **the whole SMD side reflows in one hotplate pass**
later. It also freed the space that took the board from 85 to 75 mm.

It brings three consequences that are easy to miss.

## ⚠️ 1. Every through-hole lead now lands in the middle of the SMD side

The big parts mount on top, but **their leads are soldered on the bottom** —
which is now covered in surface-mount parts, already reflowed.

**Rule: keep at least 2.5 mm of clear space around every through-hole pad on the
bottom side.** An iron tip needs to reach those pads without touching a reflowed
part beside them.

This is one of the "empty spaces" you can see. **It is not waste.**

## ⚠️ 2. The assembly order is now fixed and cannot be reversed

1. Paste, place and **reflow the bottom side**
2. Flip, insert the through-hole parts from the top
3. **Hand-solder their leads on the bottom**, between the reflowed parts

A hotplate cannot reflow a board that already has through-hole parts fitted, so
**the SMD side is always first**. You will also want a simple jig or frame to
hold the board at step 3, because it can no longer lie flat on its bottom face.

## 🔴 3. The switching supply must not sit above the analog block

This is the one that can quietly cost accuracy.

The burden resistor, the filters and the metering chip are now all on the
bottom. If the **HLK power supply sits on the top side directly above them**,
its switching noise couples straight down through 1.6 mm of fibreglass into a
**20 mV** signal.

> **Rule: the power supply and the analog block must be in different regions of
> the board in X-Y — not merely on different layers.**

Also keep the **top layer under the analog block as unbroken ground pour**. On a
two-layer board with a crowded bottom side, that pour is the only clean return
path the differential pair has.

---

# Before shrinking any further

## Check depth first — it is probably the real limit

The goal is fitting inside the panel, and in a breaker panel the binding
dimension is usually **depth**, not width.

| Layer | Height |
|---|---|
| Bottom-side SMD parts | ~2.5 mm |
| PCB | 1.6 mm |
| **Tallest top part** (ZMPT or the power supply) | **~20 mm** |
| Enclosure walls and clearance | ~4 mm |
| **Total** | **≈ 28 mm** |

**Measure the actual free depth in the target panel before doing anything else.**
If 28 mm is the tight dimension, then **every millimetre taken off X and Y is
wasted effort** — the device still will not fit, and the fix is a shorter part,
not a smaller board.

## Reshape, do not shrink

**Below the enclosure's internal size, a smaller board buys nothing.** The box
does not shrink with it.

DIN and panel enclosures are **long and narrow**, not square — a 6-module box is
roughly 105 mm wide by 90 mm deep inside. A **75 × 75 square may not fit a box
that wants 90 × 50**, while a board of the same area in the right shape drops
straight in.

> **The question is not "how small can this board be".** It is **"what shape does
> the smallest enclosure that fits actually want?"** Measure the box, then
> reshape the outline to its slot.

## Empty space that must stay empty

Before filling a gap, check which kind it is:

| Gap | Why it stays |
|---|---|
| **The 8 mm mains barrier** | Safety. Never fill it, never route across it |
| ⚠️ **Around the ESP32 antenna** | **No copper at all** — no pour, no tracks, above or below. Fill it and the range collapses, which matters most inside a metal panel |
| **2.5 mm around every through-hole pad on the bottom** | Iron access after reflow |
| **In front of the terminal blocks** | A screwdriver has to reach the screws |
| **Mounting holes and standoffs** | The enclosure needs them |

## If you still want height back

These move parts off the top and onto the bottom, which is where the room is:

| Change | Gain |
|---|---|
| **Crystal → SMD 32.768 kHz** (3.2 × 1.5 mm) | Removes a through-hole can from the top |
| **470 µF → SMD electrolytic or polymer** | Removes an 11 mm can |
| **Coin cell holder → SMD type, on the bottom** | Removes ~20 mm² of top space and 3 mm of height |

None of these touch the circuit. They only move parts to the side that has room.

---

# The 470 µF capacitor — do not shrink the value

It is 8 mm across and it is in the way. It is also **correctly sized**, and two
independent things confirm it:

- **The ESP32 draws up to 500 mA in WiFi transmit bursts**, and switches into
  that demand in **microseconds**. The standard recommendation for an ESP32 on a
  5 V rail is **470 µF to 1000 µF**.
- **The HLK's own recommended output capacitor is 470 µF.** It is not padding —
  it is the manufacturer-side value for stability.

⚠️ **Cutting it to 100 µF buys a few mm² and pays for it with random resets in
the field** — the worst failure there is. Intermittent, only in the customer's
panel, and impossible to reproduce on your bench.

## First: is it in the right place?

It exists to serve **the ESP32's transient**, not to decorate the power supply
output. If it currently sits next to the HLK and the ESP32 is 40 mm away, the
track inductance between them cancels much of its benefit.

> **Put it next to the ESP32's 5 V and GND pins.** If the ESP32 and the HLK are
> near each other, one capacitor does both jobs.

## Three ways to get the space back

### 1. ⭐ Polymer aluminium, same 470 µF

Same capacitance, much better part:

| | Radial electrolytic (now) | Polymer aluminium |
|---|---|---|
| Footprint | 8 mm circle ≈ **50 mm²** | 7.3 × 4.3 ≈ **31 mm²** |
| Height | **~11 mm** | **~4.2 mm** |
| ESR | ~200 mΩ | **~20 mΩ** |
| Life in a hot panel | dries out | **does not** |
| Price | ~$0.05 | ~$0.50 |

**38 % less area, a quarter of the height, and ten times lower ESR** — so it
actually holds the rail up *better* than the part it replaces. About **US$ 450
extra across 1 000 units**.

⚠️ **Check the voltage rating.** The small polymer parts are 6.3 V, and 5 V on a
6.3 V part is 79 % of rating — acceptable, but with little margin if the supply
overshoots. Prefer **10 V** if the size still works.

### 2. ⭐ Put it under the ESP32 module

The module sits about **8.5 mm above the board** on its headers. A **4.2 mm
polymer capacitor fits underneath with room to spare** — and that space is
already spent.

**Net cost in board area: zero.** Combined with option 1, this removes the part
from the layout entirely.

⚠️ It must be soldered and tested **before** the module goes on. Nothing under
there can be reached afterwards.

### 3. Shrink the transient instead of the capacitor

The capacitor is sized for the **WiFi transmit burst**. Make the burst smaller
and a smaller capacitor becomes genuinely correct rather than merely hopeful:

```c
WiFi.setTxPower(WIFI_POWER_11dBm);   // default is 19.5 dBm
```

The router is close and the device sends a few hundred bytes a minute — full
transmit power is wasted here. Lower power means a lower peak current draw.

**This must be proved on hardware, not assumed.**

## The test that settles it

**Design the footprint to accept both**, then let the prototype decide:

1. Fit the **470 µF**. Put a scope on the 5 V rail.
2. Trigger a **WiFi association** — the biggest burst the device ever makes.
   Record the lowest point the rail reaches.
3. Swap in **220 µF** and repeat.
4. **The rail must stay above 4.5 V**, or the 3.3 V regulator on the dev board
   starts dropping out.

If 220 µF holds above 4.5 V with margin, the smaller part is **proved**, not
guessed. That is a twenty-minute test on prototype board number one, and it is
the only honest way to answer this.

---

# Ground pours — what to do on this board

**Short answer: both. Two separate pours, on both layers, joined only at `R7`.**

Not two layers — **two regions**. The split is in the copper, not in the stack-up.

## The structure

Because all the surface-mount parts moved to the bottom, the board divides
naturally:

| Layer | Job |
|---|---|
| **Bottom** | Components and **signal routing**. Pour the leftover gaps with ground |
| **Top** | **The return path.** Pour as much solid ground as possible. Route here only what cannot go on the bottom |

Then divide the board surface into **three regions**, on **both** layers:

```
 ┌──────────────────────┬─────────────────────────────┐
 │   MAINS REGION       ║   ANALOG_GROUND pour        │
 │   no pour at all     ║   burden, filters, HLW8032, │
 │                      ║   ZMPT secondary            │
 │   fuse, MOV, X2,     ║─────[R7]────────────────────│
 │   PSU, terminals     ║   GND pour                  │
 │                      ║   ESP32, DS1307, LEDs, 5 V  │
 └──────────────────────┴─────────────────────────────┘
          ▲ 8 mm barrier, slot routed, NO copper either side
```

**Both pours exist on both layers**, stitched top-to-bottom with vias every
5–10 mm.

## The seven rules

**1. The two pours must not touch anywhere except through `R7`.**
That is the whole point of the split. Check it after every pour rebuild — a
polygon that reflows can silently bridge them.

**2. Put `R7` right next to the metering chip's ground pin.**
Not in a corner, not wherever it fits. The analog return currents all converge
at that chip, so that is where the two grounds should meet. Everything else
follows from this.

**3. No trace may cross the boundary — except one.**
A signal that crosses has to send its return current the long way round through
`R7`, which makes an enormous loop.

The **only** trace allowed to cross is the metering chip's **serial output**
(chip `TX` → the divider → the ESP32). That is a **4800 baud** signal; its return
current can take the scenic route and nothing cares.

⚠️ **No analog signal ever crosses.** `I1P`, `I1N`, `VP`, the burden and the
filters all stay entirely inside the analog region.

**4. Solid, unbroken pour on the top layer under the whole analog block.**
The analog parts and their traces are on the bottom, so the top pour is their
return path. **Do not route anything through that area on the top layer** — a
single trace cutting across forces the return current to detour around it.

**5. No pour at all in the mains region.**
Copper poured near mains reduces clearance in ways that are hard to see and hard
to check. Keep mains as discrete wide traces with generous space, and keep both
pours **at least 8 mm** clear of anything mains-connected.

**6. No copper under or around the ESP32 antenna — on either layer.**
No pour, no traces, no stitching vias. Filling it collapses the range, which
matters most inside a metal panel.

**7. ⭐ Use thermal relief on every through-hole ground pad.**

This one is about building a thousand boards, not about electrical performance.
A pad connected **solidly** to a large pour drains heat from the iron so fast
that you get cold joints — and cold joints on ground are the hardest fault to
find afterwards.

**Set thermal relief spokes for every through-hole pad on a pour.** Solid
connections are only for surface-mount pads, which have far less thermal mass.

## Where to put the boundary

Follow the signal chain, not the geometry:

| Over **ANALOG_GROUND** | Over **GND** |
|---|---|
| Clamp terminal, fuse, surge thyristor | ESP32 module |
| Burden resistor, both filter resistors | DS1307, crystal, coin cell |
| All four filter capacitors | Both LEDs and their resistors |
| Both TVS diodes | The 5 V rail, bulk capacitor, decoupling |
| ZMPT secondary, 150 Ω, its filter | The level-shift divider's lower resistor |
| **The metering chip** | |

## Check these after the pours are built

- [ ] `GND` and `ANALOG_GROUND` connect **only** through `R7`
- [ ] `R7` sits beside the metering chip's ground pin
- [ ] Only one trace crosses the boundary, and it is the slow serial line
- [ ] No trace runs across the top-layer pour under the analog block
- [ ] Both pours are ≥ 8 mm from anything mains-connected
- [ ] No copper of any kind in the antenna keepout
- [ ] Every through-hole ground pad has thermal relief spokes
- [ ] Stitching vias every 5–10 mm, especially around the analog block

## Worth knowing for v2

**A 4-layer board with a dedicated ground plane makes most of this go away.**
The plane is solid by construction, the split becomes unnecessary, and the
return path under every signal is automatic.

It roughly doubles the bare-board cost — about **US$ 1 more per device**, or 7 %
of the bill of materials. Not for v1, but it is the single change that would
most improve the analog performance and most simplify the layout.
