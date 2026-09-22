"""A firmware and a wheel must both say which pygraphics they were built from.

pygraphics#25. `os.uname().version` answers for MicroPython and says nothing
about the user C modules compiled into the image, so a rendering that moves
between two firmwares cannot be attributed to a revision. audiodsp lost one
exactly that way -- a firmware built from a throwaway source tree during a pin
move, unrecoverable from the working tree or the `.bin` files afterwards.

The case that matters here is the third: **the revision is not "unknown" in a
checkout**. Without it the whole mechanism can ship reporting `unknown` from
every target while every other assertion still passes -- the marker exists, the
two sides agree, and neither knows anything.
"""

from __future__ import annotations

import os
import re
import subprocess
import unittest

import _env  # noqa: F401  puts lib/ on sys.path when no native build is present

import pygraphics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: pygraphics ships twice (tests/_env.py): a pure-Python package under lib/ and
#: the native C extension. The marker is the *build's*, so only the native one
#: can carry it -- there is no build step to stamp a .py file with, and a source
#: package installed by mip is identified by the mip package version. Under the
#: default pure-Python mode these tests skip and say so, rather than passing
#: vacuously; PYGRAPHICS_TEST_NATIVE=1 is where they mean something.
NATIVE = not getattr(pygraphics, "__file__", "").endswith(".py")

#: `git describe --always --dirty --abbrev=7`: a tag-and-distance, or a bare
#: short hash in a repository with no tags, each optionally `-dirty`.
DESCRIBE = re.compile(r"^[0-9A-Za-z._/+-]+$")


def _in_a_checkout() -> bool:
    # os.path.exists, not isdir: in a git WORKTREE `.git` is a file pointing at
    # the real one, and isdir() silently skipped the test that matters here --
    # the same "absence reads as agreement" this file exists to prevent.
    return os.path.exists(os.path.join(ROOT, ".git"))


@unittest.skipUnless(
    NATIVE,
    "the pure-Python pygraphics carries no build marker and cannot: "
    "set PYGRAPHICS_TEST_NATIVE=1 to test the extension")
class BuildRevisionTests(unittest.TestCase):
    def test_the_module_carries_both_markers(self):
        # Asserted by name so that a rewrite of the module table fails here
        # rather than shipping a firmware that cannot be identified.
        self.assertTrue(hasattr(pygraphics, "__version__"),
                        "pygraphics.__version__ is missing: the build marker "
                        "is not in the module table")
        self.assertTrue(hasattr(pygraphics, "__revision__"),
                        "pygraphics.__revision__ is missing: the build marker "
                        "is not in the module table")
        self.assertIsInstance(pygraphics.__version__, str)
        self.assertIsInstance(pygraphics.__revision__, str)

    def test_the_version_is_the_VERSION_file(self):
        with open(os.path.join(ROOT, "VERSION"), encoding="utf-8") as handle:
            expected = handle.read().strip()
        # An extension built from an older checkout reports that checkout's
        # version, which is the point of the marker -- so this only holds where
        # the two were built together. Skip rather than lie about it.
        if pygraphics.__version__ != expected:
            self.skipTest(
                "this pygraphics reports %r and the tree says %r -- the "
                "extension was built from a different checkout, which is "
                "exactly what the marker exists to tell you"
                % (pygraphics.__version__, expected))

    def test_the_revision_is_not_unknown_in_a_checkout(self):
        """The one that catches a mechanism reporting nothing from everywhere."""
        if not _in_a_checkout():
            self.skipTest("not a git checkout; 'unknown' is the honest answer")
        # NO second escape hatch here. The first draft also skipped when
        # __version__ was "0.0.0+unknown", reading it as "built somewhere
        # else" -- and an extension built right here with the -D macros
        # forgotten says exactly that, so the planted fault SKIPPED instead of
        # failing. In a checkout, "unknown" is a failure whatever else is true.
        self.assertNotEqual(
            pygraphics.__version__, "0.0.0+unknown",
            "built inside a git checkout and still reporting the fallback "
            "version: the build did not pass -DPYGRAPHICS_VERSION")
        self.assertNotEqual(
            pygraphics.__revision__, "unknown",
            "built inside a git checkout and still reporting 'unknown': the "
            "build did not pass -DPYGRAPHICS_REVISION, so every target would "
            "report nothing while every other check here still passed")
        self.assertRegex(pygraphics.__revision__, DESCRIBE)

    def test_it_agrees_with_what_git_says_now(self):
        if not _in_a_checkout():
            self.skipTest("not a git checkout")
        try:
            described = subprocess.run(
                ["git", "-C", ROOT, "describe", "--always", "--dirty", "--abbrev=7"],
                capture_output=True, text=True, check=True).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            self.skipTest("git is not available here")
        if described != pygraphics.__revision__:
            # Not a failure: the tree moves under a built extension all day.
            # Reported, because a mismatch is a true and useful statement.
            self.skipTest(
                "this pygraphics was built from %r and the tree is now at %r"
                % (pygraphics.__revision__, described))

    def test_the_marker_is_not_sprayed_over_every_object(self):
        """A control: if everything had it, nothing would be proven by having it."""
        self.assertFalse(hasattr(pygraphics.FrameBuffer, "__revision__"),
                         "the marker belongs to the module, not to every type")
        self.assertFalse(hasattr(pygraphics.Area, "__revision__"))


if __name__ == "__main__":
    unittest.main()
