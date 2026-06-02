# Attach devflow to a consumer repository.
# Usage: .\installer\install.ps1 -TargetPath C:\path\to\your-app [-Agent cursor]

param(
    [Parameter(Mandatory = $true)]
    [string]$TargetPath,
    [ValidateSet("cursor")]
    [string]$Agent = "cursor"
)

$ErrorActionPreference = "Stop"

$FrameworkRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$TargetPath = (Resolve-Path $TargetPath).Path

function Copy-Tree {
    param([string]$Source, [string]$Dest)
    if (-not (Test-Path $Source)) { throw "Missing source: $Source" }
    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    Copy-Item -Path (Join-Path $Source "*") -Destination $Dest -Recurse -Force
}

Write-Host "Installing devflow into: $TargetPath"

# Framework core (canonical skills, templates, contracts, hooks)
Copy-Tree (Join-Path $FrameworkRoot "core") (Join-Path $TargetPath "core")
Copy-Tree (Join-Path $FrameworkRoot "adapters") (Join-Path $TargetPath "adapters")

# Consumer AI_CONTEXT
$aiContext = Join-Path $TargetPath "AI_CONTEXT"
New-Item -ItemType Directory -Force -Path $aiContext | Out-Null

$spec = Join-Path $aiContext "SPEC.md"
if (-not (Test-Path $spec)) {
    Copy-Item (Join-Path $FrameworkRoot "core\templates\SPEC.template.md") $spec
    Write-Host "Seeded AI_CONTEXT/SPEC.md from template"
}

$state = Join-Path $aiContext "PROJECT_STATE.md"
if (-not (Test-Path $state)) {
    Copy-Item (Join-Path $FrameworkRoot "core\templates\PROJECT_STATE.template.md") $state
    Write-Host "Seeded AI_CONTEXT/PROJECT_STATE.md from template"
}

if ($Agent -eq "cursor") {
    & (Join-Path $FrameworkRoot "installer\sync-cursor.ps1") -RepoRoot $TargetPath
}

Write-Host @"

Install complete.

Next steps:
  1. Edit AI_CONTEXT/SPEC.md for your product (or run /grillme in Cursor).
  2. Read core/AGENTS.md and adapters/$Agent/README.md.
  3. Follow Stage 1 -> 2 -> 3 workflow in the framework README.

"@
