# pygraphics

pygraphics is the part of OmniPython that draws: shapes, text and images into
a framebuffer, with the same code on MicroPython-compatible boards,
CircuitPython-compatible boards and CPython. Every drawing call returns the
rectangle it changed, so you can send just that part to a screen.

Edit the code below and press **Run**. It runs in your browser, on
MicroPython compiled to WebAssembly.

````{raw} html
<div class="pydevices-live-demo">
  <div class="demo-editor-pane">
    <textarea class="code-editor">
import pygraphics
from displaydev.auto import AutoDisplay

display = AutoDisplay(width=320, height=240, canvas_id=CANVAS_ID)
buf = bytearray(320 * 240 * 2)
fb = pygraphics.FrameBuffer(buf, 320, 240, pygraphics.RGB565)
fb.fill(0x1082)

fb.round_rect(20, 20, 120, 70, 10, 0xF800, f=True)
fb.circle(220, 55, 35, 0x07E0, f=True)
fb.line(20, 110, 300, 110, 0xFFFF)

pygraphics.text8(fb, "Romfont 8x8", 20, 130, 0xFFE0)
pygraphics.text14(fb, "Romfont 8x14", 20, 150, 0x07FF)
pygraphics.text16(fb, "Romfont 8x16", 20, 175, 0xFFFF)

display.blit_rect(buf, 0, 0, 320, 240)
display.show()
print("Drawn with", pygraphics.implementation())
    </textarea>
    <div class="demo-controls">
      <button class="run-btn" disabled>▶ Run</button>
      <button class="reset-btn">↺ Reset</button>
      <span class="demo-status">Initializing Python…</span>
    </div>
    <pre class="demo-output"></pre>
  </div>
  <div class="demo-canvas-pane">
    <canvas id="canvas_pygraphics_index" width="320" height="240" tabindex="0"></canvas>
  </div>
</div>
````

[Install it](get-started/install.md), then draw
[your first picture](get-started/first-program.md). The
[guides](guides/draw-shapes.md) take one task each, the
[reference](reference/index) lists every name, and
[How it works](how-it-works/index.md) explains the design.

```{toctree}
:hidden:
:caption: Get started

get-started/install
get-started/first-program
```

```{toctree}
:hidden:
:caption: Guides

guides/draw-shapes
guides/update-part-of-a-screen
guides/draw-text
guides/load-and-save-images
```

```{toctree}
:hidden:
:caption: Reference

reference/index
platforms
formats
```

```{toctree}
:hidden:
:caption: How it works

how-it-works/index
how-it-works/benchmarks
```

```{toctree}
:hidden:
:caption: Changelog

changelog
```
