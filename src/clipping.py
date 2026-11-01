"""
Cohen-Sutherland Line Clipping Algorithm against a Rectangular Viewport.
"""
from typing import Tuple, Optional

# Outcodes for 4-bit region coding
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

class CohenSutherland:
    @staticmethod
    def compute_outcode(x: float, y: float, x_min: float, y_min: float, x_max: float, y_max: float) -> int:
        code = INSIDE
        if x < x_min:
            code |= LEFT
        elif x > x_max:
            code |= RIGHT
        if y < y_min:
            code |= BOTTOM
        elif y > y_max:
            code |= TOP
        return code

    @classmethod
    def clip_line(
        cls, x0: float, y0: float, x1: float, y1: float,
        x_min: float, y_min: float, x_max: float, y_max: float
    ) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """
        Clips line segment from (x0, y0) to (x1, y1) against viewport [x_min, y_min, x_max, y_max].
        Returns ((clipped_x0, clipped_y0), (clipped_x1, clipped_y1)) or None if completely outside.
        """
        outcode0 = cls.compute_outcode(x0, y0, x_min, y_min, x_max, y_max)
        outcode1 = cls.compute_outcode(x1, y1, x_min, y_min, x_max, y_max)

        while True:
            # Trivial Accept: both endpoints inside viewport
            if (outcode0 | outcode1) == 0:
                return ((round(x0, 2), round(y0, 2)), (round(x1, 2), round(y1, 2)))

            # Trivial Reject: both endpoints share an outside region
            if (outcode0 & outcode1) != 0:
                return None

            # Calculate intersection point
            outcode_out = outcode0 if outcode0 != 0 else outcode1

            if outcode_out & TOP:
                x = x0 + (x1 - x0) * (y_max - y0) / (y1 - y0)
                y = y_max
            elif outcode_out & BOTTOM:
                x = x0 + (x1 - x0) * (y_min - y0) / (y1 - y0)
                y = y_min
            elif outcode_out & RIGHT:
                y = y0 + (y1 - y0) * (x_max - x0) / (x1 - x0)
                x = x_max
            elif outcode_out & LEFT:
                y = y0 + (y1 - y0) * (x_min - x0) / (x1 - x0)
                x = x_min

            # Update outside point and re-evaluate outcode
            if outcode_out == outcode0:
                x0, y0 = x, y
                outcode0 = cls.compute_outcode(x0, y0, x_min, y_min, x_max, y_max)
            else:
                x1, y1 = x, y
                outcode1 = cls.compute_outcode(x1, y1, x_min, y_min, x_max, y_max)

