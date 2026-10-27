# Your first picture

This program draws a card, a dot and a word into memory, tells you which part
of the picture changed, and saves it as a BMP file. It needs no screen, so it
runs the same on a desktop and on a board.

```python
import pygraphics
from pygraphics import FrameBuffer, RGB565

fb = FrameBuffer(bytearray(160 * 80 * 2), 160, 80, RGB565)
fb.fill(0x0000)
card = fb.round_rect(8, 8, 64, 40, 8, 0xF800, f=True)
dot = fb.circle(116, 28, 20, 0x07E0, f=True)
label = pygraphics.text16(fb, "Hello", 8, 56, 0xFFFF)
print("changed:", card + dot + label)
fb.save("hello.bmp")
```

It prints:

```text
changed: Area(8, 8, 128, 64)
```

and `hello.bmp` looks like this, shown here at three times its size:

![A red rounded rectangle, a green circle and the word Hello on black](../images/hello.png)

## What each line does

`FrameBuffer(bytearray(160 * 80 * 2), 160, 80, RGB565)` makes a picture 160
pixels wide and 80 high. `RGB565` stores each pixel in two bytes, which is
why the buffer is `160 * 80 * 2` bytes long. It's the format most small
colour screens take directly.

Colours are 16-bit RGB565 numbers: `0xF800` is red, `0x07E0` green, `0x001F`
blue, `0xFFFF` white and `0x0000` black.

`round_rect(x, y, w, h, r, c, f=True)` draws a rectangle with corners of
radius `r`, filled because of `f=True`. `circle(x, y, r, c, f=True)` draws a
filled circle centred on `x, y`. `text16` writes text in the built-in font
that is 8 pixels wide and 16 high.

Each of these calls returns an `Area`, the rectangle of pixels it changed.
Adding two areas gives the smallest rectangle that covers both, so
`card + dot + label` is everything this program drew. On a real screen you'd
send just that rectangle; [Update part of a screen](../guides/update-part-of-a-screen.md)
shows how.

`fb.save("hello.bmp")` writes the picture out. The file type comes from the
pixel format; [Load and save images](../guides/load-and-save-images.md) has
the others.

## Try it in your browser

This version draws onto the canvas beside the editor. Change a number and
press **Run**.

````{raw} html
<div class="pydevices-live-demo">
  <div class="demo-editor-pane">
    <textarea class="code-editor">
import pygraphics
from displaydev.auto import AutoDisplay

display = AutoDisplay(width=240, height=200, canvas_id=CANVAS_ID)
fb = pygraphics.FrameBuffer(bytearray(240 * 200 * 2), 240, 200, pygraphics.RGB565)
fb.fill(0x0000)

card = fb.round_rect(15, 15, 90, 50, 8, 0xF800, f=True)
dot = fb.circle(170, 45, 25, 0x07E0, f=True)
box = fb.rect(15, 80, 210, 40, 0x001F)
pygraphics.text14(fb, "Area Updates!", 25, 92, 0xFFFF)

display.blit_rect(fb.buffer, 0, 0, 240, 200)
display.show()
print("changed:", card + dot + box)
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
````

Next: [draw shapes](../guides/draw-shapes.md).
