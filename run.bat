@echo off
title AI Product Recognition
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Setup has not been completed yet.
    echo Run setup.bat first.
    pause
    exit /b 1
)

if not exist "runs\product_classifier\weights\best.pt" (
    echo No trained model was found.
    echo Collect photos with src\collect_data.py, then train with src\train_model.py.
    echo See README.md for the steps.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" src\recognize.py
if errorlevel 1 (
    echo.
    echo The app stopped because of an error. See the terminal message above.
    pause
)
