# Examples

Small programs that show pygraphics drawing on a display. Each one says in
its docstring what it needs and where it has been run. Run them from the
repository's root, so the ones that load a picture or a font find it in
[assets/](assets/).

| Example | What it shows |
|---|---|
| [graphics_simpletest.py](graphics_simpletest.py) | Shapes and text drawn straight on the display |
| [framebuf_simpletest.py](framebuf_simpletest.py) | The same shapes drawn into a FrameBuffer, then copied on |
| [pygraphics_landscape.py](pygraphics_landscape.py) | A landscape drawn in bands, scaled to any display |
| [rotations.py](rotations.py) | The display turned through its four rotations |
| [font_list.py](font_list.py) | Every bitmap font in a folder |
| [pbm_simpletest.py](pbm_simpletest.py) | A one-bit PBM picture shown in colour |
| [pbm_create_new.py](pbm_create_new.py) | A one-bit logo drawn, then shown in colour |
| [bmp565_simpletest.py](bmp565_simpletest.py) | A whole BMP picture loaded and shown |
| [bmp565_sprite.py](bmp565_sprite.py) | A sprite walking, read from a sprite sheet |
| [bmp565_scroll.py](bmp565_scroll.py) | A tall picture scrolled a line at a time |
| [bmp565_scroll_sprite.py](bmp565_scroll_sprite.py) | A runner on a scrolling street, played by touch |

Full apps that use pygraphics are in
[pydevices-examples](https://github.com/PyDevices/pydevices-examples).
