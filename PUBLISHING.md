# Publishing and releases

One annotated tag `vX.Y.Z` publishes **both** products at that version:

| Product | Channel | Workflow |
|---------|---------|----------|
| **graphics-cmod** | TestPyPI (platform wheels) | `publish-testpypi.yml` |
| **pydisplay-graphics** | TestPyPI (pure Python) + micropython-lib / MIP | `publish-micropython-lib.yml` |

## Pipeline

```text
graphics (commit on main)
  ./scripts/publish_release_tag.sh --push   # next patch after highest v*
           │
           ├─► publish-testpypi.yml
           │     cibuildwheel → Linux + Windows + Android → graphics-cmod
           │
           └─► publish-micropython-lib.yml
                 sync → micropython/graphics/
                 hatch + twine → pydisplay-graphics
                 rebuild mip/PyDevices → gh-pages
                 remove legacy micropython/pydisplay/graphics/
```

## Version numbers

Shared tag for **both** products. After reclaiming the historical
`pydisplay-graphics` TestPyPI line (last `0.0.24` from pydisplay), the next
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
| `TESTPYPI_API_TOKEN` | TestPyPI upload (cmod + pydisplay-graphics) |
| `MICROPYTHON_LIB_DEPLOY_TOKEN` | PAT with `contents:write` on PyDevices/micropython-lib |

Grant both secrets to the **graphics** repository (org secret repository access).

## Install

```bash
# native
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ graphics-cmod

# pure Python
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pydisplay-graphics
```

```python
mip.install("graphics", index="https://PyDevices.github.io/micropython-lib/mip/PyDevices")
```

## Local cmod wheel smoke

```bash
echo "0.0.0.dev" > VERSION
python3 -m venv .venv
.venv/bin/pip install -e .
.venv/bin/python tests/test_graphics.py
```
