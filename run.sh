#!/bin/bash

# Check if virtual environment exists and activate it
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "Virtual environment not found. Creating one..."
    python -m venv .venv
    source .venv/bin/activate
    
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the Streamlit app
echo "Starting Offer Memorandum Generator..."
streamlit run app.py 