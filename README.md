# pygraphics

Native and pure-Python **pygraphics** for MicroPython, CircuitPython, and CPython.
The C module can be built into MicroPython or CircuitPython, while the pure-Python
package is available for users who prefer not to compile their own build.
Import as `pygraphics`.

New here? Read the [newcomer's guide](docs/newcomers.md) for the portable
framebuffer model, implementation boundary, and contributor map.

| Product | Pip / MIP | Role |
|---------|-----------|------|
| **pygraphics** | TestPyPI `pydevices-pygraphics` | Native/C-extension wheel for CPython and for embedded builds that include the module (prefer on desktop/Android/Pyodide when available) |
| **pygraphics** | MIP `pygraphics` | Pure-Python package for users who do not want to compile their own build (same public API, [bar four authoring entry points](#what-the-native-build-does-not-have)) |

One release tag `vX.Y.Z` publishes both products at that version.

## Install

```bash
# Native C extension (CPython desktop, Android, Pyodide)
pip install -i https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ pydevices-pygraphics
```

```python
# Pure Python, for MicroPython and CircuitPython
import mip
mip.install("pygraphics", index="https://PyDevices.github.io/mip")
```

Full options and verification: [docs/installation.md](docs/installation.md).

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

`pygraphics` extends MicroPython's standard `framebuf` into a powerful 2D graphics engine while preserving full compatibility with `framebuf`'s own API (proved by `tools/compare_framebuf_mp.py`):

* **Zero Dependencies & Universal Use**: No required external packages; usable in any Python application.
* **Dual Invocation & `Draw` Class**: Call methods directly on `FrameBuffer` instances (`fb.circle(...)`), invoke standalone canvas functions (`pygraphics.circle(fb, ...)`), or use the **`Draw`** styling context for maximum architectural flexibility.
* **Exposed Attributes**: Direct read-only access to `.buffer`, `.width`, `.height`, `.format`, and `.color_depth` on every `FrameBuffer` instance (stride is an internal implementation detail, not a public attribute).
* **24-bit True Color (`RGB888`)**: Supports 24-bit packed RGB color format (format constant `RGB888`), ideal for 24-bit displays as well as **NeoPixel (WS2812B)** and **DotStar (APA102)** LED matrix arrays.
* **Dirty `Area` Returns**: Drawing operations return an `Area(x, y, w, h)` bounding box so drivers can flush only modified screen regions.
* **Rich Primitive Library**: Standard shapes plus `round_rect`, `circle`, `arc`, `triangle`, `polygon`, and `gradient_rect`.
* **Multi-Font Engine**: Built-in 8x8 (`text8`), 8x14 (`text14`), 8x16 (`text16`), and custom `Font` support.
* **Image & File I/O**: Load and save images directly using `load_image`, `save_image`, `BMP565`, and PBM/PGM codecs. `export_framebuffer` and the `FrameBuffer.export` / `from_bitmap` / `from_module` trio are [pure-Python only](#what-the-native-build-does-not-have).
* **Colorkey Blitting**: `blit_transparent()` for transparent sprite overlays.
* **Native C Speed & Fallback Safety**: C acceleration compiled for MicroPython, CircuitPython, and CPython wheels (TestPyPI `pydevices-pygraphics`), with a pure-Python fallback available whenever precompiled binaries are not present in the firmware or environment.



## Support and platforms

pygraphics targets MicroPython, CircuitPython, and CPython, both as a native
C extension and as the pure-Python fallback under `lib/pygraphics/`.

The native `pydevices-pygraphics` wheel is currently built for, with each
claim's tier in the vocabulary of the org's
[platform support tiers](https://github.com/PyDevices/.github/blob/main/docs/platform-support-tiers.md):

| Platform | Arch | Tier | Notes |
|----------|------|------|-------|
| manylinux | x86_64 | CI-proven | `manylinux_2_28`; the wheel is built and the suite runs on it every release |
| Windows | AMD64 (win_amd64) | CI-proven | same |
| Android | arm64_v8a, x86_64 | community-verified | the wheel builds; nobody here has run it on a device |
| Pyodide / Emscripten | wasm32 | community-verified | the wheel builds; `pyemscripten_2025_0` for cp313 and `pyemscripten_2026_0` for cp314 — micropip picks the one matching your runtime |

**No macOS or Linux aarch64 wheels.** The cause is the bench: there is no Mac
and no aarch64 Linux runner in the release matrix, so there is nothing to
build or prove them on (the org records the same posture in
[platform-support-tiers.md](https://github.com/PyDevices/.github/blob/main/docs/platform-support-tiers.md)).
On those platforms use the pure-Python package via MIP, or copy
`lib/pygraphics/` onto `sys.path`.

### What the native build does not have

Four entry points are **pure-Python only**, and the native module does not
carry them:

| Name | |
|---|---|
| `pygraphics.export_framebuffer(fb, path)` | writes an importable `.py` bitmap module |
| `FrameBuffer.export(path)` | the method form of the same thing |
| `FrameBuffer.from_bitmap(buf, w, h, fmt)` | builds a framebuffer from such a module's `BITMAP` |
| `FrameBuffer.from_module(mod)` | the same, from the module object |

They emit and consume Python source, which is authoring-time work; putting a
source generator in a C accelerator buys nothing. Callers that need them on a
native build fall back to the pure package — pdwidgets does exactly that in
its `_icon_load.py`. `tests/test_parity.py` enforces the exclusion in both
directions, so implementing one in C fails the suite until this table changes.

Everything else in `__all__` is present on both builds, checked against the
pure package's own `__all__` rather than a copy of it.

### Which index

Current releases go to **TestPyPI** (`pydevices-pygraphics`), which is the
command under [Install](#install) above. The name is also registered on
production PyPI and currently carries **0.0.37**, one release behind
TestPyPI's 0.0.38 — so a plain `pip install pydevices-pygraphics` succeeds and
gives you the older wheel. Note that the documented install line passes
TestPyPI with `-i` and PyPI with `--extra-index-url`, and pip resolves to
whichever index has the higher version.

## Links

- [Documentation](https://pygraphics.readthedocs.io)
- [API reference](https://pygraphics.readthedocs.io/en/latest/reference/pygraphics/index.html)
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
  docs/ scripts/
```

### CPython native (editable)

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
PYGRAPHICS_TEST_NATIVE=1 .venv/bin/python -m unittest discover -s tests
```

And the pure-Python side of the same suite:

```bash
.venv/bin/python -m unittest discover -s tests
```

Those are the two commands CI runs — 15 modules, not the three this section
used to name. [`tests/README.md`](tests/README.md) explains the switch and
what each module covers.

### Pure Python (no extension)

```bash
(cd /tmp && PYTHONPATH="$OLDPWD/lib" python3 -c "import pygraphics; print(pygraphics.implementation())")
```

`PYTHONPATH=lib` alone is not enough after an in-place editable build (`pip
install -e .` / `build_ext --inplace`, above): the current directory precedes
`PYTHONPATH` on `sys.path`, so the native extension sitting at the repo root
wins over `lib/`. CI (`.github/workflows/tests.yml`) sidesteps this the same
way `tests/_env.py` does — by inserting `lib/` at the front of `sys.path`
explicitly in code rather than relying on `PYTHONPATH` — but the simplest fix
from a shell is just to run from a directory that isn't the repo root, as
above.

### Parity testing (native vs pure-Python)

```bash
micropython tools/compare_graphics_run.py    # single interpreter
python tools/compare_graphics_matrix.py      # all desktop interpreters
micropython tools/compare_framebuf_mp.py     # C framebuf vs lib/pygraphics/framebuf.py
```

All three run on a unix-port MicroPython with `pygraphics` linked in as a user
C module, and on CPython with the extension built in place; the first reports
385 checks. The `micropython` runs need a build that actually contains the
module — a stock interpreter imports the pure package and the comparison is
against itself. CI runs the first and third on every push (the `micropython`
job in [`tests.yml`](.github/workflows/tests.yml)).

### MicroPython (unix)

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

**Tested against** MicroPython v1.28.0 (what the PyDevices firmware pins) and
current master — most recently `11094ea`, 1.30.0-preview. `USER_C_MODULES`
points at the *parent directory*, and MicroPython builds every module it finds
there, so that path should hold `pygraphics/` and nothing else you do not want
linked in.

### MicroPython (MCU: ESP32, RP2, …)

The unix port above is Make-based, but the CMake-based MCU ports (`esp32`,
`rp2`, …) discover user C modules differently, via `USER_C_MODULES` pointing
at `micropython.cmake` in this repo rather than at `micropython.mk`:

```bash
idf.py build -DUSER_C_MODULES=<path to pygraphics>
```

or, alongside other user C modules, as a semicolon-separated list (no
aggregator `micropython.cmake` required):

```bash
idf.py build -DUSER_C_MODULES="<path to pygraphics>;<path to displayif>"
```

The `rp2` port takes the same `-DUSER_C_MODULES` flag via its own CMake-based
build. To build several user C modules together, name them in one manifest
(this repository's `manifest.py` carries `c_module(".")`, and a manifest that
`include()`s several such files builds them all); the
[micropython-pydevices](https://github.com/PyDevices/micropython-pydevices)
repository keeps ready-made presets, variants and boards for that.

### CircuitPython (unix)

Adafruit’s [Extending CircuitPython](https://learn.adafruit.com/extending-circuitpython)
guide (and the [design guide — native modules](https://docs.circuitpython.org/en/latest/docs/design_guide.html))
describe adding `shared-bindings/` + `shared-module/` **inside** the CircuitPython
tree. This repo keeps those sources out-of-tree under `src/circuitpython_spike/`
and applies them with `./apply_cp_patches.sh` into a local (uncommitted)
CircuitPython clone — Adafruit has no separate out-of-tree C-module path.
The build glue itself lives in `circuitpython.mk` (analogous to
`micropython.mk` for MicroPython), included by the patched variant/board
Makefile for both the unix `coverage` variant used below and MCU boards.

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

**Tested against** CircuitPython 10.2.1. The patch script edits a moving tree,
so this is the fragile recipe of the two: if `--apply` fails to find what it
expects, check the CircuitPython revision first.

To build this repo with other user C modules (MicroPython), include their manifests alongside this one; with other CircuitPython extensions, run each repository's `apply_cp_patches.sh` against the same checkout before the one `make`.

### pydevices-examples integration

When this cmod is installed or linked, `pygraphics.framebuf_backend()` reports
`native` and `pygraphics.implementation()` reports `native_cmod`. Otherwise the
pure-Python package reports `pygraphics_python`.
