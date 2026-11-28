"""Free structure tests (no model calls): manifests, skill frontmatter, README links, eval scenarios."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestPluginManifests(unittest.TestCase):
    def test_plugin_json(self):
        data = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "swarmagents")
        self.assertTrue(data["description"])
        self.assertRegex(data["version"], r"^\d+\.\d+\.\d+$")

    def test_marketplace_json(self):
        data = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "swarmagents")
        self.assertIn("name", data["owner"])
        self.assertEqual(data["plugins"][0]["name"], "swarmagents")
        self.assertIn("source", data["plugins"][0])


class TestSkillFrontmatter(unittest.TestCase):
    def test_frontmatter(self):
        text = (ROOT / "skills" / "swarmagents" / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match, "SKILL.md must start with YAML frontmatter")
        front = match.group(1)
        self.assertRegex(front, r"(?m)^name:\s*swarmagents\s*$")
        self.assertRegex(front, r"(?m)^description:\s*\S+")

    def test_cost_aware_execution_modes(self):
        text = (ROOT / "skills" / "swarmagents" / "SKILL.md").read_text(encoding="utf-8")
        for mode in ("Solo", "Lean", "Full"):
            self.assertIn(f"**{mode}**", text)
        for setting in (
            "mode: auto",
            "max_active_workers:",
            "max_worker_launches:",
            "max_repair_rounds:",
            "token_budget:",
            "cost_budget:",
        ):
            self.assertIn(setting, text)
        self.assertIn("Do not preload them into implementation workers", text)

    def test_web_build_has_no_agent_count_target(self):
        text = (
            ROOT / "skills" / "swarmagents" / "references" / "parallel-web-build.md"
        ).read_text(encoding="utf-8")
        self.assertNotRegex(text, r"typically\s+5[–-]10")
        self.assertIn("decomposition menu, not a staffing target", text)


class TestReadmeLinks(unittest.TestCase):
    def check_relative_links(self, md_path):
        text = md_path.read_text(encoding="utf-8")
        for label, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            resolved = (md_path.parent / target.split("#")[0]).resolve()
            self.assertTrue(resolved.exists(), f"{md_path.name}: broken link [{label}]({target})")

    def test_root_readme(self):
        self.check_relative_links(ROOT / "README.md")

    def test_skill_readme(self):
        self.check_relative_links(ROOT / "skills" / "swarmagents" / "README.md")

    def test_demo_readme(self):
        demo = ROOT / "demo" / "taskboard" / "README.md"
        if demo.exists():
            self.check_relative_links(demo)

    def test_example_readmes(self):
        readmes = sorted((ROOT / "examples").glob("*/README.md"))
        self.assertGreaterEqual(len(readmes), 3)
        for md in readmes:
            self.check_relative_links(md)


class TestEvalScenarios(unittest.TestCase):
    def test_scenarios_well_formed(self):
        paths = sorted((ROOT / "evals" / "scenarios").glob("*.json"))
        self.assertGreaterEqual(len(paths), 5)
        for p in paths:
            data = json.loads(p.read_text(encoding="utf-8"))
            for key in ("name", "claim", "prompt", "grading_notes"):
                self.assertTrue(data.get(key), f"{p.name}: missing {key}")
            for rx in data.get("must_match", []) + data.get("must_not_match", []):
                re.compile(rx)
            self.assertEqual(data["name"], p.stem)


if __name__ == "__main__":
    unittest.main()
