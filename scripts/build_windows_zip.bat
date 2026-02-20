@echo off
setlocal
cd /d %~dp0\..

echo [NC] Starting Windows ZIP build...
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 scripts\build_windows_zip.py
) else (
  python scripts\build_windows_zip.py
)

if errorlevel 1 (
  echo.
  echo [NC] Build failed. Please read the error above.
  pause
  exit /b 1
)

echo.
echo [NC] Build completed successfully.
echo [NC] ZIP: dist\NCInvoiceManager-windows.zip
pause
