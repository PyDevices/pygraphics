#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""FrameBuffer subclass test for CPython tp_new/tp_init split."""

from pygraphics import RGB565, Area, FrameBuffer


class SubBuffer(FrameBuffer):
    def __init__(self, buf, w, h, fmt):
        super().__init__(buf, w, h, fmt)


buf = bytearray(32 * 32 * 2)
fb = SubBuffer(buf, 32, 32, RGB565)
fb.fill(0)
area = fb.fill_rect(4, 4, 8, 8, 0xF800)
assert area == Area(4, 4, 8, 8)
print("test_subclass: ok")
