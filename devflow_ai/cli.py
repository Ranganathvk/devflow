"""Command-line entry point for devflow-ai."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from devflow_ai import __version__
from devflow_ai import installer
from devflow_ai.agents import AGENTS, AgentSpec
from devflow_ai.installer import InstallScope

app = typer.Typer(
    name="devflow-ai",
    help=(
        "AI-assisted software engineering workflow framework.\n\n"
        "Quick start:\n"
        "  devflow-ai install --scope repo\n"
        "  devflow-ai install --scope repo --agent cursor\n"
        "  devflow-ai cursor install --scope repo"
    ),
    no_args_is_help=True,
)
console = Console()

PathOption = Annotated[
    Path,
    typer.Option(
        "--path",
        "-p",
        help="Target repository path (used with --scope repo).",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
]
ScopeOption = Annotated[
    InstallScope | None,
    typer.Option(
        "--scope",
        "-s",
        help="Install scope: repo (this project) or global (all projects).",
        case_sensitive=False,
    ),
]
ContextDirOption = Annotated[
    str | None,
    typer.Option(
        "--context-dir",
        "-c",
        help="Workflow context folder name (repo install only). Default: artifacts.",
    ),
]
AgentOption = Annotated[
    str,
    typer.Option(
        "--agent",
        "-a",
        help="Coding agent: cursor, claude, or copilot.",
        case_sensitive=False,
    ),
]


@app.command()
def version() -> None:
    """Print the installed devflow-ai version."""
    console.print(f"devflow-ai {__version__}")


@app.command("install")
def install_command(
    scope: ScopeOption = InstallScope.REPO,
    agent: AgentOption = "cursor",
    path: PathOption = Path.cwd(),
    context_dir: ContextDirOption = None,
) -> None:
    """Attach devflow to a repository or install skills for all projects."""
    agent_id = agent.strip().lower()
    if agent_id not in AGENTS:
        known = ", ".join(sorted(AGENTS))
        console.print(f"[red]Error:[/red] Unknown agent {agent!r}. Supported: {known}")
        raise typer.Exit(code=1)
    _run_install(agent_id, path, scope, context_dir)


def _prompt_scope(agent: AgentSpec, target: Path) -> InstallScope:
    mirror = (
        f"{agent.repo_skills_dir(target).parent}/"
        if agent.id != "copilot"
        else ".github/ and AGENTS.md"
    )
    global_skills = agent.global_skills_dir()

    console.print()
    console.print(
        f"[bold]Where should devflow be installed for {agent.display_name}?[/bold]",
    )
    console.print()
    console.print("  [1] This repository")
    console.print("      Framework files, artifacts, and agent artifacts in the target repo")
    console.print(f"      Target: [cyan]{target}[/cyan]")
    console.print(f"      Artifacts: [cyan]{mirror}[/cyan]")
    console.print()
    console.print(f"  [2] {agent.global_scope_label()}")
    console.print(f"      Skills and harness in [cyan]{global_skills.parent}[/cyan]")
    console.print()

    while True:
        choice = typer.prompt("Choose 1 or 2", default="1").strip().lower()
        if choice in {"1", "repo", "repository", "this repo", "this repository"}:
            return InstallScope.REPO
        if choice in {"2", "global", "all", "user"}:
            return InstallScope.GLOBAL
        console.print("[red]Please enter 1 (repository) or 2 (all projects).[/red]")


def _run_install(
    agent_id: str,
    path: Path,
    scope: InstallScope | None,
    context_dir: str | None,
) -> None:
    agent = AGENTS[agent_id]
    chosen = scope if scope is not None else _prompt_scope(agent, path)

    try:
        for line in installer.install(
            path,
            scope=chosen,
            agent_id=agent_id,
            context_dir=context_dir if chosen == InstallScope.REPO else None,
        ):
            console.print(line)
    except (FileNotFoundError, ValueError) as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from None


def _register_agent_install(agent_id: str, agent_app: typer.Typer) -> None:
    @agent_app.command("install")
    def agent_install_command(
        scope: ScopeOption = InstallScope.REPO,
        path: PathOption = Path.cwd(),
        context_dir: ContextDirOption = None,
    ) -> None:
        """Attach devflow to a repository or install skills for all projects."""
        _run_install(agent_id, path, scope, context_dir)


for _agent_id in AGENTS:
    _agent_app = typer.Typer(help=f"{AGENTS[_agent_id].display_name} adapter commands.")
    app.add_typer(_agent_app, name=_agent_id)
    _register_agent_install(_agent_id, _agent_app)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
