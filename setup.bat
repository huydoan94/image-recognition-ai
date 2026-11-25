@echo off
title AI Product Recognition - Setup
cd /d "%~dp0"

echo ==========================================
echo      AI PRODUCT RECOGNITION - SETUP
echo ==========================================
echo.

where py >nul 2>nul
if errorlevel 1 (
    echo Python Launcher was not found.
    echo Install Python 3.11, 3.12 or 3.13 from https://www.python.org/downloads/
    echo During installation, tick "Add Python to PATH".
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    py -3.11 -m venv .venv
    if errorlevel 1 (
        echo Trying Python 3.12...
        py -3.12 -m venv .venv
    )
    if errorlevel 1 (
        echo Trying Python 3.13...
        py -3.13 -m venv .venv
    )
    if errorlevel 1 (
        echo Could not create the virtual environment.
        echo Install Python 3.11, 3.12 or 3.13 and try again.
        pause
        exit /b 1
    )
)

echo.
echo Upgrading pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto error

echo.
echo Installing project dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error

echo.
echo Setup complete! Now double-click run.bat or enter .\run.bat in VS Code terminal.
pause
exit /b 0

:error
echo.
echo Setup failed. Check the error above and see README.md for troubleshooting.
pause
exit /b 1
