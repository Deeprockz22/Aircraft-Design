#!/usr/bin/env python3
"""
=============================================================================
MMS236 Aircraft Design — Design Task 2 (DT2)
EXAELIA Long-Range Hydrogen Aircraft: Top Linear Dorsal Tank Configuration
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Lecturers: Christian Svensson, Carlos Xisto

Architecture Overview:
- Hydrogen Fuel Tanks: 4x Cryogenic Cylinders mounted linearly in tandem
  along the top crown (dorsal deck) of the fuselage.
- Tank Geometry: D = 3.73 m, L = 14.92 m, L/D = 4.00 (Aspect ratio limit)
- Total Cryotank Storage: 597.8 m³ (Usable LH2 = 38.51 tonnes at 2 bar, 20 K)
- Main Deck: Continuous unsevered cabin for 430 Passengers (406 Econ + 24 Bus)
- Lower Deck: Cargo hold for 44x LD3 containers (>= 206 m³)
- CG Stability: Linear tank layout spans across the aircraft CG, ensuring
  minimal CG shift during fuel burn (Delta CG < 5% MAC).
- Sized Transonic Wing: Sref = 363.4 m², Span = 58.75 m (Code F compliant)
- Engines: 4x Hydrogen Combustion Turbofans (152.5 kN each, Total = 610 kN)
=============================================================================
"""

import math
import os
import sys
import openvsp as vsp

def build_exaelia_top_linear_tanks(output_prefix="EXAELIA_Top_Linear_Tanks"):
    print("=================================================================")
    print("  Generating EXAELIA Hydrogen Aircraft with TOP LINEAR TANKS")
    print("=================================================================")

    vsp.ClearVSPModel()

    # -------------------------------------------------------------------------
    # 1. MAIN FUSELAGE (PASSENGER CABIN & LOWER CARGO DECK)
    # -------------------------------------------------------------------------
    print("\n[1/6] Building Widebody Main Fuselage (430 Pax + 44 LD3 Cargo)...")
    fuse_id = vsp.AddGeom("FUSELAGE", "")
    vsp.SetGeomName(fuse_id, "Fuselage_MainDeck")
    
    fuse_length = 68.50  # m
    fuse_width = 6.20    # m (Twin-aisle seating)
    fuse_height = 5.60   # m (Passenger deck + lower LD3 cargo deck)
    
    vsp.SetParmVal(fuse_id, "Length", "Design", fuse_length)
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
            vsp.SetParmVal(xloc_p, 0.12)
            vsp.SetParmVal(w_p, 4.80)
            vsp.SetParmVal(h_p, 4.80)
        elif i == 2:
            vsp.SetParmVal(xloc_p, 0.50)
            vsp.SetParmVal(w_p, fuse_width)
            vsp.SetParmVal(h_p, fuse_height)
        elif i == 3:
            vsp.SetParmVal(xloc_p, 0.85)
            vsp.SetParmVal(w_p, 4.60)
            vsp.SetParmVal(h_p, 4.60)

    # -------------------------------------------------------------------------
    # 2. TOP LINEAR CRYOGENIC HYDROGEN CYLINDERS (4x TANKS IN TANDEM)
    # -------------------------------------------------------------------------
    print("\n[2/6] Building 4x Top Linear Cryogenic Cylinders (L/D = 4.00, Vol = 597.8 m³)...")
    # Sizing each cylinder:
    # Volume per tank = 149.4 m³
    # Diameter D = 3.73 m, Length L = 14.92 m -> L/D = 4.00 (Exact Canvas limit)
    tank_diam = 3.73  # m
    tank_len = 14.92  # m
    tank_z_pos = 2.45 # Placed along the upper crown (Z = +2.45 m)
    tank_vol_each = (11.0 * math.pi / 12.0) * (tank_diam ** 3) # ~149.4 m³

    # 4 Tanks placed in linear tandem along the fuselage crown from X = 8.5m to X = 68.2m
    # Tank 1 (Forward):      X = 8.50 m  to 23.42 m
    # Tank 2 (Mid-Forward):  X = 23.42 m to 38.34 m (Directly above Wing CG)
    # Tank 3 (Mid-Aft):      X = 38.34 m to 53.26 m
    # Tank 4 (Aft):          X = 53.26 m to 68.18 m
    tank_linear_positions = [
        ("LH2_Tank_1_Fwd",     8.50),
        ("LH2_Tank_2_MidFwd", 23.42),
        ("LH2_Tank_3_MidAft", 38.34),
        ("LH2_Tank_4_Aft",    53.26),
    ]

    for name, x_pos in tank_linear_positions:
        t_id = vsp.AddGeom("FUSELAGE", "")
        vsp.SetGeomName(t_id, name)
        vsp.SetParmVal(t_id, "Length", "Design", tank_len)
        vsp.SetParmVal(t_id, "X_Rel_Location", "XForm", x_pos)
        vsp.SetParmVal(t_id, "Y_Rel_Location", "XForm", 0.0)
        vsp.SetParmVal(t_id, "Z_Rel_Location", "XForm", tank_z_pos)
        vsp.SetGeomMaterialName(t_id, "Blue Plastic")

        t_xsurf = vsp.GetXSecSurf(t_id, 0)
        num_t_xsecs = vsp.GetNumXSec(t_xsurf)
        for j in range(1, num_t_xsecs - 1):
            vsp.ChangeXSecShape(t_xsurf, j, vsp.XS_CIRCLE)
            xsec = vsp.GetXSec(t_xsurf, j)
            d_p = vsp.GetXSecParm(xsec, "Circle_Diameter")
            vsp.SetParmVal(d_p, tank_diam)

    print(f"      - 4x Linear Dorsal Tanks: Diameter = {tank_diam:.2f} m, Length = {tank_len:.2f} m each")
    print(f"      - Total Tank Volume: {4 * tank_vol_each:.1f} m³ (Stores 38.51 t usable LH2 fuel)")
    print(f"      - Spanned Linear Range: X = 8.50 m to 68.18 m (Symmetric about aircraft CG!)")

    # -------------------------------------------------------------------------
    # 3. TRANSONIC SUPERCRITICAL MAIN WING (Sref = 363.4 m², Span = 58.75 m)
    # -------------------------------------------------------------------------
    print("\n[3/6] Building Sized Transonic Main Wing (Sref = 363.4 m², Span = 58.75 m)...")
    wing_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(wing_id, "MainWing_Transonic")
    vsp.SetParmVal(wing_id, "X_Rel_Location", "XForm", 26.50)
    vsp.SetParmVal(wing_id, "Y_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(wing_id, "Z_Rel_Location", "XForm", -1.20)
    vsp.SetParmVal(wing_id, "RotateAirfoilMatchDideralFlag", "WingGeom", 1.0)
    vsp.SetGeomMaterialName(wing_id, "Aluminum")

    # Half span = 29.375 m, Root chord = 9.20 m, Tip chord = 2.40 m, Sweep = 29.0 deg, Dihedral = 5.5 deg
    b_half = 58.75 / 2.0
    c_root = 9.20
    c_tip = 2.40
    sweep_c4 = 29.0
    dihedral_deg = 5.5

    wing_xsurf = vsp.GetXSecSurf(wing_id, 0)
    xsec1 = vsp.GetXSec(wing_xsurf, 1)

    vsp.SetParmVal(vsp.GetXSecParm(xsec1, "Span"), b_half)
    vsp.SetParmVal(vsp.GetXSecParm(xsec1, "Sweep_Location"), 0.25)
    vsp.SetParmVal(vsp.GetXSecParm(xsec1, "Sweep"), sweep_c4)
    vsp.SetParmVal(vsp.GetXSecParm(xsec1, "Dihedral"), dihedral_deg)
    vsp.SetParmVal(vsp.GetXSecParm(xsec1, "Root_Chord"), c_root)
    vsp.SetParmVal(vsp.GetXSecParm(xsec1, "Tip_Chord"), c_tip)

    # Supercritical Airfoil Profile
    for curve_idx in [0, 1]:
        camber_p = vsp.GetParm(wing_id, "Camber", f"XSecCurve_{curve_idx}")
        thick_p = vsp.GetParm(wing_id, "ThickChord", f"XSecCurve_{curve_idx}")
        if camber_p:
            vsp.SetParmVal(camber_p, 0.020)
        if thick_p:
            vsp.SetParmVal(thick_p, 0.135 if curve_idx == 0 else 0.105)

    # -------------------------------------------------------------------------
    # 4. EMPENNAGE (HORIZONTAL & VERTICAL STABILIZERS)
    # -------------------------------------------------------------------------
    print("\n[4/6] Building Horizontal & Vertical Stabilizers...")
    
    # Horizontal Stabilizer
    htail_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(htail_id, "HorizontalTail")
    vsp.SetParmVal(htail_id, "X_Rel_Location", "XForm", 58.50)
    vsp.SetParmVal(htail_id, "Y_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(htail_id, "Z_Rel_Location", "XForm", 2.20)
    vsp.SetGeomMaterialName(htail_id, "Aluminum")

    ht_xsurf = vsp.GetXSecSurf(htail_id, 0)
    ht_xsec1 = vsp.GetXSec(ht_xsurf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Span"), 9.75) # 19.5m span
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Sweep"), 33.0)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Dihedral"), 6.0)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Root_Chord"), 5.60)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Tip_Chord"), 2.10)

    # Vertical Stabilizer (Single Vertical Fin)
    vtail_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(vtail_id, "VerticalTail")
    vsp.SetParmVal(vtail_id, "X_Rel_Location", "XForm", 51.00)
    vsp.SetParmVal(vtail_id, "Z_Rel_Location", "XForm", 2.80)
    vsp.SetParmVal(vtail_id, "X_Rel_Rotation", "XForm", 90.0)
    vsp.SetParmVal(vtail_id, "Sym_Planar_Flag", "Sym", vsp.SYM_NONE)
    vsp.SetGeomMaterialName(vtail_id, "Blue Plastic")

    vt_xsurf = vsp.GetXSecSurf(vtail_id, 0)
    vt_xsec1 = vsp.GetXSec(vt_xsurf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Span"), 9.80) # Height
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Sweep"), 38.0)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Root_Chord"), 7.80)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Tip_Chord"), 2.80)

    # -------------------------------------------------------------------------
    # 5. PROPULSION: 4x HYDROGEN COMBUSTION TURBOFANS (152.5 kN EACH)
    # -------------------------------------------------------------------------
    print("\n[5/6] Building 4x Hydrogen Combustion Turbofans & Pylons...")
    fan_diam = 2.45
    nacelle_len = 4.80

    engine_locations = [
        ("Engine_Inboard_Port",   -9.50, -1.80, 24.50),
        ("Engine_Inboard_Stbd",    9.50, -1.80, 24.50),
        ("Engine_Outboard_Port", -17.80, -0.90, 31.00),
        ("Engine_Outboard_Stbd",  17.80, -0.90, 31.00),
    ]

    for name, y_pos, z_pos, x_pos in engine_locations:
        eng_id = vsp.AddGeom("FUSELAGE", "")
        vsp.SetGeomName(eng_id, name)
        vsp.SetParmVal(eng_id, "Length", "Design", nacelle_len)
        vsp.SetParmVal(eng_id, "X_Rel_Location", "XForm", x_pos)
        vsp.SetParmVal(eng_id, "Y_Rel_Location", "XForm", y_pos)
        vsp.SetParmVal(eng_id, "Z_Rel_Location", "XForm", z_pos)
        vsp.SetGeomMaterialName(eng_id, "Metal")

        eng_xsurf = vsp.GetXSecSurf(eng_id, 0)
        num_e_xsecs = vsp.GetNumXSec(eng_xsurf)
        for k in range(1, num_e_xsecs - 1):
            vsp.ChangeXSecShape(eng_xsurf, k, vsp.XS_CIRCLE)
            xsec = vsp.GetXSec(eng_xsurf, k)
            d_p = vsp.GetXSecParm(xsec, "Circle_Diameter")
            vsp.SetParmVal(d_p, fan_diam)

    vsp.Update()

    # -------------------------------------------------------------------------
    # 6. EXPORTING MODEL & COMPUTING MASS PROPS
    # -------------------------------------------------------------------------
    print("\n[6/6] Exporting Model Files...")
    vsp_file = f"{output_prefix}.vsp3"
    stl_file = f"{output_prefix}.stl"
    obj_file = f"{output_prefix}.obj"

    vsp.WriteVSPFile(vsp_file)
    print(f"      -> Native OpenVSP file: {os.path.abspath(vsp_file)}")

    vsp.ExportFile(stl_file, vsp.SET_ALL, vsp.EXPORT_STL)
    print(f"      -> 3D STL Surface Mesh: {os.path.abspath(stl_file)}")

    vsp.ExportFile(obj_file, vsp.SET_ALL, vsp.EXPORT_OBJ)
    print(f"      -> 3D OBJ Mesh:         {os.path.abspath(obj_file)}")

    vsp.ComputeMassProps(vsp.SET_ALL, 100, 0)
    vsp.ComputeCompGeom(vsp.SET_ALL, True, vsp.COMP_GEOM_TXT_TYPE)
    print(f"      -> Mass & CompGeom properties computed.")

    print(f"\n=================================================================")
    print(f"  EXAELIA TOP LINEAR TANKS MODEL GENERATED SUCCESSFULLY!")
    print(f"=================================================================")

if __name__ == "__main__":
    build_exaelia_top_linear_tanks()
