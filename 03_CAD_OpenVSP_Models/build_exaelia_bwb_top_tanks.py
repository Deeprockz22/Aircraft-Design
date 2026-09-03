#!/usr/bin/env python3
"""
=============================================================================
MMS236 Aircraft Design — EXAELIA BWB with TOP DORSAL HYDROGEN TANKS
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology

Architecture:
- B-2 / Flying Wing Aerodynamic Airframe: Sref = 520 m², Span = 65.0 m.
- Top Surface Hydrogen Storage: 7x Modular Cryogenic Cylinders (597 m³ total)
  mounted explicitly along the top dorsal crown and upper shoulders.
- Main Interior Deck: 100% dedicated to 430 Passengers + 44 LD3 Cargo Containers.
- Engines: 4x Hydrogen Turbofans mounted on upper aft deck.
- Control: Canted Wingtip Winglets + Trailing Edge Elevons.
=============================================================================
"""

import math
import os
import sys
import openvsp as vsp

def build_bwb_top_tanks(output_prefix="EXAELIA_BWB_Top_Tanks"):
    print("=================================================================")
    print("  Generating EXAELIA BWB with TOP DORSAL HYDROGEN TANKS")
    print("=================================================================")

    vsp.ClearVSPModel()

    # -------------------------------------------------------------------------
    # 1. BWB FLYING WING MAIN AIRFRAME
    # -------------------------------------------------------------------------
    print("\n[1/5] Building BWB Flying Wing Main Airframe...")
    bwb_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(bwb_id, "BWB_Main_Airframe")
    vsp.SetParmVal(bwb_id, "X_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(bwb_id, "Y_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(bwb_id, "Z_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(bwb_id, "RotateAirfoilMatchDideralFlag", "WingGeom", 1.0)
    vsp.SetGeomMaterialName(bwb_id, "White")

    bwb_xsurf = vsp.GetXSecSurf(bwb_id, 0)
    vsp.InsertXSec(bwb_id, 1, vsp.XS_FOUR_SERIES)
    vsp.InsertXSec(bwb_id, 2, vsp.XS_FOUR_SERIES)

    # Section 1: Centerbody
    sec1 = vsp.GetXSec(bwb_xsurf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(sec1, "Span"), 6.50)
    vsp.SetParmVal(vsp.GetXSecParm(sec1, "Root_Chord"), 32.00)
    vsp.SetParmVal(vsp.GetXSecParm(sec1, "Tip_Chord"), 22.00)
    vsp.SetParmVal(vsp.GetXSecParm(sec1, "Sweep"), 42.0)

    # Section 2: Transition
    sec2 = vsp.GetXSec(bwb_xsurf, 2)
    vsp.SetParmVal(vsp.GetXSecParm(sec2, "Span"), 8.50)
    vsp.SetParmVal(vsp.GetXSecParm(sec2, "Root_Chord"), 22.00)
    vsp.SetParmVal(vsp.GetXSecParm(sec2, "Tip_Chord"), 10.50)
    vsp.SetParmVal(vsp.GetXSecParm(sec2, "Sweep"), 36.0)
    vsp.SetParmVal(vsp.GetXSecParm(sec2, "Dihedral"), 2.0)

    # Section 3: Outer Wing
    sec3 = vsp.GetXSec(bwb_xsurf, 3)
    vsp.SetParmVal(vsp.GetXSecParm(sec3, "Span"), 17.50)
    vsp.SetParmVal(vsp.GetXSecParm(sec3, "Root_Chord"), 10.50)
    vsp.SetParmVal(vsp.GetXSecParm(sec3, "Tip_Chord"), 3.20)
    vsp.SetParmVal(vsp.GetXSecParm(sec3, "Sweep"), 30.0)
    vsp.SetParmVal(vsp.GetXSecParm(sec3, "Dihedral"), 4.5)

    for c_idx, tc_val in [(0, 0.15), (1, 0.14), (2, 0.12), (3, 0.10)]:
        t_p = vsp.GetParm(bwb_id, "ThickChord", f"XSecCurve_{c_idx}")
        if t_p:
            vsp.SetParmVal(t_p, tc_val)

    # -------------------------------------------------------------------------
    # 2. TOP DORSAL HYDROGEN TANKS (MOUNTED PROMINENTLY ON TOP SURFACE)
    # -------------------------------------------------------------------------
    print("\n[2/5] Mounting 7x Cryogenic Hydrogen Tanks on the TOP Surface...")
    tank_diam = 3.09
    tank_len = 12.37

    # 7 Tanks mounted on the top dorsal surface:
    # 3 on top centerline spine, 2 on port upper shoulder, 2 on starboard upper shoulder
    top_tank_positions = [
        ("Top_Tank_1_Centerline_Fwd",   8.50,   0.00,  2.20),
        ("Top_Tank_2_Centerline_Mid",  20.90,   0.00,  2.20),
        ("Top_Tank_3_Centerline_Aft",  33.30,   0.00,  2.20),
        ("Top_Tank_4_Port_Shoulder1",  14.00,  -3.80,  1.80),
        ("Top_Tank_5_Port_Shoulder2",  26.40,  -3.80,  1.80),
        ("Top_Tank_6_Stbd_Shoulder1",  14.00,   3.80,  1.80),
        ("Top_Tank_7_Stbd_Shoulder2",  26.40,   3.80,  1.80),
    ]

    for name, x_pos, y_pos, z_pos in top_tank_positions:
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

    print(f"      - 7x Top Surface Tanks Mounted: Diameter = {tank_diam} m, Length = {tank_len} m")
    print(f"      - Total Storage Volume: 596.5 m³ (100% mission fuel stored on top deck)")

    # -------------------------------------------------------------------------
    # 3. PASSENGER & CARGO MAIN DECK (INSIDE AIRFRAME)
    # -------------------------------------------------------------------------
    print("\n[3/5] Building Passenger Cabin & Cargo Holds...")
    pax_floor = vsp.AddGeom("POD", "")
    vsp.SetGeomName(pax_floor, "Cabin_430Pax_MainDeck")
    vsp.SetParmVal(pax_floor, "Length", "Design", 20.00)
    vsp.SetParmVal(pax_floor, "X_Rel_Location", "XForm", 8.00)
    vsp.SetParmVal(pax_floor, "Z_Rel_Location", "XForm", -0.20)
    vsp.SetGeomMaterialName(pax_floor, "White")

    cargo_bwb = vsp.AddGeom("POD", "")
    vsp.SetGeomName(cargo_bwb, "Cargo_44_LD3_LowerHold")
    vsp.SetParmVal(cargo_bwb, "Length", "Design", 16.00)
    vsp.SetParmVal(cargo_bwb, "X_Rel_Location", "XForm", 10.00)
    vsp.SetParmVal(cargo_bwb, "Z_Rel_Location", "XForm", -1.40)
    vsp.SetGeomMaterialName(cargo_bwb, "Aluminum")

    # -------------------------------------------------------------------------
    # 4. PROPULSION: 4x UPPER-SURFACE HYDROGEN TURBOFANS
    # -------------------------------------------------------------------------
    print("\n[4/5] Building 4x Upper Aft Deck Turbofans...")
    fan_diam = 2.45
    nacelle_len = 4.80

    engine_locations = [
        ("BWB_Engine_Port_Inboard",   -3.40,  2.10, 26.00),
        ("BWB_Engine_Stbd_Inboard",    3.40,  2.10, 26.00),
        ("BWB_Engine_Port_Outboard",  -7.40,  1.80, 27.50),
        ("BWB_Engine_Stbd_Outboard",   7.40,  1.80, 27.50),
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
    # 5. CANTED WINGLETS
    # -------------------------------------------------------------------------
    print("\n[5/5] Building Canted Wingtip Winglets...")
    wlet_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(wlet_id, "BWB_Winglets")
    vsp.SetParmVal(wlet_id, "X_Rel_Location", "XForm", 29.50)
    vsp.SetParmVal(wlet_id, "Y_Rel_Location", "XForm", 32.00)
    vsp.SetParmVal(wlet_id, "Z_Rel_Location", "XForm", 1.20)
    vsp.SetParmVal(wlet_id, "X_Rel_Rotation", "XForm", 75.0)
    vsp.SetGeomMaterialName(wlet_id, "Blue Plastic")

    wl_xsurf = vsp.GetXSecSurf(wlet_id, 0)
    wl_xsec = vsp.GetXSec(wl_xsurf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(wl_xsec, "Span"), 4.50)
    vsp.SetParmVal(vsp.GetXSecParm(wl_xsec, "Sweep"), 45.0)
    vsp.SetParmVal(vsp.GetXSecParm(wl_xsec, "Root_Chord"), 3.20)
    vsp.SetParmVal(vsp.GetXSecParm(wl_xsec, "Tip_Chord"), 1.20)

    vsp.Update()

    vsp_file = f"{output_prefix}.vsp3"
    stl_file = f"{output_prefix}.stl"
    obj_file = f"{output_prefix}.obj"

    vsp.WriteVSPFile(vsp_file)
    vsp.ExportFile(stl_file, vsp.SET_ALL, vsp.EXPORT_STL)
    vsp.ExportFile(obj_file, vsp.SET_ALL, vsp.EXPORT_OBJ)

    print(f"\n[OK] Model successfully saved to {vsp_file}")

if __name__ == "__main__":
    build_bwb_top_tanks()
