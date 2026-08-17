@echo off
setlocal
set "SKILL=%USERPROFILE%\.agents\skills\pocketmen-with-you"
if not exist "%SKILL%\SKILL.md" set "SKILL=%~dp0.agents\skills\pocketmen-with-you"
python "%SKILL%\scripts\setup_runtime.py" --skill-dir "%SKILL%" --profile neural --download-model
if errorlevel 1 (
  echo.
  echo [FAIL] Neural engine preparation failed.
  pause
  exit /b 1
)
echo.
echo [OK] PocketMen Neural Local Studio is ready and the default model is cached.
pause
