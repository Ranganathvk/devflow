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

function Get-ContextDir {
    param([string]$RepoRoot)
    if ($env:DEVFLOW_CONTEXT_DIR) {
        return $env:DEVFLOW_CONTEXT_DIR.Trim()
    }
    $manifest = Join-Path $RepoRoot "devflow.context.yaml"
    if (Test-Path $manifest) {
        foreach ($line in Get-Content $manifest) {
            $trimmed = $line.Trim()
            if ($trimmed -match '^context_dir:\s*(.+)$') {
                return $Matches[1].Trim().Trim('"').Trim("'")
            }
        }
    }
    return "artifacts"
}

Write-Host "Installing devflow into: $TargetPath"

# Framework core (canonical skills, templates, contracts, hooks)
Copy-Tree (Join-Path $FrameworkRoot "core") (Join-Path $TargetPath "core")
Copy-Tree (Join-Path $FrameworkRoot "adapters") (Join-Path $TargetPath "adapters")

$ContextDir = Get-ContextDir -RepoRoot $TargetPath
$ContextRoot = Join-Path $TargetPath $ContextDir
New-Item -ItemType Directory -Force -Path $ContextRoot | Out-Null

$manifest = Join-Path $TargetPath "devflow.context.yaml"
if (-not (Test-Path $manifest)) {
    Copy-Item (Join-Path $FrameworkRoot "core\templates\devflow.context.template.yaml") $manifest
    Write-Host "Seeded devflow.context.yaml (context_dir: $ContextDir)"
}

$spec = Join-Path $ContextRoot "SPEC.md"
if (-not (Test-Path $spec)) {
    Copy-Item (Join-Path $FrameworkRoot "core\templates\SPEC.template.md") $spec
    Write-Host "Seeded $ContextDir/SPEC.md from template"
}

$state = Join-Path $ContextRoot "PROJECT_STATE.md"
if (-not (Test-Path $state)) {
    Copy-Item (Join-Path $FrameworkRoot "core\templates\PROJECT_STATE.template.md") $state
    Write-Host "Seeded $ContextDir/PROJECT_STATE.md from template"
}

if ($Agent -eq "cursor") {
    & (Join-Path $FrameworkRoot "installer\sync-cursor.ps1") -RepoRoot $TargetPath
}

Write-Host @"

Install complete.

Next steps:
  1. Edit $ContextDir/SPEC.md for your product (or run /grillme in Cursor).
  2. Read core/AGENTS.md and adapters/$Agent/README.md.
  3. Follow Stage 1 -> 2 -> 3 workflow in the framework README.

"@
