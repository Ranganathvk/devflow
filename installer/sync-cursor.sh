#!/usr/bin/env bash
# Sync canonical core/ artifacts into .cursor/ for Cursor (derived mirror).
# Edit sources under core/ only — then run: ./installer/sync-cursor.sh

set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
CORE_AGENTS="$REPO_ROOT/core/AGENTS.md"
CURSOR_AGENTS="$REPO_ROOT/.cursor/AGENTS.md"
CORE_SKILLS="$REPO_ROOT/core/skills"
CURSOR_SKILLS="$REPO_ROOT/.cursor/skills"

resolve_context_dir() {
  if [[ -n "${DEVFLOW_CONTEXT_DIR:-}" ]]; then
    echo "$DEVFLOW_CONTEXT_DIR"
    return
  fi
  local manifest="$REPO_ROOT/devflow.context.yaml"
  if [[ -f "$manifest" ]]; then
    local value
    value="$(grep -E '^context_dir:' "$manifest" | head -1 | sed -E 's/^context_dir:[[:space:]]*//' | tr -d "\"'")"
    if [[ -n "$value" ]]; then
      echo "$value"
      return
    fi
  fi
  echo "artifacts"
}

expand_context_paths() {
  local content="$1"
  local context_dir="$2"
  content="${content//\{context_dir\}\//$context_dir/}"
  echo "${content//@\{context_dir\}\//@$context_dir/}"
}

CONTEXT_DIR="$(resolve_context_dir)"

[[ -f "$CORE_AGENTS" ]] || { echo "Missing $CORE_AGENTS" >&2; exit 1; }
[[ -d "$CORE_SKILLS" ]] || { echo "Missing $CORE_SKILLS" >&2; exit 1; }

mkdir -p "$(dirname "$CURSOR_AGENTS")"
expand_context_paths "$(cat "$CORE_AGENTS")" "$CONTEXT_DIR" > "$CURSOR_AGENTS"
echo "Synced core/AGENTS.md -> .cursor/AGENTS.md (context_dir: $CONTEXT_DIR)"

mkdir -p "$CURSOR_SKILLS"

for skill_dir in "$CORE_SKILLS"/*/; do
  [[ -d "$skill_dir" ]] || continue
  skill_md="${skill_dir}SKILL.md"
  [[ -f "$skill_md" ]] || continue
  name="$(basename "${skill_dir%/}")"
  dest_dir="$CURSOR_SKILLS/$name"
  mkdir -p "$dest_dir"
  expand_context_paths "$(cat "$skill_md")" "$CONTEXT_DIR" > "$dest_dir/SKILL.md"
  echo "Synced skill: $name"
done

# Remove stale top-level skills
for existing in "$CURSOR_SKILLS"/*/; do
  [[ -d "$existing" ]] || continue
  name="$(basename "${existing%/}")"
  if [[ ! -f "$CORE_SKILLS/$name/SKILL.md" ]]; then
    rm -rf "$existing"
    echo "Removed stale skill: $name"
  fi
done

# Remove nested duplicates
for existing in "$CURSOR_SKILLS"/*/; do
  [[ -d "$existing" ]] || continue
  name="$(basename "${existing%/}")"
  nested="$existing$name"
  if [[ -d "$nested" ]]; then
    rm -rf "$nested"
    echo "Removed nested duplicate: $nested"
  fi
done

echo "Done. Canonical sources: core/"
