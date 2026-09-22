// The two build strings, defined once. See gfx_build.h.
//
// SPDX-License-Identifier: MIT

#include "gfx_build.h"

#include "py/objstr.h"

// Passed by micropython.mk / micropython.cmake. A build that reaches here
// without them says so rather than claiming a revision it does not know --
// "unknown" is the honest answer, and a test asserts it is NOT the answer
// inside a checkout, because a mechanism that reports "unknown" everywhere
// passes every other check.
#ifndef PYGRAPHICS_VERSION
#define PYGRAPHICS_VERSION "0.0.0+unknown"
#endif
#ifndef PYGRAPHICS_REVISION
#define PYGRAPHICS_REVISION "unknown"
#endif

const MP_DEFINE_STR_OBJ(pygraphics_version_obj, PYGRAPHICS_VERSION);
const MP_DEFINE_STR_OBJ(pygraphics_revision_obj, PYGRAPHICS_REVISION);
