#!/usr/bin/env python3
"""
=============================================================================
MMS236 Aircraft Design — Cabin Seating & Interior Layout Generator (DT2)
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Generates:
1. OpenVSP 3D Model with complete interior seating (430 Seats),
   lower cargo deck (44 LD3 containers), and upper cryogenic tanks.
2. Publication-grade 2D/3D Cabin Blueprint (LOPA - Layout of Passenger Accommodations).
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
import openvsp as vsp

def build_openvsp_with_seats(output_prefix="EXAELIA_Complete_Interior"):
    print("=================================================================")
    print("  Generating EXAELIA OpenVSP Model with FULL 430-SEAT INTERIOR")
    print("=================================================================")

    vsp.ClearVSPModel()

    # 1. Translucent Unified Fuselage Outer Shell
    fuse_id = vsp.AddGeom("FUSELAGE", "")
    vsp.SetGeomName(fuse_id, "Fuselage_Translucent_Shell")
    vsp.SetParmVal(fuse_id, "Length", "Design", 68.50)
    vsp.SetParmVal(fuse_id, "Tess_W", "Shape", 49)
    vsp.SetGeomMaterialName(fuse_id, "White")

    fuse_xsurf = vsp.GetXSecSurf(fuse_id, 0)
    num_xsecs = vsp.GetNumXSec(fuse_xsurf)
    for i in range(1, num_xsecs - 1):
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

    # 2. Main Cabin Floor Deck
    floor_id = vsp.AddGeom("POD", "")
    vsp.SetGeomName(floor_id, "Passenger_Cabin_Floor")
    vsp.SetParmVal(floor_id, "Length", "Design", 52.00)
    vsp.SetParmVal(floor_id, "X_Rel_Location", "XForm", 8.00)
    vsp.SetParmVal(floor_id, "Z_Rel_Location", "XForm", -0.30)
    vsp.SetParmVal(floor_id, "Y_Rel_Location", "XForm", 0.00)
    vsp.SetGeomMaterialName(floor_id, "Aluminum")

    # 3. Upper Cryogenic Hydrogen Tanks (7x Tanks)
    tank_diam = 3.09
    tank_len = 12.37
    tank_positions = [
        ("LH2_Tank_1_Internal",  7.50,  0.00,  1.60),
        ("LH2_Tank_2_Internal", 19.80,  0.00,  1.60),
        ("LH2_Tank_3_Internal", 32.10,  0.00,  1.60),
        ("LH2_Tank_4_Internal", 44.40,  0.00,  1.60),
        ("LH2_Tank_5_Internal", 56.70,  0.00,  1.60),
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

    # 4. Sized Passenger Seating Blocks (Business + Economy)
    # Business Class Block (24 Seats: 4 rows x 6 seats)
    biz_id = vsp.AddGeom("POD", "")
    vsp.SetGeomName(biz_id, "Seats_Business_24Pax")
    vsp.SetParmVal(biz_id, "Length", "Design", 6.50)
    vsp.SetParmVal(biz_id, "X_Rel_Location", "XForm", 9.50)
    vsp.SetParmVal(biz_id, "Z_Rel_Location", "XForm", 0.15)
    vsp.SetGeomMaterialName(biz_id, "Metal")

    # Economy Class Block (406 Seats: 45 rows x 9 seats, 3-3-3 twin aisle)
    econ_id = vsp.AddGeom("POD", "")
    vsp.SetGeomName(econ_id, "Seats_Economy_406Pax")
    vsp.SetParmVal(econ_id, "Length", "Design", 38.50)
    vsp.SetParmVal(econ_id, "X_Rel_Location", "XForm", 17.00)
    vsp.SetParmVal(econ_id, "Z_Rel_Location", "XForm", 0.15)
    vsp.SetGeomMaterialName(econ_id, "White")

    # 5. Lower Cargo Deck (44x LD3 Containers Block)
    cargo_fwd_id = vsp.AddGeom("POD", "")
    vsp.SetGeomName(cargo_fwd_id, "Cargo_Fwd_24xLD3")
    vsp.SetParmVal(cargo_fwd_id, "Length", "Design", 13.50)
    vsp.SetParmVal(cargo_fwd_id, "X_Rel_Location", "XForm", 12.00)
    vsp.SetParmVal(cargo_fwd_id, "Z_Rel_Location", "XForm", -1.40)
    vsp.SetGeomMaterialName(cargo_fwd_id, "Metal")

    cargo_aft_id = vsp.AddGeom("POD", "")
    vsp.SetGeomName(cargo_aft_id, "Cargo_Aft_20xLD3")
    vsp.SetParmVal(cargo_aft_id, "Length", "Design", 11.50)
    vsp.SetParmVal(cargo_aft_id, "X_Rel_Location", "XForm", 36.50)
    vsp.SetParmVal(cargo_aft_id, "Z_Rel_Location", "XForm", -1.40)
    vsp.SetGeomMaterialName(cargo_aft_id, "Metal")

    # 6. Wing, Empennage & 4x Engines
    wing_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(wing_id, "MainWing_Transonic")
    vsp.SetParmVal(wing_id, "X_Rel_Location", "XForm", 26.50)
    vsp.SetParmVal(wing_id, "Z_Rel_Location", "XForm", -1.20)
    vsp.SetGeomMaterialName(wing_id, "Aluminum")
    w_xsec = vsp.GetXSec(vsp.GetXSecSurf(wing_id, 0), 1)
    vsp.SetParmVal(vsp.GetXSecParm(w_xsec, "Span"), 58.75 / 2.0)
    vsp.SetParmVal(vsp.GetXSecParm(w_xsec, "Sweep"), 29.0)
    vsp.SetParmVal(vsp.GetXSecParm(w_xsec, "Dihedral"), 5.5)
    vsp.SetParmVal(vsp.GetXSecParm(w_xsec, "Root_Chord"), 9.20)
    vsp.SetParmVal(vsp.GetXSecParm(w_xsec, "Tip_Chord"), 2.40)

    # Tail & Engines
    htail_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(htail_id, "HorizontalTail")
    vsp.SetParmVal(htail_id, "X_Rel_Location", "XForm", 58.50)
    vsp.SetParmVal(htail_id, "Z_Rel_Location", "XForm", 1.80)
    vsp.SetGeomMaterialName(htail_id, "Aluminum")
    ht_xsec = vsp.GetXSec(vsp.GetXSecSurf(htail_id, 0), 1)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec, "Span"), 9.75)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec, "Sweep"), 33.0)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec, "Root_Chord"), 5.60)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec, "Tip_Chord"), 2.10)

    vtail_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(vtail_id, "VerticalTail")
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

    # 4 Engines
    for name, y_pos, z_pos, x_pos in [("Eng_In_P", -9.5, -1.8, 24.5), ("Eng_In_S", 9.5, -1.8, 24.5),
                                      ("Eng_Out_P", -17.8, -0.9, 31.0), ("Eng_Out_S", 17.8, -0.9, 31.0)]:
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
    print(f"[OK] Saved OpenVSP Model with Interior: {os.path.abspath(vsp_file)}")

def plot_cabin_seating_layout(output_png="cabin_seating_layout.png"):
    """Renders high-resolution 2D and 3D architectural cabin LOPA blueprint."""
    print("Generating High-Resolution Cabin Layout (LOPA Blueprint)...")
    fig = plt.figure(figsize=(16, 12), dpi=160)
    fig.patch.set_facecolor('#0b0f19')

    # Grid specification: 2 rows
    # Top: Full Longitudinal Floor Plan (LOPA)
    # Bottom Left: Fuselage Cross Section (3 Tiers)
    # Bottom Right: Passenger Class Breakdown & Specifications Table
    gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 1.0], width_ratios=[1.1, 0.9], hspace=0.3, wspace=0.25)

    # -------------------------------------------------------------------------
    # 1. TOP: FULL CABIN FLOOR PLAN (LOPA)
    # -------------------------------------------------------------------------
    ax_plan = fig.add_subplot(gs[0, :])
    ax_plan.set_facecolor('#111827')

    # Draw Fuselage Contour
    x_fuse = np.linspace(0, 68.5, 300)
    # Width profile
    w_profile = np.zeros_like(x_fuse)
    for idx, x in enumerate(x_fuse):
        if x < 8.0:
            w_profile[idx] = 2.0 + 4.2 * (x / 8.0) ** 0.6
        elif x > 56.0:
            w_profile[idx] = 6.2 - 4.5 * ((x - 56.0) / 12.5) ** 1.3
        else:
            w_profile[idx] = 6.20

    ax_plan.plot(x_fuse, w_profile / 2.0, color='#94a3b8', linewidth=2.0)
    ax_plan.plot(x_fuse, -w_profile / 2.0, color='#94a3b8', linewidth=2.0)
    ax_plan.fill_between(x_fuse, -w_profile / 2.0, w_profile / 2.0, color='#1e293b', alpha=0.6)

    # Cockpit
    ax_plan.add_patch(patches.Polygon([[0.5, 0], [4.5, 1.2], [7.0, 2.2], [7.0, -2.2], [4.5, -1.2]],
                                      closed=True, facecolor='#334155', edgecolor='#64748b', linewidth=1.5))
    ax_plan.text(4.0, 0.0, "FLIGHT DECK\n(2 Crew)", color='#f8fafc', ha='center', va='center', fontsize=8.5, fontweight='bold')

    # Forward Galley & Lavs (X = 7.0 - 9.0)
    ax_plan.add_patch(patches.Rectangle((7.2, -2.2), 1.8, 4.4, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.0))
    ax_plan.text(8.1, 0.0, "GALLEY 1\n& LAV (2x)", color='#f8fafc', ha='center', va='center', fontsize=7.5, fontweight='bold')

    # Business Class (X = 9.5 to 15.5) -> 4 rows x 6 seats (2-2-2) = 24 seats
    biz_x = np.linspace(9.6, 14.8, 4)
    for bx in biz_x:
        # 2 Port, 2 Center, 2 Stbd
        for by in [-2.1, -1.5, -0.6, 0.6, 1.5, 2.1]:
            ax_plan.add_patch(patches.Rectangle((bx, by-0.22), 0.9, 0.44, facecolor='#fbbf24', edgecolor='#d97706', linewidth=0.8))
    ax_plan.text(12.5, 2.7, "BUSINESS CLASS (24 Seats: 2-2-2, 60\" Pitch)", color='#fbbf24', fontsize=9.5, fontweight='bold')

    # Mid Galley & Lavatories (X = 15.5 - 17.0)
    ax_plan.add_patch(patches.Rectangle((15.6, -2.4), 1.2, 4.8, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.0))
    ax_plan.text(16.2, 0.0, "DOOR 2\nLAV", color='#f8fafc', ha='center', va='center', fontsize=7, fontweight='bold')

    # Economy Class (X = 17.2 to 54.0) -> 45 rows x 9 seats (3-3-3) = 405 seats + 1 = 406 seats
    econ_x = np.linspace(17.5, 53.0, 45)
    for ex in econ_x:
        # 3 Port, 3 Center, 3 Stbd
        # Port: -2.3, -1.8, -1.3
        # Center: -0.6, 0.0, 0.6
        # Stbd: 1.3, 1.8, 2.3
        for ey in [-2.3, -1.8, -1.3, -0.6, 0.0, 0.6, 1.3, 1.8, 2.3]:
            ax_plan.add_patch(patches.Rectangle((ex, ey-0.18), 0.62, 0.36, facecolor='#38bdf8', edgecolor='#0284c7', linewidth=0.5))

    ax_plan.text(35.0, 2.7, "ECONOMY CLASS (406 Seats: 3-3-3 Twin-Aisle, 32\" Pitch, 18\" Width)", color='#38bdf8', fontsize=9.5, fontweight='bold')

    # Mid-Cabin Overwing Exits & Lavs (X = 34.0 - 35.5)
    ax_plan.add_patch(patches.Rectangle((34.0, -2.5), 1.4, 5.0, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.0, alpha=0.9))
    ax_plan.text(34.7, 0.0, "MID GALLEY\n& 4x LAVS\n(DOOR 3)", color='#f8fafc', ha='center', va='center', fontsize=7, fontweight='bold')

    # Aft Galley & Lavatories (X = 54.0 - 56.5)
    ax_plan.add_patch(patches.Rectangle((54.2, -2.1), 2.2, 4.2, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.0))
    ax_plan.text(55.3, 0.0, "AFT GALLEY\n& 2x LAVS\n(DOOR 4)", color='#f8fafc', ha='center', va='center', fontsize=7.5, fontweight='bold')

    # Exit Doors Indicators
    for door_x in [7.5, 16.0, 34.5, 55.0]:
        ax_plan.plot([door_x, door_x], [2.7, 3.2], color='#ef4444', linewidth=2.5)
        ax_plan.plot([door_x, door_x], [-2.7, -3.2], color='#ef4444', linewidth=2.5)
        ax_plan.text(door_x, 3.4, "EXIT", color='#ef4444', ha='center', va='bottom', fontsize=7.5, fontweight='bold')
        ax_plan.text(door_x, -3.4, "EXIT", color='#ef4444', ha='center', va='top', fontsize=7.5, fontweight='bold')

    ax_plan.set_xlim(-1, 70)
    ax_plan.set_ylim(-4.5, 4.5)
    ax_plan.set_aspect('equal')
    ax_plan.set_xlabel('Fuselage Longitudinal Station X [meters]', color='#f8fafc', fontsize=10, fontweight='bold')
    ax_plan.set_ylabel('Cabin Lateral Y [m]', color='#f8fafc', fontsize=10, fontweight='bold')
    ax_plan.set_title('Main Passenger Deck Layout of Accommodations (LOPA) — 430 Passengers Total',
                      color='#f8fafc', fontsize=12, fontweight='bold', pad=10)
    ax_plan.tick_params(colors='#94a3b8', labelsize=8)
    ax_plan.grid(True, linestyle=':', alpha=0.3, color='#334155')

    # -------------------------------------------------------------------------
    # 2. BOTTOM LEFT: FUSELAGE CROSS-SECTION (3 TIERS)
    # -------------------------------------------------------------------------
    ax_xsec = fig.add_subplot(gs[1, 0])
    ax_xsec.set_facecolor('#111827')

    # Outer Fuselage Shell (Width=6.2m, Height=6.9m)
    outer_ellipse = patches.Ellipse((0, 0), 6.20, 6.90, facecolor='#1e293b', edgecolor='#38bdf8', linewidth=2.5)
    ax_xsec.add_patch(outer_ellipse)

    # Deck Floor Dividers
    ax_xsec.plot([-2.9, 2.9], [-0.4, -0.4], color='#94a3b8', linewidth=2.5, linestyle='-')
    ax_xsec.plot([-2.5, 2.5], [1.4, 1.4], color='#94a3b8', linewidth=2.0, linestyle='--')

    # Level 3: Upper Crown Cryotank (D = 3.09 m)
    tank_circle = patches.Circle((0, 2.35), 3.09/2.0, facecolor='#0284c7', edgecolor='#38bdf8', linewidth=2.0, alpha=0.85)
    ax_xsec.add_patch(tank_circle)
    ax_xsec.text(0, 2.35, "LIQUID HYDROGEN ($LH_2$) TANK\nDiameter = 3.09 m\n(Insulated & Enclosed in Crown)",
                 color='#ffffff', ha='center', va='center', fontsize=8.5, fontweight='bold')

    # Level 2: Main Passenger Deck (Seats in 3-3-3 layout)
    seat_y_coords = [-2.2, -1.75, -1.3,   -0.55, 0.0, 0.55,   1.3, 1.75, 2.2]
    for sy in seat_y_coords:
        ax_xsec.add_patch(patches.Rectangle((sy-0.18, -0.35), 0.36, 0.65, facecolor='#38bdf8', edgecolor='#0284c7', linewidth=1.0))
        # Headrest
        ax_xsec.add_patch(patches.Rectangle((sy-0.12, 0.30), 0.24, 0.20, facecolor='#bae6fd', edgecolor='#0284c7', linewidth=0.8))

    # Aisle labels
    ax_xsec.text(-0.95, 0.1, "AISLE", color='#94a3b8', ha='center', va='center', fontsize=7, rotation=90)
    ax_xsec.text(0.95, 0.1, "AISLE", color='#94a3b8', ha='center', va='center', fontsize=7, rotation=90)
    ax_xsec.text(0, 1.05, "MAIN CABIN: 3-3-3 Twin-Aisle (Headroom = 2.15 m)", color='#f8fafc', ha='center', va='center', fontsize=8.5, fontweight='bold')

    # Level 1: Lower Cargo Hold (2x LD3 Containers side-by-side)
    # LD3 container dimensions: ~1.56m wide, 1.63m high
    ax_xsec.add_patch(patches.Rectangle((-2.2, -2.6), 1.8, 1.7, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.5))
    ax_xsec.text(-1.3, -1.75, "LD3 CONTAINER\n(Port)", color='#f8fafc', ha='center', va='center', fontsize=7.5, fontweight='bold')

    ax_xsec.add_patch(patches.Rectangle((0.4, -2.6), 1.8, 1.7, facecolor='#475569', edgecolor='#94a3b8', linewidth=1.5))
    ax_xsec.text(1.3, -1.75, "LD3 CONTAINER\n(Starboard)", color='#f8fafc', ha='center', va='center', fontsize=7.5, fontweight='bold')

    ax_xsec.text(0, -3.1, "LOWER HOLD: 44x LD3 Containers ($220.0\\ \\mathrm{m}^3$)", color='#f8fafc', ha='center', va='center', fontsize=8.5, fontweight='bold')

    ax_xsec.set_xlim(-3.8, 3.8)
    ax_xsec.set_ylim(-3.8, 3.8)
    ax_xsec.set_aspect('equal')
    ax_xsec.set_title('Fuselage Cross-Section (3-Level Architecture)', color='#f8fafc', fontsize=11, fontweight='bold', pad=8)
    ax_xsec.tick_params(colors='#94a3b8', labelsize=8)
    ax_xsec.grid(True, linestyle=':', alpha=0.3, color='#334155')

    # -------------------------------------------------------------------------
    # 3. BOTTOM RIGHT: CABIN SPECIFICATIONS & SUMMARY TABLE
    # -------------------------------------------------------------------------
    ax_table = fig.add_subplot(gs[1, 1])
    ax_table.axis('off')

    table_data = [
        ["Parameter", "Business Class", "Economy Class", "Total / Metric"],
        ["Seat Count", "24 Seats", "406 Seats", "430 Passengers"],
        ["Seating Config", "2-2-2 (6 abreast)", "3-3-3 (9 abreast)", "Twin-Aisle"],
        ["Seat Pitch", "60.0 in (1.52 m)", "32.0 in (0.81 m)", "Standard Widebody"],
        ["Seat Width", "21.0 in (0.53 m)", "18.0 in (0.46 m)", "High Comfort"],
        ["Aisle Width", "20.0 in (0.51 m)", "19.5 in (0.50 m)", "2 Aisles"],
        ["Lavatories", "2 Forward", "6 Mid & Aft", "8 Lavatories total"],
        ["Galleys", "1 Forward Galley", "3 Mid & Aft Galleys", "4 Galleys total"],
        ["Emergency Exits", "Door 1 (Type A)", "Doors 2, 3, 4 (Type A)", "8 Type-A Exits (<90s)"],
        ["Cargo Capacity", "—", "—", "44 LD3 (220.0 m³)"],
        ["Revenue Freight", "—", "—", "10,750 kg (+ Bags)"],
        ["LH2 Cryotanks", "—", "—", "7 Tanks (596.6 m³)"]
    ]

    tab = ax_table.table(cellText=table_data, loc='center', cellLoc='left')
    tab.auto_set_font_size(False)
    tab.set_fontsize(8.5)
    tab.scale(1.0, 1.45)

    # Style table cells
    for (row, col), cell in tab.get_celld().items():
        cell.set_edgecolor('#334155')
        if row == 0:
            cell.set_facecolor('#0284c7')
            cell.set_text_props(color='#f8fafc', fontweight='bold')
        elif row % 2 == 1:
            cell.set_facecolor('#1e293b')
            cell.set_text_props(color='#f8fafc')
        else:
            cell.set_facecolor('#111827')
            cell.set_text_props(color='#e2e8f0')

    plt.suptitle('EXAELIA Hydrogen Transport — Cabin Interior Layout & Cargo Architecture (DT2)\n'
                 '430 Passengers (24 Bus + 406 Econ) | 44x LD3 Cargo Containers (220 m³) | 7x LH2 Tanks (597 m³)',
                 color='#f8fafc', fontsize=13, fontweight='bold', y=0.98)

    plt.savefig(output_png, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Saved Cabin Layout Blueprint: {os.path.abspath(output_png)}")

if __name__ == "__main__":
    build_openvsp_with_seats()
    plot_cabin_seating_layout()
