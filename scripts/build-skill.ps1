#Requires -Version 5.1
<#
.SYNOPSIS
    Build script for the life-planning-coach.skill artifact.
    A .skill file is a renamed Markdown file with YAML frontmatter metadata.
#>

[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

# ── Configuration ──────────────────────────────────────────────────────────────
$ScriptDir  = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir '..') | Select-Object -ExpandProperty Path
$SkillMd     = Join-Path $ProjectRoot 'SKILL.md'
$OutputFile  = Join-Path $ProjectRoot 'life-planning-coach.skill'

# ── 1. Validate source file exists ─────────────────────────────────────────────
if (-not (Test-Path -Path $SkillMd -PathType Leaf)) {
    Write-Error "SKILL.md not found at: $SkillMd"
    exit 1
}

# ── 2. Parse frontmatter ─────────────────────────────────────────────────────
$content = Get-Content -Raw -Path $SkillMd

# Extract the YAML frontmatter block (content between the first two '---' lines)
$frontmatterMatch = [regex]::Match($content, '^---\r?\n(.*?)\r?\n---', [System.Text.RegularExpressions.RegexOptions]::Singleline)

if (-not $frontmatterMatch.Success) {
    Write-Error "SKILL.md is missing YAML frontmatter"
    exit 1
}

$frontmatter = $frontmatterMatch.Groups[1].Value

# Helper: extract a YAML key's value (handles quoted and unquoted values)
function Extract-Value {
    param([string]$Key, [string]$YamlBlock)
    $pattern = "^${Key}:\s*(?:['""""])?(.+?)(?:['""""])?\s*$"
    $match = [regex]::Match($YamlBlock, $pattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)
    if ($match.Success) {
        return $match.Groups[1].Value.Trim()
    }
    return $null
}

$skillName     = Extract-Value -Key 'name'        -YamlBlock $frontmatter
$skillVersion  = Extract-Value -Key 'version'     -YamlBlock $frontmatter
$requiresMcp   = Extract-Value -Key 'requires_mcp' -YamlBlock $frontmatter

# ── 3. Validate required frontmatter fields ──────────────────────────────────
$errors = 0

if ([string]::IsNullOrWhiteSpace($skillName)) {
    Write-Error "Frontmatter is missing required field 'name'"
    $errors++
}

if ([string]::IsNullOrWhiteSpace($skillVersion)) {
    Write-Error "Frontmatter is missing required field 'version'"
    $errors++
}

if ([string]::IsNullOrWhiteSpace($requiresMcp)) {
    Write-Error "Frontmatter is missing required field 'requires_mcp'"
    $errors++
}

if ($errors -gt 0) {
    exit 1
}

# ── 4. Build the artifact ────────────────────────────────────────────────────
Copy-Item -Path $SkillMd -Destination $OutputFile -Force

# ── 5. Verify output ─────────────────────────────────────────────────────────
if (-not (Test-Path -Path $OutputFile -PathType Leaf)) {
    Write-Error "Failed to create $OutputFile"
    exit 1
}

# ── 6. Success ───────────────────────────────────────────────────────────────
Write-Host "Built life-planning-coach.skill (version $skillVersion)"
