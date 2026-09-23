param([string]$AgentRoot = "C:\wasser-market-agent")

$ErrorActionPreference = "Stop"
$Runtime = Join-Path $PSScriptRoot "agent-runtime"
foreach ($Directory in @("extractor", "crawler", "config")) {
    New-Item -ItemType Directory -Force -Path (Join-Path $AgentRoot $Directory) | Out-Null
}
Copy-Item -LiteralPath (Join-Path $Runtime "extractor\commerce_parser.py") -Destination (Join-Path $AgentRoot "extractor\commerce_parser.py") -Force
Copy-Item -LiteralPath (Join-Path $Runtime "extractor\validation.py") -Destination (Join-Path $AgentRoot "extractor\validation.py") -Force
Copy-Item -LiteralPath (Join-Path $Runtime "extractor\publication.py") -Destination (Join-Path $AgentRoot "extractor\publication.py") -Force
Copy-Item -LiteralPath (Join-Path $Runtime "crawler\worker.py") -Destination (Join-Path $AgentRoot "crawler\worker.py") -Force
Copy-Item -LiteralPath (Join-Path $Runtime "crawler\candidate_worker.py") -Destination (Join-Path $AgentRoot "crawler\candidate_worker.py") -Force
Copy-Item -LiteralPath (Join-Path $Runtime "run_pipeline.py") -Destination (Join-Path $AgentRoot "run_pipeline.py") -Force
Copy-Item -LiteralPath (Join-Path $Runtime "run_discovery.py") -Destination (Join-Path $AgentRoot "run_discovery.py") -Force
Copy-Item -LiteralPath (Join-Path $Runtime "config\official_brand_domains.json") -Destination (Join-Path $AgentRoot "config\official_brand_domains.json") -Force
Copy-Item -LiteralPath (Join-Path $Runtime "test_commerce_parser.py") -Destination (Join-Path $AgentRoot "test_commerce_parser.py") -Force
$Python = Join-Path $AgentRoot ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $Python) {
    & $Python -m pip install "pypdf>=5,<7"
    if ($LASTEXITCODE -ne 0) { throw "Could not install pypdf for official manual parsing" }
}
Write-Host "Autonomous agent runtime installed in $AgentRoot"
