# How it works

pygraphics is a framebuffer: a block of memory that holds a picture, and
functions that draw into it. It starts from MicroPython's `framebuf` and adds
shapes, text, images, clipping and the changed-rectangle `Area`. It needs
nothing else from PyDevices and no screen, so it is as useful for drawing
off-screen and preparing images as for driving a display.

```text
your shapes, text and images
            |
            v
   FrameBuffer, Draw and the module functions
            |
            |-- returns an Area: the rectangle that changed
            `-- writes into .buffer: the pixels
                        |
                        v
          your display driver, a file, or nothing
```

## Two packages, one behaviour

The same `import pygraphics` comes in two forms.

The compiled package is C. It's what the `pydevices-pygraphics` wheels
contain, and it can be built into MicroPython or CircuitPython firmware.
`pygraphics.implementation()` returns `native_cmod`.

The pure-Python package is the [`lib/pygraphics/`](../../lib/pygraphics/) folder, the one mip
installs. It runs on any Python with no compiler, and returns
`pygraphics_python`. It carries `pygraphics.framebuf`, a Python copy of
MicroPython's `framebuf`, so it runs the same on CPython and CircuitPython,
which don't have that module.

Both pass the same tests, and each change is checked by drawing the same
pictures with both and comparing them byte for byte. The compiled package is
faster, by a lot: [Benchmarks](benchmarks.md) has the numbers. The four names
that only the pure package has are listed under
[Platforms](../platforms.md#names-only-the-pure-python-package-has).

## Compatible with framebuf

A `pygraphics.FrameBuffer` takes the same arguments as `framebuf.FrameBuffer`,
uses the same format numbers, and draws the same pixels for the same calls.
A tool in the repository, [`tools/compare_framebuf_mp.py`](../../tools/compare_framebuf_mp.py), checks this against
MicroPython's own `framebuf`. Two things differ on purpose: drawing methods
return an `Area` instead of `None`, and [text](../guides/draw-text.md#framebufs-text-looks-different)
uses the romfont faces.

`Draw` brings the same shapes to any object that has `framebuf`'s basic
methods, such as a display driver, without a framebuffer in between.

## Where to read the code

| Path | What's there |
|---|---|
| `lib/pygraphics/` | the pure-Python package; the API reference is generated from it |
| `src/` | the C module: framebuffer, shapes, fonts, files, and the bindings for MicroPython, CircuitPython and CPython |
| `tests/` | one suite for both packages |
| `tools/` | the comparison tools |

Building and testing your own copy is in
[CONTRIBUTING.md](https://github.com/PyDevices/pygraphics/blob/main/CONTRIBUTING.md).

## Credits

`pygraphics.framebuf` and the framebuffer drawing in both packages follow
MicroPython's `extmod/modframebuf.c` by Damien P. George, under the MIT
licence. The built-in fonts come from
[romfont](https://github.com/spacerace/romfont).
