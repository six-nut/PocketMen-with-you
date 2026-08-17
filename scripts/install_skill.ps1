$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command py -ErrorAction Stop }
& $python.Source (Join-Path $PSScriptRoot "install_skill.py") --source (Join-Path $root ".agents\skills\pocketmen-with-you")
