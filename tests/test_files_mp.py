#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""File round trips that run on MicroPython as well as CPython.

test_files.py needs ``tempfile``, which MicroPython doesn't have, so the pure
package's save, load and export went untested there. They import ``_files``
lazily from inside the method, and on MicroPython that import goes through the
package's ``__getattr__``, which CPython never exercises.
"""

import os

import _env  # noqa: F401  puts lib/ on sys.path when no native build is present
import pygraphics
from pygraphics import GS8, MONO_HLSB, RGB565, FrameBuffer

NAMES = []


def _name(stem):
    NAMES.append(stem)
    return stem


try:
    fb = FrameBuffer(bytearray(8 * 4 * 2), 8, 4, RGB565)
    fb.fill(0)
    fb.fill_rect(1, 1, 3, 2, 0xF800)
    path = fb.save(_name("_mp_files_rgb.bmp"))
    assert path == "_mp_files_rgb.bmp", path
    back = FrameBuffer.from_file(path)
    assert (back.width, back.height) == (8, 4)
    assert bytes(back.buffer) == bytes(fb.buffer)
    assert bytes(pygraphics.load_image(path).buffer) == bytes(fb.buffer)

    grey = FrameBuffer(bytearray(8 * 4), 8, 4, GS8)
    grey.fill(0x40)
    path = grey.save(_name("_mp_files_grey"))
    NAMES.append(path)
    assert path == "_mp_files_grey.pgm", path
    assert bytes(FrameBuffer.from_file(path).buffer) == bytes(grey.buffer)

    mono = FrameBuffer(bytearray(8 * 4 // 8), 8, 4, MONO_HLSB)
    mono.fill(0)
    mono.pixel(2, 1, 1)
    path = pygraphics.save_image(mono, _name("_mp_files_mono.pbm"))
    assert bytes(FrameBuffer.from_file(path).buffer) == bytes(mono.buffer)

    # Pure-Python only; the native build leaves it out on purpose.
    if hasattr(fb, "export"):
        fb.export(_name("_mp_files_export.py"))
        assert os.stat("_mp_files_export.py")[6] > 0
finally:
    for name in NAMES:
        try:  # noqa: SIM105  MicroPython has no contextlib
            os.remove(name)
        except OSError:
            pass

print("test_files_mp: ok")
