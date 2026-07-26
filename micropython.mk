# MicroPython user C module glue for pygraphics.
#
# Discovered via USER_C_MODULES pointing at the workspace directory that
# contains this repo (its parent), e.g. `make USER_C_MODULES=../../..`.

PYGRAPHICS_MOD_DIR := $(USERMOD_DIR)

CFLAGS_USERMOD += -I$(PYGRAPHICS_MOD_DIR)/src -Wno-unused-function -Wno-sign-compare -Wno-unused-const-variable
# math: cosf/sinf etc.
# - mimxrt/samd: bare `ld` — absolute libm.a in LDFLAGS
# - stm32: CROSS_COMPILE is set *after* py.mk, so $(CC) here is the host
#   compiler; use double trig via bundled libm_dbl instead of newlib libm
# - else: -lm
ifneq ($(findstring /ports/mimxrt,$(CURDIR))$(findstring /ports/samd,$(CURDIR)),)
LDFLAGS_USERMOD += $(shell $(CC) $(CFLAGS) -print-file-name=libm.a)
else ifneq ($(findstring /ports/stm32,$(CURDIR)),)
CFLAGS_USERMOD += -DGFX_USE_DOUBLE_TRIG=1
else
LDFLAGS_USERMOD += -lm
endif

SRC_USERMOD_C += \
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
