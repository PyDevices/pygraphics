`pygraphics` extends `framebuf` with extra drawing helpers (rounded rectangles, gradients, polygons) and returns **Area** bounding boxes for partial updates.

See the [installation guide](installation.md) for MIP and TestPyPI options.

## Narrative docs

- [Graphics guide](graphics-guide.md) — quick start, FrameBuffer vs Draw, Area bounds, font rendering patterns, loaders
- [Graphics files](graphics-files.md) — image loaders, the save/load matrix, and BMP565

## Key entry points

- `pygraphics.FrameBuffer` — subclass of the bundled `pygraphics.framebuf.FrameBuffer` with shape helpers and Area returns (same implementation on every interpreter)
- `pygraphics.Draw` — draws on any framebuf-compatible canvas
- `pygraphics.Area` — dirty rectangle with union/clip helpers
- Module functions — `circle`, `rect`, `text8`, … (same primitives as FrameBuffer)
- `pygraphics.Font` — romfont renderer; built-in embedded fonts or optional `.bin` path ([Fonts](graphics-guide.md#fonts))
- `load_image`, `save_image` — auto-detect load / format-aware save
- `bmp_to_framebuffer`, `pbm_to_framebuffer`, `pgm_to_framebuffer` — image loaders
- `BMP565` — sliceable/streaming RGB565 BMP asset

Generated API pages for each module appear below (build time).
