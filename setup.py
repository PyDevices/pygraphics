# SPDX-License-Identifier: MIT
"""Build native pygraphics C extension."""

import os
import subprocess
import sys

from setuptools import Extension, setup

ROOT = os.path.dirname(os.path.abspath(__file__))


def _build_strings():
    """The version and the revision, computed the way micropython.mk does.

    A wheel that cannot say which pygraphics it is leaves the same hole on the
    desktop that a firmware leaves on a board (pygraphics#25), and the two must
    answer alike or comparing them proves nothing. "unknown" from an sdist with
    no git is the honest answer, not a guess.
    """
    try:
        with open(os.path.join(ROOT, "VERSION"), encoding="utf-8") as handle:
            version = handle.read().strip() or "0.0.0+unknown"
    except OSError:
        version = "0.0.0+unknown"
    try:
        revision = subprocess.run(
            ["git", "-C", ROOT, "describe", "--always", "--dirty", "--abbrev=7"],
            capture_output=True, text=True, check=True,
        ).stdout.strip() or "unknown"
    except (OSError, subprocess.CalledProcessError):
        revision = "unknown"
    return version, revision


PYGRAPHICS_VERSION, PYGRAPHICS_REVISION = _build_strings()

if sys.platform == "win32":
    extra_compile_args = ["/wd4996"]
    extra_link_args = []
else:
    extra_compile_args = [
        "-Wno-unused-function",
        "-Wno-sign-compare",
    ]
    extra_link_args = []

GFX_SOURCES = [
    os.path.join("src", "gfx_module_cpy.c"),
    os.path.join("src", "gfx_framebuffer.c"),
    os.path.join("src", "gfx_shapes.c"),
    os.path.join("src", "gfx_draw.c"),
    os.path.join("src", "gfx_font.c"),
    os.path.join("src", "gfx_bmp565.c"),
    os.path.join("src", "gfx_files.c"),
    os.path.join("src", "gfx_capabilities.c"),
]

setup(
    name="pydevices-pygraphics",
    packages=[],
    py_modules=[],
    ext_modules=[
        Extension(
            "pygraphics",
            sources=GFX_SOURCES,
            include_dirs=[os.path.join(ROOT, "src")],
            define_macros=[
                ("PYGRAPHICS_VERSION", '"%s"' % PYGRAPHICS_VERSION),
                ("PYGRAPHICS_REVISION", '"%s"' % PYGRAPHICS_REVISION),
            ],
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
        ),
    ],
)
