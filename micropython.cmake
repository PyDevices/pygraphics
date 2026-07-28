# MicroPython CMake glue for pygraphics (ESP32, RP2, …).
#
# Make-based ports use micropython.mk in this directory. CMake-based ports
# (esp32, rp2, …) discover this file via USER_C_MODULES / an aggregator
# micropython.cmake that includes sibling modules.
#
# Point USER_C_MODULES at this repo (or this file) directly, e.g.:
#   idf.py build -DUSER_C_MODULES=<path to pygraphics>
# Or a semicolon-separated list with other modules (no aggregator required):
#   -DUSER_C_MODULES="<path to pygraphics>;<path to displayif>"

set(PYGRAPHICS_MOD_DIR ${CMAKE_CURRENT_LIST_DIR})

add_library(pygraphics INTERFACE)

target_sources(pygraphics INTERFACE
    ${PYGRAPHICS_MOD_DIR}/src/gfx_module_mp.c
    ${PYGRAPHICS_MOD_DIR}/src/gfx_bindings_mp.c
    ${PYGRAPHICS_MOD_DIR}/src/gfx_canvas_mp.c
    ${PYGRAPHICS_MOD_DIR}/src/gfx_framebuffer.c
    ${PYGRAPHICS_MOD_DIR}/src/gfx_shapes.c
    ${PYGRAPHICS_MOD_DIR}/src/gfx_draw.c
    ${PYGRAPHICS_MOD_DIR}/src/gfx_font.c
    ${PYGRAPHICS_MOD_DIR}/src/gfx_bmp565.c
    ${PYGRAPHICS_MOD_DIR}/src/gfx_files.c
    ${PYGRAPHICS_MOD_DIR}/src/gfx_capabilities.c
    ${PYGRAPHICS_MOD_DIR}/src/gfx_area_mp.c
)

target_include_directories(pygraphics INTERFACE ${PYGRAPHICS_MOD_DIR}/src)
target_compile_options(pygraphics INTERFACE
    -Wno-unused-function
    -Wno-sign-compare
    -Wno-unused-const-variable
)

# Arc/polygon use Q15 LUT (gfx_trig.h) — no libm.

target_link_libraries(usermod INTERFACE pygraphics)
