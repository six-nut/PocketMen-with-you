@echo off
setlocal
cd /d "%~dp0"
echo [PocketMen] Publishing/configuring six-nut/PocketMen-with-you v0.3.0 ...
python scripts\bootstrap_github.py --owner six-nut --repo PocketMen-with-you --public --confirm-public --release v0.3.0 --allow-existing
if errorlevel 1 (
  echo.
  echo Publication stopped safely. Read the message above, inspect any existing repository, and run again only when safe.
  pause
  exit /b 1
)
echo.
echo Done. Remember to upload assets\social-preview.png in GitHub Settings ^> Social preview if needed.
pause
