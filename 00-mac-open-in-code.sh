#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"

if ! command -v code >/dev/null 2>&1; then
  echo "The VS Code 'code' shell command is required. Install it, then retry." >&2
  exit 1
fi

exec code "$repo_root"
