---
title: Fonts and images
description: Bitmap font rendering, RGB565 bitmap access, and image conversion helpers.
---

Source snapshot: [`a02baf40d594bb77afae9676b5c803232bc188cd`](https://github.com/PyDevices/pygraphics/tree/a02baf40d594bb77afae9676b5c803232bc188cd).

Bitmap font rendering, RGB565 bitmap access, and image conversion helpers.

Every entry below is generated from a public binding table or header declaration and links to its immutable source line.

## `pygraphics.Font`

```python
class Font(font_data=None, height=0, cached=True)
```

Bitmap font loader and renderer for built-in, file, or buffer-backed glyph data.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2643)

## `pygraphics.Font.text`

```python
Font.text(canvas, text, x, y, color, scale=1, inverted=False)
```

Render bitmap text with selectable height, scale, and inversion.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2633)

## `pygraphics.Font.draw_char`

```python
Font.draw_char(char, x, y, canvas, color, scale=1, inverted=False)
```

Render one glyph through this Font onto a canvas.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2634)

## `pygraphics.Font.text_width`

```python
Font.text_width(text, scale=1)
```

Measure rendered text width at the selected scale.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2635)

## `pygraphics.Font.deinit`

```python
Font.deinit()
```

Release resources owned by the object.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2636)

## `pygraphics.Font.export`

```python
Font.export(filename)
```

Write cached font bytes to a file.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2637)

## `pygraphics.Font.width`

```python
Font.width
```

Width in pixels.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2626)

## `pygraphics.Font.height`

```python
Font.height
```

Height in pixels.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2627)

## `pygraphics.Font.font_name`

```python
Font.font_name
```

Font source name or the in-memory/default identifier.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2628)

## `pygraphics.BMP565`

```python
class BMP565(filename=None, source=None, streamed=False, mirrored=False, width=None, height=None)
```

RGB565 bitmap reader supporting buffered and streamed access.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2934)

## `pygraphics.BMP565.save`

```python
BMP565.save(filename=None)
```

Write the current image or bitmap to a versioned output path.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2923)

## `pygraphics.BMP565.deinit`

```python
BMP565.deinit()
```

Release resources owned by the object.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2924)

## `pygraphics.BMP565.width`

```python
BMP565.width
```

Width in pixels.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2914)

## `pygraphics.BMP565.height`

```python
BMP565.height
```

Height in pixels.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2915)

## `pygraphics.BMP565.buffer`

```python
BMP565.buffer
```

Backing pixel buffer when the object owns or exposes one.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2916)

## `pygraphics.BMP565.bpp`

```python
BMP565.bpp
```

Bitmap color depth in bits per pixel.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2917)

## `pygraphics.BMP565.BPP`

```python
BMP565.BPP
```

Bitmap storage width in bytes per pixel.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2918)

## `pygraphics.load_image`

```python
pygraphics.load_image(path)
```

Load a supported image file as a FrameBuffer.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2971)

## `pygraphics.save_image`

```python
pygraphics.save_image(framebuffer, path='screenshot')
```

Save a FrameBuffer to a versioned image path.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2972)

## `pygraphics.bmp_to_framebuffer`

```python
pygraphics.bmp_to_framebuffer(path)
```

Decode a BMP file into a FrameBuffer.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2973)

## `pygraphics.pbm_to_framebuffer`

```python
pygraphics.pbm_to_framebuffer(path)
```

Decode a PBM file into a FrameBuffer.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2974)

## `pygraphics.pgm_to_framebuffer`

```python
pygraphics.pgm_to_framebuffer(path)
```

Decode a PGM file into a FrameBuffer.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2975)
