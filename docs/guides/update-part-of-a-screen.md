# Update part of a screen

Sending a whole frame to a small screen over SPI is slow. Every pygraphics
drawing call returns the `Area` it changed, so you can send only those
pixels.

## Collect what changed

Add areas together to get one rectangle that covers them all:

```python
from pygraphics import FrameBuffer, RGB565

fb = FrameBuffer(bytearray(240 * 135 * 2), 240, 135, RGB565)
fb.fill(0x0000)

a = fb.fill_rect(10, 10, 20, 20, 0xF800)
b = fb.circle(60, 40, 8, 0x07E0, f=True)
dirty = a + b
print(dirty)                     # Area(10, 10, 58, 38)
```

An `Area` has `x`, `y`, `w` and `h`, and a few helpers: `contains(x, y)`,
`intersects(other)`, `clip(other)` for the overlap, and `shift(dx, dy)`.

Most calls return the area they drew. Two exceptions: `pixel(x, y)` with no
colour reads a pixel and returns its colour, and `scroll()` returns the whole
buffer, since every pixel may have moved.

## Send just that rectangle

A display driver's `blit_rect(buf, x, y, w, h)` takes a buffer holding
exactly `w * h` pixels. The framebuffer holds the whole screen, so send the
dirty rectangle one row at a time:

```python
def send(display, fb, area):
    rows = memoryview(fb.buffer)
    row_bytes = area.w * 2                      # RGB565
    for y in range(area.y, area.y + area.h):
        start = (y * fb.width + area.x) * 2
        display.blit_rect(rows[start:start + row_bytes], area.x, y, area.w, 1)

send(display_drv, fb, dirty)
```

`display_drv` is your screen's driver. Each row is one bus transfer, which is
still far less than the whole screen when the change is small. If a whole
frame changes, send it in one `blit_rect(fb.buffer, 0, 0, fb.width, fb.height)`.

## Draw inside a rectangle only

`Draw(canvas).clip(x, y, w, h)` is a context manager. Inside it, every
drawing call is cut to that rectangle; clips nest, and the clip ends with the
block.

```python
import pygraphics

draw = pygraphics.Draw(fb)
with draw.clip(100, 20, 60, 40):
    draw.fill(0x001F)                           # fills only the clip
    draw.text8("Panel", 100, 20, 0xFFFF)
    draw.circle(130, 60, 30, 0xFFE0)            # the part outside is skipped
```

This is how you redraw one panel of a screen without touching its
neighbours.

## Copy a sprite onto the picture

`blit(source, x, y, key)` copies another framebuffer in, skipping pixels of
colour `key`:

```python
sprite = FrameBuffer(bytearray(16 * 16 * 2), 16, 16, RGB565)
sprite.fill(0x0000)
sprite.circle(8, 8, 6, 0xFFE0, f=True)

fb.blit(sprite, 200, 100, 0x0000)              # black is transparent
```

To put an RGB565 sprite straight on the screen, hand its buffer to the
driver in one call: `display_drv.blit_rect(sprite.buffer, x, y, 16, 16)`.

Next: [draw text](draw-text.md).
