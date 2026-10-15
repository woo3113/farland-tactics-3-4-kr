# =============================================================================
#  stage_data.ps1 - copy your Farland Tactics 3/4 game files into the port data
#  folders so the ports are ready to test on the handheld.
#
#  ASCII only. Usage:
#     .\stage_data.ps1 -Game 3                 # FT3, korean voice only (skip CVJ/WVJ)
#     .\stage_data.ps1 -Game 3 -IncludeJpVoice # FT3 with japanese voice (bigger)
#     .\stage_data.ps1 -Game 4
#     .\stage_data.ps1 -Game all
# =============================================================================
param(
    [string]$Game = "3",
    [switch]$IncludeJpVoice,
    [string]$SourceRoot = "F:\DGGL\Games"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition

function Stage-FT3 {
    $src = Join-Path $SourceRoot "FT3_Win"
    $dst = Join-Path $root "portmaster\FarlandTactics3\farlandtactics3\data"
    if (-not (Test-Path $src)) { throw "source not found: $src" }
    Write-Host "FT3: $src -> $dst"
    $exclude = @()
    if (-not $IncludeJpVoice) { $exclude = @("CVJ", "WVJ", "FT3J.EXE", "_FT3_Jap_Voice.exe") }
    $xd = @()
    foreach ($e in $exclude) { $xd += "/XD"; $xd += (Join-Path $src $e) }
    # only files+dirs, skip DGGL metadata folder
    robocopy $src $dst /E /XF "*.bak" /XD (Join-Path $src "DosBox") @xd /NFL /NDL /NJH /NJS /NP | Out-Null
    Write-Host ("  FT3 staged (excluded: {0})" -f ($(if ($exclude) { $exclude -join ", " } else { "none" })))
}

function Stage-FT4 {
    $src = Join-Path $SourceRoot "FT4_Win"
    $dst = Join-Path $root "portmaster\FarlandTactics4\farlandtactics4\data"
    if (-not (Test-Path $src)) { throw "source not found: $src" }
    Write-Host "FT4: $src -> $dst"
    robocopy $src $dst /E /XF "*.bak" /XD (Join-Path $src "DosBox") /NFL /NDL /NJH /NJS /NP | Out-Null
    Write-Host "  FT4 staged"
}

switch ($Game.ToLower()) {
    "3"   { Stage-FT3 }
    "4"   { Stage-FT4 }
    "all" { Stage-FT3; Stage-FT4 }
    default { throw "Game must be 3, 4 or all" }
}

Write-Host ""
Write-Host "done. next: .\package.ps1 -Port FarlandTactics3   (data/ is not packaged)"
