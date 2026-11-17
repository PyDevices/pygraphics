# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""A filled polygon draws however many vertices it has (#85), and the same pixels in every build (#93).

The compiled ``poly(..., f=True)`` used to return an empty area and draw nothing
once a polygon passed 256 vertices, while the pure-Python version and the
outline path had no such limit. Each case here fills a polygon and compares the
pixels with a reference scanline fill written in this file, so the compiled
module and the pure package are held to the same picture. The reference walks
the edges the way MicroPython's ``framebuf.poly`` does, last vertex first, so a
filled polygon whose edges cross draws the same pixels as ``framebuf``.
"""

import math
import sys
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


def _flat(pts):
    """Points as a flat ``array('h')``, the form every build accepts."""
    return array("h", [v for p in pts for v in p])


def _div(a, b):
    """Integer division that truncates toward zero, as C does."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def _reference(canvas, pts, col):
    """The scanline fill ``poly`` is defined by, kept independent of ``poly``.

    Each edge runs from one vertex to the one before it, starting with the edge
    from the first vertex to the last, as ``framebuf.poly`` does. The direction
    matters: the node's rounding is taken from the edge's first vertex.
    """
    n = len(pts)
    ys = [p[1] for p in pts]
    for row in range(min(ys), max(ys) + 1):
        nodes = []
        for j in range(n):
            px1, py1 = pts[-j]
            px2, py2 = pts[-j - 1]
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
    def check(self, pts):
        """Fill ``pts`` and compare every pixel with the reference."""
        got = make_fb(w=_SIZE, h=_SIZE)
        got.fill(0)
        area = poly(got, 0, 0, _flat(pts), _WHITE, True)
        want = make_fb(w=_SIZE, h=_SIZE)
        want.fill(0)
        _reference(want, pts, _WHITE)
        drawn, expected = _pixels(got), _pixels(want)
        self.assertEqual(drawn ^ expected, set())
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        self.assertEqual(area, Area(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)))
        return got

    def test_circle_of_300_points_draws(self):
        got = self.check(_circle(300))
        self.assertTrue(count_set(got) > 5000)

    def test_exactly_256_vertices(self):
        self.assertTrue(count_set(self.check(_circle(256))) > 5000)

    def test_257_vertices(self):
        self.assertTrue(count_set(self.check(_circle(257))) > 5000)

    def test_2000_vertices(self):
        self.assertTrue(count_set(self.check(_circle(2000))) > 5000)

    def test_self_intersecting_over_256_vertices(self):
        self.assertTrue(count_set(self.check(_star(301, 120))) > 5000)

    def test_self_intersecting_under_the_old_limit(self):
        self.assertTrue(count_set(self.check(_star(201, 80))) > 5000)

    def test_bow_tie(self):
        self.assertTrue(count_set(self.check([(10, 10), (100, 100), (100, 10), (10, 100)])) > 1000)

    def test_pentagram(self):
        self.assertTrue(count_set(self.check(_star(5, 2))) > 1000)

    def test_other_pentagrams_and_stars(self):
        for n, step in ((7, 3), (9, 4), (11, 5), (13, 5), (31, 12)):
            self.assertTrue(count_set(self.check(_star(n, step))) > 500, (n, step))

    def test_vertex_exactly_on_a_scanline(self):
        # The crossing edges meet at (60, 64), a vertex on row 64 of the fill.
        pts = [(10, 20), (60, 64), (110, 20), (110, 108), (60, 64), (10, 108)]
        self.assertTrue(count_set(self.check(pts)) > 1000)

    def test_horizontal_edge(self):
        pts = [(10, 30), (118, 30), (30, 100), (90, 100), (30, 30)]
        self.assertTrue(count_set(self.check(pts)) > 1000)

    def test_horizontal_edge_in_a_crossing_figure(self):
        pts = [(20, 20), (100, 20), (20, 90), (100, 90), (64, 50), (64, 110)]
        self.assertTrue(count_set(self.check(pts)) > 1000)

    def test_degenerate_line_over_256_vertices(self):
        self.check(_line(300))

    @unittest.skipIf(sys.implementation.name == "micropython", "MicroPython's poly takes a buffer, not a list")
    def test_list_of_300_points(self):
        pts = _circle(300)
        got = make_fb(w=_SIZE, h=_SIZE)
        got.fill(0)
        poly(got, 0, 0, pts, _WHITE, True)
        self.assertEqual(_pixels(got), _pixels(self.check(pts)))


if __name__ == "__main__":
    unittest.main()
