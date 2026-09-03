#!/usr/bin/env python3
"""
=============================================================================
Airbus A380-800 Parametric Model with Cryogenic Hydrogen (LH2) Tanks
=============================================================================
Built for OpenVSP 3.51.3

Aircraft Specifications:
- Wingspan: 79.75 m
- Wing Area (Sref): 845.0 m²
- Mean Aerodynamic Chord (MAC): 12.1 m
- Fuselage Length: 72.72 m
- Fuselage Width / Height: 7.14 m / 8.40 m (Double-Deck)
- Horizontal Stabilizer Span: 30.4 m
- Vertical Stabilizer Height: 14.5 m
- Engines: 4x High-Bypass Turbofans (GP7200 / Trent 900 Class)

Hydrogen (LH2) System Architecture (Airbus ZEROe A380 Testbed Style):
- 4x Multi-Cylinder Vacuum-Insulated Cryogenic Tanks (20 K / -253 °C) in Aft Fuselage
  * Diameter: 2.2 m each
  * Length: 6.5 m each
  * Internal Usable Volume: ~95 m³ total
  * LH2 Mass Capacity: ~6,700 - 7,400 kg LH2 (density ~71 kg/m³)
- 1x Dorsal Hydrogen Test Engine Pod & Pylon (Upper Aft Fuselage Demonstrator)
=============================================================================
"""

import math
import os
import sys
import openvsp as vsp

def build_a380_hydrogen(output_prefix="A380_Hydrogen"):
    print("=================================================================")
    print("  Generating Airbus A380-800 with Cryogenic LH2 Tanks in OpenVSP")
    print("=================================================================")

    vsp.ClearVSPModel()

    # -------------------------------------------------------------------------
    # 1. DOUBLE-DECK FUSELAGE
    # -------------------------------------------------------------------------
    print("\n[1/6] Building Double-Deck Fuselage...")
    fuse_id = vsp.AddGeom("FUSELAGE", "")
    vsp.SetGeomName(fuse_id, "Fuselage_DoubleDeck")
    vsp.SetParmVal(fuse_id, "Length", "Design", 72.72)
    vsp.SetParmVal(fuse_id, "Tess_W", "Shape", 49)
    vsp.SetGeomMaterialName(fuse_id, "White")

    # Access Fuselage Cross-Sections
    fuse_xsurf = vsp.GetXSecSurf(fuse_id, 0)
    num_xsecs = vsp.GetNumXSec(fuse_xsurf)

    # Set cross-sections to ellipses with A380 double deck proportions
    # XSec 0: Nose point (X=0%)
    # XSec 1: Cockpit / Forward Cabin (X=10%)
    # XSec 2: Constant Cabin Section (X=45%) - Width: 7.14m, Height: 8.40m
    # XSec 3: Aft Cabin / Tank Section (X=75%) - Width: 6.80m, Height: 7.80m
    # XSec 4: Tail cone (X=100%)
    for i in range(1, num_xsecs - 1):
        vsp.ChangeXSecShape(fuse_xsurf, i, vsp.XS_ELLIPSE)
        xsec = vsp.GetXSec(fuse_xsurf, i)
        w_p = vsp.GetXSecParm(xsec, "Ellipse_Width")
        h_p = vsp.GetXSecParm(xsec, "Ellipse_Height")
        xloc_p = vsp.GetXSecParm(xsec, "XLocPercent")

        if i == 1:
            vsp.SetParmVal(xloc_p, 0.12)
            vsp.SetParmVal(w_p, 5.80)
            vsp.SetParmVal(h_p, 6.80)
        elif i == 2:
            vsp.SetParmVal(xloc_p, 0.50)
            vsp.SetParmVal(w_p, 7.14)
            vsp.SetParmVal(h_p, 8.40)
        elif i == 3:
            vsp.SetParmVal(xloc_p, 0.82)
            vsp.SetParmVal(w_p, 5.20)
            vsp.SetParmVal(h_p, 6.20)

    # -------------------------------------------------------------------------
    # 2. MAIN WING (Supercritical, Transonic, Multi-Section)
    # -------------------------------------------------------------------------
    print("[2/6] Building Main Wing (Span: 79.75m, Sref: 845m²)...")
    wing_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(wing_id, "MainWing")
    vsp.SetParmVal(wing_id, "X_Rel_Location", "XForm", 24.50)
    vsp.SetParmVal(wing_id, "Y_Rel_Location", "XForm", 0.0)
    vsp.SetParmVal(wing_id, "Z_Rel_Location", "XForm", -1.80)
    vsp.SetParmVal(wing_id, "RotateAirfoilMatchDideralFlag", "WingGeom", 1.0)
    vsp.SetGeomMaterialName(wing_id, "Aluminum")

    # Inboard + Outboard Section Setup
    wing_xsurf = vsp.GetXSecSurf(wing_id, 0)
    # Default wing has 1 section (XSec 0 to 1). Let's configure it with exact A380 geometry
    xsec1 = vsp.GetXSec(wing_xsurf, 1)

    span_p = vsp.GetXSecParm(xsec1, "Span")
    sweep_p = vsp.GetXSecParm(xsec1, "Sweep")
    dih_p = vsp.GetXSecParm(xsec1, "Dihedral")
    root_p = vsp.GetXSecParm(xsec1, "Root_Chord")
    tip_p = vsp.GetXSecParm(xsec1, "Tip_Chord")

    # Half span = 39.875 m, Root chord = 17.5 m, Tip chord = 3.8 m, Sweep = 33.5 deg, Dihedral = 5.5 deg
    vsp.SetParmVal(span_p, 39.875)
    vsp.SetParmVal(sweep_p, 33.50)
    vsp.SetParmVal(dih_p, 5.50)
    vsp.SetParmVal(root_p, 17.50)
    vsp.SetParmVal(tip_p, 3.80)

    # Airfoil thickness / camber (Supercritical profile approximation)
    for curve_idx in [0, 1]:
        camber_p = vsp.GetParm(wing_id, "Camber", f"XSecCurve_{curve_idx}")
        thick_p = vsp.GetParm(wing_id, "ThickChord", f"XSecCurve_{curve_idx}")
        if camber_p:
            vsp.SetParmVal(camber_p, 0.022)
        if thick_p:
            vsp.SetParmVal(thick_p, 0.125 if curve_idx == 0 else 0.095)

    # -------------------------------------------------------------------------
    # 3. EMPENNAGE (Horizontal & Vertical Stabilizers)
    # -------------------------------------------------------------------------
    print("[3/6] Building Empennage (Horizontal & Vertical Tails)...")
    # Horizontal Stabilizer
    ht_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(ht_id, "HorizontalStabilizer")
    vsp.SetParmVal(ht_id, "X_Rel_Location", "XForm", 62.50)
    vsp.SetParmVal(ht_id, "Z_Rel_Location", "XForm", 4.20)
    vsp.SetGeomMaterialName(ht_id, "Aluminum")

    ht_surf = vsp.GetXSecSurf(ht_id, 0)
    ht_xsec1 = vsp.GetXSec(ht_surf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Span"), 15.20) # Total span: 30.4m
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Sweep"), 34.50)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Dihedral"), 6.00)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Root_Chord"), 9.50)
    vsp.SetParmVal(vsp.GetXSecParm(ht_xsec1, "Tip_Chord"), 3.90)

    # Vertical Stabilizer
    vt_id = vsp.AddGeom("WING", "")
    vsp.SetGeomName(vt_id, "VerticalStabilizer")
    vsp.SetParmVal(vt_id, "X_Rel_Location", "XForm", 51.50)
    vsp.SetParmVal(vt_id, "Z_Rel_Location", "XForm", 3.80)
    vsp.SetParmVal(vt_id, "X_Rel_Rotation", "XForm", 90.0) # Vertical orientation
    vsp.SetParmVal(vt_id, "Sym_Planar_Flag", "Sym", vsp.SYM_NONE)
    vsp.SetGeomMaterialName(vt_id, "Blue Plastic")

    vt_surf = vsp.GetXSecSurf(vt_id, 0)
    vt_xsec1 = vsp.GetXSec(vt_surf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Span"), 14.50) # Height: 14.5m
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Sweep"), 40.00)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Dihedral"), 0.0)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Root_Chord"), 12.00)
    vsp.SetParmVal(vsp.GetXSecParm(vt_xsec1, "Tip_Chord"), 4.50)

    # -------------------------------------------------------------------------
    # 4. WING-MOUNTED TURBOFAN ENGINES & PYLONS (4x Engines)
    # -------------------------------------------------------------------------
    print("[4/6] Adding 4x High-Bypass Turbofan Engines & Pylons...")
    # Inboard Engines (Y = +/- 15.5 m)
    eng_inboard = vsp.AddGeom("POD", "")
    vsp.SetGeomName(eng_inboard, "Inboard_Engines")
    vsp.SetParmVal(eng_inboard, "Sym_Planar_Flag", "Sym", vsp.SYM_XZ)
    vsp.SetParmVal(eng_inboard, "Length", "Design", 7.00)
    vsp.SetParmVal(eng_inboard, "FineRatio", "Design", 7.00 / 1.90) # Diameter: 3.80m
    vsp.SetParmVal(eng_inboard, "X_Rel_Location", "XForm", 28.50)
    vsp.SetParmVal(eng_inboard, "Y_Rel_Location", "XForm", 15.50)
    vsp.SetParmVal(eng_inboard, "Z_Rel_Location", "XForm", -3.60)
    vsp.SetGeomMaterialName(eng_inboard, "Chrome")

    # Inboard Pylons
    pylon_inboard = vsp.AddGeom("WING", "")
    vsp.SetGeomName(pylon_inboard, "Inboard_Pylons")
    vsp.SetParmVal(pylon_inboard, "Sym_Planar_Flag", "Sym", vsp.SYM_XZ)
    vsp.SetParmVal(pylon_inboard, "X_Rel_Location", "XForm", 29.50)
    vsp.SetParmVal(pylon_inboard, "Y_Rel_Location", "XForm", 15.50)
    vsp.SetParmVal(pylon_inboard, "Z_Rel_Location", "XForm", -3.60)
    vsp.SetParmVal(pylon_inboard, "X_Rel_Rotation", "XForm", 90.0)
    pylon_in_surf = vsp.GetXSecSurf(pylon_inboard, 0)
    pylon_in_x1 = vsp.GetXSec(pylon_in_surf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(pylon_in_x1, "Span"), 2.20)
    vsp.SetParmVal(vsp.GetXSecParm(pylon_in_x1, "Root_Chord"), 6.00)
    vsp.SetParmVal(vsp.GetXSecParm(pylon_in_x1, "Tip_Chord"), 5.00)
    vsp.SetGeomMaterialName(pylon_inboard, "White")

    # Outboard Engines (Y = +/- 26.5 m)
    eng_outboard = vsp.AddGeom("POD", "")
    vsp.SetGeomName(eng_outboard, "Outboard_Engines")
    vsp.SetParmVal(eng_outboard, "Sym_Planar_Flag", "Sym", vsp.SYM_XZ)
    vsp.SetParmVal(eng_outboard, "Length", "Design", 7.00)
    vsp.SetParmVal(eng_outboard, "FineRatio", "Design", 7.00 / 1.90) # Diameter: 3.80m
    vsp.SetParmVal(eng_outboard, "X_Rel_Location", "XForm", 34.50)
    vsp.SetParmVal(eng_outboard, "Y_Rel_Location", "XForm", 26.50)
    vsp.SetParmVal(eng_outboard, "Z_Rel_Location", "XForm", -2.60)
    vsp.SetGeomMaterialName(eng_outboard, "Chrome")

    # Outboard Pylons
    pylon_outboard = vsp.AddGeom("WING", "")
    vsp.SetGeomName(pylon_outboard, "Outboard_Pylons")
    vsp.SetParmVal(pylon_outboard, "Sym_Planar_Flag", "Sym", vsp.SYM_XZ)
    vsp.SetParmVal(pylon_outboard, "X_Rel_Location", "XForm", 35.50)
    vsp.SetParmVal(pylon_outboard, "Y_Rel_Location", "XForm", 26.50)
    vsp.SetParmVal(pylon_outboard, "Z_Rel_Location", "XForm", -2.60)
    vsp.SetParmVal(pylon_outboard, "X_Rel_Rotation", "XForm", 90.0)
    pylon_out_surf = vsp.GetXSecSurf(pylon_outboard, 0)
    pylon_out_x1 = vsp.GetXSec(pylon_out_surf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(pylon_out_x1, "Span"), 2.00)
    vsp.SetParmVal(vsp.GetXSecParm(pylon_out_x1, "Root_Chord"), 5.50)
    vsp.SetParmVal(vsp.GetXSecParm(pylon_out_x1, "Tip_Chord"), 4.50)
    vsp.SetGeomMaterialName(pylon_outboard, "White")

    # -------------------------------------------------------------------------
    # 5. CRYOGENIC LIQUID HYDROGEN (LH2) TANKS & ZEROe TEST ENGINE POD
    # -------------------------------------------------------------------------
    print("[5/6] Integrating Cryogenic LH2 Tanks & ZEROe Hydrogen Testbed Pod...")
    # Tank Dimensions: Length = 6.60m, Diameter = 2.20m each (Radius = 1.10m)
    # FineRatio = Length / Radius = 6.60 / 1.10 = 6.00

    # Upper Pair of Cryogenic LH2 Tanks (Port & Starboard)
    lh2_upper = vsp.AddGeom("POD", "")
    vsp.SetGeomName(lh2_upper, "LH2_CryoTanks_Upper")
    vsp.SetParmVal(lh2_upper, "Sym_Planar_Flag", "Sym", vsp.SYM_XZ)
    vsp.SetParmVal(lh2_upper, "Length", "Design", 6.60)
    vsp.SetParmVal(lh2_upper, "FineRatio", "Design", 6.00)
    vsp.SetParmVal(lh2_upper, "X_Rel_Location", "XForm", 46.50)
    vsp.SetParmVal(lh2_upper, "Y_Rel_Location", "XForm", 1.35)
    vsp.SetParmVal(lh2_upper, "Z_Rel_Location", "XForm", 1.25)
    vsp.SetGeomMaterialName(lh2_upper, "Cyan Plastic")

    # Lower Pair of Cryogenic LH2 Tanks (Port & Starboard)
    lh2_lower = vsp.AddGeom("POD", "")
    vsp.SetGeomName(lh2_lower, "LH2_CryoTanks_Lower")
    vsp.SetParmVal(lh2_lower, "Sym_Planar_Flag", "Sym", vsp.SYM_XZ)
    vsp.SetParmVal(lh2_lower, "Length", "Design", 6.60)
    vsp.SetParmVal(lh2_lower, "FineRatio", "Design", 6.00)
    vsp.SetParmVal(lh2_lower, "X_Rel_Location", "XForm", 46.50)
    vsp.SetParmVal(lh2_lower, "Y_Rel_Location", "XForm", 1.35)
    vsp.SetParmVal(lh2_lower, "Z_Rel_Location", "XForm", -1.25)
    vsp.SetGeomMaterialName(lh2_lower, "Cyan Plastic")

    # ZEROe Dorsal Hydrogen Engine Test Pod (Mounted on Aft Fuselage)
    zeroe_pod = vsp.AddGeom("POD", "")
    vsp.SetGeomName(zeroe_pod, "ZEROe_Hydrogen_Engine_Pod")
    vsp.SetParmVal(zeroe_pod, "Length", "Design", 5.20)
    vsp.SetParmVal(zeroe_pod, "FineRatio", "Design", 5.20 / 1.15) # Diameter: 2.30m
    vsp.SetParmVal(zeroe_pod, "X_Rel_Location", "XForm", 55.00)
    vsp.SetParmVal(zeroe_pod, "Y_Rel_Location", "XForm", 0.00)
    vsp.SetParmVal(zeroe_pod, "Z_Rel_Location", "XForm", 5.30)
    vsp.SetGeomMaterialName(zeroe_pod, "Cyan Plastic")

    # Dorsal Pylon
    zeroe_pylon = vsp.AddGeom("WING", "")
    vsp.SetGeomName(zeroe_pylon, "ZEROe_Dorsal_Pylon")
    vsp.SetParmVal(zeroe_pylon, "X_Rel_Location", "XForm", 56.00)
    vsp.SetParmVal(zeroe_pylon, "Y_Rel_Location", "XForm", 0.00)
    vsp.SetParmVal(zeroe_pylon, "Z_Rel_Location", "XForm", 3.80)
    vsp.SetParmVal(zeroe_pylon, "X_Rel_Rotation", "XForm", 90.0)
    zeroe_pylon_surf = vsp.GetXSecSurf(zeroe_pylon, 0)
    zeroe_pylon_x1 = vsp.GetXSec(zeroe_pylon_surf, 1)
    vsp.SetParmVal(vsp.GetXSecParm(zeroe_pylon_x1, "Span"), 1.60)
    vsp.SetParmVal(vsp.GetXSecParm(zeroe_pylon_x1, "Root_Chord"), 4.20)
    vsp.SetParmVal(vsp.GetXSecParm(zeroe_pylon_x1, "Tip_Chord"), 3.20)
    vsp.SetGeomMaterialName(zeroe_pylon, "White")

    # -------------------------------------------------------------------------
    # 6. MODEL UPDATE, VOLUME ESTIMATION & FILE EXPORT
    # -------------------------------------------------------------------------
    print("[6/6] Finalizing Model Geometry & Exporting Assets...")
    vsp.Update()

    # Geometry Reference Quantities
    sref = vsp.GetParmVal(wing_id, "TotalArea", "WingGeom")
    bref = vsp.GetParmVal(wing_id, "TotalSpan", "WingGeom")
    cref = sref / bref
    print(f"\n---> Aerodynamic References:")
    print(f"     Sref (Wing Area) : {sref:.2f} m²")
    print(f"     bref (Wingspan)  : {bref:.2f} m")
    print(f"     cref (MAC)       : {cref:.2f} m")

    # Hydrogen Tank Calculations
    tank_radius = 1.10 # m
    tank_length = 6.60 # m
    # Single tank volume (Cylinder + 2 hemispherical caps)
    cyl_vol = math.pi * (tank_radius**2) * (tank_length - 2 * tank_radius)
    caps_vol = (4.0 / 3.0) * math.pi * (tank_radius**3)
    single_tank_vol = cyl_vol + caps_vol
    total_4tanks_vol = 4 * single_tank_vol
    lh2_density = 71.0 # kg/m3 (liquid hydrogen at 20 K)
    total_lh2_mass = total_4tanks_vol * lh2_density

    # Energy equivalence to Jet-A kerosene
    # LH2 LHV = 120 MJ/kg; Jet-A LHV = 42.8 MJ/kg (factor: ~2.8x)
    equivalent_jeta_mass = total_lh2_mass * (120.0 / 42.8)

    print(f"\n---> Cryogenic Liquid Hydrogen (LH2) Storage Capacity:")
    print(f"     Number of Tanks       : 4 (Isolated Aft Fuselage Bay)")
    print(f"     Single Tank Volume    : {single_tank_vol:.2f} m³")
    print(f"     Total Cryo Volume     : {total_4tanks_vol:.2f} m³")
    print(f"     Usable LH2 Capacity   : {total_lh2_mass:.1f} kg (~{total_lh2_mass/1000:.2f} tonnes)")
    print(f"     Energy Equivalent Mass: {equivalent_jeta_mass:.1f} kg Jet-A Kerosene")

    # Save VSP3 model
    vsp3_filename = f"{output_prefix}.vsp3"
    vsp.WriteVSPFile(vsp3_filename, vsp.SET_ALL)
    print(f"\n[OK] Saved OpenVSP Model: {os.path.abspath(vsp3_filename)}")

    # Export STL Mesh
    stl_filename = f"{output_prefix}.stl"
    vsp.ExportFile(stl_filename, vsp.SET_ALL, vsp.EXPORT_STL)
    print(f"[OK] Exported 3D STL Mesh: {os.path.abspath(stl_filename)}")

    # Export OBJ Mesh
    obj_filename = f"{output_prefix}.obj"
    vsp.ExportFile(obj_filename, vsp.SET_ALL, vsp.EXPORT_OBJ)
    print(f"[OK] Exported 3D OBJ Mesh: {os.path.abspath(obj_filename)}")

    print("\n=================================================================")
    print("  A380 Hydrogen Model Construction Completed Successfully!")
    print("=================================================================")
    return vsp3_filename

if __name__ == "__main__":
    build_a380_hydrogen()
