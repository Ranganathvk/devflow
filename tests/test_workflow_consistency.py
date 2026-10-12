from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ADAPTER_SKILL_DIRS = (".cursor/skills", ".claude/skills", ".github/skills")
AGENT_MIRRORS = (".cursor/AGENTS.md", ".claude/AGENTS.md")


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys instead of silently accepting the last value."""


def _construct_mapping(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping", node.start_mark,
                f"duplicate key {key!r}", key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def resolve_context_dir(root=ROOT):
    override = os.environ.get("DEVFLOW_CONTEXT_DIR", "").strip()
    if override:
        return override
    manifest = root / "devflow.context.yaml"
    if manifest.is_file():
        for line in manifest.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and line.startswith("context_dir:"):
                value = line.split(":", 1)[1].strip().strip("\"'")
                if value:
                    return value
    return "artifacts"


def materialize(text, context_dir):
    text = text.replace("@{context_dir}/", f"@{context_dir}/")
    return text.replace("{context_dir}/", f"{context_dir}/")


def canonical_skills():
    return {p.parent.name: p for p in sorted((ROOT / "core/skills").glob("*/SKILL.md"))}


class WorkflowConsistencyTests(unittest.TestCase):
    def test_agent_harness_mirrors_match_canonical(self):
        expected = materialize((ROOT / "core/AGENTS.md").read_text(encoding="utf-8"), resolve_context_dir())
        for relative in AGENT_MIRRORS:
            with self.subTest(mirror=relative):
                self.assertEqual(expected, (ROOT / relative).read_text(encoding="utf-8"),
                                 f"{relative} drifted; regenerate from core/AGENTS.md")

    def test_skill_mirrors_match_canonical_and_have_no_stale_skills(self):
        canonical = canonical_skills()
        self.assertTrue(canonical, "No canonical skills found")
        expected_names = set(canonical)
        context_dir = resolve_context_dir()
        for adapter in ADAPTER_SKILL_DIRS:
            root = ROOT / adapter
            self.assertTrue(root.is_dir(), f"Missing {adapter}")
            actual_names = {p.parent.name for p in root.glob("*/SKILL.md")}
            self.assertEqual(expected_names, actual_names, f"{adapter} has missing/stale skills")
            for name, source in canonical.items():
                with self.subTest(adapter=adapter, skill=name):
                    expected = materialize(source.read_text(encoding="utf-8"), context_dir)
                    actual = (root / name / "SKILL.md").read_text(encoding="utf-8")
                    self.assertEqual(expected, actual, f"{adapter}/{name}/SKILL.md drifted")

    def test_skill_frontmatter_names_match_directories(self):
        for name, path in canonical_skills().items():
            with self.subTest(skill=name):
                text = path.read_text(encoding="utf-8")
                front = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
                self.assertIsNotNone(front, f"{path} missing YAML frontmatter")
                found = re.search(r"^name:\s*([a-z0-9-]+)\s*$", front.group(1), re.MULTILINE)
                self.assertIsNotNone(found, f"{path} missing simple name field")
                self.assertEqual(name, found.group(1))

    def test_contract_examples_parse_and_have_consistent_metadata(self):
        paths = sorted((ROOT / "core/contracts").glob("*.contract.yaml"))
        self.assertTrue(paths, "No canonical contract examples found")
        for path in paths:
            with self.subTest(contract=path.name):
                data = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
                self.assertIsInstance(data, dict)
                for key in ("contract_version", "artifact", "workflow_profile"):
                    self.assertIn(key, data, f"{path} missing {key}")
                    self.assertIsInstance(data[key], str)
                self.assertEqual("1", data["contract_version"])
                self.assertEqual("devflow", data["workflow_profile"])
                self.assertEqual(path.name.removesuffix(".contract.yaml"), data["artifact"])

    def test_design_and_tdd_keep_explicit_approval_gate(self):
        design = (ROOT / "core/skills/design/SKILL.md").read_text(encoding="utf-8")
        tdd = (ROOT / "core/skills/tdd/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Set `design_status: approved` only after explicit human approval", design)
        self.assertIn("design_status: approved", tdd)
        self.assertIn("Do not invoke before design approval", tdd)

    def test_implement_stays_bounded_to_one_unit(self):
        text = (ROOT / "core/skills/implement/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Implement **one** bounded chunk", text)
        self.assertIn("One invocation = one task **or** one lite feature", text)
        self.assertIn("Multiple tasks/features in one run", text)

    def test_task_queue_requires_human_approval(self):
        text = (ROOT / "core/skills/tasksplit/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Stop for explicit human approval", text)
        self.assertIn("tasks_status: approved", text)


if __name__ == "__main__":
    unittest.main()
