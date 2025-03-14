#!/bin/bash

# Exit on error
set -e

# Variables
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
SETUP_PY="setup.py"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    echo "To install Python 3, run: sudo apt-get install python3"
    exit 1
fi

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv $VENV_DIR

# Activate the virtual environment
echo "Activating virtual environment..."
source $VENV_DIR/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r $REQUIREMENTS_FILE
else
    echo "Error: $REQUIREMENTS_FILE not found."
    exit 1
fi

# Run setup.py (if it exists)
if [ -f "$SETUP_PY" ]; then
    echo "Running setup.py..."
    python $SETUP_PY
else
    echo "No setup.py found. Skipping."
fi

echo "Setup complete! Virtual environment is ready to use."
echo "To activate the virtual environment, run: source $VENV_DIR/bin/activate"