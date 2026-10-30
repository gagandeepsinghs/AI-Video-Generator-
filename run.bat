@echo off
title AI Property Video Generator

cd /d "%~dp0"

echo Starting AI Property Video Generator...
echo.

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m streamlit run app.py

pause
