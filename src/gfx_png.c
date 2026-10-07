/* When a save is PNG, and what pngio is handed (gfx_png.h). The encoding is
 * pngio's. */
#include "gfx_png.h"

#include <stdlib.h>
#include <string.h>

int gfx_png_named(const char *path) {
    size_t n = strlen(path);
    return n >= 4 && path[n - 4] == '.' && (path[n - 3] | 0x20) == 'p'
        && (path[n - 2] | 0x20) == 'n' && (path[n - 1] | 0x20) == 'g';
}

int gfx_png_wanted(const gfx_fb_t *fb, const char *path) {
    return fb->format == GFX_RGB888 || gfx_png_named(path);
}

int gfx_png_source(const gfx_fb_t *fb, int *fmt, const uint8_t **buf, size_t *len, uint8_t **owned) {
    const size_t px = (size_t)fb->width * fb->height;
    *owned = NULL;
    switch (fb->format) {
        case GFX_RGB565:
            *fmt = GFX_PNGIO_RGB565, *buf = (const uint8_t *)fb->buf, *len = px * 2;
            return 0;
        case GFX_RGB888:
            *fmt = GFX_PNGIO_RGB888, *buf = (const uint8_t *)fb->buf, *len = px * 3;
            return 0;
        case GFX_GS8:
            *fmt = GFX_PNGIO_GS8, *buf = (const uint8_t *)fb->buf, *len = px;
            return 0;
        case GFX_MHLSB: {
            /* one bit a pixel, widened to grey */
            uint8_t *g = (uint8_t *)malloc(px ? px : 1);
            if (g == NULL) {
                return -1;
            }
            const uint8_t *src = (const uint8_t *)fb->buf;
            const size_t row = ((size_t)fb->width + 7) / 8;
            for (int y = 0; y < fb->height; y++) {
                for (int x = 0; x < fb->width; x++) {
                    g[(size_t)y * fb->width + x] = ((src[y * row + (x >> 3)] >> (7 - (x & 7))) & 1) ? 255 : 0;
                }
            }
            *fmt = GFX_PNGIO_GS8, *buf = g, *len = px, *owned = g;
            return 0;
        }
        default:
            return -1;
    }
}
