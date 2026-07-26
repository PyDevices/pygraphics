# pygraphics

**pygraphics** is the cross-platform 2D drawing package for the PyDevices stack —
`Area`, framebuf-compatible `FrameBuffer`, fonts, shapes, and image loaders for
MicroPython, CircuitPython, and CPython.

| Product | Channel | Role |
|---------|---------|------|
| **pygraphics-cmod** | TestPyPI | All-C extension (`implementation()` → `native_cmod`) |
| **pygraphics** | TestPyPI + MIP | Pure-Python package (`pygraphics_python`) |

Same public API either way. Prefer the cmod on desktop/Android when a matching
wheel is available.

## Links

- [Getting started](getting-started.md)
- [Installation](installation.md)
- [API Reference](reference/pygraphics/index.md)
- [Native source-linked API (Pages)](https://pydevices.github.io/pygraphics/api/)
- [pydisplay documentation](https://pydisplay.readthedocs.io)
- [GitHub](https://github.com/PyDevices/pygraphics)
