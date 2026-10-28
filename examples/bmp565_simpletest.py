# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Load a BMP picture and show it.

Loads the whole of a 16-bit BMP into memory and copies it to the display
two ways: as a slice, bmp[x0:x1, y0:y1], and as bmp[:]. Loading it all
needs RAM: a small board such as an RP2040 raises MemoryError. See
bmp565_scroll_sprite.py for reading a picture a line at a time instead.

Needs: a board_config with a display_drv, which a PyDevices board
package or pydevices-desktop provides, and pygraphics.

Run it from the repository's root:
    python examples/bmp565_simpletest.py

On a board, copy warrior.bmp to the board's examples/assets/ first.

Tested on: CPython 3.12 on Linux, in an SDL window.
"""

from board_config import display_drv
from pygraphics import BMP565, hline

try:
    from time import sleep_ms
except ImportError:
    from time import sleep

    def sleep_ms(milliseconds):
        sleep(milliseconds / 1000)


try:
    bmp = BMP565("examples/assets/warrior.bmp")
except MemoryError:
    raise MemoryError("this board doesn't have enough RAM to load the full image")

print(f"{bmp.width=}, {bmp.height=}, {bmp.bpp=}")

display_drv.fill(0x0)
display_drv.show()
display_drv.blit_rect(bmp[0 : bmp.width, 0 : bmp.height], 0, 0, bmp.width, bmp.height)
display_drv.show()
sleep_ms(1000)

display_drv.fill(0x0)
display_drv.show()
sleep_ms(250)

hline(bmp, 0, bmp.height // 2, bmp.width, 0xFFFF)
display_drv.blit_rect(bmp[:], 0, 0, bmp.width, bmp.height)
display_drv.show()
sleep_ms(1000)
