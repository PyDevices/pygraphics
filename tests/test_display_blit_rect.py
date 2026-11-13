# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Tests that blits into a display driver use its blit_rect, not pixel()."""

import unittest

import _env  # noqa: F401
from pygraphics import RGB565, Area, Draw, FrameBuffer, blit_rect, blit_transparent


class Display:
    """A display driver shape: pixel and fill_rect, plus a blit_rect that
    paints whole rectangles. Counts the calls each path takes."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = {}
        self.pixel_calls = 0
        self.blit_calls = 0

    def pixel(self, x, y, c):
        self.pixel_calls += 1
        self.pixels[(x, y)] = c

    def fill_rect(self, x, y, w, h, c):
        for row in range(y, y + h):
            for col in range(x, x + w):
                self.pixel(col, row, c)

    def blit_rect(self, buf, x, y, w, h):
        self.blit_calls += 1
        data = bytes(buf)
        if len(data) != w * h * 2:
            raise ValueError("buffer is not w*h*2 bytes")
        for row in range(h):
            for col in range(w):
                i = (row * w + col) * 2
                value = data[i] | (data[i + 1] << 8)
                if 0 <= x + col < self.width and 0 <= y + row < self.height:
                    self.pixels[(x + col, y + row)] = value


def counting(w, h):
    """A packed RGB565 rectangle whose pixels count 1, 2, 3 ..."""
    buf = bytearray()
    for i in range(w * h):
        buf += bytes((i + 1, 0))
    return buf


class TestDisplayBlitRect(unittest.TestCase):
    def test_blit_rect_is_one_call(self):
        display = Display(8, 6)
        area = blit_rect(display, counting(3, 2), 1, 2, 3, 2)
        self.assertEqual(area, Area(1, 2, 3, 2))
        self.assertEqual(display.blit_calls, 1)
        self.assertEqual(display.pixel_calls, 0)
        self.assertEqual(display.pixels, {(1 + c, 2 + r): 1 + r * 3 + c for r in range(2) for c in range(3)})

    def test_draw_blit_rect_is_one_call(self):
        display = Display(8, 6)
        Draw(display).blit_rect(counting(2, 2), 0, 0, 2, 2)
        self.assertEqual(display.blit_calls, 1)
        self.assertEqual(display.pixel_calls, 0)

    def test_draw_blit_of_a_framebuffer_uses_blit_rect(self):
        src = FrameBuffer(counting(4, 3), 4, 3, RGB565)
        display = Display(8, 6)
        area = Draw(display).blit(src, 6, 1)
        self.assertEqual(area, Area(6, 1, 2, 3))
        self.assertEqual(display.pixel_calls, 0)
        self.assertGreater(display.blit_calls, 0)
        self.assertEqual(display.pixels, {(6 + c, 1 + r): 1 + r * 4 + c for r in range(3) for c in range(2)})

    def test_blit_transparent_skips_the_key_through_blit_rect(self):
        buf = bytearray(b"\x05\x00\x00\x00\x07\x00")
        display = Display(8, 6)
        blit_transparent(display, buf, 0, 0, 3, 1, 0)
        self.assertEqual(display.pixel_calls, 0)
        self.assertEqual(display.pixels, {(0, 0): 5, (2, 0): 7})


if __name__ == "__main__":
    unittest.main()
