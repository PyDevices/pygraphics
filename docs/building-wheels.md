# Building pygraphics wheels

The release procedure is org-wide and lives in
[.github/docs/publishing-automation.md](https://github.com/PyDevices/.github/blob/main/docs/publishing-automation.md) — standard steps, shared
workflows, secrets, and the MIP queue. This page is the pygraphics-specific
build detail.

One published GitHub Release `vX.Y.Z` produces the **pydevices-pygraphics**
native/C-extension wheels (cibuildwheel for Linux, Windows, and Android, plus a
Pyodide `pyemscripten_2026_0` wasm32 wheel) and the unprefixed pure-Python
**pygraphics** MIP package. There is no pure-Python pip distribution — use MIP
for that implementation.

## Local cmod wheel smoke

```bash
echo "0.0.0.dev" > VERSION
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/python tests/test_pygraphics.py
```

After publishing to TestPyPI, verify the namespaced distribution in a fresh
environment:

```bash
./tools/test_testpypi_standalone.sh
```

## Local Pyodide / wasm wheel

Host Python **3.14** + Node.js (see `scripts/build_pyodide_wheel.sh`):

```bash
./scripts/build_pyodide_wheel.sh
# CI uses:
./scripts/build_pyodide_wheel.sh --no-copy
```

Produces `dist/pydevices_pygraphics-*-cp314-cp314-pyemscripten_2026_0_wasm32.whl` and
optionally copies it to `web/wheels/` (+ `pygraphics.json`).

## Documentation

- **Read the Docs** (guides + pure-Python API): https://pygraphics.readthedocs.io  
  Config: `.readthedocs.yaml` + `mkdocs.yml`. Connected via the org
  [Read the Docs Community GitHub App](https://github.com/organizations/PyDevices/settings/installations)
  (no per-repo webhook). See pydevices-examples
  [Building docs](https://github.com/PyDevices/.github/blob/main/docs/building-docs.md) for
  first-time import / legacy migration notes.
- **GitHub Pages** (marketing + Sourcey native API): https://pydevices.github.io/pygraphics/
