#!/usr/bin/env python3
"""
=============================================================================
CG Travel & Stability Envelope Analysis for EXAELIA Hydrogen Aircraft
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Compares:
1. All-Aft Empennage Tank Layout (Severe CG Excursion)
2. Split Forward/Aft Tank Layout (Balanced CG Travel)
=============================================================================
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plot_cg_envelope(output_png="cg_excursion_comparison.png"):
    mac = 6.18
    x_lemac = 29.50 # Leading edge of MAC

    # Component Masses (tonnes) & Locations (m)
    m_dry = 80.0
    x_dry = 31.5

    m_pax_freight = 53.75 # 430 Pax + 44 LD3 cargo
    x_pax = 26.0

    m_tank_dry = 38.51
    m_fuel = 38.51

    # Fuel levels from 0% to 100%
    fuel_fractions = np.linspace(0.0, 1.0, 100)
    
    # 1. All-Aft Configuration (Tanks at X = 52.0 m)
    x_tank_aft = 52.0
    cg_aft = []
    w_aft = []
    for f in fuel_fractions:
        fuel_curr = m_fuel * f
        tot_mass = m_dry + m_pax_freight + m_tank_dry + fuel_curr
        cg_curr = (m_dry*x_dry + m_pax_freight*x_pax + (m_tank_dry + fuel_curr)*x_tank_aft) / tot_mass
        cg_aft.append(cg_curr)
        w_aft.append(tot_mass)

    # 2. Split Configuration (50% Fwd at X=16m, 50% Aft at X=52m)
    x_tank_fwd = 16.0
    cg_split = []
    w_split = []
    for f in fuel_fractions:
        fuel_curr = m_fuel * f
        tot_mass = m_dry + m_pax_freight + m_tank_dry + fuel_curr
        fwd_mass = (m_tank_dry/2.0) + (fuel_curr/2.0)
        aft_mass = (m_tank_dry/2.0) + (fuel_curr/2.0)
        cg_curr = (m_dry*x_dry + m_pax_freight*x_pax + fwd_mass*x_tank_fwd + aft_mass*x_tank_aft) / tot_mass
        cg_split.append(cg_curr)
        w_split.append(tot_mass)

    # Convert to % MAC
    cg_aft_mac = [(x - x_lemac) / mac * 100.0 for x in cg_aft]
    cg_split_mac = [(x - x_lemac) / mac * 100.0 for x in cg_split]

    plt.style.use("seaborn-v0_8-darkgrid" if "seaborn-v0_8-darkgrid" in plt.style.available else "default")
    fig, ax = plt.subplots(figsize=(12, 7), dpi=160)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#1e293b')

    text_color = '#f8fafc'
    grid_color = '#334155'

    ax.tick_params(colors=text_color, which='both', labelsize=10)
    ax.xaxis.label.set_color(text_color)
    ax.yaxis.label.set_color(text_color)
    ax.title.set_color(text_color)
    ax.grid(True, linestyle='--', alpha=0.5, color=grid_color)
    for spine in ax.spines.values():
        spine.set_color(grid_color)

    # Standard permissible transport CG window (e.g. 12% to 32% MAC)
    ax.axvspan(12.0, 32.0, color='#34d399', alpha=0.15, label='Typical Permissible CG Window (12% - 32% MAC)')

    # Plot All-Aft curve
    ax.plot(cg_aft_mac, w_aft, color='#ef4444', linewidth=3.0, marker='o', markevery=15,
            label=f'All-Aft Tank Layout ($\\Delta X_{{CG}} = {abs(cg_aft_mac[-1]-cg_aft_mac[0]):.1f}\\%$ MAC -> Severe Shift!)')
    
    # Plot Split curve
    ax.plot(cg_split_mac, w_split, color='#38bdf8', linewidth=3.0, marker='s', markevery=15,
            label=f'Split Fwd/Aft Tank Layout ($\\Delta X_{{CG}} = {abs(cg_split_mac[-1]-cg_split_mac[0]):.1f}\\%$ MAC -> Stable)')

    # Annotate Key Points
    ax.annotate(f'Take-Off (MTOW={w_aft[-1]:.1f} t)\nCG = {cg_aft_mac[-1]:.1f}% MAC',
                xy=(cg_aft_mac[-1], w_aft[-1]), xytext=(cg_aft_mac[-1]-18, w_aft[-1]-8),
                arrowprops=dict(facecolor='#ef4444', shrink=0.08, width=1.5, headwidth=6),
                color='#f8fafc', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#ef4444', alpha=0.9))

    ax.annotate(f'Landing (ZFW={w_aft[0]:.1f} t)\nCG = {cg_aft_mac[0]:.1f}% MAC',
                xy=(cg_aft_mac[0], w_aft[0]), xytext=(cg_aft_mac[0]-20, w_aft[0]+6),
                arrowprops=dict(facecolor='#ef4444', shrink=0.08, width=1.5, headwidth=6),
                color='#f8fafc', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#ef4444', alpha=0.9))

    ax.annotate(f'Split Tanks Take-Off\nCG = {cg_split_mac[-1]:.1f}% MAC',
                xy=(cg_split_mac[-1], w_split[-1]), xytext=(cg_split_mac[-1]+8, w_split[-1]-6),
                arrowprops=dict(facecolor='#38bdf8', shrink=0.08, width=1.5, headwidth=6),
                color='#f8fafc', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.9))

    ax.annotate(f'Split Tanks Landing\nCG = {cg_split_mac[0]:.1f}% MAC',
                xy=(cg_split_mac[0], w_split[0]), xytext=(cg_split_mac[0]-15, w_split[0]-12),
                arrowprops=dict(facecolor='#38bdf8', shrink=0.08, width=1.5, headwidth=6),
                color='#f8fafc', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#1e293b', edgecolor='#38bdf8', alpha=0.9))

    ax.set_xlabel(r'Center of Gravity Location [$\% \mathrm{MAC}$]', fontsize=12, fontweight='bold')
    ax.set_ylabel(r'Total Aircraft Weight [tonnes]', fontsize=12, fontweight='bold')
    ax.set_title('EXAELIA Hydrogen Transport — Center of Gravity (CG) Travel Loading Diagram\n'
                 'All-Aft Empennage Tanks vs. Split Forward/Aft Tank Configuration (12,500 km Mission)',
                 fontsize=13, fontweight='bold', color=text_color, pad=12)

    ax.legend(loc='upper right', facecolor='#1e293b', edgecolor='#334155', fontsize=9, labelcolor=text_color)
    plt.tight_layout()
    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Saved CG Excursion Chart: {os.path.abspath(output_png)}")

if __name__ == "__main__":
    plot_cg_envelope()
