# Sync canonical core/ artifacts into .cursor/ for Cursor (derived mirror).
# Edit sources under core/ only — then run: .\installer\sync-cursor.ps1

param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
)

$ErrorActionPreference = "Stop"

$coreAgents = Join-Path $RepoRoot "core\AGENTS.md"
$cursorAgents = Join-Path $RepoRoot ".cursor\AGENTS.md"
$coreSkills = Join-Path $RepoRoot "core\skills"
$cursorSkills = Join-Path $RepoRoot ".cursor\skills"

if (-not (Test-Path $coreAgents)) { throw "Missing $coreAgents" }
if (-not (Test-Path $coreSkills)) { throw "Missing $coreSkills" }

New-Item -ItemType Directory -Force -Path (Split-Path $cursorAgents) | Out-Null
Copy-Item -Path $coreAgents -Destination $cursorAgents -Force
Write-Host "Synced core/AGENTS.md -> .cursor/AGENTS.md"

New-Item -ItemType Directory -Force -Path $cursorSkills | Out-Null

$canonical = Get-ChildItem -Path $coreSkills -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName "SKILL.md")
}

$keep = @{}
foreach ($skill in $canonical) {
    $destDir = Join-Path $cursorSkills $skill.Name
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
    Copy-Item -Path (Join-Path $skill.FullName "SKILL.md") -Destination (Join-Path $destDir "SKILL.md") -Force
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
