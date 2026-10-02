#!/usr/bin/env python3
"""
AETHER 80m Liquid Hydrogen Blended Wing Body Transport Sizing.
Course: Chalmers MMS236 Aircraft Design - Design Task 1 (Group 13)
Mission: 430 Pax | 12,500 km | Mach 0.85 at FL350

- Utskrift av värden från första delen (bränslefraktioner, MTOW-konvergens, viktfördelning, volymer) för Iteration 2.
- Jämförelse mellan Baseline, Iteration 1 och Iteration 2.
- Jämförelse mellan Iteration 1 och Iteration 2 i Constraint Matching Diagram (två separata popup-fonster).
Ruta 1 (Vänster): Iteration 1
Ruta 2 (Höger):   Iteration 2
"""

import math
import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# 1. MISSION REQUIREMENTS & SPECIFICATIONS
# ==============================================================================
g = 9.81
pax_count = 430
pax_mass = 100.0          # kg per passenger + baggage
cargo_mass = 10750.0      # kg freight
payload_mass = (pax_count * pax_mass) + cargo_mass  # 53,750 kg
crew_mass = 12 * 105.0    # 12 crew members (1,260 kg)

range_m = 12500.0 * 1000.0  # 12,500 km
cruise_mach = 0.85
cruise_alt = 10668.0        # FL350 (10,668 m)

# Fuel properties (Liquid H2)
lhv_jeta = 42.8e6         # J/kg
lhv_lh2 = 120.0e6         # J/kg
lh2_density = 71.0        # kg/m^3

# Cruise atmospheric conditions at FL350
T_cruise = 288.15 - 0.0065 * cruise_alt  # 218.81 K
v_cruise = cruise_mach * math.sqrt(1.4 * 287.05 * T_cruise)  # 251.34 m/s
rho_cruise = 0.3796       # kg/m^3
q_cruise = 0.5 * rho_cruise * (v_cruise ** 2)
rho_sl = 1.225            # kg/m^3
g0 = 9.8

# Specific fuel consumption (LH2)
sfc_jeta_cruise = 13.80e-6
sfc_jeta_loiter = 10.75e-6
sfc_lh2_cruise = sfc_jeta_cruise * (lhv_jeta / lhv_lh2)  # 4.922 mg/(N*s)
sfc_lh2_loiter = sfc_jeta_loiter * (lhv_jeta / lhv_lh2)  # 3.832 mg/(N*s)

# Fixed mission segment retained weight fractions
ff_1, ff_2, ff_3, ff_4 = 0.995, 0.995, 0.998, 0.985  # start, taxi, takeoff, climb
beta_climb = ff_1 * ff_2 * ff_3          # ~0.988
beta_cruise = ff_1 * ff_2 * ff_3 * ff_4  # ~0.973
m_airframe = 120000.0                    # 120 tonnes bare airframe
w0_guess = 250000.0                      # Initial guess [kg]
tol = 0.1                               # Konvergenstolerans [kg] (< 100 gram)

# ==============================================================================
# 2. FUNKTION FÖR MASS SIZING & NUMERISK ITERATION (BREGUET + RAYMER LOOP)
# ==============================================================================
def compute_mass_sizing(cd0, ar=9.50, oswald_e=0.85, w0_start=w0_guess, tolerance=tol):
    ld_max = 0.5 * math.sqrt((math.pi * ar * oswald_e) / cd0)
    ld_cruise = 0.866 * ld_max
    ld_loiter = ld_max

    ff_5 = math.exp(-(range_m * g * sfc_lh2_cruise) / (v_cruise * ld_cruise))
    ff_6, ff_7 = 0.990, 0.995

    # Reserves (200 nm diversion @ FL250 + 30 min loiter + 3% contingency)
    ff_div_cruise = math.exp(-(200.0 * 1852.0 * g * sfc_lh2_cruise) / (201.3 * ld_cruise * 0.95))
    ff_8 = 0.992 * ff_div_cruise * 0.995
    ff_9 = math.exp(-(1800.0 * g * sfc_lh2_loiter) / ld_loiter)
    ff_total = (1.0 - (ff_1 * ff_2 * ff_3 * ff_4 * ff_5 * ff_6 * ff_7 * ff_8 * ff_9)) * 1.03

    # Analytisk lösning:
    mtow_analytical = (payload_mass + crew_mass + m_airframe) / (1.0 - 2.0 * ff_total)

    # Numerisk iteration för att visa konvergens (Raymer / Carlos Xisto metod):
    w0 = w0_start
    history = []
    for i in range(1, 100):
        m_fuel_iter = w0 * ff_total
        m_tank_iter = m_fuel_iter        # Gi = 0.50
        m_oew_iter = m_airframe + m_tank_iter
        w0_next = payload_mass + crew_mass + m_oew_iter + m_fuel_iter
        diff = abs(w0_next - w0)
        history.append((i, w0_next, diff))
        w0 = w0_next
        if diff < tolerance:
            break

    mtow_val = w0
    m_fuel_val = mtow_val * ff_total
    m_tank_val = m_fuel_val
    m_oew_val = m_airframe + m_tank_val
    vol_liquid = m_fuel_val / lh2_density
    vol_cryo_total = vol_liquid * 1.10  # 10% ullage & vacuum insulation
    area_cabin = (406 * (0.76 * 0.46) + 24 * (0.58 * 1.52)) * 1.3  # 212.02 m^2
    ws_cabin = mtow_val / area_cabin

    return {
        'cd0': cd0,
        'ar': ar,
        'oswald_e': oswald_e,
        'ld_max': ld_max,
        'ld_cruise': ld_cruise,
        'ld_loiter': ld_loiter,
        'ff_5': ff_5,
        'ff_total': ff_total,
        'mtow': mtow_val,
        'mtow_analytical': mtow_analytical,
        'm_fuel': m_fuel_val,
        'm_tank': m_tank_val,
        'm_oew': m_oew_val,
        'vol_liquid': vol_liquid,
        'vol_cryo_total': vol_cryo_total,
        'area_cabin': area_cabin,
        'ws_cabin': ws_cabin,
        'num_iterations': len(history),
        'history': history,
        'w0_guess': w0_start,
        'tol': tolerance
    }

# ==============================================================================
# 3. PARAMETRAR: ITERATION 1 vs ITERATION 2 (ÄNDRA HÄR)
# ==============================================================================

# --- BASELINE (Ursprunglig uppskattning) ---
Cd0_base       = 0.0150
AR_base        = 5.10
oswald_e_base  = 0.9

# --- ITERATION 1 PARAMETRAR (Ruta 1 - Vänster) ---
Cd0_1          = 0.0090    # Profilmotstånd Cd0 för Iteration 1
AR_1           = 5.1      # Aspect ratio (AR)
oswald_e_1     = 0.85      # Oswald span efficiency factor (e)
Cl_max_1       = 1.3       # Max lyftkoefficient CL,max
Vstall_1       = 60.0      # Stallhastighet [m/s]
s_fl_1         = 2300.0    # Landningsbanelängd [m]
TOP_1          = 235.0     # Startparameter (TOP)
alpha_cruise_1 = 0.22      # Raymer dragkraftsnedgång (cruise lapse)
alpha_climb_1  = 0.83      # Raymer dragkraftsnedgång (climb lapse)
v_climb_1      = 80.0      # Stighastighet framåt [m/s]
v_vert_1       = 14.22    # Stighastighet vertikal [m/s]

# --- ITERATION 2 PARAMETRAR (Ruta 2 - Höger) ---
Cd0_2          = 0.01267    # Profilmotstånd Cd0 för Iteration 2
AR_2           = 5.1      # Aspect ratio (AR)
oswald_e_2     = 0.85      # Oswald span efficiency factor (e)
Cl_max_2       = 1.3      # Max lyftkoefficient CL,max
Vstall_2       = 60.0      # Stallhastighet [m/s]
s_fl_2         = 2300.0    # Landningsbanelängd [m]
TOP_2          = 235.0     # Startparameter (TOP)
alpha_cruise_2 = 0.22      # Raymer dragkraftsnedgång (cruise lapse)
alpha_climb_2  = 0.83      # Raymer dragkraftsnedgång (climb lapse)
v_climb_2      = 80.0      # Stighastighet framåt [m/s]
v_vert_2       = 14.22     # Stighastighet vertikal [m/s]

# Beräkna Mass Sizing för Baseline, Iteration 1 och Iteration 2
sizing_base = compute_mass_sizing(Cd0_base, AR_base, oswald_e_base)
sizing_1 = compute_mass_sizing(Cd0_1, AR_1, oswald_e_1)
sizing_2 = compute_mass_sizing(Cd0_2, AR_2, oswald_e_2)

# ==============================================================================
# 4. BERÄKNINGSFUNKTION FÖR CONSTRAINT DIAGRAM (MATCHING DIAGRAM)
# ==============================================================================
def compute_iteration(Cd0, AR, oswald_e, Cl_max, Vstall, s_fl, TOP, alpha_cruise, alpha_climb, v_climb, v_vert, mtow_val):
    ws = np.linspace(25, 1000, 1000)
    
    # 1. Climb med Raymer thrust lapse
    q_climb = 0.5 * rho_sl * (v_climb ** 2)
    tw_climb_local = ((q_climb * Cd0) / (beta_climb * ws * g) +
                      (beta_climb * ws * g) / (q_climb * math.pi * AR * oswald_e) +
                      (v_vert / v_climb))
    tw_climb = tw_climb_local * (beta_climb / alpha_climb)
    
    # 2. Cruise med Raymer thrust lapse
    tw_cruise_local = ((q_cruise * Cd0) / (beta_cruise * ws * g) +
                       (beta_cruise * ws * g) / (q_cruise * math.pi * AR * oswald_e))
    tw_cruise = tw_cruise_local * (beta_cruise / alpha_cruise)
    
    # 3. Takeoff (TOP method)
    sigma = 1.0
    CL_TO = Cl_max / 1.21
    ws_fps = ws * 0.204816
    tw_takeoff = ws_fps / (TOP * sigma * CL_TO)
    
    # 4. Stall & Landing limits
    ws_stall = (1.0 / (2.0 * g0)) * rho_sl * (Vstall ** 2) * Cl_max
    s_landing = s_fl / 1.67
    s_a = 305.0
    ws_landing = ((s_landing - s_a) / 4.84) * (sigma * Cl_max)
    
    # 5. Design Point
    ws_design = min(ws_stall, ws_landing)
    tw_to_design = (ws_design * 0.204816) / (TOP * sigma * CL_TO)
    tw_climb_design = (((q_climb * Cd0) / (beta_climb * ws_design * g) +
                        (beta_climb * ws_design * g) / (q_climb * math.pi * AR * oswald_e) +
                        (v_vert / v_climb)) * (beta_climb / alpha_climb))
    tw_cruise_design = (((q_cruise * Cd0) / (beta_cruise * ws_design * g) +
                         (beta_cruise * ws_design * g) / (q_cruise * math.pi * AR * oswald_e)) * (beta_cruise / alpha_cruise))
    
    tw_design = max(tw_to_design, tw_climb_design, tw_cruise_design)
    
    if tw_design == tw_cruise_design:
        crit_tag = "Cruise (Raymer lapse)"
    elif tw_design == tw_climb_design:
        crit_tag = "Climb"
    else:
        crit_tag = "Takeoff"
        
    s_wing = mtow_val / ws_design
    thrust_total_kN = (tw_design * mtow_val * g) / 1000.0
    thrust_engine_2x_kN = thrust_total_kN / 2.0
    
    return {
        'ws': ws,
        'tw_climb': tw_climb,
        'tw_cruise': tw_cruise,
        'tw_takeoff': tw_takeoff,
        'ws_stall': ws_stall,
        'ws_landing': ws_landing,
        'ws_design': ws_design,
        'tw_design': tw_design,
        'crit_tag': crit_tag,
        's_wing': s_wing,
        'thrust_total_kN': thrust_total_kN,
        'thrust_engine_2x_kN': thrust_engine_2x_kN,
        'tw_cruise_design': tw_cruise_design,
        'tw_climb_design': tw_climb_design,
        'tw_to_design': tw_to_design,
        'mtow': mtow_val
    }

res1 = compute_iteration(Cd0_1, AR_1, oswald_e_1, Cl_max_1, Vstall_1, s_fl_1, TOP_1, alpha_cruise_1, alpha_climb_1, v_climb_1, v_vert_1, sizing_1['mtow'])
res2 = compute_iteration(Cd0_2, AR_2, oswald_e_2, Cl_max_2, Vstall_2, s_fl_2, TOP_2, alpha_cruise_2, alpha_climb_2, v_climb_2, v_vert_2, sizing_2['mtow'])

# ==============================================================================
# 5. TERMINAL OUTPUT: DEL 1 (MASS SIZING & KONVERGENS) + DEL 2 (DIAGRAMRESULTAT)
# ==============================================================================
if __name__ == "__main__":
    # --- DEL 1: RESULTAT FÖR ITERATION 2 ---
    s = sizing_2  # Aktiva värden från Iteration 2
    print("=" * 78)
    print("AETHER 80m Liquid Hydrogen BWB - MASS SIZING & ITERATIV KONVERGENS (ITERATION 2)")
    print("=" * 78)
    print(f"Dimensionerande rackvidd  : {range_m/1000:,.0f} km | Marschmach: {cruise_mach:.2f} @ FL350")
    print(f"Nyttolast + Besattning    : {payload_mass + crew_mass:,.1f} kg (Pax+Frakt: {payload_mass/1000:.2f} t, Crew: {crew_mass/1000:.2f} t)")
    print(f"LH2 Cruise SFC            : {sfc_lh2_cruise * 1e6:.3f} mg/(N*s) (Jet-A motsvarighet: {sfc_jeta_cruise * 1e6:.2f})")
    print(f"Profilresistans Cd0       : {s['cd0']:.4f} | Glidtal marsch (L/D): {s['ld_cruise']:.2f} (Max L/D: {s['ld_max']:.2f})")
    print(f"Total branslefraktion     : {s['ff_total'] * 100:.2f}% (Marschbransleforbrukning: {(1.0 - s['ff_5']) * 100:.2f}%)")
    print("-" * 78)
    print("ITERATIV KONVERGENS AV MTOW (ITERATION 2):")
    print(f"  * Startgissning (W0_guess): {s['w0_guess']:,.1f} kg ({s['w0_guess']/1000:.1f} ton)")
    print(f"  * Konvergerade pa         : {s['num_iterations']} iterationer (tolerans < {s['tol']} kg)")
    print(f"  * Konvergerat MTOW        : {s['mtow']:,.1f} kg ({s['mtow']/1000:.2f} ton)")
    print("-" * 78)
    print(f"{'Iteration':<10} | {'Beraknat MTOW (kg)':<22} | {'Andring / Fel (kg)':<20}")
    print("-" * 78)
    for it, val, d in s['history']:
        print(f"Iter {it:<5} | {val:18.1f} kg | {d:16.4f} kg")
    print("-" * 78)
    print("VIKTFORDELNING (MASS BREAKDOWN - ITERATION 2):")
    print(f"{'Komponent':<30} | {'Massa (kg)':<14} | {'Massa (t)':<10} | {'Andel av MTOW':<14}")
    print("-" * 78)
    print(f"{'Basflygkropp (Airframe)':<30} | {m_airframe:12.1f} kg | {m_airframe/1000:7.2f} t  | {(m_airframe/s['mtow'])*100:6.2f}%")
    print(f"{'Kryotankar (Gi = 0.50)':<30} | {s['m_tank']:12.1f} kg | {s['m_tank']/1000:7.2f} t  | {(s['m_tank']/s['mtow'])*100:6.2f}%")
    print(f"{'Operativ tomvikt (OEW)':<30} | {s['m_oew']:12.1f} kg | {s['m_oew']/1000:7.2f} t  | {(s['m_oew']/s['mtow'])*100:6.2f}%")
    print(f"{'Missionsbransle (LH2)':<30} | {s['m_fuel']:12.1f} kg | {s['m_fuel']/1000:7.2f} t  | {(s['m_fuel']/s['mtow'])*100:6.2f}%")
    print(f"{'Designpayload (430pax+cargo)':<30} | {payload_mass:12.1f} kg | {payload_mass/1000:7.2f} t  | {(payload_mass/s['mtow'])*100:6.2f}%")
    print(f"{'Besattning (12 pers)':<30} | {crew_mass:12.1f} kg | {crew_mass/1000:7.2f} t  | {(crew_mass/s['mtow'])*100:6.2f}%")
    print("-" * 78)
    print(f"{'Max Takeoff Weight (MTOW)':<30} | {s['mtow']:12.1f} kg | {s['mtow']/1000:7.2f} t  | 100.00%")
    print("=" * 78)
    print(f"Flytande vatevolym (LH2)  : {s['vol_liquid']:.1f} m^3")
    print(f"Total tankvolym           : {s['vol_cryo_total']:.1f} m^3 (inkl. 10% ullage & isolering)")
    print(f"Kabingolvyta              : {s['area_cabin']:.2f} m^2")
    print(f"Vingbelastning (kabin)    : {s['ws_cabin']:.1f} kg/m^2")
    print("=" * 78)

    # --- DEL 2: JAMFORELSETABELL AV KONVERGENS MELLAN ALLA STEG ---
    print("\n" + "=" * 78)
    print("JAMFORELSE: MASS SIZING & KONVERGENS (BASELINE vs ITERATION 1 vs ITERATION 2)")
    print("=" * 78)
    print(f"{'Parameter / Metod':<32} | {'Baseline':<12} | {'Iteration 1':<12} | {'Iteration 2':<12}")
    print("-" * 78)
    print(f"{'Profilresistans (Cd0)':<32} | {sizing_base['cd0']:<12.4f} | {sizing_1['cd0']:<12.4f} | {sizing_2['cd0']:<12.4f}")
    print(f"{'Glidtal marsch (L/D)':<32} | {sizing_base['ld_cruise']:<12.2f} | {sizing_1['ld_cruise']:<12.2f} | {sizing_2['ld_cruise']:<12.2f}")
    print(f"{'Total branslefraktion':<32} | {sizing_base['ff_total']*100:<11.2f}% | {sizing_1['ff_total']*100:<11.2f}% | {sizing_2['ff_total']*100:<11.2f}%")
    print(f"{'Antal iterationer (konvergens)':<32} | {sizing_base['num_iterations']:<12d} | {sizing_1['num_iterations']:<12d} | {sizing_2['num_iterations']:<12d}")
    print(f"{'Konvergerat MTOW (kg)':<32} | {sizing_base['mtow']:<12.1f} | {sizing_1['mtow']:<12.1f} | {sizing_2['mtow']:<12.1f}")
    print(f"{'Konvergerat MTOW (ton)':<32} | {sizing_base['mtow']/1000:<12.2f} | {sizing_1['mtow']/1000:<12.2f} | {sizing_2['mtow']/1000:<12.2f}")
    print("=" * 78)

    # --- DEL 3: SIZING SUMMARY (ITERATION 1 vs ITERATION 2) ---
    print("\n" + "=" * 78)
    print("AETHER 80m LH2 BWB - SIZING SUMMARY (ITERATION 1 vs ITERATION 2)")
    print("=" * 78)
    print(f"{'Parameter / Result':<35} | {'Iteration 1':<17} | {'Iteration 2':<17}")
    print("-" * 78)
    print(f"{'Profile Drag (Cd0)':<35} | {Cd0_1:<17.4f} | {Cd0_2:<17.4f}")
    print(f"{'Aspect Ratio (AR)':<35} | {AR_1:<17.2f} | {AR_2:<17.2f}")
    print(f"{'Max Lift Coeff (CL,max)':<35} | {Cl_max_1:<17.2f} | {Cl_max_2:<17.2f}")
    print(f"{'MTOW (fran konvergens)':<35} | {res1['mtow']:<11.1f} kg  | {res2['mtow']:<11.1f} kg")
    print(f"{'Design Wing Loading (W/S)_0':<35} | {res1['ws_design']:<11.1f} kg/m^2| {res2['ws_design']:<11.1f} kg/m^2")
    print(f"{'Design Thrust-to-Weight (T/W)_0':<35} | {res1['tw_design']:<17.4f} | {res2['tw_design']:<17.4f}")
    print(f"{'Governing Constraint':<35} | {res1['crit_tag']:<17} | {res2['crit_tag']:<17}")
    print(f"{'Cruise T/W at design':<35} | {res1['tw_cruise_design']:<17.4f} | {res2['tw_cruise_design']:<17.4f}")
    print(f"{'Climb T/W at design':<35} | {res1['tw_climb_design']:<17.4f} | {res2['tw_climb_design']:<17.4f}")
    print(f"{'Takeoff T/W at design':<35} | {res1['tw_to_design']:<17.4f} | {res2['tw_to_design']:<17.4f}")
    print(f"{'Wing Reference Area (S)':<35} | {res1['s_wing']:<11.1f} m^2    | {res2['s_wing']:<11.1f} m^2")
    print(f"{'Total Takeoff Thrust (T0)':<35} | {res1['thrust_total_kN']:<11.1f} kN     | {res2['thrust_total_kN']:<11.1f} kN")
    print(f"{'Thrust per Engine (2x)':<35} | {res1['thrust_engine_2x_kN']:<11.1f} kN     | {res2['thrust_engine_2x_kN']:<11.1f} kN")
    print("=" * 78)


    # ==============================================================================
    # 6. PLOT: TVÅ SEPARATA POPUP-FÖNSTER (SAMMA STIL)
    # ==============================================================================
    SHOW_SEPARATE_WINDOWS = True

    def draw_diagram(ax, res, title, cd0_val):
        ax.plot(res['ws'], res['tw_climb'], 'b-', lw=2, label='Climb (T/W)')
        ax.plot(res['ws'], res['tw_cruise'], 'r-', lw=2, label='Cruise - Raymer lapse (T/W)')
        ax.plot(res['ws'], res['tw_takeoff'], 'g-', lw=2, label='Takeoff (T/W)')

        ax.axvline(res['ws_stall'], color='darkred', linestyle='--', lw=2,
                   label=f"Stall limit ({res['ws_stall']:.0f} kg/m²)")
        ax.axvline(res['ws_landing'], color='purple', linestyle='-.', lw=2,
                   label=f"Landing limit ({res['ws_landing']:.0f} kg/m²)")

        ax.plot(res['ws_design'], res['tw_design'], 'k*', markersize=13, zorder=5,
                label=f"Design Point ({res['ws_design']:.0f} kg/m², {res['tw_design']:.2f})")

        ax.set_xlabel('Wing Loading, $W/S$ [kg/m²]', fontsize=11)
        ax.set_title(f"{title} ($C_{{D0}} = {cd0_val}$)", fontsize=12, fontweight='bold')
        ax.set_xlim(50, 750)
        ax.set_ylim(0, 0.6)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(loc='upper left', fontsize=8.5)

    # 1. Skapa och spara jämförelsen sida vid sida (till fil)
    fig_comp, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5), sharey=True)
    try:
        fig_comp.canvas.manager.set_window_title('Jämförelse: Iteration 1 vs Iteration 2')
    except Exception:
        pass
    draw_diagram(ax1, res1, 'Constraint Diagram: Iteration 1', Cd0_1)
    ax1.set_ylabel('Thrust-to-Weight Ratio, $T/W$', fontsize=11)
    draw_diagram(ax2, res2, 'Constraint Diagram: Iteration 2', Cd0_2)
    ax2.set_ylabel('')
    fig_comp.tight_layout()
    fig_comp.savefig('matching_diagram_comparison.png', dpi=300)

    # 2. Skapa Fönster 1: Iteration 1
    fig1, ax_s1 = plt.subplots(figsize=(8.5, 5.2))
    try:
        fig1.canvas.manager.set_window_title('Constraint Diagram: Iteration 1')
        fig1.canvas.manager.window.geometry('+50+100')   # Placeras till vänster på skärmen
    except Exception:
        pass
    draw_diagram(ax_s1, res1, 'Constraint Diagram: Iteration 1', Cd0_1)
    ax_s1.set_ylabel('Thrust-to-Weight Ratio, $T/W$', fontsize=11)
    fig1.tight_layout()
    fig1.savefig('matching_diagram_iteration1.png', dpi=300)

    # 3. Skapa Fönster 2: Iteration 2
    fig2, ax_s2 = plt.subplots(figsize=(8.5, 5.2))
    try:
        fig2.canvas.manager.set_window_title('Constraint Diagram: Iteration 2')
        fig2.canvas.manager.window.geometry('+850+100')  # Placeras till höger på skärmen
    except Exception:
        pass
    draw_diagram(ax_s2, res2, 'Constraint Diagram: Iteration 2', Cd0_2)
    ax_s2.set_ylabel('Thrust-to-Weight Ratio, $T/W$', fontsize=11)
    fig2.tight_layout()
    fig2.savefig('matching_diagram_iteration2.png', dpi=300)

    if SHOW_SEPARATE_WINDOWS:
        # Stäng kombinerade figuren så de TVÅ separata fönstren poppar upp
        plt.close(fig_comp)
        print("Visar 2 separata popup-fonster (Fönster 1: Iteration 1, Fönster 2: Iteration 2)...")
    else:
        # Stäng enkelfönstren så endast det kombinerade fönstret visas
        plt.close(fig1)
        plt.close(fig2)
        print("Visar 1 gemensamt fönster med båda diagrammen...")

    print("Sparade bildfiler:")
    print("  -> matching_diagram_comparison.png (Bada iterationerna i tva bildrutor sida vid sida)")
    print("  -> matching_diagram_iteration1.png (Iteration 1 separat)")
    print("  -> matching_diagram_iteration2.png (Iteration 2 separat)")
    plt.show()

    # Engine sizing
    reference_thrust_kN = 513.95
    required_thrust_kN = 435.0

    reference_length_m = 7.281
    reference_fan_diameter_m = 3.2512
    reference_mass_kg = 8761.0

    SF = required_thrust_kN / reference_thrust_kN

    length_m = reference_length_m * SF**0.4
    fan_diameter_m = reference_fan_diameter_m  # Held constant
    mass_kg = reference_mass_kg * SF**1.1     # Preliminary estimate only

    print(f"Thrust scale factor: {SF:.6f}")
    print(f"Engine length:      {length_m:.3f} m")
    print(f"Fan diameter:       {fan_diameter_m:.4f} m")
    print(f"Estimated dry mass: {mass_kg:.0f} kg")

