param(
    [string]$Database = "C:\wasser-market-agent\data\wasser_market.db",
    [int]$Limit = 10,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$Repo = Split-Path -Parent $PSScriptRoot
$Lock = Join-Path $env:TEMP "wasser-market-agent-auto-import.lock"

if (Test-Path -LiteralPath $Lock) { throw "Agent import is already running." }
try {
    Set-Content -LiteralPath $Lock -Value $PID -Encoding ascii
    Set-Location $Repo
    if ((git status --porcelain).Length -ne 0) { throw "Website repository has uncommitted changes." }
    git checkout main
    git pull --ff-only origin main

    $Arguments = @("scripts/agent-auto-import.py", "--db", $Database, "--limit", $Limit)
    if (-not $DryRun) { $Arguments += "--apply" }
    python @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Agent import validation failed." }
    if ($DryRun) { exit 0 }

    python -m json.tool data/products.json | Out-Null
    python -m json.tool data/brands.json | Out-Null
    python scripts/validate-agent-import.py
    node --check assets/app.js
    if ($LASTEXITCODE -ne 0) { throw "Generated site validation failed." }

    $Changed = git status --porcelain
    if (-not $Changed) { Write-Host "No new PUBLISH_READY products."; exit 0 }
    git add assets/app.js brands data index.html products products.html sitemap.xml scripts/agent-auto-import.py scripts/agent-auto-publish.ps1 scripts/validate-agent-import.py scripts/AGENT-AUTO-IMPORT.md
    $Count = (Get-Content data/agent-import-report.json -Raw | ConvertFrom-Json).accepted.Count
    git commit -m "Auto-import $Count reviewed agent products"
    git push origin main
}
finally {
    Remove-Item -LiteralPath $Lock -Force -ErrorAction SilentlyContinue
}
