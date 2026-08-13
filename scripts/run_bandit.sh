#!/usr/bin/env bash
# Run Bandit for the project, excluding .venv and alembic by default.
set -euo pipefail

bandit -r . -ll -f json -o bandit.json -x .venv,alembic

echo "Bandit JSON output written to bandit.json"
