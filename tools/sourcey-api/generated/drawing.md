---
title: Drawing operations
description: Object-oriented and module-level shape, text, polygon, and blit operations.
---

Source snapshot: [`a02baf40d594bb77afae9676b5c803232bc188cd`](https://github.com/PyDevices/pygraphics/tree/a02baf40d594bb77afae9676b5c803232bc188cd).

Object-oriented and module-level shape, text, polygon, and blit operations.

Every entry below is generated from a public binding table or header declaration and links to its immutable source line.

## `pygraphics.Draw`

```python
class Draw(canvas)
```

Drawing facade that adds a bounded clip stack to any compatible canvas.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2085)

## `pygraphics.Draw.fill`

```python
Draw.fill(color)
```

Fill the target canvas with one color and return the affected Area.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2057)

## `pygraphics.Draw.fill_rect`

```python
Draw.fill_rect(x, y, width, height, color)
```

Fill a rectangular region and return the clipped affected Area.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2058)

## `pygraphics.Draw.pixel`

```python
Draw.pixel(x, y, color=None)
```

Read or write one pixel, depending on whether a color is supplied.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2059)

## `pygraphics.Draw.hline`

```python
Draw.hline(x, y, width, color)
```

Draw a horizontal line.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2060)

## `pygraphics.Draw.vline`

```python
Draw.vline(x, y, height, color)
```

Draw a vertical line.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2061)

## `pygraphics.Draw.line`

```python
Draw.line(x1, y1, x2, y2, color)
```

Draw a line between two points.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2062)

## `pygraphics.Draw.rect`

```python
Draw.rect(x, y, width, height, color, fill=False)
```

Draw an outlined or filled rectangle.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2063)

## `pygraphics.Draw.round_rect`

```python
Draw.round_rect(x, y, width, height, radius, color, fill=False)
```

Draw an outlined or filled rounded rectangle.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2064)

## `pygraphics.Draw.circle`

```python
Draw.circle(x, y, radius, color, fill=False)
```

Draw an outlined or filled circle.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2065)

## `pygraphics.Draw.ellipse`

```python
Draw.ellipse(x, y, x_radius, y_radius, color, fill=False, mask=0x0F)
```

Draw selected quadrants of an outlined or filled ellipse.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2066)

## `pygraphics.Draw.arc`

```python
Draw.arc(x, y, radius, start_angle, end_angle, color)
```

Draw a circular arc between two angles.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2067)

## `pygraphics.Draw.triangle`

```python
Draw.triangle(x0, y0, x1, y1, x2, y2, color, fill=False)
```

Draw an outlined or filled triangle.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2068)

## `pygraphics.Draw.gradient_rect`

```python
Draw.gradient_rect(x, y, width, height, color1, color2=None, vertical=True)
```

Fill a rectangle with a horizontal or vertical color gradient.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2069)

## `pygraphics.Draw.poly`

```python
Draw.poly(x, y, coordinates, color, fill=False)
```

Draw a polygon from a packed coordinate buffer.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2070)

## `pygraphics.Draw.polygon`

```python
Draw.polygon(points, x, y, color, angle=0, center_x=0, center_y=0)
```

Draw a translated and optionally rotated sequence of points.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2071)

## `pygraphics.Draw.blit`

```python
Draw.blit(source, x, y, key=-1, palette=None)
```

Copy another framebuffer onto the target with optional keying and palette lookup.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2072)

## `pygraphics.Draw.blit_rect`

```python
Draw.blit_rect(buffer, x, y, width, height)
```

Copy a packed RGB565 rectangle onto the target.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2073)

## `pygraphics.Draw.blit_transparent`

```python
Draw.blit_transparent(buffer, x, y, width, height, key)
```

Copy a packed RGB565 rectangle while skipping the transparent key.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2074)

## `pygraphics.Draw.text`

```python
Draw.text(text, x, y, color=1, scale=1, inverted=False, font_data=None, height=8)
```

Render bitmap text with selectable height, scale, and inversion.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2075)

## `pygraphics.Draw.text8`

```python
Draw.text8(text, x, y, color=1, scale=1, inverted=False, font_data=None)
```

Render text with the built-in 8-pixel-high font path.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2076)

## `pygraphics.Draw.text14`

```python
Draw.text14(text, x, y, color=1, scale=1, inverted=False, font_data=None)
```

Render text with the built-in 14-pixel-high font path.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2077)

## `pygraphics.Draw.text16`

```python
Draw.text16(text, x, y, color=1, scale=1, inverted=False, font_data=None)
```

Render text with the built-in 16-pixel-high font path.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2078)

## `pygraphics.Draw.clip`

```python
Draw.clip(area_or_x, y=None, width=None, height=None)
```

Return the intersection with another Area.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2079)

## `pygraphics.fill`

```python
pygraphics.fill(canvas, color)
```

Fill the target canvas with one color and return the affected Area.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2953)

## `pygraphics.fill_rect`

```python
pygraphics.fill_rect(canvas, x, y, width, height, color)
```

Fill a rectangular region and return the clipped affected Area.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2954)

## `pygraphics.pixel`

```python
pygraphics.pixel(canvas, x, y, color=None)
```

Read or write one pixel, depending on whether a color is supplied.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2955)

## `pygraphics.hline`

```python
pygraphics.hline(canvas, x, y, width, color)
```

Draw a horizontal line.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2956)

## `pygraphics.vline`

```python
pygraphics.vline(canvas, x, y, height, color)
```

Draw a vertical line.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2957)

## `pygraphics.line`

```python
pygraphics.line(canvas, x1, y1, x2, y2, color)
```

Draw a line between two points.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2958)

## `pygraphics.rect`

```python
pygraphics.rect(canvas, x, y, width, height, color, fill=False)
```

Draw an outlined or filled rectangle.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2959)

## `pygraphics.round_rect`

```python
pygraphics.round_rect(canvas, x, y, width, height, radius, color, fill=False)
```

Draw an outlined or filled rounded rectangle.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2960)

## `pygraphics.circle`

```python
pygraphics.circle(canvas, x, y, radius, color, fill=False)
```

Draw an outlined or filled circle.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2961)

## `pygraphics.ellipse`

```python
pygraphics.ellipse(canvas, x, y, x_radius, y_radius, color, fill=False, mask=0x0F)
```

Draw selected quadrants of an outlined or filled ellipse.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2962)

## `pygraphics.arc`

```python
pygraphics.arc(canvas, x, y, radius, start_angle, end_angle, color)
```

Draw a circular arc between two angles.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2963)

## `pygraphics.triangle`

```python
pygraphics.triangle(canvas, x0, y0, x1, y1, x2, y2, color, fill=False)
```

Draw an outlined or filled triangle.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2964)

## `pygraphics.gradient_rect`

```python
pygraphics.gradient_rect(canvas, x, y, width, height, color1, color2=None, vertical=True)
```

Fill a rectangle with a horizontal or vertical color gradient.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2965)

## `pygraphics.poly`

```python
pygraphics.poly(canvas, x, y, coordinates, color, fill=False)
```

Draw a polygon from a packed coordinate buffer.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2966)

## `pygraphics.blit`

```python
pygraphics.blit(canvas, source, x, y, key=-1, palette=None)
```

Copy another framebuffer onto the target with optional keying and palette lookup.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2967)

## `pygraphics.blit_rect`

```python
pygraphics.blit_rect(canvas, buffer, x, y, width, height)
```

Copy a packed RGB565 rectangle onto the target.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2968)

## `pygraphics.blit_transparent`

```python
pygraphics.blit_transparent(canvas, buffer, x, y, width, height, key)
```

Copy a packed RGB565 rectangle while skipping the transparent key.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2969)

## `pygraphics.polygon`

```python
pygraphics.polygon(canvas, points, x, y, color, angle=0, center_x=0, center_y=0)
```

Draw a translated and optionally rotated sequence of points.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2970)

## `pygraphics.text`

```python
pygraphics.text(canvas, text, x, y, color=1, scale=1, inverted=False, font_data=None, height=8)
```

Render bitmap text with selectable height, scale, and inversion.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2976)

## `pygraphics.text8`

```python
pygraphics.text8(canvas, text, x, y, color=1, scale=1, inverted=False, font_data=None)
```

Render text with the built-in 8-pixel-high font path.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2977)

## `pygraphics.text14`

```python
pygraphics.text14(canvas, text, x, y, color=1, scale=1, inverted=False, font_data=None)
```

Render text with the built-in 14-pixel-high font path.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2978)

## `pygraphics.text16`

```python
pygraphics.text16(canvas, text, x, y, color=1, scale=1, inverted=False, font_data=None)
```

Render text with the built-in 16-pixel-high font path.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2979)
