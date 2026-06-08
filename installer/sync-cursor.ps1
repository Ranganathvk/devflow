# Sync canonical core/ artifacts into .cursor/ for Cursor (derived mirror).
# Edit sources under core/ only — then run: .\installer\sync-cursor.ps1

param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

function Get-ContextDir {
    param([string]$Root)
    if ($env:DEVFLOW_CONTEXT_DIR) {
        return $env:DEVFLOW_CONTEXT_DIR.Trim()
    }
    $manifest = Join-Path $Root "devflow.context.yaml"
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

function Expand-ContextPaths {
    param([string]$Content, [string]$ContextDir)
    $text = $Content.Replace('@{context_dir}/', "@$ContextDir/")
    return $text.Replace('{context_dir}/', "$ContextDir/")
}

$ContextDir = Get-ContextDir -Root $RepoRoot

$coreAgents = Join-Path $RepoRoot "core\AGENTS.md"
$cursorAgents = Join-Path $RepoRoot ".cursor\AGENTS.md"
$coreSkills = Join-Path $RepoRoot "core\skills"
$cursorSkills = Join-Path $RepoRoot ".cursor\skills"

if (-not (Test-Path $coreAgents)) { throw "Missing $coreAgents" }
if (-not (Test-Path $coreSkills)) { throw "Missing $coreSkills" }

New-Item -ItemType Directory -Force -Path (Split-Path $cursorAgents) | Out-Null
$agentsText = Expand-ContextPaths -Content (Get-Content $coreAgents -Raw) -ContextDir $ContextDir
Set-Content -Path $cursorAgents -Value $agentsText -NoNewline
Write-Host "Synced core/AGENTS.md -> .cursor/AGENTS.md (context_dir: $ContextDir)"

New-Item -ItemType Directory -Force -Path $cursorSkills | Out-Null

$canonical = Get-ChildItem -Path $coreSkills -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName "SKILL.md")
}

$keep = @{}
foreach ($skill in $canonical) {
    $destDir = Join-Path $cursorSkills $skill.Name
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
    $skillPath = Join-Path $skill.FullName "SKILL.md"
    $skillText = Expand-ContextPaths -Content (Get-Content $skillPath -Raw) -ContextDir $ContextDir
    Set-Content -Path (Join-Path $destDir "SKILL.md") -Value $skillText -NoNewline
    $keep[$skill.Name] = $true
    Write-Host "Synced skill: $($skill.Name)"
}

# Remove stale top-level skills not in core/
Get-ChildItem -Path $cursorSkills -Directory | ForEach-Object {
    if (-not $keep.ContainsKey($_.Name)) {
        Remove-Item -Path $_.FullName -Recurse -Force
        Write-Host "Removed stale skill: $($_.Name)"
    }
}

# Remove accidental nested duplicates (e.g. .cursor/skills/foo/foo/)
Get-ChildItem -Path $cursorSkills -Directory | ForEach-Object {
    $nested = Join-Path $_.FullName $_.Name
    if (Test-Path $nested) {
        Remove-Item -Path $nested -Recurse -Force
        Write-Host "Removed nested duplicate: $nested"
    }
}

Write-Host "Done. Canonical sources: core/"
