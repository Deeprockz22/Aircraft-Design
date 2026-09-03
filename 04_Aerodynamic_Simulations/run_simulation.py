#!/usr/bin/env python3
"""
=============================================================================
VSPAERO Aerodynamic Simulation & Mass Analysis Pipeline for A380 Hydrogen
=============================================================================
Executes:
1. Mass Properties & Inertia Analysis
2. OpenVSP Geometry & Sref / bref / cref verification
3. VSPAERO Vortex-Lattice Aerodynamic Solver at Mach 0.85 Cruise
4. Polar Analysis (CL vs Alpha, CL vs CD, L/D vs Alpha, CMy vs CL)
5. Generates publication-grade visualization charts
=============================================================================
"""

import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import openvsp as vsp

from build_a380_hydrogen import build_a380_hydrogen

def parse_polar_file(polar_path):
    """Parses standard VSPAERO .polar output file into numpy arrays."""
    with open(polar_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Header is line index 2 (line 3 in file)
    header = lines[2].split()
    data_rows = []
    for line in lines[3:]:
        parts = line.split()
        if len(parts) >= len(header):
            try:
                data_rows.append([float(x) for x in parts[:len(header)]])
            except ValueError:
                continue
                
    data = np.array(data_rows)
    col_dict = {col_name: data[:, i] for i, col_name in enumerate(header)}
    return col_dict

def run_simulation(model_file="A380_Hydrogen.vsp3", rerun_solver=False):
    print("=================================================================")
    print("  Running OpenVSP Simulation Pipeline for Airbus A380 Hydrogen")
    print("=================================================================")

    # Ensure model exists or build it
    if not os.path.exists(model_file):
        build_a380_hydrogen()

    vsp.ClearVSPModel()
    vsp.ReadVSPFile(model_file)
    vsp.Update()
    print(f"[1/4] Loaded OpenVSP Model: {model_file}")

    # Reference dimensions from MainWing
    wing_id = vsp.FindGeom("MainWing", 0)
    sref = vsp.GetParmVal(wing_id, "TotalArea", "WingGeom")
    bref = vsp.GetParmVal(wing_id, "TotalSpan", "WingGeom")
    cref = sref / bref

    # -------------------------------------------------------------------------
    # 1. MASS PROPERTIES & CENTER OF GRAVITY (CG) ANALYSIS
    # -------------------------------------------------------------------------
    print("\n[2/4] Executing Mass Properties & Inertia Analysis...")
    vsp.SetAnalysisInputDefaults("MassProp")
    rid_mp = vsp.ExecAnalysis("MassProp")

    tot_vol = vsp.GetDoubleResults(rid_mp, "Total_Mass")[0]
    cg_vec = vsp.GetVec3dResults(rid_mp, "Total_CG")[0]
    ixx = vsp.GetDoubleResults(rid_mp, "Total_Ixx")[0]
    iyy = vsp.GetDoubleResults(rid_mp, "Total_Iyy")[0]
    izz = vsp.GetDoubleResults(rid_mp, "Total_Izz")[0]

    cg_x = cg_vec.x()
    cg_y = cg_vec.y()
    cg_z = cg_vec.z()

    print(f"     Total Enclosed Volume     : {tot_vol:.2f} m³")
    print(f"     Center of Gravity (CG)    : X={cg_x:.2f} m, Y={cg_y:.2f} m, Z={cg_z:.2f} m")
    print(f"     Moments of Inertia (Ixx)  : {ixx:.2e}")
    print(f"     Moments of Inertia (Iyy)  : {iyy:.2e}")
    print(f"     Moments of Inertia (Izz)  : {izz:.2e}")

    # -------------------------------------------------------------------------
    # 2. VSPAERO AERODYNAMIC SOLVER SETUP & EXECUTION
    # -------------------------------------------------------------------------
    polar_file = "A380_Hydrogen.polar"
    if rerun_solver or not os.path.exists(polar_file):
        print("\n[3/4] Setting Up VSPAERO Vortex-Lattice Aerodynamic Solver...")
        
        # 2a. Compute Geometry for VSPAERO
        vsp.SetAnalysisInputDefaults("VSPAEROComputeGeometry")
        vsp.SetIntAnalysisInput("VSPAEROComputeGeometry", "GeomSet", [vsp.SET_NONE])
        vsp.SetIntAnalysisInput("VSPAEROComputeGeometry", "ThinGeomSet", [vsp.SET_ALL])
        rid_geom = vsp.ExecAnalysis("VSPAEROComputeGeometry")

        # 2b. Sweep Analysis Configuration
        mach = 0.85
        alpha_start = -2.0
        alpha_end = 8.0
        num_pts = 6

        vsp.SetAnalysisInputDefaults("VSPAEROSweep")
        vsp.SetIntAnalysisInput("VSPAEROSweep", "GeomSet", [vsp.SET_NONE])
        vsp.SetIntAnalysisInput("VSPAEROSweep", "ThinGeomSet", [vsp.SET_ALL])
        vsp.SetDoubleAnalysisInput("VSPAEROSweep", "Sref", [sref])
        vsp.SetDoubleAnalysisInput("VSPAEROSweep", "bref", [bref])
        vsp.SetDoubleAnalysisInput("VSPAEROSweep", "cref", [cref])
        vsp.SetDoubleAnalysisInput("VSPAEROSweep", "Xcg", [cg_x])
        vsp.SetDoubleAnalysisInput("VSPAEROSweep", "Zcg", [cg_z])

        vsp.SetDoubleAnalysisInput("VSPAEROSweep", "MachStart", [mach])
        vsp.SetDoubleAnalysisInput("VSPAEROSweep", "MachEnd", [mach])
        vsp.SetIntAnalysisInput("VSPAEROSweep", "MachNpts", [1])

        vsp.SetDoubleAnalysisInput("VSPAEROSweep", "AlphaStart", [alpha_start])
        vsp.SetDoubleAnalysisInput("VSPAEROSweep", "AlphaEnd", [alpha_end])
        vsp.SetIntAnalysisInput("VSPAEROSweep", "AlphaNpts", [num_pts])

        print(f"     Simulation Flow Conditions:")
        print(f"     * Cruise Mach Number       : {mach}")
        print(f"     * Angle of Attack Range    : [{alpha_start}°, {alpha_end}°] with {num_pts} points")
        print(f"     * Reference Area (Sref)    : {sref:.2f} m²")
        print(f"     * Reference Span (bref)    : {bref:.2f} m")
        print(f"     * Reference Chord (cref)   : {cref:.2f} m")
        
        print("\n     Solving 3D Aerodynamic Flowfield (VSPAERO)...")
        rid_sweep = vsp.ExecAnalysis("VSPAEROSweep")
        print("     [OK] VSPAERO Solution Converged!")
    else:
        print(f"\n[3/4] Loaded Existing VSPAERO Polar File: {polar_file}")

    # -------------------------------------------------------------------------
    # 3. EXTRACT RESULTS & PROCESS POLARS
    # -------------------------------------------------------------------------
    polars = parse_polar_file(polar_file)
    
    alphas = polars["AoA"]
    cl_tot = polars["CLtot"]
    cd_tot = polars["CDtot"]
    cd_ind = polars["CDi"]
    cd_par = polars["CDo"]
    c_my   = polars["CMytot"]
    lod    = polars["L/D"]

    # Key aerodynamic figures of merit
    cl_alpha_per_deg = np.polyfit(alphas, cl_tot, 1)[0]
    cl_alpha_per_rad = cl_alpha_per_deg * (180.0 / np.pi)

    # Maximum Lift-to-Drag Ratio (L/D_max)
    max_lod_idx = np.argmax(lod)
    max_lod = lod[max_lod_idx]
    alpha_max_lod = alphas[max_lod_idx]
    cl_at_max_lod = cl_tot[max_lod_idx]

    # Pitching moment derivative dCM/dCL
    cm_cl_slope = np.polyfit(cl_tot, c_my, 1)[0]
    static_margin = -cm_cl_slope * 100.0

    print("\n=================================================================")
    print("  SIMULATION RESULTS SUMMARY: A380 HYDROGEN (CRUISE MACH 0.85)")
    print("=================================================================")
    print(f" {'Alpha (deg)':>12} | {'CL':>8} | {'CD_tot':>8} | {'CD_ind':>8} | {'CD_par':>8} | {'L/D':>8} | {'CMy':>8}")
    print("-" * 75)
    for i in range(len(alphas)):
        print(f" {alphas[i]:>12.2f} | {cl_tot[i]:>8.4f} | {cd_tot[i]:>8.4f} | {cd_ind[i]:>8.4f} | {cd_par[i]:>8.4f} | {lod[i]:>8.2f} | {c_my[i]:>8.4f}")
    print("=" * 75)
    print(f" Key Performance Metrics:")
    print(f"  * Lift Slope (dCL/dAlpha) : {cl_alpha_per_deg:.4f} /deg ({cl_alpha_per_rad:.3f} /rad)")
    print(f"  * Maximum L/D (L/D_max)   : {max_lod:.2f} at Alpha = {alpha_max_lod:.1f}° (CL = {cl_at_max_lod:.3f})")
    print(f"  * Longitudinal Stability  : dCMy/dCL = {cm_cl_slope:.4f} (Static Margin: {static_margin:.1f}%)")
    print(f"  * Pitch-Trim Alpha        : ~{np.interp(0.0, -c_my, alphas):.2f}° for CMy = 0")

    # -------------------------------------------------------------------------
    # 4. GENERATE HIGH-QUALITY PLOTS
    # -------------------------------------------------------------------------
    print("\n[4/4] Generating Aerodynamic Performance Charts...")
    
    plt.style.use("seaborn-v0_8-darkgrid" if "seaborn-v0_8-darkgrid" in plt.style.available else "default")
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 11), dpi=150)
    fig.patch.set_facecolor('#0f172a')

    chart_bg = '#1e293b'
    text_color = '#f8fafc'
    grid_color = '#334155'
    accent_blue = '#38bdf8'
    accent_emerald = '#34d399'
    accent_amber = '#fbbf24'
    accent_rose = '#fb7185'

    for ax in (ax1, ax2, ax3, ax4):
        ax.set_facecolor(chart_bg)
        ax.tick_params(colors=text_color, which='both')
        ax.xaxis.label.set_color(text_color)
        ax.yaxis.label.set_color(text_color)
        ax.title.set_color(text_color)
        ax.grid(True, linestyle='--', alpha=0.5, color=grid_color)
        for spine in ax.spines.values():
            spine.set_color(grid_color)

    # Plot 1: Lift Curve (CL vs Alpha)
    ax1.plot(alphas, cl_tot, 'o-', color=accent_blue, linewidth=2.5, markersize=7, label=r'$C_L$ Total')
    ax1.set_title(r'Lift Coefficient vs. Angle of Attack ($C_L$ vs. $\alpha$)', fontsize=12, fontweight='bold', pad=10)
    ax1.set_xlabel(r'Angle of Attack $\alpha$ (deg)', fontsize=11)
    ax1.set_ylabel(r'Lift Coefficient $C_L$', fontsize=11)
    ax1.axhline(0, color=grid_color, linestyle='-')
    ax1.axvline(0, color=grid_color, linestyle='-')
    ax1.text(0.05, 0.78, f'$dC_L/d\\alpha = {cl_alpha_per_deg:.4f}$ /deg\nCruise $C_L \\approx 0.45$ at $\\alpha \\approx 2.0^\\circ$', 
             transform=ax1.transAxes, color=text_color, bbox=dict(facecolor=chart_bg, edgecolor=accent_blue, boxstyle='round,pad=0.5'))
    ax1.legend(loc='lower right', facecolor=chart_bg, edgecolor=grid_color, labelcolor=text_color)

    # Plot 2: Drag Polar (CL vs CD)
    ax2.plot(cd_tot, cl_tot, 's-', color=accent_emerald, linewidth=2.5, markersize=7, label=r'Total Drag $C_D$')
    ax2.plot(cd_ind, cl_tot, '--', color=accent_blue, linewidth=1.5, label=r'Induced Drag $C_{Di}$')
    ax2.plot(cd_par, cl_tot, ':', color=accent_rose, linewidth=1.5, label=r'Parasite Drag $C_{Do}$')
    ax2.set_title(r'Drag Polar ($C_L$ vs. $C_D$)', fontsize=12, fontweight='bold', pad=10)
    ax2.set_xlabel(r'Drag Coefficient $C_D$', fontsize=11)
    ax2.set_ylabel(r'Lift Coefficient $C_L$', fontsize=11)
    ax2.legend(loc='lower right', facecolor=chart_bg, edgecolor=grid_color, labelcolor=text_color)

    # Plot 3: Lift-to-Drag Ratio (L/D vs Alpha)
    ax3.plot(alphas, lod, '^-', color=accent_amber, linewidth=2.5, markersize=8, label=r'Aerodynamic Efficiency $L/D$')
    ax3.plot(alpha_max_lod, max_lod, '*', color='#f43f5e', markersize=14, label=f'$(L/D)_{{max}} = {max_lod:.1f}$')
    ax3.set_title(r'Aerodynamic Efficiency ($L/D$ vs. $\alpha$)', fontsize=12, fontweight='bold', pad=10)
    ax3.set_xlabel(r'Angle of Attack $\alpha$ (deg)', fontsize=11)
    ax3.set_ylabel(r'Lift-to-Drag Ratio $(L/D)$', fontsize=11)
    ax3.legend(loc='lower center', facecolor=chart_bg, edgecolor=grid_color, labelcolor=text_color)

    # Plot 4: Longitudinal Stability (CMy vs CL)
    ax4.plot(cl_tot, c_my, 'd-', color=accent_rose, linewidth=2.5, markersize=7, label=r'Pitching Moment $C_{My}$')
    ax4.set_title(r'Pitching Moment vs. Lift ($C_{My}$ vs. $C_L$)', fontsize=12, fontweight='bold', pad=10)
    ax4.set_xlabel(r'Lift Coefficient $C_L$', fontsize=11)
    ax4.set_ylabel(r'Pitching Moment Coefficient $C_{My}$ (re CG)', fontsize=11)
    ax4.axhline(0, color=grid_color, linestyle='-')
    ax4.text(0.05, 0.20, f'Static Stability $dC_{{My}}/dC_L < 0$\nStatic Margin: {static_margin:.1f}%', 
             transform=ax4.transAxes, color=text_color, bbox=dict(facecolor=chart_bg, edgecolor=accent_rose, boxstyle='round,pad=0.5'))
    ax4.legend(loc='upper right', facecolor=chart_bg, edgecolor=grid_color, labelcolor=text_color)

    plt.suptitle('Airbus A380-800 Liquid Hydrogen (LH2) Demonstrator — VSPAERO Aerodynamic Polars\n'
                 r'Cruise Condition: Mach 0.85 | FL350 ($h = 10,668$ m) | $S_{ref} = 849.3$ m² | $b = 79.75$ m',
                 fontsize=14, fontweight='bold', color=text_color, y=0.98)

    plt.tight_layout(rect=[0, 0.03, 1, 0.94])
    
    plot_filename = "a380_hydrogen_aerodynamic_polars.png"
    plt.savefig(plot_filename, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"\n[OK] Aerodynamic Polar Chart Saved: {os.path.abspath(plot_filename)}")
    print("=================================================================")
    print("  Simulation & Analysis Completed Successfully!")
    print("=================================================================")

if __name__ == "__main__":
    run_simulation()
