@echo off
cd /d "%~dp0"
title REVIEW MAKER

:: Check if Python is installed
python -V >NUL 2>NUL
if errorlevel 1 (
    echo ERROR: Python not found. Please install it first.
    pause
    exit /b 1
)

:: Prompt user to decide if they want to use AI
choice /C YN /N /M "Do you want to use AI for review enhancement? Press Y for Yes, N for No."
if errorlevel 2 (
    echo User chose not to use AI. Running review generator without AI.
    python review_generator.py
) else (
    echo User chose to use AI. Running review generator with AI.
    python review_generator_ai.py
)

pause
exit
