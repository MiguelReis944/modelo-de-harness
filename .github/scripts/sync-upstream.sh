#!/usr/bin/env bash
# Copy only reusable infrastructure from a fetched upstream commit.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
ref=$(git rev-parse --verify "${1:-refs/remotes/upstream/main}^{commit}")

if [[ -n $(git status --porcelain) ]]; then
  echo "Working tree must be clean before synchronizing." >&2
  exit 1
fi
if [[ $(sed '/^[[:space:]]*#/d; /^[[:space:]]*$/d' workspace.yaml) != 'projects: []' ]] ||
   [[ -n $(git ls-files -- .gitmodules workspace) ]]; then
  echo "Synchronization requires an empty template workspace." >&2
  exit 1
fi

# A positive list prevents new project-specific root files from becoming public.
# README, AGENTS.md, .github, workspace and curated vault content belong to the template.
paths=(
  .gitattributes .gitignore LICENSE harness.config.yaml
  agents bin catalog hooks mcp templates tests vault/_meta
)

# Union includes removed files, so restore also deletes obsolete infrastructure.
# NUL separators support spaces; Git preserves executable bits in the index.
{
  git ls-tree -r -z --name-only "$ref" -- "${paths[@]}"
  git ls-files -z -- "${paths[@]}"
} | sort -zu | git --literal-pathspecs restore --source="$ref" --staged --worktree \
  --pathspec-from-file=- --pathspec-file-nul

echo "Infrastructure synchronized from $ref (changes staged)."
