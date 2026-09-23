# Newcomer's guide to pygraphics

`pygraphics` is a portable 2D framebuffer library for MicroPython,
CircuitPython, and CPython. It extends the familiar `framebuf` model with
shapes, fonts, image helpers, clipping, transparent blits, gradients, and
dirty rectangles. It has no required PyDevices hardware dependency, so it is
also useful for off-screen rendering and asset preparation.

The same `import pygraphics` API has two implementations:

- The native `pydevices-pygraphics` TestPyPI wheel is preferred on supported
  CPython, Android, and Pyodide targets.
- The MIP `pygraphics` package is the pure-Python fallback for MicroPython and
  CircuitPython or any environment without a native build.

## Start by drawing off-screen

The README shows [how to install](https://github.com/PyDevices/pygraphics#install)
either implementation and a [quick start](https://github.com/PyDevices/pygraphics#quick-start)
that draws into an off-screen framebuffer.

Drawing calls return an `Area` covering the pixels they changed. A display
driver can use that rectangle to flush only the affected part of a screen;
off-screen callers can ignore it. The practical drawing patterns are covered
by [the graphics guide](graphics-guide.md) and
[the getting-started guide](getting-started.md).

## The mental model

```text
your pixels / shapes / text
            |
            v
   FrameBuffer and canvas helpers
            |
            |-- Area: changed rectangle
            |-- buffer: pixel storage
            `-- optional display driver flush

  native C module  <-->  pure-Python fallback
          same public drawing surface
```

You can call operations as `FrameBuffer` methods, standalone functions that
take a framebuffer, or through the `Draw` styling context. The public surface
includes standard `framebuf` operations plus primitives such as circles,
polygons, rounded rectangles, arcs, gradients, text, and transparent blits.

## Repository map

| Path | Purpose |
|---|---|
| `src/` | Native C framebuffer, shape, font, file, and CPython-extension implementation. |
| `lib/pygraphics/` | Pure-Python implementation and the source of truth for generated Python API pages. |
| `micropython.mk`, `micropython.cmake`, `circuitpython.mk` | Build glue for native firmware targets. |
| `setup.py`, `pyproject.toml` | CPython native wheel build metadata. |
| `docs/` | Installation, usage, image-file, benchmark, and API documentation. |
| `tests/` | Native smoke tests and native/pure-Python parity coverage. |
| `tools/` | Comparison, benchmark, and developer helpers. |

## Native and pure-Python boundaries

Both implementations expose the normal drawing API, and the test suite checks
their parity. Four authoring-time helpers deliberately exist only in pure
Python: `export_framebuffer`, `FrameBuffer.export`,
`FrameBuffer.from_bitmap`, and `FrameBuffer.from_module`. They write or load
Python bitmap modules, which is useful asset work but not useful native
acceleration. Keep that distinction when writing portable applications.

The native wheel has platform-specific availability. Read
[installation](installation.md) for the current matrix and use the MIP package
when a native wheel is not available. A plain PyPI install can select an older
release, so prefer the documented TestPyPI command when testing current work.

## Contributor boundary

Normal users install a wheel or MIP package; building C is contributor work.
Native changes live under `src/`; pure-Python changes live under
`lib/pygraphics/`. Their behavior must stay aligned. The native and
pure-Python smoke commands are in [AGENTS.md](https://github.com/PyDevices/pygraphics/blob/main/AGENTS.md), and the parity
tools compare both implementations byte-for-byte.

After a font-source change, run `python3 scripts/sync_fonts.py`; the Python
font files are the source of truth for generated C headers. Read
[the wheel-build guide](building-wheels.md) for packaging and
[the API overview](api-overview.md) before changing public behavior. A safe
first contribution is a focused test or documentation/example improvement
that demonstrates an existing framebuffer operation.
