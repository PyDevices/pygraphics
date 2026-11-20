#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""FrameBuffer(areas=False): drawing returns None, draws the same pixels, and on MicroPython allocates nothing.

Runs under unittest discovery and on its own under MicroPython:
``micropython tests/test_areas_off.py``.
"""

import _env  # noqa: F401  (must precede the pygraphics import)
import gc
import sys

import pygraphics
from pygraphics import RGB565, Area, Draw, FrameBuffer

W = 48
H = 40


# Every drawing call, as (name, call) pairs, so one list exercises the
# FrameBuffer methods, a Draw on it, and the module functions alike.
def fb_calls(fb, src, mask):
    return [
        ("fill", lambda: fb.fill(0x1111)),
        ("fill_rect", lambda: fb.fill_rect(2, 3, 9, 7, 0xF800)),
        ("pixel", lambda: fb.pixel(5, 6, 0x07E0)),
        ("hline", lambda: fb.hline(1, 9, 20, 0x001F)),
        ("vline", lambda: fb.vline(30, 2, 15, 0xFFE0)),
        ("line", lambda: fb.line(0, 0, 40, 30, 0xF81F)),
        ("rect", lambda: fb.rect(4, 4, 12, 10, 0x07FF)),
        ("rect_fill", lambda: fb.rect(20, 20, 8, 6, 0x7BEF, True)),
        ("round_rect", lambda: fb.round_rect(6, 18, 20, 14, 4, 0xFD20)),
        ("circle", lambda: fb.circle(24, 20, 9, 0xAFE5)),
        ("circle_fill", lambda: fb.circle(36, 10, 5, 0x8410, True)),
        ("ellipse", lambda: fb.ellipse(24, 20, 12, 6, 0xF800)),
        ("arc", lambda: fb.arc(24, 20, 14, 0, 120, 0x001F)),
        ("triangle", lambda: fb.triangle(2, 38, 20, 22, 30, 38, 0x07E0)),
        ("gradient_rect", lambda: fb.gradient_rect(0, 30, 48, 6, 0x0000, 0xFFFF)),
        ("polygon", lambda: fb.polygon([(0, 0), (8, 0), (4, 6)], 30, 25, 0xFFFF)),
        ("blit", lambda: fb.blit(src, 10, 10)),
        ("blit_rect", lambda: fb.blit_rect(src.buffer, 12, 12, 8, 8)),
        ("blit_transparent", lambda: fb.blit_transparent(src.buffer, 14, 14, 8, 8, 0)),
        ("blit_alpha", lambda: fb.blit_alpha(mask, 16, 2, 8, 8, 0xF800)),
        ("text", lambda: fb.text("Hi", 1, 1, 0xFFFF)),
        ("text8", lambda: fb.text8("ok", 1, 12, 0xFFFF)),
        ("text16", lambda: fb.text16("A", 30, 20, 0xFFFF)),
        ("scroll", lambda: fb.scroll(1, 0)),
    ]


def draw_calls(fb, src):
    d = Draw(fb)
    return [
        ("Draw.fill_rect", lambda: d.fill_rect(2, 3, 9, 7, 0xF800)),
        ("Draw.circle", lambda: d.circle(24, 20, 9, 0xAFE5)),
        ("Draw.line", lambda: d.line(0, 0, 40, 30, 0xF81F)),
        ("Draw.text", lambda: d.text("Hi", 1, 1, 0xFFFF)),
        ("Draw.blit", lambda: d.blit(src, 10, 10)),
        ("Draw.arc", lambda: d.arc(24, 20, 14, 0, 120, 0x001F)),
    ]


def module_calls(fb, src):
    g = pygraphics
    return [
        ("pygraphics.fill_rect", lambda: g.fill_rect(fb, 2, 3, 9, 7, 0xF800)),
        ("pygraphics.circle", lambda: g.circle(fb, 24, 20, 9, 0xAFE5)),
        ("pygraphics.line", lambda: g.line(fb, 0, 0, 40, 30, 0xF81F)),
        ("pygraphics.text8", lambda: g.text8(fb, "ok", 1, 12, 0xFFFF)),
        ("pygraphics.blit", lambda: g.blit(fb, src, 10, 10)),
        ("pygraphics.round_rect", lambda: g.round_rect(fb, 6, 18, 20, 14, 4, 0xFD20)),
    ]


def make(areas):
    if areas is None:
        return FrameBuffer(bytearray(W * H * 2), W, H, RGB565)
    return FrameBuffer(bytearray(W * H * 2), W, H, RGB565, areas=areas)


def make_src():
    src = FrameBuffer(bytearray(8 * 8 * 2), 8, 8, RGB565)
    src.fill(0x1234)
    src.fill_rect(2, 2, 4, 4, 0)
    return src


MASK = bytearray(range(0, 256, 4))


def all_calls(fb, src):
    return fb_calls(fb, src, MASK) + draw_calls(fb, src) + module_calls(fb, src)


# The default, and areas=True, still return an Area from every call.
for areas in (None, True):
    fb = make(areas)
    assert fb.areas is True, fb.areas
    for name, call in all_calls(fb, make_src()):
        r = call()
        assert isinstance(r, Area), (areas, name, r)

# areas=False returns None from every call and says so.
off = make(False)
assert off.areas is False
for name, call in all_calls(off, make_src()):
    r = call()
    assert r is None, (name, r)

# Reading a pixel still returns its value.
off.fill(0)
off.pixel(3, 3, 0x1234)
assert off.pixel(3, 3) == 0x1234

# A clip on a Draw follows the FrameBuffer underneath it.
d = Draw(off)
with d.clip(0, 0, 10, 10):
    assert d.fill_rect(0, 0, 20, 20, 0xFFFF) is None
    assert d.text("x", 0, 0, 0) is None

# The switch changes only what is returned: both draw the same pixels.
on = make(True)
off = make(False)
for (name, a), (_, b) in zip(all_calls(on, make_src()), all_calls(off, make_src())):
    a()
    b()
    assert bytes(on.buffer) == bytes(off.buffer), name


# A subclass passes the keyword through to the base class.
class Sub(FrameBuffer):
    def __init__(self, buf, w, h, fmt, **kwargs):
        super().__init__(buf, w, h, fmt, **kwargs)


sub = Sub(bytearray(W * H * 2), W, H, RGB565, areas=False)
assert sub.areas is False
assert sub.fill_rect(1, 1, 4, 4, 0xFFFF) is None
assert Draw(sub).circle(10, 10, 5, 0xFFFF) is None
assert pygraphics.text8(sub, "s", 0, 0, 0xFFFF) is None
assert isinstance(Sub(bytearray(W * H * 2), W, H, RGB565).fill(0), Area)

# Any other keyword is still refused.
try:
    FrameBuffer(bytearray(W * H * 2), W, H, RGB565, colour=1)
except TypeError:
    pass
else:
    raise AssertionError("unknown keyword accepted")

# On MicroPython with the compiled module, drawing with areas=False allocates
# nothing. (The pure-Python package and CPython allocate in other ways.)
if sys.implementation.name == "micropython" and pygraphics.implementation() == "native_cmod":
    fb = make(False)
    src = make_src()
    d = Draw(fb)
    calls = [
        ("fill_rect", lambda: fb.fill_rect(2, 3, 9, 7, 0xF800)),
        ("text", lambda: fb.text("Hi", 1, 1, 0xFFFF)),
        ("text16", lambda: fb.text16("A", 30, 20, 0xFFFF)),
        ("blit_alpha", lambda: fb.blit_alpha(MASK, 16, 2, 8, 8, 0xF800)),
        ("blit", lambda: fb.blit(src, 10, 10)),
        ("circle", lambda: fb.circle(24, 20, 9, 0xAFE5)),
        ("Draw.circle", lambda: d.circle(24, 20, 9, 0xAFE5)),
        ("Draw.text", lambda: d.text("Hi", 1, 1, 0xFFFF)),
        ("pygraphics.text8", lambda: pygraphics.text8(fb, "ok", 1, 12, 0xFFFF)),
    ]
    for name, call in calls:
        call()
        gc.collect()
        gc.disable()
        before = gc.mem_alloc()
        for _ in range(50):
            call()
        grew = gc.mem_alloc() - before
        gc.enable()
        assert grew == 0, (name, grew)

print("test_areas_off: ok")
