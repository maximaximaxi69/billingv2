@echo off
setlocal
cd /d %~dp0\..
python scripts\build_windows_zip.py
if errorlevel 1 (
  echo Build failed.
  exit /b 1
)
echo Build completed.
