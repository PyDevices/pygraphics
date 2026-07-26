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

## What you get

- `Area` — rectangle geometry for dirty regions / clipping
- `FrameBuffer` — framebuf-compatible surface; draw methods return `Area`
- Format constants: `MONO_*`, `RGB565`, `GS*`, `RGB888`
- `Draw`, `Font`, BMP565 / PBM / PGM helpers
- `framebuf_backend()`, `capabilities()`, `implementation()`

## Examples

Drawing demos live in
[pydisplay `src/examples/`](https://github.com/PyDevices/pydisplay/tree/main/src/examples)
(`graphics_simpletest.py`, BMP565 samples, and others).
