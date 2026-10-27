# Draw text

pygraphics carries three fonts inside it, all 8 pixels wide: 8, 14 and 16
pixels high. You need no font file to use them.

```python
import pygraphics
from pygraphics import FrameBuffer, RGB565

fb = FrameBuffer(bytearray(240 * 80 * 2), 240, 80, RGB565)
fb.fill(0x0000)

pygraphics.text8(fb, "Small", 0, 0, 0xFFFF)
pygraphics.text14(fb, "Medium", 0, 12, 0xF800)
area = pygraphics.text16(fb, "Large", 0, 30, 0x07E0)
pygraphics.text16(fb, "Big", 120, 0, 0xFFE0, scale=3)
```

Each call returns the `Area` it drew. `scale=2` or more makes every pixel of
the font a square of that size. Text is transparent: only the letters are
drawn, and whatever was behind them stays.

For text on a solid background, fill the rectangle first:

```python
font = pygraphics.Font(height=16)
w = font.text_width("Score: 120")
fb.fill_rect(0, 60, w, font.height, 0x001F)
font.text(fb, "Score: 120", 0, 60, 0xFFFF)
```

`Font` keeps a font loaded so you can measure and draw with it again.

## Use a font file

`Font` also reads romfont `.bin` files, from a path or from bytes already in
memory. The height comes from a name like `font_8x14.bin`, or you can give
it:

```python
f = pygraphics.Font("fonts/font_8x14.bin")
f.text(fb, "From a file", 0, 0, 0xFFFF)

f = pygraphics.Font("fonts/custom.bin", 14)
```

By default the whole file is read into memory. `cached=False` keeps the file
open and reads each letter when it's drawn, which saves memory and costs
speed. A missing file raises `OSError` (`FileNotFoundError` on CPython). The
file layout is under
[Formats](../formats.md#romfont-files).

## Text on a real screen

Where you draw the text decides how fast it reaches the screen.

| You draw on | Memory | What the screen receives | Good for |
|---|---|---|---|
| The display driver, `text16(display_drv, ...)` | none | one small rectangle per lit pixel | a few characters |
| A framebuffer the size of the string, then `blit_rect` | the string's size | one block per string | labels on a screen with little memory |
| A framebuffer the size of the screen, then [send the dirty area](update-part-of-a-screen.md) | the whole screen | the changed rows | text that changes often |

Drawing straight on a display driver is the simplest and the slowest: on an
SPI screen, every lit pixel is its own transfer. A string-sized buffer looks
like this:

```python
s = "Ready"
w, h = font.text_width(s), font.height
label = FrameBuffer(bytearray(w * h * 2), w, h, RGB565)
label.fill(0x0000)
font.text(label, s, 0, 0, 0xFFFF)
display_drv.blit_rect(label.buffer, 10, 10, w, h)
```

Keep one buffer for your longest label and reuse it, rather than making a new
one every frame.

## framebuf's text looks different

`fb.text(s, x, y, c)` on a pygraphics `FrameBuffer` uses the same 8x8 font as
`text8`, and takes `height=14` or `height=16` for the others. MicroPython's
own `framebuf` module draws text in a different 8x8 font, so a program moved
from `framebuf` to pygraphics will show slightly different letters.

Next: [load and save images](load-and-save-images.md).
