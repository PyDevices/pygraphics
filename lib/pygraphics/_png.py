# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""PNG encoder for pygraphics FrameBuffer and pixel buffers.

Encodes RGB565, RGB888, and GS8 framebuffers into standard PNG bytes.
Works across CPython and MicroPython:
  - Uses `zlib.compress` when available (CPython / unix ports)
  - Uses `deflate.DeflateIO` when streaming deflate compression is available
  - Falls back to RFC 1950/1951 uncompressed DEFLATE blocks (BTYPE 00)
    when no compression engine is present in firmware, guaranteeing valid
    PNG output on any compliant Python runtime without dependencies.
"""

import struct

try:
    import binascii
except ImportError:
    import ubinascii as binascii  # type: ignore

try:
    import zlib
except ImportError:
    zlib = None  # type: ignore

from ._framebuf_plus import GS8, MONO_HLSB, RGB565, RGB888

_PNG_SIG = b"\x89PNG\r\n\x1a\n"


def _adler32(data):
    """Compute Adler-32 checksum (RFC 1950) in pure Python."""
    if zlib is not None and hasattr(zlib, "adler32"):
        return zlib.adler32(data) & 0xFFFFFFFF
    s1 = 1
    s2 = 0
    for b in data:
        s1 = (s1 + b) % 65521
        s2 = (s2 + s1) % 65521
    return (s2 << 16) | s1


def _crc32(data):
    """Compute CRC-32 checksum for PNG chunks."""
    return binascii.crc32(data) & 0xFFFFFFFF


def _make_uncompressed_zlib(data):
    """Wrap raw scanlines in an uncompressed zlib stream (BTYPE=00 stored blocks)."""
    out = bytearray(b"\x78\x01")  # zlib header: Deflate, 32K window, check bits
    chunk_size = 65535
    total = len(data)
    pos = 0
    if total == 0:
        out.extend(b"\x01\x00\x00\xff\xff")
    else:
        while pos < total:
            chunk = data[pos : pos + chunk_size]
            pos += len(chunk)
            bfinal = 1 if pos >= total else 0
            out.append(bfinal)
            n = len(chunk)
            out.extend(struct.pack("<HH", n, (~n) & 0xFFFF))
            out.extend(chunk)
    out.extend(struct.pack(">I", _adler32(data)))
    return bytes(out)


def _compress_scanlines(data):
    """Compress raw scanline bytes using best available method."""
    if zlib is not None and hasattr(zlib, "compress"):
        try:
            return zlib.compress(data, 6)
        except Exception:
            pass

    # Try MicroPython deflate module if available
    try:
        import io

        import deflate

        buf = io.BytesIO()
        with deflate.DeflateIO(buf, deflate.ZLIB) as df:
            df.write(data)
        return buf.getvalue()
    except Exception:
        pass

    # Fallback: RFC 1950 uncompressed DEFLATE stream
    return _make_uncompressed_zlib(data)


def _png_chunk(kind, payload):
    """Build a standard PNG chunk with 4-byte length, type, data, and CRC-32."""
    data = kind + payload
    crc = _crc32(data)
    return struct.pack(">I", len(payload)) + data + struct.pack(">I", crc)


def _rgb565_to_scanlines(buffer, width, height):
    """Convert RGB565 little-endian buffer into RGB888 scanlines (with filter byte 0)."""
    stride = width * 2
    row_len = 1 + width * 3
    scanlines = bytearray(row_len * height)

    s_offset = 0
    d_offset = 0

    for _ in range(height):
        scanlines[d_offset] = 0  # Filter type: None
        d = d_offset + 1
        s = s_offset
        for _ in range(width):
            b0 = buffer[s]
            b1 = buffer[s + 1]
            s += 2
            # R: bits 15..11 (high byte bits 7..3)
            r5 = b1 >> 3
            scanlines[d] = (r5 << 3) | (r5 >> 2)
            # G: bits 10..5 (high byte bits 2..0, low byte bits 7..5)
            g6 = ((b1 & 0x07) << 3) | (b0 >> 5)
            scanlines[d + 1] = (g6 << 2) | (g6 >> 4)
            # B: bits 4..0 (low byte bits 4..0)
            b5 = b0 & 0x1F
            scanlines[d + 2] = (b5 << 3) | (b5 >> 2)
            d += 3
        s_offset += stride
        d_offset += row_len

    return scanlines


def _rgb888_to_scanlines(buffer, width, height):
    """Convert RGB888 buffer into scanlines (adding filter byte 0 per row)."""
    stride = width * 3
    row_len = 1 + stride
    scanlines = bytearray(row_len * height)
    for y in range(height):
        src_start = y * stride
        dst_start = y * row_len
        scanlines[dst_start] = 0  # Filter: None
        scanlines[dst_start + 1 : dst_start + row_len] = buffer[src_start : src_start + stride]
    return scanlines


def _gs8_to_scanlines(buffer, width, height):
    """Convert GS8 grayscale buffer into scanlines (adding filter byte 0 per row)."""
    stride = width
    row_len = 1 + stride
    scanlines = bytearray(row_len * height)
    for y in range(height):
        src_start = y * stride
        dst_start = y * row_len
        scanlines[dst_start] = 0  # Filter: None
        scanlines[dst_start + 1 : dst_start + row_len] = buffer[src_start : src_start + stride]
    return scanlines


def encode_png(fb, width=None, height=None, format=None):
    """Encode a FrameBuffer or raw pixel buffer into standard PNG bytes.

    Args:
        fb: A ``FrameBuffer`` instance, or a bytes-like object containing raw pixels.
        width: Image width in pixels (required if ``fb`` is not a ``FrameBuffer``).
        height: Image height in pixels (required if ``fb`` is not a ``FrameBuffer``).
        format: Format constant (e.g. ``RGB565``, ``RGB888``, ``GS8``). Defaults to
            ``fb.format`` if ``fb`` is a ``FrameBuffer``, else ``RGB565``.

    Returns:
        bytes: Complete, valid PNG file contents.
    """
    if hasattr(fb, "buffer") and hasattr(fb, "width") and hasattr(fb, "height"):
        buffer = fb.buffer
        if width is None:
            width = fb.width
        if height is None:
            height = fb.height
        if format is None:
            format = getattr(fb, "format", RGB565)
    else:
        buffer = fb
        if width is None or height is None:
            raise ValueError("width and height must be specified for raw buffers")
        if format is None:
            format = RGB565

    if width <= 0 or height <= 0:
        raise ValueError(f"Invalid dimensions {width}x{height}")

    # Build scanlines and choose color type
    if format == RGB565:
        scanlines = _rgb565_to_scanlines(buffer, width, height)
        color_type = 2  # Truecolor RGB
        bit_depth = 8
    elif format == RGB888:
        scanlines = _rgb888_to_scanlines(buffer, width, height)
        color_type = 2  # Truecolor RGB
        bit_depth = 8
    elif format == GS8:
        scanlines = _gs8_to_scanlines(buffer, width, height)
        color_type = 0  # Grayscale
        bit_depth = 8
    elif format == MONO_HLSB:
        # Convert 1-bit MONO_HLSB to GS8 grayscale
        gs8_buf = bytearray(width * height)
        row_bytes = (width + 7) // 8
        for y in range(height):
            s_row = y * row_bytes
            d_row = y * width
            for x in range(width):
                byte_val = buffer[s_row + (x >> 3)]
                bit = (byte_val >> (7 - (x & 7))) & 1
                gs8_buf[d_row + x] = 255 if bit else 0
        scanlines = _gs8_to_scanlines(gs8_buf, width, height)
        color_type = 0  # Grayscale
        bit_depth = 8
    else:
        raise ValueError(f"Unsupported format {format} for PNG encoding")

    compressed = _compress_scanlines(scanlines)

    # PNG chunks: IHDR, IDAT, IEND
    ihdr_data = struct.pack(">IIBBBBB", width, height, bit_depth, color_type, 0, 0, 0)
    ihdr = _png_chunk(b"IHDR", ihdr_data)
    idat = _png_chunk(b"IDAT", compressed)
    iend = _png_chunk(b"IEND", b"")

    return _PNG_SIG + ihdr + idat + iend


def write_png_file(f, fb, width=None, height=None, format=None):
    """Encode and write PNG bytes to an open binary file stream."""
    data = encode_png(fb, width=width, height=height, format=format)
    f.write(data)
    return len(data)
