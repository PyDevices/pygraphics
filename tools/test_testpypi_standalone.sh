#!/usr/bin/env bash
# Verify the pydevices-pygraphics TestPyPI wheel in an isolated environment.

set -euo pipefail

TESTPYPI_INDEX="${TESTPYPI_INDEX:-https://test.pypi.org/simple/}"
PYPI_INDEX="${PYPI_INDEX:-https://pypi.org/simple/}"
VENV="${TESTPYPI_PYGRAPHICS_VENV:-/tmp/pygraphics-testpypi-standalone}"

if [[ $# -gt 0 ]]; then
    echo "Usage: ./tools/test_testpypi_standalone.sh" >&2
    exit 2
fi

if [[ -z "$VENV" || "$VENV" == "/" || "$VENV" == "$HOME" ]]; then
    echo "Refusing unsafe venv path: $VENV" >&2
    exit 2
fi

rm -rf "$VENV"
python3 -m venv "$VENV"
"$VENV/bin/pip" install -q -U pip
"$VENV/bin/pip" install \
    --index-url "$TESTPYPI_INDEX" \
    --extra-index-url "$PYPI_INDEX" \
    pydevices-pygraphics

"$VENV/bin/pip" freeze | sort
"$VENV/bin/python" -c \
    "import pygraphics; print('pygraphics', pygraphics.implementation())"

echo "Standalone pydevices-pygraphics TestPyPI smoke test passed."
