#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Verify graphics cmod exports match pure-Python pygraphics.__all__."""

import pygraphics

if pygraphics.implementation() != "native_cmod":
    from unittest import SkipTest

    raise SkipTest("native-only export parity probe")

ALL = [
    "BMP565",
    "GS2_HMSB",
    "GS4_HMSB",
    "GS8",
    "MONO_HLSB",
    "MONO_HMSB",
    "MONO_VLSB",
    "RGB565",
    "Area",
    "ClipContext",
    "ClippedCanvas",
    "Draw",
    "Font",
    "FrameBuffer",
    "arc",
    "blit",
    "blit_rect",
    "blit_transparent",
    "bmp_to_framebuffer",
    "capabilities",
    "circle",
    "ellipse",
    "fill",
    "fill_rect",
    "framebuf_backend",
    "gradient_rect",
    "hline",
    "implementation",
    "line",
    "load_image",
    "pbm_to_framebuffer",
    "pgm_to_framebuffer",
    "pixel",
    "poly",
    "polygon",
    "rect",
    "round_rect",
    "save_image",
    "text",
    "text8",
    "text14",
    "text16",
    "triangle",
    "vline",
]

missing = [name for name in ALL if not hasattr(pygraphics, name)]
if missing:
    raise SystemExit("missing exports: " + ", ".join(missing))

assert pygraphics.framebuf_backend() == "native", pygraphics.capabilities()
assert pygraphics.implementation() == "native_cmod", pygraphics.capabilities()

buf = bytearray(32 * 32 * 2)
fb = pygraphics.FrameBuffer(buf, 32, 32, pygraphics.RGB565)
assert fb.buffer is buf or bytes(fb.buffer) == bytes(buf)
fb.fill(0)
pygraphics.fill_rect(fb, 1, 1, 4, 4, 0xF800)
pygraphics.text8(fb, "Hi", 0, 0, 0xFFFF)
d = pygraphics.Draw(fb)
d.fill_rect(0, 0, 2, 2, 1)
print("test_parity: ok")
