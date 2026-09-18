#!/usr/bin/env python3
"""
=============================================================================
AETHER OpenVSP Parametric Design Skills Library
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Group:  13 - AETHER 80m Liquid Hydrogen Blended Wing Body (BWB)

This module provides reusable OpenVSP 3.51.3 agent skills with engineering
guardrails for parametric conceptual aircraft design:
1. initialize_aircraft_workspace: Resets and initializes OpenVSP session.
2. design_aerodynamic_wing: Builds parametric wing surface from ratios.
3. design_bwb_multisection_surface: Builds multi-section blended wing body airframe.
4. design_streamlined_fuselage: Generates low-drag streamlined bodies (cabin, tanks, nacelles).
5. run_aerodynamic_evaluation: Runs VSPAERO aerodynamic evaluation at specified Alpha and Mach.
=============================================================================
"""

import math
import os
import sys

# Ensure OpenVSP binaries (vspaero, vspscript, etc.) are in PATH
vsp_bin_paths = [
    "/Users/jakkasaisrinivasamanideep/Documents/MMS236/05_Tools_and_Environment/openvsp_bin/OpenVSP-3.51.3-MacOS",
    "/Users/jakkasaisrinivasamanideep/.gemini/antigravity-ide/scratch/openvsp_bin/OpenVSP-3.51.3-MacOS"
]
for p in vsp_bin_paths:
    if os.path.exists(p) and p not in os.environ.get("PATH", ""):
        os.environ["PATH"] = p + ":" + os.environ.get("PATH", "")

import openvsp as vsp

def initialize_aircraft_workspace():
    """
    Skill: Resets the OpenVSP environment and sets up the base coordinate grid.
    Returns: Confirmation message.
    """
    vsp.ClearVSPModel()
    vsp.Update()
    return "OpenVSP canvas cleared and initialized successfully."

def design_aerodynamic_wing(span: float, aspect_ratio: float, taper_ratio: float, sweep_deg: float,
                            dihedral_deg: float = 0.0, tc_ratio: float = 0.12,
                            name: str = "Aerodynamic_Wing", geom_set: int = 3):
    """
    Skill: Generates an optimized parametric lifting surface.
    Calculates root/tip chords dynamically based on aspect ratio to ensure physical realism.
    
    Guardrails:
    - aspect_ratio > 0
    - 0 < taper_ratio <= 1.0
    - span > 0
    """
    # 1. Enforce Engineering Constraints
    if span <= 0:
        raise ValueError(f"Invalid wingspan: {span} m. Span must be positive.")
    if aspect_ratio <= 0:
        raise ValueError(f"Invalid aspect ratio: {aspect_ratio}. AR must be positive.")
    if taper_ratio <= 0 or taper_ratio > 1.0:
        raise ValueError(f"Invalid taper ratio: {taper_ratio}. Taper ratio must be between 0 and 1.0.")

    # 2. Derive engineering dimensions from ratios
    area = (span ** 2) / aspect_ratio
    mean_chord = area / span
    root_chord = (2.0 * mean_chord) / (1.0 + taper_ratio)
    tip_chord = root_chord * taper_ratio
    semi_span = span / 2.0

    # 3. Inject into OpenVSP
    wing_id = vsp.AddGeom("WING")
    vsp.SetGeomName(wing_id, name)

    # Set driver parameters on XSec_1
    vsp.SetParmVal(wing_id, "Span", "XSec_1", semi_span)
    vsp.SetParmVal(wing_id, "Root_Chord", "XSec_1", root_chord)
    vsp.SetParmVal(wing_id, "Tip_Chord", "XSec_1", tip_chord)
    vsp.SetParmVal(wing_id, "Sweep", "XSec_1", sweep_deg)
    vsp.SetParmVal(wing_id, "Dihedral", "XSec_1", dihedral_deg)

    # Set airfoil thickness-to-chord
    vsp.SetParmVal(wing_id, "ThickChord", "XSecCurve_0", tc_ratio)
    vsp.SetParmVal(wing_id, "ThickChord", "XSecCurve_1", tc_ratio)

    if geom_set is not None:
        vsp.SetSetFlag(wing_id, geom_set, True)

    vsp.Update()

    return {
        "geom_id": wing_id,
        "name": name,
        "span_m": span,
        "semi_span_m": semi_span,
        "area_m2": round(area, 2),
        "aspect_ratio": aspect_ratio,
        "taper_ratio": taper_ratio,
        "root_chord_m": round(root_chord, 2),
        "tip_chord_m": round(tip_chord, 2),
        "sweep_deg": sweep_deg,
        "dihedral_deg": dihedral_deg,
        "status": f"Wing '{name}' created successfully."
    }

def design_bwb_multisection_surface(sections: list, name: str = "AETHER_BWB_Airframe", geom_set: int = 3):
    """
    Skill: Generates a multi-section Blended Wing Body lifting surface.
    
    sections format:
    List of dicts for each section (starting from section 1):
    [
        {"span": 8.0, "root_chord": 38.0, "tip_chord": 26.0, "sweep": 38.0, "dihedral": 1.0, "tc_root": 0.195, "tc_tip": 0.195},
        {"span": 12.0, "tip_chord": 10.0, "sweep": 42.0, "dihedral": 2.0, "tc_tip": 0.145},
        {"span": 18.8, "tip_chord": 3.5, "sweep": 33.0, "dihedral": 3.0, "tc_tip": 0.115},
        {"span": 3.5, "tip_chord": 1.6, "sweep": 45.0, "dihedral": 70.0, "tc_tip": 0.090}
    ]
    """
    if len(sections) < 1:
        raise ValueError("At least one section must be specified for BWB airframe.")

    bwb_id = vsp.AddGeom("WING")
    vsp.SetGeomName(bwb_id, name)

    # Insert additional cross sections
    num_additional_sections = len(sections) - 1
    for i in range(num_additional_sections):
        vsp.InsertXSec(bwb_id, i + 1, vsp.XS_FOUR_SERIES)

    # Apply parameters section by section
    total_projected_span = 0.0
    for idx, s in enumerate(sections):
        sec_num = idx + 1
        sec_tag = f"XSec_{sec_num}"
        curve_tag = f"XSecCurve_{sec_num}"

        vsp.SetParmVal(bwb_id, "Span", sec_tag, s["span"])
        if "root_chord" in s:
            vsp.SetParmVal(bwb_id, "Root_Chord", sec_tag, s["root_chord"])
        if "tip_chord" in s:
            vsp.SetParmVal(bwb_id, "Tip_Chord", sec_tag, s["tip_chord"])
        if "sweep" in s:
            vsp.SetParmVal(bwb_id, "Sweep", sec_tag, s["sweep"])
        if "dihedral" in s:
            vsp.SetParmVal(bwb_id, "Dihedral", sec_tag, s["dihedral"])
            dihedral_rad = math.radians(s["dihedral"])
            total_projected_span += s["span"] * math.cos(dihedral_rad)
        else:
            total_projected_span += s["span"]

        if idx == 0 and "tc_root" in s:
            vsp.SetParmVal(bwb_id, "ThickChord", "XSecCurve_0", s["tc_root"])
        if "tc_tip" in s:
            vsp.SetParmVal(bwb_id, "ThickChord", curve_tag, s["tc_tip"])

    if geom_set is not None:
        vsp.SetSetFlag(bwb_id, geom_set, True)

    vsp.Update()

    return {
        "geom_id": bwb_id,
        "name": name,
        "num_sections": len(sections),
        "total_wingspan_m": round(total_projected_span * 2.0, 2),
        "status": f"BWB Multi-Section Surface '{name}' created successfully with span {total_projected_span * 2.0:.1f} m."
    }

def design_streamlined_fuselage(length: float, max_diameter: float,
                                x_loc: float = 0.0, y_loc: float = 0.0, z_loc: float = 0.0,
                                ellipse_height: float = None, name: str = "Fuselage",
                                geom_set: int = 3):
    """
    Skill: Generates a baseline streamlined body with high-fineness ratio for low drag.
    Used for passenger cabin, cryogenic tanks, and engine nacelles.
    
    Guardrails:
    - length > 0
    - max_diameter > 0
    - Checks fineness ratio (length / max_diameter)
    """
    if length <= 0 or max_diameter <= 0:
        raise ValueError("Length and max_diameter must be strictly positive.")

    fineness_ratio = length / max_diameter
    height = ellipse_height if ellipse_height is not None else max_diameter

    fuse_id = vsp.AddGeom("FUSELAGE")
    vsp.SetGeomName(fuse_id, name)

    # Set overall length and position
    vsp.SetParmVal(fuse_id, "Length", "Design", length)
    vsp.SetParmVal(fuse_id, "X_Location", "XForm", x_loc)
    vsp.SetParmVal(fuse_id, "Y_Location", "XForm", y_loc)
    vsp.SetParmVal(fuse_id, "Z_Location", "XForm", z_loc)

    # Scale cross sections
    for i in [1, 2, 3]:
        vsp.SetParmVal(fuse_id, "Ellipse_Width", f"XSecCurve_{i}", max_diameter)
        vsp.SetParmVal(fuse_id, "Ellipse_Height", f"XSecCurve_{i}", height)

    if geom_set is not None:
        vsp.SetSetFlag(fuse_id, geom_set, True)

    vsp.Update()

    return {
        "geom_id": fuse_id,
        "name": name,
        "length_m": length,
        "width_m": max_diameter,
        "height_m": height,
        "fineness_ratio": round(fineness_ratio, 2),
        "position": (x_loc, y_loc, z_loc),
        "status": f"Streamlined body '{name}' created successfully (fineness: {fineness_ratio:.2f})."
    }

def run_aerodynamic_evaluation(alpha_deg: float, mach: float,
                               sref: float = None, bref: float = None, cref: float = None,
                               geom_set: int = 3):
    """
    Skill: Runs a VSPAERO analysis on the current setup to evaluate performance.
    Returns: Lift Coefficient (CLtot), Drag Coefficients (CDtot, CDi, CDo), and Efficiency (L/D).
    """
    # 1. Compute VSPAERO degenerate surface mesh
    mesh_analysis = "VSPAEROComputeGeometry"
    vsp.SetAnalysisInputDefaults(mesh_analysis)
    vsp.SetIntAnalysisInput(mesh_analysis, "GeomSet", [geom_set])
    vsp.ExecAnalysis(mesh_analysis)

    # 2. Setup VSPAERO Solver Sweep for single point evaluation
    solver_analysis = "VSPAEROSweep"
    vsp.SetAnalysisInputDefaults(solver_analysis)
    vsp.SetIntAnalysisInput(solver_analysis, "GeomSet", [geom_set])
    vsp.SetDoubleAnalysisInput(solver_analysis, "AlphaStart", [alpha_deg])
    vsp.SetDoubleAnalysisInput(solver_analysis, "AlphaEnd", [alpha_deg])
    vsp.SetIntAnalysisInput(solver_analysis, "AlphaNpts", [1])
    vsp.SetDoubleAnalysisInput(solver_analysis, "MachStart", [mach])
    vsp.SetDoubleAnalysisInput(solver_analysis, "MachEnd", [mach])
    vsp.SetIntAnalysisInput(solver_analysis, "MachNpts", [1])

    if sref is not None:
        vsp.SetDoubleAnalysisInput(solver_analysis, "Sref", [sref])
    if bref is not None:
        vsp.SetDoubleAnalysisInput(solver_analysis, "bref", [bref])
    if cref is not None:
        vsp.SetDoubleAnalysisInput(solver_analysis, "cref", [cref])

    # 3. Execute solver
    res_id = vsp.ExecAnalysis(solver_analysis)

    # 4. Extract polar results from child Result ID
    child_ids = vsp.GetStringResults(res_id, "ResultsVec")
    if not child_ids:
        raise RuntimeError("VSPAERO failed to produce result containers.")

    polar_cid = child_ids[0]
    data_names = vsp.GetAllDataNames(polar_cid)
    cl = vsp.GetDoubleResults(polar_cid, "CLtot")[-1]
    cd_tot = vsp.GetDoubleResults(polar_cid, "CDtot")[-1]
    cd_i = vsp.GetDoubleResults(polar_cid, "CDi")[-1]
    cd_o = vsp.GetDoubleResults(polar_cid, "CDo")[-1]
    cm_y = vsp.GetDoubleResults(polar_cid, "CMytot")[-1]
    l_over_d = cl / cd_tot if cd_tot > 0 else 0.0

    cl_wake = vsp.GetDoubleResults(polar_cid, "CLiw")[-1] if "CLiw" in data_names else cl
    cd_wake = vsp.GetDoubleResults(polar_cid, "CDiw")[-1] if "CDiw" in data_names else cd_i
    ld_wake = vsp.GetDoubleResults(polar_cid, "LoDwake")[-1] if "LoDwake" in data_names else l_over_d

    return {
        "alpha_deg": alpha_deg,
        "mach": mach,
        "lift_coefficient_CL": round(cl, 4),
        "drag_coefficient_CD": round(cd_tot, 5),
        "induced_drag_CDi": round(cd_i, 5),
        "parasite_drag_CDo": round(cd_o, 5),
        "pitching_moment_CMy": round(cm_y, 4),
        "efficiency_L_over_D": round(l_over_d, 2),
        "wake_lift_CLiw": round(cl_wake, 4),
        "wake_induced_CDiw": round(cd_wake, 5),
        "wake_efficiency_L_over_D": round(ld_wake, 2),
    }

if __name__ == "__main__":
    print("Testing AETHER OpenVSP Skills Library...")
    msg = initialize_aircraft_workspace()
    print("1.", msg)

    wing_res = design_aerodynamic_wing(span=80.0, aspect_ratio=9.5, taper_ratio=0.25, sweep_deg=33.0)
    print("2.", wing_res)

    fuse_res = design_streamlined_fuselage(length=20.0, max_diameter=14.0, ellipse_height=2.4, name="TestCabin")
    print("3.", fuse_res)

    print("Skills library self-test completed successfully.")
