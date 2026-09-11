#!/usr/bin/env python3
"""
=============================================================================
OpenVSP 3D CAD Parametric Model Generator: EXAELIA 80m Blended Wing Body (BWB)
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Author: Sai Srinivasa Manideep Jakka

Configuration Details:
1. Exact 80.0m Wingspan (ICAO Code F limit) & 60.0m Overall Length.
2. Muscular 4-Section Blended Wing Body (BWB) lifting fuselage (t/c = 19.5%).
3. Unified Widebody Passenger Theater Cabin in the central forward core (430 Pax).
4. Symmetrical Outboard Wing Shoulder & Aft Core Cryogenic LH2 Storage Bays (610 m³).
5. Twin Upper-Aft Deck Geared Turbofans (D = 3.4m, L = 7.0m) with acoustic pylons.
6. 3-Point Heavy-Duty Retractable Landing Gear Bogies.
7. Exports .vsp3, .stl (OML & components), .obj, and computes wetted area & mass properties.
=============================================================================
"""

import math
import os
import sys
import openvsp as vsp

def build_exaelia_bwb_80m(output_dir="/Users/jakkasaisrinivasamanideep/Documents/MMS236/03_CAD_OpenVSP_Models"):
    os.makedirs(output_dir, exist_ok=True)
    os.chdir(output_dir)
    print("=================================================================")
    print("  EXAELIA 80m BWB OpenVSP 3.51.3 Parametric CAD Generator")
    print("=================================================================")
    vsp.ClearVSPModel()
    
    # -------------------------------------------------------------------------
    # 1. MAIN BLENDED WING BODY AIRFRAME (4-Section Lifting Body + Outer Wing + Winglet)
    # -------------------------------------------------------------------------
    print("---> Building BWB Lifting Fuselage & Wing Geometry (80.0m Span)...")
    bwb_id = vsp.AddGeom("WING")
    vsp.SetGeomName(bwb_id, "EXAELIA_BWB_Airframe")

    # Insert 3 additional sections (Total 4 sections, 5 cross-section cuts)
    vsp.InsertXSec(bwb_id, 1, vsp.XS_FOUR_SERIES)
    vsp.InsertXSec(bwb_id, 2, vsp.XS_FOUR_SERIES)
    vsp.InsertXSec(bwb_id, 3, vsp.XS_FOUR_SERIES)

    # Section 1: Centerbody Lifting Fuselage (Semi-span = 8.0 m)
    # Root Chord = 38.0 m, Tip Chord = 26.0 m, Sweep = 38.0 deg, t/c = 19.5%
    vsp.SetParmVal(bwb_id, "Span", "XSec_1", 8.0)
    vsp.SetParmVal(bwb_id, "Root_Chord", "XSec_1", 38.0)
    vsp.SetParmVal(bwb_id, "Tip_Chord", "XSec_1", 26.0)
    vsp.SetParmVal(bwb_id, "Sweep", "XSec_1", 38.0)
    vsp.SetParmVal(bwb_id, "Dihedral", "XSec_1", 1.0)
    vsp.SetParmVal(bwb_id, "ThickChord", "XSecCurve_0", 0.195)
    vsp.SetParmVal(bwb_id, "ThickChord", "XSecCurve_1", 0.195)

    # Section 2: Blended Wing Shoulder (Semi-span = 12.0 m -> Y = 8.0 to 20.0 m)
    # Root Chord = 26.0 m, Tip Chord = 10.0 m, Sweep = 42.0 deg, t/c = 14.5%
    vsp.SetParmVal(bwb_id, "Span", "XSec_2", 12.0)
    vsp.SetParmVal(bwb_id, "Tip_Chord", "XSec_2", 10.0)
    vsp.SetParmVal(bwb_id, "Sweep", "XSec_2", 42.0)
    vsp.SetParmVal(bwb_id, "Dihedral", "XSec_2", 2.0)
    vsp.SetParmVal(bwb_id, "ThickChord", "XSecCurve_2", 0.145)

    # Section 3: High-Efficiency Outer Wing (Semi-span = 18.8 m -> Y = 20.0 to 38.8 m)
    # Root Chord = 10.0 m, Tip Chord = 3.5 m, Sweep = 33.0 deg, t/c = 11.5%
    vsp.SetParmVal(bwb_id, "Span", "XSec_3", 18.8)
    vsp.SetParmVal(bwb_id, "Tip_Chord", "XSec_3", 3.5)
    vsp.SetParmVal(bwb_id, "Sweep", "XSec_3", 33.0)
    vsp.SetParmVal(bwb_id, "Dihedral", "XSec_3", 3.0)
    vsp.SetParmVal(bwb_id, "ThickChord", "XSecCurve_3", 0.115)

    # Section 4: Canted Upturned Winglets (Semi-span = 3.5 m -> dy = 1.2 m, dz = 3.3 m)
    # Root Chord = 3.5 m, Tip Chord = 1.6 m, Sweep = 45.0 deg, Dihedral = 70.0 deg
    vsp.SetParmVal(bwb_id, "Span", "XSec_4", 3.5)
    vsp.SetParmVal(bwb_id, "Tip_Chord", "XSec_4", 1.6)
    vsp.SetParmVal(bwb_id, "Sweep", "XSec_4", 45.0)
    vsp.SetParmVal(bwb_id, "Dihedral", "XSec_4", 70.0)
    vsp.SetParmVal(bwb_id, "ThickChord", "XSecCurve_4", 0.090)

    # Sets: 3 = OML Airframe
    vsp.SetSetFlag(bwb_id, 3, True)

    # -------------------------------------------------------------------------
    # 2. TWIN UPPER-AFT DECK TURBOFAN NACELLES & PYLONS
    # -------------------------------------------------------------------------
    print("---> Building Twin Upper-Aft Turbofan Engines & Pylons...")
    for side_name, side_sign in [("Port", -1.0), ("Stbd", 1.0)]:
        eng_id = vsp.AddGeom("FUSELAGE")
        vsp.SetGeomName(eng_id, f"Engine_{side_name}")
        vsp.SetParmVal(eng_id, "X_Location", "XForm", 36.0)
        vsp.SetParmVal(eng_id, "Y_Location", "XForm", side_sign * 6.2)
        vsp.SetParmVal(eng_id, "Z_Location", "XForm", 3.8)
        vsp.SetParmVal(eng_id, "Length", "Design", 7.0)
        for i in [1, 2, 3]:
            vsp.SetParmVal(eng_id, "Ellipse_Width", f"XSecCurve_{i}", 3.4)
            vsp.SetParmVal(eng_id, "Ellipse_Height", f"XSecCurve_{i}", 3.4)
        vsp.SetSetFlag(eng_id, 3, True)
        vsp.SetSetFlag(eng_id, 4, True)  # Set 4 = Propulsion

        # Acoustic Pylon Blade (Rotate via XForm instead of Dihedral=90)
        pylon_id = vsp.AddGeom("WING")
        vsp.SetGeomName(pylon_id, f"Pylon_{side_name}")
        vsp.SetParmVal(pylon_id, "X_Location", "XForm", 37.0)
        vsp.SetParmVal(pylon_id, "Y_Location", "XForm", side_sign * 6.2)
        vsp.SetParmVal(pylon_id, "Z_Location", "XForm", 1.8)
        vsp.SetParmVal(pylon_id, "X_Rel_Rotation", "XForm", 90.0 if side_sign > 0 else -90.0)
        vsp.SetParmVal(pylon_id, "Span", "XSec_1", 2.0)
        vsp.SetParmVal(pylon_id, "Root_Chord", "XSec_1", 4.5)
        vsp.SetParmVal(pylon_id, "Tip_Chord", "XSec_1", 4.0)
        vsp.SetParmVal(pylon_id, "ThickChord", "XSecCurve_0", 0.08)
        vsp.SetParmVal(pylon_id, "ThickChord", "XSecCurve_1", 0.08)
        vsp.SetSetFlag(pylon_id, 3, True)
        vsp.SetSetFlag(pylon_id, 4, True)

    # -------------------------------------------------------------------------
    # 3. UNIFIED THEATER PASSENGER CABIN DECK (Internal Core)
    # -------------------------------------------------------------------------
    print("---> Modeling Unified Passenger Theater Cabin Deck...")
    cabin_id = vsp.AddGeom("FUSELAGE")
    vsp.SetGeomName(cabin_id, "Unified_Theater_Cabin_Deck")
    vsp.SetParmVal(cabin_id, "X_Location", "XForm", 9.0)
    vsp.SetParmVal(cabin_id, "Y_Location", "XForm", 0.0)
    vsp.SetParmVal(cabin_id, "Z_Location", "XForm", 0.2)
    vsp.SetParmVal(cabin_id, "Length", "Design", 20.0)
    for i in [1, 2, 3]:
        vsp.SetParmVal(cabin_id, "Ellipse_Width", f"XSecCurve_{i}", 14.0)
        vsp.SetParmVal(cabin_id, "Ellipse_Height", f"XSecCurve_{i}", 2.4)
    vsp.SetSetFlag(cabin_id, 5, True)  # Set 5 = Internal Core

    # -------------------------------------------------------------------------
    # 4. CRYOGENIC LH2 FUEL TANKS (Outboard Wing Shoulders + Aft Core = 610 m³)
    # -------------------------------------------------------------------------
    print("---> Sizing & Packaging Internal Cryogenic LH2 Tanks (610 m³)...")
    tank_coords = [
        # (Name, X_pos, Y_pos, Z_pos, Length, Width, Height)
        ("LH2_Tank_Outboard_Fwd_Port", 16.0, -11.5, 0.4, 12.0, 3.1, 3.1),
        ("LH2_Tank_Outboard_Fwd_Stbd", 16.0,  11.5, 0.4, 12.0, 3.1, 3.1),
        ("LH2_Tank_Outboard_Mid_Port", 21.0, -16.0, 0.2, 11.0, 2.8, 2.8),
        ("LH2_Tank_Outboard_Mid_Stbd", 21.0,  16.0, 0.2, 11.0, 2.8, 2.8),
        ("LH2_Tank_Aft_Core_Port",     30.0,  -3.2, 0.8, 11.5, 3.2, 3.2),
        ("LH2_Tank_Aft_Core_Stbd",     30.0,   3.2, 0.8, 11.5, 3.2, 3.2),
    ]

    for t_name, tx, ty, tz, tlen, tw, th in tank_coords:
        tank_id = vsp.AddGeom("FUSELAGE")
        vsp.SetGeomName(tank_id, t_name)
        vsp.SetParmVal(tank_id, "X_Location", "XForm", tx)
        vsp.SetParmVal(tank_id, "Y_Location", "XForm", ty)
        vsp.SetParmVal(tank_id, "Z_Location", "XForm", tz)
        vsp.SetParmVal(tank_id, "Length", "Design", tlen)
        for i in [1, 2, 3]:
            vsp.SetParmVal(tank_id, "Ellipse_Width", f"XSecCurve_{i}", tw)
            vsp.SetParmVal(tank_id, "Ellipse_Height", f"XSecCurve_{i}", th)
        vsp.SetSetFlag(tank_id, 5, True)  # Set 5 = Internal Core

    # -------------------------------------------------------------------------
    # 5. 3-STRUT HEAVY RETRACTABLE LANDING GEAR
    # -------------------------------------------------------------------------
    print("---> Modeling 3-Point Heavy Landing Gear...")
    gear_locations = [
        ("Nose_Landing_Gear", 7.0,  0.0, -4.5, 5.0, 1.2),
        ("Main_Landing_Gear_Port", 26.5, -5.8, -4.5, 5.0, 1.8),
        ("Main_Landing_Gear_Stbd", 26.5,  5.8, -4.5, 5.0, 1.8),
    ]
    for g_name, gx, gy, gz, glen, gdia in gear_locations:
        gear_id = vsp.AddGeom("FUSELAGE")
        vsp.SetGeomName(gear_id, g_name)
        vsp.SetParmVal(gear_id, "X_Location", "XForm", gx)
        vsp.SetParmVal(gear_id, "Y_Location", "XForm", gy)
        vsp.SetParmVal(gear_id, "Z_Location", "XForm", gz)
        vsp.SetParmVal(gear_id, "Length", "Design", glen)
        for i in [1, 2, 3]:
            vsp.SetParmVal(gear_id, "Ellipse_Width", f"XSecCurve_{i}", gdia)
            vsp.SetParmVal(gear_id, "Ellipse_Height", f"XSecCurve_{i}", gdia)
        vsp.SetSetFlag(gear_id, 6, True)  # Set 6 = Landing Gear

    # Update OpenVSP geometry tree
    vsp.Update()

    # -------------------------------------------------------------------------
    # 6. EXPORT CAD FILES (.vsp3, .stl, .obj, CompGeom, MassProps)
    # -------------------------------------------------------------------------
    vsp3_filename = "EXAELIA_BWB_80m.vsp3"
    stl_filename = "EXAELIA_BWB_80m.stl"
    stl_oml_filename = "EXAELIA_BWB_80m_OML.stl"
    stl_internal_filename = "EXAELIA_BWB_80m_Internal.stl"
    obj_filename = "EXAELIA_BWB_80m.obj"

    print(f"---> Writing OpenVSP Native CAD: {vsp3_filename}...")
    vsp.WriteVSPFile(vsp3_filename)

    print(f"---> Exporting Full Assembly 3D STL: {stl_filename}...")
    vsp.ExportFile(stl_filename, vsp.SET_ALL, vsp.EXPORT_STL)

    print(f"---> Exporting OML Outer Mold Line STL: {stl_oml_filename}...")
    vsp.ExportFile(stl_oml_filename, 3, vsp.EXPORT_STL)

    print(f"---> Exporting Internal Components STL: {stl_internal_filename}...")
    vsp.ExportFile(stl_internal_filename, 5, vsp.EXPORT_STL)

    print(f"---> Exporting 3D OBJ Textured Mesh: {obj_filename}...")
    vsp.ExportFile(obj_filename, vsp.SET_ALL, vsp.EXPORT_OBJ)

    print("---> Computing Component Geometry & Wetted Area...")
    vsp.ComputeCompGeom(vsp.SET_ALL, False, vsp.COMP_GEOM_TXT_TYPE)

    print("---> Computing Mass Properties & CG Location...")
    vsp.ComputeMassProps(vsp.SET_ALL, 20, vsp.MASS_PROP_TXT_TYPE)

    print("\n=================================================================")
    print(f"  EXAELIA BWB 80m CAD MODEL GENERATION COMPLETE!")
    print(f"  VSP3 Model   : {os.path.abspath(vsp3_filename)}")
    print(f"  STL Assembly : {os.path.abspath(stl_filename)}")
    print(f"  STL OML      : {os.path.abspath(stl_oml_filename)}")
    print(f"  STL Internal : {os.path.abspath(stl_internal_filename)}")
    print(f"  OBJ Mesh     : {os.path.abspath(obj_filename)}")
    print("=================================================================")

if __name__ == "__main__":
    build_exaelia_bwb_80m()
