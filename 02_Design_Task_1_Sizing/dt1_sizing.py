#!/usr/bin/env python3
# =============================================================================
# MMS236 Aircraft Design — Design Task 1 (DT1)
# Student: Sai Srinivasa Manideep Jakka (ID: 111923)
# Topic: EXAELIA Long-Range Liquid Hydrogen (LH2) Transport Aircraft Sizing
# =============================================================================

import math
import numpy as np

# =============================================================================
# 1. TOP-LEVEL AIRCRAFT REQUIREMENTS (TLARs) & CONSTANTS
# =============================================================================
# SOURCE: ISO Standard Atmosphere / Lecture 2 Slide 9
g = 9.80665              # Acceleration due to gravity at sea level (m/s^2)

# --- Passenger & Payload Assumptions ---
# SOURCE: MMS236 Kick-off Slide 5 ("Pax 406 (economic) + 24 (Business)")
pax_count = 430          # Total 430 passengers in a 2-class widebody cabin layout

# SOURCE: MMS236 Kick-off Slide 5 ("Typical Passenger Weight 100 kg")
# Includes passenger body mass (approx. 75 kg) + checked & carry-on baggage (25 kg)
pax_mass = 100.0         # kg/passenger
total_pax_mass = pax_count * pax_mass  # 43,000 kg (43.0 tonnes)

# SOURCE: MMS236 Kick-off Slide 5 ("Design Freight 10750 kg")
# Underfloor containerized cargo payload (approx. 20% of total payload capacity)
cargo_mass = 10750.0     # kg (10.75 tonnes)

# Total Design Payload (Revenue-generating load)
payload_mass = total_pax_mass + cargo_mass  # 53,750 kg (53.75 tonnes)

# SOURCE: Raymer (2018) Chapter 3.3 (Crew Allowance)
# 2 Flight deck pilots (at 105 kg each) + 10 Cabin crew attendants (at 105 kg each, 1 per 50 pax + margin)
crew_mass = 12 * 105.0   # 1,260 kg (1.26 tonnes)

# --- Mission Profile Requirements ---
# SOURCE: MMS236 Kick-off Slide 5 ("Range 12500 km")
range_km = 12500.0       # 12,500 km nominal cruise range (6,749 nautical miles)
range_m = range_km * 1000.0

# SOURCE: MMS236 Kick-off Slide 5 ("Cruise speed M0.85")
cruise_mach = 0.85       # Transonic design cruise speed

# SOURCE: Standard civil widebody long-range cruise altitude (Raymer Ch. 3 / Lecture 2)
# FL350 provides optimal balance between high aerodynamic efficiency and low air density
cruise_alt = 10668.0     # 35,000 ft (Flight Level 350) converted to meters

# --- Fuel & Cryotank Properties ---
# SOURCE: MMS236 Kick-off Slide 9 (Fuel Energy Density Comparison Chart)
# Lower Heating Value (LHV) represents usable thermal energy released during combustion
lhv_jeta = 42.8e6        # 42.8 MJ/kg (Standard Jet-A kerosene baseline)
lhv_lh2 = 120.0e6        # 120.0 MJ/kg (Liquid Hydrogen packs 2.80x higher energy per kg than Jet-A!)

# SOURCE: MMS236 Kick-off Slide 5 & 9 ("Liquid hydrogen at 2 bar")
# Saturated liquid density at cryogenic storage temperature of 20.3 K (-253 C) and 2.0 bar pressure
lh2_density = 71.0       # kg/m^3 (approx. 11.3x less dense than kerosene at 800 kg/m^3)

# SOURCE: MMS236 Kick-off Slide 10 (CleanSky 2 / ENABLEH2 / Xisto Baseline)
# Gravimetric Index: Gi = M_fuel / (M_fuel + M_tank) = 0.50
# This accounts for double-walled vacuum insulation (MLI), inner aluminum liner, and structural shell.
# Gi = 0.50 directly establishes: M_tank = M_fuel (Every 1 kg of LH2 requires 1 kg of cryotank structure).
gi_tank = 0.50


# =============================================================================
# 2. STANDARD ATMOSPHERE AT FL350 & AERODYNAMIC EFFICIENCY (L/D)
# =============================================================================
# SOURCE: International Standard Atmosphere (ISA) Model (ISO 2533 / Lecture 2)
T_sl = 288.15            # Sea level standard temperature (K)
p_sl = 101325.0          # Sea level standard pressure (Pa)
rho_sl = 1.225           # Sea level standard density (kg/m^3)
gamma = 1.4              # Ratio of specific heats for dry air
R = 287.05               # Specific gas constant for dry air (J/(kg*K))

# Troposphere temperature lapse rate is -6.5 K per 1,000 m (valid up to 11,000 m)
T_cruise = T_sl - 0.0065 * cruise_alt  # 218.81 K (-54.34 C)

# Hydrostatic pressure equation for constant lapse rate atmosphere
p_cruise = p_sl * (T_cruise / T_sl) ** (g / (0.0065 * R))  # 23,842 Pa (23.84 kPa)

# Ideal gas law: rho = p / (R * T)
rho_cruise = p_cruise / (R * T_cruise)  # 0.3796 kg/m^3

# Speed of sound: a = sqrt(gamma * R * T)
speed_of_sound = math.sqrt(gamma * R * T_cruise)  # 296.5 m/s (1,067 km/h)

# True Airspeed: V = Mach * a
v_cruise = cruise_mach * speed_of_sound           # 252.0 m/s (907.4 km/h)

# Dynamic pressure at cruise: q = 0.5 * rho * V^2
q_cruise = 0.5 * rho_cruise * (v_cruise ** 2)     # 12,058 Pa (12.06 kPa)

# --- Aerodynamic Efficiency Assumptions (L/D) ---
# SOURCE: MMS236 Kick-off Slide 14 & 15 (Wetted Aspect Ratio & Modern Transonic Wing Design)
# Aspect Ratio (AR = b^2 / S_ref) chosen as 9.50 (comparable to A350/B787 advanced composite wings)
# Fits within the ICAO Code F wingspan limit (Span <= 80 m, Kick-off Slide 5)
aspect_ratio = 9.50

# SOURCE: Lecture 2 Slide 9 (Oswald span efficiency factor at high transonic Mach 0.85)
oswald_e = 0.85

# SOURCE: Raymer (2018) Ch. 12 / ENABLEH2 Transonic Aerodynamic Model
# Clean zero-lift parasitic drag coefficient for smooth composite surface
cd0 = 0.0150

# SOURCE: Parabolic Drag Polar Maximum Lift-to-Drag Ratio formula: (L/D)_max = 0.5 * sqrt(pi * AR * e / CD0)
ld_max = 0.5 * math.sqrt((math.pi * aspect_ratio * oswald_e) / cd0)  # ~20.50

# SOURCE: MMS236 Kick-off Slide 15 ("For maximum range: Jet engine: 0.866 * L/D_max")
# Flying at (L/D)_cruise = 0.866 * (L/D)_max maximizes the Breguet range factor (V * L/D)
ld_cruise = 0.866 * ld_max                                           # ~17.75

# SOURCE: MMS236 Kick-off Slide 15 ("For maximum loiter: Jet engine: L/D_max")
# Loiter holding at low speed occurs at the bottom of the thrust-required curve where L/D is maximized
ld_loiter = ld_max                                                   # ~20.50


# =============================================================================
# 3. ENGINE SPECIFIC FUEL CONSUMPTION (SFC)
# =============================================================================
# SOURCE: MMS236 Kick-off Slide 13 (Engine SFC Historical Trends Chart)
# Modern ultra-high bypass geared turbofans for year 2050 EIS:
# Cruise baseline on Jet-A: 13.5 mg/(N*s) [approx. 0.476 lb/(lbf*hr)]
# Low-speed loiter baseline on Jet-A: 11.0 mg/(N*s) [approx. 0.388 lb/(lbf*hr)]
sfc_jeta_cruise = 13.5e-6   # kg/(N*s)
sfc_jeta_loiter = 11.0e-6   # kg/(N*s)

# SOURCE: Equal Thermal Energy Equivalence Principle (Kick-off Slide 9 & 13)
# SFC_LH2 = SFC_JetA * (LHV_JetA / LHV_LH2) = SFC_JetA * (42.8 / 120.0) = SFC_JetA * 0.3567
lhv_ratio = lhv_jeta / lhv_lh2  # 0.3567

# Converted Hydrogen Specific Fuel Consumption:
sfc_lh2_cruise = sfc_jeta_cruise * lhv_ratio  # 4.815 mg/(N*s) [0.170 lb/(lbf*hr)]
sfc_lh2_loiter = sfc_jeta_loiter * lhv_ratio  # 3.923 mg/(N*s) [0.138 lb/(lbf*hr)]


# =============================================================================
# 4. MISSION FUEL FRACTION BREAKDOWN (Breguet Sizing)
# =============================================================================
# SOURCE: Historical statistical segment fractions from Raymer (2018) Table 3.2 / Lecture 2
# Each fraction represents W_end / W_start for that specific flight phase

# Phase 1: Engine start and warm-up
ff_1 = 0.995   # Burns 0.5% of aircraft weight

# Phase 2: Taxi-out to runway
ff_2 = 0.995   # Burns 0.5% of aircraft weight

# Phase 3: Take-off acceleration and liftoff
ff_3 = 0.998   # Burns 0.2% of aircraft weight

# Phase 4: Climb from sea level to FL350
ff_4 = 0.985   # Burns 1.5% of aircraft weight

# Phase 5: Main Design Cruise (12,500 km at Mach 0.85, FL350)
# SOURCE: Breguet Range Equation for Jet Aircraft:
# W5 / W4 = exp( - (Range * g * SFC_cruise) / (V_cruise * (L/D)_cruise) )
breguet_exponent = (range_m * g * sfc_lh2_cruise) / (v_cruise * ld_cruise)
ff_5 = math.exp(-breguet_exponent)  # 0.8768 (Burns 12.32% of aircraft weight during main cruise)

# Phase 6: Descent from cruise altitude to approach fix
ff_6 = 0.990   # Burns 1.0% of aircraft weight

# Phase 7: Approach, landing, and taxi-in to airport gate
ff_7 = 0.995   # Burns 0.5% of aircraft weight

# --- Statutory Reserves & Contingencies ---
# Phase 8: Diversion to Alternate Airport (200 nm = 370.4 km at FL250, Mach 0.65)
# SOURCE: CS-25 / FAR-25 Airline Reserve Regulations (Lecture 2 Slide 17)
range_div_m = 200.0 * 1852.0  # 370,400 meters
v_div = 201.3                 # True airspeed at FL250 (m/s)
ld_div = ld_cruise * 0.95     # Slightly lower L/D off-design
ff_div_climb = 0.992
ff_div_cruise = math.exp(-(range_div_m * g * sfc_lh2_cruise) / (v_div * ld_div))
ff_div_descent = 0.995
ff_8 = ff_div_climb * ff_div_cruise * ff_div_descent  # 0.9820 (Burns 1.80% for diversion)

# Phase 9: Holding / Loiter (30 min = 1,800 s hold at 1,500 ft altitude)
# SOURCE: CS-25.1001 Statutory Loiter Reserve (Lecture 2 Slide 17)
# W9 / W8 = exp( - (Time * g * SFC_loiter) / (L/D)_loiter )
time_loiter_s = 30.0 * 60.0   # 1,800 seconds
ff_9 = math.exp(-(time_loiter_s * g * sfc_lh2_loiter) / ld_loiter)  # 0.9966 (Burns 0.34% during hold)

# Cumulative product of all mission phases: W_final / W_takeoff
ff_mission_product = ff_1 * ff_2 * ff_3 * ff_4 * ff_5 * ff_6 * ff_7 * ff_8 * ff_9  # 0.8309

# SOURCE: ICAO International Reserve Standards (3% route contingency fuel)
fuel_fraction_nominal = 1.0 - ff_mission_product
fuel_fraction_total = fuel_fraction_nominal * 1.03  # 18.27% of MTOW


# =============================================================================
# =============================================================================
# 5. MTOW & OEW SIZING (With Fixed 120-Tonne Airframe Weight & Cryotanks)
# =============================================================================
# User Design Requirement: Baseline Airframe Mass = 120.0 tonnes (120,000 kg)
# Covers: BWB composite airframe, engines, nacelles, landing gear, cabin interior, avionics.
#
# Sizing Equation:
# MTOW = W_payload + W_crew + W_airframe + W_tank + W_fuel
# Since Gi = 0.50: W_tank = W_fuel = Fuel_Fraction * MTOW
# MTOW = (W_payload + W_crew + W_airframe) / (1 - 2 * Fuel_Fraction)

m_airframe = 120000.0  # 120,000 kg (120.0 tonnes)

# Sizing denominator with 2x fuel fraction (Fuel + Dry Cryotanks)
denominator = 1.0 - (2.0 * fuel_fraction_total)
mtow = (payload_mass + crew_mass + m_airframe) / denominator

# Breakdown of mass components
m_fuel = mtow * fuel_fraction_total       # Usable Liquid Hydrogen (kg)
m_tank = m_fuel                           # Cryotank structural mass (kg, Gi = 0.50)
m_oew = m_airframe + m_tank               # Total Operating Empty Weight (kg)

# Cryotank storage volume sizing (Liquid LH2 volume + 10% ullage & multilayer insulation)
vol_lh2_liquid = m_fuel / lh2_density     # Liquid volume in m^3
vol_cryo_total = vol_lh2_liquid * 1.10    # 10% allowance for boil-off ullage space & MLI vacuum walls


# =============================================================================
# 6. CONSOLE PRINTOUT (Verification of Calculated Parameters)
# =============================================================================
if __name__ == "__main__":
    print("=" * 72)
    print("  EXAELIA HYDROGEN TRANSPORT — SIZING RESULTS (120t Airframe)")
    print("=" * 72)
    print(f"  Maximum Take-Off Weight (MTOW) : {mtow:10.1f} kg ({mtow/1000:6.2f} tonnes)")
    print(f"  Operating Empty Weight (OEW)   : {m_oew:10.1f} kg ({m_oew/1000:6.2f} tonnes)")
    print(f"    - Baseline Airframe & Systems: {m_airframe:10.1f} kg ({m_airframe/1000:6.2f} tonnes)")
    print(f"    - Cryogenic LH2 Tanks (50%)  : {m_tank:10.1f} kg ({m_tank/1000:6.2f} tonnes)")
    print(f"  Usable Liquid Hydrogen Fuel    : {m_fuel:10.1f} kg ({m_fuel/1000:6.2f} tonnes)")
    print(f"  Design Payload (430 Pax+Cargo) : {payload_mass:10.1f} kg ({payload_mass/1000:6.2f} tonnes)")
    print(f"  Flight & Cabin Crew (12 Crew)  : {crew_mass:10.1f} kg ({crew_mass/1000:6.2f} tonnes)")
    print(f"  Total Cryotank Storage Volume  : {vol_cryo_total:10.1f} m3 (Liquid: {vol_lh2_liquid:.1f} m3)")
    print("-" * 72)
    print("  MISSION FUEL FRACTIONS & STRUCTURAL RATIOS:")
    print(f"    - Cruise Segment Fraction (ff_5) : {ff_5:.4f} (Breguet: 12,500 km)")
    print(f"    - Total Usable Fuel Fraction     : {fuel_fraction_total*100:.2f}% of MTOW")
    print(f"    - Airframe Empty Fraction (We/W0): {(m_airframe/mtow)*100:.2f}% of MTOW")
    print(f"    - Total OEW Fraction (OEW/MTOW)  : {(m_oew/mtow)*100:.2f}% of MTOW")
    print("=" * 72)
