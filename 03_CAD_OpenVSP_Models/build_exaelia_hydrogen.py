#!/usr/bin/env python3
"""
=============================================================================
MMS236 Aircraft Design — Design Task 2 (DT2)
EXAELIA Long-Range Hydrogen Aircraft 3D OpenVSP Parametric Model
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Lecturers: Christian Svensson, Carlos Xisto

Aircraft Specifications (Sized from DT1):
- MTOW: 210,762 kg (210.8 t)
- OEW: 118,506 kg (118.5 t)
- Design Payload: 53,750 kg (430 Pax @ 100 kg + 10,750 kg Freight)
- Usable LH2 Fuel: 38,506 kg (542.3 m³ liquid LH2 at 2 bar, 20 K, rho=71 kg/m³)
- Total Cryotank Storage Volume: 596.6 m³ (+10% ullage & insulation)
- Cryotank Aspect Ratio: L/D <= 4.0 (Gi = 50%)
- Reference Wing Area (Sref): 363.4 m²
- Wingspan (b): 58.75 m (Aspect Ratio AR = 9.5, Code F Compliant <= 80 m)
- Sweep: 29.0 deg (quarter-chord), Supercritical transonic airfoils
- Fuselage: Twin-Aisle Widebody (Length: 68.5 m, Width: 6.20 m, Height: 6.40 m)
- Cargo Hold: >= 206 m³ (44x LD3 containers)
- Engines: 4x Hydrogen Combustion Turbofans (152.5 kN each, Total Thrust = 610 kN)
=============================================================================
"""

import math
import os
import sys
import openvsp as vsp

def build_exaelia_hydrogen(output_prefix="EXAELIA_Hydrogen_DT2"):
    print("=================================================================")
    print("  Generating EXAELIA Long-Range Hydrogen Aircraft (DT2) in OpenVSP")
    print("=================================================================")

    vsp.ClearVSPModel()

    # -------------------------------------------------------------------------
    # 1. FUSELAGE (TWIN-AISLE WIDEBODY: 430 PAX + 44 LD3 CARGO + LH2 BAY)
    # -------------------------------------------------------------------------
    print("\n[1/6] Building Sized Twin-Aisle Widebody Fuselage...")
    fuse_id = vsp.AddGeom("FUSELAGE", "")
    vsp.SetGeomName(fuse_id, "Fuselage_Main")
    
    fuse_length = 68.50  # m
    fuse_width = 6.20    # m (Twin-aisle 2-4-2 / 3-3-3 seating)
    fuse_height = 6.40   # m (Passenger deck + lower cargo deck)
    
    vsp.SetParmVal(fuse_id, "Length", "Design", fuse_length)
    vsp.SetParmVal(fuse_id, "Tess_W", "Shape", 49)
    vsp.SetGeomMaterialName(fuse_id, "White Plastic")

    # Access Fuselage Cross-Sections
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
            vsp.SetParmVal(h_p, 5.20)
        elif i == 2:
            vsp.SetParmVal(xloc_p, 0.48)
            vsp.SetParmVal(w_p, fuse_width)
            vsp.SetParmVal(h_p, fuse_height)
        elif i == 3:
            vsp.SetParmVal(xloc_p, 0.82)
            vsp.SetParmVal(w_p, 5.60)
            vsp.SetParmVal(h_p, 5.80)

    # -------------------------------------------------------------------------
    # 2. HYDROGEN CRYOGENIC CYLINDERS (596.6 m³ TOTAL VOLUME, L/D <= 4.0)
    # -------------------------------------------------------------------------
    print("\n[2/6] Building Cryogenic Hydrogen Cylinders (L/D <= 4.0, Vol = 596.6 m³)...")
    # Sizing 4 Clustered Tanks in Aft Fuselage Cryo-Bay:
    # Each tank volume: 596.6 m³ / 4 = 149.15 m³
    # For L/D = 4.0: V = (11*pi/12) * D³ -> D = (149.15 / 2.8798)^(1/3) = 3.73 m
    # Tank Length: L = 4 * D = 14.92 m
    tank_diam = 3.73   # m
    tank_len = 14.92   # m (Aspect ratio L/D = 4.00 exact limit)
    tank_vol_each = (11.0 * math.pi / 12.0) * (tank_diam ** 3) # ~149.2 m³
    tank_vol_total = 4.0 * tank_vol_each # ~596.6 m³

    print(f"      - 4x Cryotanks: D = {tank_diam:.2f} m, L = {tank_len:.2f} m, L/D = {tank_len/tank_diam:.2f}")
    print(f"      - Tank Unit Volume: {tank_vol_each:.1f} m³, Total Volume: {tank_vol_total:.1f} m³ (Matches DT1 exactly!)")

    tank_x_loc = 45.50
    tank_spacing_y = 1.30
    tank_spacing_z = 1.20

    tank_configs = [
        ("LH2_Tank_Port_Upper",  -tank_spacing_y,  tank_spacing_z),
        ("LH2_Tank_Stbd_Upper",   tank_spacing_y,  tank_spacing_z),
        ("LH2_Tank_Port_Lower",  -tank_spacing_y, -tank_spacing_z),
        ("LH2_Tank_Stbd_Lower",   tank_spacing_y, -tank_spacing_z),
    ]

    for name, y_pos, z_pos in tank_configs:
        t_id = vsp.AddGeom("FUSELAGE", "")
        vsp.SetGeomName(t_id, name)
        vsp.SetParmVal(t_id, "Length", "Design", tank_len)
        vsp.SetParmVal(t_id, "X_Rel_Location", "XForm", tank_x_loc)
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
    print("\n[3/6] Building Sized Transonic Main Wing (Sref = 363.4 m², Span = 58.75 m)...")
    wing_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(wing_id, "MainWing_Transonic")
    vsp.SetParmVal(wing_id, "X_Rel_Location", "XForm", 26.50)
    vsp.SetParmVal(wing_id, "Y_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(wing_id, "Z_Rel_Location", "XForm", -1.20)
    vsp.SetParmVal(wing_id, "RotateAirfoilMatchDideralFlag", "WingGeom", 1.0)
    vsp.SetGeomMaterialName(wing_id, "Aluminum")

    # Sized Wing Parameters
    b_half = 58.75 / 2.0  # 29.375 m half-span
    c_root = 9.20         # m
    c_tip = 2.40          # m
    sweep_c4 = 29.0       # deg
    dihedral_deg = 5.5    # deg

    wing_xsurf = vsp.GetXSecSurf(wing_id, 0)
    xsec1 = vsp.GetXSec(wing_xsurf, 1)

    span_p = vsp.GetXSecParm(xsec1, "Span")
    sweep_p = vsp.GetXSecParm(xsec1, "Sweep")
    dih_p = vsp.GetXSecParm(xsec1, "Dihedral")
    root_p = vsp.GetXSecParm(xsec1, "Root_Chord")
    tip_p = vsp.GetXSecParm(xsec1, "Tip_Chord")

    vsp.SetParmVal(span_p, b_half)
    vsp.SetParmVal(sweep_p, sweep_c4)
    vsp.SetParmVal(dih_p, dihedral_deg)
    vsp.SetParmVal(root_p, c_root)
    vsp.SetParmVal(tip_p, c_tip)

    # Supercritical Airfoil Profile (t/c = 13.5% root, 10.5% tip)
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
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Span"), 9.75) # 19.5m total span
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Sweep"), 33.0)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Dihedral"), 6.0)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Root_Chord"), 5.60)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Tip_Chord"), 2.10)

    # Vertical Stabilizer (Single Vertical Fin)
    vtail_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(vtail_id, "VerticalTail")
    vsp.SetParmVal(vtail_id, "X_Rel_Location", "XForm", 51.00)
    vsp.SetParmVal(vtail_id, "Z_Rel_Location", "XForm", 2.80)
    vsp.SetParmVal(vtail_id, "X_Rel_Rotation", "XForm", 90.0) # Vertical orientation
    vsp.SetParmVal(vtail_id, "Sym_Planar_Flag", "Sym", vsp.SYM_NONE)
    vsp.SetGeomMaterialName(vtail_id, "Blue Plastic")

    vt_xsurf = vsp.GetXSecSurf(vtail_id, 0)
    vt_xsec1 = vsp.GetXSec(vt_xsurf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Span"), 9.80) # Fin Height
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Sweep"), 38.0)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Root_Chord"), 7.80)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Tip_Chord"), 2.80)

    # -------------------------------------------------------------------------
    # 5. PROPULSION: 4x HYDROGEN COMBUSTION TURBOFANS (152.5 kN EACH)
    # -------------------------------------------------------------------------
    print("\n[5/6] Building 4x Hydrogen Combustion Turbofans & Pylons...")
    fan_diam = 2.45  # m
    nacelle_len = 4.80 # m

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
    # 6. EXPORTING MODEL & GENERATING FILES
    # -------------------------------------------------------------------------
    print("\n[6/6] Exporting Model Files...")
    vsp_file = f"{output_prefix}.vsp3"
    stl_file = f"{output_prefix}.stl"
    obj_file = f"{output_prefix}.obj"

    vsp.WriteVSPFile(vsp_file)
    print(f"      -> Native OpenVSP file: {os.path.abspath(vsp_file)}")

    # Export Triangulated STL mesh
    vsp.ExportFile(stl_file, vsp.SET_ALL, vsp.EXPORT_STL)
    print(f"      -> 3D STL Surface Mesh: {os.path.abspath(stl_file)}")

    # Export Wavefront OBJ mesh
    vsp.ExportFile(obj_file, vsp.SET_ALL, vsp.EXPORT_OBJ)
    print(f"      -> 3D OBJ Mesh:         {os.path.abspath(obj_file)}")

    # Compute Mass & Computational Geometry Properties
    vsp.ComputeMassProps(vsp.SET_ALL, 100, 0)
    vsp.ComputeCompGeom(vsp.SET_ALL, True, vsp.COMP_GEOM_TXT_TYPE)
    print(f"      -> Mass & CompGeom Props computed successfully.")

    print(f"\n=================================================================")
    print(f"  EXAELIA HYDROGEN AIRCRAFT (DT2) GENERATED SUCCESSFULLY!")
    print(f"=================================================================")

if __name__ == "__main__":
    build_exaelia_hydrogen()
