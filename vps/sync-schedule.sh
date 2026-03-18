#!/bin/bash
# Reads calendar/schedule.txt and installs crontab entries that trigger
# GitHub repository_dispatch with the prompt word.
# Requires .env to have REPO_PAT and REPO set.
set -e
cd "$(dirname "$0")/.."
source .env

uv run scripts/sync_schedule.py calendar/schedule.txt
