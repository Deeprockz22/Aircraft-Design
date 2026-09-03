#!/usr/bin/env python3
"""
=============================================================================
3D CAD Visualization Script for Airbus A380 Hydrogen Model
=============================================================================
Parses the generated STL mesh and renders multi-view engineering perspectives:
1. Isometric 3D Perspective
2. Top View (Planform)
3. Side View (Fuselage Profile & Dorsal Pod)
4. Front View (Dihedral & Engine Placement)
=============================================================================
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def parse_stl(stl_file):
    """Parses binary or ASCII STL into a list of triangular facet vertices."""
    triangles = []
    with open(stl_file, 'r', errors='ignore') as f:
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

def render_3d_views(stl_file="A380_Hydrogen.stl", output_img="a380_hydrogen_3d_views.png"):
    print(f"Parsing 3D STL mesh from {stl_file}...")
    tris = parse_stl(stl_file)
    print(f"Loaded {len(tris)} triangular facets.")

    # Downsample if needed for smooth plotting
    step = max(1, len(tris) // 6000)
    sampled_tris = tris[::step]

    fig = plt.figure(figsize=(16, 12), dpi=150)
    fig.patch.set_facecolor('#0b0f19')

    titles = ['Isometric 3D View', 'Top View (Planform)', 'Side View (Fuselage & LH2 Bay)', 'Front View (Dihedral & Engines)']
    views = [(28, -55), (90, -90), (0, -90), (0, 0)]

    for idx, (elev, azim) in enumerate(views):
        ax = fig.add_subplot(2, 2, idx + 1, projection='3d')
        ax.set_facecolor('#111827')
        
        # Color coding facets
        poly = Poly3DCollection(sampled_tris, alpha=0.85, edgecolor='#0284c7', linewidth=0.25)
        poly.set_facecolor('#38bdf8')
        ax.add_collection3d(poly)

        # Scale limits
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
        ax.set_title(titles[idx], color='#f8fafc', fontsize=13, fontweight='bold', pad=12)
        ax.tick_params(colors='#94a3b8', labelsize=8)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.grid(True, linestyle=':', alpha=0.3, color='#334155')

    plt.suptitle('Airbus A380-800 Cryogenic Liquid Hydrogen ($LH_2$) Demonstrator\n'
                 'Parametric 3D CAD Geometry Generated via OpenVSP 3.51.3 API',
                 fontsize=15, fontweight='bold', color='#f8fafc', y=0.98)

    plt.tight_layout(rect=[0, 0.03, 1, 0.94])
    plt.savefig(output_img, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Saved 3D CAD Multi-View: {output_img}")

if __name__ == "__main__":
    render_3d_views()
