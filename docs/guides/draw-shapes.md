# Draw shapes

Make a `FrameBuffer`, then call its shape methods. Each one returns the
`Area` it changed.

```python
import pygraphics
from pygraphics import FrameBuffer, RGB565

fb = FrameBuffer(bytearray(200 * 120 * 2), 200, 120, RGB565)
fb.fill(0x0000)

fb.line(0, 0, 199, 119, 0xFFFF)
fb.rect(10, 10, 60, 30, 0x001F)                        # outline
fb.rect(80, 10, 60, 30, 0x001F, f=True)                # filled
fb.round_rect(10, 50, 60, 30, 6, 0xF800, f=True)
fb.circle(110, 65, 15, 0x07E0)
fb.ellipse(160, 65, 25, 12, 0xFFE0, f=True)
fb.triangle(10, 110, 40, 90, 70, 110, 0xF81F, f=True)
fb.arc(110, 100, 15, 0, 180, 0x07FF)
fb.gradient_rect(140, 90, 50, 25, 0xF800, 0x001F)
```

Pass `f=True` to fill a shape that has an outline form. `arc` takes a start
and end angle in degrees. `gradient_rect` blends from the first colour to the
second, top to bottom; add `vertical=False` for left to right.

For a shape of your own, `poly(x, y, coords, c, f=False)` draws the polygon
whose points are listed in `coords` as `x0, y0, x1, y1, ...`, offset by
`x, y`. `polygon(points, x, y, c, angle=0)` takes a list of `(x, y)` pairs
and can rotate them by `angle` radians.

```python
from array import array

star = array("h", [0, -20, 6, -6, 20, -6, 9, 4, 13, 18, 0, 9, -13, 18, -9, 4, -20, -6, -6, -6])
fb.poly(100, 60, star, 0xFFE0, f=True)
```

## Three ways to call the same thing

Every shape is also a function that takes the framebuffer first, and a method
on `Draw`, which wraps anything that draws:

```python
fb.circle(50, 50, 10, 0xF800)
pygraphics.circle(fb, 50, 50, 10, 0xF800)
pygraphics.Draw(fb).circle(50, 50, 10, 0xF800)
```

All three draw the same pixels. Use the method when you have a
`FrameBuffer`. Use `Draw` when you want to draw on a display driver or on
another object that has the basic `framebuf` methods (`pixel`, `hline`,
`vline`, `fill_rect`), or when you want [clipping](update-part-of-a-screen.md#draw-inside-a-rectangle-only).

## Colours and pixel formats

`RGB565` is the usual choice for a colour screen. The other formats are for
monochrome and greyscale screens, LED strips and smaller buffers; they're
listed with their sizes under [Formats](../formats.md#pixel-formats). The
buffer must hold `width * height` pixels at the format's size, so a
`MONO_HLSB` buffer 128 by 64 is `128 * 64 // 8` bytes.

```python
from pygraphics import MONO_HLSB

oled = FrameBuffer(bytearray(128 * 64 // 8), 128, 64, MONO_HLSB)
oled.fill(0)
oled.round_rect(4, 4, 120, 56, 8, 1)
```

## Read a pixel back

`pixel(x, y, c)` sets one pixel and returns its `Area`. `pixel(x, y)` with no
colour returns the colour that's there.

```python
fb.pixel(3, 3, 0xF800)
print(hex(fb.pixel(3, 3)))      # 0xf800
```

Next: [update part of a screen](update-part-of-a-screen.md).
