# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Check that pygraphics.pyi lists exactly the names in the package's __all__.

The stub is what editors complete from and what the Reference section is built
from, so a name added to one and not the other is a gap a reader finds first.
CPython only: it parses both files with ``ast``.
"""

import ast
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _tree(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
        return ast.parse(handle.read())


def _all_names():
    for node in _tree("lib/pygraphics/__init__.py").body:
        if isinstance(node, ast.Assign) and node.targets[0].id == "__all__":
            return {element.value for element in node.value.elts}
    raise AssertionError("no __all__ in lib/pygraphics/__init__.py")


def _stub_names():
    names = set()
    for node in _tree("pygraphics.pyi").body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.AnnAssign):
            names.add(node.target.id)
    return {name for name in names if not name.startswith("_")}


class StubTest(unittest.TestCase):
    def test_stub_matches_all(self):
        public = _all_names()
        stub = _stub_names()
        self.assertEqual(sorted(public - stub), [], "in __all__ but not in pygraphics.pyi")
        self.assertEqual(sorted(stub - public), [], "in pygraphics.pyi but not in __all__")


if __name__ == "__main__":
    unittest.main()
