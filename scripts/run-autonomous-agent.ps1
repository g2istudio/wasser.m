param(
    [switch]$Publish,
    [switch]$SkipDiscovery,
    [int]$SearchLimit = 10,
    [int]$DomainLimit = 3,
    [int]$PreflightLimit = 20,
    [int]$ExtractLimit = 5,
    [int]$PublishLimit = 10,
    [string]$AgentRoot = "C:\wasser-market-agent"
)

$ErrorActionPreference = "Stop"
$Python = Join-Path $AgentRoot ".venv\Scripts\python.exe"
$Pipeline = Join-Path $AgentRoot "run_pipeline.py"
$Log = Join-Path $env:TEMP "wasser-market-autonomous-pipeline.log"
$Lock = Join-Path $env:TEMP "wasser-market-autonomous-pipeline.lock"

if (Test-Path -LiteralPath $Lock) { throw "Autonomous pipeline is already running." }
Start-Transcript -Path $Log -Append | Out-Null
try {
    Set-Content -LiteralPath $Lock -Value $PID -Encoding ascii
    if (-not (Test-Path -LiteralPath $Python)) { throw "Python runtime not found: $Python" }
    if (-not (Test-Path -LiteralPath $Pipeline)) { throw "Pipeline not found: $Pipeline" }
    $Arguments = @(
        $Pipeline,
        "--query", "umkehrosmose system germany",
        "--country", "DE",
        "--language", "de",
        "--location", "Germany",
        "--search-limit", $SearchLimit,
        "--domain-limit", $DomainLimit,
        "--preflight-limit", $PreflightLimit,
        "--extract-limit", $ExtractLimit,
        "--publish-limit", $PublishLimit
    )
    if (-not $SkipDiscovery) { $Arguments += "--discover" }
    if ($Publish) { $Arguments += "--publish" }
    & $Python @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Autonomous pipeline failed with exit code $LASTEXITCODE" }
}
finally {
    Remove-Item -LiteralPath $Lock -Force -ErrorAction SilentlyContinue
    Stop-Transcript | Out-Null
}

