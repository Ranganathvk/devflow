"""Devflow configuration (environment and repo-local overrides)."""

from __future__ import annotations

import os
from pathlib import Path

# Default workflow context directory when the user does not pass --context-dir or a manifest.
DEFAULT_CONTEXT_DIR = "artifacts"

# Package default; may reflect DEVFLOW_CONTEXT_DIR at import time. Prefer resolve_context_dir().
DEVFLOW_CONTEXT_DIR: str = os.environ.get("DEVFLOW_CONTEXT_DIR", DEFAULT_CONTEXT_DIR).strip()

CONTEXT_MANIFEST = "devflow.context.yaml"


def read_context_dir_from_manifest(repo_root: Path) -> str | None:
    """Read context_dir from repo-root devflow.context.yaml if present."""
    path = repo_root / CONTEXT_MANIFEST
    if not path.is_file():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("context_dir:"):
            value = stripped.split(":", 1)[1].strip()
            return value.strip("\"'")
    return None


def resolve_context_dir(repo_root: Path | None = None) -> str:
    """Resolve the workflow context directory name for a repository."""
    env = os.environ.get("DEVFLOW_CONTEXT_DIR", "").strip()
    if env:
        return env
    if repo_root is not None:
        manifest = read_context_dir_from_manifest(repo_root)
        if manifest:
            return manifest
    return DEFAULT_CONTEXT_DIR


def context_path(repo_root: Path) -> Path:
    """Absolute path to the workflow context directory in a repo."""
    return repo_root / resolve_context_dir(repo_root)


CONTEXT_DIR_TOKEN = "{context_dir}"


def materialize_context_paths(text: str, context_dir: str) -> str:
    """Replace ``{context_dir}/`` path prefixes with the resolved directory name."""
    text = text.replace(f"@{CONTEXT_DIR_TOKEN}/", f"@{context_dir}/")
    return text.replace(f"{CONTEXT_DIR_TOKEN}/", f"{context_dir}/")


def write_context_manifest(repo_root: Path, context_dir: str) -> None:
    """Write or update repo-root devflow.context.yaml with the given context_dir."""
    manifest = repo_root / CONTEXT_MANIFEST
    lines: list[str] = []
    if manifest.is_file():
        replaced = False
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if line.strip().startswith("context_dir:"):
                lines.append(f"context_dir: {context_dir}")
                replaced = True
            else:
                lines.append(line)
        if not replaced:
            lines.append(f"context_dir: {context_dir}")
    else:
        lines = [
            "# Devflow workflow context directory for this repository.",
            "# Override with environment variable DEVFLOW_CONTEXT_DIR.",
            f"context_dir: {context_dir}",
        ]
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
