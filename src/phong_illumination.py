"""
Phong Reflection Model: Ambient, Diffuse, and Specular Shading.
"""
import math
from typing import Tuple

class PhongShader:
    @staticmethod
    def compute_lighting(
        normal: Tuple[float, float, float],
        light_dir: Tuple[float, float, float],
        view_dir: Tuple[float, float, float],
        k_a: float = 0.1,
        k_d: float = 0.7,
        k_s: float = 0.5,
        shininess: float = 32.0
    ) -> float:
        """I = I_a*k_a + I_d*k_d*(N . L) + I_s*k_s*(R . V)^n."""
        def dot(v1, v2):
            return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

        # Ambient component
        ambient = k_a

        # Diffuse component
        n_dot_l = max(0.0, dot(normal, light_dir))
        diffuse = k_d * n_dot_l

        # Specular component: R = 2(N . L)N - L
        r = (
            2.0 * n_dot_l * normal[0] - light_dir[0],
            2.0 * n_dot_l * normal[1] - light_dir[1],
            2.0 * n_dot_l * normal[2] - light_dir[2]
        )
        r_dot_v = max(0.0, dot(r, view_dir))
        specular = k_s * (r_dot_v ** shininess) if n_dot_l > 0 else 0.0

        intensity = ambient + diffuse + specular
        return min(1.0, intensity)
