# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Tests for clip-region helpers."""

import unittest

import _env  # noqa: F401
from pygraphics import RGB565, Area, FrameBuffer

# These target pure-Python internals. When the native C extension is the
# loaded implementation, pygraphics is a single extension module rather than
# a package, so these submodules do not exist and the tests do not apply.
try:
    from pygraphics._clip import ClippedCanvas, crop_rgb565_buffer, intersect_rect
except ImportError as exc:  # pragma: no cover - depends on which build is installed
    raise unittest.SkipTest(
        "pygraphics._clip is pure-Python only; the native build is loaded (" + str(exc) + ")"
    ) from None


def make_fb(w=8, h=8):
    return FrameBuffer(bytearray(w * h * 2), w, h, RGB565)


class TestClipHelpers(unittest.TestCase):
    def test_intersect_rect(self):
        self.assertEqual(
            intersect_rect(0, 0, 10, 10, Area(5, 5, 10, 10)),
            Area(5, 5, 5, 5),
        )
        self.assertIsNone(intersect_rect(0, 0, 2, 2, Area(10, 10, 2, 2)))

    def test_crop_rgb565_buffer(self):
        buf = bytearray([0, 1, 2, 3, 4, 5, 6, 7])
        cropped = crop_rgb565_buffer(buf, 2, 1, 0, 1, 2)
        self.assertEqual(bytes(cropped), bytes([2, 3, 6, 7]))

    def test_clipped_canvas_fill_rect(self):
        fb = make_fb(w=8, h=8)
        fb.fill(0)
        clipped = ClippedCanvas(fb, Area(2, 2, 3, 3))
        clipped.fill_rect(0, 0, 8, 8, 0xFFFF)
        self.assertEqual(fb.pixel(1, 1), 0)
        self.assertEqual(fb.pixel(2, 2), 0xFFFF)
        self.assertEqual(fb.pixel(4, 4), 0xFFFF)
        self.assertEqual(fb.pixel(5, 5), 0)

    def test_clipped_canvas_text(self):
        """text must not fall through to the unclipped underlying canvas."""
        fb = make_fb(w=32, h=24)
        fb.fill(0)
        clip = Area(4, 8, 20, 8)
        clipped = ClippedCanvas(fb, clip)
        # Glyph starts above the clip; only the overlap may light pixels.
        clipped.text("Hi", 4, 0, 0xFFFF, height=16)
        outside = []
        inside = 0
        for y in range(fb.height):
            for x in range(fb.width):
                if not fb.pixel(x, y):
                    continue
                if clip.contains(x, y):
                    inside += 1
                else:
                    outside.append((x, y))
        self.assertEqual(outside, [])
        self.assertGreater(inside, 0)


if __name__ == "__main__":
    unittest.main()
