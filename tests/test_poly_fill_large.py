# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""A filled polygon draws however many vertices it has (#85).

The compiled ``poly(..., f=True)`` used to return an empty area and draw nothing
once a polygon passed 256 vertices, while the pure-Python version and the
outline path had no such limit. Each case here fills a polygon and compares the
pixels with a reference scanline fill written in this file, so the compiled
module and the pure package are held to the same picture.
"""

import math
import unittest
from array import array

import _env  # noqa: F401
from _support import count_set, make_fb
from pygraphics import Area, fill_rect, line, pixel, poly

_WHITE = 0xFFFF
_SIZE = 128


def _circle(n, cx=64, cy=64, r=50):
    return [
        (int(cx + r * math.cos(2 * math.pi * i / n)), int(cy + r * math.sin(2 * math.pi * i / n)))
        for i in range(n)
    ]


def _star(n, step):
    """Self-intersecting: every ``step``-th point of an ``n``-point circle."""
    ring = _circle(n)
    return [ring[(i * step) % n] for i in range(n)]


def _line(n):
    """All points on one diagonal, so the polygon has no area."""
    return [(10 + i % 100, 10 + i % 100) for i in range(n)]


def _div(a, b):
    """Integer division that truncates toward zero, as C does."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def _reference(canvas, pts, col):
    """The scanline fill ``poly`` is defined by, kept independent of ``poly``."""
    n = len(pts)
    ys = [p[1] for p in pts]
    for row in range(min(ys), max(ys) + 1):
        nodes = []
        for j in range(n):
            px1, py1 = pts[j]
            px2, py2 = pts[(j + 1) % n]
            if py1 != py2 and ((py1 > row and py2 <= row) or (py1 <= row and py2 > row)):
                nodes.append(_div(32 * px1 + _div(32 * (px2 - px1) * (row - py1), py2 - py1) + 16, 32))
            elif row == max(py1, py2):
                if py1 < py2:
                    pixel(canvas, px2, py2, col)
                elif py2 < py1:
                    pixel(canvas, px1, py1, col)
                else:
                    line(canvas, px1, py1, px2, py2, col)
        nodes.sort()
        for k in range(0, len(nodes) - 1, 2):
            fill_rect(canvas, nodes[k], row, nodes[k + 1] - nodes[k] + 1, 1, col)


def _pixels(canvas):
    return {
        (x, y)
        for y in range(canvas.height)
        for x in range(canvas.width)
        if canvas.pixel(x, y)
    }


class TestLargeFilledPolygon(unittest.TestCase):
    def check(self, pts, tolerance=0.0):
        """Fill ``pts`` and compare with the reference.

        ``tolerance`` is the share of the filled pixels that may differ. It is
        zero except where edges cross: the compiled module walks the edges
        backwards from the pure package, so where they cross the integer
        rounding can land an edge pixel one column over. That holds under 256
        vertices too, so it isn't part of #85.
        """
        got = make_fb(w=_SIZE, h=_SIZE)
        got.fill(0)
        area = poly(got, 0, 0, pts, _WHITE, True)
        want = make_fb(w=_SIZE, h=_SIZE)
        want.fill(0)
        _reference(want, pts, _WHITE)
        drawn, expected = _pixels(got), _pixels(want)
        self.assertLessEqual(len(drawn ^ expected), tolerance * len(expected))
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        self.assertEqual(area, Area(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)))
        return got

    def test_circle_of_300_points_draws(self):
        got = self.check(_circle(300))
        self.assertGreater(count_set(got), 5000)

    def test_exactly_256_vertices(self):
        self.assertGreater(count_set(self.check(_circle(256))), 5000)

    def test_257_vertices(self):
        self.assertGreater(count_set(self.check(_circle(257))), 5000)

    def test_2000_vertices(self):
        self.assertGreater(count_set(self.check(_circle(2000))), 5000)

    def test_self_intersecting_over_256_vertices(self):
        self.assertGreater(count_set(self.check(_star(301, 120), 0.01)), 5000)

    def test_self_intersecting_under_the_old_limit_differs_the_same_way(self):
        self.assertGreater(count_set(self.check(_star(201, 80), 0.01)), 5000)

    def test_degenerate_line_over_256_vertices(self):
        self.check(_line(300))

    def test_flat_array_of_300_points(self):
        pts = _circle(300)
        flat = array("h", [v for p in pts for v in p])
        got = make_fb(w=_SIZE, h=_SIZE)
        got.fill(0)
        poly(got, 0, 0, flat, _WHITE, True)
        self.assertEqual(_pixels(got), _pixels(self.check(pts)))


if __name__ == "__main__":
    unittest.main()
