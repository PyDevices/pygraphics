# Documentation

Hand-authored MkDocs pages live in this directory and publish to
[pygraphics.readthedocs.io](https://pygraphics.readthedocs.io).

```bash
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r docs/requirements.txt
.venv-docs/bin/mkdocs serve   # or: mkdocs build
```

The native (C) source-linked API is built separately with Sourcey under
[`tools/sourcey-api/`](../tools/sourcey-api/) and deployed to
[pydevices.github.io/pygraphics/api/](https://pydevices.github.io/pygraphics/api/).
