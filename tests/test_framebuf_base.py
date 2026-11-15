# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Which ``framebuf`` the pure-Python ``FrameBuffer`` builds on.

An install of the package ships ``pygraphics/framebuf.py``, the pure-Python
copy of MicroPython's ``framebuf``. On MicroPython the built-in C module must
still win, because the copy draws the same pixels hundreds of times slower.
These tests reload ``pygraphics._framebuf_plus`` under a stand-in for each
runtime and check the class it subclasses.
"""

import importlib
import sys
import types
import unittest

import _env  # noqa: F401


def _fake_framebuf():
    mod = types.ModuleType("framebuf")
    for value, name in enumerate(("MONO_VLSB", "RGB565", "GS4_HMSB", "MONO_HLSB", "MONO_HMSB", "GS2_HMSB", "GS8")):
        setattr(mod, name, value)

    class FrameBuffer:
        def __init__(self, *args, **kwargs):
            pass

    mod.FrameBuffer = FrameBuffer
    return mod


@unittest.skipIf(_env.USE_NATIVE or sys.implementation.name != "cpython", "reloads the pure-Python package")
class BaseFramebufTest(unittest.TestCase):
    def setUp(self):
        import pygraphics._framebuf_plus  # noqa: F401

        self.saved = {name: sys.modules.get(name) for name in ("framebuf", "pygraphics._framebuf_plus")}
        self.implementation = sys.implementation
        self.addCleanup(self.restore)

    def restore(self):
        sys.implementation = self.implementation
        for name, mod in self.saved.items():
            if mod is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = mod

    def reload_under(self, name, builtin):
        # A copy of the real one, renamed: the import machinery reads its other fields.
        sys.implementation = types.SimpleNamespace(**dict(vars(self.implementation), name=name))
        sys.modules["framebuf"] = builtin
        sys.modules.pop("pygraphics._framebuf_plus", None)
        return importlib.import_module("pygraphics._framebuf_plus")

    def test_micropython_builds_on_its_built_in_framebuf(self):
        builtin = _fake_framebuf()
        plus = self.reload_under("micropython", builtin)
        self.assertIs(plus._FrameBuffer, builtin.FrameBuffer)
        self.assertTrue(issubclass(plus.FrameBuffer, builtin.FrameBuffer))

    def test_other_runtimes_build_on_the_package_copy(self):
        plus = self.reload_under("circuitpython", _fake_framebuf())
        self.assertEqual(plus._FrameBuffer.__module__, "pygraphics.framebuf")


if __name__ == "__main__":
    unittest.main()
