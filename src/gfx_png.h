#ifndef GFX_PNG_H
#define GFX_PNG_H

#include "gfx_framebuffer.h"
#include <stddef.h>
#include <stdint.h>

/* pygraphics has no PNG encoder: PNG is pngio's (micropython-pydevices'
 * modules/pngio, or pydevices-desktop's pngio.py over Pillow on CPython).
 * What is here is the rule for when a save is PNG, and the pixels pngio is
 * handed. */

/* pngio's format codes. */
#define GFX_PNGIO_RGB565 0
#define GFX_PNGIO_GS8 1
#define GFX_PNGIO_RGB888 2

/* Whether save_image writes PNG: for a path ending ".png" (any case) or an
 * RGB888 framebuffer, as the pure-Python save_image does. Every saver asks
 * this, so the three implementations can't disagree. */
int gfx_png_wanted(const gfx_fb_t *fb, const char *path);

/* Whether path ends ".png", in any case. */
int gfx_png_named(const char *path);

/* The pixels for pngio: its format code, and the bytes -- the framebuffer's
 * own, or for MONO_HLSB a GS8 copy returned in *owned (malloc'd; the caller
 * frees it). -1 for a format PNG can't take. */
int gfx_png_source(const gfx_fb_t *fb, int *fmt, const uint8_t **buf, size_t *len, uint8_t **owned);

#endif /* GFX_PNG_H */
