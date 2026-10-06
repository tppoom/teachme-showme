#!/usr/bin/env bash
# Install TeachMe and ShowMe as personal (global) skills for whichever of
# Claude Code, Codex CLI and Antigravity are set up on this machine.
#
# Usage:  ./install.sh               skills + CAS mode (Claude Code commands/agents)
#         ./install.sh --skills-only  skills only
#
# Two ways to run each skill once installed:
#   plain skill — /teachme, /showme (or just describe the task) — Claude Code, Codex, Antigravity
#   CAS mode    — /teachme-cas, /showme-cas — Claude Code only: Command → Agent → Skill,
#                 with parallel authors and a reviewer. Links each file from cas/*/commands
#                 into ~/.claude/commands/ and cas/*/agents into ~/.claude/agents/.
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
SKILLS_ONLY=0; [ "${1:-}" = "--skills-only" ] && SKILLS_ONLY=1
linked=() skipped=() no_target=()

# link one file into dir, with the same never-clobber rules as link_into
link_file() {
  local src="$1" dir="$2" label="$3"
  local dest="$dir/$(basename "$src")"
  if [ -L "$dest" ]; then
    if [ "$(readlink "$dest")" = "$src" ]; then return
    elif [ -e "$dest" ]; then skipped+=("$label/$(basename "$src") (points elsewhere: $(readlink "$dest"))"); return
    fi
  elif [ -e "$dest" ]; then
    skipped+=("$label/$(basename "$src") (already a real file, not a symlink)"); return
  fi
  ln -sfn "$src" "$dest"
  linked+=("$label/$(basename "$src")")
}

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

# Claude Code — CAS mode: the orchestrator commands and the agents they dispatch
if [ -d "$HOME/.claude" ] && [ "$SKILLS_ONLY" = 0 ]; then
  for kind in commands agents; do
    mkdir -p "$HOME/.claude/$kind" 2>/dev/null || { no_target+=("~/.claude/$kind"); continue; }
    for name in "${SKILLS[@]}"; do
      for f in "$REPO/cas/$name/$kind"/*.md; do
        [ -f "$f" ] && link_file "$f" "$HOME/.claude/$kind" "~/.claude/$kind"
      done
    done
  done
fi

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
echo "Repo-local use needs no install at all — .claude/skills/, .claude/commands/,"
echo ".claude/agents/ and .agents/skills/ in this checkout already point at the sources."
echo
echo "Use:  /teachme or /showme      — plain skill (any tool)"
echo "      /teachme-cas /showme-cas — CAS mode: parallel agents + reviewer (Claude Code)"
echo
echo "Windows note: if these turned into plain text files instead of real"
echo "symlinks/directories, your git checkout has symlinks disabled. Run"
echo "  git config --global core.symlinks true"
echo "(with Developer Mode on, or as Administrator), then re-clone and re-run"
echo "this script — or under WSL, which handles symlinks natively."
