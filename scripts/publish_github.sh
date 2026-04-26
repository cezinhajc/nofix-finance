#!/usr/bin/env bash
set -euo pipefail

ROOT="/root/.openclaw/workspace"
PREFIX="nofix-finance"
BRANCH="nofix-finance-publish"
REMOTE_URL="https://github.com/cezinhajc/nofix-finance.git"
TARGET_BRANCH="main"

cd "$ROOT"

echo "[1/4] Creating subtree branch from $PREFIX..."
git subtree split --prefix="$PREFIX" -b "$BRANCH"

echo "[2/4] Ensuring temporary remote..."
if git remote get-url nofix-publish >/dev/null 2>&1; then
  git remote set-url nofix-publish "$REMOTE_URL"
else
  git remote add nofix-publish "$REMOTE_URL"
fi

echo "[3/4] Pushing subtree to GitHub..."
git push nofix-publish "$BRANCH":"$TARGET_BRANCH"

echo "[4/4] Done."
echo "Published $PREFIX to $REMOTE_URL ($TARGET_BRANCH)"
