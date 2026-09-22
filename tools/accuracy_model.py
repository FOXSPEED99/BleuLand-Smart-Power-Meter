#!/usr/bin/env python3
"""
Accuracy model for the BleuLand Smart Power Meter.

Produces the numbers quoted in docs/01-architecture.md §1.4 and
docs/06-risks-and-decisions.md: what each candidate metering IC would report
for a given load, and the accumulated error over a realistic household day.

This is a MODEL built from published specs plus the physics of CT phase error.
It is not measured data. Get real numbers by running a prototype against a
Class 1 reference meter for 24 h — see docs/04-calibration-and-test.md.

Edit the constants below to match your own CT, tariff and load profile.

Usage:  python3 tools/accuracy_model.py
"""
import math

# ---- Installation -------------------------------------------------------
V_MAINS   = 230.0     # nominal mains voltage
CT_FS_A   = 78.0      # CT + burden full scale, amps
BREAKER_A = 63.0      # main breaker rating

# ---- Front-end error, IDENTICAL for every chip (same clamp/burden/VT) ----
def ct_band_pct(pct_of_fs):
    """SCT-013-class clamp residual after one-point calibration, % of reading."""
    if pct_of_fs < 2:  return 4.0
    if pct_of_fs < 5:  return 2.5
    if pct_of_fs < 10: return 1.5
    return 1.0

BURDEN_TEMPCO_PCT = 0.2    # 50 ppm/degC over a 40 degC swing
V_CHANNEL_PCT     = 0.3    # voltage chain residual after calibration

# ---- Chips: (dynamic range, residual phase error in degrees) -------------
CHIPS = {
    "ATM90E26":                   (5000, 0.20),   # phase register, per unit
    "HLW8032 (no phase fix)":     (400,  1.50),   # CT phase uncorrected
    "HLW8032 + 120nF phase cap":  (400,  0.50),   # hardware compensation
}

def core_pct(chip, pct_of_fs):
    """Metering-core error, worse near the bottom of a limited dynamic range."""
    dr = CHIPS[chip][0]
    if dr >= 2000:                       # ATM90E26 class
        return 0.1
    return 3.0 if pct_of_fs < 2 else 1.5 if pct_of_fs < 10 else 0.5

def phase_bias(chip, pf):
    """Systematic error from uncorrected CT phase shift. Zero on resistive loads.

    P = V*I*cos(phi).  A phase error d makes the meter compute cos(phi - d).
    Near phi = 0 the cosine is flat, so the error vanishes; at phi = 37 deg
    (PF 0.8) it is on the steep part and the error is ~2% per 1.5 deg.
    NOTE: the SIGN depends on your specific CT and voltage transformer.
    """
    d, phi = math.radians(CHIPS[chip][1]), math.acos(pf)
    return math.cos(phi - d) / math.cos(phi) - 1.0

def spread(chip, pct_of_fs):
    """Unit-to-unit amplitude spread, as a fraction (independent terms, RSS)."""
    return math.sqrt(ct_band_pct(pct_of_fs)**2 + BURDEN_TEMPCO_PCT**2
                     + V_CHANNEL_PCT**2 + core_pct(chip, pct_of_fs)**2) / 100

# ---- A realistic household day: (label, hours, watts, power factor) ------
DAY = [
    ("Night / standby (fridge, router)", 8, 250,  0.75),
    ("Morning (kettle, water heater)",   3, 1800, 0.90),
    ("Daytime (lights, TV, fridge)",     6, 700,  0.85),
    ("Evening peak (AC, cooking)",       5, 2500, 0.90),
    ("Late evening",                     2, 500,  0.80),
]

def main():
    print(f"Installation: {V_MAINS:.0f} V, CT full scale {CT_FS_A:.0f} A, "
          f"breaker {BREAKER_A:.0f} A (= {BREAKER_A*V_MAINS/1000:.1f} kW ceiling)\n")

    print("=" * 74)
    print("INSTANTANEOUS READING vs ACTUAL")
    print("=" * 74)
    for actual in (1000.0, 10000.0):
        for pf, label in ((1.00, "resistive"), (0.90, "mixed home"), (0.80, "motor-heavy")):
            amps = actual / (V_MAINS * pf)
            pct  = amps / CT_FS_A * 100
            print(f"\n{actual/1000:g} kW @ PF {pf:.2f} ({label}) -> "
                  f"{amps:.1f} A = {pct:.1f}% of full scale")
            if amps > CT_FS_A:
                print(f"  CLIPPING: every chip saturates at ~{CT_FS_A*V_MAINS*pf/1000:.1f} kW")
                continue
            for chip in CHIPS:
                c = actual * (1 + phase_bias(chip, pf))
                s = spread(chip, pct)
                print(f"    {chip:<28} typ {c:8.0f} W   "
                      f"({c*(1-s):.0f} - {c*(1+s):.0f} W)")

    true = sum(h * w for _, h, w, _ in DAY) / 1000
    print("\n" + "=" * 74)
    print(f"END OF DAY — true total {true:.2f} kWh/day, {true*30:.0f} kWh/month")
    print("=" * 74)
    print(f"{'Chip':<30}{'kWh/day':>10}{'error':>9}{'kWh/month':>12}{'extra':>9}")
    print("-" * 74)
    for chip in CHIPS:
        rep = sum((h*w/1000) * (1 + phase_bias(chip, pf)) for _, h, w, pf in DAY)
        print(f"{chip:<30}{rep:10.2f}{(rep/true-1)*100:+8.2f}%"
              f"{rep*30:12.1f}{(rep-true)*30:+9.1f}")
    print("-" * 74)
    print(f"{'TRUE':<30}{true:10.2f}{'':>9}{true*30:12.1f}")

    print("\nLow-load floor (dynamic range limit):")
    for chip, (dr, _) in CHIPS.items():
        a = CT_FS_A / dr
        print(f"  {chip:<30} {dr:>5}:1 -> {a:.3f} A = {a*V_MAINS:.0f} W")

    print("\nKey point: the unit-to-unit spread from the CLAMP is larger than the")
    print("entire difference between the chips, and the clamp is common to all.")

if __name__ == "__main__":
    main()
