#!/usr/bin/env python3
"""
AETHER 80m liquid hydrogen blended wing body transport sizing.
Calculates mission fuel fractions and iterates takeoff weight from a 220-tonne initial estimate.
"""

import math

# Mission specifications
g = 9.80665
pax_count = 430
pax_mass = 100.0  # kg per passenger including baggage
cargo_mass = 10750.0  # kg freight
payload_mass = (pax_count * pax_mass) + cargo_mass
crew_mass = 12 * 105.0  # 12 crew members at 105 kg

range_m = 12500.0 * 1000.0
cruise_mach = 0.85
cruise_alt = 10668.0  # FL350 (m)

# Fuel properties
lhv_jeta = 42.8e6  # J/kg
lhv_lh2 = 120.0e6  # J/kg
lh2_density = 71.0  # kg/m^3 (liquid at 20.3 K, 2 bar)

# FL350 temperature and cruise true airspeed
T_cruise = 288.15 - 0.0065 * cruise_alt
v_cruise = cruise_mach * math.sqrt(1.4 * 287.05 * T_cruise)

# Aerodynamic estimates
aspect_ratio = 9.50
oswald_e = 0.85
cd0 = 0.0150
ld_max = 0.5 * math.sqrt((math.pi * aspect_ratio * oswald_e) / cd0)
ld_cruise = 0.866 * ld_max
ld_loiter = ld_max

# Engine specific fuel consumption (Carlos Xisto, MMS236 Kick-off Slide 13)
sfc_jeta_cruise = 14.5e-6  # kg/(N*s) baseline high-bypass turbofan
sfc_jeta_loiter = 11.3e-6  # kg/(N*s) low-speed loiter
lhv_ratio = lhv_jeta / lhv_lh2
sfc_lh2_cruise = sfc_jeta_cruise * lhv_ratio
sfc_lh2_loiter = sfc_jeta_loiter * lhv_ratio

# Mission fuel fraction buildup (Breguet equation)
ff_1, ff_2, ff_3, ff_4 = 0.995, 0.995, 0.998, 0.985  # start, taxi, takeoff, climb
ff_5 = math.exp(-(range_m * g * sfc_lh2_cruise) / (v_cruise * ld_cruise))
ff_6, ff_7 = 0.990, 0.995  # descent, landing and taxi-in

# Reserves: 200 nm diversion at FL250 plus 30-minute loiter
ff_div_cruise = math.exp(-(200.0 * 1852.0 * g * sfc_lh2_cruise) / (201.3 * ld_cruise * 0.95))
ff_8 = 0.992 * ff_div_cruise * 0.995
ff_9 = math.exp(-(1800.0 * g * sfc_lh2_loiter) / ld_loiter)

# Total fuel fraction with 3% route contingency
ff_total = (1.0 - (ff_1 * ff_2 * ff_3 * ff_4 * ff_5 * ff_6 * ff_7 * ff_8 * ff_9)) * 1.03

# Iterative weight sizing (Gi = 0.50: tank mass equals fuel mass)
m_airframe = 120000.0  # 120.0 t baseline airframe
mtow = 220000.0        # initial guess in kg
tolerance = 0.01       # 10-gram convergence threshold
iterations = 0

for i in range(1, 101):
    iterations = i
    m_fuel = mtow * ff_total
    m_tank = m_fuel
    mtow_new = payload_mass + crew_mass + m_airframe + m_fuel + m_tank
    if abs(mtow_new - mtow) < tolerance:
        mtow = mtow_new
        break
    mtow = mtow_new

m_oew = m_airframe + m_tank
vol_liquid = m_fuel / lh2_density
vol_cryo_total = vol_liquid * 1.10  # 10% ullage and insulation allowance

if __name__ == "__main__":
    print("AETHER LH2 BWB - Sizing Results")
    print("-" * 50)
    print(f"MTOW                  : {mtow:9.1f} kg  ({mtow/1000:6.2f} t)")
    print(f"Operating Empty (OEW) : {m_oew:9.1f} kg  ({m_oew/1000:6.2f} t)")
    print(f"  - Baseline Airframe : {m_airframe:9.1f} kg  ({m_airframe/1000:6.2f} t)")
    print(f"  - Cryotanks (Gi=0.5): {m_tank:9.1f} kg  ({m_tank/1000:6.2f} t)")
    print(f"Mission Fuel (LH2)    : {m_fuel:9.1f} kg  ({m_fuel/1000:6.2f} t)")
    print(f"Payload (430 Pax)     : {payload_mass:9.1f} kg  ({payload_mass/1000:6.2f} t)")
    print(f"Crew (12)             : {crew_mass:9.1f} kg  ({crew_mass/1000:6.2f} t)")
    print(f"Cryotank Volume       : {vol_cryo_total:9.1f} m3  (liquid: {vol_liquid:.1f} m3)")
    print("-" * 50)
    print(f"Sizing Loop           : Converged in {iterations} iterations from 220.0 t")
    print(f"LH2 Cruise SFC        : {sfc_lh2_cruise * 1e6:.3f} mg/(N*s)")
    print(f"Cruise fuel burn      : {(1.0 - ff_5) * 100:.2f}%")
    print(f"Total fuel fraction   : {ff_total * 100:.2f}%")
