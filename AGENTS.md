# AGENTS.md

- Pure-Python tests need nothing built: `python3 -m unittest discover -s tests`. The compiled module needs `.venv/bin/pip install -e .` first, then `PYGRAPHICS_TEST_NATIVE=1 .venv/bin/python -m unittest discover -s tests` ([CONTRIBUTING.md](CONTRIBUTING.md#run-the-tests)).
- Once you've built in place, the compiled `pygraphics.*.so` at the repo root wins over `PYTHONPATH=lib`. Run pure-Python checks from another directory, or let `tests/_env.py` handle it.
- `lib/pygraphics` and the C module share one public API. A change to one needs the other, and `tools/compare_graphics_run.py` byte-compares them ([CONTRIBUTING.md](CONTRIBUTING.md#compare-the-two-implementations)).
- Fonts live in `lib/pygraphics/_font_8x*.py`; after editing one, run `python3 scripts/sync_fonts.py` to rewrite the C headers. Don't edit `src/font_8x*.h` by hand.
- On a board, a frozen `pygraphics` wins over `/lib` on MicroPython and CircuitPython, so a copied or mip-installed copy never runs until you rebuild or put `/lib` first. On a source checkout, set `PYTHONPATH` (CPython) or `MICROPYPATH` (MicroPython) to `lib`.
- CircuitPython has no MicroPython-style `framebuf`; `lib/pygraphics/framebuf.py` is the shim.
- Docs build and release steps: [CONTRIBUTING.md](CONTRIBUTING.md#build-the-docs).
