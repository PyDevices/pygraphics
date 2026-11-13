# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Tests that blit_rect clips to the canvas on every implementation."""

import unittest

import _env  # noqa: F401
from pygraphics import RGB565, Area, FrameBuffer

WIDTH = 8
HEIGHT = 6


def blit(x, y, w, h):
    """Blit a rectangle whose pixels count 1, 2, 3 ... and return (area, pixels)."""
    fb = FrameBuffer(bytearray(WIDTH * HEIGHT * 2), WIDTH, HEIGHT, RGB565)
    buf = bytearray()
    for i in range(w * h):
        buf += bytes((i + 1, 0))
    area = fb.blit_rect(buf, x, y, w, h)
    pixels = {}
    for row in range(HEIGHT):
        for col in range(WIDTH):
            value = fb.pixel(col, row)
            if value:
                pixels[(col, row)] = value
    return area, pixels


class TestBlitRectClip(unittest.TestCase):
    def test_inside_is_unchanged(self):
        area, pixels = blit(2, 1, 2, 2)
        self.assertEqual(area, Area(2, 1, 2, 2))
        self.assertEqual(pixels, {(2, 1): 1, (3, 1): 2, (2, 2): 3, (3, 2): 4})

    def test_off_the_left_drops_the_left_columns_of_the_source(self):
        area, pixels = blit(-2, 1, 4, 2)
        self.assertEqual(area, Area(-2, 1, 4, 2))
        self.assertEqual(pixels, {(0, 1): 3, (1, 1): 4, (0, 2): 7, (1, 2): 8})

    def test_off_the_right_drops_the_right_columns_of_the_source(self):
        area, pixels = blit(WIDTH - 2, 1, 4, 2)
        self.assertEqual(area, Area(WIDTH - 2, 1, 4, 2))
        self.assertEqual(pixels, {(6, 1): 1, (7, 1): 2, (6, 2): 5, (7, 2): 6})

    def test_off_the_top_drops_the_top_rows_of_the_source(self):
        _, pixels = blit(0, -1, 3, 3)
        self.assertEqual(pixels, {(c, r): 4 + r * 3 + c for r in range(2) for c in range(3)})

    def test_off_the_bottom_drops_the_bottom_rows_of_the_source(self):
        _, pixels = blit(2, HEIGHT - 2, 3, 4)
        self.assertEqual(pixels, {(2 + c, HEIGHT - 2 + r): 1 + r * 3 + c for r in range(2) for c in range(3)})

    def test_off_every_side_keeps_the_middle(self):
        _, pixels = blit(-1, -1, WIDTH + 2, HEIGHT + 2)
        self.assertEqual(len(pixels), WIDTH * HEIGHT)
        self.assertEqual(pixels[(0, 0)], (WIDTH + 2) + 2)

    def test_fully_off_draws_nothing_and_still_returns_the_area(self):
        for x, y in ((-9, 0), (WIDTH, 0), (0, -9), (0, HEIGHT), (20, 20)):
            area, pixels = blit(x, y, 2, 2)
            self.assertEqual(pixels, {}, (x, y))
            self.assertEqual(area, Area(x, y, 2, 2), (x, y))


if __name__ == "__main__":
    unittest.main()
