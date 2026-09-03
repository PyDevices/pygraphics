# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Select which pygraphics implementation the tests import.

pygraphics ships twice: a pure-Python package under ``lib/`` and a native C
extension built in-place at the repo root. Both must behave identically, and
several tests exist only to prove it.

Whichever test module imports ``pygraphics`` first fixes the choice for the whole
process, so leaving it to discovery order makes results depend on filenames.
This module makes it explicit and deterministic:

* default -- pure Python. ``lib/`` goes first on ``sys.path``. Works in a fresh
  checkout with nothing built.
* ``PYGRAPHICS_TEST_NATIVE=1`` -- the in-place native build. ``lib/`` is left
  off, so the extension at the repo root wins.

Every test module must import this before importing pygraphics.

This module must also import under MicroPython and CircuitPython: the README's
unix-port build ends with ``micropython tests/test_area.py``. Those runtimes
have ``os.getenv`` but no ``os.environ``, ``os.path`` or ``pathlib``, so the
``lib/`` path is built from ``__file__`` with string operations. (There, a
pygraphics linked in as a user C module is a builtin and wins over ``sys.path``
regardless, so such a run always exercises the native build.)
"""

import os
import sys

USE_NATIVE = os.getenv("PYGRAPHICS_TEST_NATIVE") == "1"


def _abs_dir(path):
    """Directory of ``path`` as an absolute forward-slash path, string ops only."""
    p = path.replace("\\", "/")
    d = p[: p.rfind("/")] if "/" in p else "."
    if d == "":
        d = "/"
    if not (d.startswith("/") or (len(d) > 1 and d[1] == ":")):
        # Relative __file__ (a relative sys.path entry would give one): pin it
        # to the cwd now so a later chdir() cannot move lib/ out from under us.
        cwd = os.getcwd().replace("\\", "/")
        d = cwd if d == "." else cwd + "/" + d
    return d


_TESTS = _abs_dir(__file__)
_LIB = _TESTS[: _TESTS.rfind("/")] + "/lib"
if not USE_NATIVE and _LIB not in sys.path:
    sys.path.insert(0, _LIB)
