# Benchmarks

The compiled package is more than a hundred times faster than the pure-Python
one, on CPython and on MicroPython.

Milliseconds per call, drawing into a 160 × 128 `RGB565` framebuffer:

| Call | CPython, compiled | CPython, pure | MicroPython, compiled | MicroPython, pure |
|---|---|---|---|---|
| `fill_rect`, the whole buffer | 0.0008 | 3.15 | 0.0059 | 1.79 |
| filled `circle`, radius 40 | 0.0075 | 1.67 | 0.0063 | 1.21 |
| filled `round_rect`, 120 × 80, radius 10 | 0.0029 | 1.77 | 0.0047 | 1.08 |
| `text16`, 20 characters | 0.0037 | 0.68 | 0.0042 | 1.41 |
| `blit`, a 64 × 64 sprite | 0.024 | 3.57 | 0.021 | 4.40 |

Measured on one laptop (Intel Core Ultra 7 155H, Linux): CPython 3.12.3 with
pydevices-pygraphics 0.1.1, and MicroPython 1.30 preview unix builds, one
with the compiled module built in and one without. Neither pure run had numpy
or ulab to call on. A board is far slower than a laptop; the ratio between
the columns is what carries over.

The pure package fills `RGB565` rectangles with numpy when it can import it
(ulab's numpy on MicroPython), which makes its `fill_rect` many times faster.

## Run it yourself

[`tools/benchmark.py`](../../tools/benchmark.py) is the script behind the table. It prints which package
it imported, then one line per call.

```bash
python tools/benchmark.py
```

Run it from a directory other than the repository root to get the installed
package. To time the pure package on CPython, put `lib/` first on the path
from inside Python, because the repository root comes before `PYTHONPATH`:

```bash
cd /tmp && python -c "import sys; sys.path.insert(0, '/path/to/pygraphics/lib'); exec(open('/path/to/pygraphics/tools/benchmark.py').read())"
```

On MicroPython, a compiled module built into the firmware wins over any
folder on the path, so time the pure package on a build without it:

```bash
MICROPYPATH=lib micropython tools/benchmark.py
```
