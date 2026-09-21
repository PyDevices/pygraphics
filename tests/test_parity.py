#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Verify the native cmod's surface against the pure package's ``__all__``.

This used to carry a frozen 44-name copy of ``__all__``, which had already
drifted from the real one in both directions -- it listed ``capabilities`` and
``framebuf_backend`` (not public API) and omitted ``RGB888`` and
``export_framebuffer``, the latter being one of the very names the native
module does not have. A guard that cannot detect the gap it exists for is not
a guard (PyDevices/pygraphics#23).

So the list is read from ``lib/pygraphics/__init__.py`` at run time. It is
parsed out of the source rather than imported, because under a native build
``import pygraphics`` gives the C module and the pure package is not importable
under that name in the same process -- and because this has to work on
MicroPython, which has no ``ast`` and no ``importlib``.

``PURE_ONLY`` below is the recorded exclusion: names that are pure-Python by
design. Both directions are enforced, so implementing one in C fails this test
until the README and docs/graphics-files.md stop calling it pure-only.
"""

import _env  # noqa: F401
import pygraphics

if pygraphics.implementation() != "native_cmod":
    from unittest import SkipTest

    raise SkipTest("native-only export parity probe")


# Recorded exclusion, and its cause. These write or read an importable ``.py``
# bitmap module -- an authoring-time convenience that emits Python source.
# Putting a source generator in the C accelerator buys nothing, so the native
# module does without and callers fall back to the pure package (pdwidgets
# does exactly that, in its _icon_load.py).
PURE_ONLY_MODULE = ("export_framebuffer",)
PURE_ONLY_FRAMEBUFFER = ("export", "from_bitmap", "from_module")


def _pure_all():
    """``__all__`` from lib/pygraphics/__init__.py, by reading the source.

    String operations only: no ast, no importlib, no os.path -- this module
    runs under MicroPython too.
    """
    here = _env._abs_dir(__file__)
    path = here[: here.rfind("/")] + "/lib/pygraphics/__init__.py"
    with open(path) as handle:
        text = handle.read()
    start = text.find("__all__")
    if start < 0:
        raise SystemExit(path + ": no __all__ to check against")
    start = text.find("[", start)
    end = text.find("]", start)
    if start < 0 or end < 0:
        raise SystemExit(path + ": __all__ is not a simple list literal")
    names = []
    for chunk in text[start + 1 : end].split(","):
        chunk = chunk.strip()
        if chunk.startswith("#") or not chunk:
            continue
        names.append(chunk.strip("\"'"))
    if not names:
        raise SystemExit(path + ": __all__ parsed empty")
    return names


ALL = _pure_all()

missing = [
    name
    for name in ALL
    if name not in PURE_ONLY_MODULE and not hasattr(pygraphics, name)
]
if missing:
    raise SystemExit(
        "native module is missing public names: "
        + ", ".join(missing)
        + " -- implement them, or add them to PURE_ONLY_MODULE and record the "
        "exclusion in README.md and docs/graphics-files.md"
    )

# The other direction: an exclusion that stops being true has to be noticed.
unexpected = [name for name in PURE_ONLY_MODULE if hasattr(pygraphics, name)]
unexpected += [
    name for name in PURE_ONLY_FRAMEBUFFER if hasattr(pygraphics.FrameBuffer, name)
]
if unexpected:
    raise SystemExit(
        "these are implemented in C now: "
        + ", ".join(unexpected)
        + " -- drop them from PURE_ONLY_* here and from the 'pure-Python only' "
        "notes in README.md and docs/graphics-files.md"
    )

# Named in __all__ but absent from the pure package would mean __all__ itself lies.
stale = [name for name in PURE_ONLY_MODULE if name not in ALL]
if stale:
    raise SystemExit(
        "PURE_ONLY_MODULE names not in __all__: " + ", ".join(stale)
    )

assert pygraphics.framebuf_backend() == "native", pygraphics.capabilities()
assert pygraphics.implementation() == "native_cmod", pygraphics.capabilities()

buf = bytearray(32 * 32 * 2)
fb = pygraphics.FrameBuffer(buf, 32, 32, pygraphics.RGB565)
assert fb.buffer is buf or bytes(fb.buffer) == bytes(buf)
fb.fill(0)
pygraphics.fill_rect(fb, 1, 1, 4, 4, 0xF800)
pygraphics.text8(fb, "Hi", 0, 0, 0xFFFF)
d = pygraphics.Draw(fb)
d.fill_rect(0, 0, 2, 2, 1)
print("test_parity: ok (%d public names, %d recorded pure-only)" % (
    len(ALL), len(PURE_ONLY_MODULE) + len(PURE_ONLY_FRAMEBUFFER)))
