# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Scroll a tall BMP picture down the display.

Draws a picture taller than the screen one line at a time, then keeps
going with the display's hardware scrolling (vscsad), so it never needs
the whole picture in memory.

Needs: a board_config with a display_drv, which a PyDevices board
package or pydevices-desktop provides, appdev and pygraphics.

Run it from the repository's root:
    python examples/bmp565_scroll.py

On a board, copy longstreet.bmp to the board's examples/assets/ first.

Tested on: CPython 3.12 on Linux, in an SDL window.
"""

from board_config import display_drv
import board_config
import appdev

app = appdev.App(board_config)
from pygraphics import BMP565

display_drv.rotation = 0

image = BMP565("examples/assets/longstreet.bmp", streamed=True)
print(f"\n{image.width=}, {image.height=}, {image.bpp=}")


def draw_bg(dest_x, dest_y, source_x, source_y, source_image=image, width=image.width, height=1):
    display_drv.blit_rect(
        source_image[source_x : source_x + width, source_y : source_y + height],
        dest_x,
        dest_y,
        width,
        height,
    )


def main():
    st = {"phase": "fill", "j": 0, "i": display_drv.height}

    def _tick(_=None):
        if app.quit_requested:
            return
        if st["phase"] == "fill":
            j = st["j"]
            if j < display_drv.height:
                draw_bg(0, j, 0, j, height=1)
                st["j"] = j + 1
                if st["j"] >= display_drv.height:
                    st["phase"] = "scroll"
                return
        # scroll phase
        i = st["i"]
        display_drv.vscsad(i % display_drv.height)
        draw_bg(0, i % display_drv.height, 0, i % image.height)
        st["i"] = i + 1

    app.every(_tick, period=1)


main()
