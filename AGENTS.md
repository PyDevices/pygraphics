# AGENTS.md — graphics

Native and pure-Python **graphics** (`import graphics`) for MicroPython,
CircuitPython, and CPython. Prefer `graphics-cmod` on desktop/Android when
available; otherwise `graphics-py` / MIP `graphics`.

## Layout

- Root: `micropython.mk`, `micropython.cmake`, `circuitpython.mk`, `setup.py`,
  patch scripts — build glue stays here for `USER_C_MODULES` discovery
- `src/` — all `.c` sources (shared core + MP/CP bindings + CPython extension)
- `include/` — shared headers (`gfx_*.h`, `font_8x*.h`, `graphics_qstrdefs.h`)
- `lib/graphics/` — pure-Python package (same public API as the cmod)
- `tests/` — native smoke and parity scripts
- No `.c` / `.h` at repo root

## Smoke

```bash
# native
python3 -m venv .venv
echo 0.0.0 > VERSION
.venv/bin/pip install -e .
.venv/bin/python tests/test_area.py
.venv/bin/python tests/test_graphics.py

# pure Python
PYTHONPATH=lib .venv/bin/python -c "import graphics; assert graphics.implementation() == 'graphics_python'"
```

## Publishing

One tag `vX.Y.Z` publishes:

1. **graphics-cmod** — `publish-testpypi.yml` (cibuildwheel)
2. **graphics-py** + MIP — `publish-micropython-lib.yml` (micropython-lib + TestPyPI + gh-pages)

See `PUBLISHING.md`. Next shared version continues the `graphics-cmod` line
(`v0.0.9` → `v0.0.10`).

## After C changes

Refresh pydisplay’s committed runtimes with `../build_pydisplay_runtimes.sh`
from the cmods workspace root when the usermod is linked into those interpreters.

Font C headers: `python3 scripts/sync_fonts.py` (source of truth is
`lib/graphics/_font_8x*.py`).
