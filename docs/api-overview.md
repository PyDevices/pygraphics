`pygraphics` extends `framebuf` with extra drawing helpers (rounded rectangles, gradients, polygons) and returns **Area** bounding boxes for partial updates.

!!! note "Package ownership"
    `pygraphics` is maintained in this repository and used by the
    `pydevices-examples` applications. See the local [installation guide](installation.md)
    for MIP and TestPyPI options.

## Narrative docs

- [Graphics concept](https://pydisplay.readthedocs.io/en/latest/concepts/graphics/) — quick start, font rendering patterns, loaders
- [Drawing and fonts](https://pydisplay.readthedocs.io/en/latest/concepts/drawing-and-fonts/) — application drawing stack
- [Graphics files](https://pydisplay.readthedocs.io/en/latest/concepts/graphics-files/) — loaders and BMP565

## Key entry points

- `pygraphics.FrameBuffer` — subclass of the bundled `pygraphics.framebuf.FrameBuffer` with shape helpers and Area returns (same implementation on every runtime)
- `pygraphics.Draw` — draws on any framebuf-compatible canvas
- `pygraphics.Area` — dirty rectangle with union/clip helpers
- Module functions — `circle`, `rect`, `text8`, … (same primitives as FrameBuffer)
- `pygraphics.Font` — romfont renderer; built-in embedded fonts or optional `.bin` path ([Fonts](https://pydisplay.readthedocs.io/en/latest/concepts/graphics/#fonts))
- `load_image`, `save_image` — auto-detect load / format-aware save
- `bmp_to_framebuffer`, `pbm_to_framebuffer`, `pgm_to_framebuffer` — image loaders
- `BMP565` — sliceable/streaming RGB565 BMP asset

Generated API pages for each module appear below (build time).
