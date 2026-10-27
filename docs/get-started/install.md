# Install

pygraphics comes two ways under one import name: a compiled package for
CPython, and a pure-Python package for boards. Your code doesn't change
between them.

## On a desktop (CPython)

```bash
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pydevices-pygraphics
```

The package is called `pydevices-pygraphics` and you import `pygraphics`.
Releases are on TestPyPI for now, which is why the command names it. There
are compiled wheels for Linux x86_64, Windows, Android and Pyodide;
[Platforms](../platforms.md) has the list and what to do on a Mac.

## On a MicroPython-compatible board

From the board's REPL, with the board online:

```python
import mip
mip.install("pygraphics", index="https://PyDevices.github.io/mip")
```

## On a CircuitPython-compatible board

Copy the [`lib/pygraphics/`](../../lib/pygraphics/) folder from this repository to the board's
`CIRCUITPY/lib/` folder.

## In the browser (Pyodide)

```python
import micropip
await micropip.install("pydevices-pygraphics", index_urls="https://test.pypi.org/simple/")
```

micropip picks the wheel that matches your Pyodide version.

## Check it worked

```python
import pygraphics
print(pygraphics.implementation())
```

You'll see `native_cmod` from the compiled package, or `pygraphics_python`
from the pure-Python one. Both draw the same pixels.

Next: [draw your first picture](first-program.md).
