"""Offline tests for plugins/rpm-openproject/skills/openproject/scripts/openproject.sh.

A fake `curl` on PATH records its argv and the --config it reads from stdin, and
returns canned JSON, so no network is used.
"""

import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/rpm-openproject/skills/openproject/scripts/openproject.sh"

FAKE_CURL = r"""#!/usr/bin/env bash
log="$FAKE_CURL_LOG"
printf '%s\n' "ARGV: $*" >> "$log"
config="$(cat)"
printf '%s\n' "CONFIG: $config" >> "$log"
case "$config" in
  *"/api/v3/work_packages/7\""*) printf '{"id":7,"lockVersion":4}' ;;
  *) printf '{"ok":true}' ;;
esac
"""


@unittest.skipUnless(shutil.which("bash") and shutil.which("git"), "needs bash and git")
class TestOpenProjectHelper(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.project = self.tmp / "project"
        self.project.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=self.project, check=True)
        bindir = self.tmp / "bin"
        bindir.mkdir()
        curl = bindir / "curl"
        curl.write_text(FAKE_CURL)
        curl.chmod(0o755)
        self.log = self.tmp / "curl.log"
        self.home = self.tmp / "home"
        self.home.mkdir()
        self.env = {
            "PATH": f"{bindir}:{os.environ['PATH']}",
            "HOME": str(self.home),
            "FAKE_CURL_LOG": str(self.log),
        }

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write_env(self, path, **values):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(f"{k}={v}\n" for k, v in values.items()))

    def run_sh(self, *args, env=None):
        return subprocess.run(
            ["bash", str(SCRIPT), *args], cwd=self.project, capture_output=True, text=True,
            env={**self.env, **(env or {})},
        )

    def calls(self):
        return self.log.read_text() if self.log.exists() else ""

    def test_missing_config_explains_setup(self):
        out = self.run_sh("statuses")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("OPEN_PROJECT_BASE_URL is not set", out.stderr)

    def test_project_env_wins_over_user_env(self):
        self.write_env(self.project / ".env.local", OPEN_PROJECT_BASE_URL="https://proj.example", OPEN_PROJECT_ACCESS_TOKEN="projtok")
        self.write_env(self.home / ".config/openproject/env", OPEN_PROJECT_BASE_URL="https://user.example", OPEN_PROJECT_ACCESS_TOKEN="usertok")
        out = self.run_sh("wp", "1")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn('url = "https://proj.example/api/v3/work_packages/1"', self.calls())

    def test_user_env_is_fallback_and_exported_env_wins(self):
        self.write_env(self.home / ".config/openproject/env", OPEN_PROJECT_BASE_URL="https://user.example/", OPEN_PROJECT_ACCESS_TOKEN="usertok")
        self.run_sh("wp", "1")
        self.assertIn('url = "https://user.example/api/v3/work_packages/1"', self.calls())
        self.run_sh("wp", "2", env={"OPEN_PROJECT_BASE_URL": "https://exported.example"})
        self.assertIn('url = "https://exported.example/api/v3/work_packages/2"', self.calls())

    def test_env_file_override_and_export_prefix_and_quotes(self):
        custom = self.tmp / "other.env"
        custom.write_text('export OPEN_PROJECT_BASE_URL="https://other.example"\nOPEN_PROJECT_ACCESS_TOKEN=\'tok\'\n')
        out = self.run_sh("wp", "3", env={"OPEN_PROJECT_ENV_FILE": str(custom)})
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn('url = "https://other.example/api/v3/work_packages/3"', self.calls())
        self.assertIn('user = "apikey:tok"', self.calls())

    def test_config_file_cannot_run_code(self):
        marker = self.tmp / "pwned"
        (self.project / ".env.local").write_text(
            f"touch {marker}\nOPEN_PROJECT_BASE_URL=https://x.example\nOPEN_PROJECT_ACCESS_TOKEN=t\n")
        self.run_sh("wp", "1")
        self.assertFalse(marker.exists())

    def test_token_never_in_argv(self):
        self.write_env(self.project / ".env.local", OPEN_PROJECT_BASE_URL="https://x.example", OPEN_PROJECT_ACCESS_TOKEN="SECRET123")
        self.run_sh("wp", "1")
        argv_lines = [l for l in self.calls().splitlines() if l.startswith("ARGV:")]
        self.assertTrue(argv_lines)
        self.assertFalse(any("SECRET123" in l for l in argv_lines))

    def test_config_command_redacts_token(self):
        self.write_env(self.project / ".env.local", OPEN_PROJECT_BASE_URL="https://x.example", OPEN_PROJECT_ACCESS_TOKEN="SECRET123")
        out = self.run_sh("config")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertNotIn("SECRET123", out.stdout)
        self.assertIn("https://x.example", out.stdout)

    def test_readonly_blocks_writes_but_not_reads(self):
        self.write_env(self.project / ".env.local", OPEN_PROJECT_BASE_URL="https://x.example", OPEN_PROJECT_ACCESS_TOKEN="t", OPEN_PROJECT_READONLY="true")
        for args in (["comment", "1", "hi"], ["status", "1", "2"], ["patch", "/api/v3/work_packages/1", "{}"], ["post", "/api/v3/x", "{}"]):
            with self.subTest(args=args):
                out = self.run_sh(*args)
                self.assertNotEqual(out.returncode, 0)
                self.assertIn("READONLY", out.stderr)
        self.assertEqual(self.calls(), "")
        self.assertEqual(self.run_sh("wp", "1").returncode, 0)

    def test_rejects_paths_outside_api(self):
        self.write_env(self.project / ".env.local", OPEN_PROJECT_BASE_URL="https://x.example", OPEN_PROJECT_ACCESS_TOKEN="t")
        for path in ("/admin", "/api/v3/../x", "/api/v3//evil.example"):
            with self.subTest(path=path):
                self.assertNotEqual(self.run_sh("get", path).returncode, 0)
        self.assertEqual(self.calls(), "")

    def test_no_delete_path(self):
        self.write_env(self.project / ".env.local", OPEN_PROJECT_BASE_URL="https://x.example", OPEN_PROJECT_ACCESS_TOKEN="t")
        out = self.run_sh("delete", "/api/v3/work_packages/1")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("no delete path", out.stderr)
        self.assertNotRegex(SCRIPT.read_text(), r"op_curl\s+DELETE|--request\s+DELETE|-X\s*DELETE")

    def test_status_sends_current_lock_version(self):
        self.write_env(self.project / ".env.local", OPEN_PROJECT_BASE_URL="https://x.example", OPEN_PROJECT_ACCESS_TOKEN="t")
        out = self.run_sh("status", "7", "22")
        self.assertEqual(out.returncode, 0, out.stderr)
        patch = [l for l in self.calls().splitlines() if "--request PATCH" in l]
        self.assertTrue(patch)
        self.assertIn('"lockVersion":4', patch[0])
        self.assertIn("/api/v3/statuses/22", patch[0])


if __name__ == "__main__":
    unittest.main()
