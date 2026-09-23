param(
    [string]$Database = "C:\wasser-market-agent\data\wasser_market.db",
    [int]$Limit = 10,
    [int]$ProductId = 0,
    [switch]$DryRun,
    [string]$GitExe = "C:\Users\myuae\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe",
    [string]$PythonExe = "C:\Python314\python.exe",
    [string]$NodeExe = "C:\Program Files\nodejs\node.exe"
)

$ErrorActionPreference = "Stop"
$Repo = Split-Path -Parent $PSScriptRoot
$Lock = Join-Path $env:TEMP "wasser-market-agent-auto-import.lock"
$Log = Join-Path $env:TEMP "wasser-market-agent-auto-import.log"
function Assert-NativeSuccess([string]$Message) {
    if ($LASTEXITCODE -ne 0) { throw "$Message (exit $LASTEXITCODE)" }
}

if (Test-Path -LiteralPath $Lock) { throw "Agent import is already running." }
Start-Transcript -Path $Log -Append | Out-Null
try {
    Set-Content -LiteralPath $Lock -Value $PID -Encoding ascii
    Set-Location $Repo
    foreach ($Tool in @($GitExe, $PythonExe, $NodeExe)) {
        if (-not (Test-Path -LiteralPath $Tool)) { throw "Required tool not found: $Tool" }
    }
    $Status = & $GitExe status --porcelain
    Assert-NativeSuccess "Cannot read Git status"
    if ($Status.Length -ne 0) { throw "Website repository has uncommitted changes." }
    & $GitExe checkout main
    Assert-NativeSuccess "Cannot check out main"
    & $GitExe pull --ff-only origin main
    Assert-NativeSuccess "Cannot update main"

    $Arguments = @("scripts/agent-auto-import.py", "--db", $Database, "--limit", $Limit)
    if ($ProductId -gt 0) { $Arguments += @("--ids", $ProductId) }
    if (-not $DryRun) { $Arguments += "--apply" }
    & $PythonExe @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Agent import validation failed." }
    if ($DryRun) { exit 0 }

    & $PythonExe -m json.tool data/products.json | Out-Null
    & $PythonExe -m json.tool data/brands.json | Out-Null
    & $PythonExe scripts/validate-agent-import.py
    & $NodeExe --check assets/app.js
    if ($LASTEXITCODE -ne 0) { throw "Generated site validation failed." }

    $Changed = & $GitExe status --porcelain
    if (-not $Changed) { Write-Host "No new PUBLISH_READY products."; exit 0 }
    & $GitExe add assets/app.js brands brands.html compare.html data index.html products products.html sitemap.xml scripts/agent-auto-import.py scripts/agent-auto-publish.ps1 scripts/validate-agent-import.py scripts/AGENT-AUTO-IMPORT.md
    $Count = (Get-Content data/agent-import-report.json -Raw | ConvertFrom-Json).accepted.Count
    & $GitExe commit -m "Auto-import $Count reviewed agent products"
    Assert-NativeSuccess "Cannot commit imported products"
    & $GitExe push origin main
    Assert-NativeSuccess "Cannot push imported products"
}
catch {
    Write-Error $_
    exit 1
}
finally {
    Remove-Item -LiteralPath $Lock -Force -ErrorAction SilentlyContinue
    Stop-Transcript | Out-Null
}
