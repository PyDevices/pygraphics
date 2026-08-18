# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Shared helpers for the pygraphics test modules.

Imported as a top-level module (``from _support import ...``) because
``_env`` has already put the tests directory's parent layout on ``sys.path``;
the tests directory itself is on ``sys.path`` by virtue of being the
discovery start directory.
"""

import _env  # noqa: F401  (must precede the pygraphics import)
from pygraphics import RGB565, FrameBuffer

# Bytes per pixel for each supported format, used to size the backing buffer.
# Sub-byte formats round up to one byte per pixel, which is always enough.
_BITS_PER_PIXEL = {
    "MONO_VLSB": 1,
    "MONO_HLSB": 1,
    "MONO_HMSB": 1,
    "GS2_HMSB": 2,
    "GS4_HMSB": 4,
    "GS8": 8,
    "RGB565": 16,
}


def _bits_for(fmt):
    """Bits per pixel for a pygraphics format constant."""
    import pygraphics

    for name, bits in _BITS_PER_PIXEL.items():
        if getattr(pygraphics, name, None) == fmt:
            return bits
    raise ValueError(f"unknown framebuffer format: {fmt!r}")


def make_fb(fmt=RGB565, w=8, h=8):
    """Build a zeroed :class:`pygraphics.FrameBuffer` of ``w`` x ``h``.

    Args:
        fmt (int): A pygraphics format constant. Defaults to ``RGB565``.
        w (int): Width in pixels.
        h (int): Height in pixels.

    Returns:
        FrameBuffer: A framebuffer backed by a freshly zeroed ``bytearray``.
    """
    bits = _bits_for(fmt)
    # Rows are byte-aligned, matching the framebuf stride convention.
    row_bytes = (w * bits + 7) // 8
    return FrameBuffer(bytearray(row_bytes * h), w, h, fmt)


def count_set(canvas):
    """Count pixels on ``canvas`` whose value is non-zero.

    Tests draw in a single non-zero color against a zeroed buffer, so this is
    the number of pixels the drawing operation touched.

    Args:
        canvas (FrameBuffer): The surface to scan.

    Returns:
        int: How many pixels are non-zero.
    """
    return sum(
        1
        for y in range(canvas.height)
        for x in range(canvas.width)
        if canvas.pixel(x, y)
    )
