# pygraphics tests

pygraphics ships twice — a pure-Python package under `lib/` and a native C
extension — and the two must behave identically. `_env.py` decides which one the
suite imports, because whichever module imports `pygraphics` first fixes the
choice for the entire process.

```bash
# Pure Python (default). Works in a fresh checkout with nothing built.
python3 -m unittest discover -s tests

# The in-place native build. Requires: python3 setup.py build_ext --inplace
PYGRAPHICS_TEST_NATIVE=1 python3 -m unittest discover -s tests
```

Every test module must `import _env` before importing `pygraphics`.

## Current state

**Pure Python passes** — 98 tests, with 3 native-only parity probes skipped.

**The native build does not.** As of 2026-08-18 it has 11 behavioral divergences
from the pure-Python reference; the suite reports 6 failures and 5 errors. These
are native defects, not test bugs: the same tests pass against the pure-Python
implementation. Two more modules skip under native (`test_clip`,
`test_blit_hooks`) because they import pure-Python-only submodules — a native
build is one extension module, not a package.

CI runs the pure-Python mode only, so it stays green. A native job should be
added once those divergences are closed, or it would fail on every push.
