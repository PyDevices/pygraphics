# Publishing and releases

One annotated tag `vX.Y.Z` publishes **both** products at that version:

| Product | Channel | Workflow |
|---------|---------|----------|
| **graphics-cmod** | TestPyPI (platform wheels) | `publish-testpypi.yml` |
| **graphics-py** | TestPyPI (pure Python) + micropython-lib / MIP | `publish-micropython-lib.yml` |

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
                 hatch + twine → graphics-py
                 rebuild mip/PyDevices → gh-pages
                 remove legacy micropython/pydisplay/graphics/
```

## Version numbers

Continue the **graphics-cmod** line (`v0.0.9` → `v0.0.10`, …). Preview:

```bash
./scripts/next_release_version.sh --verbose
./scripts/publish_release_tag.sh --dry-run
```

## Secrets

| Secret | Purpose |
|--------|---------|
| `TESTPYPI_API_TOKEN` | TestPyPI upload (cmod + graphics-py) |
| `MICROPYTHON_LIB_DEPLOY_TOKEN` | PAT with `contents:write` on PyDevices/micropython-lib |

Grant both secrets to the **graphics** repository (org secret repository access).

## Install

```bash
# native
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ graphics-cmod

# pure Python
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ graphics-py
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
