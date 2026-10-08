# MicroPython user C module glue for pygraphics.
#
# Discovered via USER_C_MODULES pointing at the workspace directory that
# contains this repo (its parent), e.g. `make USER_C_MODULES=../../..`.

PYGRAPHICS_MOD_DIR := $(USERMOD_DIR)

# PYGRAPHICS_USER_C_MODULE tells the C that it was built through USER_C_MODULES,
# which CircuitPython builds also honour. Its unix port sets CIRCUITPY=1, and
# without this the module would skip MP_REGISTER_MODULE and never be importable.
CFLAGS_USERMOD += -DPYGRAPHICS_USER_C_MODULE=1 -I$(PYGRAPHICS_MOD_DIR)/src -Wno-unused-function -Wno-sign-compare -Wno-unused-const-variable
# Arc/polygon use Q15 LUT in gfx_trig.h — no libm required.

# --- which pygraphics this firmware was built from --------------------------
#
# pygraphics#25. `os.uname().version` answers for MicroPython and says nothing
# about the user C modules in the image, so a rendering that moves between two
# firmwares cannot be attributed. Computed HERE, from the directory the build
# is actually reading, because that is the only thing that knows which tree it
# compiled -- audiodsp lost a revision exactly this way, to a throwaway source
# tree during a pin move.
#
# `--always --dirty` so a tree with uncommitted changes says so: dirty is the
# normal state in this workspace and a bare hash would claim more than it knows.
# Both fall back to "unknown" rather than guessing -- see src/gfx_build.c.
PYGRAPHICS_VERSION := $(shell cat $(PYGRAPHICS_MOD_DIR)/VERSION 2>/dev/null || echo 0.0.0+unknown)
PYGRAPHICS_REVISION := $(shell git -C $(PYGRAPHICS_MOD_DIR) describe --always --dirty --abbrev=7 2>/dev/null || echo unknown)
CFLAGS_USERMOD += -DPYGRAPHICS_VERSION='"$(PYGRAPHICS_VERSION)"'
CFLAGS_USERMOD += -DPYGRAPHICS_REVISION='"$(PYGRAPHICS_REVISION)"'

SRC_USERMOD_C += \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_build.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_module_mp.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_bindings_mp.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_canvas_mp.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_framebuffer.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_shapes.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_draw.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_font.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_bmp565.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_files.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_png.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_capabilities.c \
    $(PYGRAPHICS_MOD_DIR)/src/gfx_area_mp.c

# Warnings the drawing code trips on purpose: comparing an angle against an
# exact 0.0f to skip rotation, mixed-sign loop bounds, tables only some builds
# use. CFLAGS_USERMOD above carries them for MicroPython. They are given again
# per object because CircuitPython's MCU ports append -Wsign-compare and
# -Wfloat-equal (under -Werror) after the user module flags, and the later
# flag wins; a target-specific flag lands last. The object path is the one py/py.mk gives a user module's source since
# MicroPython 1.29: $(BUILD)/<module directory name>/<path inside it>.o.
PYGRAPHICS_OBJ_CFLAGS := -Wno-unused-function -Wno-sign-compare -Wno-unused-const-variable -Wno-float-equal
$(foreach _src,$(filter $(PYGRAPHICS_MOD_DIR)/%,$(SRC_USERMOD_C)),\
    $(eval $(BUILD)/$(notdir $(PYGRAPHICS_MOD_DIR))/$(patsubst $(PYGRAPHICS_MOD_DIR)/%.c,%.o,$(_src)): CFLAGS += $(PYGRAPHICS_OBJ_CFLAGS)))
