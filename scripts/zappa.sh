#!/usr/bin/env bash

# Set the working directory
cd $CODEBUILD_SRC_DIR

# Create venv
virtualenv -p python3.6 venv

# Install requirement
venv/bin/pip install -r requirements.txt

# Get lambda python script
wget $SCRIPT_URL/scripts/zappa.py
chmod u+x zappa.py

# Run lambda python script
venv/bin/python zappa.py