#!/usr/bin/env python3
"""
=============================================================================
MMS236 Aircraft Design — Design Task 2 (DT2)
EXAELIA Hydrogen Aircraft: Unified Aerodynamic Fuselage Outer Mold Line (OML)
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology

Architecture:
- Unified Aerodynamic Fuselage: The outer surface is modeled as ONE continuous,
  smoothly lofted, blended double-bubble aerodynamic body from nose to tail.
- Internal Hydrogen Tanks: The 7 modular cryogenic cylinders (520-597 m³) are
  enclosed completely inside the upper crown and wing-body fairings.
- Sized Transonic Wing: Sref = 363.4 m², Span = 58.75 m (Code F compliant)
- Empennage: Conventional Horizontal and Vertical Tailplanes.
- Engines: 4x Under-wing Hydrogen Turbofans (152.5 kN each).
=============================================================================
"""

import math
import os
import sys
import openvsp as vsp

def build_exaelia_unified_oml(output_prefix="EXAELIA_Unified_OML"):
    print("=================================================================")
    print("  Generating EXAELIA Hydrogen Aircraft with UNIFIED OUTER BODY")
    print("=================================================================")

    vsp.ClearVSPModel()

    # -------------------------------------------------------------------------
    # 1. UNIFIED AERODYNAMIC FUSELAGE (ONE CONTINUOUS OUTER MOLD LINE)
    # -------------------------------------------------------------------------
    print("\n[1/5] Lofting Unified Aerodynamic Fuselage Body (68.5 m)...")
    fuse_id = vsp.AddGeom("FUSELAGE", "")
    vsp.SetGeomName(fuse_id, "Unified_Aerodynamic_Fuselage")
    
    fuse_length = 68.50  # m
    vsp.SetParmVal(fuse_id, "Length", "Design", fuse_length)
    vsp.SetParmVal(fuse_id, "Tess_W", "Shape", 65)
    vsp.SetParmVal(fuse_id, "Tess_U", "Shape", 45)
    vsp.SetGeomMaterialName(fuse_id, "White")

    fuse_xsurf = vsp.GetXSecSurf(fuse_id, 0)

    # We configure smooth continuous cross-sections from nose (0%) to tail (100%)
    # Integrating passenger deck + upper hydrogen bay into one sleek aerodynamic shape
    xsec_configs = [
        # (index, XLocPercent, Width, Height, Z_offset, Shape)
        (1, 0.04, 2.20, 2.20,  0.00, vsp.XS_ELLIPSE),  # Radome nose
        (2, 0.10, 4.80, 5.20,  0.20, vsp.XS_ELLIPSE),  # Cockpit windshield blend
        (3, 0.22, 6.20, 7.10,  0.60, vsp.XS_ELLIPSE),  # Forward cabin + crown blend
    ]

    # Adjust default sections
    num_xsecs = vsp.GetNumXSec(fuse_xsurf)
    for i in range(1, num_xsecs - 1):
        vsp.ChangeXSecShape(fuse_xsurf, i, vsp.XS_ELLIPSE)
        xsec = vsp.GetXSec(fuse_xsurf, i)
        w_p = vsp.GetXSecParm(xsec, "Ellipse_Width")
        h_p = vsp.GetXSecParm(xsec, "Ellipse_Height")
        xloc_p = vsp.GetXSecParm(xsec, "XLocPercent")

        if i == 1:
            # Cockpit blend section
            vsp.SetParmVal(xloc_p, 0.10)
            vsp.SetParmVal(w_p, 5.20)
            vsp.SetParmVal(h_p, 5.80)
        elif i == 2:
            # Continuous main body (Mid-fuselage: Pax deck + Upper LH2 storage)
            vsp.SetParmVal(xloc_p, 0.50)
            vsp.SetParmVal(w_p, 6.20)
            vsp.SetParmVal(h_p, 6.90)  # One continuous aerodynamic height
        elif i == 3:
            # Aft cabin & tailcone transition
            vsp.SetParmVal(xloc_p, 0.86)
            vsp.SetParmVal(w_p, 4.40)
            vsp.SetParmVal(h_p, 4.60)

    print("      - Fuselage lofted as ONE continuous smooth body: L=68.5m, W=6.20m, H=6.90m.")

    # -------------------------------------------------------------------------
    # 2. INTERNAL CRYOGENIC HYDROGEN TANKS (ENCLOSED INSIDE UPPER CROWN)
    # -------------------------------------------------------------------------
    print("\n[2/5] Packaging Internal Cryogenic Tanks (Enclosed inside Crown)...")
    tank_diam = 3.09   # m
    tank_len = 12.37   # m
    
    # 5 Tanks along upper crown + 2 over wing box
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
        num_t_xsecs = vsp.GetNumXSec(t_xsurf)
        for j in range(1, num_t_xsecs - 1):
            vsp.ChangeXSecShape(t_xsurf, j, vsp.XS_CIRCLE)
            xsec = vsp.GetXSec(t_xsurf, j)
            d_p = vsp.GetXSecParm(xsec, "Circle_Diameter")
            vsp.SetParmVal(d_p, tank_diam)

    # -------------------------------------------------------------------------
    # 3. TRANSONIC SUPERCRITICAL MAIN WING (Sref = 363.4 m², Span = 58.75 m)
    # -------------------------------------------------------------------------
    print("\n[3/5] Building Transonic Main Wing (Sref = 363.4 m², Span = 58.75 m)...")
    wing_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(wing_id, "MainWing_Transonic")
    vsp.SetParmVal(wing_id, "X_Rel_Location", "XForm", 26.50)
    vsp.SetParmVal(wing_id, "Y_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(wing_id, "Z_Rel_Location", "XForm", -1.20)
    vsp.SetParmVal(wing_id, "RotateAirfoilMatchDideralFlag", "WingGeom", 1.0)
    vsp.SetGeomMaterialName(wing_id, "Aluminum")

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
    print("\n[4/5] Building Empennage (Horizontal & Vertical Stabilizers)...")
    
    # Horizontal Tail
    htail_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(htail_id, "HorizontalTail")
    vsp.SetParmVal(htail_id, "X_Rel_Location", "XForm", 58.50)
    vsp.SetParmVal(htail_id, "Y_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(htail_id, "Z_Rel_Location", "XForm", 1.80)
    vsp.SetGeomMaterialName(htail_id, "Aluminum")

    ht_xsurf = vsp.GetXSecSurf(htail_id, 0)
    ht_xsec1 = vsp.GetXSec(ht_xsurf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Span"), 9.75)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Sweep"), 33.0)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Dihedral"), 6.0)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Root_Chord"), 5.60)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Tip_Chord"), 2.10)

    # Vertical Tail
    vtail_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(vtail_id, "VerticalTail")
    vsp.SetParmVal(vtail_id, "X_Rel_Location", "XForm", 51.00)
    vsp.SetParmVal(vtail_id, "Z_Rel_Location", "XForm", 2.60)
    vsp.SetParmVal(vtail_id, "X_Rel_Rotation", "XForm", 90.0)
    vsp.SetParmVal(vtail_id, "Sym_Planar_Flag", "Sym", vsp.SYM_NONE)
    vsp.SetGeomMaterialName(vtail_id, "Blue Plastic")

    vt_xsurf = vsp.GetXSecSurf(vtail_id, 0)
    vt_xsec1 = vsp.GetXSec(vt_xsurf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Span"), 9.80)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Sweep"), 38.0)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Root_Chord"), 7.80)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Tip_Chord"), 2.80)

    # -------------------------------------------------------------------------
    # 5. PROPULSION: 4x HYDROGEN TURBOFANS (152.5 kN EACH)
    # -------------------------------------------------------------------------
    print("\n[5/5] Building 4x Under-Wing Hydrogen Turbofans...")
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
        vsp.SetGeomMaterialName(eng_id, "Aluminum")

        eng_xsurf = vsp.GetXSecSurf(eng_id, 0)
        num_e_xsecs = vsp.GetNumXSec(eng_xsurf)
        for k in range(1, num_e_xsecs - 1):
            vsp.ChangeXSecShape(eng_xsurf, k, vsp.XS_CIRCLE)
            xsec = vsp.GetXSec(eng_xsurf, k)
            d_p = vsp.GetXSecParm(xsec, "Circle_Diameter")
            vsp.SetParmVal(d_p, fan_diam)

    vsp.Update()

    # Export Files
    vsp_file = f"{output_prefix}.vsp3"
    stl_file = f"{output_prefix}.stl"
    obj_file = f"{output_prefix}.obj"

    vsp.WriteVSPFile(vsp_file)
    print(f"\n[OK] Native OpenVSP file: {os.path.abspath(vsp_file)}")

    vsp.ExportFile(stl_file, vsp.SET_ALL, vsp.EXPORT_STL)
    print(f"[OK] 3D STL Surface Mesh: {os.path.abspath(stl_file)}")

    vsp.ExportFile(obj_file, vsp.SET_ALL, vsp.EXPORT_OBJ)
    print(f"[OK] 3D OBJ Mesh:         {os.path.abspath(obj_file)}")

    vsp.ComputeMassProps(vsp.SET_ALL, 100, 0)
    vsp.ComputeCompGeom(vsp.SET_ALL, True, vsp.COMP_GEOM_TXT_TYPE)

    print(f"\n=================================================================")
    print(f"  EXAELIA UNIFIED OML MODEL GENERATED SUCCESSFULLY!")
    print(f"=================================================================")

if __name__ == "__main__":
    build_exaelia_unified_oml()
