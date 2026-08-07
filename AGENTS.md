# AGENTS.md — pygraphics

Native and pure-Python **pygraphics** (`import pygraphics`) for MicroPython,
CircuitPython, and CPython. Prefer the native `pygraphics` wheel on desktop/Android when
available; otherwise use the pure-Python `pygraphics` package from MIP.

## Layout

- Root: `micropython.mk`, `micropython.cmake`, `circuitpython.mk`, `setup.py`,
  patch scripts — build glue stays here for `USER_C_MODULES` discovery
- `src/` — `.c` sources and shared headers (`gfx_*.h`, `font_8x*.h`,
  `pygraphics_qstrdefs.h`)
- `lib/pygraphics/` — pure-Python package (same public API as the cmod)
- `tests/` — native smoke and parity scripts
- `tools/` — developer benchmarks / helpers (not maintainer publish scripts)
- No `.c` / `.h` at repo root

## Smoke

```bash
# native
python3 -m venv .venv
echo 0.0.0 > VERSION
.venv/bin/pip install -e .
.venv/bin/python tests/test_area.py
.venv/bin/python tests/test_pygraphics.py

# pure Python
PYTHONPATH=lib .venv/bin/python -c "import pygraphics; assert pygraphics.implementation() == 'pygraphics_python'"
```

## Parity testing (native vs pure-Python)

`tools/compare_graphics*.py` and `tools/compare_framebuf_mp.py` byte-compare
native `pygraphics` against the pure-Python `lib/pygraphics` package (and, for
`framebuf`, MicroPython's built-in C `framebuf` against `lib/pygraphics/framebuf.py`).
Run from the repo root:

```bash
micropython tools/compare_graphics_run.py    # single runtime, native + staged lib/pygraphics
python tools/compare_graphics_matrix.py      # all desktop runtimes (installs pygraphics
                                              # from TestPyPI for cpython-venv/python.exe)
micropython tools/compare_framebuf_mp.py     # MicroPython C framebuf vs lib/pygraphics/framebuf.py
```

`compare_graphics_matrix.py` resolves runtimes itself (PATH, `~/bin/<name>`,
and `.venv/bin/python` for `cpython-venv`) — it has no dependency on
pydisplay's `tools/example_runtimes.toml`.

## Publishing

One tag `vX.Y.Z` publishes:

1. **pygraphics** (native/C-extension) — `publish-testpypi.yml` (cibuildwheel Linux/Windows/Android
   + Pyodide `pyemscripten_2026_0` wasm32 via `scripts/build_pyodide_wheel.sh`)
2. **pygraphics** (pure Python) + MIP — `publish-micropython-lib.yml` (micropython-lib + gh-pages)

See `docs/publishing.md`. The next shared release continues the `pygraphics` line.
(`v0.0.9` → `v0.0.10`).

## After C changes

Font C headers: `python3 scripts/sync_fonts.py` (source of truth is
`lib/pygraphics/_font_8x*.py`).

## Documentation

- MkDocs under `docs/` → https://pygraphics.readthedocs.io (`.readthedocs.yaml`)
- Sourcey native API under `tools/sourcey-api/` → Pages `/api/`
- Local: `python3 -m venv .venv-docs && .venv-docs/bin/pip install -r docs/requirements.txt && .venv-docs/bin/mkdocs serve`

