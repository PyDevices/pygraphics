"""Sphinx configuration for the pygraphics documentation.

Everything shared by the PyDevices documentation projects (theme, top bar,
Markdown and docstring setup, the reference map) comes from pydevices-docs.
"""

from pydevices_docs import configure

globals().update(configure(
    "pygraphics", __file__,
    repo="PyDevices/pygraphics", edit_path="docs",
    source_dirs=["../lib"], api_packages=["pygraphics"],
    # The public names live in private modules and are re-exported by
    # pygraphics/__init__.py's __all__, which is what the reference documents.
    use_module_all=True,
    version_file="../VERSION",
))
