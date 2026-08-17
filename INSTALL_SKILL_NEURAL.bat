@echo off
setlocal
cd /d "%~dp0"
python scripts\install_skill.py --source ".agents\skills\pocketmen-with-you" --profile neural
if errorlevel 1 (
  echo.
  echo [FAIL] PocketMen Neural skill installation failed.
  pause
  exit /b 1
)
echo.
echo [OK] PocketMen skill + Neural Local Studio dependencies installed.
echo The first neural creation will download FLUX.2-klein-4B into the Hugging Face cache.
pause
