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

**Both implementations pass.** Pure Python runs 98 tests (3 native-only parity
probes skipped); the native build runs 85 (2 skipped — `test_clip` and
`test_blit_hooks` import pure-Python-only submodules, and a native build is one
extension module, not a package).

CI runs both, so a divergence between them fails the build. Eleven such
divergences existed as of August 2026 and were invisible because the suite could
not run; see the Phase 10 notes in the consolidation plan.
