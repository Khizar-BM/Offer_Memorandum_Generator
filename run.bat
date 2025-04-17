@echo off
echo Offer Memorandum Generator

:: Check if virtual environment exists and activate it
if exist .venv (
    echo Activating virtual environment...
    call .venv\Scripts\activate
) else (
    echo Virtual environment not found. Creating one...
    python -m venv .venv
    call .venv\Scripts\activate
    
    echo Installing dependencies...
    pip install -r requirements.txt
)

:: Run the Streamlit app
echo Starting Offer Memorandum Generator...
streamlit run app.py 