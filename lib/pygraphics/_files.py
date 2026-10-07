"""Load and save ``FrameBuffer`` images (PBM, PGM, RGB565 BMP) and export modules."""

from ._bmp565 import load_bmp565_buffer, read_bmp565_header, write_bmp565_file
from ._framebuf_plus import (
    GS2_HMSB,
    GS4_HMSB,
    GS8,
    MONO_HLSB,
    RGB565,
    RGB888,
    FrameBuffer,
)

# Framebuffer formats that ``save_image`` can write, keyed by file extension.
_SAVE_FORMATS = {
    MONO_HLSB: "pbm",
    GS2_HMSB: "pgm",
    GS4_HMSB: "pgm",
    GS8: "pgm",
    RGB565: "bmp",
    RGB888: "png",
}


def _read_header_line(f):
    """Read one PNM header line, skipping ``#`` comments. Returns bytes without newline."""
    while True:
        line = bytearray()
        while True:
            b = f.read(1)
            if not b:
                raise ValueError("Unexpected end of image header")
            if b == b"\n":
                break
            line.extend(b)
        if line and line[0] == 35:  # comment
            continue
        return bytes(line)


def _read_exact(f, n):
    """Allocate an ``n``-byte buffer and fill it from ``f`` (peak ≈ one pixel buffer)."""
    buf = bytearray(n)
    # Prefer readinto when available (CPython / most MicroPython ports).
    readinto = getattr(f, "readinto", None)
    if readinto is not None:
        mv = memoryview(buf)
        got = 0
        while got < n:
            nread = readinto(mv[got:])
            if not nread:
                raise ValueError("Truncated image pixel data")
            got += nread
        return buf
    data = f.read(n)
    if data is None or len(data) != n:
        raise ValueError("Truncated image pixel data")
    buf[:] = data
    return buf


def load_image(filename):
    """Load a ``FrameBuffer`` from a PBM, PGM, or RGB565 BMP file."""
    with open(filename, "rb") as f:
        header = f.read(2)
    if header == b"P4":
        return pbm_to_framebuffer(filename)
    if header == b"P5":
        return pgm_to_framebuffer(filename)
    if header == b"BM":
        return bmp_to_framebuffer(filename)
    raise ValueError(f"Unsupported image file {filename!r} (header {header!r})")


def _save_png(fb, filename):
    """PNG through pngio: MicroPython's built-in module, or on CPython
    pydevices-desktop's, over Pillow. pygraphics has no PNG encoder of its own."""
    try:
        import pngio
    except ImportError:
        raise ImportError(
            "saving PNG needs pngio: PyDevices MicroPython firmware has it built in; "
            "on CPython install pydevices-desktop and Pillow (pip install pillow)"
        ) from None
    w, h = fb.width, fb.height
    if fb.format == RGB565:
        fmt, buf = pngio.RGB565, fb.buffer
    elif fb.format == RGB888:
        fmt, buf = pngio.RGB888, fb.buffer
    elif fb.format == GS8:
        fmt, buf = pngio.GS8, fb.buffer
    elif fb.format == MONO_HLSB:
        # one bit a pixel, widened to grey
        fmt, buf, row = pngio.GS8, bytearray(w * h), (w + 7) // 8
        src = fb.buffer
        for y in range(h):
            for x in range(w):
                if (src[y * row + (x >> 3)] >> (7 - (x & 7))) & 1:
                    buf[y * w + x] = 255
    else:
        raise ValueError(f"PNG save not supported for format {fb.format}")
    data = pngio.PngEncoder().encode(buf, w, h, format=fmt)
    with open(filename, "wb") as f:
        f.write(data)


def save_image(fb, filename=None):
    """Save a ``FrameBuffer`` to PBM, PGM, BMP, or PNG based on format or filename.

    MONO_HLSB → PBM, GS2/GS4/GS8 → PGM, RGB565 → BMP (or PNG if filename ends in .png),
    RGB888 → PNG. Other formats raise ``ValueError``.
    """
    if filename is None:
        filename = "screenshot"

    file_ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else None
    if file_ext == "png" or fb.format == RGB888:
        if file_ext != "png":
            filename += ".png"
        _save_png(fb, filename)
        return filename

    ext = _SAVE_FORMATS.get(fb.format)
    if ext is None:
        raise ValueError(f"Save not supported for format {fb.format}")
    if file_ext != ext:
        filename += f".{ext}"
    if fb.format == MONO_HLSB:
        with open(filename, "wb") as f:
            f.write(b"P4\n")
            f.write(f"{fb.width} {fb.height}\n".encode())
            f.write(fb.buffer)
    elif fb.format == GS2_HMSB:
        with open(filename, "wb") as f:
            f.write(b"P5\n")
            f.write(f"{fb.width} {fb.height}\n".encode())
            f.write(b"3\n")
            f.write(fb.buffer)
    elif fb.format == GS4_HMSB:
        with open(filename, "wb") as f:
            f.write(b"P5\n")
            f.write(f"{fb.width} {fb.height}\n".encode())
            f.write(b"15\n")
            f.write(fb.buffer)
    elif fb.format == GS8:
        with open(filename, "wb") as f:
            f.write(b"P5\n")
            f.write(f"{fb.width} {fb.height}\n".encode())
            f.write(b"255\n")
            f.write(fb.buffer)
    elif fb.format == RGB565:
        with open(filename, "wb") as f:
            write_bmp565_file(f, fb.buffer, fb.width, fb.height)
    return filename


def pbm_to_framebuffer(filename):
    """
    Convert a PBM file to a MONO_HLSB FrameBuffer.

    Allocates one pixel buffer and reads pixels with ``readinto`` (peak ~1x).

    Args:
        filename (str): Filename of the PBM file

    Returns:
        FrameBuffer: Loaded monochrome framebuffer.
    """
    with open(filename, "rb") as f:
        if f.read(3) != b"P4\n":
            raise ValueError(f"Invalid PBM file {filename}")
        dims = _read_header_line(f).split()
        if len(dims) != 2:
            raise ValueError(f"Invalid PBM dimensions in {filename}")
        width, height = int(dims[0]), int(dims[1])
        buf = _read_exact(f, (width + 7) // 8 * height)
    return FrameBuffer(buf, width, height, MONO_HLSB)


def pgm_to_framebuffer(filename):
    """
    Convert a PGM file to a GS2_HMSB, GS4_HMSB or GS8 FrameBuffer.

    Allocates one pixel buffer and reads pixels with ``readinto`` (peak ~1x).

    Args:
        filename (str): Filename of the PGM file

    Returns:
        FrameBuffer: Loaded greyscale framebuffer (format from max value).
    """
    with open(filename, "rb") as f:
        if f.read(3) != b"P5\n":
            raise ValueError(f"Invalid PGM file {filename}")
        dims = _read_header_line(f).split()
        if len(dims) != 2:
            raise ValueError(f"Invalid PGM dimensions in {filename}")
        width, height = int(dims[0]), int(dims[1])
        max_value = int(_read_header_line(f))
        if max_value == 3:
            format = GS2_HMSB
            array_size = (width + 3) // 4 * height
        elif max_value == 15:
            format = GS4_HMSB
            array_size = (width + 1) // 2 * height
        elif max_value == 255:
            format = GS8
            array_size = width * height
        else:
            raise ValueError(f"Unsupported max value {max_value}")
        buf = _read_exact(f, array_size)
    return FrameBuffer(buf, width, height, format)


def bmp_to_framebuffer(filename):
    """
    Convert an RGB565 BMP file to a FrameBuffer.

    Args:
        filename (str): Path to the BMP file.

    Returns:
        FrameBuffer: Loaded RGB565 framebuffer.
    """
    with open(filename, "rb") as f:
        width, height, data_offset = read_bmp565_header(f)
        buffer = load_bmp565_buffer(f, width, height, data_offset)
    return FrameBuffer(buffer, width, height, RGB565)


def _bytes_literal_lines(data, width=16):
    lines = []
    for i in range(0, len(data), width):
        chunk = data[i : i + width]
        lit = "".join(f"\\x{b:02x}" for b in chunk)
        cont = "\\" if i + width < len(data) else ""
        lines.append(f"b'{lit}'{cont}")
    return lines


def export_framebuffer(fb, filename):
    """Export a ``FrameBuffer`` as an importable ``.py`` bitmap module.

    Format::

        WIDTH = …
        HEIGHT = …
        FORMAT = …
        BITMAP = bytearray(
        b'…'\\
        b'…'
        )

    ``BITMAP`` is a writable ``bytearray`` so MicroPython can wrap it in a
    ``FrameBuffer`` without copying. Prefer :meth:`FrameBuffer.from_bitmap` to
    load. Differs from :meth:`Font.export`, which keeps a read-only
    ``memoryview`` for glyph indexing.
    """
    if not filename.endswith(".py"):
        filename += ".py"
    data = bytes(fb.buffer)
    lines = [
        f"WIDTH = {int(fb.width)}",
        f"HEIGHT = {int(fb.height)}",
        f"FORMAT = {int(fb.format)}",
        "BITMAP = bytearray(",
    ]
    lines.extend(_bytes_literal_lines(data))
    lines.append(")")
    lines.append("")
    with open(filename, "w") as f:
        f.write("\n".join(lines) + "\n")
    return filename
