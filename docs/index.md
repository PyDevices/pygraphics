# pygraphics

```{raw} html
<div class="hero-banner">
  <p><strong>Cross-platform 2D drawing and graphics engine</strong> for the PyDevices stack — <code>Area</code> dirty bounding boxes, framebuf-compatible <code>FrameBuffer</code>, embedded romfonts, shapes, and image loaders.</p>
  <div class="badge-row">
    <span class="badge badge-brand">MIP: pygraphics</span>
    <span class="badge badge-brand">TestPyPI: pydevices-pygraphics</span>
    <span class="badge badge-green">Native C & Pure-Python Parity</span>
    <span class="badge">MicroPython · CircuitPython · CPython · Direct WebAssembly · Pyodide</span>
  </div>
</div>
```

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Area Bounding Boxes

Every shape and text primitive returns an `Area(x, y, w, h)` bounding box for partial screen refresh and dirty-rect updates.
:::

:::{grid-item-card} Embedded Romfonts

Zero-dependency built-in 8x8, 8x14, and 8x16 romfonts with arbitrary scaling, transparency, and external `.bin` file support.
:::

:::{grid-item-card} Streaming BMP565

Stream and slice massive 16-bit RGB565 bitmaps without loading full images into microcontroller RAM.
:::

:::{grid-item-card} Hardware Blit Fast-Paths

Direct SPI/SDL bulk blit dispatch with clipping context managers (`with draw.clip(...)`).
:::

::::

---

## 💻 Live Interactive 2D Drawing Demo

Try editing the drawing primitives below and click **▶ Run** to execute them with direct MicroPython WebAssembly:

````{raw} html
<div class="pydevices-live-demo">
  <div class="demo-editor-pane">
    <textarea class="code-editor">
import pygraphics
from displaydev.auto import AutoDisplay

# Initialize display canvas (320x240)
display = AutoDisplay(width=320, height=240, canvas_id=CANVAS_ID)
buf = bytearray(320 * 240 * 2)
fb = pygraphics.FrameBuffer(buf, 320, 240, pygraphics.RGB565)
fb.fill(0x1082)

# Draw shapes with Area returns
fb.round_rect(20, 20, 120, 70, 10, 0xF800, f=True)
fb.circle(220, 55, 35, 0x07E0, f=True)
fb.line(20, 110, 300, 110, 0xFFFF)

# Render embedded romfonts
pygraphics.text8(fb, "Romfont 8x8", 20, 130, 0xFFE0)
pygraphics.text14(fb, "Romfont 8x14", 20, 150, 0x07FF)
pygraphics.text16(fb, "Romfont 8x16", 20, 175, 0xFFFF)

# Blit to display and present
display.blit_rect(buf, 0, 0, 320, 240)
display.show()
print(f"Drawn shapes in {pygraphics.implementation()} backend!")
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

---

## 🚀 Quick Install

| Distribution | Channel | Role |
|:---|:---|:---|
| **`pydevices-pygraphics`** | TestPyPI | Native C-extension wheel for desktop, Android, and CPython (`native_cmod`) |
| **`pygraphics`** | MIP | Pure-Python package for microcontrollers and builds without a C compiler (`pygraphics_python`) |

```bash
# CPython / Desktop
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pydevices-pygraphics
```

```python
# MicroPython
import mip
mip.install("pygraphics", index="https://PyDevices.github.io/mip")
```

---

## 🎮 Featured Browser Demos

Explore complete applications and arcade games built with `pygraphics`:

::::{grid} 1 1 2 2
:gutter: 2

:::{grid-item-card} Bouncing Balls
:link: https://pydevices.github.io/pydevices-examples/pyscript/pyodide.html?modules=bouncing_balls&deps=pydevices-pygraphics
:link-type: url

High-framerate physics simulation with vector circles and bounding-box collision detection.

**Launch Live Demo**
:::

:::{grid-item-card} Alien Arcade
:link: https://pydevices.github.io/pydevices-examples/pyscript/pyodide.html?manifests=alien&deps=pydevices-palettes,pydevices-pygraphics
:link-type: url

Retro Space Invaders-style sprite engine with transparency and animated framebuffers.

**Launch Live Demo**
:::

:::{grid-item-card} Dino Runner
:link: https://pydevices.github.io/pydevices-examples/pyscript/pyodide.html?modules=dino&deps=pydevices-pygraphics
:link-type: url

Classic obstacle jumping arcade running with dirty scanline refresh and physics.

**Launch Live Demo**
:::

:::{grid-item-card} Testris Arcade
:link: https://pydevices.github.io/pydevices-examples/pyscript/pyodide.html?modules=testris&deps=pydevices-pygraphics
:link-type: url

Full-featured falling-blocks game with matrix rotation, score tracking, and ghost pieces.

**Launch Live Demo**
:::

::::

---

## 📚 Documentation Map

* 🚀 [**Getting started**](getting-started.md) — Core drawing workflows, dirty rectangles, and canvases.
* 📦 [**Installation**](installation.md) — MIP, TestPyPI, wheel building, and platform matrix.
* 🎨 [**Graphics guide**](graphics-guide.md) — FrameBuffer vs Draw, clipping stacks, fonts, and blit fast-paths.
* 🖼️ [**Graphics files**](graphics-files.md) — BMP565, PBM, PGM image loaders and streaming.
* ⚡ [**Benchmarks**](benchmarks.md) — Native C extension vs Pure-Python performance metrics.
* 📚 [**API Reference**](reference/index.rst) — Full autogenerated API documentation.

```{toctree}
:hidden:

newcomers
getting-started
installation
graphics-guide
graphics-files
api-overview
benchmarks
building-wheels
reference/index
```
