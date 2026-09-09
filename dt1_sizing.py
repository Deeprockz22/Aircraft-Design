#!/usr/bin/env python3
# =============================================================================
# MMS236 Aircraft Design - Design Task 1 (DT1)
# Student: Sai Srinivasa Manideep Jakka
# Topic: EXAELIA Liquid Hydrogen (LH2) Transport Aircraft Sizing
# =============================================================================

import math
import numpy as np

# -----------------------------------------------------------------------------
# 1. Mission Requirements & Constants (Kick-off Slide 5)
# -----------------------------------------------------------------------------
g = 9.80665              # acceleration due to gravity (m/s^2)

# Payload & Passenger Setup
pax_count = 430          # 406 Economy + 24 Business
pax_mass = 100.0         # kg per passenger (including baggage)
total_pax_mass = pax_count * pax_mass  # 43,000 kg
cargo_mass = 10750.0     # design freight in kg
payload_mass = total_pax_mass + cargo_mass  # 53,750 kg
crew_mass = 12 * 105.0   # 12 flight & cabin crew = 1,260 kg

# Mission Targets
range_km = 12500.0       # 12,500 km main range
range_m = range_km * 1000.0
cruise_mach = 0.85
cruise_alt = 10668.0     # FL350 in meters

# Fuel Properties (Jet-A vs Liquid Hydrogen, Slides 9 & 10)
lhv_jeta = 42.8e6        # J/kg (Kerosene heating value)
lhv_lh2 = 120.0e6        # J/kg (Hydrogen heating value)
lh2_density = 71.0       # kg/m^3 (liquid density at 20 K, 2 bar)
gi_tank = 0.50           # Gi = 50% means Tank Mass = Fuel Mass

# -----------------------------------------------------------------------------
# 2. Atmosphere at FL350 (10,668 m, ISA) & Aerodynamic Efficiency (L/D)
# -----------------------------------------------------------------------------
T_sl = 288.15            # Sea level temperature in K
p_sl = 101325.0          # Sea level pressure in Pa
rho_sl = 1.225           # Sea level density in kg/m^3
gamma = 1.4
R = 287.05

# Temperature drops 6.5 K per 1000 m in troposphere
T_cruise = T_sl - 0.0065 * cruise_alt  # 218.81 K (-54.34 C)
p_cruise = p_sl * (T_cruise / T_sl) ** (g / (0.0065 * R)) # 23,842 Pa
rho_cruise = p_cruise / (R * T_cruise) # 0.3796 kg/m^3

# Cruise Speeds & Dynamic Pressure
speed_of_sound = math.sqrt(gamma * R * T_cruise)  # 296.5 m/s
v_cruise = cruise_mach * speed_of_sound           # 252.0 m/s (~907 km/h)
q_cruise = 0.5 * rho_cruise * (v_cruise ** 2)     # Dynamic pressure = 12,058 Pa

# Aerodynamic Efficiency (Kick-off Slides 14 & 15)
aspect_ratio = 9.50      # AR = b^2 / S_ref
oswald_e = 0.85          # span efficiency factor
cd0 = 0.0150             # zero-lift parasitic drag

ld_max = 0.5 * math.sqrt((math.pi * aspect_ratio * oswald_e) / cd0)  # ~20.50
ld_cruise = 0.866 * ld_max                                           # ~17.75 (maximum jet range)
ld_loiter = ld_max                                                   # ~20.50 (maximum loiter endurance)

# -----------------------------------------------------------------------------
# 3. Engine Specific Fuel Consumption (SFC, Slide 13)
# -----------------------------------------------------------------------------
sfc_jeta_cruise = 13.5e-6   # 13.5 mg/(N*s)
sfc_jeta_loiter = 11.0e-6   # 11.0 mg/(N*s)

# Standard conversion to hydrogen by Lower Heating Value ratio
lhv_ratio = lhv_jeta / lhv_lh2  # 42.8 / 120.0 = 0.3567

sfc_lh2_cruise = sfc_jeta_cruise * lhv_ratio  # 4.815 mg/(N*s)
sfc_lh2_loiter = sfc_jeta_loiter * lhv_ratio  # 3.923 mg/(N*s)

# -----------------------------------------------------------------------------
# 4. Mission Fuel Fraction Breakdown (Breguet Range Equation)
# -----------------------------------------------------------------------------
# Segment fractions (W_i / W_{i-1})
ff_1 = 0.995   # 1. Engine start & warm-up
ff_2 = 0.995   # 2. Taxi-out
ff_3 = 0.998   # 3. Take-off run
ff_4 = 0.985   # 4. Climb to FL350

# 5. Main Cruise (12,500 km) using Breguet Range Equation:
# W_end / W_start = exp( - (Range * g * SFC) / (V * L/D) )
breguet_exponent = (range_m * g * sfc_lh2_cruise) / (v_cruise * ld_cruise)
ff_5 = math.exp(-breguet_exponent)

# 6 & 7. Descent & Landing
ff_6 = 0.990   # 6. Descent to destination
ff_7 = 0.995   # 7. Approach, landing & taxi-in

# 8. Diversion Reserve (200 nm = 370.4 km at FL250, Mach 0.65)
range_div_m = 200.0 * 1852.0
v_div = 201.3  # m/s
ld_div = ld_cruise * 0.95
ff_div_climb = 0.992
ff_div_cruise = math.exp(-(range_div_m * g * sfc_lh2_cruise) / (v_div * ld_div))
ff_div_descent = 0.995
ff_8 = ff_div_climb * ff_div_cruise * ff_div_descent

# 9. Loiter Hold Reserve (30 min = 1,800 s at 1,500 ft, max L/D)
time_loiter_s = 30.0 * 60.0
ff_9 = math.exp(-(time_loiter_s * g * sfc_lh2_loiter) / ld_loiter)

# Cumulative product of all mission phases (W_landing / W_takeoff)
ff_mission_product = ff_1 * ff_2 * ff_3 * ff_4 * ff_5 * ff_6 * ff_7 * ff_8 * ff_9

# Total usable fuel fraction with 3% contingency reserve allowance
fuel_fraction_nominal = 1.0 - ff_mission_product
fuel_fraction_total = fuel_fraction_nominal * 1.03  # ~18.27% of MTOW

# -----------------------------------------------------------------------------
# 5. Iterative MTOW & OEW Sizing Loop (with Cryotanks Gi = 0.50)
# -----------------------------------------------------------------------------
mtow_guess = 220000.0   # initial guess in kg
tolerance = 0.01        # convergence tolerance in kg
max_iter = 100

for i in range(max_iter):
    # Year 2050 advanced composite transport empty weight correlation:
    # Baseline airframe fraction without conventional kerosene fuel system
    we_w0_no_tank = 0.88 * (mtow_guess ** -0.06) * 0.90
    
    # Sizing formula:
    # MTOW = (Payload + Crew) / (1 - 2*Fuel_Fraction - Airframe_Fraction)
    # The factor of 2 accounts for: 1.0*Fuel + 1.0*Tank (because Gi = 0.50)
    denominator = 1.0 - (2.0 * fuel_fraction_total) - we_w0_no_tank
    
    mtow_calculated = (payload_mass + crew_mass) / denominator
    
    if abs(mtow_calculated - mtow_guess) < tolerance:
        mtow = mtow_calculated
        break
    mtow_guess = 0.5 * (mtow_guess + mtow_calculated)

# Breakdown of mass components
m_fuel = mtow * fuel_fraction_total       # Usable Liquid Hydrogen (kg)
m_tank = m_fuel                           # Cryotank structure mass (kg)
m_airframe = mtow * we_w0_no_tank         # Structure, engines, systems (kg)
m_oew = m_airframe + m_tank               # Operating Empty Weight (kg)

# Cryotank storage volume sizing
vol_lh2_liquid = m_fuel / lh2_density     # Liquid volume in m^3
vol_cryo_total = vol_lh2_liquid * 1.10    # 10% allowance for ullage & insulation

# -----------------------------------------------------------------------------
# 6. Print Sizing Results to Console
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 72)
    print("  EXAELIA HYDROGEN TRANSPORT — SIZING RESULTS (DT1)")
    print("=" * 72)
    print(f"  Maximum Take-Off Weight (MTOW) : {mtow:10.1f} kg ({mtow/1000:6.2f} tonnes)")
    print(f"  Operating Empty Weight (OEW)   : {m_oew:10.1f} kg ({m_oew/1000:6.2f} tonnes)")
    print(f"    - Baseline Airframe & Systems: {m_airframe:10.1f} kg ({m_airframe/1000:6.2f} tonnes)")
    print(f"    - Cryogenic LH2 Tanks (50%)  : {m_tank:10.1f} kg ({m_tank/1000:6.2f} tonnes)")
    print(f"  Usable Liquid Hydrogen Fuel    : {m_fuel:10.1f} kg ({m_fuel/1000:6.2f} tonnes)")
    print(f"  Design Payload (430 Pax+Cargo) : {payload_mass:10.1f} kg ({payload_mass/1000:6.2f} tonnes)")
    print(f"  Total Cryotank Storage Volume  : {vol_cryo_total:10.1f} m3 (Liquid: {vol_lh2_liquid:.1f} m3)")
    print("-" * 72)
    print("  MISSION FUEL FRACTIONS:")
    print(f"    - Cruise Segment Fraction (ff_5) : {ff_5:.4f} (Breguet: 12,500 km)")
    print(f"    - Total Fuel Fraction (M_f/MTOW) : {fuel_fraction_total*100:.2f}%")
    print(f"    - Airframe Empty Fraction (We/W0): {we_w0_no_tank*100:.2f}%")
    print(f"    - Total OEW Fraction (OEW/MTOW)  : {(m_oew/mtow)*100:.2f}%")
    print("=" * 72)
