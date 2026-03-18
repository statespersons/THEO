#!/bin/bash
set -ea
export PATH="/root/.opencode/bin:/root/.local/bin:$PATH"
cd "$(dirname "$0")"
source .env
set +a
git config user.name "Theo"
git config user.email "theo@agent"
git remote set-url origin "https://x-access-token:${REPO_PAT}@github.com/${REPO}.git"
git pull --rebase
PROMPT="${1:-FREE}"
TIME=$(TZ='America/Los_Angeles' date '+%Y-%m-%d %H:%M %Z')
BALANCE=$(uv run scripts/check_balance.py 2>/dev/null || echo "unknown")
opencode run "[$TIME | $BALANCE] $PROMPT. Read AGENTS.md."
git add -A && git commit -m "$(date +%Y%m%d-%H%M) $PROMPT" || true
git push
uv run scripts/sync_secrets.py "$REPO"
