# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Cross-platform 2D drawing for MicroPython, CircuitPython and CPython.

Draw shapes, text and images into a framebuffer. Every drawing call returns
the `Area` it changed, so you can send just that part to a screen.

The compiled module and the pure-Python package have the same names, except
four that write or read Python source and exist only in the pure-Python
package; each says so. `implementation()` tells you which one you have.

Example::

    import pygraphics

    fb = pygraphics.FrameBuffer(bytearray(16 * 16 * 2), 16, 16, pygraphics.RGB565)
    fb.fill(0)
    area = fb.fill_rect(1, 1, 6, 6, 0xFFFF)
    pygraphics.text8(fb, "Hi", 0, 0, 0xFFFF)
"""

from __future__ import annotations

from typing import Any, Iterator

__revision__: str
"""Which source this build came from, from `git describe`: a release tag, or
the nearest one and the commit. Only the compiled module has it."""

# -- pixel formats ------------------------------------------------------------

MONO_VLSB: int
"""1 bit per pixel; each byte is 8 pixels down a column, low bit at the top."""
MONO_HLSB: int
"""1 bit per pixel; bytes run across a row, high bit on the left."""
MONO_HMSB: int
"""1 bit per pixel; bytes run across a row, low bit on the left."""
GS2_HMSB: int
"""2 bits per pixel: four-level greyscale."""
GS4_HMSB: int
"""4 bits per pixel: sixteen-level greyscale."""
GS8: int
"""8 bits per pixel: 256-level greyscale."""
RGB565: int
"""16 bits per pixel, the format of most small colour screens."""
RGB888: int
"""24 bits per pixel, stored red, green, blue. pygraphics' own format, not
`framebuf`'s."""

class Area:
    """Rectangular geometry helper used for dirty-rectangle updates, hit testing,
    and clipping.

    `Area` values are commonly returned by drawing helpers such as
    `fill_rect` and `circle` and can be used to refresh only the
    pixels that changed. They are also useful for widget hit testing, button
    bounds, and trimming a draw operation to a sub-region of the screen.

    The constructor accepts either separate ``(x, y, w, h)`` values or a single
    tuple containing those four values.

    Attributes:
        x (int | float): The x-coordinate of the top-left corner of the area.
        y (int | float): The y-coordinate of the top-left corner of the area.
        w (int | float): The width of the area.
        h (int | float): The height of the area.
    """

    x: int | float
    y: int | float
    w: int | float
    h: int | float

    def __init__(self, x: int | float | tuple[int | float, int | float, int | float, int | float], y: int | float | None = None, w: int | float | None = None, h: int | float | None = None) -> None:
        """Create an area from explicit coordinates or from a single ``(x, y, w, h)`` tuple.

        Args:
            x (int | float | tuple): The left edge, or a tuple containing
                ``(x, y, w, h)``.
            y (int | float): The top edge.
            w (int | float): The width of the area.
            h (int | float): The height of the area.
        """

    def contains(self, x: int | tuple, y: int | None = None) -> bool:
        """Checks if the specified point is contained within the area.

        Args:
            x (int | tuple): The x-coordinate of the point to check
                or a tuple containing the x and y coordinates of the point.
            y (int): The y-coordinate of the point to check.

        Returns:
            (bool): True if the point is contained within the area, False otherwise.
        """

    def contains_area(self, other: Area) -> bool:
        """Checks if the specified area is contained within the area.

        Args:
            other (Area): The other area to check.

        Returns:
            (bool): True if the other area is contained within the area, False otherwise.
        """

    def intersects(self, other: Area) -> bool:
        """Checks if the current Area object intersects with another Area object.

        Args:
            other (Area): The other Area object to check for overlap.

        Returns:
            (bool): True if the two Area objects intersect, False otherwise.
        """

    def touches_or_intersects(self, other: Area) -> bool:
        """Checks if the current Area object touches or intersects with another Area object.

        Args:
            other (Area): The other Area object to check for overlap or touch.

        Returns:
            (bool): True if the two Area objects touch or intersect, False otherwise.
        """

    def shift(self, dx: int | float = 0, dy: int | float = 0) -> Area:
        """Returns a new Area shifted by the specified amount in the x and y directions.

        Args:
            dx (int | float): The amount to shift the area in the x direction.
            dy (int | float): The amount to shift the area in the y direction.

        Returns:
            (Area): A new Area object shift by the specified amount in the x and y directions.
        """

    def clip(self, other: Area) -> Area:
        """Clips the current Area object to the specified Area object.

        Args:
            other (Area): The other Area object to clip to.

        Returns:
            (Area): A new Area object representing the clipped area.
        """

    def offset(self, d1: int | float, d2: int | float | None = None, d3: int | float | None = None, d4: int | float | None = None) -> Area:
        """Returns a new Area offset by the specified amount(s).

        If only one argument is provided, it is used as the offset in all 4 directions.
        If two arguments are provided, the first is used as the offset in the x direction and the second as the offset in the y direction.
        If three arguments are provided, they are used as the offsets in the left, top/bottom, and right directions, respectively.
        If four arguments are provided, they are used as the offsets in the left, top, right, and bottom directions, respectively.

        Args:
            d1 (int | float): The offset in the x direction or the offset in all 4 directions.
            d2 (int | float): The offset in the y direction or the offset in the top/bottom direction.
            d3 (int | float): The offset in the right direction.
            d4 (int | float): The offset in the bottom direction.

        Returns:
            (Area): A new Area object offset by the specified amount(s).
        """

    def inset(self, d1: int | float, d2: int | float | None = None, d3: int | float | None = None, d4: int | float | None = None) -> Area:
        """Returns a new Area inset by the specified amount(s).

        If only one argument is provided, it is used as the inset in all 4 directions.
        If two arguments are provided, the first is used as the inset in the x direction and the second as the inset in the y direction.
        If three arguments are provided, they are used as the insets in the left, top/bottom, and right directions, respectively.
        If four arguments are provided, they are used as the insets in the left, top, right, and bottom directions, respectively.

        Args:
            d1 (int | float): The inset in the x direction or the inset in all 4 directions.
            d2 (int | float): The inset in the y direction or the inset in the top/bottom direction.
            d3 (int | float): The inset in the right direction.
            d4 (int | float): The inset in the bottom direction.

        Returns:
            (Area): A new Area object inset by the specified amount(s).
        """

    def __eq__(self, other: object) -> bool:
        """Checks if the current Area object is equal to another Area object.

        Args:
            other (Area): The other Area object to compare with.

        Returns:
            (bool): True if the two Area objects are equal, False otherwise.
        """

    def __ne__(self, other: object) -> bool:
        """Checks if the current Area object is not equal to another Area object.

        Args:
            other (Area): The other Area object to compare with.

        Returns:
            (bool): True if the two Area objects are not equal, False otherwise.
        """

    def __add__(self, other: Area) -> Area:
        """Computes the union of the current Area object and another Area object.

        Args:
            other (Area): The other Area object to compute the union with.

        Returns:
            (Area): A new Area object representing the union of the two areas.
        """

    def __bool__(self) -> bool:
        """True when the area has positive width and height."""

    def __iter__(self) -> Iterator[int | float]:
        """Returns an iterator over the elements of the Area object.

        Returns:
            (iterator): An iterator over the elements of the Area object.
        """

class FrameBuffer:
    """Framebuffer surface for drawing either to the display itself or to an
    off-screen buffer.

    This class preserves the standard ``framebuf`` API while adding helpers for
    shapes, text, and image I/O. Each draw operation returns an `Area`
    describing the pixels that changed, which is ideal for dirty-rectangle
    updates and for compositing a pre-rendered scene before pushing it to the
    display.

    Typical usage is to create a ``bytearray`` large enough for the target size,
    draw a frame with `fill`, `fill_rect`, `circle`, or
    `text8`, then copy that buffer to a display driver or use the returned
    ``Area`` to refresh only the changed region.

    Args:
        buffer (bytearray): Framebuffer buffer.
        width (int): Width in pixels.
        height (int): Height in pixels.
        format (int): Framebuffer format constant such as ``RGB565`` or ``RGB888``.
    """

    def __init__(self, buffer: bytearray, width: int, height: int, format: int, *args: Any, **kwargs: Any) -> None:
        """Create a framebuffer wrapping ``buffer``.

        Args:
            buffer (bytearray): Pixel storage (writable).
            width (int): Width in pixels.
            height (int): Height in pixels.
            format (int): Pixel format constant (``RGB565``, ``RGB888``, etc.).
            *args (Any): Forwarded to the base ``framebuf.FrameBuffer`` (e.g. stride).
            **kwargs (Any): Forwarded to the base constructor (e.g. ``stride=``).

        Raises:
            ValueError: If ``format`` is not a supported constant.
        """

    @property
    def color_depth(self) -> int:
        """Bits per pixel for the current format (1, 2, 4, 8, 16, or 24)."""

    @property
    def width(self) -> int:
        """Framebuffer width in pixels."""

    @property
    def height(self) -> int:
        """Framebuffer height in pixels."""

    @property
    def buffer(self) -> bytearray | memoryview:
        """Underlying pixel buffer passed to the constructor."""

    @property
    def format(self) -> int:
        """Pixel format constant (``RGB565``, ``RGB888``, ``MONO_HLSB``, …)."""

    def fill_rect(self, x: int, y: int, w: int, h: int, c: int) -> Area:
        """Fill a rectangle with a solid color.

        This is the usual primitive for clearing a region, drawing panels, or
        staging a background before more detailed shapes or text are drawn.

        Args:
            x (int): X coordinate of the top-left corner.
            y (int): Y coordinate of the top-left corner.
            w (int): Width in pixels.
            h (int): Height in pixels.
            c (int): Color to write.

        Returns:
            Area: Bounding box of the filled rectangle.
        """

    def pixel(self, x: int, y: int, c: int | None = None) -> Area | int:
        """Read or draw a single pixel.

        With ``c`` it draws the pixel; without, it reads the pixel's color.

        Args:
            x (int): x coordinate
            y (int): y coordinate
            c (int): color to draw (default: None, to read the pixel)

        Returns:
            (Area | int): The bounding box of the pixel when drawing, or the
            pixel's color when reading.
        """

    def fill(self, c: int) -> Area:
        """Fill the buffer with the given color.

        Args:
            c (int): color

        Returns:
            (Area): Bounding box of the filled buffer
        """

    def ellipse(self, x: int, y: int, rx: int, ry: int, c: int, f: bool = False, m: int = 15) -> Area:
        """Draw an ellipse at the given location, radii and color.

        Args:
            x (int): Center x coordinate
            y (int): Center y coordinate
            rx (int): X radius
            ry (int): Y radius
            c (int): color
            f (bool): Fill the ellipse (default: False)
            m (int): Bitmask to determine which quadrants to draw (default: 0b1111)

        Returns:
            (Area): Bounding box of the ellipse
        """

    def hline(self, x: int, y: int, w: int, c: int) -> Area:
        """Draw a horizontal line at the given location, width and color.

        Args:
            x (int): x coordinate
            y (int): y coordinate
            w (int): Width in pixels
            c (int): color

        Returns:
            (Area): Bounding box of the horizontal line
        """

    def line(self, x1: int, y1: int, x2: int, y2: int, c: int) -> Area:
        """Draw a line between the given start and end points and color.

        Args:
            x1 (int): Start x coordinate
            y1 (int): Start y coordinate
            x2 (int): End x coordinate
            y2 (int): End y coordinate
            c (int): color

        Returns:
            (Area): Bounding box of the line
        """

    def poly(self, x: int, y: int, coords: list[int] | tuple[int, ...], c: int, f: bool = False) -> Area:
        """Draw a polygon at the given location, coordinates and color.

        Args:
            x (int): x coordinate
            y (int): y coordinate
            coords (array): Array of x, y coordinate tuples
            c (int): color
            f (bool): Fill the polygon (default: False)

        Returns:
            (Area): Bounding box of the polygon
        """

    def rect(self, x: int, y: int, w: int, h: int, c: int, f: bool = False) -> Area:
        """Draw a rectangle at the given location, size and color.

        Args:
            x (int): Top left corner x coordinate
            y (int): Top left corner y coordinate
            w (int): Width in pixels
            h (int): Height in pixels
            c (int): color
            f (bool): Fill the rectangle (default: False)

        Returns:
            (Area): Bounding box of the rectangle
        """

    def vline(self, x: int, y: int, h: int, c: int) -> Area:
        """Draw a vertical line at the given location, height and color.

        Args:
            x (int): x coordinate
            y (int): y coordinate
            h (int): Height in pixels
            c (int): color

        Returns:
            (Area): Bounding box of the vertical line
        """

    def text(self, s: str, x: int, y: int, c: int = 1, scale: int = 1, inverted: bool = False, font_data: str | None = None, height: int = 8) -> Area:
        """Draw text at the given location, using the given font and color.

        Args:
            s (str): Text to draw
            x (int): x coordinate
            y (int): y coordinate
            c (int): color
            scale (int): Scale factor (default: 1)
            inverted (bool): Invert the text (default: False)
            font_data (str): Path to the font file (default: None)
            height (int): Height of the font (default: 8)

        Returns:
            (Area): Bounding box of the text
        """

    def blit(self, source, x: int, y: int, key: int = -1, palette: Any = None) -> Area:
        """Blit the given buffer at the given location.

        Args:
            source (FrameBuffer): FrameBuffer to blit
            x (int): x coordinate
            y (int): y coordinate
            key (int): Color key (default: -1)
            palette (FrameBuffer): Palette (default: None)

        Returns:
            (Area): Bounding box of the blitted buffer
        """

    def arc(self, x: int, y: int, r: int, a0: float, a1: float, c: int) -> Area:
        """Arc drawing function.  Will draw a single pixel wide arc with a radius r
        centered at x, y from a0 to a1.

        Args:
            x (int): X-coordinate of the arc's center.
            y (int): Y-coordinate of the arc's center.
            r (int): Radius of the arc.
            a0 (float): Starting angle in degrees.
            a1 (float): Ending angle in degrees.
            c (int): color.

        Returns:
            (Area): The bounding box of the arc.
        """

    def blit_rect(self, buf, x: int, y: int, w: int, h: int) -> Area:
        """Blit a rectangular area from a buffer to the canvas.  Uses the canvas's blit_rect method if available,
        otherwise writes directly to the buffer.

        Args:
            buf (memoryview): Buffer to blit. Must already be byte-swapped if necessary.
            x (int): X-coordinate to blit to.
            y (int): Y-coordinate to blit to.
            w (int): Width of the area to blit.
            h (int): Height of the area to blit.

        Returns:
            (Area): The bounding box of the blitted area.
        """

    def blit_transparent(self, buf, x: int, y: int, w: int, h: int, key: int) -> Area:
        """Blit a buffer with transparency.

        Args:
            buf (memoryview): Buffer to blit.
            x (int): X-coordinate to blit to.
            y (int): Y-coordinate to blit to.
            w (int): Width of the area to blit.
            h (int): Height of the area to blit.
            key (int): Key value for transparency.

        Returns:
            (Area): The bounding box of the blitted area.
        """

    def circle(self, x0: int, y0: int, r: int, c: int, f: bool = False) -> Area:
        """Circle drawing function.  Will draw a single pixel wide circle
        centered at x0, y0 and the specified r.

        Args:
            x0 (int): Center x coordinate
            y0 (int): Center y coordinate
            r (int): Radius
            c (int): Color
            f (bool): Fill the circle (default: False)

        Returns:
            (Area): The bounding box of the circle.
        """

    def gradient_rect(self, x: int, y: int, w: int, h: int, c1: int, c2: int | None = None, vertical: bool = True) -> Area:
        """Fill a rectangle with a gradient.

        Args:
            x (int): X-coordinate of the top-left corner of the rectangle.
            y (int): Y-coordinate of the top-left corner of the rectangle.
            w (int): Width of the rectangle.
            h (int): Height of the rectangle.
            c1 (int): 565 encoded color for the top or left edge.
            c2 (int): 565 encoded color for the bottom or right edge.  If None or the same as c1,
                        fill_rect will be called instead.
            vertical (bool): If True, the gradient will be vertical.  If False, the gradient will be horizontal.

        Returns:
            (Area): The bounding box of the filled area.
        """

    def polygon(self, points: list, x: int, y: int, color: int, angle: float = 0, center_x: int = 0, center_y: int = 0) -> Area:
        """Draw a polygon on the canvas.

        Args:
            points (list): List of points to draw.
            x (int): X-coordinate of the polygon's position.
            y (int): Y-coordinate of the polygon's position.
            color (int): color.
            angle (float): Rotation angle in radians (default: 0).
            center_x (int): X-coordinate of the rotation center (default: 0).
            center_y (int): Y-coordinate of the rotation center (default: 0).

        Raises:
            ValueError: If the polygon has less than 3 points.

        Returns:
            (Area): The bounding box of the polygon.
        """

    def round_rect(self, x0: int, y0: int, w: int, h: int, r: int, c: int, f: bool = False) -> Area:
        """Rounded rectangle drawing function.  Will draw a single pixel wide rounded rectangle starting at
        x0, y0 and extending w, h pixels with the specified radius.

        Args:
            x0 (int): X-coordinate of the top-left corner of the rectangle.
            y0 (int): Y-coordinate of the top-left corner of the rectangle.
            w (int): Width of the rectangle.
            h (int): Height of the rectangle.
            r (int): Radius of the corners.
            c (int): color.
            f (bool): Fill the rectangle (default: False).

        Returns:
            (Area): The bounding box of the rectangle.
        """

    def triangle(self, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, c: int, f: bool = False) -> Area:
        """Triangle drawing function.  Draws a single pixel wide triangle with vertices at
        (x0, y0), (x1, y1), and (x2, y2).

        Args:
            x0 (int): X-coordinate of the first vertex.
            y0 (int): Y-coordinate of the first vertex.
            x1 (int): X-coordinate of the second vertex.
            y1 (int): Y-coordinate of the second vertex.
            x2 (int): X-coordinate of the third vertex.
            y2 (int): Y-coordinate of the third vertex.
            c (int): color.
            f (bool): Fill the triangle (default: False).

        Returns:
            (Area): The bounding box of the triangle.
        """

    def text8(self, s: str, x: int, y: int, c: int = 1, scale: int = 1, inverted: bool = False, font_data: str | None = None) -> Area:
        """Place text on the canvas with an 8 pixel high font.
        Breaks on ``\\n`` to next line.  Does not break on line going off canvas.

        Args:
            s (str): The text to draw.
            x (int): The x position to start drawing the text.
            y (int): The y position to start drawing the text.
            c (int): The color to draw the text in.  Default is 1.
            scale (int): The scale factor to draw the text at.  Default is 1.
            inverted (bool): If True, draw the text inverted.  Default is False.
            font_data (str): The path to the font file to use.  Default is None.

        Returns:
            Area: The area that was drawn to.
        """

    def text14(self, s: str, x: int, y: int, c: int = 1, scale: int = 1, inverted: bool = False, font_data: str | None = None) -> Area:
        """Place text on the canvas with a 14 pixel high font.
        Breaks on ``\\n`` to next line.  Does not break on line going off canvas.

        Args:
            s (str): The text to draw.
            x (int): The x position to start drawing the text.
            y (int): The y position to start drawing the text.
            c (int): The color to draw the text in.  Default is 1.
            scale (int): The scale factor to draw the text at.  Default is 1.
            inverted (bool): If True, draw the text inverted.  Default is False.
            font_data (str): The path to the font file to use.  Default is None.

        Returns:
            Area: The area that was drawn to.
        """

    def text16(self, s: str, x: int, y: int, c: int = 1, scale: int = 1, inverted: bool = False, font_data: str | None = None) -> Area:
        """Place text on the canvas with a 16 pixel high font.
        Breaks on ``\\n`` to next line.  Does not break on line going off canvas.

        Args:
            s (str): The text to draw.
            x (int): The x position to start drawing the text.
            y (int): The y position to start drawing the text.
            c (int): The color to draw the text in.  Default is 1.
            scale (int): The scale factor to draw the text at.  Default is 1.
            inverted (bool): If True, draw the text inverted.  Default is False.
            font_data (str): The path to the font file to use.  Default is None.

        Returns:
            Area: The area that was drawn to.
        """

    def scroll(self, xstep: int, ystep: int) -> Area:
        """Scroll buffer contents. Returns the full buffer bounds."""

    def save(self, filename: str | None = None) -> str:
        """Save the framebuffer to a file.  The file extension must match the format, otherwise
        the extension will be appended to the filename.

        Saves 1-bit formats as PBM, 2-bit formats as PGM with max value 3, 4-bit formats as PGM with max value 15,
        8-bit formats as PGM with max value 255, and 16-bit formats as BMP.

        Args:
            filename (str): Filename to save to
        """

    def export(self, filename: str) -> str:
        """Export this framebuffer as an importable ``.py`` bitmap module.

        Only the pure-Python package has this.

        See `pygraphics._files.export_framebuffer`. Ships ``BITMAP`` as a
        ``bytearray`` for zero-copy `from_bitmap` on MicroPython.
        """

    @staticmethod
    def from_file(filename: str) -> FrameBuffer:
        """Load a framebuffer from a file.

        Args:
            filename (str): Filename to load from

        Returns:
            FrameBuffer: Image loaded as a framebuffer.
        """

    @staticmethod
    def from_bitmap(buffer: bytearray | memoryview | bytes, width: int, height: int, format: int) -> FrameBuffer:
        """Build a ``FrameBuffer`` from a bitmap buffer (export-module style).

        If ``buffer`` is already a writable ``bytearray`` (or a writable
        ``memoryview``), it is used without copying. Legacy ``bytes`` /
        ``memoryview(bytes)`` modules get one ``bytearray`` copy so MicroPython
        can own a writable pixel buffer.

        Only the pure-Python package has this.
        """

    @staticmethod
    def from_module(mod: Any) -> FrameBuffer:
        """Load from a module with ``WIDTH``, ``HEIGHT``, ``FORMAT``, ``BITMAP``.

        Only the pure-Python package has this.
        """

def arc(canvas, x: int, y: int, r: int, a0: float, a1: float, c: int) -> Area:
    """Arc drawing function.  Will draw a single pixel wide arc with a radius r
    centered at x, y from a0 to a1.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x (int): X-coordinate of the arc's center.
        y (int): Y-coordinate of the arc's center.
        r (int): Radius of the arc.
        a0 (float): Starting angle in degrees.
        a1 (float): Ending angle in degrees.
        c (int): color.

    Returns:
        (Area): The bounding box of the arc.
    """

def blit(canvas, source, x: int, y: int, key: int = -1, palette: Any = None) -> Area:
    """Copy a source buffer or sprite onto a canvas.

    This is useful for compositing an off-screen frame into the live display,
    for scrolling text and sprite animations, and for drawing pre-rendered tiles
    or bitmaps. The returned area is the region that was written so that it can
    be treated as a dirty rectangle.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        source (FrameBuffer): Source framebuffer or canvas-like object.
        x (int): X-coordinate to blit to.
        y (int): Y-coordinate to blit to.
        key (int): Key value for transparency (default: -1).
        palette (Palette): Palette object for color translation (default: None).

    Returns:
        Area: The bounding box of the blitted area.
    """

def blit_rect(canvas, buf, x: int, y: int, w: int, h: int) -> Area:
    """Blit a rectangular area from a buffer to the canvas.  Uses the canvas's blit_rect method if available,
    otherwise writes directly to the buffer.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        buf (memoryview): Buffer to blit. Must already be byte-swapped if necessary.
        x (int): X-coordinate to blit to.
        y (int): Y-coordinate to blit to.
        w (int): Width of the area to blit.
        h (int): Height of the area to blit.

    Returns:
        (Area): The bounding box of the blitted area.
    """

def blit_transparent(canvas, buf, x: int, y: int, w: int, h: int, key: int) -> Area:
    """Blit a buffer with transparency.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        buf (memoryview): Buffer to blit.
        x (int): X-coordinate to blit to.
        y (int): Y-coordinate to blit to.
        w (int): Width of the area to blit.
        h (int): Height of the area to blit.
        key (int): Key value for transparency.

    Returns:
        (Area): The bounding box of the blitted area.
    """

def circle(canvas, x0: int, y0: int, r: int, c: int, f: bool = False) -> Area:
    """Draw a circle or filled disk centered at ``(x0, y0)``.

    This is a common primitive for buttons, status indicators, animated balls,
    and other UI ornaments. Pass ``f=True`` for a filled circle.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x0 (int): Center x coordinate.
        y0 (int): Center y coordinate.
        r (int): Radius.
        c (int): Color.
        f (bool): Fill the circle (default: ``False``).

    Returns:
        Area: The bounding box of the circle.
    """

def ellipse(canvas, x0: int, y0: int, r1: int, r2: int, c: int, f: bool = False, m: int = 15, w: int | None = None, h: int | None = None) -> Area:
    """Midpoint ellipse algorithm
    Draw an ellipse at the given location. Radii r1 and r2 define the geometry; equal values cause a
    circle to be drawn. The c parameter defines the color.

    The optional f parameter can be set to True to fill the ellipse. Otherwise just a one pixel outline
    is drawn.

    The optional m parameter enables drawing to be restricted to certain quadrants of the ellipse.
    The LS four bits determine which quadrants are to be drawn, with bit 0 specifying Q1, b1 Q2,
    b2 Q3 and b3 Q4. Quadrants are numbered counterclockwise with Q1 being top right.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x0 (int): Center x coordinate
        y0 (int): Center y coordinate
        r1 (int): x radius
        r2 (int): y radius
        c (int): color
        f (bool): Fill the ellipse (default: False)
        m (int): Bitmask to determine which quadrants to draw (default: 0b1111)
        w (int): Width of the ellipse (default: None)
        h (int): Height of the ellipse (default: None)

    Returns:
        (Area): The bounding box of the ellipse.
    """

def fill(canvas, c: int) -> Area:
    """Fill the entire canvas with a solid color.

    This is the typical first step for each frame: clear the previous scene,
    then draw the next frame on top of it.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        c (int): Color.

    Returns:
        Area: The bounding box of the filled area.
    """

def fill_rect(canvas, x: int, y: int, w: int, h: int, c: int) -> Area:
    """Draw a filled rectangle.

    Use this for backgrounds, panels, status bars, and other simple UI blocks.
    It is also the workhorse for clipping and partial redraw operations.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x (int): X-coordinate of the top-left corner.
        y (int): Y-coordinate of the top-left corner.
        w (int): Width of the rectangle.
        h (int): Height of the rectangle.
        c (int): Color.

    Returns:
        Area: The bounding box of the filled area.
    """

def gradient_rect(canvas, x: int, y: int, w: int, h: int, c1: int, c2: int | None = None, vertical: bool = True) -> Area:
    """Fill a rectangle with a vertical or horizontal color ramp.

    This is useful for scenery, backgrounds, and other effects where a smooth
    transition looks better than a flat fill. The gallery applications use it for
    animated skies and other stylized backdrops.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x (int): X-coordinate of the top-left corner.
        y (int): Y-coordinate of the top-left corner.
        w (int): Width of the rectangle.
        h (int): Height of the rectangle.
        c1 (int): Color for the top or left edge (format-native).
        c2 (int): Color for the bottom or right edge. If omitted or equal to
            ``c1``, the helper falls back to `fill_rect`.
        vertical (bool): If ``True``, draw a vertical gradient; otherwise a horizontal one.

    Returns:
        Area: The bounding box of the filled area.
    """

def hline(canvas, x0: int, y0: int, w: int, c: int) -> Area:
    """Horizontal line drawing function.  Will draw a single pixel wide line.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x0 (int): X-coordinate of the start of the line.
        y0 (int): Y-coordinate of the start of the line.
        w (int): Width of the line.
        c (int): color.

    Returns:
        (Area): The bounding box of the line.
    """

def line(canvas, x0: int, y0: int, x1: int, y1: int, c: int) -> Area:
    """Draw a single-pixel line from ``(x0, y0)`` to ``(x1, y1)``.

    Use this for outlines, rulers, charts, and small UI connectors where a solid
    stroke is more appropriate than a filled shape.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x0 (int): X-coordinate of the start of the line.
        y0 (int): Y-coordinate of the start of the line.
        x1 (int): X-coordinate of the end of the line.
        y1 (int): Y-coordinate of the end of the line.
        c (int): Color.

    Returns:
        Area: The bounding box of the line.
    """

def pixel(canvas, x: int, y: int, c: int) -> Area:
    """Draw a single pixel at the specified x, y location.  Uses the canvas's pixel method if available,
    otherwise writes directly to the buffer.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x (int): X-coordinate of the pixel.
        y (int): Y-coordinate of the pixel.
        c (int): color.

    Returns:
        (Area): The bounding box of the pixel.
    """

def poly(canvas, x: int, y: int, coords: list, c: int, f: bool = False) -> Area:
    """Given a list of coordinates, draw an arbitrary (convex or concave) closed polygon at the given x, y location
    using the given color.

    The coords must be specified as an array of integers, e.g. array('h', [x0, y0, x1, y1, ... xn, yn]) or a
    list or tuple of points, e.g. [(x0, y0), (x1, y1), ... (xn, yn)].

    The optional f parameter can be set to True to fill the polygon. Otherwise, just a one-pixel outline is drawn.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x (int): X-coordinate of the polygon's position.
        y (int): Y-coordinate of the polygon's position.
        coords (list): List of coordinates.
        c (int): color.
        f (bool): Fill the polygon (default: False).

    Returns:
        (Area): The bounding box of the polygon.
    """

def polygon(canvas, points: list, x: int, y: int, color: int, angle: float = 0, center_x: int = 0, center_y: int = 0) -> Area:
    """Draw a polygon on the canvas.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        points (list): List of points to draw.
        x (int): X-coordinate of the polygon's position.
        y (int): Y-coordinate of the polygon's position.
        color (int): color.
        angle (float): Rotation angle in radians (default: 0).
        center_x (int): X-coordinate of the rotation center (default: 0).
        center_y (int): Y-coordinate of the rotation center (default: 0).

    Raises:
        ValueError: If the polygon has less than 3 points.

    Returns:
        (Area): The bounding box of the polygon.
    """

def rect(canvas, x0: int, y0: int, w: int, h: int, c: int, f: bool = False) -> Area:
    """Rectangle drawing function.  Will draw a single pixel wide rectangle starting at
    x0, y0 and extending w, h pixels.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x0 (int): X-coordinate of the top-left corner of the rectangle.
        y0 (int): Y-coordinate of the top-left corner of the rectangle.
        w (int): Width of the rectangle.
        h (int): Height of the rectangle.
        c (int): color.
        f (bool): Fill the rectangle (default: False).

    Returns:
        (Area): The bounding box of the rectangle.
    """

def round_rect(canvas, x0: int, y0: int, w: int, h: int, r: int, c: int, f: bool = False) -> Area:
    """Rounded rectangle drawing function.  Will draw a single pixel wide rounded rectangle starting at
    x0, y0 and extending w, h pixels with the specified radius.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x0 (int): X-coordinate of the top-left corner of the rectangle.
        y0 (int): Y-coordinate of the top-left corner of the rectangle.
        w (int): Width of the rectangle.
        h (int): Height of the rectangle.
        r (int): Radius of the corners.
        c (int): color.
        f (bool): Fill the rectangle (default: False).

    Returns:
        (Area): The bounding box of the rectangle.
    """

def triangle(canvas, x0: int, y0: int, x1: int, y1: int, x2: int, y2: int, c: int, f: bool = False) -> Area:
    """Triangle drawing function.  Draws a single pixel wide triangle with vertices at
    (x0, y0), (x1, y1), and (x2, y2).

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x0 (int): X-coordinate of the first vertex.
        y0 (int): Y-coordinate of the first vertex.
        x1 (int): X-coordinate of the second vertex.
        y1 (int): Y-coordinate of the second vertex.
        x2 (int): X-coordinate of the third vertex.
        y2 (int): Y-coordinate of the third vertex.
        c (int): color.
        f (bool): Fill the triangle (default: False).

    Returns:
        (Area): The bounding box of the triangle.
    """

def vline(canvas, x0: int, y0: int, h: int, c: int) -> Area:
    """Horizontal line drawing function.  Will draw a single pixel wide line.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        x0 (int): X-coordinate of the start of the line.
        y0 (int): Y-coordinate of the start of the line.
        h (int): Height of the line.
        c (int): color.

    Returns:
        (Area): The bounding box of the line.
    """

def text(*args, height: int = 8, **kwargs) -> Area:
    """Selector to call the correct text function based on the height of the font.
    See text8, text14, and text16 for more information.

    Args:
        height (int): The height of the font to use.  Default is 8.
    """

def text8(canvas, s: str, x: int, y: int, c: int = 1, scale: int = 1, inverted: bool = False, font_data=None) -> Area:
    """Draw a single line of text with the built-in 8-pixel font.

    This helper suits labels, status text, and scrolling captions. The text is written into the given canvas at
    ``(x, y)`` and returns the region that was updated so that it can be used
    as a dirty rectangle.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        s (str): The text to draw.
        x (int): The x position to start drawing the text.
        y (int): The y position to start drawing the text.
        c (int): The color to draw the text in. Default is ``1``.
        scale (int): The scale factor to draw the text at. Default is ``1``.
        inverted (bool): If ``True``, draw the text inverted. Default is ``False``.
        font_data (str | bytearray): Path to a font file or memoryview. Default is ``None``.

    Returns:
        Area: The area that was drawn to.
    """

def text14(canvas, s: str, x: int, y: int, c: int = 1, scale: int = 1, inverted: bool = False, font_data=None) -> Area:
    """Place text on the canvas with a 14 pixel high font.
    Breaks on ``\\n`` to next line.  Does not break on line going off canvas.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        s (str): The text to draw.
        x (int): The x position to start drawing the text.
        y (int): The y position to start drawing the text.
        c (int): The color to draw the text in.  Default is 1.
        scale (int): The scale factor to draw the text at.  Default is 1.
        inverted (bool): If True, draw the text inverted.  Default is False.
        font_data (str | bytearray): The path to the font .bin file or memoryview.  Default is None.

    Returns:
        Area: The area that was drawn to.
    """

def text16(canvas, s: str, x: int, y: int, c: int = 1, scale: int = 1, inverted: bool = False, font_data=None) -> Area:
    """Place text on the canvas with a 16 pixel high font.
    Breaks on ``\\n`` to next line.  Does not break on line going off canvas.

    Args:
        canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
        s (str): The text to draw.
        x (int): The x position to start drawing the text.
        y (int): The y position to start drawing the text.
        c (int): The color to draw the text in.  Default is 1.
        scale (int): The scale factor to draw the text at.  Default is 1.
        inverted (bool): If True, draw the text inverted.  Default is False.
        font_data (str | bytearray): The path to the font .bin file or memoryview.  Default is None.

    Returns:
        Area: The area that was drawn to.
    """

class Font:
    """Load a bundled romfont and reuse it for multiple text draws.

    `Font` is useful when the same UI needs to draw several labels, scores, or
    status strings with the same glyph set. It can load either an embedded font
    or a custom ``.bin`` file from disk or from memory.

    Args:
        font_data (str | bytearray): Path to a font file or memoryview. Default is ``None``.
        height (int): The height of the font. Default is ``None``.
        cached (bool): If ``True`` (default), read the font into memory on init.
            If ``False``, read it from disk each time it is needed.
    """

    font_name: str
    """What the font is called: ``"default"``, the file's base name, or ``"memoryview"``."""

    def __init__(self, font_data: str | memoryview | bytes | None = None, height: int | None = None, cached: bool = True) -> None:
        """Load a romfont from a path, ``memoryview``, or embedded default.

        Binary font layout: 256 glyphs in ASCII order, one byte per pixel row
        per glyph (fonts up to 8 pixels wide). If ``height`` is omitted and
        ``font_data`` is a path like ``font_8x14.bin``, height is taken from the
        name; for a ``memoryview``, height is ``len(data) // 256``.

        Args:
            font_data (str | memoryview): Path to a ``.bin`` font file, or a
                ``memoryview`` of glyph bytes. Default uses the embedded font
                for ``height`` (or 8×8).
            height (int): Glyph height in pixels. Overrides height inferred from
                the file name when both are set.
            cached (bool): If True (default), read the whole file into memory.
                If False, seek the open file for each glyph row.

        Raises:
            FileNotFoundError: If ``font_data`` is a path that cannot be opened.
            RuntimeError: If the file size does not match the expected font size.
        """

    @property
    def width(self) -> int:
        """Return the width of the font in pixels."""

    @property
    def height(self) -> int:
        """Return the height of the font in pixels."""

    def deinit(self) -> None:
        """Close the font file as cleanup."""

    def __enter__(self) -> Font:
        """Open the font for a ``with`` block.

        Only the pure-Python package has this.
        """

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        """Close the font at the end of a ``with`` block.

        Only the pure-Python package has this.
        """

    def draw_char(self, char: str, x: int, y: int, canvas, color: int, scale: int = 1, inverted: bool = False) -> Area:
        """Draw one character at position (x,y).

        Args:
            char (str): The character to draw.
            x (int): The x position to draw the character.
            y (int): The y position to draw the character.
            canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
            color (int): The color to draw the character in.
            scale (int): The scale factor to draw the character at.  Default is 1.
            inverted (bool): If True, draw the character inverted.  Default is False.

        Returns:
            (Area): The area that was drawn to.
        """

    def text(self, canvas, string: str, x: int, y: int, color: int, scale: int = 1, inverted: bool = False) -> Area:
        """Draw text to the canvas.

        Args:
            canvas (FrameBuffer): The surface to draw on; any object with the same drawing methods works.
            string (str): The text to draw.
            x (int): The x position to start drawing the text.
            y (int): The y position to start drawing the text.
            color (int): The color to draw the text in.
            scale (int): The scale factor to draw the text at.  Default is 1.
            inverted (bool): If True, draw the text inverted.  Default is False.

        Returns:
            (Area): The area that was drawn to.
        """

    def text_width(self, text: str, scale: int = 1) -> int:
        """Return the pixel width of the specified text message.
        Takes into account the scale factor, but not any newlines.

        Args:
            text (str): The text to measure.
            scale (int): The scale factor to measure the text at.  Default is 1.

        Returns:
            int: Width in pixels.
        """

    def export(self, filename: str) -> None:
        """Export the font data in self._cache to a .py file that can be imported.
        The format is a single bytes object named _FONT.  There are 256 lines, one for each character.
        The last line is `FONT = memoryview(_FONT)`.

        Args:
            filename (str): The path to save the file to.
        """

class Draw:
    """Draw shapes on a canvas (display, FrameBuffer, or compatible object).

    Each method delegates to ``pygraphics._shapes`` and returns an ``Area`` bounding box.

    Args:
        canvas: Object with framebuf-compatible drawing methods.

    Example::

        draw = Draw(display)
        draw.fill(0x0000)
        draw.rect(10, 10, 100, 100, 0xFFFF)

        with draw.clip(5, 5, 50, 30):
            draw.fill_rect(0, 0, 200, 200, 0xF800)  # clipped to the 50x30 region
    """

    canvas: Any
    """The canvas this object draws on."""

    def __init__(self, canvas: Any) -> None:
        """Attach drawing helpers to ``canvas``.

        Args:
            canvas: Object with framebuf-compatible drawing methods (e.g.
                `FrameBuffer <pygraphics.FrameBuffer>` or a display driver).
        """

    def clip(self, x: int, y: int | None = None, w: int | None = None, h: int | None = None) -> ClipContext:
        """Return a context manager that clips drawing to a rectangle.

        Accepts ``clip(x, y, w, h)`` or ``clip(Area(...))``. Nested clips intersect.
        """

    def arc(self, x: int, y: int, r: int, a0: float, a1: float, c: int) -> Area:
        """Draw an arc. Returns Area bounds."""

    def blit(self, source, x: int, y: int, key: int = -1, palette: Any = None) -> Area:
        """Blit a source buffer. Returns Area bounds."""

    def blit_rect(self, buf, x: int, y: int, w: int, h: int) -> Area:
        """Blit a raw rectangle buffer. Returns Area bounds."""

    def blit_transparent(self, buf, x: int, y: int, w: int, h: int, key: int | None = None) -> Area:
        """Blit with transparency. Returns Area bounds."""

    def circle(self, x: int, y: int, r: int, c: int, f: bool = False) -> Area:
        """Draw a circle. Returns Area bounds."""

    def ellipse(self, x: int, y: int, r1: int, r2: int, c: int, f: bool = False, m: int = 15, w: int | None = None, h: int | None = None) -> Area:
        """Draw an ellipse. Returns Area bounds."""

    def fill(self, c: int) -> Area:
        """Fill the canvas. Returns Area bounds."""

    def fill_rect(self, x: int, y: int, w: int, h: int, c: int) -> Area:
        """Fill a rectangle. Returns Area bounds."""

    def gradient_rect(self, x: int, y: int, w: int, h: int, c1: int, c2: int | None = None, vertical: bool = True) -> Area:
        """Fill a rectangle with a gradient. Returns Area bounds."""

    def hline(self, x: int, y: int, w: int, c: int) -> Area:
        """Draw a horizontal line. Returns Area bounds."""

    def line(self, x1: int, y1: int, x2: int, y2: int, c: int) -> Area:
        """Draw a line. Returns Area bounds."""

    def pixel(self, x: int, y: int, c: int) -> Area:
        """Draw a pixel. Returns Area bounds."""

    def poly(self, x: int, y: int, coords: list[int] | tuple[int, ...], c: int, f: bool = False) -> Area:
        """Draw a polygon from flat coordinates. Returns Area bounds."""

    def polygon(self, points: list[tuple[int, int]], x: int, y: int, c: int, angle: int = 0, center_x: int = 0, center_y: int = 0) -> Area:
        """Draw a polygon from point list. Returns Area bounds."""

    def rect(self, x: int, y: int, w: int, h: int, c: int, f: bool = False) -> Area:
        """Draw a rectangle. Returns Area bounds."""

    def round_rect(self, x: int, y: int, w: int, h: int, r: int, c: int, f: bool = False) -> Area:
        """Draw a rounded rectangle. Returns Area bounds."""

    def triangle(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, c: int, f: bool = False) -> Area:
        """Draw a triangle. Returns Area bounds."""

    def vline(self, x: int, y: int, h: int, c: int) -> Area:
        """Draw a vertical line. Returns Area bounds."""

    def text(self, *args, **kwargs) -> Area:
        """Draw text using height from kwargs. Returns Area bounds."""

    def text8(self, *args, **kwargs) -> Area:
        """Draw 8px-high text. Returns Area bounds."""

    def text14(self, *args, **kwargs) -> Area:
        """Draw 14px-high text. Returns Area bounds."""

    def text16(self, *args, **kwargs) -> Area:
        """Draw 16px-high text. Returns Area bounds."""

class ClippedCanvas:
    """Proxy that restricts drawing on ``canvas`` to ``clip``.

    Drawing methods that intersect the clip region are forwarded to the
    underlying canvas; pixels outside the clip are ignored. Unknown attributes
    fall through to ``canvas`` via ``__getattr__``.
    """

    def __init__(self, canvas, clip: Area) -> None:
        """Wrap ``canvas`` so drawing is limited to ``clip``.

        Args:
            canvas: Framebuf-compatible draw target.
            clip (Area): Inclusive rectangle in canvas coordinates.
        """

    @property
    def width(self) -> int:
        """Underlying canvas width in pixels."""

    @property
    def height(self) -> int:
        """Underlying canvas height in pixels."""

    def pixel(self, x: int, y: int, c: int | None = None) -> Area | int:
        """Get or set a pixel if ``(x, y)`` is inside the clip.

        Args:
            x: X coordinate.
            y: Y coordinate.
            c: Color to set. If ``None``, read the existing pixel color.

        Returns:
            On set: ``Area`` of the pixel, or ``None`` if outside the clip.
            On get: pixel color, or ``None`` if outside the clip.
        """

    def fill(self, c: int) -> Area:
        """Fill the entire clip rectangle with color ``c``.

        Args:
            c: Fill color.

        Returns:
            ``Area`` of the filled clip, or ``None`` if empty.
        """

    def fill_rect(self, x: int, y: int, w: int, h: int, c: int) -> Area:
        """Fill the intersection of the given rectangle with the clip.

        Args:
            x: Left edge.
            y: Top edge.
            w: Width.
            h: Height.
            c: Fill color.

        Returns:
            Clipped ``Area`` that was filled, or ``None`` if no overlap.
        """

    def hline(self, x: int, y: int, w: int, c: int) -> Area:
        """Draw a horizontal line clipped to this region.

        Args:
            x: Start x.
            y: Y coordinate.
            w: Width in pixels.
            c: Color.

        Returns:
            Clipped ``Area``, or ``None`` if no overlap.
        """

    def vline(self, x: int, y: int, h: int, c: int) -> Area:
        """Draw a vertical line clipped to this region.

        Args:
            x: X coordinate.
            y: Start y.
            h: Height in pixels.
            c: Color.

        Returns:
            Clipped ``Area``, or ``None`` if no overlap.
        """

    def blit_rect(self, buf, x: int, y: int, w: int, h: int) -> Area:
        """Blit a packed buffer, cropping to the clip region.

        Args:
            buf: Source bytes for a ``w`` x ``h`` rectangle (canvas bpp).
            x: Destination x.
            y: Destination y.
            w: Source width.
            h: Source height.

        Returns:
            Clipped destination ``Area``, or ``None`` if no overlap.
        """

    def blit_transparent(self, buf, x: int, y: int, w: int, h: int, key: int) -> Area:
        """Blit a packed buffer with transparency, cropped to the clip.

        Args:
            buf: Source bytes for a ``w`` x ``h`` rectangle (canvas bpp).
            x: Destination x.
            y: Destination y.
            w: Source width.
            h: Source height.
            key: Transparent color key.

        Returns:
            Clipped destination ``Area``, or ``None`` if no overlap.
        """

    def text(self, s: str, x: int, y: int, c: int = 1, scale: int = 1, inverted: bool = False, font_data=None, height=8) -> Area:
        """Draw romfont text clipped to this region.

        Glyphs are rendered via `fill_rect` on ``self``, so pixels
        outside the clip are discarded (unlike falling through to the
        underlying canvas ``text``, which draws unclipped).

        Args:
            s: Text to draw.
            x: Left edge.
            y: Top edge.
            c: Foreground color.
            scale: Glyph scale factor.
            inverted: Mirror glyphs when True.
            font_data: Optional romfont bytes / path.
            height: Romfont height (8, 14, or 16).

        Returns:
            Unclipped text ``Area`` (same contract as ``FrameBuffer.text``).
        """

    def text8(self, s: str, x: int, y: int, c: int = 1, scale: int = 1, inverted: bool = False, font_data=None) -> Area:
        """Draw 8px-high romfont text clipped to this region."""

    def text14(self, s: str, x: int, y: int, c: int = 1, scale: int = 1, inverted: bool = False, font_data=None) -> Area:
        """Draw 14px-high romfont text clipped to this region."""

    def text16(self, s: str, x: int, y: int, c: int = 1, scale: int = 1, inverted: bool = False, font_data=None) -> Area:
        """Draw 16px-high romfont text clipped to this region."""

class ClipContext:
    """Context manager that pushes a clip rectangle onto a `Draw` stack.

    Entering returns the effective (intersected) clip ``Area``. Nested
    ``with draw.clip(...)`` blocks intersect.
    """

    def __init__(self, draw, area: Area) -> None:
        """Bind this context to ``draw`` and the clip ``area``.

        Args:
            draw (Draw): Draw instance whose clip stack is updated.
            area (Area): Clip rectangle to push on enter.
        """

    def __enter__(self) -> ClipContext:
        """Push the clip and return the effective clip ``Area``."""

    def __exit__(self, exc_type, exc, tb) -> None:
        """Pop the clip rectangle from the draw stack."""

class BMP565:
    """Read a 16-bit RGB565 BMP as a sliceable, optionally streamed asset.

    Provide either ``filename`` (path to a BMP file) or ``source`` (an in-memory
    RGB565 buffer with ``width`` and ``height``).
    """

    width: int
    """Image width in pixels."""
    height: int
    """Image height in pixels."""
    bpp: int
    """Bits per pixel: 16."""
    BPP: int
    """Bytes per pixel: 2."""

    def __init__(self, filename: str | None = None, source: bytearray | memoryview | None = None, streamed: bool = False, mirrored: bool = False, width: int | None = None, height: int | None = None) -> None:
        """Load from a file path or an existing RGB565 buffer.

        Args:
            filename: Path to an RGB565 BMP file. Mutually exclusive with ``source``.
            source: Existing RGB565 pixel buffer. Requires ``width`` and ``height``.
            streamed: If True with ``filename``, keep the file open and read rows
                on demand instead of loading the full image into memory.
            mirrored: When streaming, reverse each row read (rarely needed).
            width: Pixel width when constructing from ``source``.
            height: Pixel height when constructing from ``source``.

        Raises:
            ValueError: If neither ``filename`` nor ``source`` is given, or the
                file is not a valid RGB565 BMP.
        """

    def __call__(self, x: int, y: int, w: int, h: int) -> bytes | bytearray | memoryview:
        """Return the RGB565 bytes for the rectangle at ``(x, y)`` size ``w`` × ``h``.

        Equivalent to ``self[x : x + w, y : y + h]``.

        Args:
            x: Left edge in pixels.
            y: Top edge in pixels.
            w: Width in pixels.
            h: Height in pixels.

        Returns:
            Raw RGB565 bytes for the requested region.
        """

    @property
    def buffer(self) -> memoryview | None:
        """Writable ``memoryview`` of the full RGB565 pixel buffer, or ``None`` if streamed."""

    def save(self, filename: str | None = None) -> str:
        """Write this image as an RGB565 BMP file.

        If ``filename`` already exists, a numeric suffix is appended
        (``image.bmp`` → ``image_1.bmp``, etc.).

        Args:
            filename: Output path. Defaults to the source filename or ``image.bmp``.

        Returns:
            The path actually written.
        """

    def __getitem__(self, key: int | slice | tuple[int | slice, int | slice]) -> int | bytes | bytearray | memoryview:
        """Index or slice pixel data.

        Args:
            key: One of:

                * ``(x, y)`` — single pixel as an ``int`` (RGB565)
                * ``(x_slice, y_slice)`` — rectangular region as ``bytearray``
                * ``int`` — flat pixel index as an ``int``
                * ``slice`` — full-width row range as ``bytearray``

        Returns:
            Pixel value(s) for the requested key.

        Raises:
            ValueError: If ``key`` is not a supported index form.
        """

    def deinit(self) -> None:
        """Close the open file handle when constructed with ``streamed=True``."""

    def __exit__(self, exception_type, exception_value, traceback) -> None:
        """Close the image at the end of a ``with`` block, as `deinit` does.

        Only the pure-Python package has this.
        """

def load_image(filename: str) -> FrameBuffer:
    """Load a ``FrameBuffer`` from a PBM, PGM, or RGB565 BMP file."""

def save_image(fb: FrameBuffer, filename: str | None = None) -> str:
    """Save a ``FrameBuffer`` to PBM, PGM, BMP, or PNG based on format or filename.

    MONO_HLSB → PBM, GS2/GS4/GS8 → PGM, RGB565 → BMP (or PNG if filename ends in .png),
    RGB888 → PNG. Other formats raise ``ValueError``.
    """

def pbm_to_framebuffer(filename: str) -> FrameBuffer:
    """Convert a PBM file to a MONO_HLSB FrameBuffer.

    Allocates one pixel buffer and reads pixels with ``readinto`` (peak ~1x).

    Args:
        filename (str): Filename of the PBM file

    Returns:
        FrameBuffer: Loaded monochrome framebuffer.
    """

def pgm_to_framebuffer(filename: str) -> FrameBuffer:
    """Convert a PGM file to a GS2_HMSB, GS4_HMSB or GS8 FrameBuffer.

    Allocates one pixel buffer and reads pixels with ``readinto`` (peak ~1x).

    Args:
        filename (str): Filename of the PGM file

    Returns:
        FrameBuffer: Loaded greyscale framebuffer (format from max value).
    """

def bmp_to_framebuffer(filename: str) -> FrameBuffer:
    """Convert an RGB565 BMP file to a FrameBuffer.

    Args:
        filename (str): Path to the BMP file.

    Returns:
        FrameBuffer: Loaded RGB565 framebuffer.
    """

def export_framebuffer(fb: FrameBuffer, filename: str) -> str:
    """Export a ``FrameBuffer`` as an importable ``.py`` bitmap module.

    Only the pure-Python package has this.

    Format::

        WIDTH = …
        HEIGHT = …
        FORMAT = …
        BITMAP = bytearray(
        b'…'\
        b'…'
        )

    ``BITMAP`` is a writable ``bytearray`` so MicroPython can wrap it in a
    ``FrameBuffer`` without copying. Prefer `FrameBuffer.from_bitmap` to
    load. Differs from `Font.export`, which keeps a read-only
    ``memoryview`` for glyph indexing.
    """

def implementation() -> str:
    """Say which package this is: ``"native_cmod"`` for the compiled module, ``"pygraphics_python"`` for the pure-Python one."""
