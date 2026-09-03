# MMS236 Aircraft Design Workspace
## Chalmers University of Technology — EXAELIA Long-Range Hydrogen Aircraft Project

**Student:** Sai Srinivasa Manideep Jakka (ID: `111923`)  
**Course:** MMS236 Aircraft Design (Canvas ID: `40847`)  
**Lecturers:** Christian Svensson, Carlos Xisto  

---

### 📂 Directory Structure

```text
MMS236/
├── 01_Course_Materials/          # PDF lecture slides, syllabus & kick-off project briefs
│   ├── MMS236 Aircraft Design Kick-off.pdf
│   ├── lec2.pdf                  # Sizing & Constraint Analysis equations
│   └── lec3.pdf                  # Conceptual layout, cabin & landing gear
│
├── 02_Design_Task_1_Sizing/      # DT1 Sizing loop, constraint diagram & report
│   ├── dt1_sizing_matching.py    # Python sizing & constraint matching engine
│   ├── dt1_sizing_report.md      # Full technical sizing report
│   └── dt1_constraint_diagram.png # High-res T/W vs W/S matching chart
│
├── 03_CAD_OpenVSP_Models/        # OpenVSP 3D CAD parametric models & renders
│   ├── build_a380_hydrogen.py    # OpenVSP parametric geometry builder
│   ├── render_3d_views.py        # Multi-view CAD rendering engine
│   ├── A380_Hydrogen.vsp3        # Native OpenVSP project file
│   ├── A380_Hydrogen.stl         # 3D triangular surface mesh
│   ├── A380_Hydrogen.obj         # Wavefront 3D mesh format
│   └── a380_hydrogen_3d_views.png# 3D orthographic multi-view visual
│
├── 04_Aerodynamic_Simulations/   # VSPAERO vortex lattice / panel solver & polars
│   ├── run_simulation.py         # Automated MassProp & VSPAERO solver pipeline
│   ├── A380_Hydrogen.polar       # Aerodynamic polar table (CL, CD, CS, L/D, CM)
│   ├── A380_Hydrogen.vspaero     # Solver run configuration
│   ├── a380_hydrogen_aerodynamic_polars.png # Aerodynamic curves & drag polar
│   └── raw_solver_data/          # ADB, case matrices, and mesh slices
│
└── 05_Tools_and_Environment/     # Virtual environment, OpenVSP binaries & MCP server
    ├── venv/                     # Python 3.13 dedicated environment
    ├── openvsp_bin/              # Native OpenVSP 3.51.3 ARM64 binaries
    ├── OpenVSP3Plugin/           # NASA OpenMDAO plugin repository
    └── canvas-mcp/               # Canvas LMS MCP Server integration
```

---

### 🚀 Quick Execution Commands

Activate the dedicated Python environment:
```bash
source 05_Tools_and_Environment/venv/bin/activate
```

Run Design Task 1 Sizing & Constraint Matching:
```bash
python3 02_Design_Task_1_Sizing/dt1_sizing_matching.py
```

Build / Regenerate the 3D OpenVSP Airframe Model:
```bash
python3 03_CAD_OpenVSP_Models/build_a380_hydrogen.py
```

Run Aerodynamic Simulations (VSPAERO):
```bash
python3 04_Aerodynamic_Simulations/run_simulation.py
```

Launch the OpenVSP GUI:
```bash
05_Tools_and_Environment/openvsp_bin/OpenVSP-3.51.3-MacOS/vsp 03_CAD_OpenVSP_Models/A380_Hydrogen.vsp3 &
```
