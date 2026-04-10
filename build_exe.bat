@echo off
echo ============================================
echo Building Windows Executable
echo ============================================

REM Create virtual environment
python -m venv .venv
call .venv\Scripts\activate

REM Install dependencies
pip install selenium pyinstaller

REM Build the executable
pyinstaller --onefile --name campaign_assigner browser_automation_windows.py

echo.
echo ============================================
echo Build complete!
echo Executable location: dist\campaign_assigner.exe
echo ============================================
pause
