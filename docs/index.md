# pygraphics

<div class="hero-banner">
  <h1>🖌️ pygraphics</h1>
  <p><strong>Cross-platform 2D drawing and graphics engine</strong> for the PyDevices stack — <code>Area</code> dirty bounding boxes, framebuf-compatible <code>FrameBuffer</code>, embedded romfonts, shapes, and image loaders.</p>
  <div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin-top:0.75rem;">
    <span class="badge badge-orange">📦 MIP: pygraphics</span>
    <span class="badge badge-orange">🐍 PyPI: pydevices-pygraphics</span>
    <span class="badge badge-green">⚡ Native C & Pure-Python Parity</span>
    <span class="badge">🌐 MicroPython · CircuitPython · CPython · Pyodide</span>
  </div>
</div>

<div class="grid cards">
  <div>
    <h3>📐 Area Bounding Boxes</h3>
    <p>Every shape and text primitive returns an <code>Area(x, y, w, h)</code> bounding box for partial screen refresh and dirty-rect updates.</p>
  </div>
  <div>
    <h3>🔤 Embedded Romfonts</h3>
    <p>Zero-dependency built-in 8x8, 8x14, and 8x16 romfonts with arbitrary scaling, transparency, and external <code>.bin</code> file support.</p>
  </div>
  <div>
    <h3>🖼️ Streaming BMP565</h3>
    <p>Stream and slice massive 16-bit RGB565 bitmaps without loading full images into microcontroller RAM.</p>
  </div>
  <div>
    <h3>⚡ Hardware Blit Fast-Paths</h3>
    <p>Direct SPI/SDL bulk blit dispatch with clipping context managers (<code>with draw.clip(...)</code>).</p>
  </div>
</div>

---

## 💻 Live Interactive 2D Drawing Demo

Try editing the drawing primitives below and click **▶ Run** to execute live in your browser:

<div class="pydevices-live-demo">
  <div class="demo-editor-pane">
    <textarea class="code-editor">
import pygraphics
from displaydev.psdisplay import PSDisplay

# Initialize display canvas (320x240)
display = PSDisplay(CANVAS_ID, width=320, height=240)
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

<div class="grid cards">
  <div>
    <h3>🔴 Bouncing Balls</h3>
    <p>High-framerate physics simulation with vector circles and bounding-box collision detection.</p>
    <p><a href="https://pydevices.github.io/pydevices-examples/pyscript/pyodide.html?modules=bouncing_balls&deps=pydevices-pygraphics" target="_blank" rel="noopener"><strong>▶ Launch Live Demo</strong></a></p>
  </div>
  <div>
    <h3>👾 Alien Arcade</h3>
    <p>Retro Space Invaders-style sprite engine with transparency and animated framebuffers.</p>
    <p><a href="https://pydevices.github.io/pydevices-examples/pyscript/pyodide.html?manifests=alien&deps=pydevices-pygraphics" target="_blank" rel="noopener"><strong>▶ Launch Live Demo</strong></a></p>
  </div>
  <div>
    <h3>🦖 Dino Runner</h3>
    <p>Classic obstacle jumping arcade running with dirty scanline refresh and physics.</p>
    <p><a href="https://pydevices.github.io/pydevices-examples/pyscript/pyodide.html?modules=dino&deps=pydevices-pygraphics" target="_blank" rel="noopener"><strong>▶ Launch Live Demo</strong></a></p>
  </div>
  <div>
    <h3>🕹️ Testris Arcade</h3>
    <p>Full-featured falling-blocks game with matrix rotation, score tracking, and ghost pieces.</p>
    <p><a href="https://pydevices.github.io/pydevices-examples/pyscript/pyodide.html?modules=testris&deps=pydevices-pygraphics" target="_blank" rel="noopener"><strong>▶ Launch Live Demo</strong></a></p>
  </div>
</div>

---

## 📚 Documentation Map

* 🚀 [**Getting started**](getting-started.md) — Core drawing workflows, dirty rectangles, and canvases.
* 📦 [**Installation**](installation.md) — MIP, TestPyPI, wheel building, and platform matrix.
* 🎨 [**Graphics guide**](graphics-guide.md) — FrameBuffer vs Draw, clipping stacks, fonts, and blit fast-paths.
* 🖼️ [**Graphics files**](graphics-files.md) — BMP565, PBM, PGM image loaders and streaming.
* ⚡ [**Benchmarks**](benchmarks.md) — Native C extension vs Pure-Python performance metrics.
* 📚 [**API Reference**](reference/pygraphics/index.md) — Full autogenerated API documentation.
