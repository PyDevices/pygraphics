#ifndef GFX_PNG_H
#define GFX_PNG_H

#include "gfx_framebuffer.h"
#include <stddef.h>

/* Compute the exact byte size of the uncompressed PNG for the given framebuffer.
 * Returns -1 if the format is unsupported. */
int gfx_png_encoded_size(const gfx_fb_t *fb, size_t *out_len);

/* Encode the framebuffer into the destination buffer as an uncompressed PNG.
 * dst must be at least the size returned by gfx_png_encoded_size. */
int gfx_png_encode(const gfx_fb_t *fb, uint8_t *dst, size_t dst_len, size_t *out_len);

#endif /* GFX_PNG_H */
