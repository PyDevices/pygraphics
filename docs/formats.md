# Formats

## Pixel formats

| Constant | Bits per pixel | Buffer size for `w` × `h` | Typical use |
|---|---|---|---|
| `MONO_VLSB` | 1 | `w * ((h + 7) // 8)` | monochrome screens, each byte is 8 pixels down a column, low bit at the top |
| `MONO_HLSB` | 1 | `((w + 7) // 8) * h` | monochrome screens, bytes run across, high bit on the left |
| `MONO_HMSB` | 1 | `((w + 7) // 8) * h` | as `MONO_HLSB`, low bit on the left |
| `GS2_HMSB` | 2 | `((w + 3) // 4) * h` | four-level greyscale |
| `GS4_HMSB` | 4 | `((w + 1) // 2) * h` | sixteen-level greyscale |
| `GS8` | 8 | `w * h` | 256-level greyscale |
| `RGB565` | 16 | `w * h * 2` | most small colour screens |
| `RGB888` | 24 | `w * h * 3` | 24-bit screens and RGB LED strips |

The first seven are `framebuf`'s formats with `framebuf`'s numbering, so a
buffer laid out for `framebuf` works here unchanged. `RGB888` is pygraphics'
own; its bytes are stored red, green, blue.

## Which file each format saves as

| Format | `save()` writes |
|---|---|
| `MONO_HLSB` | PBM (P4) |
| `GS2_HMSB` | PGM (P5, maximum 3) |
| `GS4_HMSB` | PGM (P5, maximum 15) |
| `GS8` | PGM (P5, maximum 255) |
| `RGB565` | BMP, 16-bit RGB565 |
| `RGB888` | PNG, always |
| `RGB565`, `GS8`, `MONO_HLSB` | PNG, when the name ends in `.png` |

`MONO_VLSB` and `MONO_HMSB` can't be saved directly and raise `ValueError`;
blit them into a `MONO_HLSB` framebuffer first. PNG needs the `pngio` module,
as [Load and save images](guides/load-and-save-images.md#save-a-picture)
explains.

`load_image()` reads PBM (P4), PGM (P5) and 16-bit RGB565 BMP files.

## Romfont files

A romfont `.bin` file, as `Font` reads it, is glyph rows and nothing else:

| | |
|---|---|
| Glyphs | 256, for characters 0–255, or 128 for 0–127 |
| Bytes per glyph | the font's height, one byte per row |
| Width | 8 pixels; the high bit of each byte is the leftmost pixel |
| File size | `256 × height` or `128 × height` bytes |

The built-in 8x8, 8x14 and 8x16 fonts come from the
[romfont](https://github.com/spacerace/romfont) collection.
