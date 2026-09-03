# Installation

## Platform matrix

| Platform | Arch | Path |
|----------|------|------|
| MicroPython / CircuitPython (any MCU or unix port) | any | MIP / pure-Python copy — see below |
| CPython — Linux | manylinux x86_64 | Native wheel (TestPyPI) |
| CPython — Windows | AMD64 | Native wheel (TestPyPI) |
| CPython — Android | arm64_v8a, x86_64 | Native wheel (TestPyPI) |
| Pyodide / browser | wasm32 | Native wheel (TestPyPI, `pyemscripten_2026_0_wasm32`) |
| CPython — macOS | x86_64, arm64 | Not built yet — use MIP / pure-Python |
| CPython — Linux aarch64 | aarch64 | Not built yet — use MIP / pure-Python |

Native wheels are published to TestPyPI only; this is deliberate, not a
placeholder. macOS and Linux aarch64 are deliberately not built yet — install
the pure-Python package via MIP (or copy `lib/pygraphics/` onto `sys.path`)
on those platforms instead; the public API is identical either way.

## MicroPython (MIP)

```python
import mip
mip.install("pygraphics", index="https://PyDevices.github.io/mip")
```

The package path on mip is `micropython/pygraphics/` (import name
`pygraphics`). Older installs that used MIP name `graphics` should reinstall
under the new name — the cutover publish already went out.

## CircuitPython / copy install

Copy the `pygraphics/` package folder onto `sys.path` (from
`lib/pygraphics/` in this repo, or from mip).

To link the **native** cmod into a CircuitPython unix build (out-of-tree
[Extending CircuitPython](https://learn.adafruit.com/extending-circuitpython)
layout via spike + `apply_cp_patches.sh` — see the
[repository README](https://github.com/PyDevices/pygraphics#circuitpython-unix)):

```bash
# siblings: circuitpython/ and pygraphics/
./apply_cp_patches.sh --apply
cd ../circuitpython/ports/unix && make -j VARIANT=coverage
```

See the org's [optional aggregator workspace](https://github.com/PyDevices/cmods) for an easier way to build this repo with other user C modules (MicroPython) or extensions (CircuitPython).

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

## Name cutover

| Role | Current | Retired (do not use) |
|------|---------|----------------------|
| Import | `pygraphics` | `graphics` |
| Pure-Python pip | Not published; use MIP | `pygraphics` |
| Native/C pip | `pydevices-pygraphics` | `pygraphics`, `graphics-cmod` |
| MIP | `pygraphics` | `graphics` |

TestPyPI may still list the old project names until they age out; install the
**current** names above.
