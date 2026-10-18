#!/usr/bin/env bash
# update_repos.sh - Pull latest commits for all open-source OLake repositories
set -e

echo "========================================================"
echo "🔄 Updating OLake Open-Source Repositories"
echo "========================================================"

REPOS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/repos" && pwd)"

for repo in "$REPOS_DIR"/*; do
  if [ -d "$repo/.git" ]; then
    repo_name=$(basename "$repo")
    echo -n "Fetching updates for $repo_name... "
    git -C "$repo" fetch --depth=1 origin 2>/dev/null || git -C "$repo" fetch origin 2>/dev/null
    git -C "$repo" reset --hard origin/HEAD >/dev/null 2>&1 || git -C "$repo" reset --hard origin/master >/dev/null 2>&1 || git -C "$repo" reset --hard origin/main >/dev/null 2>&1
    commit_hash=$(git -C "$repo" rev-parse --short HEAD)
    echo "✅ Updated (HEAD: $commit_hash)"
  fi
done

echo "--------------------------------------------------------"
echo "✅ All repositories updated to latest upstream commits!"
echo "Next loop rounds and queries will immediately use these changes."
echo "========================================================"
