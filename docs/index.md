# pygraphics

**pygraphics** is the cross-platform 2D drawing package for the PyDevices stack —
`Area`, framebuf-compatible `FrameBuffer`, fonts, shapes, and image loaders for
MicroPython, CircuitPython, and CPython.

| Product | Channel | Role |
|---------|---------|------|
| **pydevices-pygraphics** | TestPyPI | Native/C-extension wheel, imported as `pygraphics`, for embedded builds and CPython (`implementation()` → `native_cmod`) |
| **pygraphics** | MIP | Pure-Python package for users who do not want to compile their own build (`pygraphics_python`) |

Same public API either way. Prefer the cmod on desktop/Android/Pyodide when a
matching wheel is available.

## Links

- [Getting started](getting-started.md)
- [Installation](installation.md)
- [API Reference](reference/pygraphics/index.md)
- [Native source-linked API (Pages)](https://pydevices.github.io/pygraphics/api/)
- [pydisplay documentation](https://pydisplay.readthedocs.io)
- [GitHub](https://github.com/PyDevices/pygraphics)
