# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT

"""package.json lists the Python package's files and names the module it stands in for."""

import json
import os
import unittest

import _env  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class PackageJson(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(ROOT, "package.json"), encoding="utf-8") as handle:
            self.body = json.load(handle)

    def test_it_lists_every_python_file_of_the_package(self):
        folder = os.path.join(ROOT, "lib", "pygraphics")
        files = sorted(name for name in os.listdir(folder) if name.endswith(".py"))
        listed = sorted(self.body["urls"])
        self.assertEqual(listed, [["pygraphics/" + name, "lib/pygraphics/" + name] for name in files])

    def test_it_names_the_c_module_it_stands_in_for(self):
        self.assertEqual(self.body["stands_in_for"], "pygraphics")


if __name__ == "__main__":
    unittest.main()
