"""
Unit tests for PyRenderer 2D rasterization, line clipping, 3D transformations, and Phong shading.
"""
import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rasterizer_2d import bresenham_line, midpoint_circle
from src.clipping import CohenSutherland
from src.transformations_3d import Transform3D
from src.phong_illumination import PhongShader

class TestGraphics(unittest.TestCase):
    def test_bresenham(self):
        pts = bresenham_line(0, 0, 3, 0)
        self.assertEqual(pts, [(0, 0), (1, 0), (2, 0), (3, 0)])

    def test_circle(self):
        pts = midpoint_circle(0, 0, 3)
        self.assertTrue((0, 3) in pts)
        self.assertTrue((3, 0) in pts)

    def test_cohen_sutherland_clipping(self):
        # Line partially overlapping viewport [0..10, 0..10]
        res = CohenSutherland.clip_line(-5, 5, 15, 5, 0, 0, 10, 10)
        self.assertIsNotNone(res)
        self.assertEqual(res, ((0.0, 5.0), (10.0, 5.0)))

        # Line completely outside
        res_out = CohenSutherland.clip_line(15, 15, 20, 20, 0, 0, 10, 10)
        self.assertIsNone(res_out)

    def test_transform_3d(self):
        v = (1.0, 0.0, 0.0)
        v_rot = Transform3D.rotate_y(v, 0.0)
        self.assertAlmostEqual(v_rot[0], 1.0, places=4)

        # Perspective projection
        pt_2d = Transform3D.perspective_project((0.0, 0.0, 1.0), camera_distance=1.0, screen_scale=100.0, screen_center=(50, 50))
        self.assertEqual(pt_2d, (50, 50))

    def test_phong(self):
        n = (0.0, 1.0, 0.0)
        l = (0.0, 1.0, 0.0)
        v = (0.0, 1.0, 0.0)
        i = PhongShader.compute_lighting(n, l, v)
        self.assertTrue(0.5 < i <= 1.0)

if __name__ == "__main__":
    unittest.main()
