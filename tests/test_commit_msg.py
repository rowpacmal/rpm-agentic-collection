"""Tests for plugins/rpm-core/skills/commit/assets/commit-msg."""

import pathlib
import subprocess
import tempfile
import unittest

HOOK = pathlib.Path(__file__).resolve().parents[1] / "plugins/rpm-core/skills/commit/assets/commit-msg"

ACCEPT = [
    "feat: add x\n",
    "fix(api): return 404 for unknown ids\n",
    "feat(api)!: drop v1 endpoints\n",
    "chore: release 2.0.0\n\nRelease-As: 2.0.0\n",
    "docs: fix typo\n# a git comment line\n",
]
REJECT = [
    "feat: add x\n\nwith a body\n",
    "feat: add x\n\nCo-Authored-By: someone\n",
    "Added a thing\n",
    "fix: .\n",
    "fix: trailing period.\n",
]


class TestCommitMsg(unittest.TestCase):
    def run_hook(self, message: str) -> int:
        with tempfile.TemporaryDirectory() as tmp:
            msg = pathlib.Path(tmp) / "MSG"
            msg.write_text(message)
            return subprocess.run(["sh", str(HOOK), str(msg)], cwd=tmp, capture_output=True).returncode

    def test_accept(self):
        for m in ACCEPT:
            with self.subTest(m=m):
                self.assertEqual(self.run_hook(m), 0)

    def test_reject(self):
        for m in REJECT:
            with self.subTest(m=m):
                self.assertEqual(self.run_hook(m), 1)


if __name__ == "__main__":
    unittest.main()
