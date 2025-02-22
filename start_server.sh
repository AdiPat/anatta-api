#!/bin/bash

# Check if the virtual environment is already activated
if [ -z "$VIRTUAL_ENV" ]; then
    # Check if venv directory exists
    if [ ! -d "venv" ]; then
        echo "Virtual environment not found. Creating venv..."
        python3 -m venv venv
        source venv/bin/activate
        echo "Installing requirements..."
        pip install -r requirements.txt
    else
        echo "Virtual environment found. Activating venv..."
        source venv/bin/activate
    fi
else
    echo "Virtual environment is already activated."
fi

# Start the FastAPI server
python -m fastapi dev anatta/server.py