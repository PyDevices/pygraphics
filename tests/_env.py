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
"""

import os
import sys

USE_NATIVE = os.environ.get("PYGRAPHICS_TEST_NATIVE") == "1"

_LIB = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lib"))
if not USE_NATIVE and _LIB not in sys.path:
    sys.path.insert(0, _LIB)
