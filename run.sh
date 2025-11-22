#!/bin/bash
# Activation script for Interview Practice System

# Navigate to project directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/bin/activate

# Run the application
python main.py

