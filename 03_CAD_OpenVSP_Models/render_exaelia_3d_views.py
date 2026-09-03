#!/usr/bin/env python3
"""
=============================================================================
3D CAD Visualization Script for EXAELIA Hydrogen Aircraft Model (DT2)
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Parses the generated STL mesh and renders multi-view engineering perspectives:
1. Isometric 3D Perspective
2. Top View (Planform)
3. Side View (Fuselage Profile & LH2 Bay)
4. Front View (Dihedral & Engine Placement)
=============================================================================
"""

import os
import struct
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def load_stl_mesh(stl_path):
    """Parses binary or ASCII STL into a list of triangles."""
    with open(stl_path, 'rb') as f:
        header = f.read(80)
        num_triangles_bytes = f.read(4)
        if len(num_triangles_bytes) == 4:
            num_triangles = struct.unpack('<I', num_triangles_bytes)[0]
            # Check if valid binary STL
            expected_size = 84 + num_triangles * 50
            f.seek(0, 2)
            actual_size = f.tell()
            if actual_size == expected_size:
                f.seek(84)
                triangles = []
                for _ in range(num_triangles):
                    data = f.read(50)
                    if len(data) < 50:
                        break
                    # normal(3f), v1(3f), v2(3f), v3(3f), attr(h)
                    floats = struct.unpack('<12f', data[:48])
                    v1 = floats[3:6]
                    v2 = floats[6:9]
                    v3 = floats[9:12]
                    triangles.append([v1, v2, v3])
                return np.array(triangles)
                
    # Fallback to ASCII parser
    triangles = []
    with open(stl_path, 'r', errors='ignore') as f:
        lines = f.readlines()
    current_tri = []
    for line in lines:
        line = line.strip()
        if line.startswith('vertex'):
            parts = [float(x) for x in line.split()[1:]]
            current_tri.append(parts)
            if len(current_tri) == 3:
                triangles.append(current_tri)
                current_tri = []
    return np.array(triangles)

def render_exaelia_views(stl_file="EXAELIA_Hydrogen_DT2.stl", output_img="exaelia_hydrogen_3d_views.png"):
    print(f"Parsing 3D STL mesh from {stl_file}...")
    tris = load_stl_mesh(stl_file)
    print(f"Loaded {len(tris)} triangular facets.")

    # Downsample if needed for smooth plotting
    target_facets = 7000
    step = max(1, len(tris) // target_facets)
    sampled_tris = tris[::step]

    fig = plt.figure(figsize=(16, 12), dpi=160)
    fig.patch.set_facecolor('#0b0f19')

    titles = ['Isometric 3D Perspective', 'Top View (Planform: Sref=363.4m², Span=58.8m)', 'Side View (Fuselage: 68.5m & 596.6m³ LH2 Bay)', 'Front View (Dihedral & 4x LH2 Turbofans)']
    views = [(28, -55), (90, -90), (0, -90), (0, 0)]

    for idx, (elev, azim) in enumerate(views):
        ax = fig.add_subplot(2, 2, idx + 1, projection='3d')
        ax.set_facecolor('#111827')
        
        # Facet collection with edge shading
        poly = Poly3DCollection(sampled_tris, alpha=0.85, edgecolor='#0284c7', linewidth=0.20)
        poly.set_facecolor('#38bdf8')
        ax.add_collection3d(poly)

        # Compute bounding box
        all_pts = sampled_tris.reshape(-1, 3)
        min_x, max_x = all_pts[:, 0].min(), all_pts[:, 0].max()
        min_y, max_y = all_pts[:, 1].min(), all_pts[:, 1].max()
        min_z, max_z = all_pts[:, 2].min(), all_pts[:, 2].max()

        max_range = max(max_x - min_x, max_y - min_y, max_z - min_z) / 2.0
        mid_x = (max_x + min_x) * 0.5
        mid_y = (max_y + min_y) * 0.5
        mid_z = (max_z + min_z) * 0.5

        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)

        ax.view_init(elev=elev, azim=azim)
        ax.set_title(titles[idx], color='#f8fafc', fontsize=12, fontweight='bold', pad=10)
        ax.tick_params(colors='#94a3b8', labelsize=8)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.grid(True, linestyle=':', alpha=0.3, color='#334155')

    plt.suptitle('EXAELIA Long-Range Hydrogen Aircraft (MMS236 Design Task 2)\n'
                 '430 Pax | 12,500 km | 4x LH2 Turbofans | 4x Cryotanks (596.6 m³, L/D=4.0) | OpenVSP 3.51.3 CAD',
                 fontsize=14, fontweight='bold', color='#f8fafc', y=0.98)

    plt.tight_layout(rect=[0, 0.03, 1, 0.94])
    plt.savefig(output_img, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Saved 3D CAD Multi-View: {os.path.abspath(output_img)}")

if __name__ == "__main__":
    stl_path = "EXAELIA_Hydrogen_DT2.stl"
    out_img = "exaelia_hydrogen_3d_views.png"
    if os.path.exists(stl_path):
        render_exaelia_views(stl_path, out_img)
    else:
        print(f"Error: {stl_path} not found.")
