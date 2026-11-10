# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT

"""Sphinx configuration for the pygraphics documentation.

Everything shared by the PyDevices documentation projects (theme, top bar,
Markdown and docstring setup, the reference map) comes from pydevices-docs.

The Reference section is written from ``pygraphics.pyi``, the stub that lists
every name the compiled module and the pure-Python package share, so the
pages describe both. The build copies the stub into ``_build`` as an
importable ``pygraphics`` package, so autodoc reads it and never imports the
package under ``lib/``.
"""

import sys
from pathlib import Path

from pydevices_docs import configure

globals().update(configure(
    "pygraphics", __file__,
    repo="PyDevices/pygraphics", edit_path="docs",
    version_file="../VERSION",
))

_DOCS = Path(__file__).resolve().parent
_STUB = _DOCS.parent / "pygraphics.pyi"
_STUB_ROOT = _DOCS / "_build" / "stub"


def _write_reference(app):
    """Make the stub importable and write the reference page that documents it."""
    package = _STUB_ROOT / "pygraphics"
    package.mkdir(parents=True, exist_ok=True)
    (package / "__init__.py").write_text(_STUB.read_text())
    if str(_STUB_ROOT) not in sys.path:
        sys.path.insert(0, str(_STUB_ROOT))
    for name in [n for n in sys.modules if n == "pygraphics" or n.startswith("pygraphics.")]:
        del sys.modules[name]
    page = Path(app.srcdir) / "reference" / "pygraphics.rst"
    text = "pygraphics\n==========\n\n.. automodule:: pygraphics\n"
    if not page.exists() or page.read_text() != text:
        page.write_text(text)


def setup(app):
    app.connect("builder-inited", _write_reference)
    return {"version": "1", "parallel_read_safe": True, "parallel_write_safe": True}
