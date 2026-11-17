# Install

pygraphics comes two ways under one import name: a compiled package for
CPython, and a pure-Python package for boards. Your code doesn't change
between them.

## On a desktop (CPython)

```bash
pip install omnipython-pygraphics
```

The package is called `omnipython-pygraphics` and you import `pygraphics`.
There are compiled wheels for Linux on x86_64 and ARM64, Windows, Android and Pyodide;
[Platforms](../reference/platforms.md) has the list and what to do on a Mac.

## On a MicroPython-compatible board

From the board's REPL, with the board online:

```python
import omip
omip.install("pygraphics")
```

`omip` comes with OmniPython firmware. On other MicroPython firmware, run
`mip.install("github:PyDevices/omnipython/lib/omip.py")` once to put it on the board.

## On a CircuitPython-compatible board

Copy the [`lib/pygraphics/`](https://github.com/PyDevices/pygraphics/tree/main/lib/pygraphics) folder from this repository to the board's
`CIRCUITPY/lib/` folder.

## In the browser (Pyodide)

```python
import micropip
await micropip.install("omnipython-pygraphics")
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
