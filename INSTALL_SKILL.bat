@echo off
setlocal
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File scripts\install_skill.ps1
pause
