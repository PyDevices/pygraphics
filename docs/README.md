# Documentation

Hand-authored Markdown pages (built by Sphinx; `conf.py` is here) live in this directory and publish to
[pygraphics.readthedocs.io](https://pygraphics.readthedocs.io).

```bash
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r docs/requirements.txt
.venv-docs/bin/sphinx-build -W --keep-going -b html docs docs/_build/html
```

A source-linked reference for the **native C bindings** — which autodoc
cannot reach, since it reads Python docstrings — can be generated on demand with
Sourcey under [`tools/sourcey-api/`](../tools/sourcey-api/):

```bash
python3 tools/sourcey-api/scripts/generate_reference.py
```

Its output under `tools/sourcey-api/generated/` is **not tracked** and is not
published anywhere today. See `tools/sourcey-api/README.md`.
