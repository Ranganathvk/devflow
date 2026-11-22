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

    def test_design_markdown_is_optional_and_harness_has_no_rollup_contract(self):
        design = (ROOT / "core/skills/design/SKILL.md").read_text(encoding="utf-8")
        agents = (ROOT / "core/AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Optional when separate human review adds value or is requested", design)
        self.assertIn("optional design review", agents.lower())
        self.assertNotIn("UNDERSTAND.contract.yaml", agents)

    def test_implement_stays_bounded_to_one_unit(self):
        text = (ROOT / "core/skills/implement/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Implement **one** bounded chunk", text)
        self.assertIn("One invocation = one task **or** one lite feature", text)
        self.assertIn("Multiple tasks/features in one run", text)

    def test_task_queue_requires_human_approval(self):
        text = (ROOT / "core/skills/tasksplit/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Stop for explicit human approval", text)
        self.assertIn("tasks_status: approved", text)

    def test_skill_contract_reads_are_written(self):
        """Fail when a skill reads a contract artifact or dotted field no skill writes.

        Catches handoff drift such as a required ``UNDERSTAND.contract.yaml`` after
        ``/understand`` stopped emitting it, or a gate on ``design_stages.compat.blocking``
        after ``/design`` dropped that stage machine.
        """
        written_artifacts, written_fields = set(), set()
        read_artifacts, read_fields = {}, {}
        for name, path in canonical_skills().items():
            text = path.read_text(encoding="utf-8")
            written_artifacts |= _written_contract_artifacts(text)
            written_fields |= _written_contract_fields(text)
            for artifact in _read_contract_artifacts(text):
                read_artifacts.setdefault(artifact, set()).add(name)
            for field in _read_contract_fields(text):
                read_fields.setdefault(field, set()).add(name)
        for path in sorted((ROOT / "core/contracts").glob("*.contract.yaml")):
            written_fields |= _yaml_key_paths(path.read_text(encoding="utf-8"))

        missing = {
            "artifacts": {
                artifact: sorted(skills)
                for artifact, skills in sorted(read_artifacts.items())
                if artifact not in written_artifacts
            },
            "fields": {
                field: sorted(skills)
                for field, skills in sorted(read_fields.items())
                if field not in written_fields
            },
        }
        self.assertEqual(
            {"artifacts": {}, "fields": {}},
            missing,
            "contract artifacts or fields read by a skill are never written",
        )


_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
_HEADING_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)
_BACKTICK_RE = re.compile(r"`([^`]+)`")
_WRITE_LINE_RE = re.compile(r"(?i)\b(write|writes|persist|persists|append|appended|created or replaced)\b")
_READ_LINE_RE = re.compile(r"(?i)\b(requires?|required|read|load|resume|gates?)\b")
_NEGATIVE_LINE_RE = re.compile(
    r"(?i)(?:\b(?:do not|don't|never)\b|\bnot\b).{0,48}\b(?:create|write|emit|require|look)\b"
)
_FIELD_RE = re.compile(r"^[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]+)+$")
_FILE_EXT_RE = re.compile(r"\.(?:yaml|yml|md|py|json|toml|txt|sh|ps1)$", re.IGNORECASE)
_YAML_KEY_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_-]*")


def _skill_prose(text):
    text = _FRONTMATTER_RE.sub("", text, count=1)
    return _FENCE_RE.sub("", text)


def _sections(text):
    matches = list(_HEADING_RE.finditer(text))
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        yield match.group(1).strip().lower(), text[start:end]


def _normalize_contract(token):
    token = token.strip().strip(".,;:")
    for prefix in ("{context_dir}/", "<context_dir>/"):
        token = token.replace(prefix, "")
    if "/" in token or "\\" in token or not token.endswith(".contract.yaml"):
        return None
    token = token.replace("<FEATURE>", "FEATURE").replace("<feature>", "FEATURE")
    token = token.replace("*", "FEATURE")
    token = re.sub(r"<[^>]+>", "", token)
    return token


def _contracts_on_line(line):
    found = []
    for token in _BACKTICK_RE.findall(line):
        normalized = _normalize_contract(token)
        if normalized:
            found.append(normalized)
    return found


def _read_contract_artifacts(text):
    prose = _skill_prose(text)
    found = set()
    for title, body in _sections(prose):
        is_input = title.startswith("input")
        for line in body.splitlines():
            if _NEGATIVE_LINE_RE.search(line):
                continue
            if is_input or _READ_LINE_RE.search(line):
                found.update(_contracts_on_line(line))
    return found


def _written_contract_artifacts(text):
    prose = _skill_prose(text)
    found = set()
    for title, body in _sections(prose):
        is_output = "output" in title or title.startswith("durable")
        for line in body.splitlines():
            if _NEGATIVE_LINE_RE.search(line):
                continue
            if is_output or _WRITE_LINE_RE.search(line):
                found.update(_contracts_on_line(line))
    return found


def _read_contract_fields(text):
    found = set()
    for token in _BACKTICK_RE.findall(_skill_prose(text)):
        token = token.strip()
        if _FILE_EXT_RE.search(token) or "/" in token or "*" in token or " " in token:
            continue
        if _FIELD_RE.fullmatch(token):
            found.add(token)
    return found


def _yaml_key_paths(yaml_text):
    paths = set()
    stack = []
    for line in yaml_text.splitlines():
        code = line.split("#", 1)[0].rstrip()
        if not code.strip():
            continue
        indent = len(code) - len(code.lstrip(" "))
        stripped = code.strip()
        if stripped.startswith("- "):
            rest = stripped[2:].strip()
            if ":" not in rest:
                continue
            key = rest.split(":", 1)[0].strip()
            key_indent = indent + 2
        elif ":" in stripped:
            key = stripped.split(":", 1)[0].strip()
            key_indent = indent
        else:
            continue
        if not _YAML_KEY_RE.fullmatch(key or ""):
            continue
        while stack and stack[-1][0] >= key_indent:
            stack.pop()
        paths.add(".".join([item[1] for item in stack] + [key]))
        stack.append((key_indent, key))
    return paths


def _written_contract_fields(text):
    text = _FRONTMATTER_RE.sub("", text, count=1)
    found = set()
    for block in re.findall(r"```yaml\n(.*?)```", text, flags=re.DOTALL):
        found |= _yaml_key_paths(block)
    return found


if __name__ == "__main__":
    unittest.main()
