param([string]$AgentRoot = "C:\wasser-market-agent")

$ErrorActionPreference = "Stop"
$Runtime = Join-Path $PSScriptRoot "agent-runtime"
foreach ($Directory in @("extractor", "crawler", "config", "database", "models", "sources")) {
    New-Item -ItemType Directory -Force -Path (Join-Path $AgentRoot $Directory) | Out-Null
}
foreach ($Directory in @("extractor", "crawler", "config", "database", "models", "sources")) {
    Copy-Item -Path (Join-Path $Runtime "$Directory\*") -Destination (Join-Path $AgentRoot $Directory) -Recurse -Force
}
foreach ($File in @("run_pipeline.py", "run_discovery.py", "wasser_agent.py", "runtime_control.py", "provenance.py", "semantic_resolution.py", "test_commerce_parser.py", "test_runtime_architecture.py")) {
    Copy-Item -LiteralPath (Join-Path $Runtime $File) -Destination (Join-Path $AgentRoot $File) -Force
}
if (-not (Test-Path -LiteralPath (Join-Path $AgentRoot ".env.example"))) {
    Copy-Item -LiteralPath (Join-Path $Runtime ".env.example") -Destination (Join-Path $AgentRoot ".env.example")
}
$Launcher = Join-Path $AgentRoot "wasser-agent.cmd"
Set-Content -LiteralPath $Launcher -Encoding ascii -Value '@echo off', '"%~dp0.venv\Scripts\python.exe" "%~dp0wasser_agent.py" %*'
$Python = Join-Path $AgentRoot ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $Python) {
    & $Python -m pip install "pypdf>=5,<7"
    if ($LASTEXITCODE -ne 0) { throw "Could not install pypdf for official manual parsing" }
}
Write-Host "Autonomous agent runtime installed in $AgentRoot"
