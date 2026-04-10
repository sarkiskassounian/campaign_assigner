@echo off
setlocal EnableDelayedExpansion

echo ============================================
echo   Campaign Assigner - Build Script
echo   Creates standalone .exe (no Python needed)
echo ============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is required to BUILD the .exe
    echo Please install Python from https://python.org
    echo.
    echo Once built, the .exe will work WITHOUT Python.
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
if exist .venv (
    echo      Virtual environment already exists, skipping...
) else (
    python -m venv .venv
)

echo [2/4] Activating virtual environment...
call .venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install --upgrade pip >nul 2>&1
pip install selenium pyinstaller

echo [4/4] Building executable...
echo.

REM Build single-file executable with console window
pyinstaller ^
    --onefile ^
    --console ^
    --name "CampaignAssigner" ^
    --icon NONE ^
    --add-data ".venv\Lib\site-packages\selenium\webdriver\common\selenium-manager;selenium\webdriver\common" ^
    campaign_assigner.py

echo.
echo ============================================
echo   BUILD COMPLETE!
echo ============================================
echo.
echo   Executable: dist\CampaignAssigner.exe
echo.
echo   This .exe includes:
echo   - Python runtime (bundled)
echo   - Selenium library (bundled)
echo   - ChromeDriver manager (bundled)
echo.
echo   Requirements for end users:
echo   - Google Chrome installed
echo   - NO Python needed!
echo.
echo ============================================
echo.

pause
