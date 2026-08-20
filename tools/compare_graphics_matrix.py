#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT
"""Cross-interpreter matrix: native ``pygraphics`` vs pure-Python ``pygraphics``.

Run from the pygraphics repo root::

    python tools/compare_graphics_matrix.py
    python tools/compare_graphics_matrix.py --only-interpreter micropython,cpython-venv

For ``cpython-venv`` and ``python.exe``, installs ``pydevices-pygraphics`` from TestPyPI
(first time per interpreter) so ``import pygraphics`` resolves to the native wheel.

Results: summary table on stderr, JSON in the system temp directory.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"
RUN_SCRIPT = TOOLS / "compare_graphics_run.py"


def _temp_dir() -> Path:
    return Path(
        os.environ.get("TEMP")
        or os.environ.get("TMPDIR")
        or os.environ.get("TMP")
        or tempfile.gettempdir()
    )


RESULTS_JSON = _temp_dir() / "compare_graphics_results.json"
RESULT_RE = re.compile(r"^GRAPHICS_COMPARE_RESULT=(.+)$", re.MULTILINE)

# Desktop subprocess interpreters that can load native pygraphics alongside
# staged pure-Python pygraphics. Self-contained (no dependency on pydevices-examples's
# tools/example_interpreters.toml) — resolved via PATH, ~/bin/<name>, and (for
# cpython-venv) the repo-root .venv.
DEFAULT_INTERPRETER_IDS = (
    "micropython",
    "micropython.exe",
    "circuitpython",
    "cpython-venv",
    "python.exe",
)

# interpreter_id -> resolution rule. "cpython-venv" resolves solely to the
# repo's own .venv; the others resolve by executable name via PATH / ~/bin.
INTERPRETER_EXE_NAMES = {
    "micropython": "micropython",
    "micropython.exe": "micropython.exe",
    "circuitpython": "circuitpython",
    "python.exe": "python.exe",
}

TESTPYPI_INDEX = os.environ.get("TESTPYPI_INDEX", "https://test.pypi.org/simple/")
PYPI_INDEX = os.environ.get("PYPI_INDEX", "https://pypi.org/simple/")

CPYTHON_INTERPRETER_IDS = frozenset({"cpython-venv", "python.exe"})


def _expand_user(path: str) -> str:
    return os.path.expanduser(path)


def resolve_interpreter_exe(interpreter_id: str) -> str | None:
    if interpreter_id == "cpython-venv":
        candidate = REPO / ".venv" / "bin" / "python"
        return str(candidate) if candidate.exists() else None

    name = INTERPRETER_EXE_NAMES.get(interpreter_id)
    if not name:
        return None

    found = shutil.which(name)
    if found:
        return found

    candidate = _expand_user("~/bin/" + name)
    if Path(candidate).exists():
        return candidate

    return None


def interpreter_available(interpreter_id: str) -> bool:
    return resolve_interpreter_exe(interpreter_id) is not None


def _graphics_impl(python_exe: str) -> str | None:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    proc = subprocess.run(
        [
            python_exe,
            "-c",
            "import pygraphics; print(pygraphics.implementation())",
        ],
        cwd=str(REPO),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def ensure_graphics_native(python_exe: str, *, verbose: bool) -> tuple[bool, str]:
    impl = _graphics_impl(python_exe)
    if impl == "native_cmod":
        return True, "native pygraphics already active"
    if impl == "pygraphics_python":
        if verbose:
            print(
                "Installing pydevices-pygraphics from TestPyPI for {}...".format(python_exe),
                file=sys.stderr,
            )
    elif impl:
        return False, "unexpected graphics implementation: {!r}".format(impl)
    else:
        if verbose:
            print(
                "graphics not importable in {}; installing pydevices-pygraphics...".format(python_exe),
                file=sys.stderr,
            )

    pip = [python_exe, "-m", "pip", "install", "-q", "-U", "pip"]
    subprocess.run(pip, check=True)
    install = [
        python_exe,
        "-m",
        "pip",
        "install",
        "-q",
        "-i",
        TESTPYPI_INDEX,
        "--extra-index-url",
        PYPI_INDEX,
        "pydevices-pygraphics",
    ]
    subprocess.run(install, check=True)

    impl = _graphics_impl(python_exe)
    if impl != "native_cmod":
        return False, "pygraphics install failed (implementation={!r})".format(impl)
    return True, "installed pydevices-pygraphics from TestPyPI"


def parse_result(stdout: str) -> dict | None:
    for match in RESULT_RE.finditer(stdout):
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
    return None


def run_case(interpreter_id: str, *, verbose: bool, timeout_s: float) -> dict:
    exe = resolve_interpreter_exe(interpreter_id)
    if not exe:
        return {
            "interpreter": interpreter_id,
            "status": "skip",
            "summary": "interpreter not available",
            "returncode": None,
        }

    setup_note = ""
    if interpreter_id in CPYTHON_INTERPRETER_IDS:
        ok, setup_note = ensure_graphics_native(exe, verbose=verbose)
        if not ok:
            return {
                "interpreter": interpreter_id,
                "status": "error",
                "summary": setup_note,
                "returncode": 1,
            }

    cmd = [exe, str(RUN_SCRIPT), "--repo", str(REPO), "--quiet"]
    env = os.environ.copy()
    # Avoid repo src/lib shadowing the pip-installed pygraphics on CPython.
    env.pop("PYTHONPATH", None)

    t0 = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(REPO),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_s,
            check=False,
        )
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        proc = exc
        timed_out = True
    elapsed = time.monotonic() - t0

    stdout = proc.stdout if hasattr(proc, "stdout") and proc.stdout else ""
    stderr = proc.stderr if hasattr(proc, "stderr") and proc.stderr else ""
    returncode = proc.returncode if hasattr(proc, "returncode") else 124

    result = parse_result(stdout)
    row = {
        "interpreter": interpreter_id,
        "exe": exe,
        "returncode": returncode,
        "timed_out": timed_out,
        "duration_s": round(elapsed, 2),
        "setup": setup_note,
        "stdout_tail": stdout[-4000:],
        "stderr_tail": stderr[-4000:],
        "result": result,
    }

    if timed_out:
        row["status"] = "error"
        row["summary"] = "timeout"
        return row

    if result:
        n_err = len(result.get("errors", []))
        n_ok = result.get("checks_passed", 0)
        if result.get("status") == "ok":
            row["status"] = "ok"
            row["summary"] = "{} checks ok".format(n_ok)
        else:
            row["status"] = "error"
            if n_err:
                row["summary"] = "{} fail, first: {}".format(
                    n_err, result.get("errors", [result.get("error")])[0]
                )
            else:
                row["summary"] = result.get("error", "error")
    elif returncode == 0:
        row["status"] = "ok"
        row["summary"] = "ok (no result json)"
    else:
        row["status"] = "error"
        if stdout.strip():
            tail = stdout.strip().splitlines()
        else:
            tail = (stderr or "").strip().splitlines()
        row["summary"] = tail[-1] if tail else "exit {}".format(returncode)

    return row


def print_table(rows: list[dict]) -> None:
    interpreters = [row["interpreter"] for row in rows]
    width = max([8, *[len(r) for r in interpreters]])
    print(file=sys.stderr)
    print("{:<{w}} | summary".format("interpreter", w=width), file=sys.stderr)
    print("{}-+-{}".format("-" * width, "-" * 60), file=sys.stderr)
    for row in rows:
        print(
            "{:<{w}} | {}".format(row["interpreter"], row.get("summary", ""), w=width),
            file=sys.stderr,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Native pygraphics vs pure-Python pygraphics parity matrix"
    )
    parser.add_argument(
        "--only-interpreter",
        help="Comma-separated interpreter ids (default: all desktop subprocess interpreters)",
    )
    parser.add_argument("--timeout", type=float, default=120.0, help="Per-interpreter timeout seconds")
    parser.add_argument("--verbose", action="store_true", help="Show install/setup notes")
    args = parser.parse_args(argv)

    if args.only_interpreter:
        wanted = [x.strip() for x in args.only_interpreter.split(",") if x.strip()]
    else:
        wanted = list(DEFAULT_INTERPRETER_IDS)

    rows: list[dict] = []
    for interpreter_id in wanted:
        if interpreter_id not in DEFAULT_INTERPRETER_IDS and interpreter_id not in INTERPRETER_EXE_NAMES:
            rows.append(
                {
                    "interpreter": interpreter_id,
                    "status": "skip",
                    "summary": "unknown interpreter id",
                }
            )
            continue
        if not interpreter_available(interpreter_id):
            rows.append(
                {
                    "interpreter": interpreter_id,
                    "status": "skip",
                    "summary": "not available",
                }
            )
            continue
        if args.verbose:
            print("Running {}...".format(interpreter_id), file=sys.stderr)
        rows.append(run_case(interpreter_id, verbose=args.verbose, timeout_s=args.timeout))

    RESULTS_JSON.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_JSON.write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print("Full results: {}".format(RESULTS_JSON), file=sys.stderr)
    print_table(rows)

    failed = [r for r in rows if r.get("status") == "error"]
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        raise SystemExit(130) from None
