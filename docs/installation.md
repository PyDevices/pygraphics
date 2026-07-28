# Installation

## MicroPython (MIP)

```python
import mip
mip.install("pygraphics", index="https://PyDevices.github.io/micropython-lib/mip/PyDevices")
```

The package path on micropython-lib is `micropython/pygraphics/` (import name
`pygraphics`). Older installs that used MIP name `graphics` should reinstall
under the new name after the next publish.

## CircuitPython / copy install

Copy the `pygraphics/` package folder onto `sys.path` (from
`lib/pygraphics/` in this repo, or from micropython-lib).

## CPython — native (preferred when available)

```bash
pip install \
  -i https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  pygraphics-cmod
```

## Pyodide / browser (WASM)

Each TestPyPI release includes a `pyemscripten_2026_0_wasm32` wheel (same semver).
micropip selects it automatically:

```python
import micropip
await micropip.install("pygraphics-cmod", index_urls="https://test.pypi.org/simple/")
```

## CPython — pure Python

```bash
pip install \
  -i https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  pygraphics
```

## Name cutover

| Role | Current | Retired (do not use) |
|------|---------|----------------------|
| Import | `pygraphics` | `graphics` |
| Pure-Python pip | `pygraphics` | `pydisplay-graphics` |
| Native pip | `pygraphics-cmod` | `graphics-cmod` |
| MIP | `pygraphics` | `graphics` |

TestPyPI may still list the old project names until they age out; install the
**current** names above.
