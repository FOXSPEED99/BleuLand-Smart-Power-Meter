# How It Works, and Why It Was Built This Way

---

## 1. The basic idea

Electricity bills are based on **energy** — kilowatt-hours. Energy is power
multiplied by time. So to estimate a bill, we need to measure **power**, all the
time.

Power in an AC circuit is:

```
Power (watts) = Voltage × Current × Power Factor
```

That third term is the one everybody forgets, and it is why this device measures
**both** voltage and current rather than just current.

---

## 2. Measuring current without cutting any wire

A **current clamp** (a split-core current transformer) opens up, closes around
the main live cable, and measures the magnetic field the current creates. It
never touches the conductor inside.

Our clamp has a ratio of **2000 : 1**. For every 2,000 amps flowing in the house
cable, 1 amp comes out of the clamp's two thin wires. So a 40 A load produces
20 mA from the clamp.

The clamp gives us a *current*, but the measuring chip needs a *voltage*. So we
pass it through one precise resistor — the **burden resistor `Rb`**, 0.68 Ω:

```
40 A in the house  →  20 mA from the clamp  →  20 mA × 0.68 Ω = 13.6 mV
```

**That single resistor's value defines every current reading the device will ever
make.** This is why the parts list insists on 1 % tolerance and 50 ppm/°C
temperature stability. A cheap resistor drifting with the temperature inside a
hot breaker panel would change your customer's bill.

---

## 3. Why we measure voltage too

You could skip the voltage measurement, assume 230 V, and multiply. It would be
much simpler. It would also be wrong, in two different ways.

### Power factor

Motors — fridges, freezers, washing machines, water pumps, air conditioners —
draw current that is out of step with the voltage. The result is that the actual
power is **less** than volts × amps:

| Load | Power factor | 10 A at 230 V really means |
|---|---|---|
| Heater, kettle, incandescent lamp | 1.00 | 2,300 W |
| Mixed household | 0.90 | 2,070 W |
| Fridge, pump, air conditioner | 0.80 | **1,840 W** |

Current-only monitoring would report 2,300 W in every case — **over-reporting by
up to 25 %** in a home full of motors. Your customer's utility meter charges for
real watts. If your app disagrees with their bill by 25 %, the product is
worthless.

### Voltage is not actually 230 V

Syrian distribution voltage moves around a lot. If the real voltage is 200 V and
you assumed 230 V, you are **15 % wrong before you start**.

Measuring voltage costs one small transformer and four resistors. It is the
highest-value decision in the whole design.

---

## 4. How the voltage gets measured safely

We cannot connect mains directly to a measuring chip. Instead:

1. Four **47 kΩ resistors in series** (188 kΩ total) reduce the mains to a tiny
   current — about **1.2 mA** at 230 V.
2. That current flows through the primary of a small transformer, `T1`
   (**ZMPT101B**).
3. The same current appears on the secondary side, but with **no electrical
   connection** between the two.
4. `Rv5` (150 Ω) turns that current back into a small voltage the chip can read.

The transformer is a **physical gap**. Mains cannot cross it.

### Why four resistors and not one

1. **Voltage rating.** A single resistor across 230 V is at its limit and will
   arc over during a surge. Four share the stress — about 58 V each.
2. **Safe failure.** If one fails it fails open, and the chain safely
   disconnects.
3. **Heat.** 0.28 W spread over four parts instead of one hot spot next to mains
   tracks.

---

## 5. The safety barrier — the most important design decision

Look at any cheap smart plug or energy meter and you will usually find that its
electronics sit **at mains potential**. It works, and it is cheaper. We did not
do that.

Our device has **two magnetic components** that let signals and power cross a
physical gap:

| Component | Carries across the barrier |
|---|---|
| `PS1` (HLK-PM01) | Power — 230 V in, isolated 5 V out |
| `T1` (ZMPT101B) | The voltage measurement signal |

Because both paths go through magnetics, **the entire low-voltage side is safe
to touch.**

### Why that was worth the extra US$ 2.70

1. **You are hand-building and testing 1,000 units.** On a non-isolated board,
   plugging a USB cable into a mains-powered unit puts mains voltage on your
   laptop's ground. That destroys laptops and, much worse, people. With
   isolation, a technician can plug in USB on a live running unit safely.
2. **Live and neutral get swapped all the time** in real Syrian distribution
   boards. On a non-isolated board, a reversed installation puts the whole board
   at 230 V. Here, it is harmless.
3. **The clamp's cable is a metre of wire hanging inside a panel.** On our board
   it can never become live.
4. **Liability.** You are selling a product a homeowner or a local electrician
   will fit inside their own panel.

---

## 6. The measuring chip

`U2` is an **HLW8032**. It has two analog-to-digital converters inside, one for
voltage and one for current, and a small processor that does the real maths:
multiplying the two signals together thousands of times a second and averaging
the result.

It sends a **24-byte packet every 50 milliseconds** containing voltage, current,
power, power factor and an energy counter.

### What it can and cannot do

| Can | Cannot |
|---|---|
| Measure V, A, W, power factor, kWh | Be configured — it only talks, never listens |
| Run without an external crystal | Correct the clamp's timing error itself |
| Work reliably from US$ 0.27 | Measure small loads below ~45 W accurately |

Both limitations have answers:

- **The timing error is corrected in hardware** with `Rf2`/`Rf3` (see below).
- **Calibration lives in the ESP32's firmware** instead of the chip.

### The timing correction

A current clamp shifts the current signal slightly in time — about **1.5
degrees**, which at 50 Hz is **83 millionths of a second**. That tiny shift
barely matters on a heater, but costs about **2 % on a motor load**.

The ATM90E26 (our v2 chip) has a register to cancel it. The HLW8032 does not. So
we cancel it with the **filter resistors that are already on the board**: by
making `Rf2` and `Rf3` (1.5 kΩ) larger than `Rf1` (1 kΩ), the current signal is
delayed by exactly enough to line back up with the voltage signal.

**One resistor value, tuned once during calibration, recovers almost all of it.**

---

## 7. The ESP32 board

`MCU1` is an off-the-shelf **ESP32 development board** — the common "ESP32
Type-C" with 30 pins and a metal-shielded ESP-WROOM-32 module.

### Why a ready-made board instead of a bare module

Three reasons, all practical:

1. **It is sold locally in Syria.** No import, no customs, no six-week wait.
   Sourcing was the binding constraint on this project, and this removes it.
2. **It programs over a USB cable.** No programming jig, no header, no
   auto-reset transistors, no serial adapter. Plug in, press upload.
3. **It already contains parts we would otherwise fit ourselves** — a 3.3 V
   regulator, a USB-to-serial chip, an auto-reset circuit and two buttons. That
   is **seven components removed** from our board.

### Why this particular board and not a "SuperMini"

The tiny SuperMini boards look attractive, but they have a **documented antenna
problem**: the board is too small to give a 2.4 GHz antenna the clearance it
needs, and the range is poor enough that people solder wire antennas onto them.

The board we chose carries a **genuine ESP-WROOM-32 module** — a proper,
certified, characterised antenna that someone actually measured. For a device
that lives inside a distribution board, that matters more than size.

### Mounting it right

Plug it into two 15-hole female headers so that:
- the **antenna end overhangs the edge** of our PCB — giving it completely clear
  space, which is *better* RF than a soldered module would have had;
- the **USB socket faces the enclosure wall**, so a technician can update
  firmware without opening the box.

Only **8 of its 30 pins** are used.

---

## 8. Knowing what time it is

`U4` is a **DS1307** clock chip with its own coin cell. Its only job is to keep
time running while the device is switched off.

### Why it is needed at all

The ESP32 can work out most timestamps by itself. It counts seconds since it
powered on and stores that count with every reading. The moment it reaches the
internet and learns the real time, it subtracts backwards:

```
  real time of a reading  =  time now  −  (uptime now  −  uptime when stored)
```

Every buffered reading gets an exact timestamp, retroactively. **So for the
common case — mains on, internet off — no clock chip is needed at all.**

The gap is when **mains cuts while the internet is still down.** The counter
resets to zero, and nothing inside the ESP32 counted while it was dead. It knows
the time is *later* than the last value it saved to flash, but not by how much.

One power cut is recoverable: when the internet returns, the ESP32 can work out
both the current session's times and how long the outage was. **Two or more cuts
before the internet returns is not** — it learns the total time it lost but
cannot split it between the individual outages, so earlier readings can sit
hours out of place on the graph.

In Syrian homes, with daily power cuts and intermittent internet, that is not an
edge case. Hence the clock chip.

### How it works

A DS1307 is a little watch with a **32.768 kHz crystal** as its pendulum. The
crystal vibrates 32,768 times per second — that odd number is 2¹⁵, so the chip
just halves it fifteen times with simple binary dividers and lands on exactly one
tick per second.

A **CR2032 coin cell** keeps it running when mains is off. At 0.84 µA that cell
lasts **8–10 years**, and in this device it only discharges while mains is out,
so realistically the cell's own shelf life is the limit.

On every boot the ESP32 simply asks the chip what time it is, and gets the right
answer — internet or not.

### Accuracy, and why ±3 seconds a day is plenty

The DS1307 has no temperature compensation, so its accuracy is entirely the
crystal's: roughly ±35 ppm, or **about 3 seconds per day**.

That sounds poor next to a DS3231's ±2 ppm, and it does not matter at all. The
ESP32 resets the clock from the internet every time it connects. **The chip's job
is to bridge days, not years.** Paying extra for a decade of unattended accuracy
would be buying something we throw away every time the WiFi comes back.

### The two things that must be right

1. **The chip runs on 5 V, but its data lines are pulled up to 3.3 V.** The
   DS1307 needs 4.5–5.5 V, and ESP32 pins are not 5 V tolerant. Because the data
   lines are open-drain — they can only pull down, never push up — pulling them
   up to 3.3 V keeps the whole bus at 3.3 V. In the other direction the DS1307
   reads anything above 2.2 V as high, so 3.3 V drives it fine.
2. **The battery connects straight to the chip and nothing else.** No diode, no
   resistor, no charging circuit. The chip switches over internally.

Both of these are why the design uses the **bare chip, not a ready-made module**.
The common DS1307 "Tiny RTC" module puts a resistor divider on the battery pin
and pulls its data lines to whatever powers it; the DS3231 "blue module" has a
trickle charger that destroys a non-rechargeable CR2032. Both are broken by
design for this application.

### Firmware rules

1. **The clock chip is the source of truth**; the internet corrects it whenever
   available.
2. **Store the 64-bit microsecond uptime counter with every reading too** — not
   Arduino's `millis()`, which wraps every 49.7 days. It costs nothing and gives
   you a cross-check.
3. **Flag every reading** as *time from internet*, *time from clock chip*, or
   *time estimated*. Your server can then weight the data, and you learn how
   often each case actually happens.

## 9. Storing readings when the internet is down

Internet in Syria is not reliable, so the device must keep working without it.

| | |
|---|---|
| One reading | ~16 bytes (time, volts, amps, watts, energy, flags) |
| How often | once a minute |
| Per day | ~23 KB |
| Space available | ~1 MB of the ESP32's flash |
| **Holds** | **~40 days of readings** |

When the connection comes back, the device uploads everything it missed, in
order.

**Bill from the energy counter, never from the sum of power readings.** The
counter cannot lose energy during a network stall; a sum of samples can.

---

## 10. The two ground zones

The ESP32 draws half an amp in short bursts when it transmits over WiFi. The
measuring chip is reading signals of a few thousandths of a volt. If they share
the same ground path, those bursts appear as noise in the measurements.

So the board has **two ground areas**, joined at exactly one point through `R7`
(a 0 Ω link) placed right beside the measuring chip.

```
    GROUND  ────[R7]────  ANALOG GROUND
   (ESP32,    ONE POINT    (measuring chip,
    clock,                  clamp, filters)
    LEDs)
```

This is one of those details that costs nothing to get right at design time and
is almost impossible to fix afterwards.

---

## 11. What v1 deliberately does not do

| Not included | Why |
|---|---|
| Switching the power on and off | The product is non-invasive monitoring. A relay would put house current through it |
| A second clamp | One channel is what was asked for |
| A screen | The phone app is the interface |
| Solar export measurement | Not needed today — but the hardware can already do it, so firmware must log the sign of the power reading, not just its size |
| CE / EMC certification | Out of scope for the first production run |
| The phone app | A separate project |

---

## 12. What the app will be able to show

Without any hardware change, the device can report every minute:

`time · volts · amps · watts · volt-amps · power factor · total kWh · quality
flags · hardware version`

That is enough for: live consumption, daily/weekly/monthly totals, bill
estimation at a user-entered price per kWh, voltage quality history and brownout
alerts, "which day cost the most", and unusual-usage detection.

**Two rules for whoever builds the backend**, both free now and painful to
retrofit later:

1. **Store the raw volts, amps and watts** — not only the kWh total. When the v2
   board arrives you will want to put an old and a new unit on the same house and
   compare them directly.
2. **Put a `hardware_version` field on every record from day one.**
