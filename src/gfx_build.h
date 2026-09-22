// Which pygraphics a firmware was built from, readable on the device.
//
// pygraphics#25, following audiodsp's 04e9578. `os.uname().version` answers for
// MicroPython and says nothing about the user C modules compiled into the
// image, so when a rendering moves between two firmwares there is no way to ask
// the board which pygraphics produced it. On audiodsp that was not hypothetical:
// a firmware had been built from a throwaway source tree during a pin move and
// the commit was not recoverable from the working tree or from the .bin files
// left on disk, by any means. Hence: computed at build time, never stored.
//
// The two strings are defined ONCE (gfx_build.c) and the module table points at
// them, so the cost is two `mp_obj_str_t` plus two table entries.
//
// NOT in the sources the CPython extension compiles: `mp_obj_str_t` is a
// MicroPython type. The CPython target answers the same question from
// gfx_module_cpy.c, from the same two macros, computed the same way in
// setup.py -- so `pygraphics.__revision__` reads alike on a board and in the
// wheel.

#pragma once

#include "py/obj.h"
#include "py/objstr.h"  // mp_obj_str_t -- py/obj.h alone does not declare it

extern const mp_obj_str_t pygraphics_version_obj;
extern const mp_obj_str_t pygraphics_revision_obj;

// One line inside the module's existing globals table.
#define PYGRAPHICS_BUILD_GLOBALS \
    { MP_ROM_QSTR(MP_QSTR___version__), MP_ROM_PTR(&pygraphics_version_obj) }, \
    { MP_ROM_QSTR(MP_QSTR___revision__), MP_ROM_PTR(&pygraphics_revision_obj) }
