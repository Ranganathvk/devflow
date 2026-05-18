#!/usr/bin/env bash
# Attach agentic-dev-os to a consumer repository.
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

echo "Installing agentic-dev-os into: $TARGET"

copy_tree "$FRAMEWORK_ROOT/core" "$TARGET/core"
copy_tree "$FRAMEWORK_ROOT/adapters" "$TARGET/adapters"

mkdir -p "$TARGET/AI_CONTEXT"
if [[ ! -f "$TARGET/AI_CONTEXT/SPEC.md" ]]; then
  cp "$FRAMEWORK_ROOT/core/templates/SPEC.template.md" "$TARGET/AI_CONTEXT/SPEC.md"
  echo "Seeded AI_CONTEXT/SPEC.md"
fi
if [[ ! -f "$TARGET/AI_CONTEXT/PROJECT_STATE.md" ]]; then
  cp "$FRAMEWORK_ROOT/core/templates/PROJECT_STATE.template.md" "$TARGET/AI_CONTEXT/PROJECT_STATE.md"
  echo "Seeded AI_CONTEXT/PROJECT_STATE.md"
fi

REPO_ROOT="$TARGET" "$FRAMEWORK_ROOT/installer/sync-cursor.sh"

cat <<EOF

Install complete.

Next steps:
  1. Edit AI_CONTEXT/SPEC.md (or run /grillme in Cursor).
  2. Read core/AGENTS.md and adapters/cursor/README.md.
  3. Follow the workflow in docs/GETTING_STARTED.md.

EOF
