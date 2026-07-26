// CircuitPython shared-bindings registration for pygraphics.
#include "shared-bindings/pygraphics/__init__.h"
#include "py/obj.h"
#include "py/runtime.h"

extern const mp_obj_module_t mp_module_pygraphics;

MP_REGISTER_MODULE(MP_QSTR_pygraphics, mp_module_pygraphics);
