# SPDX-License-Identifier: MIT
"""MONO_HLSB stride must match MicroPython (row byte-aligned)."""

import unittest

from pygraphics import MONO_HLSB, RGB565, FrameBuffer


class TestMonoHlsbStride(unittest.TestCase):
    def test_icon_width_not_multiple_of_eight(self):
        # 18-wide PBM-style + (same layout as pdwidgets add_18dp).
        bitmap = bytearray(
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc0\x00\x00"
            b"\xc0\x00\x00\xc0\x00\x00\xc0\x00\x0f\xfc\x00\x0f\xfc\x00\x00\xc0"
            b"\x00\x00\xc0\x00\x00\xc0\x00\x00\xc0\x00\x00\x00\x00\x00\x00\x00"
            b"\x00\x00\x00\x00\x00\x00"
        )
        src = FrameBuffer(bitmap, 18, 18, MONO_HLSB)
        row4 = [src.pixel(x, 4) for x in range(18)]
        row8 = [src.pixel(x, 8) for x in range(18)]
        self.assertEqual(row4, [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(row8, [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0])

        dst = FrameBuffer(bytearray(18 * 18 * 2), 18, 18, RGB565)
        dst.fill(0)
        pal = FrameBuffer(memoryview(bytearray(4)), 2, 1, RGB565)
        pal.pixel(0, 0, 0)
        pal.pixel(1, 0, 0xFFFF)
        dst.blit(src, 0, 0, -1, pal)
        # Horizontal bar of the +
        self.assertTrue(all(dst.pixel(x, 8) for x in range(4, 14)))
        self.assertFalse(dst.pixel(0, 8))
        # Vertical stem
        self.assertTrue(dst.pixel(8, 4) and dst.pixel(9, 4))


if __name__ == "__main__":
    unittest.main()
