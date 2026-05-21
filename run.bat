@echo off
echo ============================================
echo   Offline Coding AI Assistant - Starting...
echo ============================================

REM Go to project root
cd /d "%~dp0"

REM Find Python
set "PY="
py --version >nul 2>nul
if not errorlevel 1 set "PY=py"
if not defined PY (
    python --version >nul 2>nul
    if not errorlevel 1 set "PY=python"
)
if not defined PY (
    echo [ERROR] Python not found. Install Python 3.10+ and add to PATH.
    pause
    exit /b 1
)
echo Found Python: %PY%

REM Check if dependencies are installed
%PY% -c "import numpy, pandas, matplotlib, cv2, pyperclip" >nul 2>nul
if errorlevel 1 (
    echo Installing dependencies first time, may take a minute...
    %PY% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b 1
    )
) else (
    echo Dependencies OK.
)

REM Train model if needed
if not exist "models\markov_model.json" (
    echo Training model first run only...
    %PY% train_model.py
)

REM Launch the assistant
echo Starting assistant...
echo.
%PY% main.py
pause
