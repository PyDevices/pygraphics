# Sourcey native API reference

Generates a source-linked reference for pygraphics' **native C bindings** from
the public binding tables and headers in `src/`. This covers ground the RTD site
cannot: mkdocstrings reads Python docstrings, so the C symbols are invisible to it.

```bash
python3 scripts/generate_reference.py
```

Output lands in `generated/` and is **not tracked in git**.

## Status: generated, not published

There is no deployment for this today. `sourcey.config.ts` sets
`baseUrl: "/pygraphics/api/"` and the generator stamps
`https://pydevices.github.io/pygraphics/api` into each page, but the `gh-pages`
branch contains only the marketing landing page — that URL has never served
anything.

The output used to be committed. It was untracked in August 2026 because it had
gone stale: the tracked snapshot was pinned to commit `a02baf4` (from before the
org rename to PyDevices), with 11 subsequent commits to `src/`. Generated
artifacts that are committed drift silently; regenerating takes one command.

**If this reference should be published**, the natural home is the existing
ReadTheDocs site rather than a second Pages surface — org policy is that Pages
carries marketing and ReadTheDocs carries library documentation. The generated
pages already use YAML front matter with `title` and `description`, so they
should drop into the MkDocs nav with little work; the generator would need to run
as part of the docs build, which it can, since it parses `src/` from this repo.
