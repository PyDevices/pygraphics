# Publishing and releases

One annotated tag `vX.Y.Z` publishes **both** products at that version:

| Product | Channel | Workflow |
|---------|---------|----------|
| **pygraphics-cmod** | TestPyPI (platform + Pyodide wasm wheels) | `publish-testpypi.yml` |
| **pygraphics** | TestPyPI (pure Python) + micropython-lib / MIP | `publish-micropython-lib.yml` |

## Pipeline

```text
pygraphics (commit on main)
  ./scripts/publish_release_tag.sh --push   # next patch after highest v*
           │
           ├─► publish-testpypi.yml
           │     cibuildwheel → Linux + Windows + Android → pygraphics-cmod
           │     build_pyodide_wheel.sh → pyemscripten_2026_0 wasm32
           │
           └─► publish-micropython-lib.yml
                 sync → micropython/pygraphics/
                 hatch + twine → pygraphics
                 rebuild mip/PyDevices → gh-pages
                 remove legacy micropython/graphics/ and pydisplay/graphics/
```

## Version numbers

Shared tag for **both** products. After reclaiming the historical
`pygraphics` TestPyPI line (last `0.0.24` from pydisplay), the next
release is **`v0.0.25`** (not `v0.0.11`). Later tags continue from the highest
`v*` tag:

```bash
./scripts/next_release_version.sh --verbose
./scripts/publish_release_tag.sh --dry-run
# first reclaim: ./scripts/publish_release_tag.sh 0.0.25 --push
```

## Secrets

| Secret | Purpose |
|--------|---------|
| `TESTPYPI_API_TOKEN` | TestPyPI upload (cmod + pygraphics) |
| `MICROPYTHON_LIB_DEPLOY_TOKEN` | PAT with `contents:write` on PyDevices/micropython-lib |

Grant both secrets to the **pygraphics** repository (org secret repository access).

## Install

```bash
# native (desktop / Android)
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pygraphics-cmod

# pure Python
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pygraphics
```

```python
# Pyodide / micropip (pyemscripten_2026_0 wasm32 wheel from the same release)
await micropip.install("pygraphics-cmod", index_urls="https://test.pypi.org/simple/")
```

```python
mip.install("pygraphics", index="https://PyDevices.github.io/micropython-lib/mip/PyDevices")
```

## Local cmod wheel smoke

```bash
echo "0.0.0.dev" > VERSION
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/python tests/test_pygraphics.py
```

## Local Pyodide / wasm wheel

Host Python **3.14** + Node.js (see `scripts/build_pyodide_wheel.sh`):

```bash
./scripts/build_pyodide_wheel.sh
# CI uses:
./scripts/build_pyodide_wheel.sh --no-copy
```

Produces `dist/pygraphics_cmod-*-cp314-cp314-pyemscripten_2026_0_wasm32.whl` and
optionally copies it to `web/wheels/` (+ `pygraphics.json`).

## Documentation

- **Read the Docs** (guides + pure-Python API): https://pygraphics.readthedocs.io  
  Config: `.readthedocs.yaml` + `mkdocs.yml`. Connected via the org
  [Read the Docs Community GitHub App](https://github.com/organizations/PyDevices/settings/installations/149173814)
  (no per-repo webhook). See pydisplay
  [Building docs](https://pydisplay.readthedocs.io/en/latest/building-docs/) for
  first-time import / legacy migration notes.
- **GitHub Pages** (marketing + Sourcey native API): https://pydevices.github.io/pygraphics/
