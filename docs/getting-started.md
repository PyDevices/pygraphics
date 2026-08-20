# Getting started

## Setup

=== "MicroPython (MIP)"

    ```python
    import mip
    mip.install("pygraphics", index="https://PyDevices.github.io/mip")
    ```

=== "CPython (TestPyPI)"

    ```bash
    pip install -i https://test.pypi.org/simple/ \
      --extra-index-url https://pypi.org/simple/ pydevices-pygraphics
    ```

=== "CircuitPython"

    Copy `lib/pygraphics/` to your board's `CIRCUITPY/lib/` directory.

=== "PyScript / Pyodide"

    ```python
    # pyscript mip: pygraphics
    # pyodide wheels: pygraphics
    ```

---

## 💻 Live Interactive Drawing Canvas

Experiment with 2D shapes, colors, and font rendering live in your browser:

<div class="pydevices-live-demo">
  <div class="demo-editor-pane">
    <textarea class="code-editor">
import pygraphics
from displaydev.psdisplay import PSDisplay

# Initialize display canvas (240x200)
display = PSDisplay(CANVAS_ID, width=240, height=200)
fb = pygraphics.FrameBuffer(bytearray(240 * 200 * 2), 240, 200, pygraphics.RGB565)
fb.fill(0x0000)

# Draw filled & outlined shapes
area1 = fb.round_rect(15, 15, 90, 50, 8, 0xF800, f=True)
area2 = fb.circle(170, 45, 25, 0x07E0, f=True)
area3 = fb.rect(15, 80, 210, 40, 0x001F)

# Draw text
pygraphics.text14(fb, "Area Updates!", 25, 92, 0xFFFF)

display.blit_rect(fb.buffer, 0, 0, 240, 200)
display.show()
print(f"Shapes drawn! Dirty bounds: {area1 + area2}")
    </textarea>
    <div class="demo-controls">
      <button class="run-btn" disabled>▶ Run</button>
      <button class="reset-btn">↺ Reset</button>
      <span class="demo-status">Initializing Python…</span>
    </div>
    <pre class="demo-output"></pre>
  </div>
  <div class="demo-canvas-pane">
    <canvas id="canvas_pygraphics_getting_started" width="240" height="200" tabindex="0"></canvas>
  </div>
</div>

---

## Basic Usage

```python
import pygraphics
from pygraphics import FrameBuffer, RGB565, Area

fb = FrameBuffer(bytearray(160 * 128 * 2), 160, 128, RGB565)
fb.fill(0)
area = fb.fill_rect(10, 10, 40, 40, 0xF800)
assert isinstance(area, Area)
print(pygraphics.implementation())  # native_cmod or pygraphics_python
```

---

## Common Patterns

### 1. Draw to an off-screen buffer first
Use a `FrameBuffer` as a canvas, then copy the result to the display:

```python
import pygraphics
from pygraphics import FrameBuffer, RGB565, text8

buf = FrameBuffer(bytearray(160 * 128 * 2), 160, 128, RGB565)
buf.fill(0x0000)
pygraphics.fill_rect(buf, 10, 10, 40, 20, 0xF800)
text8(buf, "Hello", 12, 14, 0xFFFF)
```

### 2. Use the returned `Area` as a dirty rectangle
Many draw helpers return an `Area` describing the pixels they changed. That is useful when refreshing only the part of the screen that changed:

```python
area = pygraphics.circle(buf, 80, 40, 12, 0x07E0, f=True)
# area.x, area.y, area.w, area.h describe the changed region
display_drv.blit_rect(buf.buffer, area.x, area.y, area.w, area.h)
```
