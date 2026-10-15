# =============================================================================
#  package.ps1 - FarlandPort : build a PortMaster autoinstall zip
#  ASCII only (PowerShell 5.1 reads BOM-less .ps1 as ANSI)
#
#  usage:
#     .\package.ps1 -Port FarlandTactics3
#     .\package.ps1 -Port FarlandTactics4
#
#  Note: actual zip creation is done by tools\make_port_zip.py so that zip
#        entries always use '/' separators and UTF-8 names (7-Zip on Windows
#        writes '\' which breaks extraction on Linux).
# =============================================================================
param(
    [string]$Port = "FarlandTactics3",
    [string]$OutDir = "dist"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
$py   = "C:\Users\woo31\AppData\Local\Programs\Python\Python312\python.exe"
if (-not (Test-Path $py)) { $py = "python" }

$zipTool = Join-Path $root "tools\make_port_zip.py"
if (-not (Test-Path $zipTool)) { throw "not found: $zipTool" }

& $py $zipTool $root $Port $OutDir
if ($LASTEXITCODE -ne 0) { throw "zip build failed" }
