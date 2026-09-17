#!/usr/bin/env bash
# Install TeachMe and ShowMe as personal (global) skills for whichever of
# Claude Code, Codex CLI and Antigravity are set up on this machine.
#
# Usage:  ./install.sh
#
# You do NOT need this script just to try the skills: opening this cloned
# repo directly in Claude Code, Codex or Antigravity already works, because
# .claude/skills/ and .agents/skills/ inside the repo point at skills/*.
# This script instead links them into your *personal* config directories so
# they're available in every project, not just this one.
#
# Safe to re-run. Never overwrites a real (non-symlink) directory or a
# symlink that already points somewhere else — it reports those and leaves
# them alone so you can decide by hand.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
REPO="$(pwd -P)"
SKILLS=(teachme showme)
linked=() skipped=() no_target=()

link_into() {
  local base="$1" label="$2"
  local dir="$base/skills"
  mkdir -p "$dir" 2>/dev/null || { no_target+=("$label"); return; }
  for name in "${SKILLS[@]}"; do
    local dest="$dir/$name" src="$REPO/skills/$name"
    if [ -L "$dest" ]; then
      if [ "$(readlink "$dest")" = "$src" ]; then continue
      elif [ -e "$dest" ]; then skipped+=("$label/skills/$name (points elsewhere: $(readlink "$dest"))"); continue
      fi   # broken symlink (e.g. from a git checkout with core.symlinks=false) — fall through and replace it
    elif [ -e "$dest" ]; then
      skipped+=("$label/skills/$name (already a real file/dir, not a symlink)"); continue
    fi
    ln -sfn "$src" "$dest"
    linked+=("$label/skills/$name")
  done
}

# Claude Code — personal skills
[ -d "$HOME/.claude" ] && link_into "$HOME/.claude" "~/.claude"

# Codex CLI and any other agentskills.io-compliant tool — the shared personal path
link_into "$HOME/.agents" "~/.agents"

# Antigravity — the global path has moved at least once during 2026; link into
# every variant we've seen documented so whichever your version reads, it works.
# Harmless if a path is unused: it's just an extra symlink nobody reads.
if [ -d "$HOME/.gemini" ]; then
  for variant in antigravity-cli antigravity; do
    [ -d "$HOME/.gemini/$variant" ] || mkdir -p "$HOME/.gemini/$variant" 2>/dev/null || continue
    link_into "$HOME/.gemini/$variant" "~/.gemini/$variant"
  done
fi

echo "TeachMe + ShowMe installer"
echo "=========================="
if [ ${#linked[@]} -gt 0 ]; then
  echo "Linked:"; printf '  %s\n' "${linked[@]}"
else
  echo "Nothing new to link."
fi
if [ ${#skipped[@]} -gt 0 ]; then
  echo "Skipped (already present, left as-is):"; printf '  %s\n' "${skipped[@]}"
fi
if [ ${#no_target[@]} -gt 0 ]; then
  echo "No writable config dir for: ${no_target[*]}"
fi
echo
echo "Repo-local use needs no install at all — .claude/skills/ and .agents/skills/"
echo "in this checkout already point at skills/teachme and skills/showme."
echo
echo "Windows note: if these turned into plain text files instead of real"
echo "symlinks/directories, your git checkout has symlinks disabled. Run"
echo "  git config --global core.symlinks true"
echo "(with Developer Mode on, or as Administrator), then re-clone and re-run"
echo "this script — or under WSL, which handles symlinks natively."
