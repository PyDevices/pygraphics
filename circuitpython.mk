# CircuitPython build glue for pygraphics (unix coverage and MCU ports).
#
# Prefer caller-set GRAPHICS_MOD_DIR / PYGRAPHICS_MOD_DIR. Do not use a lazy
# ``MAKEFILE_LIST`` default: QSTR_DEFS prerequisites expand late, after other
# makefiles have been parsed, so ``lastword $(MAKEFILE_LIST)`` becomes wrong
# (e.g. ``../../py/src/pygraphics_qstrdefs.h``).
# Include guard: this file is included from both the enable makefile
# (variant on unix, board on MCU ports) and the port Makefile. Without the
# guard SRC_C gets every source twice and the link fails with "multiple
# definition of ..." naming the *same* object file on both sides.
ifndef PYGRAPHICS_MK_INCLUDED
PYGRAPHICS_MK_INCLUDED := 1

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

# -Wno-float-equal: CircuitPython builds with -Werror=float-equal, and the
# shape code compares a caller-supplied angle against exact 0.0f to skip
# rotation. That is a deliberate fast path, not accumulated-float equality.
GRAPHICS_SUPPRESS_CFLAGS := -Wno-unused-function -Wno-sign-compare -Wno-float-equal
$(foreach _gfx,$(GRAPHICS_SOURCES),$(eval $(BUILD)/$(_gfx:.c=.o): CFLAGS += $(GRAPHICS_SUPPRESS_CFLAGS)))

SRC_C += $(GRAPHICS_SOURCES)

endif  # PYGRAPHICS_MK_INCLUDED
