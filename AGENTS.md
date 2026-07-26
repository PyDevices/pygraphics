# AGENTS.md — graphics

Native all-C **graphics** module for MicroPython, CircuitPython, and CPython
(`import graphics`). Prefer this wheel on desktop/Android when available; the
pure-Python alternative is pydisplay's `src/lib/graphics`.

## Layout

MicroPython-style usermod layout (same pattern as sibling `usdl2`):

- Root: `micropython.mk`, `micropython.cmake`, `circuitpython.mk`, `setup.py`,
  patch scripts — build glue stays here for `USER_C_MODULES` discovery
- `src/` — all `.c` sources (shared core + MP/CP bindings + CPython extension)
- `include/` — shared headers (`gfx_*.h`, `font_8x*.h`, `graphics_qstrdefs.h`)
- `tests/` — smoke and parity scripts
- No `.c` / `.h` at repo root

## Smoke

```bash
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/python tests/test_area.py
.venv/bin/python tests/test_graphics.py
.venv/bin/python tests/test_subclass.py
```

MicroPython / CircuitPython: build via cmods `./build_mp.sh` /
`lv_circuitpython_mod/build_cp.sh`, then run the same scripts under `tests/`.

## After C changes

Refresh pydisplay’s committed runtimes (desktop bins + PyScript vendor wasm)
with `../build_pydisplay_runtimes.sh` from the cmods workspace root when the
usermod is linked into those interpreters.
