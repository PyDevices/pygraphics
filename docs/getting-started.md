# Getting started

## Setup

Install from [MIP](installation.md) or [TestPyPI](installation.md):

```python
import mip
mip.install("pygraphics", index="https://PyDevices.github.io/micropython-lib/mip/PyDevices")
```

Development clone — put `lib/` on `PYTHONPATH`, or `pip install -e .` for the
native cmod.

## Basic usage

```python
import pygraphics
from pygraphics import FrameBuffer, RGB565, Area

fb = FrameBuffer(bytearray(160 * 128 * 2), 160, 128, RGB565)
fb.fill(0)
area = fb.fill_rect(10, 10, 40, 40, 0xF800)
assert isinstance(area, Area)
print(pygraphics.implementation())  # native_cmod or pygraphics_python
```

## Common patterns

### Draw to an off-screen buffer first

Use a `FrameBuffer` or the display driver itself as a canvas, then copy the
result to the display. This is the pattern used by pydisplay's animated demos:

```python
import pygraphics
from pygraphics import FrameBuffer, RGB565, text8

buf = FrameBuffer(bytearray(160 * 128 * 2), 160, 128, RGB565)
buf.fill(0x0000)
pygraphics.fill_rect(buf, 10, 10, 40, 20, 0xF800)
text8(buf, "Hello", 12, 14, 0xFFFF)
```

### Use the returned `Area` as a dirty rectangle

Many draw helpers return an `Area` describing the pixels they changed. That is
useful when you want to refresh only the part of the screen that changed instead
of redrawing the whole frame.

```python
area = pygraphics.circle(buf, 80, 40, 12, 0x07E0, f=True)
# area.x, area.y, area.w, area.h describe the changed region
```

### Build a scene, then present it

For simple UI work, clear the frame, draw widgets or text, and then present the
updated buffer. The pydisplay examples use that pattern for bouncing balls,
scrolling text, and gradient backgrounds.

## What you get

- `Area` — rectangle geometry for dirty regions / clipping
- `FrameBuffer` — framebuf-compatible surface; draw methods return `Area`
- Format constants: `MONO_*`, `RGB565`, `GS*`, `RGB888`
- `Draw`, `Font`, BMP565 / PBM / PGM helpers
- `implementation()` — tells you whether the native cmod or pure-Python package is active

## Examples

Drawing demos live in
[pydisplay `src/examples/`](https://github.com/PyDevices/pydisplay/tree/main/src/examples)
for patterns such as bouncing balls, scrolling text, and gradient scenes.
