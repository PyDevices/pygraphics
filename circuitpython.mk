# CircuitPython build glue for pygraphics (unix coverage).
#
# Prefer caller-set GRAPHICS_MOD_DIR / PYGRAPHICS_MOD_DIR. Do not use a lazy
# ``MAKEFILE_LIST`` default: QSTR_DEFS prerequisites expand late, after other
# makefiles have been parsed, so ``lastword $(MAKEFILE_LIST)`` becomes wrong
# (e.g. ``../../py/src/pygraphics_qstrdefs.h``).
ifndef PYGRAPHICS_MOD_DIR
  ifdef GRAPHICS_MOD_DIR
    PYGRAPHICS_MOD_DIR := $(GRAPHICS_MOD_DIR)
  else
    PYGRAPHICS_MOD_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
  endif
endif

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
