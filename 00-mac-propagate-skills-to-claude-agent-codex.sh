#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
visual_language_skills=(kit lit pix dac dac-help cop wiz fix val act umm mem map tut dora)
documentation_standard_skills=(kit lit cop wiz fix val map tut dora)
skills=(nix kit lit pix dac dac-help cop wiz fix val act umm mem map tut gap)
agent_roots=("$HOME/.claude" "$HOME/.codex" "$HOME/.agents")

pause() {
  read -r -p "Press Enter to continue..." _
}

copy_reference() {
  local reference_name="$1"
  local skill
  shift

  for skill in "$@"; do
    mkdir -p "$repo_root/$skill/references"
    cp -pf "$repo_root/nix/references/$reference_name" "$repo_root/$skill/references/$reference_name"
  done
}

printf '%s\n' '*** Copying nix master visual-language.md to all skills ***'
pause
copy_reference visual-language.md "${visual_language_skills[@]}"

printf '%s\n' '*** Copying nix master documentation-standard.md to all applicable skills ***'
copy_reference documentation-standard.md "${documentation_standard_skills[@]}"

printf '%s\n' '*** Copying jira-fields.local.yaml to agent roots ***'
if [[ -f "$repo_root/jira-fields.local.yaml" ]]; then
  for agent_root in "${agent_roots[@]}"; do
    mkdir -p "$agent_root"
    cp -pf "$repo_root/jira-fields.local.yaml" "$agent_root/jira-fields.local.yaml"
  done
fi

printf '%s\n' '*** Copying all skills to .claude, .codex, and .agents ***'
pause
for skill in "${skills[@]}"; do
  for agent_root in "${agent_roots[@]}"; do
    mkdir -p "$agent_root/skills/$skill"
    rsync -a --delete "$repo_root/$skill/" "$agent_root/skills/$skill/"
  done
done

printf '%s\n' '*** Done ***'
pause
