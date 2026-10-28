# Contributing to pygraphics

pygraphics is two implementations of one API: C under `src/` and pure Python
under [`lib/pygraphics/`](lib/pygraphics/). A change to one needs the same change in the other,
and the tests run against both. A focused test, or a docs example that shows
an existing call, is a good first contribution.

## Where things are

| Path | What's there |
|---|---|
| `src/` | the C module, and its bindings for MicroPython, CircuitPython and CPython |
| `lib/pygraphics/` | the pure-Python package; the API reference is generated from its docstrings |
| `micropython.mk`, `micropython.cmake`, `manifest.py` | build glue for MicroPython and CircuitPython firmware |
| `setup.py`, `pyproject.toml` | the CPython wheel |
| `tests/` | one suite for both implementations; [tests/README.md](tests/README.md) explains the switch |
| `tools/` | comparison tools and `benchmark.py` |
| [`scripts/sync_fonts.py`](scripts/sync_fonts.py) | writes the C font headers from the Python font files |
| `docs/` | the documentation site |

## Run the tests

Pure Python, which needs nothing built:

```bash
python3 -m unittest discover -s tests
```

The compiled module, built in place:

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
PYGRAPHICS_TEST_NATIVE=1 .venv/bin/python -m unittest discover -s tests
```

These are the two runs CI makes on every change. `PYTHONPATH=lib` alone does
not select the pure package once you've built in place, because the
repository root comes before `PYTHONPATH` on `sys.path` and the compiled
module there wins. [`tests/_env.py`](tests/_env.py) handles that for the suite; from a shell,
run from another directory.

## Compare the two implementations

```bash
micropython tools/compare_graphics_run.py    # compiled vs pure, byte for byte
python tools/compare_graphics_matrix.py      # the same on every desktop interpreter it finds
micropython tools/compare_framebuf_mp.py     # MicroPython's framebuf vs lib/pygraphics/framebuf.py
```

The `micropython` runs need a build with the C module linked in, as below;
on a stock build the comparison is the pure package against itself. CI runs
the first and third on every change.

After you change a font in `lib/pygraphics/_font_8x*.py`, regenerate the C
headers:

```bash
python3 scripts/sync_fonts.py
```

## Build it into MicroPython

With MicroPython 1.29 or later, add one line to the manifest your build
uses:

```python
include("/path/to/pygraphics/manifest.py")
```

On unix that's `ports/unix/variants/standard/manifest.py`; on esp32 and rp2
it's usually `ports/<port>/boards/manifest.py`, unless your board brings its
own. Then build as usual:

```bash
cd micropython/ports/unix
make submodules && make
./build-standard/micropython -c "import pygraphics; print(pygraphics.implementation())"
```

That prints `native_cmod`. The manifest adds the C module with `c_module()`
and freezes nothing.

To leave the MicroPython tree alone, write your own manifest and pass it as
`FROZEN_MANIFEST=`. That replaces the port's default manifest, so include the
default too (`include("$(PORT_DIR)/variants/standard/manifest.py")` on unix,
`include("$(PORT_DIR)/boards/manifest.py")` on esp32), or you lose `asyncio`
and the port's other frozen modules.

Before 1.29, manifests have no `c_module()`, so use `USER_C_MODULES`. On
esp32 and rp2, point it at this repository:
`make BOARD=<board> USER_C_MODULES=/path/to/pygraphics/micropython.cmake`.
On Make ports such as unix, point it at a directory that *contains* this
repository; MicroPython builds every module it finds there, so keep that
directory to the modules you want. CI builds the unix port of MicroPython
1.28.0 this way.

MicroPython's [manifest reference](https://docs.micropython.org/en/v1.29.0/reference/manifest.html)
has more on `c_module()` and `include()`.
[micropython-pydevices](https://github.com/PyDevices/micropython-pydevices)
keeps ready-made manifests and boards for building several PyDevices modules
at once.

## Build it into CircuitPython

CircuitPython builds user C modules through `USER_C_MODULES` too, with
`micropython.mk` as the glue. From a CircuitPython 11 checkout:

```bash
make -C ports/unix -j VARIANT=coverage USER_C_MODULES=/path/to/pygraphics
make -C ports/raspberrypi -j BOARD=adafruit_feather_rp2040 USER_C_MODULES=/path/to/pygraphics
```

This has been built on CircuitPython 11.0.0-alpha.1 for unix, raspberrypi
(Feather RP2040) and atmel-samd (Feather M4 Express, with `CIRCUITPY_ULAB=0`
to fit in 512 KB). The atmel-samd and raspberrypi ports turn some warnings
into errors; `micropython.mk` turns them off again for this module's files
only. To build with other user C modules, list them all in the one
`USER_C_MODULES`.

## Build the wheels

cibuildwheel builds them from the settings in `pyproject.toml`: CPython on
Linux x86_64, Windows and Android, and one wheel per supported Pyodide
version. For the browser wheels:

```bash
pipx run cibuildwheel --platform pyodide
```

Wheels land in `wheelhouse/`.

## Build the docs

```bash
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r docs/requirements.txt
.venv-docs/bin/sphinx-build -W --keep-going -b html docs docs/_build/html
```

The API reference under `docs/reference/` is generated during the build and
isn't tracked. Sphinx reads Python docstrings, so it can't see the C module;
[`tools/sourcey-api/`](tools/sourcey-api/) generates a reference for the C bindings on demand, and
its README says how.

`lib/pygraphics` is the source of truth for the generated Python API pages.
Keep guidance true for both the compiled module and the pure-Python package:
don't document an API shape that differs between them, and prefer worked
examples (off-screen rendering, dirty rectangles, hit testing, sprite blits,
gradients, text) over bare method lists.

## Releases

Each release tag `vX.Y.Z` publishes the compiled wheels to TestPyPI as
`pydevices-pygraphics` and the pure package to the mip index as `pygraphics`,
both at that version.
