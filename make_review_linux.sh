#!/bin/bash

# Check if Python is installed
python3 -V &>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Python not found. Please install it first."
    exit 1
fi

# Prompt user to decide if they want to use AI
read -p "Do you want to use AI for review enhancement? (Y/N): " choice

if [[ "$choice" == [Yy]* ]]; then
    echo "User chose to use AI. Running review generator with AI."
    python3 review_generator_ai.py
else
    echo "User chose not to use AI. Running review generator without AI."
    python3 review_generator.py
fi
