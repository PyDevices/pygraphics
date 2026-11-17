# pygraphics

This folder is the pure-Python pygraphics package: `FrameBuffer`, `Draw`,
shapes, fonts and image files, with the same API as the compiled module.
Import it as `pygraphics`.

On a MicroPython-compatible board, install it with mip:

```python
import omip
omip.install("pygraphics")
```

`omip` comes with OmniPython firmware. On other MicroPython firmware, run
`mip.install("github:PyDevices/omnipython/lib/omip.py")` once to put it on the board.

On a CircuitPython-compatible board, copy this folder to `CIRCUITPY/lib/`.
On CPython, install the compiled package instead:

```bash
pip install omnipython-pygraphics
```

```python
import pygraphics

fb = pygraphics.FrameBuffer(bytearray(160 * 128 * 2), 160, 128, pygraphics.RGB565)
fb.fill(0)
print(fb.fill_rect(10, 10, 40, 40, 0xF800))   # Area(10, 10, 40, 40)
print(pygraphics.implementation())            # pygraphics_python
```

[Docs](https://docs.omnipython.org/en/latest/pygraphics/) · [Source](https://github.com/PyDevices/pygraphics)
