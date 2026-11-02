"""Tests for plugins/rpm-security/scripts/secret_guard.py."""

import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "plugins/rpm-security/scripts/secret_guard.py"
spec = importlib.util.spec_from_file_location("secret_guard", SCRIPT)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

# Fake secrets are assembled at runtime so this file doesn't trip scanners itself.
FAKE = {
    "private key": "-----BEGIN " + "OPENSSH PRIVATE KEY-----\nabc",
    "AWS access key id": "AKIA" + "ABCDEFGHIJKLMNOP",
    "GitHub token": "ghp_" + "a1" * 18,
    "Anthropic API key": "sk-ant-" + "api03-" + "x" * 40,
    "Stripe live key": "sk_" + "live_" + "a" * 24,
    "Slack token": "xoxb-" + "1234567890-" + "abcdefghijkl",
    "Google API key": "AIza" + "B" * 35,
}
SAFE = [
    "const apiKey = process.env.ANTHROPIC_API_KEY;",
    "AWS_ACCESS_KEY_ID=your-key-here",
    "sk-ant-...",
    "stripe test key: sk_" + "test_" + "a" * 24,
    "-----BEGIN PUBLIC KEY-----",
    "ghp_short",
]


class TestFindSecret(unittest.TestCase):
    def test_detects(self):
        for label, text in FAKE.items():
            with self.subTest(label=label):
                self.assertEqual(guard.find_secret(f"x = '{text}'"), label)

    def test_ignores_safe(self):
        for text in SAFE:
            with self.subTest(text=text):
                self.assertIsNone(guard.find_secret(text))

    def test_edit_and_multiedit_inputs(self):
        self.assertIn("AKIA", guard.written_text({"new_string": FAKE["AWS access key id"]}))
        self.assertIn("AKIA", guard.written_text({"edits": [{"new_string": FAKE["AWS access key id"]}]}))


class TestEnvFile(unittest.TestCase):
    def test_env_files(self):
        for path in [".env", "/app/.env.local", "backend/.env.production", ".envrc"]:
            with self.subTest(path=path):
                self.assertTrue(guard.is_env_file(path))

    def test_not_env_files(self):
        for path in [".env.example", "/app/.env.sample", "src/env.ts", "environment.md", ".envoy.yaml"]:
            with self.subTest(path=path):
                self.assertFalse(guard.is_env_file(path))


class TestHookIO(unittest.TestCase):
    def run_hook(self, payload):
        return subprocess.run([sys.executable, "-I", str(SCRIPT)], input=payload, capture_output=True, text=True)

    def test_ask_json(self):
        payload = json.dumps({"tool_name": "Write", "tool_input": {"file_path": "a.ts", "content": FAKE["GitHub token"]}})
        out = self.run_hook(payload)
        self.assertEqual(json.loads(out.stdout)["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_clean_write_silent(self):
        out = self.run_hook(json.dumps({"tool_name": "Write", "tool_input": {"file_path": "a.ts", "content": "x = 1"}}))
        self.assertEqual((out.returncode, out.stdout), (0, ""))

    def test_bad_input_fails_open(self):
        self.assertEqual(self.run_hook("{").stdout, "")


    def test_env_edit_asks_without_secret(self):
        payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": "/p/.env.local", "new_string": "DEBUG=1"}})
        out = self.run_hook(payload)
        self.assertEqual(json.loads(out.stdout)["hookSpecificOutput"]["permissionDecision"], "ask")

    def test_example_edit_silent(self):
        payload = json.dumps({"tool_name": "Edit", "tool_input": {"file_path": "/p/.env.example", "new_string": "DEBUG=1"}})
        self.assertEqual(self.run_hook(payload).stdout, "")


if __name__ == "__main__":
    unittest.main()
