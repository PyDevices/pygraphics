# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Show every bitmap font in a folder.

Finds each .bin font in examples/assets/, draws the alphabet and the
font's name in it, and scrolls the display when the list runs past the
bottom. Font files are named fontname_WxH.bin, W wide and H high. Set
EXPORT to True to also save each font as a .py module.

Needs: a board_config with a display_drv, which a PyDevices board
package or pydevices-desktop provides, and pygraphics.

Run it from the repository's root:
    python examples/font_list.py

On a board, copy the font_*.bin files to the board's examples/assets/ first.

Tested on: CPython 3.12 on Linux, in an SDL window.
"""

from board_config import display_drv
from pygraphics import Font, FrameBuffer, RGB565
import os


# Change this to match your setup: True also saves each font as a .py file.
EXPORT = False

display_drv.fill(0)
y_pos = 0


def main():
    global y_pos

    # Specify the directory containing the .bin files
    directory = "examples/assets/"

    def gather_font_files(directory):
        font_files = []
        for file in os.listdir(directory):
            if file.endswith(".bin"):
                file_path = "/".join([directory, file])
                font_files.append(file_path)
        return font_files

    font_files = gather_font_files(directory)

    bg_color = 0
    fg_color = 0x07E0
    scale = 1

    for font_file in font_files:
        try:
            font = Font(font_file)
        except RuntimeError as e:
            print(e)
            continue

        if EXPORT:
            font.export(font.font_data.replace(".bin", ".py"))

        height = font.height
        font_name = font.font_name

        buffer = bytearray(display_drv.width * height * 2)
        fb = FrameBuffer(buffer, display_drv.width, height, RGB565)
        fb.fill(bg_color)
        string = "".join([chr(i) for i in range(65, 91)]) + ": " + font_name.split("/")[-1]
        font.text(fb, string, 0, 0, fg_color, scale)
        display_drv.blit_rect(buffer, 0, y_pos % display_drv.height, display_drv.width, height)
        y_pos += height
        if y_pos > display_drv.height:
            display_drv.vscsad((y_pos - display_drv.height) % display_drv.height)
        display_drv.show()


main()
