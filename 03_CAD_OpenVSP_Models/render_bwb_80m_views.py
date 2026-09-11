#!/usr/bin/env python3
"""
=============================================================================
3D CAD Visualization Script: EXAELIA 80m Blended Wing Body (OpenVSP 3.51.3)
=============================================================================
Course: MMS236 Aircraft Design | Chalmers University of Technology
Parses the generated STL surface mesh and produces 4 engineering perspectives:
1. Isometric 3D Shaded Solid (Overall Blended Airframe, Engines & Winglets)
2. Top View (80.0m Wingspan Code F Planform + Internal Architecture Packaging)
3. Side Elevation (Centerbody Lifting Airfoil Profile & Stand-up Depth)
4. Front Elevation (Spanwise Camber & 70° Canted Winglets)
=============================================================================
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patches as patches

def load_stl_mesh(stl_path):
    if not os.path.exists(stl_path):
        return np.array([])
    triangles = []
    current_tri = []
    with open(stl_path, 'r', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith('vertex'):
                parts = [float(x) for x in line.split()[1:4]]
                current_tri.append(parts)
                if len(current_tri) == 3:
                    triangles.append(current_tri)
                    current_tri = []
    return np.array(triangles)

def compute_face_shading(triangles, base_rgb=(0.14, 0.65, 0.95), light_dir=(0.35, -0.55, 0.75), alpha=0.92, min_intensity=0.25):
    if len(triangles) == 0:
        return np.array([])
    light = np.array(light_dir) / np.linalg.norm(light_dir)
    v0 = triangles[:, 0, :]
    v1 = triangles[:, 1, :]
    v2 = triangles[:, 2, :]
    normals = np.cross(v1 - v0, v2 - v0)
    norm_mag = np.linalg.norm(normals, axis=1, keepdims=True)
    norm_mag[norm_mag == 0] = 1.0
    normals = normals / norm_mag
    
    intensity = np.clip(np.abs(np.dot(normals, light)), min_intensity, 1.0)
    colors = intensity[:, np.newaxis] * np.array(base_rgb)
    colors = np.clip(colors, 0.0, 1.0)
    
    rgba = np.zeros((len(triangles), 4))
    rgba[:, :3] = colors
    rgba[:, 3] = alpha
    return rgba

def render_bwb_80m_views(
    oml_stl="/Users/jakkasaisrinivasamanideep/Documents/MMS236/03_CAD_OpenVSP_Models/EXAELIA_BWB_80m_OML.stl",
    output_img="/Users/jakkasaisrinivasamanideep/Documents/MMS236/03_CAD_OpenVSP_Models/exaelia_bwb_80m_3d_views.png"
):
    print("Loading 3D STL mesh...")
    tris = load_stl_mesh(oml_stl)
    print(f"Loaded OML Mesh: {len(tris)} triangular facets.")

    face_colors = compute_face_shading(tris, base_rgb=(0.15, 0.68, 0.98), light_dir=(0.35, -0.55, 0.75), alpha=0.94)

    fig = plt.figure(figsize=(19, 13.5), dpi=220)
    fig.patch.set_facecolor('#070b14')

    all_pts = tris.reshape(-1, 3)
    min_x, max_x = all_pts[:, 0].min(), all_pts[:, 0].max()
    min_y, max_y = all_pts[:, 1].min(), all_pts[:, 1].max()
    min_z, max_z = all_pts[:, 2].min(), all_pts[:, 2].max()

    mid_x = (max_x + min_x) * 0.5
    mid_y = (max_y + min_y) * 0.5
    mid_z = (max_z + min_z) * 0.5
    max_xy_range = max(max_x - min_x, max_y - min_y) / 2.0

    # -------------------------------------------------------------------------
    # Panel 1: Isometric 3D Solid Shaded Mesh
    # -------------------------------------------------------------------------
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    ax1.set_facecolor('#0d1424')
    
    poly = Poly3DCollection(tris, facecolors=face_colors, edgecolors='#0284c7', linewidth=0.10)
    ax1.add_collection3d(poly)

    ax1.set_xlim(mid_x - max_xy_range*0.75, mid_x + max_xy_range*0.75)
    ax1.set_ylim(mid_y - max_xy_range*0.75, mid_y + max_xy_range*0.75)
    ax1.set_zlim(mid_z - max_xy_range*0.22, mid_z + max_xy_range*0.22)
    ax1.view_init(elev=27, azim=-55)
    ax1.set_title("1. Isometric 3D Solid CAD Model (OpenVSP 3.51.3 Parametric Surface)", 
                  color='#38bdf8', fontsize=11.5, fontweight='bold', pad=8)
    ax1.set_xlabel("X (m) [Longitudinal]", color='#94a3b8', fontsize=8, labelpad=4)
    ax1.set_ylabel("Y (m) [Spanwise]", color='#94a3b8', fontsize=8, labelpad=4)
    ax1.set_zlabel("Z (m) [Vertical]", color='#94a3b8', fontsize=8, labelpad=4)
    ax1.tick_params(colors='#64748b', labelsize=7)
    ax1.xaxis.pane.fill = False
    ax1.yaxis.pane.fill = False
    ax1.zaxis.pane.fill = False
    ax1.grid(True, linestyle=':', alpha=0.25, color='#334155')

    # -------------------------------------------------------------------------
    # Panel 2: Planform (Top View) - 2D Projection with Internal Packaging Overlay
    # -------------------------------------------------------------------------
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.set_facecolor('#0d1424')
    
    # Outer airframe mesh triangles (Top View: Y vs X)
    for tri, col in zip(tris[::2], face_colors[::2]):
        ax2.fill(tri[:, 1], tri[:, 0], color=col[:3], edgecolor='#0284c7', linewidth=0.2, alpha=0.55)

    # Cabin footprint (X = 9.0 to 29.0, Y = -7.0 to +7.0)
    cabin_rect = patches.FancyBboxPatch((-7.0, 9.0), 14.0, 20.0, boxstyle="round,pad=0.3,rounding_size=1.5",
                                        linewidth=1.4, edgecolor='#f43f5e', facecolor='#881337', alpha=0.88, zorder=5)
    ax2.add_patch(cabin_rect)

    # 6 Cryogenic LH2 Tanks
    tanks = [
        # (x, y, dx, dy, name)
        (16.0, -11.5, 3.1, 12.0),
        (16.0,  11.5, 3.1, 12.0),
        (21.0, -16.0, 2.8, 11.0),
        (21.0,  16.0, 2.8, 11.0),
        (30.0,  -3.2, 3.2, 11.5),
        (30.0,   3.2, 3.2, 11.5),
    ]
    for tx, ty, td, tl in tanks:
        tank_rect = patches.FancyBboxPatch((ty - td/2, tx), td, tl, boxstyle="round,pad=0.2,rounding_size=1.0",
                                           linewidth=1.2, edgecolor='#10b981', facecolor='#064e3b', alpha=0.92, zorder=6)
        ax2.add_patch(tank_rect)

    # Twin Turbofan Engines (X = 36.0, Y = ±6.2, L = 7.0, D = 3.4)
    for ey in [-6.2, 6.2]:
        eng_rect = patches.FancyBboxPatch((ey - 1.7, 36.0), 3.4, 7.0, boxstyle="round,pad=0.2,rounding_size=0.8",
                                          linewidth=1.4, edgecolor='#facc15', facecolor='#78350f', alpha=0.95, zorder=7)
        ax2.add_patch(eng_rect)

    ax2.set_aspect('equal', 'box')
    ax2.set_xlim(-44, 44)
    ax2.set_ylim(64, -4)  # Nose at 0, tail at 60
    ax2.set_title("2. Top View: 80.0m Wingspan (ICAO Code F) & Internal Architecture Packaging", 
                  color='#38bdf8', fontsize=11.5, fontweight='bold', pad=8)
    ax2.set_xlabel("Spanwise Y-Coordinate (m) [Wingspan b = 80.0 m]", color='#94a3b8', fontsize=8.5)
    ax2.set_ylabel("Longitudinal X-Coordinate (m) [Length L = 60.0 m]", color='#94a3b8', fontsize=8.5)
    ax2.tick_params(colors='#64748b', labelsize=8)
    ax2.grid(True, linestyle=':', alpha=0.35, color='#334155')
    
    # Legend labels
    ax2.text(0, 19.0, "Unified 430-Pax Theater Deck\n(20.0m × 14.0m × 2.4m)", color='#fdf2f8', fontsize=8, fontweight='bold', ha='center', va='center', zorder=10)
    ax2.text(-15.5, 30.0, "Port LH₂ Tanks\n(2 Cylinders)", color='#6ee7b7', fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=10)
    ax2.text(15.5, 30.0, "Stbd LH₂ Tanks\n(2 Cylinders)", color='#6ee7b7', fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=10)
    ax2.text(0, 35.8, "Aft Core LH₂ Tanks\n(610 m³ Total)", color='#a7f3d0', fontsize=7.5, fontweight='bold', ha='center', va='center', zorder=10)
    ax2.text(0, 48.5, "Twin Geared Turbofans (D = 3.4m, L = 7.0m)\nUpper Deck Acoustic Shielding", color='#fde047', fontsize=7.5, fontweight='bold', ha='center', va='center',
             bbox=dict(boxstyle="round,pad=0.25", fc="#451a03", ec="#f59e0b", alpha=0.85), zorder=10)

    # -------------------------------------------------------------------------
    # Panel 3: Side View (Profile)
    # -------------------------------------------------------------------------
    ax3 = fig.add_subplot(2, 2, 3)
    ax3.set_facecolor('#0d1424')
    for tri, col in zip(tris[::2], face_colors[::2]):
        ax3.fill(tri[:, 0], tri[:, 2], color=col[:3], edgecolor='#0284c7', linewidth=0.2, alpha=0.6)
    
    # Draw engine profile on side view
    eng_side = patches.FancyBboxPatch((36.0, 2.1), 7.0, 3.4, boxstyle="round,pad=0.15,rounding_size=0.6",
                                      linewidth=1.2, edgecolor='#facc15', facecolor='#78350f', alpha=0.95, zorder=7)
    ax3.add_patch(eng_side)

    # Draw cabin profile
    cab_side = patches.Rectangle((9.0, -1.0), 20.0, 2.4, linewidth=1.0, edgecolor='#f43f5e', facecolor='#881337', alpha=0.85, zorder=6)
    ax3.add_patch(cab_side)

    ax3.set_aspect('equal', 'box')
    ax3.set_xlim(-4, 64)
    ax3.set_ylim(-6, 11)
    ax3.set_title("3. Side Elevation: Centerbody Lifting Airfoil (t/c = 19.5%) & Top Engines", 
                  color='#38bdf8', fontsize=11.5, fontweight='bold', pad=8)
    ax3.set_xlabel("Longitudinal X-Coordinate (m)", color='#94a3b8', fontsize=8.5)
    ax3.set_ylabel("Vertical Z-Coordinate (m)", color='#94a3b8', fontsize=8.5)
    ax3.tick_params(colors='#64748b', labelsize=8)
    ax3.grid(True, linestyle=':', alpha=0.35, color='#334155')
    ax3.text(19.0, 0.2, "Cabin Deck (2.4m)", color='#fdf2f8', fontsize=7.5, fontweight='bold', ha='center', zorder=10)
    ax3.text(19.0, 4.5, "Centerbody Depth = 7.41 m", color='#bae6fd', fontsize=8, fontweight='bold', ha='center',
             bbox=dict(boxstyle="round,pad=0.2", fc="#0369a1", ec="#38bdf8", alpha=0.85), zorder=10)
    ax3.text(39.5, 6.2, "Top Nacelle (Aft Deck)", color='#fde047', fontsize=7.5, fontweight='bold', ha='center', zorder=10)

    # -------------------------------------------------------------------------
    # Panel 4: Front View (Dihedral & Canted Winglets)
    # -------------------------------------------------------------------------
    ax4 = fig.add_subplot(2, 2, 4)
    ax4.set_facecolor('#0d1424')
    for tri, col in zip(tris[::2], face_colors[::2]):
        ax4.fill(tri[:, 1], tri[:, 2], color=col[:3], edgecolor='#0284c7', linewidth=0.2, alpha=0.6)
    
    # Draw engine front circles
    for ey in [-6.2, 6.2]:
        eng_front = patches.Circle((ey, 3.8), 1.7, linewidth=1.2, edgecolor='#facc15', facecolor='#78350f', alpha=0.95, zorder=7)
        ax4.add_patch(eng_front)

    ax4.set_aspect('equal', 'box')
    ax4.set_xlim(-44, 44)
    ax4.set_ylim(-6, 11)
    ax4.set_title("4. Front Elevation: Spanwise Camber & 70° Canted Winglets", 
                  color='#38bdf8', fontsize=11.5, fontweight='bold', pad=8)
    ax4.set_xlabel("Spanwise Y-Coordinate (m)", color='#94a3b8', fontsize=8.5)
    ax4.set_ylabel("Vertical Z-Coordinate (m)", color='#94a3b8', fontsize=8.5)
    ax4.tick_params(colors='#64748b', labelsize=8)
    ax4.grid(True, linestyle=':', alpha=0.35, color='#334155')
    ax4.text(-39.0, 6.8, "Port Winglet\n(70° Cant, h = 3.3m)", color='#38bdf8', fontsize=7.5, fontweight='bold', ha='center',
             bbox=dict(boxstyle="round,pad=0.2", fc="#0f172a", ec="#0284c7", alpha=0.85), zorder=10)
    ax4.text(39.0, 6.8, "Stbd Winglet\n(70° Cant, h = 3.3m)", color='#38bdf8', fontsize=7.5, fontweight='bold', ha='center',
             bbox=dict(boxstyle="round,pad=0.2", fc="#0f172a", ec="#0284c7", alpha=0.85), zorder=10)
    ax4.text(0, -2.5, "Centerbody Dihedral: +1.0° | Winglet Cant: 70.0°", color='#94a3b8', fontsize=8, ha='center')

    plt.suptitle('EXAELIA 80m Hydrogen Blended Wing Body (OpenVSP 3.51.3 Parametric CAD Model)\n'
                 'Wingspan: 80.0 m (ICAO Code F Compliant) | Length: 60.0 m | 430 Pax Unified Theater Cabin | 610 m³ Cryotanks',
                 fontsize=13.5, fontweight='bold', color='#f8fafc', y=0.98)

    plt.tight_layout(rect=[0, 0.02, 1, 0.94])
    plt.savefig(output_img, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"[OK] Saved 3D CAD Multi-View: {os.path.abspath(output_img)}")

if __name__ == "__main__":
    render_bwb_80m_views()
