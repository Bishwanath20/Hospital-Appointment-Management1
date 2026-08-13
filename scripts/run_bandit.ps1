# PowerShell runner for Bandit (Windows-friendly).
param()

Write-Output "Running Bandit (excluding .venv and alembic)..."

$banditCmd = "python -m bandit -r . -ll -f json -o bandit.json -x .venv,alembic"
Write-Output "Command: $banditCmd"

Invoke-Expression $banditCmd

Write-Output "Bandit JSON output written to: $(Resolve-Path bandit.json)"
