# The clamp input — protection and safety

**You do not need this file to draw the board.** Block 4 of
[`02-connections.md`](02-connections.md) has the wiring, and it is complete on
its own. This file is the reasoning behind it: why the fuse and the crowbar are
there, what happens if someone wires mains into the clamp terminal, and why the
two terminal blocks are different sizes.

Read it when you want to know *why*, or when someone asks you to justify a
design decision — not while you are trying to finish a schematic.

---

## Quick summary

| Question | Answer |
|---|---|
| What is the worst thing that can happen? | Mains wired into the clamp screws |
| Without protection? | Hundreds of joules on the board, fire risk |
| With the fuse and crowbar? | Under one joule — one fuse to replace |
| Does the protection cost accuracy? | **No.** The fuse sits outside the measured path |
| What it costs | About **US$ 0.40** per device |
| The one free protection | The clamp terminal is **too small for a mains wire to fit** |

---

### ⚠️ The clamp arrives with a plug on it. You have to cut it off.

The SCT-013-000 comes with a **3.5 mm stereo plug moulded onto its cable**. A
screw terminal cannot accept that, so for every unit someone must cut the plug
off and strip the two wires.

**This was a deliberate choice.** A socket would avoid the cutting, but a
2-pin screw terminal is just **two holes at a fixed spacing** — identical on
every manufacturer's part, so the footprint can never be wrong. Audio sockets
all have different pin layouts, and picking the wrong footprint means a
thousand unusable boards. Reliability of the footprint won over convenience of
assembly. Revisit it in v2 once a specific socket is qualified.

### Polarity — mark it and keep it consistent

Cutting the plug off loses the one thing the plug guaranteed: **which wire is
which.** The two wires are not interchangeable.

| Wire | Was connected to | Goes to |
|---|---|---|
| **White** | the plug's **tip** | the **clamp signal** point (step 1 below) |
| **Red** | the plug's **sleeve** | **ANALOG GROUND** (step 2 below) |

⚠️ **Check the colours on your actual clamps before building 1,000 of them** —
suppliers do change them. Cut one plug open and look.

Get this backwards and the current waveform is inverted: the meter reports
**negative power**, and if you ever add solar in v2 it will read import and
export the wrong way round. **Print the wire colour next to each screw on the
silkscreen** so an installer cannot get it wrong.

**Connections**

1. One screw of the **clamp terminal block** — the one the **white** wire goes
   into — is your **clamp signal** point. Connect three things: the
   **0.68 Ω burden resistor**, a **protection diode**, and the **first 1.5 kΩ
   filter resistor**.
2. The **other screw** — for the **red** wire — goes to **ANALOG GROUND**.
3. The **burden resistor's other end** goes to **ANALOG GROUND**.
4. The **diode's other end** goes to **ANALOG GROUND**.
5. The **first 1.5 kΩ resistor's other end** is your **current +** point.
   Connect three things: a **33 nF capacitor**, a **10 nF capacitor**, and the
   metering chip's **I1P** pin.
6. Separately, connect **ANALOG GROUND** to the **second 1.5 kΩ resistor**.
7. That resistor's **other end** is your **current −** point. Connect three
   things: the **33 nF capacitor's other end** (the same one from step 5), the
   **second 10 nF capacitor**, and the metering chip's **I1N** pin.
8. Both **10 nF capacitors' other ends** go to **ANALOG GROUND**.

**The second 1.5 kΩ resistor looks pointless but is essential.** It runs from
ground into the chip's negative input. The chip compares its two inputs against
each other — if the two paths have different resistance, noise picked up by the
clamp cable stops cancelling out. **Both resistors must be the same value.**

**They also correct the clamp's timing error.** A clamp shifts the current signal
slightly in time, which makes readings wrong on motor loads. Making these two
bigger than the 1 kΩ voltage filter resistor compensates. 1.5 kΩ is the starting
point — you tune it during calibration, and you always change both together.

### Three things to get right

**1. Keep it on the low-voltage side of the barrier.** The terminal block and
everything it touches belong on the safe side of the 8 mm gap. Never route a
clamp track across the barrier.

**2. The two terminal blocks are different sizes on purpose.** Mains is
**5.08 mm**, the clamp is **2.54 mm** — the smallest terminal that still takes
the clamp cable. Do not "standardise" them to save a part number; that
difference is the safety interlock described above.

**3. Give the cable a strain relief in the plastic case.** A screw terminal grips
bare copper, not insulation, so a pull on the cable puts all the force on the
wire right where it enters the screw, and it work-hardens and snaps. Mould a
slot or clamp into the 3D-printed case that grips the **cable jacket** before it
reaches the board.

### ⚠️⚠️ What happens if someone wires mains into the clamp terminal

**Short answer: yes, it is violent, and yes, it can be fixed in hardware.**
Two different accidents are possible and they behave completely differently.

#### Accident A — live AND neutral into the two clamp screws

The **0.68 Ω burden resistor sits directly across those two screws.** It is the
whole fault path.

| | |
|---|---|
| Voltage across a 0.68 Ω chip resistor | **230 V** |
| Power, if it held | 230² ÷ 0.68 = **78,000 watts** |
| What a 1206 chip resistor survives | a few **hundredths of a joule** |

It does not hold. In sequence, over a few milliseconds:

1. The **protection diode** (SMAJ5.0CA, a 5 V part) avalanches instantly and
   **fails short** — which is what TVS diodes do. The input is now a dead short.
2. The **burden resistor** vaporises. Microseconds.
3. The fault is now limited only by the house wiring — roughly **0.4 Ω**, so
   **500–600 A**.
4. The **63 A breaker** trips magnetically, but that takes about **10 ms**.

**Hundreds of joules** land in a few square millimetres of board. Copper traces
vaporise, and copper vapour is conductive, so it sustains an arc. Expect
fibreglass and molten solder ejected, the plastic enclosure cracked or melted,
and a real ignition risk **inside a breaker panel**.

The **clamp is destroyed too** — its fine secondary winding burns, while it is
wrapped around a live house cable.

⚠️ **The protection diode we already have makes this worse, not better.** It
fails short and there is nothing downstream to clear the short. **A clamping
device with no clearing device is not protection.**

#### Accident B — live only, into one clamp screw

Completely different, and in one way worse.

The low-voltage side of the board is **isolated** from mains by the power
module's transformer. Put live on one clamp screw and there is no return path,
so **almost no current flows** — a fraction of a milliamp through stray
capacitance.

**Nothing blows. Nothing trips. Nothing looks wrong.** The device keeps working.

But the **entire low-voltage side is now sitting at 230 V** relative to earth:
the clamp cable, the clamp, the ESP32, and the USB socket on it. The enclosure
and the clamp's own insulation are all that stand between that and a person.

**No component on the board can fix Accident B.** There is no voltage *across*
anything — the whole side floats up together. Only mechanical prevention helps.

---

### The fix for Accident A — a fuse and a crowbar

This is the standard protection used on telephone line cards, which face exactly
this hazard (mains contacting a phone line). Two parts:

```
                     ┌── FUSE ──┬──────────┬─── clamp signal ──[1.5k]─► I1P
 clamp screw 1 ──────┘          │          │
                            CROWBAR      0.68 Ω
                                │          │
 clamp screw 2 ─────────────────┴──────────┴─── ANALOG GROUND ─[1.5k]─► I1N
```

**The crowbar** (a thyristor surge protector, ~58 V breakover) does nothing
until the voltage across the input goes above about 58 V. Then it switches to a
near short and holds the node at **about 3 volts**. The burden resistor never
sees more than that.

**The fuse** then clears the fault. With the crowbar holding the line down, the
current through the fuse is hundreds of amps, and a small fast fuse opens in
**microseconds**.

| | Today | With fuse + crowbar |
|---|---|---|
| Energy into the board | **hundreds of joules** | **under one joule** |
| Time to clear | ~10 ms (breaker) | ~2 µs (fuse) |
| Outcome | explosion, ignition risk | two parts to replace |

#### Why this costs **zero** accuracy

This is the part that makes it work. **Put the fuse outside the measured path.**

The chip measures the voltage across the **burden resistor only** — the filter
resistor taps the node *between* the fuse and the burden. The fuse carries the
clamp current but its voltage drop is never measured. **Its resistance and its
temperature coefficient do not enter the reading at all.**

The fuse does add its resistance to the clamp's total loop burden, and that does
affect the clamp itself — but there is enormous room. OpenEnergyMonitor measured
this same clamp with a **22 Ω** burden in the emonPi and emonTx V3 and found the
phase error there is about 4°, which they call insignificant. Our loop is
**0.68 Ω**, and a 500 mA fuse adds under **1 Ω**. We stay far inside proven
territory.

The crowbar is off in normal operation — leakage is nanoamps and its capacitance
is tens of picofarads, which is nothing at 50 Hz.

#### What to buy

| Part | Specification | Why |
|---|---|---|
| **Fuse** | **500 mA, fast-acting, rated 250 VAC** | Clamp delivers at most 50 mA, so 10× headroom — it will never nuisance-blow |
| **Crowbar** | Thyristor surge protector (TSPD / SIDACtor type), **~58 V breakover**, bidirectional | Above the clamp's own 22 V internal limit, so it never interferes; far below anything that hurts the board |

⚠️ **The fuse must be rated 250 VAC, not 63 V.** Most small SMD fuses are 63 V
parts — across 230 V they arc over instead of interrupting, and then they are
not a fuse at all. Same rule as the mains fuse in Block 1.

💡 **Keep the SMAJ5.0CA too.** It still handles the everyday job — static from
handling the clamp cable. The crowbar handles the catastrophic job. They are not
alternatives.

**Cost: roughly US$ 0.40 per device** — about 3 % of the bill of materials, to
turn a fire into a blown fuse.

---

### After the fuse blows — what state is the device in?

**The board survives. One part is used up: the fuse.**

| Part | State afterwards |
|---|---|
| **Fuse** | **Blown. Must be replaced.** |
| Crowbar | **Survives.** It only conducts for a few microseconds before the fuse opens — far inside its surge rating |
| 0.68 Ω burden resistor | Survives — the crowbar never let it see more than ~3 V |
| Metering chip, ESP32, power supply | Untouched |
| The clamp itself | Survives |

**But the device does not keep working.** With the fuse open, no clamp signal
reaches the chip. It will read **0 watts, forever**, until someone replaces one
component.

### Why there is no way to make it survive untouched

It is worth understanding why, so nobody spends a month looking for a cleverer
circuit.

For the 0.68 Ω burden resistor to survive on its own, the fault current would
have to stay under about **0.6 A**. At 230 V that needs **more than 380 Ω** in
the loop. But that resistance sits in the clamp's own loop, and a clamp stops
being accurate long before that — OpenEnergyMonitor measured about **10° of
phase error at 120 Ω** and called it troublesome.

> **The resistance that would save the resistor is far more than the resistance
> that ruins the measurement.** There is no value that does both.

A **resettable fuse** (PTC) does not help either. Those are rated for tens of
volts, not 230, and they take tenths of a second to react. At mains voltage they
burn rather than trip.

**So something has to be sacrificed.** The design choice is only *what* — and a
fuse is the cheapest, smallest, most predictable thing to give up.

### The three things that actually help

**1. Make the accident impossible — the 2.54 mm terminal.** Free, and it is the
only measure that also covers the live-only case. This is the closest thing to a
magic answer that exists.

**2. Make the repair trivial.** If a fuse must blow, decide now who replaces it:

| Choice | Board area | Repair |
|---|---|---|
| **Soldered SMD fuse** ← recommended for v1 | almost none | hot-air station, ~2 minutes, by you |
| Sub-miniature fuse in a socket (TR5 / TE5 type) | ~10 × 5 mm | pulled out by hand, no tools |
| 5 × 20 mm cartridge in clips | ~25 × 8 mm | by hand, but eats 12 % of the board |

A device sealed inside a breaker panel needs an electrician to open it whatever
happens, so the socket saves a couple of minutes, not the visit. **Solder it for
v1**; revisit if field returns ever become common.

**3. Make the device say what is wrong.** ⭐ **This is the cheap one, and it
matters most.**

A blown clamp fuse looks exactly like a house using no electricity. Without
firmware help, the customer sees **"0 W"** and assumes the product is broken —
or worse, believes it.

The firmware must be able to tell those apart and report
**"clamp signal lost"**. Two ways, both nearly free:

- **Plausibility check.** A real house is never at exactly 0.000 W for hours
  while mains voltage is present and healthy. Flag it.
- **Switch contact**, if a socket is ever fitted in v2 — a direct, unambiguous
  "nothing is plugged in" signal.

**Turning a silent wrong reading into a clear alert is worth more than any
component on this page.** It is the difference between a customer who calls you
and a customer who stops trusting the product.

### The other half — make the mistake harder to make

The fuse and crowbar fix Accident A. **Only geometry fixes Accident B.** All of
these are physical, not stickers:

1. **Keep the two terminal blocks at opposite ends of the board**, with the
   isolation barrier between them. Wiring both by mistake should mean reaching
   across the whole device.
2. **Use a small-aperture clamp terminal.** The clamp's cable is thin — about
   0.3 mm². A **2.54 mm pitch** terminal block accepts roughly 0.5 mm² and no
   more. Mains wiring in a panel is **1.5 mm² at the very least**. It physically
   will not go in.
3. **Recess the clamp terminal** in the plastic case so only a thin cable can
   reach the screws.
4. **Different colour.** A black clamp terminal beside a blue mains terminal
   costs nothing.

**Point 2 is the strongest single change available**, and it is the one that
also covers Accident B. If you do nothing else here, do that.

### Is it safe to unscrew the clamp while the power is on?

**Yes.** Normally, disconnecting a current transformer while current flows
through the cable it is clamped around is dangerous: the winding tries to push
current into an open circuit and the voltage climbs. The **SCT-013-000 has a
transient voltage suppressor built inside it** for exactly this reason (older
units used two 22 V zener diodes), so the voltage stays at a safe level.

**Good practice anyway:** unclip the clamp from the cable before loosening the
screws.

---
