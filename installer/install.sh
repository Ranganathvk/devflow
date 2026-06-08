#!/usr/bin/env bash
# Attach devflow to a consumer repository.
# Usage: ./installer/install.sh /path/to/your-app

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <target-repo-path>" >&2
  exit 1
fi

TARGET="$(cd "$1" && pwd)"
FRAMEWORK_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

copy_tree() {
  local src="$1" dest="$2"
  [[ -d "$src" ]] || { echo "Missing $src" >&2; exit 1; }
  mkdir -p "$dest"
  cp -R "$src"/. "$dest"/
}

resolve_context_dir() {
  if [[ -n "${DEVFLOW_CONTEXT_DIR:-}" ]]; then
    echo "$DEVFLOW_CONTEXT_DIR"
    return
  fi
  local manifest="$TARGET/devflow.context.yaml"
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

echo "Installing devflow into: $TARGET"

copy_tree "$FRAMEWORK_ROOT/core" "$TARGET/core"
copy_tree "$FRAMEWORK_ROOT/adapters" "$TARGET/adapters"

CONTEXT_DIR="$(resolve_context_dir)"
mkdir -p "$TARGET/$CONTEXT_DIR"

if [[ ! -f "$TARGET/devflow.context.yaml" ]]; then
  cp "$FRAMEWORK_ROOT/core/templates/devflow.context.template.yaml" "$TARGET/devflow.context.yaml"
  echo "Seeded devflow.context.yaml (context_dir: $CONTEXT_DIR)"
fi

if [[ ! -f "$TARGET/$CONTEXT_DIR/SPEC.md" ]]; then
  cp "$FRAMEWORK_ROOT/core/templates/SPEC.template.md" "$TARGET/$CONTEXT_DIR/SPEC.md"
  echo "Seeded $CONTEXT_DIR/SPEC.md"
fi
if [[ ! -f "$TARGET/$CONTEXT_DIR/PROJECT_STATE.md" ]]; then
  cp "$FRAMEWORK_ROOT/core/templates/PROJECT_STATE.template.md" "$TARGET/$CONTEXT_DIR/PROJECT_STATE.md"
  echo "Seeded $CONTEXT_DIR/PROJECT_STATE.md"
fi

REPO_ROOT="$TARGET" "$FRAMEWORK_ROOT/installer/sync-cursor.sh"

cat <<EOF

Install complete.

Next steps:
  1. Edit $CONTEXT_DIR/SPEC.md (or run /grillme in Cursor).
  2. Read core/AGENTS.md and adapters/cursor/README.md.
  3. Follow the workflow in docs/GETTING_STARTED.md.

EOF
