#!/usr/bin/env python3
"""
=============================================================================
AETHER 80m Liquid Hydrogen Blended Wing Body (BWB) Parametric CAD Generator
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Group:  13 - AETHER (430 Pax, 12,500 km range, Mach 0.85 at FL350)
Author: Sai Srinivasa Manideep Jakka

This script uses the AETHER OpenVSP Parametric Skills module to construct:
1. Exact 80.0m Wingspan ICAO Code F Blended Wing Body lifting surface.
2. Unified 430-Passenger Widebody Theater Cabin (20m x 14m x 2.4m).
3. 6 Cryogenic LH2 Storage Tanks totaling ~798-802 m³ installed volume.
4. 3 Upper-Aft Deck Geared Turbofans (D = 3.4m, L = 7.0m) with acoustic pylons.
5. 3-Point Heavy-Duty Retractable Landing Gear.
6. Exports .vsp3, .stl, .obj, and runs CompGeom and VSPAERO aerodynamic evaluation.
=============================================================================
"""

import math
import os
import sys

# Ensure local module imports work
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

import openvsp as vsp
from aether_openvsp_skills import (
    initialize_aircraft_workspace,
    design_aerodynamic_wing,
    design_bwb_multisection_surface,
    design_streamlined_fuselage,
    run_aerodynamic_evaluation
)

def build_aether_bwb_80m(output_dir=script_dir):
    os.makedirs(output_dir, exist_ok=True)
    os.chdir(output_dir)

    print("=" * 74)
    print("  AETHER 80m Liquid Hydrogen BWB OpenVSP 3.51.3 Parametric CAD Generator")
    print("  Group 13 | 430 Pax | 12,500 km Range | Mach 0.85 | MTOW = 277.97 t")
    print("=" * 74)

    # -------------------------------------------------------------------------
    # 0. INITIALIZE WORKSPACE
    # -------------------------------------------------------------------------
    init_msg = initialize_aircraft_workspace()
    print(f"---> [Skill 1] {init_msg}")

    # -------------------------------------------------------------------------
    # 1. MAIN BWB AIRFRAME (4-Section Blended Wing Body Lifting Surface)
    # -------------------------------------------------------------------------
    print("---> [Skill 2] Generating Multi-Section BWB Lifting Surface (b = 80.0 m)...")
    bwb_sections = [
        # Section 1: Centerbody Cabin (Semi-span = 8.0 m)
        {
            "span": 8.0,
            "root_chord": 38.0,
            "tip_chord": 26.0,
            "sweep": 38.0,
            "dihedral": 1.0,
            "tc_root": 0.195,
            "tc_tip": 0.195,
        },
        # Section 2: Blended Shoulder / Cryotank Bay (Semi-span = 12.0 m -> Y = 8 to 20 m)
        {
            "span": 12.0,
            "tip_chord": 10.0,
            "sweep": 42.0,
            "dihedral": 2.0,
            "tc_tip": 0.145,
        },
        # Section 3: High-Efficiency Outer Transonic Wing (Semi-span = 18.8 m -> Y = 20 to 38.8 m)
        {
            "span": 18.8,
            "tip_chord": 3.5,
            "sweep": 33.0,
            "dihedral": 3.0,
            "tc_tip": 0.115,
        },
        # Section 4: Canted Winglets (Semi-span = 3.5 m -> dy = 1.2 m, dz = 3.3 m)
        {
            "span": 3.5,
            "tip_chord": 1.6,
            "sweep": 45.0,
            "dihedral": 70.0,
            "tc_tip": 0.090,
        },
    ]

    airframe_meta = design_bwb_multisection_surface(
        sections=bwb_sections,
        name="AETHER_BWB_Airframe",
        geom_set=3 # Set 3 = Outer Mold Line (OML)
    )
    bwb_id = airframe_meta["geom_id"]
    print(f"     Airframe created: Span = {airframe_meta['total_wingspan_m']} m, ID = {bwb_id}")

    # -------------------------------------------------------------------------
    # 2. TRIPLE UPPER-AFT DECK TURBOFANS & ACOUSTIC PYLONS
    # -------------------------------------------------------------------------
    print("---> [Skill 3] Generating 3 Upper-Aft Geared Turbofans & Acoustic Pylons...")
    engines = [
        ("Center",  36.5,   0.0, 4.2),
        ("Port",    36.0,  -6.2, 3.8),
        ("Stbd",    36.0,   6.2, 3.8),
    ]

    for eng_name, ex, ey, ez in engines:
        design_streamlined_fuselage(
            length=7.0,
            max_diameter=3.4,
            x_loc=ex,
            y_loc=ey,
            z_loc=ez,
            name=f"Turbofan_Engine_{eng_name}",
            geom_set=3
        )

        # Acoustic Support Pylon
        pylon_id = vsp.AddGeom("WING")
        vsp.SetGeomName(pylon_id, f"Engine_Pylon_{eng_name}")
        vsp.SetParmVal(pylon_id, "X_Location", "XForm", ex + 1.0)
        vsp.SetParmVal(pylon_id, "Y_Location", "XForm", ey)
        vsp.SetParmVal(pylon_id, "Z_Location", "XForm", ez - 2.0)
        # Vertical blade orientation
        if ey > 0:
            vsp.SetParmVal(pylon_id, "X_Rel_Rotation", "XForm", 90.0)
        elif ey < 0:
            vsp.SetParmVal(pylon_id, "X_Rel_Rotation", "XForm", -90.0)
        else:
            vsp.SetParmVal(pylon_id, "X_Rel_Rotation", "XForm", 90.0)

        vsp.SetParmVal(pylon_id, "Span", "XSec_1", 2.0)
        vsp.SetParmVal(pylon_id, "Root_Chord", "XSec_1", 4.5)
        vsp.SetParmVal(pylon_id, "Tip_Chord", "XSec_1", 4.0)
        vsp.SetParmVal(pylon_id, "ThickChord", "XSecCurve_0", 0.08)
        vsp.SetParmVal(pylon_id, "ThickChord", "XSecCurve_1", 0.08)
        vsp.SetSetFlag(pylon_id, 3, True)

    # -------------------------------------------------------------------------
    # 3. UNIFIED PASSENGER THEATER CABIN (Internal Deck: 430 Pax)
    # -------------------------------------------------------------------------
    print("---> [Skill 3] Modeling Unified 430-Pax Theater Cabin Deck...")
    design_streamlined_fuselage(
        length=20.0,
        max_diameter=14.0,
        ellipse_height=2.4,
        x_loc=9.0,
        y_loc=0.0,
        z_loc=0.2,
        name="Unified_430Pax_Theater_Cabin",
        geom_set=5 # Set 5 = Internal Systems & Cabin
    )

    # -------------------------------------------------------------------------
    # 4. CRYOGENIC LH2 FUEL TANKS (797.6 m³ Total Sized Volume)
    # -------------------------------------------------------------------------
    print("---> [Skill 3] Packaging 6 Cryogenic Hydrogen Tanks (~798 m³ Sized)...")
    tank_definitions = [
        # (Name, X, Y, Z, Length, Diameter, Approx Volume m³)
        ("LH2_Tank_Outboard_Fwd_Port", 16.0, -11.5, 0.4, 12.5, 3.3),  # ~106.9 m³
        ("LH2_Tank_Outboard_Fwd_Stbd", 16.0,  11.5, 0.4, 12.5, 3.3),  # ~106.9 m³
        ("LH2_Tank_Outboard_Mid_Port", 21.0, -16.0, 0.2, 12.0, 3.1),  # ~90.6 m³
        ("LH2_Tank_Outboard_Mid_Stbd", 21.0,  16.0, 0.2, 12.0, 3.1),  # ~90.6 m³
        ("LH2_Tank_Aft_Core_Port",     30.0,  -3.2, 0.8, 14.0, 4.3),  # ~203.3 m³
        ("LH2_Tank_Aft_Core_Stbd",     30.0,   3.2, 0.8, 14.0, 4.3),  # ~203.3 m³
    ]

    total_tank_vol = 0.0
    for t_name, tx, ty, tz, tlen, td in tank_definitions:
        design_streamlined_fuselage(
            length=tlen,
            max_diameter=td,
            x_loc=tx,
            y_loc=ty,
            z_loc=tz,
            name=t_name,
            geom_set=5 # Set 5 = Internal Systems
        )
        vol_approx = math.pi * ((td / 2.0) ** 2) * (tlen * 0.85) # factoring rounded end domes
        total_tank_vol += vol_approx

    print(f"     Internal Cryogenic Storage Packaged: {total_tank_vol:.1f} m³ (Target: 797.6 m³)")

    # -------------------------------------------------------------------------
    # 5. RETRACTABLE HEAVY-DUTY LANDING GEAR
    # -------------------------------------------------------------------------
    print("---> [Skill 3] Modeling 3-Point Heavy Landing Gear Retraction Struts...")
    gear_definitions = [
        ("Nose_Gear_Strut",        7.0,  0.0, -4.5, 5.0, 1.2),
        ("Main_Gear_Strut_Port",  26.5, -5.8, -4.5, 5.0, 1.8),
        ("Main_Gear_Strut_Stbd",  26.5,  5.8, -4.5, 5.0, 1.8),
    ]
    for g_name, gx, gy, gz, glen, gdia in gear_definitions:
        design_streamlined_fuselage(
            length=glen,
            max_diameter=gdia,
            x_loc=gx,
            y_loc=gy,
            z_loc=gz,
            name=g_name,
            geom_set=6 # Set 6 = Landing Gear
        )

    vsp.Update()

    # -------------------------------------------------------------------------
    # 6. EXPORT CAD FILES (.vsp3, .stl, .obj, CompGeom, MassProps)
    # -------------------------------------------------------------------------
    vsp3_filename = "AETHER_BWB_80m.vsp3"
    stl_filename = "AETHER_BWB_80m.stl"
    stl_oml_filename = "AETHER_BWB_80m_OML.stl"
    stl_internal_filename = "AETHER_BWB_80m_Internal.stl"
    obj_filename = "AETHER_BWB_80m.obj"

    print(f"---> Exporting Native OpenVSP File: {vsp3_filename}...")
    vsp.WriteVSPFile(vsp3_filename)

    print(f"---> Exporting Full Assembly STL: {stl_filename}...")
    vsp.ExportFile(stl_filename, vsp.SET_ALL, vsp.EXPORT_STL)

    print(f"---> Exporting OML Airframe STL: {stl_oml_filename}...")
    vsp.ExportFile(stl_oml_filename, 3, vsp.EXPORT_STL)

    print(f"---> Exporting Internal Cabin & Tank STL: {stl_internal_filename}...")
    vsp.ExportFile(stl_internal_filename, 5, vsp.EXPORT_STL)

    print(f"---> Exporting Textured 3D Mesh OBJ: {obj_filename}...")
    vsp.ExportFile(obj_filename, vsp.SET_ALL, vsp.EXPORT_OBJ)

    # -------------------------------------------------------------------------
    # 7. COMPUTE COMPONENT GEOMETRY & WETTED AREAS
    # -------------------------------------------------------------------------
    print("---> Computing Component Geometry & Planform Areas (CompGeom)...")
    vsp.ComputeCompGeom(vsp.SET_ALL, False, vsp.COMP_GEOM_TXT_TYPE)

    # -------------------------------------------------------------------------
    # 8. AERODYNAMIC EVALUATION AT CRUISE (VSPAERO Skill)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 74)
    print("  [Skill 4] VSPAERO AERODYNAMIC EVALUATION (Mach 0.85 at FL350)")
    print("=" * 74)

    # Re-initialize reference aerodynamic lifting surface for VLM solver
    initialize_aircraft_workspace()
    w_aero = design_aerodynamic_wing(
        span=80.0,
        aspect_ratio=9.50,
        taper_ratio=0.25,
        sweep_deg=33.0,
        tc_ratio=0.11,
        name="AETHER_Aero_Reference",
        geom_set=1
    )

    s_ref = w_aero["area_m2"]
    b_ref = w_aero["span_m"]
    c_ref = w_aero["root_chord_m"]

    alpha_sweep = [1.0, 2.0, 2.7, 3.0, 4.0]
    results_table = []

    print(f"{'Alpha (deg)':<12} | {'Mach':<6} | {'CL':<8} | {'CDtot':<9} | {'CDi':<9} | {'CDo':<9} | {'Wake L/D':<9} | {'CMy':<8}")
    print("-" * 74)

    for alpha in alpha_sweep:
        try:
            res = run_aerodynamic_evaluation(
                alpha_deg=alpha,
                mach=0.85,
                sref=s_ref,
                bref=b_ref,
                cref=c_ref,
                geom_set=1
            )
            results_table.append(res)
            print(f"{res['alpha_deg']:<12.1f} | {res['mach']:<6.2f} | {res['lift_coefficient_CL']:<8.4f} | "
                  f"{res['drag_coefficient_CD']:<9.5f} | {res['induced_drag_CDi']:<9.5f} | "
                  f"{res['parasite_drag_CDo']:<9.5f} | {res['wake_efficiency_L_over_D']:<9.2f} | "
                  f"{res['pitching_moment_CMy']:<8.4f}")
        except Exception as e:
            print(f"Error at alpha {alpha}°: {e}")

    print("=" * 74)
    print("AETHER 80m BWB OpenVSP Model Generation & Aerodynamic Analysis COMPLETE!")
    print(f"Native CAD Model : {os.path.abspath(vsp3_filename)}")
    print(f"STL Surface Mesh : {os.path.abspath(stl_filename)}")
    print(f"OML Surface Mesh : {os.path.abspath(stl_oml_filename)}")
    print(f"Internal Mesh    : {os.path.abspath(stl_internal_filename)}")
    print(f"OBJ 3D Mesh      : {os.path.abspath(obj_filename)}")
    print("=" * 74)

    return {
        "vsp3": os.path.abspath(vsp3_filename),
        "stl_oml": os.path.abspath(stl_oml_filename),
        "aero_results": results_table
    }

if __name__ == "__main__":
    build_aether_bwb_80m()
