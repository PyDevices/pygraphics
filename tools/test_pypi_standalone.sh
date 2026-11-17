#!/usr/bin/env bash
# Verify the omnipython-pygraphics PyPI wheel in an isolated environment.

set -euo pipefail

VENV="${PYPI_PYGRAPHICS_VENV:-/tmp/pygraphics-pypi-standalone}"

if [[ $# -gt 0 ]]; then
    echo "Usage: ./tools/test_pypi_standalone.sh" >&2
    exit 2
fi

if [[ -z "$VENV" || "$VENV" == "/" || "$VENV" == "$HOME" ]]; then
    echo "Refusing unsafe venv path: $VENV" >&2
    exit 2
fi

rm -rf "$VENV"
python3 -m venv "$VENV"
"$VENV/bin/pip" install -q -U pip
"$VENV/bin/pip" install omnipython-pygraphics

"$VENV/bin/pip" freeze | sort
"$VENV/bin/python" -c \
    "import pygraphics; print('pygraphics', pygraphics.implementation())"

echo "Standalone omnipython-pygraphics PyPI smoke test passed."
