@echo off
setlocal
cd /d "%~dp0"
python -m pip install -e .[dev]
if errorlevel 1 goto :fail
ruff check .
if errorlevel 1 goto :fail
pytest -q
if errorlevel 1 goto :fail
echo.
echo PocketMen project checks passed.
pause
exit /b 0
:fail
echo.
echo Checks failed. Do not publish until fixed.
pause
exit /b 1
