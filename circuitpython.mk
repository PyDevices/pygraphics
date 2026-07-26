# CircuitPython build glue for pygraphics (unix coverage).
PYGRAPHICS_MOD_DIR ?= $(patsubst %/,%,$(dir $(lastword $(MAKEFILE_LIST))))

CFLAGS += -I$(PYGRAPHICS_MOD_DIR)/src -DCIRCUITPY_PYGRAPHICS=1
QSTR_DEFS += $(PYGRAPHICS_MOD_DIR)/src/pygraphics_qstrdefs.h

GRAPHICS_SOURCES := \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_module_mp.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_bindings_mp.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_canvas_mp.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_framebuffer.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_shapes.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_draw.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_font.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_bmp565.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_files.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_capabilities.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_area_mp.c

GRAPHICS_SUPPRESS_CFLAGS := -Wno-unused-function -Wno-sign-compare
$(foreach _gfx,$(GRAPHICS_SOURCES),$(eval $(BUILD)/$(_gfx:.c=.o): CFLAGS += $(GRAPHICS_SUPPRESS_CFLAGS)))

SRC_C += $(GRAPHICS_SOURCES)
