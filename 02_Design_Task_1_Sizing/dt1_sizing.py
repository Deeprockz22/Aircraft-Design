#!/usr/bin/env python3
"""
AETHER 80m Liquid Hydrogen Blended Wing Body Transport Sizing.
Course: Chalmers MMS236 Aircraft Design - Design Task 1 (Group 13)
Aircraft: AETHER (430 Pax, 12,500 km range, Mach 0.85 at FL350)

Calculates mission fuel fractions and derives empty weight fractions from
empirical widebody transport data, composite/BWB structural factors, and
Carlos Xisto's cryogenic tank sizing guidelines.
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
# 3. EMPTY WEIGHT FRACTION DERIVATION (Empirical Widebody Baseline & BWB Physics)
# ==============================================================================
# Step A: Empirical average of modern widebody transports (A350, B787, B777, A330neo)
we_empirical_baseline = 0.4964  # 49.64%

# Step B: Remove conventional kerosene fuel system (-2.0% MTOW)
we_no_tank = we_empirical_baseline - 0.0200  # 47.64%

# Step C: 2050 advanced composite technology factor (Raymer 6th ed., p. 60)
we_composite = we_no_tank * 0.95  # 45.26%

# Step D: Blended Wing Body (BWB) structural benefit (Raymer Ch. 23.2, p. 838 & Carlos Lec 3 Slide 29)
# Span loading cuts wing-root bending moment by ~50%; elimination of tail cone & empennage.
# Boeing BWB-450 studies predict 15% structural airframe weight reduction:
bwb_structural_factor = 0.85
we_airframe_bwb = we_composite * bwb_structural_factor  # 0.3847 (38.47%)

# ==============================================================================
# 4. MASS SIZING SOLUTIONS
# ==============================================================================
# Model 1: BWB Empirical Scaling Model
# Sizing Equation: MTOW = (Payload + Crew) / (1 - E_airframe - 2 * Fuel_Fraction)
# where 2 * Fuel_Fraction accounts for fuel + cryotanks (Gi = 0.50 -> M_tank = M_fuel)
mtow_bwb = (payload_mass + crew_mass) / (1.0 - we_airframe_bwb - 2.0 * ff_total)
m_fuel_bwb = mtow_bwb * ff_total
m_tank_bwb = m_fuel_bwb  # Gi = 0.50 (Carlos Kick-off Slide 10)
m_airframe_bwb = mtow_bwb * we_airframe_bwb
oew_bwb = m_airframe_bwb + m_tank_bwb
empty_frac_bwb = oew_bwb / mtow_bwb
vol_liquid_bwb = m_fuel_bwb / lh2_density
vol_cryo_bwb = vol_liquid_bwb * 1.10  # 10% ullage & vacuum insulation

# Model 2: Conservative Fixed-Airframe Benchmark (120.0 t baseline airframe)
m_airframe_fixed = 120000.0
mtow_fixed = (payload_mass + crew_mass + m_airframe_fixed) / (1.0 - 2.0 * ff_total)
m_fuel_fixed = mtow_fixed * ff_total
m_tank_fixed = m_fuel_fixed
oew_fixed = m_airframe_fixed + m_tank_fixed
empty_frac_fixed = oew_fixed / mtow_fixed
vol_liquid_fixed = m_fuel_fixed / lh2_density
vol_cryo_fixed = vol_liquid_fixed * 1.10

# Default design point variables
mtow = mtow_bwb
m_oew = oew_bwb
m_airframe = m_airframe_bwb
m_tank = m_tank_bwb
m_fuel = m_fuel_bwb
vol_liquid = vol_liquid_bwb
vol_cryo_total = vol_cryo_bwb

if __name__ == "__main__":
    print("=" * 74)
    print("AETHER 80m Liquid Hydrogen BWB - Mass Sizing & Weight Fractions")
    print("Course: Chalmers MMS236 Aircraft Design | Group 13")
    print("Mission: 430 Pax | 12,500 km | Mach 0.85 at FL350 | Gi = 0.50")
    print("=" * 74)
    print(f"LH2 Cruise SFC            : {sfc_lh2_cruise * 1e6:.3f} mg/(N*s) (Jet-A equiv: {sfc_jeta_cruise*1e6:.2f})")
    print(f"Mission Fuel Fraction     : {ff_total * 100:.2f}% (Cruise burn: {(1.0 - ff_5)*100:.2f}%)")
    print(f"Fixed Payload + Crew      : {payload_mass + crew_mass:,.1f} kg ({payload_mass/1000:.2f} t Pax/Cargo + {crew_mass/1000:.2f} t Crew)")
    print("-" * 74)
    print(f"{'Parameter':<28} | {'1. BWB Empirical Model':<20} | {'2. Conservative Baseline':<20}")
    print("-" * 74)
    print(f"{'MTOW':<28} | {mtow_bwb/1000:7.2f} t ({mtow_bwb:9.1f} kg) | {mtow_fixed/1000:7.2f} t ({mtow_fixed:9.1f} kg)")
    print(f"{'OEW (Empty Weight)':<28} | {oew_bwb/1000:7.2f} t ({empty_frac_bwb*100:5.2f}%)     | {oew_fixed/1000:7.2f} t ({empty_frac_fixed*100:5.2f}%)")
    print(f"{'  - Airframe Structure':<28} | {m_airframe_bwb/1000:7.2f} t ({we_airframe_bwb*100:5.2f}%)     | {m_airframe_fixed/1000:7.2f} t ({m_airframe_fixed/mtow_fixed*100:5.2f}%)")
    print(f"{'  - Cryotanks (Gi=0.50)':<28} | {m_tank_bwb/1000:7.2f} t ({ff_total*100:5.2f}%)     | {m_tank_fixed/1000:7.2f} t ({ff_total*100:5.2f}%)")
    print(f"{'Mission Fuel (LH2)':<28} | {m_fuel_bwb/1000:7.2f} t ({ff_total*100:5.2f}%)     | {m_fuel_fixed/1000:7.2f} t ({ff_total*100:5.2f}%)")
    print(f"{'Payload Fraction':<28} | {payload_mass/mtow_bwb*100:5.2f}%               | {payload_mass/mtow_fixed*100:5.2f}%")
    print(f"{'Cryotank Installed Vol':<28} | {vol_cryo_bwb:7.1f} m3 (Liq: {vol_liquid_bwb:5.1f})| {vol_cryo_fixed:7.1f} m3 (Liq: {vol_liquid_fixed:5.1f})")
    print("=" * 74)
