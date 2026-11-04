@echo off
chcp 65001 >nul
cd /d "%~dp0"
if exist "assets\SILK_PRINT_LOCKED.txt" (
  echo 【已锁定】丝印二维码 PNG 禁止覆盖。
  echo 若必须重印产品：python generate_qr_pngs.py --force
  echo.
  pause
  exit /b 2
)
python generate_qr_pngs.py
if errorlevel 1 pause
echo.
pause
