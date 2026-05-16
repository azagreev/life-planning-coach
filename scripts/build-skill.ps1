#Requires -Version 5.1
<#
.SYNOPSIS
    Build script for the life-planning-coach skill artifact.
    Creates a ZIP archive of the skill folder per Anthropic's official requirements.
    https://support.claude.com/en/articles/12512180-use-skills-in-claude

    The ZIP must contain the skill folder at the root level, not just SKILL.md.
#>

[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

# ── Configuration ──────────────────────────────────────────────────────────────
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir '..') | Select-Object -ExpandProperty Path
$SkillMd     = Join-Path $ProjectRoot 'SKILL.md'
$BuildDir    = Join-Path $ProjectRoot '.build'
$SkillFolder = Join-Path $BuildDir 'life-planning-coach'
$OutputZip   = Join-Path $ProjectRoot 'life-planning-coach.zip'
$OutputSkill = Join-Path $ProjectRoot 'life-planning-coach.skill'

# ── 1. Validate source file exists ─────────────────────────────────────────────
if (-not (Test-Path -Path $SkillMd -PathType Leaf)) {
    Write-Error "SKILL.md not found at: $SkillMd"
    exit 1
}

# ── 2. Parse frontmatter ─────────────────────────────────────────────────────
$content = Get-Content -Raw -Path $SkillMd

$frontmatterMatch = [regex]::Match($content, '^---\r?\n(.*?)\r?\n---', [System.Text.RegularExpressions.RegexOptions]::Singleline)

if (-not $frontmatterMatch.Success) {
    Write-Error "SKILL.md is missing YAML frontmatter"
    exit 1
}

$frontmatter = $frontmatterMatch.Groups[1].Value

function Extract-Value {
    param([string]$Key, [string]$YamlBlock)
    $pattern = "^${Key}:\s*(?:['\"\"\"])?(.+?)(?:['\"\"\"])?\s*$"
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

# ── 4. Clean and create build directory ──────────────────────────────────────
if (Test-Path $BuildDir) {
    Remove-Item -Recurse -Force $BuildDir
}
New-Item -ItemType Directory -Path $SkillFolder -Force | Out-Null

# ── 5. Copy skill contents ───────────────────────────────────────────────────
Copy-Item -Path $SkillMd -Destination (Join-Path $SkillFolder 'SKILL.md')

$ReferencesDir = Join-Path $ProjectRoot 'references'
if (Test-Path $ReferencesDir -PathType Container) {
    Copy-Item -Recurse -Path $ReferencesDir -Destination (Join-Path $SkillFolder 'references')
}

$DashboardFile = Join-Path $ProjectRoot 'life-planning-dashboard.html'
if (Test-Path $DashboardFile -PathType Leaf) {
    Copy-Item -Path $DashboardFile -Destination (Join-Path $SkillFolder 'life-planning-dashboard.html')
}

# ── 6. Validate skill folder structure ───────────────────────────────────────
$BuiltSkillMd = Join-Path $SkillFolder 'SKILL.md'
if (-not (Test-Path $BuiltSkillMd -PathType Leaf)) {
    Write-Error "SKILL.md not found in build folder"
    exit 1
}

# ── 7. Create ZIP archive ────────────────────────────────────────────────────
if (Test-Path $OutputZip) {
    Remove-Item -Force $OutputZip
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($BuildDir, $OutputZip)

# ── 8. Also create .skill file (backward compatibility) ─────────────────────
Copy-Item -Path $SkillMd -Destination $OutputSkill -Force

# ── 9. Verify outputs ────────────────────────────────────────────────────────
if (-not (Test-Path $OutputZip -PathType Leaf)) {
    Write-Error "Failed to create $OutputZip"
    exit 1
}

$zipSize = (Get-Item $OutputZip).Length
$zipSizeMb = [math]::Round($zipSize / 1MB, 2)

# ── 10. Success ──────────────────────────────────────────────────────────────
Write-Host "Built life-planning-coach.zip (version $skillVersion, size: ${zipSizeMb} MB)"
Write-Host "Built life-planning-coach.skill (backward compatibility)"
Write-Host ""
Write-Host "Upload to Claude.ai:"
Write-Host "  1. Settings -> Capabilities -> enable 'Code execution and file creation'"
Write-Host "  2. Customize -> Skills -> '+' -> 'Upload a skill'"
Write-Host "  3. Select: $OutputZip"
