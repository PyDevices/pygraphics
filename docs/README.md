# Documentation

Hand-authored MkDocs pages live in this directory and publish to
[pygraphics.readthedocs.io](https://pygraphics.readthedocs.io).

```bash
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r docs/requirements.txt
.venv-docs/bin/mkdocs serve   # or: mkdocs build
```

A source-linked reference for the **native C bindings** — which mkdocstrings
cannot reach, since it reads Python docstrings — can be generated on demand with
Sourcey under [`tools/sourcey-api/`](../tools/sourcey-api/):

```bash
python3 tools/sourcey-api/scripts/generate_reference.py
```

Its output under `tools/sourcey-api/generated/` is **not tracked** and is not
published anywhere today. See `tools/sourcey-api/README.md`.
