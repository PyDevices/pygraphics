---
title: Runtime and pixel formats
description: Runtime capability probes and the exported framebuffer format constants.
---

Source snapshot: [`a02baf40d594bb77afae9676b5c803232bc188cd`](https://github.com/PyDevices/pygraphics/tree/a02baf40d594bb77afae9676b5c803232bc188cd).

Runtime capability probes and the exported framebuffer format constants.

Every entry below is generated from a public binding table or header declaration and links to its immutable source line.

## `pygraphics.framebuf_backend`

```python
pygraphics.framebuf_backend()
```

Return the active framebuffer backend identifier.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2950)

## `pygraphics.implementation`

```python
pygraphics.implementation()
```

Return the implementation identifier for this pygraphics module.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2951)

## `pygraphics.capabilities`

```python
pygraphics.capabilities()
```

Return structured runtime feature and pixel-format capabilities.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L2952)

## `pygraphics.MONO_VLSB`

```python
pygraphics.MONO_VLSB
```

Monochrome vertical least-significant-bit layout.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L3027)

## `pygraphics.MONO_HLSB`

```python
pygraphics.MONO_HLSB
```

Monochrome horizontal least-significant-bit layout.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L3028)

## `pygraphics.MONO_HMSB`

```python
pygraphics.MONO_HMSB
```

Monochrome horizontal most-significant-bit layout.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L3029)

## `pygraphics.RGB565`

```python
pygraphics.RGB565
```

16-bit RGB565 pixel layout.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L3030)

## `pygraphics.GS2_HMSB`

```python
pygraphics.GS2_HMSB
```

2-bit grayscale horizontal most-significant-bit layout.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L3031)

## `pygraphics.GS4_HMSB`

```python
pygraphics.GS4_HMSB
```

4-bit grayscale horizontal most-significant-bit layout.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L3032)

## `pygraphics.GS8`

```python
pygraphics.GS8
```

8-bit grayscale layout.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L3033)

## `pygraphics.RGB888`

```python
pygraphics.RGB888
```

24-bit RGB888 pixel layout.

[View the pinned source declaration](https://github.com/PyDevices/pygraphics/blob/a02baf40d594bb77afae9676b5c803232bc188cd/src/gfx_module_cpy.c#L3034)
