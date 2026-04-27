#!/usr/bin/env bash
set -euo pipefail

ROOT="/root/.openclaw/workspace"
PRODUCT_DIR="$ROOT/nofix-finance"
VERSION_FILE="$PRODUCT_DIR/VERSION"
CHANGELOG_FILE="$PRODUCT_DIR/CHANGELOG.md"

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <new-version> <release-note-summary>"
  echo "Example: $0 0.1.1 'fix: improve XP card consolidation'"
  exit 1
fi

NEW_VERSION="$1"
shift
SUMMARY="$*"
TODAY="$(date -u +%Y-%m-%d)"

cd "$ROOT"

if [[ ! -f "$VERSION_FILE" ]]; then
  echo "VERSION file not found: $VERSION_FILE"
  exit 1
fi

CURRENT_VERSION="$(cat "$VERSION_FILE" | tr -d '[:space:]')"

echo "Current version: $CURRENT_VERSION"
echo "New version: $NEW_VERSION"

printf '%s\n' "$NEW_VERSION" > "$VERSION_FILE"

TMP_FILE="$(mktemp)"
{
  echo "# CHANGELOG - Nofix Finance"
  echo
  echo "Todas as mudanças relevantes do produto devem ser registradas aqui."
  echo
  echo "O formato segue uma convenção simples inspirada em Semantic Versioning."
  echo
  echo "## [$NEW_VERSION] - $TODAY"
  echo "### release"
  echo "- $SUMMARY"
  echo
  tail -n +6 "$CHANGELOG_FILE"
} > "$TMP_FILE"
mv "$TMP_FILE" "$CHANGELOG_FILE"

git add nofix-finance/VERSION nofix-finance/CHANGELOG.md nofix-finance/scripts/release.sh
if ! git diff --cached --quiet; then
  git commit -m "Release Nofix $NEW_VERSION"
fi

bash "$PRODUCT_DIR/scripts/publish_github.sh"

echo "Release completed: $NEW_VERSION"
