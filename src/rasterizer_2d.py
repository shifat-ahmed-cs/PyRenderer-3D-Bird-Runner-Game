"""
Fundamental 2D Graphics Algorithms: Bresenham's Line and Midpoint Circle.
"""
from typing import List, Tuple

def bresenham_line(x0: int, y0: int, x1: int, y1: int) -> List[Tuple[int, int]]:
    """Bresenham's line algorithm handling all octants."""
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    x, y = x0, y0
    while True:
        points.append((x, y))
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy
    return points

def midpoint_circle(cx: int, cy: int, radius: int) -> List[Tuple[int, int]]:
    """Midpoint 8-way symmetric circle generation."""
    points = []
    x = 0
    y = radius
    d = 1 - radius

    def add_octants(x, y):
        pts = [
            (cx + x, cy + y), (cx - x, cy + y), (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x), (cx + y, cy - x), (cx - y, cy - x)
        ]
        points.extend(pts)

    add_octants(x, y)
    while x < y:
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
        add_octants(x, y)
    return points
