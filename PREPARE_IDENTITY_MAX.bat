@echo off
setlocal
set "SKILL=%USERPROFILE%\.agents\skills\pocketmen-with-you"
if not exist "%SKILL%\SKILL.md" set "SKILL=%~dp0.agents\skills\pocketmen-with-you"
python "%SKILL%\scripts\setup_runtime.py" --skill-dir "%SKILL%" --profile identity-max --download-model
if errorlevel 1 (
  echo.
  echo [FAIL] Identity-Max engine preparation failed.
  pause
  exit /b 1
)
echo.
echo [OK] Qwen Image Edit 2511 Identity-Max backend is ready.
pause
