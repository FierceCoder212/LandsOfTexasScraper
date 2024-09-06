#!/bin/bash
git checkout main
git pull origin

# Step 1: Check if the virtual environment exists
if [[ ! -d "venv" ]]; then
    echo "Virtual environment not found. Creating a new one..."
    python -m venv venv
    echo "Virtual environment created."
fi

# Step 2: Activate the virtual environment
echo "Activating the virtual environment..."
source venv/Scripts/activate

# Step 3: Install dependencies from requirements.txt
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Step 4: Run the main Python script
echo "Running main.py..."
python Main.py
