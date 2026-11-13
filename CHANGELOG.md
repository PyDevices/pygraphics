## v0.1.3 (2026-11-13)

- blit_rect: pure Python clips to the canvas like the compiled module (#74)

## v0.1.3.dev1 (2026-11-13)

- FrameBuffer: blit_alpha tints a colour through an 8-bit alpha mask (#71)
- CI: build the MicroPython module test on v1.29.0 (#70)
- Type stub: Area equality takes any object, and CI runs mypy on the stub (#68)
- pygraphics: a type stub for editors, and a Reference section built from it (#67)
- Docs: Raspberry Pi 5 should take the aarch64 wheel; reports welcome (#66)

## v0.1.3.dev0 (2026-11-07)

- Wheels for Linux on ARM64, such as 64-bit Raspberry Pi OS (#64)
- Style check: fail a pull request on the mechanical style rules (#63)
- LICENSE: copyright Brad Barnett, as the file headers say (#62)
- Docstrings: Google sections and cross-references; licence headers on every file (#61)
- Roadmap: the native-module kit's remaining pieces (#60)
- AGENTS.md: say how examples are written (#59)

## v0.1.2 (2026-10-29)


## v0.1.2rc1 (2026-10-29)

- Point at PyDevices/gallery (#56)
- Examples: graphics, framebuffer, font, PBM and BMP examples (#55)
- Shorten AGENTS.md to tips; move the docs guidance into CONTRIBUTING (#54)
- Docs: link the repo paths the prose names (#53)
- Ignore site/, the mkdocs build output (#52)
- Docs: restructure to Get started, Guides, Reference, How it works (#51)
- Docs: Sphinx on the shared pydevices-docs package, in place of MkDocs (#45)
- Pure package: save, export and from_file work on MicroPython (#50)
- README: TestPyPI's current release is 0.1.1 (#49)
- Adopt publishing-v17: the empty macOS wheel cell uploads nothing instead of failing (#48)
- Adopt publishing-v16: the macOS wheel cell builds nothing instead of failing (#47)

## v0.1.1 (2026-10-22)

- Adopt publishing-v15: a release also asks the library index to rebuild (#44)
- CircuitPython builds pygraphics as a user C module only (#43)

## v0.1.0 (2026-10-08)

- Build as a user C module in CircuitPython too (#41)
- Add ROADMAP.md for planned work (#40)
- Release PRs from publishing-v13: the description says what the PR changes and what merging does

## v0.0.42rc1 (2026-10-07)

- PNG saves go through pngio; remove pygraphics' own encoder (#38)

## v0.0.41 (2026-10-06)

- encode_png: RGB565 framebuffer to PNG (#36)

## v0.0.40 (2026-09-27)

- blit: accept MicroPython's tuple source in the bounding box (#34)

## v0.0.39 (2026-09-24)

- README: add this module to your own MicroPython build with one include() line (#32)
- Docs: current releases are on TestPyPI; PyPI holds an older release parked to reserve the name (#31)
- docs: add pygraphics newcomer guide (#30)
- Docs: build with other modules through manifests and apply scripts, not cmods
- CircuitPython: compile the build stamp there too (#29)
- manifest: name this repo's C module with c_module() (MicroPython 1.29)
- Every pygraphics build says which pygraphics it is (#28)
- Cold-eyes #23: record the four pure-only entry points, tier the platform claims, and put MicroPython in CI
- Drop Python 3.10
- Remove the Documentation placeholder: it cannot release the orphan
- Restore the Documentation path to release the orphaned queued run
- --dry-run now checks the anchors it claims it would insert after
- --status exits nonzero when the tree is not in the applied state
- Make tests/_env.py and the parity tool importable on MicroPython
- Describe the aggregator workspace by role, not by repo name
- ci: bump the actions group across 1 directory with 2 updates (#19)
- docs theme: the header bar takes a deeper cyan
- docs theme: the Instrument palette
- docs theme: extra.css is now synced from dotgithub
- docs theme: drop the dead .color-swatch rule
- docs(theme): consolidate every color into the token blocks

## v0.0.38 (2026-08-29)


## v0.0.38.dev1 (2026-08-29)

- Adopt publishing-v6 (MIP second-publication race fix)
- Fix stale and broken claims in README and installation docs
- Grant publishing-v5's permission ceiling (assets + OIDC)
- Adopt publishing-v5 and release-PR automation (Phase 1 batch 1)
- Use direct WebAssembly host for documentation demos
