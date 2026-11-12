# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Draw smooth-edged shapes in any colour from an alpha mask.

Builds two 8-bit alpha masks in code, a disc and a ring, then draws each one
in several colours on a coloured background with `blit_alpha`. A mask stores
only how much of the colour to lay down at each pixel, so one mask serves
every colour, and the edges blend into whatever is behind them. The picture
is saved as a BMP, and the program prints its name.

Needs: MicroPython-compatible, CircuitPython-compatible or CPython with
pygraphics. Nothing else.

Run it from the repository's root:
    python examples/blit_alpha_icons.py

Tested on: CPython 3.12 on Linux, with the pure-Python package and the
compiled one.
"""

from math import sqrt

from pygraphics import RGB565, FrameBuffer

# Change these to match your setup.
SIZE = 40  # width and height of each mask, in pixels
GAP = 10  # space between shapes, in pixels
BACKGROUND = 0x2965  # dark slate, as an RGB565 value
COLORS = (0xF800, 0xFFE0, 0x07E0, 0x07FF)  # red, yellow, green, cyan
FILENAME = "blit_alpha_icons.bmp"

# Leave room on the right for a shape that hangs half off the picture.
WIDTH = GAP + len(COLORS) * (SIZE + GAP) + SIZE // 2
HEIGHT = GAP + 2 * (SIZE + GAP)


def disc_mask(size, radius):
    """Return a size x size mask that is 255 inside a circle and fades to 0 at its rim."""
    mask = bytearray(size * size)
    middle = (size - 1) / 2
    for y in range(size):
        for x in range(size):
            distance = sqrt((x - middle) ** 2 + (y - middle) ** 2)
            # One pixel of edge: full inside, none outside, a ramp between.
            coverage = min(1.0, max(0.0, radius + 0.5 - distance))
            mask[y * size + x] = int(coverage * 255 + 0.5)
    return mask


def ring_mask(size, outer, inner):
    """Return a mask for a ring: the outer disc with the inner disc taken away."""
    outer_mask = disc_mask(size, outer)
    inner_mask = disc_mask(size, inner)
    return bytes(max(0, o - i) for o, i in zip(outer_mask, inner_mask))


# Wrap the masks in memoryviews. blit_alpha reads them where they are, and a
# memoryview over a bytes literal in frozen firmware never copies it into RAM.
disc = memoryview(bytes(disc_mask(SIZE, SIZE // 2 - 1)))
ring = memoryview(ring_mask(SIZE, SIZE // 2 - 1, SIZE // 2 - 7))

# Draw on a coloured background so the blended edges show.
fb = FrameBuffer(bytearray(WIDTH * HEIGHT * 2), WIDTH, HEIGHT, RGB565)
fb.fill(BACKGROUND)

# Draw the same two masks once per colour: discs in the top row, rings below.
for index, color in enumerate(COLORS):
    x = GAP + index * (SIZE + GAP)
    fb.blit_alpha(disc, x, GAP, SIZE, SIZE, color)
    fb.blit_alpha(ring, x, 2 * GAP + SIZE, SIZE, SIZE, color)

# Draw one disc half off the edge to show that the mask is clipped to the picture.
fb.blit_alpha(disc, WIDTH - SIZE // 2, (HEIGHT - SIZE) // 2, SIZE, SIZE, 0xFFFF)

# Save the picture and report where it went.
print(fb.save(FILENAME))
