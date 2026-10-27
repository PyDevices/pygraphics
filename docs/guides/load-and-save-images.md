# Load and save images

## Save a picture

`fb.save(name)` writes a file in the type that fits the pixel format: BMP for
`RGB565`, PGM for greyscale, PBM for `MONO_HLSB`, PNG for `RGB888`. If the
name doesn't end in that type's extension, the extension is added, and the
name it wrote is returned.

```python
from pygraphics import FrameBuffer, RGB565, GS8

fb = FrameBuffer(bytearray(64 * 64 * 2), 64, 64, RGB565)
fb.fill(0x001F)
print(fb.save("sky.bmp"))        # sky.bmp

grey = FrameBuffer(bytearray(64 * 64), 64, 64, GS8)
grey.gradient_rect(0, 0, 64, 64, 0, 255)
print(grey.save("ramp"))         # ramp.pgm
```

`pygraphics.save_image(fb, name)` does the same thing as a function. The full
list of formats and file types is under [Formats](../formats.md#which-file-each-format-saves-as).

A name ending in `.png` saves an `RGB565`, `GS8` or `MONO_HLSB` picture as
PNG. PNG needs the `pngio` module: PyDevices firmware has it built in, and on
CPython it comes with the `pydevices-desktop` package and needs Pillow.
Without it, saving a PNG raises an `ImportError` that says what to install.

## Load a picture

`load_image(path)` reads a BMP, PGM or PBM file, works out which from the
file itself, and returns a `FrameBuffer`:

```python
import pygraphics

sky = pygraphics.load_image("sky.bmp")
print(sky.width, sky.height)      # 64 64
fb.blit(sky, 0, 0)
```

The whole image goes into memory. BMP files must be 16-bit RGB565, which is
what GIMP writes when you export as BMP with "R5 G6 B5" under advanced
options.

## Stream a large BMP

An image bigger than your board's free memory can still be shown in pieces.
`BMP565` opens an RGB565 BMP and lets you slice out a rectangle;
`streamed=True` reads only the rows you ask for:

```python
from pygraphics import BMP565

bg = BMP565("sky.bmp", streamed=True)
tile = bg[0:16, 0:16]             # x from 0 to 16, y from 0 to 16
display_drv.blit_rect(tile, 0, 0, 16, 16)
```

A slice is raw RGB565 bytes, ready for a display driver's `blit_rect`.
`bg(x, y, w, h)` is the same as `bg[x:x + w, y:y + h]`.

## Turn a picture into Python source

The pure-Python package can write a framebuffer out as a `.py` module, so an
icon can be frozen into firmware or imported like any other module:

```python
fb.export("icon.py")

import icon
again = FrameBuffer.from_module(icon)
```

`export`, `export_framebuffer`, `from_bitmap` and `from_module` are in the
pure-Python package only; the compiled package leaves them out because they
write and read Python source, which is preparation work rather than drawing.
On CPython with the compiled package, run that step with the pure package on
your path. [Platforms](../platforms.md#names-only-the-pure-python-package-has)
lists them.
