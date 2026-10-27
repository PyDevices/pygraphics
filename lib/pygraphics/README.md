# pygraphics

This folder is the pure-Python pygraphics package: `FrameBuffer`, `Draw`,
shapes, fonts and image files, with the same API as the compiled module.
Import it as `pygraphics`.

On a MicroPython-compatible board, install it with mip:

```python
import mip
mip.install("pygraphics", index="https://PyDevices.github.io/mip")
```

On a CircuitPython-compatible board, copy this folder to `CIRCUITPY/lib/`.
On CPython, install the compiled package instead:

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pydevices-pygraphics
```

```python
import pygraphics

fb = pygraphics.FrameBuffer(bytearray(160 * 128 * 2), 160, 128, pygraphics.RGB565)
fb.fill(0)
print(fb.fill_rect(10, 10, 40, 40, 0xF800))   # Area(10, 10, 40, 40)
print(pygraphics.implementation())            # pygraphics_python
```

[Docs](https://pygraphics.readthedocs.io) · [Source](https://github.com/PyDevices/pygraphics)
