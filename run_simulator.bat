@echo off
title Battle Simulator Launcher
echo.
echo ========================================
echo   Battle Simulator - Easy Launcher
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Using smart launcher with automatic dependency installation...
echo.
python launcher.py

echo.
echo Simulator closed. Press any key to exit...
pause >nul
