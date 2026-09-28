import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('harness_sync', SOURCE / 'bin/sync.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SyncTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(SOURCE / 'bin', self.root / 'bin')
        self.put('harness.config.yaml', 'tools:\n  - claude\n  - codex\nactive_skills:\n  - demo\nactive_agents:\n  - reviewer\n')
        self.put('catalog/skills/demo/SKILL.md', '---\nname: demo\ndescription: Demo\n---\nTest')
        self.put('agents/reviewer/AGENT.md', '# Reviewer\nReview "code".\n')
        self.put('AGENTS.md', 'Shared instructions')
        self.put('hooks/hooks.json', '{"hooks": {}}')
        self.put('mcp/servers.json', json.dumps({'servers': {
            'git': {'enabled': True, 'command': 'npx', 'env': {'TOKEN': '${TOKEN}'}},
            'web': {'enabled': True, 'transport': 'http', 'url': 'https://example.com/mcp'},
            'off': {'enabled': False}}}))

    def put(self, path, content):
        module.write(self.root / path, content)

    def test_both_clients_and_idempotence(self):
        self.put('.claude/settings.json', '{"permissions": {"allow": ["Read"]}}')
        module.sync(self.root)
        config = (self.root / '.codex/config.toml').read_text()
        self.assertIn('env_vars = ["TOKEN"]', config)
        self.assertNotIn('${TOKEN}', config)
        self.assertNotIn('off', config)
        self.assertTrue((self.root / '.agents/skills/demo/SKILL.md').exists())
        self.assertIn('developer_instructions = ', (self.root / '.codex/agents/reviewer.toml').read_text())
        self.assertTrue((self.root / '.claude/agents/reviewer.md').read_text().startswith('---\nname: reviewer\n'))
        self.assertEqual(json.loads((self.root / '.claude/settings.json').read_text())['permissions']['allow'], ['Read'])
        module.sync(self.root)
        self.assertEqual(config, (self.root / '.codex/config.toml').read_text())
        self.put('harness.config.yaml', 'tools:\n  - codex\nactive_skills:\nactive_agents:\n')
        module.sync(self.root)
        self.assertFalse((self.root / '.agents/skills/demo').exists())
        self.assertFalse((self.root / '.codex/agents/reviewer.toml').exists())
        self.assertTrue((self.root / '.claude/skills/demo').exists())

    def test_preserves_unmanaged_config(self):
        self.put('.codex/config.toml', 'model = "custom"\n')
        with self.assertRaisesRegex(ValueError, 'not generated'):
            module.sync(self.root)
        self.assertEqual((self.root / '.codex/config.toml').read_text(), 'model = "custom"\n')
        self.assertFalse((self.root / '.claude').exists())

    def test_missing_skill_does_not_destroy_projection(self):
        module.sync(self.root)
        self.put('harness.config.yaml', 'tools:\n  - codex\nactive_skills:\n  - absent\n')
        with self.assertRaisesRegex(ValueError, 'Missing skill'):
            module.sync(self.root)
        self.assertTrue((self.root / '.agents/skills/demo/SKILL.md').exists())

    def test_env_alias_fails_without_materializing_secret(self):
        with self.assertRaises(ValueError):
            module.codex_mcp({'a': {'enabled': True, 'command': 'npx', 'env': {'A': '${B}'}}})


if __name__ == '__main__':
    unittest.main()
