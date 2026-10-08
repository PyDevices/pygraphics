# Installation

## Platform matrix

Tiers are the org's
[platform support tiers](https://github.com/PyDevices/.github/blob/main/docs/platform-support-tiers.md).

| Platform | Arch | Tier | Path |
|----------|------|------|------|
| MicroPython / CircuitPython (any MCU or unix port) | any | CI-proven (unix port) | MIP / pure-Python copy — see below |
| CPython — Linux | manylinux x86_64 | CI-proven | Native wheel (TestPyPI) |
| CPython — Windows | AMD64 | CI-proven | Native wheel (TestPyPI) |
| CPython — Android | arm64_v8a, x86_64 | community-verified | Native wheel (TestPyPI); builds, never run on a device here |
| Pyodide / browser | wasm32 | community-verified | Native wheel (TestPyPI); `pyemscripten_2025_0` for cp313, `pyemscripten_2026_0` for cp314 |
| CPython — macOS | x86_64, arm64 | — | No wheel: no Mac on the bench — use MIP / pure-Python |
| CPython — Linux aarch64 | aarch64 | — | No wheel: no aarch64 runner — use MIP / pure-Python |

Current releases go to TestPyPI; install from there. Production PyPI holds one
older release (0.0.37, against TestPyPI's 0.0.38), parked to reserve the name,
so a plain `pip install pydevices-pygraphics` succeeds and gives the older wheel.

The public API is the same on both builds **except** for four authoring entry
points — `export_framebuffer`, and `FrameBuffer.export` / `from_bitmap` /
`from_module` — which are pure-Python only. See
[what the native build does not have](https://github.com/PyDevices/pygraphics#what-the-native-build-does-not-have).

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

To build the **native** module into CircuitPython, hand this repository to the
port's `make` as a user C module:

```bash
make -C ports/unix -j VARIANT=coverage USER_C_MODULES=/path/to/pygraphics
```

That works on CircuitPython 11 and on boards as well as unix; the
[repository README](https://github.com/PyDevices/pygraphics#circuitpython) has
the board command and what was tested. The MicroPython recipe is tested against
v1.28.0 and current master.

## CPython — native/C extension (preferred when available)

```bash
pip install \
  -i https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  pydevices-pygraphics
```

## Pyodide / browser (WASM)

Each TestPyPI release includes wasm wheels — `pyemscripten_2025_0_wasm32` for
cp313 and `pyemscripten_2026_0_wasm32` for cp314 (same semver). micropip
selects the one matching your runtime automatically:

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
