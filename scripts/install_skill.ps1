$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
python (Join-Path $PSScriptRoot "install_skill.py") --source (Join-Path $root ".agents\skills\pocketmen-with-you")
