@echo off
echo Starting Offer Memorandum Generator...
echo.

REM Check if virtual environment exists
if not exist .venv (
    echo ERROR: Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Starting the application...
streamlit run app.py

pause 