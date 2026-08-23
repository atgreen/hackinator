#!/usr/bin/env bash
# Install hackinator skills for BOTH Claude Code and Codex, globally (all projects).
#
# Claude Code loads personal skills from ~/.claude/skills/<name>/SKILL.md
# Codex     loads personal skills from ~/.codex/skills/<name>/SKILL.md
# Both use the identical SKILL.md format, so we symlink each skill into both trees.
# Symlinks (not copies) mean edits in this repo take effect immediately.
#
# Usage:  ./install.sh            # install into both runtimes
#         ./install.sh --claude   # only Claude Code
#         ./install.sh --codex    # only Codex
#         ./install.sh --uninstall# remove hackinator's symlinks from both trees
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
SKILLS_SRC="$REPO/skills"

CLAUDE_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
CODEX_DIR="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"

do_claude=1 do_codex=1 uninstall=0
case "${1:-}" in
  --claude) do_codex=0 ;;
  --codex)  do_claude=0 ;;
  --uninstall) uninstall=1 ;;
  "" ) ;;
  * ) echo "unknown arg: $1" >&2; exit 2 ;;
esac

link_into() {
  local dest_root="$1"; local runtime="$2"
  [ -d "$dest_root" ] || { mkdir -p "$dest_root"; echo "created $dest_root"; }
  for src in "$SKILLS_SRC"/*/; do
    local name; name="$(basename "$src")"
    local dest="$dest_root/$name"
    if [ -L "$dest" ]; then
      # already a symlink — repoint if it's ours or stale, else leave foreign links alone
      local cur; cur="$(readlink "$dest")"
      case "$cur" in
        "$REPO"/*) ln -sfn "${src%/}" "$dest"; echo "  [$runtime] ok    $name" ;;
        *) echo "  [$runtime] SKIP  $name (symlink points elsewhere: $cur)" ;;
      esac
    elif [ -e "$dest" ]; then
      echo "  [$runtime] SKIP  $name (a real file/dir already exists there)"
    else
      ln -sfn "${src%/}" "$dest"; echo "  [$runtime] link  $name"
    fi
  done
}

unlink_from() {
  local dest_root="$1"; local runtime="$2"
  [ -d "$dest_root" ] || return 0
  for src in "$SKILLS_SRC"/*/; do
    local name; name="$(basename "$src")"
    local dest="$dest_root/$name"
    if [ -L "$dest" ] && case "$(readlink "$dest")" in "$REPO"/*) true;; *) false;; esac; then
      rm "$dest"; echo "  [$runtime] unlink $name"
    fi
  done
}

if [ "$uninstall" = 1 ]; then
  echo "Uninstalling hackinator symlinks..."
  unlink_from "$CLAUDE_DIR" claude
  unlink_from "$CODEX_DIR" codex
  echo "Done."
  exit 0
fi

echo "Installing hackinator skills from $REPO"
[ "$do_claude" = 1 ] && { echo "→ Claude Code ($CLAUDE_DIR)"; link_into "$CLAUDE_DIR" claude; }
[ "$do_codex"  = 1 ] && { echo "→ Codex ($CODEX_DIR)";      link_into "$CODEX_DIR"  codex; }
echo
echo "Done. New shells / sessions will discover the skills."
echo "Tip: for the 'always use beads' rule, run 'bd onboard' and add its snippet to your global"
echo "     instructions (~/.claude/CLAUDE.md and ~/.codex/AGENTS.md)."
