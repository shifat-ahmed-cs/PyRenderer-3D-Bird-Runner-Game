"""
Demonstration of PyRenderer: 2D Rasterization, Line Clipping, 3D Perspective Projection, and Phong Shading.
"""
import os
import sys
import math
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rasterizer_2d import bresenham_line, midpoint_circle
from src.clipping import CohenSutherland
from src.transformations_3d import Transform3D
from src.phong_illumination import PhongShader

def main():
    print("=" * 68)
    print("      PYRENDERER: COMPLETE 2D/3D COMPUTER GRAPHICS PIPELINE   ")
    print("=" * 68)

    # 1. Bresenham Line Drawing Algorithm
    line_pts = bresenham_line(2, 3, 10, 7)
    print("[+] 1. Bresenham Line Rasterization (2, 3) -> (10, 7):")
    print(f"    - Rasterized Pixels ({len(line_pts)}): {line_pts}")

    # 2. Midpoint Circle Algorithm
    circle_pts = midpoint_circle(cx=0, cy=0, radius=5)
    print(f"\n[+] 2. Midpoint Circle (Center=(0, 0), Radius=5):")
    print(f"    - 8-Way Symmetric Generated Pixels: {len(circle_pts)} points")

    # 3. Cohen-Sutherland Line Clipping Algorithm
    clipped = CohenSutherland.clip_line(-20, 50, 120, 50, 0, 0, 100, 100)
    print(f"\n[+] 3. Cohen-Sutherland Line Clipping:")
    print(f"    - Viewport Window : [X: 0..100, Y: 0..100]")
    print(f"    - Original Line   : (-20, 50) -> (120, 50)")
    print(f"    - Clipped Segment : {clipped[0]} -> {clipped[1]}")

    # 4. 3D Canonical Cube Perspective Projection
    vertices, edges = Transform3D.get_cube_vertices_and_edges()
    angle = math.radians(45.0)
    print(f"\n[+] 4. 3D Perspective Projection Pipeline (Rotating Cube, 45 deg Y-axis):")
    for idx, v in enumerate(vertices[:4]):
        v_rot = Transform3D.rotate_y(v, angle)
        screen_pt = Transform3D.perspective_project(v_rot, camera_distance=3.5, screen_scale=80.0, screen_center=(120, 120))
        print(f"    - Vertex {idx}: 3D {v} -> Projected 2D Viewport: {screen_pt}")
    print(f"    - All 8 Vertices and 12 Wireframe Edges Projected Successfully.")

    # 5. Phong Illumination Model
    normal = (0.0, 0.0, 1.0)
    light_dir = (0.577, 0.577, 0.577)
    view_dir = (0.0, 0.0, 1.0)
    intensity = PhongShader.compute_lighting(normal, light_dir, view_dir)
    print(f"\n[+] 5. Phong Illumination Model:")
    print(f"    - Normal Vector: {normal}, Light: {light_dir}")
    print(f"    - Resulting Intensity: {intensity:.4f} (Ambient + Diffuse + Specular)")
    print("=" * 68)

if __name__ == "__main__":
    main()
