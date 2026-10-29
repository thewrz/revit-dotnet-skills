"""Packaging regression checks: observable install identity and discoverability."""
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class PackageTests(unittest.TestCase):
    def test_fork_identity_is_consistent(self):
        for path in ('.claude-plugin/plugin.json', '.codex-plugin/plugin.json',
                     '.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json'):
            with self.subTest(path=path):
                data = json.loads((ROOT / path).read_text())
                self.assertEqual(data['name'], 'revit-dotnet-skills')

    def test_revit_skill_is_installed_and_indexed(self):
        data = json.loads((ROOT / '.claude-plugin/plugin.json').read_text())
        self.assertIn('./skills/revit-development', data['skills'])
        index = subprocess.check_output(['bash', 'scripts/generate-skill-index-snippets.sh'], cwd=ROOT, text=True)
        self.assertIn('|revit:{revit-development}', index)

    def test_upstream_license_is_retained(self):
        self.assertIn('Copyright (c) 2025 Aaron Stannard', (ROOT / 'LICENSE').read_text())

if __name__ == '__main__':
    unittest.main()
