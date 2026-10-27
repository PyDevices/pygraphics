# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Time a few common drawing calls. Runs on CPython and MicroPython.

Prints which pygraphics it imported, then one line per call:
``name|milliseconds per call``. docs/how-it-works/benchmarks.md shows how to
run it against each package.
"""

import time

import pygraphics
from pygraphics import RGB565, FrameBuffer

W, H = 160, 128
fb = FrameBuffer(bytearray(W * H * 2), W, H, RGB565)
sprite = FrameBuffer(bytearray(64 * 64 * 2), 64, 64, RGB565)
sprite.fill(0xF800)

cases = [
    ("fill_rect, 160 x 128", lambda: fb.fill_rect(0, 0, W, H, 0x001F)),
    ("filled circle, r = 40", lambda: fb.circle(80, 64, 40, 0x07E0, f=True)),
    ("filled round_rect, 120 x 80, r = 10", lambda: fb.round_rect(20, 24, 120, 80, 10, 0xF800, f=True)),
    ("text16, 20 characters", lambda: pygraphics.text16(fb, "abcdefghijklmnopqrst", 0, 50, 0xFFFF)),
    ("blit, 64 x 64 sprite", lambda: fb.blit(sprite, 40, 30)),
]

try:
    clock = time.perf_counter
except AttributeError:

    def clock():
        return time.ticks_us() / 1e6


print(pygraphics.implementation())
for name, fn in cases:
    n = 0
    t0 = clock()
    while clock() - t0 < 0.5:
        fn()
        n += 1
    print("%s|%.4f" % (name, (clock() - t0) / n * 1000))
