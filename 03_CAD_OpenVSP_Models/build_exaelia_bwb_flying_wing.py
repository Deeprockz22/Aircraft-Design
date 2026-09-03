#!/usr/bin/env python3
"""
=============================================================================
MMS236 Aircraft Design — EXAELIA Blended Wing Body (BWB / Flying Wing)
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology

Architecture (B-2 Inspired Flying Wing / Blended Wing Body):
- Deep Aerodynamic Centerbody: Houses 430 passengers in a modern theatre cabin,
  44 LD3 cargo containers, and 7x insulated cryogenic LH2 tanks (597 m³).
- High Aerodynamic Efficiency: (L/D)max > 22.5 (25% lower fuel burn than tube-and-wing).
- Sized Wingspan: 65.0 m (Within ICAO Code F 80m gate limit).
- Propulsion: 4x Hydrogen Turbofans mounted on upper aft deck (Acoustic shielding & low drag).
- Pitch/Yaw Control: Multi-segment elevons + drag rudders / wingtip winglets.
=============================================================================
"""

import math
import os
import sys
import openvsp as vsp

def build_exaelia_bwb(output_prefix="EXAELIA_BWB_Flying_Wing"):
    print("=================================================================")
    print("  Generating EXAELIA B-2 Inspired Blended Wing Body (BWB)")
    print("=================================================================")

    vsp.ClearVSPModel()

    # -------------------------------------------------------------------------
    # 1. BLENDED WING BODY (CENTERBODY + TRANSITION + OUTER WINGS)
    # -------------------------------------------------------------------------
    print("\n[1/5] Building Blended Wing Body Centerbody & Outer Wings...")
    bwb_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(bwb_id, "BWB_Airframe_Main")
    vsp.SetParmVal(bwb_id, "X_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(bwb_id, "Y_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(bwb_id, "Z_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(bwb_id, "RotateAirfoilMatchDideralFlag", "WingGeom", 1.0)
    vsp.SetGeomMaterialName(bwb_id, "White")

    # We configure 3 wing sections (Centerbody, Blended Mid-Body, Outer Wing)
    # Section 0: Centerbody (Root Chord = 32.0 m, Span = 6.0 m, t/c = 17%)
    # Section 1: Mid-Body Transition (Chord = 16.0 m, Span = 8.5 m, t/c = 14%)
    # Section 2: Outer Wing (Tip Chord = 3.2 m, Span = 18.0 m, t/c = 10.5%)
    # Total Half-Span = 6.0 + 8.5 + 18.0 = 32.5 m -> Full Wingspan = 65.0 m!
    
    bwb_xsurf = vsp.GetXSecSurf(bwb_id, 0)
    
    # Insert 2 additional sections for a 3-stage BWB
    vsp.InsertXSec(bwb_id, 1, vsp.XS_FOUR_SERIES)
    vsp.InsertXSec(bwb_id, 2, vsp.XS_FOUR_SERIES)

    # Section 1: Centerbody (Cabin & Cryotank Zone)
    sec1 = vsp.GetXSec(bwb_xsurf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(sec1, "Span"), 6.50)
    vsp.SetParmVal(vsp.GetXSecParm(sec1, "Root_Chord"), 32.00)
    vsp.SetParmVal(vsp.GetXSecParm(sec1, "Tip_Chord"), 22.00)
    vsp.SetParmVal(vsp.GetXSecParm(sec1, "Sweep"), 42.0)
    vsp.SetParmVal(vsp.GetXSecParm(sec1, "Dihedral"), 0.0)

    # Section 2: Blended Transition
    sec2 = vsp.GetXSec(bwb_xsurf, 2)
    vsp.SetParmVal(vsp.GetXSecParm(sec2, "Span"), 8.50)
    vsp.SetParmVal(vsp.GetXSecParm(sec2, "Root_Chord"), 22.00)
    vsp.SetParmVal(vsp.GetXSecParm(sec2, "Tip_Chord"), 10.50)
    vsp.SetParmVal(vsp.GetXSecParm(sec2, "Sweep"), 36.0)
    vsp.SetParmVal(vsp.GetXSecParm(sec2, "Dihedral"), 2.0)

    # Section 3: Outer Aerodynamic Wing
    sec3 = vsp.GetXSec(bwb_xsurf, 3)
    vsp.SetParmVal(vsp.GetXSecParm(sec3, "Span"), 17.50)
    vsp.SetParmVal(vsp.GetXSecParm(sec3, "Root_Chord"), 10.50)
    vsp.SetParmVal(vsp.GetXSecParm(sec3, "Tip_Chord"), 3.20)
    vsp.SetParmVal(vsp.GetXSecParm(sec3, "Sweep"), 30.0)
    vsp.SetParmVal(vsp.GetXSecParm(sec3, "Dihedral"), 4.5)

    # Adjust thickness/camber along the span
    # Centerbody thick supercritical airfoil (t/c = 17% for cabin & tanks)
    for c_idx, tc_val, camb_val in [(0, 0.175, 0.02), (1, 0.160, 0.02), (2, 0.130, 0.015), (3, 0.105, 0.012)]:
        c_p = vsp.GetParm(bwb_id, "Camber", f"XSecCurve_{c_idx}")
        t_p = vsp.GetParm(bwb_id, "ThickChord", f"XSecCurve_{c_idx}")
        if c_p:
            vsp.SetParmVal(c_p, camb_val)
        if t_p:
            vsp.SetParmVal(t_p, tc_val)

    # -------------------------------------------------------------------------
    # 2. INTERNAL 7x CRYOGENIC HYDROGEN TANKS (PACKAGED INSIDE CENTERBODY)
    # -------------------------------------------------------------------------
    print("\n[2/5] Packaging 7x Internal Cryotanks in BWB Centerbody...")
    tank_diam = 3.09
    tank_len = 12.37

    # Inside the BWB, tanks are placed symmetrically around the CG
    bwb_tank_positions = [
        ("BWB_LH2_Tank_Center",     12.00,   0.00,  0.40),
        ("BWB_LH2_Tank_Port_Inner", 14.50,  -3.50,  0.30),
        ("BWB_LH2_Tank_Stbd_Inner", 14.50,   3.50,  0.30),
        ("BWB_LH2_Tank_Port_Outer", 17.00,  -7.00,  0.20),
        ("BWB_LH2_Tank_Stbd_Outer", 17.00,   7.00,  0.20),
        ("BWB_LH2_Tank_Aft_Port",   20.00,  -3.50,  0.30),
        ("BWB_LH2_Tank_Aft_Stbd",   20.00,   3.50,  0.30),
    ]

    for name, x_pos, y_pos, z_pos in bwb_tank_positions:
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

    # -------------------------------------------------------------------------
    # 3. CABIN SEATING (430 PASSENGERS THEATRE-STYLE DECK)
    # -------------------------------------------------------------------------
    print("\n[3/5] Packaging 430-Passenger Widebody Theatre Cabin & Cargo Deck...")
    # BWB Passenger Floor Deck
    pax_floor = vsp.AddGeom("POD", "")
    vsp.SetGeomName(pax_floor, "BWB_Passenger_Floor_430Pax")
    vsp.SetParmVal(pax_floor, "Length", "Design", 18.50)
    vsp.SetParmVal(pax_floor, "X_Rel_Location", "XForm", 8.00)
    vsp.SetParmVal(pax_floor, "Z_Rel_Location", "XForm", 0.00)
    vsp.SetGeomMaterialName(pax_floor, "White")

    # Lower Cargo Hold (44 LD3 Containers)
    cargo_bwb = vsp.AddGeom("POD", "")
    vsp.SetGeomName(cargo_bwb, "BWB_Cargo_Hold_44_LD3")
    vsp.SetParmVal(cargo_bwb, "Length", "Design", 16.00)
    vsp.SetParmVal(cargo_bwb, "X_Rel_Location", "XForm", 10.00)
    vsp.SetParmVal(cargo_bwb, "Z_Rel_Location", "XForm", -1.20)
    vsp.SetGeomMaterialName(cargo_bwb, "Aluminum")

    # -------------------------------------------------------------------------
    # 4. PROPULSION: 4x UPPER-SURFACE MOUNTED HYDROGEN TURBOFANS
    # -------------------------------------------------------------------------
    print("\n[4/5] Building 4x Upper-Deck Hydrogen Turbofans (B-2 / BWB Style)...")
    # Placing engines on the upper aft deck provides acoustic shielding and cleans underbody flow
    fan_diam = 2.45
    nacelle_len = 4.80

    engine_locations = [
        ("BWB_Engine_Port_Inboard",   -3.20,  1.80, 24.50),
        ("BWB_Engine_Stbd_Inboard",    3.20,  1.80, 24.50),
        ("BWB_Engine_Port_Outboard",  -7.20,  1.60, 26.00),
        ("BWB_Engine_Stbd_Outboard",   7.20,  1.60, 26.00),
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
        for k in range(1, vsp.GetNumXSec(eng_xsurf) - 1):
            vsp.ChangeXSecShape(eng_xsurf, k, vsp.XS_CIRCLE)
            vsp.SetParmVal(vsp.GetXSecParm(vsp.GetXSec(eng_xsurf, k), "Circle_Diameter"), fan_diam)

    # -------------------------------------------------------------------------
    # 5. CANTED WINGLETS (YAW & ROLL CONTROL / STABILITY)
    # -------------------------------------------------------------------------
    print("\n[5/5] Building Aerodynamic Canted Winglets...")
    wlet_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(wlet_id, "BWB_Winglets")
    vsp.SetParmVal(wlet_id, "X_Rel_Location", "XForm", 29.50)
    vsp.SetParmVal(wlet_id, "Y_Rel_Location", "XForm", 32.00)
    vsp.SetParmVal(wlet_id, "Z_Rel_Location", "XForm", 1.20)
    vsp.SetParmVal(wlet_id, "X_Rel_Rotation", "XForm", 75.0) # Canted vertical
    vsp.SetGeomMaterialName(wlet_id, "Blue Plastic")

    wl_xsurf = vsp.GetXSecSurf(wlet_id, 0)
    wl_xsec = vsp.GetXSec(wl_xsurf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(wl_xsec, "Span"), 4.50)
    vsp.SetParmVal(vsp.GetXSecParm(wl_xsec, "Sweep"), 45.0)
    vsp.SetParmVal(vsp.GetXSecParm(wl_xsec, "Root_Chord"), 3.20)
    vsp.SetParmVal(vsp.GetXSecParm(wl_xsec, "Tip_Chord"), 1.20)

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

    print(f"\n=================================================================")
    print(f"  EXAELIA B-2 FLYING WING (BWB) MODEL GENERATED SUCCESSFULLY!")
    print(f"=================================================================")

if __name__ == "__main__":
    build_exaelia_bwb()
