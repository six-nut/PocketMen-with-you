@echo off
setlocal
cd /d "%~dp0"
echo [PocketMen] Publishing six-nut/PocketMen-with-you ...
python scripts\bootstrap_github.py --owner six-nut --repo PocketMen-with-you --public --confirm-public --release v0.1.0
if errorlevel 1 (
  echo.
  echo Publication stopped safely. Read the message above, fix the prerequisite, and run again.
  pause
  exit /b 1
)
echo.
echo Done. Remember to upload assets\social-preview.png in GitHub Settings ^> Social preview.
pause
