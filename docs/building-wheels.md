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

cibuildwheel drives pyodide-build and the emscripten toolchain:

```bash
pipx run cibuildwheel --platform pyodide
```

Wheels land in `wheelhouse/`. CI runs the same command.

Produces one wheel per Pyodide target, currently:

```
pydevices_pygraphics-<version>-cp313-cp313-pyemscripten_2025_0_wasm32.whl
pydevices_pygraphics-<version>-cp314-cp314-pyemscripten_2026_0_wasm32.whl
```

## Documentation

- **Read the Docs** (guides + pure-Python API): https://pygraphics.readthedocs.io  
  Config: `.readthedocs.yaml` + `mkdocs.yml`. Connected via the org
  [Read the Docs Community GitHub App](https://github.com/organizations/PyDevices/settings/installations)
  (no per-repo webhook). See pydevices-examples
  [Building docs](https://github.com/PyDevices/.github/blob/main/docs/building-docs.md) for
  first-time import / legacy migration notes.
- **GitHub Pages** (marketing + Sourcey native API): https://pydevices.github.io/pygraphics/
