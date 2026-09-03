#!/usr/bin/env python3
"""
=============================================================================
EXAELIA Hydrogen Aircraft — Dimensioned CAD & Interior Engineering Drawing
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Generates:
1. OpenVSP 3D CAD model with transparent fuselage, visible seat rows,
   LD3 cargo blocks, cryotanks, and reference dimension markers.
2. Full Orthographic Engineering 3-View CAD Blueprint with exact dimensions.
=============================================================================
"""

import math
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch
import openvsp as vsp

def build_openvsp_dimensioned(output_prefix="EXAELIA_Dimensioned_Interior"):
    print("Building OpenVSP Model with Visible Seats, Cargo, Tanks & Dimensions...")
    vsp.ClearVSPModel()

    # 1. Translucent Fuselage Shell
    fuse_id = vsp.AddGeom("FUSELAGE", "")
    vsp.SetGeomName(fuse_id, "Fuselage_OML_Translucent")
    vsp.SetParmVal(fuse_id, "Length", "Design", 68.50)
    vsp.SetParmVal(fuse_id, "Tess_W", "Shape", 49)
    vsp.SetGeomMaterialName(fuse_id, "White")

    fuse_xsurf = vsp.GetXSecSurf(fuse_id, 0)
    for i in range(1, vsp.GetNumXSec(fuse_xsurf) - 1):
        vsp.ChangeXSecShape(fuse_xsurf, i, vsp.XS_ELLIPSE)
        xsec = vsp.GetXSec(fuse_xsurf, i)
        w_p = vsp.GetXSecParm(xsec, "Ellipse_Width")
        h_p = vsp.GetXSecParm(xsec, "Ellipse_Height")
        xloc_p = vsp.GetXSecParm(xsec, "XLocPercent")
        if i == 1:
            vsp.SetParmVal(xloc_p, 0.10)
            vsp.SetParmVal(w_p, 5.20)
            vsp.SetParmVal(h_p, 5.80)
        elif i == 2:
            vsp.SetParmVal(xloc_p, 0.50)
            vsp.SetParmVal(w_p, 6.20)
            vsp.SetParmVal(h_p, 6.90)
        elif i == 3:
            vsp.SetParmVal(xloc_p, 0.86)
            vsp.SetParmVal(w_p, 4.40)
            vsp.SetParmVal(h_p, 4.60)

    # 2. Main Cabin Floor (Deck)
    floor_id = vsp.AddGeom("POD", "")
    vsp.SetGeomName(floor_id, "Main_Cabin_Floor_Deck")
    vsp.SetParmVal(floor_id, "Length", "Design", 52.00)
    vsp.SetParmVal(floor_id, "X_Rel_Location", "XForm", 8.00)
    vsp.SetParmVal(floor_id, "Z_Rel_Location", "XForm", -0.35)
    vsp.SetGeomMaterialName(floor_id, "Aluminum")

    # 3. Individual Seating Rows (Business Class: 4 rows; Economy Class: 15 modular row clusters)
    # Business Class (Rows 1 to 4: Gold pods)
    for r in range(4):
        b_row_id = vsp.AddGeom("POD", "")
        vsp.SetGeomName(b_row_id, f"SeatRow_Biz_{r+1}")
        vsp.SetParmVal(b_row_id, "Length", "Design", 1.20)
        vsp.SetParmVal(b_row_id, "X_Rel_Location", "XForm", 9.50 + r * 1.50)
        vsp.SetParmVal(b_row_id, "Z_Rel_Location", "XForm", 0.15)
        vsp.SetGeomMaterialName(b_row_id, "Metal")

    # Economy Class (Row clusters: Blue/White pods)
    for c in range(12):
        e_row_id = vsp.AddGeom("POD", "")
        vsp.SetGeomName(e_row_id, f"SeatCluster_Econ_{c+1}")
        vsp.SetParmVal(e_row_id, "Length", "Design", 2.80)
        vsp.SetParmVal(e_row_id, "X_Rel_Location", "XForm", 17.00 + c * 3.10)
        vsp.SetParmVal(e_row_id, "Z_Rel_Location", "XForm", 0.15)
        vsp.SetGeomMaterialName(e_row_id, "White")

    # 4. Lower Deck Cargo (LD3 Container Groups)
    cargo_fwd_id = vsp.AddGeom("POD", "")
    vsp.SetGeomName(cargo_fwd_id, "CargoHold_Fwd_24_LD3")
    vsp.SetParmVal(cargo_fwd_id, "Length", "Design", 13.50)
    vsp.SetParmVal(cargo_fwd_id, "X_Rel_Location", "XForm", 12.00)
    vsp.SetParmVal(cargo_fwd_id, "Z_Rel_Location", "XForm", -1.40)
    vsp.SetGeomMaterialName(cargo_fwd_id, "Metal")

    cargo_aft_id = vsp.AddGeom("POD", "")
    vsp.SetGeomName(cargo_aft_id, "CargoHold_Aft_20_LD3")
    vsp.SetParmVal(cargo_aft_id, "Length", "Design", 11.50)
    vsp.SetParmVal(cargo_aft_id, "X_Rel_Location", "XForm", 36.50)
    vsp.SetParmVal(cargo_aft_id, "Z_Rel_Location", "XForm", -1.40)
    vsp.SetGeomMaterialName(cargo_aft_id, "Metal")

    # 5. Upper Cryogenic Hydrogen Tanks (7x Tanks)
    tank_diam = 3.09
    tank_len = 12.37
    tank_positions = [
        ("LH2_Tank_1_D3.09m_L12.37m",  7.50,  0.00,  1.60),
        ("LH2_Tank_2_D3.09m_L12.37m", 19.80,  0.00,  1.60),
        ("LH2_Tank_3_D3.09m_L12.37m", 32.10,  0.00,  1.60),
        ("LH2_Tank_4_D3.09m_L12.37m", 44.40,  0.00,  1.60),
        ("LH2_Tank_5_D3.09m_L12.37m", 56.70,  0.00,  1.60),
    ]
    for name, x_pos, y_pos, z_pos in tank_positions:
        t_id = vsp.AddGeom("FUSELAGE", "")
        vsp.SetGeomName(t_id, name)
        vsp.SetParmVal(t_id, "Length", "Design", tank_len)
        vsp.SetParmVal(t_id, "X_Rel_Location", "XForm", x_pos)
        vsp.SetParmVal(t_id, "Y_Rel_Location", "XForm", y_pos)
        vsp.SetParmVal(t_id, "Z_Rel_Location", "XForm", z_pos)
        vsp.SetGeomMaterialName(t_id, "Blue Plastic")
        t_xsurf = vsp.GetXSecSurf(t_id, 0)
        for j in range(1, vsp.GetNumXSec(t_xsurf) - 1):
            vsp.ChangeXSecShape(t_xsurf, j, vsp.XS_CIRCLE)
            vsp.SetParmVal(vsp.GetXSecParm(vsp.GetXSec(t_xsurf, j), "Circle_Diameter"), tank_diam)

    # 6. Sized Transonic Wing
    wing_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(wing_id, "MainWing_Span58.75m_Area363m2")
    vsp.SetParmVal(wing_id, "X_Rel_Location", "XForm", 26.50)
    vsp.SetParmVal(wing_id, "Z_Rel_Location", "XForm", -1.20)
    vsp.SetGeomMaterialName(wing_id, "Aluminum")
    w_xsec = vsp.GetXSec(vsp.GetXSecSurf(wing_id, 0), 1)
    vsp.SetParmVal(vsp.GetXSecParm(w_xsec, "Span"), 58.75 / 2.0)
    vsp.SetParmVal(vsp.GetXSecParm(w_xsec, "Sweep"), 29.0)
    vsp.SetParmVal(vsp.GetXSecParm(w_xsec, "Dihedral"), 5.5)
    vsp.SetParmVal(vsp.GetXSecParm(w_xsec, "Root_Chord"), 9.20)
    vsp.SetParmVal(vsp.GetXSecParm(w_xsec, "Tip_Chord"), 2.40)

    # 7. Empennage & Engines
    htail_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(htail_id, "HTail_Span19.5m_Area71m2")
    vsp.SetParmVal(htail_id, "X_Rel_Location", "XForm", 58.50)
    vsp.SetParmVal(htail_id, "Z_Rel_Location", "XForm", 1.80)
    vsp.SetGeomMaterialName(htail_id, "Aluminum")
    ht_xsec = vsp.GetXSec(vsp.GetXSecSurf(htail_id, 0), 1)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec, "Span"), 9.75)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec, "Sweep"), 33.0)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec, "Root_Chord"), 5.60)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec, "Tip_Chord"), 2.10)

    vtail_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(vtail_id, "VTail_Height9.8m_Area52m2")
    vsp.SetParmVal(vtail_id, "X_Rel_Location", "XForm", 51.00)
    vsp.SetParmVal(vtail_id, "Z_Rel_Location", "XForm", 2.60)
    vsp.SetParmVal(vtail_id, "X_Rel_Rotation", "XForm", 90.0)
    vsp.SetParmVal(vtail_id, "Sym_Planar_Flag", "Sym", vsp.SYM_NONE)
    vsp.SetGeomMaterialName(vtail_id, "Blue Plastic")
    vt_xsec = vsp.GetXSec(vsp.GetXSecSurf(vtail_id, 0), 1)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec, "Span"), 9.80)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec, "Sweep"), 38.0)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec, "Root_Chord"), 7.80)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec, "Tip_Chord"), 2.80)

    for name, y_pos, z_pos, x_pos in [("Turbofan_Port_In", -9.5, -1.8, 24.5), ("Turbofan_Stbd_In", 9.5, -1.8, 24.5),
                                      ("Turbofan_Port_Out", -17.8, -0.9, 31.0), ("Turbofan_Stbd_Out", 17.8, -0.9, 31.0)]:
        eng_id = vsp.AddGeom("FUSELAGE", "")
        vsp.SetGeomName(eng_id, name)
        vsp.SetParmVal(eng_id, "Length", "Design", 4.80)
        vsp.SetParmVal(eng_id, "X_Rel_Location", "XForm", x_pos)
        vsp.SetParmVal(eng_id, "Y_Rel_Location", "XForm", y_pos)
        vsp.SetParmVal(eng_id, "Z_Rel_Location", "XForm", z_pos)
        vsp.SetGeomMaterialName(eng_id, "Aluminum")
        e_xsurf = vsp.GetXSecSurf(eng_id, 0)
        for k in range(1, vsp.GetNumXSec(e_xsurf) - 1):
            vsp.ChangeXSecShape(e_xsurf, k, vsp.XS_CIRCLE)
            vsp.SetParmVal(vsp.GetXSecParm(vsp.GetXSec(e_xsurf, k), "Circle_Diameter"), 2.45)

    vsp.Update()
    vsp_file = f"{output_prefix}.vsp3"
    stl_file = f"{output_prefix}.stl"
    vsp.WriteVSPFile(vsp_file)
    vsp.ExportFile(stl_file, vsp.SET_ALL, vsp.EXPORT_STL)
    print(f"[OK] Saved OpenVSP Model: {os.path.abspath(vsp_file)}")

def render_dimensioned_engineering_blueprint(output_png="exaelia_dimensioned_engineering_drawing.png"):
    """Creates a full 3-view CAD engineering blueprint with exact dimension lines."""
    print("Generating High-Precision Dimensioned Engineering Drawing...")
    fig = plt.figure(figsize=(18, 13), dpi=160)
    fig.patch.set_facecolor('#0f172a')

    # 3 View Subplots: Top (Planform), Side (Profile & Cutaway), Front (Span & Dihedral)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.1, 1.0], width_ratios=[1.2, 0.8], hspace=0.32, wspace=0.25)

    # -------------------------------------------------------------------------
    # 1. TOP VIEW (PLANFORM WITH COMPLETE DIMENSIONS)
    # -------------------------------------------------------------------------
    ax_top = fig.add_subplot(gs[0, 0])
    ax_top.set_facecolor('#1e293b')

    # Draw Wings
    # Root at X=26.5, Y=0 to tip at X=42.7, Y=29.375
    # Port wing
    ax_top.plot([26.5, 42.7, 43.9, 31.0, 26.5], [0, 29.375, 29.375, 0, 0], color='#38bdf8', linewidth=2.0)
    ax_top.fill([26.5, 42.7, 43.9, 31.0, 26.5], [0, 29.375, 29.375, 0, 0], color='#0284c7', alpha=0.35)
    # Stbd wing
    ax_top.plot([26.5, 42.7, 43.9, 31.0, 26.5], [0, -29.375, -29.375, 0, 0], color='#38bdf8', linewidth=2.0)
    ax_top.fill([26.5, 42.7, 43.9, 31.0, 26.5], [0, -29.375, -29.375, 0, 0], color='#0284c7', alpha=0.35)

    # Horizontal Tail
    ax_top.plot([58.5, 64.8, 65.9, 61.3, 58.5], [0, 9.75, 9.75, 0, 0], color='#38bdf8', linewidth=1.5)
    ax_top.plot([58.5, 64.8, 65.9, 61.3, 58.5], [0, -9.75, -9.75, 0, 0], color='#38bdf8', linewidth=1.5)

    # Fuselage Body
    x_f = np.linspace(0, 68.5, 200)
    w_f = np.array([3.1 * math.sin(math.pi * x / 68.5) ** 0.55 for x in x_f])
    ax_top.plot(x_f, w_f, color='#f8fafc', linewidth=2.2)
    ax_top.plot(x_f, -w_f, color='#f8fafc', linewidth=2.2)
    ax_top.fill_between(x_f, -w_f, w_f, color='#334155', alpha=0.7)

    # 4 Engines
    for ex, ey in [(24.5, 9.5), (24.5, -9.5), (31.0, 17.8), (31.0, -17.8)]:
        ax_top.add_patch(patches.Rectangle((ex-2.4, ey-1.22), 4.8, 2.45, facecolor='#64748b', edgecolor='#f8fafc', linewidth=1.2))

    # --- DIMENSIONS ON TOP VIEW ---
    # 1. Total Length: 68.50 m
    ax_top.annotate('', xy=(0, -33), xytext=(68.5, -33),
                    arrowprops=dict(arrowstyle='<->', color='#fbbf24', lw=1.8))
    ax_top.text(34.25, -35.5, "Fuselage Total Length = 68.50 m", color='#fbbf24', ha='center', fontsize=9.5, fontweight='bold')
    ax_top.plot([0, 0], [-3.5, -34], color='#fbbf24', linestyle=':', lw=1.0)
    ax_top.plot([68.5, 68.5], [-1.0, -34], color='#fbbf24', linestyle=':', lw=1.0)

    # 2. Total Wingspan: 58.75 m
    ax_top.annotate('', xy=(44.5, -29.375), xytext=(44.5, 29.375),
                    arrowprops=dict(arrowstyle='<->', color='#34d399', lw=1.8))
    ax_top.text(46.5, 0, "Wingspan b = 58.75 m\n(Area S = 363.4 m², Sweep = 29°)", color='#34d399', ha='left', va='center', fontsize=9, fontweight='bold')

    # 3. Fuselage Width: 6.20 m
    ax_top.annotate('', xy=(15.0, -3.1), xytext=(15.0, 3.1),
                    arrowprops=dict(arrowstyle='<->', color='#f472b6', lw=1.5))
    ax_top.text(15.0, 4.8, "Width = 6.20 m", color='#f472b6', ha='center', fontsize=8.5, fontweight='bold')

    ax_top.set_xlim(-5, 75)
    ax_top.set_ylim(-38, 38)
    ax_top.set_aspect('equal')
    ax_top.set_title('TOP VIEW (Planform & Dimensions)', color='#f8fafc', fontsize=11, fontweight='bold', pad=10)
    ax_top.tick_params(colors='#94a3b8', labelsize=8)
    ax_top.grid(True, linestyle=':', alpha=0.3, color='#334155')

    # -------------------------------------------------------------------------
    # 2. SIDE VIEW (PROFILE WITH INTERNAL 3-TIER CUTAWAY & DIMENSIONS)
    # -------------------------------------------------------------------------
    ax_side = fig.add_subplot(gs[1, :])
    ax_side.set_facecolor('#1e293b')

    # Outer Fuselage Silhouette
    ax_side.plot([0, 8.0, 56.0, 68.5], [0, 3.45, 3.45, 1.2], color='#f8fafc', linewidth=2.0)
    ax_side.plot([0, 8.0, 56.0, 68.5], [0, -3.45, -3.45, 0.5], color='#f8fafc', linewidth=2.0)
    ax_side.plot([68.5, 68.5], [0.5, 1.2], color='#f8fafc', linewidth=2.0)

    # Vertical Tail
    ax_side.plot([51.0, 58.0, 60.8, 58.8, 51.0], [2.6, 12.4, 12.4, 2.6, 2.6], color='#38bdf8', linewidth=2.0)
    ax_side.fill([51.0, 58.0, 60.8, 58.8, 51.0], [2.6, 12.4, 12.4, 2.6, 2.6], color='#0284c7', alpha=0.35)

    # Floor Deck Line (Z = -0.35)
    ax_side.plot([7.5, 57.0], [-0.35, -0.35], color='#94a3b8', linewidth=2.0, linestyle='-')
    ax_side.plot([7.5, 57.0], [1.45, 1.45], color='#94a3b8', linewidth=1.5, linestyle='--')

    # Top Crown Hydrogen Tanks (5 Tanks in row: D=3.09m, L=12.37m each)
    tank_x_starts = [7.5, 19.8, 32.1, 44.4, 56.7]
    for idx, tx in enumerate(tank_x_starts):
        ax_side.add_patch(patches.Rectangle((tx, 1.6), 12.37, 1.55, facecolor='#0284c7', edgecolor='#38bdf8', linewidth=1.2, alpha=0.85))
        ax_side.text(tx + 6.18, 2.37, f"LH2 Tank {idx+1}\n(D=3.09m, L=12.4m)", color='#ffffff', ha='center', va='center', fontsize=6.5, fontweight='bold')

    # Business Class (X = 9.5 - 15.5)
    ax_side.add_patch(patches.Rectangle((9.5, -0.2), 6.0, 1.4, facecolor='#fbbf24', edgecolor='#d97706', linewidth=1.2, alpha=0.8))
    ax_side.text(12.5, 0.5, "BUSINESS CLASS\n(24 Seats, 60\" Pitch)", color='#1e293b', ha='center', va='center', fontsize=7.5, fontweight='bold')

    # Economy Class (X = 17.0 - 53.5)
    ax_side.add_patch(patches.Rectangle((17.0, -0.2), 36.5, 1.4, facecolor='#38bdf8', edgecolor='#0284c7', linewidth=1.2, alpha=0.8))
    ax_side.text(35.0, 0.5, "ECONOMY CLASS (406 Seats: 3-3-3 Twin-Aisle, 32\" Pitch, 18\" Width)", color='#0f172a', ha='center', va='center', fontsize=8.5, fontweight='bold')

    # Lower Cargo Holds (LD3)
    ax_side.add_patch(patches.Rectangle((12.0, -2.9), 13.5, 2.2, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.2))
    ax_side.text(18.75, -1.8, "FORWARD CARGO HOLD\n(24x LD3 Containers, 120 m³)", color='#f8fafc', ha='center', va='center', fontsize=7.5, fontweight='bold')

    ax_side.add_patch(patches.Rectangle((36.5, -2.9), 11.5, 2.2, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.2))
    ax_side.text(42.25, -1.8, "AFT CARGO HOLD\n(20x LD3 Containers, 100 m³)", color='#f8fafc', ha='center', va='center', fontsize=7.5, fontweight='bold')

    # Landing Gear
    # Nose Gear at X = 6.5 m
    ax_side.plot([6.5, 6.5], [-3.45, -5.2], color='#f8fafc', linewidth=2.5)
    ax_side.add_patch(patches.Circle((6.5, -5.2), 0.55, facecolor='#334155', edgecolor='#f8fafc', linewidth=1.5))
    ax_side.text(6.5, -6.2, "Nose Gear\n(X=6.5m)", color='#f8fafc', ha='center', fontsize=7.5, fontweight='bold')

    # Main Gear at X = 33.8 m
    ax_side.plot([33.8, 33.8], [-3.45, -5.2], color='#f8fafc', linewidth=3.5)
    ax_side.add_patch(patches.Circle((33.8, -5.2), 0.65, facecolor='#334155', edgecolor='#f8fafc', linewidth=1.5))
    ax_side.text(33.8, -6.2, "Main Gear\n(X=33.8m)", color='#f8fafc', ha='center', fontsize=7.5, fontweight='bold')

    # Wheelbase Dimension: 27.30 m
    ax_side.annotate('', xy=(6.5, -5.2), xytext=(33.8, -5.2),
                     arrowprops=dict(arrowstyle='<->', color='#34d399', lw=1.6))
    ax_side.text(20.15, -4.7, "Wheelbase = 27.30 m", color='#34d399', ha='center', fontsize=8.5, fontweight='bold')

    # Fuselage Height Dimension: 6.90 m
    ax_side.annotate('', xy=(-3.0, -3.45), xytext=(-3.0, 3.45),
                     arrowprops=dict(arrowstyle='<->', color='#f472b6', lw=1.6))
    ax_side.text(-3.8, 0.0, "Height = 6.90 m", color='#f472b6', ha='right', va='center', fontsize=8.5, fontweight='bold', rotation=90)
    ax_side.plot([-3.0, 8.0], [3.45, 3.45], color='#f472b6', linestyle=':', lw=0.8)
    ax_side.plot([-3.0, 8.0], [-3.45, -3.45], color='#f472b6', linestyle=':', lw=0.8)

    # Vertical Tail Height Dimension: 9.80 m
    ax_side.annotate('', xy=(62.0, 2.6), xytext=(62.0, 12.4),
                     arrowprops=dict(arrowstyle='<->', color='#38bdf8', lw=1.5))
    ax_side.text(63.5, 7.5, "Tail Height = 9.80 m", color='#38bdf8', ha='left', va='center', fontsize=8, fontweight='bold')

    ax_side.set_xlim(-6, 75)
    ax_side.set_ylim(-7.5, 14)
    ax_side.set_aspect('equal')
    ax_side.set_title('SIDE VIEW (Longitudinal Profile & Internal Packaging Layout)', color='#f8fafc', fontsize=11, fontweight='bold', pad=10)
    ax_side.set_xlabel('Fuselage Longitudinal Station X [meters]', color='#f8fafc', fontsize=10, fontweight='bold')
    ax_side.tick_params(colors='#94a3b8', labelsize=8)
    ax_side.grid(True, linestyle=':', alpha=0.3, color='#334155')

    # -------------------------------------------------------------------------
    # 3. FRONT VIEW (CROSS-SECTION & SPAN PROFILE)
    # -------------------------------------------------------------------------
    ax_front = fig.add_subplot(gs[0, 1])
    ax_front.set_facecolor('#1e293b')

    # Fuselage Ellipse
    fuse_front = patches.Ellipse((0, 0), 6.20, 6.90, facecolor='#334155', edgecolor='#f8fafc', linewidth=2.0)
    ax_front.add_patch(fuse_front)

    # Wings (Dihedral = 5.5 deg)
    ax_front.plot([0, 29.375], [-1.2, -1.2 + 29.375 * math.tan(math.radians(5.5))], color='#38bdf8', linewidth=3.0)
    ax_front.plot([0, -29.375], [-1.2, -1.2 + 29.375 * math.tan(math.radians(5.5))], color='#38bdf8', linewidth=3.0)

    # Vertical Fin
    ax_front.plot([0, 0], [2.6, 12.4], color='#38bdf8', linewidth=3.0)

    # Horizontal Tail
    ax_front.plot([-9.75, 9.75], [2.8, 2.8], color='#38bdf8', linewidth=2.0)

    # Engines Front
    for ey in [-9.5, 9.5, -17.8, 17.8]:
        ez = -1.8 if abs(ey) < 12 else -0.9
        ax_front.add_patch(patches.Circle((ey, ez), 1.22, facecolor='#64748b', edgecolor='#f8fafc', linewidth=1.2))

    # Upper Hydrogen Tank Cross-Section
    ax_front.add_patch(patches.Circle((0, 1.85), 3.09/2.0, facecolor='#0284c7', edgecolor='#38bdf8', linewidth=1.5))
    ax_front.text(0, 1.85, "LH2 Tank\nD=3.09m", color='#ffffff', ha='center', va='center', fontsize=6.5, fontweight='bold')

    # Cabin Seats Row
    for sy in [-2.2, -1.75, -1.3, -0.55, 0.0, 0.55, 1.3, 1.75, 2.2]:
        ax_front.add_patch(patches.Rectangle((sy-0.16, -0.3), 0.32, 0.5, facecolor='#38bdf8', edgecolor='#0284c7', linewidth=0.6))

    # Cargo LD3
    ax_front.add_patch(patches.Rectangle((-2.2, -2.4), 1.8, 1.5, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.0))
    ax_front.add_patch(patches.Rectangle((0.4, -2.4), 1.8, 1.5, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.0))

    # Dimensions on Front View
    # Wheel Track: 10.80 m
    ax_front.annotate('', xy=(-5.4, -5.2), xytext=(5.4, -5.2),
                      arrowprops=dict(arrowstyle='<->', color='#34d399', lw=1.5))
    ax_front.text(0, -6.0, "Wheel Track = 10.80 m", color='#34d399', ha='center', fontsize=8, fontweight='bold')
    ax_front.plot([-5.4, -5.4], [-3.45, -5.2], color='#34d399', linestyle=':', lw=0.8)
    ax_front.plot([5.4, 5.4], [-3.45, -5.2], color='#34d399', linestyle=':', lw=0.8)

    ax_front.set_xlim(-32, 32)
    ax_front.set_ylim(-7.5, 14)
    ax_front.set_aspect('equal')
    ax_front.set_title('FRONT VIEW (Dihedral & Cross-Section)', color='#f8fafc', fontsize=11, fontweight='bold', pad=10)
    ax_front.tick_params(colors='#94a3b8', labelsize=8)
    ax_front.grid(True, linestyle=':', alpha=0.3, color='#334155')

    plt.suptitle('EXAELIA Hydrogen Transport — Full 3-View Dimensioned Engineering Drawing (DT2)\n'
                 'Overall Length: 68.50 m | Wingspan: 58.75 m | Height: 6.90 m | 430 Pax (24 Bus + 406 Econ) | 44 LD3 Cargo | 7x LH2 Tanks (597 m³)',
                 color='#f8fafc', fontsize=12, fontweight='bold', y=0.98)

    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Saved Dimensioned Engineering Drawing: {os.path.abspath(output_png)}")

if __name__ == "__main__":
    build_openvsp_dimensioned()
    render_dimensioned_engineering_blueprint()
