# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Tests for ``pygraphics.FrameBuffer`` (the ``_framebuf_plus`` wrapper).

This is the ``FrameBuffer`` exported from the package. Unlike the bare
``framebuf`` base class, every drawing method returns an `pygraphics.Area`
bounding box and the buffer/format/color_depth are exposed as properties.
"""

import unittest

import _env  # noqa: F401
from _support import make_fb
from pygraphics import (
    GS2_HMSB,
    GS4_HMSB,
    GS8,
    MONO_HLSB,
    MONO_HMSB,
    MONO_VLSB,
    RGB565,
    RGB888,
    Area,
    FrameBuffer,
)

_DEPTHS = {
    MONO_VLSB: 1,
    MONO_HLSB: 1,
    MONO_HMSB: 1,
    RGB565: 16,
    GS2_HMSB: 2,
    GS4_HMSB: 4,
    GS8: 8,
}


class TestProperties(unittest.TestCase):
    def test_dimensions_and_format(self):
        buffer = bytearray(20 * 10 * 2)
        fb = FrameBuffer(buffer, 20, 10, RGB565)
        self.assertEqual(fb.width, 20)
        self.assertEqual(fb.height, 10)
        self.assertEqual(fb.format, RGB565)
        self.assertIs(fb.buffer, buffer)

    def test_color_depth_for_each_format(self):
        for fmt, depth in _DEPTHS.items():
            with self.subTest(format=fmt):
                fb = make_fb(fmt, 8, 8)
                self.assertEqual(fb.color_depth, depth)

    def test_invalid_format_raises(self):
        with self.assertRaises(ValueError):
            FrameBuffer(bytearray(64), 4, 4, 99)


class TestMethodsReturnArea(unittest.TestCase):
    def setUp(self):
        self.fb = make_fb(RGB565, 16, 16)

    def test_fill_returns_area(self):
        self.assertEqual(self.fb.fill(0), Area(0, 0, 16, 16))

    def test_fill_rect_returns_area(self):
        self.assertEqual(self.fb.fill_rect(2, 3, 4, 5, 0xFFFF), Area(2, 3, 4, 5))

    def test_pixel_set_returns_area(self):
        self.assertEqual(self.fb.pixel(1, 1, 0xFFFF), Area(1, 1, 1, 1))

    def test_pixel_get_returns_int(self):
        self.fb.pixel(1, 1, 0x1234)
        self.assertEqual(self.fb.pixel(1, 1), 0x1234)

    def test_hline_returns_area(self):
        self.assertEqual(self.fb.hline(0, 0, 5, 0xFFFF), Area(0, 0, 5, 1))

    def test_vline_returns_area(self):
        self.assertEqual(self.fb.vline(0, 0, 5, 0xFFFF), Area(0, 0, 1, 5))

    def test_rect_returns_area(self):
        self.assertEqual(self.fb.rect(1, 1, 5, 6, 0xFFFF), Area(1, 1, 5, 6))

    def test_line_returns_area(self):
        self.assertIsInstance(self.fb.line(0, 0, 5, 5, 0xFFFF), Area)

    def test_ellipse_returns_area(self):
        self.assertEqual(self.fb.ellipse(8, 8, 3, 2, 0xFFFF), Area(5, 6, 6, 4))

    def test_blit_returns_area(self):
        src = make_fb(RGB565, 4, 4)
        src.fill(0xABCD)
        self.assertEqual(self.fb.blit(src, 2, 2), Area(2, 2, 4, 4))
        self.assertEqual(self.fb.pixel(2, 2), 0xABCD)

    def test_blit_same_format_copies_rows(self):
        # Same format with no key or palette takes the row-copy path: whole
        # frames, offsets and every clipped edge must match the pixel loop.
        for fmt, bpp in ((RGB565, 2), (GS8, 1), (RGB888, 3)):
            for sw, sh, x, y in ((16, 16, 0, 0), (5, 4, 3, 2), (6, 5, -2, -1), (6, 5, 13, 12), (20, 3, -2, 4)):
                src_buf = bytearray(sw * sh * bpp)
                for i in range(len(src_buf)):
                    src_buf[i] = (i * 7 + 13) & 0xFF
                dst_buf = bytearray(16 * 16 * bpp)
                src = FrameBuffer(src_buf, sw, sh, fmt)
                dst = FrameBuffer(dst_buf, 16, 16, fmt)
                area = dst.blit(src, x, y)
                x0, y0 = max(0, x), max(0, y)
                x1, y1 = min(16, x + sw), min(16, y + sh)
                self.assertEqual(area, Area(x0, y0, x1 - x0, y1 - y0))
                want = bytearray(16 * 16 * bpp)
                for row in range(y0, y1):
                    for col in range(x0, x1):
                        s = ((row - y) * sw + (col - x)) * bpp
                        d = (row * 16 + col) * bpp
                        want[d : d + bpp] = src_buf[s : s + bpp]
                self.assertEqual(bytes(dst_buf), bytes(want), (fmt, sw, sh, x, y))

    def test_blit_tuple_source_returns_area(self):
        # MicroPython's framebuf.blit takes (buffer, width, height, format).
        buf = bytearray(b"\xcd\xab" * 12)
        self.assertEqual(self.fb.blit((buf, 4, 3, RGB565), 2, 2), Area(2, 2, 4, 3))
        self.assertEqual(self.fb.pixel(2, 2), 0xABCD)
        self.assertIsNone(self.fb.blit((buf, 4, 3, RGB565), -4, 0))

    def test_scroll_returns_area(self):
        self.fb.fill_rect(0, 0, 4, 4, 0xFFFF)
        self.assertEqual(self.fb.scroll(1, 0), Area(0, 0, 16, 16))


class TestDrawingEffects(unittest.TestCase):
    def setUp(self):
        self.fb = make_fb(RGB565, 16, 16)
        self.fb.fill(0)

    def test_fill_rect_sets_interior_only(self):
        self.fb.fill_rect(4, 4, 3, 3, 0xFFFF)
        self.assertEqual(self.fb.pixel(4, 4), 0xFFFF)
        self.assertEqual(self.fb.pixel(6, 6), 0xFFFF)
        self.assertEqual(self.fb.pixel(7, 7), 0)

    def test_rect_outline_is_hollow(self):
        self.fb.rect(2, 2, 6, 6, 0xFFFF)
        # corners drawn, centre untouched
        self.assertEqual(self.fb.pixel(2, 2), 0xFFFF)
        self.assertEqual(self.fb.pixel(7, 7), 0xFFFF)
        self.assertEqual(self.fb.pixel(4, 4), 0)

    def test_rect_filled(self):
        self.fb.rect(2, 2, 6, 6, 0xFFFF, True)
        self.assertEqual(self.fb.pixel(4, 4), 0xFFFF)


if __name__ == "__main__":
    unittest.main()
