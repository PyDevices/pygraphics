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

To link the **native** cmod into a CircuitPython unix build (out-of-tree
[Extending CircuitPython](https://learn.adafruit.com/extending-circuitpython)
layout via spike + `apply_cp_patches.sh` — see the
[repository README](https://github.com/PyDevices/pygraphics#circuitpython-unix)):

```bash
# siblings: circuitpython/ and pygraphics/
./apply_cp_patches.sh --apply
cd ../circuitpython/ports/unix && make -j VARIANT=coverage
```

See the [cmods workspace](https://github.com/PyDevices/cmods) for an easier way to build this repo with other user C modules (MicroPython) or extensions (CircuitPython).

## CPython — native/C extension (preferred when available)

```bash
pip install \
  -i https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  pydevices-pygraphics
```

## Pyodide / browser (WASM)

Each TestPyPI release includes a `pyemscripten_2026_0_wasm32` wheel (same semver).
micropip selects it automatically:

```python
import micropip
await micropip.install("pydevices-pygraphics", index_urls="https://test.pypi.org/simple/")
```

## CPython — pure Python (for users who do not want to compile)

```bash
pip install \
  -i https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  pydevices-pygraphics
```

## Name cutover

| Role | Current | Retired (do not use) |
|------|---------|----------------------|
| Import | `pygraphics` | `graphics` |
| Pure-Python pip | `pydevices-pygraphics` | `pygraphics` |
| Native/C pip | `pydevices-pygraphics` | `pygraphics`, `graphics-cmod` |
| MIP | `pygraphics` | `graphics` |

TestPyPI may still list the old project names until they age out; install the
**current** names above.
