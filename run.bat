@echo off
setlocal EnableDelayedExpansion
echo ============================================
echo   Offline Coding AI Assistant - Starting...
echo ============================================

REM Determine project root from script location
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

REM Try to find Python: py, python, python3
set "PYTHON_CMD="

where py >nul 2>nul
if !errorlevel! equ 0 (
    py -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=py"
        goto :found_python
    )
)

where python >nul 2>nul
if !errorlevel! equ 0 (
    python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=python"
        goto :found_python
    )
)

where python3 >nul 2>nul
if !errorlevel! equ 0 (
    python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=python3"
        goto :found_python
    )
)

echo [ERROR] Could not find Python 3.10 or later.
echo.
echo Please install Python 3.10+ from https://www.python.org/downloads/
echo Make sure to check "Add Python to PATH" during installation.
pause
exit /b 1

:found_python
echo Found Python: %PYTHON_CMD%
%PYTHON_CMD% --version

REM Create virtual environment if it doesn't exist
if not exist ".venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv .venv
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
if !errorlevel! neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

REM Train model if it doesn't exist
if not exist "models\markov_model.json" (
    echo Training the AI model first run only...
    python train_model.py
    if !errorlevel! neq 0 (
        echo [ERROR] Model training failed.
        pause
        exit /b 1
    )
)

REM Launch the application
echo Starting the assistant...
echo.
cmd /k python main.py