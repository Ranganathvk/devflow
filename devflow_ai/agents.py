"""Per-agent materialization paths for devflow install/sync."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgentSpec:
    id: str
    display_name: str

    def repo_skills_dir(self, target: Path) -> Path:
        raise NotImplementedError

    def repo_agents_path(self, target: Path) -> Path | None:
        raise NotImplementedError

    def global_skills_dir(self) -> Path:
        raise NotImplementedError

    def global_agents_path(self) -> Path | None:
        raise NotImplementedError

    def global_scope_label(self) -> str:
        return f"all {self.display_name} projects (user-level)"


@dataclass(frozen=True)
class MirrorAgentSpec(AgentSpec):
    """Agents that mirror core/ into a dot-directory (Cursor, Claude)."""

    mirror_dir: str

    def repo_mirror_root(self, target: Path) -> Path:
        return target / self.mirror_dir

    def repo_skills_dir(self, target: Path) -> Path:
        return self.repo_mirror_root(target) / "skills"

    def repo_agents_path(self, target: Path) -> Path:
        return self.repo_mirror_root(target) / "AGENTS.md"

    def global_mirror_root(self) -> Path:
        return Path.home() / self.mirror_dir

    def global_skills_dir(self) -> Path:
        return self.global_mirror_root() / "skills"

    def global_agents_path(self) -> Path:
        return self.global_mirror_root() / "AGENTS.md"


@dataclass(frozen=True)
class CopilotAgentSpec(AgentSpec):
    def repo_skills_dir(self, target: Path) -> Path:
        return target / ".github" / "skills"

    def repo_agents_path(self, target: Path) -> Path:
        return target / "AGENTS.md"

    def global_skills_dir(self) -> Path:
        return Path.home() / ".copilot" / "skills"

    def global_agents_path(self) -> Path:
        return Path.home() / ".copilot" / "AGENTS.md"


AGENTS: dict[str, AgentSpec] = {
    "cursor": MirrorAgentSpec(
        id="cursor",
        display_name="Cursor",
        mirror_dir=".cursor",
    ),
    "claude": MirrorAgentSpec(
        id="claude",
        display_name="Claude Code",
        mirror_dir=".claude",
    ),
    "copilot": CopilotAgentSpec(
        id="copilot",
        display_name="GitHub Copilot",
    ),
}


def get_agent(agent_id: str) -> AgentSpec:
    try:
        return AGENTS[agent_id]
    except KeyError as exc:
        known = ", ".join(sorted(AGENTS))
        msg = f"Unknown agent {agent_id!r}. Supported: {known}"
        raise ValueError(msg) from exc
