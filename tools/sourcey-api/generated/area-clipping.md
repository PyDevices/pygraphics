---
title: Area and clipping
description: Rectangle geometry, scoped clip contexts, and clipped canvas operations.
---

Source snapshot: [`a02baf40d594bb77afae9676b5c803232bc188cd`](https://github.com/PyDevices/pygraphics/tree/a02baf40d594bb77afae9676b5c803232bc188cd).

Rectangle geometry, scoped clip contexts, and clipped canvas operations.

Every entry below is generated from a public binding table or header declaration and links to its immutable source line.

## `pygraphics.Area`

```python
class Area(x=0, y=0, w=0, h=0)
```

Immutable rectangle geometry used for bounds, clipping, and draw results.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L395)

## `pygraphics.Area.contains`

```python
Area.contains(point_or_x, y=None)
```

Test whether the area contains a point.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L377)

## `pygraphics.Area.contains_area`

```python
Area.contains_area(other)
```

Test whether another Area is fully contained.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L378)

## `pygraphics.Area.intersects`

```python
Area.intersects(other)
```

Test whether two areas overlap.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L379)

## `pygraphics.Area.touches_or_intersects`

```python
Area.touches_or_intersects(other)
```

Test whether two areas overlap or share an edge.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L380)

## `pygraphics.Area.shift`

```python
Area.shift(dx=0, dy=0)
```

Return a copy translated by the requested offset.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L381)

## `pygraphics.Area.clip`

```python
Area.clip(other)
```

Return the intersection with another Area.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L382)

## `pygraphics.Area.offset`

```python
Area.offset(left, top=None, right=None, bottom=None)
```

Return an Area expanded independently on each edge.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L383)

## `pygraphics.Area.inset`

```python
Area.inset(left, top=None, right=None, bottom=None)
```

Return an Area reduced independently on each edge.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L384)

## `pygraphics.Area.x`

```python
Area.x
```

Left coordinate.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L229)

## `pygraphics.Area.y`

```python
Area.y
```

Top coordinate.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L230)

## `pygraphics.Area.w`

```python
Area.w
```

Width in pixels.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L231)

## `pygraphics.Area.h`

```python
Area.h
```

Height in pixels.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L232)

## `pygraphics.ClipContext`

```python
class ClipContext(draw, area)
```

Context manager returned by Draw.clip() for scoped clipping.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2147)

## `pygraphics.ClipContext.__enter__`

```python
ClipContext.__enter__()
```

Push the requested clipping area and return the effective clip.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2140)

## `pygraphics.ClipContext.__exit__`

```python
ClipContext.__exit__(exc_type, exc_value, traceback)
```

Pop the clipping area when leaving the context.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2141)

## `pygraphics.ClippedCanvas`

```python
class ClippedCanvas(canvas, clip)
```

Canvas proxy that intersects writes with a fixed Area.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2414)

## `pygraphics.ClippedCanvas.pixel`

```python
ClippedCanvas.pixel(x, y, color=None)
```

Read or write one pixel, depending on whether a color is supplied.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2402)

## `pygraphics.ClippedCanvas.fill`

```python
ClippedCanvas.fill(color)
```

Fill the target canvas with one color and return the affected Area.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2403)

## `pygraphics.ClippedCanvas.fill_rect`

```python
ClippedCanvas.fill_rect(x, y, width, height, color)
```

Fill a rectangular region and return the clipped affected Area.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2404)

## `pygraphics.ClippedCanvas.hline`

```python
ClippedCanvas.hline(x, y, width, color)
```

Draw a horizontal line.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2405)

## `pygraphics.ClippedCanvas.vline`

```python
ClippedCanvas.vline(x, y, height, color)
```

Draw a vertical line.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2406)

## `pygraphics.ClippedCanvas.blit_rect`

```python
ClippedCanvas.blit_rect(buffer, x, y, width, height)
```

Copy a packed RGB565 rectangle onto the target.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2407)

## `pygraphics.ClippedCanvas.blit_transparent`

```python
ClippedCanvas.blit_transparent(buffer, x, y, width, height, key)
```

Copy a packed RGB565 rectangle while skipping the transparent key.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2408)

## `pygraphics.ClippedCanvas.width`

```python
ClippedCanvas.width
```

Width in pixels.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2223)

## `pygraphics.ClippedCanvas.height`

```python
ClippedCanvas.height
```

Height in pixels.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2224)
