# AGENTS.md — pygraphics

Native and pure-Python **pygraphics** (`import pygraphics`) for MicroPython,
CircuitPython, and CPython. Prefer `pygraphics-cmod` on desktop/Android when
available; otherwise `pygraphics` / MIP `pygraphics`.

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

## Publishing

One tag `vX.Y.Z` publishes:

1. **pygraphics-cmod** — `publish-testpypi.yml` (cibuildwheel)
2. **pygraphics** + MIP — `publish-micropython-lib.yml` (micropython-lib + TestPyPI + gh-pages)

See `docs/PUBLISHING.md`. Next shared version continues the `pygraphics-cmod` line
(`v0.0.9` → `v0.0.10`).

## After C changes

Refresh pydisplay’s committed runtimes with `../build_pydisplay_runtimes.sh`
from the cmods workspace root when the usermod is linked into those interpreters.

Font C headers: `python3 scripts/sync_fonts.py` (source of truth is
`lib/pygraphics/_font_8x*.py`).
