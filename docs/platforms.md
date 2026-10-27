# Platforms

## Where each package runs

| Where | Package | How it's tested |
|---|---|---|
| CPython 3.11–3.14 on Linux x86_64 (manylinux_2_28) | compiled wheel, `pydevices-pygraphics` | the full tests run on every change, against both packages |
| CPython 3.11–3.14 on Windows x86_64 | compiled wheel | each release checks the wheel loads its compiled module |
| CPython 3.13–3.14 on Android, arm64-v8a and x86_64 | compiled wheel | the wheel builds; it isn't run on a device |
| Pyodide, CPython 3.13 and 3.14 | compiled wheel (`pyemscripten_2025_0` and `pyemscripten_2026_0`) | the wheel builds; micropip picks the one for your Pyodide |
| MicroPython, any port | pure-Python, from mip | the compiled module's tests and the comparison against `framebuf` run on the unix port on every change |
| CircuitPython | pure-Python, copied to `CIRCUITPY/lib/` | not tested automatically |
| macOS, Linux on ARM | pure-Python | no compiled wheel: copy `lib/pygraphics/` onto your path |

The compiled module can also be built into MicroPython or CircuitPython
firmware; [CONTRIBUTING.md](https://github.com/PyDevices/pygraphics/blob/main/CONTRIBUTING.md#build-it-into-micropython)
has the steps. `pygraphics.implementation()` tells you which one you have:
`native_cmod` for the compiled module, `pygraphics_python` for the pure one.

## Which index

Releases go to TestPyPI, which is why the install command names it. PyPI
holds one old release, 0.0.37, kept to reserve the name, so
`pip install pydevices-pygraphics` without the TestPyPI index succeeds and
gives you that old version.

## Names only the pure-Python package has

Everything in `pygraphics.__all__` is in both packages, except four names
that write or read Python source. The compiled package leaves them out:

| Name | What it does |
|---|---|
| `pygraphics.export_framebuffer(fb, path)` | writes a framebuffer as an importable `.py` module |
| `FrameBuffer.export(path)` | the same, as a method |
| `FrameBuffer.from_bitmap(buf, w, h, fmt)` | makes a framebuffer from such a module's `BITMAP` |
| `FrameBuffer.from_module(mod)` | the same, from the imported module |

## Old names

If you installed pygraphics under an earlier name, uninstall that and install
the current one.

| | Now | Earlier |
|---|---|---|
| Import | `pygraphics` | `graphics` |
| pip (compiled) | `pydevices-pygraphics` | `pygraphics`, `graphics-cmod` |
| mip | `pygraphics` | `graphics` |
