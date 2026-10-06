#include "gfx_png.h"
#include <string.h>
#include <stdlib.h>

static uint32_t adler32(const uint8_t *data, size_t len) {
    uint32_t s1 = 1;
    uint32_t s2 = 0;
    for (size_t i = 0; i < len; i++) {
        s1 = (s1 + data[i]) % 65521;
        s2 = (s2 + s1) % 65521;
    }
    return (s2 << 16) | s1;
}

static uint32_t crc32(const uint8_t *data, size_t len) {
    uint32_t crc = 0xFFFFFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= data[i];
        for (int j = 0; j < 8; j++) {
            if (crc & 1)
                crc = (crc >> 1) ^ 0xEDB88320;
            else
                crc >>= 1;
        }
    }
    return crc ^ 0xFFFFFFFF;
}

static void write_u32_be(uint8_t *p, uint32_t v) {
    p[0] = (uint8_t)(v >> 24);
    p[1] = (uint8_t)(v >> 16);
    p[2] = (uint8_t)(v >> 8);
    p[3] = (uint8_t)(v);
}

static void write_u16_le(uint8_t *p, uint16_t v) {
    p[0] = (uint8_t)(v);
    p[1] = (uint8_t)(v >> 8);
}

static size_t write_chunk(uint8_t *dst, const char *type, const uint8_t *data, size_t len) {
    write_u32_be(dst, (uint32_t)len);
    memcpy(dst + 4, type, 4);
    if (len > 0) {
        memcpy(dst + 8, data, len);
    }
    uint32_t crc = crc32(dst + 4, len + 4);
    write_u32_be(dst + 8 + len, crc);
    return 12 + len;
}

static size_t get_scanlines_size(const gfx_fb_t *fb, int *channels) {
    size_t row_len = 0;
    if (fb->format == GFX_RGB565 || fb->format == GFX_RGB888) {
        row_len = 1 + (size_t)fb->width * 3;
        *channels = 3;
    } else if (fb->format == GFX_GS8 || fb->format == GFX_MHLSB) {
        row_len = 1 + (size_t)fb->width;
        *channels = 1;
    } else {
        return 0;
    }
    return row_len * (size_t)fb->height;
}

int gfx_png_encoded_size(const gfx_fb_t *fb, size_t *out_len) {
    int channels = 0;
    size_t scanlines_size = get_scanlines_size(fb, &channels);
    if (scanlines_size == 0) return -1;
    
    size_t chunks = (scanlines_size + 65534) / 65535;
    if (scanlines_size == 0) chunks = 1;
    
    size_t idat_payload_len = 2 + chunks * 5 + scanlines_size + 4;
    
    size_t total = 8 + /* signature */
                   25 + /* IHDR */
                   12 + idat_payload_len + /* IDAT */
                   12; /* IEND */
    *out_len = total;
    return 0;
}

int gfx_png_encode(const gfx_fb_t *fb, uint8_t *dst, size_t dst_len, size_t *out_len) {
    size_t total_size = 0;
    if (gfx_png_encoded_size(fb, &total_size) < 0 || dst_len < total_size) {
        return -1;
    }
    
    int channels = 0;
    size_t scanlines_size = get_scanlines_size(fb, &channels);
    uint8_t *scanlines = (uint8_t *)malloc(scanlines_size > 0 ? scanlines_size : 1);
    if (!scanlines) return -1;
    
    const uint8_t *fb_buf = (const uint8_t *)fb->buf;
    if (fb->format == GFX_RGB565) {
        size_t s_off = 0;
        size_t d_off = 0;
        size_t stride = (size_t)fb->width * 2;
        size_t row_len = 1 + (size_t)fb->width * 3;
        for (int y = 0; y < fb->height; y++) {
            scanlines[d_off] = 0; // Filter
            size_t d = d_off + 1;
            size_t s = s_off;
            for (int x = 0; x < fb->width; x++) {
                uint8_t b0 = fb_buf[s];
                uint8_t b1 = fb_buf[s+1];
                s += 2;
                uint8_t r5 = b1 >> 3;
                scanlines[d] = (r5 << 3) | (r5 >> 2);
                uint8_t g6 = ((b1 & 0x07) << 3) | (b0 >> 5);
                scanlines[d+1] = (g6 << 2) | (g6 >> 4);
                uint8_t b5 = b0 & 0x1F;
                scanlines[d+2] = (b5 << 3) | (b5 >> 2);
                d += 3;
            }
            s_off += stride;
            d_off += row_len;
        }
    } else if (fb->format == GFX_RGB888) {
        size_t stride = (size_t)fb->width * 3;
        size_t row_len = 1 + stride;
        for (int y = 0; y < fb->height; y++) {
            scanlines[y * row_len] = 0;
            memcpy(scanlines + y * row_len + 1, fb_buf + y * stride, stride);
        }
    } else if (fb->format == GFX_GS8) {
        size_t stride = (size_t)fb->width;
        size_t row_len = 1 + stride;
        for (int y = 0; y < fb->height; y++) {
            scanlines[y * row_len] = 0;
            memcpy(scanlines + y * row_len + 1, fb_buf + y * stride, stride);
        }
    } else if (fb->format == GFX_MHLSB) {
        size_t row_bytes = ((size_t)fb->width + 7) / 8;
        size_t row_len = 1 + (size_t)fb->width;
        for (int y = 0; y < fb->height; y++) {
            size_t s_row = y * row_bytes;
            size_t d_row = y * row_len;
            scanlines[d_row] = 0;
            for (int x = 0; x < fb->width; x++) {
                uint8_t b = fb_buf[s_row + (x >> 3)];
                uint8_t bit = (b >> (7 - (x & 7))) & 1;
                scanlines[d_row + 1 + x] = bit ? 255 : 0;
            }
        }
    }
    
    // PNG Signature
    const uint8_t sig[8] = { 0x89, 'P', 'N', 'G', '\r', '\n', 0x1A, '\n' };
    memcpy(dst, sig, 8);
    size_t o = 8;
    
    // IHDR
    uint8_t ihdr[13];
    write_u32_be(ihdr, (uint32_t)fb->width);
    write_u32_be(ihdr + 4, (uint32_t)fb->height);
    ihdr[8] = 8; // bit depth
    ihdr[9] = (channels == 3) ? 2 : 0; // color type
    ihdr[10] = 0; // compression
    ihdr[11] = 0; // filter
    ihdr[12] = 0; // interlace
    o += write_chunk(dst + o, "IHDR", ihdr, 13);
    
    // IDAT
    size_t chunks = (scanlines_size + 65534) / 65535;
    if (scanlines_size == 0) chunks = 1;
    size_t idat_payload_len = 2 + chunks * 5 + scanlines_size + 4;
    
    write_u32_be(dst + o, (uint32_t)idat_payload_len);
    memcpy(dst + o + 4, "IDAT", 4);
    uint8_t *idat = dst + o + 8;
    
    idat[0] = 0x78;
    idat[1] = 0x01;
    size_t io = 2;
    size_t pos = 0;
    if (scanlines_size == 0) {
        idat[io++] = 0x01;
        write_u16_le(idat + io, 0);
        write_u16_le(idat + io + 2, 0xFFFF);
        io += 4;
    } else {
        while (pos < scanlines_size) {
            size_t chunk_size = scanlines_size - pos;
            if (chunk_size > 65535) chunk_size = 65535;
            uint8_t bfinal = (pos + chunk_size >= scanlines_size) ? 1 : 0;
            idat[io++] = bfinal;
            write_u16_le(idat + io, (uint16_t)chunk_size);
            write_u16_le(idat + io + 2, (uint16_t)(~chunk_size));
            io += 4;
            memcpy(idat + io, scanlines + pos, chunk_size);
            io += chunk_size;
            pos += chunk_size;
        }
    }
    uint32_t adler = adler32(scanlines, scanlines_size);
    write_u32_be(idat + io, adler);
    io += 4;
    uint32_t idat_crc = crc32(dst + o + 4, idat_payload_len + 4);
    write_u32_be(dst + o + 8 + idat_payload_len, idat_crc);
    o += 12 + idat_payload_len;
    
    free(scanlines);
    
    // IEND
    o += write_chunk(dst + o, "IEND", NULL, 0);
    
    *out_len = o;
    return 0;
}

int gfx_png_named(const char *path) {
    size_t n = strlen(path);
    return n >= 4 && path[n - 4] == '.' && (path[n - 3] | 0x20) == 'p'
        && (path[n - 2] | 0x20) == 'n' && (path[n - 1] | 0x20) == 'g';
}

int gfx_png_wanted(const gfx_fb_t *fb, const char *path) {
    return fb->format == GFX_RGB888 || gfx_png_named(path);
}
