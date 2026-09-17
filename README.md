# AETHER — 80m Liquid Hydrogen Blended Wing Body Transport

**Chalmers University of Technology**  
Department of Mechanics and Maritime Sciences  
**Course:** MMS236 Aircraft Design (Design Task 1)  
**Group:** 13  
**Aircraft Name:** AETHER  

---

## Overview

**AETHER** is a conceptual 80-meter wingspan, zero-emission liquid hydrogen (LH₂) blended wing body (BWB) commercial transport engineered for Entry-Into-Service (EIS) in 2050. By integrating the lifting fuselage, passenger cabin, and cryogenic storage into a single continuous aerodynamic surface, AETHER achieves long-haul intercontinental reach with zero carbon emissions.

```
       ___________________________________________
      /                                           \
     /       [ A E T H E R   B W B - 8 0 M ]       \
    /      430 Pax  •  12,500 km  •  Mach 0.85      \
   /_________________________________________________\
   \===\                                         /===/
        \=======================================/
```

---

## Key Performance Specifications

| Parameter | Value | Reference / Notes |
|---|---|---|
| **Design Range** | **12,500 km** (6,750 nm) | Long-haul intercontinental missions |
| **Cruise Speed** | **Mach 0.85** (252 m/s TAS) | FL350 (10,668 m ISA conditions) |
| **Passenger Capacity** | **430 passengers** | 3-class single-deck theater cabin layout |
| **Cargo Capacity** | **10,750 kg** (44 LD3 containers) | Lower deck cargo bay |
| **Maximum Take-Off Weight (MTOW)** | **275,017 kg** (275.02 t) | Converged via iterative weight sizing |
| **Operating Empty Weight (OEW)** | **170,004 kg** (170.00 t) | 120.0 t airframe + 50.0 t cryotanks |
| **Mission Fuel (LH₂)** | **50,004 kg** (50.00 t) | 18.18% mission fuel fraction (Breguet) |
| **Cryogenic Storage Volume** | **774.7 m³** | 6 vacuum-insulated tanks (10% ullage) |
| **Aerodynamic Efficiency (L/D)** | **17.75 cruise / 20.50 loiter** | Aspect ratio 9.50, Oswald e = 0.85 |
| **Engine SFC (LH₂ Cruise)** | **4.779 mg/(N·s)** | Converted from 13.4 mg/(N·s) Jet-A baseline |

---

## Mass Breakdown

```
Take-Off Weight: 275.02 tonnes
├── Operating Empty Weight (OEW): 170.00 t (61.8%)
│   ├── Baseline Airframe & Systems: 120.00 t (43.6%)
│   └── Cryotanks (Gi = 0.50):        50.00 t (18.2%)
├── Usable Fuel (Liquid Hydrogen):   50.00 t (18.2%)
├── Payload (430 Pax + Cargo):        53.75 t (19.5%)
└── Flight & Cabin Crew (12 crew):     1.26 t  (0.5%)
```

---

## Quick Start: Running the Sizing Model

The primary sizing model runs with zero external dependencies using Python's standard library:

```bash
python3 dt1_sizing.py
```

### Expected Output
```text
AETHER LH2 BWB - Sizing Results
--------------------------------------------------
MTOW                  :  275017.3 kg  (275.02 t)
Operating Empty (OEW) :  170003.6 kg  (170.00 t)
  - Baseline Airframe :  120000.0 kg  (120.00 t)
  - Cryotanks (Gi=0.5):   50003.6 kg  ( 50.00 t)
Mission Fuel (LH2)    :   50003.6 kg  ( 50.00 t)
Payload (430 Pax)     :   53750.0 kg  ( 53.75 t)
Crew (12)             :    1260.0 kg  (  1.26 t)
Cryotank Volume       :     774.7 m3  (liquid: 704.3 m3)
--------------------------------------------------
Sizing Loop           : Converged in 16 iterations from 220.0 t
LH2 Cruise SFC        : 4.779 mg/(N*s)
Cruise fuel burn      : 12.24%
Total fuel fraction   : 18.18%
```

---

## Repository Structure

```text
Aircraft-Design/
├── README.md                          # Project documentation
├── dt1_sizing.py                      # Master aircraft sizing script
├── 01_Course_Materials/               # Chalmers MMS236 lectures & reference textbooks
│   ├── MMS236 Aircraft Design Kick-off.pdf
│   ├── lec2.pdf
│   ├── lec3.pdf
│   └── Aircraft Design A Conceptual Approach 6th Edition - Daniel P Raymer.pdf
├── 02_Design_Task_1_Sizing/           # Sizing loop scripts and fuel fraction calculations
│   └── dt1_sizing.py
├── 03_CAD_OpenVSP_Models/             # Parametric 3D CAD files (OpenVSP 3.51.3)
│   ├── build_exaelia_bwb_80m.py
│   ├── EXAELIA_BWB_80m.vsp3
│   └── EXAELIA_BWB_80m_OML.stl
├── 04_Presentation_Assets/            # Aerodynamic polars, cabin drawings, renders
├── 06_Overleaf_Report/                # Full LaTeX report source
└── Aircraft_Design_DT1_EXAELIA_Group13.pptx # Presentation deck
```

---

## Key Design Principles

1. **Tailless Pitch Stability**: Neutral point is at ~25% Mean Aerodynamic Chord (MAC). The 6 cryogenic fuel tanks are balanced symmetrically around the aircraft CG to minimize CG excursion throughout the flight envelope.
2. **Span Loading Alleviation**: Cryogenic tanks positioned along the inner wing and centerbody relieve wing root bending moments, reducing overall airframe structural weight.
3. **Airport Gate Compatibility**: Fits within standard ICAO Code F 80 × 80 meter airport gate boxes.
