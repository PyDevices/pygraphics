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

