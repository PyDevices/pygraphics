# pygraphics

Native and pure-Python **pygraphics** for MicroPython, CircuitPython, and CPython.
The C module can be built into MicroPython or CircuitPython, while the pure-Python
package is available for users who prefer not to compile their own build.
Import as `pygraphics`.

| Product | Pip / MIP | Role |
|---------|-----------|------|
| **pygraphics** | TestPyPI `pydevices-pygraphics` | Native/C-extension wheel for CPython and for embedded builds that include the module (prefer on desktop/Android/Pyodide when available) |
| **pygraphics** | MIP `pygraphics` | Pure-Python package for users who do not want to compile their own build (same public API) |

One release tag `vX.Y.Z` publishes both products at that version.

## Install

### Native (TestPyPI)

```bash
pip install \
  -i https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  pydevices-pygraphics
```

### Pure Python (MIP)

```python
import mip
mip.install("pygraphics", index="https://PyDevices.github.io/micropython-lib/mip/PyDevices")
```

### MicroPython (MIP)

```python
import mip
mip.install("pygraphics", index="https://PyDevices.github.io/micropython-lib/mip/PyDevices")
```

### Quick start

```python
import pygraphics
from pygraphics import FrameBuffer, RGB565

fb = FrameBuffer(bytearray(160 * 128 * 2), 160, 128, RGB565)
fb.fill(0)
fb.fill_rect(10, 10, 40, 40, 0xF800)
print(pygraphics.implementation())  # native_cmod or pygraphics_python
```

`pygraphics` has **zero external dependencies** on any other PyDevices libraries or hardware modules. It functions as an independent, portable 2D graphics engine that can be used in any MicroPython, CircuitPython, or CPython project needing fast drawing primitives or off-screen framebuffer manipulation, regardless of whether you are using PyDevices displays.

`pygraphics` extends MicroPython's standard `framebuf` into a powerful 2D graphics engine while preserving full API compatibility:

* **Zero Dependencies & Universal Use**: No required external packages; usable in any Python application.
* **Dual Invocation & `Draw` Class**: Call methods directly on `FrameBuffer` instances (`fb.circle(...)`), invoke standalone canvas functions (`pygraphics.circle(fb, ...)`), or use the **`Draw`** styling context for maximum architectural flexibility.
* **Exposed Attributes**: Direct read-only access to `.buf`, `.width`, `.height`, `.stride`, `.format`, and `.color_depth` on every `FrameBuffer` instance.
* **24-bit True Color (`RGB888`)**: Supports 24-bit packed RGB color format (format constant `RGB888`), ideal for 24-bit displays as well as **NeoPixel (WS2812B)** and **DotStar (APA102)** LED matrix arrays.
* **Dirty `Area` Returns**: Drawing operations return an `Area(x, y, w, h)` bounding box so drivers can flush only modified screen regions.
* **Rich Primitive Library**: Standard shapes plus `round_rect`, `circle`, `arc`, `triangle`, `polygon`, and `gradient_rect`.
* **Multi-Font Engine**: Built-in 8x8 (`text8`), 8x14 (`text14`), 8x16 (`text16`), and custom `Font` support.
* **Image & File I/O**: Load and save images directly using `load_image`, `save_image`, `export_framebuffer`, `BMP565`, and PBM/PGM codecs.
* **Colorkey Blitting**: `blit_transparent()` for transparent sprite overlays.
* **Native C Speed & Fallback Safety**: C acceleration compiled for MicroPython, CircuitPython, and CPython wheels (TestPyPI `pydevices-pygraphics`), with a pure-Python fallback available whenever precompiled binaries are not present in the firmware or environment.



## Links

- [Documentation](https://pygraphics.readthedocs.io)
- [Source-linked API reference](https://pydevices.github.io/pygraphics/api/)
- [Source](https://github.com/PyDevices/pygraphics)
- [Issues](https://github.com/PyDevices/pygraphics/issues)
- Related: [pydevices-examples](https://github.com/PyDevices/pydevices-examples)

## License

MIT (framebuf algorithms derived from MicroPython `extmod/modframebuf.c`, Damien P. George).


---

## Build from source

### Layout

```
pygraphics/
  micropython.mk / micropython.cmake / circuitpython.mk / setup.py
  src/                     # C sources + headers (gfx_*.h, font_8x*.h, qstrs)
  lib/pygraphics/            # pure-Python package (import pygraphics)
  tests/                   # native smoke / parity tests
  tools/                   # developer benchmarks / helpers
  docs/ scripts/ web/
```

### CPython native (editable)

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/python tests/test_area.py
.venv/bin/python tests/test_pygraphics.py
.venv/bin/python tests/test_subclass.py
```

### Pure Python (no extension)

```bash
PYTHONPATH=lib python3 -c "import pygraphics; print(pygraphics.implementation())"
```

### Parity testing (native vs pure-Python)

```bash
micropython tools/compare_graphics_run.py    # single runtime
python tools/compare_graphics_matrix.py      # all desktop runtimes
micropython tools/compare_framebuf_mp.py     # C framebuf vs lib/pygraphics/framebuf.py
```

### MicroPython

Clone as a sibling of `micropython/`:

```
workspace/
  pygraphics/     ← this repo
  micropython/
```

```bash
cd micropython/ports/unix
make submodules
make USER_C_MODULES=../../..
cd ../../..
./micropython/ports/unix/build-standard/micropython pygraphics/tests/test_area.py
```

### CircuitPython (unix)

Adafruit’s [Extending CircuitPython](https://learn.adafruit.com/extending-circuitpython)
guide (and the [design guide — native modules](https://docs.circuitpython.org/en/latest/docs/design_guide.html))
describe adding `shared-bindings/` + `shared-module/` **inside** the CircuitPython
tree. This repo keeps those sources out-of-tree under `src/circuitpython_spike/`
and applies them with `./apply_cp_patches.sh` into a local (uncommitted)
CircuitPython clone — Adafruit has no separate out-of-tree C-module path.

| Adafruit step | This repo |
|---------------|-----------|
| `shared-bindings/<mod>/` | `src/circuitpython_spike/shared-bindings/pygraphics/` |
| `shared-module/<mod>/` | `src/circuitpython_spike/shared-module/pygraphics/` |
| Enable `CIRCUITPY_*` | Patches set `CIRCUITPY_PYGRAPHICS` |
| List sources in port Makefile | Variant `.mk` + `SRC_PATTERNS` |
| Build | `make` after `--apply` |

Clone as a sibling of `circuitpython/`:

```bash
# siblings: circuitpython/ and pygraphics/
./apply_cp_patches.sh --apply
cd ../circuitpython/ports/unix && make -j VARIANT=coverage
```

See the [cmods workspace](https://github.com/PyDevices/cmods) for an easier way to build this repo with other user C modules (MicroPython) or extensions (CircuitPython).

### pydevices-examples integration

When this cmod is installed or linked, `pygraphics.framebuf_backend()` reports
`native` and `pygraphics.implementation()` reports `native_cmod`. Otherwise the
pure-Python package reports `pygraphics_python`.
