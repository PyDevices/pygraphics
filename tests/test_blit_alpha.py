# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Tests for ``FrameBuffer.blit_alpha``: tinting through an 8-bit alpha mask."""

import unittest

import _env  # noqa: F401
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

_BYTES_PER_PIXEL = {RGB565: 2, RGB888: 3, GS8: 1}
_BACKGROUND = {RGB565: 0x1234, RGB888: 0x336699, GS8: 0x40}
_TINT = {RGB565: 0xF81F, RGB888: 0xFF8000, GS8: 0xE0}
# Channel layout per format: (shift, max) pairs from the high channel down.
_CHANNELS = {
    RGB565: ((11, 0x1F), (5, 0x3F), (0, 0x1F)),
    RGB888: ((16, 0xFF), (8, 0xFF), (0, 0xFF)),
    GS8: ((0, 0xFF),),
}


def _expected(fmt, color, old, a):
    """The blend, written out channel by channel."""
    out = 0
    for shift, top in _CHANNELS[fmt]:
        c = (color >> shift) & top
        d = (old >> shift) & top
        out |= ((c * a + d * (255 - a) + 127) // 255) << shift
    return out


def _make(fmt, w, h, fill=None):
    fb = FrameBuffer(bytearray(w * h * _BYTES_PER_PIXEL[fmt]), w, h, fmt)
    fb.fill(_BACKGROUND[fmt] if fill is None else fill)
    return fb


def _pixels(fb):
    return [[fb.pixel(x, y) for x in range(fb.width)] for y in range(fb.height)]


class TestBlend(unittest.TestCase):
    def test_zero_leaves_pixels_alone(self):
        for fmt in _BYTES_PER_PIXEL:
            fb = _make(fmt, 4, 3)
            before = bytes(fb.buffer)
            fb.blit_alpha(bytes(12), 0, 0, 4, 3, _TINT[fmt])
            self.assertEqual(bytes(fb.buffer), before, fmt)

    def test_255_writes_the_color(self):
        for fmt in _BYTES_PER_PIXEL:
            fb = _make(fmt, 4, 3)
            fb.blit_alpha(b"\xff" * 12, 0, 0, 4, 3, _TINT[fmt])
            self.assertEqual(_pixels(fb), [[_TINT[fmt]] * 4] * 3, fmt)

    def test_every_alpha_matches_the_formula(self):
        for fmt in _BYTES_PER_PIXEL:
            fb = _make(fmt, 256, 1)
            fb.blit_alpha(bytes(range(256)), 0, 0, 256, 1, _TINT[fmt])
            for a in range(256):
                want = _expected(fmt, _TINT[fmt], _BACKGROUND[fmt], a)
                self.assertEqual(fb.pixel(a, 0), want, "fmt %d alpha %d" % (fmt, a))

    def test_blends_over_a_varied_background(self):
        fb = _make(RGB888, 3, 1)
        for x, colour in enumerate((0x000000, 0xFFFFFF, 0x123456)):
            fb.pixel(x, 0, colour)
        fb.blit_alpha(bytes((100, 100, 100)), 0, 0, 3, 1, 0xC08040)
        for x, old in enumerate((0x000000, 0xFFFFFF, 0x123456)):
            self.assertEqual(fb.pixel(x, 0), _expected(RGB888, 0xC08040, old, 100))

    def test_rgb565_uses_the_stored_value_order(self):
        # Red in 565 is 0xF800 as pixel() reports it; 255 alpha writes it as-is.
        fb = _make(RGB565, 2, 1, 0)
        fb.blit_alpha(b"\xff\x00", 0, 0, 2, 1, 0xF800)
        self.assertEqual(fb.pixel(0, 0), 0xF800)
        self.assertEqual(fb.pixel(1, 0), 0)
        self.assertEqual(bytes(fb.buffer), b"\x00\xf8\x00\x00")

    def test_rgb888_buffer_is_r_g_b(self):
        fb = _make(RGB888, 1, 1, 0)
        fb.blit_alpha(b"\xff", 0, 0, 1, 1, 0x102030)
        self.assertEqual(bytes(fb.buffer), b"\x10\x20\x30")

    def test_strided_framebuffer(self):
        fb = FrameBuffer(bytearray(6 * 2 * 2), 4, 2, RGB565, 6)
        fb.fill(0)
        fb.blit_alpha(b"\xff" * 8, 0, 0, 4, 2, 0xFFFF)
        self.assertEqual(_pixels(fb), [[0xFFFF] * 4] * 2)
        self.assertEqual(bytes(fb.buffer[8:12]), b"\x00" * 4)

    def test_returns_the_mask_area(self):
        fb = _make(GS8, 4, 4)
        area = fb.blit_alpha(bytes(6), 1, 1, 3, 2, 255)
        self.assertEqual(area, Area(1, 1, 3, 2))

    def test_empty_mask_is_a_no_op(self):
        fb = _make(GS8, 4, 4)
        before = bytes(fb.buffer)
        fb.blit_alpha(b"", 1, 1, 0, 0, 255)
        fb.blit_alpha(b"", 1, 1, 0, 3, 255)
        self.assertEqual(bytes(fb.buffer), before)

    def test_accepts_any_buffer_and_does_not_copy_it(self):
        mask = bytearray((0, 128, 255, 64))
        for source in (bytes(mask), mask, memoryview(bytes(mask)), memoryview(mask)):
            fb = _make(GS8, 4, 1)
            fb.blit_alpha(source, 0, 0, 4, 1, 255)
            self.assertEqual([fb.pixel(x, 0) for x in range(4)], [_expected(GS8, 255, 0x40, a) for a in mask])
        # A change to the bytearray after the call can't show in the result,
        # and one before the call is seen: the buffer is read where it lives.
        mask[0] = 255
        fb = _make(GS8, 4, 1)
        fb.blit_alpha(memoryview(mask), 0, 0, 4, 1, 255)
        self.assertEqual(fb.pixel(0, 0), 255)

    def test_reads_a_slice_of_a_larger_mask(self):
        mask = memoryview(bytes((0, 0, 255, 255, 0, 0)))[2:4]
        fb = _make(GS8, 2, 1)
        fb.blit_alpha(mask, 0, 0, 2, 1, 7)
        self.assertEqual([fb.pixel(0, 0), fb.pixel(1, 0)], [7, 7])


class TestClipping(unittest.TestCase):
    W = 6
    H = 5

    def _check(self, x, y, mw, mh):
        for fmt in _BYTES_PER_PIXEL:
            fb = _make(fmt, self.W, self.H)
            mask = bytes((1 + (j * mw + i) * 7) % 255 + 1 for j in range(mh) for i in range(mw))
            fb.blit_alpha(mask, x, y, mw, mh, _TINT[fmt])
            for j in range(self.H):
                for i in range(self.W):
                    mx, my = i - x, j - y
                    if 0 <= mx < mw and 0 <= my < mh:
                        want = _expected(fmt, _TINT[fmt], _BACKGROUND[fmt], mask[my * mw + mx])
                    else:
                        want = _BACKGROUND[fmt]
                    self.assertEqual(fb.pixel(i, j), want, "fmt %d at %d,%d" % (fmt, i, j))

    def test_inside(self):
        self._check(1, 1, 3, 2)

    def test_overhang_left(self):
        self._check(-2, 1, 4, 3)

    def test_overhang_top(self):
        self._check(1, -2, 4, 3)

    def test_overhang_right(self):
        self._check(4, 1, 4, 3)

    def test_overhang_bottom(self):
        self._check(1, 3, 4, 4)

    def test_overhang_every_side(self):
        self._check(-2, -2, 10, 9)

    def test_fully_off_screen(self):
        for x, y in ((-4, 0), (0, -3), (self.W, 0), (0, self.H), (-9, -9), (50, 50)):
            self._check(x, y, 4, 3)


class TestErrors(unittest.TestCase):
    def test_unsupported_formats_name_the_format(self):
        for name, fmt in (
            ("MONO_VLSB", MONO_VLSB),
            ("MONO_HLSB", MONO_HLSB),
            ("MONO_HMSB", MONO_HMSB),
            ("GS2_HMSB", GS2_HMSB),
            ("GS4_HMSB", GS4_HMSB),
        ):
            fb = FrameBuffer(bytearray(8 * 8), 8, 8, fmt)
            with self.assertRaises(ValueError) as caught:
                fb.blit_alpha(bytes(4), 0, 0, 2, 2, 1)
            self.assertIn(name, str(caught.exception))

    def test_short_buffer(self):
        for fmt in _BYTES_PER_PIXEL:
            fb = _make(fmt, 4, 4)
            before = bytes(fb.buffer)
            with self.assertRaises(ValueError):
                fb.blit_alpha(bytes(5), 0, 0, 3, 2, 255)
            self.assertEqual(bytes(fb.buffer), before)

    def test_short_buffer_is_an_error_even_when_off_screen(self):
        fb = _make(GS8, 4, 4)
        with self.assertRaises(ValueError):
            fb.blit_alpha(bytes(1), 100, 100, 3, 2, 255)

    def test_negative_size(self):
        fb = _make(GS8, 4, 4)
        with self.assertRaises(ValueError):
            fb.blit_alpha(b"", 0, 0, -1, 2, 255)
        with self.assertRaises(ValueError):
            fb.blit_alpha(b"", 0, 0, 2, -1, 255)

    def test_not_a_buffer(self):
        fb = _make(GS8, 4, 4)
        with self.assertRaises((TypeError, ValueError)):
            fb.blit_alpha(12, 0, 0, 1, 1, 255)


if __name__ == "__main__":
    unittest.main()
