"""Attach devflow to a consumer repository and sync agent artifacts."""

from __future__ import annotations

import enum
import os
import shutil
from pathlib import Path

from devflow_ai.agents import AgentSpec, MirrorAgentSpec, get_agent
from devflow_ai.config import (
    CONTEXT_MANIFEST,
    materialize_context_paths,
    resolve_context_dir,
    write_context_manifest,
)


class InstallScope(enum.StrEnum):
    REPO = "repo"
    GLOBAL = "global"


def framework_root() -> Path:
    """Return the devflow framework root (contains core/ and adapters/)."""
    env = os.environ.get("DEVFLOW_FRAMEWORK_ROOT", "").strip()
    if env:
        root = Path(env).resolve()
        if (root / "core").is_dir():
            return root
        msg = f"DEVFLOW_FRAMEWORK_ROOT has no core/: {root}"
        raise FileNotFoundError(msg)

    package_dir = Path(__file__).resolve().parent
    bundled = package_dir / "bundled"
    if (bundled / "core").is_dir():
        return bundled

    checkout = package_dir.parent
    if (checkout / "core").is_dir():
        return checkout

    msg = (
        "Cannot locate framework files (core/). "
        "Reinstall: uv tool install --force <path-to-devflow-clone>. "
        "Or set DEVFLOW_FRAMEWORK_ROOT to a devflow repo, "
        "or run: uv run --project <devflow-clone> devflow-ai install ..."
    )
    raise FileNotFoundError(msg)


def copy_tree(source: Path, dest: Path) -> None:
    if not source.is_dir():
        raise FileNotFoundError(f"Missing source: {source}")
    dest.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def seed_context_contracts(
    framework: Path,
    context_root: Path,
    *,
    context_name: str,
) -> list[str]:
    """Copy core/contracts reference schemas into the context directory."""
    source = framework / "core" / "contracts"
    if not source.is_dir():
        raise FileNotFoundError(f"Missing {source}")

    dest = context_root / "contracts"
    dest.mkdir(parents=True, exist_ok=True)
    lines = [f"Synced core/contracts -> {context_name}/contracts/"]

    for item in sorted(source.iterdir()):
        if not item.is_file():
            continue
        target = dest / item.name
        if item.suffix in {".yaml", ".yml", ".md"}:
            text = item.read_text(encoding="utf-8")
            target.write_text(
                materialize_context_paths(text, context_name),
                encoding="utf-8",
            )
        else:
            shutil.copy2(item, target)
        lines.append(f"  {item.name}")

    return lines


def sync_artifacts(
    framework: Path,
    *,
    skills_dest: Path,
    agents_dest: Path | None,
    prune_stale: bool,
    context_dir: str | None = None,
) -> list[str]:
    """Mirror core/skills and core/AGENTS.md into agent-specific paths."""
    core_agents = framework / "core" / "AGENTS.md"
    core_skills = framework / "core" / "skills"

    if not core_agents.is_file():
        raise FileNotFoundError(f"Missing {core_agents}")
    if not core_skills.is_dir():
        raise FileNotFoundError(f"Missing {core_skills}")

    lines: list[str] = []

    if agents_dest is not None:
        agents_dest.parent.mkdir(parents=True, exist_ok=True)
        agents_text = core_agents.read_text(encoding="utf-8")
        if context_dir is not None:
            agents_text = materialize_context_paths(agents_text, context_dir)
        agents_dest.write_text(agents_text, encoding="utf-8")
        lines.append(f"Synced {core_agents} -> {agents_dest}")

    skills_dest.mkdir(parents=True, exist_ok=True)
    keep: set[str] = set()

    for skill_dir in sorted(core_skills.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            continue
        name = skill_dir.name
        dest_dir = skills_dest / name
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        shutil.copytree(skill_dir, dest_dir)
        skill_text = skill_md.read_text(encoding="utf-8")
        if context_dir is not None:
            skill_text = materialize_context_paths(skill_text, context_dir)
        (dest_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")
        keep.add(name)
        lines.append(f"Synced skill: {name}")

    if prune_stale:
        for existing in skills_dest.iterdir():
            if existing.is_dir() and existing.name not in keep:
                shutil.rmtree(existing)
                lines.append(f"Removed stale skill: {existing.name}")

        for existing in skills_dest.iterdir():
            if not existing.is_dir():
                continue
            nested = existing / existing.name
            if nested.is_dir():
                shutil.rmtree(nested)
                lines.append(f"Removed nested duplicate: {nested}")
    else:
        lines.append("Left existing user skills unchanged")

    lines.append("Done. Canonical sources: core/")
    return lines


def _seed_claude_md(target: Path, lines: list[str]) -> None:
    """Point Claude Code at the mirrored harness without duplicating content."""
    claude_md = target / "CLAUDE.md"
    if claude_md.exists():
        return
    claude_md.write_text("@.claude/AGENTS.md\n", encoding="utf-8")
    lines.append("Seeded CLAUDE.md -> @.claude/AGENTS.md")


def _sync_repo_agent(
    target: Path,
    framework: Path,
    agent: AgentSpec,
    *,
    context_dir: str,
) -> list[str]:
    agents_dest = agent.repo_agents_path(target)
    if target == framework and agent.id == "copilot":
        lines = [
            "Framework repo detected - skipping root AGENTS.md copy",
            "  (this repo keeps a thin root AGENTS.md; harness is in core/AGENTS.md)",
        ]
        agents_dest = None
    else:
        lines = []

    lines.extend(
        _sync_scope(
            agent,
            skills_dest=agent.repo_skills_dir(target),
            agents_dest=agents_dest,
            prune_stale=True,
            framework=framework,
            context_dir=context_dir,
        ),
    )
    if isinstance(agent, MirrorAgentSpec) and agent.id == "claude":
        _seed_claude_md(target, lines)
    return lines


def _sync_global_agent(framework: Path, agent: AgentSpec) -> list[str]:
    return _sync_scope(
        agent,
        skills_dest=agent.global_skills_dir(),
        agents_dest=agent.global_agents_path(),
        prune_stale=False,
        framework=framework,
    )


def _sync_scope(
    agent: AgentSpec,
    *,
    skills_dest: Path,
    agents_dest: Path | None,
    prune_stale: bool,
    framework: Path,
    context_dir: str | None = None,
) -> list[str]:
    lines = [
        f"Syncing {agent.display_name} artifacts:",
        f"  skills -> {skills_dest}",
    ]
    if agents_dest is not None:
        lines.append(f"  harness -> {agents_dest}")
    lines.extend(
        sync_artifacts(
            framework,
            skills_dest=skills_dest,
            agents_dest=agents_dest,
            prune_stale=prune_stale,
            context_dir=context_dir,
        ),
    )
    return lines


def install_repo(
    target: Path,
    *,
    agent_id: str,
    context_dir: str | None = None,
) -> list[str]:
    """Attach devflow to a target repository. Returns log lines."""
    agent = get_agent(agent_id)
    framework = framework_root()
    target = target.resolve()
    lines = [
        f"Installing devflow for {agent.display_name} into repository: {target}",
    ]

    if target == framework:
        lines.append("Framework repo detected - skipping core/adapters copy")
    else:
        copy_tree(framework / "core", target / "core")
        copy_tree(framework / "adapters", target / "adapters")

    manifest = target / CONTEXT_MANIFEST
    if context_dir is not None:
        write_context_manifest(target, context_dir.strip())
        lines.append(f"Set {CONTEXT_MANIFEST} context_dir: {context_dir.strip()}")
    elif not manifest.exists():
        write_context_manifest(target, resolve_context_dir(target))
        lines.append(
            f"Seeded {CONTEXT_MANIFEST} (context_dir: {resolve_context_dir(target)})",
        )

    context_name = resolve_context_dir(target)
    lines.append(f"Context directory: {context_name}")
    context_root = target / context_name
    context_root.mkdir(parents=True, exist_ok=True)

    spec = context_root / "SPEC.md"
    if not spec.exists():
        shutil.copy2(framework / "core" / "templates" / "SPEC.template.md", spec)
        lines.append(f"Seeded {context_name}/SPEC.md from template")

    state = context_root / "PROJECT_STATE.md"
    if not state.exists():
        shutil.copy2(
            framework / "core" / "templates" / "PROJECT_STATE.template.md",
            state,
        )
        lines.append(f"Seeded {context_name}/PROJECT_STATE.md from template")

    lines.extend(seed_context_contracts(framework, context_root, context_name=context_name))

    lines.extend(_sync_repo_agent(target, framework, agent, context_dir=context_name))
    lines.extend(_repo_next_steps(agent, context_name))
    return lines


def install_global(*, agent_id: str) -> list[str]:
    """Install devflow skills for all projects of an agent (user-level)."""
    agent = get_agent(agent_id)
    framework = framework_root()
    lines = [
        f"Installing devflow for {agent.global_scope_label()}",
    ]
    lines.extend(_sync_global_agent(framework, agent))
    lines.extend(
        [
            "",
            "Install complete.",
            "",
            "Next steps:",
            f"  1. Open any project in {agent.display_name} - devflow slash commands are available.",
            f"  2. For per-repo {resolve_context_dir()}/ files and framework core, run:",
            f"       devflow-ai {agent_id} install --scope repo",
            f"  3. Read adapters/{agent_id}/README.md for discovery details.",
        ]
    )
    return lines


def install(
    target: Path,
    *,
    scope: InstallScope,
    agent_id: str,
    context_dir: str | None = None,
) -> list[str]:
    """Install devflow for the chosen scope and agent."""
    if scope == InstallScope.GLOBAL:
        return install_global(agent_id=agent_id)
    return install_repo(target, agent_id=agent_id, context_dir=context_dir)


def _repo_next_steps(agent: AgentSpec, context_name: str) -> list[str]:
    return [
        "",
        "Install complete.",
        "",
        "Next steps:",
        f"  1. Edit {context_name}/SPEC.md for your product (or run /grillme).",
        f"  2. Read core/AGENTS.md and adapters/{agent.id}/README.md.",
        "  3. Follow the workflow in docs/GETTING_STARTED.md.",
    ]
