"""
3D Geometric Transformations and Perspective Projection Engine.
"""
import math
from typing import List, Tuple

class Transform3D:
    @staticmethod
    def rotate_y(point: Tuple[float, float, float], angle_rad: float) -> Tuple[float, float, float]:
        """Rotates point around Y axis."""
        x, y, z = point
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        x_new = x * cos_a + z * sin_a
        z_new = -x * sin_a + z * cos_a
        return (x_new, y, z_new)

    @staticmethod
    def rotate_x(point: Tuple[float, float, float], angle_rad: float) -> Tuple[float, float, float]:
        """Rotates point around X axis."""
        x, y, z = point
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        y_new = y * cos_a - z * sin_a
        z_new = y * sin_a + z * cos_a
        return (x, y_new, z_new)

    @staticmethod
    def perspective_project(
        point: Tuple[float, float, float],
        camera_distance: float = 3.0,
        screen_scale: float = 100.0,
        screen_center: Tuple[int, int] = (100, 100)
    ) -> Tuple[int, int]:
        """
        Projects 3D point (x, y, z) into 2D viewport coordinates using perspective division:
        x_screen = (x / (z + d)) * scale + cx
        y_screen = (y / (z + d)) * scale + cy
        """
        x, y, z = point
        denom = z + camera_distance
        if denom <= 0.1:
            denom = 0.1  # Prevent division by zero / clipping behind camera
        proj_x = (x / denom) * screen_scale + screen_center[0]
        proj_y = (-y / denom) * screen_scale + screen_center[1]  # Invert Y for screen raster
        return int(round(proj_x)), int(round(proj_y))

    @classmethod
    def get_cube_vertices_and_edges(cls) -> Tuple[List[Tuple[float, float, float]], List[Tuple[int, int]]]:
        """Returns the 8 vertices and 12 connecting edges of a canonical 3D cube."""
        vertices = [
            (-1.0, -1.0, -1.0),
            ( 1.0, -1.0, -1.0),
            ( 1.0,  1.0, -1.0),
            (-1.0,  1.0, -1.0),
            (-1.0, -1.0,  1.0),
            ( 1.0, -1.0,  1.0),
            ( 1.0,  1.0,  1.0),
            (-1.0,  1.0,  1.0),
        ]
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),  # Back face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Front face
            (0, 4), (1, 5), (2, 6), (3, 7)   # Interconnecting side edges
        ]
        return vertices, edges

