# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Turn the display through all four rotations.

Every two seconds the display turns another 90 degrees and changes colour,
and says which rotation and colour it shows. Use it to check that a
board_config's rotation settings put the picture the right way up.

Needs: a board_config with a display_drv, which a PyDevices board
package or pydevices-desktop provides, appdev and pygraphics, and palettes.

Run it from the repository's root:
    python examples/rotations.py

Tested on: CPython 3.12 on Linux, in an SDL window.
"""

from board_config import display_drv
import board_config
import appdev

app = appdev.App(board_config)
from pygraphics import Draw, text16
from palettes import get_palette

pal = get_palette()
draw = Draw(display_drv)

FONT_W = 8
FONT_H = 16


def center_text(text, y, fg, bg):
    x = (display_drv.width - len(text) * FONT_W) // 2
    # Opaque label: fill bg strip then draw glyphs.
    draw.fill_rect(x, y, len(text) * FONT_W, FONT_H, bg)
    text16(display_drv, text, x, y, fg)


def clear_screen(color):
    """Expand rectangles from the center toward the edges."""
    width = display_drv.width
    height = display_drv.height
    x_center = width // 2
    y_center = height // 2

    for i in range(min(x_center, y_center)):
        x = x_center - i
        y = y_center - i
        draw.rect(x, y, 2 * i + 1, 2 * i + 1, color)


def main():
    colors = (
        ("Red", pal.RED, pal.WHITE),
        ("Green", pal.GREEN, pal.BLACK),
        ("Blue", pal.BLUE, pal.WHITE),
        ("Black", pal.BLACK, pal.WHITE),
        ("White", pal.WHITE, pal.BLACK),
        ("Yellow", pal.YELLOW, pal.BLACK),
        ("Cyan", pal.CYAN, pal.BLACK),
        ("Magenta", pal.MAGENTA, pal.BLACK),
    )

    st = {"rotation": 0, "color_idx": 0}

    def poll():
        rotation = st["rotation"]
        color_idx = st["color_idx"]
        display_drv.rotation = rotation * 90
        height = display_drv.height
        fg = colors[color_idx][2]
        bg = colors[color_idx][1]

        draw.fill(bg)
        draw.rect(0, 0, display_drv.width, height, pal.WHITE)
        clear_screen(bg)
        center_text("Rotation", height // 3 - FONT_H // 2, fg, bg)
        center_text(str(rotation * 90), height // 2 - FONT_H // 2, fg, bg)
        center_text(colors[color_idx][0], height // 3 * 2 - FONT_H // 2, fg, bg)
        st["color_idx"] = (color_idx + 1) % len(colors)
        st["rotation"] = (rotation + 1) % 4
        return False

    def _tick(_=None):
        poll()

    app.every(_tick, period=2000)


main()
