"""Exercise the real synchronizer against disposable Git repositories."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync-upstream.sh"


class SyncUpstreamTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "core.autocrlf", "false")
        self.write("workspace.yaml", "projects: []\n")
        self.write("README.md", "Template\n")
        self.write("AGENTS.md", "Template agent rules\n")
        self.write(".github/workflows/ci.yml", "template CI\n")
        self.write("vault/index.md", "Empty vault\n")
        self.write("vault/AGENTS.md", "Template vault instructions\n")
        self.write("bin/removed", "obsolete\n")
        self.write("catalog/skill.md", "old\n")
        self.commit("template")
        self.git("checkout", "-q", "-b", "upstream")
        self.write("workspace.yaml", "projects: [private-project]\n")
        self.write(".gitmodules", "private submodule\n")
        self.write("workspace/private/file", "private\n")
        self.write("vault/projects/private/file", "private\n")
        self.write("vault/index.md", "Private project index\n")
        self.write("vault/AGENTS.md", "Private project registry\n")
        self.write("README.md", "Official harness\n")
        self.write("AGENTS.md", "Private agent rules\n")
        self.write(".github/workflows/ci.yml", "upstream CI\n")
        self.write(".env", "PRIVATE_DATA=must-not-copy\n")
        self.write("catalog/skill.md", "new\n")
        self.write("catalog/new skill.md", "new file\n")
        self.write("bin/tool", "#!/bin/sh\nexit 0\n")
        self.write("vault/_meta/skills/query.md", "updated tooling\n")
        self.git("rm", "bin/removed")
        self.git("add", ".")
        self.git("update-index", "--chmod=+x", "bin/tool")
        self.git("commit", "-qm", "upstream")
        self.git("checkout", "-q", "main")

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True,
                              capture_output=True, text=True).stdout

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-qm", message)

    def sync(self, ref="upstream"):
        return subprocess.run([os.environ.get("HARNESS_TEST_BASH", "bash"),
                               str(SCRIPT), ref], cwd=self.root,
                              capture_output=True, text=True)

    def test_updates_deletes_and_preserves_template(self):
        result = self.sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / "catalog/skill.md").read_text(), "new\n")
        self.assertTrue((self.root / "catalog/new skill.md").exists())
        self.assertFalse((self.root / "bin/removed").exists())
        self.assertTrue(self.git("ls-files", "--stage", "bin/tool").startswith("100755"))
        self.assertEqual((self.root / "workspace.yaml").read_text(), "projects: []\n")
        self.assertEqual((self.root / "README.md").read_text(), "Template\n")
        self.assertEqual((self.root / "AGENTS.md").read_text(), "Template agent rules\n")
        self.assertEqual((self.root / "vault/index.md").read_text(), "Empty vault\n")
        self.assertEqual((self.root / "vault/AGENTS.md").read_text(), "Template vault instructions\n")
        self.assertEqual((self.root / ".github/workflows/ci.yml").read_text(), "template CI\n")
        self.assertTrue((self.root / "vault/_meta/skills/query.md").exists())
        for name in [".env", ".gitmodules", "workspace/private/file", "vault/projects/private/file"]:
            self.assertFalse((self.root / name).exists(), name)
        self.commit("sync")
        result = self.sync()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_refuses_local_changes(self):
        self.write("catalog/skill.md", "local work\n")
        result = self.sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Working tree must be clean", result.stderr)
        self.assertEqual((self.root / "catalog/skill.md").read_text(), "local work\n")

    def test_refuses_nonempty_workspace(self):
        self.write("workspace.yaml", "projects: [my-project]\n")
        self.commit("adopt template")
        result = self.sync()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("empty template workspace", result.stderr)
        self.assertEqual((self.root / "catalog/skill.md").read_text(), "old\n")

    def test_invalid_ref_does_not_change_files(self):
        self.assertNotEqual(self.sync("missing-reference").returncode, 0)
        self.assertEqual(self.git("status", "--porcelain"), "")


if __name__ == "__main__":
    unittest.main()
