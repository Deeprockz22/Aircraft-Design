#!/usr/bin/env python3
"""
AETHER 80m Liquid Hydrogen Blended Wing Body Transport Sizing.
Course: Chalmers MMS236 Aircraft Design - Design Task 1 (Group 13)
Aircraft: AETHER (430 Pax, 12,500 km range, Mach 0.85 at FL350)

Locked Baseline Airframe: 120.0 tonnes (120,000 kg)
Backed by empirical widebody peer data, Raymer's transport correlations,
and Carlos Xisto's Clean Sky 2 cryogenic tank sizing guidelines (Gi = 0.50).
"""

import math

# ==============================================================================
# 1. MISSION REQUIREMENTS (Carlos Xisto Kick-off Slide 5 & 7)
# ==============================================================================
g = 9.80665
pax_count = 430
pax_mass = 100.0          # kg per passenger including baggage (Slide 5)
cargo_mass = 10750.0      # kg design freight (Slide 5)
payload_mass = (pax_count * pax_mass) + cargo_mass  # 53,750 kg
crew_mass = 12 * 105.0    # 12 crew members at 105 kg (1,260 kg)

range_m = 12500.0 * 1000.0  # 12,500 km design range (Slide 5)
cruise_mach = 0.85          # Cruise Mach (Slide 5)
cruise_alt = 10668.0        # FL350 (10,668 m) (Slide 7)

# Fuel properties
lhv_jeta = 42.8e6         # J/kg
lhv_lh2 = 120.0e6         # J/kg
lh2_density = 71.0        # kg/m^3 (liquid at 20.3 K, 2 bar, Slide 5 & 9)

# Atmosphere at FL350
T_cruise = 288.15 - 0.0065 * cruise_alt  # 218.81 K
v_cruise = cruise_mach * math.sqrt(1.4 * 287.05 * T_cruise)  # 251.34 m/s

# Aerodynamics (Aspect Ratio 9.5, Oswald e = 0.85, Cd0 = 0.0150)
aspect_ratio = 9.50
oswald_e = 0.85
cd0 = 0.0150
ld_max = 0.5 * math.sqrt((math.pi * aspect_ratio * oswald_e) / cd0)  # 21.05
ld_cruise = 0.866 * ld_max  # 18.23 (Carlos Kick-off Slide 15)
ld_loiter = ld_max          # 21.05

# Engine SFC (2050 Asymptotic Extrapolation: Jet-A 13.80 mg/(N*s) baseline)
sfc_jeta_cruise = 13.80e-6  # kg/(N*s)
sfc_jeta_loiter = 10.75e-6  # kg/(N*s) scaled for low-speed loiter
lhv_ratio = lhv_jeta / lhv_lh2
sfc_lh2_cruise = sfc_jeta_cruise * lhv_ratio  # 4.922 mg/(N*s)
sfc_lh2_loiter = sfc_jeta_loiter * lhv_ratio  # 3.832 mg/(N*s)

# ==============================================================================
# 2. MISSION FUEL FRACTION BUILDUP (Breguet Range Equation)
# ==============================================================================
ff_1, ff_2, ff_3, ff_4 = 0.995, 0.995, 0.998, 0.985  # engine start, taxi, takeoff, climb
ff_5 = math.exp(-(range_m * g * sfc_lh2_cruise) / (v_cruise * ld_cruise))  # main cruise (12,500 km)
ff_6, ff_7 = 0.990, 0.995  # descent, landing & taxi-in

# Reserves (Carlos Kick-off Slide 7: 200 nm diversion at FL250 + 30 min loiter)
ff_div_cruise = math.exp(-(200.0 * 1852.0 * g * sfc_lh2_cruise) / (201.3 * ld_cruise * 0.95))
ff_8 = 0.992 * ff_div_cruise * 0.995  # diversion climb, cruise, descent
ff_9 = math.exp(-(1800.0 * g * sfc_lh2_loiter) / ld_loiter)  # 30-min loiter

# Total fuel fraction with 3% route contingency
ff_total = (1.0 - (ff_1 * ff_2 * ff_3 * ff_4 * ff_5 * ff_6 * ff_7 * ff_8 * ff_9)) * 1.03

# ==============================================================================
# 3. BASELINE AIRFRAME MASS & MASS SIZING (Locked at 120.0 tonnes)
# ==============================================================================
# Locked baseline airframe mass (structure, cabin furnishings, systems, engines)
# Supported by:
#  1. Raymer metric transport formula on 278 t: (0.4566 - 0.02) * 278 t = 121.4 t
#  2. 406-passenger widebody course benchmark: 117.5 t * (430/406) = 124.5 t
#  3. Modern composite widebody fleet (A350-1000, B787-10) scaled to 2050
m_airframe = 120000.0  # 120.0 t locked baseline

# Sizing loop / closed-form solution:
# MTOW = (Payload + Crew + M_airframe) / (1 - 2 * Fuel_Fraction)
# where 2 * Fuel_Fraction accounts for fuel + cryotanks (Gi = 0.50 -> M_tank = M_fuel)
mtow = (payload_mass + crew_mass + m_airframe) / (1.0 - 2.0 * ff_total)
m_fuel = mtow * ff_total
m_tank = m_fuel  # Gi = 0.50 (Carlos Kick-off Slide 10)
m_oew = m_airframe + m_tank

# Fractions & volumes
empty_weight_fraction = m_oew / mtow
fuel_fraction = m_fuel / mtow
airframe_fraction = m_airframe / mtow
payload_fraction = payload_mass / mtow
crew_fraction = crew_mass / mtow

vol_liquid = m_fuel / lh2_density
vol_cryo_total = vol_liquid * 1.10  # 10% ullage & vacuum insulation

if __name__ == "__main__":
    print("=" * 72)
    print("AETHER 80m Liquid Hydrogen BWB - Mass Sizing & Weight Breakdown")
    print("Course: Chalmers MMS236 Aircraft Design | Group 13")
    print("Mission: 430 Pax | 12,500 km | Mach 0.85 at FL350 | Gi = 0.50")
    print("=" * 72)
    print(f"LH2 Cruise SFC            : {sfc_lh2_cruise * 1e6:.3f} mg/(N*s)  (Jet-A baseline: {sfc_jeta_cruise*1e6:.2f})")
    print(f"Mission Fuel Fraction     : {ff_total * 100:.2f}%  (Cruise fuel burn: {(1.0 - ff_5)*100:.2f}%)")
    print(f"Fixed Payload + Crew      : {payload_mass + crew_mass:,.1f} kg  (Payload: {payload_mass/1000:.2f} t, Crew: {crew_mass/1000:.2f} t)")
    print("-" * 72)
    print(f"{'Component':<32} | {'Mass (kg)':<14} | {'Mass (t)':<10} | {'Fraction of MTOW':<16}")
    print("-" * 72)
    print(f"{'Baseline Airframe Structure':<32} | {m_airframe:12.1f} kg | {m_airframe/1000:7.2f} t  | {airframe_fraction*100:6.2f}%")
    print(f"{'Cryotanks (Gi = 0.50)':<32} | {m_tank:12.1f} kg | {m_tank/1000:7.2f} t  | {fuel_fraction*100:6.2f}%")
    print(f"{'Operating Empty Weight (OEW)':<32} | {m_oew:12.1f} kg | {m_oew/1000:7.2f} t  | {empty_weight_fraction*100:6.2f}%")
    print(f"{'Mission Fuel (Liquid H2)':<32} | {m_fuel:12.1f} kg | {m_fuel/1000:7.2f} t  | {fuel_fraction*100:6.2f}%")
    print(f"{'Design Payload (430 Pax + Cargo)':<32} | {payload_mass:12.1f} kg | {payload_mass/1000:7.2f} t  | {payload_fraction*100:6.2f}%")
    print(f"{'Flight & Cabin Crew (12)':<32} | {crew_mass:12.1f} kg | {crew_mass/1000:7.2f} t  | {crew_fraction*100:6.2f}%")
    print("-" * 72)
    print(f"{'Maximum Takeoff Weight (MTOW)':<32} | {mtow:12.1f} kg | {mtow/1000:7.2f} t  | 100.00%")
    print("=" * 72)
    print(f"Liquid Hydrogen Volume    : {vol_liquid:.1f} m3")
    print(f"Total Cryotank Volume     : {vol_cryo_total:.1f} m3  (includes 10% ullage & insulation)")
    print("=" * 72)
