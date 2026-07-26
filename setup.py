# SPDX-License-Identifier: MIT
"""Build native pygraphics C extension."""

import os
import sys

from setuptools import Extension, setup

ROOT = os.path.dirname(os.path.abspath(__file__))

if sys.platform == "win32":
    extra_compile_args = ["/wd4996"]
    extra_link_args = []
else:
    extra_compile_args = [
        "-Wno-unused-function",
        "-Wno-sign-compare",
    ]
    extra_link_args = ["-lm"]

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
    name="pygraphics-cmod",
    packages=[],
    py_modules=[],
    ext_modules=[
        Extension(
            "pygraphics",
            sources=GFX_SOURCES,
            include_dirs=[os.path.join(ROOT, "src")],
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
        ),
    ],
)
